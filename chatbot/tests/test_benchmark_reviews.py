import json
import os
import re
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
os.environ['HF_HUB_OFFLINE'] = '1'
with patch('threading.Thread.start'), patch('transformers.AutoTokenizer.from_pretrained'):
    import web_app

class BenchmarkReviewRouteTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.run = self.root / 'benchmark/runs/20261116T010000.000000Z'
        self.run.mkdir(parents=True)
        case = {'id':'c1','question':'Which class?', 'checks':['Use the right class'], 'sources':['source.java']}
        rows = [{'id':'c1/base/0','case_id':'c1','variant':'base','repeat':0,'kind':'qa','status':'ok','answer':'a','elapsed_seconds':1},
                {'id':'c1/lora/0','case_id':'c1','variant':'lora','repeat':0,'kind':'code','status':'ok','answer':'b','elapsed_seconds':1},
                {'id':'c1/cloud/0','case_id':'c1','variant':'cloud','repeat':0,'kind':'qa','status':'error','answer':'','elapsed_seconds':1}]
        (self.run/'cases.json').write_text(json.dumps([case]),encoding='utf8')
        (self.run/'manifest.json').write_text(json.dumps({'case_count':1,'modes':['base','lora','cloud'],'repeats':1}),encoding='utf8')
        (self.run/'results.jsonl').write_text(''.join(json.dumps(x)+'\n' for x in rows),encoding='utf8')
        (self.run/'reviews.jsonl').write_text(''.join(json.dumps({'id':r['id'],'verdict':'pending'})+'\n' for r in rows),encoding='utf8')
        self.patch = patch.object(web_app,'root_dir',str(self.root));self.patch.start()
        self.client=web_app.app.test_client()
    def tearDown(self):
        self.patch.stop();self.tmp.cleanup()
    def tokens(self):
        html=self.client.get('/benchmark-report').get_data(as_text=True)
        return {name:re.search(r'name="'+name+r'" value="([^"]+)"',html).group(1) for name in ('csrf_token','review_version')}
    def post_review(self, **values):
        payload={'run':self.run.name,'id':'c1/base/0','verdict':'pass','reviewer':'An','evidence':'Checked source.java',
                 'compile_status':'not_applicable','test_status':'not_applicable',**self.tokens(),**values}
        return self.client.post('/benchmark-report/review',data=payload)
    def test_review_is_saved_and_report_updates(self):
        response=self.post_review()
        self.assertEqual(response.status_code,303)
        reviews=[json.loads(x) for x in (self.run/'reviews.jsonl').read_text(encoding='utf8').splitlines()]
        self.assertEqual(reviews[0]['verdict'],'pass')
        self.assertEqual(reviews[1]['verdict'],'pending')
        html=self.client.get('/benchmark-report').get_data(as_text=True)
        self.assertIn('Checked source.java',html)
        self.assertIn('Use the right class',html)
        self.assertIn('source.java',html)
    def test_invalid_review_cannot_change_file(self):
        before=(self.run/'reviews.jsonl').read_bytes()
        for values in ({'evidence':''},{'id':'c1/cloud/0'}, {'id':'c1/lora/0'}, {'id':'missing'}, {'csrf_token':'invalid'}):
            self.assertIn(self.post_review(**values).status_code,(400,403))
            self.assertEqual((self.run/'reviews.jsonl').read_bytes(),before)
    def test_small_pair_is_shown_without_percentage_claim(self):
        self.assertEqual(self.post_review().status_code,303)
        self.assertEqual(self.post_review(id='c1/lora/0',verdict='fail').status_code,303)
        html=self.client.get('/benchmark-report').get_data(as_text=True)
        self.assertIn('So sánh theo cặp',html)
        self.assertIn('Chưa hiển thị (dưới 5 cặp)',html)

    def test_incomplete_run_cannot_be_reviewed(self):
        tokens=self.tokens()
        (self.run/'reviews.jsonl').unlink()
        response=self.client.post('/benchmark-report/review', data={'run':self.run.name, 'id':'c1/base/0',
            'verdict':'pass', 'reviewer':'An', 'evidence':'source', 'compile_status':'not_run', 'test_status':'not_run', **tokens})
        self.assertEqual(response.status_code,409)
        self.assertFalse((self.run/'reviews.jsonl').exists())

    def test_generated_code_pass_requires_recorded_compile_and_test(self):
        result=self.post_review(id='c1/lora/0', compile_status='pass', test_status='not_run')
        self.assertEqual(result.status_code,400)
        result=self.post_review(id='c1/lora/0', compile_status='pass', test_status='pass')
        self.assertEqual(result.status_code,303)
        reviews=[json.loads(x) for x in (self.run/'reviews.jsonl').read_text(encoding='utf8').splitlines()]
        review=next(x for x in reviews if x['id']=='c1/lora/0')
        self.assertEqual((review['compile_status'],review['test_status']),('pass','pass'))

    def test_stale_version_is_rejected(self):
        old=self.tokens()
        self.assertEqual(self.post_review().status_code,303)
        self.assertEqual(self.post_review(**old).status_code,409)
    def test_traversal_is_rejected(self):
        self.assertEqual(self.post_review(run='../outside').status_code,404)

if __name__ == '__main__': unittest.main()
