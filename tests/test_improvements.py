import json
import pytest
from medtech.html_report import render_html, priority_findings
from medtech.monitoring import publish_metrics, NAMESPACE
from medtech.offline import Offline
from medtech.cli import main
from test_checker import fixture, run, REGION


def test_html_escapes_untrusted_values():
    data=run(fixture())
    for f in data['findings']:
        f['resource']='<img src=x onerror=alert(1)>'
        f['reason']='<script>alert(1)</script>'
        f['evidence']={'unsafe':'<script>document.cookie</script>'}
    html=render_html(data)
    assert '<script>' not in html and '<img src=x' not in html
    assert '&lt;script&gt;' in html and '&lt;img' in html


def test_html_prioritizes_critical_and_disclaimer():
    data=run(fixture('misconfigured'))
    assert priority_findings(data)[0]['resource']=='root'
    html=render_html(data)
    assert 'not a HIPAA compliance determination' in html
    assert 'No remediation was applied' in html


def test_incomplete_demo(tmp_path):
    assert main(['demo','incomplete','--out',str(tmp_path)])==2
    data=json.loads((tmp_path/'incomplete.json').read_text())
    assert data['summary']['status']=='INCOMPLETE'
    assert data['summary']['counts']=={'PASS':5,'FAIL':0,'UNKNOWN':1,'NOT_APPLICABLE':1}
    assert data['summary']['assessed_pass_percent']==100.0
    html=(tmp_path/'incomplete.html').read_text()
    assert 'INCOMPLETE' in html and 'Unknown' in html
    assert json.loads((tmp_path/'incomplete.delivery.json').read_text())['sns']=='PREVIEW_ONLY'


def test_metrics_disabled():
    assert publish_metrics(run(fixture()))=={'status':'DISABLED'}


def test_metrics_parameters():
    data=run(fixture('misconfigured'))
    f={'clients':{f'cloudwatch:{REGION}':[{'operation':'put_metric_data','params':{'Namespace':NAMESPACE,'MetricData':[
        {'MetricName':'FailedFindings','Value':6,'Unit':'Count'},
        {'MetricName':'UnknownFindings','Value':0,'Unit':'Count'},
        {'MetricName':'CompletedRuns','Value':1,'Unit':'Count'},
    ]},'response':{}}]}}
    with Offline(f) as provider:
        assert publish_metrics(data,provider,REGION,True)['status']=='PUBLISHED'


def test_metrics_require_config():
    with pytest.raises(ValueError):publish_metrics(run(fixture()),enabled=True)


def test_demo_never_publishes_metrics(monkeypatch):
    from medtech.lambda_handler import handler
    monkeypatch.setenv('SCAN_MODE','demo');monkeypatch.setenv('DEMO_SCENARIO','incomplete');monkeypatch.setenv('ENABLE_METRICS','true')
    result=handler({},None)
    assert result['metrics']['status']=='DISABLED'
    assert result['report']['summary']['status']=='INCOMPLETE'


def test_unknown_before_pass():
    assert priority_findings(run(fixture('incomplete')))[0]['status']=='UNKNOWN'


def test_html_upload_failure_propagates():
    from medtech.delivery import deliver
    class BrokenHTML:
        def client(self,*args):return self
        def put_object(self,**kw):
            if kw['Key'].endswith('.html'):raise RuntimeError('HTML upload failure')
        def publish(self,**kw):pytest.fail('should not publish after partial upload')
    with pytest.raises(RuntimeError):deliver(run(fixture('misconfigured')),BrokenHTML(),REGION,'reports','topic',True,True)
