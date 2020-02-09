import os
import tempfile
import json

import pytest

os.environ['IS_OFFLINE'] = 'true'
os.environ['MOVIES_TABLE'] = 'movies-table-test'

from api import app

@pytest.fixture(scope='session', autouse=True)
def client():
  app.app.config['TESTING'] = True

  with app.app.test_client() as client:
    yield client

  app.Movie.Table.delete(wait=True)

def test_empty_db(client):
  """Start with a blank database."""

  rv = client.get('/movies')
  data = json.loads(rv.data)
  assert not data['movies']

def test_create_movie(client):
  """Create a new movie"""

  data = {
    "title": "Top Gun",
    "release_year": 1986,
    "length": 110,
    "format": "VHS",
    "rating": 4
  }

  rv = client.post('/movies', data=json.dumps(data), content_type="application/json")

  response_data = rv.json

  assert all(item in response_data.items() for item in data.items())

def test_get_movie(client):
  """Get a specific movie"""
  rv = client.get('/movie/Top%20Gun', content_type="application/json")

  response_data = rv.json

  data = {
    "title": "Top Gun",
    "release_year": 1986,
    "length": 110,
    "format": "VHS",
    "rating": 4
  }

  assert all(item in response_data.items() for item in data.items())

def test_update_movie(client):
  """Update a movie"""

  data = {
    "rating": 5
  }

  rv = client.put('/movie/Top%20Gun', data=json.dumps(data), content_type="application/json")

  response_data = rv.json

  data = {
    "title": "Top Gun",
    "release_year": 1986,
    "length": 110,
    "format": "VHS",
    "rating": 5
  }

  assert all(item in response_data.items() for item in data.items())

def test_delete_movie(client):
  """Test deleting a movie"""
  rv = client.delete('/movie/Top%20Gun', content_type="application/json")

  get_rv = client.get('/movie/Top%20Gun', content_type="application/json")

  assert rv.status == '204 NO CONTENT'
  assert get_rv.status == '404 NOT FOUND'


def test_404(client):
  """Make sure we get a 404 on a non-existent movie"""
  rv = client.get('/movie/FooBar', content_type="application/json")
  assert rv.status == '404 NOT FOUND'