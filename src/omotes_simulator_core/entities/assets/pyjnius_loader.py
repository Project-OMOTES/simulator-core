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

"""Binding to Rosim through Pyjnius."""
import glob
import hashlib
import logging
import os
import stat
import tempfile
import urllib.request
from typing import Callable

JavaClass = Callable
logger = logging.getLogger(__name__)

# These three values describe one specific published Rosim JAR asset and must be bumped
# together whenever a new Rosim JAR is released.
#
# The tag names the release whose asset is read, not the release this code ships in.
# `upload_rosim_to_release.yml` attaches a JAR to every release, but this code does not read
# those attachments: bumping the workflow's output alone leaves the pin serving the old JAR
# with its checksum still matching.
#
# When bumping, establish the digest from a trusted build of the JAR rather than from a copy
# downloaded through this pin. A digest taken from the downloaded file only restates that
# file's contents and would attest to a tampered artifact just as readily as a genuine one.
ROSIM_RELEASE_TAG = "0.0.30"
ROSIM_JAR_NAME = "rosim-batch-1.2.0.jar"
ROSIM_JAR_SHA256 = "8483fb9eb68608cffc3b72279b19947b2c1cfd9f936377c278ee0f3291b68547"

# Derived at import; patching a constant above in a test will not change it.
ROSIM_JAR_URL = (
    f"https://github.com/Project-OMOTES/simulator-core/releases/download/"
    f"{ROSIM_RELEASE_TAG}/{ROSIM_JAR_NAME}"
)

_HASH_CHUNK_SIZE = 1024 * 1024


def _get_bin_path() -> str:
    """Return the directory that holds the bundled JAR files."""
    return os.path.join(os.path.dirname(__file__), "bin")


def _sha256_of_file(file_path: str) -> str:
    """Return the hex SHA-256 digest of a file, read in chunks to bound memory use."""
    digest = hashlib.sha256()
    with open(file_path, "rb") as file_handle:
        for chunk in iter(lambda: file_handle.read(_HASH_CHUNK_SIZE), b""):
            digest.update(chunk)
    return digest.hexdigest()


class PyjniusLoader:
    """Class to load Pyjnius and connect to Rosim.

    This is a singleton and you should only use PyjniusLoader.get_loader() instead of
    constructing this class directly.

    Also ensure that after loading this class, the process is not forked into a subprocess
    as this will destroy the connection to Pyjnius and may lead to an indefinite hang when using
    Java code.
    """

    INSTANCE = None
    loaded_classes: dict[str, JavaClass]

    def __init__(self) -> None:
        """Create an instance of PyjniusLoader.

        This function should only be called ONCE. Do not use construct this class directly
        but rather use `PyjniusLoader.get_loader`.
        """
        bin_path = _get_bin_path()
        import jnius_config  # noqa

        # Resolved through _get_bin_path so the classpath cannot drift from the folder
        # download_rosim_jar writes into.
        self.rosim_jar = self.download_rosim_jar()
        jnius_config.add_classpath(os.path.join(bin_path, "jfxrt.jar"))
        jnius_config.add_classpath(os.path.join(bin_path, self.rosim_jar))
        self.loaded_classes = {}

    @staticmethod
    def download_rosim_jar() -> str:
        """Ensure the Rosim JAR is present in the `bin` folder and return its file name.

        The JAR is downloaded at runtime rather than shipped inside the wheel because it
        exceeds the 100 MB per-file size limit on PyPI.

        If any `rosim*.jar` is already present in the `bin` folder, no download happens and
        that file is used, whatever its version. Picking up a newer Rosim JAR therefore takes
        both steps: bump the module-level constants and delete the local copy, since either
        one alone leaves the existing file in place.

        The JAR is fetched from a pinned release asset URL, written to a temporary file in
        the `bin` folder and verified against `ROSIM_JAR_SHA256`. Only a file with a matching
        digest is moved into its final place, so an interrupted or corrupted download can
        never be picked up as a valid cached JAR. A RuntimeError is raised when the digest
        does not match.
        """
        bin_path = _get_bin_path()

        # First a check if there are already jar files present.
        jar_files = glob.glob(os.path.join(bin_path, "rosim*.jar"))
        if jar_files:
            logger.debug("Rosim JAR files already present, skipping download.")
            logger.debug("Using Rosim JAR file: %s", jar_files[0])
            return os.path.basename(jar_files[0])

        logger.debug("Downloading Rosim JAR files from GitHub")
        os.makedirs(bin_path, exist_ok=True)
        final_path = os.path.join(bin_path, ROSIM_JAR_NAME)

        # Download next to the target so the final move is an atomic rename on the same volume.
        # The temporary name must never match the `rosim*.jar` cache glob above: a partial
        # download left behind by a killed process would otherwise be cached as a valid JAR.
        temp_fd, temp_path = tempfile.mkstemp(dir=bin_path, prefix=".rosim-download-")
        try:
            os.close(temp_fd)
            # mkstemp creates the file 0600 and os.replace preserves that, where a plain
            # download would have taken the umask default. Copy the mode of a sibling that the
            # package itself shipped, so the JAR ends up as readable as the rest of `bin` for
            # whoever the JVM runs as. Reading the umask instead would mean mutating
            # process-global state, which is not safe to do from a library.
            reference = os.path.join(bin_path, "jfxrt.jar")
            if os.path.exists(reference):
                os.chmod(temp_path, stat.S_IMODE(os.stat(reference).st_mode))
            urllib.request.urlretrieve(ROSIM_JAR_URL, temp_path)
            actual_hash = _sha256_of_file(temp_path)
            if actual_hash != ROSIM_JAR_SHA256:
                raise RuntimeError(
                    f"Checksum mismatch for downloaded Rosim JAR from {ROSIM_JAR_URL}: "
                    f"expected SHA-256 {ROSIM_JAR_SHA256}, got {actual_hash}."
                )
            os.replace(temp_path, final_path)
        except BaseException:
            try:
                if os.path.exists(temp_path):
                    os.remove(temp_path)
            except OSError:
                # A failure to clean up must not replace the error that caused it, which
                # carries the reason the download is unusable.
                logger.warning("Failed to remove temporary download %s.", temp_path, exc_info=True)
            raise

        logger.debug("Using Rosim JAR file: %s", final_path)
        return ROSIM_JAR_NAME

    def load_class(self, classpath: str) -> JavaClass:
        """Load a Java class.

        If it has been loaded previously, the reference to the class will be loaded from cache.
        Otherwise, it is loaded through pyjnius.

        """
        from jnius import autoclass  # noqa

        try:
            if classpath not in self.loaded_classes:
                self.loaded_classes[classpath] = autoclass(classpath)
        except Exception as exc:
            logger.error(f"Failed to load Java class {classpath}: {exc}")

        return self.loaded_classes[classpath]

    @staticmethod
    def get_loader() -> "PyjniusLoader":
        """Get the global instance of the PyjniusLoader.

        This loader allows to load Java classes. This is the preferred method of retrieving
        a reference to the PyjniusLoader.
        """
        if PyjniusLoader.INSTANCE is None:
            PyjniusLoader.INSTANCE = PyjniusLoader()
        return PyjniusLoader.INSTANCE
