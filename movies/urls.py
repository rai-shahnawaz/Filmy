                        # Admin toggle featured/pinned status
                        path('admin/toggle_featured/', toggle_featured_status, name='toggle_featured_status'),
                    # Admin notes/comments
                    path('admin/notes/add/', add_admin_note, name='add_admin_note'),
                    path('admin/notes/list/', list_admin_notes, name='list_admin_notes'),
                # Admin dashboard analytics
                path('admin/dashboard/analytics/', admin_dashboard_analytics, name='admin_dashboard_analytics'),
            # Admin approve/reject user content
            path('admin/reviews/<str:uid>/approve/', approve_review, name='approve_review'),
            path('admin/reviews/<str:uid>/reject/', reject_review, name='reject_review'),
            path('admin/lists/<str:uid>/approve/', approve_list, name='approve_list'),
            path('admin/lists/<str:uid>/reject/', reject_list, name='reject_list'),
        # Admin relationship management
        path('admin/assign_person/', assign_person_to_object, name='assign_person_to_object'),
        path('admin/remove_person/', remove_person_from_object, name='remove_person_from_object'),
    # Admin soft delete/restore
    path('admin/films/<str:uid>/soft_delete/', soft_delete_film, name='soft_delete_film'),
    path('admin/films/<str:uid>/restore/', restore_film, name='restore_film'),
    path('admin/series/<str:uid>/soft_delete/', soft_delete_series, name='soft_delete_series'),
    path('admin/series/<str:uid>/restore/', restore_series, name='restore_series'),
    path('admin/people/<str:uid>/soft_delete/', soft_delete_person, name='soft_delete_person'),
    path('admin/people/<str:uid>/restore/', restore_person, name='restore_person'),
    path('admin/episodes/<str:uid>/soft_delete/', soft_delete_episode, name='soft_delete_episode'),
    path('admin/episodes/<str:uid>/restore/', restore_episode, name='restore_episode'),
from django.urls import path
from movies.views import FilmList, FilmDetail, GenreList, SeriesList, SeriesDetail, SeasonList, SeasonDetail, EpisodeList, EpisodeDetail, PersonList, PersonDetail, BadgeList, AdminLoginView, AdminDashboardView
from movies.views import export_films_json, import_films_json, export_films_csv, import_films_csv
from movies.views import export_series_json, import_series_json, export_series_csv, import_series_csv
from movies.views import export_people_json, import_people_json, export_people_csv, import_people_csv
from snippets.neoviews import MovieListView, MovieSearchView, MovieRateView, MovieReviewView

urlpatterns = [
    # Admin bulk import/export
    path('admin/films/export/json/', export_films_json, name='export_films_json'),
    path('admin/films/import/json/', import_films_json, name='import_films_json'),
    path('admin/films/export/csv/', export_films_csv, name='export_films_csv'),
    path('admin/films/import/csv/', import_films_csv, name='import_films_csv'),

    path('admin/series/export/json/', export_series_json, name='export_series_json'),
    path('admin/series/import/json/', import_series_json, name='import_series_json'),
    path('admin/series/export/csv/', export_series_csv, name='export_series_csv'),
    path('admin/series/import/csv/', import_series_csv, name='import_series_csv'),

    path('admin/people/export/json/', export_people_json, name='export_people_json'),
    path('admin/people/import/json/', import_people_json, name='import_people_json'),
    path('admin/people/export/csv/', export_people_csv, name='export_people_csv'),
    path('admin/people/import/csv/', import_people_csv, name='import_people_csv'),
    path('admin/login/', AdminLoginView.as_view(), name='admin_login'),
    path('admin/dashboard/', AdminDashboardView.as_view(), name='admin_dashboard'),
    path('films/', FilmList.as_view()),
    path('films/<int:pk>/', FilmDetail.as_view()),
    path('genres/', GenreList.as_view()),
    path('series/', SeriesList.as_view()),
    path('series/<str:pk>/', SeriesDetail.as_view()),
    path('seasons/', SeasonList.as_view()),
    path('seasons/<str:pk>/', SeasonDetail.as_view()),
    path('episodes/', EpisodeList.as_view()),
    path('episodes/<str:pk>/', EpisodeDetail.as_view()),
    path('people/', PersonList.as_view()),
    path('people/<str:pk>/', PersonDetail.as_view()),
    path('badges/', BadgeList.as_view()),

    # ...existing code for MovieListView, MovieSearchView, etc.
    path('movies/', MovieListView.as_view(), name='movie_list'),
    path('movies/search/', MovieSearchView.as_view(), name='movie_search'),
    path('movies/<str:uid>/rate/', MovieRateView.as_view(), name='movie_rate'),
    path('movies/<str:uid>/review/', MovieReviewView.as_view(), name='movie_review'),
]