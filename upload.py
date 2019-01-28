import boto3
session = boto3.Session(
    aws_access_key_id="AKIAIZOLPEVSQKIYH4JQ",
    aws_secret_access_key="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",
)



dynamodb = session.resource("dynamodb")

table = dynamodb.Table('thomais')

# Print out some data about the table.
# This will cause a request to be made to DynamoDB and its attribute
# values will be set based on the response.
print(table.creation_date_time)
