from aws_cdk import (
    SecretValue,
    aws_rds as rds,
    aws_ec2 as ec2,
)
# from stacks.config import InfraConfig

class RDSService:
    @staticmethod
    def create_rds_instance(stack):
        creds = rds.Credentials.from_password(username='admin', password=SecretValue.unsafe_plain_text("bdcljbdfou3gg87et2323r2r87glj"))
        db_engine = rds.DatabaseInstanceEngine.mysql(version=rds.MysqlEngineVersion.VER_8_0_28)
        instance_type = ec2.InstanceType.of(instance_class=ec2.InstanceClass.T2, instance_size=ec2.InstanceSize.MICRO)
        # param_group = rds.ParameterGroup.from_parameter_group_name(stack, 'RDSMySqlPG', 'RDSMySqlPG')
        op_group = rds.OptionGroup.from_option_group_name(stack, 'default:mysql-8-0', 'default:mysql-8-0')
        sg = ec2.SecurityGroup.from_lookup_by_id(stack, 'sg-30d1332f', 'sg-30d1332f')
        param_group = rds.ParameterGroup(scope=stack, id='RDS-MySQL-PG', engine=db_engine, parameters={'binlog_format': 'ROW'})
        DBInstance = rds.DatabaseInstance(stack, "Mysql-db-instance-for-CDC", credentials=creds, engine=db_engine, database_name= "MysqlDBforCDC",
                                          instance_type=instance_type,
                                          vpc= ec2.Vpc.from_lookup(stack, 'vpc-132a5e6e', is_default=True, vpc_id='vpc-132a5e6e'),
                                          auto_minor_version_upgrade=False,
                                          instance_identifier="Mysql-db-instance-for-CDC",
                                          parameter_group=param_group,
                                          option_group=op_group,
                                          security_groups=[sg],
                                          publicly_accessible=True,
                                          vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC))
        return DBInstance