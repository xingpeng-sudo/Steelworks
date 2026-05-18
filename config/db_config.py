"""数据库配置"""

import os

STEELWORKS_DB = {
    "user": os.getenv("DB_USER", "steelworks"),
    "password": os.getenv("DB_PASSWORD", "steelworks"),
    "dsn": f"{os.getenv('DB_HOST', '192.168.1.121')}:{os.getenv('DB_PORT', '1521')}/{os.getenv('DB_SERVICE', 'ORCLPDB')}"
}

# 多环境配置（可扩展）
DB_CONFIGS = {
    "test": STEELWORKS_DB,
    # "prod": {...}
}
