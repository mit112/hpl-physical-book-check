// Runs inside a permitted cua_repl host. All catalog access uses its supplied tab.
// No browser launch, network requests, credentials, holds, or hidden application state.
import {existsSync, mkdirSync, readFileSync, renameSync, writeFileSync} from 'node:fs';
import {execFileSync} from 'node:child_process';
import {join} from 'node:path';

const ENTRY='https://halan.sdp.sirsi.net/client/en_US/hou/';
const challenge=/Just a moment|Performing security verification|Verify you are human/i;
const printFormat=/^(Books?|Large print|Regular print)$/i;
const clean=s=>String(s || '').replace(/\s+/g,' ').trim();
const field=(fields,name)=>clean(fields.find(s=>new RegExp('^'+name+'\\s*:','i').test(s))?.replace(/^[^:]+:/,''));
const recordId=url=>decodeURIComponent(new URL(url).pathname).match(/SD_ILS:(\d+)(?:\/|$)/)?.[1];
const queryKey=url=>new URL(url).searchParams.getAll('qu').map(clean).filter(Boolean).sort().join('\n');
function publicRecord(url) {
  const u=new URL(url);
  if(u.origin!==new URL(ENTRY).origin || u.username || u.password || !u.pathname.includes('/search/detailnonmodal/') || !recordId(url))
    throw new Error('Not an observed public HPL record URL');
  return url;
}

// Selectors describe the inspected public catalog markup. Drift fails closed.
// Only rendered text/cells/links are read; hidden metadata is never a fallback.
function rendered() {
  const visible=e=>e.getClientRects().length>0 && getComputedStyle(e).visibility!=='hidden';
  const text=document.body.innerText;
  const cards=[...document.querySelectorAll('[id^="results_cell"]')].filter(visible).map(e=>{
    const a=e.querySelector('a[id^="detailLink"]');
    return {title:a?.innerText,url:a?.href,text:e.innerText,
      ordinal:Number(e.innerText.match(/^\s*(\d+)\./)?.[1]),
      format:e.innerText.match(/Format:\s*([^\n]+)/)?.[1]?.trim()};
  });
  return {url:location.href,text,cards,
    total:Number(text.match(/([\d,]+) Results Found/i)?.[1]?.replaceAll(',','')),
    fields:[...document.querySelectorAll('#detail_biblio0 > .documentSummaries')].filter(visible).map(e=>e.innerText),
    tables:[...document.querySelectorAll('table')].filter(visible).map(t=>[...t.rows].filter(visible).map(r=>[...r.cells].map(c=>c.innerText.trim()))),
    links:[...document.querySelectorAll('a')].filter(visible).map(a=>({text:a.innerText.trim(),title:a.title,label:a.getAttribute('aria-label'),url:a.href})),
    selects:[...document.querySelectorAll('select')].filter(visible).map(e=>({id:e.id,selected:e.selectedOptions[0]?.textContent.trim()}))};
}

