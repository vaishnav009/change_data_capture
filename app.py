#!/usr/bin/env python3

import aws_cdk as cdk

from change_data_capture.change_data_capture_stack import ChangeDataCaptureStack


app = cdk.App()
ChangeDataCaptureStack(app, "change-data-capture")

app.synth()
