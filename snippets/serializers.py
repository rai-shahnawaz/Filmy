from rest_framework import serializers
from .models import *


class FilmSerializer(serializers.ModelSerializer):

    class Meta:
        model = Film
        fields = ('__all__')
        
        
class BadgeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Badge
        fields = ('__all__')
        
        
class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('__all__')
        
        
class SubGenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = SubGenre
        fields = ('__all__')
        