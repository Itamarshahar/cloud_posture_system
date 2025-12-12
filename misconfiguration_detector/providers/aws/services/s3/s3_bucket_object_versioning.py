from misconfiguration_detector.client_factory import ClientFactory
from misconfiguration_detector.models import Misconfiguration, MisconfigurationSeverity


class S3BucketObjectVersioning(Misconfiguration):
    uid = "s3_bucket_object_versioning"
    title = "S3 Bucket Object Versioning Disabled"
    description = "S3 Bucket does not have object versioning enabled."
    severity = MisconfigurationSeverity.HIGH
    remediation_steps = (
        "Enable S3 bucket versioning to retain previous versions of objects and "
        "protect against accidental overwrites, deletions, and malicious modifications. "
        "Versioning is a foundational control for data recovery and ransomware resilience. "
        "You can enable versioning using the AWS Management Console or API. "
        "AWS guidance is available at: "
        "https://docs.aws.amazon.com/AmazonS3/latest/userguide/Versioning.html. "
    )
    def _evaluate(self) -> None:
        s3_bucket = ClientFactory.get_s3_client(account_id=self.account_id)
        for bucket in s3_bucket.buckets:
            if not bucket.versioning:
                self.misconfigured_resources.append(bucket)
            else:
                self.not_misconfigured_resources.append(bucket)
