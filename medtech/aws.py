"""AWS client factory. No client is created by the offline CLI path."""
import boto3
from botocore.config import Config


class AWS:
    def __init__(self):
        self.session = boto3.Session()
        self.clients = {}

    def client(self, service, region):
        key = (service, region)
        if key not in self.clients:
            self.clients[key] = self.session.client(service, region_name=region, config=Config(
                retries={"mode": "standard", "total_max_attempts": 4}, connect_timeout=3, read_timeout=10))
        return self.clients[key]

    def verify_account(self, scope):
        account = self.client("sts", scope.regions[0]).get_caller_identity()["Account"]
        if account != scope.account_id:
            raise ValueError("caller account does not match explicit scan scope; scan aborted")
