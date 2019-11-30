import json

import csv

import boto3
import numpy as np
from faker import Faker
import random
import statistics
import os



region=os.environ["REGION"]
bucket=os.environ["BUCKETNAME"] # Replace with your s3 bucket name
prefix = os.environ["PREFIX"] # Used as part of the path in the bucket where you store data
bucket_path = 'https://s3-{}.amazonaws.com/{}'.format(region, bucket) # The URL to access the bucket


def lambda_handler(event, context):
    # Preparing Data Reading from Lambda Event
    numberOfStudentsData = int(event['numberOfStudents'])
    data_partition_names = ['train', 'verify', 'test']
    noiselevel = int(event['noiseLevel'])

    messages={}

    for data_partition_name in data_partition_names:
        faker = Faker()
        students = []
        labels = []
        x=0

        # Students showing Consistently high effort.
        for j in range(numberOfStudentsData):
            features = []
            x=x+1
            # features.append(x)
            # Class work grades
            features.append(random.randint(90,100))
            features.append(random.randint(90,100))
            features.append(random.randint(90,100))
            features.append(random.randint(90,100))
            features.append(random.randint(90,100))
            # Home work grades
            features.append(random.randint(90,100))
            features.append(random.randint(90,100))
            features.append(random.randint(90,100))
            features.append(random.randint(90,100))

            # Minor Assessments Grades
            features.append(random.randint(90,100))
            features.append( random.randint(90,100))
            features.append( random.randint(90,100))

            # Major Assessment Grades
            features.append(random.randint(90,100))

            if j % noiselevel == 0:
                features = []
                # Class work grades
                features.append(random.randint(20,100))
                features.append(random.randint(20,100))
                features.append(random.randint(20,100))
                features.append(random.randint(20,100))
                features.append(random.randint(20,100))
                # Home work grades
                features.append(random.randint(20,100))
                features.append(random.randint(20,100))
                features.append(random.randint(20,100))
                features.append(random.randint(20,100))

                # Minor Assessments Grades
                features.append(random.randint(20,100))
                features.append( random.randint(20,100))
                features.append( random.randint(20,100))

                # Major Assessment Grades
                features.append(random.randint(20,100))

            # Calculating Grades
            grade = int( 0.10 * statistics.mean(features[0:4])) \
                    + int(0.10 * statistics.mean(features[5:8])) \
                    + int(0.35 * statistics.mean(features[9:11])) \
                    + int(0.45 * features[12])

            features.append(grade)
            students.append(features)
            labels.append(1)
            # print(grade)
            # print('Record: \n' + str(features))

            # Students Showing improvement/good effort but the student is finding work difficult.
        for j in range(numberOfStudentsData):
            features = []
            x=x+1
            # features.append(x)
            # Class work grades
            features.append(random.randint(70,80))
            features.append(random.randint(70,80))
            features.append(random.randint(80,90))
            features.append(random.randint(90,95))
            features.append(random.randint(80,95))
            # Home work grades
            features.append(random.randint(70,95))
            features.append(random.randint(80,95))
            features.append(random.randint(90,95))
            features.append(random.randint(70,95))

            # Minor Assessments Grades
            features.append(random.randint(70,80))
            features.append( random.randint(70,90))
            features.append( random.randint(70,90))

            # Major Assessment Grades
            features.append(random.randint(70,90))

            if j % noiselevel == 0:
                features = []
                # Class work grades
                features.append(random.randint(20,100))
                features.append(random.randint(20,100))
                features.append(random.randint(20,100))
                features.append(random.randint(20,100))
                features.append(random.randint(20,100))
                # Home work grades
                features.append(random.randint(20,100))
                features.append(random.randint(20,100))
                features.append(random.randint(20,100))
                features.append(random.randint(20,100))

                # Minor Assessments Grades
                features.append(random.randint(20,100))
                features.append( random.randint(20,100))
                features.append( random.randint(20,100))

                # Major Assessment Grades
                features.append(random.randint(20,100))

            # Calculating Grades
            grade = int( 0.10 * statistics.mean(features[0:4])) \
                    + int(0.10 * statistics.mean(features[5:8])) \
                    + int(0.35 * statistics.mean(features[9:11])) \
                    + int(0.45 * features[12])

            features.append(grade)
            students.append(features)
            labels.append(2)
            # print(grade)
            # print('Record: \n' + str(features))


        # Students Not Utilizes class time productively and Class work is not satisfactory. finding work difficult.
        for j in range(numberOfStudentsData):
            features = []
            x=x+1
            # features.append(x)
            # Class work grades
            features.append(random.randint(40,70))
            features.append(random.randint(40,70))
            features.append(random.randint(40,80))
            features.append(random.randint(40,70))
            features.append(random.randint(40,70))
            # Home work grades
            features.append(random.randint(40,70))
            features.append(random.randint(40,70))
            features.append(random.randint(40,70))
            features.append(random.randint(40,70))

            # Minor Assessments Grades
            features.append(random.randint(40,70))
            features.append( random.randint(40,70))
            features.append( random.randint(40,70))

            # Major Assessment Grades
            features.append(random.randint(40,70))

            if j % noiselevel == 0:
                features = []
                # Class work grades
                features.append(random.randint(20,100))
                features.append(random.randint(20,100))
                features.append(random.randint(20,100))
                features.append(random.randint(20,100))
                features.append(random.randint(20,100))
                # Home work grades
                features.append(random.randint(20,100))
                features.append(random.randint(20,100))
                features.append(random.randint(20,100))
                features.append(random.randint(20,100))

                # Minor Assessments Grades
                features.append(random.randint(20,100))
                features.append( random.randint(20,100))
                features.append( random.randint(20,100))

                # Major Assessment Grades
                features.append(random.randint(20,100))

            # Calculating Grades
            grade = int( 0.10 * statistics.mean(features[0:4])) \
                    + int(0.10 * statistics.mean(features[5:8])) \
                    + int(0.35 * statistics.mean(features[9:11])) \
                    + int(0.45 * features[12])

            features.append(grade)
            students.append(features)
            labels.append(3)
            # print(grade)
            # print('Record: \n' + str(features))


        # Students Good in Class work but home work not satisfactorily. finding work difficult.
        for j in range(numberOfStudentsData):
            features = []
            x=x+1
            # features.append(x)
            # Class work grades
            features.append(random.randint(80,90))
            features.append(random.randint(80,90))
            features.append(random.randint(80,90))
            features.append(random.randint(80,90))
            features.append(random.randint(80,90))
            # Home work grades
            features.append(random.randint(40,70))
            features.append(random.randint(40,80))
            features.append(random.randint(40,70))
            features.append(random.randint(40,70))

            # Minor Assessments Grades
            features.append(random.randint(60,90))
            features.append( random.randint(70,90))
            features.append( random.randint(80,90))

            # Major Assessment Grades
            features.append(random.randint(70,90))

            if j % noiselevel == 0:
                features = []
                # Class work grades
                features.append(random.randint(20,100))
                features.append(random.randint(20,100))
                features.append(random.randint(20,100))
                features.append(random.randint(20,100))
                features.append(random.randint(20,100))
                # Home work grades
                features.append(random.randint(20,100))
                features.append(random.randint(20,100))
                features.append(random.randint(20,100))
                features.append(random.randint(20,100))

                # Minor Assessments Grades
                features.append(random.randint(20,100))
                features.append( random.randint(20,100))
                features.append( random.randint(20,100))

                # Major Assessment Grades
                features.append(random.randint(20,100))

            # Calculating Grades
            grade = int( 0.10 * statistics.mean(features[0:4])) \
                    + int(0.10 * statistics.mean(features[5:8])) \
                    + int(0.35 * statistics.mean(features[9:11])) \
                    + int(0.45 * features[12])

            features.append(grade)
            students.append(features)
            labels.append(4)

            # print(grade)
            # print('Record: \n' + str(features))



        # Students anxiety issue during exam .
        for j in range(numberOfStudentsData):
            features = []
            x=x+1
            # features.append(x)
            # Class work grades
            features.append(random.randint(90,100))
            features.append(random.randint(90,100))
            features.append(random.randint(90,100))
            features.append(random.randint(90,100))
            features.append(random.randint(90,100))
            # Home work grades
            features.append(random.randint(90,100))
            features.append(random.randint(90,100))
            features.append(random.randint(90,100))
            features.append(random.randint(90,100))

            # Minor Assessments Grades
            features.append(random.randint(60,80))
            features.append( random.randint(60,80))
            features.append( random.randint(60,80))

            # Major Assessment Grades
            features.append(random.randint(60,70))

            if j % noiselevel == 0:
                features = []
                # Class work grades
                features.append(random.randint(20,100))
                features.append(random.randint(20,100))
                features.append(random.randint(20,100))
                features.append(random.randint(20,100))
                features.append(random.randint(20,100))
                # Home work grades
                features.append(random.randint(20,100))
                features.append(random.randint(20,100))
                features.append(random.randint(20,100))
                features.append(random.randint(20,100))

                # Minor Assessments Grades
                features.append(random.randint(20,100))
                features.append( random.randint(20,100))
                features.append( random.randint(20,100))

                # Major Assessment Grades
                features.append(random.randint(20,100))

            # Calculating Grades
            grade = int( 0.10 * statistics.mean(features[0:4])) \
                    + int(0.10 * statistics.mean(features[5:8])) \
                    + int(0.35 * statistics.mean(features[9:11])) \
                    + int(0.45 * features[12])

            features.append(grade)
            students.append(features)
            labels.append(5)

            # print(grade)
            # print('Record: \n' + str(features))

            #
            # print('Labels ' + str(labels))
            # print('Students ' + str(students))

        # uploading generated data to S3

        examples = np.insert(students, 0, labels, axis=1)
        np.random.shuffle(examples)
        # print(examples)
        np.savetxt('/tmp/data.csv', examples, delimiter=',')

        key = "{}/{}/examples".format(prefix, data_partition_name)
        url = 's3://{}/{}'.format(bucket, key)
        boto3.Session().resource('s3').Bucket(bucket).Object(key).upload_file('/tmp/data.csv')
        print('Done writing {}, # of records {} to {}'.format(data_partition_name,examples.shape,url))
        messages[data_partition_name]=url

    return {
        'statusCode': 200,
        'body': json.dumps(messages)
    }
