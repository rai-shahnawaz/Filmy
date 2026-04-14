from neomodel import StructuredNode, StringProperty, RelationshipTo, RelationshipFrom
from snippets.neomodels import Film

class MovieList(StructuredNode):
    name = StringProperty(unique_index=True, required=True)
    description = StringProperty()
    # Relationship to films in the list
    films = RelationshipTo(Film, 'INCLUDES')
