from typing import Optional

from misconfiguration_detector.providers.aws.models import AwsResource
from botocore.client import ClientError

from misconfiguration_detector.utils.logging import logger


class S3Bucket(AwsResource):
    encryption: Optional[str]
    versioning: bool = False
    mfa_delete: bool = False
    object_lock: bool = False
    logging: bool = False
    logging_target_bucket: bool = False
    def __init__(self, *, bucket_data: dict, aws_s3_client):
        self.client = aws_s3_client
        self.name = bucket_data.get("Name", "")
        self.resource_id = bucket_data.get("BucketArn", "")
        self._set_bucket_versioning()
        self._set_bucket_encryption()
    def _set_bucket_versioning(self):
        try:
            bucket_versioning = self.client.get_bucket_versioning(Bucket=self.name)
            if "Status" in bucket_versioning:
                if "Enabled" == bucket_versioning["Status"]:
                    self.versioning = True
            if "MFADelete" in bucket_versioning:
                if "Enabled" == bucket_versioning["MFADelete"]:
                    self.mfa_delete = True
        except Exception as error:
            logger.warning(f"Got an error while fetching bucket versioning. e={error}")
    def _set_bucket_encryption(self):
        logger.info("S3 - Get buckets encryption...")
        try:
            self.encryption = self.client.get_bucket_encryption(
                Bucket=self.name
            )["ServerSideEncryptionConfiguration"]["Rules"][0]["ApplyServerSideEncryptionByDefault"]["SSEAlgorithm"]
        except Exception as error:
            logger.warning(
                f"Got an error while fetching bucket versioning. e={error}"
            )

    def _get_object_lock_configuration(self):
        logger.info("S3 - Get buckets ownership controls...")
        try:
            self.client.get_object_lock_configuration(Bucket=self.name)
            self.object_lock = True
        except Exception as error:
            self.object_lock = False
            logger.warning(f"Got an error while fetching bucket object lock configuration. e={error}")

    def _get_bucket_logging(self):
        logger.info("S3 - Get buckets logging...")
        try:
            bucket_logging = self.client.get_bucket_logging(Bucket=self.name)
            if "LoggingEnabled" in bucket_logging:
                self.logging = True
                self.logging_target_bucket = \
                bucket_logging["LoggingEnabled"]["TargetBucket"]
        except ClientError as error:
            logger.warning(
                f"Got an error while fetching bucket object lock configuration. e={error}")
