# 技术原理板块调研笔记：手机移动网络（4G/5G）与 WiFi 功耗差异

> 调研定位：为"手机移动网络与 WiFi 功耗差异"内容创作提供技术原理支撑。
> 标注规则：**[已查证]**＝已核对原始规范/标准/同行评审论文/官方认证文档；**[一方称]**＝厂商或博客单方数据，未独立复核，引用时需保留口径。
> 单位换算速查：0 dBm = 1 mW；+10 dBm ≈ 10 mW；+20 dBm ≈ 100 mW；+23 dBm ≈ 200 mW；+33 dBm ≈ 2000 mW(2 W)。

---

## 子问题 1：移动网络与 WiFi 的技术原理差异

### 结论
蜂窝网络（4G LTE / 5G NR）是一套**带核心网、有运营商身份管理、支持大范围移动的"自治通信系统"**；WiFi（802.11）本质是**一个局域网（LAN）的无线延伸段**，接入点（AP）只负责桥接，没有用户鉴权、位置管理和寻呼这些重型流程。这一架构差异，决定了蜂窝手机即使在待机时也要维持一整套信令监听，而 WiFi 终端可以更"轻"地休眠。

### 技术解释

#### 1.1 覆盖范围：广域蜂窝 vs 局域无线
- **蜂窝**：面向广域连续覆盖，单小区理论覆盖可达数公里至数十公里。ITU 技术报告给出的手机链路工作距离参考为 **1–30 km**（发射功率平均最高约 0.25 W、EIRP 2 W、天线增益 0 dBi）。[已查证]
- **WiFi**：面向室内/短距，典型覆盖半径几十米，依赖 AP 本身就是"小基站"，没有越区切换和大范围位置跟踪的设计需求。

#### 1.2 接入方式：SIM 卡鉴权 vs 本地关联
- **蜂窝**：开机即通过 NAS 层与核心网完成**注册/鉴权（EPS-AKA for 4G；5G-AKA for 5G）**，身份凭据存在 USIM 卡和归属网络（HSS/UDM）中。CableLabs 技术白皮书明确：4G 由 HSS 存储用户凭据并完成鉴权，5G 在 3GPP TS 33.501 框架下定义了多种鉴权流程。[已查证]
- **WiFi**：终端与 AP 之间只需完成 **802.11 关联（Association）+ 四次握手**，鉴权是可选的（开放网络/PSK/802.1X），即使加密也只是链路层安全，不存在"运营商级"用户身份在核心网的登记与位置跟踪。

#### 1.3 核心网架构：有 vs 无
- **4G EPC**：由 MME（移动性管理/寻呼/承载建立）、S-GW、P-GW、HSS（用户数据）、PCRF（策略）等专用网元经固定接口（GTP/Diameter）互联。[已查证]
- **5G 5GC**：云原生模块化，AMF 负责注册/移动性，SMF 负责会话，UPF 负责用户面转发——本质仍是"有状态、有位置管理"的核心网。3GPP TS 23.501 / ETSI TS 123 501 为系统架构规范。[已查证]
- **WiFi**：**没有核心网**。AP 是二层桥接设备，DHCP、DNS、上网认证全部交给上游路由器/宽带网络完成，手机侧不维护"注册状态"，也没有跟踪区（TA）/RNA 这类位置概念。

#### 1.4 协议栈差异
- **蜂窝**：分层为 NAS（非接入层，走核心网）＋ RRC（无线资源控制）＋ PDCP/RLC/MAC/PHY，信令与数据分离，RRC 状态机（IDLE/CONNECTED/INACTIVE）由网络控制。
- **WiFi**：只有 802.11 MAC + PHY，上面直接跑以太网/IP，没有 RRC、没有 NAS、没有专门的寻呼信道设计（靠 Beacon 中的 TIM/DTIM 通知缓冲数据）。

