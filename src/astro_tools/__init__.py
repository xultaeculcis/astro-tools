"""Astro Tools main entrypoint."""

#  Copyright (c) xultaeculcis. All rights reserved.
#  Licensed under MIT License.
from __future__ import annotations

import click

from astro_tools.cli.create_dirs import create_dirs


@click.group()  # type: ignore[misc]
def cli() -> None:
    """Main entrypoint for CLI."""


cli.add_command(create_dirs)


if __name__ == "__main__":
    cli()
