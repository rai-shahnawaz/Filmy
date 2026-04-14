import csv
import io
import json
from datetime import timedelta

from django.contrib.auth import authenticate, get_user, get_user_model, login
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from django.utils.decorators import method_decorator
from rest_framework import generics
from rest_framework.decorators import api_view, parser_classes, permission_classes
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from lists.neomodels import MovieList
from people.models import Person
from .adminnotes import AdminNote
from .auditlog import AuditLog
from .neomodels import Episode, Favorite, Film, Genre, Season, Series, Watchlist
from .serializers import (
    EpisodeSerializer,
    FilmSerializer,
    GenreSerializer,
    SeriesSerializer,
    SeasonSerializer,
)


def homepage(request):
    return render(request, "index.html")


def _content_model(object_type):
    return {
        "film": Film,
        "series": Series,
        "episode": Episode,
        "person": Person,
    }.get(object_type)


def _get_object(object_type, object_uid):
    model = _content_model(object_type)
    if model is None:
        return None
    return model.nodes.get_or_none(uid=object_uid)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_dashboard(request):
    user_id = str(request.user.id)
    from .neomodels import UserRating, UserReview

    ratings = list(UserRating.nodes.filter(user_id=user_id))
    reviews = list(UserReview.nodes.filter(user_id=user_id))
    favorites = list(Favorite.nodes.filter(user_id=user_id))
    watchlist = list(Watchlist.nodes.filter(user_id=user_id))
    lists = list(MovieList.nodes.filter(owner_id=user_id))

    activity = []
    for rating in sorted(ratings, key=lambda item: getattr(item, "created_at", timezone.now()), reverse=True)[:3]:
        activity.append(
            {
                "type": "rating",
                "object": getattr(rating.film.single(), "uid", None),
                "value": rating.rating,
                "date": getattr(rating, "created_at", None),
            }
        )
    for review in sorted(reviews, key=lambda item: getattr(item, "created_at", timezone.now()), reverse=True)[:3]:
        activity.append(
            {
                "type": "review",
                "object": getattr(review.film.single(), "uid", None),
                "text": review.review,
                "date": getattr(review, "created_at", None),
            }
        )
    for favorite in sorted(favorites, key=lambda item: getattr(item, "created_at", timezone.now()), reverse=True)[:2]:
        activity.append(
            {
                "type": "favorite",
                "object": getattr(favorite.film.single(), "uid", None),
                "date": getattr(favorite, "created_at", None),
            }
        )
    for watch in sorted(watchlist, key=lambda item: getattr(item, "created_at", timezone.now()), reverse=True)[:2]:
        activity.append(
            {
                "type": "watchlist",
                "object": getattr(watch.film.single(), "uid", None),
                "date": getattr(watch, "created_at", None),
            }
        )

    activity = sorted(activity, key=lambda item: item.get("date") or timezone.now(), reverse=True)[:10]
    stats = {
        "ratings_count": len(ratings),
        "reviews_count": len(reviews),
        "favorites_count": len(favorites),
        "watchlist_count": len(watchlist),
        "lists_count": len(lists),
    }
    contributions = [
        {
            "uid": movie_list.uid,
            "name": movie_list.name,
            "created_at": getattr(movie_list, "created_at", None),
        }
        for movie_list in lists
    ]

    recent_logins = []
    if request.user.last_login:
        recent_logins.append({"last_login": request.user.last_login})

    badges = []
    if stats["ratings_count"] > 10:
        badges.append({"name": "Movie Buff", "desc": "Rated 10+ movies"})
    if stats["reviews_count"] > 5:
        badges.append({"name": "Reviewer", "desc": "Wrote 5+ reviews"})

    profile = {
        "username": request.user.username,
        "email": request.user.email,
        "first_name": request.user.first_name,
        "last_name": request.user.last_name,
    }
    return Response(
        {
            "profile": profile,
            "activity": activity,
            "stats": stats,
            "contributions": contributions,
            "recent_logins": recent_logins,
            "badges": badges,
        }
    )


