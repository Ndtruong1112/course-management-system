const {test}=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm'),path=require('node:path');
const source=fs.readFileSync(path.join(__dirname,'../../main/resources/static/index.html'),'utf8');
const start=source.indexOf('    async function downloadDocument('), end=source.indexOf('    async function uploadDocument(',start);
test('authenticated download streams directly to chosen file', async()=>{
 assert.ok(start>=0 && end>start,'downloadDocument is missing');
 const calls=[];let piped=false;
 const sandbox={API_BASE:'http://local',authToken:'test-token',encodeURIComponent,console,
 window:{showSaveFilePicker:async()=>({createWritable:async()=>({})})},
 fetch:async (url,options)=>{calls.push({url,options});return {ok:true,body:{pipeTo:async()=>{piped=true}}}},showToast:()=>{}};
 vm.createContext(sandbox);vm.runInContext(source.slice(start,end),sandbox);
 await vm.runInContext('downloadDocument("id-1","file.pdf")',sandbox);
 assert.match(calls[0].url,/\/api\/documents\/download\/id-1$/);
 assert.equal(calls[0].options.headers.Authorization,'Bearer test-token');assert.equal(piped,true);
});

test('unauthorized download is reported and never opens a writable stream', async()=>{
 const messages=[];let opened=false;
 const sandbox={API_BASE:'http://local',authToken:'test-token',encodeURIComponent,console,
 window:{showSaveFilePicker:async()=>({createWritable:async()=>{opened=true}})},
 fetch:async()=>({ok:false,status:403}),showToast:msg=>messages.push(msg)};
 vm.createContext(sandbox);vm.runInContext(source.slice(start,end),sandbox);
 await vm.runInContext('downloadDocument("id-1","file.pdf")',sandbox);
 assert.equal(opened,false);assert.match(messages[0],/403/);
});

test('fallback cancels files above the browser memory limit', async()=>{
 const messages=[];let cancelled=false;
 const sandbox={API_BASE:'http://local',authToken:'test-token',encodeURIComponent,console,window:{},
 fetch:async()=>({ok:true,body:{getReader:()=>({read:async()=>({done:false,value:{byteLength:50*1024*1024+1}}),cancel:async()=>{cancelled=true}})}}),
 showToast:msg=>messages.push(msg)};
 vm.createContext(sandbox);vm.runInContext(source.slice(start,end),sandbox);
 await vm.runInContext('downloadDocument("id-1","file.pdf")',sandbox);
 assert.equal(cancelled,true);assert.match(messages[0],/50 MB/);
});
