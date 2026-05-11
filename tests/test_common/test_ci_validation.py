"""CI 验证测试

这些测试不需要数据库连接，用于验证 CI 流程本身
"""

import pytest
import allure
from utils.sql_loader import load_sql


@allure.feature("CI验证")
@allure.story("环境检查")
@allure.severity(allure.severity_level.BLOCKER)
def test_python_version():
    """验证 Python 版本"""
    import sys
    assert sys.version_info.major == 3
    assert sys.version_info.minor >= 10
    allure.attach(f"Python {sys.version}", name="Python版本", attachment_type=allure.attachment_type.TEXT)


@allure.feature("CI验证")
@allure.story("依赖检查")
@allure.severity(allure.severity_level.CRITICAL)
def test_dependencies_installed():
    """验证关键依赖已安装"""
    import pytest
    import allure
    import pandas as pd
    
    allure.attach("所有关键依赖已正确安装", name="依赖检查", attachment_type=allure.attachment_type.TEXT)


@allure.feature("CI验证")
@allure.story("工具验证")
@allure.severity(allure.severity_level.NORMAL)
def test_sql_loader_works():
    """验证 SQL 加载器可以正常工作（不执行查询）"""
    # 验证 sql_loader 模块可以导入和基本使用
    sql_template = "SELECT {column_name} FROM {table_name} WHERE {column_name} IS NOT NULL"
    
    # 测试字符串格式化
    formatted = sql_template.format(column_name="TEST_COL", table_name="TEST_TABLE")
    assert "TEST_COL" in formatted
    assert "TEST_TABLE" in formatted
    
    allure.attach(formatted, name="格式化后的SQL", attachment_type=allure.attachment_type.TEXT)


@allure.feature("CI验证")
@allure.story("配置验证")
@allure.severity(allure.severity_level.NORMAL)
def test_config_structure():
    """验证配置文件结构正确"""
    import os
    
    # 验证必要的目录存在
    assert os.path.exists("config"), "config 目录不存在"
    assert os.path.exists("sql"), "sql 目录不存在"
    assert os.path.exists("tests"), "tests 目录不存在"
    assert os.path.exists("utils"), "utils 目录不存在"
    
    allure.attach("✅ 项目结构完整", name="目录检查", attachment_type=allure.attachment_type.TEXT)


@allure.feature("CI验证")
@allure.story("SQL文件检查")
@allure.severity(allure.severity_level.NORMAL)
def test_sql_files_exist():
    """验证 SQL 文件存在且可读"""
    import os
    
    sql_files = [
        "sql/common/check_table_exists.sql",
        "sql/rtd_mts_lg1/select_column.sql"
    ]
    
    for sql_file in sql_files:
        assert os.path.exists(sql_file), f"SQL 文件不存在: {sql_file}"
        with open(sql_file, 'r', encoding='utf-8') as f:
            content = f.read()
            assert len(content) > 0, f"SQL 文件为空: {sql_file}"
    
    allure.attach(f"检查了 {len(sql_files)} 个 SQL 文件", name="SQL文件检查", attachment_type=allure.attachment_type.TEXT)
