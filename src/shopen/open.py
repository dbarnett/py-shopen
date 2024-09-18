import os
import subprocess
import sys
from typing import Union


def open(path: Union[os.PathLike, str]):
    if hasattr(os, "startfile"):
        os.startfile(path)
        return

    openers_to_try = []
    if sys.platform != "darwin":
        openers_to_try.append("xdg-open")
    if sys.platform != "win32":
        openers_to_try.append("open")

    for opener in openers_to_try:
        try:
            subprocess.call((opener, path))
            return
        except OSError:
            pass

    tried_str = ["os.startfile"] + openers_to_try
    raise OSError(
        f'open failed: no opener found for platform {sys.platform}. '
        f'Tried: {", ".join(tried_str)}'
    )
