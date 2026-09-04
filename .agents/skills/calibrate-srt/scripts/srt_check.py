#!/usr/bin/env python3
"""校验校准后的 SRT 字幕：时间轴不变、无标点、无空白异常。

用法：python3 srt_check.py <原始.srt> <校准后.srt>
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

PUNCTUATION = (
    "，。！？；：、…—·“”‘’「」『』《》〈〉（）【】《》"
    ",!?;:'\"()[]<>~@#$%^&*_+=/\\|"
)
TIMING_LINE = re.compile(
    r"^\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}$"
)


def parse_srt(path: Path) -> list[tuple[str, str, list[str]]]:
    text = path.read_text(encoding="utf-8-sig")
    blocks = re.split(r"\n\s*\n", text.strip())
    cues = []
    for block in blocks:
        lines = block.strip().splitlines()
        if len(lines) < 3:
            continue
        index, timing, text_lines = lines[0], lines[1], lines[2:]
        cues.append((index, timing, text_lines))
    return cues


def main() -> int:
    if len(sys.argv) != 3:
        print("用法：python3 srt_check.py <原始.srt> <校准后.srt>", file=sys.stderr)
        return 2

    original = parse_srt(Path(sys.argv[1]))
    calibrated = parse_srt(Path(sys.argv[2]))
    problems: list[str] = []

    if len(original) != len(calibrated):
        problems.append(
            f"字幕条数不一致：原始 {len(original)} 条，校准后 {len(calibrated)} 条"
        )
    for position, (old, new) in enumerate(zip(original, calibrated), start=1):
        if old[0] != new[0]:
            problems.append(f"第 {position} 块序号变化：{old[0]} -> {new[0]}")
        if old[1] != new[1]:
            problems.append(f"第 {position} 块时间轴变化：{old[1]} -> {new[1]}")
        if not TIMING_LINE.match(new[1]):
            problems.append(f"第 {position} 块时间轴格式异常：{new[1]!r}")

    for position, (_, _, text_lines) in enumerate(calibrated, start=1):
        for line in text_lines:
            if line != line.strip():
                problems.append(f"第 {position} 块存在行首或行尾空格：{line!r}")
            if "  " in line:
                problems.append(f"第 {position} 块存在连续空格：{line!r}")
            for match in re.finditer(r"[.．]", line):
                start, end = match.span()
                if not (
                    start > 0
                    and end < len(line)
                    and line[start - 1].isdigit()
                    and line[end].isdigit()
                ):
                    problems.append(
                        f"第 {position} 块存在非小数用法的点号：{line!r}"
                    )
            for char in line:
                if char in PUNCTUATION:
                    problems.append(f"第 {position} 块存在标点 {char!r}：{line!r}")
                    break

    if problems:
        print(f"[警告] 发现 {len(problems)} 个问题")
        for problem in problems:
            print(f"  {problem}")
        return 1
    print(
        f"[通过] {len(calibrated)} 条字幕：序号与时间轴全部一致，"
        "文本无标点、无空白异常"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
