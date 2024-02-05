import validators

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from starlette.datastructures import URL

from . import crud, models, schemas
from .database import SessionLocal, engine
from .config import get_settings

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


def get_admin_info(db_url: models.URL) -> schemas.URLInfo:
    """
    获取URL信息

    Args:
        db_url (models.URL): URL对象

    Returns:
        schemas.URLInfo: URL信息
    """
    base_url = URL(get_settings().base_url)
    admin_endpoint = app.url_path_for(
        "administration info", secret_key=db_url.secret_key
    )
    db_url.url = str(base_url.replace(path=db_url.key))
    db_url.admin_url = str(base_url.replace(path=admin_endpoint))
    return db_url


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
    db_url = crud.create_db_url(db, url)

    return get_admin_info(db_url)


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
    if db_url := crud.get_db_url_by_key(db, url_key):
        crud.update_db_clicks(db, db_url)
        return RedirectResponse(db_url.target_url)
    else:
        raise_not_found(request)


@app.get(
    "/admin/{secret_key}", name="administration info", response_model=schemas.URLInfo
)
def get_url_info(secret_key: str, request: Request, db: Session = Depends(get_db)):
    """
    获取URL信息

    Args:
        secret_key (str): URL的secret_key
        request (Request): 请求对象
        db (Session): 数据库会话对象

    Returns:
        schemas.URLInfo: URL信息
    """
    if db_url := crud.get_db_url_by_secret_key(db, secret_key):
        return get_admin_info(db_url)
    else:
        raise_not_found(request)
