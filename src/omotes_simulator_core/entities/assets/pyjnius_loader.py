import os
from typing import Dict

JavaClass = str


class PyjniusLoader:
    INSTANCE = None
    loaded_classes: Dict[str, JavaClass]

    def __init__(self):
        path = os.path.dirname(__file__)
        import jnius_config  # noqa

        jnius_config.add_classpath(os.path.join(path, "bin/jfxrt.jar"))
        jnius_config.add_classpath(os.path.join(path, "bin/rosim-batch-0.4.2.jar"))

        self.loaded_classes = {}

    def load_class(self, classpath: str) -> JavaClass:
        from jnius import autoclass  # noqa
        if classpath not in self.loaded_classes:
            self.loaded_classes[classpath] = autoclass(classpath)

        return self.loaded_classes[classpath]

    @staticmethod
    def get_loader() -> 'PyjniusLoader':
        if PyjniusLoader.INSTANCE is None:
            PyjniusLoader.INSTANCE = PyjniusLoader()
        return PyjniusLoader.INSTANCE
