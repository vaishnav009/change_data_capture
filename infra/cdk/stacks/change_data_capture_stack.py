from typing import Any
from constructs import Construct
from aws_cdk import (
    Duration,
    Stack,
    SecretValue,
    aws_iam as iam,
    aws_sqs as sqs,
    aws_sns as sns,
    aws_sns_subscriptions as subs,
    aws_rds as rds,
    aws_ec2 as ec2,
    aws_s3 as s3,
    aws_dms as dms,
    aws_lambda as _lambda,
    aws_s3_notifications as s3_notif,
    aws_glue as glue
)

class ChangeDataCaptureStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, env: dict[str, Any], **kwargs) -> None:
        super().__init__(scope, construct_id, env=env, **kwargs)

        # queue = sqs.Queue(
        #     self, "ChangeDataCaptureQueue",
        #     visibility_timeout=Duration.seconds(300),
        # )

        # topic = sns.Topic(
        #     self, "ChangeDataCaptureTopic"
        # )

        # topic.add_subscription(subs.SqsSubscription(queue))
        creds = rds.Credentials.from_password(username='admin', password=SecretValue.unsafe_plain_text("bdcljbdfou3gg87et2323r2r87glj"))
        db_engine = rds.DatabaseInstanceEngine.mysql(version=rds.MysqlEngineVersion.VER_8_0_28)
        instance_type = ec2.InstanceType.of(instance_class=ec2.InstanceClass.T2, instance_size=ec2.InstanceSize.MICRO)
        param_group = rds.ParameterGroup.from_parameter_group_name(self, 'RDSMySqlPG', 'RDSMySqlPG')
        op_group = rds.OptionGroup.from_option_group_name(self, 'default:mysql-8-0', 'default:mysql-8-0')
        sg = ec2.SecurityGroup.from_lookup_by_id(self, 'sg-30d1332f', 'sg-30d1332f')
        DBInstance = rds.DatabaseInstance(self, "Mysql-db-instance-for-CDC", credentials=creds, engine=db_engine, database_name= "MysqlDBforCDC",
                                          instance_type=instance_type,
                                          vpc= ec2.Vpc.from_lookup(self, 'vpc-132a5e6e', is_default=True, vpc_id='vpc-132a5e6e'),
                                          auto_minor_version_upgrade=False,
                                          instance_identifier="Mysql-db-instance-for-CDC",
                                          parameter_group=param_group,
                                          option_group=op_group,
                                          security_groups=[sg],
                                          publicly_accessible=True,
                                          vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC))
        block_public_access = s3.BlockPublicAccess(block_public_acls=False, block_public_policy=False, ignore_public_acls=False, restrict_public_buckets= False)
        full_load_bucket = s3.Bucket(self, "full-load-bucket-for-cdc", bucket_name='full-load-bucket-for-cdc',
                                     block_public_access=block_public_access)
        final_data_bucket = s3.Bucket(self, "final-data-bucket-for-cdc", bucket_name='final-data-bucket-for-cdc',
                                     block_public_access=block_public_access)
        
        source_endpt = dms.CfnEndpoint(self, "RDS-source-endpt", endpoint_type='source',
                                       endpoint_identifier='RDS-source-endpt',
                                       engine_name='mysql',
                                       database_name='MysqlDBforCDC',
                                       password='bdcljbdfou3gg87et2323r2r87glj',
                                       username='admin',
                                       port=3306,
                                       server_name='mysql-db-instance-for-cdc.cwkebb8rx5wk.us-east-1.rds.amazonaws.com')
        s3_access_role = iam.Role(self, "s3-Access-Role", role_name='s3-access-role-for-dms', assumed_by=iam.ServicePrincipal('dms.amazonaws.com'))
        s3_access_role.add_managed_policy(iam.ManagedPolicy.from_managed_policy_arn(self, "s3-managed-policy", 'arn:aws:iam::aws:policy/AmazonS3FullAccess'))
        s3_settings = dms.CfnEndpoint.S3SettingsProperty(service_access_role_arn=s3_access_role.role_arn, bucket_name='full-load-bucket-for-cdc')
        dest_endpoint = dms.CfnEndpoint(self, 'S3-destination-endpt', endpoint_type='target',
                                       endpoint_identifier='S3-destination-endpt',
                                       engine_name='s3',
                                       s3_settings=s3_settings)
        dms_replication_instance = dms.CfnReplicationInstance(self, 'dms-instance-rds-s3-cdc',
                                                              replication_instance_class='dms.t2.micro',
                                                              allocated_storage=50,
                                                              engine_version='3.4.7',
                                                              auto_minor_version_upgrade=False,
                                                              allow_major_version_upgrade=False,
                                                              publicly_accessible=True,
                                                              replication_instance_identifier='dms-instance-rds-s3-cdc-pipeline',
                                                              vpc_security_group_ids=['sg-30d1332f'])
        
        
        # lambda_vpc = ec2.Vpc.from_lookup(self, 'vpc-132a5e6e', vpc_id='vpc-132a5e6e')
        lambda_role = iam.Role(self, "trigger-lambda-role", role_name='s3-glue-access-role', assumed_by=iam.ServicePrincipal('lambda.amazonaws.com'))
        lambda_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name('AmazonS3FullAccess'))
        lambda_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name('AWSGlueConsoleFullAccess'))
        lambda_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name('CloudWatchFullAccess'))
        
        trigger_lambda = _lambda.Function(self, "cdc-trigger-lambda",
                                          code=_lambda.Code.from_asset('lambdas'),
                                          handler='glue_invocator.lambda_handler',
                                          runtime=_lambda.Runtime.PYTHON_3_9,
                                          role=lambda_role)
        trigger_prefix = s3.NotificationKeyFilter(prefix='dbo/Persons/')
        full_load_bucket.add_event_notification(
            s3.EventType.OBJECT_CREATED_PUT,
            s3_notif.LambdaDestination(trigger_lambda),
            trigger_prefix
        )
        full_load_bucket.add_event_notification(
            s3.EventType.OBJECT_CREATED_COMPLETE_MULTIPART_UPLOAD,
            s3_notif.LambdaDestination(trigger_lambda),
            trigger_prefix
        )
        full_load_bucket.add_event_notification(
            s3.EventType.OBJECT_CREATED_COPY,
            s3_notif.LambdaDestination(trigger_lambda),
            trigger_prefix
        )


        glue_role = iam.Role(self, 'glue-job-role', assumed_by=iam.ServicePrincipal('glue.amazonaws.com'))
        glue_job_command = glue.CfnJob.JobCommandProperty(
            name='glueetl',
            python_version='3',
            script_location='s3://full-load-bucket-for-cdc/glue_scripts/cdc_glue_job_script.py'
        )
        glue_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name('AmazonS3FullAccess'))
        glue_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name('CloudWatchFullAccess'))
        glue_job = glue.CfnJob(self, 'cdc-glue-job',
                               name='cdc-glue-job',
                               command=glue_job_command,
                               glue_version='4.0',
                               role=glue_role.role_arn,
                               number_of_workers=2,
                               worker_type='Standard')

