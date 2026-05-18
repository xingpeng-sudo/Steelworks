# 基础镜像：Python 3.12 slim 版
FROM python:3.12-slim

# 设置工作目录
WORKDIR /app

# 安装 Oracle 客户端依赖（oracledb 需要）
RUN apt-get update && \
    apt-get install -y --no-install-recommends libaio1t64 && \
    ln -s /usr/lib/x86_64-linux-gnu/libaio.so.1t64 /usr/lib/x86_64-linux-gnu/libaio.so.1 && \
    rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装 Python 依赖（用清华镜像加速）
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 复制项目代码
COPY . .

# 默认运行 pytest
CMD ["pytest", "-v", "--alluredir=allure-results"]