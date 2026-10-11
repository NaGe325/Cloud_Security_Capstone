"""Fail closed if any test attempts to send an HTTP request to AWS."""
import pytest
from botocore.httpsession import URLLib3Session


@pytest.fixture(autouse=True)
def no_aws_network(monkeypatch):
    def blocked(*args, **kwargs):
        raise AssertionError("Tests must never send AWS network requests")
    monkeypatch.setattr(URLLib3Session, "send", blocked)
