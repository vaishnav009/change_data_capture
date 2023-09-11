from aws_cdk import (
    aws_s3 as s3,
    aws_s3_notifications as s3_notif
)
# from stacks.config import InfraConfig


class S3Service:
    @staticmethod
    def create_bucket(stack, bucket_name):
        block_public_access = s3.BlockPublicAccess(block_public_acls=False, block_public_policy=False, ignore_public_acls=False, restrict_public_buckets= False)
        bucket = s3.Bucket(stack, bucket_name+"-id", bucket_name=bucket_name,
                           block_public_access=block_public_access)
        return bucket
        
    @staticmethod
    def create_lambda_trigger(bucket, dest_lambda, prefix):
        trigger_prefix = s3.NotificationKeyFilter(prefix=prefix)
        bucket.add_event_notification(
            s3.EventType.OBJECT_CREATED_PUT,
            s3_notif.LambdaDestination(dest_lambda),
            trigger_prefix
        )
        bucket.add_event_notification(
            s3.EventType.OBJECT_CREATED_COMPLETE_MULTIPART_UPLOAD,
            s3_notif.LambdaDestination(dest_lambda),
            trigger_prefix
        )
        bucket.add_event_notification(
            s3.EventType.OBJECT_CREATED_COPY,
            s3_notif.LambdaDestination(dest_lambda),
            trigger_prefix
        )
        return 'OK'