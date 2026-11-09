#!/usr/bin/env python3
"""
Adds 'return to customer + full re-edit' to:
  Fxflowofficial.html          (customer portal)
  FXFlowAdminPortal 3.html     (admin portal)

Usage:  put this script next to both HTML files, then
        python3 patch_fxflow.py
Creates .bak backups and patches in place. Safe to re-run.
"""
import sys, shutil, pathlib

CUST  = "Fxflowofficial.html"
ADMIN = "FXFlowAdminPortal 3.html"
E = []
def add(f, l, o, n): E.append((f, l, o, n))

# ============================ CUSTOMER PORTAL ============================

# C1  CSS: returned-request card on the landing page
add(CUST, "C1 CSS returned card",
r""".banner{margin-top:16px;padding:14px;background:var(--cream);border:1px solid var(--gold);border-radius:8px;color:var(--heading)}
.banner.ok{border-color:var(--success)}""",
r""".banner{margin-top:16px;padding:14px;background:var(--cream);border:1px solid var(--gold);border-radius:8px;color:var(--heading)}
.banner.ok{border-color:var(--success)}
.ret{width:100%;max-width:420px;background:#fff8f8;border:1px solid var(--alert);border-radius:12px;padding:16px;text-align:left}
.ret-h{display:flex;align-items:flex-start;gap:10px;margin-bottom:10px}
.ret-i{width:28px;height:28px;flex:none;border-radius:50%;background:var(--alert);color:#fff;display:flex;align-items:center;justify-content:center;font-weight:800}
.ret-row{padding:12px 0;border-top:1px solid rgba(214,69,69,.25)}
.ret-row:first-of-type{border-top:0;padding-top:0}
.ret-row .btn{margin-top:10px}""")

# C2  helper that lists returned requests
add(CUST, "C2 RETURNED() helper",
r"""const rqUpd=(tf,f)=>{const o=rqAll();if(!o[tf])return false;f(o[tf]);rqSave(o);return true};""",
r"""const rqUpd=(tf,f)=>{const o=rqAll();if(!o[tf])return false;f(o[tf]);rqSave(o);return true};
const RETURNED=()=>Object.entries(rqAll()).filter(([k,r])=>r&&r.status==='Returned').map(([tf,r])=>({tf,r})).sort((a,b)=>new Date((b.r.return&&b.r.return.at)||b.r.at||0)-new Date((a.r.return&&a.r.return.at)||a.r.at||0));""")

# C3  home screen: notification card + count on Track button
add(CUST, "C3 home screen notice",
r"""home:()=>`<div class="stack home"><span class="badge">Foreign Transfers Made Simple</span><h1 class="h1">Your Foreign Transfer Starts Here</h1><p class="body muted center">Request a foreign transfer, upload your documents and track every stage online.</p>${btn('Start a Transfer','go:ctype','w-281')}${btn('Track My Request','go:track','secondary w-281')}${btn('Upload After Shipment Documents','go:psfind','secondary w-281')}<p class="hint center" style="margin-top:-12px">For Advance Payment requests only.</p>${rates()}</div>`,""",
r"""home:()=>{const n=RETURNED().length;return `<div class="stack home"><span class="badge">Foreign Transfers Made Simple</span><h1 class="h1">Your Foreign Transfer Starts Here</h1><p class="body muted center">Request a foreign transfer, upload your documents and track every stage online.</p>${retCard()}${btn('Start a Transfer','go:ctype','w-281')}${btn('Track My Request'+(n?' · '+n+' returned':''),'go:track','secondary w-281')}${btn('Upload After Shipment Documents','go:psfind','secondary w-281')}<p class="hint center" style="margin-top:-12px">For Advance Payment requests only.</p>${rates()}</div>`},""")

