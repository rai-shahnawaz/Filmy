from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from movies.neomodels import Film, Series

# User-facing recommendations endpoint (basic: recommend by genre overlap with favorites/watchlist)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_recommendations(request):
	user_id = str(request.user.id)
	from movies.neomodels import Favorite, Watchlist
	# Gather genres from user's favorites and watchlist
	genre_counter = {}
	for fav in Favorite.nodes.filter(user_id=user_id):
		film = fav.film.single()
		if film:
			for genre in getattr(film, 'genres', []):
				genre_counter[genre.name] = genre_counter.get(genre.name, 0) + 1
	for wl in Watchlist.nodes.filter(user_id=user_id):
		film = wl.film.single()
		if film:
			for genre in getattr(film, 'genres', []):
				genre_counter[genre.name] = genre_counter.get(genre.name, 0) + 1
	# Recommend top films/series in top genres not already in favorites/watchlist
	top_genres = sorted(genre_counter, key=genre_counter.get, reverse=True)[:3]
	exclude_uids = set()
	for fav in Favorite.nodes.filter(user_id=user_id):
		film = fav.film.single()
		if film:
			exclude_uids.add(film.uid)
	for wl in Watchlist.nodes.filter(user_id=user_id):
		film = wl.film.single()
		if film:
			exclude_uids.add(film.uid)
	recommendations = []
	for genre_name in top_genres:
		for film in Film.nodes.filter(is_active=1):
			if any(g.name == genre_name for g in getattr(film, 'genres', [])) and film.uid not in exclude_uids:
				recommendations.append({'uid': film.uid, 'title': film.title, 'description': film.description, 'genre': genre_name})
		for series in Series.nodes.filter(is_active=1):
			if any(g.name == genre_name for g in getattr(series, 'genres', [])) and series.uid not in exclude_uids:
				recommendations.append({'uid': series.uid, 'title': series.title, 'description': series.description, 'genre': genre_name})
	return Response({'recommendations': recommendations[:20]})
