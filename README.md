# Claude Code 对话可视化工具

一个功能强大的 Claude Code 对话历史可视化工具，让你能够方便地浏览、搜索和管理与 Claude 的完整对话记录。

## ✨ 功能特性

- 📊 **对话统计**: 展示对话总数、涉及项目、会话统计等
- 💬 **完整对话展示**: 显示用户问题和Claude回复的完整对话记录
- 📝 **历史浏览**: 分页浏览所有对话记录，支持时间排序
- 🔍 **全文搜索**: 在用户问题和Claude回复中搜索关键词，支持项目过滤
- 🗂️ **项目管理**: 按项目路径组织和筛选对话
- 📋 **快速操作**: 一键复制问题、完整对话内容，查看详细信息
- 🎨 **美观界面**: 基于 Bootstrap 的现代化 Web 界面
- 🏷️ **状态标识**: 区分完整对话和仅有问题的记录
- 🎯 **消息类型**: 清晰区分用户消息和Claude回复

## 🚀 快速开始

### 方法一：一键启动（推荐）

```bash
# 自动检查环境、安装依赖并启动
python3 start.py
```

### 方法二：简化启动

```bash
# 检查依赖并提供安装建议
python3 run_simple.py
```

### 方法三：完整安装

```bash
# 运行安装向导（创建启动脚本）
python3 install.py
```

### 方法四：手动启动

```bash
# 1. 创建虚拟环境（推荐）
python3 -m venv venv
source venv/bin/activate

# 2. 安装依赖
pip install -r requirements.txt

# 3. 运行工具
python app.py
```

### 方法五：使用脚本启动

```bash
# 使用提供的启动脚本
./setup.sh    # 初始化环境（仅需运行一次）
./run.sh      # 启动工具
```

然后在浏览器中访问 `http://localhost:5000`

## 📁 数据源说明

工具会自动读取 Claude Code 的数据：
- **历史记录**: `~/.claude/history.jsonl` - 对话基本信息和用户问题
- **完整对话**: `~/.claude/projects/{project}/{sessionId}.jsonl` - 包含Claude回复的完整对话记录
- **调试日志**: `~/.claude/debug/{sessionId}.txt` - 详细的会话调试信息
- **项目信息**: 自动提取项目路径信息和会话关联

## 🛠️ 技术栈

- **后端**: Python 3.7+ + Flask
- **前端**: Bootstrap 5 + JavaScript
- **数据解析**: 智能JSON Lines解析器，支持多种消息格式
- **界面**: 响应式设计，支持移动端
- **构建**: PyInstaller支持，可打包为独立可执行文件

## 📸 主要功能

### 🏠 主页仪表板
- 📊 对话统计卡片（总数、项目数、会话数、时间范围）
- 📝 最近对话预览（显示用户问题和Claude回复）
- 🗂️ 项目列表展示和快速导航
- 🏷️ 完整对话状态标识

### 💬 对话历史页面
- 📖 完整对话展示（用户问题 + Claude回复）
- 🎨 消息类型区分（用户消息蓝色，Claude回复绿色）
- ⏰ 精确时间戳显示
- 📋 多种复制选项（复制问题、复制完整对话）
- 👁️ 详细信息模态框
- 📄 分页浏览支持

### 🔍 搜索功能
- 🎯 全文搜索（用户问题 + Claude回复）
- 🔆 关键词高亮显示
- 🗂️ 项目过滤选项
- ⚡ 实时搜索结果
- 🏷️ 匹配内容标识

## 📦 构建和分发

### 构建可执行文件

```bash
# 构建独立可执行文件
python3 build_exe.py
```

构建完成后会生成：
- `dist/claude-code-viz` (Linux/macOS) 或 `dist/claude-code-viz.exe` (Windows)
- 包含所有依赖的独立可执行文件
- 自动创建分发包目录

### 系统要求

- **Python**: 3.7 或更高版本
- **操作系统**: Windows / macOS / Linux
- **内存**: 建议 512MB 以上
- **磁盘**: 50MB 可用空间
- **Claude Code**: 需要已安装并有对话记录

### 依赖包

```
Flask==2.3.3
Jinja2==3.1.2
python-dateutil==2.8.2
markdown==3.5.1
```

## 🔧 开发扩展

### 添加新功能
1. 在 `claude_parser.py` 中添加数据解析逻辑
2. 在 `app.py` 中添加路由和API
3. 在 `templates/` 中添加页面模板

### 自定义样式
- 修改 `templates/base.html` 中的 CSS
- 使用 Bootstrap 变量进行主题定制

### 数据处理扩展
- 支持新的消息格式解析
- 添加数据导出功能
- 实现实时数据监听

## 📋 TODO

- [ ] 实时监听 Claude Code 对话更新
- [ ] 导出对话记录为 Markdown/PDF/JSON
- [ ] 对话内容语法高亮（代码块）
- [ ] 标签和分类功能
- [ ] 对话统计图表和可视化
- [ ] 搜索历史记录
- [ ] 多语言支持（英文界面）
- [ ] 主题切换（深色/浅色模式）
- [ ] 对话收藏和书签功能
- [ ] 批量操作（删除、导出）

## 🚨 注意事项

- 确保已安装 Claude Code 并有对话记录
- 工具会读取 `~/.claude/` 目录下的数据
- 对话内容可能包含敏感信息，请注意访问控制
- 大量对话记录可能影响加载性能
- 建议定期备份重要对话记录

## 📚 相关文档

- [快速开始指南](QUICK_START.md) - 详细的安装和使用说明
- [使用指南](USAGE_GUIDE.md) - 完整功能介绍和使用场景
- [用户指南](USER_GUIDE.md) - 面向用户的详细操作手册
- [分发指南](DISTRIBUTION_GUIDE.md) - 构建和分发说明

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

### 贡献方式
1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 📄 许可证

MIT License

---

**享受你的 Claude Code 对话可视化体验！** 🎉