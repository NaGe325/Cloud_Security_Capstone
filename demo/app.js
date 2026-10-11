(() => {
  'use strict';
  const db=window.MEDTECH_DATA;
  const names={S3_PUBLIC_ACCESS:'S3 public access',S3_ENCRYPTION:'S3 default encryption',IAM_MFA:'Root and console-user MFA',EC2_ADMIN_PORTS:'SSH and RDP ingress',CLOUDTRAIL_LOGGING:'CloudTrail logging'};
  const priorities={FAIL:0,UNKNOWN:1,PASS:2,NOT_APPLICABLE:3},severity={CRITICAL:0,HIGH:1,MEDIUM:2,LOW:3,INFORMATIONAL:4};
  let scenario='misconfigured',selected=null;
  const get=id=>document.getElementById(id);
  const text=(id,value)=>get(id).textContent=value;
  const el=(tag,cls,value)=>{const e=document.createElement(tag);if(cls)e.className=cls;if(value!==undefined)e.textContent=value;return e;};
  const report=()=>db[scenario].report;
  function showDetail(f){
    selected=f.id;const d=get('detail');d.replaceChildren();
    const tag=el('span','status '+f.status.toLowerCase(),f.status);tag.style.marginTop='14px';
    d.append(tag,el('h3','',names[f.control_id]),el('p','detail-meta',f.resource+' / '+f.region),el('p','detail-reason',f.reason));
    const next=el('div','next-step');next.append(el('strong','',f.status==='UNKNOWN'?'Restore evidence access':'Recommended next step'),el('span','',f.status==='FAIL'?f.remediation:f.status==='UNKNOWN'?'Review the read permission, then rerun this control. Keep the run marked incomplete until evidence is available.':'No remediation proposed by this check.'));
    d.append(next,el('div','evidence-label','OBSERVED EVIDENCE'),el('pre','',JSON.stringify(f.evidence,null,2)));
    document.querySelectorAll('.finding-button').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.id===selected)));
  }
  function update(){
    const r=report(),s=r.summary,c=s.counts,current=db[scenario];
    document.querySelectorAll('[data-scenario]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.scenario===scenario)));
    text('overall',s.status);get('overall').className='status '+s.status.toLowerCase();
    text('coverage',s.coverage==='INCOMPLETE'?'Coverage incomplete':'Complete within configured scope');text('run-id',r.run_id);
    text('passed',c.PASS);text('failed',c.FAIL);text('unknown',c.UNKNOWN);text('na',c.NOT_APPLICABLE);
    text('scenario-note',current.note);
    const sorted=[...r.findings].sort((a,b)=>priorities[a.status]-priorities[b.status]||severity[a.severity]-severity[b.severity]||a.control_id.localeCompare(b.control_id)||a.resource.localeCompare(b.resource));
    const list=get('findings-list');list.replaceChildren();text('finding-count',r.findings.length+' results / 5 controls');
    sorted.forEach(f=>{const b=el('button','finding-button');b.type='button';b.dataset.id=f.id;b.setAttribute('aria-pressed','false');
      b.append(el('span','name',names[f.control_id]),el('span','severity '+f.severity,f.status==='FAIL'?f.severity:f.status==='NOT_APPLICABLE'?'N/A':f.status),el('span','resource',f.resource));
      b.addEventListener('click',()=>showDetail(f));list.append(b);});
    showDetail(sorted[0]);
    const inputs=get('input-list');inputs.replaceChildren();
    current.inputs.forEach(([name,value])=>{const row=el('div','input-row');row.append(el('strong','',name),el('span','',value));inputs.append(row);});
    text('fixture-json',JSON.stringify(current.fixture,null,2));
    text('notification-state',current.delivery.sns);
    const message=current.delivery.notification_preview;
    text('notification-subject',message?message.Subject:'No notification required');
    text('notification-message',message?JSON.stringify(JSON.parse(message.Message),null,2):'No failed or unknown findings. The report remains available for review.');
    get('download-json').href='reports/'+scenario+'.json';get('download-html').href='reports/'+scenario+'.html';
  }
  document.querySelectorAll('[data-scenario]').forEach(b=>b.addEventListener('click',()=>{scenario=b.dataset.scenario;update();}));
  const tabs=[...document.querySelectorAll('[data-tab]')];
  function showTab(button){tabs.forEach(b=>{const active=b===button;b.setAttribute('aria-selected',String(active));get(b.dataset.tab+'-view').hidden=!active;});}
  tabs.forEach((b,index)=>{b.addEventListener('click',()=>showTab(b));b.addEventListener('keydown',e=>{if(e.key==='ArrowRight'||e.key==='ArrowLeft'){e.preventDefault();const next=tabs[(index+(e.key==='ArrowRight'?1:-1)+tabs.length)%tabs.length];showTab(next);next.focus();}});});
  const comparison=get('compare-grid');
  Object.entries(db).forEach(([key,value])=>{const item=el('div','compare-item');const s=value.report.summary;
    item.append(el('h3','',key[0].toUpperCase()+key.slice(1)),el('span','status '+s.status.toLowerCase(),s.status),el('p','rate',s.assessed_pass_percent+'%'),el('p','',key==='incomplete'?'All assessed items pass, but one control is unknown. The run remains incomplete.':key==='compliant'?'All six assessed items pass. One service identity is not applicable.':'Six baseline gaps need review. Root MFA receives the highest priority.'));comparison.append(item);});
  update();
})();