#### 1.5 蜂窝独有、WiFi 不需要的流程
| 流程 | 蜂窝（4G/5G） | WiFi |
|---|---|---|
| 鉴权/注册 | EPS-AKA/5G-AKA，USIM 与核心网双向认证 | 无运营商鉴权；关联即可，加密可选 |
| 移动性管理 | 切换（Handover）、跟踪区更新（TAU）、RNA 更新 | 无；AP 间漫游为 L2 重关联，非核心网流程 |
| 寻呼（Paging） | 网络在 Paging Occasion 唤醒终端，下行可达性依赖它 | 无寻呼；AP 在 Beacon 的 TIM/DTIM 里提示有缓冲帧 |
| 位置登记 | 网络需知道终端所在 TA/RNA 才能呼入 | 网络不知道也不关心终端在哪 |

> **创作提示**：蜂窝手机待机省电的关键，不是"关收音机"，而是在 DRX 节奏下周期性醒来监听 PDCCH/寻呼——这套流程 WiFi 没有对应物，这是两者待机功耗差别的架构根源之一。

### 来源
- ITU 技术报告（手机发射功率/工作距离表）：https://itu.ch/wftp3/Public/epub_shared/TSB/ITUT-Tech-Report-Specs/2016/en/ITUT-Tech-Rep-Specs-2016_opf_files/pdfs/ITUT-Tech-Rep-Specs-2016_612.pdf  **[已查证]**
- 5G/6G Academy《EPC vs 5GC》（MME/AMF 职责对比）：https://www.5g6gacademy.com/compare/epc-vs-5gc  **[已查证]**
- CableLabs《A Comparative Introduction to 4G and 5G Authentication》：https://www.cablelabs.com/tech-vision/tech-policy/informed-insights-whitepapers/a-comparative-introduction-to-4g-and-5g-authentication  **[已查证]**
- NTT DOCOMO 技术期刊《Overview of 5G Core Network Technologies》：https://www.docomo.ne.jp/english/corporate/technology/rd/technical_journal/bn/vol24_4/001.html  **[已查证]**
- ETSI TS 123 501（3GPP TS 23.501，5GS 系统架构）：https://www.etsi.org/deliver/etsi_ts/123500_123599/123501/17.06.00_60/ts_123501v170600p.pdf  **[已查证]**

---

## 子问题 2：基站距离、信号强度对功耗的影响机制

### 结论
手机上行发射功率是由**下行信号强度反推**的：下行越弱＝路径损耗越大＝手机必须把功率放大器（PA）的工作点往上抬。距离每翻一倍，自由空间路径损耗约增加 **6 dB**；而 PA 在接近最大功率时效率会急剧恶化，导致"为了发同样的数据，电池消耗非线性飙升"。

### 技术解释

#### 2.1 自由空间路径损耗与"距离翻倍 +6 dB"
- 自由空间路径损耗公式（ITU-R P.525-3 / Friis）：
  **FSPL(dB) = 20·log₁₀(4πd/λ) = 20·log₁₀(d) + 20·log₁₀(f) + 常数**
- 由于距离项是 **20·log₁₀(d)**，距离 d 翻倍时：20·log₁₀(2) ≈ **6.02 dB**。即"距离每增加一倍，路径损耗约增加 6 dB"是对数距离关系的直接推论。[已查证]
- 真实城区还有阴影衰落和多径，路径损耗指数通常 >2（约 2.7–3.5），实际衰减比自由空间更陡；但"距离越远、损耗越大、手机越要抬功率"的机制不变。

#### 2.2 开环功率控制：手机"听下行强弱，自己决定上行发多大力"
- LTE/5G 上行功率控制由**开环＋闭环**组成。开环部分：UE 测量下行参考信号（CRS/SSB）的接收功率（RSRP），与网络广播的参考信号发射功率比较，估算路径损耗：
  **路径损耗 = 参考信号发射功率 − 实测 RSRP**
