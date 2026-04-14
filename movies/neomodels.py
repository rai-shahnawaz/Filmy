from neomodel import DateProperty, DateTimeProperty, FloatProperty, IntegerProperty, RelationshipFrom, RelationshipTo, StringProperty, StructuredNode, UniqueIdProperty
from people.models import Person

class Film(StructuredNode):
    uid = UniqueIdProperty()
    title = StringProperty(unique_index=True, required=True)
    description = StringProperty()
    release_year = IntegerProperty()
    type = StringProperty(choices={"movie": "movie", "series": "series"}, default="movie")
    is_active = IntegerProperty(default=1)
    is_featured = IntegerProperty(default=0)
    genres = RelationshipTo('Genre', 'IN_GENRE')
    actors = RelationshipFrom('people.models.Person', 'ACTED_IN')
    directors = RelationshipFrom('people.models.Person', 'DIRECTED')
    producers = RelationshipFrom('people.models.Person', 'PRODUCED')
    creators = RelationshipFrom('people.models.Person', 'CREATED')
    crew = RelationshipFrom('people.models.Person', 'CREW')
    ratings = RelationshipFrom('UserRating', 'RATED')
    reviews = RelationshipFrom('UserReview', 'REVIEWED')

# TV Series/Show/Drama/Soap
class Series(StructuredNode):
    uid = UniqueIdProperty()
    title = StringProperty(unique_index=True, required=True)
    description = StringProperty()
    start_year = IntegerProperty()
    end_year = IntegerProperty()
    is_active = IntegerProperty(default=1)
    is_featured = IntegerProperty(default=0)
    genres = RelationshipTo('Genre', 'IN_GENRE')
    actors = RelationshipFrom('people.models.Person', 'ACTED_IN')
    directors = RelationshipFrom('people.models.Person', 'DIRECTED')
    producers = RelationshipFrom('people.models.Person', 'PRODUCED')
    creators = RelationshipFrom('people.models.Person', 'CREATED')
    crew = RelationshipFrom('people.models.Person', 'CREW')
    seasons = RelationshipTo('Season', 'HAS_SEASON')
    ratings = RelationshipFrom('UserRating', 'RATED')
    reviews = RelationshipFrom('UserReview', 'REVIEWED')

class Season(StructuredNode):
    uid = UniqueIdProperty()
    season_number = IntegerProperty(required=True)
    series = RelationshipFrom('Series', 'HAS_SEASON')
    episodes = RelationshipTo('Episode', 'HAS_EPISODE')

class Episode(StructuredNode):
    uid = UniqueIdProperty()
    title = StringProperty(required=True)
    episode_number = IntegerProperty(required=True)
    season = RelationshipFrom('Season', 'HAS_EPISODE')
    air_date = DateProperty()
    description = StringProperty()
    is_active = IntegerProperty(default=1)
    is_featured = IntegerProperty(default=0)
    actors = RelationshipFrom('people.models.Person', 'ACTED_IN')
    directors = RelationshipFrom('people.models.Person', 'DIRECTED')
    producers = RelationshipFrom('people.models.Person', 'PRODUCED')
    creators = RelationshipFrom('people.models.Person', 'CREATED')
    crew = RelationshipFrom('people.models.Person', 'CREW')

class Genre(StructuredNode):
    uid = UniqueIdProperty()
    name = StringProperty(unique_index=True, required=True)
    films = RelationshipFrom('Film', 'IN_GENRE')

class UserRating(StructuredNode):
    uid = UniqueIdProperty()
    user_id = StringProperty(required=True)
    rating = FloatProperty(required=True)
    created_at = DateTimeProperty(default_now=True)
    film = RelationshipTo('Film', 'RATED')

class UserReview(StructuredNode):
    uid = UniqueIdProperty()
    user_id = StringProperty(required=True)
    review = StringProperty(required=True)
    created_at = DateTimeProperty(default_now=True)
    film = RelationshipTo('Film', 'REVIEWED')
    status = StringProperty(
        default='pending',
        choices={"pending": "pending", "approved": "approved", "rejected": "rejected"},
    )

class Favorite(StructuredNode):
    uid = UniqueIdProperty()
    user_id = StringProperty(required=True)
    created_at = DateTimeProperty(default_now=True)
    film = RelationshipTo('Film', 'FAVORITED')

class Watchlist(StructuredNode):
    uid = UniqueIdProperty()
    user_id = StringProperty(required=True)
    created_at = DateTimeProperty(default_now=True)
    film = RelationshipTo('Film', 'WATCHLISTED')
