# 智能涌动（AI Saga）- 公开版书籍

《智能涌动》公开版源代码和构建脚本。使用 [mdBook](https://rust-lang.github.io/mdBook/) 进行在线发布，使用 Typst 进行 PDF 排版。

## 📚 项目概览

**关于这本书**：
- 📖 **标题**: 智能涌动 - 从 ChatGPT 到智能体时代
- ✍️ **作者**: 新褶
- 🤖 **协作**: AI Agent（资料检索、校对、修订）
- 📊 **规模**: 34 章，分 6 卷，约 22 万字

**完整内容**：
- 卷一 破晓 — ch01-05：ChatGPT 诞生与全球震动
- 卷二 扩散 — ch06-10：开源、中国入场与监管初现
- 卷三 权力 — ch11-15：OpenAI 政变、产品冲刺与算力博弈
- 卷四 入侵现实 — ch16-21：多模态、苹果入场与 Agent 泡沫
- 卷五 裂缝与重构 — ch22-29：DeepSeek、MCP、编程 Agent 与物质世界
- 卷六 智能体时代 — ch30-34：ChatGPT Agent、开源反攻、护栏与未来

## 🔗 在线阅读和下载

- 📖 **在线阅读**: [GitHub Pages](https://leether.github.io/ai-saga-book)
- 📥 **下载格式**:
  - 📕 PDF（精排版）
  - 📗 EPUB（电子书）
  - 📘 DOCX（Word 文档）
  - 📙 HTML（网页）
  
  所有发布版本可在 [GitHub Releases](https://github.com/leether/ai-saga-book/releases) 下载

## 📁 项目结构

```
ai-saga-book/
├── README.md              # 项目说明（本文件）
├── CONTRIBUTING.md        # 贡献指南
├── LICENSE               # 代码许可证（MIT）
├── .env.example          # 环境变量模板
├── pyproject.toml        # Python 项目配置
│
├── book/                 # mdBook 项目
│   ├── book.toml         # mdBook 配置
│   ├── src/              # 书籍源文件
│   │   ├── SUMMARY.md    # 目录
│   │   ├── ch01.md - ch34.md  # 34 个章节
│   │   └── ...
│   └── theme/            # 自定义主题
│       └── custom.css
│
├── scripts/              # 构建脚本
│   ├── utils.py          # 共享工具（新）
│   ├── merge_chapters.py  # 合并章节为单个文件
│   └── build_pdf_typst.py # 生成 PDF（Typst）
│
├── images/               # 图片和二维码
│   ├── xinzhe-qr.jpg     # 作者微信二维码
│   └── AI-world-qr.jpg   # 微信群二维码
│
└── .github/
    └── workflows/        # GitHub Actions 工作流
        ├── deploy-pages.yml   # 构建和部署网站
        └── release.yml        # 创建发布
```

## 🚀 快速开始

### 系统要求
- Python 3.13+
- Rust（用于 mdBook）
- typst（用于 PDF 生成）或 Pandoc

### 环境配置

1. **克隆仓库**
   ```bash
   git clone https://github.com/leether/ai-saga-book.git
   cd ai-saga-book
   ```

2. **创建虚拟环境**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **安装 Rust 工具链**（如果未安装）
   ```bash
   curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
   source $HOME/.cargo/env
   ```

4. **安装 mdBook**
   ```bash
   cargo install mdbook
   ```

5. **安装 Typst**（用于 PDF 生成）
   ```bash
   cargo install typst-cli
   ```

## 📖 使用指南

### 在线阅读和构建网站

```bash
# 查看本地网站（http://localhost:3000）
mdbook serve book/

# 构建静态 HTML（输出到 book-output/html/）
mdbook build book/
```

### 生成 PDF

```bash
# 使用 Typst 生成精排 PDF
python3 scripts/build_pdf_typst.py

# 输出文件：智能涌动.pdf
```

### 合并章节

```bash
# 将所有 34 章合并为单个 Markdown 文件
python3 scripts/merge_chapters.py

# 输出文件：全书.md（用于转换其他格式）
```

## 🛠️ 脚本说明

### `scripts/merge_chapters.py`
合并所有章节 Markdown 文件为单个文件。

**功能**：
- 读取 book/src/ 中的 ch01.md ~ ch34.md
- 按卷添加分卷标题
- 输出到 全书.md

**用法**：
```bash
python3 scripts/merge_chapters.py
```

### `scripts/build_pdf_typst.py`
使用 Typst 排版引擎生成精排 PDF。

**功能**：
- 读取所有章节
- 应用排版和样式
- 生成作者说明和 CTA 页面
- 输出高质量 PDF

**用法**：
```bash
python3 scripts/build_pdf_typst.py
```

**输出**：
- 智能涌动.typ（Typst 源文件）
- 智能涌动.pdf（最终 PDF）

### `scripts/utils.py`
共享工具库（新增）。

**提供函数**：
- `setup_logging()` - 日志配置
- `read_file()` / `write_file()` - 文件操作
- `run_command()` - 执行外部命令
- `validate_chapters()` - 验证章节完整性
- `list_chapters()` - 列出所有章节

## 📋 配置文件

### `book/book.toml`
mdBook 项目配置：

```toml
[book]
title = "智能涌动"
authors = ["新褶"]
language = "zh"
src = "src"

[output.html]
default-theme = "navy"
git-repository-url = "https://github.com/leether/ai-saga-book"
additional-css = ["theme/custom.css"]
```

### `.env.example`
环境变量配置模板。

## 📊 工作流程

### 本地开发
1. 编辑 book/src/ 中的章节文件
2. 运行 `mdbook serve book/` 本地预览
3. 检查排版和链接
4. 提交更改

### 发布流程
1. 更新章节内容
2. 标记版本号（例如 v2.8）
3. 创建 Git 标签：`git tag v2.8`
4. 推送到 GitHub：`git push origin main --tags`
5. GitHub Actions 自动：
   - 构建静态网站
   - 生成 PDF、EPUB、DOCX
   - 创建 Release 发布
   - 部署到 GitHub Pages

## 🔄 CI/CD 工作流

### `.github/workflows/deploy-pages.yml`
- 在 main 分支更新时运行
- 构建 mdBook HTML
- 部署到 GitHub Pages

### `.github/workflows/release.yml`
- 在创建标签时运行
- 生成多种格式（PDF、EPUB、DOCX）
- 创建 GitHub Release
- 上传文件作为发布资产

## 🔐 许可证

- **书籍内容**: [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/)
  - 署名：需注明作者"新褶"
  - 非商用：禁止商业使用
  - 禁止演绎：不能修改和重新发布

- **源代码和脚本**: [MIT License](LICENSE)
  - 自由使用、修改和分发
  - 保留许可证和版权声明

## 🤝 贡献指南

欢迎提交问题报告和改进建议！

### 报告问题
- 错别字或排版问题
- 事实错误或需要验证的内容
- 链接失效
- 格式或显示问题

在 [GitHub Issues](https://github.com/leether/ai-saga-book/issues) 提交 Issue

### 改进内容
- 更正语法或表述
- 补充参考资料
- 改进代码和脚本
- 优化网站样式

请参考 [CONTRIBUTING.md](CONTRIBUTING.md) 了解详细流程

## 📞 联系和关注

继续阅读 AI 时代的观察和分析：

- **微信公众号**: 新褶
- **微信群**: AI 大世界
- **GitHub**: [@leether](https://github.com/leether)

## 📝 更新日志

### 最近更新
- **v2.8** (2026-05-05): 修复 CI 配置和资产命名
- **v2.0** (2026-01-XX): 完整的 34 章公开版发布

详见 [GitHub Releases](https://github.com/leether/ai-saga-book/releases)

---

**项目地址**: [github.com/leether/ai-saga-book](https://github.com/leether/ai-saga-book)  
**在线阅读**: [leether.github.io/ai-saga-book](https://leether.github.io/ai-saga-book)  
**最后更新**: 2026-05-05