- 路径损耗越大，UE 上行发射功率设定越高（部分路径损耗补偿 α·PL）。ShareTechnote（基于 3GPP 流程）与 3GPP RAN4 文稿均确认："UE decode 参考信号并测其功率，再与网络告知的参考功率比较，即可算出到基站的路径损耗，从而决定允许的发射功率。"[已查证]
- 5G NR 进一步是**波束级**路径损耗（beam-dependent），FR2 毫米波因遮挡路径损耗变化极快，上行功率更不稳定。[已查证]

#### 2.3 为什么信号差时 PA 必须"高工作点"且效率下降
- 蜂窝发射是**线性调制信号**（OFDM/QAM，峰均比 PAPR 高），PA 必须工作在功率回退区以保证线性度，避免频谱泄漏（ACLR）。
- PA 效率随输出功率非单调：在接近饱和点（Psat/P1dB）时效率最高，越往下回退效率越低。
  - 典型 Class-AB PA：Psat 处效率约 50%，**6 dB 回退处约 25%，10 dB 回退处约 10%**。[已查证]
  - 工程综述给出另一组口径：峰值 80% 效率的 PA，6 dB 回退后可降到 40% 甚至更低。[已查证]
  - 手机常用 Doherty 结构改善回退效率：某手机 Doherty PA 在 P1dB=30 dBm 时 PAE 44%，6 dB 回退处仍有 34%。[已查证]
- **关键反差**：信号差时手机被迫把 PA 顶到高输出（接近最大功率），此时虽然接近效率峰值点，但**绝对功耗基数大**，且为维持线性度还要配合包络跟踪（ET）等电路；更重要的是弱信号下伴随重传、长占空比、频繁唤醒（见子问题 4），整体能耗被放大。
- 反之，近距离/强信号时手机只需很低的上行功率（功率控制下限可到约 −40 dBm），PA 工作在低功耗区，瞬时电流小。

### 来源
- ITU-R P.525-3《计算自由空间损耗》（FSPL=20log(4πd/λ)）：https://www.itu.int/dms_pubrec/itu-r/rec/p/R-REC-P.525-3-201611-S!!PDF-C.pdf  **[已查证]**
- noim3《FSPL 公式与 6 dB 规则》（距离翻倍 20log10 2 ≈ 6.02 dB）：https://noim3.com/what-is-free-space-path-loss-fspl  **[已查证]**
- ShareTechnote《Power Control LTE》（UE 测 RSRP→算路径损耗→定上行功率）：https://5ghub.ericsson.sharetechnote.com/html/PowerControl_LTE.html  **[已查证]**
- NXG Connect《Power Control in 5G NR》（波束级路径损耗、FR2 遮挡）：https://www.nxgconnect.com/post/power-control-in-5g-nr  **[已查证]**
- 3GPP RAN4 R4-99362《UE output power dynamics / open loop power control》：https://www.3gpp.org/ftp/TSG_RAN/WG4_Radio/TSGR4_06/Docs/Pdfs/r4-99362.pdf  **[已查证]**
- RF Essentials《Sequential PA / back-off efficiency》（Class-AB：Psat≈50%、6 dB 回退≈25%、10 dB 回退≈10%）：https://rfessentials.com/rf-knowledge-base/what-is-the-sequential-power-amplifier-concept-and-how-does-it-improve-efficienc/  **[已查证]**
- Engineering Niche《PA efficiency on battery life》（峰值 80%→6 dB 回退 ≤40%）：https://engineeringniche.com/article/the-impact-of-power-amplifier-efficiency-on-battery-life-in-portable-devices/  **[已查证]**
- ResearchGate《A Handy Dandy Doherty PA for mobile handset》（30 dBm P1dB→44% PAE，6 dB 回退→34%）：https://www.researchgate.net/publication/319425818  **[已查证]**

---

## 子问题 3：移动网络与 WiFi 在射频功率、数据传输方式上的具体差异

### 结论
**手机蜂窝上行发射功率上限（GSM 约 2 W，LTE/5G 约 200 mW）普遍比手机 WiFi 模块（实测约 10–20 mW）高出一个数量级以上**；同时蜂窝必须持续监听寻呼信道、用 DRX/eDRX 休眠，WiFi 则用 PSM/DTIM 让终端整体"打盹"。调制方式、MIMO、载波聚合（CA）会进一步改变瞬时功耗。