export function makeHplRunner({tab,ledgerPath,processorPath,python='python3'}) {
  if(!tab?.playwright || typeof tab.playwright.evaluate!=='function' || typeof tab.getAXState!=='function')
    throw new Error('A compatible CUA tab is required before executing the queue');
  const directory=ledgerPath+'.browser';
  mkdirSync(directory,{recursive:true});
  const load=path=>JSON.parse(readFileSync(path,'utf8'));
  function save(path,value) {
    writeFileSync(path+'.tmp',JSON.stringify(value,null,2)+'\n');
    renameSync(path+'.tmp',path);
  }
  function broker(...args) {
    try { return JSON.parse(execFileSync(python,['-B',processorPath,...args],{encoding:'utf8',maxBuffer:16*1024*1024})); }
    catch(e) { if(args[0]==='finalize' && e.status===1) return JSON.parse(e.stdout); throw e; }
  }
  const ledger=()=>load(ledgerPath);
  let sequence=0;
  let securityRecovery=false;
  async function capture() {
    await tab.getAXState({emit:false});
    const v=await tab.playwright.evaluate(rendered);
    v.checked_at=new Date().toISOString();
    // Raw views are durable before any subsequent navigation.
    save(join(directory,Date.now()+'-'+(++sequence)+'.view.json'),v);
    if(challenge.test(v.text)) {
      if(!securityRecovery) {
        securityRecovery=true; await tab.reload();
        try {await tab.playwright.getByRole('link',{name:'Advanced Search',exact:true}).waitFor({state:'visible',timeoutMs:15000});}
        catch { /* Preserve the remaining challenge rather than infer inventory. */ }
        return capture();
      }
      const e=new Error('Catalog security challenge remains after one ordinary reload');
      e.sitewide=true; e.evidence=v.text; throw e;
    }
    return v;
  }
  async function search(work,relaxAuthor=false) {
    const queryTitle=work.title.split(':')[0].trim();
    await tab.playwright.getByRole('link',{name:'Advanced Search',exact:true}).click({timeoutMs:15000});
    let v=await capture();
    if(!new URL(v.url).pathname.endsWith('/search/advanced') || v.cards.length || recordId(v.url))
      throw new Error('Advanced Search did not replace the previous result view');
    await tab.playwright.getByRole('textbox',{name:'Title:',exact:true}).fill(queryTitle,{timeoutMs:15000});
    await tab.playwright.getByRole('textbox',{name:'Author:',exact:true}).fill(relaxAuthor?'':work.author,{timeoutMs:15000});
    await tab.playwright.getByRole('checkbox',{name:'Library Search',exact:true}).check({timeoutMs:15000});
    await tab.playwright.getByRole('button',{name:'Advanced Search',exact:true}).click({timeoutMs:15000});
    try {await tab.playwright.locator('[id^="results_cell"], #nm_detail_wrapper').waitFor({state:'visible',timeoutMs:15000});}
    catch { /* Capture the actual destination, including a possible challenge. */ }
    v=await capture();
    const params=new URL(v.url).searchParams;
    const query=params.getAll('qu').filter(Boolean).join(' ');
    if(!clean(query).toLowerCase().includes(clean(queryTitle).toLowerCase()) || params.get('te')!=='ILS')
      throw new Error('Search destination query differs from the requested title');
    const submittedQuery=queryKey(v.url);
    const candidates=[], pages=[], ordinals=new Set(), signatures=new Set();
    while(true) {
      if(queryKey(v.url)!==submittedQuery || new URL(v.url).searchParams.get('te')!=='ILS')
        throw new Error('Page destination query changed during traversal');
      if(!v.cards.length && /No (?:search )?results (?:were )?found|0 Results Found/i.test(v.text)) {
        pages.push(v); break;
      }
      if(v.cards.length===0 && recordId(v.url)) {
        candidates.push({id:recordId(v.url),url:publicRecord(v.url),title:field(v.fields,'Title'),format:field(v.fields,'Format'),text:v.text});
        pages.push(v); break;
      }
      if(!Number.isInteger(v.total) || !v.cards.length) throw new Error('No completed result cards/count; cannot infer zero matches');
      const signature=v.cards.map(c=>c.url).join('\n');
      if(signatures.has(signature)) throw new Error('Repeated or stale search page cards');
      signatures.add(signature);
      pages.push(v);
      const offset=Number(new URL(v.url).searchParams.get('rw') || 0);
      for(const c of v.cards) {
        const position=offset+c.ordinal;
        if(!c.ordinal || ordinals.has(position)) throw new Error('Repeated or missing result position');
        ordinals.add(position);
        const id=recordId(publicRecord(c.url));
        if(queryKey(c.url)!==submittedQuery) throw new Error('Stale candidate query differs from submitted search');
        if(!candidates.some(old=>old.id===id)) candidates.push({...c,id});
      }
      if(ordinals.size===v.total && Math.max(...ordinals)===v.total) break;
      const next=v.links.find(a=>/^(Next|Next >|>)$/i.test(a.text) || /^Next(?: page)?$/i.test(a.title) || a.label==='Next');
      if(!next) throw new Error('Unscreened results remain but no observed Next control');
      const destination=new URL(next.url);
      if(destination.origin!==new URL(ENTRY).origin || destination.username || destination.password
        || !destination.pathname.startsWith('/client/en_US/hou/search/results') || queryKey(next.url)!==submittedQuery)
        throw new Error('Next control is not a scoped public HPL search URL');
      await tab.goto(next.url);
      await tab.playwright.locator('[id^="results_cell"]').waitFor({state:'visible',timeoutMs:15000});
      v=await capture();
    }
    if(!candidates.length && work.author && !relaxAuthor) {
      // Initials can be indexed under the author's expanded given name. A surname
      // query preserves those editions; identity still requires operator review.
      const surname=work.author.trim().split(/\s+/).at(-1);
      const fallback=/\b[A-Za-z]\./.test(work.author) && surname!==work.author
        ? await search({...work,author:surname}) : await search(work,true);
      return {...fallback,pages:[...pages,...fallback.pages]};
    }
    return {pages,candidates,relax_author:relaxAuthor};
  }
  async function readRecord(c,run_id) {
    await tab.goto(publicRecord(c.url));
    await tab.playwright.getByRole('tab',{name:/Click to show holdings/}).waitFor({state:'visible',timeoutMs:15000});
    await capture();
    if(await tab.playwright.getByText('MORE DETAILS',{exact:true}).isVisible()) {
      await tab.playwright.getByText('MORE DETAILS',{exact:true}).click({timeoutMs:15000});
      await capture();
    }
    await tab.playwright.getByRole('tab',{name:/Click to show holdings/}).click({timeoutMs:15000});
    const v=await capture();
    if(recordId(v.url)!==c.id) throw new Error('Detail destination record differs from observed candidate');
    const table=v.tables.find(t=>t[0]?.includes('Library') && t[0]?.includes('Material Type') && t[0]?.includes('Status'));
    const expected=Number(v.text.match(/Copies:\s*(\d+)/)?.[1]);
    return {record_id:c.id,url:v.url,title:field(v.fields,'Title'),author:field(v.fields,'Author'),format:field(v.fields,'Format'),
      language:field(v.fields,'Language'),edition:'Unresolved',match_state:'unresolved',checked_at:v.checked_at,run_id,
      query:new URL(v.url).searchParams.getAll('qu').find(Boolean) || '',
      holdings_complete:!!table && Number.isInteger(expected) && table.length-1===expected,
      ...(Number.isInteger(expected)?{expected_copies:expected}:{}),...(table?{table}:{items:[]}),observation:v};
  }
  return {
    finalize:()=>broker('finalize',ledgerPath),
    retry(key) {
      const state=ledger(), entry=state.titles.find(w=>w.key===key);
      if(!entry) throw new Error('Unknown work key');
      const path=join(directory,key+'.json'), saved=load(path);
      if(saved.run_id!==state.run_id || saved.reopened || entry.browser_reopens) throw new Error('Ordinary reopen recovery is unavailable');
      // Persist intent and invalidate closure in the same atomic ledger write.
      entry.browser_reopens=1; entry.browser_retry=true;
      entry.search_complete=false; entry.editions_complete=false; save(ledgerPath,state);
    },
    async collect(limit=10) {
      if(!Number.isInteger(limit) || limit<1 || limit>10) throw new Error('Collect between one and ten works per host call');
      if(ledger().mode!=='thorough') throw new Error('The live batch runner currently requires thorough mode');
      const queue=broker('next',ledgerPath), works=[];
      const transportErrors=[];
      if(queue.state!=='continue') return {...queue,works};
      for(const work of queue.next_batch.slice(0,limit)) {
        const path=join(directory,work.key+'.json');
        let retained=existsSync(path)?load(path):null;
        if(retained?.run_id!==ledger().run_id) retained=null;
        const entry=ledger().titles.find(w=>w.key===work.key);
        if(retained?.collected && !retained.error && !entry.browser_retry) {works.push(retained); continue;}
        const result={...work,run_id:ledger().run_id,pages:[],candidates:[],collected:false,reopened:entry.browser_reopens>0 || retained?.reopened===true};
        try {
          Object.assign(result,await search(work,retained?.relax_author===true)); save(path,result);
          // A narrower/refreshed search cannot erase a known edition. Revisit its
          // observed URL before accepting closure, including changed holdings.
          const knownRecords=entry.records.map(r=>({id:r.record_id,url:r.url,title:r.title,format:r.format,record:r}));
          for(const known of [...(retained?.candidates || []),...knownRecords]) {
            if(!result.candidates.some(c=>c.id===known.id)) result.candidates.push({...known});
          }
          for(const c of result.candidates) {
            if(printFormat.test(c.format)) c.record=await readRecord(c,result.run_id);
            save(path,result);
          }
          result.collected=true;
        } catch(e) {
          result.error=String(e); result.failure_evidence=e.evidence || String(e);
          if(e.sitewide) broker('checkpoint',ledgerPath,'--kind','access','--detail',result.error,'--evidence',result.failure_evidence);
          if(/CDP.*(?:deadline|timed out)|Browser is not available|browser.*(?:closed|disconnected)|kernel reset/i.test(result.error))
            transportErrors.push(result.error);
          const hostBlocked=transportErrors.length>=2;
          if(hostBlocked) broker('checkpoint',ledgerPath,'--kind','host_limit',
            '--detail','Two catalog actions failed in the host browser transport; remaining work is unverified.',
            '--evidence',transportErrors.join('\n'));
          save(path,result); works.push(result);
          if(e.sitewide || hostBlocked) return {state:'blocked',works};
          continue;
        }
        save(path,result); works.push(result);
      }
      return {state:'review',works};
    },
    review(reviews) {
      for(const review of reviews) {
        const saved=load(join(directory,review.key+'.json'));
        if(saved.run_id!==ledger().run_id || !saved.collected || saved.error) throw new Error('No complete current-run collection to review');
        if(review.decisions.length!==saved.candidates.length || new Set(review.decisions.map(d=>d.id)).size!==saved.candidates.length)
          throw new Error('Every observed candidate requires exactly one decision');
        const prepared=[];
        for(const c of saved.candidates) {
          const d=review.decisions.find(d=>d.id===c.id);
          if(!d || !['exact','excluded','unresolved'].includes(d.match_state)) throw new Error('Missing candidate identity decision');
          if(d.match_state==='excluded' && !d.reason?.trim()) throw new Error('Exclusion needs an observed reason');
          if(d.match_state!=='excluded' && !c.record) throw new Error('Matching candidate has no captured record');
          const record={...(c.record || {record_id:c.id,url:c.url,title:c.title,author:'Excluded candidate',format:c.format,
            language:'',holdings_complete:false,items:[],checked_at:saved.pages[0].checked_at,run_id:saved.run_id,
            query:new URL(c.url).searchParams.getAll('qu').find(Boolean) || ''}),
            match_state:d.match_state,edition:d.edition || 'Excluded',reason:d.reason};
          delete record.observation;
          if(d.match_state==='exact' && !d.edition) throw new Error('Confirm the observed edition before accepting identity');
          if(d.match_state==='excluded' && !record.author) record.author='Unknown';
          const path=join(directory,review.key+'-'+c.id+'.record.json'); save(path,record); prepared.push(path);
        }
        for(const path of prepared) broker('ingest',ledgerPath,'--key',review.key,'--record',path);
        save(join(directory,review.key+'.review.json'),review);
        if(review.decisions.every(d=>d.match_state==='excluded') && !saved.relax_author && saved.author) {
          saved.collected=false; saved.relax_author=true; save(join(directory,review.key+'.json'),saved);
        } else if(review.decisions.every(d=>d.match_state!=='unresolved')) {
          broker('mark',ledgerPath,'--key',review.key,'--search-complete','--editions-complete',
            ...(saved.relax_author?['--fallback-complete']:[]));
        }
        const state=ledger(), entry=state.titles.find(w=>w.key===review.key);
        entry.browser_retry=false; save(ledgerPath,state);
      }
      return broker('next',ledgerPath);
    }
  };
}
