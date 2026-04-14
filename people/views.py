# Person-related views migrated from movies/views.py
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from .models import Person
from .serializers import PersonSerializer

class PersonList(generics.ListCreateAPIView):
	def get_permissions(self):
		from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
		if self.request.method == 'GET':
			return [AllowAny()]
		elif self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
			return [IsAdminUser()]
		return [IsAuthenticated()]
	serializer_class = PersonSerializer

	def get_queryset(self):
		return Person.nodes.all()

class PersonDetail(generics.RetrieveUpdateDestroyAPIView):
	def get_permissions(self):
		from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
		if self.request.method == 'GET':
			return [AllowAny()]
		elif self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
			return [IsAdminUser()]
		return [IsAuthenticated()]
	serializer_class = PersonSerializer
	def get_queryset(self):
		return Person.nodes.all()

from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from django.http import HttpResponse
import json, csv, io

@api_view(['GET'])
@permission_classes([AllowAny])
def search_people(request):
	q = request.GET.get('q', '')
	results = []
	if q:
		results = [
			{'uid': p.uid, 'name': p.name, 'bio': p.bio}
			for p in Person.nodes.filter(is_active=1) if q.lower() in p.name.lower()
		]
	else:
		results = [
			{'uid': p.uid, 'name': p.name, 'bio': p.bio}
			for p in Person.nodes.filter(is_active=1)
		]
	return Response({'results': results})

@api_view(['POST'])
@permission_classes([IsAdminUser])
def soft_delete_person(request, uid):
	person = Person.nodes.get_or_none(uid=uid)
	if not person:
		return Response({'error': 'Person not found.'}, status=404)
	person.is_active = 0
	person.save()
	return Response({'status': 'Person soft deleted.'})

@api_view(['POST'])
@permission_classes([IsAdminUser])
def restore_person(request, uid):
	person = Person.nodes.get_or_none(uid=uid)
	if not person:
		return Response({'error': 'Person not found.'}, status=404)
	person.is_active = 1
	person.save()
	return Response({'status': 'Person restored.'})

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
