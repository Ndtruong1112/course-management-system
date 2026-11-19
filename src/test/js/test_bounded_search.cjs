const {test}=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs'),vm=require('node:vm'),path=require('node:path');
const source=fs.readFileSync(path.join(__dirname,'../../main/resources/static/index.html'),'utf8');
const part=source.slice(source.indexOf('    async function loadCourses('),source.indexOf('    function openCourseModal('));
test('course search and price filter use bounded pages and preserve filters',async()=>{
 const els={courseSearchInput:{value:'Java'},courseMinPrice:{value:'10'},courseMaxPrice:{value:'20'},coursePageInfo:{},courseTableBody:{}};
 const calls=[];const sandbox={API_BASE:'http://local',URLSearchParams,encodeURIComponent,console,setTimeout,clearTimeout,
 document:{getElementById:id=>els[id]},axios:{get:async url=>{calls.push(url);return {data:{content:[],number:calls.length-1,totalPages:2,totalElements:9}}}},renderCourseRows:()=>{}};
 vm.createContext(sandbox);vm.runInContext('let cachedCourses=[], coursePage=0, courseTotalPages=1, courseRequestId=0, courseSearchTimer;'+part,sandbox);
 await vm.runInContext('searchCourses()',sandbox);await vm.runInContext('changeCoursePage(1)',sandbox);
 assert.match(calls[0],/courses\/browse\?/);assert.match(calls[1],/page=1/);assert.match(calls[1],/keyword=Java/);assert.match(calls[1],/minPrice=10/);
});

test('student search keeps query and uses server-side pages',async()=>{
 const studentPart=source.slice(source.indexOf('    async function loadStudents('),source.indexOf('    function openStudentModal('));
 const els={studentSearchInput:{value:'mail@example.test'},studentPageInfo:{}};
 const calls=[];const sandbox={API_BASE:'http://local',URLSearchParams,encodeURIComponent,console,setTimeout,clearTimeout,
 document:{getElementById:id=>els[id]},axios:{get:async url=>{calls.push(url);return {data:{content:[],number:calls.length-1,totalPages:2,totalElements:9}}}},renderStudentRows:()=>{}};
 vm.createContext(sandbox);vm.runInContext('let cachedStudents=[], studentPage=0, studentTotalPages=1, studentRequestId=0, studentSearchTimer;'+studentPart,sandbox);
 await vm.runInContext('searchStudents()',sandbox);await vm.runInContext('changeStudentPage(1)',sandbox);
 assert.match(calls[1],/students\/search-paged\?/);assert.match(calls[1],/page=1/);assert.match(calls[1],/keyword=mail%40example.test/);
});

test('document lists use bounded pages for the selected record',async()=>{
 const part=source.slice(source.indexOf('    async function loadDocuments('),source.indexOf('    async function uploadDocument('));
 const els={docAppId:{value:'APP_1'},docTableBody:{innerHTML:''},docPageInfo:{innerText:''},docPrevBtn:{},docNextBtn:{}};
 const calls=[];const sandbox={API_BASE:'http://local',encodeURIComponent,console,document:{getElementById:id=>els[id]},
 axios:{get:async url=>{calls.push(url);return {data:{content:[],number:calls.length-1,totalPages:2,totalElements:21}}}},showToast:()=>{},escapeHtml:s=>s};
 vm.createContext(sandbox);vm.runInContext('let documentPage=0, documentTotalPages=1, documentRequestId=0, documentLoadedAppId="";'+part,sandbox);
 await vm.runInContext('loadDocuments()',sandbox);await vm.runInContext('changeDocumentPage(1)',sandbox);
 assert.match(calls[1],/documents\/app\/APP_1\/paged\?page=1&size=20/);
});