### 技术解释

#### 3.1 上行最大发射功率对比（核心数值，均有标准/认证文档支撑）
| 技术 | 功率等级 | 最大发射功率 | 换算 | 来源/口径 |
|---|---|---|---|---|
| GSM（GSM900/850） | Power Class 4（手持机强制 class 4/5） | **+33 dBm** | ≈ **2 W** | ETSI GSM 02.06 / 05.05；模组手册实测 +33 dBm±2 dB。**[已查证]** |
| GSM（DCS1800/PCS1900） | Class 1 | +30 dBm | ≈ 1 W | 同上。**[已查证]** |
| LTE（FDD/TDD） | Power Class 3（主流手机） | **+23 dBm** | ≈ **200 mW** | 3GPP LTE-Advanced RF 文稿；NTIA LTE 特性文档（最大 23 dBm、最小 −40 dBm、动态范围 63 dB）。**[已查证]** |
| 5G NR | PC3（主流手机） | **+23 dBm** | ≈ **200 mW** | 工信部 YD/T 3627 修改单、ETSI TS 138 161。**[已查证]** |
| 5G NR | PC2（TDD SA，高功率终端） | +26 dBm | ≈ 400 mW | 工信部 YD/T 3627（SA 模式 TDD 必选 PC2=+26 dBm）。**[已查证]** |
| 手机 WiFi 模块（conducted，非 AP） | — | 约 **+11～+13 dBm** | ≈ **12～20 mW** | FCC ID 认证报告中手机 WiFi 802.11b/g/n 峰值传导功率实测约 11.2–12.3 dBm。**[已查证]** |

- **注意区分**：各国法规对 WiFi EIRP 的上限很高（美国 FCC 2.4 GHz Part 15.247 可达 30 dBm 传导＋6 dBi 天线＝36 dBm EIRP），但那是**路由器/AP** 的发射上限；**手机端 WiFi 模组**因近距离、省电需求，实际传导功率远低于此，FCC 认证报告里多在 10–13 dBm。[已查证]
- 结论性对比：**手机蜂窝最大发射（200 mW～2 W）是手机 WiFi 实际发射（约 10–20 mW）的 10～100 倍**。这是两者射频功耗差别的物理基数。

#### 3.2 持续监听 vs 周期唤醒：寻呼/DRX 与 WiFi PSM
- **蜂窝必须"常驻"控制信道**：即使无数据，UE 也要在 RRC_IDLE 周期醒来监听 PDCCH/寻呼。DRX（Discontinuous Reception）让 UE 在两次唤醒之间关闭接收机进入低功耗休眠，只在预设 Paging Occasion 醒来——"没有 DRX，UE 会每个 slot 都监听 PDCCH，电池一天都撑不住"。[已查证]
- **eDRX**：DRX 的增强版，进一步拉长监听周期，主要面向 LTE-M/NB-IoT 这类低功耗广域物联网设备，手机场景较少用到，但机制同源。[已查证]
- **WiFi PSM（Power Save Mode）**：终端（STA）在 doze 状态**整体关掉射频收发**，AP 负责为其缓存下行帧；STA 每个 Listen Interval（若干 Beacon 间隔）醒来听 Beacon，看 TIM/DTIM 里有没有自己 AID 的缓冲帧，有则发 PS-Poll 取数据。IETF 文稿与 802.11ba 论文均确认：PSM 下 STA 在 awake/doze 两态切换，doze 时既不能发也不能收。[已查证]
- **结构差异**：蜂窝的 DRX 是"在连接态/空闲态周期性监听控制信道"，唤醒后要做基带解调；WiFi 的 PSM 更简单，终端可整体断电，AP 替它"看着门"。

#### 3.3 状态功耗量级（RRC 状态机）
- 移动网络性能领域广泛引用的一组量级（Ilya Grigorik《High Performance Browser Networking》）：
  - **RRC_IDLE**：低功率，约 **<15 mW**，只监听寻呼/广播；
  - **RRC_CONNECTED**：高功率，约 **1000–3500 mW**，专用无线资源已分配。[一方称/行业广泛引用，非单一规范数值]
