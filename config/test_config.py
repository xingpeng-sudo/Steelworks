"""测试数据配置

将测试数据范围从硬编码改为配置化，便于维护和调整。
支持从环境变量或配置文件读取。
"""

import os


# ==================== RTD_MTS_LG1 模块配置 ====================

class PointBOF1No1Config:
    """转炉温度数据验证配置"""

    # 表名和列名
    TABLE_NAME = os.getenv("TEST_TABLE_NAME", "RTD_MTS_LG1_POINTBOF1NO1")
    COLUMN_NAME = os.getenv("TEST_COLUMN_NAME", "LUHOU_WENDU")

    # 数据范围（从环境变量读取，支持动态配置）
    # 格式：最小值-最大值，如 "22220-22229"
    @property
    def min_value(self) -> float:
        return float(os.getenv("TEST_MIN_VALUE", "22220"))

    @property
    def max_value(self) -> float:
        return float(os.getenv("TEST_MAX_VALUE", "22229"))

    def validate_range(self, value: float) -> bool:
        """验证值是否在范围内"""
        return self.min_value <= value <= self.max_value


# 全局配置实例
pointbof1no1_config = PointBOF1No1Config()
