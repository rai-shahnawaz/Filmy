from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .neomodels import MovieList


# User-facing endpoints for personal lists
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_personal_list(request):
	name = request.data.get('name')
	description = request.data.get('description', '')
	films_titles = request.data.get('films', [])
	user_id = str(request.user.id)
	if not name:
		return Response({'error': 'Name is required.'}, status=400)
	movie_list = MovieList(name=name, description=description, status='pending').save()
	for title in films_titles:
		film = Film.nodes.get_or_none(title=title)
		if film:
			movie_list.films.connect(film)
	# Optionally, connect list to user (if you add a user field)
	return Response({'status': 'List created and submitted for approval.'})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_personal_list(request):
	uid = request.data.get('uid')
	name = request.data.get('name')
	description = request.data.get('description', '')
	films_titles = request.data.get('films', [])
	if not uid:
		return Response({'error': 'List uid is required.'}, status=400)
	movie_list = MovieList.nodes.get_or_none(uid=uid)
	if not movie_list:
		return Response({'error': 'List not found.'}, status=404)
	if name:
		movie_list.name = name
	movie_list.description = description
	# Remove all films and re-add
	for film in list(movie_list.films):
		movie_list.films.disconnect(film)
	for title in films_titles:
		film = Film.nodes.get_or_none(title=title)
		if film:
			movie_list.films.connect(film)
	movie_list.save()
	return Response({'status': 'List updated.'})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete_personal_list(request):
	uid = request.data.get('uid')
	if not uid:
		return Response({'error': 'List uid is required.'}, status=400)
	movie_list = MovieList.nodes.get_or_none(uid=uid)
	if not movie_list:
		return Response({'error': 'List not found.'}, status=404)
	movie_list.delete()
	return Response({'status': 'List deleted.'})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_personal_lists(request):
	# Optionally, filter by user if you add a user field
	lists = MovieList.nodes.filter(status='approved')
	data = [
		{'uid': l.uid, 'name': l.name, 'description': l.description, 'films': [f.title for f in l.films]}
		for l in lists
	]
	return Response({'lists': data})
from django.shortcuts import render

# Create your views here.
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .neomodels import MovieList

from .serializers import MovieListSerializer

class MovieListListCreateView(generics.ListCreateAPIView):
	def get_permissions(self):
		from rest_framework.permissions import AllowAny, IsAuthenticated
		if self.request.method == 'GET':
			return [AllowAny()]
		return [IsAuthenticated()]
	serializer_class = MovieListSerializer

	def get_queryset(self):
		return MovieList.nodes.all()

	def perform_create(self, serializer):
		name = serializer.validated_data['name']
		description = serializer.validated_data.get('description', '')
		films_titles = serializer.validated_data.get('films', [])
		movie_list = MovieList(name=name, description=description).save()
		for title in films_titles:
			film = Film.nodes.get_or_none(title=title)
			if film:
				movie_list.films.connect(film)
		return movie_list

class MovieListDetailView(generics.RetrieveUpdateDestroyAPIView):
	def get_permissions(self):
		from rest_framework.permissions import AllowAny, IsAuthenticated
		if self.request.method == 'GET':
			return [AllowAny()]
		return [IsAuthenticated()]
	serializer_class = MovieListSerializer

	def get_queryset(self):
		return MovieList.nodes.all()
