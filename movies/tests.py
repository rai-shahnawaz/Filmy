from django.test import SimpleTestCase
from django.urls import resolve, reverse

from movies.views import homepage, search_movies, user_dashboard


class MoviesUrlTests(SimpleTestCase):
    def test_homepage_route_resolves(self):
        match = resolve("/api/")
        self.assertIs(match.func, homepage)

    def test_search_movies_route_resolves(self):
        match = resolve(reverse("search_movies"))
        self.assertIs(match.func, search_movies)

    def test_user_dashboard_route_is_named(self):
        self.assertEqual(reverse("user_dashboard"), "/api/user/dashboard/")
