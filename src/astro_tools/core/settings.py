"""Application settings.

Examples:
    ```python
    import logging

    from src.core.settings import current_settings


    # log current environment
    logging.info(current_settings.env)  # INFO:dev
    ```

"""
#  Copyright (c) xultaeculcis. All rights reserved.
#  Licensed under MIT License.

from __future__ import annotations

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

from astro_tools.core import consts


class BlobStorageSettings(BaseModel):
    """Blob Storage settings."""

    account_name: str
    """Account name."""
    account_key: str
    """Account key."""

    @property
    def connection_string(self) -> str:
        """Connection string."""
        return (
            f"DefaultEndpointsProtocol=https;AccountName={self.account_name};AccountKey={self.account_key};"
            "EndpointSuffix=core.windows.net"
        )


class Settings(BaseSettings):
    """Represents Application Settings with nested configuration sections."""

    environment: str = "local"
    blob: BlobStorageSettings

    model_config = SettingsConfigDict(
        env_file=consts.directories.ROOT_DIR / ".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        extra="ignore",
    )


def current_settings() -> Settings:
    """Instantiate current application settings.

    Returns:
        Current application settings.

    """
    return Settings()
