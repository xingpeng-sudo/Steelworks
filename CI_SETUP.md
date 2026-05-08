# CI/CD 配置指南

## 已配置功能

✅ **GitHub Actions 工作流** (`.github/workflows/ci.yml`)
- 代码质量检查 (flake8, black, isort)
- 自动化测试执行
- 覆盖率报告生成
- Allure 报告自动生成并部署到 GitHub Pages

## 首次配置步骤

### 1. 配置数据库 Secrets（必须）

进入 GitHub 仓库 → Settings → Secrets and variables → Actions → New repository secret

添加以下 Secrets：

| Secret Name | 说明 | 示例值 |
|:---|:---|:---|
| `DB_USER` | 数据库用户名 | `steelworks` |
| `DB_PASSWORD` | 数据库密码 | `your_password` |
| `DB_DSN` | 数据库连接串 | `192.168.1.121:1521/ORCLPDB` |

### 2. 启用 GitHub Pages

Settings → Pages → Source → 选择 `gh-pages` 分支

### 3. 本地配置

```bash
# 复制 CI 配置模板
cp config/db_config.py.ci config/db_config.py

# 编辑 db_config.py，填入实际的数据库信息
# 确保 db_config.py 不会被提交（已在 .gitignore 中）
```

## CI 触发条件

| 触发方式 | 说明 |
|:---|:---|
| Push 到 main/master/develop | 自动触发完整 CI |
| 提交 Pull Request | 自动触发完整 CI |
| 手动触发 | Actions 页面 → 选择 workflow → Run workflow |

## CI 流程说明

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Push/PR   │ →  │  Code Lint  │ →  │  Run Tests  │ →  │   Report    │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
                          │                  │                  │
                    flake8/black          pytest           Allure
                    代码格式检查         冒烟+全量测试      报告部署
```

## 报告查看

| 报告类型 | 查看地址 |
|:---|:---|
| Allure 报告 | `https://xingpeng-sudo.github.io/Steelworks/` |
| 覆盖率报告 | CI Artifacts 中下载 |
| 测试日志 | GitHub Actions 日志 |

## 本地模拟 CI 环境

```bash
# 安装 CI 依赖
pip install flake8 black isort pytest-cov

# 代码格式检查
black --check .
flake8 .

# 运行测试（带覆盖率）
pytest --cov=utils --cov=tests --cov-report=html

# 生成 Allure 报告
pytest --alluredir=reports/allure-results
allure serve reports/allure-results
```

## 常见问题

### Q: CI 中数据库连接失败？
A: 检查 Secrets 是否正确配置，数据库网络是否允许 GitHub Actions 访问

### Q: 某些测试在 CI 中不需要运行？
A: 添加 `@pytest.mark.skip_ci` 标记，在 CI 中跳过

### Q: 如何只运行冒烟测试？
A: CI 默认会运行冒烟测试，如需调整修改 `.github/workflows/ci.yml`

## 进阶配置

### 添加定时触发

在 `ci.yml` 的 `on:` 部分添加：

```yaml
schedule:
  # 每天凌晨 2 点运行
  - cron: '0 2 * * *'
```

### 多环境测试

添加多个 job，分别测试不同环境：

```yaml
test-dev:
  environment: development
  
test-prod:
  environment: production
  needs: test-dev
```
