import os
from dynamorm import DynaModel
from marshmallow import fields, validate

IS_OFFLINE = os.environ.get('IS_OFFLINE')

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
    title = fields.Str(validate=validate.Length(1, 50))
    format = fields.Str(validate=validate.OneOf(['VHS', 'DVD', 'Streaming']))
    length = fields.Int(validate=validate.Range(1, 500))
    release_year = fields.Int(validate=validate.Range(1800, 2100))
    rating = fields.Int(validate=validate.Range(1, 5))