# C4  track screen: returned status + reason + re-edit button
add(CUST, "C4 track screen",
r"""track:()=>{const r=S.tr&&TRK()[S.tr],st=r?STAGES(r.g):[];return `<div class="content track"><h2 class="h2">Track your transfer</h2><p class="small muted sub">Enter your Request ID to see where your transfer is.</p><div class="tsearch"><input id="tq" placeholder="Request ID, e.g. TF2026000184" value="${e(S.tq||S.ref||'')}" autocomplete="off" aria-label="Request ID"><button class="btn" data-act="tsearch">Search</button></div>${err('tq')}${r?`<div class="dark pop"><div class="dark-title">GCB FXFlow</div><div class="small white">Request ID: ${e(S.tr)}</div><div class="small white">Status: ${r.at===0?'Submitted':r.at>=st.length-1?'Completed':'Under Review'}</div><div class="stages">${st.map((s,i)=>`<div class="stage${i===r.at?' current':i>r.at?' wait':''}"><i></i><span>${s}</span></div>`).join('')}</div></div><p class="small muted note">We’ll email ${S.email?e(S.email):'you'} each time your request moves to the next stage.</p>${psTrack()}`:'<div class="demo">Demo Request ID: TF2026000184</div>'}${btn('Back to Home','go:home','secondary w-full')}</div>`},""",
r"""track:()=>{const r=S.tr&&TRK()[S.tr],st=r?STAGES(r.g):[],rr=S.tr?rqGet(S.tr):null,isRet=!!(rr&&rr.status==='Returned');return `<div class="content track"><h2 class="h2">Track your transfer</h2><p class="small muted sub">Enter your Request ID to see where your transfer is.</p><div class="tsearch"><input id="tq" placeholder="Request ID, e.g. TF2026000184" value="${e(S.tq||S.ref||'')}" autocomplete="off" aria-label="Request ID"><button class="btn" data-act="tsearch">Search</button></div>${err('tq')}${r?`<div class="dark pop"><div class="dark-title">GCB FXFlow</div><div class="small white">Request ID: ${e(S.tr)}</div><div class="small white">Status: ${isRet?'Returned for corrections':r.at===0?'Submitted':r.at>=st.length-1?'Completed':'Under Review'}</div><div class="stages">${st.map((s,i)=>`<div class="stage${i===r.at?' current':i>r.at?' wait':''}"><i></i><span>${s}</span></div>`).join('')}</div></div>${isRet?retNote(rr):''}<p class="small muted note">We’ll email ${S.email?e(S.email):'you'} each time your request moves to the next stage.</p>${psTrack()}`:'<div class="demo">Demo Request ID: TF2026000184</div>'}${btn('Back to Home','go:home','secondary w-full')}</div>`},""")

# C5  new render helpers before the SC screen map
add(CUST, "C5 retCard/retNote/isResub",
r"""function boot(){rqSeed();const m=location.hash.match(/^#sig=([A-Za-z0-9]+)/);if(m)return openSig(m[1],1);if(location.hash==='#signatories'){const R=msLoad();if(R&&R.ctx){restoreCtx(R);hist=['home','ctype','ctin','identity'];cur='sigs';return render()}}render()}

const SC={""",
r"""function boot(){rqSeed();const m=location.hash.match(/^#sig=([A-Za-z0-9]+)/);if(m)return openSig(m[1],1);if(location.hash==='#signatories'){const R=msLoad();if(R&&R.ctx){restoreCtx(R);hist=['home','ctype','ctin','identity'];cur='sigs';return render()}}render()}

const isResub=()=>{const r=S.ref&&rqGet(S.ref);return !!(r&&r.resub)};
const retCard=()=>{const R=RETURNED();if(!R.length)return '';return `<div class="ret" role="alert"><div class="ret-h"><span class="ret-i">!</span><div><div class="card-title">Action needed: ${R.length} transfer${R.length>1?'s':''} returned</div><div class="small muted">The bank returned ${R.length>1?'these requests':'this request'} for corrections. Edit and resubmit to continue.</div></div></div>${R.map(({tf,r})=>`<div class="ret-row"><div><b>${e(tf)}</b> · USD ${Number(r.amt||0).toLocaleString()}${r.purpose?' · '+e(r.purpose):''}</div>${r.return&&r.return.reason?`<div class="small" style="margin-top:4px">Reason: ${e(r.return.reason)}</div>`:''}<div class="small muted" style="margin-top:2px">${r.return&&r.return.at?'Returned '+fdt(r.return.at):'Returned for corrections'}${r.return&&r.return.by?' · '+e(r.return.by):''}</div>${btn('Edit and resubmit','reedit:'+e(tf),'w-full')}</div>`).join('')}</div>`};
const retNote=r=>`<div class="banner miss"><div class="card-title">Returned for corrections</div><div class="small">${e((r.return&&r.return.reason)||'Please review your request and resubmit with the required changes.')}</div><div class="small muted" style="margin-top:4px">${r.return&&r.return.at?'Returned '+fdt(r.return.at):''}${r.return&&r.return.by?' by '+e(r.return.by):''}</div>${btn('Edit and resubmit','reedit:'+e(r.tf||S.tr),'w-full')}</div>`;

const SC={""")

