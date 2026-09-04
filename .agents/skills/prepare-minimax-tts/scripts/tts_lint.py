#!/usr/bin/env python3
"""检查 MiniMax 中文 TTS 口播稿中可静态识别的格式和读音风险。"""

from __future__ import annotations

import argparse
import re
import sys
from decimal import Decimal, InvalidOperation
from pathlib import Path


Warning = tuple[int, str, str]

PAUSE_CANDIDATE = re.compile(r"<#[^\n<>]*#>")
NUMERIC_PAUSE_TAG = re.compile(r"<#(\d+(?:\.\d+)?)#>")
PAUSE_MARKER = re.compile(r"<#|#>")
INLINE_PAUSE_PUNCTUATION = "，。！？；：、—…"

MIXED_CASE_INITIALISM = re.compile(
    r"(?<![A-Za-z])(?:SoC|eSIM)(?![A-Za-z])"
)
COMPACT_UPPERCASE = re.compile(r"(?<![A-Za-z])([A-Z]{2,})(?![A-Za-z])")
CONNECTED_UPPERCASE_ALLOWLIST = {"OPPO"}
UNIT_INITIALISMS = {"KB", "MB", "GB", "TB"}

RAW_UNIT = re.compile(
    r"(?i)(?<![A-Za-z])(?:"
    r"GB/s|MB/s|KB/s|GHz|MHz|kHz|Hz|Gbps|Mbps|kbps|fps|rpm|"
    r"mAh|kWh|Wh|TOPS|TFLOPS|FLOPS|nm|[μµ]m|mm|cm|kg|ms|"
    r"GB|MB|KB|TB|°C|℃|dB|nits?|cd/m²"
    r")(?![A-Za-z])"
)

CHINESE_NUMBER_CHARS = "零〇一二三四五六七八九十百千万亿两点"
WRONG_SENSOR_FRACTION = re.compile(
    rf"[{CHINESE_NUMBER_CHARS}]+分之一点[{CHINESE_NUMBER_CHARS}]+英寸"
)
WRONG_DIMENSITY_MODEL = re.compile(
    rf"天玑\s*[{CHINESE_NUMBER_CHARS}]+千[{CHINESE_NUMBER_CHARS}]+百"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="检查已准备好的 MiniMax 中文 TTS 口播稿。"
    )
    parser.add_argument(
        "path",
        help="TTS 稿件路径；使用 '-' 可从标准输入读取 UTF-8 文本。",
    )
    return parser.parse_args()


def read_text(path_arg: str) -> tuple[str, str]:
    if path_arg == "-":
        return sys.stdin.read(), "<stdin>"
    path = Path(path_arg)
    return path.read_text(encoding="utf-8"), str(path)


def add_warning(
    warnings: list[Warning], line_number: int, kind: str, detail: str
) -> None:
    warning = (line_number, kind, detail)
    if warning not in warnings:
        warnings.append(warning)


