{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 204,
   "metadata": {},
   "outputs": [],
   "source": [
    "import os\n",
    "import boto3\n",
    "import re\n",
    "import copy\n",
    "import time\n",
    "from time import gmtime, strftime\n",
    "from sagemaker import get_execution_role\n",
    "\n",
    "role = get_execution_role()\n",
    "\n",
    "region = boto3.Session().region_name\n",
    "\n",
    "bucket='mitesh-sagemaker-11142019' # Replace with your s3 bucket name\n",
    "\n",
    "bucket_path = 'https://s3-{}.amazonaws.com/{}'.format(region,bucket) # The URL to access the bucket"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 205,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "S3 location of train data s3://mitesh-sagemaker-11142019/sagemaker/xgboost-students-grades/train\n",
      "S3 location of validation_data  s3://mitesh-sagemaker-11142019/sagemaker/xgboost-students-grades/verify\n",
      "CPU times: user 125 µs, sys: 18 µs, total: 143 µs\n",
      "Wall time: 106 µs\n"
     ]
    }
   ],
   "source": [
    "%%time \n",
    "import pickle, gzip, urllib.request, json\n",
    "import numpy as np\n",
    "\n",
    "prefix = 'sagemaker/xgboost-students-grades' \n",
    "\n",
    "data_types = ['train', 'verify', 'test']\n",
    "\n",
    "train_data = 's3://{}/{}/{}'.format(bucket, prefix, 'train')\n",
    "\n",
    "validation_data = 's3://{}/{}/{}'.format(bucket, prefix, 'verify')\n",
    "\n",
    "test_data = 's3://{}/{}/{}'.format(bucket, prefix, 'test')\n",
    "\n",
    "s3_data_sets = [s3_train_data, s3_validation_data, s3_test_data]\n",
    "\n",
    "s3_output_location = 's3://{}/{}/{}'.format(bucket, prefix, 'xgboost_model_sdk')\n",
    "print(\"S3 location of train data {}\".format(train_data))\n",
    "print(\"S3 location of validation_data  {}\".format(validation_data))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 206,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Reading sample train data\n",
      "-->  Grade [100.  90.  94.  97.  99. 100.  79.  75.  79.  62.  71.] labled as 3\n",
      "-->  Grade [94. 88. 86. 84. 92. 72. 78. 89. 78. 87. 84.] labled as 4\n",
      "-->  Grade [84. 83. 64. 47. 44. 67. 82. 87. 82. 72. 74.] labled as 1\n",
      "-->  Grade [46. 45. 61. 57. 44. 59. 49. 62. 49. 44. 48.] labled as 3\n",
      "-->  Grade [64. 59. 58. 50. 57. 60. 61. 68. 66. 65. 62.] labled as 2\n",
      "-->  Grade [ 93.  95.  94. 100.  94.  94.  91.  98.  90.  99.  95.] labled as 2\n",
      "-->  Grade [91. 82. 94. 90. 92. 70. 78. 87. 89. 73. 77.] labled as 2\n",
      "-->  Grade [ 97.  90.  93. 100.  95.  98.  65.  66.  80.  68.  70.] labled as 4\n",
      "-->  Grade [83. 81. 61. 72. 62. 45. 65. 78. 84. 90. 79.] labled as 3\n",
      "-->  Grade [100.  92. 100.  99.  99.  94.  93.  96. 100.  97.  94.] labled as 1\n",
      "Reading sample verify data\n",
      "-->  Grade [100.  90.  94.  97.  99. 100.  79.  75.  79.  62.  71.] labled as 2\n",
      "-->  Grade [94. 88. 86. 84. 92. 72. 78. 89. 78. 87. 84.] labled as 3\n",
      "-->  Grade [84. 83. 64. 47. 44. 67. 82. 87. 82. 72. 74.] labled as 2\n",
      "-->  Grade [46. 45. 61. 57. 44. 59. 49. 62. 49. 44. 48.] labled as 5\n",
      "-->  Grade [64. 59. 58. 50. 57. 60. 61. 68. 66. 65. 62.] labled as 1\n",
      "-->  Grade [ 93.  95.  94. 100.  94.  94.  91.  98.  90.  99.  95.] labled as 1\n",
      "-->  Grade [91. 82. 94. 90. 92. 70. 78. 87. 89. 73. 77.] labled as 4\n",
      "-->  Grade [ 97.  90.  93. 100.  95.  98.  65.  66.  80.  68.  70.] labled as 1\n",
      "-->  Grade [83. 81. 61. 72. 62. 45. 65. 78. 84. 90. 79.] labled as 2\n",
      "-->  Grade [100.  92. 100.  99.  99.  94.  93.  96. 100.  97.  94.] labled as 5\n",
      "Reading sample test data\n",
      "-->  Grade [100.  90.  94.  97.  99. 100.  79.  75.  79.  62.  71.] labled as 1\n",
      "-->  Grade [94. 88. 86. 84. 92. 72. 78. 89. 78. 87. 84.] labled as 4\n",
      "-->  Grade [84. 83. 64. 47. 44. 67. 82. 87. 82. 72. 74.] labled as 1\n",
      "-->  Grade [46. 45. 61. 57. 44. 59. 49. 62. 49. 44. 48.] labled as 4\n",
      "-->  Grade [64. 59. 58. 50. 57. 60. 61. 68. 66. 65. 62.] labled as 3\n",
      "-->  Grade [ 93.  95.  94. 100.  94.  94.  91.  98.  90.  99.  95.] labled as 4\n",
      "-->  Grade [91. 82. 94. 90. 92. 70. 78. 87. 89. 73. 77.] labled as 1\n",
      "-->  Grade [ 97.  90.  93. 100.  95.  98.  65.  66.  80.  68.  70.] labled as 1\n",
      "-->  Grade [83. 81. 61. 72. 62. 45. 65. 78. 84. 90. 79.] labled as 5\n",
      "-->  Grade [100.  92. 100.  99.  99.  94.  93.  96. 100.  97.  94.] labled as 2\n"
     ]
    }
   ],
   "source": [
    "%matplotlib inline\n",
    "import matplotlib.pyplot as plt\n",
    "\n",
    "s3 = boto3.resource('s3')\n",
    "# Exploring Data and Transforming to load in to S3 for training\n",
    "for types in data_types:\n",
    "    print(\"Reading sample {} data\".format(types))\n",
    "    s3_data_key = \"{}/{}/examples\".format(prefix,types)\n",
    "    s3.Bucket(bucket).download_file(s3_data_key, 'raw_data')\n",
    "\n",
    "\n",
    "    data_from_s3 = genfromtxt('raw_data', delimiter=',')\n",
    "    labels = []\n",
    "    \n",
    "\n",
    "    for t in data_from_s3:\n",
    "        labels.append(int(t[0]))\n",
    "       \n",
    "\n",
    "    grades = np.delete(train_data_from_s3,[0,1],1)\n",
    "\n",
    "    for t in range(0, 10):\n",
    "        print(\"-->  Grade {} labled as {}\".format(grades[t],labels[t]))\n",
    "\n",
    "\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": 207,
   "metadata": {},
   "outputs": [],
   "source": [
    "import sagemaker\n",
    "\n",
    "from sagemaker.amazon.amazon_estimator import get_image_uri\n",
    "\n",
    "container = get_image_uri(boto3.Session().region_name, 'xgboost','0.90-1')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 208,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "s3://mitesh-sagemaker-11142019/sagemaker/xgboost-students-grades/train\n"
     ]
    }
   ],
   "source": [
    "train_data = 's3://{}/{}/{}'.format(bucket, prefix, 'train')\n",
    "\n",
    "validation_data = 's3://{}/{}/{}'.format(bucket, prefix, 'verify')\n",
    "\n",
    "s3_output_location = 's3://{}/{}/{}'.format(bucket, prefix, 'xgboost_model_sdk')\n",
    "print(train_data)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 209,
   "metadata": {},
   "outputs": [],
   "source": [
    "xgb_model = sagemaker.estimator.Estimator(container,\n",
    "                                         role, \n",
    "                                         train_instance_count=1, \n",
    "                                         train_instance_type='ml.m4.xlarge',\n",
    "                                         train_volume_size = 5,\n",
    "                                         output_path=s3_output_location,\n",
    "                                         sagemaker_session=sagemaker.Session())"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 210,
   "metadata": {},
   "outputs": [],
   "source": [
    "xgb_model.set_hyperparameters(max_depth = 5,\n",
    "                              eta = .2,\n",
    "                              gamma = 4,\n",
    "                              min_child_weight = 6,\n",
    "                              silent = 0,\n",
    "                              objective = \"multi:softmax\",\n",
    "                              num_class = 10,\n",
    "                              num_round = 10)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 211,
   "metadata": {},
   "outputs": [],
   "source": [
    "train_channel = sagemaker.session.s3_input(train_data, content_type='text/csv')\n",
    "valid_channel = sagemaker.session.s3_input(validation_data, content_type='text/csv')\n",
    "\n",
    "data_channels = {'train': train_channel, 'validation': valid_channel}"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 212,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "2019-11-28 18:33:27 Starting - Starting the training job...\n",
      "2019-11-28 18:33:28 Starting - Launching requested ML instances......\n",
      "2019-11-28 18:34:31 Starting - Preparing the instances for training......\n",
      "2019-11-28 18:35:36 Downloading - Downloading input data...\n",
      "2019-11-28 18:36:25 Training - Training image download completed. Training in progress..\u001b[31mINFO:sagemaker-containers:Imported framework sagemaker_xgboost_container.training\u001b[0m\n",
      "\u001b[31mINFO:sagemaker-containers:Failed to parse hyperparameter objective value multi:softmax to Json.\u001b[0m\n",
      "\u001b[31mReturning the value itself\u001b[0m\n",
      "\u001b[31mINFO:sagemaker-containers:No GPUs detected (normal if no gpus installed)\u001b[0m\n",
      "\u001b[31mINFO:sagemaker_xgboost_container.training:Running XGBoost Sagemaker in algorithm mode\u001b[0m\n",
      "\u001b[31mINFO:root:Determined delimiter of CSV input is ','\u001b[0m\n",
      "\u001b[31mINFO:root:Determined delimiter of CSV input is ','\u001b[0m\n",
      "\u001b[31mINFO:root:Determined delimiter of CSV input is ','\u001b[0m\n",
      "\u001b[31m[18:36:27] 500x14 matrix with 7000 entries loaded from /opt/ml/input/data/train?format=csv&label_column=0&delimiter=,\u001b[0m\n",
      "\u001b[31mINFO:root:Determined delimiter of CSV input is ','\u001b[0m\n",
      "\u001b[31m[18:36:27] 500x14 matrix with 7000 entries loaded from /opt/ml/input/data/validation?format=csv&label_column=0&delimiter=,\u001b[0m\n",
      "\u001b[31mINFO:root:Single node training.\u001b[0m\n",
      "\u001b[31mINFO:root:Train matrix has 500 rows\u001b[0m\n",
      "\u001b[31mINFO:root:Validation matrix has 500 rows\u001b[0m\n",
      "\u001b[31m[0]#011train-merror:0.142#011validation-merror:0.162\u001b[0m\n",
      "\u001b[31m[1]#011train-merror:0.142#011validation-merror:0.154\u001b[0m\n",
      "\u001b[31m[2]#011train-merror:0.136#011validation-merror:0.156\u001b[0m\n",
      "\u001b[31m[3]#011train-merror:0.12#011validation-merror:0.162\u001b[0m\n",
      "\u001b[31m[4]#011train-merror:0.126#011validation-merror:0.16\u001b[0m\n",
      "\u001b[31m[5]#011train-merror:0.118#011validation-merror:0.158\u001b[0m\n",
      "\u001b[31m[6]#011train-merror:0.12#011validation-merror:0.162\u001b[0m\n",
      "\u001b[31m[7]#011train-merror:0.12#011validation-merror:0.158\u001b[0m\n",
      "\u001b[31m[8]#011train-merror:0.114#011validation-merror:0.158\u001b[0m\n",
      "\u001b[31m[9]#011train-merror:0.116#011validation-merror:0.158\u001b[0m\n",
      "\n",
      "2019-11-28 18:36:36 Uploading - Uploading generated training model\n",
      "2019-11-28 18:36:36 Completed - Training job completed\n",
      "Training seconds: 60\n",
      "Billable seconds: 60\n"
     ]
    }
   ],
   "source": [
    "xgb_model.fit(inputs=data_channels,  logs=True)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 213,
   "metadata": {},
   "outputs": [
    {
     "ename": "ResourceLimitExceeded",
     "evalue": "An error occurred (ResourceLimitExceeded) when calling the CreateEndpoint operation: The account-level service limit 'Number of instances across active endpoints' is 3 Instances, with current utilization of 3 Instances and a request delta of 1 Instances. Please contact AWS support to request an increase for this limit.",
     "output_type": "error",
     "traceback": [
      "\u001b[0;31m---------------------------------------------------------------------------\u001b[0m",
      "\u001b[0;31mResourceLimitExceeded\u001b[0m                     Traceback (most recent call last)",
      "\u001b[0;32m<ipython-input-213-8505024a7d61>\u001b[0m in \u001b[0;36m<module>\u001b[0;34m()\u001b[0m\n\u001b[1;32m      1\u001b[0m xgb_predictor = xgb_model.deploy(initial_instance_count=1,\n\u001b[0;32m----> 2\u001b[0;31m                                 \u001b[0minstance_type\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0;34m'ml.m4.xlarge'\u001b[0m\u001b[0;34m,\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m      3\u001b[0m                                 )\n",
      "\u001b[0;32m~/anaconda3/envs/python3/lib/python3.6/site-packages/sagemaker/estimator.py\u001b[0m in \u001b[0;36mdeploy\u001b[0;34m(self, initial_instance_count, instance_type, accelerator_type, endpoint_name, use_compiled_model, update_endpoint, wait, model_name, kms_key, **kwargs)\u001b[0m\n\u001b[1;32m    559\u001b[0m             \u001b[0mtags\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0mself\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mtags\u001b[0m\u001b[0;34m,\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    560\u001b[0m             \u001b[0mwait\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0mwait\u001b[0m\u001b[0;34m,\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m--> 561\u001b[0;31m             \u001b[0mkms_key\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0mkms_key\u001b[0m\u001b[0;34m,\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m    562\u001b[0m         )\n\u001b[1;32m    563\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n",
      "\u001b[0;32m~/anaconda3/envs/python3/lib/python3.6/site-packages/sagemaker/model.py\u001b[0m in \u001b[0;36mdeploy\u001b[0;34m(self, initial_instance_count, instance_type, accelerator_type, endpoint_name, update_endpoint, tags, kms_key, wait)\u001b[0m\n\u001b[1;32m    468\u001b[0m         \u001b[0;32melse\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    469\u001b[0m             self.sagemaker_session.endpoint_from_production_variants(\n\u001b[0;32m--> 470\u001b[0;31m                 \u001b[0mself\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mendpoint_name\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0;34m[\u001b[0m\u001b[0mproduction_variant\u001b[0m\u001b[0;34m]\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mtags\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mkms_key\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mwait\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m    471\u001b[0m             )\n\u001b[1;32m    472\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n",
      "\u001b[0;32m~/anaconda3/envs/python3/lib/python3.6/site-packages/sagemaker/session.py\u001b[0m in \u001b[0;36mendpoint_from_production_variants\u001b[0;34m(self, name, production_variants, tags, kms_key, wait)\u001b[0m\n\u001b[1;32m   1363\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m   1364\u001b[0m             \u001b[0mself\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0msagemaker_client\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mcreate_endpoint_config\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;34m**\u001b[0m\u001b[0mconfig_options\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m-> 1365\u001b[0;31m         \u001b[0;32mreturn\u001b[0m \u001b[0mself\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mcreate_endpoint\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mendpoint_name\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0mname\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mconfig_name\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0mname\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mtags\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0mtags\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mwait\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0mwait\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m   1366\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m   1367\u001b[0m     \u001b[0;32mdef\u001b[0m \u001b[0mexpand_role\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mself\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mrole\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
      "\u001b[0;32m~/anaconda3/envs/python3/lib/python3.6/site-packages/sagemaker/session.py\u001b[0m in \u001b[0;36mcreate_endpoint\u001b[0;34m(self, endpoint_name, config_name, tags, wait)\u001b[0m\n\u001b[1;32m    977\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    978\u001b[0m         self.sagemaker_client.create_endpoint(\n\u001b[0;32m--> 979\u001b[0;31m             \u001b[0mEndpointName\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0mendpoint_name\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mEndpointConfigName\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0mconfig_name\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mTags\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0mtags\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m    980\u001b[0m         )\n\u001b[1;32m    981\u001b[0m         \u001b[0;32mif\u001b[0m \u001b[0mwait\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
      "\u001b[0;32m~/anaconda3/envs/python3/lib/python3.6/site-packages/botocore/client.py\u001b[0m in \u001b[0;36m_api_call\u001b[0;34m(self, *args, **kwargs)\u001b[0m\n\u001b[1;32m    355\u001b[0m                     \"%s() only accepts keyword arguments.\" % py_operation_name)\n\u001b[1;32m    356\u001b[0m             \u001b[0;31m# The \"self\" in this scope is referring to the BaseClient.\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m--> 357\u001b[0;31m             \u001b[0;32mreturn\u001b[0m \u001b[0mself\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0m_make_api_call\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0moperation_name\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mkwargs\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m    358\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    359\u001b[0m         \u001b[0m_api_call\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0m__name__\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0mstr\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mpy_operation_name\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
      "\u001b[0;32m~/anaconda3/envs/python3/lib/python3.6/site-packages/botocore/client.py\u001b[0m in \u001b[0;36m_make_api_call\u001b[0;34m(self, operation_name, api_params)\u001b[0m\n\u001b[1;32m    659\u001b[0m             \u001b[0merror_code\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0mparsed_response\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mget\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;34m\"Error\"\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0;34m{\u001b[0m\u001b[0;34m}\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mget\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;34m\"Code\"\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    660\u001b[0m             \u001b[0merror_class\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0mself\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mexceptions\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mfrom_code\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0merror_code\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m--> 661\u001b[0;31m             \u001b[0;32mraise\u001b[0m \u001b[0merror_class\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mparsed_response\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0moperation_name\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m    662\u001b[0m         \u001b[0;32melse\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    663\u001b[0m             \u001b[0;32mreturn\u001b[0m \u001b[0mparsed_response\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
      "\u001b[0;31mResourceLimitExceeded\u001b[0m: An error occurred (ResourceLimitExceeded) when calling the CreateEndpoint operation: The account-level service limit 'Number of instances across active endpoints' is 3 Instances, with current utilization of 3 Instances and a request delta of 1 Instances. Please contact AWS support to request an increase for this limit."
     ]
    }
   ],
   "source": [
    "xgb_predictor = xgb_model.deploy(initial_instance_count=1,\n",
    "                                instance_type='ml.m4.xlarge',\n",
    "                                )"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "\n",
    "\n",
    "test_key = \"{}/test/examples\".format(prefix)\n",
    "\n",
    "s3.Bucket(bucket).download_file(test_key, 'test_data')\n",
    "\n",
    "print(test_key)\n",
    "      \n",
    "            "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 182,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Student grade [70. 76. 84. 95. 91. 82. 95. 90. 87. 76. 76. 84. 86. 80.] with lable 2.0\n",
      "Student grade [100.  95.  94.  95.  92.  99.  90.  96.  97.  73.  74.  60.  60.  70.] with lable 5.0\n",
      "Student grade [81. 87. 85. 86. 85. 62. 75. 62. 54. 83. 88. 87. 77. 77.] with lable 4.0\n",
      "Student grade [80. 78. 86. 94. 87. 82. 94. 95. 75. 71. 80. 90. 77. 77.] with lable 2.0\n",
      "Student grade [89. 90. 82. 82. 84. 41. 56. 54. 45. 78. 86. 87. 83. 78.] with lable 4.0\n",
      "Student grade [52. 58. 79. 46. 50. 61. 41. 47. 57. 63. 69. 65. 60. 59.] with lable 3.0\n",
      "Student grade [44. 43. 62. 56. 61. 63. 54. 69. 57. 70. 55. 63. 58. 58.] with lable 3.0\n",
      "Student grade [71. 75. 83. 95. 81. 93. 92. 91. 84. 73. 84. 74. 74. 77.] with lable 2.0\n",
      "Student grade [56. 58. 51. 47. 64. 42. 43. 65. 68. 61. 59. 49. 60. 58.] with lable 3.0\n",
      "Student grade [ 97.  92.  93.  92.  91.  97.  96.  99.  94. 100.  93.  91.  93.  92.] with lable 1.0\n"
     ]
    }
   ],
   "source": [
    "%matplotlib inline\n",
    "from numpy import genfromtxt\n",
    "\n",
    "\n",
    "test_data = \"{}/test/examples\".format(prefix)\n",
    "\n",
    "s3.Bucket(bucket).download_file(test_data, 'test_data')\n",
    "\n",
    "\n",
    "test_data = genfromtxt('test_data', delimiter=',')\n",
    "test_lables = []\n",
    "test_features = []\n",
    "\n",
    "for t in test_data:\n",
    "    test_lables.append(t[0])\n",
    "\n",
    "    \n",
    "test_data = np.delete(test_data,0,1)\n",
    "        \n",
    "# print(test_lables)\n",
    "# print(test_data)\n",
    "\n",
    "np.savetxt('test_data.csv', test_data, delimiter=',')\n",
    "\n",
    "\n",
    "    \n",
    "for i in range (0, 10):\n",
    "    grades = test_data[i]\n",
    "    label = test_lables[i]\n",
    "#     img_reshape = img.reshape((28,28))\n",
    "#     imgplot = plt.imshow(img, cmap='gray')\n",
    "   \n",
    "    print('Student grade {} with lable {}'.format(grades,label))\n",
    "   "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 203,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "500\n",
      "500\n"
     ]
    }
   ],
   "source": [
    "from sagemaker.predictor import csv_serializer\n",
    "xgb_predictor.content_type = 'text/csv'\n",
    "xgb_predictor.serializer = csv_serializer\n",
    "xgb_predictor.deserializer = None\n",
    "\n",
    "sum = 0\n",
    "with open('test_data.csv', 'r') as f:\n",
    "    \n",
    "    for j in range(0,500):\n",
    "        single_test = f.readline()\n",
    "        result = xgb_predictor.predict(single_test)\n",
    "       \n",
    "#         print(\"Data Expected: {} -- Model result {}\".format(test_lables[j],result))\n",
    "        if str(test_lables[j]) in str(result):\n",
    "            sum = sum + 1\n",
    "        \n",
    "\n",
    "        \n",
    "\n",
    "        \n",
    "print(sum)\n",
    "print(len(test_lables))\n",
    "\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "conda_python3",
   "language": "python",
   "name": "conda_python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.6.5"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
