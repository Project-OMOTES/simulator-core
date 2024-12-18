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

import os
from typing import Dict, Callable

JavaClass = Callable


class PyjniusLoader:
    """Class to load Pyjnius and connect to Rosim.

    This is a singleton and you should only use PyjniusLoader.get_loader() instead of
    constructing this class directly.

    Also ensure that after loading this class, the process is not forked into a subprocess
    as this will destroy the connection to Pyjnius and may lead to an indefinite hang when using
    Java code.
    """

    INSTANCE = None
    loaded_classes: Dict[str, JavaClass]

    def __init__(self) -> None:
        """Create an instance of PyjniusLoader.

        This function should only be called ONCE. Do not use construct this class directly
        but rather use `PyjniusLoader.get_loader`.
        """
        path = os.path.dirname(__file__)
        import jnius_config  # noqa

        jnius_config.add_classpath(os.path.join(path, "bin/jfxrt.jar"))
        jnius_config.add_classpath(os.path.join(path, "bin/rosim-batch-0.4.2.jar"))

        self.loaded_classes = {}

    def load_class(self, classpath: str) -> JavaClass:
        """Load a Java class.

        If it has been loaded previously, the reference to the class will be loaded from cache.
        Otherwise, it is loaded through pyjnius.

        """
        from jnius import autoclass  # noqa
        if classpath not in self.loaded_classes:
            self.loaded_classes[classpath] = autoclass(classpath)

        return self.loaded_classes[classpath]

    @staticmethod
    def get_loader() -> 'PyjniusLoader':
        """Get the global instance of the PyjniusLoader.

        This loader allows to load Java classes. This is the preferred method of retrieving
        a reference to the PyjniusLoader.
        """
        if PyjniusLoader.INSTANCE is None:
            PyjniusLoader.INSTANCE = PyjniusLoader()
        return PyjniusLoader.INSTANCE
