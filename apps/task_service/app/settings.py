from pathlib import Path
from tempfile import gettempdir
from typing import Optional

from pydantic import BaseSettings
from yarl import URL

TEMP_DIR = Path(gettempdir())


class Settings(BaseSettings):
    """Application settings."""

    host: str = "127.0.0.1"
    port: int = 8000
    # quantity of workers for uvicorn
    workers_count: int = 1
    # Enable uvicorn reloading
    reload: bool = False
    db_file: Path = TEMP_DIR / "db.sqlite3"
    db_echo: bool = False
    @property
    def db_url(self) -> URL:
        """
        Assemble database URL from settings.

        :return: database URL.
        """
        return URL.build(
            scheme="sqlite+aiosqlite",
            path=f"///{self.db_file}",
        )

    class Config:
        env_file = ".env"
        env_prefix = "TASK_SERVICE_"
        env_file_encoding = "utf-8"


settings = Settings()
