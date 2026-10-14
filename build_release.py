"""Build and inspect the public skills-only release using only the standard library."""
from pathlib import Path, PurePosixPath
import json,re,stat,struct,sys,zipfile

ROOT=Path(__file__).resolve().parent
FILES=['plugin.json','.codex-plugin/plugin.json','README.md','SUPPORT.md','PRIVACY.md','TERMS.md','LICENSE','VALIDATION.md','CHANGELOG.md','.gitignore','build_release.py','verify.py','assets/icon.png','skills/hpl-physical-book-check/SKILL.md','skills/hpl-physical-book-check/references/catalog-access.md','skills/hpl-physical-book-check/references/evidence-toolkit.md','skills/hpl-physical-book-check/references/work-workflow.md','skills/hpl-physical-book-check/scripts/hpl_evidence.py','tests/test_evidence.py','tests/fixtures/dune-live.json','tests/fixtures/employees-live.json']

def inspect(path: Path, *, require_urls: bool=False) -> dict:
 with zipfile.ZipFile(path) as z:
  names=z.namelist(); assert len(names)==len(set(names)), 'Duplicate archive paths'
  prefix='hpl-physical-book-check/'
  assert set(names)=={prefix+p for p in FILES}, 'Unexpected or missing archive files'
  for info in z.infolist():
   p=PurePosixPath(info.filename)
   assert not p.is_absolute() and '..' not in p.parts and not stat.S_ISLNK(info.external_attr>>16), 'Unsafe archive path'
   assert not any(x in {'.env','.app.json','__pycache__','.git','.DS_Store'} for x in p.parts), 'Forbidden archive file'
   if p.suffix in {'.py','.json','.md'}:
    text=z.read(info.filename).decode('utf-8')
    assert not re.search(r'BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY|ghp_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,}|sk-[A-Za-z0-9]{32,}|\x2fUsers\x2f|skill:[/]{2}plugins_',text), 'Nonportable or sensitive content'
  m=json.loads(z.read(prefix+'plugin.json')); legacy=json.loads(z.read(prefix+'.codex-plugin/plugin.json'))
  assert m['name']=='hpl-physical-book-check' and re.fullmatch(r'\d+\.\d+\.\d+',m['version'])
  assert m['version']==legacy['version']=='1.3.5'
  assert set(m)<={'$schema','name','version','description','author','homepage','repository','license','keywords','extensions'}, 'Nonportable manifest fields'
  for v in [m,legacy]:
   assert v.get('apps') is None and v.get('extensions',{}).get('com.openai',{}).get('apps') is None, 'Private app bindings'
  ext=m['extensions']['com.openai']; i=ext['interface']; assert legacy['interface']==i
  assert legacy['author']==m['author']=={'name':'Mit'} and m['license']==legacy['license']=='MIT'
  for key,limit in [('displayName',30),('shortDescription',30),('longDescription',4000),('developerName',80)]: assert 0<len(i[key])<=limit,key
  prompts=[i['defaultPrompt']] if isinstance(i['defaultPrompt'],str) else i['defaultPrompt']
  assert 1<=len(prompts)<=3 and len({' '.join(p.split()) for p in prompts})==len(prompts)
  assert all(p.strip() and '\n' not in p and len(p)<=128 and '@' not in p for p in prompts)
  assert ext['publication']['countries']==['US'] and ext['review']['commerce'] is False
  assert 'release_notes' in ext['publication']
  assert not any(x in ext['review'] for x in ['test_cases','demo_recording_url']), 'Unnecessary skills-only review declarations'
  urls={k:i.get(k) for k in ['websiteURL','supportURL','privacyPolicyURL','termsOfServiceURL']}
  if require_urls: assert all(urls.values()), 'Listing URLs incomplete'
  for url in urls.values():
   if url: assert re.fullmatch(r'https://github\.com/mit112/hpl-physical-book-check(?:/blob/main/(?:SUPPORT|PRIVACY|TERMS)\.md)?',url)
  png=z.read(prefix+i['logo']); assert i['logo']==i['composerIcon']=='assets/icon.png'
  assert png[:8]==b'\x89PNG\r\n\x1a\n' and len(png)<=5*1024*1024
  width,height=struct.unpack('>II',png[16:24]); assert 256<=width==height<=4096
  skill=z.read(prefix+'skills/hpl-physical-book-check/SKILL.md').decode()
  assert 'name: hpl-physical-book-check' in skill and 'Workflow release: **1.3.5**.' in skill
  for link in re.findall(r'\]\((references/[^)]+)\)',skill): assert prefix+'skills/hpl-physical-book-check/'+link in names
  return dict(version=m['version'],files=len(names),icon=dict(width=width,height=height,bytes=len(png)),listing_urls_complete=all(urls.values()),subtitle_characters=len(i['shortDescription']))

def build(path: Path, *, require_urls: bool=False) -> dict:
 assert not any((ROOT/name).is_symlink() for name in FILES)
 with zipfile.ZipFile(path,'w',compression=zipfile.ZIP_DEFLATED) as z:
  for name in FILES: z.write(ROOT/name,'hpl-physical-book-check/'+name)
 return inspect(path,require_urls=require_urls)

if __name__=='__main__':
 dest=Path(sys.argv[1]) if len(sys.argv)>1 and not sys.argv[1].startswith('--') else ROOT.parent/'hpl-physical-book-check-1.3.5.zip'
 print(json.dumps(build(dest,require_urls='--require-urls' in sys.argv),indent=2))
