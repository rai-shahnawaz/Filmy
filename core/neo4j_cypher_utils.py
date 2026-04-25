"""
core/neo4j_cypher_utils.py

Utility module to encapsulate Cypher query execution for hybrid Neomodel/Cypher usage.
"""
import logging
from neomodel import db
from neomodel.exceptions import CypherException

logger = logging.getLogger(__name__)


def run_cypher(query, params=None, read_only=True):
    """
    Execute a Cypher query using Neomodel's db.cypher_query.
    Args:
        query (str): Cypher query string
        params (dict): Parameters for the query
        read_only (bool): If True, runs as a read query
    Returns:
        tuple: (results, meta)
    Raises:
        CypherException: If the query fails
    """
    try:
        results, meta = db.cypher_query(query, params or {}, resolve_objects=False)
        logger.debug(f"Cypher executed: {query} | params: {params} | meta: {meta}")
        return results, meta
    except CypherException as e:
        logger.error(f"Cypher query failed: {query} | params: {params} | error: {e}")
        raise


def run_write_cypher(query, params=None):
    """
    Execute a write Cypher query (CREATE, MERGE, etc).
    """
    return run_cypher(query, params, read_only=False)


def run_read_cypher(query, params=None):
    """
    Execute a read Cypher query (MATCH, RETURN, etc).
    """
    return run_cypher(query, params, read_only=True)

