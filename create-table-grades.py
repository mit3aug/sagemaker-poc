from __future__ import print_function # Python 2/3 compatibility
import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')


table = dynamodb.create_table(
    TableName='grades',
    KeySchema=[
        {
            'AttributeName': 'teacherId',
            'KeyType': 'HASH'  #Partition key
        },
        {
            'AttributeName': 'studentId',
            'KeyType': 'RANGE'  #Sort key
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'teacherId',
            'AttributeType': 'N'
        },
        {
            'AttributeName': 'studentId',
            'AttributeType': 'N'
        },

    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 1,
        'WriteCapacityUnits': 1
    }
)

print("Table status:", table.table_status)