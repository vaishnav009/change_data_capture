import json
import boto3


def lambda_handler(event, context):
    print("We'll invoke glue job from here ....!!!")
    print(event)
    print(event["Records"][0]['s3']['bucket']['name'])
    print(event["Records"][0]['s3']['object']['key'])
    
    cdc_bucket_name = event["Records"][0]['s3']['bucket']['name']
    changed_data_file_key = event["Records"][0]['s3']['object']['key']
    
    client = boto3.client('glue')
    response = client.start_job_run(
        JobName = 'cdc-glue-job',
        Arguments = {
        "--s3-target-path-key": changed_data_file_key,
        "--s3-target-bucket": cdc_bucket_name
        }
    )
    print(response)
    return {
        'status_code': 200,
        'body': json.dumps('Glue job invoked successfully..!!')
    }