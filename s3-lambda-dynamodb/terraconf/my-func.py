import boto3
import uuid
import urllib.parse
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

endpoint_url = "http://localstack:4566"


def handler(event, context):
	try:
		dynamodb_client = boto3.client('dynamodb', region_name='us-east-1', endpoint_url=endpoint_url)

		bucket_name = event['Records'][0]['s3']['bucket']['name']
		key = event['Records'][0]['s3']['object']['key']
		key = urllib.parse.unquote_plus(key, encoding='utf-8')

		message = f"File uploaded: {key} to bucket: {bucket_name}"
		logger.info(message)

		id_db = uuid.uuid4()
		id_value = str(id_db)

		response = dynamodb_client.put_item(
			TableName='my-dynamotable',
			Item={
				'id': {'S': id_value},
				'filename': {'S': key}
			}
		)

		logger.info(f"Successfully inserted item into DynamoDB with ID: {id_value}")
		return {
			'statusCode': 200,
			'body': 'Success'
		}

	except Exception as e:
		logger.error(f"Error processing S3 event: {str(e)}")
		return {
			'statusCode': 500,
			'body': f"Error: {str(e)}"
		}

