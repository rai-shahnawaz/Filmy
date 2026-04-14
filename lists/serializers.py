from rest_framework import serializers
from .neomodels import MovieList


class MovieListSerializer(serializers.Serializer):
    name = serializers.CharField()
    description = serializers.CharField(allow_blank=True, required=False)
    films = serializers.ListField(child=serializers.CharField(), required=False)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['films'] = [film.title for film in instance.films]
        return data
