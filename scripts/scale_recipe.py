#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""烘焙百分比份量換算。

用法：
  # A. 百分比 → 克數（給目標麵粉重量）
  python3 scale_recipe.py from-percent --flour 250 \
    --pct "高筋麵粉=100,水=80,鹽=2,糖=0.8,橄欖油=4,速發酵母=0.8"

  # B. 克數食譜 → 換成別的麵粉重量（自動抓麵粉當 100%）
  python3 scale_recipe.py rescale --to-flour 150 \
    --recipe "高筋麵粉=500,水=400,鹽=10,速發酵母=4"

  # C. 克數食譜 → 乘倍數
  python3 scale_recipe.py rescale --factor 0.5 \
    --recipe "高筋麵粉=500,水=400,鹽=10,速發酵母=4"

材料名含「粉 / 麵粉 / flour」視為麵粉基準；多種粉會相加當 100%。
可用 --flour-key 明確指定基準材料名。
"""
import argparse
import sys

FLOUR_HINTS = ("麵粉", "粉", "flour")


def parse_pairs(s):
    """'a=1,b=2' -> [(a,1.0),(b,2.0)]，保留順序。"""
    out = []
    for chunk in s.split(","):
        chunk = chunk.strip()
        if not chunk:
            continue
        if "=" not in chunk:
            print(f"格式錯誤：'{chunk}' 應為 名稱=數字")
            sys.exit(1)
        name, val = chunk.split("=", 1)
        try:
            out.append((name.strip(), float(val.strip())))
        except ValueError:
            print(f"數字錯誤：'{chunk}'")
            sys.exit(1)
    return out


def fmt(x):
    if abs(x) < 10:
        return f"{round(x, 2):g}"
    return f"{round(x, 1):g}"


def find_flour(pairs, flour_key):
    """回傳麵粉總量 (float)。多種粉相加。"""
    if flour_key:
        for n, v in pairs:
            if n == flour_key:
                return v
        print(f"找不到指定基準材料「{flour_key}」")
        sys.exit(1)
    total = sum(v for n, v in pairs if any(h in n.lower() for h in
               [h.lower() for h in FLOUR_HINTS]))
    if total <= 0:
        print("抓不到麵粉基準，請用 --flour-key 指定（例如 --flour-key 高筋麵粉）。")
        sys.exit(1)
    return total


def print_table(rows, total_label="總重"):
    w = max(len(n) for n, _ in rows)
    total = 0.0
    for n, v in rows:
        total += v
        print(f"  {n.ljust(w)}  {fmt(v).rjust(8)} g")
    print(f"  {'—' * (w + 11)}")
    print(f"  {total_label.ljust(w)}  {fmt(total).rjust(8)} g")


def cmd_from_percent(flour, pct_pairs, flour_key):
    # 找到基準百分比（麵粉那一列，通常=100）
    base_pct = None
    if flour_key:
        for n, v in pct_pairs:
            if n == flour_key:
                base_pct = v
    else:
        base_pct = sum(v for n, v in pct_pairs
                       if any(h.lower() in n.lower() for h in FLOUR_HINTS))
    if not base_pct:
        base_pct = 100.0
    factor = flour / base_pct  # 每 1% 對應的克數
    rows = [(n, v * factor) for n, v in pct_pairs]
    print(f"目標麵粉 {fmt(flour)} g（基準 {fmt(base_pct)}%）：\n")
    print_table(rows, "總麵團")
    _yeast_note(rows)


def cmd_rescale(recipe_pairs, to_flour, factor, flour_key):
    if to_flour is not None:
        cur_flour = find_flour(recipe_pairs, flour_key)
        factor = to_flour / cur_flour
        head = f"麵粉 {fmt(cur_flour)} → {fmt(to_flour)} g（×{fmt(factor)}）"
    else:
        head = f"全部 ×{fmt(factor)}"
    rows = [(n, v * factor) for n, v in recipe_pairs]
    print(head + "：\n")
    print_table(rows, "總重")
    _yeast_note(rows)


def _yeast_note(rows):
    for n, v in rows:
        if ("酵母" in n or "yeast" in n.lower()) and v < 1:
            print(f"\n※ {n} 僅 {fmt(v)} g（<1g）：建議用酵母水稀釋法——"
                  f"10g 酵母+100g 水攪勻，取 {fmt(v * 10)} g 酵母水，總水量記得扣掉。")
            break
    if any("酵母" in n or "yeast" in n.lower() for n, _ in rows):
        print("※ 放大縮小時酵母另依發酵時間/室溫調整（時間久、天熱→更少），見 references/scaling.md。")


def main():
    p = argparse.ArgumentParser(description="烘焙百分比份量換算")
    sub = p.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("from-percent", help="百分比 → 克數")
    a.add_argument("--flour", type=float, required=True, help="目標麵粉總重 (g)")
    a.add_argument("--pct", required=True, help='如 "高筋麵粉=100,水=80,鹽=2"')
    a.add_argument("--flour-key", default=None)

    b = sub.add_parser("rescale", help="克數食譜 → 換麵粉重量或乘倍數")
    b.add_argument("--recipe", required=True, help='如 "高筋麵粉=500,水=400,鹽=10"')
    g = b.add_mutually_exclusive_group(required=True)
    g.add_argument("--to-flour", type=float, help="目標麵粉總重 (g)")
    g.add_argument("--factor", type=float, help="直接乘的倍數")
    b.add_argument("--flour-key", default=None)

    args = p.parse_args()
    if args.cmd == "from-percent":
        cmd_from_percent(args.flour, parse_pairs(args.pct), args.flour_key)
    elif args.cmd == "rescale":
        cmd_rescale(parse_pairs(args.recipe), args.to_flour,
                    args.factor, args.flour_key)


if __name__ == "__main__":
    main()
