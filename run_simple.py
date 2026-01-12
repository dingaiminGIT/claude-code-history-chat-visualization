#!/usr/bin/env python3
"""
Claude Code 可视化工具 - 简化启动脚本
无需虚拟环境，直接运行
"""

import sys
import os
import subprocess
from pathlib import Path

def check_and_install_dependencies():
    """检查并安装必要的依赖"""
    required_packages = {
        'flask': 'Flask==2.3.3',
        'jinja2': 'Jinja2==3.1.2',
        'dateutil': 'python-dateutil==2.8.2'
    }

    missing_packages = []

    # 检查已安装的包
    for package, pip_name in required_packages.items():
        try:
            __import__(package)
            print(f"✅ {package} 已安装")
        except ImportError:
            missing_packages.append(pip_name)
            print(f"❌ {package} 未安装")

    # 如果有缺失的包，提供解决方案
    if missing_packages:
        print(f"\n📦 检测到 {len(missing_packages)} 个缺失的依赖包")
        print("\n🔧 推荐的解决方案:")
        print("   方案1: 使用虚拟环境（推荐）")
        print("     python3 -m venv venv")
        print("     source venv/bin/activate")
        print("     pip install -r requirements.txt")
        print("     python app.py")
        print("")
        print("   方案2: 使用现有虚拟环境")
        print("     source venv/bin/activate")
        print("     python app.py")
        print("")
        print("   方案3: 系统级安装（不推荐）")
        print("     pip install --user Flask Jinja2 python-dateutil")

        # 尝试自动使用虚拟环境
        venv_path = Path("venv")
        if venv_path.exists():
            print(f"\n✅ 发现虚拟环境: {venv_path}")
            print("   建议运行: source venv/bin/activate && python app.py")

        return False

    return True

def check_claude_data():
    """检查Claude数据是否存在"""
    claude_dir = Path.home() / ".claude"

    if not claude_dir.exists():
        print("❌ 未找到Claude Code配置目录")
        print("   请先安装并使用Claude Code")
        return False

    history_file = claude_dir / "history.jsonl"
    if not history_file.exists():
        print("⚠️  Claude配置目录存在，但没有对话记录")
        print("   请先使用Claude Code进行一些对话")
        return False

    print(f"✅ 找到Claude数据目录: {claude_dir}")
    return True

def start_app():
    """启动应用"""
    print("\n🚀 启动Claude Code可视化工具...")
    print("   访问地址: http://localhost:5000")
    print("   按 Ctrl+C 停止服务")
    print("-" * 50)

    try:
        # 导入并运行Flask应用
        from app import app
        app.run(debug=False, host='0.0.0.0', port=5000)
    except ImportError:
        print("❌ 无法导入应用，请检查app.py文件是否存在")
        return False
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        return False

    return True

def main():
    """主函数"""
    print("🎯 Claude Code 可视化工具")
    print("=" * 40)

    # 1. 检查Claude数据
    if not check_claude_data():
        input("\n按回车键退出...")
        return

    # 2. 检查并安装依赖
    if not check_and_install_dependencies():
        print("❌ 依赖安装失败")
        input("\n按回车键退出...")
        return

    # 3. 启动应用
    try:
        start_app()
    except KeyboardInterrupt:
        print("\n\n👋 应用已停止")
    except Exception as e:
        print(f"\n❌ 运行错误: {e}")

    input("\n按回车键退出...")

if __name__ == "__main__":
    main()