- MIT CSAIL（Conext'12）论文确认 LTE 只有 RRC_CONNECTED 与 RRC_IDLE 两态，无数据一段时间后网络把设备降回 Idle；WiFi 侧 CAM（常醒）↔PSM（打盹）切换。[已查证]
- 含义：蜂窝从"空闲"到"传数据"要经历 RRC 连接建立，且传输结束后有一段"尾（tail）功耗"维持在 CONNECTED 高功率态，这部分"尾巴能耗"WiFi 没有对应物。

#### 3.4 调制方式、MIMO、载波聚合（CA）对功耗的影响
- **调制/MCS**：高阶调制（64/256-QAM）速率高但需要更高 SNR、更可靠链路；弱信号时被迫降阶到低阶调制（QPSK/低码率），传同样数据占用空中接口时间更长，射频通电时间更长。Ding 2013 实测：WiFi 在 −90 dBm 时 **92.6% 的帧用最低 1 Mbps 速率**发送。[已查证]
- **MIMO/多接收链**：多天线 MIMO 提升速率但要多开接收链路。
- **载波聚合 CA**：聚合多个分量载波（CC）需额外接收链。实测：
  - 多个 CC 会增加约 **300 mW** 的接收链供电；只要资源块（RB）能塞进单载波，就不应开 CA。[已查证]
  - 真机实测：2 个 10+10 MHz 载波在传输期间比单载波多耗约 **15% 能量**；3 CC 比 2 CC 再高约 7%。[已查证]
  - 另一组实测：CA 使活跃传输期间电流 +13%，但因传输更快结束、更早进入 Idle，平均能耗反而下降约 39%。[已查证]
  - 含义：CA 是"瞬时功耗↑、但传输时间↓"的权衡，弱信号下往往无法靠 CA 提速，却仍要付出多链代价。

### 来源
- ETSI GSM 02.06《Types of MS》（GSM class 4 手持机功率表）：https://www.etsi.org/deliver/etsi_i_ets/300500_300599/300504/01_60/ets_300504e01p.pdf  **[已查证]**
- 3GPP LTE-Advanced RF Aspects（UE transmit power BC3=23 dBm max）：https://www.3gpp.org/ftp/workshop/2009-12-17_itu-r_imt-adv_eval/docs/pdf/rev-090006.pdf  **[已查证]**
- NTIA《LTE(FDD) Transmitter and Receiver Characteristics》（23 dBm 最大、−40 dBm 最小、63 dB 动态范围）：https://ntia.gov/sites/default/files/meetings/lte_technical_characteristics_0.pdf  **[已查证]**
- 工信部 YD/T 3627 修改通知单（5G UE 功率等级 PC2=+26 dBm / PC3=+23 dBm）：https://www.miit.gov.cn/cms_files/filemanager/1226211233/attach/202112/11bdf077d692418794ee2d29090180e0.pdf  **[已查证]**
- ETSI TS 138 161（5G NR UE TRP/功率等级 PC2/PC3 测试）：https://www.etsi.org/deliver/etsi_ts/138100_138199/138161/19.01.00_60/ts_138161v190100p.pdf  **[已查证]**
- FCC ID 认证报告（手机 WiFi 802.11b/g/n 传导功率 11.2–12.3 dBm）：https://fccid.io/QISU8186-7/RF-Exposure-Info/RF-Exposure-info-attachment-1736407.pdf  **[已查证]**
- RF Essentials《WiFi 各国法规最大发射功率》（FCC 2.4G 30 dBm/36 dBm EIRP，属 AP/路由器口径）：https://rfessentials.com/rf-knowledge-base/what-is-the-maximum-transmit-power-for-a-wi-fi-device-operating-in-each-regulato/  **[已查证]**
- 3GPP Spec Explorer《DRX》：https://3gpp-explorer.com/glossary/drx/  **[已查证]**
- ShareTechnote《5G Paging / DRX》：https://www.sharetechnote.com/html/5G/5G_Paging.html  **[已查证]**
- TELCOMA《eDRX》：https://telecomtrainingpro.com/what-is-edrx-extended-discontinuous-reception/  **[已查证]**
- IETF 文稿《802.11 PSM：STA 睡、AP 缓存、Listen Interval 醒来听 Beacon》：https://www.ietf.org/proceedings/90/id/draft-ietf-lwig-energy-efficient-03.txt  **[已查证]**
- arXiv《IEEE 802.11ba》（PSM awake/doze，doze 时不能收发）：https://arxiv.org/html/1909.00594v1  **[已查证]**
- Ilya Grigorik《High Performance Browser Networking》移动网络 RRC 状态功耗（IDLE <15 mW / CONNECTED 1000–3500 mW）：https://quheng.gitbooks.io/high-performance-browser-networking/content/mobile-networks.html  **[一方称，行业广泛引用]**
- MIT CSAIL Conext'12《Traffic-Aware Techniques...》：http://people.csail.mit.edu/shuodeng/papers/conext12.pdf  **[已查证]**
- TU Dortmund SFB876《CA is economical?》（多 CC 增加约 300 mW 接收链）：https://sfb876.tu-dortmund.de/en/PublicPublicationFiles/falkenberg_etal_2017a.pdf  **[已查证]**
- SBRT2020《LTE-A UE Power for CA》（CA 活跃电流 +13%，平均能耗 −39%）：https://www.sbrt.org.br/sbrt2020/papers/1570661121.pdf  **[已查证]**
- Bazzo 2020《UE current consumption on CA》（2CC 10+10 传输多耗约 15%，3CC 再 +7%）：https://sci-hub.st/downloads/2021-06-16/83/joaobazzo2020.pdf  **[已查证]**

