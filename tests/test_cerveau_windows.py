import os, subprocess, tempfile, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/'tools/windows.ps1'
@unittest.skipUnless(os.name=='nt','Windows launchers')
class LauncherTests(unittest.TestCase):
    def test_both_assistants_open_and_install_detection_without_real_account(self):
        with tempfile.TemporaryDirectory() as temp:
            p=Path(temp)
            for tool in ['claude','codex']:
                (p/(tool+'.cmd')).write_text('@echo off\necho MOCK-'+tool+' %*\nexit /b 0\n',encoding='ascii')
            env=dict(os.environ);env['PATH']=str(p)+os.pathsep+env.get('PATH','')
            for action in ['Open','Install']:
                for choice,tool in [('1','claude'),('2','codex')]:
                    result=subprocess.run(['powershell.exe','-NoLogo','-NoProfile','-ExecutionPolicy','Bypass','-File',str(SCRIPT),'-Action',action],input=choice+'\n',env=env,capture_output=True,text=True,timeout=30)
                    self.assertEqual(result.returncode,0,result.stdout+result.stderr)
                    self.assertIn('MOCK-'+tool,result.stdout)
            result=subprocess.run(['powershell.exe','-NoLogo','-NoProfile','-ExecutionPolicy','Bypass','-File',str(SCRIPT),'-Action','Install'],input='9\n',env=env,capture_output=True,text=True,timeout=30)
            self.assertEqual(result.returncode,1)
            self.assertNotIn('MOCK-',result.stdout)
if __name__=='__main__':unittest.main()
