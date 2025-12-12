from misconfiguration_detector.client_factory import ClientFactory
from misconfiguration_detector.models import Misconfiguration, \
    MisconfigurationSeverity


class S3BucketEnableMfaDelete(Misconfiguration):
    uid = "s3_bucket_enable_mfa_delete"
    title = "S3 Bucket MFA Delete Not Enabled"
    description = "S3 Bucket does not have MFA Delete enabled."
    severity = MisconfigurationSeverity.MEDIUM
    remediation_steps = (
        "Enable MFA Delete on the S3 bucket to require multi-factor authentication "
        "when changing the bucket versioning state or deleting object versions. "
        "This adds an additional layer of protection against accidental or malicious "
        "data deletion in the event of compromised IAM credentials. "
        "You can enable MFA Delete using the AWS CLI (requires root or privileged credentials): "
        "aws s3api put-bucket-versioning --profile <ROOT_PROFILE> --bucket <BUCKET_NAME> "
        "--versioning-configuration Status=Enabled,MFADelete=Enabled "
        "--mfa 'arn:aws:iam::<ACCOUNT_ID>:mfa/<MFA_DEVICE> <MFA_CODE>'. "
        "For more details, see AWS documentation: "
        "https://docs.aws.amazon.com/AmazonS3/latest/userguide/MultiFactorAuthenticationDelete.html. "
    )

    def _evaluate(self) -> None:
        s3_bucket = ClientFactory.get_s3_client(account_id=self.account_id)
        for bucket in s3_bucket.buckets:
            if not bucket.mfa_delete:
                self.misconfigured_resources.append(bucket)
            else:
                self.not_misconfigured_resources.append(bucket)
