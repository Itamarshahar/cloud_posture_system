import typing

from misconfiguration_detector.client_factory import ClientFactory
from misconfiguration_detector.models import Misconfiguration, \
    MisconfigurationSeverity


class S3BucketS3BucketObjectLock(Misconfiguration):
    uid = "s3_bucket_object_lock"
    title = "S3 Bucket Object Lock Disabled"
    description = "S3 Bucket does not have Object Lock enabled."
    severity = MisconfigurationSeverity.MEDIUM
    remediation_steps = (
        "Enable S3 Object Lock on the bucket to enforce write-once-read-many (WORM) "
        "protections. Object Lock prevents objects from being deleted or overwritten "
        "for a defined retention period, strengthening protection against ransomware "
        "and unauthorized data tampering, especially for backups and audit logs. "
        "Object Lock can be enabled using the AWS CLI as follows: "
        "aws s3 put-object-lock-configuration --bucket <BUCKET_NAME> "
        "--object-lock-configuration "
        "'{\"ObjectLockEnabled\":\"Enabled\","
        "\"Rule\":{\"DefaultRetention\":{\"Mode\":\"GOVERNANCE\",\"Days\":1}}}'. "
        "For more information, see AWS documentation: "
        "https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock-overview.html. "
    )

    def _evaluate(self) -> None:
        s3_bucket = ClientFactory.get_s3_client(account_id=self.account_id)
        for bucket in s3_bucket.buckets:
            if not bucket.object_lock:
                self.misconfigured_resources.append(bucket)
            else:
                self.not_misconfigured_resources.append(bucket)
