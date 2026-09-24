# 手机移动网络（4G/5G）与WiFi功耗差异调研
## 板块：市场现状 + 可讲案例

> 调研日期：2026-09-23
> 标注规则：【已查证】= 权威评测机构/学术论文/运营商或厂商官方可追溯；【一方称】= 厂商宣传口径，未经第三方独立验证
> 所有测试数据均标注测试条件；区分实测数据与厂商宣传数据。

---

# 一、市场现状

## 1. 主流旗舰机的 WiFi 和移动网络模块功耗数据

### 1.1 核心结论
在同等使用场景下，**WiFi 普遍比 5G/4G 蜂窝网络更省电**，优势约 30–40%；视频流媒体、FaceTime 等持续数据传输场景差距最大；纯语音通话/短信场景两者几乎无差别。

### 1.2 WiFi vs 5G 同机对比实测

**PhoneBuff / Notebookcheck 双机对照测试（两台 iPhone 17 Pro Max）**【已查证】
- 测试条件：两台 iPhone 17 Pro Max，一台连 WiFi、一台纯 5G；均工厂重置、安装相同 App、同亮度、全新账号；全程 26 小时，覆盖语音通话/短信/FaceTime/网页浏览/待机/社媒/视频流媒体。
| 场景 | 5G 机电量变化 | WiFi 机电量变化 | 差距 |
|---|---|---|---|
| FaceTime 通话 2 小时 | 100%→46%（掉 42%） | 100%→62%（掉 25%） | 5G 多耗 17 个百分点 |
| Instagram 浏览 2 小时 | →4%（再掉 13%） | →26%（再掉 10%） | 5G 多耗 3 个百分点 |
| 流媒体电影约 22 分钟 | **直接关机** | 仍剩 25% | 5G 提前耗尽 |
- 来源：https://www.notebookcheck.net/WiFi-vs-5G-Test-shows-major-differences-in-battery-drain.1223624.0.html

**abwavestech 15 款手机 24 小时受控测试**【已查证，自媒体实测，方法透明】
- 测试条件：15 台手机（iPhone 14/15/16、三星 S23/S24/S25、Pixel 7/8/9、一加 12/13）；屏幕亮度锁定 50%（非自动）；关闭定位/后台刷新/WiFi；统一使用模式（30 分钟浏览 + 30 分钟待机，循环 24 小时）。
| 机型 | LTE 24h耗电 | 5G 24h耗电 | WiFi 24h耗电 |
|---|---|---|---|
| iPhone 15 | 18% | 28%（+10） | 12% |
| Samsung S24 | 22% | 31%（+9） | 14% |
| Pixel 9 | 20% | 27%（+7） | — |
| OnePlus 13 | 24% | 32%（+8） | — |
- 结论：**WiFi 比 5G 高效约 30–40%**；强信号下 5G 比 LTE 多耗 7–10 个百分点。
- 来源：https://abwavestech.com/i-tested-15-phones-for-5g-battery-drain/

**Geeky Gadgets 引用场景测试**【已查证】
- 网页浏览：WiFi 比 5G 节能 4%
- 社媒滑动：WiFi 省 3%
- 视频流媒体：**WiFi 优势达 25%**
- 来源：https://www.geeky-gadgets.com/wi-fi-or-5g-which-one-secretly-drains-your-phone-faster/

### 1.3 主流旗舰机续航基线（供横向参考）

**iPhone 16（3561 mAh，高通基带）**【已查证】
- PhoneArena 电池测试：综合续航估计 6h21min；浏览 16h48min；视频播放 7h30min；游戏 9h52min。
  - 来源：https://www.phonearena.com/reviews/iphone-16e-vs-iphone-16_id6743
- GSMArena：Active use score 15:42h。
  - 来源：https://www.gsmarena.com/compare.php3?idPhone1=11103&idPhone2=13317
- 苹果官方标称：视频播放最长 22 小时，流媒体视频最长 18 小时。【一方称】
  - 来源：https://support.apple.com/en-gb/121029

**iPhone 16e（4005 mAh，苹果自研 C1 基带）**【已查证】
- PhoneArena：综合续航 6h4min；浏览 17h27min；视频 6h59min；游戏 7h45min。
- 苹果官方标称：视频播放最长 26 小时，流媒体 21 小时。【一方称】
  - 来源：https://www.phonearena.com/reviews/iphone-16e-vs-iphone-16_id6743

