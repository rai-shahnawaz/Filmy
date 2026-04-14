from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from movies.neomodels import Film
from .neomodels import MovieList
from .serializers import MovieListSerializer


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_personal_list(request):
    name = request.data.get("name")
    description = request.data.get("description", "")
    film_titles = request.data.get("films", [])
    user_id = str(request.user.id)

    if not name:
        return Response({"error": "Name is required."}, status=400)

    movie_list = MovieList(
        name=name,
        description=description,
        status="pending",
        owner_id=user_id,
    ).save()
    for title in film_titles:
        film = Film.nodes.get_or_none(title=title)
        if film:
            movie_list.films.connect(film)
    return Response({"status": "List created and submitted for approval."})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def update_personal_list(request):
    uid = request.data.get("uid")
    name = request.data.get("name")
    description = request.data.get("description", "")
    film_titles = request.data.get("films", [])

    if not uid:
        return Response({"error": "List uid is required."}, status=400)

    movie_list = MovieList.nodes.get_or_none(uid=uid)
    if movie_list is None:
        return Response({"error": "List not found."}, status=404)

    if name:
        movie_list.name = name
    movie_list.description = description
    for film in list(movie_list.films):
        movie_list.films.disconnect(film)
    for title in film_titles:
        film = Film.nodes.get_or_none(title=title)
        if film:
            movie_list.films.connect(film)
    movie_list.save()
    return Response({"status": "List updated."})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def delete_personal_list(request):
    uid = request.data.get("uid")
    if not uid:
        return Response({"error": "List uid is required."}, status=400)

    movie_list = MovieList.nodes.get_or_none(uid=uid)
    if movie_list is None:
        return Response({"error": "List not found."}, status=404)

    movie_list.delete()
    return Response({"status": "List deleted."})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_personal_lists(request):
    movie_lists = MovieList.nodes.filter(owner_id=str(request.user.id))
    data = [
        {
            "uid": movie_list.uid,
            "name": movie_list.name,
            "description": movie_list.description,
            "films": [film.title for film in movie_list.films],
        }
        for movie_list in movie_lists
    ]
    return Response({"lists": data})


class MovieListListCreateView(generics.ListCreateAPIView):
    serializer_class = MovieListSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_queryset(self):
        return MovieList.nodes.all()

    def perform_create(self, serializer):
        name = serializer.validated_data["name"]
        description = serializer.validated_data.get("description", "")
        film_titles = serializer.validated_data.get("films", [])

        movie_list = MovieList(
            name=name,
            description=description,
            owner_id=str(self.request.user.id),
        ).save()
        for title in film_titles:
            film = Film.nodes.get_or_none(title=title)
            if film:
                movie_list.films.connect(film)
        return movie_list


class MovieListDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MovieListSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_queryset(self):
        return MovieList.nodes.all()
