
# Welcome to your CDK Python project!

# Summary
This Project is developed to capture the change in the existing data stored in RDS DB Instance table. Change Data Capture pipeline (CDC) will first go for the full load of data from RDS to S3.
After full load, it will continue to listen and capture tha changes occuring in the data and keep on replicating to the data stored in S3.

# Architecture
![image](https://github.com/vaishnav009/change_data_capture/assets/30192796/9d646378-0930-4085-b7f1-b1b71ff2ae3e)

Thanks


