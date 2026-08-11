#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""發酵排程倒推 ＋ 溫度×時間×酵母三角換算。

用法：
  # A. 排程倒推：說好幾點「出爐」，倒推整條時間軸
  python3 ferment.py schedule --at "08:00"                     # cold-proof 歐包（預設）
  python3 ferment.py schedule --at "2026-08-15 08:00" --cold-hours 14
  python3 ferment.py schedule --at "18:00" --style same-day    # 直接法當天完成

  # B. 溫度換算：室溫不同，時間或酵母怎麼調
  python3 ferment.py adjust --hours 2 --from-temp 25 --to-temp 32
  python3 ferment.py adjust --hours 2 --from-temp 25 --to-temp 32 --yeast 3

  # C. 波蘭種配方：發酵時數＋室溫 → 酵母克數（rustic-bread.md §7 反比表＋溫度修正）
  python3 ferment.py poolish --flour 100 --hours 14 --temp 30

經驗法則：溫度每 ±8°C，發酵時間約減半/加倍（近似值，最終看狀態，
見 references/fermentation-guide.md）。
"""
import argparse
import sys
from datetime import datetime, timedelta

WEEKDAYS = "一二三四五六日"


def parse_at(s):
    """接受 'HH:MM'（自動抓下一個未來時間點）或 'YYYY-MM-DD HH:MM'。"""
    now = datetime.now()
    s = s.strip()
    try:
        return datetime.strptime(s, "%Y-%m-%d %H:%M")
    except ValueError:
        pass
    try:
        t = datetime.strptime(s, "%H:%M").time()
    except ValueError:
        print(f"看不懂時間「{s}」，請用 HH:MM 或 YYYY-MM-DD HH:MM")
        sys.exit(1)
    dt = datetime.combine(now.date(), t)
    if dt <= now:
        dt += timedelta(days=1)
    return dt


def fmt(dt):
    return f"{dt.month:02d}/{dt.day:02d}（週{WEEKDAYS[dt.weekday()]}）{dt:%H:%M}"


def print_timeline(steps, out_time):
    """steps: [(datetime, 標題, 附註)]，由早到晚印出。"""
    steps = sorted(steps, key=lambda x: x[0])
    span = out_time - steps[0][0]
    print(f"目標出爐：{fmt(out_time)}（全程約 {span.total_seconds() / 3600:.1f} 小時）\n")
    for dt, title, note in steps:
        line = f"  {fmt(dt)}  {title}"
        print(line)
        if note:
            print(f"{' ' * 22}└ {note}")
    now = datetime.now()
    if steps[0][0] < now:
        late = (now - steps[0][0]).total_seconds() / 3600
        earliest = now + span + timedelta(minutes=10)
        print(f"\n⚠️ 第一步已經過了 {late:.1f} 小時——來不及。現在馬上開始的話，"
              f"最早約 {fmt(earliest)} 出爐（用 --at 重排），或縮短 --poolish-hours / --cold-hours。")


def cmd_schedule(args):
    out = parse_at(args.at)
    if args.style == "cold-proof":
        if not (8 <= args.cold_hours <= 16):
            print("※ 冷藏發酵建議 10～14 小時（酵母偏多時別放滿 16），你設的值在常規範圍外。\n")
        bake_in = out - timedelta(minutes=args.bake_minutes)
        preheat = bake_in - timedelta(minutes=20)
        fridge = bake_in - timedelta(hours=args.cold_hours)
        shape = fridge - timedelta(minutes=10)
        preshape = shape - timedelta(minutes=25)
        bulk = preshape - timedelta(hours=args.bulk_hours)
        autolyse = bulk - timedelta(minutes=30)
        poolish = autolyse - timedelta(hours=args.poolish_hours)
        steps = [
            (poolish, "攪波蘭種",
             f"室溫過夜 {args.poolish_hours:g}h；酵母克數用 `ferment.py poolish --flour 粉量 "
             f"--hours {args.poolish_hours:g} --temp 室溫` 算；冷藏一天亦可"),
            (autolyse, "Autolyse：主麵團粉＋冰水拌到無粉粒", "靜置 30 分（台灣高溫 30 分剛好）"),
            (bulk, "加波蘭種＋鹽成團，開始 Bulk", "每 30 分摺疊一次 ×3，續發到約 1.8 倍"),
            (preshape, "預整形＋鬆弛", "刮板輕收鬆散圓、不排氣，鬆弛 20～30 分"),
            (shape, "最終整形，入藤籃/碗", "收緊表面張力，收口朝上"),
            (fridge, f"進冷藏 Cold Proof（{args.cold_hours:g} 小時）", "冷藏 10～14h 為安全範圍"),
            (preheat, "預熱：鍋＋鋁箔蓋 200°C", "15～20 分；氣炸鍋做麵包務必預熱"),
            (bake_in, "取出→倒扣→噴水霧→割線→進爐", "不退冰直接烤；十字、1cm、果斷"),
            (out, "出爐", f"加蓋 10～12 分後開蓋續烤；中心 96～98°C 才出爐（共約 {args.bake_minutes:g} 分）"),
        ]
        print("【Cold Proof 歐包排程】（基準流程：rustic-bread.md §3）\n")
        print_timeline(steps, out)
        print("\n※ 想更晚/更早進冷藏 → 調 --cold-hours（10～14h 內都行），整條往前後平移。")
    else:  # same-day 直接法
        bake_in = out - timedelta(minutes=args.bake_minutes)
        preheat = bake_in - timedelta(minutes=15)
        proof = bake_in - timedelta(minutes=60)
        shape = proof
        divide = shape - timedelta(minutes=25)
        bulk = divide - timedelta(hours=args.bulk_hours)
        mix = bulk - timedelta(minutes=15)
        steps = [
            (mix, "開始攪拌", "約 15 分（含出膜檢查）"),
            (bulk, f"Bulk 主發酵（{args.bulk_hours:g} 小時）", "發到約 2 倍，戳洞測試確認"),
            (divide, "分割滾圓＋中間鬆弛", "約 25 分"),
            (shape, "整形 → 最終發酵（60 分）", "發到約 1.5～2 倍、慢回彈"),
            (preheat, "預熱", "15 分"),
            (bake_in, "進爐", ""),
            (out, "出爐", f"烤約 {args.bake_minutes:g} 分（品項而異）"),
        ]
        print("【直接法當天排程】（餐包/吐司類基準）\n")
        print_timeline(steps, out)
        print("\n※ 台灣夏天室溫 30°C+ 時 bulk 會更快，提早檢查（時間 ×0.6～0.7 就先看）。")


# 波蘭種酵母反比表（rustic-bread.md §7；速發酵母 IDY，佔波蘭種粉重%，基準約 20°C）
POOLISH_TABLE = [(2, 2.5), (3, 1.5), (8, 0.5), (12, 0.2), (16, 0.1)]


def cmd_poolish(args):
    import math
    h = args.hours
    t = POOLISH_TABLE
    if h < t[0][0] or h > t[-1][0]:
        print(f"發酵時數建議在 {t[0][0]}～{t[-1][0]} 小時之間（你給的 {h:g}h 超出表格範圍）")
        sys.exit(1)
    # 對數空間內插（酵母量隨時間近似反比，線性內插會高估）
    for (h1, p1), (h2, p2) in zip(t, t[1:]):
        if h <= h2:
            k = (math.log(h) - math.log(h1)) / (math.log(h2) - math.log(h1))
            pct20 = math.exp(math.log(p1) + k * (math.log(p2) - math.log(p1)))
            break
    factor = 2 ** ((20 - args.temp) / 8.0)   # 比 20°C 熱 → 酵母要更少
    pct = pct20 * factor
    grams = args.flour * pct / 100
    print(f"波蘭種：粉 {args.flour:g} g ＋ 水 {args.flour:g} g（100% 水合）")
    print(f"室溫 {args.temp:g}°C 發 {h:g} 小時 → 速發酵母 {pct:.2f}%（20°C 基準 {pct20:.2f}% × 溫度倍率 {factor:.2f}）")
    print(f"\n→ 酵母 {grams:.2f} g")
    if grams < 1:
        print(f"   ※ <1g 用酵母水稀釋法：10g 酵母＋100g 水攪勻，取 {grams * 10:.1f} g 酵母水（主麵團總水量記得扣掉）")
    print("\n完成判斷：表面滿布氣泡、中心微微塌陷、拉開有絲、微酸酒香（fermentation-guide.md §4）。")
    print("※ 改冷藏一天亦可（成功基準流程作法）：酵母用 1g/100g 粉，冷藏 24h（rustic-bread.md §3）。")
    print("※ 新鮮酵母活性約速發的 1/3，用量 ×3。")


def cmd_adjust(args):
    factor = 2 ** ((args.from_temp - args.to_temp) / 8.0)
    new_hours = args.hours * factor
    print(f"基準：{args.from_temp:g}°C 發 {args.hours:g} 小時 → 現在 {args.to_temp:g}°C")
    print(f"（經驗法則：每 ±8°C 時間約減半/加倍；此處倍率 ×{factor:.2f}）\n")
    h = int(new_hours)
    m = round((new_hours - h) * 60)
    print(f"A. 酵母不變 → 時間改為約 {new_hours:.1f} 小時（{h}h{m:02d}m），提早開始檢查狀態")
    if args.yeast:
        new_yeast = args.yeast * factor
        print(f"B. 想維持 {args.hours:g} 小時 → 酵母 ×{factor:.2f}：{args.yeast:g} g → {new_yeast:.2f} g")
        if new_yeast < 1:
            print(f"   ※ <1g 用酵母水稀釋法：10g 酵母＋100g 水，取 {new_yeast * 10:.0f} g 酵母水（總水量記得扣）")
    else:
        print(f"B. 想維持原時間 → 酵母 ×{factor:.2f}（帶 --yeast 原克數幫你算）")
    if args.to_temp >= 35:
        print("\n⚠️ 35°C+ 發酵風味差、易過酸——建議減酵母＋找涼點（冷氣房），或改冷藏分擔。")
    elif args.to_temp <= 6:
        print("\n※ 6°C 以下（冷藏）發酵近乎停滯，適合 10 小時以上的 cold proof / cold bulk。")
    print("\n※ 近似值誤差會累積：時間只當鬧鐘，出爐與否看狀態（references/fermentation-guide.md）。")


def main():
    p = argparse.ArgumentParser(description="發酵排程倒推＋溫度換算")
    sub = p.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("schedule", help="從出爐時間倒推時間軸")
    a.add_argument("--at", required=True, help="出爐時間：HH:MM 或 YYYY-MM-DD HH:MM")
    a.add_argument("--style", choices=["cold-proof", "same-day"], default="cold-proof")
    a.add_argument("--cold-hours", type=float, default=12, help="冷藏發酵時數（預設 12，安全範圍 10~14）")
    a.add_argument("--poolish-hours", type=float, default=14, help="波蘭種發酵時數（預設 14）")
    a.add_argument("--bulk-hours", type=float, default=2.5, help="bulk 時數（cold-proof 預設 2.5 / same-day 建議 1.5~2）")
    a.add_argument("--bake-minutes", type=float, default=40, help="烘烤分鐘（cold-proof 預設 40 / same-day 常見 20~30）")

    b = sub.add_parser("adjust", help="溫度×時間×酵母換算")
    b.add_argument("--hours", type=float, required=True, help="基準溫度下的發酵時數")
    b.add_argument("--from-temp", type=float, required=True, help="食譜基準溫度 °C")
    b.add_argument("--to-temp", type=float, required=True, help="實際室溫 °C")
    b.add_argument("--yeast", type=float, default=0, help="原酵母克數（給了就算等效酵母量）")

    c = sub.add_parser("poolish", help="波蘭種酵母量：時數＋室溫 → 克數")
    c.add_argument("--flour", type=float, required=True, help="波蘭種粉量 (g)，水量同粉量")
    c.add_argument("--hours", type=float, required=True, help="室溫發酵時數（2~16）")
    c.add_argument("--temp", type=float, default=20, help="室溫 °C（預設 20，表格基準）")

    args = p.parse_args()
    if args.cmd == "schedule":
        if args.style == "same-day" and args.bulk_hours == 2.5:
            args.bulk_hours = 1.75
        if args.style == "same-day" and args.bake_minutes == 40:
            args.bake_minutes = 25
        cmd_schedule(args)
    elif args.cmd == "poolish":
        cmd_poolish(args)
    else:
        cmd_adjust(args)


if __name__ == "__main__":
    main()
