from .models import *
from django.contrib.auth.models import User
from .serializers import *
from .decorators import *
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, OutstandingToken, BlacklistedToken
from rest_framework.renderers import TemplateHTMLRenderer
    

class RegisterView(generics.CreateAPIView):
    
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
    
    
class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        
class LogoutAllView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        tokens = OutstandingToken.objects.filter(user_id=request.user.id)
        for token in tokens:
            t, _ = BlacklistedToken.objects.get_or_create(token=token)

        return Response(status=status.HTTP_205_RESET_CONTENT)


class ChangePasswordView(generics.UpdateAPIView):
    
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer
    
    
class UpdateProfileView(generics.UpdateAPIView):
    
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UpdateUserSerializer
    
    
class FilmList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Film.objects.all()
    serializer_class = FilmSerializer


class FilmDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Film.objects.all()
    serializer_class = FilmSerializer
    
    
class GenreList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    
    
class SubGenreList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = SubGenre.objects.all()
    serializer_class = SubGenreSerializer
    
    
class BadgeList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = SubGenre.objects.all()
    serializer_class = BadgeSerializer
    

class MovieList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'index.html'
    
    def get(self, request):
        queryset = Film.objects.all()
        return Response({'films': queryset})
    