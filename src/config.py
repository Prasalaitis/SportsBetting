from pydantic import BaseSettings

class Settings(BaseSettings):
    app_key: str
    session_token: str
    kafka_bootstrap_servers: str
    kafka_topic: str

    class Config:
        env_file = ".env"

settings = Settings()