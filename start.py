#!/usr/bin/env python3
"""
Claude Code 可视化工具启动脚本
"""

import subprocess
import sys
import os
from pathlib import Path

def check_dependencies():
    """检查依赖"""
    print("检查依赖...")

    # 检查 Python 版本
    if sys.version_info < (3, 7):
        print("❌ 需要 Python 3.7 或更高版本")
        return False

    print(f"✅ Python 版本: {sys.version}")

    # 检查 Claude 目录
    claude_dir = os.path.expanduser("~/.claude")
    if not os.path.exists(claude_dir):
        print("⚠️  警告: 未找到 Claude 配置目录 ~/.claude")
        print("   请确保已安装并使用过 Claude Code")
        return False

    print(f"✅ Claude 配置目录: {claude_dir}")

    # 检查历史文件
    history_file = os.path.join(claude_dir, "history.jsonl")
    if os.path.exists(history_file):
        with open(history_file, 'r') as f:
            lines = len(f.readlines())
        print(f"✅ 找到历史记录: {lines} 条对话")
    else:
        print("⚠️  警告: 未找到历史记录文件")

    return True

def install_dependencies():
    """安装 Python 依赖"""
    print("安装 Python 依赖...")

    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ 依赖安装完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 依赖安装失败: {e}")
        return False

def start_server():
    """启动服务器"""
    print("\n" + "="*50)
    print("🚀 启动 Claude Code 可视化工具")
    print("="*50)

    try:
        from app import app
        print("\n📱 访问地址:")
        print("   http://localhost:5000")
        print("\n💡 功能:")
        print("   - 查看对话历史")
        print("   - 搜索对话内容")
        print("   - 统计信息展示")
        print("\n🛑 按 Ctrl+C 停止服务")
        print("-"*50)

        app.run(debug=False, host='0.0.0.0', port=5000)

    except ImportError as e:
        print(f"❌ 导入错误: {e}")
        print("请先安装依赖: pip install -r requirements.txt")
        return False
    except KeyboardInterrupt:
        print("\n\n👋 服务已停止")
        return True
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        return False

def main():
    """主函数"""
    print("Claude Code 可视化工具")
    print("="*30)

    # 检查依赖
    if not check_dependencies():
        print("\n❌ 环境检查失败")
        return

    # 检查是否需要安装依赖
    try:
        import flask
        print("✅ Flask 已安装")
    except ImportError:
        if not install_dependencies():
            return

    # 启动服务器
    start_server()

if __name__ == "__main__":
    main()