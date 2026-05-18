"""SQL 文件加载工具"""

from pathlib import Path

SQL_DIR = Path(__file__).parent.parent / "sql"


def load_sql(filename: str, **params) -> str:
    """
    加载 SQL 文件并替换参数
    
    Args:
        filename: SQL 文件相对路径（相对于 sql 目录）
        **params: SQL 中的占位符参数
    
    Returns:
        格式化后的 SQL 语句
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
    
    # 替换参数
    if params:
        sql = sql.format(**params)
    
    return sql
