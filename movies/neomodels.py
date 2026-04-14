from neomodel import StructuredNode, StringProperty, IntegerProperty, RelationshipTo, RelationshipFrom, UniqueIdProperty, DateProperty, FloatProperty

class Person(StructuredNode):
    uid = UniqueIdProperty()
    name = StringProperty(unique_index=True, required=True)
    bio = StringProperty()
    birth_date = DateProperty()
    is_active = IntegerProperty(default=1)
    is_featured = IntegerProperty(default=0)
    # Relationships to films
    acted_in_films = RelationshipTo('Film', 'ACTED_IN')
    directed_films = RelationshipTo('Film', 'DIRECTED')
    produced_films = RelationshipTo('Film', 'PRODUCED')
    created_films = RelationshipTo('Film', 'CREATED')
    crew_films = RelationshipTo('Film', 'CREW')
    # Relationships to series
    acted_in_series = RelationshipTo('Series', 'ACTED_IN')
    directed_series = RelationshipTo('Series', 'DIRECTED')
    produced_series = RelationshipTo('Series', 'PRODUCED')
    created_series = RelationshipTo('Series', 'CREATED')
    crew_series = RelationshipTo('Series', 'CREW')
    # Relationships to episodes
    acted_in_episodes = RelationshipTo('Episode', 'ACTED_IN')
    directed_episodes = RelationshipTo('Episode', 'DIRECTED')
    produced_episodes = RelationshipTo('Episode', 'PRODUCED')
    created_episodes = RelationshipTo('Episode', 'CREATED')
    crew_episodes = RelationshipTo('Episode', 'CREW')

class Film(StructuredNode):
    uid = UniqueIdProperty()
    title = StringProperty(unique_index=True, required=True)
    description = StringProperty()
    release_year = IntegerProperty()
    type = StringProperty(choices={"movie", "series"}, default="movie")
    is_active = IntegerProperty(default=1)
    is_featured = IntegerProperty(default=0)
    genres = RelationshipTo('Genre', 'IN_GENRE')
    actors = RelationshipFrom('Person', 'ACTED_IN')
    directors = RelationshipFrom('Person', 'DIRECTED')
    producers = RelationshipFrom('Person', 'PRODUCED')
    creators = RelationshipFrom('Person', 'CREATED')
    crew = RelationshipFrom('Person', 'CREW')
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
    actors = RelationshipFrom('Person', 'ACTED_IN')
    directors = RelationshipFrom('Person', 'DIRECTED')
    producers = RelationshipFrom('Person', 'PRODUCED')
    creators = RelationshipFrom('Person', 'CREATED')
    crew = RelationshipFrom('Person', 'CREW')
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
    actors = RelationshipFrom('Person', 'ACTED_IN')
    directors = RelationshipFrom('Person', 'DIRECTED')
    producers = RelationshipFrom('Person', 'PRODUCED')
    creators = RelationshipFrom('Person', 'CREATED')
    crew = RelationshipFrom('Person', 'CREW')

class Genre(StructuredNode):
    uid = UniqueIdProperty()
    name = StringProperty(unique_index=True, required=True)
    films = RelationshipFrom('Film', 'IN_GENRE')

class UserRating(StructuredNode):
    uid = UniqueIdProperty()
    user_id = StringProperty(required=True)
    rating = FloatProperty(required=True)
    film = RelationshipTo('Film', 'RATED')

class UserReview(StructuredNode):
    uid = UniqueIdProperty()
    user_id = StringProperty(required=True)
    review = StringProperty(required=True)
    film = RelationshipTo('Film', 'REVIEWED')
    status = StringProperty(default='pending', choices={'pending', 'approved', 'rejected'})

class Favorite(StructuredNode):
    uid = UniqueIdProperty()
    user_id = StringProperty(required=True)
    film = RelationshipTo('Film', 'FAVORITED')

class Watchlist(StructuredNode):
    uid = UniqueIdProperty()
    user_id = StringProperty(required=True)
    film = RelationshipTo('Film', 'WATCHLISTED')
