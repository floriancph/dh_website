import boto3
import base64
from botocore.exceptions import ClientError
import json

def get_secret(secret_name):
    region_name = "eu-central-1"

    try:
        # Create a Secrets Manager client
        session = boto3.session.Session()
        client = session.client(
            service_name='secretsmanager',
            region_name=region_name
        )

        # In this sample we only handle the specific exceptions for the 'GetSecretValue' API.
        # See https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        # We rethrow the exception by default.

        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )

        answer = json.loads(get_secret_value_response['SecretString'])
    except:
        answer = {'user': 'fail'}

    return answer
            
