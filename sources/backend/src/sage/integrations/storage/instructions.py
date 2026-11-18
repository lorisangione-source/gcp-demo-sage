"""Reads dynamic prompt instructions from Cloud Storage on each request."""

import logging

from google.api_core.exceptions import GoogleAPICallError, NotFound
from google.cloud import storage

from sage.config import get_app_config

log = logging.getLogger(__name__)


def fetch_extra_instructions() -> str:
    config = get_app_config()
    if not config.instructions_bucket:
        return ""
    try:
        client = storage.Client(project=config.project_id)
        bucket = client.bucket(config.instructions_bucket)
        blob = bucket.blob(config.instructions_blob)
        return blob.download_as_text(encoding="utf-8").strip()
    except NotFound:
        log.warning(
            "File %s non trovato nel bucket %s",
            config.instructions_blob,
            config.instructions_bucket,
        )
        return ""
    except GoogleAPICallError:
        log.warning(
            "Impossibile leggere %s da %s",
            config.instructions_blob,
            config.instructions_bucket,
            exc_info=True,
        )
        return ""