@api_view(["GET"])
@permission_classes([AllowAny])
def search_movies(request):
    query = request.GET.get("q", "").strip().lower()
    films = Film.nodes.filter(is_active=1)
    results = [
        {"uid": film.uid, "title": film.title, "description": film.description}
        for film in films
        if not query or query in film.title.lower()
    ]
    return Response({"results": results})


@api_view(["GET"])
@permission_classes([AllowAny])
def search_series(request):
    query = request.GET.get("q", "").strip().lower()
    series_items = Series.nodes.filter(is_active=1)
    results = [
        {"uid": series.uid, "title": series.title, "description": series.description}
        for series in series_items
        if not query or query in series.title.lower()
    ]
    return Response({"results": results})


@api_view(["GET"])
@permission_classes([AllowAny])
def search_lists(request):
    query = request.GET.get("q", "").strip().lower()
    approved_lists = MovieList.nodes.filter(status="approved")
    results = [
        {"uid": movie_list.uid, "name": movie_list.name, "description": movie_list.description}
        for movie_list in approved_lists
        if not query or query in movie_list.name.lower()
    ]
    return Response({"results": results})


def _connect_user_relation(relation_model, user_id, object_uid, target):
    for existing in relation_model.nodes.filter(user_id=user_id):
        linked = existing.film.single()
        if linked and linked.uid == object_uid:
            existing.delete()
    relation = relation_model(user_id=user_id).save()
    relation.film.connect(target)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_favorite(request):
    object_type = request.data.get("object_type")
    object_uid = request.data.get("object_uid")
    if not object_type or not object_uid:
        return Response({"error": "Missing required fields."}, status=400)

    target = _get_object(object_type, object_uid)
    if target is None:
        return Response({"error": f"{object_type.title()} not found."}, status=404)

    _connect_user_relation(Favorite, str(request.user.id), object_uid, target)
    return Response({"status": "Added to favorites."})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def remove_favorite(request):
    object_uid = request.data.get("object_uid")
    if not object_uid:
        return Response({"error": "Missing required fields."}, status=400)

    for favorite in Favorite.nodes.filter(user_id=str(request.user.id)):
        linked = favorite.film.single()
        if linked and linked.uid == object_uid:
            favorite.delete()
            return Response({"status": "Removed from favorites."})
    return Response({"error": "Favorite not found."}, status=404)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_watchlist(request):
    object_type = request.data.get("object_type")
    object_uid = request.data.get("object_uid")
    if not object_type or not object_uid:
        return Response({"error": "Missing required fields."}, status=400)

    target = _get_object(object_type, object_uid)
    if target is None:
        return Response({"error": f"{object_type.title()} not found."}, status=404)

    _connect_user_relation(Watchlist, str(request.user.id), object_uid, target)
    return Response({"status": "Added to watchlist."})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def remove_watchlist(request):
    object_uid = request.data.get("object_uid")
    if not object_uid:
        return Response({"error": "Missing required fields."}, status=400)

    for watchlist_item in Watchlist.nodes.filter(user_id=str(request.user.id)):
        linked = watchlist_item.film.single()
        if linked and linked.uid == object_uid:
            watchlist_item.delete()
            return Response({"status": "Removed from watchlist."})
    return Response({"error": "Watchlist item not found."}, status=404)


def log_audit(request, action, obj, object_type, details=""):
    user = get_user(request)
    AuditLog.objects.create(
        user=user if getattr(user, "is_authenticated", False) else None,
        action=action,
        object_type=object_type,
        object_uid=getattr(obj, "uid", ""),
        object_repr=str(obj),
        details=details,
    )


