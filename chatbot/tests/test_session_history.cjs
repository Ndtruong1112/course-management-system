const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const source = fs.readFileSync(require('node:path').join(__dirname, '../web_app.py'), 'utf8');
function section(from, to) { return source.slice(source.indexOf(from), source.indexOf(to, source.indexOf(from))); }
function setup() {
  const db = new Map();
  const chatBox = {innerHTML:'', textContent:'', querySelectorAll:()=>[]};
  const sandbox = {Date, JSON, Array, String,
    localStorage:{getItem:k=>db.get(k)||null, setItem:(k,v)=>db.set(k,v)},
    document:{getElementById:()=>chatBox}, window:{DOMPurify:true}, DOMPurify:{sanitize:s=>s},
    renderHistorySidebar:()=>{}, enhanceCodeBlocks:()=>{}, showToast:()=>{}, hydrateLiveReview:()=>{}};
  vm.createContext(sandbox);
  vm.runInContext('let chatHistory = []; let activeSessionId = null;\n'+section('        function getSessions()', '        function renderHistorySidebar()')+
    section('        function restoreSession(id)', '        function clearAllHistory()'), sandbox);
  return {sandbox, db, chatBox};
}
test('restoring a saved session restores its actual model context', () => {
  const {sandbox}=setup();
  vm.runInContext(`chatHistory=[{role:'user',content:'first question'},{role:'assistant',content:'first answer'}]; saveSession('first question','local','first html'); chatHistory=[{role:'user',content:'different session'}]; restoreSession(getSessions()[0].id);`, sandbox);
  assert.deepEqual(JSON.parse(vm.runInContext('JSON.stringify(chatHistory)',sandbox)), [{role:'user',content:'first question'},{role:'assistant',content:'first answer'}]);
});
test('old snapshots without history clear stale context', () => {
  const {sandbox,db}=setup();
  db.set('cms_ai_sessions',JSON.stringify([{id:'legacy',html:'saved',prompt:'q',mode:'local'}]));
  vm.runInContext(`chatHistory=[{role:'user',content:'unrelated'}]; restoreSession('legacy');`,sandbox);
  assert.deepEqual(JSON.parse(vm.runInContext('JSON.stringify(chatHistory)',sandbox)),[]);
});

test('provider limit and interrupted stream produce distinct warnings', () => {
  const {sandbox}=setup();
  vm.runInContext(section('        function generationWarning(', '        function readLiveReviews()'), sandbox);
  assert.match(vm.runInContext('generationWarning({finish_reason:"length",max_new_tokens:4096})', sandbox), /4096/);
  assert.match(vm.runInContext('generationWarning({finish_reason:"interrupted"})', sandbox), /gián đoạn/);
  assert.equal(vm.runInContext('generationWarning({finish_reason:"stop"})', sandbox), '');
});

test('multiple turns update one session snapshot without duplicating prior history', () => {
  const {sandbox}=setup();
  vm.runInContext(`chatHistory=[{role:'user',content:'one'}]; saveSession('one','local','first html'); chatHistory.push({role:'assistant',content:'answer'}); saveSession('two','local','full conversation');`, sandbox);
  const sessions=JSON.parse(vm.runInContext('JSON.stringify(getSessions())',sandbox));
  assert.equal(sessions.length,1);
  assert.equal(sessions[0].html,'full conversation');
  assert.equal(sessions[0].history.length,2);
});

test('storage quota failure warns without marking response generation as failed', () => {
  const {sandbox}=setup(); let warned=false;
  sandbox.localStorage.setItem=()=>{throw new Error('QuotaExceededError')};
  sandbox.showToast=()=>{warned=true};
  assert.doesNotThrow(()=>vm.runInContext('saveSession("q","local","answer")',sandbox));
  assert.equal(warned,true);
});
