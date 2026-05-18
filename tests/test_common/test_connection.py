"""数据库连接测试"""

import pytest
import allure
from utils.db_helper import DBHelper
from utils.sql_loader import load_sql


@allure.feature("基础设施")
@allure.story("数据库连接")
@pytest.mark.smoke
@pytest.mark.connection
@pytest.mark.skip_ci
def test_db_connection():
    """测试数据库连接"""
    with allure.step("建立连接并执行查询"):
        db = DBHelper()
        db.connect()
        df = db.query_to_df("SELECT 1 as test FROM DUAL")
        db.close()
    
    assert df.iloc[0, 0] == 1, "数据库连接失败"


@allure.feature("基础设施")
@allure.story("数据库连接")
@pytest.mark.connection
@pytest.mark.skip_ci
def test_table_accessible(db):
    """测试目标表可访问"""
    with allure.step("检查表是否存在"):
        sql = load_sql("common/check_table_exists.sql", table_name="RTD_MTS_LG1_POINTBOF1NO1")
        df = db.query_to_df(sql)
    
    assert not df.empty, "无法访问目标表"
