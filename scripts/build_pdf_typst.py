#!/usr/bin/env python3
"""Generate a book-style PDF using Typst from merged chapters."""

from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).parent.parent
CHAPTERS_DIR = ROOT / "book" / "src"
IMAGES = ROOT / "images"
TYPST_OUT = ROOT / "智能涌动.typ"
PDF_OUT = ROOT / "智能涌动.pdf"

VOLUME_MAP = {
    1: "卷一 破晓",
    6: "卷二 扩散",
    11: "卷三 权力",
    16: "卷四 入侵现实",
    22: "卷五 裂缝与重构",
    30: "卷六 智能体时代",
}


def esc(text: str) -> str:
    text = text.replace("𝕏", "X")
    text = text.replace("**", "")
    text = text.replace("\\", "\\\\")
    for char in ["#", "$", "[", "]", "@"]:
        text = text.replace(char, "\\" + char)
    return text


def plain_title(line: str) -> str:
    return line.lstrip("#").strip()


def paragraph(text: str, *, small: bool = False, indent: bool = True) -> str:
    size = "8.7pt" if small else "10.2pt"
    body = ("\u3000\u3000" + text) if indent else text
    return f'#text(size: {size})[#par(justify: true, first-line-indent: 0em, leading: 0.84em)[{esc(body)}]]'


def heading(level: int, title: str) -> str:
    if level == 1:
        return (
            '#pagebreak(weak: true)\n'
            '#v(24mm)\n'
            f'#heading(level: 1, numbering: none, outlined: true)[{esc(title)}]\n'
            '#v(9mm)\n'
            '#align(center)[#line(length: 24mm, stroke: 0.45pt + rgb("9a8f82"))]\n'
            '#v(9mm)'
        )
    if level == 2:
        return f'#block(above: 1.2em, below: 0.9em)[#text(font: "Noto Sans CJK SC", size: 12pt, weight: "medium")[{esc(title)}]]'
    return f'#block(above: 0.85em, below: 0.55em)[#text(font: "Noto Sans CJK SC", size: 10.6pt, weight: "medium")[{esc(title)}]]'


def volume_page(title: str) -> str:
    return (
        '#pagebreak(weak: true)\n'
        '#v(55mm)\n'
        f'#align(center)[#text(font: "Noto Sans CJK SC", size: 24pt, weight: "medium", tracking: 0.08em)[{esc(title)}]]\n'
        '#v(7mm)\n'
        '#align(center)[#line(length: 28mm, stroke: 0.55pt + rgb("8a7f70"))]\n'
        '#pagebreak()'
    )


def convert_markdown(md: str) -> str:
    blocks: list[str] = []
    in_refs = False

    for raw in md.splitlines():
        line = raw.strip()
        if not line:
            continue

        if line.startswith("# "):
            blocks.append(heading(1, plain_title(line)))
            in_refs = False
            continue
        if line.startswith("## "):
            title = plain_title(line)
            blocks.append(heading(2, title))
            in_refs = "参考文献" in title
            continue
        if line.startswith("### "):
            blocks.append(heading(3, plain_title(line)))
            continue

        if re.match(r"^\d+\.\s+", line) or line.startswith("- "):
            item = re.sub(r"^\d+\.\s+", "", line)
            item = item[2:] if item.startswith("- ") else item
            blocks.append(f'#pad(left: 1.4em, right: 0.5em)[#text(size: 8.3pt)[{esc(item)}]]')
            continue

        blocks.append(paragraph(line, small=in_refs, indent=not in_refs))

    return "\n\n".join(blocks)


def read_chapters() -> list[tuple[int, str]]:
    chapters = []
    for i in range(1, 35):
        path = CHAPTERS_DIR / f"ch{i:02d}.md"
        if not path.exists():
            raise FileNotFoundError(f"Missing chapter: {path}")
        chapters.append((i, path.read_text(encoding="utf-8")))
    return chapters


def build_author_note() -> str:
    lines = [
        '#v(28mm)',
        '#align(center)[#text(font: "Noto Sans CJK SC", size: 13pt, weight: "medium", tracking: 0.06em)[作者说明]]',
        '#v(10mm)',
        '#block(width: 100%, inset: (left: 8mm, right: 8mm))[',
        '  #text(size: 9.5pt, fill: rgb("4a4540"))[',
        '    #par(justify: true, leading: 1.1em)[新褶，是大脑中的一道新褶。]',
        '    #v(5mm)',
        '    #par(justify: true, leading: 1.1em)[如果说每一次技术革命都会改变人的工具、职业和生活方式，那么 AI 时代更深的一层变化，是它要求人重新长出理解世界的纹路。这道褶，不属于机器，属于仍在学习、判断和选择的人。]',
        '    #v(5mm)',
        '    #par(justify: true, leading: 1.1em)[本书由新褶主导写作，AI Agent 参与资料检索、结构审校、事实校对、草稿修订与排版生成。它不是替代作者的署名，而是这本书所记录时代的一部分。]',
        '  ]',
        ']',
    ]
    return "\n".join(lines)


