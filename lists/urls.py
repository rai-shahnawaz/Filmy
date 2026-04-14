    # User-facing personal lists
    path('user/create_list/', create_personal_list, name='create_personal_list'),
    path('user/update_list/', update_personal_list, name='update_personal_list'),
    path('user/delete_list/', delete_personal_list, name='delete_personal_list'),
    path('user/lists/', list_personal_lists, name='list_personal_lists'),
from django.urls import path
from .views import MovieListListCreateView, MovieListDetailView

urlpatterns = [
    path('lists/', MovieListListCreateView.as_view(), name='movie_list_list_create'),
    path('lists/<str:pk>/', MovieListDetailView.as_view(), name='movie_list_detail'),
]
