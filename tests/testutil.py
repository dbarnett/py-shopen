from enum import Enum
from typing import Any, Dict, List, NamedTuple


class FuncArgs(NamedTuple):
    args: List[Any]
    kwargs: Dict[str, Any]


class OpScenario(FuncArgs, Enum):
    NO_OPERATION = FuncArgs([], {})
    ARG_NONE = FuncArgs([None], {})
    KWARG_NONE = FuncArgs([], {"operation": None})
    OPEN = FuncArgs(["open"], {})
    EDIT = FuncArgs(["edit"], {})


def no_such_command_callback(process):
    raise FileNotFoundError(2, "No such file or directory")
