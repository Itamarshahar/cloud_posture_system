import abc
import typing
import enum

from misconfiguration_detector.utils.logging import logger


class MisconfigurationSeverity(enum.Enum):
    INFO = "INFO"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class SupportedProviders(enum.Enum):
    AWS = "aws"


class MisconfigurationStatus(enum.Enum):
    PASSED = "PASSED"
    FAILED = "FAILED"
    PENDING = "PENDING"


class Resource(abc.ABC):
    name: str
    resource_id: str


class Misconfiguration(abc.ABC):
    uid: str
    title: str
    description: str
    severity: MisconfigurationSeverity
    remediation_steps: str
    misconfigured_resources: list[typing.Type[Resource]]
    not_misconfigured_resources: list[typing.Type[Resource]]
    account_id: str
    status: MisconfigurationStatus = MisconfigurationStatus.PENDING

    def __init__(self, account_id: str, region:str, **data: typing.Any):
        super().__init__(**data)
        self.account_id = account_id
        self.region = region
        self.misconfigured_resources = []
        self.not_misconfigured_resources = []

    @abc.abstractmethod
    def _evaluate(self) -> None:
        raise NotImplementedError()

    def evaluate(self) -> None:
        try:
            logger.info(
                f"Evaluating misconfiguration: {self.title}, Account ID: {self.account_id}")
            self._evaluate()
            logger.info(
                f"Setting status for misconfiguration: {self.title}, Account ID: {self.account_id}")
            self.set_status()
        except Exception as error:
            logger.error(
                f"Error evaluating misconfiguration [{self.title}] [{self.account_id}]: {error}")
            self.status = MisconfigurationStatus.FAILED

    def set_status(self) -> None:
        if self.misconfigured_resources:
            self.status = MisconfigurationStatus.FAILED
        else:
            self.status = MisconfigurationStatus.PASSED

    def print(self):
        print("=" * 80)
        print(f"Misconfiguration: {self.title}")
        print(
            f"Account: {self.account_id} | Severity: {self.severity.name} | Status: {self.status.name}")
        print("=" * 80)

        print("Description:")
        print(f"  {self.description}\n")

        print("Remediation Steps:")
        print(f"  {self.remediation_steps}\n")

        print("Affected Resources:")
        print("-" * 80)
        print(f"{'Name':<30} {'Resource ID':<40} {'Status':<10}")
        print("-" * 80)

        for resource in self.misconfigured_resources:
            print(
                f"{resource.name:<30} "
                f"{resource.resource_id:<40} "
                f"{MisconfigurationStatus.FAILED.name:<10}"
            )

        for resource in self.not_misconfigured_resources:
            print(
                f"{resource.name:<30} "
                f"{resource.resource_id:<40} "
                f"{MisconfigurationStatus.PASSED.name:<10}"
            )

        print("-" * 80)
        print("\n")


class BaseClient(abc.ABC):
    provider_name: str
    region_name: str

    def __init__(self, *, account_id: str, region_name: str = "eu-central-1"):
        self.account_id = account_id
        self.region_name = region_name
