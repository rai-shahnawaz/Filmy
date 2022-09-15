from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from snippets import views

urlpatterns = [
    path('films', views.FilmList.as_view()),
    path('<int:pk>/', views.FilmDetail.as_view()),
    path('genres', views.GenreList.as_view()),
    path('subgenres', views.SubGenreList.as_view()),
    path('badges', views.BadgeList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
