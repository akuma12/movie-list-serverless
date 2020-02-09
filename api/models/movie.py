import os
import requests
import json
import boto3
from dynamorm import DynaModel
from marshmallow import fields, validate

IS_OFFLINE = os.environ.get('IS_OFFLINE')
OMDB_API_PARAM = os.environ.get('OMDB_API_PARAM')
SSM = boto3.client('ssm')

class Movie(DynaModel):

  class Table:
    name = os.environ['MOVIES_TABLE']
    hash_key = 'title'
    read = 10
    write = 10
    if IS_OFFLINE:
      session_kwargs = {
          'region_name': 'us-east-2'
      }
      resource_kwargs = {
          'endpoint_url': 'http://localhost:8000'
      }
  
  class Schema:
    title = fields.Str(
      required=True,
      validate=validate.Length(1, 50),
      error_messages={"required": {"message": "title required", "code": 400}}
    )
    format = fields.Str(
      required=True,
      validate=validate.OneOf(['VHS', 'DVD', 'Streaming']),
      error_messages={"required": {"message": "format required", "code": 400}}
    )
    length = fields.Int(
      required=True,
      validate=validate.Range(1, 500),
      error_messages={"required": {"message": "Length required", "code": 400}}
    )
    release_year = fields.Int(
      required=True,
      validate=validate.Range(1800, 2100),
      error_messages={"required": {"message": "release_year required", "code": 400}}
    )
    rating = fields.Int(
      required=True,
      validate=validate.Range(1, 5),
      error_messages={"required": {"message": "rating required", "code": 400}}
    )
    poster = fields.Url()

  def get_omdb_api_key(self):
    """ Get the OMDB API Key from Parameter Store """
    try:
      api_key_response = SSM.get_parameter(Name=OMDB_API_PARAM)
      if api_key_response:
        return api_key_response['Parameter']['Value']
    except Exception as e:
      print(f"Could not retrieve API key {e}")
      return None

    return None

  def get_omdb_poster(self):
    """ Get the Poster image from OMDB """
    omdb_api_key = self.get_omdb_api_key()
    if omdb_api_key:
      omdb_url = f"http://www.omdbapi.com/?apikey={omdb_api_key}&t={self.title}"
      omdb_movie_response = requests.get(omdb_url)
      if omdb_movie_response.ok:
        try:
          omdb_movie = omdb_movie_response.json()
          if 'Poster' in omdb_movie:
            return omdb_movie['Poster']
          else:
            return None
        except json.decoder.JSONDecodeError:
          return None
    else:
      return None

    