---

## 子问题 4：为什么信号差时手机更费电——底层机制与实测数据

### 结论
弱信号费电不是单一原因，而是**五条机制叠加**：①PA 被顶到高功率区、线性度代价大；②链路/BLER 升高导致 MAC/链路层重传激增；③手机频繁做小区测量/重选和主动扫描；④RRC 在 IDLE↔CONNECTED 间频繁切换、产生"连接建立＋尾功耗"；⑤为维持可达性而高频唤醒。**受控实验**显示：WiFi RSSI 从 −50 降到 −90 dBm，传同样 100 KB 数据能耗可增加约 **810.5%**；3G RSSI 从 −85 降到 −105 dBm，能耗增加约 **52.0%**。

### 技术解释

#### 4.1 PA 效率与高工作点代价
- 见子问题 2.3：弱信号→路径损耗大→开环功率控制把上行功率往上顶→PA 接近饱和/高工作点。此时虽然接近效率峰值，但**绝对输出功率大**（从近距离的 0 dBm 量级抬到 +10～+23 dBm），电池电流成倍上升；同时 OFDM 高 PAPR 要求 PA 留足回退余量，配合包络跟踪/偏置电路，静态功耗也上升。[已查证]

#### 4.2 重传机制：BLER 升高 → MAC/链路层重传暴增
- 弱信道下误块率（BLER）升高，未被 ACK 的数据帧要在 MAC/链路层重传，传输一次成功的概率下降，实际"发一次"变成"发 N 次"。
- **Ding 2013 受控实测（WiFi）**：
  - DATA 帧重传率从 **−60 dBm 的 1.3%** 飙升到 **−85 dBm 的 58.7%**、**−90 dBm 的 97.7%**；
  - ACK 帧重传率从 **−50 dBm 的 14.9%** 升到 **−90 dBm 的 146.0%**；
  - −90 dBm 时 92.6% 的帧被迫用最低 1 Mbps 速率发送。[已查证]
- 含义：弱信号时"传同样的字节数"，空中接口上实际发送的帧数、射频通电时间都翻倍甚至十几倍，这是能耗放大的最直接来源。

