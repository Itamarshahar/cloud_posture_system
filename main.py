import argparse
import typing

from misconfiguration_detector.models import SupportedProviders, BaseClient, \
    Misconfiguration
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
from misconfiguration_detector.utils.logging import logger, set_logging_config

parser = argparse.ArgumentParser()

DEFAULT_REGION = "eu-central-1"
PROVIDER_TO_CLIENT_MAP: typing.Dict[
    SupportedProviders, typing.List[typing.Type[BaseClient]]] = {
    SupportedProviders.AWS: [S3BucketClient]
}

PROVIDER_TO_MISCONFIG_MAP: typing.Dict[
    SupportedProviders, typing.List[typing.Type[Misconfiguration]]] = {
    SupportedProviders.AWS: [
        S3BucketDefaultEncryption,
        S3BucketObjectVersioning,
        S3BucketEnableMfaDelete,
        S3BucketS3BucketObjectLock
    ]
}


def setup_misconfigurations(account_id: str, region: str):
    try:
        for provider in SupportedProviders:
            for client_cls in PROVIDER_TO_CLIENT_MAP[provider]:
                client_cls(account_id=account_id, region_name=region)

    except Exception as error:
        logger.error(
            f"Error during misconfiguration setup: {error}, account_id={account_id}, region={region}")
        raise


def evaluate_misconfigurations(account_id: str, region: str):
    try:
        for provider in SupportedProviders:
            for cls_misconfig in PROVIDER_TO_MISCONFIG_MAP[provider]:
                misconfig = cls_misconfig(account_id=account_id,
                                          region=region)
                misconfig.evaluate()
                misconfig.print()
    except Exception as error:
        logger.error(
            f"Error during misconfiguration evaluation: {error}, account_id={account_id}")


def get_sys_args():
    parser.add_argument('--account_id', required=True,
                        help='AWS Account ID to evaluate')
    parser.add_argument('--region', required=False,
                        help='AWS Region to evaluate', default=DEFAULT_REGION)
    return parser.parse_args()


if __name__ == '__main__':
    set_logging_config()
    logger.info("Logger initialized")
    args = get_sys_args()
    logger.info("Starting misconfiguration setup")
    setup_misconfigurations(account_id=args.account_id, region=args.region)
    logger.info("Starting misconfiguration evaluation")
    evaluate_misconfigurations(account_id=args.account_id, region=args.region)
