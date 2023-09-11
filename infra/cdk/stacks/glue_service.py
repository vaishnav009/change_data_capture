from aws_cdk import (
    aws_glue as glue
)
# from stacks.config import InfraConfig


class GlueService:
    @staticmethod
    def create_glue_job(stack, job_type, python_version, script_location, job_name, glue_role):
        glue_job_command = glue.CfnJob.JobCommandProperty(
            name=job_type,
            python_version=python_version,
            script_location=script_location
        )
        glue_job = glue.CfnJob(stack, job_name,
                               name=job_name,
                               command=glue_job_command,
                               glue_version='4.0',
                               role=glue_role.role_arn,
                               number_of_workers=2,
                               worker_type='Standard')
        return glue_job