**说明**：GSMArena/PhoneArena 的续航测试未单独拆分"WiFi 网络"与"蜂窝网络"子项，上述为综合续航基线；WiFi vs 蜂窝的差异主要来自 1.2 节的专项对照测试。小米 14、华为 Mate 60/70、三星 S24 的 WiFi/蜂窝分项功耗，国内专业评测机构（小白测评、极客湾、科技美学）多以短视频形式发布，未形成可追溯的结构化网页数据；可引用的是下方第 2 节的 4G/5G 专项实测。

---

## 2. 4G 和 5G 在功耗上的具体差异

### 2.1 待机 / 空闲功耗（"隐形耗电"）
**结论：5G 空闲功耗约为 4G 的 1.5–2 倍，即使不主动用流量也在额外耗电。**

- abwavestech 24 小时空闲（无活跃数据使用）【已查证】
  | 机型 | 4G 空闲 | 5G 空闲 | 差值 |
  |---|---|---|---|
  | iPhone 15 | 8% | 16% | +8% |
  | Samsung S24 | 10% | 19% | +9% |
  | Pixel 9 | 9% | 17% | +8% |
  | OnePlus 13 | 11% | 21% | +10% |
  - 来源：https://abwavestech.com/i-tested-15-phones-for-5g-battery-drain/

- 雷科技 / 36氪 小米 13 双机实测【已查证】
  - 测试条件：两台同批次小米 13（骁龙 8 Gen 2），同系统版本、自动亮度、中国电信卡；一台锁 4G、一台默认 5G。
  - 锁屏待机 1 小时：5G 掉 5% vs 4G 掉 3%（+2%）
  - 重启无后台待机 6 小时：5G 掉 2% vs 4G 掉 1%
  - 来源：https://m.36kr.com/p/2338410570483328

- 学术论文【已查证】
  - eScholarship：5G 待机功耗约为 4G 的 **2 倍**；Samsung S23+（高通 X70）比 Pixel 7A（Exynos 5300）功耗更低。
    - 来源：https://escholarship.org/content/qt7dw491rp/qt7dw491rp.pdf
  - Princeton 测量研究：5G 模块功耗是 4G 的 **2–3 倍**，是屏幕显示功耗的 1.8 倍；该高功耗源于 5G 射频硬件和 DRX 状态机本身，标准省电方案难以奏效。
    - 来源：https://www.cs.princeton.edu/courses/archive/spring21/cos563/papers/5G_measurement.pdf

### 2.2 使用中功耗（浏览 / 视频 / 下载）
**结论：信号良好时，5G 比 4G 多耗约 6–11% 电量；全天累积差距可达 20%+。**

- **Ookla（Speedtest Intelligence 大数据，2023 Q1）**【已查证，权威】
  - 方法：识别全球 Android 设备中早上 6:00–12:00 电量为 100% 的设备，对比下午 12:00–18:00 的最低电量。
  - 骁龙 8 Gen 2（X70 基带）：5G 耗电 31% vs 4G 耗电 25%（+6 个百分点）
  - 天玑 9200：5G 耗电 34%（上代天玑 9000 为 45%，代际能效大幅改善）
  - 总体结论：**5G 比 4G LTE 多耗 6%–11%**，取决于 SoC。
  - 来源：https://www.ookla.com/articles/5g-battery-drain

- **雷科技 / 36氪 小米 13 全天多场景实测**【已查证】
  - 测试条件：两台小米 13，从 98% 同步测试，覆盖办公楼/商场/地铁/老旧小区 4 个场景，使用 B站/抖音在线视频 + 微博。
  | 场景（1 小时左右） | 5G 耗电 | 4G 耗电 | 差值 |
  |---|---|---|---|
  | 办公楼（信号稳定） | 11% | 9% | +2% |
  | 商场白天 30min | 5% | 4% | +1% |
  | 商场晚上（人流密集）30min | 8% | 7% | +1% |
  | 广州地铁 3 号线 1 小时 | 13% | 9% | **+4%** |
  | 老旧小区 1 小时 | 14% | 12% | +2% |
  | 锁屏待机 1 小时 | 5% | 3% | +2% |
  - **最终结果**：5G 机在 2% 电量自动关机时，4G 机还剩 **25%** 电量，全天累积差距 **23 个百分点**。
  - 来源：https://m.36kr.com/p/2338410570483328