@api_view(["POST"])
@permission_classes([IsAdminUser])
def toggle_featured_status(request):
    object_type = request.data.get("object_type")
    object_uid = request.data.get("object_uid")
    if not object_type or not object_uid:
        return Response({"error": "Missing required fields."}, status=400)

    obj = _get_object(object_type, object_uid)
    if obj is None:
        return Response({"error": f"{object_type.title()} not found."}, status=404)

    obj.is_featured = 0 if getattr(obj, "is_featured", 0) else 1
    obj.save()
    log_audit(request, "update", obj, object_type.title(), f"Toggled featured to {obj.is_featured}")
    return Response({"status": f"Featured status set to {obj.is_featured}."})


@api_view(["POST"])
@permission_classes([IsAdminUser])
def add_admin_note(request):
    object_type = request.data.get("object_type")
    object_uid = request.data.get("object_uid")
    note = request.data.get("note")
    if not object_type or not object_uid or not note:
        return Response({"error": "Missing required fields."}, status=400)

    admin_note = AdminNote(
        object_type=object_type,
        object_uid=object_uid,
        user_id=str(request.user.id),
        note=note,
    ).save()
    log_audit(request, "update", admin_note, "AdminNote", "Added note")
    return Response({"status": "Note added."})


@api_view(["GET"])
@permission_classes([IsAdminUser])
def list_admin_notes(request):
    object_type = request.GET.get("object_type")
    object_uid = request.GET.get("object_uid")
    if not object_type or not object_uid:
        return Response({"error": "Missing required fields."}, status=400)

    notes = AdminNote.nodes.filter(object_type=object_type, object_uid=object_uid)
    return Response(
        {
            "notes": [
                {"note": note.note, "user_id": note.user_id, "created_at": note.created_at}
                for note in notes
            ]
        }
    )


@api_view(["GET"])
@permission_classes([IsAdminUser])
def admin_dashboard_analytics(request):
    week_ago = timezone.now() - timedelta(days=7)
    recent_logs = AuditLog.objects.filter(timestamp__gte=week_ago).order_by("-timestamp")[:20]
    top_users = (
        AuditLog.objects.values("user")
        .exclude(user=None)
        .annotate(count=Count("id"))
        .order_by("-count")[:5]
    )

    user_model = get_user_model()
    user_map = {user.id: str(user) for user in user_model.objects.filter(id__in=[item["user"] for item in top_users])}
    return Response(
        {
            "film_count": Film.nodes.filter(is_active=1).count(),
            "series_count": Series.nodes.filter(is_active=1).count(),
            "person_count": Person.nodes.filter(is_active=1).count(),
            "recent_changes": [
                {
                    "timestamp": log.timestamp,
                    "user": str(log.user),
                    "action": log.action,
                    "object_type": log.object_type,
                    "object_uid": log.object_uid,
                    "details": log.details,
                }
                for log in recent_logs
            ],
            "top_contributors": [
                {"user": user_map.get(item["user"], "Unknown"), "count": item["count"]}
                for item in top_users
            ],
        }
    )


def _relationship_name(role):
    return {
        "actor": "actors",
        "director": "directors",
        "producer": "producers",
        "creator": "creators",
        "crew": "crew",
    }.get(role)


@api_view(["POST"])
@permission_classes([IsAdminUser])
def assign_person_to_object(request):
    object_type = request.data.get("object_type")
    object_uid = request.data.get("object_uid")
    person_uid = request.data.get("person_uid")
    role = request.data.get("role")
    if not all([object_type, object_uid, person_uid, role]):
        return Response({"error": "Missing required fields."}, status=400)

    person = Person.nodes.get_or_none(uid=person_uid)
    obj = _get_object(object_type, object_uid)
    relation_name = _relationship_name(role)
    if person is None:
        return Response({"error": "Person not found."}, status=404)
    if obj is None:
        return Response({"error": f"{object_type.title()} not found."}, status=404)
    if relation_name is None or not hasattr(obj, relation_name):
        return Response({"error": "Invalid role."}, status=400)

    getattr(obj, relation_name).connect(person)
    obj.save()
    log_audit(request, "update", obj, object_type.title(), f"Assigned {role} {person_uid}")
    return Response({"status": f"{role.title()} assigned."})


