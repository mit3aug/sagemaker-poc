from __future__ import print_function # Python 2/3 compatibility
from faker import Faker
import random
import time
import json
import boto3
import decimal


dynamodb = boto3.resource('dynamodb', region_name='us-east-1')


table = dynamodb.Table('grades')

fake = Faker()
MPS = ["MP1", "MP2","MP3","MP4"]
ASSESSMENTTYPE = ["class","home","minor","major"]
snum = 90
# Grades for A Grade Students

# Classwork Grades

for mp in MPS:
    for day in range(30):
        for x in range(10):
            record={};
            record['teacherId'] = 1;
            record['studentId'] = snum+x;
            record['markingPeriod'] = mp;
            record['date']=day;
            record['assessmenttype'] = 'class';
            record['result'] = random.randint(30,60)

            table.put_item(Item=record);
            print('Record: \n' + str(record));


# Homework Grades


for mp in MPS:
    for day in range(30):
        for x in range(10):
            record={};
            record['teacherId'] = 1;
            record['studentId'] = snum+x;
            record['markingPeriod'] = mp;
            record['date']=day;
            record['assessmenttype'] = 'home';
            record['result'] = random.randint(30,100)

            table.put_item(Item=record);
            print('Record: \n' + str(record));


# Minor Assessment Grades

for mp in MPS:
    for day in range(12):
        for x in range(10):
            record={};
            record['teacherId'] = 1;
            record['studentId'] = snum+x;
            record['markingPeriod'] = mp;
            record['date']=day;
            record['assessmenttype'] = 'minor';
            record['result'] = random.randint(30,70)

            table.put_item(Item=record);
            print('Record: \n' + str(record));


# Major Assessment Grades

for mp in MPS:
    for day in range(3):
        for x in range(10):
            record={};
            record['teacherId'] = 1;
            record['studentId'] = snum+x;
            record['markingPeriod'] = mp;
            record['date']=day;
            record['assessmenttype'] = 'major';
            record['result'] = random.randint(20,70)

            table.put_item(Item=record);
            print('Record: \n' + str(record));

