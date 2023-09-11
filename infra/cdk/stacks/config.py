import json
import os

class InfraConfig:
    data = None
    with open("./configs.json", 'r') as json_file:
        data = json.load(json_file)

    @staticmethod
    def get_vpc_name():
        return InfraConfig.data["RDS"]["vpc_name"]

    @staticmethod
    def get_rds_instance_identifier():
        return InfraConfig.data["RDS"]["instance_id"]

    @staticmethod
    def get_db_name():
        return InfraConfig.data["RDS"]["db_name"]

    @staticmethod
    def get_parameter_group_name():
        return InfraConfig.data["RDS"]["parameter_group"]["name"]

    @staticmethod
    def get_pg_parameters():
        return InfraConfig.data["RDS"]["parameter_group"]["parameters"]

    @staticmethod
    def get_security_group_name():
        return InfraConfig.data["RDS"]["security_group"]

    @staticmethod
    def get_option_grp_name():
        return InfraConfig.data["RDS"]["option_group"]

    @staticmethod
    def get_db_username():
        return InfraConfig.data["RDS"]["db_username"]

    @staticmethod
    def get_db_passwrod():
        return InfraConfig.data["RDS"]["db_password"]
    
    @staticmethod
    def get_data_load_bucket_name():
        return InfraConfig.data["S3"]["data_load_bucket"]
    
    @staticmethod
    def get_final_data_bucket_name():
        return InfraConfig.data["S3"]["final_data_bucket"]
    
    @staticmethod
    def get_src_endpoint_identifier():
        return InfraConfig.data["DMS"]["Source_Endpoint"]["identifier"]
    
    @staticmethod
    def get_src_engine_name():
        return InfraConfig.data["DMS"]["Source_Endpoint"]["engine_name"]
    
    @staticmethod
    def get_db_port():
        return InfraConfig.data["DMS"]["Source_Endpoint"]["port"]
    
    @staticmethod
    def get_db_server_name():
        return InfraConfig.data["DMS"]["Source_Endpoint"]["server_name"]
    
    @staticmethod
    def get_target_endpoint_identifier():
        return InfraConfig.data["DMS"]["Target_Endpoint"]["identifier"]
    
    @staticmethod
    def get_target_engine_name():
        return InfraConfig.data["DMS"]["Target_Endpoint"]["engine_name"]
    
    @staticmethod
    def get_target_bucket_name():
        return InfraConfig.data["DMS"]["Target_Endpoint"]["bucket_name"]
    
    @staticmethod
    def get_dms_instance_identifier():
        return InfraConfig.data["DMS"]["Instance"]["identifier"]
    
    @staticmethod
    def get_instance_class():
        return InfraConfig.data["DMS"]["Instance"]["instance_class"]
    
    @staticmethod
    def get_storage_limit():
        return InfraConfig.data["DMS"]["Instance"]["storage"]
    
    @staticmethod
    def get_dms_instance_engine_version():
        return InfraConfig.data["DMS"]["Instance"]["engine_version"]
    
    @staticmethod
    def get_security_groups():
        return InfraConfig.data["DMS"]["Instance"]["security_groups"]
    
    @staticmethod
    def get_dms_s3_access_role():
        return InfraConfig.data["IAM"]["DMS"]["s3-access_role"]
    
    @staticmethod
    def get_dms_managed_policies():
        return InfraConfig.data["IAM"]["DMS"]["managed_policies"]
    
    @staticmethod
    def get_lambda_s3_access_role():
        return InfraConfig.data["IAM"]["Lambda"]["s3-access_role"]
    
    @staticmethod
    def get_lambda_managed_policies():
        return InfraConfig.data["IAM"]["Lambda"]["managed_policies"]
    
    @staticmethod
    def get_glue_s3_access_role():
        return InfraConfig.data["IAM"]["Glue"]["s3-access_role"]
    
    @staticmethod
    def get_glue_managed_policies():
        return InfraConfig.data["IAM"]["Glue"]["managed_policies"]
    
    @staticmethod
    def get_script_location():
        return InfraConfig.data["Glue"]["script_location"]
    
    @staticmethod
    def get_job_name():
         return InfraConfig.data["Glue"]["job_name"]
    
    @staticmethod
    def get_trigger_lambda_name():
        return InfraConfig.data["Lambda"]["function_name"]
    
    @staticmethod
    def get_trigger_lambda_handler():
         return InfraConfig.data["Lambda"]["handler"]
    
    @staticmethod
    def get_prefix_for_lambda_trigger():
         return InfraConfig.data["S3"]["lambda_trigger_prefix"]
