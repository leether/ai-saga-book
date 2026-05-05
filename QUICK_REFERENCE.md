# 快速参考指南 (Quick Reference)

## 常用命令速查

### 本地开发
```bash
# 查看本地网站（热重载）
mdbook serve book/

# 构建静态 HTML
mdbook build book/

# 生成精排 PDF
python3 scripts/build_pdf_typst.py

# 合并章节
python3 scripts/merge_chapters.py
```

### 项目管理
```bash
# 验证所有 34 章
python3 -c "from scripts.utils import validate_chapters; validate_chapters()"

# 列出所有章节
python3 -c "from scripts.utils import list_chapters; print(list_chapters())"
```

### 发布流程
```bash
# 标记版本
git tag v2.8

# 推送到 GitHub（自动触发 Actions）
git push origin main --tags

# 查看 GitHub Actions 进度
gh run list
```

## 文件结构速查

```
📖 书籍内容
├── book/
│   ├── src/
│   │   ├── SUMMARY.md      ← 目录
│   │   ├── ch01.md         ← 卷一
│   │   ├── ch05.md
│   │   ├── ch06.md         ← 卷二
│   │   ├── ch10.md
│   │   ├── ch11.md         ← 卷三
│   │   └── ch34.md         ← 卷六
│   ├── book.toml           ← mdBook 配置
│   └── theme/custom.css    ← 自定义样式

🛠️  构建脚本
├── scripts/
│   ├── utils.py            ← 共享工具（新）
│   ├── merge_chapters.py   ← 合并章节
│   └── build_pdf_typst.py  ← 生成 PDF

🖼️  资源
├── images/
│   ├── xinzhe-qr.jpg
│   └── AI-world-qr.jpg

⚙️  配置
├── .github/workflows/
│   ├── deploy-pages.yml
│   └── release.yml
├── .env.example
├── pyproject.toml
└── LICENSE
```

## mdBook 常用语法

```markdown
# 章标题（一级标题）

## 节标题（二级标题）

### 小节标题（三级标题）

正文段落。

> 引用文字

- 列表项 1
- 列表项 2

1. 编号列表 1
2. 编号列表 2

**加粗** _斜体_ `代码`

[链接文本](URL)

![图片描述](images/image.jpg)
```

## 章节编号规则

```
卷一 破晓     — ch01-05
卷二 扩散     — ch06-10
卷三 权力     — ch11-15
卷四 入侵现实 — ch16-21
卷五 裂缝与重构 — ch22-29
卷六 智能体时代 — ch30-34
```

**文件命名**: `ch01.md`, `ch02.md`, ..., `ch34.md`

## 常见任务

### 添加新章节
```bash
# 创建新文件
touch book/src/ch35.md

# 在 SUMMARY.md 中添加入目
- [第35章 标题](ch35.md)

# 本地测试
mdbook serve book/
```

### 修改章节内容
```bash
# 编辑文件
vim book/src/ch01.md

# 本地预览（自动刷新）
mdbook serve book/

# 提交
git add book/src/ch01.md
git commit -m "docs(ch01): 修改说明"
```

### 更新样式
```bash
# 编辑 CSS
vim book/theme/custom.css

# 重新构建查看效果
mdbook serve book/
```

### 生成发布版本
```bash
# 1. 更新所有章节
# 2. 本地验证
mdbook build book/
python3 scripts/build_pdf_typst.py

# 3. 标记版本
git tag v2.9
git push origin main --tags

# 4. GitHub Actions 自动发布
# 检查 Actions 状态：https://github.com/leether/ai-saga-book/actions
```

## 错误排查

| 错误 | 原因 | 解决方案 |
|------|------|--------|
| `mdbook: command not found` | mdBook 未安装 | `cargo install mdbook` |
| `typst: command not found` | Typst 未安装 | `cargo install typst-cli` |
| `FileNotFoundError: ch01.md` | 章节缺失 | 检查 book/src/ 中的文件 |
| `No chapters found` | SUMMARY.md 配置错误 | 检查 SUMMARY.md 语法 |
| PDF 生成失败 | 字体或 Typst 版本问题 | 检查 Typst 是否最新版本 |

## 有用的链接

- **mdBook 文档**: https://rust-lang.github.io/mdBook/
- **Typst 文档**: https://typst.app/docs/
- **本项目主页**: https://github.com/leether/ai-saga-book
- **在线阅读**: https://leether.github.io/ai-saga-book

## 工作流最佳实践

### 编辑内容
1. 创建分支：`git checkout -b fix/chapter-typo`
2. 编辑文件：修改 Markdown 内容
3. 本地验证：`mdbook serve book/`
4. 提交：`git commit -m "fix: 修复ch01 typo"`
5. 推送和创建 PR

### 发布新版本
1. 完成所有编辑
2. 本地构建验证：`mdbook build book/`
3. 生成 PDF：`python3 scripts/build_pdf_typst.py`
4. 提交所有更改
5. 标记版本：`git tag v2.9 -m "发布说明"`
6. 推送：`git push origin main --tags`
7. 等待 GitHub Actions 完成
8. 查看 Releases 页面

---

**更新**: 2026-05-05 | **版本**: 2.8
