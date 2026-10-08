import sys, tempfile, unittest, json, zipfile, hashlib
from pathlib import Path
from unittest.mock import patch
ROOT = Path(__file__).resolve().parents[1]
KIT = ROOT
sys.path.insert(0,str(KIT / "tools/tubescribe"))
from tubescribe import config, state, pipeline, watchlist
class KitTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(); self.root=Path(self.temp.name)
        self.cfg=config.Config(self.root/'youtube.md', self.root/'raw/youtube')
    def tearDown(self): self.temp.cleanup()
    def test_urls(self):
        self.assertEqual(watchlist.video_id('https://youtu.be/abcdefghijk?t=2'),'abcdefghijk')
        for url in ['https://youtube.com.evil.test/watch?v=abcdefghijk','https://evil.test/?youtube.com/watch?v=abcdefghijk','file:///abcdefghijk','https://user:pass@youtube.com/watch?v=abcdefghijk','https://youtu.be/short']:
            self.assertIsNone(watchlist.video_id(url))
    def test_config_portability(self):
        target=self.root/'tools/tubescribe/config.toml';target.parent.mkdir(parents=True)
        target.write_text((KIT/'tools/tubescribe/config.example.toml').read_text(),encoding='utf-8')
        c=config.load(target);self.assertEqual(c.watchlist_file,self.root/'youtube.md');self.assertEqual(c.whisper_device,'cpu')
    def test_corrupt_state_preserved(self):
        p=self.root/'state.json';p.write_text('{broken')
        with self.assertRaises(RuntimeError): state.load(p)
        self.assertEqual(p.read_text(),'{broken')
    def test_transcription_is_preserved_and_duplicate_not_downloaded(self):
        with patch.object(pipeline.downloader,'fetch_audio',return_value=(self.root/'audio.wav',{'title':'Example'})) as download, patch.object(pipeline.transcriber,'transcribe',return_value=([(0,2,'Example transcript')],'fr')):
            pipeline.process_url('https://youtu.be/abcdefghijk',self.cfg)
            note=self.cfg.output_dir/'abcdefghijk.md';before=note.read_bytes()
            pipeline.process_url('https://youtu.be/abcdefghijk',self.cfg)
            self.assertEqual(download.call_count,1);self.assertEqual(note.read_bytes(),before)
            self.assertIn('[0:00',note.read_text(encoding='utf-8'))
    def test_failed_download_does_not_stop_next_video(self):
        self.cfg.watchlist_file.write_text('- [ ] https://youtu.be/abcdefghijk\n- [ ] https://youtu.be/lmnopqrstuv\n',encoding='utf-8')
        with patch.object(pipeline,'process_url',side_effect=[RuntimeError('unavailable'),'lmnopqrstuv']):
            with self.assertRaises(RuntimeError): pipeline.watch(self.cfg)
        lines=self.cfg.watchlist_file.read_text(encoding='utf-8');self.assertIn('- [ ] https://youtu.be/abcdefghijk',lines);self.assertIn('- [x] https://www.youtube.com/watch?v=lmnopqrstuv',lines)
    def test_empty_transcription_is_not_success(self):
        with patch.object(pipeline.downloader,'fetch_audio',return_value=(self.root/'audio.wav',{})),patch.object(pipeline.transcriber,'transcribe',return_value=([],'fr')):
            with self.assertRaises(RuntimeError): pipeline.process_url('https://youtu.be/abcdefghijk',self.cfg)
        self.assertFalse(self.cfg.state_file.exists())
    def test_concurrent_list_edit_is_not_overwritten(self):
        p=self.cfg.watchlist_file;p.write_text('- [ ] https://youtu.be/abcdefghijk\n')
        entry=watchlist.pending_entries(p)[0];p.write_text('user editing')
        with self.assertRaises(RuntimeError): watchlist.mark_done(p,entry,'abcdefghijk','2026-10-08')
        self.assertEqual(p.read_text(),'user editing')
    def test_archive_contains_only_allowlist_with_valid_hashes(self):
        allowed=json.loads((ROOT/'scripts/cerveau-files.json').read_text())
        with zipfile.ZipFile(ROOT/'dist/cerveau-kit-1.1.0.zip') as z:
            self.assertEqual(set(z.namelist()),{'CerveauKit/'+n for n in allowed+['MANIFEST.json']})
            manifest=json.loads(z.read('CerveauKit/MANIFEST.json'))
            for name,digest in manifest['files'].items():self.assertEqual(hashlib.sha256(z.read('CerveauKit/'+name)).hexdigest(),digest)
            self.assertEqual(z.read('CerveauKit/CLAUDE.md'),z.read('CerveauKit/AGENTS.md'))
if __name__=='__main__': unittest.main()
