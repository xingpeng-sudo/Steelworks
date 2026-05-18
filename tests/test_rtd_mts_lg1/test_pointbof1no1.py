"""转炉温度数据验证测试"""

import os
import pytest
import allure
from utils.sql_loader import load_sql

# 确保报告目录存在
os.makedirs("reports", exist_ok=True)

# CI 环境跳过
pytestmark = pytest.mark.skip_ci

# 测试配置
TABLE_NAME = "RTD_MTS_LG1_POINTBOF1NO1"
COLUMN_NAME = "LUHOU_WENDU"
MIN_VALUE = 22220
MAX_VALUE = 22229


@pytest.fixture(scope="module")
def df_data(db):
    """加载测试数据"""
    with allure.step("加载数据"):
        sql = load_sql("rtd_mts_lg1/select_column.sql", column_name=COLUMN_NAME, table_name=TABLE_NAME)
        df = db.query_to_df(sql)
        allure.attach(f"共 {len(df)} 条记录", name="数据量", attachment_type=allure.attachment_type.TEXT)
        return df


# ========== 基础检查 ==========

@allure.feature("数据验证")
@allure.story("基础检查")
@pytest.mark.smoke
@pytest.mark.data_validation
def test_table_has_data(df_data):
    """表中有数据"""
    assert not df_data.empty, f"表 {TABLE_NAME} 无数据"


# ========== 范围检查 ==========

@allure.feature("数据验证")
@allure.story("范围检查")
@pytest.mark.data_validation
def test_value_range_min(df_data):
    """最小值在范围内"""
    actual_min = df_data[COLUMN_NAME].min()
    assert actual_min >= MIN_VALUE, f"最小值 {actual_min} < {MIN_VALUE}"


@allure.feature("数据验证")
@allure.story("范围检查")
@pytest.mark.data_validation
def test_value_range_max(df_data):
    """最大值在范围内"""
    actual_max = df_data[COLUMN_NAME].max()
    assert actual_max <= MAX_VALUE, f"最大值 {actual_max} > {MAX_VALUE}"


@allure.feature("数据验证")
@allure.story("范围检查")
@pytest.mark.data_validation
def test_all_values_in_range(df_data):
    """所有值都在范围内"""
    out_of_range = df_data[(df_data[COLUMN_NAME] < MIN_VALUE) | (df_data[COLUMN_NAME] > MAX_VALUE)]
    
    if not out_of_range.empty:
        out_of_range.to_csv("reports/out_of_range.csv", index=False)
        allure.attach.file("reports/out_of_range.csv", name="异常数据", attachment_type=allure.attachment_type.CSV)
    
    assert out_of_range.empty, f"发现 {len(out_of_range)} 条异常数据"


# ========== 统计信息 ==========

@allure.feature("数据验证")
@allure.story("统计信息")
@pytest.mark.data_validation
def test_statistics(df_data):
    """输出统计信息"""
    stats = f"""总记录数: {len(df_data)}
最小值: {df_data[COLUMN_NAME].min()}
最大值: {df_data[COLUMN_NAME].max()}
平均值: {df_data[COLUMN_NAME].mean():.2f}
中位数: {df_data[COLUMN_NAME].median()}
标准差: {df_data[COLUMN_NAME].std():.2f}"""
    
    allure.attach(stats, name="统计数据", attachment_type=allure.attachment_type.TEXT)
