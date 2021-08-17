import importlib
from typing import Type


def dynamic_classimport(module_name: str, module_path: str) -> Type:
    """Dynamic import class method inspired by ESPnet.
    https://github.com/espnet/espnet

    Args:
        module_name (str): Module name. Import class name must be capitalized by this value.
            For example, in the case of `module_name=iterated_rippled_noise`,
            the class name is `IteratedRippledNoise`.
        import_dir (str): Directory path to import.
            The value must be splitted by `.` instead of `/` to import.

    Returns:
        Type: class object (i.e. <class 'type'>)
    """

    classname = "".join([i.capitalize() for i in module_name.split("_")])
    m = importlib.import_module(module_path + "." + module_name)
    return getattr(m, classname)