# C6  loadReedit(): turns a returned request back into full wizard state
add(CUST, "C6 loadReedit()",
r"""S.st='ok';if(!S.nm)S.nm=NMMAP[S.type]||''}
function chkcard(){""",
r"""S.st='ok';if(!S.nm)S.nm=NMMAP[S.type]||''}
function loadReedit(tf,r){if(!r)return;S.reeditTF=tf;S.subd='';S.ref='';
S.ctype=r.kind==='co'?'co':'ind';S.kind=r.kind==='co'?'co':'ind';S.mand=S.kind==='co'?2:1;
S.card=S.kind==='ind'?(r.cid||''):'';S.tin=S.kind==='co'?(r.cid||''):'';
S.acct=r.acct||'';S.srcno=r.acct||'';
const rec=REC[r.acct]||{},cur=r.srcCur||rec.cur||'';
S.src=SRCS.find(x=>cur&&x.indexOf('('+cur+')')>=0)||'';
S.fat=r.fat||rec.fat||'';
S.aname=rec.n||r.cname||'';S.phone=rec.p?'0'+rec.p:'';S.email=rec.e||r.email||'';S.dob=rec.dob||r.dob||'';
S.grp=r.grp;S.type=r.type||'';S.purpose=r.purpose||'';
S.amt=String(r.amt==null?'':r.amt);
S.items=Array.isArray(r.items)&&r.items.length?r.items.map(x=>({d:x.d||'',inv:x.inv==null?'':String(x.inv),pay:x.pay==null?'':String(x.pay),idf:x.idf||'',idfd:x.idfd||'',gorig:x.gorig||'',garr:x.garr||''})):[{d:'',inv:'',pay:'',idf:'',idfd:'',gorig:'',garr:''}];
const b=r.ben||{};
S.bname=b.name||'';S.bcountry=b.country||'';S.bbank=b.bank||'';S.swift=b.swift||'';
S.bacct=b.acctFull||(/^[•]/.test(String(b.acct||''))?'':b.acct||'');
S.baddr=b.addr||'';S.bbaddr=b.bankAddr||'';S.ibank=b.ibank||'';S.ibic=b.ibic||'';S.route=b.route||'';
S.rel=r.rel||'';S.chg=r.chg||'';S.branch=r.branch||'';
S.nm=r.nm||'';S.nmo=r.nmo||'';S.nmx=!!r.nmx;
S.raddr=r.raddr||rec.addr||'';S.post=r.post||'';S.adbt=r.adbt||'';
S.rt=r.rt||'ind';S.cm=r.cm||'ind';S.srate=r.srate||'';S.scom=r.scom||'';
S.agr=r.agr?{name:r.agr.name,size:r.agr.size||0}:null;
S.files={};S.signed=false;S.sigD='';S.sigU='';S.sigMode='';S.sigOk=false;S.tc=false;S.ok=false;S.pok=true;S.menu=false;S.modal=false;S.ct=0;S.sf=0;
S.mrec=null;S.mkey='';
if(S.kind==='co'){const ks=Object.keys(REC).filter(k=>REC[k].tin===S.tin),mk=ks.find(k=>REC[k].sg)||r.acct;S.mkey=mk||'';S.mrec=(REC[mk]||{}).sg||null;S.sg=((REC[mk]||{}).sg||[]).map(g=>({card:g.card,phone:'0'+g.p,email:g.e}));while(S.sg.length<2)S.sg.push({card:'',phone:'',email:''})}
S.er={};S.tries=0;S.st='ok';
hist=[];cur='accts';render('fwd')}
function chkcard(){""")

