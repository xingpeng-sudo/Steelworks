"""SQL 加载器安全测试"""

import pytest
import allure
from utils.sql_loader import load_sql, _validate_param_name, _validate_param_value


@allure.feature("安全测试")
@allure.story("SQL注入防护")
class TestSQLInjectionProtection:
    """验证 SQL 注入防护功能"""

    # ========== 参数名验证测试 ==========

    @allure.title("合法参数名应通过验证")
    def test_valid_param_names(self):
        """合法参数名：字母、数字、下划线"""
        assert _validate_param_name("table_name") is True
        assert _validate_param_name("column_name") is True
        assert _validate_param_name("TABLE_NAME") is True
        assert _validate_param_name("_private") is True
        assert _validate_param_name("name123") is True

    @allure.title("非法参数名应被拒绝")
    def test_invalid_param_names(self):
        """非法参数名：包含特殊字符"""
        assert _validate_param_name("table;name") is False
        assert _validate_param_name("column-name") is False
        assert _validate_param_name("name.drop") is False
        assert _validate_param_name("123name") is False  # 数字开头
        assert _validate_param_name("") is False  # 空字符串

    # ========== 参数值验证测试 ==========

    @allure.title("合法参数值应通过验证")
    def test_valid_param_values(self):
        """合法参数值：表名、列名等标识符"""
        assert _validate_param_value("TABLE_NAME") is True
        assert _validate_param_value("column_name") is True
        assert _validate_param_value("RTD_MTS_LG1") is True
        assert _validate_param_value(123) is True  # 数字类型

    @allure.title("SQL注入字符应被拒绝")
    def test_dangerous_param_values(self):
        """危险字符：SQL注入常用字符"""
        # 分号
        assert _validate_param_value("TABLE;DROP") is False
        # 单引号
        assert _validate_param_value("TABLE'OR'1'='1") is False
        # 双引号
        assert _validate_param_value("TABLE\"OR\"1\"=\"1") is False
        # SQL注释
        assert _validate_param_value("TABLE--comment") is False
        assert _validate_param_value("TABLE/*comment*/") is False
        # 空字节
        assert _validate_param_value("TABLE\x00DROP") is False

    # ========== load_sql 安全测试 ==========

    @allure.title("合法SQL加载应成功")
    def test_load_sql_valid_params(self):
        """合法参数应成功加载SQL"""
        sql = load_sql("common/check_table_exists.sql", table_name="TEST_TABLE")
        assert "TEST_TABLE" in sql
        assert "SELECT" in sql.upper()

    @allure.title("非法参数名应抛出异常")
    def test_load_sql_invalid_param_name(self):
        """非法参数名应抛出 ValueError"""
        with pytest.raises(ValueError, match="非法参数名"):
            load_sql("common/check_table_exists.sql", **{"table;name": "TEST"})

    @allure.title("危险参数值应抛出异常")
    def test_load_sql_dangerous_param_value(self):
        """包含注入字符的参数值应抛出 ValueError"""
        with pytest.raises(ValueError, match="危险字符"):
            load_sql("common/check_table_exists.sql", table_name="TABLE;DROP TABLE users;--")

    @allure.title("SQL注入攻击应被阻止")
    @pytest.mark.parametrize("attack_payload", [
        "users; DROP TABLE users;--",
        "users' OR '1'='1",
        "users\" OR \"1\"=\"1",
        "users/* comment */",
        "users--",
    ])
    def test_sql_injection_attacks_blocked(self, attack_payload):
        """常见SQL注入攻击应被阻止"""
        with pytest.raises(ValueError):
            load_sql("common/check_table_exists.sql", table_name=attack_payload)


@allure.feature("安全测试")
@allure.story("功能验证")
class TestSQLLoaderFunctionality:
    """验证原有功能保持不变"""

    @allure.title("SQL文件加载功能正常")
    def test_load_sql_basic(self):
        """基本SQL加载功能"""
        sql = load_sql("common/check_table_exists.sql", table_name="RTD_MTS_LG1_POINTBOF1NO1")
        assert "RTD_MTS_LG1_POINTBOF1NO1" in sql
        assert "SELECT" in sql
        assert "user_tables" in sql.lower()

    @allure.title("SQL注释移除功能正常")
    def test_sql_comment_removal(self):
        """注释行应被移除"""
        sql = load_sql("common/check_table_exists.sql", table_name="TEST")
        # 检查没有注释行
        lines = sql.split("\n")
        for line in lines:
            if line.strip():
                assert not line.strip().startswith("--")

    @allure.title("不存在的文件应抛出异常")
    def test_load_sql_file_not_found(self):
        """不存在的SQL文件应抛出 FileNotFoundError"""
        with pytest.raises(FileNotFoundError):
            load_sql("nonexistent/file.sql")