import test from 'node:test';
import assert from 'node:assert/strict';
import {mkdtempSync, readFileSync, writeFileSync, existsSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {join, resolve} from 'node:path';
import {execFileSync} from 'node:child_process';
import {makeHplRunner} from '../skills/hpl-physical-book-check/scripts/hpl_browser.mjs';

// Breaks caught: returning after one work; accepting stale results; losing a captured
// work at restart; treating a challenge as no matches; closing unreviewed identity.
const processor = resolve('skills/hpl-physical-book-check/scripts/hpl_evidence.py');
const python = process.env.HPL_TEST_PYTHON || 'python3';
const origin = 'https://halan.sdp.sirsi.net/client/en_US/hou/';
function setup(titles) {
  const dir = mkdtempSync(join(tmpdir(), 'hpl-browser-'));
  const ledgerPath = join(dir, 'ledger.json');
  writeFileSync(join(dir, 'titles.json'), JSON.stringify(titles));
  execFileSync(python, ['-B', processor, 'init', '--titles', join(dir, 'titles.json'), '--output', ledgerPath, '--branch', 'Looscan']);
  return {dir, ledgerPath, processorPath:processor, python};
}
const card = (title, id) => ({id:String(id), url:origin+'search/detailnonmodal/ent:$002f$002fSD_ILS$002f0$002fSD_ILS:'+id+'/ada?qu=TITLE%3D'+encodeURIComponent(title), title,
  text:title+'\nAuthor: Example, Alice\nFormat: Books\nCopies: 1', format:'Books', ordinal:1});
function fakeTab(views) {
  let state = {url:origin, text:'Advanced Search', links:[], cards:[], tables:[]};
  let submittedTitle='';
  const visited=[];
  return {
    visited,
    goto:async url => { visited.push(url); state={...views.shift(), url}; },
    reload:async () => {state=views.shift() || state;},
    getAXState:async () => state.text,
    playwright:{
      evaluate:async () => structuredClone(state),
      getByRole:(_role, options) => ({fill:async value=>{if(options.name==='Title:') submittedTitle=value;}, check:async()=>{}, selectOption:async()=>{}, waitFor:async()=>{},
        click:async()=>{if(options.name==='Advanced Search') {
          state=views.shift() || state;
          if(state.expectedTitle) assert.equal(submittedTitle,state.expectedTitle);
        }}}),
      getByText:()=>({click:async()=>{}, waitFor:async()=>{},isVisible:async()=>false}),
      locator:()=>({waitFor:async()=>{}})
    }
  };
}
function search(title, id) {
  return {url:origin+'search/results?qu=TITLE%3D'+encodeURIComponent(title)+'&te=ILS',text:'1 Results Found',total:1,
    cards:[card(title,id)],links:[],tables:[]};
}
const advanced = {url:origin+'search/advanced',text:'Title: Library Search',cards:[],links:[],tables:[]};
const detail = title => ({text:'Title : '+title+'\nAuthor: Example, Alice\nFormat: Books\nLanguage: English\nCopies: 1',
  fields:['Title : '+title,'Author: Example, Alice','Format: Books','Language: English','Physical Description: 100 pages'],
  cards:[],links:[],tables:[[['Library','Material Type','Shelf Number','Status'],['Looscan','Book','EXAMP','Available']]]});

test('collects every queued work and requires review before completion', async () => {
  const opts=setup([{title:'Alpha',author:'Alice Example'},{title:'Beta',author:'Alice Example'}]);
  const tab=fakeTab([advanced,search('Alpha',1),detail('Alpha'),advanced,search('Beta',2),detail('Beta')]);
  const runner=makeHplRunner({...opts,tab});
  const result=await runner.collect();
  assert.deepEqual(result.works.map(w=>w.title),['Alpha','Beta']);
  assert.equal(runner.finalize().state,'continue');
  assert.ok(existsSync(join(opts.ledgerPath+'.browser',result.works[0].key+'.json')));
  runner.review(result.works.map(w=>({key:w.key,decisions:[{id:w.candidates[0].id,match_state:'exact',edition:'Regular print'}]})));
  assert.equal(runner.finalize().state,'complete');
});

test('restart reuses retained collection without losing pending review', async () => {
  const opts=setup([{title:'Alpha',author:'Alice Example'}]);
  const first=makeHplRunner({...opts,tab:fakeTab([advanced,search('Alpha',1),detail('Alpha')])});
  await first.collect();
  const resumed=makeHplRunner({...opts,tab:fakeTab([])});
  assert.equal((await resumed.collect()).works[0].candidates[0].record.table[1][3],'Available');
  assert.equal(resumed.finalize().state,'continue');
});

test('a challenge stops the whole batch once and retains the actual failure', async () => {
  const opts=setup([{title:'Alpha',author:'Alice Example'},{title:'Beta',author:'Alice Example'}]);
  const challenge={url:origin,text:'Just a moment... Performing security verification',cards:[],links:[],tables:[]};
  const runner=makeHplRunner({...opts,tab:fakeTab([challenge,challenge])});
  await runner.collect();
  const receipt=runner.finalize();
  assert.equal(receipt.state,'blocked');
  assert.match(receipt.blockers[0].evidence,/security verification/);
  assert.equal(receipt.remaining,2);
});

test('stale search destination is retained as a gap, never closed as no match', async () => {
  const opts=setup([{title:'Alpha',author:'Alice Example'}]);
  const runner=makeHplRunner({...opts,tab:fakeTab([advanced,search('Old title',3)])});
  const result=await runner.collect();
  assert.equal(runner.finalize().state,'continue');
  assert.match(result.works[0].error,/query|destination/i);
  assert.equal(JSON.parse(readFileSync(opts.ledgerPath)).titles[0].search_complete,false);
});

test('follows the observed aria-labelled Next link and retains both pages', async () => {
  const opts=setup([{title:'Alpha',author:'Alice Example'}]);
  const first={...search('Alpha',1),total:2,links:[{text:'',title:'',label:'Next',url:origin+'search/results?qu=TITLE%3DAlpha&te=ILS&rw=1'}]};
  const second={...search('Alpha',2),total:2,cards:[{...card('Alpha',2),ordinal:1}]};
  const runner=makeHplRunner({...opts,tab:fakeTab([advanced,first,second,detail('Alpha'),detail('Alpha')])});
  const result=await runner.collect();
  assert.deepEqual(result.works[0].candidates.map(c=>c.id),['1','2']);
  assert.equal(result.works[0].pages.length,2);
  assert.equal(result.works[0].collected,true);
});

test('searches the main title without requiring a subtitle to be indexed', async () => {
  const opts=setup([{title:'Alpha: A Long Subtitle',author:'Alice Example'}]);
  const view={...search('Alpha',1),expectedTitle:'Alpha'};
  const runner=makeHplRunner({...opts,tab:fakeTab([advanced,view,detail('Alpha')])});
  const result=await runner.collect();
  assert.equal(result.works[0].collected,true);
  assert.equal(result.works[0].candidates[0].id,'1');
});

test('an explicit zero triggers an author-relaxed search before a no-match receipt', async () => {
  const opts=setup([{title:'Alpha',author:'Alice Example'}]);
  const zero={...search('Alpha',1),text:'No results found',total:0,cards:[]};
  const runner=makeHplRunner({...opts,tab:fakeTab([advanced,zero,advanced,zero])});
  const result=await runner.collect();
  assert.equal(result.works[0].pages.length,2);
  runner.review([{key:result.works[0].key,decisions:[]}]);
  assert.equal(runner.finalize().state,'complete');
});

test('a short host call checkpoints a work without declaring the request done', async () => {
  const opts=setup([{title:'Alpha',author:'Alice Example'},{title:'Beta',author:'Alice Example'}]);
  const runner=makeHplRunner({...opts,tab:fakeTab([advanced,search('Alpha',1),detail('Alpha'),advanced,search('Beta',2),detail('Beta')])});
  const result=await runner.collect(1);
  assert.equal(result.works.length,1);
  assert.equal(runner.finalize().remaining,2);
  runner.review([{key:result.works[0].key,decisions:[{id:'1',match_state:'exact',edition:'Regular print'}]}]);
  assert.equal(runner.finalize().next_batch[0].title,'Beta');
});

test('an unrelated record with no displayed author can be excluded without inventing one', async () => {
  const opts=setup([{title:'Alpha',author:'Alice Example'}]);
  const unrelated={...detail('Other work'),fields:['Title : Other work','Format: Books','Language: English']};
  const runner=makeHplRunner({...opts,tab:fakeTab([advanced,search('Alpha',1),unrelated])});
  const result=await runner.collect();
  assert.doesNotThrow(()=>runner.review([{key:result.works[0].key,decisions:[{id:'1',match_state:'excluded',reason:'Observed different title: Other work'}]}]));
  const stored=JSON.parse(readFileSync(opts.ledgerPath));
  assert.equal(stored.titles[0].records[0].author,'Unknown');
  assert.equal(runner.finalize().state,'continue');
});

test('an external Next link cannot navigate outside the public catalog', async () => {
  const opts=setup([{title:'Alpha',author:'Alice Example'}]);
  const first={...search('Alpha',1),total:2,links:[{label:'Next',url:'https://example.org/account'}]};
  const tab=fakeTab([advanced,first,search('Alpha',2)]);
  const runner=makeHplRunner({...opts,tab});
  await runner.collect();
  assert.ok(tab.visited.every(url=>new URL(url).origin===new URL(origin).origin));
  assert.equal(runner.finalize().state,'continue');
});

test('new URL with stale candidate links does not close a search', async () => {
  const opts=setup([{title:'Alpha',author:'Alice Example'}]);
  const stale={...search('Alpha',1),cards:[card('Old title',1)]};
  const runner=makeHplRunner({...opts,tab:fakeTab([advanced,stale,detail('Old title')])});
  const result=await runner.collect();
  assert.equal(result.works[0].collected,false);
  assert.match(result.works[0].error,/query|stale/i);
});

test('a repeated card set at a new page offset cannot close missing pages', async () => {
  const opts=setup([{title:'Alpha',author:'Alice Example'}]);
  const first={...search('Alpha',1),total:2,links:[{label:'Next',url:origin+'search/results?qu=TITLE%3DAlpha&te=ILS&rw=1'}]};
  const runner=makeHplRunner({...opts,tab:fakeTab([advanced,first,{...search('Alpha',1),total:2},detail('Alpha')])});
  const result=await runner.collect();
  assert.equal(result.works[0].collected,false);
  assert.match(result.works[0].error,/Repeated|stale/i);
});

test('one bounded reopen replaces a retained unresolved item observation', async () => {
  const opts=setup([{title:'Alpha',author:'Alice Example'}]);
  const loading=detail('Alpha'); loading.tables[0][1][3]='Searching...';
  const runner=makeHplRunner({...opts,tab:fakeTab([advanced,search('Alpha',1),loading,advanced,search('Alpha',1),detail('Alpha')])});
  const collected=await runner.collect();
  const review=[{key:collected.works[0].key,decisions:[{id:'1',match_state:'exact',edition:'Regular print'}]}];
  runner.review(review);
  assert.equal(runner.finalize().state,'continue');
  runner.retry(collected.works[0].key);
  await runner.collect(); runner.review(review);
  assert.equal(runner.finalize().state,'complete');
  assert.throws(()=>runner.retry(collected.works[0].key),/reopen|recovery/i);
});

test('reopen invalidates closure and rechecks a known edition omitted by the new search', async () => {
  const opts=setup([{title:'Alpha',author:'Alice Example'}]);
  const zero={...search('Alpha',1),text:'No results found',total:0,cards:[]};
  const checkedOut=detail('Alpha'); checkedOut.tables[0][1][3]='Checked out';
  const runner=makeHplRunner({...opts,tab:fakeTab([advanced,search('Alpha',1),detail('Alpha'),advanced,zero,advanced,zero,checkedOut])});
  const initial=await runner.collect();
  const review=[{key:initial.works[0].key,decisions:[{id:'1',match_state:'exact',edition:'Regular print'}]}];
  runner.review(review); assert.equal(runner.finalize().state,'complete');
  runner.retry(initial.works[0].key);
  assert.equal(runner.finalize().state,'continue');
  const reopened=await runner.collect();
  assert.equal(reopened.works[0].candidates.length,1);
  runner.review(review);
  assert.equal(runner.finalize().report.results[0].status_code,'held_unavailable');
  assert.equal(runner.finalize().state,'complete');
});

test('a failed reopen cannot erase a known edition before a later resume', async () => {
  const opts=setup([{title:'Alpha',author:'Alice Example'}]);
  const initialRunner=makeHplRunner({...opts,tab:fakeTab([advanced,search('Alpha',1),detail('Alpha')])});
  const initial=await initialRunner.collect();
  const review=[{key:initial.works[0].key,decisions:[{id:'1',match_state:'exact',edition:'Regular print'}]}];
  initialRunner.review(review); initialRunner.retry(initial.works[0].key);
  const failedTab=fakeTab([advanced]); failedTab.getAXState=async()=>{throw new Error('Transport lost');};
  await makeHplRunner({...opts,tab:failedTab}).collect();
  const zero={...search('Alpha',1),text:'No results found',total:0,cards:[]};
  const checkedOut=detail('Alpha'); checkedOut.tables[0][1][3]='Checked out';
  const resumed=makeHplRunner({...opts,tab:fakeTab([advanced,zero,advanced,zero,checkedOut])});
  const result=await resumed.collect();
  assert.equal(result.works[0].candidates.length,1);
  resumed.review(review);
  assert.equal(resumed.finalize().report.results[0].status_code,'held_unavailable');
});

test('two host transport failures checkpoint the whole remaining queue once', async () => {
  const opts=setup([{title:'Alpha',author:'Alice Example'},{title:'Beta',author:'Alice Example'},{title:'Gamma',author:'Alice Example'}]);
  const tab=fakeTab([]); let attempts=0;
  tab.playwright.getByRole=()=>({click:async()=>{attempts++;throw new Error('CDP operation exceeded its deadline before command dispatch');}});
  const runner=makeHplRunner({...opts,tab});
  await runner.collect();
  assert.equal(attempts,2);
  const receipt=runner.finalize();
  assert.equal(receipt.state,'blocked');
  assert.equal(receipt.remaining,3);
  assert.equal(receipt.blockers[0].kind,'host_limit');
  assert.match(receipt.blockers[0].evidence,/CDP/);
});

test('a missing browser capability is rejected before queue execution', () => {
  const opts=setup([{title:'Alpha',author:'Alice Example'}]);
  assert.throws(()=>makeHplRunner(opts),/compatible CUA tab/i);
});

test('a later refresh starts a new ordinary-reopen budget', async () => {
  const opts=setup([{title:'Alpha',author:'Alice Example'}]);
  const views=[advanced,search('Alpha',1),detail('Alpha'),advanced,search('Alpha',1),detail('Alpha'),advanced,search('Alpha',1),detail('Alpha')];
  const runner=makeHplRunner({...opts,tab:fakeTab(views)});
  const initial=await runner.collect();
  const key=initial.works[0].key, review=[{key,decisions:[{id:'1',match_state:'exact',edition:'Regular print'}]}];
  runner.review(review); runner.retry(key); await runner.collect(); runner.review(review);
  execFileSync(python,['-B',processor,'refresh',opts.ledgerPath]);
  await runner.collect(); runner.review(review);
  assert.doesNotThrow(()=>runner.retry(key));
  assert.equal(runner.finalize().state,'continue');
});