# C7  submitReq(): resubmission branch keeps the same TF number
add(CUST, "C7 submitReq resubmission",
r"""function submitReq(){if(S.subd&&S.subd===S.ref)return go('done');const b=balChk();if(!S.acct||!b.ok){go('review');S.er={tick:(b.why||BALMSG)+' <button class="edit" data-act="go:amount">Change amount</button> <button class="edit" data-act="go:accts">Choose another account</button>'};return render()}
const o=rqAll();let tf;do{tf='TF2026'+(Math.floor(Math.random()*900000)+100000)}while(o[tf]||TRKDEMO[tf]);
o[tf]={tf,kind:S.kind==='co'?'co':'ind',cid:S.kind==='co'?S.tin:S.card,cname:S.aname,grp:G(),type:S.type,purpose:(TYPES[S.type]||{}).t||'',acct:S.acct,srcCur:CUR(),txCur:'USD',amt:+S.amt,debit:dbt(),rate:rateTxt(),branch:S.branch||'',ben:{name:S.bname,country:S.bcountry,bank:S.bbank,swift:S.swift,acct:'•••• '+String(S.bacct||'').slice(-4)},items:TR()?S.items.map(x=>({d:x.d,inv:+x.inv,pay:+x.pay,idf:x.idf})):[],at:new Date().toISOString(),stage:0,status:'Submitted'};
if(G()==='adv')o[tf].ps={docs:{},submitted:false,status:'Pending Documents'};
rqSave(o);S.ref=tf;S.subd=tf;go('done')}""",
r"""function submitReq(){if(S.subd&&S.subd===S.ref)return go('done');const b=balChk();if(!S.acct||!b.ok){go('review');S.er={tick:(b.why||BALMSG)+' <button class="edit" data-act="go:amount">Change amount</button> <button class="edit" data-act="go:accts">Choose another account</button>'};return render()}
const now=new Date().toISOString();
const core={kind:S.kind==='co'?'co':'ind',cid:S.kind==='co'?S.tin:S.card,cname:S.aname,grp:G(),type:S.type,purpose:(TYPES[S.type]||{}).t||'',acct:S.acct,srcCur:CUR(),txCur:'USD',amt:+S.amt,debit:dbt(),rate:rateTxt(),branch:S.branch||'',ben:{name:S.bname,country:S.bcountry,bank:S.bbank,swift:S.swift,acct:'•••• '+String(S.bacct||'').slice(-4),acctFull:S.bacct||'',addr:S.baddr||'',bankAddr:S.bbaddr||'',ibank:S.ibank||'',ibic:S.ibic||'',route:S.route||''},items:TR()?S.items.map(x=>({d:x.d,inv:+x.inv,pay:+x.pay,idf:x.idf||'',idfd:x.idfd||'',gorig:x.gorig||'',garr:x.garr||''})):[],stage:0,status:'Submitted',src:S.src||'',fat:S.fat||'',chg:S.chg||'',rel:S.rel||'',nm:S.nm||'',nmo:S.nmo||'',nmx:!!S.nmx,raddr:S.raddr||'',post:S.post||'',adbt:S.adbt||'',rt:S.rt||'ind',cm:S.cm||'ind',srate:S.srate||'',scom:S.scom||'',agr:S.agr?{name:S.agr.name,size:S.agr.size||0}:null,mand:S.mand,phone:S.phone||'',email:S.email||'',dob:S.dob||''};
if(G()==='adv')core.ps={docs:{},submitted:false,status:'Pending Documents'};
const o=rqAll();
if(S.reeditTF){const tf=S.reeditTF,old=o[tf]||{};o[tf]=Object.assign({},old,core,{tf,at:now,firstAt:old.firstAt||old.at,resubmittedAt:now,resub:(old.resub||0)+1,return:null,returnHistory:(old.returnHistory||[]).concat(old.return?[old.return]:[])});rqSave(o);S.ref=tf;S.subd=tf;S.reeditTF='';return go('done')}
let tf;do{tf='TF2026'+(Math.floor(Math.random()*900000)+100000)}while(o[tf]||TRKDEMO[tf]);
o[tf]=Object.assign({tf,at:now,firstAt:now},core);rqSave(o);S.ref=tf;S.subd=tf;go('done')}""")

