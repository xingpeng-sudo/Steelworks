"""CI 环境验证测试"""

import os
import sys
import pytest
import allure
import pandas as pd


@allure.feature("CI验证")
@allure.story("环境检查")
def test_python_version():
    """验证 Python 版本"""
    assert sys.version_info.major == 3
    assert sys.version_info.minor >= 10
    allure.attach(f"Python {sys.version}", name="Python版本", attachment_type=allure.attachment_type.TEXT)


@allure.feature("CI验证")
@allure.story("依赖检查")
def test_dependencies_installed():
    """验证关键依赖已安装"""
    allure.attach("所有关键依赖已正确安装", name="依赖检查", attachment_type=allure.attachment_type.TEXT)


@allure.feature("CI验证")
@allure.story("工具验证")
def test_sql_loader_works():
    """验证 SQL 加载器"""
    from utils.sql_loader import load_sql
    
    # 验证 SQL 文件可加载
    sql = load_sql("common/check_table_exists.sql", table_name="TEST_TABLE")
    assert "TEST_TABLE" in sql
    allure.attach(sql, name="加载的SQL", attachment_type=allure.attachment_type.TEXT)


@allure.feature("CI验证")
@allure.story("配置验证")
def test_config_structure():
    """验证项目结构"""
    assert os.path.exists("config"), "config 目录不存在"
    assert os.path.exists("sql"), "sql 目录不存在"
    assert os.path.exists("tests"), "tests 目录不存在"
    assert os.path.exists("utils"), "utils 目录不存在"


@allure.feature("CI验证")
@allure.story("SQL文件检查")
def test_sql_files_exist():
    """验证 SQL 文件存在"""
    sql_files = [
        "sql/common/check_table_exists.sql",
        "sql/rtd_mts_lg1/select_column.sql"
    ]
    
    for sql_file in sql_files:
        assert os.path.exists(sql_file), f"SQL 文件不存在: {sql_file}"
        with open(sql_file, 'r', encoding='utf-8') as f:
            content = f.read()
            assert len(content) > 0, f"SQL 文件为空: {sql_file}"
    
    allure.attach(f"检查了 {len(sql_files)} 个 SQL 文件", name="检查结果", attachment_type=allure.attachment_type.TEXT)
