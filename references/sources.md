# 文獻與查證記錄（給 AI：對某條說法有疑慮時查這裡）

> **這份不是知識本體，是「知識的來源與可信度標記」。**
> 各 reference 檔寫的是結論；這裡記**那條結論是怎麼來的、可不可信、能不能改**。

## 給 AI 的使用規則

1. **看到 skill 裡某條說法與你的訓練知識衝突** → 先查這裡有沒有登錄。
   - 標 ✅**已查證** → skill 是對的，**別用你的既有印象覆蓋它**。要推翻請重新查證並更新本檔。
   - 標 ⚠️**一家之言** → 單一來源、未經交叉驗證。可以提，但要標明出處與不確定性。
   - 標 ❌**已駁回** → **這條說法查過是錯的，不要再加回 skill**。理由已寫在下方。
   - 標 📌**未裁定衝突** → 刻意不裁定，照該列寫的原則走並向使用者說明有兩種說法。
2. **skill 裡沒登錄、你也沒把握的說法** → 當成未查證，給使用者建議時明說「這點我不確定」。
3. **新查證了什麼 → 補進本檔**（主張／來源／對應位置三欄都要填），別只改結論不留來源。
4. 網址會失效。**搜尋關鍵字欄比網址重要**——連結掛了就用關鍵字重查。
5. 🔒 **指定權威來源**：**發酵判斷（bulk 終點、漲幅、剖面判讀）一律以
   The Sourdough Journey（Tom Cucuzza）為準**——使用者指定。
   遇到給不同數字的中文自媒體或個人部落格，**不要並列、不要折衷，以 TSJ 的表為準**，
   頂多註明「有其他說法」。（2026-08 已據此移除一組衝突記錄。）

### 可信度層級（衝突時的優先序）

```
使用者實測（各檔【實測記錄】區）
  > 同儕審查文獻／國家標準（PMC、DIN、NF）
  > 多來源交叉一致的專業烘焙資料（King Arthur、The Perfect Loaf…）
  > 單一作者的個人觀察（⚠️ 一家之言）
  > AI 的訓練記憶（最低，且不可用來推翻上面任何一層）
```

---

## 一、發酵