- **注意反直觉点**：下载大文件时 5G 可能反而省电（单位数据量能耗更低）。抖音科普引用测试：5G 下载 10GB 电影 8 分钟耗电 4%，4G 下载同文件 50 分钟耗电 6%。【一方称，自媒体实测】
  - 来源：https://www.iesdouyin.com/share/video/7640731114377612580

### 2.3 弱信号场景（最大耗电放大器）
**结论：信号越差，5G 相对 4G 的功耗差距越大；弱信号下 5G 电流可达 4G 的 2.7 倍。**

- 信号强度 vs 实测电流【已查证】
  | RSRP 信号强度 | 5G 电流 | LTE 电流 | 差值 |
  |---|---|---|---|
  | −85 dBm（优秀） | 312 mA | 228 mA | +37% |
  | −98 dBm（中等） | 487 mA | 265 mA | +84% |
  | −108 dBm（差） | 792 mA | 291 mA | **+172%** |
  - 来源：https://lifetips.alibaba.com/tech-efficiency/your-smartphones-5g-icon-might-be-bogus

- abwavestech 弱信号场景（RSRP −120~−130 dBm）【已查证】
  - iPhone 15：35% vs LTE 18%（+17 个百分点）
  - Samsung S24：38% vs LTE 22%（+16 个百分点）
  - 原理：调制解调器进入"信号搜索"状态（signal hunting），持续主动发射探测信号。
  - 来源：https://abwavestech.com/i-tested-15-phones-for-5g-battery-drain/

- 太平洋科技：地铁车厢/地下车库等弱覆盖环境，手机频繁小区重选与波束扫描，**瞬时发射功率峰值可达 4G 的 31.6 倍**。【一方称，媒体实测】
  - 来源：https://g.pconline.com.cn/ask/57908.html

- 新浪科技：弱信号区域（地铁、地下室）5G 功耗比 4G 高 **40% 以上**。【一方称】
  - 来源：https://www.sina.cn/news/article/comos_niqmmyy2878296.html

### 2.4 5G NSA vs SA 模式功耗差异
**结论：SA 独立组网比 NSA 非独立组网省电约 20%；NSA 需同时维持 4G+5G 双连接，是额外耗电根源。**

- 沃达丰（运营商官方）【已查证】：NSA 模式下手机同时双连接 5G NR 和 4G LTE；SA 仅连 5G NR 一张网，**省电约 20%**。
  - 来源：https://mobile.iotworld.com.cn/View.aspx/news-642d1c8c7c6b568b

- Ookla / Omdia《5G SA 全球现状报告 2026》【已查证，权威】
  - 英国 EE 网络：SA 设备中位放电时间比 NSA **长约 22%**
  - 英国 O2 网络：SA 比 NSA 长约 11%
  - 实际续航差距最多约 **3 小时**
  - 来源：https://ookla-marketing-generator.ookla.dev/s/media/2026/02/ookla_omdia-5GSA_2026_a.pdf

- 稀土掘金 HarmonyOS 5 基带功耗实测【已查证，技术博客】
  | 场景 | SA 功耗 | NSA 功耗 | 差值 |
  |---|---|---|---|
  | 空闲状态 | 45 mW | 68 mW | +51% |
  | 高清语音通话 | 320 mW | 410 mW | +28% |
  | 100 Mbps 下载 | 850 mW | 1100 mW | +29% |
  | 弱信号场景 | 620 mW | 890 mW | +43% |
  - 来源：https://juejin.cn/post/7515395360534511628

- Circles.Life（新加坡运营商）：SA 比 NSA 省电 20–30%。【一方称】
  - 来源：https://www.circles.life/sg/blog/5g-sa-vs-nsa-in-singapore-why-circles-life-m1-powered-5g-is-faster/

### 2.5 Sub-6GHz vs mmWave 功耗差异
**结论：mmWave 功耗显著高于 Sub-6GHz，比 LTE 多耗约 40–60%；Sub-6GHz 比 LTE 多耗约 15–25%。**

