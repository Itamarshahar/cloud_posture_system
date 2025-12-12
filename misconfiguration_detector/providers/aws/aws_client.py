from misconfiguration_detector.models import Client, SupportedProviders


class AwsClient(Client):
    provider_name: SupportedProviders = SupportedProviders.AWS
    region_name: str
