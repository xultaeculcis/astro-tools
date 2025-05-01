#  Copyright (c) xultaeculcis. All rights reserved.
#  Licensed under MIT License.

from __future__ import annotations

import pathlib
import typing

import pytest

if typing.TYPE_CHECKING:
    from _pytest.config import Config
    from _pytest.python import Function

MARKERS = ["unit"]


def pytest_collection_modifyitems(config: Config, items: list[Function]) -> None:  # noqa: ARG001
    rootdir = pathlib.Path(__file__).parent.parent
    for item in items:
        rel_path = pathlib.Path(item.fspath).relative_to(rootdir)
        mark_name = rel_path.as_posix().split("/")[1]
        if mark_name in MARKERS:
            mark = getattr(pytest.mark, mark_name)
            item.add_marker(mark)
