# 🍞 baking-recipes — 烘焙與麵包 Skill

Renee 的個人烘焙助手（Claude Code / Claude 可用的 skill）。專長麵包。

## 四大功能
1. **烤箱 ↔ 氣炸鍋**：溫度/時間換算 + 氣炸鍋做麵包的實測限制。
2. **茶匙/湯匙 ↔ 公克/毫升**：依材料密度換算（麵粉、糖、鹽、酵母、油…）。
3. **各種麵種**：直接法、中種、湯種、波蘭種 Poolish、Biga、法式老麵、酸種的比例與製程。
4. **份量換算**：用烘焙百分比放大縮小食譜。

## 結構
```
SKILL.md              # 主入口（何時觸發 + 功能導覽 + 連動 Notion 食譜庫）
references/
  conversions.md      # 溫度/時間 + 計量單位對照表
  doughs.md           # 麵種比例與製程總表
  rustic-bread.md     # 歐包實戰：水合度分級、熱鍋蒸氣法、Cold Proof、波蘭種酵母表
  scaling.md          # 烘焙百分比換算法 + 烤模/酵母對照
scripts/
  convert.py          # 溫度/時間 + 單位換算器
  scale_recipe.py     # 烘焙百分比份量縮放
```

## 常用指令
```bash
python3 scripts/convert.py oven2airfryer --temp 200 --minutes 20
python3 scripts/convert.py vol2g --ingredient 速發酵母 --tsp 2
python3 scripts/scale_recipe.py from-percent --flour 250 --pct "高筋麵粉=100,水=80,鹽=2"
python3 scripts/scale_recipe.py rescale --to-flour 150 --recipe "高筋麵粉=500,水=400,鹽=10"
```

## 食譜庫
現有食譜存在 Notion 🍽️ Recipe 資料庫，透過 Notion MCP 即時撈取（見 SKILL.md §5）。

已透過 `~/.claude/skills/baking-recipes` 符號連結啟用。
