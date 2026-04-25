from core.neo4j_cypher_utils import run_read_cypher
from lists.neomodels import get_lists_by_owner
#
# Test Cypher utility usage
from django.test import SimpleTestCase

class CypherUtilityTests(SimpleTestCase):
	def test_get_lists_by_owner(self):
		# This test assumes at least one list exists for owner_id 'test-owner'
		try:
			results = get_lists_by_owner('test-owner')
			self.assertIsInstance(results, list)
		except Exception as e:
			self.fail(f"Cypher utility failed: {e}")
from django.test import TestCase

# Create your tests here.
