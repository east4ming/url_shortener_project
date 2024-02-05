from sqlalchemy import Column, Integer, String, Boolean
from .database import Base

class URL(Base):
    """
    URL模型类

    属性:
    - id: URL的ID，主键
    - key: URL的唯一标识，唯一且具有索引
    - secret_key: URL的密钥，唯一且具有索引
    - target_url: URL的目标地址，具有索引
    - is_active: URL是否可用，默认为True
    - clicks: URL的点击次数，默认为0
    """
    __tablename__ = "urls"
    
    id = Column(Integer, primary_key=True)
    key = Column(String, unique=True, index=True)
    secret_key = Column(String, unique=True, index=True)
    target_url = Column(String, index=True)
    is_active = Column(Boolean, default=True)
    clicks = Column(Integer, default=0)
