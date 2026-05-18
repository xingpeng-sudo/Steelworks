"""pytest 全局配置"""

import pytest
import allure
from utils.db_helper import DBHelper


@pytest.fixture(scope="session")
def db():
    """全局数据库连接"""
    with allure.step("建立数据库连接"):
        helper = DBHelper()
        helper.connect()
        yield helper
    
    with allure.step("关闭数据库连接"):
        helper.close()


@pytest.fixture(scope="session")
def db_connection(db):
    """兼容旧代码"""
    yield db._connection
