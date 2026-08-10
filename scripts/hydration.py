#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""總水合計算器：總水合 = 總水 ÷ 總粉（含麵種）。

用法：
  # 正算：主麵團 + 麵種 → 總水合%
  python3 hydration.py calc --flour 300 --water 175 --pre-flour 100 --pre-water 100

  # 麵種懶得拆：給總重 + 含水比（波蘭種=100、湯種=500、Biga=50~60）
  python3 hydration.py calc --flour 300 --water 175 --preferment 200 --pre-hydration 100

  # 反推：想要的總水合% → 主麵團該加多少水
  python3 hydration.py target --hydration 69 --flour 300 --preferment 200 --pre-hydration 100

分級表與實測經驗見 references/rustic-bread.md §1。
"""
import argparse
import sys

# (下限, 上限, 分級, 說明)
BANDS = [
    (0, 60, "低水合", "偏乾硬的麵團（貝果、部分吐司）"),
    (60, 65, "中低水合", "吐司、一般麵包"),
    (65, 70, "中高水合（入門歐包安全區）", "第一次做歐包從這裡開始（實測 69% 全程順利）"),
    (70, 75, "高水合", "開始需要技巧：後加水法 bassinage＋多摺疊"),
    (75, 999, "高水合進階（高風險區）", "筋撐不住的區域（實測前兩次栽在 75%）"),
]


def split_preferment(args):
    """回傳 (麵種粉, 麵種水)。--pre-flour/--pre-water 優先；否則由總重+含水比拆。"""
    if args.pre_flour or args.pre_water:
        return args.pre_flour, args.pre_water
    if args.preferment:
        h = args.pre_hydration / 100.0
        pf = args.preferment / (1 + h)
        return pf, args.preferment - pf
    return 0.0, 0.0


def band_of(pct):
    for lo, hi, name, note in BANDS:
        if lo <= pct < hi:
            return name, note
    return "?", ""


def report(total_flour, total_water, pre_flour, pre_water):
    pct = total_water / total_flour * 100
    name, note = band_of(pct)
    print(f"總粉 {total_flour:g} g（主麵團 {total_flour - pre_flour:g} + 麵種 {pre_flour:g}）")
    print(f"總水 {total_water:g} g（主麵團 {total_water - pre_water:g} + 麵種 {pre_water:g}）")
    print(f"\n總水合 = {total_water:g} ÷ {total_flour:g} = {pct:.1f}%")
    print(f"→ 分級：{name}——{note}")
    if pct >= 75:
        print("⚠️ 75%+ 連鎖後果：牽絲就斷 → 發酵往旁攤 → 整形站不住 → 扁＋細密孔 → 中心難熟。")
        print("   建議先降回 65～70% 打好基準，要挑戰請用後加水法＋4~5 次摺疊（rustic-bread.md §5）。")
    elif pct >= 70:
        print("※ 70%+ 建議：autolyse 先保留部分水，摺疊 1~2 次後再分次加（後加水法）。")
    print("\n※ 含牛奶/蛋的食譜：牛奶約 87% 是水、全蛋約 75% 是水，折算後併入水量再算。")


def cmd_calc(args):
    pre_flour, pre_water = split_preferment(args)
    total_flour = args.flour + pre_flour
    total_water = args.water + pre_water
    if total_flour <= 0:
        print("總粉不能為 0")
        sys.exit(1)
    report(total_flour, total_water, pre_flour, pre_water)


def cmd_target(args):
    pre_flour, pre_water = split_preferment(args)
    total_flour = args.flour + pre_flour
    need_water = args.hydration / 100.0 * total_flour
    main_water = need_water - pre_water
    print(f"目標總水合 {args.hydration:g}%，總粉 {total_flour:g} g（主麵團 {args.flour:g} + 麵種 {pre_flour:g}）")
    print(f"需要總水 {need_water:.0f} g，麵種已含 {pre_water:g} g")
    if main_water < 0:
        print(f"⚠️ 麵種的水已超過目標 {-main_water:.0f} g——降不下去。請減少麵種量或提高目標水合。")
        sys.exit(1)
    print(f"\n→ 主麵團加水 {main_water:.0f} g")
    name, note = band_of(args.hydration)
    print(f"→ 分級：{name}——{note}")
    print("\n※ 歐包建議用冰水（配合台灣高溫控制麵團溫度，見 scripts/ddt.py）。")


def main():
    p = argparse.ArgumentParser(description="總水合計算器（含麵種）")
    sub = p.add_subparsers(dest="cmd", required=True)

    def common(sp, with_water, with_target):
        sp.add_argument("--flour", type=float, required=True, help="主麵團麵粉 (g)，不含麵種")
        if with_water:
            sp.add_argument("--water", type=float, required=True, help="主麵團水 (g)，不含麵種")
        if with_target:
            sp.add_argument("--hydration", type=float, required=True, help="目標總水合 %%（如 69）")
        sp.add_argument("--pre-flour", type=float, default=0, help="麵種內的粉 (g)")
        sp.add_argument("--pre-water", type=float, default=0, help="麵種內的水 (g)")
        sp.add_argument("--preferment", type=float, default=0, help="麵種總重 (g)（懶人法，搭配 --pre-hydration）")
        sp.add_argument("--pre-hydration", type=float, default=100,
                        help="麵種含水比 %%：波蘭種 100、湯種 500、Biga 50~60、老麵約 65（預設 100）")

    a = sub.add_parser("calc", help="正算總水合%")
    common(a, with_water=True, with_target=False)

    b = sub.add_parser("target", help="反推主麵團加水量")
    common(b, with_water=False, with_target=True)

    args = p.parse_args()
    if args.cmd == "calc":
        cmd_calc(args)
    else:
        cmd_target(args)


if __name__ == "__main__":
    main()
