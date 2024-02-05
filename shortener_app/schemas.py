from pydantic import BaseModel

class URLBase(BaseModel):
    target_url: str
    
    # 基础URL模型，包含目标URL属性
    # target_url: str

class URL(URLBase):
    is_active: bool
    clicks: int
    
    class Config:
        orm_mode = True

    # URL模型，继承自URLBase，包含是否激活、点击次数属性
    # is_active: bool
    # clicks: int
    
    # 配置ORM模式为True
    class Config:
        orm_mode = True

class URLInfo(URL):
    url: str
    admin_url: str

    # URL信息模型，继承自URL，包含URL和管理URL属性
    # url: str
    # admin_url: str
