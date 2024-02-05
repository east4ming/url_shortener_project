import secrets
import validators

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from . import models, schemas
from .database import SessionLocal, engine

app = FastAPI()
models.Base.metadata.create_all(bind=engine)


def get_db():
    """
    获取数据库会话对象

    Returns:
        Session: 数据库会话对象
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def raise_bad_request(message):
    """
    抛出400错误

    Args:
        message (str): 错误信息

    Raises:
        HTTPException: 400错误
    """
    raise HTTPException(status_code=400, detail=message)


def raise_not_found(request):
    """
    抛出404错误

    Args:
        message (str): 错误信息

    Raises:
        HTTPException: 404错误
    """
    message = f"URL '{request.url}' not found."
    raise HTTPException(status_code=404, detail=message)


@app.get("/")
async def root():
    """
    获取根路径

    Returns:
        dict: {"message": "Hello World"}
    """
    return {"message": "Hello World"}


@app.post("/url", response_model=schemas.URLInfo)
def create_url(url: schemas.URLBase, db: Session = Depends(get_db)):
    """
    创建URL

    Args:
        url (schemas.URLBase): URL基本信息
        db (Session): 数据库会话对象

    Returns:
        schemas.URLInfo: 创建的URL信息
    """
    if not validators.url(url.target_url):
        raise_bad_request(message="Invalid URL")
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    key = "".join(secrets.choice(chars) for _ in range(5))
    secret_key = "".join(secrets.choice(chars) for _ in range(8))
    db_url = models.URL(target_url=url.target_url, key=key, secret_key=secret_key)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    db_url.url = key
    db_url.admin_url = secret_key

    return db_url


@app.get("/{url_key}")
def forward_to_target_url(
    url_key: str, request: Request, db: Session = Depends(get_db)
):
    """
    转发到目标URL

    Args:
        url_key (str): URL的key
        request (Request): 请求对象
        db (Session): 数据库会话对象

    Returns:
        RedirectResponse: 重定向响应
    """
    db_url = (
        db.query(models.URL)
        .filter(models.URL.key == url_key, models.URL.is_active)
        .first()
    )
    if db_url:
        return RedirectResponse(db_url.target_url)
    else:
        raise_not_found(request)