# C8  confirmation screen reflects a resubmission
add(CUST, "C8 confirmation title",
r"""<h1 class="h1">Request Submitted</h1><p class="body muted center">Your request has been submitted successfully for review</p>""",
r"""<h1 class="h1">${isResub()?'Request Resubmitted':'Request Submitted'}</h1><p class="body muted center">${isResub()?'Your changes have been submitted again for review':'Your request has been submitted successfully for review'}</p>${isResub()?`<div class="banner ok">Resubmitted after corrections. This is submission ${rqGet(S.ref).resub+1} for ${e(S.ref)}.</div>`:''}""")

# C9  account step banner while re-editing
add(CUST, "C9 accts re-edit banner",
r"""accts:()=>{const L=elig(),co=S.ctype==='co';return `<div class="content">${hd(2)}<h2 class="h2">Choose the account to pay from</h2>""",
r"""accts:()=>{const L=elig(),co=S.ctype==='co';return `<div class="content">${hd(2)}${S.reeditTF?`<div class="banner miss"><div class="card-title">Editing returned request ${e(S.reeditTF)}</div><div class="small">Make your changes, then continue to review and resubmit.${(rqGet(S.reeditTF)||{}).return&&rqGet(S.reeditTF).return.reason?' Reason given: '+e(rqGet(S.reeditTF).return.reason):''}</div></div>`:''}<h2 class="h2">Choose the account to pay from</h2>""")

# C10 action map: reedit handler + clear re-edit state on fresh start
add(CUST, "C10 A map reedit",
r"""const A={go,back,chkcard,shot,...MS,""",
r"""const goA=n=>{if(n==='ctype'||n==='home')S.reeditTF='';go(n)};
const A={go:goA,back,chkcard,shot,reedit:v=>{const r=rqGet(v);if(!r){S.er={};return render()}loadReedit(v,r)},...MS,""")

add(CUST, "C10b jump clears reedit",
r"""jump:v=>{seed();S.subd='';S.menu=false;S.tr='';cur=v;hist=[];S.er={};render('fwd')},""",
r"""jump:v=>{seed();S.reeditTF='';S.subd='';S.menu=false;S.tr='';cur=v;hist=[];S.er={};render('fwd')},""")

# C11 live refresh when the admin returns/resubmits in another tab
add(CUST, "C11 storage listener",
r"""addEventListener('storage',ev=>{if(ev.key===RQK&&(cur==='psup'||cur==='track'))render();if(ev.key===MSK&&(cur==='sigs'||cur==='sigv'))render()});""",
r"""addEventListener('storage',ev=>{if(ev.key===RQK&&(cur==='psup'||cur==='track'||cur==='home'||cur==='done'))render();if(ev.key===MSK&&(cur==='sigs'||cur==='sigv'))render()});""")

# ============================ ADMIN PORTAL ============================

# A1 docRows(): ignore reviews recorded before the customer's resubmission
add(ADMIN, "A1 docRows stale reviews",
r"""function docRows(v){const a=A(v.tf).docs;return reqDocs(v).map(d=>Object.assign(d,{rv:a[d.k]||null}))}""",
r"""function docRows(v){const a=A(v.tf).docs,cut=tm(v.r.resubmittedAt||0);return reqDocs(v).map(d=>{const rv=a[d.k]||null,stale=!!(rv&&cut&&tm(rv.at)<cut);return Object.assign(d,{rv:stale?null:rv,stale})})}""")

# A2 events(): show resubmission in the activity timeline
add(ADMIN, "A2 events resubmission",
r"""function events(v){const E=[];if(v.at)E.push({at:v.at,t:'Request submitted',d:GRP[v.grp]+', '+v.cur+' '+fm(v.amt),src:'Customer record'});
  const ps=v.r.ps;""",
r"""function events(v){const E=[],first=v.r.firstAt||v.at;if(first)E.push({at:first,t:'Request submitted',d:GRP[v.grp]+', '+v.cur+' '+fm(v.amt),src:'Customer record'});
  if(v.r.resubmittedAt)E.push({at:v.r.resubmittedAt,t:'Customer resubmitted after corrections'+(v.r.resub?' (resubmission '+v.r.resub+')':''),d:(v.r.returnHistory&&v.r.returnHistory.length)?'Last return reason: '+v.r.returnHistory[v.r.returnHistory.length-1].reason:'',src:'Customer record'});
  const ps=v.r.ps;""")

