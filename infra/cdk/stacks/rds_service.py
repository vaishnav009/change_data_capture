from aws_cdk import (
    SecretValue,
    aws_rds as rds,
    aws_ec2 as ec2,
)


class RDSService:
    @staticmethod
    def create_rds_instance(stack, vpc_name, db_instance_name, db_name, param_grp_name, pg_parameters,
                            security_grp_name, option_grp_name, uname, password):
        
        creds = rds.Credentials.from_password(username=uname, password=SecretValue.unsafe_plain_text(password))
        db_engine = rds.DatabaseInstanceEngine.mysql(version=rds.MysqlEngineVersion.VER_8_0_28)
        instance_type = ec2.InstanceType.of(instance_class=ec2.InstanceClass.T2, instance_size=ec2.InstanceSize.MICRO)
        op_group = rds.OptionGroup.from_option_group_name(stack, option_grp_name, option_grp_name)
        sg = ec2.SecurityGroup.from_lookup_by_id(stack, security_grp_name, security_grp_name)
        param_group = rds.ParameterGroup(scope=stack, id=param_grp_name, engine=db_engine, parameters=pg_parameters)
        DBInstance = rds.DatabaseInstance(stack, db_instance_name, credentials=creds, engine=db_engine, database_name=db_name,
                                          instance_type=instance_type,
                                          vpc= ec2.Vpc.from_lookup(stack, vpc_name, is_default=True, vpc_id=vpc_name),
                                          auto_minor_version_upgrade=False,
                                          instance_identifier=db_instance_name,
                                          parameter_group=param_group,
                                          option_group=op_group,
                                          security_groups=[sg],
                                          publicly_accessible=True,
                                          vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC))
        return DBInstance

        