# Serverless Movie API
This is a demonstration of a REST API deployed using the Serverless Framework. It uses AWS Lambda, API Gateway, and DynamoDB.

### Running Locally
* Install [Serverless](https://serverless.com/framework/docs/getting-started/)
* Install DynamoDB local by running `sls install dynamodb`
* Start DynamoDB local by running `sls start dynamodb`
* Start the development server by running `IS_OFFLINE=true sls wsgi serve`