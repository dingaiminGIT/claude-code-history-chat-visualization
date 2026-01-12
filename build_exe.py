#!/usr/bin/env python3
"""
构建可执行文件的脚本
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def install_pyinstaller():
    """安装PyInstaller"""
    try:
        import PyInstaller
        print("✅ PyInstaller已安装")
        return True
    except ImportError:
        print("📦 安装PyInstaller...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
            print("✅ PyInstaller安装成功")
            return True
        except subprocess.CalledProcessError:
            print("❌ PyInstaller安装失败")
            return False

def build_executable():
    """构建可执行文件"""
    system = platform.system()

    # 构建命令
    cmd = [
        "pyinstaller",
        "--onefile",                    # 打包为单个文件
        "--name=claude-code-viz",       # 可执行文件名称
        "--add-data=templates:templates",  # 包含模板文件
        "--add-data=*.md:.",            # 包含说明文档
        "app.py"                        # 主程序文件
    ]

    # Windows特定选项
    if system == "Windows":
        cmd.append("--windowed")        # 隐藏控制台窗口

    print(f"🔨 开始构建 {system} 可执行文件...")
    print(f"命令: {' '.join(cmd)}")

    try:
        subprocess.check_call(cmd)
        print("✅ 构建成功!")

        # 显示输出文件位置
        dist_dir = Path("dist")
        if system == "Windows":
            exe_file = dist_dir / "claude-code-viz.exe"
        else:
            exe_file = dist_dir / "claude-code-viz"

        if exe_file.exists():
            print(f"📁 可执行文件位置: {exe_file}")
            print(f"📏 文件大小: {exe_file.stat().st_size / 1024 / 1024:.1f} MB")

        return True

    except subprocess.CalledProcessError as e:
        print(f"❌ 构建失败: {e}")
        return False

def create_distribution_package():
    """创建分发包"""
    print("\n📦 创建分发包...")

    # 创建分发目录
    dist_name = f"claude-code-viz-{platform.system().lower()}"
    dist_path = Path(dist_name)

    if dist_path.exists():
        import shutil
        shutil.rmtree(dist_path)

    dist_path.mkdir()

    # 复制文件
    import shutil

    # 复制可执行文件
    system = platform.system()
    if system == "Windows":
        exe_name = "claude-code-viz.exe"
    else:
        exe_name = "claude-code-viz"

    exe_source = Path("dist") / exe_name
    if exe_source.exists():
        shutil.copy2(exe_source, dist_path / exe_name)
        print(f"✅ 复制可执行文件: {exe_name}")

    # 复制说明文档
    docs = ["README.md", "USER_GUIDE.md", "USAGE_GUIDE.md"]
    for doc in docs:
        if Path(doc).exists():
            shutil.copy2(doc, dist_path / doc)
            print(f"✅ 复制文档: {doc}")

    print(f"📁 分发包创建完成: {dist_path}")
    return dist_path

def main():
    """主函数"""
    print("🏗️  Claude Code 可视化工具 - 构建脚本")
    print("=" * 50)

    # 检查并安装PyInstaller
    if not install_pyinstaller():
        return False

    # 构建可执行文件
    if not build_executable():
        return False

    # 创建分发包
    dist_path = create_distribution_package()

    print("\n🎉 构建完成!")
    print(f"\n📋 分发包位置: {dist_path}")
    print("\n💡 接下来可以:")
    print("   1. 测试可执行文件是否正常运行")
    print("   2. 压缩分发包并上传到GitHub")
    print("   3. 编写发布说明")

    return True

if __name__ == "__main__":
    main()