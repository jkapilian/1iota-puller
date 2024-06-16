#connect to DynamoDB database
import boto3
from boto3.dynamodb.types import TypeDeserializer
from boto3.dynamodb.types import TypeSerializer
from boto3.dynamodb.conditions import Key
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
	try:
		response = table.query(
			KeyConditionExpression=Key("EventId").eq(eventId),
			ScanIndexForward=False,
			Limit=1
		)
		if response["Count"] == 0:
			return None
		return dynamo_to_python(response["Items"][0]["Event"])
	except Exception as e:
		print(e)
		raise e



	#if response, for each value in response, chec
	#if not response['Item']

def putItem(eventId, event, cur_time):
	try:
		table.put_item(
			Item={
				'EventId': eventId,
				'Timestamp': str(cur_time),
				'Event': python_to_dynamo(event)
			}
		)
	except Exception as e:
		print(e)