def build_cta_page() -> str:
    qr_xinzhe = "images/xinzhe-qr.jpg"
    qr_aiworld = "images/AI-world-qr.jpg"
    lines = [
        '#pagebreak(weak: true)',
        '#v(22mm)',
        '#align(center)[#text(font: "Noto Sans CJK SC", size: 15pt, weight: "medium", tracking: 0.06em)[继续进入 AI 大世界]]',
        '#v(8mm)',
        '#align(center)[#line(length: 22mm, stroke: 0.45pt + rgb("9a8f82"))]',
        '#v(10mm)',
        '#text(size: 9.5pt, fill: rgb("4a4540"))[',
        '  #par(justify: true, leading: 1.1em)[这本书写到这里，并不是结尾。AI 仍在快速变化，模型、产品、产业和普通人的生活都还在继续刷新。新褶会在微信公众号中持续记录这个时代的变化，也在「AI 大世界」微信群里和读者、从业者、学习者一起交流新的工具、新的问题和新的判断。]',
        ']',
        '#v(4mm)',
        '#text(size: 9pt, fill: rgb("5f574f"))[',
        '  #par(justify: true, leading: 1.1em)[如果你愿意继续跟进 AI 时代的下一页，欢迎扫码关注和加入。]',
        ']',
        '#v(4mm)',
        '#text(size: 8pt, fill: rgb("8a7f70"))[',
        '  #par(justify: true, leading: 1.1em)[本书源码与构建脚本开源在 github.com\\/leether\\/ai-saga-book，欢迎反馈问题。]',
        ']',
        '#v(10mm)',
        '#align(center)[#grid(',
        '  columns: (1fr, 1fr),',
        '  column-gutter: 20mm,',
        '  align(center)[',
        f'    #image("{qr_xinzhe}", width: 32mm)',
        '    #v(3mm)',
        '    #text(size: 8.5pt, fill: rgb("5f574f"))[微信公众号：新褶]\\',
        '    #text(size: 7.5pt, fill: rgb("8a7f70"))[继续阅读 AI 观察]',
        '  ],',
        '  align(center)[',
        f'    #image("{qr_aiworld}", width: 32mm)',
        '    #v(3mm)',
        '    #text(size: 8.5pt, fill: rgb("5f574f"))[微信群：AI 大世界]\\',
        '    #text(size: 7.5pt, fill: rgb("8a7f70"))[加入读者交流]',
        '  ],',
        ')]',
    ]
    return "\n".join(lines)


def build_typst() -> str:
    parts = [
        '#set document(title: "智能涌动", author: "新褶")',
        '#set page(width: 148mm, height: 210mm, margin: (top: 20mm, bottom: 18mm, inside: 20mm, outside: 16mm), numbering: "1")',
        '#set text(font: "Noto Serif CJK SC", size: 10.2pt, lang: "zh", region: "CN")',
        '#set par(justify: true, leading: 0.82em)',
        '#show link: set text(fill: rgb("4b6584"))',
        '#show emph: it => text(font: "Noto Serif CJK SC", style: "italic", it.body)',
        '#show heading.where(level: 1): it => block(width: 100%, above: 0pt, below: 0pt)[#align(center)[#text(font: "Noto Sans CJK SC", size: 17.5pt, weight: "medium", tracking: 0.04em)[#it.body]]]',
        '#align(center + horizon)[',
        '  #text(font: "Noto Sans CJK SC", size: 31pt, weight: "medium", tracking: 0.12em)[智能涌动]\\',
        '  #v(9mm)',
        '  #text(font: "Noto Serif CJK SC", size: 12.5pt, fill: rgb("5f574f"))[从 ChatGPT 到智能体时代]\\',
        '  #v(2.5mm)',
        '  #text(font: "Noto Serif CJK SC", size: 11.5pt, fill: rgb("5f574f"))[时代中的个体如何进入 AI 狂飙]',
        '  #v(12mm)',
        '  #text(font: "Noto Serif CJK SC", size: 11pt, fill: rgb("5f574f"))[新褶 著]',
        '  #v(3mm)',
        '  #text(font: "Noto Serif CJK SC", size: 9pt, fill: rgb("8a7f70"))[AI Agent 协作]',
        '  #v(14mm)',
        '  #line(length: 40mm, stroke: 0.65pt + rgb("8a7f70"))',
        '  #v(10mm)',
        '  #text(size: 9pt, fill: rgb("7b7167"))[精排版]',
        ']',
        '#pagebreak()',
        build_author_note(),
        '#pagebreak()',
        '#v(18mm)',
        '#align(center)[#text(font: "Noto Sans CJK SC", size: 12pt, weight: "medium", tracking: 0.08em)[目录]]',
        '#v(5mm)',
        '#text(size: 8pt)[#set par(leading: 0.55em)\n#outline(title: none, depth: 1)]',
    ]

    for idx, md in read_chapters():
        if idx in VOLUME_MAP:
            parts.append(volume_page(VOLUME_MAP[idx]))
        parts.append(convert_markdown(md))

    parts.append(build_cta_page())

    return "\n\n".join(parts) + "\n"


def main() -> None:
    typst = build_typst()
    TYPST_OUT.write_text(typst, encoding="utf-8")
    subprocess.run(["typst", "compile", "--root", str(ROOT), str(TYPST_OUT), str(PDF_OUT)], check=True, timeout=300)
    print(f"Typst: {TYPST_OUT}")
    print(f"PDF: {PDF_OUT}")


if __name__ == "__main__":
    main()
