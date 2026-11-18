"""Application settings, loaded from environment variables prefixed with SAGE_."""

from functools import lru_cache

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="SAGE_", case_sensitive=False, extra="ignore")

    # GCP
    project_id: str
    region: str = "europe-west6"
    resource_prefix: str = ""

    # Cloud Storage (istruzioni aggiuntive)
    instructions_bucket: str = ""
    instructions_blob: str = "istruzioni.md"

    # Firestore
    firestore_database: str = "(default)"
    firestore_collection: str = "chunks"
    top_k: int = 5

    # Vertex AI models
    chat_model: str = "gemini-2.5-flash"
    embedding_model: str = "text-embedding-004"
    embedding_dimension: int = 768

    # BigQuery
    bq_dataset: str = "sage_analytics"
    bq_table: str = "question_log"

    # Ingestion
    chunk_max_chars: int = 1500

    @model_validator(mode="after")
    def _apply_resource_prefix(self) -> "AppConfig":
        if not self.resource_prefix:
            if not self.instructions_bucket:
                self.instructions_bucket = f"{self.project_id}-instructions"
            return self
        self.firestore_database = self.resource_prefix
        self.bq_dataset = f"{self.resource_prefix.replace('-', '_')}_{self.bq_dataset}"
        if not self.instructions_bucket:
            self.instructions_bucket = f"{self.resource_prefix}-instructions"
        return self


@lru_cache
def get_app_config() -> AppConfig:
    return AppConfig()
