"""Test Descriptr JSON API."""

from apipkg import create_app
import flask_unittest
import json
import os


""" Change working directory to one level above here """
os.chdir(os.path.dirname(os.path.dirname(__file__)))


class TestDescriptrApi(flask_unittest.ClientTestCase):
    """A unittest class whose "test_*" methods will be called."""
    app = create_app()

    def test_root(self, client):
        """Test that the root endpoint returns the correct response."""
        ret = client.get("/")
        self.assertIn('available_endpoints', ret.json)
        self.assertIn('/search', ret.json["available_endpoints"])

    def test_search_get(self, client):
        """Test that the root endpoint returns the correct response."""
        ret = client.get("/search")
        self.assertIn('available_filters', ret.json)
        self.assertNotEqual(len(ret.json["available_filters"]), 0)

    def test_search_post_simple(self, client):
        """Test POSTing a simple search and getting correct response."""
        ret = client.post("/search", json=dict(number=dict(query="2750", comparison='=')))
        ret_json = ret.get_json()
        self.assertIn('courses', ret_json)
        self.assertGreater(len(ret_json["courses"]), 0)

    def test_search_post_complex(self, client):
        """Test POSTing a complex search and getting correct response."""
        ret = client.post("/search", json=dict(code=dict(query='cis', comparison='='), level=dict(query="1", comparison='=')))
        ret_json = ret.get_json()
        self.assertIn('courses', ret_json)
        self.assertGreater(len(ret.json["courses"]), 0)
    
    def test_prerequisite_search(self, client):
        """Test that the prerequisite search endpoint returns the correct response."""
        ret = client.get("/prerequisite/cis-2750")
        ret_json = ret.get_json().get('courses', None)

        self.assertIsNotNone(ret_json)

        root_course = json.loads(ret_json['course'])
        self.assertEqual(root_course['code'], "CIS")
        self.assertEqual(root_course['number'], "2750")

        def courseIdMapper(prereq):
            course = json.loads(prereq['course'])
            return f"{course['code']}*{course['number']}"

        prereq_ids = list(map(courseIdMapper, ret_json['prerequisites']))
        self.assertIn("CIS*2430", prereq_ids)
        self.assertIn("CIS*2520", prereq_ids)

    def test_prerequisite_search_not_found(self, client):
        """Test that the prerequisite search endpoint returns an error if root course not found."""
        ret = client.get("/prerequisite/dne-1234")
        ret_json = ret.get_json()

        self.assertEqual(len(ret_json['courses']), 0)
        self.assertIsNotNone(ret_json['error'])