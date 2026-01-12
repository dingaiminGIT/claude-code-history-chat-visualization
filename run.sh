#!/bin/bash
# Claude Code 可视化工具运行脚本

echo "🚀 启动 Claude Code 可视化工具"
echo "================================"

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "❌ 虚拟环境不存在，请先运行: ./setup.sh"
    exit 1
fi

# 激活虚拟环境
echo "🔧 激活虚拟环境..."
source venv/bin/activate

# 检查 Claude 配置
if [ ! -d "$HOME/.claude" ]; then
    echo "⚠️  警告: 未找到 Claude 配置目录 ~/.claude"
    echo "   请确保已安装并使用过 Claude Code"
fi

# 启动应用
echo "🌐 启动 Web 服务器..."
echo "📱 访问地址: http://localhost:5000"
echo "🛑 按 Ctrl+C 停止服务"
echo "--------------------------------"

python app.py