"""Zip archive validation functions and classes."""

#  Copyright (c) xultaeculcis. All rights reserved.
#  Licensed under MIT License.
from __future__ import annotations

import logging
import zipfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import click
import pyzipper
from tqdm import tqdm

from astro_tools.utils.logging import get_logger

_logger = get_logger(__name__)


def check_zip_fast(zip_path: Path) -> tuple[Path, str | None]:
    """Runs fast zip archive check by trying to list compressed file metadata.

    Args:
        zip_path: The path to the zip file.

    Returns:
        A tuple containing a zip file path and a string summary of errors.

    """
    errors = []
    try:
        with zipfile.ZipFile(zip_path, "r") as zf:
            # List files and sizes
            _ = [
                f"{info.filename} - {info.file_size} bytes (compressed: {info.compress_size} bytes)"
                for info in zf.infolist()
            ]
            _logger.info("File %s is OK", zip_path.as_posix())
            return zip_path, None

    except zipfile.BadZipFile:
        msg = f"Bad ZIP file: {zip_path.as_posix()}"
        _logger.exception(msg)
        errors.append(msg)

    except NotImplementedError:
        try:
            _logger.warning("Unsupported compression for file %s - fallback to pyzipper", zip_path.as_posix())
            with pyzipper.AESZipFile(zip_path) as zf:
                _ = zf.namelist()
                _logger.info("File %s is OK", zip_path.as_posix())

        except Exception:
            msg = f"Error checking {zip_path.as_posix()}"
            _logger.exception(msg)
            errors.append(msg)

    except Exception:
        msg = f"Error checking {zip_path.as_posix()}"
        _logger.exception(msg)
        errors.append(msg)

    return zip_path, "\n".join(errors)


def check_zip_full(zip_path: Path) -> tuple[Path, str | None]:
    """Runs full zip archive check by running zip test.

    Args:
        zip_path: A path to the zip file.

    Returns:
        A tuple containing a zip file path and a string summary of errors.

    """
    try:
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            bad_file = zip_ref.testzip()
            if bad_file:
                msg = f"Corrupted file '{bad_file}' in archive: {zip_path.as_posix()}"
                _logger.warning(msg)
                return zip_path, msg
            _logger.info("File %s is OK", zip_path.as_posix())
            return zip_path, None
    except zipfile.BadZipFile:
        msg = f"Bad ZIP file: {zip_path.as_posix()}"
        _logger.exception(msg)
        return zip_path, msg
    except Exception:
        msg = f"Error checking {zip_path.as_posix()}"
        _logger.exception(msg)
        return zip_path, msg


@click.command("check")  # type: ignore[misc]
@click.option(  # type: ignore[misc]
    "--directory",
    type=click.Path(exists=True, file_okay=False, path_type=Path, resolve_path=True),
    default=".",
    help="Directory to check",
)
@click.option(  # type: ignore[misc]
    "--log_file",
    type=click.Path(writable=True, file_okay=True, dir_okay=False, path_type=Path),
    default="./zip-check.log",
    help="Path to the log file (will create one in the current working directory if not specified)",
)
@click.option(  # type: ignore[misc]
    "--workers",
    default=2,
    show_default=True,
    help="Number of threads for parallel checking",
)
@click.option(  # type: ignore[misc]
    "--fast",
    default=False,
    is_flag=True,
    help="Run fast check only by trying to list zip contents",
)
@click.option(  # type: ignore[misc]
    "--full",
    default=False,
    is_flag=True,
    help="Run full check by running zip test",
)
def check_zips(
    directory: Path,
    log_file: Path,
    workers: int,
    *,
    fast: bool = False,
    full: bool = False,
) -> None:
    """Runs corruption check against zip archives in specified directory.

    Args:
        directory: The directory containing zip archives.
        log_file: Path to the log file (will create one in the current working directory if not specified).
        workers: Number of threads for parallel checking.
        fast: Run fast check by trying to list zip contents.
        full: Run full check by running zip test.

    """
    zip_log_file = Path(f"zip_check-{directory.stem}.log")
    if zip_log_file.exists():
        zip_log_file.unlink()

    _logger.addHandler(logging.FileHandler(log_file))

    if not fast and not full:
        _logger.warning("No zip check mode specified - running fast check only.")

    zip_files = list(directory.rglob("*.zip"))
    _logger.info("Found %d ZIP files in %s", len(zip_files), directory.as_posix())

    corrupted = []

    func = check_zip_fast if fast else check_zip_full

    with ThreadPoolExecutor(max_workers=workers) as executor:
        future_to_path = {executor.submit(func, zip_path): zip_path for zip_path in zip_files}
        for future in tqdm(as_completed(future_to_path), total=len(zip_files), desc="Checking ZIP files", unit="file"):
            zip_path, error_msg = future.result()
            if error_msg:
                _logger.error(error_msg)
                corrupted.append(zip_path)

    if corrupted:
        _logger.info("\nSummary: Corrupted archives found:")
        for path in corrupted:
            _logger.info(" - %s", path.as_posix())
        _logger.info("Total corrupted files: %d", len(corrupted))
    else:
        _logger.info("No corrupted ZIP files found.")
