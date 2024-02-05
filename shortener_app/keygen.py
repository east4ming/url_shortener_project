import secrets
import string

from sqlalchemy.orm import Session

from . import crud


def create_random_key(length: int = 5) -> str:
    """
    Creates a random key of a given length.
    """
    chars = string.ascii_uppercase + string.digits
    return "".join(secrets.choice(chars) for _ in range(length))


def create_unique_key(db: Session) -> str:
    """
    Creates a unique key.
    """
    while True:
        key = create_random_key()
        if not crud.get_db_url_by_key(db, key):
            return key
