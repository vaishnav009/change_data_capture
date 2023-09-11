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
# from stacks.config import InfraConfig


class IAMService:
    @staticmethod
    def create_role(stack, role_name, principal):
        role = iam.Role(stack, role_name+"-id", role_name=role_name, assumed_by=iam.ServicePrincipal(principal))
        return role

    @staticmethod
    def add_mamaged_policies(stack, role, policies):
        for policy in policies:
            role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name(policy))
        return role