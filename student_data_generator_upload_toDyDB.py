from __future__ import print_function # Python 2/3 compatibility
from faker import Faker
import random
import time
import json
import boto3
import decimal


dynamodb = boto3.resource('dynamodb', region_name='us-east-1')



studentList = []

fake = Faker()
for _ in range(100):
    studentList.append(fake.name())
print(studentList)


i=0;
table = dynamodb.Table('students')
for student in studentList:
    record={}
    i=i+1;
    record['studentId'] = i;
    record['name'] = student;
    record['gardianEmail'] = str(fake.email());
    record['gardianName'] = str(fake.name());
    record['gardianPhone'] = 7322015128;
    record['zipCode'] = str(fake.postalcode());
    table.put_item(Item=record);
    print('Record: \n' + str(record));


