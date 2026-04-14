# Person model moved from movies/neomodels.py
from neomodel import StructuredNode, StringProperty, IntegerProperty, RelationshipTo, UniqueIdProperty, DateProperty

class Person(StructuredNode):
	uid = UniqueIdProperty()
	name = StringProperty(unique_index=True, required=True)
	bio = StringProperty()
	birth_date = DateProperty()
	is_active = IntegerProperty(default=1)
	is_featured = IntegerProperty(default=0)
	# Relationships to films
	acted_in_films = RelationshipTo('movies.neomodels.Film', 'ACTED_IN')
	directed_films = RelationshipTo('movies.neomodels.Film', 'DIRECTED')
	produced_films = RelationshipTo('movies.neomodels.Film', 'PRODUCED')
	created_films = RelationshipTo('movies.neomodels.Film', 'CREATED')
	crew_films = RelationshipTo('movies.neomodels.Film', 'CREW')
	# Relationships to series
	acted_in_series = RelationshipTo('movies.neomodels.Series', 'ACTED_IN')
	directed_series = RelationshipTo('movies.neomodels.Series', 'DIRECTED')
	produced_series = RelationshipTo('movies.neomodels.Series', 'PRODUCED')
	created_series = RelationshipTo('movies.neomodels.Series', 'CREATED')
	crew_series = RelationshipTo('movies.neomodels.Series', 'CREW')
	# Relationships to episodes
	acted_in_episodes = RelationshipTo('movies.neomodels.Episode', 'ACTED_IN')
	directed_episodes = RelationshipTo('movies.neomodels.Episode', 'DIRECTED')
	produced_episodes = RelationshipTo('movies.neomodels.Episode', 'PRODUCED')
	created_episodes = RelationshipTo('movies.neomodels.Episode', 'CREATED')
	crew_episodes = RelationshipTo('movies.neomodels.Episode', 'CREW')
# People app models placeholder
