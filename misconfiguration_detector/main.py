import argparse

from misconfiguration_detector.providers.aws.services.s3.s3_bucket_default_encryption import \
    S3BucketDefaultEncryption
from misconfiguration_detector.providers.aws.services.s3.s3_bucket_enable_mfa import \
    S3BucketEnableMfaDelete
from misconfiguration_detector.providers.aws.services.s3.s3_bucket_object_lock import \
    S3BucketS3BucketObjectLock
from misconfiguration_detector.providers.aws.services.s3.s3_bucket_object_versioning import \
    S3BucketObjectVersioning
from misconfiguration_detector.providers.aws.services.s3.s3_client import \
    S3BucketClient

parser = argparse.ArgumentParser()

DEFAULT_REGION = "eu-central-1"
MISCONFIGURATIONS = [
    S3BucketDefaultEncryption,
    S3BucketObjectVersioning,
    S3BucketEnableMfaDelete,
    S3BucketS3BucketObjectLock
]

def setup(account_id: str, region: str):
    S3BucketClient(account_id=account_id, region_name=region)

def evaluate_misconfigurations(account_id: str):
    for cls_misconfig in MISCONFIGURATIONS:
        misconfig = cls_misconfig(account_id=account_id)
        misconfig.evaluate()
        misconfig.print()

if __name__ == '__main__':
    parser.add_argument('--account_id', required=True, help='AWS Account ID to evaluate')
    parser.add_argument('--region', required=False, help='AWS Region to evaluate', default=DEFAULT_REGION)
    args = parser.parse_args()
    setup(account_id=args.account_id, region=args.region)
    evaluate_misconfigurations(account_id=args.account_id)

