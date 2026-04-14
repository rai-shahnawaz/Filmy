from django.urls import path
from .views import add_rating, add_review, get_ratings_reviews

urlpatterns = [
	path('add-rating/', add_rating, name='add_rating'),
	path('add-review/', add_review, name='add_review'),
	path('ratings-reviews/', get_ratings_reviews, name='get_ratings_reviews'),
]
