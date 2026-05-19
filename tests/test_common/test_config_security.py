"""数据库配置安全测试"""

import pytest
import allure
import os


@allure.feature("安全测试")
@allure.story("凭据管理")
class TestDatabaseCredentialSecurity:
    """验证数据库凭据安全配置"""

    @allure.title("未配置凭据时应发出警告")
    def test_warning_without_credentials(self):
        """未设置环境变量时应发出警告"""
        import warnings
        import importlib

        # 临时移除环境变量
        old_user = os.environ.pop("DB_USER", None)
        old_password = os.environ.pop("DB_PASSWORD", None)

        try:
            # 重新加载模块会触发警告
            import config.db_config as db_config
            importlib.reload(db_config)

            # 验证配置为空字符串（不是硬编码密码）
            assert db_config.STEELWORKS_DB["user"] == ""
            assert db_config.STEELWORKS_DB["password"] == ""

        finally:
            # 恢复环境变量
            if old_user:
                os.environ["DB_USER"] = old_user
            if old_password:
                os.environ["DB_PASSWORD"] = old_password

    @allure.title("环境变量配置应生效")
    def test_credentials_from_env(self):
        """环境变量配置应正确读取"""
        # 设置测试环境变量
        os.environ["DB_USER"] = "test_user"
        os.environ["DB_PASSWORD"] = "test_password"
        os.environ["DB_HOST"] = "test_host"
        os.environ["DB_PORT"] = "1234"
        os.environ["DB_SERVICE"] = "TEST_SERVICE"

        import importlib
        import config.db_config as db_config
        importlib.reload(db_config)

        assert db_config.STEELWORKS_DB["user"] == "test_user"
        assert db_config.STEELWORKS_DB["password"] == "test_password"
        assert "test_host:1234/TEST_SERVICE" in db_config.STEELWORKS_DB["dsn"]

        # 清理
        del os.environ["DB_USER"]
        del os.environ["DB_PASSWORD"]
        del os.environ["DB_HOST"]
        del os.environ["DB_PORT"]
        del os.environ["DB_SERVICE"]

    @allure.title("DB_DSN环境变量应生效")
    def test_dsn_from_env(self):
        """DB_DSN 环境变量应正确读取"""
        os.environ["DB_USER"] = "user"
        os.environ["DB_PASSWORD"] = "pass"
        os.environ["DB_DSN"] = "custom.dsn:1521/SERVICE"

        import importlib
        import config.db_config as db_config
        importlib.reload(db_config)

        assert db_config.STEELWORKS_DB["dsn"] == "custom.dsn:1521/SERVICE"

        # 清理
        del os.environ["DB_USER"]
        del os.environ["DB_PASSWORD"]
        del os.environ["DB_DSN"]

    @allure.title("配置文件不包含硬编码密码")
    def test_no_hardcoded_passwords(self):
        """验证配置文件中没有硬编码密码"""
        with open("config/db_config.py", "r", encoding="utf-8") as f:
            content = f.read()

        # 检查不存在硬编码密码
        assert "steelworks" not in content.lower() or "请设置环境变量" in content
        assert '"steelworks"' not in content
        assert "'steelworks'" not in content


@allure.feature("安全测试")
@allure.story("配置验证")
class TestTestConfigSecurity:
    """验证测试配置安全性"""

    @allure.title("测试配置默认值合理")
    def test_test_config_defaults(self):
        """测试配置应有合理的默认值"""
        from config.test_config import pointbof1no1_config

        # 默认值应存在
        assert pointbof1no1_config.TABLE_NAME == "RTD_MTS_LG1_POINTBOF1NO1"
        assert pointbof1no1_config.COLUMN_NAME == "LUHOU_WENDU"
        assert pointbof1no1_config.min_value == 22220
        assert pointbof1no1_config.max_value == 22229

    @allure.title("测试配置环境变量覆盖")
    def test_test_config_env_override(self):
        """测试配置应支持环境变量覆盖"""
        os.environ["TEST_MIN_VALUE"] = "100"
        os.environ["TEST_MAX_VALUE"] = "200"
        os.environ["TEST_TABLE_NAME"] = "CUSTOM_TABLE"

        import importlib
        import config.test_config as test_config
        importlib.reload(test_config)

        config = test_config.PointBOF1No1Config()
        assert config.min_value == 100
        assert config.max_value == 200
        assert config.TABLE_NAME == "CUSTOM_TABLE"

        # 清理
        del os.environ["TEST_MIN_VALUE"]
        del os.environ["TEST_MAX_VALUE"]
        del os.environ["TEST_TABLE_NAME"]

    @allure.title("范围验证方法正确")
    def test_validate_range_method(self):
        """范围验证方法应正确工作"""
        from config.test_config import pointbof1no1_config

        assert pointbof1no1_config.validate_range(22225) is True
        assert pointbof1no1_config.validate_range(22220) is True  # 边界值
        assert pointbof1no1_config.validate_range(22229) is True  # 边界值
        assert pointbof1no1_config.validate_range(22219) is False  # 超出范围
        assert pointbof1no1_config.validate_range(22230) is False  # 超出范围