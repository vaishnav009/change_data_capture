from aws_cdk import (
    aws_iam as iam
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