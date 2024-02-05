# 导入所需的模块
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 导入配置模块
from .config import get_settings

# 获取数据库引擎
engine = create_engine(get_settings().db_url, connect_args={"check_same_thread": False})

# 创建会话类
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建基类
Base = declarative_base()