# A3 clearer label when returning after a Payments rejection
add(ADMIN, "A3 return action label",
r"""  if(['submitted','docs','review'].includes(v.cat))L.push({id:'return',l:'Request Corrections',to:'returned',bad:1,reason:1});""",
r"""  if(['submitted','docs','review'].includes(v.cat))L.push({id:'return',l:(A(v.tf).sentBack&&v.cat==='review')?'Return to Customer for Corrections':'Request Corrections',to:'returned',bad:1,reason:1});""")

# A4 doStage(): write the customer-visible return record into the shared request
add(ADMIN, "A4 doStage return record",
r"""   onOk:reason=>{load();const f=DATA.byTf[tf];if(!f||f.cat!==v.cat){toast('This request changed elsewhere. The view has been refreshed.');return render()}
    const ok=rqUpd(tf,r=>setStage(r,f,to));if(!ok&&!memRQ)return toast('The request couldn\'t be saved.');
    const ad=adm(),q=areq(ad,tf),now=new Date().toISOString();if(to==='returned')q.returned={reason,at:now,by:ADMIN.id};if(a.id==='resume')q.returned=null;if(to==='approval'){q.sent={at:now,by:ADMIN.id,note:reason||''};q.sentBack=null}admSave(ad);
    logEv({tf,action:a.l,prev:CAT[v.cat].l,next:CAT[to].l,note:reason||''});toast(v.tf+' is now '+CAT[to].l+'.');render.keepScroll=true;render()}})}""",
r"""   onOk:reason=>{load();const f=DATA.byTf[tf];if(!f||f.cat!==v.cat){toast('This request changed elsewhere. The view has been refreshed.');return render()}
    const now=new Date().toISOString();
    const ok=rqUpd(tf,r=>{setStage(r,f,to);if(to==='returned'){const rec={reason,at:now,by:ADMIN.id,fromStage:f.st,fromStatus:CAT[f.cat].l};r.return=rec;r.returnHistory=Array.isArray(r.returnHistory)?r.returnHistory.concat([rec]):[rec]}else if(a.id==='resume'){r.return=null}});if(!ok&&!memRQ)return toast('The request couldn\'t be saved.');
    const ad=adm(),q=areq(ad,tf);if(to==='returned')q.returned={reason,at:now,by:ADMIN.id};if(a.id==='resume')q.returned=null;if(to==='approval'){q.sent={at:now,by:ADMIN.id,note:reason||''};q.sentBack=null}admSave(ad);
    logEv({tf,action:a.l,prev:CAT[v.cat].l,next:CAT[to].l,note:reason||''});toast(v.tf+' is now '+CAT[to].l+'.');render.keepScroll=true;render()}})}""")

# A5 return modal mentions the landing-page notice
add(ADMIN, "A5 modal body",
r"""${to==='approval'?'<p>It will appear in the Payments Officer\'s Approval Queue.</p>':''}<p class="small muted">This is a simulated prototype action.</p>`,reason:a.reason?'Reason for the customer (required)':'Comment (optional)'""",
r"""${to==='approval'?'<p>It will appear in the Payments Officer\'s Approval Queue.</p>':''}${to==='returned'?'<p>The customer will see an action-needed notice on the customer portal landing page with this reason, and can edit and resubmit the whole transfer.</p>':''}<p class="small muted">This is a simulated prototype action.</p>`,reason:a.reason?'Reason for the customer (required)':'Comment (optional)'""")

# A6 resubmission badge in the detail header
add(ADMIN, "A6 dtitle resubmission badge",
r"""  <div class="dtitle"><h1>Application ${esc(v.tf)}</h1>${badge(v.cat,1)}${v.r.demo?'<span class="tag">Demo record</span>':''}</div>""",
r"""  <div class="dtitle"><h1>Application ${esc(v.tf)}</h1>${badge(v.cat,1)}${v.r.resub?`<span class="b warn">Resubmission ${v.r.resub}</span>`:''}${v.r.demo?'<span class="tag">Demo record</span>':''}</div>""")

