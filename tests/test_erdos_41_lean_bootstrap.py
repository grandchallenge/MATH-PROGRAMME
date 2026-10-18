"""Hostile lock checks for Colab's pinned elan installer."""
import unittest
from unittest.mock import patch
from colab import erdos_41_lean_worker as worker

class BootstrapTests(unittest.TestCase):
    def test_pinned_release_url_and_digest(self):
        self.assertEqual(worker.ELAN_RELEASE, "v4.2.4")
        self.assertIn("/v4.2.4/elan-x86_64-unknown-linux-gnu.tar.gz", worker.ELAN_URL)
        self.assertEqual(worker.ELAN_ARCHIVE_SHA256,
                         "42b94d4244e8353142c456ec0e4ca6528fd898a6c604d4059f494e706e431f63")
    def test_reject_modified_release_archive(self):
        class FakeResponse:
            def __enter__(self): return self
            def __exit__(self,*args): pass
            def read(self, n): return b"tampered release archive"
        with patch.object(worker.shutil, "which", return_value=None), \
             patch.object(worker.platform, "machine", return_value="x86_64"), \
             patch.object(worker.urllib.request, "urlopen", return_value=FakeResponse()):
            with self.assertRaisesRegex(RuntimeError, "SHA256 mismatch"):
                worker.provision_elan()
    def test_reject_unpinned_architecture(self):
        with patch.object(worker.shutil, "which", return_value=None), \
             patch.object(worker.platform, "machine", return_value="aarch64"):
            with self.assertRaisesRegex(RuntimeError, "x86_64"):
                worker.provision_elan()
    def test_preinstalled_does_not_download(self):
        with patch.object(worker.shutil, "which", return_value="/usr/bin/elan"), \
             patch.object(worker.urllib.request, "urlopen") as net:
            self.assertEqual(worker.provision_elan(),
                             ("/usr/bin/elan", "preinstalled_version_checked", None))
            net.assert_not_called()
