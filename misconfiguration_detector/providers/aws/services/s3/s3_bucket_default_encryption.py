from misconfiguration_detector.client_factory import ClientFactory
from misconfiguration_detector.models import Misconfiguration, \
    MisconfigurationSeverity


class S3BucketDefaultEncryption(Misconfiguration):
    uid = "s3_bucket_default_encryption"
    title = "S3 Bucket Default Encryption Disabled"
    description = "S3 Bucket does not have default encryption enabled."
    severity = MisconfigurationSeverity.HIGH
    remediation_steps = (
        "Enable default server-side encryption on the S3 bucket to ensure that all "
        "objects are encrypted at rest. Enforcing encryption strengthens data "
        "protection and helps meet security and compliance requirements. "
        "You can enable default encryption using the AWS CLI with the following command: "
        "aws s3api put-bucket-encryption --bucket <BUCKET_NAME> "
        "--server-side-encryption-configuration "
        "'{\"Rules\": [{\"ApplyServerSideEncryptionByDefault\": "
        "{\"SSEAlgorithm\": \"AES256\"}}]}'. "
        "For additional guidance and best practices, refer to AWS documentation: "
        "https://aws.amazon.com/blogs/security/how-to-prevent-uploads-of-unencrypted-objects-to-amazon-s3/."
    )

    def _evaluate(self) -> None:
        s3_bucket = ClientFactory.get_s3_client(self.account_id)
        for bucket in s3_bucket.buckets:
            if not bucket.encryption:
                self.misconfigured_resources.append(bucket)
            else:
                self.not_misconfigured_resources.append(bucket)
