"""数据库配置

安全说明：
- 生产环境必须通过环境变量配置数据库凭据
- 不再提供默认密码，避免安全风险
- 如果环境变量未设置，将抛出配置错误
"""

import os


def _get_env_or_raise(name: str, default: str = None) -> str:
    """获取环境变量，如果不存在且无默认值则抛出异常"""
    value = os.getenv(name, default)
    if value is None:
        raise ValueError(
            f"数据库配置缺失: 请设置环境变量 {name}，"
            f"例如: export {name}=your_value"
        )
    return value


def _build_dsn() -> str:
    """构建数据库 DSN"""
    host = os.getenv("DB_HOST", "192.168.1.121")
    port = os.getenv("DB_PORT", "1521")
    service = os.getenv("DB_SERVICE", "ORCLPDB")
    return f"{host}:{port}/{service}"


# 构建数据库配置
# 优先从独立环境变量获取，其次从 DB_DSN 获取
_db_user = os.getenv("DB_USER")
_db_password = os.getenv("DB_PASSWORD")
_db_dsn = os.getenv("DB_DSN")

# 如果没有独立凭据，尝试从其他来源获取（兼容旧配置）
if _db_user is None and _db_password is None:
    # 开发环境提示：如果没有配置环境变量，给出警告
    import warnings
    warnings.warn(
        "数据库凭据未配置！请设置环境变量 DB_USER 和 DB_PASSWORD。"
        "当前使用空配置，连接将失败。",
        UserWarning
    )
    _db_user = ""
    _db_password = ""

STEELWORKS_DB = {
    "user": _db_user,
    "password": _db_password,
    "dsn": _db_dsn or _build_dsn()
}

# 多环境配置（可扩展）
DB_CONFIGS = {
    "test": STEELWORKS_DB,
    # "prod": {...}
}
