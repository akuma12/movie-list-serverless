import json

from flask import Flask, request, Response
from dynamorm.exceptions import ValidationError
from api.models.movie import Movie

app = Flask(__name__)

# Create the DynamoDB table if it doesn't exist
if not Movie.Table.exists:
  Movie.Table.create_table(wait=True)

@app.route('/movies', methods=['GET'])
def list_movies():
  """ Retrieve all movies from the table.
  Optionally sort by specifying query params sort_column and sort_dir.
  """
  sort_column = request.args.get('sort_column')
  sort_dir = request.args.get('sort_dir')
  result = {}
  movies = Movie.scan()
  
  result['movies'] = [movie.to_dict() for movie in movies]
  if sort_column:
    if sort_dir:
      if sort_dir == 'desc':
        result['movies'].sort(reverse=True, key=lambda i: (i[sort_column]))
      else:
        result['movies'].sort(key=lambda i: (i[sort_column]))   
    else:
      result['movies'].sort(key=lambda i: (i[sort_column]))

  return Response(json.dumps(result), mimetype='application/json')

@app.route('/movies/<string:title>', methods=['GET'])
def show_movie(title):
  """ Retrieve a specific movie by title. """
  movie = Movie.get(title=title)
  if movie:
    return Response(json.dumps(movie.to_dict()), mimetype='application/json')
  else:
    return Response("{}", mimetype='application/json', status=404)

@app.route('/movies', methods=['POST'])
def create_movie():
  """ Create a new movie. """
  data = request.get_json()
  try:
    movie = Movie(**data)
    poster = movie.get_omdb_poster()
    if poster:
      movie.poster = poster
    movie.save()
    return Response(json.dumps(movie.to_dict()), mimetype='application/json', status=201)
  except ValidationError as e:
    return Response(json.dumps(e.errors), mimetype='application/json', status=400)

@app.route('/movies/<string:title>', methods=['PUT', 'PATCH'])
def update_movie(title):
  """ Update a movie. """
  try:
    data = request.get_json(force=True)
  except json.decoder.JSONDecodeError as e:
    data = request.form
  
  movie = Movie.get(title=title)

  try:
    if movie:
      movie.update(**data)
      return Response(json.dumps(movie.to_dict()), mimetype='application/json')
    else:
      return Response("{}", mimetype='application/json', status=404)
  except ValidationError as e:
    return Response(json.dumps(e.errors), mimetype='application/json', status=400)

@app.route('/movies/<string:title>', methods=['DELETE'])
def delete_movie(title):
  """ Delete a movie. """
    movie = Movie.get(title=title)
    if movie:
      movie.delete()
    return Response("{}", mimetype='application/json', status=204)
