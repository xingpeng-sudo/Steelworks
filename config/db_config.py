"""数据库配置"""

STEELWORKS_DB = {
    "user": "steelworks",
    "password": "steelworks",
    "dsn": "192.168.1.121:1521/ORCLPDB"
}

# 可以扩展多个环境
DB_CONFIGS = {
    "test": STEELWORKS_DB,
    # "prod": {...}  # 生产环境
}
