const {test}=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm'),path=require('node:path');
const source=fs.readFileSync(path.join(__dirname,'../../main/resources/static/index.html'),'utf8');
const part=source.slice(source.indexOf('    async function openEnrollModal('),source.indexOf('    async function saveEnrollment('));
test('editing preserves student and course outside the first page and fetches bounded choices',async()=>{
 const ids=['enrollStudentSelect','enrollCourseSelect','enrollStudentSearch','enrollCourseSearch','enrollStudentOptionsInfo','enrollCourseOptionsInfo','enrollStudentPrev','enrollStudentNext','enrollCoursePrev','enrollCourseNext','enrollIdInput','enrollModalTitle','enrollStatusSelect','enrollProgressInput','enrollNotesInput','enrollModal'];
 const els=Object.fromEntries(ids.map(id=>[id,{value:'',innerHTML:'',innerText:'',disabled:false,options:[],selectedIndex:0}]));const urls=[];
 const sandbox={API_BASE:'http://local',URLSearchParams,encodeURIComponent,console,setTimeout,clearTimeout,document:{getElementById:id=>els[id]},
 axios:{get:async url=>{urls.push(url);return {data:{content:[],totalPages:1,totalElements:0}}}},
 bootstrap:{Modal:{getOrCreateInstance:()=>({show(){}})}},showToast:()=>{},escapeHtml:s=>String(s||'')};
 vm.createContext(sandbox);
 vm.runInContext('let cachedEnrollments=[{id:42,studentId:123,studentName:"Nguyen",courseId:456,courseTitle:"Course",status:"ENROLLED"}]; let enrollmentOptions={}; let enrollmentOptionTimers={};'+part,sandbox);
 await vm.runInContext('openEnrollModal(42)',sandbox);
 assert.ok(urls.some(url=>url.includes('/students/search-paged?')&&url.includes('size=20')));
 assert.ok(urls.some(url=>url.includes('/courses/browse?')&&url.includes('size=20')));
 assert.match(els.enrollStudentSelect.innerHTML,/value="123"/);assert.equal(els.enrollStudentSelect.value,'123');
 assert.match(els.enrollCourseSelect.innerHTML,/value="456"/);assert.equal(els.enrollCourseSelect.value,'456');
});
