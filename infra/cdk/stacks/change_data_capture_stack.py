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
from stacks.config import InfraConfig

class ChangeDataCaptureStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, env: dict[str, Any], **kwargs) -> None:
        super().__init__(scope, construct_id, env=env, **kwargs)
        ChangeDataCaptureStack.create_stack(self)
        
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
        stack.db = RDSService.create_rds_instance(stack,                                    
                                                  InfraConfig.get_vpc_name(),
                                                  InfraConfig.get_rds_instance_identifier(),
                                                  InfraConfig.get_db_name(),
                                                  InfraConfig.get_parameter_group_name(),
                                                  InfraConfig.get_pg_parameters(),
                                                  InfraConfig.get_security_group_name(),
                                                  InfraConfig.get_option_grp_name(),
                                                  InfraConfig.get_db_username(),
                                                  InfraConfig.get_db_passwrod())

    @staticmethod
    def create_data_load_bucket(stack):
        stack.data_load_bucket = S3Service.create_bucket(stack, bucket_name=InfraConfig.get_data_load_bucket_name())

    @staticmethod
    def create_final_load_bucket(stack):
        stack.final_data_bucket = S3Service.create_bucket(stack, bucket_name=InfraConfig.get_final_data_bucket_name())

    @staticmethod
    def create_rds_source_endpoint(stack):
        stack.rds_source_endpoint = DMSService.create_source_endpoint(stack,
                                                                      InfraConfig.get_src_endpoint_identifier(),
                                                                      InfraConfig.get_src_engine_name(),
                                                                      InfraConfig.get_db_name(),
                                                                      InfraConfig.get_db_passwrod(),
                                                                      InfraConfig.get_db_username(),
                                                                      InfraConfig.get_db_port(),
                                                                      InfraConfig.get_db_server_name())

    @staticmethod
    def create_s3_access_role(stack):
        stack.s3_access_role = IAMService.create_role(stack, role_name=InfraConfig.get_dms_s3_access_role(), principal='dms.amazonaws.com')
        stack.s3_access_role = IAMService.add_mamaged_policies(stack, stack.s3_access_role, InfraConfig.get_dms_managed_policies())
    
    @staticmethod
    def create_s3_destination_endpoint(stack):
        stack.s3_destination_endpoint = DMSService.create_destination_endpoint(stack,
                                                                               InfraConfig.get_target_endpoint_identifier(),
                                                                               InfraConfig.get_target_engine_name(),
                                                                               stack.s3_access_role,
                                                                               InfraConfig.get_target_bucket_name())
    
    @staticmethod
    def create_rds_to_s3_migration_instance(stack):
        stack.rds_to_s3_migration_instance = DMSService.create_dms_instance(stack,
                                                                            InfraConfig.get_dms_instance_identifier(),
                                                                            InfraConfig.get_instance_class(),
                                                                            InfraConfig.get_storage_limit(),
                                                                            InfraConfig.get_dms_instance_engine_version(),
                                                                            InfraConfig.get_security_groups())

    @staticmethod
    def create_trigger_lambda_role(stack):
        stack.trigger_lambda_role = IAMService.create_role(stack, role_name=InfraConfig.get_lambda_s3_access_role(), principal='lambda.amazonaws.com')
        stack.trigger_lambda_role = IAMService.add_mamaged_policies(stack, stack.trigger_lambda_role, InfraConfig.get_lambda_managed_policies())
    
    @staticmethod
    def create_trigger_lambda(stack):
        stack.trigger_lambda = LmabdaService.create_lambda_function(stack,
                                                                    InfraConfig.get_trigger_lambda_name(),
                                                                    InfraConfig.get_trigger_lambda_handler(),
                                                                    stack.trigger_lambda_role)
        stack.triggers = S3Service.create_lambda_trigger(stack.data_load_bucket, stack.trigger_lambda, prefix= InfraConfig.get_prefix_for_lambda_trigger())
    
    @staticmethod
    def create_glue_job_role(stack):
        stack.glue_job_role = IAMService.create_role(stack, InfraConfig.get_glue_s3_access_role(), principal='glue.amazonaws.com')
        stack.glue_job_role = IAMService.add_mamaged_policies(stack, stack.glue_job_role, InfraConfig.get_glue_managed_policies())
    
    @staticmethod
    def create_transformation_glue_job(stack):
        stack.transformation_glue_job = GlueService.create_glue_job(stack,
                                                                    job_type='glueetl',
                                                                    python_version='3',
                                                                    script_location=InfraConfig.get_script_location(),
                                                                    job_name=InfraConfig.get_job_name(),
                                                                    glue_role=stack.glue_job_role)
