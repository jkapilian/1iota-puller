#connect to DynamoDB database
import boto3
import secrets


dynamodb = boto3.resource('dynamodb', region_name='us-east-2', aws_access_key_id=secrets.ACCESS_KEY, aws_secret_access_key=secrets.SECRET_ACCESS_KEY)
table = dynamodb.Table('Shows-1iota')


def checkEvent(eventId, event):

	#check if eventId is in DB
	response = table.get_item(Key={'showId':eventId})
	print(response)
	#if not response['Item']
	