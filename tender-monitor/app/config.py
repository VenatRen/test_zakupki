from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class Settings(BaseSettings):

    database_url: str
    redis_url: str

    telegram_bot_token: str = ""
    telegram_chat_id: str = ""

    collect_interval_minutes: int = 15

    okpd_prefix: str = "85"

    initial_lookback_days: int = 7

    download_documents: bool = True
    document_dir: str = "/app/data/documents"

    headless: bool = True
    browser_timeout_ms: int = 60000

    enable_eis: bool = True
    enable_fabrikant: bool = True
    enable_tektorg: bool = True
    enable_rts: bool = True

    fabrikant_url: str

    tektorg_url: str
    rts_url: str

    max_pages_per_source: int = 100
    request_delay_seconds: float = 2

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()
