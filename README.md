# 🍞 baking-recipes — 烘焙與麵包 Skill

Renee 的個人烘焙助手（Claude Code / Claude 可用的 skill）。專長麵包。

## 功能
1. **烤箱 ↔ 氣炸鍋**：溫度/時間換算 + 氣炸鍋做麵包的實測限制。
2. **茶匙/湯匙 ↔ 公克/毫升**：依材料密度換算（麵粉、糖、鹽、酵母、油…）。
3. **各種麵種**：直接法、中種、湯種、波蘭種 Poolish、Biga、法式老麵、酸種的比例與製程。
4. **歐包實戰**：水合度計算、熱鍋蒸氣法、Cold Proof、整型指南。
5. **養酸種**：從零養種、餵養計算、台灣高溫調整。
6. **發酵管理**：排程倒推（幾點出爐→幾點開始）、溫度×時間×酵母換算、DDT 水溫計算、發酵判斷。
7. **份量換算**：用烘焙百分比放大縮小食譜。
8. **疑難排解**：失敗症狀對照表、台灣麵粉品牌筆記。

## 結構
```
SKILL.md              # 主入口（何時觸發 + 功能導覽 + 連動 Notion 食譜庫）
references/
  conversions.md      # 溫度/時間 + 計量單位對照表
  doughs.md           # 麵種比例與製程總表
  rustic-bread.md     # 歐包實戰：水合度分級、熱鍋蒸氣法、Cold Proof、波蘭種酵母表
  sourdough-starter.md # 養酸種天然酵母：從零養種、台灣高溫調整、維護與疑難排解
  scaling.md          # 烘焙百分比換算法 + 烤模/酵母對照
  fermentation-guide.md # 發酵判斷：1.8 倍怎麼抓、戳洞測試、過發 vs 不足、麵種成熟
  shaping.md          # 整型指南：預整形、boule/batard、高水合對策、滾圓/擀捲
  troubleshooting.md  # 失敗症狀對照表（攪拌/發酵/整形/烘烤/剖面 五區）
  flour-notes.md      # 台灣麵粉品牌筆記（蛋白質、吸水性、換粉守則）
scripts/
  convert.py          # 溫度/時間 + 單位換算器
  scale_recipe.py     # 烘焙百分比份量縮放
  hydration.py        # 總水合計算（正算 + 反推加水量，含麵種）
  ferment.py          # 發酵排程倒推 + 溫度×時間×酵母換算
  starter_feed.py     # 酸種餵養計算（比例→用量 + 到顛峰時間估算）
  ddt.py              # DDT 麵團溫度：反推水溫
```

## 常用指令
```bash
python3 scripts/convert.py oven2airfryer --temp 200 --minutes 20
python3 scripts/convert.py vol2g --ingredient 速發酵母 --tsp 2
python3 scripts/scale_recipe.py from-percent --flour 250 --pct "高筋麵粉=100,水=80,鹽=2"
python3 scripts/scale_recipe.py rescale --to-flour 150 --recipe "高筋麵粉=500,水=400,鹽=10"
python3 scripts/hydration.py calc --flour 300 --water 175 --preferment 200 --pre-hydration 100
python3 scripts/hydration.py target --hydration 69 --flour 300 --preferment 200 --pre-hydration 100
python3 scripts/ferment.py schedule --at "08:00"                    # 倒推 cold-proof 歐包時間軸
python3 scripts/ferment.py adjust --hours 2 --from-temp 25 --to-temp 32 --yeast 3
python3 scripts/ferment.py poolish --flour 100 --hours 14 --temp 30   # 波蘭種酵母克數
python3 scripts/starter_feed.py --keep 30 --ratio 1:5:5 --temp 32
python3 scripts/ddt.py --target 25 --room 32
```

## 食譜庫
現有食譜存在 Notion 🍽️ Recipe 資料庫，透過 Notion MCP 即時撈取（見 SKILL.md §5）。

已透過 `~/.claude/skills/baking-recipes` 符號連結啟用。
