"""数据库连接测试

测试目标：验证数据库连接和基础访问能力
业务场景：所有数据测试的前置条件
"""

import pytest
import allure
from utils.db_helper import DBHelper
from utils.sql_loader import load_sql


@allure.feature("基础设施")
@allure.story("数据库连接")
@allure.severity(allure.severity_level.BLOCKER)
@pytest.mark.smoke
@pytest.mark.connection
@pytest.mark.skip_ci
def test_db_connection():
    """测试数据库能否正常连接
    
    验证目标：确保数据库连接可用
    前置条件：数据库服务已启动
    预期结果：能成功执行简单查询
    影响范围：此测试失败将阻塞所有数据测试
    """
    with allure.step("建立数据库连接"):
        db = DBHelper()
        db.connect()
        
    with allure.step("执行测试查询"):
        df = db.query_to_df("SELECT 1 as test FROM DUAL")
        allure.attach(
            f"查询结果: {df.iloc[0, 0]}",
            name="连接测试结果",
            attachment_type=allure.attachment_type.TEXT
        )
        
    with allure.step("关闭连接"):
        db.close()
        
    with allure.step("断言：查询结果正确"):
        assert df.iloc[0, 0] == 1, "数据库连接测试失败"


@allure.feature("基础设施")
@allure.story("数据库连接")
@allure.severity(allure.severity_level.BLOCKER)
@pytest.mark.connection
@pytest.mark.skip_ci
def test_steelworks_schema_accessible(db):
    """测试能访问 steelworks 用户的表
    
    验证目标：确保有权限访问目标表
    前置条件：数据库连接正常
    预期结果：能查询目标表结构
    影响范围：此测试失败将阻塞后续数据验证测试
    """
    with allure.step("检查目标表是否存在"):
        sql = load_sql(
            "common/check_table_exists.sql",
            table_name="RTD_MTS_LG1_POINTBOF1NO1"
        )
        allure.attach(sql, name="执行的SQL", attachment_type=allure.attachment_type.TEXT)
        
        df = db.query_to_df(sql)
        
    with allure.step("断言：表可访问"):
        assert not df.empty, "无法访问目标表"
        
    with allure.step("记录结果"):
        allure.attach(
            "✅ 目标表可正常访问",
            name="访问权限检查",
            attachment_type=allure.attachment_type.TEXT
        )
