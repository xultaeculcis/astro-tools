"""Astro Tools main entrypoint."""

#  Copyright (c) xultaeculcis. All rights reserved.
#  Licensed under MIT License.
from __future__ import annotations

import click

from astro_tools.cli.blob.blob_upload import blob_upload
from astro_tools.cli.dirs.create_dirs import create_dirs
from astro_tools.cli.zips.check_zips import check_zips
from astro_tools.cli.zips.rename_zips import rename_zips


@click.group()  # type: ignore[misc]
def cli() -> None:
    """Main entrypoint for CLI."""


@cli.group("dir")  # type: ignore[misc]
def cli_dir() -> None:
    """Astro directory related operations."""


@cli.group("zip")  # type: ignore[misc]
def cli_zip() -> None:
    """Zip archive related operations."""


@cli.group("blob")  # type: ignore[misc]
def cli_blob() -> None:
    """Blob storage related operations."""


cli_dir.add_command(create_dirs)
cli_zip.add_command(rename_zips)
cli_zip.add_command(check_zips)
cli_blob.add_command(blob_upload)


if __name__ == "__main__":
    cli()
