import os
import subprocess
import sys
from typing import Union

SUPPORTED_OPERATIONS = frozenset({"open", "edit"})


def open(
    path: Union[os.PathLike, str],
    operation: str = "open",
):
    if operation not in SUPPORTED_OPERATIONS:
        raise ValueError(
            f"Unsupported operation {operation!r}. "
            f"Operation must be one of: {', '.join(SUPPORTED_OPERATIONS)}"
        )

    if hasattr(os, "startfile"):
        os.startfile(path, operation)
        return

    openers_to_try = []
    if operation == "edit" and sys.platform != "win32":
        openers_to_try.append("editor")
        from_env = os.environ.get("EDITOR")
        if from_env:
            openers_to_try.append(from_env)
    if sys.platform != "win32":
        if sys.platform != "darwin":
            openers_to_try.append("xdg-open")
        openers_to_try.append("open")

    for opener in openers_to_try:
        try:
            subprocess.call([opener, path])
            return
        except OSError:
            pass

    tried_str = ["os.startfile"] + openers_to_try
    raise OSError(
        f'open failed: no opener found for platform {sys.platform}. '
        f'Tried: {", ".join(tried_str)}'
    )
