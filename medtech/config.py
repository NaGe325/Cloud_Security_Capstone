"""Explicit scan scope: no automatic account or region expansion."""
from dataclasses import dataclass
import re


@dataclass(frozen=True)
class Scope:
    account_id: str
    regions: tuple[str, ...]
    buckets: dict[str, str]

    @classmethod
    def from_dict(cls, value):
        account = value.get("account_id", "")
        regions = value.get("regions", [])
        buckets = value.get("buckets", {})
        if not re.fullmatch(r"\d{12}", account):
            raise ValueError("account_id must be an explicit 12-digit AWS account")
        if not regions or len(regions) != len(set(regions)):
            raise ValueError("regions must be nonempty and unique")
        for region in regions:
            if not re.fullmatch(r"[a-z]{2}(?:-[a-z]+)+-\d", region):
                raise ValueError("invalid region")
        if not isinstance(buckets, dict) or not buckets:
            raise ValueError("provide at least one bucket-to-region mapping")
        for name, region in buckets.items():
            if not re.fullmatch(r"[a-z0-9][a-z0-9.-]{1,61}[a-z0-9]", name):
                raise ValueError("invalid bucket name")
            if region not in regions:
                raise ValueError("bucket region must be inside scan regions")
        return cls(account, tuple(regions), dict(buckets))
