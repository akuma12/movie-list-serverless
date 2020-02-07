import json

from flask import Flask, request, Response
from api.models.movie import Movie

app = Flask(__name__)

schema = Movie.Schema()

@app.route('/movies', methods=['GET'])
def list_movies():
  sort = request.args.get("sort")
  sort_dir = request.args.get("sort_dir")
  movies = Movie.scan()
  result = {}
  result['movies'] = [schema.dump(movie) for movie in movies]
  if sort:
    if sort_dir:
      if sort_dir == 'desc':
        result['movies'].sort(reverse=True, key=lambda i: (i[sort]))
      else:
        result['movies'].sort(key=lambda i: (i[sort]))   
    else:
      result['movies'].sort(key=lambda i: (i[sort]))
  return Response(json.dumps(result), mimetype='application/json')

@app.route('/movie/<string:title>', methods=['GET'])
def show_movie(title):
    movie = Movie.get(title=title)
    return Response(json.dumps(schema.dump(movie)), mimetype='application/json')

@app.route('/movies', methods=['POST'])
def create_movie():
  args = request.get_json()
  movie = Movie(**args)
  movie.save()
  result = schema.dumps(movie)
  return Response(result, mimetype='application/json')

@app.route('/movie/<string:title>', methods=['PUT', 'PATCH'])
def update_movie(title):
    args = request.get_json()
    movie = Movie.get(title=title)
    movie.update(**args, conditions={'title': movie.title})
    result = schema.dumps(movie)
    return Response(result, mimetype='application/json')

@app.route('/movie/<string:title>', methods=['DELETE'])
def delete_movie(title):
    movie = Movie.get(title=title)
    movie.delete()
    return Response(dict(), mimetype='application/json')
