
import streamlit as st
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from .env or environment variables."""

    app_name: str = "Amanara AI Chatbot"
    app_env: str = "development"
    debug: bool = False

    google_api_key: str = ""

    qdrant_url: str = "http://localhost:6333"
    qdrant_api_key: str = ""
    qdrant_collection: str = "amanara_docs"

    llm_model: str = "gemini-2.5-flash"
    embedding_model: str = "text-embedding-004"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


# Load local .env and environment variables first.
settings = Settings()

# Override with Streamlit Cloud secrets when available.
try:
    secret_mapping = {
        "GOOGLE_API_KEY": "google_api_key",
        "QDRANT_URL": "qdrant_url",
        "QDRANT_API_KEY": "qdrant_api_key",
        "QDRANT_COLLECTION": "qdrant_collection",
    }

    for secret_name, setting_name in secret_mapping.items():
        if secret_name in st.secrets:
            setattr(settings, setting_name, st.secrets[secret_name])

except Exception:
    # Streamlit secrets may not exist during local development.
    pass
