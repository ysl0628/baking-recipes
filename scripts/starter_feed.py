#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""酸種餵養計算器：比例 → 各加多少、預估幾小時到顛峰（含溫度修正）。

用法：
  python3 starter_feed.py --keep 30 --ratio 1:5:5 --temp 32      # 留 30g 種照 1:5:5 餵
  python3 starter_feed.py --target-total 330 --ratio 1:5:5       # 反推：想要總量 330g
  python3 starter_feed.py --keep 20 --ratio 1:2:2                # 日常維護（預設 25°C）

比例＝種:粉:水（重量比）。到顛峰基準時間見 references/sourdough-starter.md §5。
"""
import argparse
import sys

# 餵養倍數（粉÷種）→ 25°C 到顛峰的時間範圍（小時）。sourdough-starter.md §5。
PEAK_TABLE = [(1, 4, 6), (2, 6, 8), (5, 8, 12), (10, 12, 16)]


def parse_ratio(s):
    parts = s.replace("：", ":").split(":")
    if len(parts) != 3:
        print(f"比例格式錯誤「{s}」，應為 種:粉:水（如 1:5:5）")
        sys.exit(1)
    try:
        a, b, c = (float(x) for x in parts)
    except ValueError:
        print(f"比例要是數字：「{s}」")
        sys.exit(1)
    if a <= 0 or b <= 0:
        print("種與粉的比例必須 > 0")
        sys.exit(1)
    return a, b, c


def peak_hours(feed_mult):
    """線性內插 25°C 的到顛峰時間範圍。"""
    t = PEAK_TABLE
    if feed_mult <= t[0][0]:
        return t[0][1], t[0][2]
    for (x1, lo1, hi1), (x2, lo2, hi2) in zip(t, t[1:]):
        if feed_mult <= x2:
            k = (feed_mult - x1) / (x2 - x1)
            return lo1 + k * (lo2 - lo1), hi1 + k * (hi2 - hi1)
    return t[-1][1], t[-1][2]


def main():
    p = argparse.ArgumentParser(description="酸種餵養計算器")
    p.add_argument("--ratio", required=True, help="種:粉:水，如 1:1:1 / 1:2:2 / 1:5:5")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--keep", type=float, help="留下的種量 (g)")
    g.add_argument("--target-total", type=float, help="想要的餵後總量 (g)，反推留種量")
    p.add_argument("--temp", type=float, default=25, help="環境溫度 °C（預設 25）")
    args = p.parse_args()

    a, b, c = parse_ratio(args.ratio)
    if args.keep:
        keep = args.keep
    else:
        keep = args.target_total * a / (a + b + c)
    flour = keep * b / a
    water = keep * c / a
    total = keep + flour + water

    print(f"比例 {a:g}:{b:g}:{c:g}（種:粉:水）@ {args.temp:g}°C\n")
    print(f"  留種    {keep:6.0f} g")
    print(f"  加麵粉  {flour:6.0f} g")
    print(f"  加水    {water:6.0f} g")
    print(f"  ─────────────")
    print(f"  餵後總量 {total:5.0f} g")

    if c != b:
        h = c / b * 100
        print(f"\n※ 粉水比 {h:.0f}%：{'偏稠（硬種），發得慢、較耐放' if h < 100 else '偏稀（液種），發得快、偏酸'}"
              f"——一般維護建議 100%（粉=水）。")

    # 到顛峰時間：25°C 基準 × 溫度倍率（每 ±8°C 減半/加倍）
    lo, hi = peak_hours(b / a)
    factor = 2 ** ((25 - args.temp) / 8.0)
    lo_t, hi_t = lo * factor, hi * factor
    print(f"\n預估到顛峰：約 {lo_t:.1f}～{hi_t:.1f} 小時"
          f"（25°C 基準 {lo:.0f}~{hi:.0f}h × 溫度倍率 {factor:.2f}）")
    print("→ 用種時機：升到最高點、微微回落前活性最好。")

    if args.temp >= 30:
        print("\n【台灣高溫提醒】30°C+ 菌相容易失衡：")
        print("  - 活性期改 8～12h 餵一次，或拉大比例（1:5:5 更耐放）")
        print("  - 過酸（刺鼻醋味）→ 1:5:5 連餵 2～3 次洗種")
        print("  - 找涼點：冷氣房、陰涼角落，別放窗邊或電器旁")
    if args.temp <= 10:
        print("\n※ 10°C 以下（冷藏）幾乎停滯：適合保存，每週取出餵一次即可。")
    if keep < 10:
        print(f"\n※ 留種只有 {keep:.0f} g：太少不穩定，建議至少留 10～20 g。")


if __name__ == "__main__":
    main()
