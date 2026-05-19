# Steelworks 数据验证测试项目

炼钢厂数据准确性测试项目，使用 pytest + Oracle 进行数据验证。
#测试
## 目录结构

```
Steelworks/
├── conftest.py              # pytest 全局配置
├── pytest.ini               # pytest 配置
├── requirements.txt         # 依赖清单
├── Dockerfile               # Docker 镜像定义
├── main.py                  # 入口文件
├── run_report.bat           # 一键生成报告脚本
│
├── config/                  # 配置目录
│   └── db_config.py         # 数据库配置
│
├── utils/                   # 工具模块
│   ├── db_helper.py         # 数据库连接工具
│   └── sql_loader.py        # SQL 文件加载器
│
├── sql/                     # SQL 文件目录
│   ├── common/              # 通用 SQL
│   │   └── check_table_exists.sql
│   └── rtd_mts_lg1/         # 业务模块 SQL
│       └── select_column.sql
│
├── tests/                   # 测试目录
│   ├── test_common/         # 通用测试
│   │   ├── test_connection.py      # 数据库连接测试
│   │   └── test_ci_validation.py   # CI 环境验证测试
│   └── test_rtd_mts_lg1/    # 业务模块测试
│       └── test_pointbof1no1.py    # 转炉温度数据验证
│
├── reports/                 # 测试报告
│   └── allure-results/      # Allure 报告数据
│
├── docs/                    # 文档目录
│   └── 代码整理报告.md
│
└── .github/                 # GitHub 配置
    └── workflows/           # CI/CD 工作流
        ├── ci.yml              # Self-Hosted Runner CI
        ├── ci-self-hosted.yml  # Self-Hosted 备用
        ├── ci-docker.yml       # Docker CI
        └── ci-lite.yml         # 简化版 CI
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

# 只跑连接测试
pytest -m connection

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
# 生成 HTML 报告
allure generate reports/allure-results -o reports/allure-report --clean

# 用浏览器打开 reports/allure-report/index.html
```

## 配置说明

- 数据库连接信息在 `config/db_config.py` 中配置
- SQL 语句统一放在 `sql/` 目录下，通过 `utils/sql_loader.py` 加载
- 支持环境变量配置：`DB_USER`、`DB_PASSWORD`、`DB_HOST`、`DB_PORT`、`DB_SERVICE`

## Docker 支持

```bash
# 构建镜像
docker build -t steelworks .

# 运行测试
docker run --rm steelworks
```

## CI/CD

项目支持多种 CI 模式：

| CI 配置 | 运行环境 | 说明 |
|:---|:---|:---|
| ci.yml | Self-Hosted Runner | 本地 Windows 机器，可连内网数据库 |
| ci-docker.yml | GitHub Cloud + Docker | 云端容器化运行 |
| ci-lite.yml | GitHub Cloud | 简化版，只做代码检查 |

## 测试用例

| 测试文件 | 测试数 | 说明 |
|:---|:---|:---|
| test_connection.py | 2 | 数据库连接测试 |
| test_ci_validation.py | 5 | CI 环境验证测试 |
| test_pointbof1no1.py | 5 | 转炉温度数据验证 |
