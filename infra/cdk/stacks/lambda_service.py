from aws_cdk import (
    aws_lambda as _lambda
)
# from stacks.config import InfraConfig\


class LmabdaService:
    @staticmethod
    def create_lambda_function(stack, function_name, handler, lambda_role):
        # lambda_vpc = ec2.Vpc.from_lookup(stack, 'vpc-132a5e6e', vpc_id='vpc-132a5e6e')
        function = _lambda.Function(stack, function_name,
                                          code=_lambda.Code.from_asset('./../../src/lambdas/handlers'),
                                          handler=handler,
                                          runtime=_lambda.Runtime.PYTHON_3_9,
                                          role=lambda_role)
        return function