const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const source = fs.readFileSync(require('node:path').join(__dirname, '../web_app.py'), 'utf8');
function section(from, to) { return source.slice(source.indexOf(from), source.indexOf(to, source.indexOf(from))); }
test('provider limit and interrupted stream produce distinct warnings', () => {
  const sandbox = {};
  vm.createContext(sandbox);
  vm.runInContext(section('        function generationWarning(', '        function readLiveReviews()'), sandbox);
  assert.match(vm.runInContext('generationWarning({finish_reason:"length",max_new_tokens:4096})', sandbox), /4096/);
  assert.match(vm.runInContext('generationWarning({finish_reason:"interrupted"})', sandbox), /gián đoạn/);
  assert.equal(vm.runInContext('generationWarning({finish_reason:"stop"})', sandbox), '');
});
