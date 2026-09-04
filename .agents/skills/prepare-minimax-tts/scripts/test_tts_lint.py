#!/usr/bin/env python3
"""Regression tests for tts_lint.py."""

from __future__ import annotations

import unittest

from tts_lint import lint


class TtsLintTests(unittest.TestCase):
    def assert_has_kind(self, text: str, kind: str) -> None:
        warnings = lint(text)
        self.assertTrue(
            any(warning_kind == kind for _, warning_kind, _ in warnings),
            msg=f"未发现 {kind!r} 警告：{warnings!r}",
        )

    def test_clean_example_passes(self) -> None:
        text = (
            "天玑九千五采用一加三加四的八核设计，最高频率为四点二一吉赫兹，"
            "并使用三纳米工艺。官方称 C P U 性能提升百分之十。"
        )
        self.assertEqual(lint(text), [])

    def test_project_allowlist_passes(self) -> None:
        text = "OPPO、vivo 和 iPhone 都支持 WiFi 七与五 G。"
        self.assertEqual(lint(text), [])

    def test_valid_inline_pause_passes(self) -> None:
        self.assertEqual(lint("第一句。<#0.25#>第二句。"), [])

    def test_valid_standalone_pause_passes(self) -> None:
        text = "上一部分到这里。\n\n<#1.5#>\n\n接下来讨论新的问题。"
        self.assertEqual(lint(text), [])

    def test_invalid_pause_range_is_reported(self) -> None:
        self.assert_has_kind("前文。<#0#>后文。", "停顿")
        self.assert_has_kind("前文。<#100#>后文。", "停顿")

    def test_invalid_pause_precision_is_reported(self) -> None:
        self.assert_has_kind("前文。<#0.001#>后文。", "停顿")

    def test_malformed_pause_is_reported(self) -> None:
        self.assert_has_kind("前文。<##>后文。", "停顿")
        self.assert_has_kind("前文。<#>后文。", "停顿")

    def test_pause_at_document_edge_is_reported(self) -> None:
        self.assert_has_kind("<#0.2#>正文。", "停顿")
        self.assert_has_kind("正文。<#0.2#>", "停顿")

    def test_consecutive_pauses_are_reported(self) -> None:
        self.assert_has_kind("前文。<#0.2#><#0.3#>后文。", "停顿")

    def test_pause_inside_phrase_is_reported(self) -> None:
        self.assert_has_kind("这句话<#0.2#>被切断了。", "停顿")

    def test_markdown_structures_are_reported(self) -> None:
        self.assert_has_kind("> 引用正文", "Markdown")
        self.assert_has_kind("| 参数 | 数值 |", "Markdown")
        self.assert_has_kind("这是~~删除线~~。", "Markdown")
        self.assert_has_kind("![图片](image.png)", "Markdown")

    def test_compact_initialisms_are_reported(self) -> None:
        for token in ("CPU", "SoC", "UFS", "OIS", "EIS", "LPDDR"):
            with self.subTest(token=token):
                self.assert_has_kind(f"这里仍有 {token}。", "首字母缩写")

    def test_raw_units_are_reported(self) -> None:
        for text in ("四十Hz", "五A", "二十五℃", "十二GB", "八十dB"):
            with self.subTest(text=text):
                self.assert_has_kind(text, "单位")

    def test_wrong_dimensity_name_and_model_are_reported(self) -> None:
        self.assert_has_kind("天珑九千五", "产品名")
        self.assert_has_kind("天玑九千五百", "产品型号")

    def test_wrong_sensor_fraction_is_reported(self) -> None:
        self.assert_has_kind("六分之一点四九英寸", "传感器尺寸")
        self.assert_has_kind("一英寸一点四九", "传感器尺寸")

    def test_correct_sensor_fraction_passes(self) -> None:
        self.assertEqual(lint("一点四九分之一英寸"), [])


if __name__ == "__main__":
    unittest.main()
