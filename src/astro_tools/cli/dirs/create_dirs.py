"""Automating directory creation."""
#  Copyright (c) xultaeculcis. All rights reserved.
#  Licensed under MIT License.

from __future__ import annotations

from pathlib import Path

import click
from tqdm import tqdm


@click.command("create")  # type: ignore[misc]
@click.option(  # type: ignore[misc]
    "--names_fp",
    type=click.Path(exists=True, file_okay=True, dir_okay=False, resolve_path=True, path_type=Path),
    help="Names file - one dir name per line",
)
@click.option(  # type: ignore[misc]
    "--target_dir",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, resolve_path=True, path_type=Path),
    help="Target directory where new sub-directories will be created",
)
def create_dirs(names_fp: Path, target_dir: Path) -> None:
    """Creates directories based on file with dir names."""
    names = names_fp.read_text().splitlines()
    target_dir.mkdir(parents=True, exist_ok=True)
    for name in tqdm(names, desc="Creating dirs"):
        (target_dir / name).mkdir(parents=True, exist_ok=True)
