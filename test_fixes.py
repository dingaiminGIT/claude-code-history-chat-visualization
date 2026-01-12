#!/usr/bin/env python3
"""
测试修复效果的脚本
"""

import urllib.request
import json

def test_api():
    """测试API功能"""
    base_url = "http://localhost:5000"

    print("🔍 测试API功能...")

    # 测试统计API
    try:
        with urllib.request.urlopen(f"{base_url}/api/stats") as response:
            if response.status == 200:
                stats = json.loads(response.read().decode())
                print(f"✅ 统计API正常: {stats['total_conversations']}条对话, {len(stats['projects'])}个项目")
            else:
                print(f"❌ 统计API失败: {response.status}")
    except Exception as e:
        print(f"❌ 统计API错误: {e}")

    # 测试对话详情API
    try:
        # 获取一个有效的会话ID
        from claude_parser import ClaudeDataParser
        parser = ClaudeDataParser()
        conversations = parser.parse_full_conversations()

        if conversations:
            session_id = conversations[0].get('sessionId')
            if session_id:
                with urllib.request.urlopen(f"{base_url}/api/conversation/{session_id}") as response:
                    if response.status == 200:
                        data = json.loads(response.read().decode())
                        has_full = data.get('has_full_content', False)
                        print(f"✅ 对话详情API正常: 会话 {session_id[:8]}..., 完整内容: {has_full}")

                        if has_full and data['conversation'].get('full_conversation'):
                            messages = data['conversation']['full_conversation']
                            print(f"   📝 包含 {len(messages)} 条消息")

                            # 检查消息格式
                            for i, msg in enumerate(messages[:2]):
                                content_preview = msg['content'][:50] + '...' if len(msg['content']) > 50 else msg['content']
                                print(f"   {i+1}. [{msg['type']}] {content_preview}")

                    else:
                        print(f"❌ 对话详情API失败: {response.status}")
            else:
                print("⚠️  没有找到有效的会话ID")
        else:
            print("⚠️  没有找到对话记录")

    except Exception as e:
        print(f"❌ 对话详情API错误: {e}")

def test_content_formatting():
    """测试内容格式化"""
    print("\n🎨 测试内容格式化...")

    from claude_parser import ClaudeDataParser
    parser = ClaudeDataParser()

    conversations = parser.parse_full_conversations()

    if conversations:
        conv = conversations[0]
        if conv.get('has_full_content') and conv.get('full_conversation'):
            messages = conv['full_conversation']

            print(f"✅ 找到完整对话: {len(messages)} 条消息")

            for i, msg in enumerate(messages[:3]):
                print(f"\n消息 {i+1} [{msg['type']}]:")
                content = msg['content']

                # 检查是否有换行符
                if '\\n' in content:
                    print("   ✅ 包含换行符，需要格式化")
                    formatted = content.replace('\\n', '<br>')
                    print(f"   📄 格式化预览: {formatted[:100]}...")
                else:
                    print("   ℹ️  内容较短，无需特殊格式化")
                    print(f"   📄 内容预览: {content[:100]}...")
        else:
            print("❌ 没有找到完整对话内容")
    else:
        print("❌ 没有找到对话记录")

if __name__ == "__main__":
    print("🧪 Claude Code 可视化工具 - 修复测试")
    print("=" * 50)

    test_api()
    test_content_formatting()

    print("\n🎉 测试完成!")
    print("\n💡 现在您可以:")
    print("   1. 访问 http://localhost:5000 查看修复后的界面")
    print("   2. 点击眼睛按钮查看完整对话（不再是调试日志）")
    print("   3. Claude回复内容现在有换行格式化")
    print("   4. 可以在模态框中复制完整对话")