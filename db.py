#connect to DynamoDB database
import boto3
from boto3.dynamodb.types import TypeDeserializer
from boto3.dynamodb.types import TypeSerializer
import secrets


dynamodb = boto3.resource('dynamodb', region_name='us-east-2', aws_access_key_id=secrets.ACCESS_KEY, aws_secret_access_key=secrets.SECRET_ACCESS_KEY)
table = dynamodb.Table('Shows-1iota')

"""
eventId: {
	time1: {
		event details
	}
	time2: {
		event details
	}
}
"""

def dynamo_to_python(dynamo_object: dict) -> dict:
    deserializer = TypeDeserializer()
    return {
        k: deserializer.deserialize(v) 
        for k, v in dynamo_object.items()
    }  
  
def python_to_dynamo(python_object: dict) -> dict:
    serializer = TypeSerializer()
    return {
        k: serializer.serialize(v)
        for k, v in python_object.items()
    }

def checkEvent(eventId):

	#check if eventId is in DB
	response = table.get_item(Key={'EventId':eventId})
	try:
		return response["Item"]
	except:
		return None



	#if response, for each value in response, chec
	#if not response['Item']

def putItem(eventId, event):

	cur_time = "0"
	table.put_item(
		Item={
			'EventId': eventId,
			'time': {
				cur_time: python_to_dynamo(event)
			},
		}
	)

def updateItem():
	pass