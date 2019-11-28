from __future__ import print_function # Python 2/3 compatibility
import csv

import boto3
import numpy as np
from faker import Faker
import random
import statistics


numberOfStudentsData = 1000
data_partition_names = ['train', 'verify', 'test']
noiselevel = 5


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



    # if data_partition_name != 'test':
        examples = np.insert(students, 0, labels, axis=1)
    # else:
    #     examples = students

    # print(examples)

    np.random.shuffle(examples)

    # print(examples)

    np.savetxt('data.csv', examples, delimiter=',')

    region='us-east-1'

    bucket='mitesh-sagemaker-11142019' # Replace with your s3 bucket name
    prefix = 'sagemaker/xgboost-students-grades' # Used as part of the path in the bucket where you store data
    bucket_path = 'https://s3-{}.amazonaws.com/{}'.format(region, bucket) # The URL to access the bucket

    key = "{}/{}/examples".format(prefix, data_partition_name)
    url = 's3://{}/{}'.format(bucket, key)
    boto3.Session().resource('s3').Bucket(bucket).Object(key).upload_file('data.csv')
    print('Done writing to {}'.format(url))