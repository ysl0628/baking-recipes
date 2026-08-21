#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""酸種麵包排程倒推：給出爐時間 → 倒推每一步的時刻，可輸出 .ics 行事曆。

⚠️ 這支是「酸種（天然酵母）」專用。商業酵母波蘭種麵包請用 ferment.py schedule
   ——兩者的 bulk 終點判準完全不同（見 references/fermentation-guide.md §1）。

用法：
  # 一條龍（室溫 bulk → 整形 → 單次冷藏 → 烤）
  python3 sourdough_schedule.py --bake-at "2026-08-25 10:00" --dough-temp 26

  # 兩段冷藏（混合後冷藏 → 整形後再冷藏，風味更佳）
  python3 sourdough_schedule.py --bake-at "10:00" --dough-temp 24 \
      --mode two-stage --cold-hours 8 --cold-hours-2 10

  # 當天做完不冷藏
  python3 sourdough_schedule.py --bake-at "18:00" --dough-temp 27 --mode same-day

  # 順便輸出行事曆
  python3 sourdough_schedule.py --bake-at "10:00" --dough-temp 26 --ics plan.ics

🌡️ --dough-temp 是**麵團溫度**，不是室溫，也不是氣象預報的氣溫。
   兩者常差 1～3°C，而 bulk 終點是麵團溫度的函數。攪拌完插溫度計量一次。
