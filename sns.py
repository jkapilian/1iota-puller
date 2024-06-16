#connect to SNS
import boto3
import secrets

client = boto3.resource('sns', region_name='us-east-2', aws_access_key_id=secrets.ACCESS_KEY, aws_secret_access_key=secrets.SECRET_ACCESS_KEY)
topic = client.Topic(f'arn:aws:sns:us-east-2:{secrets.ACCOUNT_ID}:1iota-Show-Changes')

def publish(message):
	topic.publish(Message=message)