from core.neo4j_cypher_utils import run_read_cypher
# Example: Direct Cypher query using the utility
def get_lists_by_owner(owner_id):
    query = """
    MATCH (l:MovieList) WHERE l.owner_id = $owner_id RETURN l.name, l.description
    """
    results, _ = run_read_cypher(query, {'owner_id': owner_id})
    return results
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
