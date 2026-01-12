#!/bin/bash
# Claude Code 可视化工具安装脚本

echo "🚀 Claude Code 可视化工具安装"
echo "================================"

# 检查 Python 版本
python3 --version || {
    echo "❌ 需要安装 Python 3.7+"
    exit 1
}

# 创建虚拟环境
echo "📦 创建虚拟环境..."
python3 -m venv venv

# 激活虚拟环境
echo "🔧 激活虚拟环境..."
source venv/bin/activate

# 安装依赖
echo "⬇️  安装依赖..."
pip install -r requirements.txt

echo "✅ 安装完成！"
echo ""
echo "🎯 使用方法："
echo "1. 激活虚拟环境: source venv/bin/activate"
echo "2. 启动工具: python app.py"
echo "3. 访问: http://localhost:5000"
echo ""
echo "或者运行: ./run.sh"