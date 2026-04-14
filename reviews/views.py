from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from movies.neomodels import Film, Series, Episode

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_rating(request):
	object_type = request.data.get('object_type')
	object_uid = request.data.get('object_uid')
	rating = request.data.get('rating')
	if not all([object_type, object_uid, rating]):
		return Response({'error': 'Missing required fields.'}, status=400)
	user_id = str(request.user.id)
	Model = None
	if object_type == 'film':
		Model = Film
	elif object_type == 'series':
		Model = Series
	elif object_type == 'episode':
		Model = Episode
	obj = Model.nodes.get_or_none(uid=object_uid) if Model else None
	if not obj:
		return Response({'error': f'{object_type.title()} not found.'}, status=404)
	from movies.neomodels import UserRating
	# Remove old rating if exists
	for ur in UserRating.nodes.filter(user_id=user_id):
		if ur.film.single() and ur.film.single().uid == object_uid:
			ur.delete()
	ur = UserRating(user_id=user_id, rating=float(rating)).save()
	ur.film.connect(obj)
	return Response({'status': 'Rating added.'})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_review(request):
	object_type = request.data.get('object_type')
	object_uid = request.data.get('object_uid')
	review = request.data.get('review')
	if not all([object_type, object_uid, review]):
		return Response({'error': 'Missing required fields.'}, status=400)
	user_id = str(request.user.id)
	Model = None
	if object_type == 'film':
		Model = Film
	elif object_type == 'series':
		Model = Series
	elif object_type == 'episode':
		Model = Episode
	obj = Model.nodes.get_or_none(uid=object_uid) if Model else None
	if not obj:
		return Response({'error': f'{object_type.title()} not found.'}, status=404)
	from movies.neomodels import UserReview
	ur = UserReview(user_id=user_id, review=review, status='pending').save()
	ur.film.connect(obj)
	return Response({'status': 'Review submitted for approval.'})

@api_view(['GET'])
@permission_classes([AllowAny])
def get_ratings_reviews(request):
	object_type = request.GET.get('object_type')
	object_uid = request.GET.get('object_uid')
	if not all([object_type, object_uid]):
		return Response({'error': 'Missing required fields.'}, status=400)
	Model = None
	if object_type == 'film':
		Model = Film
	elif object_type == 'series':
		Model = Series
	elif object_type == 'episode':
		Model = Episode
	obj = Model.nodes.get_or_none(uid=object_uid) if Model else None
	if not obj:
		return Response({'error': f'{object_type.title()} not found.'}, status=404)
	from movies.neomodels import UserRating, UserReview
	ratings = [float(r.rating) for r in UserRating.nodes.filter() if r.film.single() and r.film.single().uid == object_uid]
	reviews = [
		{'user_id': r.user_id, 'review': r.review, 'status': r.status}
		for r in UserReview.nodes.filter(status='approved') if r.film.single() and r.film.single().uid == object_uid
	]
	avg_rating = sum(ratings) / len(ratings) if ratings else None
	return Response({'avg_rating': avg_rating, 'ratings': ratings, 'reviews': reviews})
