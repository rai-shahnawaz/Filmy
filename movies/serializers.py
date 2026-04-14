from rest_framework import serializers
from .neomodels import Film, Genre, Series, Season, Episode, Person

class PersonSerializer(serializers.Serializer):
    uid = serializers.CharField()
    name = serializers.CharField()
    bio = serializers.CharField(allow_blank=True, required=False)
    birth_date = serializers.DateField(required=False, allow_null=True)

class FilmSerializer(serializers.Serializer):
    uid = serializers.CharField()
    title = serializers.CharField()
    description = serializers.CharField(allow_blank=True, required=False)
    release_year = serializers.IntegerField(required=False)
    type = serializers.CharField()
    genres = serializers.ListField(child=serializers.CharField(), required=False)
    actors = PersonSerializer(many=True, required=False)
    directors = PersonSerializer(many=True, required=False)
    producers = PersonSerializer(many=True, required=False)
    creators = PersonSerializer(many=True, required=False)
    crew = PersonSerializer(many=True, required=False)
class SeriesSerializer(serializers.Serializer):
    uid = serializers.CharField()
    title = serializers.CharField()
    description = serializers.CharField(allow_blank=True, required=False)
    start_year = serializers.IntegerField(required=False)
    end_year = serializers.IntegerField(required=False)
    genres = serializers.ListField(child=serializers.CharField(), required=False)
    actors = PersonSerializer(many=True, required=False)
    directors = PersonSerializer(many=True, required=False)
    producers = PersonSerializer(many=True, required=False)
    creators = PersonSerializer(many=True, required=False)
    crew = PersonSerializer(many=True, required=False)
    seasons = serializers.ListField(child=serializers.CharField(), required=False)

class SeasonSerializer(serializers.Serializer):
    uid = serializers.CharField()
    season_number = serializers.IntegerField()
    episodes = serializers.ListField(child=serializers.CharField(), required=False)

class EpisodeSerializer(serializers.Serializer):
    uid = serializers.CharField()
    title = serializers.CharField()
    episode_number = serializers.IntegerField()
    air_date = serializers.DateField(required=False, allow_null=True)
    description = serializers.CharField(allow_blank=True, required=False)
    actors = PersonSerializer(many=True, required=False)
    directors = PersonSerializer(many=True, required=False)
    producers = PersonSerializer(many=True, required=False)
    creators = PersonSerializer(many=True, required=False)
    crew = PersonSerializer(many=True, required=False)

class GenreSerializer(serializers.Serializer):
    # Define fields as per Genre neomodel
    pass

class SubGenreSerializer(serializers.Serializer):
    # Define fields as per SubGenre neomodel
    pass

class BadgeSerializer(serializers.Serializer):
    # Define fields as per Badge neomodel
    pass
