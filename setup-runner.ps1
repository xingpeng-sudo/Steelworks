# Self-Hosted Runner 安装脚本
# 运行前请确保：
# 1. 此机器能访问内网数据库 192.168.1.121
# 2. 已安装 Python 3.12
# 3. 已从 GitHub 获取了 token

param(
    [Parameter(Mandatory=$true)]
    [string]$Token
)

$RunnerVersion = "2.311.0"
$RunnerUrl = "https://github.com/actions/runner/releases/download/v$RunnerVersion/actions-runner-win-x64-$RunnerVersion.zip"

Write-Host "=== GitHub Actions Self-Hosted Runner 安装 ===" -ForegroundColor Green
Write-Host ""

# 创建目录
$RunnerDir = "$env:USERPROFILE\actions-runner"
if (-not (Test-Path $RunnerDir)) {
    New-Item -ItemType Directory -Path $RunnerDir | Out-Null
}

Set-Location $RunnerDir

# 下载 runner
Write-Host "[1/4] 下载 runner..." -ForegroundColor Yellow
if (-not (Test-Path "actions-runner-win-x64-$RunnerVersion.zip")) {
    Invoke-WebRequest -Uri $RunnerUrl -OutFile "actions-runner-win-x64-$RunnerVersion.zip"
    Write-Host "下载完成" -ForegroundColor Green
} else {
    Write-Host "文件已存在，跳过下载" -ForegroundColor Gray
}

# 解压
Write-Host "[2/4] 解压..." -ForegroundColor Yellow
if (-not (Test-Path "config.cmd")) {
    Expand-Archive -Path "actions-runner-win-x64-$RunnerVersion.zip" -DestinationPath . -Force
    Write-Host "解压完成" -ForegroundColor Green
} else {
    Write-Host "已解压，跳过" -ForegroundColor Gray
}

# 配置
Write-Host "[3/4] 配置 runner..." -ForegroundColor Yellow
Write-Host "Token: $Token" -ForegroundColor Gray

$ConfigArgs = @(
    "--url", "https://github.com/xingpeng-sudo/Steelworks",
    "--token", $Token,
    "--name", "steelworks-runner",
    "--labels", "self-hosted,steelworks",
    "--work", "_work"
)

& .\config.cmd @ConfigArgs

if ($LASTEXITCODE -ne 0) {
    Write-Host "配置失败！请检查 token 是否正确" -ForegroundColor Red
    exit 1
}

Write-Host "配置完成" -ForegroundColor Green

# 安装为服务（可选，推荐）
Write-Host "[4/4] 安装为 Windows 服务..." -ForegroundColor Yellow
$InstallService = Read-Host "是否安装为 Windows 服务？(y/n)"
if ($InstallService -eq "y") {
    & .\svc.cmd install
    & .\svc.cmd start
    Write-Host "服务已安装并启动" -ForegroundColor Green
    Write-Host ""
    Write-Host "查看服务状态: services.msc -> GitHub Actions Runner" -ForegroundColor Cyan
} else {
    Write-Host "跳过服务安装" -ForegroundColor Gray
    Write-Host ""
    Write-Host "手动启动命令: .\run.cmd" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "=== 安装完成 ===" -ForegroundColor Green
Write-Host ""
Write-Host "Runner 名称: steelworks-runner" -ForegroundColor White
Write-Host "标签: self-hosted, steelworks" -ForegroundColor White
Write-Host ""
Write-Host "在 GitHub 上查看: https://github.com/xingpeng-sudo/Steelworks/settings/actions/runners" -ForegroundColor Cyan
