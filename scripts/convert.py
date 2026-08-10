#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""烘焙換算器：烤箱↔氣炸鍋 溫度/時間、體積(茶匙/湯匙/杯)↔重量(公克)。

用法：
  python3 convert.py oven2airfryer --temp 200 --minutes 20
  python3 convert.py airfryer2oven --temp 180 --minutes 15
  python3 convert.py vol2g --ingredient 速發酵母 --tsp 2
  python3 convert.py vol2g --ingredient 細砂糖 --tbsp 1 --cup 0.5
  python3 convert.py g2vol --ingredient 高筋麵粉 --grams 120
  python3 convert.py list
"""
import argparse
import sys

# 每種材料：每 1 ml 的克數（密度）。表格值由 references/conversions.md 推導。
# tsp=5ml, tbsp=15ml, cup=240ml。
G_PER_ML = {
    "水": 1.0, "牛奶": 1.02,
    "高筋麵粉": 0.52, "中筋麵粉": 0.52, "低筋麵粉": 0.48,
    "玉米粉": 0.50, "麵粉": 0.52,
    "細砂糖": 0.80, "砂糖": 0.80, "糖": 0.80, "糖粉": 0.50,
    "二砂": 0.90, "紅糖": 0.90, "黑糖": 0.90,
    "鹽": 1.20, "精鹽": 1.20, "食鹽": 1.20, "海鹽": 1.00, "粗鹽": 1.00,
    "速發酵母": 0.60, "酵母": 0.60, "乾酵母": 0.60,
    "泡打粉": 0.80, "小蘇打": 0.92, "小蘇打粉": 0.92,
    "奶油": 0.94, "無鹽奶油": 0.94,
    "橄欖油": 0.90, "植物油": 0.90, "油": 0.90, "液體油": 0.90,
    "蜂蜜": 1.40, "糖漿": 1.40, "麥芽糖": 1.40,
    "可可粉": 0.42, "奶粉": 0.50,
}

TSP_ML, TBSP_ML, CUP_ML = 5.0, 15.0, 240.0


def _round(x):
    return round(x, 1) if x < 10 else round(x)


def cmd_oven2airfryer(temp, minutes, reverse=False):
    if reverse:  # 氣炸 -> 烤箱
        t_lo, t_hi = temp + 10, temp + 20
        m = minutes * 1.18 if minutes else None
        label_from, label_to = "氣炸鍋", "一般烤箱"
    else:        # 烤箱 -> 氣炸
        t_lo, t_hi = temp - 20, temp - 10
        m = minutes * 0.82 if minutes else None
        label_from, label_to = "一般烤箱", "氣炸鍋"
    print(f"{label_from} {temp}°C" + (f" / {minutes} 分" if minutes else ""))
    print(f"→ {label_to}：{t_lo:.0f}～{t_hi:.0f}°C", end="")
    if m:
        print(f"，約 {m:.0f} 分（提早 3～5 分開始盯上色）")
    else:
        print()
    if not reverse:
        print("提醒：做麵包氣炸鍋務必先預熱 10～15 分；氣炸烤箱無法上下火分離，蒸氣易被吹散。")


def _resolve(ingredient):
    if ingredient in G_PER_ML:
        return ingredient, G_PER_ML[ingredient]
    for k, v in G_PER_ML.items():        # 模糊：包含關係
        if k in ingredient or ingredient in k:
            return k, v
    return None, None


def cmd_vol2g(ingredient, tsp, tbsp, cup, ml):
    key, dens = _resolve(ingredient)
    if dens is None:
        print(f"找不到材料「{ingredient}」。用 `convert.py list` 看支援清單。")
        sys.exit(1)
    total_ml = tsp * TSP_ML + tbsp * TBSP_ML + cup * CUP_ML + ml
    grams = total_ml * dens
    parts = []
    if tsp: parts.append(f"{tsp:g} 茶匙")
    if tbsp: parts.append(f"{tbsp:g} 湯匙")
    if cup: parts.append(f"{cup:g} 杯")
    if ml: parts.append(f"{ml:g} ml")
    src = " + ".join(parts) if parts else "0"
    print(f"{key}：{src}（共 {total_ml:g} ml）≈ {_round(grams)} g")


def cmd_g2vol(ingredient, grams):
    key, dens = _resolve(ingredient)
    if dens is None:
        print(f"找不到材料「{ingredient}」。用 `convert.py list` 看支援清單。")
        sys.exit(1)
    ml = grams / dens
    print(f"{key}：{grams:g} g ≈ {ml:.1f} ml"
          f" = {ml / TBSP_ML:.1f} 湯匙 = {ml / TSP_ML:.1f} 茶匙")


def cmd_list():
    print("支援材料（密度 g/ml）：")
    seen = {}
    for k, v in G_PER_ML.items():
        seen.setdefault(v, []).append(k)
    for v in sorted(seen):
        print(f"  {v:>4}  " + "、".join(seen[v]))
    print("\n提示：1 茶匙=5ml、1 湯匙=15ml、1 杯=240ml。")


def main():
    p = argparse.ArgumentParser(description="烘焙換算器")
    sub = p.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("oven2airfryer", help="烤箱 → 氣炸鍋")
    a.add_argument("--temp", type=float, required=True)
    a.add_argument("--minutes", type=float, default=0)

    b = sub.add_parser("airfryer2oven", help="氣炸鍋 → 烤箱")
    b.add_argument("--temp", type=float, required=True)
    b.add_argument("--minutes", type=float, default=0)

    c = sub.add_parser("vol2g", help="體積 → 公克")
    c.add_argument("--ingredient", required=True)
    c.add_argument("--tsp", type=float, default=0, help="茶匙")
    c.add_argument("--tbsp", type=float, default=0, help="湯匙")
    c.add_argument("--cup", type=float, default=0, help="杯")
    c.add_argument("--ml", type=float, default=0)

    d = sub.add_parser("g2vol", help="公克 → 體積")
    d.add_argument("--ingredient", required=True)
    d.add_argument("--grams", type=float, required=True)

    sub.add_parser("list", help="列出支援材料")

    args = p.parse_args()
    if args.cmd == "oven2airfryer":
        cmd_oven2airfryer(args.temp, args.minutes, reverse=False)
    elif args.cmd == "airfryer2oven":
        cmd_oven2airfryer(args.temp, args.minutes, reverse=True)
    elif args.cmd == "vol2g":
        cmd_vol2g(args.ingredient, args.tsp, args.tbsp, args.cup, args.ml)
    elif args.cmd == "g2vol":
        cmd_g2vol(args.ingredient, args.grams)
    elif args.cmd == "list":
        cmd_list()


if __name__ == "__main__":
    main()
