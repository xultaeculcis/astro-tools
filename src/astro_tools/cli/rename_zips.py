"""Renaming telescope-live zip archives."""

#  Copyright (c) xultaeculcis. All rights reserved.
#  Licensed under MIT License.
from __future__ import annotations

import shutil
import zipfile
from collections import defaultdict
from pathlib import Path

import click

CHANNEL_LOOKUP = {
    "_ha_": "H",
    "_halpha_": "H",
    "_sii_": "S",
    "_oiii_": "O",
    "_luminance_": "L",
    "_lum_": "L",
    "_red_": "R",
    "_green_": "G",
    "_blue_": "B",
}
CHANNEL_PATTERNS = ("_ha_", "_halpha_", "_sii_", "_oiii_", "_blue_", "_red_", "_green_", "_lum_", "_luminance_")


@click.command("rename-zips")  # type: ignore[misc]
@click.option(  # type: ignore[misc]
    "--data_dir",
    type=click.Path(exists=True, dir_okay=True, file_okay=False, path_type=Path),
    help="Path to the directory containing telescope-live data",
)
def rename_zips(data_dir: Path) -> None:
    """Rename telescope-live zip archives.

    Args:
        data_dir: Path to the directory containing telescope-live data.

    """
    fps = sorted(data_dir.rglob("*.zip"))

    name_lookup: dict[str, list[Path]] = defaultdict(list)
    for zip_fp in fps:
        with zipfile.ZipFile(zip_fp, "r") as zf:
            channels = set()
            for info in zf.infolist():
                for f in CHANNEL_PATTERNS:
                    if f in info.filename.lower():
                        channels.add(f)
            channel_combination = ""
            for c, v in CHANNEL_LOOKUP.items():
                if c in channels:
                    channel_combination += v
            target, telescope, frames, _ = zip_fp.stem.split("_")
            new_zip_archive_name = f"{target}_{telescope}_{channel_combination}_{frames}"
            name_lookup[new_zip_archive_name].append(zip_fp)

    for new_name, files in name_lookup.items():
        if len(files) > 1:
            for idx, fp in enumerate(files, start=1):
                click.echo(f"Renaming {fp.name} to {new_name}-{idx}.zip")
                shutil.move(fp, fp.parent / f"{new_name}-{idx}.zip")
            continue
        fp = files[0]
        click.echo(f"Renaming {fp.name} to {new_name}.zip")
        shutil.move(fp, fp.parent / f"{new_name}.zip")
