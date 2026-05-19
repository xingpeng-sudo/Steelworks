"""SQL 文件加载工具"""

import re
from pathlib import Path

SQL_DIR = Path(__file__).parent.parent / "sql"

# 允许的参数名模式（只允许字母、数字、下划线）
VALID_PARAM_PATTERN = re.compile(r'^[a-zA-Z_][a-zA-Z0-9_]*$')


def _validate_param_name(name: str) -> bool:
    """验证参数名是否合法（防止注入）"""
    return bool(VALID_PARAM_PATTERN.match(name))


def _validate_param_value(value) -> bool:
    """验证参数值是否安全"""
    if isinstance(value, str):
        # 只允许字母、数字、下划线、点号（用于表名、列名等标识符）
        # 不允许特殊字符如 ; ' " -- /* 等SQL注入字符
        dangerous_chars = [';', "'", '"', '--', '/*', '*/', '\x00']
        for char in dangerous_chars:
            if char in value:
                return False
    return True


def load_sql(filename: str, **params) -> str:
    """
    加载 SQL 文件并替换参数

    Args:
        filename: SQL 文件相对路径（相对于 sql 目录）
        **params: SQL 中的占位符参数（仅支持标识符替换，如表名、列名）

    Returns:
        格式化后的 SQL 语句

    Raises:
        FileNotFoundError: SQL 文件不存在
        ValueError: 参数名或参数值不合法
    """
    sql_path = SQL_DIR / filename

    if not sql_path.exists():
        raise FileNotFoundError(f"SQL 文件不存在: {sql_path}")

    with open(sql_path, "r", encoding="utf-8") as f:
        sql = f.read()

    # 移除注释行
    lines = [line for line in sql.split("\n")
             if line.strip() and not line.strip().startswith("--")]
    sql = "\n".join(lines)

    # 安全地替换参数
    if params:
        validated_params = {}
        for key, value in params.items():
            # 验证参数名
            if not _validate_param_name(key):
                raise ValueError(f"非法参数名: {key}")
            # 验证参数值
            if not _validate_param_value(value):
                raise ValueError(f"参数值包含危险字符: {key}={value}")
            validated_params[key] = value

        sql = sql.format(**validated_params)

    return sql
