from aws_cdk import (
    aws_dms as dms
)
# from stacks.config import InfraConfig


class DMSService:
    @staticmethod
    def create_source_endpoint(stack):
        source_endpt = dms.CfnEndpoint(stack, "RDS-source-endpt", endpoint_type='source',
                                       endpoint_identifier='RDS-source-endpt',
                                       engine_name='mysql',
                                       database_name='MysqlDBforCDC',
                                       password='bdcljbdfou3gg87et2323r2r87glj',
                                       username='admin',
                                       port=3306,
                                       server_name='mysql-db-instance-for-cdc.cwkebb8rx5wk.us-east-1.rds.amazonaws.com')
        return source_endpt
        
    @staticmethod
    def create_destination_endpoint(stack, s3_access_role):
        s3_settings = dms.CfnEndpoint.S3SettingsProperty(service_access_role_arn=s3_access_role.role_arn, bucket_name='full-load-bucket-for-cdc')
        dest_endpoint = dms.CfnEndpoint(stack, 'S3-destination-endpt', endpoint_type='target',
                                       endpoint_identifier='S3-destination-endpt',
                                       engine_name='s3',
                                       s3_settings=s3_settings)
        return dest_endpoint
        
    @staticmethod
    def create_dms_instance(stack):
        dms_replication_instance = dms.CfnReplicationInstance(stack, 'dms-instance-rds-s3-cdc',
                                                              replication_instance_class='dms.t2.micro',
                                                              allocated_storage=50,
                                                              engine_version='3.4.7',
                                                              auto_minor_version_upgrade=False,
                                                              allow_major_version_upgrade=False,
                                                              publicly_accessible=True,
                                                              replication_instance_identifier='dms-instance-rds-s3-cdc-pipeline',
                                                              vpc_security_group_ids=['sg-30d1332f'])
        return dms_replication_instance