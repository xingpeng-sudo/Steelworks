@echo off
echo ========================================
echo Steelworks 测试报告生成脚本
echo ========================================
echo.

echo [1/2] 运行测试并生成 Allure 数据...
pytest

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [警告] 测试执行有失败，但继续生成报告...
)

echo.
echo [2/2] 启动 Allure 报告服务...
echo 报告将在浏览器中自动打开
echo 按 Ctrl+C 可停止服务
echo.

allure serve reports/allure-results
