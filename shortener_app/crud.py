from sqlalchemy.orm import Session

from . import models, schemas, keygen


def create_db_url(db: Session, url: schemas.URLBase) -> models.URL:
    """
    创建一个URL对象，将传入的url对象的target_url属性作为URL对象的target_url属性，key为生成的key，secret_key为生成的secret_key
    :param db: 数据库会话对象
    :param url: 传入的url对象
    :return: 创建的URL对象
    """
    # 生成一个唯一的随机的key
    key = keygen.create_unique_key(db)
    # 生成一个随机的密钥，将其与给定的key拼接起来作为secret_key的值
    secret_key = f"{key}_{keygen.create_random_key(length=8)}"
    # 创建一个URL对象，目标URL为传入的url对象的target_url属性，key为生成的key，secret_key为生成的secret_key
    db_url = models.URL(target_url=url.target_url, key=key, secret_key=secret_key)
    # 将db_url对象添加到数据库中
    db.add(db_url)
    # 提交数据库的更改
    db.commit()
    # 刷新db_url对象，使其包含最新的数据库更改
    db.refresh(db_url)

    # 返回db_url对象
    return db_url


def get_db_url_by_key(db: Session, url_key: str) -> models.URL:
    """
    通过传入的url_key获取URL对象
    :param db: 数据库会话对象
    :param url_key: 传入的url_key
    :return: 获取到的URL对象
    """
    # 通过传入的url_key获取URL对象
    db_url = (
        db.query(models.URL)
        .filter(models.URL.key == url_key, models.URL.is_active)
        .first()
    )
    # 返回db_url对象
    return db_url


def get_db_url_by_secret_key(db: Session, secret_key: str) -> models.URL:
    """
    通过传入的secret_key获取URL对象
    :param db: 数据库会话对象
    :param secret_key: 传入的secret_key
    :return: 获取到的URL对象
    """
    # 通过传入的secret_key获取URL对象
    return (
        db.query(models.URL)
        .filter(models.URL.secret_key == secret_key, models.URL.is_active)
        .first()
    )


def update_db_clicks(db: Session, db_url: schemas.URL) -> models.URL:
    """
    更新URL对象的clicks属性
    :param db: 数据库会话对象
    :param db_url: 传入的URL对象
    :return: 更新后的URL对象
    """
    # 更新URL对象的clicks属性
    db_url.clicks += 1
    # 提交数据库的更改
    db.commit()
    db.refresh(db_url)
    return db_url
