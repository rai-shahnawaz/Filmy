# Admin endpoints to toggle featured/pinned status
@api_view(['POST'])
@permission_classes([IsAdminUser])
def toggle_featured_status(request):
	object_type = request.data.get('object_type')
	object_uid = request.data.get('object_uid')
	if not all([object_type, object_uid]):
		return Response({'error': 'Missing required fields.'}, status=400)
	obj = None
	if object_type == 'film':
		obj = Film.nodes.get_or_none(uid=object_uid)
	elif object_type == 'series':
		obj = Series.nodes.get_or_none(uid=object_uid)
	elif object_type == 'person':
		obj = Person.nodes.get_or_none(uid=object_uid)
	elif object_type == 'episode':
		obj = Episode.nodes.get_or_none(uid=object_uid)
	if not obj:
		return Response({'error': f'{object_type.title()} not found.'}, status=404)
	obj.is_featured = 0 if getattr(obj, 'is_featured', 0) else 1
	obj.save()
	log_audit(request, 'update', obj, object_type.title(), f'Toggled featured to {obj.is_featured}')
	return Response({'status': f'Featured status set to {obj.is_featured}.'})
# Admin notes/comments endpoints
from .adminnotes import AdminNote
@api_view(['POST'])
@permission_classes([IsAdminUser])
def add_admin_note(request):
	object_type = request.data.get('object_type')
	object_uid = request.data.get('object_uid')
	note = request.data.get('note')
	user = request.user
	if not all([object_type, object_uid, note]):
		return Response({'error': 'Missing required fields.'}, status=400)
	admin_note = AdminNote(
		object_type=object_type,
		object_uid=object_uid,
		user_id=str(user.id),
		note=note
	).save()
	log_audit(request, 'update', admin_note, 'AdminNote', 'Added note')
	return Response({'status': 'Note added.'})

@api_view(['GET'])
@permission_classes([IsAdminUser])
def list_admin_notes(request):
	object_type = request.GET.get('object_type')
	object_uid = request.GET.get('object_uid')
	if not all([object_type, object_uid]):
		return Response({'error': 'Missing required fields.'}, status=400)
	notes = AdminNote.nodes.filter(object_type=object_type, object_uid=object_uid)
	data = [
		{
			'note': n.note,
			'user_id': n.user_id,
			'created_at': n.created_at,
		} for n in notes
	]
	return Response({'notes': data})
# Admin dashboard analytics endpoint
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model

@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_dashboard_analytics(request):
	# Counts
	film_count = Film.nodes.filter(is_active=1).count()
	series_count = Series.nodes.filter(is_active=1).count()
	person_count = Person.nodes.filter(is_active=1).count()
	# Recent changes (last 7 days)
	week_ago = timezone.now() - timedelta(days=7)
	from .auditlog import AuditLog
	recent_logs = AuditLog.objects.filter(timestamp__gte=week_ago).order_by('-timestamp')[:20]
	recent_changes = [
		{
			'timestamp': log.timestamp,
			'user': str(log.user),
			'action': log.action,
			'object_type': log.object_type,
			'object_uid': log.object_uid,
			'details': log.details,
		}
		for log in recent_logs
	]
	# Top contributors (by action count)
	User = get_user_model()
	top_users = (
		AuditLog.objects.values('user')
		.exclude(user=None)
		.annotate(count=models.Count('id'))
		.order_by('-count')[:5]
	)
	user_map = {u.id: str(u) for u in User.objects.filter(id__in=[x['user'] for x in top_users])}
	top_contributors = [
		{'user': user_map.get(x['user'], 'Unknown'), 'count': x['count']} for x in top_users
	]
	return Response({
		'film_count': film_count,
		'series_count': series_count,
		'person_count': person_count,
		'recent_changes': recent_changes,
		'top_contributors': top_contributors,
	})
