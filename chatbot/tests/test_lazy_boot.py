import os
import subprocess
import sys
import unittest
from pathlib import Path

class LazyBootTests(unittest.TestCase):
    def test_boot_does_not_import_ml_runtime_until_needed(self):
        env = os.environ.copy()
        env.update({'LOCAL_MODEL_AUTOSTART':'false', 'HF_HUB_OFFLINE':'1', 'PYTHONUTF8':'1'})
        script = "import sys; sys.path.insert(0, 'chatbot'); import web_app; print('RUNTIME_LOADED=', 'torch' in sys.modules, 'transformers' in sys.modules, web_app.local_load_state)"
        result = subprocess.run([sys.executable, '-c', script], cwd=Path(__file__).resolve().parents[2],
                                env=env, text=True, encoding='utf8', capture_output=True, timeout=30)
        self.assertEqual(result.returncode,0, result.stderr)
        self.assertIn('RUNTIME_LOADED= False False idle', result.stdout)

if __name__ == '__main__': unittest.main()
