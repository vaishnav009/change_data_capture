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
# from stacks.config import InfraConfig\


class LmabdaService:
    @staticmethod
    def create_lambda_function(stack, lambda_role):
        # lambda_vpc = ec2.Vpc.from_lookup(stack, 'vpc-132a5e6e', vpc_id='vpc-132a5e6e')
        function = _lambda.Function(stack, "cdc-trigger-lambda",
                                          code=_lambda.Code.from_asset('lambdas'),
                                          handler='glue_invocator.lambda_handler',
                                          runtime=_lambda.Runtime.PYTHON_3_9,
                                          role=lambda_role)
        return function