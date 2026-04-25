from core.neo4j_cypher_utils import run_read_cypher
from movies.neomodels import get_films_with_min_year

class CypherUtilityTests(SimpleTestCase):
    def test_get_films_with_min_year(self):
        # This test assumes at least one film exists with release_year >= 2000
        try:
            results = get_films_with_min_year(2000)
            self.assertIsInstance(results, list)
        except Exception as e:
            self.fail(f"Cypher utility failed: {e}")
from django.test import SimpleTestCase
from django.urls import resolve, reverse

from movies.views import homepage, search_movies, user_dashboard


class MoviesUrlTests(SimpleTestCase):
    def test_homepage_route_resolves(self):
        match = resolve("/api/")
        self.assertIs(match.func, homepage)

    def test_root_route_resolves(self):
        match = resolve("/")
        self.assertIs(match.func, homepage)

    def test_search_movies_route_resolves(self):
        match = resolve(reverse("search_movies"))
        self.assertIs(match.func, search_movies)

    def test_user_dashboard_route_is_named(self):
        self.assertEqual(reverse("user_dashboard"), "/api/user/dashboard/")
