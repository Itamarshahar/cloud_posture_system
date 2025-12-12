import boto3

from misconfiguration_detector.providers.aws.aws_client import AwsClient
from misconfiguration_detector.providers.aws.services.s3.models import S3Bucket
from misconfiguration_detector.utils.logging import logger


class S3BucketClient(AwsClient):
    def __init__(self, *, account_id: str, region_name: str = "eu-central-1"):
        super().__init__()
        self.account_id = account_id
        self.region_name = region_name
        self.aws_s3_client = boto3.client("s3", region_name=self.region_name)
        self.buckets = self.init_buckets()

    def init_buckets(self):
        try:
            buckets = []
            response = self.aws_s3_client.list_buckets()
            for bucket in response.get('Buckets'):
                buckets.append(S3Bucket(bucket_data=bucket, aws_s3_client=self.aws_s3_client))
            return buckets
        except Exception as error:
            logger.error(f"Error initializing S3 buckets: {error}")