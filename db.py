#connect to DynamoDB database
import boto3


dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
table = dynamodb.Table('Shows-1iota')


def checkEvent(eventId, event):

	#check if eventId is in DB
	response = table.get_item(Key={'showId':eventId})
	print(response)
	#if not response['Item']
	