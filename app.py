"""
Claude Code 可视化工具 Web 应用
"""

from flask import Flask, render_template, request, jsonify
from claude_parser import ClaudeDataParser
import os

app = Flask(__name__)
parser = ClaudeDataParser()


@app.route('/')
def index():
    """主页"""
    summary = parser.get_conversation_summary()
    recent_conversations = parser.parse_full_conversations()[:10]  # 最近10条对话

    return render_template('index.html',
                         summary=summary,
                         recent_conversations=recent_conversations)


@app.route('/conversations')
def conversations():
    """对话列表页"""
    page = request.args.get('page', 1, type=int)
    per_page = 20

    all_conversations = parser.parse_full_conversations()
    total = len(all_conversations)

    # 分页
    start = (page - 1) * per_page
    end = start + per_page
    conversations = all_conversations[start:end]

    # 分页信息
    pagination = {
        'page': page,
        'per_page': per_page,
        'total': total,
        'pages': (total + per_page - 1) // per_page,
        'has_prev': page > 1,
        'has_next': end < total
    }

    return render_template('conversations.html',
                         conversations=conversations,
                         pagination=pagination)


@app.route('/search')
def search():
    """搜索页面"""
    query = request.args.get('q', '').strip()
    project = request.args.get('project', '').strip()

    results = []
    if query:
        results = parser.search_full_conversations(query, project if project else None)

    # 获取所有项目用于过滤
    all_conversations = parser.parse_full_conversations()
    projects = sorted(set(conv.get('project', 'Unknown') for conv in all_conversations))

    return render_template('search.html',
                         query=query,
                         project=project,
                         results=results,
                         projects=projects)


@app.route('/api/conversation/<session_id>')
def get_conversation_details(session_id):
    """获取对话详情API"""
    debug_logs = parser.get_debug_logs(session_id)

    # 从完整对话记录中找到对应的对话
    conversations = parser.parse_full_conversations()
    conversation = None
    for conv in conversations:
        if conv.get('sessionId') == session_id:
            conversation = conv
            break

    return jsonify({
        'conversation': conversation,
        'debug_logs': debug_logs,
        'has_logs': debug_logs is not None,
        'has_full_content': conversation.get('has_full_content', False) if conversation else False
    })


@app.route('/api/stats')
def get_stats():
    """获取统计信息API"""
    return jsonify(parser.get_conversation_summary())


if __name__ == '__main__':
    print("启动 Claude Code 可视化工具...")
    print("访问 http://localhost:5000 查看界面")

    # 检查 Claude 目录是否存在
    if not os.path.exists(os.path.expanduser("~/.claude")):
        print("警告: 未找到 Claude 配置目录 ~/.claude")
        print("请确保已安装并使用过 Claude Code")

    app.run(debug=True, host='0.0.0.0', port=5000)