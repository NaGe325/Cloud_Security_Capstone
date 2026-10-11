"""Portable, escaped HTML reports ordered by action priority."""
from html import escape
import json

CONTROL_NAMES = {
    "S3_PUBLIC_ACCESS": "S3 public access", "S3_ENCRYPTION": "S3 default encryption",
    "IAM_MFA": "Root and console-user MFA", "EC2_ADMIN_PORTS": "SSH and RDP ingress",
    "CLOUDTRAIL_LOGGING": "CloudTrail active logging",
}
SEVERITY_ORDER = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3, "INFORMATIONAL": 4}


def priority_findings(data):
    """Confirmed risks first, then coverage gaps, passed items and N/A."""
    status_order = {"FAIL": 0, "UNKNOWN": 1, "PASS": 2, "NOT_APPLICABLE": 3}
    return sorted(data["findings"], key=lambda f: (status_order[f["status"]], SEVERITY_ORDER[f["severity"]], f["control_id"], f["resource"]))


def render_html(data):
    e = lambda value: escape(str(value), quote=True)
    s, scope = data["summary"], data["scope"]
    rows = []
    for f in priority_findings(data):
        next_step = f["remediation"] if f["status"] == "FAIL" else "Restore evidence access and rerun this control." if f["status"] == "UNKNOWN" else "No remediation proposed by this check."
        rows.append(f'''<article class="finding"><div class="finding-head"><span class="status {e(f['status'].lower())}">{e(f['status'])}</span><span>{e(f['severity'])}</span></div>
<h3>{e(CONTROL_NAMES[f['control_id']])}</h3><div class="resource">{e(f['resource'])} / {e(f['region'])}</div>
<p>{e(f['reason'])}</p><p class="next"><strong>Next step:</strong> {e(next_step)}</p>
<details><summary>Evidence</summary><pre>{e(json.dumps(f['evidence'], indent=2, sort_keys=True))}</pre></details></article>''')
    cards = ''.join(f'<div><strong>{s["counts"][k]}</strong><span>{label}</span></div>' for k, label in [("PASS","Passed"),("FAIL","Failed"),("UNKNOWN","Unknown"),("NOT_APPLICABLE","Not applicable")])
    rate = "Not available" if s["assessed_pass_percent"] is None else f"{s['assessed_pass_percent']}%"
    control_rows = ''.join(f'<tr><td>{e(CONTROL_NAMES[k])}</td><td>{e(v)}</td></tr>' for k,v in s["controls"].items())
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>MedTech report / {e(data['run_id'])}</title><style>
:root{{color-scheme:light}}*{{box-sizing:border-box}}body{{margin:0;background:#f6f7f9;color:#0f172a;font:16px/1.5 Arial,sans-serif}}header{{background:#1b2a49;color:white;padding:32px max(24px,calc((100% - 1060px)/2))}}header p{{margin-bottom:0}}h1{{font-size:28px;margin:8px 0}}main{{max-width:1108px;margin:auto;padding:24px}}.eyebrow{{font-size:12px;letter-spacing:.1em}}.stats{{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin:24px 0}}.stats>div{{background:white;padding:16px;border-bottom:3px solid #1b2a49}}.stats strong{{display:block;font-size:32px}}.stats span{{color:#55595f}}.notice{{border-left:4px solid #8a5a00;background:#fff6dd;padding:16px}}.finding{{background:white;border:1px solid #d5dce6;padding:22px;margin:16px 0;border-radius:8px}}.finding-head{{display:flex;gap:12px;align-items:center;font-size:12px;font-weight:bold}}.status{{padding:3px 8px;border-radius:4px;background:#eef1f6}}.fail{{background:#fbe9ec;color:#b42318}}.unknown{{background:#fff6dd;color:#8a5a00}}.pass{{background:#e6f4ec;color:#246947}}h3{{margin:10px 0 4px}}.resource{{overflow-wrap:anywhere;color:#55595f;font-size:14px}}.next{{border-top:1px solid #d5dce6;padding-top:12px}}pre{{white-space:pre-wrap;overflow-wrap:anywhere;background:#23262b;color:#e6e8eb;padding:16px;border-radius:6px;font-size:13px}}summary{{cursor:pointer}}table{{border-collapse:collapse;width:100%;background:white}}td{{padding:10px;border-bottom:1px solid #d5dce6}}footer{{margin-top:24px;color:#55595f;font-size:13px}}@media(max-width:600px){{.stats{{grid-template-columns:repeat(2,1fr)}}h1{{font-size:23px}}}}@media print{{header{{background:white;color:#1b2a49}}.finding{{break-inside:avoid}}}}
</style></head><body><header><div class="eyebrow">MEDTECH AI / SECURITY BASELINE</div><h1>Security compliance report</h1><p>{e(data['mode'])} / {e(data['run_id'])}</p></header><main>
<h2>{e(s['status'])}</h2><p>Coverage: <strong>{e(s['coverage'])}</strong></p>
<div class="stats">{cards}</div><p>Assessed pass rate: <strong>{e(rate)}</strong>. Excludes unknown and not-applicable results.</p>
<div class="notice">{e(data['disclaimer'])}</div><p>Account: {e(scope['account_id'])}<br>Regions: {e(', '.join(scope['regions']))}<br>Generated: {e(data['generated_at'])}</p>
<h2>Five control groups</h2><table><tbody>{control_rows}</tbody></table>
<h2>Findings and next steps</h2>{''.join(rows)}<footer>Read-only inspection. No remediation was applied. Evidence and resource identifiers require appropriate access controls.</footer></main></body></html>'''
