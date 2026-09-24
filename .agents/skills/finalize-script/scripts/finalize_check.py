#!/usr/bin/env python3
"""定稿前检查：对比 AI 原稿和林序改过的初稿，扫描禁用词，统计口播字数。

用法（在项目根目录）：python3 .agents/skills/finalize-script/scripts/finalize_check.py <选题>
<选题> 是不带 .md 的文件名，也可以直接给初稿路径。
"""

from __future__ import annotations

import difflib
import re
import sys
from pathlib import Path

WORDS_PER_MINUTE = 330

BANNED = [
    (re.compile(r"不是[^。！？\n]{0,40}而是"), "禁用句式「不是……而是……」"),
    (re.compile(r"军备|战争|大战|战场"), "禁用战争词"),
    (re.compile(r"路径依赖|底层逻辑|多方博弈|用户心智|囚徒困境|三重结构"), "分析术语说出口了"),
    (re.compile(r"\d{1,2}:\d{2}\s*[-–]\s*\d{1,2}:\d{2}"), "时间轴标注"),
]

DANGLING = re.compile(r"马上说到|马上就说|后面会讲|后面再说|待会儿|等下说|接下来我们|最后说个|我们下面")


def spoken_text(text: str) -> str:
    lines = []
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("#") or s.startswith(">") or s.startswith("---"):
            continue
        lines.append(re.sub(r"【画面[^】]*】", "", s))
    return "".join("".join(lines).split())


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    arg = sys.argv[1]
    root = Path.cwd()
    draft = Path(arg) if arg.endswith(".md") else root / "稿件库/1-初稿" / f"{arg}.md"
    name = draft.name
    backup = root / "稿件库/0-AI原稿" / name
    final = root / "稿件库/2-正式稿" / name

    problems = 0
    if not draft.exists():
        print(f"[错误] 找不到初稿：{draft}")
        return 1
    if final.exists():
        print(f"[注意] 正式稿已有同名文件：{final}，移动前要问林序覆盖还是另存")
        problems += 1

    text = draft.read_text(encoding="utf-8")

    print("=" * 20, "AI 原稿 → 林序版本 差异", "=" * 20)
    if backup.exists():
        diff = list(difflib.unified_diff(
            backup.read_text(encoding="utf-8").splitlines(),
            text.splitlines(),
            fromfile="0-AI原稿", tofile="1-初稿（林序）", lineterm="", n=1,
        ))
        print("\n".join(diff) if diff else "（没有修改）")
    else:
        print(f"（没有 AI 原稿备份：{backup}，跳过对比和修改记录）")

    print("=" * 20, "扫描", "=" * 20)
    for no, line in enumerate(text.splitlines(), 1):
        for pattern, label in BANNED:
            if pattern.search(line):
                print(f"[禁用] 第{no}行 {label}：{line.strip()}")
                problems += 1
        if DANGLING.search(line):
            print(f"[断口?] 第{no}行 预告后文，确认后面真的讲了：{line.strip()}")
            problems += 1
    if re.search(r"\n---\s*\n\s*\n*---", text) or re.search(r"\n\n\n\n", text):
        print("[格式] 有连续分隔线或多余空行")
        problems += 1

    count = len(spoken_text(text))
    minutes = count / WORDS_PER_MINUTE
    print("=" * 20, "字数", "=" * 20)
    print(f"口播净字数 {count}，约 {int(minutes)} 分 {round((minutes % 1) * 60)} 秒（按 {WORDS_PER_MINUTE} 字/分钟）")

    print("=" * 20)
    print(f"需要人工确认的提示 {problems} 条。脚本看不出所有断口，仍要完整读一遍初稿。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
