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
import logging
import os
from typing import Callable

JavaClass = Callable
logger = logging.getLogger(__name__)


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
        path = os.path.dirname(__file__)
        import jnius_config  # noqa

        self.rosim_jar = self.download_rosim_jar()
        jnius_config.add_classpath(os.path.join(path, "bin/jfxrt.jar"))
        jnius_config.add_classpath(os.path.join(path, "bin", self.rosim_jar))
        self.loaded_classes = {}

    @staticmethod
    def download_rosim_jar() -> str:
        """Download the Rosim JAR files.

        This function will download the required Rosim JAR files into the `bin` folder.
        It will download it from the latest release on github of the simulator-core repository.
        If there is already a rosim jar in the bin folder it will not download it and use that one.
        If you want the downloaded the latest one, simply delete your local copy.
        We have implemented this to bypass the 100 mb size limit on pypi.
        It returns the name of the downloaded JAR file.
        """
        import glob
        import urllib.request

        import requests

        # First a check if there are already jar files present.
        base_path = os.path.dirname(__file__)
        bin_path = os.path.join(base_path, "bin")

        jar_files = glob.glob(os.path.join(bin_path, "rosim*.jar"))
        if jar_files:
            logger.debug("Rosim JAR files already present, skipping download.")
            logger.debug(f"Using Rosim JAR file: {jar_files[0]}")
            return jar_files[0]

        repo = "Project-OMOTES/simulator-core"
        api_url = f"https://api.github.com/repos/{repo}/releases/latest"

        response = requests.get(api_url)
        release_data = response.json()
        assets = release_data["assets"]
        for asset in assets:
            if "rosim" in asset["name"]:
                # downloading the jar file from github releeases
                logger.debug("Downloading Rosim JAR files from GitHub")
                url = asset["browser_download_url"]
                jar_file = os.path.join(bin_path, asset["name"])
                response_url = urllib.request.urlretrieve(
                    url,
                    jar_file,
                )
                if response_url is None:
                    raise RuntimeError("Failed to download Rosim JAR files.")
                return str(asset["name"])
        raise RuntimeError("Failed to find Rosim JAR files in GitHub releases.")

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
