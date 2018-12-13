# Copyright 2017 Amazon Web Services, Inc. or its affiliates. All rights
# reserved.

import sys
from datetime import datetime, timedelta
import boto3
import utils
import solution as dynamodb_solution

BUCKET_NAME = utils.LAB_S3_BUCKET_NAME
BUCKET_REGION = utils.LAB_S3_BUCKET_REGION
PATIENT_REPORT_PREFIX = utils.LAB_S3_PATIENT_REPORT_PREFIX
infections_table_name = utils.LAB_S3_INFECTIONS_TABLE_NAME
HTTP_STATUS_SUCCESS = 200

# Sample reports exist for patient ids 1, 2, 3


def link_patient_report(table_name=infections_table_name):
    dynamodb = boto3.resource('dynamodb')
    # Update Infections table item for patient ids 1, 2, 3 with the report url
    try:
        for i in range(1, 4):
            object_key = PATIENT_REPORT_PREFIX + str(i) + ".txt"
            # Construct the URL for the patient report
            report_url = "https://s3-{0}.amazonaws.com/{1}/{2}".format(
                BUCKET_REGION, BUCKET_NAME, object_key)
            update_item_with_link(dynamodb, i, report_url, table_name)
    except Exception as err:
        print("Error message {0}".format(err))


def update_item_with_link(dynamodb, patient_id, report_url, table_name):
    """Update an item in the table

    Keyword arguments:
    dynamodb -- DynamoDB resource
    patient_id -- Patient ID
    report_url -- Report URL
    table_name -- Table name
    """

    # TODO 3: Replace the solution with your own code
    myTable = dynamodb.Table(infections_table_name)
    try:
        # Update item in table for the given patient_id key.
        resp = myTable.update_item(
            Key={'PatientId': str(patient_id)},
            UpdateExpression='set PatientReportUrl=:val1',
            ExpressionAttributeValues={':val1': {'S': report_url}})
        print("Item updated")
        print(
            "PatientId:{0}, PatientReportUrl:{1}".format(
                patient_id,
                report_url))
    except Exception as err:
        print("Error message {0}".format(err))


if __name__ == '__main__':
    print("Update report url for patient ids 1, 2, 3:")
    link_patient_report()
