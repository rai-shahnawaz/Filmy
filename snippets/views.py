from rest_framework import generics
from .models import *
from .serializers import *

# Create your views here.
class FilmList(generics.ListCreateAPIView):
    queryset = Film.objects.all()
    serializer_class = FilmSerializer


class FilmDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Film.objects.all()
    serializer_class = FilmSerializer
    
    
class GenreList(generics.ListCreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    
    
class SubGenreList(generics.ListCreateAPIView):
    queryset = SubGenre.objects.all()
    serializer_class = SubGenreSerializer
    
    
class BadgeList(generics.ListCreateAPIView):
    queryset = SubGenre.objects.all()
    serializer_class = BadgeSerializer
    