# Admin endpoints to manage relationships (assign/remove people to films, series, episodes)
@api_view(['POST'])
@permission_classes([IsAdminUser])
def assign_person_to_object(request):
	"""
	POST data: {
		'object_type': 'film'|'series'|'episode',
		'object_uid': '...',
		'person_uid': '...',
		'role': 'actor'|'director'|'producer'|'creator'|'crew'
	}
	"""
	object_type = request.data.get('object_type')
	object_uid = request.data.get('object_uid')
	person_uid = request.data.get('person_uid')
	role = request.data.get('role')
	if not all([object_type, object_uid, person_uid, role]):
		return Response({'error': 'Missing required fields.'}, status=400)
	# Get objects
	person = Person.nodes.get_or_none(uid=person_uid)
	if not person:
		return Response({'error': 'Person not found.'}, status=404)
	obj = None
	if object_type == 'film':
		obj = Film.nodes.get_or_none(uid=object_uid)
	elif object_type == 'series':
		obj = Series.nodes.get_or_none(uid=object_uid)
	elif object_type == 'episode':
		obj = Episode.nodes.get_or_none(uid=object_uid)
	if not obj:
		return Response({'error': f'{object_type.title()} not found.'}, status=404)
	# Assign relationship
	rel_map = {
		'actor': 'actors',
		'director': 'directors',
		'producer': 'producers',
		'creator': 'creators',
		'crew': 'crew',
	}
	rel = rel_map.get(role)
	if not rel or not hasattr(obj, rel):
		return Response({'error': 'Invalid role.'}, status=400)
	getattr(obj, rel).connect(person)
	obj.save()
	log_audit(request, 'update', obj, object_type.title(), f'Assigned {role} {person_uid}')
	return Response({'status': f'{role.title()} assigned.'})

@api_view(['POST'])
@permission_classes([IsAdminUser])
def remove_person_from_object(request):
	"""
	POST data: {
		'object_type': 'film'|'series'|'episode',
		'object_uid': '...',
		'person_uid': '...',
		'role': 'actor'|'director'|'producer'|'creator'|'crew'
	}
	"""
	object_type = request.data.get('object_type')
	object_uid = request.data.get('object_uid')
	person_uid = request.data.get('person_uid')
	role = request.data.get('role')
	if not all([object_type, object_uid, person_uid, role]):
		return Response({'error': 'Missing required fields.'}, status=400)
	# Get objects
	person = Person.nodes.get_or_none(uid=person_uid)
	if not person:
		return Response({'error': 'Person not found.'}, status=404)
	obj = None
	if object_type == 'film':
		obj = Film.nodes.get_or_none(uid=object_uid)
	elif object_type == 'series':
		obj = Series.nodes.get_or_none(uid=object_uid)
	elif object_type == 'episode':
		obj = Episode.nodes.get_or_none(uid=object_uid)
	if not obj:
		return Response({'error': f'{object_type.title()} not found.'}, status=404)
	# Remove relationship
	rel_map = {
		'actor': 'actors',
		'director': 'directors',
		'producer': 'producers',
		'creator': 'creators',
		'crew': 'crew',
	}
	rel = rel_map.get(role)
	if not rel or not hasattr(obj, rel):
		return Response({'error': 'Invalid role.'}, status=400)
	getattr(obj, rel).disconnect(person)
	obj.save()
	log_audit(request, 'update', obj, object_type.title(), f'Removed {role} {person_uid}')
	return Response({'status': f'{role.title()} removed.'})
from .auditlog import AuditLog
from django.contrib.auth import get_user
# Utility to log admin actions
def log_audit(request, action, obj, obj_type, details=None):
	user = get_user(request)
	AuditLog.objects.create(
		user=user if user.is_authenticated else None,
		action=action,
		object_type=obj_type,
		object_uid=getattr(obj, 'uid', ''),
		object_repr=str(obj),
		details=details or ''
	)
# Soft delete/restore endpoints (admin only)
@api_view(['POST'])
@permission_classes([IsAdminUser])
def soft_delete_film(request, uid):
	film = Film.nodes.get_or_none(uid=uid)
	if not film:
		return Response({'error': 'Film not found.'}, status=404)
	film.is_active = 0
	film.save()
	log_audit(request, 'delete', film, 'Film')
	return Response({'status': 'Film soft deleted.'})

@api_view(['POST'])
@permission_classes([IsAdminUser])
def restore_film(request, uid):
	film = Film.nodes.get_or_none(uid=uid)
	if not film:
		return Response({'error': 'Film not found.'}, status=404)
	film.is_active = 1
	film.save()
	log_audit(request, 'restore', film, 'Film')
	return Response({'status': 'Film restored.'})