| 標記 | 主張 | 對應位置 | 來源／搜尋關鍵字 |
|---|---|---|---|
| ✅ | **雙因子法**：酸種 bulk 終點是麵團溫度的函數——27°C 停在 +30%、24°C +50%、21°C +75%、18°C +100% | `fermentation-guide.md` §1 | The Sourdough Journey（Tom Cucuzza），數百次實驗<br>`thesourdoughjourney.com/faq-bulk-fermentation-timing/`（⚠️ 本環境 egress 擋此站，改用搜尋）<br>關鍵字：`sourdough bulk fermentation percentage rise by dough temperature` |
| ✅ | **Tartine 旁證**：麵團控在 78～82°F（25.6～27.8°C）、bulk 3～4h、終點 +20～30%。**常被誤記成 28～29°C** | `fermentation-guide.md` §1 | Chad Robertson《Tartine Bread》；[The Perfect Loaf 版本](https://www.theperfectloaf.com/tartine-sourdough-country-loaf-bread-recipe/)<br>關鍵字：`Tartine country bread 78-82F bulk 20-30% rise` |
| ✅ | **各家漲幅數字從 +30% 到 +100% 都有，兩種都做得出好麵包**——差別幾乎全來自**麵團溫度**：暖溫食譜配低漲幅、涼溫食譜配高漲幅，因為 bulk 之後每一步都還在發酵。修正項：**蛋白質 >12.5% 目標上調 5～10 個百分點**；levain 接種比例越低越能容忍高漲幅 | `fermentation-guide.md` §1 | [The Sourdough Journey — The Mystery of Percentage Rise in Bulk Fermentation](https://thesourdoughjourney.com/the-mystery-of-percentage-rise-in-bulk-fermentation/)<br>關鍵字：`mystery of percentage rise bulk fermentation 30% vs 100% dough temperature` |
| ✅ | **高溫要早收的主因＝酸活化 protease 吃掉麵筋**（不是冰箱續發）。65～78°F 酶活性可控；逼近 **90°F（32°C）protease 極活躍，麵筋 30～60 分內崩壞**。⚠️ 不進冰箱、當天室溫做完一樣成立 | `fermentation-guide.md` §1 | [Sourdough Archive — Bulk Fermentation Percentage Rise](https://sourdougharchive.com/bulk-fermentation-percentage-rise/)<br>關鍵字：`bulk fermentation protease gluten degradation warm dough` |
| ✅ | **降溫滯後**：容器進冰箱後中心要 1～2h 才降到發酵近停，這段還在續發 → 要冷藏過夜的麵種要在顛峰前就進 | `fermentation-guide.md` §4 | 熱傳導＋酵母活性隨溫度衰減的常識推論，多家教學一致<br>關鍵字：`dough cold retard thermal lag continues fermenting fridge` |
| ✅ | **Blisters（表皮起泡）＝冷藏發酵的指紋**：冷藏時 CO₂ 滲入並滯留麵團表層（越冷溶越多），進爐後膨脹但被已定型的外皮擋住 → 小泡；冷藏越久越明顯。🚨 **只證明製程，不證明品質**；好壞是**文化差異**——美國視為成功象徵、**法國常視為瑕疵** | `troubleshooting.md` §0 | [The Pantry Mama — How To Get Blisters](https://pantrymama.com/how-to-get-blisters-on-sourdough-bread/)、[The Fresh Loaf — retarding = more blistering?](https://www.thefreshloaf.com/node/59248/retarding-more-blistering)<br>關鍵字：`sourdough blisters cold retard CO2 trapped crust cultural flaw France` |
| ❌ | ~~「有 blisters／有爆口 ear ＝ 這爐做得好」~~ | — | **已駁回（同一類錯誤，2026-08）**：兩者都是**製程或筋性的證據，不是品質的證據**。blisters 只說明有冷藏發酵；漂亮的爆口甚至在**發酵不足**時更容易出現（筋更強）。→ 判品質一律回到「壁」（`troubleshooting.md` §0 強制步驟） |
| ✅ | **剖面 → 發酵程度 12 格判定表**：大氣孔常代表**發酵不足**（孤立洞穴／隧道＋旁邊密實區），不是成功；密實在過發與不足**兩端都會出現**，用形狀扁不扁分辨；過發**先垮形狀後垮組織** | `troubleshooting.md` §0 | The Sourdough Journey, "How to Read a Sourdough Crumb – Gallery" (© 2021)<br>關鍵字：`How to Read a Sourdough Crumb gallery underproofed tunneling caverns overproofed` |
| ✅ | **追開放組織的變因優先序：發酵 ≈ 手法 ＞＞＞ 水合**。原文：*"fermentation and dough handling are responsible for building the majority of a loaf's crumb structure, while hydration is **nothing but a distant third**"*。Wilson 光 bulk fermentation 就寫約 80 頁 | `troubleshooting.md` §0 | Trevor Jay Wilson《Open Crumb Mastery》；[brotokoll 訪談](https://brotokoll.com/open-crumb-mastery-a-holey-talk-with-trevor-j-wilson/?lang=en)、[trevorjaywilson.com](https://trevorjaywilson.com/open-crumb-mastery/)<br>關鍵字：`Trevor Wilson open crumb hydration distant third fermentation dough handling` |
| ⚠️ | **open crumb 是光譜**：均勻型（refined crumb）與極端不規則型（**molten crumb** / wild crumb）兩端都算開放組織。**一般開放組織約 70% 水合即可**，「要 open crumb 就得高水合」的說法多半是把極端那端當成全部 | `troubleshooting.md` §0 | 概念本身與 Wilson「水合是第三名」一致；**但「molten crumb 是 Wilson 的用語且需極高水合」這項歸屬未查證**——該詞亦見於 The Sourdough Journey 的 crumb gallery（加引號使用）。⚠️ 引用時**別把此定義掛在 Wilson 名下**，除非查到書中原文 |
| ✅ | 🔒 **判發酵程度唯一可靠的判準是「壁」不是「孔」**：發酵到位＝孔與孔之間的麵團**薄、半透明、熟透如卡士達（custardy）**；發酵不足＝**厚、不透光、麵團感（doughy）**，配大小不一的孔與黏的質地。孔的數量／分布／圓不圓／有無密實帶**全都會誤導** | `troubleshooting.md` §0 強制步驟 | [Sourdough Archive — Crumb Guide: Open vs Dense vs Fool's Crumb](https://sourdougharchive.com/sourdough-crumb-guide/)、[Simplicity and a Starter](https://simplicityandastarter.com/identifying-underproofed-sourdough-bread-with-examples/)<br>關鍵字：`thin translucent custardy cell walls proofed vs thick doughy walls underproofed` |
| ❌ | ~~「孔很多／分布均勻／一路分布到底部沒有密實帶 → 發酵到位」~~ | — | **已駁回（AI 連續兩次同型失誤，2026-08）**：實心麵團上也能有很多分布均勻的洞。**整塊都厚壁時反而不會出現「密實帶」**，因為沒有對比。另駁回「有爆口/ear、形狀挺＝發酵夠」——**發酵不足的麵團筋更強、更容易爆得漂亮**。→ 已改為強制先描述壁再下判定 |
| ✅ | **傻瓜氣孔（fool's crumb）**：緊實細密的小孔＋上半部孤立大孔＋下半部更密實 ＝ **發酵不足**，不是開放組織成功。成因為產氣不足且分布不均，氣體在最弱處（近上皮）撐開孤立大洞。**判準是「小孔區蓬不蓬」不是「有沒有大孔」** | `troubleshooting.md` §0 | [Simplicity and a Starter — Identifying Underproofed Sourdough](https://simplicityandastarter.com/identifying-underproofed-sourdough-bread-with-examples/)、[The Pantry Mama — 5 Ways To Tell If Under Fermented](https://pantrymama.com/underfermentedsourdough/)<br>關鍵字：`fool's crumb underproofed dense bottom large holes top` |
| ❌ | ~~「孔洞圓潤平滑＝氣體撐出來的＝不是發酵不足；撕裂狀才是」~~ | — | **已駁回，且是 AI 憑空發明的判準**（2026-08 判讀失誤）：來源圖表從未提出此區分，**發酵不足的孤立大洞常常就是圓的**。連帶三個同源的合理化也一併駁回：「上大下小是正常的」（那正是 fool's crumb 定義）、「大孔周圍充氣正常所以不算密實區」（密實是相對於發好的麵包，不是相對於旁邊）、「沒隧道沒濕黏所以不是發酵不足」（那是**嚴重**發酵不足的徵象，輕中度不長那樣）。詳見 `troubleshooting.md` §0 合理化對照表 |
| ✅ | **全麥/裸麥麵種表面氣泡少是正常**：麩皮切筋鎖不住氣，氣泡浮到表面就破 → 改看罐壁氣泡＋漲幅＋氣味 | `fermentation-guide.md` §4 | 與麩皮切筋機制同源（見三、全穀）<br>關鍵字：`whole wheat starter fewer surface bubbles normal` |

---

## 二、酸種養種

| 標記 | 主張 | 對應位置 | 來源／搜尋關鍵字 |
|---|---|---|---|
| ✅ | **兩段式溫度**：建立期 27～28°C（80～83°F）加速拓殖 → 穩定後降 24～25°C（75～76°F）維護 | `sourdough-starter.md` §1 | [Northwest Sourdough — Starters and Temperature](https://northwestsourdough.com/sourdough-starters-and-temperature/)<br>關鍵字：`sourdough starter keep warmer 80F when beginning then 72-80F established` |
| ✅ | **機制**：溫度決定菌相——**5°C 由 Leuconostoc 主導、25°C 換 Lactobacillus 主導**。暖起步 → Lactobacillus 更快接管 → pH 降更快。菌相演替約 Day 2～6 多樣性達峰、Day 10～14 收斂成耐酸的 climax community | `sourdough-starter.md` §1 | [PMC10559884 — Sourdough starters exhibit similar succession patterns](https://pmc.ncbi.nlm.nih.gov/articles/PMC10559884/)<br>[Microbial Ecology Dynamics during Rye and Wheat Sourdough Preparation (AEM)](https://journals.asm.org/doi/full/10.1128/aem.02955-13) |
| ✅ | **建立初期的氣泡多半是 Leuconostoc 假高峰**，此時大量餵養會稀釋酸度、拉高 pH，反而延長雜菌期 → 建立期大方向是**讓 pH 一路降下去** | `sourdough-starter.md` §1 | Debra Wink, "Lactic Acid Fermentation in Sourdough"（The Fresh Loaf / BreadBakers Guild）<br>關鍵字：`Debra Wink pineapple juice solution Leuconostoc sourdough starter pH` |
| ✅ | **酸種發酵是厭氧過程**，蓋子留縫是為排 CO₂ 防爆罐，**不是「讓它呼吸」**。（攪拌帶氧另有其用：酵母**增殖**偏好有氧，與產氣發酵厭氧不矛盾） | `sourdough-starter.md` §3 | 發酵生化學通識；關鍵字：`sourdough fermentation anaerobic yeast propagation aerobic loose lid CO2` |
| ✅ | **水**：活性碳過濾水／礦泉水最佳（去氯留礦物質）；**RO 逆滲透水、蒸餾水不適合**（礦物質被拔光）。⚠️ 中文「過濾水」常被用來指 RO——**必須向使用者確認是哪一種** | `sourdough-starter.md` §1 | 關鍵字：`sourdough starter distilled reverse osmosis water lacks minerals chlorine chloramine` |
| ✅ | **夏天加鹽減速**：約餵入粉重 **1%**；**別超過 2%**——更高濃度（4%+）會不成比例地抑制乳酸菌、改變菌相 | `sourdough-starter.md` §2 | 關鍵字：`salt inhibits lactic acid bacteria sourdough starter percentage slow fermentation` |
| ✅ | **Float test 兩個方向都會誤判**：全麥/裸麥種筋弱鎖不住氣 → 已 ready 卻沉（假不合格）；硬種結構強 → 過了顛峰仍浮（假合格）。**翻倍幅度＋氣味永遠優先** | `sourdough-starter.md` §1 | 關鍵字：`sourdough float test unreliable false negative whole wheat rye stiff starter` |
| ✅ | **肥皂泡浮沫**：顛峰時起泡＋確實漲高＝健康旺盛；**滿是細泡卻沒真正漲起來／沒結構＝失衡**，成因為太熱／間隔太長而餵太少／太稀 | `sourdough-starter.md` §4 | [The Perfect Loaf — 21 Common Starter Problems](https://www.theperfectloaf.com/21-common-sourdough-starter-problems-with-solutions/)<br>關鍵字：`sourdough starter foamy soapy bubbles no rise too warm` |
| ✅ | **起種粉蛋白質 12～14% 都適用**；12.5～13% 之所以是甜蜜點，理由是**顛峰穩定度**（11% 出頭的粉提早到頂又撐不住） | `sourdough-starter.md` §1 | [Summit Sourdough — High vs Low Protein Flour](https://www.summitsourdough.com/en-us/blogs/information-and-process-5/high-protein-flour-vs-low-protein-flour-with-sourdough) |
| ✅ | **Peak 不是固定倍數**：peak ＝ 該酵種脹到「它自己的」最大體積並開始停止上升，**每個種不同**（有的可長到 5 倍，那種種在 2～3 倍時仍是發酵中期）。文獻：peak 是**流動的概念不是精確時間點**；peak 時間由**溫度＋餵養比例**共同決定 | `sourdough-starter.md` §1 | [Sourdough Archive — Starter Chart](https://sourdougharchive.com/sourdough-starter-chart/)、[Brod & Taylor — Feeding Ratios](https://brodandtaylor.com/blogs/recipes/feeding-ratios)<br>關鍵字：`sourdough starter peak not fixed doubling varies feeding ratio temperature` |
| ✅ | **顛峰冷藏法**：酵種／levain **正好在 peak 時進冷藏**，之後再用。TSJ 2025 實測——12～24h 最佳（**每小時產生的 CO₂ 比室溫在顛峰直接用的種還多**，即冷藏對此時間點是**增強**不只是保存）；2～3 天尚可；**5 天品質明顯衰退不建議**。時機必須是 at peak：**顛峰前冰、過顛峰才冰，效果都差一截**。代價：冷藏**減緩但不停止** LAB → 持續變酸，前 24h 無不良影響，之後每天略弱 | `sourdough-starter.md` §1、§3、§7.1 | The Sourdough Journey（2025 實測系列）——**本檔指定的發酵權威來源**。⚠️ 屬 TSJ 自家實驗結果，未見獨立複現<br>關鍵字：`Sourdough Journey refrigerate starter leaven at peak stronger rising power` |
| ✅ | **Domed top ≠ Peak**：圓頂隆起時還在上升，**表面轉平才是 peak** | `sourdough-starter.md` §1、`fermentation-guide.md` §5 | 本檔 `fermentation-guide.md` §5 原有判準（「圓頂剛轉平、質地如慕斯」），與多家教學一致<br>關鍵字：`sourdough starter peak domed top vs flattened surface` |
| ✅ | **Float test 假合格的根本原因：過了 peak 一樣會浮**（不限硬種）——它測含氣量，而含氣量在 peak 前後都高，**分不出上升段與下降段** | `sourdough-starter.md` §1 | 同上；補強原有條目 |
| ⚠️ | **餵養粉的蛋白質影響顛峰穩定度**：偏低（11～11.5%）的種提早到頂又**撐不住顛峰**，窗口窄容易錯過 | `sourdough-starter.md` §1 | 《Secrets of Open Crumb / The Sourdough Starter Expert》單一來源。⚠️ 同書「14%+ 有害」那條已駁回（見下），此條僅取「顛峰穩定度」的方向 |
| ⚠️ | **比例階梯當強度指標**：間隔內漲了又落＝該加碼，1:1:1 →…→ 1:6:6，小步遞增 | `sourdough-starter.md` §1 | 《Secrets of Open Crumb / The Sourdough Starter Expert》。單一來源，但邏輯自洽（提早耗盡食物＝該多餵）且與台式兩週法的漸進拉大一致 → **採納但標明** |
| ⚠️ | **攪拌隨稠度演進為迷你 stretch and fold** | `sourdough-starter.md` §1 | 同上，單一來源；低風險操作建議 |
| ❌ | ~~「蛋白質 14%+ 會讓菌消化不掉、種變弱發黏」~~ | — | **已駁回**。主流資料把 12～14% 全列為適用區，高蛋白粉甚至因養分與保氣力較好被推薦；**原作者自陳 "at least that was my observation"**。→ 不要把「14% 有害」寫回 skill |
| ❌ | ~~「起種一定要用全白高筋粉」~~ | — | **未採納**（非錯誤，是流派）。全白可行但慢且受環境主導（作者自陳同粉：佛州幾天 vs 華盛頓州 14 天）。本檔維持**全麥／裸麥點火**（麩皮胚芽的微生物與礦物質多、成功率高），全白列為並行選項 |

---

## 三、全穀與麵粉

| 標記 | 主張 | 對應位置 | 來源／搜尋關鍵字 |
|---|---|---|---|
| ✅ | **麩皮壓低氣孔天花板的機制**：麩皮顆粒像小刀片**切斷筋膜**、大片麩皮**刺破氣室**；全穀粉還要用較少的有效筋撐起較重的麩皮胚芽 → 保氣力下降 | `troubleshooting.md` §0 | 關鍵字：`bran particles cut gluten strands puncture gas cells whole wheat dense crumb` |
| ✅ | **研磨粗細是獨立於灰分的變因**：顆粒越細破壞越小 → 超細全粒粉的氣孔天花板高於粗磨 | `flour-notes.md` 全穀段 | 同上機制的直接推論；關鍵字：`fine milled whole wheat flour more open crumb particle size` |
| ✅ | **50% 以上全穀仍可做出開放組織**——前提是技術與發酵到位。**「全穀比例＝硬牆」是錯的**，那是難度梯度不是不可能 | `troubleshooting.md` §0 | King Arthur Baking、The Perfect Loaf、Breadtopia 多來源一致<br>關鍵字：`open crumb high percentage whole wheat sourdough 50% possible` |
| ✅ | **篩麩皮＋soaker 回加**：全粒粉過篩 → 粗麩皮 1:1 加水泡軟 30 分＋ → 麵團先用細粉建筋網 → **摺疊後段**再拌回 | `troubleshooting.md` §0、`flour-notes.md` | 同上來源群；關鍵字：`sift bran soaker add back late whole wheat open crumb technique` |
| ✅ | **法國 T 號 ＝ 每公斤幾克灰分**（NF V03-720）；**德國 Type ＝ 每 100g 幾毫克灰分**（DIN 10355）。裸麥分級與小麥**不同檔** | `flour-notes.md` 裸麥段 | NF V03-720；DIN 10355<br>關鍵字：`French flour T number ash content DIN 10355 German Type rye` |
| ✅ | **編號是「區間的名稱」，不是精確值**（曾誤判）：德制 **Type 1370 合法區間 1.31～1.60%**，標 1.60% 是合法上緣品不是標錯。**一律以包裝標示為準** | `flour-notes.md` 裸麥段 | DIN 10355 分級表<br>⚠️ **歷史錯誤**：曾據「1370→1.37%」判定廠商標錯，方向剛好相反 |
| ✅ | **T 號只管風味不管結構**：同為 T65，蛋白質可從 10.5% 到 12.7%（差 2.2pp），灰分卻穩定落在 0.62～0.75 → **買法國粉一律看蛋白質標示** | `flour-notes.md` | 冠軍之手 2026-08 商品規格橫向比對（12 款以上） |
| ✅ | **裸麥的結構靠戊聚醣（pentosans）不是麵筋**——缺乏形成筋網所需的麥穀蛋白結構，所以「揉出筋」那條路根本不存在 | `flour-notes.md` 裸麥段 | 穀物化學通識；關鍵字：`rye pentosans arabinoxylan not gluten structure bread` |
| ✅ | **鷹牌 12.0±0.5%／0.38±0.03、拿破崙 11.8±0.5%／0.42±0.04**（已對 Nippn 原廠規格查證吻合）。**原廠規格本身帶公差** → 這就是「換新粉先減水 3%」的科學理由 | `flour-notes.md` | Nippn 原廠規格 |
| ✅ | **全麥/裸麥粉室溫僅約 1～3 個月**（麩皮胚芽油脂氧化酸敗）；白粉台灣夏天保守抓 3 個月。冷凍 2～5 天可殺蟲卵 | `flour-notes.md` 儲存段 | 多來源一致；關鍵字：`whole wheat flour rancidity shelf life refrigerate freeze` |

---

## 四、待查證（有疑慮但還沒查的，別當定論用）

| 項目 | 現況 | 該查什麼 |
|---|---|---|
| 氣炸烤箱 200°C 上限對 oven spring 的實際影響量 | skill 列為「開放組織的第二限制因子」，**未量化** | `oven spring temperature 230C vs 200C crumb openness` |
| 商業酵母麵團在高溫下的 bulk 終點 | 目前沿用「Cold Proof 1.8 倍／室溫 2 倍」；⚠️ 雙因子法**不適用**（無 LAB 大量產酸），但高溫是否仍需下修終點未查 | `commercial yeast dough bulk fermentation high temperature endpoint` |
| 配料（乾果堅果）用量上限 10～20% of flour | 記為「通行上限」，未找到一次來源 | `inclusions percentage of flour weight bread limit` |

---

## 更新這份檔的規則

- **新查證** → 在對應章節加一列，四欄填滿（標記／主張／對應位置／來源）。
- **推翻既有 ✅** → 不要直接刪，**改標 ❌ 並寫明推翻理由**——留著才能防止未來又被加回來。
- **使用者實測與文獻衝突** → 實測優先，但兩邊都記，並在對應檔標註衝突。
- 只在「有人可能會質疑」的說法上花力氣登錄；顯而易見的常識不必列。
