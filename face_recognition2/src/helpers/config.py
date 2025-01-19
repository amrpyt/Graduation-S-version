from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    CAMER_INPUT: int = 0

    class Config:
        env_file = ".env"

def get_settings():
    return Settings()