@api_view(['POST'])
@permission_classes([IsAdminUser])
def soft_delete_series(request, uid):
	series = Series.nodes.get_or_none(uid=uid)
	if not series:
		return Response({'error': 'Series not found.'}, status=404)
	series.is_active = 0
	series.save()
	log_audit(request, 'delete', series, 'Series')
	return Response({'status': 'Series soft deleted.'})

@api_view(['POST'])
@permission_classes([IsAdminUser])
def restore_series(request, uid):
	series = Series.nodes.get_or_none(uid=uid)
	if not series:
		return Response({'error': 'Series not found.'}, status=404)
	series.is_active = 1
	series.save()
	log_audit(request, 'restore', series, 'Series')
	return Response({'status': 'Series restored.'})

@api_view(['POST'])
@permission_classes([IsAdminUser])
def soft_delete_person(request, uid):
	person = Person.nodes.get_or_none(uid=uid)
	if not person:
		return Response({'error': 'Person not found.'}, status=404)
	person.is_active = 0
	person.save()
	log_audit(request, 'delete', person, 'Person')
	return Response({'status': 'Person soft deleted.'})

@api_view(['POST'])
@permission_classes([IsAdminUser])
def restore_person(request, uid):
	person = Person.nodes.get_or_none(uid=uid)
	if not person:
		return Response({'error': 'Person not found.'}, status=404)
	person.is_active = 1
	person.save()
	log_audit(request, 'restore', person, 'Person')
	return Response({'status': 'Person restored.'})

@api_view(['POST'])
@permission_classes([IsAdminUser])
def soft_delete_episode(request, uid):
	episode = Episode.nodes.get_or_none(uid=uid)
	if not episode:
		return Response({'error': 'Episode not found.'}, status=404)
	episode.is_active = 0
	episode.save()
	return Response({'status': 'Episode soft deleted.'})

@api_view(['POST'])
@permission_classes([IsAdminUser])
def restore_episode(request, uid):
	episode = Episode.nodes.get_or_none(uid=uid)
	if not episode:
		return Response({'error': 'Episode not found.'}, status=404)
	episode.is_active = 1
	episode.save()
	return Response({'status': 'Episode restored.'})
import csv
import io
import json
from rest_framework.parsers import MultiPartParser, FormParser
# Bulk import/export endpoints (admin only)
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAdminUser
from django.http import HttpResponse

@api_view(['GET'])
@permission_classes([IsAdminUser])
def export_films_json(request):
	films = Film.nodes.filter(is_active=1)
	data = [film.__properties__ for film in films]
	return HttpResponse(json.dumps(data, default=str), content_type='application/json')

@api_view(['POST'])
@permission_classes([IsAdminUser])
@parser_classes([MultiPartParser, FormParser])
def import_films_json(request):
	file = request.FILES.get('file')
	if not file:
		return Response({'error': 'No file uploaded.'}, status=400)
	data = json.load(file)
	for entry in data:
		Film(**entry).save()
	return Response({'status': 'Import complete.'})

@api_view(['GET'])
@permission_classes([IsAdminUser])
def export_films_csv(request):
	films = Film.nodes.filter(is_active=1)
	if not films:
		return HttpResponse('', content_type='text/csv')
	output = io.StringIO()
	writer = csv.DictWriter(output, fieldnames=films[0].__properties__.keys())
	writer.writeheader()
	for film in films:
		writer.writerow(film.__properties__)
	return HttpResponse(output.getvalue(), content_type='text/csv')

@api_view(['POST'])
@permission_classes([IsAdminUser])
@parser_classes([MultiPartParser, FormParser])
def import_films_csv(request):
	file = request.FILES.get('file')
	if not file:
		return Response({'error': 'No file uploaded.'}, status=400)
	decoded = file.read().decode('utf-8')
	reader = csv.DictReader(io.StringIO(decoded))
	for row in reader:
		Film(**row).save()
	return Response({'status': 'Import complete.'})

