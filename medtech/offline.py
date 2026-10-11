"""Replay AWS-shaped fixtures through real boto3 clients and botocore Stubber.

Dummy credentials and a transport denial hook prevent accidental network fallback.
"""
from contextlib import ExitStack
import json
from pathlib import Path
import boto3
from botocore.config import Config
from botocore.stub import Stubber


class Offline:
    def __init__(self, fixture):
        self.fixture = json.loads(Path(fixture).read_text()) if isinstance(fixture, (str, Path)) else fixture
        self.clients, self.stubbers = {}, []
        self.stack = ExitStack()

    def __enter__(self):
        session = boto3.Session(aws_access_key_id="offline", aws_secret_access_key="offline", aws_session_token="offline")
        for key, calls in self.fixture["clients"].items():
            service, region = key.split(":")
            client = session.client(service, region_name=region, config=Config(retries={"max_attempts": 0}))
            client.meta.events.register("before-send.*.*", self.block_network)
            stub = Stubber(client)
            for call in calls:
                if "error" in call:
                    stub.add_client_error(call["operation"], service_error_code=call["error"],
                                          http_status_code=call.get("http_status", 403), expected_params=call["params"])
                else:
                    stub.add_response(call["operation"], call["response"], call["params"])
            self.stack.enter_context(stub)
            self.clients[(service, region)] = client
            self.stubbers.append(stub)
        return self

    @staticmethod
    def block_network(**kwargs):
        raise RuntimeError("Network transport prohibited in offline mode")

    def client(self, service, region):
        return self.clients[(service, region)]

    def __exit__(self, kind, value, traceback):
        try:
            if kind is None:
                for stub in self.stubbers:
                    stub.assert_no_pending_responses()
        finally:
            self.stack.close()
