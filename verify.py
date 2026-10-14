"""Full offline release gate. No network, catalog actions or external dependencies."""
import json,os,subprocess,sys,tempfile,zipfile
from pathlib import Path
import build_release as b

def main() -> None:
 env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
 result=subprocess.run([sys.executable,'-W','error::ResourceWarning','-m','unittest','discover','-s','tests','-v'],cwd=b.ROOT,env=env)
 if result.returncode: raise SystemExit(result.returncode)
 with tempfile.TemporaryDirectory() as directory:
  root=Path(directory); archive=root/'release.zip'; report=b.build(archive)
  forbidden=root/'forbidden.zip'
  with zipfile.ZipFile(archive) as src,zipfile.ZipFile(forbidden,'w') as dst:
   for name in src.namelist(): dst.writestr(name,src.read(name))
   dst.writestr('hpl-physical-book-check/.env','RELEASE_CONTROL=not-a-secret\n')
  try: b.inspect(forbidden)
  except AssertionError: pass
  else: raise AssertionError('Forbidden-file control was not rejected')
  binding=root/'private-binding.zip'
  with zipfile.ZipFile(archive) as src,zipfile.ZipFile(binding,'w') as dst:
   for name in src.namelist():
    value=src.read(name)
    if name.endswith('/.codex-plugin/plugin.json'):
     m=json.loads(value); m['apps']='private-binding.json'; value=json.dumps(m).encode()
    dst.writestr(name,value)
  try: b.inspect(binding)
  except AssertionError: pass
  else: raise AssertionError('Private-binding control was not rejected')
  wrong=root/'wrong-marketplace-path.zip'
  with zipfile.ZipFile(archive) as src,zipfile.ZipFile(wrong,'w') as dst:
   for name in src.namelist():
    value=src.read(name)
    if name.endswith('/.agents/plugins/marketplace.json'):
     catalog=json.loads(value); catalog['plugins'][0]['source']['path']='./missing'; value=json.dumps(catalog).encode()
    dst.writestr(name,value)
  try: b.inspect(wrong)
  except AssertionError: pass
  else: raise AssertionError('Wrong marketplace path was not rejected')
 print(json.dumps(dict(package=report,forbidden_file_control_rejected=True,private_binding_control_rejected=True,wrong_marketplace_path_control_rejected=True),indent=2))
 print('PASS: processor suite and actual ZIP checks. Live host reliability is not certified.')

if __name__=='__main__': main()