#### 4.3 小区搜索/测量与主动扫描
- **蜂窝（IDLE 态）**：UE 持续测量服务小区与邻区 RSRP/RSRQ。当服务小区质量低于网络配置的 Qsearch 阈值时，UE 必须**持续测量**并尝试小区重选；若找不到合格小区，会做全频段扫描、尝试更高优先级 PLMN，这些都要开射频与基带。3GPP TS 36.304（LTE）/ TS 38.304（5G）规定了空闲态小区重选与测量规则。[已查证]
- **WiFi**：当信号低于约 −80 dBm 时，手机会发起主动扫描（Probe Request/Response），正常约 40–100 ms 完成；弱信号下 Probe 帧及其 ACK 丢失，扫描可拖到约 **1 秒**、伴随数十次重传，显著耗电。Ding 2013 实测记录。[已查证]

#### 4.4 RRC 状态频繁切换与"尾功耗"
- 弱信号下数据断断续续：每次有数据要传都要从 RRC_IDLE 建立 RRC 连接（RACH→RRC Setup→鉴权/承载），传输完又因不活跃被降回 IDLE，反复在两态间跳变。
- RRC_CONNECTED 高功率态（行业引用约 1000–3500 mW）即使没有数据也会维持一段"尾（tail）时间"再释放，这部分"空等"的能耗在弱信号下被频繁切换放大。[一方称/行业广泛引用；机制本身 MIT/arXiv 论文已查证]
- 5G 引入 RRC_INACTIVE 态正是为了缓解"CONNECTED↔IDLE 频繁重建"的信令与能耗代价。[已查证]

#### 4.5 高频监听/可达性维持
- 弱信号下 UE 往往需要更频繁地测量邻区、更快地在 DRX 唤醒窗口保持接收，以避免掉网；寻呼信道监听、SIB 解码等基带处理次数增加。[已查证]

#### 4.6 关键实测数据（信号强度 ↔ 功耗/时延）
| 场景 | 信号条件 | 实测结果 | 来源/口径 |
|---|---|---|---|
| WiFi 传 100 KB（30 ms RTT） | RSSI −50 → −90 dBm | 能耗增加约 **810.5%**（低速率＋MAC 重传主导） | Ding 2013 受控实验。**[已查证]** |
| 3G 传 100 KB（30 ms RTT） | RSSI −85 → −105 dBm | 能耗增加约 **52.0%**（数据传输＋RRC 状态降档主导） | Ding 2013。**[已查证]** |
| WiFi DATA 帧重传率 | −60 / −85 / −90 dBm | 1.3% / 58.7% / 97.7% | Ding 2013。**[已查证]** |
| WiFi ACK 帧重传率 | −50 / −90 dBm | 14.9% / 146.0% | Ding 2013。**[已查证]** |
| WiFi 主动扫描 | <−80 dBm | 正常 40–100 ms；弱信号下最长约 1 s、数十次重传 | Ding 2013。**[已查证]** |
| 蜂窝时延参考 | RSRP −70～−80 vs −100～−110 dBm | 平均时延约 40 ms vs 86 ms | IJARSE 实测论文。**[已查证]** |
| 5G 全天掉电（强信号下） | 5G 开启、信号良好 | 24 h 掉电 27%–32%（比 LTE 高约 7–10 个百分点） | abwavestech 博客 15 机测试。**[一方称]** |

> **关于"−120 dBm vs −70 dBm 功耗对比"**：题目设想的这组精确对照（−120 vs −70 dBm）未在本调研中找到公开、带测试条件的权威实测数值直接给出 mA 对比。可稳妥引用的是 Ding 2013 的 −50→−90（WiFi）、−85→−105（3G）受控对照，以及 RSRP −70~−80 vs −100~−110 的时延对照；−120 dBm 已接近多数终端的接收灵敏度下限，多处于频繁小区重选/脱网状态，功耗会进一步恶化，但具体 mA 数值建议以厂商实验室数据或自行测试为准，不宜直接编造。