"""
import argparse
import re
import sys
from datetime import datetime, timedelta, timezone

# ── 雙因子法：麵團溫度 → (目標漲幅 %, bulk 時數 lo, hi) ─────────────────
# 來源：The Sourdough Journey（fermentation-guide.md §1）。30°C 那列為台灣高溫外推。
BULK_TABLE = [
    (30, 22, 2.5, 4.0),
    (27, 30, 3.5, 5.5),
    (24, 50, 5.0, 7.0),
    (21, 75, 8.0, 12.0),
    (18, 100, 12.0, 16.0),
]

# 餵養倍數（粉÷種）→ 25°C 到顛峰時數。與 starter_feed.py 同表。
PEAK_TABLE = [(1, 4, 6), (2, 6, 8), (5, 8, 12), (10, 12, 16)]


def interp(x, table):
    """table 依第一欄遞減排列，回傳其餘欄位的線性內插值。"""
    if x >= table[0][0]:
        return table[0][1:], x > table[0][0]
    if x <= table[-1][0]:
        return table[-1][1:], x < table[-1][0]
    for hi, lo in zip(table, table[1:]):
        if lo[0] <= x <= hi[0]:
            k = (x - lo[0]) / (hi[0] - lo[0])
            return tuple(l + k * (h - l) for l, h in zip(lo[1:], hi[1:])), False
    return table[-1][1:], True


def parse_ratio(s):
    parts = s.replace("：", ":").split(":")
    if len(parts) != 3:
        sys.exit(f"levain 比例格式錯誤「{s}」，應為 種:粉:水（如 1:5:5）")
    try:
        a, b, c = (float(x) for x in parts)
    except ValueError:
        sys.exit(f"比例要是數字：「{s}」")
    if a <= 0 or b <= 0:
        sys.exit("種與粉的比例必須 > 0")
    return a, b, c


def levain_peak_hours(feed_mult, temp):
    t = PEAK_TABLE
    if feed_mult <= t[0][0]:
        lo, hi = t[0][1], t[0][2]
    else:
        lo, hi = t[-1][1], t[-1][2]
        for (x1, l1, h1), (x2, l2, h2) in zip(t, t[1:]):
            if feed_mult <= x2:
                k = (feed_mult - x1) / (x2 - x1)
                lo, hi = l1 + k * (l2 - l1), h1 + k * (h2 - h1)
                break
    factor = 2 ** ((25 - temp) / 8.0)
    return lo * factor, hi * factor


def parse_when(s):
    s = s.strip()
    if re.fullmatch(r"\d{1,2}:\d{2}", s):
        today = datetime.now().replace(second=0, microsecond=0)
        h, m = (int(x) for x in s.split(":"))
        when = today.replace(hour=h, minute=m)
        if when <= today:
            when += timedelta(days=1)
        return when
    for fmt in ("%Y-%m-%d %H:%M", "%Y/%m/%d %H:%M", "%m-%d %H:%M", "%m/%d %H:%M"):
        try:
            d = datetime.strptime(s, fmt)
        except ValueError:
            continue
        if d.year == 1900:
            d = d.replace(year=datetime.now().year)
        return d
    sys.exit(f'時間格式看不懂「{s}」。用 "HH:MM" 或 "YYYY-MM-DD HH:MM"。')


def build(args):
    """回傳 [(時刻, 步驟名, 說明), ...]，由出爐往回推。"""
    bake_end = parse_when(args.bake_at)
    (rise_pct, bulk_lo, bulk_hi), extrapolated = interp(args.dough_temp, BULK_TABLE)
    bulk_mid = (bulk_lo + bulk_hi) / 2

    steps = []          # (datetime, name, note)
    t = bake_end
    steps.append((t, "出爐", f"中心 96～98°C；完全放涼再切（標準 1 小時）"))

    t -= timedelta(minutes=args.bake_minutes)
    steps.append((t, "進爐", f"烘烤 {args.bake_minutes} 分；前段加蓋補蒸氣"))

    preheat_start = t - timedelta(minutes=args.preheat)
    steps.append((preheat_start, "開始預熱", f"預熱 {args.preheat} 分（氣炸烤箱務必預熱）"))

    if args.mode == "same-day":
        t -= timedelta(hours=args.final_hours)
        steps.append((t, "整形完成→最後發酵",
                      f"室溫 {args.final_hours:g}h；戳洞測試：慢回彈留淺痕＝進爐"))
    else:
        cold2 = args.cold_hours_2 if args.mode == "two-stage" else args.cold_hours
        t -= timedelta(hours=cold2)
        steps.append((t, "整形完成→進冷藏", f"冷藏最後發酵 {cold2:g}h；不退冰直接倒扣、割線、進爐"))

    t -= timedelta(minutes=args.shape)
    steps.append((t, "整形", "輕手不排氣；收口捏緊（shaping.md）"))

    t -= timedelta(minutes=args.bench)
    steps.append((t, "預整形 + bench rest", f"預整形後鬆弛 {args.bench} 分"))

    if args.mode == "two-stage":
        t -= timedelta(hours=args.cold_hours)
        steps.append((t, "第一次冷藏結束→取出", f"冷藏 bulk {args.cold_hours:g}h 結束，回溫後預整形"))
        room_bulk = max(bulk_mid * args.warm_frac, 0.5)
        t -= timedelta(hours=room_bulk)
        bulk_start = t
        steps.append((t, "混合完成→室溫 bulk（部分）",
                      f"室溫發到約目標漲幅的 {args.warm_frac:.0%}（約 {room_bulk:.1f}h）再進冷藏"))
    else:
        t -= timedelta(hours=bulk_mid)
        bulk_start = t
        steps.append((t, "混合完成→bulk 開始",
                      f"目標 +{rise_pct:.0f}%（{bulk_lo:.1f}～{bulk_hi:.1f}h）"
                      f"｜⚠️ 看漲幅不看時鐘"))

    # 摺疊：bulk 開始後每 30 分一次，最多 4 次
    for i in range(1, 5):
        ft = bulk_start + timedelta(minutes=30 * i)
        steps.append((ft, f"摺疊第 {i} 次", "bulk 期間；後段可改輕柔 coil fold"))

    t = bulk_start - timedelta(minutes=args.mix)
    steps.append((t, "混合（加 levain + 鹽）", f"混合約 {args.mix} 分鐘"))

    if args.autolyse > 0:
        t -= timedelta(minutes=args.autolyse)
        steps.append((t, "Autolyse 開始（粉＋水）",
                      f"靜置 {args.autolyse} 分——**看主麵團裡有多少全穀**：白粉 30～60 分、"
                      f"含全穀 60～90 分、>50% 全穀 2h+（mixing.md）"))

    a, b, c = parse_ratio(args.levain_ratio)
    lv_lo, lv_hi = levain_peak_hours(b / a, args.levain_temp)
    lv_mid = (lv_lo + lv_hi) / 2
    mix_time = next(s[0] for s in steps if s[1].startswith("混合（"))
    t = mix_time - timedelta(hours=lv_mid)
    steps.append((t, "建 levain",
                  f"{args.levain_ratio} @ {args.levain_temp:g}°C，約 {lv_lo:.1f}～{lv_hi:.1f}h 到頂"
                  f"｜⚠️ 圓頂轉平才是 peak"))

    steps.sort(key=lambda s: s[0])
    return steps, dict(rise_pct=rise_pct, bulk_lo=bulk_lo, bulk_hi=bulk_hi,
                       lv_lo=lv_lo, lv_hi=lv_hi, extrapolated=extrapolated)


def esc(s):
    return (s.replace("\\", "\\\\").replace(";", r"\;")
             .replace(",", r"\,").replace("\n", r"\n"))


def fold_line(line):
    """ICS 每行 75 octets 折行。"""
    out, buf = [], b""
    for ch in line:
        e = ch.encode("utf-8")
        if len(buf) + len(e) > 73:
            out.append(buf.decode("utf-8"))
            buf = b" "
        buf += e
    out.append(buf.decode("utf-8"))
    return "\r\n".join(out)


def write_ics(steps, path, alarm_min):
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    lines = ["BEGIN:VCALENDAR", "VERSION:2.0",
             "PRODID:-//baking-recipes//sourdough-schedule//ZH", "CALSCALE:GREGORIAN"]
    for i, (when, name, note) in enumerate(steps):
        lines += [
            "BEGIN:VEVENT",
            f"UID:sd-{stamp}-{i}@baking-recipes",
            f"DTSTAMP:{stamp}",
            f"DTSTART:{when.strftime('%Y%m%dT%H%M%S')}",
            "DURATION:PT10M",
            fold_line(f"SUMMARY:🍞 {esc(name)}"),
            fold_line(f"DESCRIPTION:{esc(note)}"),
            "BEGIN:VALARM", f"TRIGGER:-PT{alarm_min}M", "ACTION:DISPLAY",
            fold_line(f"DESCRIPTION:{esc(name)}"), "END:VALARM",
            "END:VEVENT",
        ]
    lines.append("END:VCALENDAR")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write("\r\n".join(lines) + "\r\n")


def main():
    p = argparse.ArgumentParser(description="酸種麵包排程倒推（含 .ics 輸出）")
    p.add_argument("--bake-at", required=True, help='出爐時間："HH:MM" 或 "YYYY-MM-DD HH:MM"')
    p.add_argument("--dough-temp", type=float, required=True,
                   help="⚠️ 麵團溫度 °C（不是室溫、不是氣象預報）")
    p.add_argument("--mode", choices=["one-stage", "two-stage", "same-day"],
                   default="one-stage",
                   help="one-stage=室溫bulk→整形→單次冷藏；two-stage=兩段冷藏；same-day=全室溫")
    p.add_argument("--levain-ratio", default="1:5:5", help="種:粉:水（預設 1:5:5 過夜）")
    p.add_argument("--levain-temp", type=float, default=None, help="levain 環境溫度（預設同麵團溫度）")
    p.add_argument("--cold-hours", type=float, default=12, help="冷藏時數（two-stage 時為第一次）")
    p.add_argument("--cold-hours-2", type=float, default=10, help="two-stage 的第二次冷藏時數")
    p.add_argument("--warm-frac", type=float, default=0.6,
                   help="two-stage：進冷藏前室溫先發到目標的幾成（預設 0.6）")
    p.add_argument("--final-hours", type=float, default=2.5, help="same-day 的室溫最後發酵時數")
    p.add_argument("--autolyse", type=int, default=30, help="autolyse 分鐘（0＝不做）")
    p.add_argument("--mix", type=int, default=15, help="混合分鐘")
    p.add_argument("--bench", type=int, default=25, help="預整形後鬆弛分鐘")
    p.add_argument("--shape", type=int, default=15, help="整形分鐘")
    p.add_argument("--preheat", type=int, default=30, help="預熱分鐘")
    p.add_argument("--bake-minutes", type=int, default=45, help="烘烤分鐘")
    p.add_argument("--protein", type=float, default=None, help="麵粉蛋白質 %%（>12.5 會提示上調漲幅）")
    p.add_argument("--ics", help="輸出 .ics 檔路徑")
    p.add_argument("--alarm", type=int, default=10, help=".ics 提前幾分鐘提醒（預設 10）")
    args = p.parse_args()

    if args.levain_temp is None:
        args.levain_temp = args.dough_temp

    steps, info = build(args)

    mode_name = {"one-stage": "一條龍（單次冷藏）", "two-stage": "兩段冷藏",
                 "same-day": "當天完成（全室溫）"}[args.mode]
    print(f"酸種排程｜{mode_name}｜麵團溫度 {args.dough_temp:g}°C\n")
    print(f"  bulk 目標漲幅 **+{info['rise_pct']:.0f}%**"
          f"（約 {info['bulk_lo']:.1f}～{info['bulk_hi']:.1f} 小時）")
    if args.protein and args.protein > 12.5:
        print(f"  ※ 蛋白質 {args.protein:g}% > 12.5% → 目標漲幅上調 5～10pp，"
              f"改抓 +{info['rise_pct']+5:.0f}～{info['rise_pct']+10:.0f}%")
    print(f"  levain 到頂 約 {info['lv_lo']:.1f}～{info['lv_hi']:.1f} 小時\n")

    day = None
    for when, name, note in steps:
        if when.date() != day:
            day = when.date()
            print(f"── {day:%m/%d (%a)} ──")
        print(f"  {when:%H:%M}  {name}")
        if note:
            print(f"          └ {note}")

    first, now = steps[0][0], datetime.now().replace(second=0, microsecond=0)
    if first < now:
        short = (now - first).total_seconds() / 3600
        lead = (parse_when(args.bake_at) - first).total_seconds() / 3600
        print(f"\n🚨 **來不及**：第一步（{steps[0][1]}）落在 {first:%m/%d %H:%M}，"
              f"已經過去 {short:.1f} 小時。")
        print(f"   這個流程總共需要 {lead:.1f} 小時前置。若現在開始，"
              f"最早能出爐的時間是 **{(now + timedelta(hours=lead)):%m/%d %H:%M}**。")
        print("   縮短的辦法：拉高麵團溫度（bulk 變快）、改小 levain 比例"
              "（如 1:2:2 到頂較快）、或縮短冷藏時數。")

    print("\n⚠️ 時間只是鬧鐘，終點永遠看狀態：")
    print("   bulk → 漲幅（直壁容器標線）＋邊緣拱起＋jiggle，不是看時鐘")
    print("   最後發酵 → 戳洞測試（冷藏麵團不準，改看體積與表面氣泡）")
    print("   成品驗收 → 剖面看「壁」是脊還是塊（troubleshooting.md §0 強制步驟）")

    if info["extrapolated"]:
        print(f"\n⚠️ 麵團溫度 {args.dough_temp:g}°C 在雙因子表（18～30°C）之外，"
              f"上面的數字是外推值，請當粗估。")
    if args.dough_temp >= 29:
        print("\n【高溫警告】麵團 29°C+：protease 開始快速吃掉麵筋，"
              "30～60 分內可能從剛好崩到救不回來。")
        print("   → 寧可早收；更根本的做法是用冰水把麵溫壓到 24～26°C（ddt.py）。")

    if args.ics:
        write_ics(steps, args.ics, args.alarm)
        print(f"\n✅ 已輸出行事曆：{args.ics}（{len(steps)} 個提醒，各提前 {args.alarm} 分）")
        print("   匯入方式：手機點開檔案 → 加入行事曆；或 Google 日曆「匯入」。")


if __name__ == "__main__":
    main()
