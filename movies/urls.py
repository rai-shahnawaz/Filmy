from django.urls import path
from movies.views import FilmList, FilmDetail, GenreList, SubGenreList, BadgeList
from snippets.neoviews import MovieListView, MovieSearchView, MovieRateView, MovieReviewView

urlpatterns = [
    path('films/', FilmList.as_view()),
    path('films/<int:pk>/', FilmDetail.as_view()),
    path('genres/', GenreList.as_view()),
    path('subgenres/', SubGenreList.as_view()),
    path('badges/', BadgeList.as_view()),

    path('movies/', MovieListView.as_view(), name='movie_list'),
    path('movies/search/', MovieSearchView.as_view(), name='movie_search'),
    path('movies/<str:uid>/rate/', MovieRateView.as_view(), name='movie_rate'),
    path('movies/<str:uid>/review/', MovieReviewView.as_view(), name='movie_review'),
]