def line_number_at(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def validate_pause_tags(text: str, warnings: list[Warning]) -> None:
    candidates = list(PAUSE_CANDIDATE.finditer(text))
    valid_tags: list[re.Match[str]] = []

    for match in candidates:
        line_number = line_number_at(text, match.start())
        numeric = NUMERIC_PAUSE_TAG.fullmatch(match.group(0))
        if numeric is None:
            add_warning(
                warnings,
                line_number,
                "停顿",
                f"停顿标签格式无效：{match.group(0)!r}",
            )
            continue

        value = numeric.group(1)
        if re.fullmatch(r"\d+(?:\.\d{1,2})?", value) is None:
            add_warning(
                warnings,
                line_number,
                "停顿",
                f"停顿秒数最多保留两位小数：{match.group(0)!r}",
            )
            continue

        try:
            seconds = Decimal(value)
        except InvalidOperation:
            seconds = Decimal("-1")
        if not Decimal("0.01") <= seconds <= Decimal("99.99"):
            add_warning(
                warnings,
                line_number,
                "停顿",
                f"停顿秒数必须位于 0.01 到 99.99：{match.group(0)!r}",
            )
            continue

        valid_tags.append(match)

    text_without_candidates = PAUSE_CANDIDATE.sub("", text)
    for marker in PAUSE_MARKER.finditer(text_without_candidates):
        add_warning(
            warnings,
            line_number_at(text_without_candidates, marker.start()),
            "停顿",
            "发现未闭合或格式错误的停顿标签",
        )

    for previous, current in zip(candidates, candidates[1:]):
        if text[previous.end() : current.start()].strip() == "":
            add_warning(
                warnings,
                line_number_at(text, current.start()),
                "停顿",
                "停顿标签不得连续放置",
            )

    for match in valid_tags:
        line_number = line_number_at(text, match.start())
        before = PAUSE_CANDIDATE.sub("", text[: match.start()]).rstrip()
        after = PAUSE_CANDIDATE.sub("", text[match.end() :]).lstrip()
        if not before or not after:
            add_warning(
                warnings,
                line_number,
                "停顿",
                "停顿标签必须位于两个可朗读文本段之间，不能放在全文开头或结尾",
            )
            continue

        line_start = text.rfind("\n", 0, match.start()) + 1
        line_end = text.find("\n", match.end())
        if line_end == -1:
            line_end = len(text)
        current_line = text[line_start:line_end]
        is_standalone = current_line.strip() == match.group(0)
        if not is_standalone:
            immediate_before = text[: match.start()].rstrip()
            if (
                not immediate_before
                or immediate_before[-1] not in INLINE_PAUSE_PUNCTUATION
            ):
                add_warning(
                    warnings,
                    line_number,
                    "停顿",
                    "内联停顿标签应紧接在中文标点之后，不能插入词语内部",
                )


def lint_markdown(line: str, line_number: int, warnings: list[Warning]) -> None:
    if re.match(r"^\s{0,3}#{1,6}(?:\s+|$)", line):
        add_warning(warnings, line_number, "Markdown", "仍包含 Markdown 标题")
    if re.match(r"^\s*(?:[-*+]|\d+[.)])\s+", line):
        add_warning(warnings, line_number, "Markdown", "仍包含列表格式")
    if re.match(r"^\s*>+\s?", line):
        add_warning(warnings, line_number, "Markdown", "仍包含引用块格式")
    if re.search(r"```|~~~", line):
        add_warning(warnings, line_number, "Markdown", "仍包含代码块标记")
    if re.search(r"(?:\*\*|__|~~|`)", line):
        add_warning(warnings, line_number, "Markdown", "仍包含行内 Markdown 格式")
    if re.search(r"!\[[^\]]*\]\([^)]+\)", line):
        add_warning(warnings, line_number, "Markdown", "仍包含 Markdown 图片")
    if re.search(r"(?<!!)\[[^\]]+\]\([^)]+\)", line):
        add_warning(warnings, line_number, "Markdown", "仍包含 Markdown 链接")
    if re.search(r"\[\^[^\]]+\]|^\s*\[[^\]]+\]:", line):
        add_warning(warnings, line_number, "Markdown", "仍包含脚注或引用定义")
    if line.count("|") >= 2 or re.match(r"^\s*\|?\s*:?-{3,}", line):
        add_warning(warnings, line_number, "Markdown", "仍包含表格格式")
    if re.search(r"https?://|www\.", line):
        add_warning(warnings, line_number, "网址", "仍包含 URL")
    if "[画面" in line or "【画面" in line:
        add_warning(warnings, line_number, "画面提示", "仍包含画面提示")
    if re.search(r"(?:\[|【)(?:作者注|备注|制作提示|旁白提示)", line):
        add_warning(warnings, line_number, "制作提示", "仍包含作者或制作备注")
    if re.match(r"^\s*(?:参考资料|资料来源|作者注|备注)\s*[：:]?\s*$", line):
        add_warning(warnings, line_number, "资料", "仍包含资料或备注标题")


def lint_spoken_units(
    spoken: str, line_number: int, warnings: list[Warning]
) -> None:
    unit_spans: list[tuple[int, int]] = []
    for unit in RAW_UNIT.finditer(spoken):
        unit_spans.append(unit.span())
        add_warning(
            warnings,
            line_number,
            "单位",
            f"仍包含未展开或未拆分的单位：{unit.group(0)!r}",
        )

    mixed = MIXED_CASE_INITIALISM.search(spoken)
    if mixed:
        add_warning(
            warnings,
            line_number,
            "首字母缩写",
            f"仍包含未拆分的首字母缩写：{mixed.group(0)!r}",
        )

    for initialism in COMPACT_UPPERCASE.finditer(spoken):
        token = initialism.group(1)
        if token in CONNECTED_UPPERCASE_ALLOWLIST or token in UNIT_INITIALISMS:
            continue
        if any(
            start <= initialism.start() and initialism.end() <= end
            for start, end in unit_spans
        ):
            continue
        add_warning(
            warnings,
            line_number,
            "首字母缩写",
            f"仍包含未拆分的首字母缩写：{token!r}",
        )

    single_letter_unit = re.search(
        rf"[{CHINESE_NUMBER_CHARS}]\s*[WVA](?![A-Za-z])", spoken
    )
    if single_letter_unit:
        add_warning(
            warnings,
            line_number,
            "单位",
            f"可能仍包含单字母单位：{single_letter_unit.group(0)!r}",
        )

    compact_protocol = re.search(
        rf"[{CHINESE_NUMBER_CHARS}][GK](?![A-Za-z])", spoken
    )
    if compact_protocol:
        add_warning(
            warnings,
            line_number,
            "协议名",
            f"数字与协议字母之间缺少读音边界：{compact_protocol.group(0)!r}",
        )


def lint(text: str) -> list[Warning]:
    warnings: list[Warning] = []
    validate_pause_tags(text, warnings)

    for line_number, line in enumerate(text.splitlines(), start=1):
        lint_markdown(line, line_number, warnings)
        spoken = PAUSE_CANDIDATE.sub("", line)

        if "Wi-Fi" in spoken:
            add_warning(
                warnings,
                line_number,
                "协议名",
                "仍包含带连字符的 Wi-Fi；请使用项目约定的口播读法",
            )

        if "天珑" in spoken:
            add_warning(
                warnings,
                line_number,
                "产品名",
                "联发科 Dimensity 的中文产品名应为“天玑”",
            )
        if WRONG_DIMENSITY_MODEL.search(spoken):
            add_warning(
                warnings,
                line_number,
                "产品型号",
                "天玑四位型号可能误用了“百”，请按项目简化读法检查",
            )
        if WRONG_SENSOR_FRACTION.search(spoken) or "一英寸一点" in spoken:
            add_warning(
                warnings,
                line_number,
                "传感器尺寸",
                "传感器分数读法可能颠倒了分子和分母",
            )

        digit = re.search(r"[0-9０-９]", spoken)
        if digit:
            add_warning(
                warnings,
                line_number,
                "数字",
                f"仍包含阿拉伯数字，位置接近 {digit.group(0)!r}",
            )

        lint_spoken_units(spoken, line_number, warnings)

        symbol = re.search(r"[/％%+×÷=&@<>≤≥±~～|]", spoken)
        if symbol:
            add_warning(
                warnings,
                line_number,
                "符号",
                f"仍包含未展开的符号：{symbol.group(0)!r}",
            )

    warnings.sort(key=lambda item: (item[0], item[1], item[2]))
    return warnings


def main() -> int:
    args = parse_args()
    try:
        text, label = read_text(args.path)
    except (OSError, UnicodeError) as exc:
        print(f"[错误] 无法读取 {args.path}：{exc}", file=sys.stderr)
        return 2

    warnings = lint(text)
    if not warnings:
        print(
            f"[通过] {label}：未发现可静态识别的 TTS 文本风险；"
            "仍需对照源稿检查读法和事实"
        )
        return 0

    print(f"[警告] {label}：发现 {len(warnings)} 个潜在问题")
    for line_number, kind, detail in warnings:
        print(f"  第 {line_number} 行：[{kind}] {detail}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
