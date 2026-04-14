from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from .serializers import FilmSerializer, GenreSerializer, SubGenreSerializer, BadgeSerializer
from snippets.neomodels import Film, Genre, SubGenre, Badge

class FilmList(generics.ListCreateAPIView):
	permission_classes = (IsAuthenticated,)
	queryset = Film.nodes.all()
	serializer_class = FilmSerializer

class FilmDetail(generics.RetrieveUpdateDestroyAPIView):
	permission_classes = (IsAuthenticated,)
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
