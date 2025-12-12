from misconfiguration_detector.providers.aws.services.s3.s3_client import \
    S3BucketClient


class ClientFactory:
    _initialized_clients = {}
    @staticmethod
    def get_s3_client(account_id: str, region_name: str = "eu-central-1"):
        key = f"s3_{account_id}_{region_name}"
        if key not in ClientFactory._initialized_clients:
            ClientFactory._initialized_clients[key] = S3BucketClient(
                account_id=account_id,
                region_name=region_name
            )
        return ClientFactory._initialized_clients[key]
