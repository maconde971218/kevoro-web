"""The downloadable ZIP contains only explicitly public preview files."""
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from zipfile import ZipFile

from package_preview import build_archive


class PreviewBundleTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for path in ('index.html', 'assets/app.js', 'marca/index.html',
                     'instagram/index.html', 'scripts/preview.mjs', 'package.json'):
            file = self.root / path
            file.parent.mkdir(parents=True, exist_ok=True)
            file.write_text('public synthetic fixture: ' + path)
        (self.root / '.git').mkdir()
        (self.root / '.git' / 'private-fixture').write_text('excluded synthetic fixture')
        self.output = self.root / 'preview.zip'

    def test_archive_omits_repo_internals_and_has_matching_hashes(self):
        self.assertEqual(build_archive(self.output, self.root), 6)
        with ZipFile(self.output) as archive:
            self.assertIsNone(archive.testzip())
            self.assertFalse(any('.git/' in name for name in archive.namelist()))
            manifest = json.loads(archive.read('kevoro-preview/preview-manifest.json'))
            self.assertEqual(len(manifest), 6)
            for path, digest in manifest.items():
                data = archive.read('kevoro-preview/' + path)
                self.assertEqual(hashlib.sha256(data).hexdigest(), digest)
            self.assertIn('npm run dev', archive.read('kevoro-preview/README-PREVIEW.txt').decode())

    def test_symlinked_public_directory_is_rejected(self):
        (self.root / 'assets').rename(self.root / 'outside-public-list')
        (self.root / 'assets').symlink_to(self.root / 'outside-public-list', target_is_directory=True)
        with self.assertRaisesRegex(ValueError, 'Symlinks'):
            build_archive(self.output, self.root)

    def test_symlinked_parent_of_allowlisted_file_is_rejected(self):
        (self.root / 'scripts').rename(self.root / 'outside-public-list')
        (self.root / 'scripts').symlink_to(self.root / 'outside-public-list', target_is_directory=True)
        with self.assertRaisesRegex(ValueError, 'Symlinks'):
            build_archive(self.output, self.root)

    def test_hidden_file_within_assets_is_rejected(self):
        (self.root / 'assets' / '.private-fixture').write_text('synthetic fixture')
        with self.assertRaisesRegex(ValueError, 'Hidden files'):
            build_archive(self.output, self.root)


if __name__ == '__main__':
    unittest.main()
