import pytest
from shortener_app.schemas import *


def test_URLBase():
    url_base = URLBase(target_url="https://www.example.com")
    assert url_base.target_url == "https://www.example.com"

def test_URL():
    url = URL(target_url="https://www.example.com", is_active=True, clicks=10)
    assert url.target_url == "https://www.example.com"
    assert url.is_active == True
    assert url.clicks == 10

def test_URLInfo():
    url_info = URLInfo(target_url="https://www.example.com", is_active=True, clicks=10, url="JYPOP", admin_url="LZPMUVSQ")
    assert url_info.url == "JYPOP"
    assert url_info.admin_url == "LZPMUVSQ"