@api_view(["POST"])
@permission_classes([IsAdminUser])
def remove_person_from_object(request):
    object_type = request.data.get("object_type")
    object_uid = request.data.get("object_uid")
    person_uid = request.data.get("person_uid")
    role = request.data.get("role")
    if not all([object_type, object_uid, person_uid, role]):
        return Response({"error": "Missing required fields."}, status=400)

    person = Person.nodes.get_or_none(uid=person_uid)
    obj = _get_object(object_type, object_uid)
    relation_name = _relationship_name(role)
    if person is None:
        return Response({"error": "Person not found."}, status=404)
    if obj is None:
        return Response({"error": f"{object_type.title()} not found."}, status=404)
    if relation_name is None or not hasattr(obj, relation_name):
        return Response({"error": "Invalid role."}, status=400)

    getattr(obj, relation_name).disconnect(person)
    obj.save()
    log_audit(request, "update", obj, object_type.title(), f"Removed {role} {person_uid}")
    return Response({"status": f"{role.title()} removed."})


@api_view(["POST"])
@permission_classes([IsAdminUser])
def soft_delete_film(request, uid):
    film = Film.nodes.get_or_none(uid=uid)
    if film is None:
        return Response({"error": "Film not found."}, status=404)
    film.is_active = 0
    film.save()
    log_audit(request, "delete", film, "Film")
    return Response({"status": "Film soft deleted."})


@api_view(["POST"])
@permission_classes([IsAdminUser])
def restore_film(request, uid):
    film = Film.nodes.get_or_none(uid=uid)
    if film is None:
        return Response({"error": "Film not found."}, status=404)
    film.is_active = 1
    film.save()
    log_audit(request, "restore", film, "Film")
    return Response({"status": "Film restored."})


@api_view(["POST"])
@permission_classes([IsAdminUser])
def soft_delete_series(request, uid):
    series = Series.nodes.get_or_none(uid=uid)
    if series is None:
        return Response({"error": "Series not found."}, status=404)
    series.is_active = 0
    series.save()
    log_audit(request, "delete", series, "Series")
    return Response({"status": "Series soft deleted."})


@api_view(["POST"])
@permission_classes([IsAdminUser])
def restore_series(request, uid):
    series = Series.nodes.get_or_none(uid=uid)
    if series is None:
        return Response({"error": "Series not found."}, status=404)
    series.is_active = 1
    series.save()
    log_audit(request, "restore", series, "Series")
    return Response({"status": "Series restored."})


@api_view(["POST"])
@permission_classes([IsAdminUser])
def soft_delete_episode(request, uid):
    episode = Episode.nodes.get_or_none(uid=uid)
    if episode is None:
        return Response({"error": "Episode not found."}, status=404)
    episode.is_active = 0
    episode.save()
    log_audit(request, "delete", episode, "Episode")
    return Response({"status": "Episode soft deleted."})


@api_view(["POST"])
@permission_classes([IsAdminUser])
def restore_episode(request, uid):
    episode = Episode.nodes.get_or_none(uid=uid)
    if episode is None:
        return Response({"error": "Episode not found."}, status=404)
    episode.is_active = 1
    episode.save()
    log_audit(request, "restore", episode, "Episode")
    return Response({"status": "Episode restored."})


@api_view(["GET"])
@permission_classes([IsAdminUser])
def export_films_json(request):
    films = Film.nodes.filter(is_active=1)
    data = [film.__properties__ for film in films]
    return HttpResponse(json.dumps(data, default=str), content_type="application/json")


@api_view(["POST"])
@permission_classes([IsAdminUser])
@parser_classes([MultiPartParser, FormParser])
def import_films_json(request):
    file = request.FILES.get("file")
    if not file:
        return Response({"error": "No file uploaded."}, status=400)
    for entry in json.load(file):
        Film(**entry).save()
    return Response({"status": "Import complete."})


