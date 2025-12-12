from misconfiguration_detector.models import BaseClient, SupportedProviders


class AwsClient(BaseClient):
    provider_name: SupportedProviders = SupportedProviders.AWS
    region_name: str
