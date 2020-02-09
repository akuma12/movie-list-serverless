# Serverless Movie API
This is a demonstration of a REST API deployed using the Serverless Framework. It uses AWS Lambda, API Gateway, and DynamoDB.

### Requirements
* Python 3.8
* NPM

### Running Locally
* Install [Serverless](https://serverless.com/framework/docs/getting-started/)
* Install DynamoDB local by running `sls install dynamodb`
* Start DynamoDB local by running `sls start dynamodb`
* Start the development server by running `IS_OFFLINE=true sls wsgi serve`

### Deploying
* Set up your AWS credentials
* Run `sls deploy`
* Authentication key will be provided in the Serverless output

### Endpoints
```
GET /movies application/json
params:
  sort_column: column name to sort by ['title', 'format' ,'length', 'release_year', 'rating']
  sort_dir: sort direction ['asc', 'desc'] (default 'asc')
Returns all movies
```

```
GET /movies/<title:string> application/json
params:
  title: URL formatted title
Returns a specific movie
```

```
POST /movies application/json
Authentication: 
  x-api-key: <api_key>
body: application/json
{
  "title": <String [1-50]>,
  "format": <String ["VHS", "DVD", "Streaming"]>
  "length" <Integer [1-500]>,
  "release_year": <Integer [1800-2100]>
  "rating": <Integer [1-5]>
}
Creates a new movie
```

```
PUT /movies/<title:string> application/json
Authentication: 
  x-api-key: <api_key>
body: application/json
{
  "title": <String [1-50]>,
  "format": <String ["VHS", "DVD", "Streaming"]>
  "length" <Integer [1-500]>,
  "release_year": <Integer [1800-2100]>
  "rating": <Integer [1-5]>
}
Updates a movie
```

```
DELETE /movies/<title:string> application/json
Authentication: 
  x-api-key: <api_key>
Deletes a movie
```

### Testing
`pip install pytest`
Run `pytest` from the root directory