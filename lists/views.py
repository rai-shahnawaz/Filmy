from django.shortcuts import render

# Create your views here.
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .neomodels import MovieList
from snippets.neomodels import Film
from .serializers import MovieListSerializer

class MovieListListCreateView(generics.ListCreateAPIView):
	permission_classes = (IsAuthenticated,)
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
	permission_classes = (IsAuthenticated,)
	serializer_class = MovieListSerializer

	def get_queryset(self):
		return MovieList.nodes.all()