- S24 Ultra 分频段实测【已查证】
  | 网络模式 | 每小时耗电 | vs LTE |
  |---|---|---|
  | 4G LTE | 11.2% | 基准 |
  | 5G Sub-6（n77） | 13.8% | +23% |
  | 5G mmWave（n260） | 16.5% | +47% |
  - 来源：https://electronics.alibaba.com/question/s24-ultra-5g-real-world-performance,-battery-impact-compatibility-guide

- 其他来源交叉印证：
  - abwavestech：mmWave 比 LTE 多耗 35–50%。【已查证】
  - PuraSIM 对比表：Sub-6 +15–25% vs 4G；mmWave +40–60% vs 4G。【一方称】
  - Dr.Fone：Sub-6 +10–20%；mmWave +20–30%。【一方称】
  - 来源：https://purasim.com/en/blogs/guias/esim-5g-vs-4g-merece-pena-viajar

---

## 3. 各家厂商在降低移动网络功耗上的技术方案

### 3.1 苹果：Smart Data Mode（智能数据模式）/ 5G Auto
- **机制**：从 iPhone 12 起默认提供"5G Auto"选项；当 5G 速度不能带来明显体验提升时，系统自动回落到 LTE，以延长电池续航。用户也可手动选"5G On"（始终用 5G，更耗电）或"LTE"（仅 4G）。
- **配套**：低数据模式（Low Data Mode）— 停止后台 App 刷新、降低流媒体质量、暂停自动下载与 iCloud 同步。
- 来源：Apple 官方支持文档【已查证】
  - https://support.apple.com/zh-cn/120745
  - https://support.apple.com/en-nz/HT211828

### 3.2 高通：5G PowerSave 系列 + X75 集成射频架构
- **X65（2021）**：搭载 **5G PowerSave 2.0**，支持 3GPP Release 16 UAI（UE-Assisted Information），终端与基站动态协商载波数量、带宽、MIMO 层数、热状态，按需分配资源。【一方称】
  - 来源：https://www.qualcomm.com/news/releases/2021/05/qualcomm-announces-new-features-snapdragon-x65-5g-modem-rf-system-global-5g
- **X75（2023 年 2 月）**：
  - 全球首款 5G Advanced-ready 调制解调器；
  - **首次将 mmWave 和 Sub-6GHz 集成到同一射频收发器**：PCB 面积减少 25%，**功耗降低高达 20%**（即使不使用 mmWave 也可降 20%）；
  - **5G PowerSave Gen 4** + RF Power Efficiency Suite；
  - AI 传感器辅助 mmWave 波束管理，针对**电梯、地铁、机场、停车场、移动游戏**等场景优化持续性能。【一方称】
  - 来源：https://www.qualcomm.com/news/onq/2023/02/worlds-first-5g-advanced-ready-modem-rf-snapdragon-x75
  - 第三方印证：https://www.eet-china.com/news/202312052144.html 、https://www.androidauthority.com/qualcomm-x75-3282696/

### 3.3 华为：Link Turbo（全网络聚合）+ WLAN+
- **Link Turbo**：WiFi 与移动数据并发使用，突破单网带宽限制。
  - 华为官方专利数据：并发下载速率提升 **83%**，游戏时延降低 **69%**，视频起播时延下降 **87%**。【一方称】
  - 注意：Link Turbo 主定位是"网络加速"，并发时会同时激活蜂窝模块；其省电逻辑是"快速完成传输→更早进入休眠"，而非直接降低蜂窝待机功耗。
  - 来源：https://www.huawei.com/cn/ipr/ 、https://consumer.huawei.com/cn/support/content/zh-cn15903400/
- **WLAN+**：智能在 WiFi 与移动数据间切换，WiFi 信号弱时自动切蜂窝，避免 WiFi 模块空耗。

### 3.4 联发科：5G UltraSave 系列
- **5G UltraSave 3.0+**（天玑 7100/7300/7400 等）：
  - Modem 功耗节省可达 **23%**；
  - 日常网络连接场景整体能效提升可达 **30%**（vs 同类竞品）；
  - 完整支持 5G R16 省电增强。【一方称】
  - 来源：https://www.mediatek.com/zh-tw/products/smartphones/mediatek-dimensity-7100
