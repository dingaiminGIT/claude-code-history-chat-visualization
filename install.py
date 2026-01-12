#!/usr/bin/env python3
"""
Claude Code 可视化工具 - 一键安装脚本
适用于 Windows、macOS、Linux
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def check_python_version():
    """检查Python版本"""
    if sys.version_info < (3, 7):
        print("❌ 需要Python 3.7或更高版本")
        print(f"   当前版本: {sys.version}")
        return False
    print(f"✅ Python版本检查通过: {sys.version.split()[0]}")
    return True

def check_claude_directory():
    """检查Claude Code是否已安装"""
    claude_dir = Path.home() / ".claude"
    if not claude_dir.exists():
        print("❌ 未找到Claude Code配置目录")
        print("   请先安装并使用Claude Code，然后重新运行此脚本")
        return False

    history_file = claude_dir / "history.jsonl"
    if not history_file.exists():
        print("⚠️  Claude配置目录存在，但没有对话记录")
        print("   请先使用Claude Code进行一些对话，然后重新运行")
        return False

    print(f"✅ 找到Claude Code配置目录: {claude_dir}")
    return True

def install_dependencies():
    """安装Python依赖"""
    print("\n📦 安装依赖包...")

    try:
        # 检查是否有pip
        subprocess.run([sys.executable, "-m", "pip", "--version"],
                      check=True, capture_output=True)
        print("✅ pip可用")
    except subprocess.CalledProcessError:
        print("❌ pip不可用，请安装pip")
        return False

    # 安装依赖
    requirements = [
        "Flask==2.3.3",
        "Jinja2==3.1.2",
        "python-dateutil==2.8.2",
        "markdown==3.5.1"
    ]

    for req in requirements:
        try:
            print(f"   安装 {req}...")
            subprocess.run([sys.executable, "-m", "pip", "install", req],
                          check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            print(f"❌ 安装 {req} 失败")
            print(f"   错误: {e}")
            return False

    print("✅ 所有依赖安装完成")
    return True

def create_launcher():
    """创建启动脚本"""
    print("\n🚀 创建启动脚本...")

    current_dir = Path(__file__).parent
    system = platform.system()

    if system == "Windows":
        # Windows批处理文件
        launcher_content = f'''@echo off
echo 启动 Claude Code 可视化工具...
cd /d "{current_dir}"
python app.py
pause
'''
        launcher_path = current_dir / "启动工具.bat"
        with open(launcher_path, 'w', encoding='utf-8') as f:
            f.write(launcher_content)
        print(f"✅ 创建Windows启动脚本: {launcher_path}")

    else:
        # macOS/Linux shell脚本
        launcher_content = f'''#!/bin/bash
echo "启动 Claude Code 可视化工具..."
cd "{current_dir}"
python3 app.py
'''
        launcher_path = current_dir / "启动工具.sh"
        with open(launcher_path, 'w', encoding='utf-8') as f:
            f.write(launcher_content)

        # 添加执行权限
        os.chmod(launcher_path, 0o755)
        print(f"✅ 创建启动脚本: {launcher_path}")

    return launcher_path

def create_desktop_shortcut(launcher_path):
    """创建桌面快捷方式（可选）"""
    system = platform.system()

    if system == "Windows":
        # Windows快捷方式需要额外的库，这里提供说明
        print("\n💡 Windows用户可以:")
        print(f"   右键 {launcher_path} -> 发送到 -> 桌面快捷方式")

    elif system == "Darwin":  # macOS
        print("\n💡 macOS用户可以:")
        print(f"   将 {launcher_path} 拖拽到应用程序文件夹或Dock")

    else:  # Linux
        desktop_dir = Path.home() / "Desktop"
        if desktop_dir.exists():
            print(f"\n💡 Linux用户可以:")
            print(f"   复制 {launcher_path} 到桌面: cp {launcher_path} {desktop_dir}/")

def main():
    """主安装流程"""
    print("🔧 Claude Code 可视化工具 - 安装向导")
    print("=" * 50)

    # 1. 检查Python版本
    if not check_python_version():
        return False

    # 2. 检查Claude Code
    if not check_claude_directory():
        return False

    # 3. 安装依赖
    if not install_dependencies():
        return False

    # 4. 创建启动脚本
    launcher_path = create_launcher()

    # 5. 创建快捷方式提示
    create_desktop_shortcut(launcher_path)

    print("\n🎉 安装完成!")
    print("\n📖 使用说明:")
    print(f"   1. 双击运行: {launcher_path}")
    print("   2. 打开浏览器访问: http://localhost:5000")
    print("   3. 开始浏览您的Claude Code对话记录")

    print("\n⚠️  注意事项:")
    print("   - 请确保Claude Code正在使用中以获取最新对话")
    print("   - 工具运行时请保持终端窗口打开")
    print("   - 按Ctrl+C可以停止工具")

    return True

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            input("\n按回车键退出...")
            sys.exit(1)
        else:
            input("\n按回车键退出...")
    except KeyboardInterrupt:
        print("\n\n安装被用户取消")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 安装过程中出现错误: {e}")
        input("按回车键退出...")
        sys.exit(1)