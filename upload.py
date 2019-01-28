import boto3
try:
	from keys import *
except:
	ACCESS_KEY = raw_input("ACCESS KEY: ")
	SECRET_KEY = raw_input("SECRET KEY: ")

session = boto3.Session(
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
)



dynamodb = session.resource("dynamodb")

table = dynamodb.Table('thomais')

# Print out some data about the table.
# This will cause a request to be made to DynamoDB and its attribute
# values will be set based on the response.
print(table.creation_date_time)
