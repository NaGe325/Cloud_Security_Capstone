"""Serializable evidence, stable finding IDs, and explicit incomplete coverage."""
from collections import Counter
from datetime import datetime, timezone
from hashlib import sha256
import json

CONTROLS = ("S3_PUBLIC_ACCESS", "S3_ENCRYPTION", "IAM_MFA", "EC2_ADMIN_PORTS", "CLOUDTRAIL_LOGGING")


def finding(control, resource, region, status, severity, reason, evidence=None, remediation=""):
    return {
        "id": sha256(f"{control}|{region}|{resource}".encode()).hexdigest()[:20],
        "control_id": control, "resource": resource, "region": region,
        "status": status, "severity": severity if status == "FAIL" else "INFORMATIONAL",
        "reason": reason, "evidence": evidence or {}, "remediation": remediation,
    }


def report(scope, findings, mode, run_id, timestamp=None):
    counts = {s: sum(f["status"] == s for f in findings) for s in ("PASS", "FAIL", "UNKNOWN", "NOT_APPLICABLE")}
    assessed = counts["PASS"] + counts["FAIL"]
    coverage = "INCOMPLETE" if counts["UNKNOWN"] else "COMPLETE_WITHIN_SCOPE"
    status = "FAIL" if counts["FAIL"] else ("INCOMPLETE" if counts["UNKNOWN"] else "PASS")
    controls = {}
    for c in CONTROLS:
        statuses = [f["status"] for f in findings if f["control_id"] == c]
        controls[c] = "FAIL" if "FAIL" in statuses else "UNKNOWN" if "UNKNOWN" in statuses or not statuses else "PASS" if "PASS" in statuses else "NOT_APPLICABLE"
    return {
        "schema_version": "1.0", "baseline": "MedTech educational baseline v1",
        "run_id": run_id, "generated_at": timestamp or datetime.now(timezone.utc).isoformat(),
        "mode": mode, "scope": {"account_id": scope.account_id, "regions": list(scope.regions), "buckets": scope.buckets},
        "disclaimer": "Five technical controls only; not a HIPAA compliance determination. PASS applies only to this baseline and explicit scope.",
        "summary": {"status": status, "coverage": coverage, "counts": counts,
                    "assessed_pass_percent": round(100 * counts["PASS"] / assessed, 2) if assessed else None,
                    "risk_counts": dict(Counter(f["severity"] for f in findings if f["status"] == "FAIL")),
                    "controls": controls},
        "findings": sorted(findings, key=lambda f: (f["control_id"], f["region"], f["resource"])),
    }


def markdown(data):
    s = data["summary"]
    lines = ["# MedTech AWS security baseline report", "", data["disclaimer"], "",
             f"Run: `{data['run_id']}` · Mode: **{data['mode']}** · Time: {data['generated_at']}",
             f"Result: **{s['status']}** · Coverage: **{s['coverage']}**", "",
             f"Counts: {json.dumps(s['counts'])}",
             f"Assessed-resource pass rate: {s['assessed_pass_percent']}% (excludes UNKNOWN and NOT_APPLICABLE).", "",
             "| Control | Resource | Region | Result | Risk | Explanation |", "|---|---|---|---|---|---|"]
    for f in data["findings"]:
        cells = [f[k] for k in ("control_id", "resource", "region", "status", "severity", "reason")]
        lines.append("| " + " | ".join(str(v).replace("|", "\\|").replace("\n", " ") for v in cells) + " |")
    lines += ["", "## Remediation proposals (never applied automatically)", ""]
    lines += [f"- **{f['resource']}**: {f['remediation']}" for f in data["findings"] if f["status"] == "FAIL"]
    return "\n".join(lines) + "\n"
