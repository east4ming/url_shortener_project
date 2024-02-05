# test_config.py
import pytest
from shortener_app.config import *

# 创建一个测试用例
class TestGetSettings:
    # 测试 get_settings 函数返回的是否是 Settings 类的实例
    def test_get_settings_returns_settings_instance(self):
        settings = get_settings()
        assert isinstance(settings, BaseSettings), "get_settings should return an instance of BaseSettings"

    # 测试 get_settings 函数是否正确设置了 env_name 属性
    def test_get_settings_env_name(self):
        settings = get_settings()
        assert settings.env_name is not None, "env_name should not be None"
        # 如果 env_name 是一个字符串，确保它不是空字符串
        assert isinstance(settings.env_name, str) and settings.env_name, "env_name should be a non-empty string"

# 如果需要，可以添加更多的测试用例
