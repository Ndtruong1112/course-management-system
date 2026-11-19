const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');
const source = fs.readFileSync(path.join(__dirname, '../../main/resources/static/index.html'), 'utf8');
const part = source.slice(source.indexOf('    async function loadEnrollments('), source.indexOf('    async function openEnrollModal('));
test('loading enrollments uses a bounded page and moves between pages', async () => {
    const calls = [], elements = {enrollSearchInput:{value:''}, enrollPageInfo:{}, enrollPrevBtn:{}, enrollNextBtn:{}};
    const sandbox = {API_BASE:'http://local', console, encodeURIComponent, setTimeout, clearTimeout,
        document:{getElementById:id=>elements[id]},
        axios:{get:async url=>{calls.push(url);return {data:{content:[{id:1}],totalPages:3,totalElements:42}}}},
        renderEnrollmentRows: rows => {sandbox.rendered = rows}, showToast:()=>{}};
    vm.createContext(sandbox);
    vm.runInContext('let cachedEnrollments=[]; let enrollmentPage=0, enrollmentTotalPages=1, enrollmentRequestId=0, enrollmentSearchTimer;'+part,sandbox);
    await vm.runInContext('loadEnrollments()',sandbox);
    assert.match(calls[0], /\/api\/enrollments\/paged\?page=0&size=20/);
    assert.equal(sandbox.rendered.length,1);
    assert.equal(elements.enrollPrevBtn.disabled,true);
    await vm.runInContext('changeEnrollmentPage(1)',sandbox);
    assert.match(calls[1], /page=1&size=20/);
    assert.equal(elements.enrollPrevBtn.disabled,false);
});

test('failed paged course request never falls back to an unbounded list', async () => {
    const part = source.slice(source.indexOf('    async function loadCourses('), source.indexOf('    async function changeCoursePage('));
    const calls = [], elements = {courseTableBody:{innerHTML:''}, coursePageInfo:{innerText:''}};
    const sandbox = {API_BASE:'http://local', URLSearchParams, document:{getElementById:id=>elements[id]},
        axios:{get:async url=>{calls.push(url);throw new Error('network')}}, renderCourseRows:()=>{}};
    vm.createContext(sandbox);
    vm.runInContext('let cachedCourses=[], coursePage=0, courseTotalPages=1, courseRequestId=0, courseSearchTimer;'+part,sandbox);
    await vm.runInContext('loadCourses(0)',sandbox);
    assert.equal(calls.length,1);
    assert.match(calls[0], /courses\/paged/);
    assert.match(elements.courseTableBody.innerHTML, /Không thể tải/);
});

test('a stale page response cannot replace newer search results', async () => {
    let resolvePage;
    const elements = {enrollSearchInput:{value:''}, enrollPageInfo:{}, enrollPrevBtn:{}, enrollNextBtn:{}};
    const sandbox = {API_BASE:'http://local', console, encodeURIComponent, setTimeout, clearTimeout,
        document:{getElementById:id=>elements[id]},
        axios:{get:url=>url.includes('/paged?') ? new Promise(r=>{resolvePage=r}) : Promise.resolve({data:{content:[{id:2}],totalPages:1,totalElements:1}})},
        renderEnrollmentRows:rows=>{sandbox.rendered=rows}, showToast:()=>{}};
    vm.createContext(sandbox);
    vm.runInContext('let cachedEnrollments=[]; let enrollmentPage=0, enrollmentTotalPages=1, enrollmentRequestId=0, enrollmentSearchTimer;'+part,sandbox);
    const pending=vm.runInContext('loadEnrollments()',sandbox);
    elements.enrollSearchInput.value='Nguyen';
    await vm.runInContext('searchEnrollments()',sandbox);
    resolvePage({data:{content:[{id:1}],totalPages:1,totalElements:1}});
    await pending;
    assert.equal(sandbox.rendered[0].id,2);
});

test('search navigation keeps the keyword and uses a bounded server page', async () => {
    const calls = [], elements = {enrollSearchInput:{value:'Java'}, enrollPageInfo:{}, enrollPrevBtn:{}, enrollNextBtn:{}};
    const sandbox = {API_BASE:'http://local', console, encodeURIComponent, setTimeout, clearTimeout,
        document:{getElementById:id=>elements[id]},
        axios:{get:async url=>{calls.push(url);return {data:{content:[{id:1}],totalPages:2,totalElements:21}}}},
        renderEnrollmentRows:()=>{}, showToast:()=>{}};
    vm.createContext(sandbox);
    vm.runInContext('let cachedEnrollments=[]; let enrollmentPage=0, enrollmentTotalPages=1, enrollmentRequestId=0, enrollmentSearchTimer;'+part,sandbox);
    await vm.runInContext('searchEnrollments()',sandbox);
    await vm.runInContext('changeEnrollmentPage(1)',sandbox);
    assert.match(calls[1], /search-paged\?keyword=Java&page=1&size=20/);
});
