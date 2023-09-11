from typing import Any
from constructs import Construct
from aws_cdk import (
    Stack
)
from stacks.rds_service import RDSService
from stacks.s3_service import S3Service
from stacks.lambda_service import LmabdaService
from stacks.glue_service import GlueService
from stacks.dms_service import DMSService
from stacks.iam_service import IAMService

class ChangeDataCaptureStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, env: dict[str, Any], **kwargs) -> None:
        super().__init__(scope, construct_id, env=env, **kwargs)
        ChangeDataCaptureStack.create_stack(self)

        # queue = sqs.Queue(
        #     self, "ChangeDataCaptureQueue",
        #     visibility_timeout=Duration.seconds(300),
        # )

        # topic = sns.Topic(
        #     self, "ChangeDataCaptureTopic"
        # )

        # topic.add_subscription(subs.SqsSubscription(queue))    
        
    @staticmethod
    def create_stack(stack):
        ChangeDataCaptureStack.create_db_instance(stack)
        ChangeDataCaptureStack.create_data_load_bucket(stack)
        ChangeDataCaptureStack.create_final_load_bucket(stack)
        ChangeDataCaptureStack.create_rds_source_endpoint(stack)
        ChangeDataCaptureStack.create_s3_access_role(stack)
        ChangeDataCaptureStack.create_s3_destination_endpoint(stack)
        ChangeDataCaptureStack.create_rds_to_s3_migration_instance(stack)
        ChangeDataCaptureStack.create_trigger_lambda_role(stack)
        ChangeDataCaptureStack.create_trigger_lambda(stack)
        ChangeDataCaptureStack.create_glue_job_role(stack)
        ChangeDataCaptureStack.create_transformation_glue_job(stack)

    @staticmethod
    def create_db_instance(stack):
        stack.db = RDSService.create_rds_instance(stack)

    @staticmethod
    def create_data_load_bucket(stack):
        stack.data_load_bucket = S3Service.create_bucket(stack, bucket_name='data-load-bucket-for-cdc')

    @staticmethod
    def create_final_load_bucket(stack):
        stack.final_data_bucket = S3Service.create_bucket(stack, bucket_name='final-data-bucket-for-cdc')

    @staticmethod
    def create_rds_source_endpoint(stack):
        stack.rds_source_endpoint = DMSService.create_source_endpoint(stack)

    @staticmethod
    def create_s3_access_role(stack):
        stack.s3_access_role = IAMService.create_role(stack, role_name='s3-access-role-for-dms', principal='dms.amazonaws.com')
        stack.s3_access_role = IAMService.add_mamaged_policies(stack, stack.s3_access_role, ['AmazonS3FullAccess'])
    
    @staticmethod
    def create_s3_destination_endpoint(stack):
        stack.s3_destination_endpoint = DMSService.create_destination_endpoint(stack, stack.s3_access_role)
    
    @staticmethod
    def create_rds_to_s3_migration_instance(stack):
        stack.rds_to_s3_migration_instance = DMSService.create_dms_instance(stack)

    @staticmethod
    def create_trigger_lambda_role(stack):
        stack.trigger_lambda_role = IAMService.create_role(stack, role_name='s3-glue-access-role', principal='lambda.amazonaws.com')
        stack.trigger_lambda_role = IAMService.add_mamaged_policies(stack, stack.trigger_lambda_role, ['AmazonS3FullAccess', 'AWSGlueConsoleFullAccess', 'CloudWatchFullAccess'])
    
    @staticmethod
    def create_trigger_lambda(stack):
        stack.trigger_lambda = LmabdaService.create_lambda_function(stack, stack.trigger_lambda_role)
        stack.triggers = S3Service.create_lambda_trigger(stack, stack.data_load_bucket, stack.trigger_lambda)
    
    @staticmethod
    def create_glue_job_role(stack):
        stack.glue_job_role = IAMService.create_role(stack, 'glue-job-role', principal='glue.amazonaws.com')
        stack.glue_job_role = IAMService.add_mamaged_policies(stack, stack.glue_job_role, ['AmazonS3FullAccess', 'CloudWatchFullAccess'])
    
    @staticmethod
    def create_transformation_glue_job(stack):
        stack.transformation_glue_job = GlueService.create_glue_job(stack, stack.glue_job_role)
