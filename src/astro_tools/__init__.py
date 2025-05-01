"""Astro Tools main entrypoint."""

#  Copyright (c) xultaeculcis. All rights reserved.
#  Licensed under MIT License.
from __future__ import annotations

from astro_tools.utils.logging import get_logger

_logger = get_logger(__name__)


def main() -> None:
    """Main entry point for astro-tools."""
    _logger.info("Hello from astro-tools!")


if __name__ == "__main__":
    main()
