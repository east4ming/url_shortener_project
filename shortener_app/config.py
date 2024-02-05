from functools import lru_cache

from pydantic import BaseSettings

class Settings(BaseSettings):
    """
    设置类，继承自BaseSettings类
    """

    env_name: str = "Local"  # 环境名称，默认为"Local"
    base_url: str = "http://localhost:8000"  # 基础URL，默认为"http://localhost:8000"
    db_url: str = "sqlite:///./shortener.sqlite"  # 数据库URL，默认为"sqlite:///./shortener.sqlite"

    class Config:
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    """
    获取设置类实例
    """
    settings = Settings()
    print(f"Loading settings for: {settings.env_name}")
    return settings

if __name__ == "__main__":
    get_settings()