- **天玑 9200 UltraSave 3.0**：轻载应用能效提升 10%，重载场景功耗节省 19%；支持 100MHz Wideband UL Envelope Tracking 提升上行能效。【一方称】
  - 来源：https://www.mediatek.com/products/smartphones/mediatek-dimensity-9200plus
- **场景模式**：第二代高铁模式连接性能提升 20%；地铁/车库模式专项优化。【一方称】
  - 来源：https://www.mediatek.com/zh-cn/products/smartphones/mediatek-dimensity-7400x

### 3.5 小米 / OPPO / vivo
- **小米**：默认"智能 5G"策略（5G 信号好连 5G，弱则回落 4G）；5G 开关保留在移动网络设置中。
- **OPPO**：将 5G 开关藏在"省电模式"和"开发者选项"中，引导用户使用智能切换。
- **vivo**：需进入工程模式才能关闭 5G。
- **行业趋势**：5G 开关在系统设置中越来越隐蔽，厂商默认配置为自动 5G，减少用户手动切换的成本；雷科技评论认为"未来 5G 开关可能彻底消失"。
  - 来源：https://m.36kr.com/p/2338410570483328

---

# 二、可讲案例

## 4. 厂商在降低移动网络功耗上的技术突破案例

### 案例 1：苹果 C1 自研基带 — iPhone 有史以来能效最高的调制解调器
- **发布时间**：2025 年 2 月，随 iPhone 16e 首发。
- **技术名称**：Apple C1 调制解调器（苹果首款自研蜂窝基带）。
- **苹果宣称**【一方称】：
  - "iPhone 有史以来能效最高的调制解调器（the most power-efficient modem ever on an iPhone）"；
  - 比其他 iPhone 使用的高通 X71 基带**能效高约 25%**；
  - 与 A18 芯片深度协同、硬件级整合，智能管理网络拥塞、优先处理关键数据传输。
- **第三方实测（极客湾 Geekerwan）**【已查证】：
  - iPhone 16e 平均功耗 **0.67 W**；
  - iPhone 16（高通基带）平均功耗 **0.88 W**；
  - 差距约 **24%**，与苹果宣称的 25% 基本吻合。
- **续航效果**：
  - iPhone 16e 视频播放续航 **26 小时** vs iPhone 16 的 **22 小时**（多 4 小时）；
  - 流媒体视频：16e 为 21 小时 vs 16 为 18 小时。
- **代价**：C1 不支持 mmWave，仅支持 Sub-6GHz 5G（国内本就无 mmWave，影响小）。
- 来源：
  - 苹果官方新闻稿【一方称】：https://images.apple.com/hu/newsroom/2025/02/apple-debuts-iphone-16e-a-powerful-new-member-of-the-iphone-16-family/
  - MacRumors 报道（引用极客湾实测）【已查证】：https://www.macrumors.com/2025/02/28/apple-c1-modem-5g-speed-tests
  - AppleInsider【已查证】：https://appleinsider.com/articles/25/02/27/apples-c1-modem-breaks-no-records-for-speed-but-is-exceptionally-power-efficient

### 案例 2：高通 X75 基带 — mmWave/Sub-6 集成架构带来 20% 功耗降低
- **发布时间**：2023 年 2 月 15 日，随骁龙 8 Gen 3 首发商用。
- **技术突破**：首次将 mmWave 和 Sub-6GHz 支持集成到**同一射频收发器**（此前需两颗独立收发器）。
- **效果数据**【一方称，高通官方；Android Authority 旁证为实验室数据】：
  - PCB 面积减少 **25%**；
  - 功耗降低高达 **20%**（相比 X70）；
  - 即使不使用 mmWave 模组，也可实现 20% 功耗降低。
- **配套技术**：5G PowerSave Gen 4、AI 传感器辅助 mmWave 波束管理、第二代 GNSS 定位（精度提升 50%）。
- **场景优化**：高通官方明确点名电梯、地铁、机场、停车场、移动游戏等弱网/移动场景的持续性能改进。
- 来源：
  - 高通官方【一方称】：https://www.qualcomm.com/news/onq/2023/02/worlds-first-5g-advanced-ready-modem-rf-snapdragon-x75
  - EET-China 报道【已查证】：https://www.eet-china.com/news/202312052144.html
  - Android Authority【已查证】：https://www.androidauthority.com/qualcomm-x75-3282696/

