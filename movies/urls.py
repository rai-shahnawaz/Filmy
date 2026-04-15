from django.urls import path
from movies.views import (
    FilmList, FilmDetail, GenreList, SeriesList, SeriesDetail, SeasonList, SeasonDetail,
    EpisodeList, EpisodeDetail, BadgeList, AdminLoginView, AdminDashboardView,
    export_films_json, import_films_json, export_films_csv, import_films_csv,
    export_series_json, import_series_json, export_series_csv, import_series_csv,
    search_movies, search_series, search_lists, add_favorite, remove_favorite,
    add_watchlist, remove_watchlist, user_dashboard, homepage, discover_panel, toggle_featured_status,
    add_admin_note, list_admin_notes, admin_dashboard_analytics,
    assign_person_to_object, remove_person_from_object,
    soft_delete_film, restore_film, soft_delete_series, restore_series,
    soft_delete_episode, restore_episode
)
from recommendations.views import get_recommendations
from reviews.views import add_rating, add_review, get_ratings_reviews

urlpatterns = [
    path('', homepage, name='homepage'),
    path('user/dashboard/', user_dashboard, name='user_dashboard'),
    path('user/discover/', discover_panel, name='discover_panel'),
    # User-facing browse/search/filter
    path('user/search_movies/', search_movies, name='search_movies'),
    path('user/search_series/', search_series, name='search_series'),
    path('user/search_lists/', search_lists, name='search_lists'),
    path('user/recommendations/', get_recommendations, name='user_recommendations'),
    # User-facing favorites and watchlist
    path('user/add_favorite/', add_favorite, name='add_favorite'),
    path('user/remove_favorite/', remove_favorite, name='remove_favorite'),
    path('user/add_watchlist/', add_watchlist, name='add_watchlist'),
    path('user/remove_watchlist/', remove_watchlist, name='remove_watchlist'),
    # User-facing ratings and reviews
    path('user/add_rating/', add_rating, name='add_rating'),
    path('user/add_review/', add_review, name='add_review'),
    path('user/get_ratings_reviews/', get_ratings_reviews, name='get_ratings_reviews'),
    # Admin bulk import/export
    path('admin/films/export/json/', export_films_json, name='export_films_json'),
    path('admin/films/import/json/', import_films_json, name='import_films_json'),
    path('admin/films/export/csv/', export_films_csv, name='export_films_csv'),
    path('admin/films/import/csv/', import_films_csv, name='import_films_csv'),
    path('admin/series/export/json/', export_series_json, name='export_series_json'),
    path('admin/series/import/json/', import_series_json, name='import_series_json'),
    path('admin/series/export/csv/', export_series_csv, name='export_series_csv'),
    path('admin/series/import/csv/', import_series_csv, name='import_series_csv'),
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
    path('badges/', BadgeList.as_view()),
    # Admin toggle featured/pinned status
    path('admin/toggle_featured/', toggle_featured_status, name='toggle_featured_status'),
    # Admin notes/comments
    path('admin/notes/add/', add_admin_note, name='add_admin_note'),
    path('admin/notes/list/', list_admin_notes, name='list_admin_notes'),
    # Admin dashboard analytics
    path('admin/dashboard/analytics/', admin_dashboard_analytics, name='admin_dashboard_analytics'),
    # Admin relationship management
    path('admin/assign_person/', assign_person_to_object, name='assign_person_to_object'),
    path('admin/remove_person/', remove_person_from_object, name='remove_person_from_object'),
    # Admin soft delete/restore
    path('admin/films/<str:uid>/soft_delete/', soft_delete_film, name='soft_delete_film'),
    path('admin/films/<str:uid>/restore/', restore_film, name='restore_film'),
    path('admin/series/<str:uid>/soft_delete/', soft_delete_series, name='soft_delete_series'),
    path('admin/series/<str:uid>/restore/', restore_series, name='restore_series'),
    path('admin/episodes/<str:uid>/soft_delete/', soft_delete_episode, name='soft_delete_episode'),
    path('admin/episodes/<str:uid>/restore/', restore_episode, name='restore_episode'),
]
