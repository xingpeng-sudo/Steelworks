"""pytest 全局配置和共享 fixture"""

import pytest
import allure
from utils.db_helper import DBHelper


@pytest.fixture(scope="session")
def db():
    """全局数据库连接 fixture"""
    with allure.step("建立数据库连接"):
        helper = DBHelper()
        helper.connect()
        allure.attach(
            "Oracle 数据库连接已建立",
            name="连接状态",
            attachment_type=allure.attachment_type.TEXT
        )
        yield helper
    
    with allure.step("关闭数据库连接"):
        helper.close()
        allure.attach(
            "数据库连接已关闭",
            name="连接状态",
            attachment_type=allure.attachment_type.TEXT
        )


@pytest.fixture(scope="session")
def db_connection(db):
    """兼容旧代码的 connection fixture"""
    yield db._connection
