from misconfiguration_detector.providers.aws.services.s3.s3_client import \
    S3BucketClient


class ClientFactory:
    @staticmethod
    def get_s3_client(account_id: str, region_name: str = "eu-central-1"):
        return S3BucketClient(account_id=account_id, region_name=region_name)
