from django.urls import path
from .views import MovieListListCreateView, MovieListDetailView

urlpatterns = [
    path('lists/', MovieListListCreateView.as_view(), name='movie_list_list_create'),
    path('lists/<str:pk>/', MovieListDetailView.as_view(), name='movie_list_detail'),
]
