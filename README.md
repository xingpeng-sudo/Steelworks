# Steelworks 数据验证测试项目

炼钢厂数据准确性测试项目，使用 pytest + Oracle 进行数据验证。

## 目录结构

```
steelworks_data_validation/
├── conftest.py              # pytest 全局配置
├── pytest.ini               # pytest 配置
├── requirements.txt         # 依赖清单
├── run_report.bat           # 一键生成报告脚本
├── config/                  # 配置目录
│   └── db_config.py         # 数据库配置
├── utils/                   # 工具模块
│   ├── db_helper.py         # 数据库连接工具
│   └── sql_loader.py        # SQL 文件加载器
├── sql/                     # SQL 文件目录
│   ├── common/              # 通用 SQL
│   │   └── check_table_exists.sql
│   └── rtd_mts_lg1/         # 业务模块 SQL
│       └── select_column.sql
├── tests/                   # 测试目录
│   ├── test_rtd_mts_lg1/    # 业务模块测试
│   │   └── test_pointbof1no1.py
│   └── test_common/         # 通用测试
│       └── test_connection.py
└── reports/                 # 测试报告
    └── allure-results/      # Allure 报告数据
```

## 安装依赖

```bash
pip install -r requirements.txt
```

## 运行测试

```bash
# 运行所有测试
pytest

# 只跑冒烟测试
pytest -m smoke

# 只跑数据验证
pytest -m data_validation

# 显示打印输出
pytest -v -s
```

## 生成测试报告

### 方式一：使用脚本（推荐）

双击 `run_report.bat`，自动运行测试并打开 Allure 报告。

### 方式二：命令行

```bash
# 运行测试并生成 Allure 数据
pytest

# 启动报告服务（浏览器自动打开）
allure serve reports/allure-results
```

### 方式三：生成静态报告

```bash
# 生成 HTML 报告到指定目录
allure generate reports/allure-results -o reports/allure-report --clean

# 用浏览器打开 reports/allure-report/index.html
```

## 配置说明

- 数据库连接信息在 `config/db_config.py` 中配置
- SQL 语句统一放在 `sql/` 目录下，通过 `utils/sql_loader.py` 加载
