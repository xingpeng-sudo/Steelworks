"""Pytest 配置文件

定义共享的 fixtures
"""

import pytest
import allure
from utils.db_helper import DBHelper


@pytest.fixture(scope="session")
def db():
    """数据库连接 fixture
    
    提供数据库连接，所有测试共享一个连接
    """
    with allure.step("初始化数据库连接"):
        helper = DBHelper()
        helper.connect()
        
    yield helper
    
    with allure.step("关闭数据库连接"):
        helper.close()
