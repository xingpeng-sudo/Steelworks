# CI 验证检查清单

## 如何确认 CI 真正跑通了

不要只看绿色 ✅，要检查每个环节的**实际输出**。

---

## 1. 检查 Workflow 运行状态

访问: https://github.com/xingpeng-sudo/Steelworks/actions

### 应该看到 3 个 Workflow

| Workflow | 触发条件 | 预期结果 |
|----------|----------|----------|
| `Steelworks CI (Self-Hosted)` | push 到 main | 在 `菠萝清香` 上运行 |
| `Steelworks CI` | push 到 main | 在 `菠萝清香` 上运行 (ci.yml) |
| `Steelworks CI` | push 到 main | 在 Ubuntu 上运行 (ci-lite.yml) |

---

## 2. 验证 Self-Hosted Runner 真正运行

### 检查点 A: Runner 在线
```
Settings → Actions → Runners
应该看到: 菠萝清香 (Online)
```

### 检查点 B: 工作目录有代码
在你的机器上检查：
```powershell
Get-ChildItem 'D:\github-actions-runner\actions-runner\_work\Steelworks\Steelworks'
# 应该能看到最新的代码文件
```

### 检查点 C: 测试真的运行了
在 GitHub Actions 日志中查找：
```
Run python -m pytest --cov=utils --cov=tests ...
============================= test session starts ==============================
...
PASSED / FAILED / ERROR  (实际测试结果)
```

---

## 3. 验证数据库连接真正成功

### 在 Actions 日志中查找：

```
Checking database connectivity...
DSN: ***
Host: 192.168.1.121, Port: 1521
Database is reachable
```

### 如果看到：
- `WARNING: Cannot connect to database` → 连接失败 ❌
- `Database is reachable` → 连接成功 ✅

---

## 4. 验证 Allure 报告真正生成

### 检查点 A: allure-results 目录有内容
在 Actions 日志中查找：
```
Check downloaded files:
Reports directory:
    allure-results
        *.json 文件
```

### 检查点 B: Allure 命令执行成功
```
Using Allure: D:\allure-2.24.1\bin\allure.bat
Allure exists: True
Found allure-results, generating report...
Report successfully generated to allure-report
```

### 检查点 C: 报告文件真的存在
```powershell
# 在你的机器上检查
Get-ChildItem 'D:\github-actions-runner\actions-runner\_work\Steelworks\Steelworks\allure-history'
# 应该能看到 index.html 和其他文件
```

---

## 5. 验证 GitHub Pages 真正部署

### 检查点 A: gh-pages 分支有内容
```
https://github.com/xingpeng-sudo/Steelworks/tree/gh-pages
应该能看到生成的报告文件
```

### 检查点 B: 网站可以访问
```
https://xingpeng-sudo.github.io/Steelworks/
应该能看到 Allure 报告页面
```

---

## 6. 验证测试真的跑了（不是跳过的）

### 在 pytest 输出中查找：

```
# 好的输出（真的跑了测试）：
tests/test_common/test_connection.py::test_db_connection PASSED [ 50%]
tests/test_common/test_ci_validation.py::test_imports PASSED [ 100%]

# 坏的输出（测试被跳过）：
tests/test_common/test_connection.py::test_db_connection SKIPPED [ 50%]
```

### 检查覆盖率报告：
```
Coverage report:
Name                    Stmts   Miss  Cover
-------------------------------------------
utils/db_helper.py       50     10    80%
```

---

## 7. 验证 Secrets 真正注入

### 检查 db_config.py 内容
在 Actions 日志中查找（或者添加调试步骤）：
```powershell
Get-Content config/db_config.py
# 应该看到：
# "user": os.getenv("DB_USER", ""),
# 而不是空的
```

---

## 8. 完整的验证命令

你可以手动在本地验证：

```powershell
# 1. 进入工作目录
cd 'D:\github-actions-runner\actions-runner\_work\Steelworks\Steelworks'

# 2. 检查代码是否最新
git log --oneline -1

# 3. 检查测试是否能跑
python -m pytest tests/test_common/test_ci_validation.py -v

# 4. 检查数据库连接
python -c "from utils.db_helper import DBHelper; print('Import OK')"

# 5. 检查 Allure 是否可用
D:\allure-2.24.1\bin\allure.bat --version

# 6. 检查报告目录
Get-ChildItem reports\allure-results -ErrorAction SilentlyContinue
```

---

## 9. 常见"假成功"陷阱

| 现象 | 实际含义 | 如何验证 |
|------|----------|----------|
| ✅ CI 全绿 | 可能只是 `continue-on-error: true` | 检查每个步骤的实际输出 |
| ✅ Tests passed | 可能只是跳过了所有测试 | 检查 `pytest -v` 输出 |
| ✅ Report generated | 可能只是空目录 | 检查 `allure-results/*.json` |
| ✅ Deployed to Pages | 可能只是部署了旧版本 | 访问网站查看最新内容 |

---

## 10. 终极验证：手动触发一次

```powershell
# 在你的机器上手动执行 CI 步骤
cd 'D:\Steelworks\项目代码\Steelworks'

# 步骤 1: 安装依赖
pip install -r requirements.txt

# 步骤 2: 运行测试
python -m pytest --alluredir=reports\allure-results -v

# 步骤 3: 生成 Allure 报告
D:\allure-2.24.1\bin\allure.bat generate reports\allure-results -o allure-report --clean

# 步骤 4: 检查结果
Start-Process allure-report\index.html
```

如果本地能跑通，CI 应该也能跑通。

---

## 快速检查清单

- [ ] Runner 状态 Online
- [ ] CI 日志显示实际测试运行（不是跳过）
- [ ] 数据库连接显示 "reachable"
- [ ] allure-results 目录有 .json 文件
- [ ] Allure 报告生成成功
- [ ] gh-pages 分支有更新
- [ ] https://xingpeng-sudo.github.io/Steelworks/ 能访问

全部勾选 ✅ 才算真正跑通！
