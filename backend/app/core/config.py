from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "InnoPMS Starter API"
    app_env: str = "development"
    debug: bool = True
    api_v1_str: str = "/api/v1"
    mysql_host: str = "127.0.0.1"
    mysql_port: int = 3306
    mysql_user: str = "root"
    mysql_password: str = "secret"
    mysql_database: str = "innopms"
    database_url: str = "mysql+pymysql://root:secret@127.0.0.1:3306/innopms"

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False, extra="ignore")


settings = Settings()
