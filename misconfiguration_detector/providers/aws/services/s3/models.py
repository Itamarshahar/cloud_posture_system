from typing import Optional
from botocore.exceptions import ClientError
from misconfiguration_detector.providers.aws.models import AwsResource
from misconfiguration_detector.utils.logging import logger


class S3Bucket(AwsResource):
    encryption: Optional[str]
    versioning: bool = False
    mfa_delete: bool = False
    object_lock: bool = False
    logging: bool = False
    logging_target_bucket: Optional[str] = None

    def __init__(self, *, bucket_data: dict, aws_s3_client):
        self.client = aws_s3_client
        self.name = bucket_data.get("Name", "")
        self.resource_id = bucket_data.get("BucketArn", "")
        self._set_bucket_versioning()
        self._set_bucket_encryption()
        self._set_bucket_logging()
        self._set_object_lock_configuration()

    def _set_bucket_versioning(self):
        logger.info(f"S3 - checking versioning for bucket: {self.name}")
        try:
            response = self.client.get_bucket_versioning(Bucket=self.name)

            self.versioning = response.get("Status") == "Enabled"
            self.mfa_delete = response.get("MFADelete") == "Enabled"

        except ClientError as e:
            code = e.response["Error"]["Code"]

            if code == "AccessDenied":
                logger.warning(f"S3 - access denied when reading versioning for {self.name}")
            elif code == "Throttling":
                logger.warning(f"S3 - throttled while reading versioning for {self.name}")
            else:
                logger.error(f"S3 - unexpected error getting versioning for {self.name}: {e}")

    def _set_bucket_encryption(self):
        logger.info(f"S3 - checking encryption for bucket: {self.name}")
        try:
            response = self.client.get_bucket_encryption(Bucket=self.name)
            self.encryption = (
                response["ServerSideEncryptionConfiguration"]["Rules"][0]
                ["ApplyServerSideEncryptionByDefault"]["SSEAlgorithm"]
            )

        except ClientError as e:
            code = e.response["Error"]["Code"]

            if code == "ServerSideEncryptionConfigurationNotFoundError":
                logger.info(f"S3 - encryption not enabled for bucket {self.name}")
                self.encryption = None
            elif code == "AccessDenied":
                logger.warning(f"S3 - access denied when reading encryption for {self.name}")
            elif code == "Throttling":
                logger.warning(f"S3 - throttled while reading encryption for {self.name}")
            else:
                logger.error(f"S3 - unexpected error getting encryption for {self.name}: {e}")

    def _set_object_lock_configuration(self):
        logger.info(f"S3 - checking object lock for bucket: {self.name}")
        try:
            self.client.get_object_lock_configuration(Bucket=self.name)
            self.object_lock = True

        except ClientError as e:
            code = e.response["Error"]["Code"]

            if code in ("ObjectLockConfigurationNotFoundError", "InvalidRequest"):
                self.object_lock = False
            elif code == "AccessDenied":
                logger.warning(f"S3 - access denied when reading object lock for {self.name}")
            elif code == "Throttling":
                logger.warning(f"S3 - throttled while reading object lock for {self.name}")
            else:
                logger.error(f"S3 - unexpected error getting object lock for {self.name}: {e}")

    def _set_bucket_logging(self):
        logger.info(f"S3 - checking access logging for bucket: {self.name}")
        try:
            response = self.client.get_bucket_logging(Bucket=self.name)

            if "LoggingEnabled" in response:
                self.logging = True
                self.logging_target_bucket = response["LoggingEnabled"]["TargetBucket"]

        except ClientError as e:
            code = e.response["Error"]["Code"]

            if code == "AccessDenied":
                logger.warning(f"S3 - access denied when reading logging for {self.name}")
            elif code == "Throttling":
                logger.warning(f"S3 - throttled while reading logging for {self.name}")
            else:
                logger.error(f"S3 - unexpected error getting logging for {self.name}: {e}")