# Repeat for Series and Person (JSON/CSV)
@api_view(['GET'])
@permission_classes([IsAdminUser])
def export_series_json(request):
	series = Series.nodes.filter(is_active=1)
	data = [s.__properties__ for s in series]
	return HttpResponse(json.dumps(data, default=str), content_type='application/json')

@api_view(['POST'])
@permission_classes([IsAdminUser])
@parser_classes([MultiPartParser, FormParser])
def import_series_json(request):
	file = request.FILES.get('file')
	if not file:
		return Response({'error': 'No file uploaded.'}, status=400)
	data = json.load(file)
	for entry in data:
		Series(**entry).save()
	return Response({'status': 'Import complete.'})

@api_view(['GET'])
@permission_classes([IsAdminUser])
def export_series_csv(request):
	series = Series.nodes.filter(is_active=1)
	if not series:
		return HttpResponse('', content_type='text/csv')
	output = io.StringIO()
	writer = csv.DictWriter(output, fieldnames=series[0].__properties__.keys())
	writer.writeheader()
	for s in series:
		writer.writerow(s.__properties__)
	return HttpResponse(output.getvalue(), content_type='text/csv')

@api_view(['POST'])
@permission_classes([IsAdminUser])
@parser_classes([MultiPartParser, FormParser])
def import_series_csv(request):
	file = request.FILES.get('file')
	if not file:
		return Response({'error': 'No file uploaded.'}, status=400)
	decoded = file.read().decode('utf-8')
	reader = csv.DictReader(io.StringIO(decoded))
	for row in reader:
		Series(**row).save()
	return Response({'status': 'Import complete.'})

@api_view(['GET'])
@permission_classes([IsAdminUser])
def export_people_json(request):
	people = Person.nodes.filter(is_active=1)
	data = [p.__properties__ for p in people]
	return HttpResponse(json.dumps(data, default=str), content_type='application/json')

@api_view(['POST'])
@permission_classes([IsAdminUser])
@parser_classes([MultiPartParser, FormParser])
def import_people_json(request):
	file = request.FILES.get('file')
	if not file:
		return Response({'error': 'No file uploaded.'}, status=400)
	data = json.load(file)
	for entry in data:
		Person(**entry).save()
	return Response({'status': 'Import complete.'})

@api_view(['GET'])
@permission_classes([IsAdminUser])
def export_people_csv(request):
	people = Person.nodes.filter(is_active=1)
	if not people:
		return HttpResponse('', content_type='text/csv')
	output = io.StringIO()
	writer = csv.DictWriter(output, fieldnames=people[0].__properties__.keys())
	writer.writeheader()
	for p in people:
		writer.writerow(p.__properties__)
	return HttpResponse(output.getvalue(), content_type='text/csv')

@api_view(['POST'])
@permission_classes([IsAdminUser])
@parser_classes([MultiPartParser, FormParser])
def import_people_csv(request):
	file = request.FILES.get('file')
	if not file:
		return Response({'error': 'No file uploaded.'}, status=400)
	decoded = file.read().decode('utf-8')
	reader = csv.DictReader(io.StringIO(decoded))
	for row in reader:
		Person(**row).save()
	return Response({'status': 'Import complete.'})
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
# Admin login view (HTML form)
class AdminLoginView(APIView):
	renderer_classes = [TemplateHTMLRenderer]
	template_name = 'admin_login.html'
	permission_classes = []

	def get(self, request):
		return Response({})

	def post(self, request):
		username = request.data.get('username')
		password = request.data.get('password')
		user = authenticate(request, username=username, password=password)
		if user is not None and user.is_staff:
			login(request, user)
			return redirect('admin_dashboard')
		return Response({'error': 'Invalid credentials or not an admin.'}, status=401)

# Admin dashboard view (HTML, protected)
@method_decorator(user_passes_test(lambda u: u.is_staff), name='dispatch')
class AdminDashboardView(APIView):
	renderer_classes = [TemplateHTMLRenderer]
	template_name = 'admin_dashboard.html'
	permission_classes = [IsAuthenticated]

	def get(self, request):
		# Example: show counts of objects, links to add/edit
		film_count = Film.nodes.count()
		series_count = Series.nodes.count()
		person_count = Person.nodes.count()
		return Response({
			'film_count': film_count,
			'series_count': series_count,
			'person_count': person_count,
		})
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from .serializers import FilmSerializer, GenreSerializer, SeriesSerializer, SeasonSerializer, EpisodeSerializer, PersonSerializer
from .neomodels import Film, Genre, Series, Season, Episode, Person

