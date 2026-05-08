"""数据库工具类"""

import oracledb
import pandas as pd
from config.db_config import STEELWORKS_DB


class DBHelper:
    """数据库连接助手"""
    
    def __init__(self, config=None):
        self.config = config or STEELWORKS_DB
        self._connection = None
    
    def connect(self):
        """建立连接"""
        self._connection = oracledb.connect(**self.config)
        return self._connection
    
    def close(self):
        """关闭连接"""
        if self._connection:
            self._connection.close()
            self._connection = None
    
    def query_to_df(self, sql):
        """执行查询返回 DataFrame"""
        if not self._connection:
            self.connect()
        return pd.read_sql(sql, self._connection)
    
    def __enter__(self):
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False