---

## 5. 用户在实际使用中发现流量特别费电的真实场景

### 场景 1：地铁通勤 — 4G/5G 频繁切换导致额外耗电
- **场景还原**：广州地铁"死亡 3 号线"，车厢内全程播放 B 站在线视频来回 1 小时；虽广州 5G 覆盖广泛，但地铁高速运行中 5G 频繁切到 4G，接近站又切回 5G，驶离再切回。
- **实测数据（雷科技）**【已查证】：
  - 5G 模式 1 小时耗电 **13%**，4G 模式耗电 **9%**，差 **4 个百分点**；
  - 频繁切换还导致快进时短暂缓冲，体验反而不如全程 4G 稳定。
  - 来源：https://m.36kr.com/p/2338410570483328
- **真实用户反馈**：
  - **荣耀俱乐部用户帖**（2026-04-21，河北）："昨天把 5G 关了，120 高刷改成智能刷新率后，**续航大幅度提升**！" 跟帖用户："在外面把 5G 和高刷关了省电非常明显。"
    - 来源：https://club-api.c.hihonor.com/thread-30163991-1-1.html 【已查证，真实用户帖】
  - **太平洋科技**：地铁车厢、地下停车场、老旧小区等弱覆盖环境，手机频繁发起小区重选与波束扫描，瞬时发射功率峰值可达 4G 的 **31.6 倍**；建议手动设为"智能 5G/4G 自动切换"而非"仅 5G"。【一方称，媒体实测】
    - 来源：https://g.pconline.com.cn/ask/57908.html

### 场景 2：地下车库 / 电梯 — 弱信号或无信号导致"搜网耗电"
- **场景还原**：地下车库静置（无 WiFi），手机常开 5G vs 锁定 4G。
- **实测数据**【已查证】：
  - 搜狐引用博主测试：地下车库静置 8 小时，**常开 5G 掉电 12% 以上，锁定 4G 只掉 2.8%**；红米 K80 用户反馈类似。
  - 来源：https://m.sohu.com/a/1066583190_121761735/
- **学术解释**【已查证】：
  - Princeton 研究：5G 空闲状态下的 DRX（不连续接收）状态机使模块保持较高功耗，标准省电方案效果有限；
  - 完全无信号时，手机不断搜索可用网络、尝试注册和小区重选，**射频和处理器长期无法休眠**。
  - 来源：https://www.cs.princeton.edu/courses/archive/spring21/cos563/papers/5G_measurement.pdf
- **用户应对**：新浪科技建议，地铁隧道、地下车库等弱信号环境，**开启飞行模式或使用 WiFi 通话**可有效缓解电量快速下降。【一方称】
  - 来源：https://www.sina.cn/news/article/comos_nisencu8921526.html

---

# 附：数据可信度与使用提示

| 来源类型 | 代表 | 可信度 |
|---|---|---|
| 权威大数据 / 学术论文 | Ookla Speedtest Intelligence、Princeton、eScholarship | 高，已查证 |
| 专业评测机构双机对照 | PhoneBuff/Notebookcheck、雷科技、极客湾 | 高，已查证 |
| 运营商官方 | 沃达丰、Ookla/Omdia、Circles.Life | 中高，已查证（但带立场） |
| 厂商官方宣传 | 高通、联发科、苹果官网参数页 | 中，标注【一方称】 |
| 自媒体实测 | abwavestech、太平洋科技、新浪科技问答 | 中，方法透明但样本量小 |
| 真实用户帖 | 荣耀俱乐部、搜狐引用红米用户反馈 | 低-中，仅作体感佐证 |

**使用注意**：
1. 不同测试条件（屏幕亮度、信号强度 RSRP、使用场景、电池健康度、SoC 代际）会导致数据差异极大，引用时必须连同测试条件一起引用。
2. "5G 比 4G 费电 X%"必须区分"信号良好"与"弱信号"两种场景——弱信号下的差距（40%+）远大于信号良好时（6–11%）。
3. 下载大文件时 5G 可能反而省电（单位数据量能耗更低），不要一刀切说"5G 一定更费电"。
4. NSA vs SA 的差距在国内尤其关键：国内初期 5G 多为 NSA，SA 铺开后理论上可省约 20%。
