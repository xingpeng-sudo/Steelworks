"""RTD_MTS_LG1_POINTBOF1NO1 表数据验证测试

测试目标：验证转炉温度数据的完整性和范围有效性
业务场景：炼钢过程中炉后温度监测

注意：此模块的测试需要连接内网数据库，CI环境默认跳过
"""

import os
import pytest
import allure
import pandas as pd
from utils.sql_loader import load_sql

# 确保reports目录存在
os.makedirs("reports", exist_ok=True)

# 标记整个模块的测试在CI环境中跳过
pytestmark = pytest.mark.skip_ci

# 测试配置
TABLE_NAME = "RTD_MTS_LG1_POINTBOF1NO1"
COLUMN_NAME = "LUHOU_WENDU"
MIN_VALUE = 22220
MAX_VALUE = 22229


@pytest.fixture(scope="module")
def df_data(db):
    """加载测试数据"""
    with allure.step(f"从数据库加载表 {TABLE_NAME} 的数据"):
        sql = load_sql(
            "rtd_mts_lg1/select_column.sql",
            column_name=COLUMN_NAME,
            table_name=TABLE_NAME
        )
        allure.attach(sql, name="执行的SQL语句", attachment_type=allure.attachment_type.TEXT)
        
        df = db.query_to_df(sql)
        
        allure.attach(
            f"加载完成，共 {len(df)} 条记录",
            name="数据加载结果",
            attachment_type=allure.attachment_type.TEXT
        )
        return df


@allure.feature("数据验证")
@allure.story("基础数据检查")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
@pytest.mark.data_validation
def test_table_has_data(df_data):
    """测试：表中有数据
    
    验证目标：确保目标表中有数据记录
    前置条件：数据库连接正常
    预期结果：表不为空，至少有一条记录
    """
    with allure.step("检查数据是否为空"):
        row_count = len(df_data)
        allure.attach(
            f"表名: {TABLE_NAME}\n列名: {COLUMN_NAME}\n记录数: {row_count}",
            name="数据概览",
            attachment_type=allure.attachment_type.TEXT
        )
        
    with allure.step("断言：数据不为空"):
        assert not df_data.empty, f"表 {TABLE_NAME} 无数据"
        
    with allure.step("记录测试结果"):
        allure.attach(
            f"✅ 测试通过 - 表 {TABLE_NAME} 包含 {row_count} 条数据",
            name="测试结论",
            attachment_type=allure.attachment_type.TEXT
        )


@allure.feature("数据验证")
@allure.story("范围检查")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.data_validation
def test_luhou_wendu_range_min(df_data):
    """测试：最小值在范围内
    
    验证目标：确保温度最小值不低于下限
    业务含义：温度过低可能导致工艺异常
    影响范围：最小值异常可能表示存在极端异常数据
    """
    with allure.step(f"计算 {COLUMN_NAME} 列的最小值"):
        actual_min = df_data[COLUMN_NAME].min()
        allure.attach(
            f"实际最小值: {actual_min}\n期望最小值: {MIN_VALUE}",
            name="最小值对比",
            attachment_type=allure.attachment_type.TEXT
        )
        
    with allure.step("断言：最小值 >= 期望下限"):
        assert actual_min >= MIN_VALUE, f"最小值 {actual_min} < {MIN_VALUE}"


@allure.feature("数据验证")
@allure.story("范围检查")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.data_validation
def test_luhou_wendu_range_max(df_data):
    """测试：最大值在范围内
    
    验证目标：确保温度最大值不超过上限
    业务含义：温度过高可能导致设备损坏
    影响范围：最大值异常可能表示存在极端异常数据
    """
    with allure.step(f"计算 {COLUMN_NAME} 列的最大值"):
        actual_max = df_data[COLUMN_NAME].max()
        allure.attach(
            f"实际最大值: {actual_max}\n期望最大值: {MAX_VALUE}",
            name="最大值对比",
            attachment_type=allure.attachment_type.TEXT
        )
        
    with allure.step("断言：最大值 <= 期望上限"):
        assert actual_max <= MAX_VALUE, f"最大值 {actual_max} > {MAX_VALUE}"


@allure.feature("数据验证")
@allure.story("数据质量")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.data_validation
def test_luhou_wendu_all_in_range(df_data):
    """测试：所有值都在范围内
    
    验证目标：确保所有温度数据都在有效范围内
    业务含义：异常数据需要排查原因
    """
    with allure.step("筛选超出范围的数据"):
        out_of_range = df_data[
            (df_data[COLUMN_NAME] < MIN_VALUE) | 
            (df_data[COLUMN_NAME] > MAX_VALUE)
        ]
        
    with allure.step("生成异常数据报告"):
        if not out_of_range.empty:
            # 附加异常数据到报告
            allure.attach(
                out_of_range.to_string(),
                name=f"异常数据详情 ({len(out_of_range)} 条)",
                attachment_type=allure.attachment_type.TEXT
            )
            out_of_range.to_csv("reports/out_of_range.csv", index=False)
            allure.attach.file(
                "reports/out_of_range.csv",
                name="异常数据CSV",
                attachment_type=allure.attachment_type.CSV
            )
        else:
            allure.attach(
                "所有数据都在有效范围内",
                name="数据质量检查",
                attachment_type=allure.attachment_type.TEXT
            )
            
    with allure.step("断言：无异常数据"):
        assert out_of_range.empty, f"发现 {len(out_of_range)} 条异常数据"


@allure.feature("数据验证")
@allure.story("统计分析")
@allure.severity(allure.severity_level.MINOR)
@pytest.mark.data_validation
def test_luhou_wendu_statistics(df_data):
    """测试：输出统计信息
    
    验证目标：展示温度数据的统计概览
    用途：为数据分析提供基础信息
    """
    with allure.step("计算统计数据"):
        stats = {
            "总记录数": len(df_data),
            "最小值": df_data[COLUMN_NAME].min(),
            "最大值": df_data[COLUMN_NAME].max(),
            "平均值": round(df_data[COLUMN_NAME].mean(), 2),
            "中位数": df_data[COLUMN_NAME].median(),
            "标准差": round(df_data[COLUMN_NAME].std(), 2)
        }
        
    with allure.step("附加统计报告"):
        stats_text = "\n".join([f"{k}: {v}" for k, v in stats.items()])
        allure.attach(
            stats_text,
            name="温度数据统计",
            attachment_type=allure.attachment_type.TEXT
        )
        
        # 附加数据分布直方图（文本形式）
        value_counts = df_data[COLUMN_NAME].value_counts().sort_index()
        histogram = "\n".join([f"{val}: {'█' * min(count // 10 + 1, 50)} ({count})" 
                               for val, count in value_counts.items()])
        allure.attach(histogram, name="数据分布", attachment_type=allure.attachment_type.TEXT)
        
    print(f"\n统计: 共{len(df_data)}条, "
          f"范围[{df_data[COLUMN_NAME].min()}, {df_data[COLUMN_NAME].max()}], "
          f"均值{df_data[COLUMN_NAME].mean():.2f}")
