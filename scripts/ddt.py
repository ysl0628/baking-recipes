#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""麵團目標溫度 DDT (Desired Dough Temperature)：反推該用幾度的水。

夏天控溫關鍵：材料裡只有「水溫」最好控制，所以用它來抵銷室溫/粉溫/攪拌升溫。

公式（各因素平均分擔）：
  水溫 = 目標溫度 × N − (室溫 + 粉溫 [+ 麵種溫] + 摩擦升溫)
  N = 3（無麵種）或 4（有麵種）

用法：
  python3 ddt.py --target 25 --room 32                          # 免揉/手揉
  python3 ddt.py --target 25 --room 32 --mixer                  # 攪拌機
  python3 ddt.py --target 24 --room 33 --flour-temp 30 --preferment-temp 8

目標溫度參考：歐包 24～26°C、吐司/甜麵包（速發酵母）26～28°C。
"""
import argparse


def main():
    p = argparse.ArgumentParser(description="DDT 麵團溫度計算器")
    p.add_argument("--target", type=float, required=True, help="目標麵團溫度 °C（歐包 24~26、甜麵包 26~28）")
    p.add_argument("--room", type=float, required=True, help="室溫 °C")
    p.add_argument("--flour-temp", type=float, default=None, help="粉溫 °C（預設＝室溫）")
    p.add_argument("--preferment-temp", type=float, default=None,
                   help="麵種溫度 °C（有麵種才給；剛出冷藏約 5~8）")
    p.add_argument("--friction", type=float, default=None,
                   help="摩擦升溫 °C（預設：手揉/免揉 1、攪拌機 6）")
    p.add_argument("--mixer", action="store_true", help="用攪拌機（摩擦升溫預設改 6）")
    args = p.parse_args()

    flour_t = args.flour_temp if args.flour_temp is not None else args.room
    friction = args.friction if args.friction is not None else (6 if args.mixer else 1)

    factors = [("室溫", args.room), ("粉溫", flour_t), ("摩擦升溫", friction)]
    if args.preferment_temp is not None:
        factors.insert(2, ("麵種溫", args.preferment_temp))
    n = len(factors)
    water = args.target * n - sum(v for _, v in factors)

    print(f"目標麵團溫度 {args.target:g}°C（N={n}）")
    for name, v in factors:
        print(f"  {name}：{v:g}°C")
    print(f"\n→ 水溫 = {args.target:g}×{n} − ({' + '.join(f'{v:g}' for _, v in factors)}) = {water:.0f}°C")

    if water < 0:
        print("\n⚠️ 算出負值——光靠冰水壓不下來：")
        print("  - 水全用冰水（含冰塊，冰算進水重）")
        print("  - 粉先冷藏 30 分～1 小時再用")
        print("  - 免揉/減少攪拌時間、分次攪拌中間休息")
    elif water <= 15:
        print("\n※ 需要冰水：先放冰塊再補水到目標重量（冰塊算進總水重），或冷藏過的水。")
    elif water > 40:
        print("\n⚠️ 超過 40°C 會傷酵母——改用溫水上限 38°C，不足的靠環境保溫（發酵箱/烤箱燈）補。")

    print("\n※ 攪拌完實測麵團中心溫度，差 1~2°C 屬正常；連續做幾次就能校準自家的摩擦升溫值。")
    print("※ 麵團溫度每差 1°C，發酵快慢差約 10~15%——控溫比掐時間有效。")


if __name__ == "__main__":
    main()
