"""Parallel blob storage data upload functions and classes."""

#  Copyright (c) xultaeculcis. All rights reserved.
#  Licensed under MIT License.
from __future__ import annotations

import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import click
from azure.storage.blob import BlobServiceClient, ContainerClient
from tqdm import tqdm

from astro_tools.core.settings import current_settings
from astro_tools.utils.logging import get_logger

_logger = get_logger(__name__)

# CONFIG
PREFIX = "whwang/gdrive-export"
LOCAL_DIRECTORY = "/content/drive/MyDrive/Other/Astrophoto_Release/"


@click.command("upload")  # type: ignore[misc]
@click.option(  # type: ignore[misc]
    "--source_dir",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path),
    required=True,
    help="The path to the source directory",
)
@click.option(  # type: ignore[misc]
    "--lookup_file",
    type=click.Path(file_okay=True, dir_okay=False, path_type=Path),
    help="The lookup file path to be used instead of listing the contents of the source directory.",
)
@click.option("--prefix", help="The prefix for the blob files.", required=True)  # type: ignore[misc]
@click.option(  # type: ignore[misc]
    "--container",
    default="datasets",
    help="The name of the  blob container.",
)
@click.option(  # type: ignore[misc]
    "--workers",
    default=4,
    help="The number of worker threads to use for uploading.",
)
def blob_upload(
    source_dir: Path,
    prefix: str,
    lookup_file: Path | None = None,
    container: str = "datasets",
    workers: int = 4,
) -> None:
    """Uploads files from source directory to specified Blob Storage container."""
    settings = current_settings()
    source_dir = source_dir.resolve().absolute()

    blob_service_client = BlobServiceClient.from_connection_string(settings.blob.connection_string)
    container_client = blob_service_client.get_container_client(container)

    if lookup_file is None:
        lookup_file = Path.cwd() / "file_lookup.txt"

    prefix = prefix.strip("/")

    # Load lookup files
    if lookup_file.exists():
        all_files = {Path(line) for line in lookup_file.read_text().splitlines()}
    else:
        all_files = {
            Path(fp)
            for fp in tqdm(source_dir.rglob("*"), desc=f"Listing files under: {source_dir.name}")
            if fp.is_file()
        }
        lookup_file.write_text("\n".join([fp.as_posix() for fp in all_files]))

    all_files = {path.relative_to(source_dir) for path in all_files}

    if not all_files:
        _logger.warning("No files to upload under %s.", source_dir.as_posix())
        return

    # Remove already uploaded files from the set
    _logger.info("File count before deduplication: %d", len(all_files))
    _logger.info("Scanning Azure Blob Storage for existing blobs under '%s'...", prefix)

    existing_blobs = _list_existing_blobs(container_client, prefix)
    existing_relative_paths = {
        Path(blob_name[len(prefix) + 1 :]) for blob_name in existing_blobs
    }  # remove prefix from paths
    files_to_upload = all_files - existing_relative_paths

    if not files_to_upload:
        _logger.info("All files already uploaded... Nothing to do.")
        return

    _logger.info("File count after deduplication: %d", len(files_to_upload))

    # Run the upload
    _upload_files_parallel(
        base_path=source_dir,
        files_to_upload=[Path(source_dir) / fp for fp in files_to_upload],
        container_client=container_client,
        max_workers=workers,
        prefix=prefix,
    )


def _blob_exists(container_client: ContainerClient, blob_name: str) -> bool:
    """Check if a blob already exists."""
    try:
        container_client.get_blob_client(blob_name).get_blob_properties()
    except Exception:  # noqa: BLE001
        return False
    else:
        return True


def _list_existing_blobs(container_client: ContainerClient, prefix: str) -> set[str]:
    """List all existing blobs under a given prefix."""
    blob_names: set[str] = set()
    blobs = container_client.list_blobs(name_starts_with=prefix)
    blob_names.update(blob.name for blob in blobs)
    return blob_names


def _upload_single_file(
    path: Path,
    base_path: Path,
    container_client: ContainerClient,
    prefix: str,
) -> tuple[str, int]:
    """Upload one file if it doesn't exist."""
    blob_name = f"{prefix}/" + str(path.relative_to(base_path)).replace("\\", "/")
    blob_client = container_client.get_blob_client(blob_name)
    file_data = path.read_bytes()
    blob_client.upload_blob(file_data)
    return blob_name, len(file_data)  # Return size of uploaded file


def _upload_files_parallel(
    base_path: Path,
    files_to_upload: list[Path],
    container_client: ContainerClient,
    prefix: str,
    max_workers: int = 2,
) -> None:
    """Uploads selected files to Blob Storage in parallel."""
    total_size_uploaded = 0
    start_time = time.time()

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(
                _upload_single_file,
                path,
                base_path,
                container_client,
                prefix,
            )
            for path in files_to_upload
        ]

        with tqdm(total=len(futures), unit="file") as pbar:
            for future in as_completed(futures):
                blob_name, size_uploaded = future.result()
                if size_uploaded > 0:
                    total_size_uploaded += size_uploaded
                pbar.set_description(f"Last: {blob_name} ({size_uploaded / 1024 / 1024:.2f} MB)")
                pbar.update(1)

    elapsed_time = time.time() - start_time
    throughput = (total_size_uploaded / (1024 * 1024)) / elapsed_time  # MB/sec

    _logger.info("\nUploaded %s MB in %s seconds.", f"{total_size_uploaded / (1024 * 1024):.2f}", f"{elapsed_time:.2f}")
    _logger.info("Average throughput: %s MB/s", f"{throughput:.2f}")
