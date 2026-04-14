from neomodel import DateTimeProperty, RelationshipTo, StringProperty, StructuredNode, UniqueIdProperty
from movies.neomodels import Film

class MovieList(StructuredNode):
    uid = UniqueIdProperty()
    name = StringProperty(unique_index=True, required=True)
    description = StringProperty()
    owner_id = StringProperty()
    status = StringProperty(default="pending")
    created_at = DateTimeProperty(default_now=True)
    # Relationship to films in the list
    films = RelationshipTo(Film, 'INCLUDES')
