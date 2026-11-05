#  Copyright (c) 2023. Deltares & TNO
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""Test the Rosim JAR download logic of the Pyjnius loader."""
import fnmatch
import glob
import hashlib
import os
import tempfile
import unittest
from typing import Optional
from unittest.mock import patch

from omotes_simulator_core.entities.assets import pyjnius_loader
from omotes_simulator_core.entities.assets.pyjnius_loader import PyjniusLoader

PAYLOAD = b"this is not really a jar file" * 100
PAYLOAD_SHA256 = hashlib.sha256(PAYLOAD).hexdigest()

# A git-LFS pointer stub is a few hundred bytes of text; a real JAR is over 100 MB.
_LFS_POINTER_MAX_SIZE = 1024


def _lfs_pointer_digest(file_path: str) -> Optional[str]:
    """Return the sha256 oid recorded in a git-LFS pointer stub, or None for real content."""
    if os.path.getsize(file_path) > _LFS_POINTER_MAX_SIZE:
        return None
    try:
        with open(file_path, "r", encoding="utf-8") as file_handle:
            lines = file_handle.read().splitlines()
    except UnicodeDecodeError:
        return None

    if not lines or not lines[0].startswith("version https://git-lfs.github.com/spec/"):
        return None
    for line in lines:
        if line.startswith("oid sha256:"):
            return line.split("oid sha256:", 1)[1].strip()
    return None


class DownloadRosimJarTest(unittest.TestCase):
    """Testcase for PyjniusLoader.download_rosim_jar."""

    def setUp(self) -> None:
        """Point the loader at an empty temporary bin folder."""
        self._temp_dir = tempfile.TemporaryDirectory()
        self.bin_dir = self._temp_dir.name
        patcher = patch.object(pyjnius_loader, "_get_bin_path", return_value=self.bin_dir)
        patcher.start()
        self.addCleanup(patcher.stop)
        self.addCleanup(self._temp_dir.cleanup)

    def _write_payload(self, _url, target_path):
        """Stand in for urllib.request.urlretrieve by writing the known payload."""
        with open(target_path, "wb") as file_handle:
            file_handle.write(PAYLOAD)
        return target_path, None

    def test_cache_hit_skips_download(self):
        """An existing rosim JAR short-circuits the download and yields its bare name."""
        cached_name = "rosim-test-9.9.9.jar"
        with open(os.path.join(self.bin_dir, cached_name), "wb") as file_handle:
            file_handle.write(b"cached")

        with patch.object(pyjnius_loader.urllib.request, "urlretrieve") as fake_retrieve:
            result = PyjniusLoader.download_rosim_jar()

        self.assertEqual(result, cached_name)
        self.assertEqual(fake_retrieve.call_count, 0)
        self.assertEqual(sorted(os.listdir(self.bin_dir)), [cached_name])

    def test_successful_download_moves_file_into_place(self):
        """A download whose digest matches lands at the final path and leaves no temp file."""
        with patch.object(pyjnius_loader, "ROSIM_JAR_SHA256", PAYLOAD_SHA256):
            with patch.object(
                pyjnius_loader.urllib.request, "urlretrieve", side_effect=self._write_payload
            ) as fake_retrieve:
                result = PyjniusLoader.download_rosim_jar()

        self.assertEqual(result, pyjnius_loader.ROSIM_JAR_NAME)
        self.assertEqual(fake_retrieve.call_count, 1)
        self.assertEqual(fake_retrieve.call_args[0][0], pyjnius_loader.ROSIM_JAR_URL)
        self.assertEqual(sorted(os.listdir(self.bin_dir)), [pyjnius_loader.ROSIM_JAR_NAME])
        with open(os.path.join(self.bin_dir, pyjnius_loader.ROSIM_JAR_NAME), "rb") as file_handle:
            self.assertEqual(file_handle.read(), PAYLOAD)

    def test_hash_mismatch_raises_and_leaves_nothing_behind(self):
        """A digest mismatch raises RuntimeError and no file is kept, temporary or final."""
        wrong_hash = "0" * 64
        with patch.object(pyjnius_loader, "ROSIM_JAR_SHA256", wrong_hash):
            with patch.object(
                pyjnius_loader.urllib.request, "urlretrieve", side_effect=self._write_payload
            ):
                with self.assertRaises(RuntimeError) as context:
                    PyjniusLoader.download_rosim_jar()

        message = str(context.exception)
        self.assertIn(wrong_hash, message)
        self.assertIn(PAYLOAD_SHA256, message)
        self.assertFalse(os.path.exists(os.path.join(self.bin_dir, pyjnius_loader.ROSIM_JAR_NAME)))
        self.assertEqual(os.listdir(self.bin_dir), [])

    def test_download_error_propagates_and_leaves_nothing_behind(self):
        """A failing download propagates and removes the partial temporary file."""

        def failing_retrieve(_url, target_path):
            with open(target_path, "wb") as file_handle:
                file_handle.write(b"partial")
            raise OSError("connection reset")

        with patch.object(
            pyjnius_loader.urllib.request, "urlretrieve", side_effect=failing_retrieve
        ):
            with self.assertRaises(OSError):
                PyjniusLoader.download_rosim_jar()

        self.assertEqual(os.listdir(self.bin_dir), [])

    def test_partial_download_is_never_visible_to_the_cache_glob(self):
        """While a download is in flight its file must not match the `rosim*.jar` cache glob.

        A process killed mid-download leaves the partial file behind. If that name matched the
        glob, the next run would short-circuit on it and treat a truncated file as a valid
        cached JAR forever, so the temporary name is load-bearing rather than cosmetic.
        """
        targets: list[str] = []

        def retrieve_and_inspect(_url, target_path):
            targets.append(target_path)
            with open(target_path, "wb") as file_handle:
                file_handle.write(b"partial")
            raise OSError("killed mid-download")

        with patch.object(
            pyjnius_loader.urllib.request, "urlretrieve", side_effect=retrieve_and_inspect
        ):
            with self.assertRaises(OSError):
                PyjniusLoader.download_rosim_jar()

        self.assertEqual(len(targets), 1)
        # Assert on the name itself: globbing the bin folder would also come up empty if the
        # download were written somewhere else entirely, passing for the wrong reason.
        self.assertEqual(os.path.dirname(targets[0]), self.bin_dir)
        self.assertFalse(
            fnmatch.fnmatch(os.path.basename(targets[0]), "rosim*.jar"),
            f"in-flight download {os.path.basename(targets[0])} matches the cache glob",
        )


class LfsPointerDigestTest(unittest.TestCase):
    """Testcase for the git-LFS pointer parsing used by the pinned-constant guard.

    The pinned-digest test below reads a real JAR, so these branches are never exercised
    there. Without direct coverage a broken parser would silently make that guard hash the
    wrong bytes rather than fail.
    """

    def setUp(self) -> None:
        """Provide a temporary folder to write pointer fixtures into."""
        self._temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self._temp_dir.cleanup)

    def _write(self, text: str, name: str = "stub") -> str:
        """Write a fixture file and return its path."""
        path = os.path.join(self._temp_dir.name, name)
        with open(path, "w", encoding="utf-8") as file_handle:
            file_handle.write(text)
        return path

    def test_reads_oid_from_pointer(self):
        """A well-formed pointer yields the digest recorded in its oid line."""
        oid = "a" * 64
        path = self._write(
            "version https://git-lfs.github.com/spec/v1\n" f"oid sha256:{oid}\nsize 129225676\n"
        )
        self.assertEqual(_lfs_pointer_digest(path), oid)

    def test_returns_none_for_large_file(self):
        """Content above the pointer size limit is rejected on size alone.

        The fixture is a valid pointer padded past the limit, so only the size guard can
        reject it; a fixture that also failed the header check would pass even with the
        size guard removed.
        """
        oid = "c" * 64
        padding = "\n" * _LFS_POINTER_MAX_SIZE
        path = self._write(
            "version https://git-lfs.github.com/spec/v1\n" f"oid sha256:{oid}\n{padding}"
        )
        self.assertGreater(os.path.getsize(path), _LFS_POINTER_MAX_SIZE)
        self.assertIsNone(_lfs_pointer_digest(path))

    def test_returns_none_for_binary_content(self):
        """A small binary file is not a pointer and must not raise while being checked."""
        path = os.path.join(self._temp_dir.name, "binary")
        with open(path, "wb") as file_handle:
            file_handle.write(b"\xff\xfe\x00\x01")
        self.assertIsNone(_lfs_pointer_digest(path))

    def test_returns_none_without_pointer_header(self):
        """Small text lacking the LFS version header is not a pointer."""
        path = self._write(f"oid sha256:{'b' * 64}\n")
        self.assertIsNone(_lfs_pointer_digest(path))

    def test_returns_none_when_oid_line_missing(self):
        """A pointer header with no oid line yields no digest rather than a wrong one."""
        path = self._write("version https://git-lfs.github.com/spec/v1\nsize 42\n")
        self.assertIsNone(_lfs_pointer_digest(path))


class PinnedConstantsMatchRepositoryTest(unittest.TestCase):
    """Guard the pinned constants against drifting from the JAR committed in `bin`.

    `upload_rosim_to_release.yml` publishes whatever `rosim*.jar` sits in `bin`, while the
    loader reads a hardcoded release asset. Nothing links the two, so swapping the JAR without
    updating the constants leaves the pin serving the previous JAR whose checksum still
    matches -- a silently wrong Rosim version rather than a visible failure. Replacing the JAR
    without updating `ROSIM_JAR_NAME` and `ROSIM_JAR_SHA256` fails here instead.

    Two limits are deliberate. `ROSIM_RELEASE_TAG` is checked against nothing, so bumping the
    tag alone is not caught; it points the URL at a possibly absent asset and surfaces as a
    download failure at runtime, which is loud enough. And an empty `bin` skips rather than
    fails, because `pyproject.toml` does not ship `rosim-batch-*.jar` as package data: an
    installed package has no JAR until the first download, and only a repository checkout
    carries the committed one these tests compare against.
    """

    def setUp(self) -> None:
        """Locate the JAR committed in the real `bin` folder."""
        self.bin_dir = pyjnius_loader._get_bin_path()
        self.jars = sorted(
            os.path.basename(path) for path in glob.glob(os.path.join(self.bin_dir, "rosim*.jar"))
        )

    def test_at_most_one_rosim_jar_is_committed(self):
        """Several candidate JARs make the loader's cache short-circuit ambiguous.

        Zero JARs is not a drift signal: `pyproject.toml` does not ship `rosim-batch-*.jar`
        as package data, so an installed package legitimately has none until the first
        download. Only the ambiguous case is a failure.
        """
        self.assertLessEqual(
            len(self.jars), 1, f"expected at most one rosim JAR in bin, found {self.jars}"
        )

    def _single_jar(self) -> str:
        """Return the committed rosim JAR, skipping when there is no single one to compare.

        An empty `bin` is legitimate outside a repository checkout; an ambiguous one is
        reported by the count test above rather than again here.
        """
        if len(self.jars) != 1:
            self.skipTest(f"no single rosim JAR in bin to compare against, found {self.jars}")
        return self.jars[0]

    def test_pinned_name_matches_committed_jar(self):
        """ROSIM_JAR_NAME must name the JAR actually shipped in `bin`."""
        self.assertEqual(
            pyjnius_loader.ROSIM_JAR_NAME,
            self._single_jar(),
            "ROSIM_JAR_NAME does not match the JAR in bin; bump the pinned constants "
            "(tag, name and SHA-256) together with the JAR.",
        )

    def test_pinned_digest_matches_committed_jar(self):
        """ROSIM_JAR_SHA256 must match the committed JAR's content digest.

        On a checkout without git-LFS content the file is a small pointer stub, whose
        `oid sha256:` line records the real digest; hashing the stub would compare the wrong
        bytes. The stub is read in that case so the check stays meaningful either way.
        """
        jar_path = os.path.join(self.bin_dir, self._single_jar())
        digest = _lfs_pointer_digest(jar_path)
        if digest is None:
            digest = pyjnius_loader._sha256_of_file(jar_path)

        self.assertEqual(
            digest,
            pyjnius_loader.ROSIM_JAR_SHA256,
            "ROSIM_JAR_SHA256 does not match the JAR in bin; bump the pinned constants "
            "(tag, name and SHA-256) together with the JAR.",
        )