class FilmList(generics.ListCreateAPIView):
	permission_classes = (IsAuthenticated,)
	def get_permissions(self):
		if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
			return [IsAdminUser()]
		return [IsAuthenticated()]
	queryset = Film.nodes.all()
	serializer_class = FilmSerializer

class SeriesList(generics.ListCreateAPIView):
	permission_classes = (IsAuthenticated,)
	def get_permissions(self):
		if self.request.method in ['PUT', 'PATCH', 'DELETE']:
			return [IsAdminUser()]
		return [IsAuthenticated()]
	queryset = Series.nodes.all()
	serializer_class = SeriesSerializer

class SeriesDetail(generics.RetrieveUpdateDestroyAPIView):
	permission_classes = (IsAuthenticated,)
	def get_permissions(self):
		if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
			return [IsAdminUser()]
		return [IsAuthenticated()]
	serializer_class = SeriesSerializer
	def get_queryset(self):
		return Series.nodes.all()

class SeasonList(generics.ListCreateAPIView):
	permission_classes = (IsAuthenticated,)
	def get_permissions(self):
		if self.request.method in ['PUT', 'PATCH', 'DELETE']:
			return [IsAdminUser()]
		return [IsAuthenticated()]
	queryset = Season.nodes.all()
	serializer_class = SeasonSerializer

class SeasonDetail(generics.RetrieveUpdateDestroyAPIView):
	permission_classes = (IsAuthenticated,)
	def get_permissions(self):
		if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
			return [IsAdminUser()]
		return [IsAuthenticated()]
	serializer_class = SeasonSerializer
	def get_queryset(self):
		return Season.nodes.all()

class EpisodeList(generics.ListCreateAPIView):
	permission_classes = (IsAuthenticated,)
	def get_permissions(self):
		if self.request.method in ['PUT', 'PATCH', 'DELETE']:
			return [IsAdminUser()]
		return [IsAuthenticated()]
	queryset = Episode.nodes.all()
	serializer_class = EpisodeSerializer

class EpisodeDetail(generics.RetrieveUpdateDestroyAPIView):
	permission_classes = (IsAuthenticated,)
	def get_permissions(self):
		if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
			return [IsAdminUser()]
		return [IsAuthenticated()]
	serializer_class = EpisodeSerializer
	def get_queryset(self):
		return Episode.nodes.all()

class PersonList(generics.ListCreateAPIView):
	permission_classes = (IsAuthenticated,)
	def get_permissions(self):
		if self.request.method in ['PUT', 'PATCH', 'DELETE']:
			return [IsAdminUser()]
		return [IsAuthenticated()]
	queryset = Person.nodes.all()
	serializer_class = PersonSerializer

class PersonDetail(generics.RetrieveUpdateDestroyAPIView):
	permission_classes = (IsAuthenticated,)
	def get_permissions(self):
		if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
			return [IsAdminUser()]
		return [IsAuthenticated()]
	serializer_class = PersonSerializer
	def get_queryset(self):
		return Person.nodes.all()

class FilmDetail(generics.RetrieveUpdateDestroyAPIView):
	permission_classes = (IsAuthenticated,)
	def get_permissions(self):
		if self.request.method in ['PUT', 'PATCH', 'DELETE']:
			return [IsAdminUser()]
		return [IsAuthenticated()]
	serializer_class = FilmSerializer

	def get_queryset(self):
		return Film.nodes.all()

class GenreList(generics.ListCreateAPIView):
	permission_classes = (IsAuthenticated,)
	queryset = Genre.nodes.all()
	serializer_class = GenreSerializer

class SubGenreList(generics.ListCreateAPIView):
	permission_classes = (IsAuthenticated,)
	queryset = SubGenre.nodes.all()
	serializer_class = SubGenreSerializer

class BadgeList(generics.ListCreateAPIView):
	permission_classes = (IsAuthenticated,)
	queryset = Badge.nodes.all()
	serializer_class = BadgeSerializer
