from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from snippets.views import *
# from knox import views as knox_views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    # path('register/', RegisterAPI.as_view(), name='register'),
    # path('api/login/', LoginAPI.as_view(), name='login'),
    # path('api/logout/', knox_views.LogoutView.as_view(), name='logout'),
    # path('api/logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('films', FilmList),
    path('<int:pk>/', FilmDetail.as_view()),
    path('genres', GenreList.as_view()),
    path('subgenres', SubGenreList.as_view()),
    path('badges', BadgeList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
