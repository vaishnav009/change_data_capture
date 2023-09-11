#!/usr/bin/env python3

import aws_cdk as cdk
import os

from stacks.change_data_capture_stack import ChangeDataCaptureStack


app = cdk.App()
aws_env = {'account': os.environ['CDK_DEFAULT_ACCOUNT'], 
           'region': os.environ['CDK_DEFAULT_REGION']}
ChangeDataCaptureStack(app, "change-data-capture", env=aws_env)

app.synth()
