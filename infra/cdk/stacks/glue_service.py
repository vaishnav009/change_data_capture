from aws_cdk import (
    aws_glue as glue
)
# from stacks.config import InfraConfig


class GlueService:
    @staticmethod
    def create_glue_job(stack, glue_role):
        glue_job_command = glue.CfnJob.JobCommandProperty(
            name='glueetl',
            python_version='3',
            script_location='s3://full-load-bucket-for-cdc/glue_scripts/cdc_glue_job_script.py'
        )
        glue_job = glue.CfnJob(stack, 'cdc-glue-job',
                               name='cdc-glue-job',
                               command=glue_job_command,
                               glue_version='4.0',
                               role=glue_role.role_arn,
                               number_of_workers=2,
                               worker_type='Standard')
        return glue_job