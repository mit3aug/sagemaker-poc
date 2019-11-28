#!/usr/bin/env python3

import boto3
from faker import Faker
import random
import time
import json

DeliveryStreamName = 'patient-data-kfh'
client = boto3.client('firehose')
fake = Faker()

with open('./data.txt') as f:
    drug = f.read().split('\n')

with open('./risky.txt') as f1:
    riskyList = f1.read().split('\n')

with open('./pharmacy.txt') as f1:
    pharmacyList = f1.read().split('\n')

providerList = []

fake1 = Faker()
for _ in range(1000):
  providerList.append("Dr. " + fake1.name())
print(providerList)


record = {}
while True:

  record['age'] = random.randint(18,90);
  record['height'] = random.randint(60, 84);
  record['zipCode'] = str(fake.postalcode());
  record['email'] = str(fake.email());
  record['ssn'] = str(fake.ssn());
  gender = random.randint(0,1);
  record['gender'] = random.randint(0,1);

  record['patientCondition'] = "normal";
  record['dosage'] = random.randint(5,10)
  record['drugCombo'] = 0;
  record['pharmacy'] = random.choice(pharmacyList);

  record['providerRiskRating'] = random.randint(20,50)
  record['patientRiskRating'] = random.randint(20,50)

  record['patientName'] = fake.name();
  if random.randint(1,1000) < 5:
        record['drug'] = random.choice(riskyList);
        randNum = random.randint(1,100)
        record['providerName'] = providerList[randNum];
        record['dosage'] = random.randint(20,25)
        record['patientCondition'] = "dead"
        record['drugCombo'] = 1;
        record['providerRiskRating'] =  random.randint(90,100)
        record['patientRiskRating'] =  random.randint(90,100)
  else:
        record['providerRiskRating'] =  random.randint(50,75)
        record['patientRiskRating'] =  random.randint(50,75)
        record['drug'] = random.choice(drug);
        record['providerName'] = random.choice(providerList)
        ri = random.randint(1, 100)
        if (ri < 20):
            record['dosage'] = random.randint(15,20)
            record['drugCombo'] = 1;
            record['patientCondition'] = "critical";
            record['providerRiskRating'] = random.randint(80,90);
            record['patientRiskRating'] = random.randint(80,90);
        elif(ri > 20 and ri < 40):
            record['drugCombo'] = 1;
            record['patientCondition'] = "severe";
            record['dosage'] = random.randint(10,15)
            record['patientRiskRating'] = random.randint(70,80)
            record['providerRiskRating'] = random.randint(70,80)
        else:
            record['patientCondition'] = "normal";
            record['dosage'] = random.randint(5,10)
            record['drugCombo'] = 0;
            record['providerRiskRating'] = random.randint(30,70)
            record['patientRiskRating'] = random.randint(30,70)


  record['timestamp'] = time.time();

  response = client.put_record(
    DeliveryStreamName=DeliveryStreamName,
    Record={
    'Data': json.dumps(record)
    }
  )
  print('Record: \n' + str(record));