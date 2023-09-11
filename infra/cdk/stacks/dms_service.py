from aws_cdk import (
    aws_dms as dms
)
# from stacks.config import InfraConfig


class DMSService:
    @staticmethod
    def create_source_endpoint(stack, identifier, engine_name, db_name, password, username, port, server_name):
        source_endpt = dms.CfnEndpoint(stack, identifier, endpoint_type='source',
                                       endpoint_identifier=identifier,
                                       engine_name=engine_name,
                                       database_name=db_name,
                                       password=password,
                                       username=username,
                                       port=port,
                                       server_name=server_name)
        return source_endpt
        
    @staticmethod
    def create_destination_endpoint(stack, identifier, engine_name, s3_access_role, bucket_name):
        s3_settings = dms.CfnEndpoint.S3SettingsProperty(service_access_role_arn=s3_access_role.role_arn, bucket_name=bucket_name)
        dest_endpoint = dms.CfnEndpoint(stack, identifier, endpoint_type='target',
                                       endpoint_identifier=identifier,
                                       engine_name=engine_name,
                                       s3_settings=s3_settings)
        return dest_endpoint
        
    @staticmethod
    def create_dms_instance(stack, identifier, instance_class, storage, engine_version, security_groups):
        dms_replication_instance = dms.CfnReplicationInstance(stack, identifier,
                                                              replication_instance_class=instance_class,
                                                              allocated_storage=storage,
                                                              engine_version=engine_version,
                                                              auto_minor_version_upgrade=False,
                                                              allow_major_version_upgrade=False,
                                                              publicly_accessible=True,
                                                              replication_instance_identifier=identifier,
                                                              vpc_security_group_ids=security_groups)
        return dms_replication_instance