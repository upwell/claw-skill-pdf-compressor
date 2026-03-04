#!/bin/bash

# 退出如果发生任何错误
set -e

# 定位当前脚本目录
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

# 清理旧的构建产物
echo "🧹 Cleaning up old builds..."
rm -rf build/ dist/ *.egg-info .pytest_cache __pycache__ src/__pycache__ pdf_compressor_skill.zip

# 同步依赖并生成 lock 文件
echo "🔒 Running uv lock to ensure dependencies are resolved..."
uv lock

# 创建发布压缩包
echo "📦 Creating release package (pdf_compressor_skill.zip)..."
zip -r pdf_compressor_skill.zip \
    SKILL.md \
    pyproject.toml \
    uv.lock \
    README.md \
    src/ \
    -x "*/__pycache__/*" "*/.DS_Store" "*/.pytest_cache/*"

echo "✅ Build completed successfully!"
echo "📄 The package 'pdf_compressor_skill.zip' is ready to be published or uploaded to OpenClaw."