# A7 actions card: guidance after a Payments rejection, hidden once resubmitted
add(ADMIN, "A7 sentBack guidance",
r"""  ${s.sentBack&&v.cat==='review'?`<div class="alert warn" style="margin-bottom:12px"><b>Sent back by the Payments Officer</b> on ${fdtt(s.sentBack.at)}: ${esc(s.sentBack.reason)}</div>`:''}""",
r"""  ${s.sentBack&&v.cat==='review'&&(!v.r.resubmittedAt||tm(s.sentBack.at)>tm(v.r.resubmittedAt))?`<div class="alert warn" style="margin-bottom:12px"><b>Sent back by the Payments Officer</b> on ${fdtt(s.sentBack.at)}: ${esc(s.sentBack.reason)}<div class="small" style="margin-top:6px">Review the reason, then either resume review or use Request Corrections to return the request to the customer, who can edit and resubmit the whole transfer.</div></div>`:''}""")

# A8 Payments 'send back' modal mentions the onward customer step
add(ADMIN, "A8 sendback modal text",
r"""  const cfg={sendback:{t:'Send back to Operations?',b:'The request returns to Under Review with your reason. No payment is made.',reason:'Reason (required)',need:1,ok:'Send Back',bad:1},""",
r"""  const cfg={sendback:{t:'Send back to Operations?',b:'The request returns to Under Review with your reason. No payment is made. The Operations Reviewer can then return it to the customer, who can edit and resubmit the whole transfer.',reason:'Reason (required)',need:1,ok:'Send Back',bad:1},""")

# A9 documents tab: resubmission notice
add(ADMIN, "A9 docs resubmission notice",
r"""  let h=`<div class="ctitle">${ic('file')}Initial supporting documents</div><div class="alert info small" style="margin-bottom:14px">""",
r"""  let h=`<div class="ctitle">${ic('file')}Initial supporting documents</div>${v.r.resubmittedAt?`<div class="alert info small" style="margin-bottom:12px">The customer resubmitted this request on ${fdtt(v.r.resubmittedAt)}. Reviews recorded before that date are treated as not reviewed.</div>`:''}<div class="alert info small" style="margin-bottom:14px">""")

# A10 documents tab: mark reviews reset by a resubmission
add(ADMIN, "A10 docs row stale",
r"""  <td>${d.rv?pill(d.rv.st,d.rv.st==='Accepted in Prototype'?'ok':d.rv.st==='Requires Correction'?'bad':'warn')+`<div class="small muted" style="margin-top:4px">${fdtt(d.rv.at)} · ${esc(d.rv.by)}</div>${d.rv.reason?`<div class="small">${esc(d.rv.reason)}</div>`:''}`:pill('Not reviewed','')}</td>""",
r"""  <td>${d.rv?pill(d.rv.st,d.rv.st==='Accepted in Prototype'?'ok':d.rv.st==='Requires Correction'?'bad':'warn')+`<div class="small muted" style="margin-top:4px">${fdtt(d.rv.at)} · ${esc(d.rv.by)}</div>${d.rv.reason?`<div class="small">${esc(d.rv.reason)}</div>`:''}`:(d.stale?pill('Not reviewed','')+'<div class="small muted" style="margin-top:4px">Earlier review reset by the resubmission</div>':pill('Not reviewed',''))}</td>""")

# ============================ APPLY ============================
def main():
    files = {}
    for f, *_ in E:
        p = pathlib.Path(f)
        if not p.exists():
            sys.exit(f"Missing file: {f}  (run this script in the folder that holds both HTML files)")
        files[f] = p.read_text(encoding="utf-8")
    out, problems = dict(files), []
    for f, label, old, new in E:
        t = out[f]
        if old not in t and new in t:
            print(f"skip   {f}: {label} (already applied)"); continue
        c = t.count(old)
        if c != 1:
            problems.append(f"{f}: {label} -> anchor found {c} times (expected 1)"); continue
        out[f] = t.replace(old, new, 1)
        print(f"ok     {f}: {label}")
    if problems:
        print("\nABORTED — nothing was written:")
        for x in problems: print("  -", x)
        sys.exit(1)
    for f, txt in out.items():
        if txt != files[f]:
            shutil.copyfile(f, f + ".bak")
            pathlib.Path(f).write_text(txt, encoding="utf-8")
            print(f"wrote  {f}  (backup: {f}.bak)")
    print("\nDone. Open both pages from the same origin and try the return/resubmit loop.")

if __name__ == "__main__":
    main()