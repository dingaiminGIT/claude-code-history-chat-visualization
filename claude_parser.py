"""
Claude Code 数据解析器
解析 Claude Code 的历史记录和对话数据
"""

import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional


class ClaudeDataParser:
    """Claude Code 数据解析器"""

    def __init__(self, claude_dir: str = None):
        """
        初始化解析器

        Args:
            claude_dir: Claude 配置目录路径，默认为 ~/.claude
        """
        if claude_dir is None:
            claude_dir = os.path.expanduser("~/.claude")

        self.claude_dir = Path(claude_dir)
        self.history_file = self.claude_dir / "history.jsonl"
        self.debug_dir = self.claude_dir / "debug"
        self.projects_dir = self.claude_dir / "projects"

    def parse_history(self) -> List[Dict]:
        """
        解析历史记录文件

        Returns:
            List[Dict]: 历史记录列表
        """
        conversations = []

        if not self.history_file.exists():
            return conversations

        try:
            with open(self.history_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        data = json.loads(line.strip())
                        # 转换时间戳
                        if 'timestamp' in data:
                            data['formatted_time'] = self._format_timestamp(data['timestamp'])
                        conversations.append(data)
        except Exception as e:
            print(f"解析历史记录时出错: {e}")

        # 按时间排序，最新的在前
        conversations.sort(key=lambda x: x.get('timestamp', 0), reverse=True)
        return conversations

    def get_debug_logs(self, session_id: str) -> Optional[str]:
        """
        获取指定会话的调试日志

        Args:
            session_id: 会话ID

        Returns:
            str: 调试日志内容，如果不存在则返回 None
        """
        debug_file = self.debug_dir / f"{session_id}.txt"

        if not debug_file.exists():
            return None

        try:
            with open(debug_file, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"读取调试日志时出错: {e}")
            return None

    def get_conversation_summary(self) -> Dict:
        """
        获取对话统计摘要

        Returns:
            Dict: 包含统计信息的字典
        """
        conversations = self.parse_history()

        if not conversations:
            return {
                'total_conversations': 0,
                'projects': [],
                'date_range': None
            }

        # 统计项目
        projects = list(set(conv.get('project', 'Unknown') for conv in conversations))

        # 时间范围
        timestamps = [conv.get('timestamp', 0) for conv in conversations if conv.get('timestamp')]
        date_range = None
        if timestamps:
            earliest = min(timestamps)
            latest = max(timestamps)
            date_range = {
                'earliest': self._format_timestamp(earliest),
                'latest': self._format_timestamp(latest)
            }

        return {
            'total_conversations': len(conversations),
            'projects': projects,
            'date_range': date_range,
            'sessions': len(set(conv.get('sessionId') for conv in conversations if conv.get('sessionId')))
        }

    def search_conversations(self, query: str, project: str = None) -> List[Dict]:
        """
        搜索对话记录

        Args:
            query: 搜索关键词
            project: 项目路径过滤（可选）

        Returns:
            List[Dict]: 匹配的对话记录
        """
        conversations = self.parse_history()
        results = []

        for conv in conversations:
            # 项目过滤
            if project and conv.get('project') != project:
                continue

            # 关键词搜索
            if query.lower() in conv.get('display', '').lower():
                results.append(conv)

        return results

    def parse_full_conversations(self) -> List[Dict]:
        """
        解析完整对话记录，包含用户问题和Claude回复

        Returns:
            List[Dict]: 包含完整对话的记录列表
        """
        conversations = []

        # 首先获取基础历史记录
        basic_history = self.parse_history()

        # 为每个会话获取完整对话
        for entry in basic_history:
            session_id = entry.get('sessionId')
            project = entry.get('project', '')

            if not session_id:
                continue

            # 获取完整对话内容
            full_conversation = self._get_full_conversation(session_id, project)

            if full_conversation:
                # 合并基础信息和完整对话
                enhanced_entry = {
                    **entry,
                    'full_conversation': full_conversation,
                    'has_full_content': True
                }
                conversations.append(enhanced_entry)
            else:
                # 如果没有找到完整对话，保留原始记录
                entry['has_full_content'] = False
                conversations.append(entry)

        return conversations

    def _get_full_conversation(self, session_id: str, project: str) -> Optional[List[Dict]]:
        """
        获取指定会话的完整对话记录

        Args:
            session_id: 会话ID
            project: 项目路径

        Returns:
            List[Dict]: 对话消息列表，如果不存在则返回 None
        """
        # 构建项目目录路径
        project_safe = project.replace('/', '-').replace('\\', '-')
        if project_safe.startswith('-'):
            project_safe = project_safe[1:]

        # 查找对话文件
        conversation_file = None
        project_dir = self.projects_dir / project_safe

        if project_dir.exists():
            # 查找以session_id命名的文件
            session_file = project_dir / f"{session_id}.jsonl"
            if session_file.exists():
                conversation_file = session_file

        if not conversation_file:
            # 如果没有找到，尝试在所有项目目录中搜索
            for project_path in self.projects_dir.glob("*"):
                if project_path.is_dir():
                    session_file = project_path / f"{session_id}.jsonl"
                    if session_file.exists():
                        conversation_file = session_file
                        break

        if not conversation_file:
            return None

        try:
            messages = []
            with open(conversation_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        data = json.loads(line.strip())

                        # 只处理用户和助手消息
                        if data.get('type') in ['user', 'assistant']:
                            message_data = data.get('message', {})

                            # 提取消息内容
                            content = self._extract_message_content(message_data)

                            if content:
                                message = {
                                    'type': data.get('type'),
                                    'content': content,
                                    'timestamp': data.get('timestamp'),
                                    'uuid': data.get('uuid'),
                                    'formatted_time': self._format_iso_timestamp(data.get('timestamp'))
                                }
                                messages.append(message)

            return messages if messages else None

        except Exception as e:
            print(f"解析对话文件时出错 {conversation_file}: {e}")
            return None

    def _extract_message_content(self, message_data: Dict) -> Optional[str]:
        """
        从消息数据中提取文本内容

        Args:
            message_data: 消息数据字典

        Returns:
            str: 提取的文本内容
        """
        content = message_data.get('content')

        if isinstance(content, str):
            return content
        elif isinstance(content, list):
            # 处理包含多个部分的内容
            text_parts = []
            for item in content:
                if isinstance(item, dict):
                    if item.get('type') == 'text':
                        text_parts.append(item.get('text', ''))
                    elif item.get('type') == 'tool_use':
                        # 对于工具调用，显示工具名称和参数摘要
                        tool_name = item.get('name', 'unknown')
                        text_parts.append(f"[使用工具: {tool_name}]")
                elif isinstance(item, str):
                    text_parts.append(item)

            return '\n'.join(text_parts) if text_parts else None

        return None

    def _format_iso_timestamp(self, timestamp: str) -> str:
        """
        格式化ISO时间戳

        Args:
            timestamp: ISO格式时间戳

        Returns:
            str: 格式化后的时间字符串
        """
        if not timestamp:
            return "Unknown"

        try:
            # 解析ISO时间戳
            dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            # 转换为本地时间
            local_dt = dt.replace(tzinfo=None)
            return local_dt.strftime('%Y-%m-%d %H:%M:%S')
        except:
            return "Unknown"

    def search_full_conversations(self, query: str, project: str = None) -> List[Dict]:
        """
        搜索完整对话记录（包括用户问题和Claude回复）

        Args:
            query: 搜索关键词
            project: 项目路径过滤（可选）

        Returns:
            List[Dict]: 匹配的对话记录
        """
        conversations = self.parse_full_conversations()
        results = []

        for conv in conversations:
            # 项目过滤
            if project and conv.get('project') != project:
                continue

            # 搜索基础显示内容
            if query.lower() in conv.get('display', '').lower():
                results.append(conv)
                continue

            # 搜索完整对话内容
            if conv.get('has_full_content') and conv.get('full_conversation'):
                for message in conv['full_conversation']:
                    content = message.get('content', '')
                    if query.lower() in content.lower():
                        results.append(conv)
                        break

        return results

    def _format_timestamp(self, timestamp: int) -> str:
        """
        格式化时间戳

        Args:
            timestamp: 毫秒级时间戳

        Returns:
            str: 格式化后的时间字符串
        """
        try:
            dt = datetime.fromtimestamp(timestamp / 1000)
            return dt.strftime('%Y-%m-%d %H:%M:%S')
        except:
            return "Unknown"


if __name__ == "__main__":
    # 测试代码
    parser = ClaudeDataParser()

    print("=== Claude Code 完整对话历史 ===")
    conversations = parser.parse_full_conversations()
    for conv in conversations[:3]:  # 显示前3条
        print(f"时间: {conv.get('formatted_time')}")
        print(f"问题: {conv.get('display')}")
        print(f"项目: {conv.get('project')}")
        print(f"有完整内容: {conv.get('has_full_content')}")

        if conv.get('full_conversation'):
            print("对话内容:")
            for i, msg in enumerate(conv['full_conversation'][:4]):  # 显示前4条消息
                msg_type = "用户" if msg['type'] == 'user' else "Claude"
                content = msg['content'][:100] + "..." if len(msg['content']) > 100 else msg['content']
                print(f"  {i+1}. [{msg_type}] {content}")
        print("-" * 80)

    print("\n=== 统计摘要 ===")
    summary = parser.get_conversation_summary()
    print(f"总对话数: {summary['total_conversations']}")
    print(f"涉及项目: {len(summary['projects'])}")
    print(f"会话数: {summary['sessions']}")
    if summary['date_range']:
        print(f"时间范围: {summary['date_range']['earliest']} 到 {summary['date_range']['latest']}")

    print("\n=== 搜索测试 ===")
    search_results = parser.search_full_conversations("程序员")
    print(f"搜索'程序员'的结果数: {len(search_results)}")
    for result in search_results[:2]:
        print(f"匹配项目: {result.get('project')}")
        print(f"匹配问题: {result.get('display')}")
        print(f"有完整内容: {result.get('has_full_content')}")
        print("-" * 40)