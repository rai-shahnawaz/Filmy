from .models import *
from .serializers import *
from .decorators import *
from rest_framework import generics, permissions
from rest_framework.response import Response
# from knox.models import AuthToken
from .serializers import UserSerializer
from django.contrib.auth import login
from rest_framework.authtoken.serializers import AuthTokenSerializer
# from knox.views import LoginView as KnoxLoginView

# Create your views here.
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny
from .serializers import MyTokenObtainPairSerializer


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer

# Register API
# class RegisterAPI(generics.GenericAPIView):
#     serializer_class = RegisterSerializer

#     def post(self, request, *args, **kwargs):
#         if self.request.version == 'v1':
#             # you can put here business logic that
#             # is specific to version 1
#             serializer = self.get_serializer(data=request.data)
#             serializer.is_valid(raise_exception=True)
#             user = serializer.save()
#             return Response({"user": UserSerializer(user, 
#                                                     context=self.get_serializer_context()).data,
#                             "token": AuthToken.objects.create(user)[1]
#                             })
#         # You can put here the current version
#         # business logic
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.save()
#         return Response({"user": UserSerializer(user, 
#                                                 context=self.get_serializer_context()).data,
#                         "token": AuthToken.objects.create(user)[1]
#                         })
        
        
# class LoginAPI(KnoxLoginView):
#     permission_classes = (permissions.AllowAny,)

#     def post(self, request, format=None):
#         serializer = AuthTokenSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         login(request, user)
#         return super(LoginAPI, self).post(request, format=None)
    
        
@user_is_entry_author
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
    