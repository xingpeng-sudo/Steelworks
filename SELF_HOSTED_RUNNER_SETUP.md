# Self-Hosted Runner 安装指南

## 概述

此指南帮助你在能访问内网数据库的机器上安装 GitHub Actions Self-Hosted Runner，让 CI 能真正运行数据库测试。

## 前提条件

- Windows 10/11 或 Windows Server 机器
- 能访问内网数据库 `192.168.1.121:1521`
- Python 3.12 已安装
- 机器能连接互联网（访问 GitHub）
- 建议机器能长期开机

## 安装步骤

### 步骤 1：从 GitHub 获取 Token

1. 打开 https://github.com/xingpeng-sudo/Steelworks/settings/actions/runners
2. 点击 **"New self-hosted runner"**
3. 选择 **Windows** 和 **x64**
4. 复制页面上的 token（格式类似：`ABCD1234EFGH5678IJ...`）

### 步骤 2：运行安装脚本

**方式 A：使用 PowerShell 脚本（推荐）**

```powershell
# 打开 PowerShell（管理员权限）
cd D:\Steelworks\项目代码\Steelworks

# 运行安装脚本
.\setup-runner.ps1 -Token "你的token"
```

**方式 B：手动安装**

```powershell
# 1. 创建目录
mkdir $env:USERPROFILE\actions-runner; cd $env:USERPROFILE\actions-runner

# 2. 下载 runner（版本 2.311.0）
Invoke-WebRequest -Uri https://github.com/actions/runner/releases/download/v2.311.0/actions-runner-win-x64-2.311.0.zip -OutFile actions-runner-win-x64-2.311.0.zip

# 3. 解压
Add-Type -AssemblyName System.IO.Compression.FileSystem
[System.IO.Compression.ZipFile]::ExtractToDirectory("$PWD\actions-runner-win-x64-2.311.0.zip", "$PWD")

# 4. 配置（替换 YOUR_TOKEN）
.\config.cmd --url https://github.com/xingpeng-sudo/Steelworks --token YOUR_TOKEN --name steelworks-runner --labels self-hosted,steelworks --work _work

# 5. 运行（前台模式，用于测试）
.\run.cmd
```

### 步骤 3：安装为 Windows 服务（推荐）

```powershell
cd $env:USERPROFILE\actions-runner

# 安装服务
.\svc.cmd install

# 启动服务
.\svc.cmd start

# 查看状态
.\svc.cmd status
```

### 步骤 4：验证 Runner 状态

1. 打开 https://github.com/xingpeng-sudo/Steelworks/settings/actions/runners
2. 应该看到 `steelworks-runner` 显示为 **Online**（绿色）

## 配置 CI 使用 Self-Hosted Runner

安装完成后，CI 会自动使用 self-hosted runner。工作流文件已配置：

```yaml
runs-on: self-hosted
```

## 测试 Runner

推送代码到 main 分支，触发 CI：

```bash
git push origin main
```

然后在 GitHub Actions 页面查看运行状态：
https://github.com/xingpeng-sudo/Steelworks/actions

## 常见问题

### Q: Runner 显示 Offline？
A: 检查机器是否开机，服务是否运行：
```powershell
.\svc.cmd status
```

### Q: 如何更新 Runner？
A: 停止服务，重新下载最新版本，替换文件：
```powershell
.\svc.cmd stop
# 下载新版本并解压
.\svc.cmd start
```

### Q: 如何卸载 Runner？
A: 
```powershell
.\svc.cmd stop
.\svc.cmd uninstall
.\config.cmd remove --token YOUR_TOKEN
```

### Q: 如何查看 Runner 日志？
A: 日志位于 `_work\_diag\` 目录下

## 安全注意事项

1. **Token 保密**：不要泄露配置 token
2. **Secrets 配置**：在 GitHub 仓库中配置数据库 Secrets：
   - `DB_USER`
   - `DB_PASSWORD`
   - `DB_DSN`
3. **访问控制**：确保只有授权用户能访问 runner 机器

## 下一步

1. 在 GitHub 上配置 Secrets（如果还没配置）
2. 推送代码触发 CI
3. 查看 Allure 报告

---

有问题随时问我！
