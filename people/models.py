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
# People app models placeholder
