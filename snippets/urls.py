from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from snippets.views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import RegisterView


urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('change_password/<int:pk>/', ChangePasswordView.as_view(), name='auth_change_password'),
    path('update_profile/<int:pk>/', UpdateProfileView.as_view(), name='auth_update_profile'),
    path('logout/', LogoutView.as_view(), name='auth_logout'),
    path('logout_all/', LogoutAllView.as_view(), name='auth_logout_all'),

    path('films/', FilmList),
    path('<int:pk>/', FilmDetail.as_view()),
    path('genres/', GenreList.as_view()),
    path('subgenres/', SubGenreList.as_view()),
    path('badges/', BadgeList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