@api_view(["GET"])
@permission_classes([IsAdminUser])
def export_films_csv(request):
    films = list(Film.nodes.filter(is_active=1))
    if not films:
        return HttpResponse("", content_type="text/csv")
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=films[0].__properties__.keys())
    writer.writeheader()
    for film in films:
        writer.writerow(film.__properties__)
    return HttpResponse(output.getvalue(), content_type="text/csv")


@api_view(["POST"])
@permission_classes([IsAdminUser])
@parser_classes([MultiPartParser, FormParser])
def import_films_csv(request):
    file = request.FILES.get("file")
    if not file:
        return Response({"error": "No file uploaded."}, status=400)
    decoded = file.read().decode("utf-8")
    for row in csv.DictReader(io.StringIO(decoded)):
        Film(**row).save()
    return Response({"status": "Import complete."})


@api_view(["GET"])
@permission_classes([IsAdminUser])
def export_series_json(request):
    items = Series.nodes.filter(is_active=1)
    data = [series.__properties__ for series in items]
    return HttpResponse(json.dumps(data, default=str), content_type="application/json")


@api_view(["POST"])
@permission_classes([IsAdminUser])
@parser_classes([MultiPartParser, FormParser])
def import_series_json(request):
    file = request.FILES.get("file")
    if not file:
        return Response({"error": "No file uploaded."}, status=400)
    for entry in json.load(file):
        Series(**entry).save()
    return Response({"status": "Import complete."})


@api_view(["GET"])
@permission_classes([IsAdminUser])
def export_series_csv(request):
    items = list(Series.nodes.filter(is_active=1))
    if not items:
        return HttpResponse("", content_type="text/csv")
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=items[0].__properties__.keys())
    writer.writeheader()
    for series in items:
        writer.writerow(series.__properties__)
    return HttpResponse(output.getvalue(), content_type="text/csv")


@api_view(["POST"])
@permission_classes([IsAdminUser])
@parser_classes([MultiPartParser, FormParser])
def import_series_csv(request):
    file = request.FILES.get("file")
    if not file:
        return Response({"error": "No file uploaded."}, status=400)
    decoded = file.read().decode("utf-8")
    for row in csv.DictReader(io.StringIO(decoded)):
        Series(**row).save()
    return Response({"status": "Import complete."})


class AdminLoginView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "admin_login.html"
    permission_classes = []

    def get(self, request):
        return Response({})

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect("admin_dashboard")
        return Response({"error": "Invalid credentials or not an admin."}, status=401)


@method_decorator(user_passes_test(lambda user: user.is_staff), name="dispatch")
class AdminDashboardView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "admin_dashboard.html"
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(
            {
                "film_count": Film.nodes.count(),
                "series_count": Series.nodes.count(),
                "person_count": Person.nodes.count(),
            }
        )


class FilmList(generics.ListCreateAPIView):
    serializer_class = FilmSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAdminUser()]

    def get_queryset(self):
        return Film.nodes.all()


class FilmDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FilmSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAdminUser()]

    def get_queryset(self):
        return Film.nodes.all()


class GenreList(generics.ListCreateAPIView):
    serializer_class = GenreSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAdminUser()]

    def get_queryset(self):
        return Genre.nodes.all()


class SeriesList(generics.ListCreateAPIView):
    serializer_class = SeriesSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAdminUser()]

    def get_queryset(self):
        return Season.nodes.all()


class SeriesDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SeriesSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAdminUser()]

    def get_queryset(self):
        return Season.nodes.all()


class SeasonList(generics.ListCreateAPIView):
    serializer_class = SeasonSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAdminUser()]

    def get_queryset(self):
        return Series.nodes.all()


class SeasonDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SeasonSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAdminUser()]

    def get_queryset(self):
        return Series.nodes.all()


class EpisodeList(generics.ListCreateAPIView):
    serializer_class = EpisodeSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAdminUser()]

    def get_queryset(self):
        return Episode.nodes.all()


class EpisodeDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EpisodeSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAdminUser()]

    def get_queryset(self):
        return Episode.nodes.all()


class BadgeList(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({"results": []})