### 来源
- Ding 2013《Characterizing and Modeling the Impact of Wireless Signal Strength on Smartphone Battery Drain》（MobiCom 系；WiFi −50→−90 dBm 能耗 +810.5%；3G −85→−105 dBm +52.0%；重传率/扫描实测）：https://www.sci-hub.st/storage/2024/4375/faaae7a45ebcaa89f0766e5bfd811478/ding2013.pdf  **[已查证]**
- ETSI TS 136 304（LTE UE 空闲态小区重选流程）：https://www.etsi.org/deliver/etsi_ts/136300_136399/136304/09.01.00_60/ts_136304v090100p.pdf  **[已查证]**
- ETSI TS 138 304（5G NR 空闲/RRC_INACTIVE 小区重选与 RNA 更新）：https://www.etsi.org/deliver/etsi_ts/138300_138399/138304/19.01.00_60/ts_138304v190100p.pdf  **[已查证]**
- 3GPP R2-99808《Cell Selection and Reselection Criteria》（低于 Qsearch 仍须持续测量）：https://www.3gpp.org/FTP/tsg_ran/WG2_RL2/TSGR2_06/Docs/Pdfs/r2-99808.pdf  **[已查证]**
- MIT CSAIL Conext'12（RRC 状态/tail 能耗）：http://people.csail.mit.edu/shuodeng/papers/conext12.pdf  **[已查证]**
- Olax Wireless《5G RRC_INACTIVE 态为何存在》（缓解 IDLE↔CONNECTED 重建代价）：https://www.olaxwireless.com/blogs/5g-nr-terminal-ue-rrc-inactive-state-1/  **[已查证]**
- IJARSE《Anatomizing...Radio Signaling Energy》（RSRP −70~−80 vs −100~−110 dBm 时延 40 vs 86 ms）：https://mail.ijarse.com/ADMIN/admin/postimages/images/fullpdf/1527223826_Reva529ijarse.pdf  **[已查证]**
- abwavestech《I tested 15 Phones for 5G battery drain》（5G 强信号 24h 掉电 27–32%）：https://abwavestech.com/i-tested-15-phones-for-5g-battery-drain/  **[一方称]**

---

## 附：可直接引用的核心数字清单（供内容创作）
1. **GSM 手机最大发射功率 +33 dBm ≈ 2 W**（手持机 Power Class 4，ETSI GSM 02.06/05.05）。
2. **LTE/5G 手机主流功率等级 +23 dBm ≈ 200 mW**（3GPP Power Class 3）；5G TDD 高功率终端 +26 dBm ≈ 400 mW。
3. **手机 WiFi 模组实测传导功率约 +11～+13 dBm ≈ 12～20 mW**（FCC 认证报告）；即手机蜂窝发射功率基数是 WiFi 的约 10～100 倍。
4. **距离翻倍，自由空间路径损耗约 +6 dB**（20·log₁₀2，ITU-R P.525）。
5. **PA 效率**：Class-AB 在 Psat 约 50%、6 dB 回退约 25%、10 dB 回退约 10%；手机 Doherty PA 在 6 dB 回退仍有约 34% PAE。
6. **RRC 状态功耗（行业广泛引用）**：IDLE <15 mW，CONNECTED 约 1000–3500 mW。
7. **弱信号受控实验（Ding 2013）**：WiFi RSSI −50→−90 dBm，100 KB 下载能耗 +810.5%；3G −85→−105 dBm，能耗 +52.0%；WiFi DATA 重传率 −60/−85/−90 dBm 为 1.3%/58.7%/97.7%。
8. **载波聚合代价**：多 CC 增加约 300 mW 接收链；2CC 传输期多耗约 15% 能量。

> 风险提示：标注为"一方称"的数值（RRC 状态 mW 量级、abwavestech 5G 掉电）在正式内容中建议表述为"行业测试/普遍引用"，避免写成规范定值；−120 dBm vs −70 dBm 的精确 mA 对比暂无公开权威数据，不建议直接给出具体数值。
