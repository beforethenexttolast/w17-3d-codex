# p0_d36 — wire-schedule validation

| Check | Result | Detail |
|---|---|---|
| authoritative connector map exists | **PASS** | ../w17-electrical-inputs-for-codex.md |
| authoritative connector map hash | **PASS** | e7b96a8fdbaeeed47352c208777743f70e0b4f60b252527eff12d9fb43d6fd51 |
| authoritative control PinMap exists | **PASS** | ../w17-control-fw/lib/config/include/config/PinMap.hpp |
| authoritative control PinMap hash | **PASS** | bf6cfe79aa4eedfcf356e92e393dd0d6789b19b9f74009a205ca308bf0dbaf8b |
| authoritative sound/light PinMap exists | **PASS** | ../w17-soundlight-fw/lib/config/include/config/PinMap.hpp |
| authoritative sound/light PinMap hash | **PASS** | 71e0a93a63f1c899717454ebcbe55ae37e5bb6122d63f15d5b69b1ad90510f5d |
| control firmware pin tokens | **PASS** | 11 exact assignments |
| sound/light firmware pin tokens | **PASS** | 6 exact assignments |
| CSV exists | **PASS** | 10_assembly_architecture/Z_wire_schedule.csv |
| CSV exact generator parity | **PASS** | 96/96 rows |
| wire IDs unique | **PASS** | 96 unique IDs |
| per-row fields complete | **PASS** | 96 complete physical cuts |
| bundle build order | **PASS** | on-PDB → on-cassette → pedestal-conduit → umbilical |
| four-bundle coverage | **PASS** | on-PDB=15, on-cassette=48, pedestal-conduit=12, umbilical=21 |
| Markdown exists | **PASS** | 10_assembly_architecture/Z_wire_schedule.md |
| Markdown wire-ID coverage | **PASS** | all IDs present |
| Markdown Joint-ID links | **PASS** | every row has one or more clickable Joint Register links |
| Markdown sources and totals | **PASS** | source hashes + control-pin provenance + wire/connector totals + ASM checks |
| connector-count manifest | **PASS** | 34 mating pairs/receptacles; 67 housings/halves; 175 loaded contacts/mapped pads |
| cut arithmetic | **PASS** | route + slack + relief = cut for every row |
| rounded estimate discipline | **PASS** | all route/slack/relief/cut values are 10 mm increments |
| gauge vocabulary | **PASS** | 16 AWG, 20 AWG, 22 AWG, 24 AWG, 28 AWG, 50 Ω micro-coax |
| battery-main gauge | **PASS** | all battery-main cuts are 16 AWG |
| RF no-field-cut rule | **PASS** | U.FL rows are factory-terminated 80 mm leads |
| dry-fit flags | **PASS** | all field wire waits for dry-fit; coax is buy-to-length |
| authoritative endpoint-pair coverage | **PASS** | 20 exact pairs |
| no invented GPIO | **PASS** | ESP32#1.GPIO13, ESP32#1.GPIO14, ESP32#1.GPIO16, ESP32#1.GPIO17, ESP32#1.GPIO18, ESP32#1.GPIO19, ESP32#1.GPIO23, ESP32#1.GPIO25, ESP32#1.GPIO26, ESP32#1.GPIO34, ESP32#1.GPIO35, ESP32#2.GPIO4, ESP32#2.GPIO16, ESP32#2.GPIO17, ESP32#2.GPIO22, ESP32#2.GPIO25, ESP32#2.GPIO26 |
| per-circuit cut coverage | **PASS** | 96 physical pieces across 32 circuits |
| ganged-dock two-sided segmentation | **PASS** | 10 remote circuits have SOURCE and LOAD cuts |
| in-transit DEFER discipline | **PASS** | 33 cuts deferred |
| optional ACK not populated | **PASS** | one GPIO17(#2)→GPIO26(#1) reserve |
| ESC BEC isolation | **PASS** | signal + GND only; no +5 conductor |
| source-side power shrouding | **PASS** | XT60 + both dock XT30 source halves explicitly shrouded/socketed |
| Joint-ID cross-links resolve | **PASS** | 24 unique Joint IDs |
| traction-power omission disclosed | **PASS** | PDB→ESC and ESC→motor await authoritative map update |
| blower conduit conflict disclosed | **PASS** | blower route remains HOLD, not silently added to firm conduit |

**Verdict: PASS — 36/36 checks passed.**
