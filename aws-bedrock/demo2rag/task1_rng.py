import sys, os, json
import boto3, botocore

from botocore.exceptions import ClientError
from botocore.client import Config

region_name = "us-east-1"
model_id = "amazon.nova-micro-v1:0"
model_arn = f'arn:aws:bedrock:{region_name}::foundation-model/{model_id}'

session = boto3.Session()

sts_client = boto3.client('sts', config=Config(signature_version='s3v4'))
boto3_session = boto3.Session()

bedrock_config = Config(
    region_name=region_name,
    retries={
        'max_attempts': 0,
        'mode': 'standard'
    },
    connect_timeout=125,
    read_timeout=5,
    max_pool_connections=10,
    user_agent_extra='demo2rag',)

bedrock_agent_client = boto3_session.client("bedrock-agent-runtime", config=bedrock_config)
bedrock_client = session.client("bedrock-agent")

try:
    response = bedrock_client.list_knowledge_bases(maxResults=1)

    print(response)

except ClientError as e:
    print(e)

query = "Provide a summary of consolidated statements of cash flows of AnyCompany Financial for the fiscal years ended December 31, 2019?"
response = bedrock_agent_client.retrieve_and_generate(
    input={
        "text": query
    },
    retrieveAndGenerateConfiguration={
        "type": "KNOWLEDGE_BASE",
        "knowledgeBaseConfiguration": {
            'knowledgeBaseId': kb_id,
            "modelArn": model_arn,
            "retrievalConfiguration": {
                "vectorSearchConfiguration": {
                    "numberOfResults":3
                } 
            }
        }
    }
)

print(response['output']['text'],end='\n'*2)