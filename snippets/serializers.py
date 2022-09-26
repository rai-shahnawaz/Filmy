from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')
        
        
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        token['username'] = user.username
        return token


# Register Serializer
# class RegisterSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('id', 'username', 'email', 'password')
#         extra_kwargs = {'password': {'write_only': True}}

#     def create(self, validated_data):
#         user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])
#         user_profile = UserProfile.objects.create(user=user)
#         user_profile.email = validated_data['email']
#         user_profile.password = validated_data['password']
#         user_profile.save()

#         return user
    
    
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
        