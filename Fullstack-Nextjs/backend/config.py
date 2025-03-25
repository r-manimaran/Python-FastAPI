from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Awesome API"
    database_host: str
    database_port: str
    database_name: str
    database_user: str
    database_password: str
    
    class Config:
        env_file = ".env"