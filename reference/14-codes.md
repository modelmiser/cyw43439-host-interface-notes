# Codes and encodings

Chanspec encoding, command status codes, and the status, reason and flag codes of events, as each driver defines and uses them.

## Chanspec encoding

A chanspec is an unsigned 16-bit word in all four drivers. `linux/include/brcmu_d11.h:131` `whd/inc/whd_types.h:918` `whd/src/include/whd_wlioctl.h:48` `embassy/structs.rs:527-528` `c-driver/cyw43_ll.c:497`

linux and whd describe it as holding channel number, band, bandwidth and control sideband. `linux/include/brcmu_d11.h:13-15` `linux/include/brcmu_wifi.h:12-15` `whd/inc/whd_types.h:918`

Chanspec handling is not found in embassy-pio, the sdio-crate sources or the pico-sdk Bluetooth shared-bus file: the names `chanspec` and `chspec`, in any letter case, do not occur there. The citations name the files, not a particular line. `embassy-pio/lib.rs:1` `pico-sdk/cybt_shared_bus.c:1` `sdio-crate/src/lib.rs:1`

### Bit fields per version

linux names two layout versions ("d11 io type"): `BRCMU_D11N_IOTYPE` = 1 and `BRCMU_D11AC_IOTYPE` = 2. `linux/include/brcmu_d11.h:9-11` `linux/include/brcmu_d11.h:139-152`

Bits 0-7 are the channel number in both layouts. The upper byte differs. `linux/include/brcmu_d11.h:20-24` `linux/include/brcmu_d11.h:30-49` `linux/include/brcmu_d11.h:51-86`

| Layout | Bits | Mask | Shift | Field | Values | Citations |
|---|---|---|---|---|---|---|
| both | 0-7 | 0x00ff | 0 | channel number | linux uses one `BRCMU_CHSPEC_CH_MASK` for D11N and D11AC; whd uses `WL_CHANSPEC_CHAN_MASK` 0x00ff for every chip; c-driver masks a received value with 0xff; embassy has no channel mask constant and never extracts the channel | `linux/include/brcmu_d11.h:20-24` `linux/brcmutil/d11.c:100` `linux/brcmutil/d11.c:141` `whd/src/include/whd_chip_constants.h:75` `whd/src/include/whd_chip_constants.h:85` `c-driver/cyw43_ll.c:714` `embassy/lib.rs:102-114` |
| both (linux header only) | 0-3, 4-7 | 0x000f, 0x00f0 | 0, 4 | 80+80 MHz: low channel id, high channel id | linux's decoder treats an 80+80 bandwidth code as an invalid chanspec (WARN). Not found in whd, embassy or c-driver | `linux/include/brcmu_d11.h:20-28` `linux/brcmutil/d11.c:218-221` |
| D11N (io type 1) | 8-9 | 0x0300 | 8 | control sideband | 0x0100 lower, 0x0200 upper, 0x0300 none | `linux/include/brcmu_d11.h:30-49` |
| D11N | 10-11 | 0x0c00 | 10 | bandwidth | 0x0400 10 MHz, 0x0800 20 MHz, 0x0c00 40 MHz | `linux/include/brcmu_d11.h:30-49` |
| D11N | 12-13 | 0x3000 | 12 | band | 0x1000 5 GHz, 0x2000 2.4 GHz | `linux/include/brcmu_d11.h:30-49` |
| D11N | 14-15 | | | "not used" | | `linux/include/brcmu_d11.h:30-49` |
| D11AC (io type 2) | 8-10 | 0x0700 | 8 | control sideband | LLL 0x0000, LLU 0x0100, LUL 0x0200, LUU 0x0300, ULL 0x0400, ULU 0x0500, UUL 0x0600, UUU 0x0700. Aliases: LL=LLL, LU=LLU, UL=LUL, UU=LUU, L=LLL, U=LLU | `linux/include/brcmu_d11.h:51-86` |
| D11AC | 11-13 | 0x3800 | 11 | bandwidth | 0x0000 5 MHz, 0x0800 10 MHz, 0x1000 20 MHz, 0x1800 40 MHz, 0x2000 80 MHz, 0x2800 160 MHz, 0x3000 80+80 MHz | `linux/include/brcmu_d11.h:51-86` |
| D11AC | 14-15 | 0xc000 | 14 | band | 0x0000 2G, 0x4000 "3G", 0x8000 "4G", 0xc000 5G | `linux/include/brcmu_d11.h:51-86` |

The number in bits 0-7 is the centre channel, not the control (primary) channel, per linux: `struct brcmu_chan.chnum` is documented as the centre channel number and the encoder "requires center channel number, ignores control one". `linux/include/brcmu_d11.h:123-128` `linux/include/brcmu_d11.h:143-145`

whd's scan-result code says the same for 40 MHz or wider: the channel in the chanspec is the centre frequency, which may differ from the 20 MHz channel the beacon is on. `whd/src/whd_wifi_api.c:2690-2692`

"No sideband" is encoded differently in the two layouts. D11N has a dedicated code 0x0300; D11AC has none. `linux/include/brcmu_d11.h:40`

| Driver | "No sideband" value in the D11AC-valued set | Citations |
|---|---|---|
| linux | encoder substitutes sideband L (0x0000) for 20 MHz or `SB_NONE` | `linux/brcmutil/d11.c:43-44` `linux/brcmutil/d11.c:79-80` |
| whd | returns `WL_CHANSPEC_CTL_SB_LLL` (0x0000) as `CHANSPEC_CTL_SB_NONE` for non-legacy chips, 0x0300 for legacy ones | `whd/src/whd_chip_constants.c:598-610` |
| embassy | `chanspec_ctl_sb_none` 0x0000, equal to `chanspec_ctl_sb_lower` | `embassy/lib.rs:290-292` |
| c-driver | defines `WL_CHANSPEC_CTL_SB_NONE` as `WL_CHANSPEC_CTL_SB_LLL` | `c-driver/cyw43_ll.c:2313-2314` |

### Constant sets per driver

"whd legacy" is whd's set for chip ids 43362, 4334, 43340, 43342. "whd other" is whd's set for every other chip id, which includes 43430 and 43439 (neither is in the legacy list). `whd/src/whd_chip_constants.c:132-136` `whd/src/whd_chip_constants.c:163-228` `whd/src/whd_chip_constants.c:430-610` `whd/src/whd_chip_constants.c:724-736`

| Constant | linux D11N | whd legacy | linux D11AC | whd other | embassy (43439) | c-driver | Citations |
|---|---|---|---|---|---|---|---|
| band mask | 0x3000 | 0xf000 | 0xc000 | 0xc000 | 0xc000 | not defined | `linux/include/brcmu_d11.h:30-49` `whd/src/whd_chip_constants.c:430-441` `linux/include/brcmu_d11.h:51-86` `whd/src/whd_chip_constants.c:430-610` `embassy/lib.rs:281-293` |
| band 2G | 0x2000 | 0x2000 | 0x0000 | 0x0000 | 0x0000 | 0x0000 | `linux/include/brcmu_d11.h:30-49` `whd/src/whd_chip_constants.c:430-470` `linux/include/brcmu_d11.h:51-86` `whd/src/whd_chip_constants.c:430-610` `embassy/lib.rs:281-293` `c-driver/cyw43_ll.c:2312-2315` |
| band 5G | 0x1000 | 0x1000 | 0xc000 | 0xc000 | 0xc000 | not defined | `linux/include/brcmu_d11.h:30-49` `whd/src/whd_chip_constants.c:430-470` `linux/include/brcmu_d11.h:51-86` `whd/src/whd_chip_constants.c:430-610` `embassy/lib.rs:281-293` |
| band 6G | not defined | 0 | 0x8000 is named `BND_4G` | 0x8000 for chip ids 55500, 55560, 55900, 55530; 0 for all others | not defined | not defined | `whd/src/whd_chip_constants.c:472-483` `whd/src/whd_chip_constants.c:430-483` `linux/include/brcmu_d11.h:51-86` |
| band shift | 12 | 12 for 4334, 43340, 43342; 14 for 43362 | 14 | 14 | 14 | not defined | `linux/include/brcmu_d11.h:30-49` `whd/src/whd_chip_constants.c:486-498` `linux/include/brcmu_d11.h:51-86` `embassy/lib.rs:281-293` |
| bw 10 MHz | 0x0400 | 0x0400 | 0x0800 | 0x0800 | 0x0800 | not defined | `linux/include/brcmu_d11.h:30-49` `whd/src/whd_chip_constants.c:486-610` `linux/include/brcmu_d11.h:51-86` `whd/src/whd_chip_constants.c:430-610` `embassy/lib.rs:281-293` |
| bw 20 MHz | 0x0800 | 0x0800 | 0x1000 | 0x1000 | 0x1000 | 0x1000 | `linux/include/brcmu_d11.h:30-49` `whd/src/whd_chip_constants.c:486-610` `linux/include/brcmu_d11.h:51-86` `whd/src/whd_chip_constants.c:430-610` `embassy/lib.rs:281-293` `c-driver/cyw43_ll.c:2312-2315` |
| bw 40 MHz | 0x0c00 | 0x0c00 | 0x1800 | 0x1800 | 0x1800 | not defined | `linux/include/brcmu_d11.h:30-49` `whd/src/whd_chip_constants.c:486-610` `linux/include/brcmu_d11.h:51-86` `whd/src/whd_chip_constants.c:430-610` `embassy/lib.rs:281-293` |
| bw 80 MHz | not in the D11N header | `WHD_UNSUPPORTED` | 0x2000 | 0x2000 | not defined | not defined | `linux/include/brcmu_d11.h:30-49` `whd/src/whd_chip_constants.c:486-610` `linux/include/brcmu_d11.h:51-86` `whd/src/whd_chip_constants.c:430-610` `embassy/lib.rs:281-293` |
| bw 160 MHz | not in the D11N header | `WHD_UNSUPPORTED` | 0x2800 | 0x2800 | not defined | not defined | `linux/include/brcmu_d11.h:30-49` `whd/src/whd_chip_constants.c:486-610` `linux/include/brcmu_d11.h:51-86` `whd/src/whd_chip_constants.c:430-610` `embassy/lib.rs:281-293` |
| bw mask | 0x0c00 | 0x0c00 | 0x3800 | 0x3800 | 0x3800 | not defined | `linux/include/brcmu_d11.h:30-49` `whd/src/whd_chip_constants.c:486-610` `linux/include/brcmu_d11.h:51-86` `whd/src/whd_chip_constants.c:430-610` `embassy/lib.rs:281-293` |
| bw shift | 10 | 10 for 4334, 43340, 43342; 11 for 43362 | 11 | 11 | 11 | not defined | `linux/include/brcmu_d11.h:30-49` `whd/src/whd_chip_constants.c:584-596` `linux/include/brcmu_d11.h:51-86` `embassy/lib.rs:281-293` |
| sideband none | 0x0300 | 0x0300 | no code (see above) | 0x0000 | 0x0000 | 0x0000 | `linux/include/brcmu_d11.h:40` `whd/src/whd_chip_constants.c:598-610` `embassy/lib.rs:290-292` `c-driver/cyw43_ll.c:2313-2314` |
| sideband lower | 0x0100 | 0x0100 (LLL = L) | 0x0000 | 0x0000 | 0x0000 | 0x0000 (LLL) | `linux/include/brcmu_d11.h:30-49` `whd/src/whd_chip_constants.c:612-736` `linux/include/brcmu_d11.h:51-86` `whd/src/include/whd_wlioctl.h:4215-4234` `embassy/lib.rs:281-293` `c-driver/cyw43_ll.c:2312-2315` |
| sideband upper | 0x0200 | 0x0200 (LLU = U) | 0x0100 | 0x0100 | 0x0100 | not defined | `linux/include/brcmu_d11.h:30-49` `whd/src/whd_chip_constants.c:612-736` `linux/include/brcmu_d11.h:51-86` `whd/src/include/whd_wlioctl.h:4215-4234` `embassy/lib.rs:281-293` |
| sideband LUL..UUU | not in the D11N header | `WHD_UNSUPPORTED` | 0x0200..0x0700 | 0x0200..0x0700 | not defined | not defined | `linux/include/brcmu_d11.h:30-49` `whd/src/whd_chip_constants.c:612-736` `linux/include/brcmu_d11.h:51-86` `whd/src/include/whd_wlioctl.h:4215-4234` `embassy/lib.rs:281-293` |
| sideband mask | 0x0300 | 0x0300 | 0x0700 | 0x0700 | 0x0700 | not defined | `linux/include/brcmu_d11.h:30-49` `linux/include/brcmu_d11.h:51-86` `whd/src/whd_chip_constants.c:724-736` `embassy/lib.rs:281-293` |

Notes on the whd legacy set:

- The band-shift and bw-shift getters list only 4334, 43340, 43342, so chip id 43362 gets the non-legacy shifts 14 and 11 alongside the legacy masks. `whd/src/whd_chip_constants.c:486-498` `whd/src/whd_chip_constants.c:584-596`
- `get_whd_var` wraps each getter in `CHECK_RETURN`. A caller asking for bw80, bw160 or LUL..UUU on a legacy chip receives the numeric `WHD_UNSUPPORTED` result code (`WHD_RESULT_CREATE(1020)`) as if it were the constant. `whd/src/whd_chip_constants.c:187-192` `whd/src/include/whd_types_int.h:85-94` `whd/inc/whd_types.h:1009`
- `whd_chip_get_chanspec_ctl_channel_num` avoids this by returning early for the legacy chip list. `whd/src/whd_chip_constants.c:58-63`
- No code in these sources reads `CHANSPEC_BAND_SHIFT` or `CHANSPEC_BW_SHIFT` through `get_whd_var` / `GET_C_VAR`; the two names appear only in the enum and in `get_whd_var`'s own switch. `whd/src/include/whd_chip_constants.h:42` `whd/src/include/whd_chip_constants.h:49` `whd/src/whd_chip_constants.c:175` `whd/src/whd_chip_constants.c:196`

Chip-independent macros:

- whd's header defines `WL_CHANSPEC_CTL_SB_LLL`..`UUU` = 0x0000..0x0700 (aliases LL, LU, UL, UU, L, U as in linux D11AC), `WL_CHANSPEC_CTL_SB_SHIFT` 8, `WL_CHANSPEC_BW_5` 0x0000, `BW_80` 0x2000, `BW_160` 0x2800, `BW_8080` 0x3000 and `INVCHANSPEC` 255. The `include_helium` copy has the same lines. `whd/src/include/whd_wlioctl.h:4215-4234` `whd/src/include_helium/whd_wlioctl.h:4382` `whd/src/include_helium/whd_wlioctl.h:4396`
- linux also defines `INVCHANSPEC` 255 and `BRCMU_CHSPEC_INVALID` 255. `linux/include/brcmu_wifi.h:62` `linux/include/brcmu_d11.h:19`
- linux's older header `brcmu_wifi.h` repeats the D11N layout under `WL_CHANSPEC_*` names with band mask 0xf000 and an extra `WL_CHANSPEC_BW_80` 0x2000. No `.c` file in these sources uses the `WL_CHANSPEC_*` macros; `INVCHANSPEC` from the same header is used at `linux/brcmfmac/cfg80211.c:8349`. `linux/include/brcmu_wifi.h:42-62`
- The same linux header carries helpers written against those names: `CHSPEC_CHANNEL`, `CHSPEC_BAND`, `CHSPEC_CTL_SB`, `CHSPEC_BW`, `CHSPEC_IS10/20/40/80`, `CHSPEC_IS5G/IS2G`, `CHSPEC_SB_NONE/UPPER/LOWER`, `CHSPEC_CTL_CHAN`, `CHSPEC2BAND`, `chspec_bandunit()` and `ch20mhz_chspec(channel)` = channel \| 0x0800 \| 0x0300 \| (channel <= 14 ? 0x2000 : 0x1000). `linux/include/brcmu_wifi.h:97-135` `linux/include/brcmu_wifi.h:150-162`
- No `.c` file under linux/ in these sources calls `ch20mhz_chspec`, `CHSPEC_CTL_CHAN` or `chspec_bandunit` (brcmsmac is not in the source set); brcmfmac uses the d11inf encode/decode pair instead. For channel 1 `ch20mhz_chspec` would give 0x2b01, the same value as the D11N encoder. `linux/include/brcmu_wifi.h:150-162` `linux/brcmutil/d11.c:41-58`

### Which layout each driver uses
| Driver | How the layout is chosen | What it means for a 43439 | Citations |
|---|---|---|---|
| linux | At run time, once, when the cfg80211 state is attached. linux sends `BRCMF_C_GET_VERSION` (command 1) with `brcmf_fil_cmd_int_get` (reply converted le32 to cpu), truncates the result to u8 into `cfg->d11inf.io_type` and calls `brcmu_d11_attach`. That installs the D11N encode/decode pair when io_type == 1 and the D11AC pair for every other value (not only 2). A failed query aborts the attach. | Not settled by these sources. linux has no chip-id-based choice: `io_type` is referenced only at `linux/brcmfmac/cfg80211.c:8538`, `linux/brcmfmac/cfg80211.c:8576`, `linux/brcmfmac/cfg80211.c:8581`, `linux/brcmutil/d11.c:239` and `linux/include/brcmu_d11.h:142-148` (`linux/brcmfmac/cfg80211.h:399` declares the `d11inf` member that holds it). linux takes the layout from the value it reads in the reply to command 1; that value is not in these sources. | `linux/brcmfmac/cfg80211.c:8575-8582` `linux/brcmfmac/fwil.h:14` `linux/brcmfmac/fwil.h:97-104` `linux/brcmutil/d11.c:237-246` `linux/brcmfmac/cfg80211.h:399` `linux/brcmfmac/cfg80211.c:8538` |
| whd | Per chip id from a compiled table (`get_whd_var` -> `get_wl_chanspec_*`). whd never sends `WLC_GET_VERSION`: the number is defined and appears only in a name table and in an unused filter macro. | Chip ids 43362, 4334, 43340, 43342 get the D11N-valued set. Every other id, including 43430 and 43439, gets the D11AC-valued set. | `whd/src/whd_chip_constants.c:132-136` `whd/src/whd_chip_constants.c:163-228` `whd/src/whd_chip_constants.c:430-610` `whd/src/whd_chip_constants.c:724-736` `whd/src/whd_utils.c:523` `whd/src/include/whd_wlioctl.h:1304` `whd/src/include/whd_wlioctl.h:3679` |
| embassy | A compiled `ChipInfo` per chip type. `Ioctl::GetVersion` = 1 is defined but never sent. | Cyw43439, Cyw4373 and Cyw43455 all carry the same D11AC-valued set. The struct is `#[allow(unused)]`, every accessor is `#[allow(dead_code)]`, and nothing outside lib.rs calls them: embassy never encodes or decodes a chanspec and never queries the io version. | `embassy/lib.rs:91-115` `embassy/lib.rs:199-262` `embassy/lib.rs:265-294` `embassy/lib.rs:297-326` `embassy/lib.rs:329-361` `embassy/consts.rs:449` |
| c-driver | Hard-coded D11AC-valued `#define`s local to `cyw43_ll_wifi_join` (`BW_20` 0x1000, `CTL_SB_NONE` 0x0000, `BAND_2G` 0x0000). No chip-id test. `WLC_GET_VERSION` not found in c-driver. | Always the D11AC-valued constants. | `c-driver/cyw43_ll.c:2311-2315` |

### Encoding rules per driver
| Driver | Rule | Citations |
|---|---|---|
| linux, D11N (`brcmu_d11n_encchspec`) | If bw is 20 MHz force sb = NONE. Zero the word. Bits 0-7 = chnum. Sideband from the map NONE->0x0300, L->0x0100, U->0x0200. Bandwidth from the map 20->0x0800, 40->0x0c00 (any other bw: `WARN_ON`, 0). OR in 0x2000 (2G) if chnum <= 14 (`CH_MAX_2G_CHANNEL`), else 0x1000 (5G). `ch->band` is not read. | `linux/brcmutil/d11.c:13-58` `linux/include/brcmu_wifi.h:28` |
| linux, D11AC (`brcmu_d11ac_encchspec`) | If bw is 20 MHz or sb is NONE set sb = L (enum value 0). Bits 0-7 = chnum. Bits 8-10 = the raw `enum brcmu_chan_sb` value (LLL=0 .. UUU=7). Bandwidth from the map 20->0x1000, 40->0x1800, 80->0x2000, 160->0x2800 (other: `WARN_ON`, 0). Clear bits 14-15, then OR 0x0000 (2G) if chnum <= 14 else 0xc000 (5G). The word is not zeroed first, but the four masks 0x00ff, 0x0700, 0x3800, 0xc000 together cover all 16 bits. `ch->band` is not read. | `linux/brcmutil/d11.c:60-94` `linux/include/brcmu_d11.h:99-115` |
| linux, callers | Every chanspec is built through `d11inf.encchspec`. `channel_to_chanspec`: channel from the centre frequency, bw 20. `chandef_to_chanspec`: chnum from `center_freq1`, bw from the chandef width 20/40/80/160, sideband from the primary-channel offset: 40 MHz offset>0 -> U else L; 80 MHz -30/-10/+10/else -> LL/LU/UL/UU; 160 MHz -70..+50/else -> LLL..UUU. Widths 80+80, 5 and 10 MHz hit `WARN_ON_ONCE`. | `linux/brcmfmac/cfg80211.c:327-400` `linux/brcmfmac/cfg80211.c:403-413` |
| linux, direct `encchspec` calls | All with bw 20: p2p listen channel, p2p social/default channel list, p2p temporary channel (`brcmf_p2p_get_current_chanspec` fallback), the `per_chan_info` query and the `chanspecs` query (chnum 0, sb NONE). | `linux/brcmfmac/p2p.c:976-981` `linux/brcmfmac/p2p.c:1109-1126` `linux/brcmfmac/p2p.c:2055-2059` `linux/brcmfmac/cfg80211.c:7322-7326` `linux/brcmfmac/cfg80211.c:7383-7388` |
| linux, connect | In `brcmf_cfg80211_connect` the local chanspec is `channel_to_chanspec(chan)` when a channel is given and 0 otherwise. It is written to the join parameters only when `cfg->channel` is non-zero. | `linux/brcmfmac/cfg80211.c:2477-2486` `linux/brcmfmac/cfg80211.c:2594-2598` |
| linux, scan | Sends an encoded chanspec per requested scan channel. No chanspec literals. | `linux/brcmfmac/cfg80211.c:1141-1145` |
| whd, join | `ap->channel` \| BAND_2G/5G/6G (chosen by `ap->band`) \| BW_20 \| CTL_SB_NONE. Skipped when `ap->channel` == 0 (chanspec stays 0). The channel is not masked to 8 bits. When `ap->bss_type` is ad-hoc the same value is also sent with the `chanspec` named variable (iovar) before the join. | `whd/src/whd_wifi_api.c:2274-2300` `whd/src/whd_wifi_api.c:2338-2340` |
| whd, AP-role `whd_wifi_set_channel` (`csa` named variable) | BW_20 \| CTL_SB_NONE \| channel \| band, with band = 2G if channel <= 14 else 5G (`whd_channel_to_wl_band`). The channel is not masked to 8 bits. | `whd/src/whd_wifi_api.c:402-406` `whd/src/whd_wifi_api.c:636-649` `whd/src/include/whd_wlioctl.h:33` |
| whd, scan channel list and `whd_wifi_init_ap` | The `CH20MHZ_CHSPEC` macro. `whd_wifi_init_ap` takes a uint16_t `chanspec` argument, sends `CH20MHZ_CHSPEC` of it with the `chanspec` named variable, and later tests `CHSPEC_IS2G` on the raw argument. | `whd/src/whd_wifi_api.c:3379` `whd/src/whd_ap.c:333-334` `whd/src/whd_ap.c:419-420` `whd/src/whd_ap.c:519` |
| whd, `whd_wifi_set_chanspec` (public API) | Sends the caller's value unchanged. "Only 20 MHz" holds for values whd builds itself, not for this API. | `whd/src/whd_wifi_api.c:556` `whd/src/whd_wifi_api.c:586-590` |
| c-driver | Exactly one place: `cyw43_ll_wifi_join`, only when a bssid is given and channel != `CYW43_CHANNEL_NONE` (0xffffffff). chspec = channel \| 0x1000 \| 0x0000 \| 0x0000 (20 MHz, no sideband, 2.4 GHz). channel is a uint32_t narrowed to uint16_t without masking. Writes `chanspec_num` = 1 as le32 at buffer offset 4+32+20+8 = 64 and the chanspec as le16 at offset 4+32+20+12 = 68, and sends the 70-byte buffer as the `join` named variable. | `c-driver/cyw43_ll.c:2207` `c-driver/cyw43_ll.c:2301-2325` `c-driver/cyw43_ll.h:205` |
| embassy | Does not encode. Its scan request always sends `channel_num` 0 and `channel_list` [0]. c-driver's scan does the same. | `embassy/control.rs:824-825` `embassy/control.rs:835` `embassy/structs.rs:467-468` `c-driver/cyw43_ll.c:2200-2202` |

Band from channel number: linux's encoders and whd's `whd_channel_to_wl_band` both test channel <= 14 (`CH_MAX_2G_CHANNEL`); channel 15 and above get the 5 GHz band bits. `linux/brcmutil/d11.c:54-57` `linux/brcmutil/d11.c:90-93` `linux/include/brcmu_wifi.h:28` `whd/src/whd_wifi_api.c:402-406` `whd/src/include/whd_wlioctl.h:33`

c-driver always ORs the 2.4 GHz value regardless of the channel number. `c-driver/cyw43_ll.c:2315-2319`

whd's `CH20MHZ_CHSPEC(x)` = (x & 0x00ff) \| BW_20 \| CTL_SB_NONE \| band, where band is re-derived from x's own band bits: the 2G value if (x & BAND_MASK) == BAND_2G, else the 5G value if it equals BAND_5G, else the 6G value. `whd/src/include/whd_chip_constants.h:75-91`

It is applied to each entry of the scan API's `optional_channel_list`, which the API comment describes as an "array of channel numbers". `whd/src/whd_wifi_api.c:3372-3381` `whd/inc/whd_wifi_api.h:276-277`

Results of the macro for sample inputs (computed, not observed running). `whd/src/include/whd_chip_constants.h:75-91`

| Input | Chip set | Result | Citations |
|---|---|---|---|
| bare channel number | whd other | band bits 0 = BAND_2G, so channel \| 0x1000 for any channel number | `whd/src/include/whd_chip_constants.h:75-91` `whd/src/whd_chip_constants.c:444-483` |
| bare channel number | whd legacy | matches neither 0x2000 nor 0x1000 and gets the 6G value 0, so channel \| 0x0b00 with no band bits | `whd/src/include/whd_chip_constants.h:75-91` `whd/src/whd_chip_constants.c:444-483` |
| 0x1001 (well-formed 20 MHz chanspec) | whd other | 0x1001 (unchanged) | `whd/src/include/whd_chip_constants.h:75-91` `whd/src/whd_chip_constants.c:444-483` |
| 0xd024 | whd other | 0x0024 \| 0x1000 \| 0xc000 = 0xd024 (unchanged) | `whd/src/include/whd_chip_constants.h:75-91` `whd/src/whd_chip_constants.c:444-483` |

whd passes chanspec literals, not channel numbers, through that macro in its own scan calls. All are in the D11AC-valued layout regardless of chip id. `whd/src/whd_wifi_api.c:3268-3273` `whd/src/whd_wifi_api.c:3372-3381`

| whd literal list | Contents | When used | Citations |
|---|---|---|---|
| `channel_list_2G_5G_6G` in `whd_wifi_scan` | 0x1001..0x100B (channels 1-11, 20 MHz, band bits 00), 0xD038, 0xd024..0xd0a5 (band bits 11, 20 MHz), 0x9005..0x90E5 (band bits 10, 20 MHz), terminating 0 | Substituted for the caller's list when an SSID is given and `whd_wifi_platform_supports_triband(ifp)` is true. whd decides that at run time from the reply to `WLC_GET_BANDLIST`, so its value for a 43439 is not stated in these sources. | `whd/src/whd_wifi_api.c:3268-3273` `whd/src/whd_wifi_api.c:3290-3302` `whd/src/whd_wifi_api.c:509-516` |
| TWT setup/teardown list | {0x1001, 0x1009, 0} | Inside `#ifdef PROTO_MSGBUF` only | `whd/src/whd_wifi_api.c:4585` `whd/src/whd_wifi_api.c:4699` |

Each entry goes out as `htod16(CH20MHZ_CHSPEC(entry))` and the list ends at a 0 entry. `whd/src/whd_wifi_api.c:3372-3381`

### Decoding rules per driver
| Driver | Rule | Citations |
|---|---|---|
| linux, D11N | chnum = word & 0x00ff; `control_ch_num` starts equal to it. Bandwidth code 0x0800 -> bw 20, sb NONE. 0x0c00 -> bw 40: if the sideband bits == 0x0100 then sb L and control_ch_num -= 2, otherwise sb U and control_ch_num += 2. Any other bandwidth code (including 0x0400, 10 MHz) -> WARN "Invalid chanspec". Band bits 0x1000 -> 5G, 0x2000 -> 2G, else WARN. | `linux/brcmutil/d11.c:96-135` `linux/include/brcmu_wifi.h:25` |
| linux, D11AC | chnum = word & 0x00ff; `control_ch_num` starts equal. bw code 0x1000 -> 20 MHz, sb NONE. 0x1800 -> 40 MHz: sideband 0x0000 -> L, 0x0100 -> U, else WARN. 0x2000 -> 80 MHz: sb field 0..3 = LL/LU/UL/UU, else WARN. 0x2800 -> 160 MHz: sb field 0..7. 0x3000 (80+80) and every other code (5, 10 MHz) -> WARN "Invalid chanspec". Band bits 0xc000 -> 5G, 0x0000 -> 2G, 0x4000 and 0x8000 -> WARN. Offsets in the table below. | `linux/brcmutil/d11.c:137-235` `linux/include/brcmu_wifi.h:21-25` |
| linux, bss_info readers | `brcmf_inform_single_bss` uses `bi->ctl_ch` when it is non-zero and decodes the chanspec (`decchspec` -> `control_ch_num`) only when `ctl_ch` is 0, writing the result back into `bi->ctl_ch`. The p2p path does the same. Other readers (`linux/brcmfmac/cfg80211.c:3527-3528`, `linux/brcmfmac/cfg80211.c:3640-3643`, `linux/brcmfmac/cfg80211.c:6630-6631`) always decode the chanspec. | `linux/brcmfmac/cfg80211.c:3412-3417` |
| whd, `whd_chip_get_chanspec_ctl_channel_num` | `*ctrl_ch_num` is first set to chanspec & 0x00ff. For chip ids 43362, 4334, 43340, 43342 it returns that unchanged (no +/-2 for 40 MHz). Otherwise bw 20 -> unchanged; bw 40/80/160 -> offsets in the table below; any other bandwidth or sideband code -> `WHD_BADARG` with `*ctrl_ch_num` left at the low 8 bits. It does not decode the band. Its only caller in these sources is the `CHSPEC_IS6G` branch of the scan-result handler, which ignores the return value. | `whd/src/whd_chip_constants.c:52-128` `whd/src/whd_wifi_api.c:2681-2687` |
| whd, scan-result handler | Reads `bss_info->chanspec` with `dtoh16(WHD_READ_16(..))`. Reported channel: if `CHSPEC_IS6G(chanspec)`, the control channel computed by `whd_chip_get_chanspec_ctl_channel_num`; else if `bss_info->n_cap` is non-zero, `bss_info->ctl_ch` (the chanspec's channel bits are ignored); else chanspec & 0x00ff. The band of the record comes from `CHSPEC_IS2G` tested first, then `CHSPEC_IS5G`, else 6 GHz. | `whd/src/whd_wifi_api.c:2679-2699` `whd/src/whd_wifi_api.c:3008-3009` `whd/src/include/whd_types_int.h:143` |
| c-driver | Only decode is in `cyw43_ll_wifi_parse_scan_result`: `ev->u.scan_result.channel &= 0xff`. The public `cyw43_ev_scan_result_t.channel` field (uint16_t at struct offset 84) overlays the chanspec field of the internal bss record (offset 72 in the record, which starts 12 bytes into the escan result), so the driver masks the chanspec in place. Bandwidth, sideband and band bits are discarded. `ctl_ch` is not consulted. | `c-driver/cyw43_ll.c:486-516` `c-driver/cyw43_ll.c:668-675` `c-driver/cyw43_ll.c:714` `c-driver/cyw43_ll.h:222-234` `c-driver/cyw43_ll.h:237-249` |
| embassy | Does not decode. `BssInfo.chanspec` is handed to the user as a raw public u16 with no accessor that splits it. | `embassy/structs.rs:527-528` |

whd's `CHSPEC_IS6G` on a 43439. This paragraph follows from the macro definitions and the per-chip constant functions; it was not run on whd or on a board: `CHSPEC_IS6G` is (chanspec & BAND_MASK) == BAND_6G. whd's BAND_6G value is 0x8000 only for chip ids 55500, 55560, 55900, 55530 and 0 for every other id. On a non-legacy chip outside that list, which includes 43430 and 43439, the band mask is 0xc000 and both BAND_2G and BAND_6G are 0x0000. `CHSPEC_IS6G` is then true for every chanspec whose bits 14-15 are 00, i.e. every 2.4 GHz chanspec, so the first branch (control channel computed from the bandwidth and sideband bits) is the one taken, and the `n_cap` / `ctl_ch` branch is reached only for 5 GHz chanspecs. A band-bits-00 chanspec is still reported as 2.4 GHz because `CHSPEC_IS2G` is tested first for the band. On the legacy list (mask 0xf000, 2G 0x2000, 5G 0x1000, 6G 0) `CHSPEC_IS6G` is false for 2G and 5G chanspecs. `whd/src/whd_wifi_api.c:2679-2699` `whd/src/include/whd_chip_constants.h:76-85` `whd/src/whd_chip_constants.c:430-483`

Control channel = centre channel + offset (channel-number units). linux names the steps `CH_10MHZ_APART` 2, `CH_30MHZ_APART` 6, `CH_50MHZ_APART` 10, `CH_70MHZ_APART` 14. `linux/include/brcmu_wifi.h:21-25`

| Bandwidth | Sideband | Offset, linux D11AC | Offset, whd (non-legacy chips) | Citations |
|---|---|---|---|---|
| 20 MHz | any | 0 | 0 | `linux/brcmutil/d11.c:137-235` `whd/src/whd_chip_constants.c:52-128` |
| 40 MHz | L | -2 | -2 | `linux/brcmutil/d11.c:137-235` `whd/src/whd_chip_constants.c:52-128` |
| 40 MHz | U | +2 | +2 | `linux/brcmutil/d11.c:137-235` `whd/src/whd_chip_constants.c:52-128` |
| 80 MHz | LL / LU / UL / UU | -6 / -2 / +2 / +6 | -6 / -2 / +2 / +6 | `linux/brcmutil/d11.c:137-235` `whd/src/whd_chip_constants.c:52-128` |
| 160 MHz | LLL / LLU / LUL / LUU / ULL / ULU / UUL / UUU | -14 / -10 / -6 / -2 / +2 / +6 / +10 / +14 | -14 / -10 / -6 / -2 / +2 / +6 / +10 / +14 | `linux/brcmutil/d11.c:137-235` `whd/src/whd_chip_constants.c:52-128` |
| 40 MHz, linux D11N | sideband bits 0x0100 / anything else | -2 / +2 | whd legacy chips: no adjustment | `linux/brcmutil/d11.c:96-135` `whd/src/whd_chip_constants.c:58-63` |

### Byte order and field width
| Driver | Sending a 16-bit chanspec field | Receiving a 16-bit chanspec field | Citations |
|---|---|---|---|
| linux | `cpu_to_le16` where the chanspec sits in a 16-bit struct field: escan `channel_list`, join/assoc `chanspec_list` (IBSS join, extended join, legacy join params), p2p discover-state `chspec`, p2p escan `channel_list`, p2p interface add/change requests, and the first 2 bytes of the `chanspecs` query buffer. The record fields are declared `__le16`. | `le16_to_cpu` on `struct brcmf_bss_info_le.chanspec` (`__le16`) before decoding. | `linux/brcmfmac/cfg80211.c:1141-1145` `linux/brcmfmac/cfg80211.c:1899-1903` `linux/brcmfmac/cfg80211.c:2595-2598` `linux/brcmfmac/cfg80211.c:2642-2643` `linux/brcmfmac/p2p.c:572` `linux/brcmfmac/p2p.c:773` `linux/brcmfmac/p2p.c:2099` `linux/brcmfmac/p2p.c:2138` `linux/brcmfmac/cfg80211.c:7387-7388` `linux/brcmfmac/fwil_types.h:265` `linux/brcmfmac/fwil_types.h:489` `linux/brcmfmac/fwil_types.h:405` `linux/brcmfmac/fwil_types.h:449` `linux/brcmfmac/fwil_types.h:217-221` `linux/brcmfmac/p2p.c:107` `linux/brcmfmac/fwil_types.h:328` `linux/brcmfmac/cfg80211.c:3413-3414` `linux/brcmfmac/cfg80211.c:3527-3528` `linux/brcmfmac/cfg80211.c:3640-3643` `linux/brcmfmac/cfg80211.c:6630-6631` `linux/brcmfmac/p2p.c:1282-1283` `linux/brcmfmac/p2p.c:2048` |
| whd | `htod16` (csa `chspec`, join and legacy-join `chanspec_list[0]`, scan `channel_list` entries). | `dtoh16` (scan-result bss_info chanspec; `CSA_COMPLETE_IND` chspec, where it then prints chspec & 0xff as the channel). | `whd/src/whd_wifi_api.c:645` `whd/src/whd_wifi_api.c:2365` `whd/src/whd_wifi_api.c:2384` `whd/src/whd_wifi_api.c:3379` `whd/src/whd_wifi_api.c:2680` `whd/src/whd_wifi_api.c:1460` |
| c-driver | Writes the join chanspec byte by byte, low byte first (`cyw43_put_le16`); host-endian independent. | No conversion: the scan-result chanspec is accessed in place as a native uint16_t, although the same function chain byte-swaps the event header fields (flags, event_type, status, reason) from big-endian. The c-driver source does not state the byte order of this field. (inferred, not run: a native read gives the same value as linux's and whd's little-endian read only when the host is little-endian) | `c-driver/cyw43_ll.c:77-80` `c-driver/cyw43_ll.c:2320` `c-driver/cyw43_ll.c:714` `c-driver/cyw43_ll.h:229` `c-driver/cyw43_ll.c:737-741` |
| embassy | No conversion. `ScanParams` and `BssInfo` are converted to and from bytes by `core::mem::transmute` (`impl_bytes!`), so u16 fields are in host byte order. The only chanspec-typed value it sends is the constant 0 in `ScanParams.channel_list`. | No conversion; the field is exposed through a transmuted `#[repr(C, packed(2))]` struct. | `embassy/structs.rs:13` `embassy/structs.rs:26` `embassy/structs.rs:40` `embassy/structs.rs:467-470` `embassy/structs.rs:528` `embassy/control.rs:824-825` |

Further byte-order and width facts:

- `linux/brcmfmac/fwil_types.h:265` in the linux row is the TDLS named-variable record's `__le16` chanspec, which no cited code writes. `linux/brcmfmac/fwil_types.h:265`
- whd's `htod16` / `dtoh16` are the identity unless `IL_BIGENDIAN` is defined, in which case they are `SWAP16`. On a little-endian host whd performs no swap. `whd/src/include/whd_endian.h:44-57`
- whd uses a chanspec with no `dtoh16` in two places, inside `#ifdef PROTO_MSGBUF`: the TWT setup and teardown paths compare `bss_info.chanspec` with `optional_channel_list[0]` (a local list {0x1001, 0x1009, 0}). The bss_info comes from `whd_wifi_get_ap_info`, which copies the `WLC_GET_BSS_INFO` reply with `whd_mem_memcpy` and converts no field. `whd/src/whd_wifi_api.c:4585` `whd/src/whd_wifi_api.c:4630-4639` `whd/src/whd_wifi_api.c:4738-4739` `whd/src/whd_wifi_api.c:3730-3733`
- The `chanspec` named variable is carried as a 32-bit little-endian integer, not a 16-bit one. linux sets it with `brcmf_fil_iovar_int_set` (`cpu_to_le32` of the u16 widened to u32) and reads it with `brcmf_fil_iovar_int_get` (`le32_to_cpu` into a u32, then assigned to the u16 chspec). `linux/brcmfmac/fwil.h:122-137` `linux/brcmfmac/cfg80211.c:5393` `linux/brcmfmac/cfg80211.c:5459` `linux/brcmfmac/cfg80211.c:5864-5871` `linux/brcmfmac/cfg80211.c:8348-8350`
- whd's `whd_wifi_set_chanspec` writes `htod32((uint32_t)chanspec)` into a 4-byte named variable buffer; the ad-hoc join path goes through the same function. `whd/src/whd_wifi_api.c:586-590` `whd/src/include/whd_wlioctl.h:1165` `whd/src/whd_wifi_api.c:2338-2340`
- linux parses the reply to the `chanspecs` named variable as `struct brcmf_chanspec_list`: a le32 count followed by le32 elements. Each element is converted with `le32_to_cpu` and truncated to u16 before `decchspec`. The count is rejected if it exceeds `BRCMF_MAX_CHANSPEC_LIST`. `linux/brcmfmac/fwil_types.h:708-711` `linux/brcmfmac/cfg80211.c:7248-7258` `linux/brcmfmac/cfg80211.c:7399-7410` `linux/brcmfmac/cfg80211.c:105`
- For `per_chan_info` linux passes an encoded chanspec as a u32 through `brcmf_fil_bsscfg_int_query`. `linux/brcmfmac/cfg80211.c:7322-7326`
- linux treats the chanspec inside `struct brcmf_rx_mgmt_data` (the data of `WLC_E_PROBRESP_MSG`, `WLC_E_P2P_PROBREQ_MSG`, `WLC_E_ACTION_FRAME_RX`) as big-endian. The field is declared `__be16` (after a `__be16` version, before `__be32` rssi, mactime, rate) and is read with `be16_to_cpu` before `decchspec`, at three call sites. This struct is the only place in these sources where a chanspec is byte-swapped on a little-endian host. `linux/brcmfmac/fwil_types.h:713-724` `linux/brcmfmac/p2p.c:1439-1440` `linux/brcmfmac/p2p.c:1979-1980` `linux/brcmfmac/cyw/core.c:306-307`
- whd declares `wl_rx_mgmt_data_t` with the same field sizes but calls the second field `uint16_t channel`, with no byte-order annotation. Its only user, the `WLC_E_EXT_AUTH_FRAME_RX` handler, skips the header (`rxframe + 1`) and never reads the field, so whd neither swaps nor decodes it. Not found in embassy or c-driver. `whd/src/include/whd_wlioctl.h:76-83` `whd/src/whd_wifi_api.c:3077-3088`

### Where a bare channel number is used instead
| Driver | Operation | What is sent | Citations |
|---|---|---|---|
| embassy | set AP channel | command 30 (`SetChannel`) with the channel as a 32-bit value | `embassy/control.rs:585-586` `embassy/consts.rs:471` |
| c-driver | set AP channel | command 30 (`WLC_SET_CHANNEL`) with the channel as a 32-bit value | `c-driver/cyw43_ll.c:173` `c-driver/cyw43_ll.c:2388-2389` |
| whd | `whd_wifi_set_channel`, STA role | `WLC_SET_CHANNEL` with `htod32(channel)` | `whd/src/whd_wifi_api.c:629-633` |
| whd | `whd_wifi_set_channel`, AP role | a chanspec in the `csa` named variable (not the `chanspec` named variable) | `whd/src/whd_wifi_api.c:637-649` |
| whd | soft-AP start (`whd_wifi_init_ap`) | `whd_wifi_set_chanspec(CH20MHZ_CHSPEC(chanspec))`, i.e. the `chanspec` named variable | `whd/src/whd_ap.c:419-420` |
| linux | AP start | `brcmf_fil_iovar_int_set(ifp, "chanspec", chanspec)` | `linux/brcmfmac/cfg80211.c:5393` |

Command number 292 is named as a chanspec query in two drivers and sent by none. whd defines `WLC_GET_CHANSPEC` = 292 (and `OID_STA_CHANSPEC` from it) and uses it only in a command-name string table. embassy's `Ioctl` enum has `GetChanspec` = 292 with no use outside consts.rs. Not found in linux/brcmfmac/fwil.h or in c-driver. `whd/src/include/whd_wlioctl.h:1568` `whd/src/include/whd_wlioctl.h:1597` `whd/src/whd_utils.c:785` `embassy/consts.rs:713`

The drivers that read the current chanspec at all use the `chanspec` named variable (linux) or `WLC_GET_CHANNEL` / `WLC_GET_BSS_INFO` (whd). `linux/brcmfmac/cfg80211.c:5864` `whd/src/whd_wifi_api.c:679-683` `whd/src/whd_wifi_api.c:3730-3733`

### Worked examples

All values are (computed) from the cited encode code, not captured from a device. 20 MHz, 2.4 GHz. `linux/brcmutil/d11.c:41-58` `linux/brcmutil/d11.c:77-94` `c-driver/cyw43_ll.c:2312-2320`

"D11AC-valued" is what linux produces with io type 2, whd on a non-legacy chip id such as 43439/43430, and c-driver's join. embassy's constants would give the same value but embassy never builds one; its AP channel goes out as the bare number in a 32-bit `SetChannel` payload. "D11N-valued" is what linux produces with io type 1 and whd on its legacy chip list. For linux the value therefore depends on the run-time io type. `linux/brcmutil/d11.c:237-246` `embassy/control.rs:586`

| Channel | D11AC-valued chanspec | As a little-endian 16-bit field | D11N-valued chanspec | As a little-endian 16-bit field | Citations |
|---|---|---|---|---|---|
| 1 | 4097 (0x1001) | 01 10 | 11009 (0x2b01) | 01 2b | `linux/brcmutil/d11.c:41-58` `linux/brcmutil/d11.c:77-94` `whd/src/whd_wifi_api.c:2278-2283` `whd/src/whd_chip_constants.c:444-455` `whd/src/whd_chip_constants.c:514-525` `whd/src/whd_chip_constants.c:598-610` `c-driver/cyw43_ll.c:2312-2320` `embassy/lib.rs:281-292` |
| 6 | 4102 (0x1006) | 06 10 | 11014 (0x2b06) | 06 2b | `linux/brcmutil/d11.c:41-58` `linux/brcmutil/d11.c:77-94` `whd/src/whd_wifi_api.c:2278-2283` `whd/src/whd_chip_constants.c:444-455` `whd/src/whd_chip_constants.c:514-525` `whd/src/whd_chip_constants.c:598-610` `c-driver/cyw43_ll.c:2312-2320` `embassy/lib.rs:281-292` |
| 11 | 4107 (0x100b) | 0b 10 | 11019 (0x2b0b) | 0b 2b | `linux/brcmutil/d11.c:41-58` `linux/brcmutil/d11.c:77-94` `whd/src/whd_wifi_api.c:2278-2283` `whd/src/whd_chip_constants.c:444-455` `whd/src/whd_chip_constants.c:514-525` `whd/src/whd_chip_constants.c:598-610` `c-driver/cyw43_ll.c:2312-2320` `embassy/lib.rs:281-292` |
| 14 | 4110 (0x100e) | 0e 10 | 11022 (0x2b0e) | 0e 2b | `linux/brcmutil/d11.c:41-58` `linux/brcmutil/d11.c:77-94` `whd/src/whd_wifi_api.c:2278-2283` `whd/src/whd_chip_constants.c:444-455` `whd/src/whd_chip_constants.c:514-525` `whd/src/whd_chip_constants.c:598-610` `c-driver/cyw43_ll.c:2312-2320` `embassy/lib.rs:281-292` |

Channel 14 is the last number linux and whd treat as 2.4 GHz; c-driver applies the 2.4 GHz value to every channel number. `linux/brcmutil/d11.c:54-57` `linux/brcmutil/d11.c:90-93` `whd/src/whd_wifi_api.c:402-406` `c-driver/cyw43_ll.c:2319`

## Command status codes

The code is the `status` field of the CDC/BCDC header of a command reply, 32 bits, little-endian as read by linux and whd. `linux/brcmfmac/bcdc.c:209` `linux/brcmfmac/bcdc.c:210` `whd/src/whd_cdc_bdc.c:277`

What follows is what each driver's table says. The mapping to actual firmware behaviour is not established by these sources.

### When each driver reads the status
| Driver | Rule | Citations |
|---|---|---|
| linux | reads the status only when the reply's error flag (0x01) is set | `linux/brcmfmac/bcdc.c:209` `linux/brcmfmac/bcdc.c:210` |
| whd | reads the status only when the reply's error flag (0x01) is set | `whd/src/whd_cdc_bdc.c:295` `whd/src/whd_cdc_bdc.c:302` |
| embassy | tests status != 0 without looking at the flag | `embassy/runner.rs:1174` |
| c-driver | never reads the status of a reply (the only code touching it is commented out) | `c-driver/cyw43_ll.c:1006` `c-driver/cyw43_ll.c:1007` |

### Sign of the status

linux and whd treat a failing status as a negative number whose magnitude indexes a name table. linux indexes `brcmf_fil_errstr[]` with -fwerr. whd returns `WHD_RESULT_CREATE(2000 - status)`, which for a status of -n lands on the `WHD_WLAN_*` code defined as 2000+n. `linux/brcmfmac/fwil.c:118` `linux/brcmfmac/fwil.c:119` `linux/brcmfmac/fwil.c:120` `whd/inc/whd_types.h:1066` `whd/src/whd_cdc_bdc.c:303`

| Driver | Evidence | Citations |
|---|---|---|
| linux | linux treats fwerr < 0 as a firmware error and looks the name up with (u32)(-fwerr) | `linux/brcmfmac/fwil.c:118` `linux/brcmfmac/fwil.c:119` `linux/brcmfmac/fwil.c:120` |
| linux | linux compares the returned firmware error against -BRCMF_FW_UNSUPPORTED where BRCMF_FW_UNSUPPORTED is 23 | `linux/brcmfmac/feature.c:20` `linux/brcmfmac/feature.c:197` `linux/brcmfmac/feature.c:218` |
| whd | whd computes WHD_RESULT_CREATE(WLAN_ENUM_OFFSET - status) with WLAN_ENUM_OFFSET 2000 and status a uint32_t read with dtoh32 from the cdc header; the subtraction only yields 2001..2046 if status is the two's-complement of 1..46 (inferred from the arithmetic, not stated in whd) | `whd/inc/whd_types.h:1066` `whd/src/whd_cdc_bdc.c:167` `whd/src/whd_cdc_bdc.c:277` `whd/src/whd_cdc_bdc.c:303` |
| c-driver | a c-driver comment quotes a status of 0xffffffe2 (which is -30 as a signed 32-bit value) and a commented-out print shows '2000 - ioctl_header->status' | `c-driver/cyw43_ll.c:2359` `c-driver/cyw43_ll.c:1008` |
| embassy | embassy logs the u32 status cast to i32 | `embassy/structs.rs:138` `embassy/runner.rs:1176` |

### Extent of each driver's table
| Driver | Table | Citations |
|---|---|---|
| linux | 53 names, magnitudes 0..52 (BCME_OK .. BCME_IE_NOTFOUND); table compiled only under #ifdef DEBUG; magnitudes >= 53 print "(unknown)"; without DEBUG the name is the empty string | `linux/brcmfmac/fwil.c:25` `linux/brcmfmac/fwil.c:26` `linux/brcmfmac/fwil.c:80` `linux/brcmfmac/fwil.c:82` `linux/brcmfmac/fwil.c:84` `linux/brcmfmac/fwil.c:85` `linux/brcmfmac/fwil.c:87` `linux/brcmfmac/fwil.c:90` `linux/brcmfmac/fwil.c:92` |
| whd | 46 defines, WHD_RESULT_CREATE(2001)..(2046) (WHD_WLAN_ERROR .. WHD_WLAN_NOBAND); the same WHD_WLAN_* values are also returned directly by whd host code (examples cited), so a WHD_WLAN_* define is not by itself evidence that a firmware status of that magnitude exists. Host-side returns are found for names where linux and whd agree (WHD_WLAN_BADARG, WHD_WLAN_NOMEM, WHD_WLAN_BADSSIDLEN) as well as for two of the five where they disagree (WHD_WLAN_NOFUNCTION, WHD_WLAN_INVALID), so host use does not tell the two groups apart. WHD_WLAN_UNFINISHED, WHD_WLAN_DISABLED and WHD_WLAN_NOBAND are not used anywhere in whd/src or whd/inc besides their defines. | `whd/inc/whd_types.h:1066` `whd/inc/whd_types.h:1068` `whd/inc/whd_types.h:1113` `whd/inc/whd_types.h:984` `whd/inc/whd_types.h:985` `whd/src/whd_network_if.c:84` `whd/src/whd_chip.c:519` `whd/src/whd_management.c:103` `whd/src/whd_proto.c:84` `whd/src/whd_ap.c:370` `whd/inc/whd_types.h:1108` `whd/inc/whd_types.h:1110` |
| c-driver | error-code table: not found in these sources; the code that would read the status is commented out | `c-driver/cyw43_ll.c:1006` `c-driver/cyw43_ll.c:1007` `c-driver/cyw43_ll.c:1008` |
| embassy | error-code table: not found in these sources; the status is only logged as a number | `embassy/runner.rs:1174` `embassy/runner.rs:1176` |
| all four | numeric `BCME_*` defines: Not found in linux, whd, c-driver or embassy. The only BCME_ macro in linux is BCME_STRLEN 64 (a string length, not a code). | `linux/include/brcmu_utils.h:28` |

Neither linux nor whd defines numeric `BCME_*` macros in these sources. linux has only the string table (position = magnitude) plus one numeric define, `BRCMF_FW_UNSUPPORTED` 23. whd has the `WHD_WLAN_*` defines 2001..2046. `linux/brcmfmac/fwil.c:26` `linux/brcmfmac/feature.c:20` `whd/inc/whd_types.h:1068` `whd/inc/whd_types.h:1113`

### Code table

"Status" is the signed value as linux and whd interpret it. "whd result number" is the x in `WHD_RESULT_CREATE(x)`. The linux names are positions in a string table; linux has no comment for any of them. The "whd comment" column is whd's comment on its define. Not found in c-driver or embassy: neither has an error-code table. Rows marked (unverified) are the ones where the two tables carry different names and nothing in these sources resolves it. `linux/brcmfmac/fwil.c:26` `whd/inc/whd_types.h:1068`

linux and whd give the same base name for magnitudes 1..40 and 42. At 36 and 37 the names are not identical; that they describe the same condition is a reading of the names, not stated in either source. At 41 and 43..46 the two tables carry different names. 47..52 exist only in linux. The name DISABLED appears in both tables at different magnitudes: linux `BCME_DISABLED` at 47, whd `WHD_WLAN_DISABLED` at 43. `linux/brcmfmac/fwil.c:74` `whd/inc/whd_types.h:1110`

| Status | Magnitude | linux | whd | whd result number | whd comment | Notes | Citations |
|---|---|---|---|---|---|---|---|
| 0 | 0 | `BCME_OK` | — | — |  | no WHD_WLAN_* define; see whd handling: WHD_SUCCESS when the error flag is clear, WHD_IOCTL_FAIL when the error flag is set and status is 0. linux: fwerr is initialised to 0 and only overwritten when the BCDC error flag is set | `linux/brcmfmac/fwil.c:27` `whd/src/whd_cdc_bdc.c:295` `whd/src/whd_cdc_bdc.c:302` `whd/src/whd_cdc_bdc.c:305` `whd/src/whd_cdc_bdc.c:308` `whd/inc/whd_types.h:998` `whd/inc/whd_types.h:987` `linux/brcmfmac/bcdc.c:169` `linux/brcmfmac/bcdc.c:209` `linux/brcmfmac/bcdc.c:210` |
| -1 | 1 | `BCME_ERROR` | `WHD_WLAN_ERROR` | 2001 | Generic Error |  | `linux/brcmfmac/fwil.c:28` `whd/inc/whd_types.h:1068` |
| -2 | 2 | `BCME_BADARG` | `WHD_WLAN_BADARG` | 2002 | Bad Argument |  | `linux/brcmfmac/fwil.c:29` `whd/inc/whd_types.h:1069` |
| -3 | 3 | `BCME_BADOPTION` | `WHD_WLAN_BADOPTION` | 2003 | Bad option |  | `linux/brcmfmac/fwil.c:30` `whd/inc/whd_types.h:1070` |
| -4 | 4 | `BCME_NOTUP` | `WHD_WLAN_NOTUP` | 2004 | Not up |  | `linux/brcmfmac/fwil.c:31` `whd/inc/whd_types.h:1071` |
| -5 | 5 | `BCME_NOTDOWN` | `WHD_WLAN_NOTDOWN` | 2005 | Not down |  | `linux/brcmfmac/fwil.c:32` `whd/inc/whd_types.h:1072` |
| -6 | 6 | `BCME_NOTAP` | `WHD_WLAN_NOTAP` | 2006 | Not AP |  | `linux/brcmfmac/fwil.c:33` `whd/inc/whd_types.h:1073` |
| -7 | 7 | `BCME_NOTSTA` | `WHD_WLAN_NOTSTA` | 2007 | Not STA |  | `linux/brcmfmac/fwil.c:34` `whd/inc/whd_types.h:1074` |
| -8 | 8 | `BCME_BADKEYIDX` | `WHD_WLAN_BADKEYIDX` | 2008 | BAD Key Index |  | `linux/brcmfmac/fwil.c:35` `whd/inc/whd_types.h:1075` |
| -9 | 9 | `BCME_RADIOOFF` | `WHD_WLAN_RADIOOFF` | 2009 | Radio Off |  | `linux/brcmfmac/fwil.c:36` `whd/inc/whd_types.h:1076` |
| -10 | 10 | `BCME_NOTBANDLOCKED` | `WHD_WLAN_NOTBANDLOCKED` | 2010 | Not band locked |  | `linux/brcmfmac/fwil.c:37` `whd/inc/whd_types.h:1077` |
| -11 | 11 | `BCME_NOCLK` | `WHD_WLAN_NOCLK` | 2011 | No Clock |  | `linux/brcmfmac/fwil.c:38` `whd/inc/whd_types.h:1078` |
| -12 | 12 | `BCME_BADRATESET` | `WHD_WLAN_BADRATESET` | 2012 | BAD Rate valueset |  | `linux/brcmfmac/fwil.c:39` `whd/inc/whd_types.h:1079` |
| -13 | 13 | `BCME_BADBAND` | `WHD_WLAN_BADBAND` | 2013 | BAD Band |  | `linux/brcmfmac/fwil.c:40` `whd/inc/whd_types.h:1080` |
| -14 | 14 | `BCME_BUFTOOSHORT` | `WHD_WLAN_BUFTOOSHORT` | 2014 | Buffer too short |  | `linux/brcmfmac/fwil.c:41` `whd/inc/whd_types.h:1081` |
| -15 | 15 | `BCME_BUFTOOLONG` | `WHD_WLAN_BUFTOOLONG` | 2015 | Buffer too long |  | `linux/brcmfmac/fwil.c:42` `whd/inc/whd_types.h:1082` |
| -16 | 16 | `BCME_BUSY` | `WHD_WLAN_BUSY` | 2016 | Busy |  | `linux/brcmfmac/fwil.c:43` `whd/inc/whd_types.h:1083` |
| -17 | 17 | `BCME_NOTASSOCIATED` | `WHD_WLAN_NOTASSOCIATED` | 2017 | Not Associated | c-driver comment labels status 0xffffffe2 (-30) as NOTASSOCIATED; in linux and whd NOTASSOCIATED is magnitude 17 and 30 is NOTFOUND. See magnitude 30. | `linux/brcmfmac/fwil.c:44` `whd/inc/whd_types.h:1084` `c-driver/cyw43_ll.c:2359` |
| -18 | 18 | `BCME_BADSSIDLEN` | `WHD_WLAN_BADSSIDLEN` | 2018 | Bad SSID len |  | `linux/brcmfmac/fwil.c:45` `whd/inc/whd_types.h:1085` |
| -19 | 19 | `BCME_OUTOFRANGECHAN` | `WHD_WLAN_OUTOFRANGECHAN` | 2019 | Out of Range Channel |  | `linux/brcmfmac/fwil.c:46` `whd/inc/whd_types.h:1086` |
| -20 | 20 | `BCME_BADCHAN` | `WHD_WLAN_BADCHAN` | 2020 | Bad Channel |  | `linux/brcmfmac/fwil.c:47` `whd/inc/whd_types.h:1087` |
| -21 | 21 | `BCME_BADADDR` | `WHD_WLAN_BADADDR` | 2021 | Bad Address |  | `linux/brcmfmac/fwil.c:48` `whd/inc/whd_types.h:1088` |
| -22 | 22 | `BCME_NORESOURCE` | `WHD_WLAN_NORESOURCE` | 2022 | Not Enough Resources |  | `linux/brcmfmac/fwil.c:49` `whd/inc/whd_types.h:1089` |
| -23 | 23 | `BCME_UNSUPPORTED` | `WHD_WLAN_UNSUPPORTED` | 2023 | Unsupported | linux also has the numeric define BRCMF_FW_UNSUPPORTED 23 and tests err != -BRCMF_FW_UNSUPPORTED in feature probing. whd tolerates WHD_WLAN_UNSUPPORTED after some named variable sets (apsta, tx glomming, join fallback, CHECK_RETURN_UNSUPPORTED_CONTINUE) | `linux/brcmfmac/fwil.c:50` `whd/inc/whd_types.h:1090` `linux/brcmfmac/feature.c:20` `linux/brcmfmac/feature.c:197` `linux/brcmfmac/feature.c:218` `whd/src/whd_ap.c:229` `whd/src/whd_management.c:473` `whd/src/whd_management.c:491` `whd/src/whd_wifi_api.c:2370` `whd/src/include/whd_types_int.h:103` |
| -24 | 24 | `BCME_BADLEN` | `WHD_WLAN_BADLEN` | 2024 | Bad length |  | `linux/brcmfmac/fwil.c:51` `whd/inc/whd_types.h:1091` |
| -25 | 25 | `BCME_NOTREADY` | `WHD_WLAN_NOTREADY` | 2025 | Not Ready |  | `linux/brcmfmac/fwil.c:52` `whd/inc/whd_types.h:1092` |
| -26 | 26 | `BCME_EPERM` | `WHD_WLAN_EPERM` | 2026 | Not Permitted |  | `linux/brcmfmac/fwil.c:53` `whd/inc/whd_types.h:1093` |
| -27 | 27 | `BCME_NOMEM` | `WHD_WLAN_NOMEM` | 2027 | No Memory |  | `linux/brcmfmac/fwil.c:54` `whd/inc/whd_types.h:1094` |
| -28 | 28 | `BCME_ASSOCIATED` | `WHD_WLAN_ASSOCIATED` | 2028 | Associated |  | `linux/brcmfmac/fwil.c:55` `whd/inc/whd_types.h:1095` |
| -29 | 29 | `BCME_RANGE` | `WHD_WLAN_RANGE` | 2029 | Not In Range |  | `linux/brcmfmac/fwil.c:56` `whd/inc/whd_types.h:1096` |
| -30 | 30 | `BCME_NOTFOUND` | `WHD_WLAN_NOTFOUND` | 2030 | Not Found | whd treats WHD_WLAN_NOTFOUND from a 'bss' named variable get as 'AP interface does not exist'. c-driver comment on the 'bss' named variable get says it 'can fail with sdpcm status = 0xffffffe2 (NOTASSOCIATED)'. 0xffffffe2 is -30, which linux and whd both name NOTFOUND; NOTASSOCIATED is magnitude 17 in both tables. The c-driver comment's number and label do not match each other under either table. | `linux/brcmfmac/fwil.c:57` `whd/inc/whd_types.h:1097` `whd/src/whd_ap.c:627` `whd/src/whd_ap.c:628` `c-driver/cyw43_ll.c:2359` |
| -31 | 31 | `BCME_WME_NOT_ENABLED` | `WHD_WLAN_WME_NOT_ENABLED` | 2031 | WME Not Enabled |  | `linux/brcmfmac/fwil.c:58` `whd/inc/whd_types.h:1098` |
| -32 | 32 | `BCME_TSPEC_NOTFOUND` | `WHD_WLAN_TSPEC_NOTFOUND` | 2032 | TSPEC Not Found |  | `linux/brcmfmac/fwil.c:59` `whd/inc/whd_types.h:1099` |
| -33 | 33 | `BCME_ACM_NOTSUPPORTED` | `WHD_WLAN_ACM_NOTSUPPORTED` | 2033 | ACM Not Supported |  | `linux/brcmfmac/fwil.c:60` `whd/inc/whd_types.h:1100` |
| -34 | 34 | `BCME_NOT_WME_ASSOCIATION` | `WHD_WLAN_NOT_WME_ASSOCIATION` | 2034 | Not WME Association |  | `linux/brcmfmac/fwil.c:61` `whd/inc/whd_types.h:1101` |
| -35 | 35 | `BCME_SDIO_ERROR` | `WHD_WLAN_SDIO_ERROR` | 2035 | SDIO Bus Error |  | `linux/brcmfmac/fwil.c:62` `whd/inc/whd_types.h:1102` |
| -36 | 36 | `BCME_DONGLE_DOWN` | `WHD_WLAN_WLAN_DOWN` | 2036 | WLAN Not Accessible | names are not identical; same table position (linux BCME_DONGLE_DOWN, whd WHD_WLAN_WLAN_DOWN) | `linux/brcmfmac/fwil.c:63` `whd/inc/whd_types.h:1103` |
| -37 | 37 | `BCME_VERSION` | `WHD_WLAN_BAD_VERSION` | 2037 | Incorrect version | names are not identical; same table position (linux BCME_VERSION, whd WHD_WLAN_BAD_VERSION) | `linux/brcmfmac/fwil.c:64` `whd/inc/whd_types.h:1104` |
| -38 | 38 | `BCME_TXFAIL` | `WHD_WLAN_TXFAIL` | 2038 | TX failure |  | `linux/brcmfmac/fwil.c:65` `whd/inc/whd_types.h:1105` |
| -39 | 39 | `BCME_RXFAIL` | `WHD_WLAN_RXFAIL` | 2039 | RX failure |  | `linux/brcmfmac/fwil.c:66` `whd/inc/whd_types.h:1106` |
| -40 | 40 | `BCME_NODEVICE` | `WHD_WLAN_NODEVICE` | 2040 | Device not present |  | `linux/brcmfmac/fwil.c:67` `whd/inc/whd_types.h:1107` |
| -41 (unverified) | 41 | `BCME_NMODE_DISABLED` | `WHD_WLAN_UNFINISHED` | 2041 | To be finished | Names differ: linux BCME_NMODE_DISABLED vs whd WHD_WLAN_UNFINISHED at the same magnitude; not resolved by these sources. WHD_WLAN_UNFINISHED is not used anywhere in whd/src or whd/inc besides its define; nothing in these sources says whether it is a firmware status or a host-only result | `linux/brcmfmac/fwil.c:68` `whd/inc/whd_types.h:1108` |
| -42 | 42 | `BCME_NONRESIDENT` | `WHD_WLAN_NONRESIDENT` | 2042 | access to nonresident overlay |  | `linux/brcmfmac/fwil.c:69` `whd/inc/whd_types.h:1109` |
| -43 (unverified) | 43 | `BCME_SCANREJECT` | `WHD_WLAN_DISABLED` | 2043 | Disabled in this build | Names differ: linux BCME_SCANREJECT vs whd WHD_WLAN_DISABLED at the same magnitude; not resolved by these sources. WHD_WLAN_DISABLED is not used anywhere in whd/src or whd/inc besides its define; nothing in these sources says whether it is a firmware status or a host-only result | `linux/brcmfmac/fwil.c:70` `whd/inc/whd_types.h:1110` |
| -44 (unverified) | 44 | `BCME_USAGE_ERROR` | `WHD_WLAN_NOFUNCTION` | 2044 | Function pointer not provided | Names differ: linux BCME_USAGE_ERROR vs whd WHD_WLAN_NOFUNCTION at the same magnitude; not resolved by these sources. WHD_WLAN_NOFUNCTION is returned by whd host code (e.g. `whd/src/whd_network_if.c:84`), so this whd name is in use as a host-side result; whether whd also expects it as a firmware status is not stated | `linux/brcmfmac/fwil.c:71` `whd/inc/whd_types.h:1111` `whd/src/whd_network_if.c:84` |
| -45 (unverified) | 45 | `BCME_IOCTL_ERROR` | `WHD_WLAN_INVALID` | 2045 | Not valid | Names differ: linux BCME_IOCTL_ERROR vs whd WHD_WLAN_INVALID at the same magnitude; not resolved by these sources. WHD_WLAN_INVALID is returned by whd host code (`whd/src/whd_chip.c:519`, `whd/src/whd_chip.c:526`), so this whd name is in use as a host-side result; whether whd also expects it as a firmware status is not stated | `linux/brcmfmac/fwil.c:72` `whd/inc/whd_types.h:1112` `whd/src/whd_chip.c:519` `whd/src/whd_chip.c:526` |
| -46 (unverified) | 46 | `BCME_SERIAL_PORT_ERR` | `WHD_WLAN_NOBAND` | 2046 | No Band | Names differ: linux BCME_SERIAL_PORT_ERR vs whd WHD_WLAN_NOBAND at the same magnitude; not resolved by these sources. WHD_WLAN_NOBAND is not used anywhere in whd/src or whd/inc besides its define; nothing in these sources says whether it is a firmware status or a host-only result | `linux/brcmfmac/fwil.c:73` `whd/inc/whd_types.h:1113` |
| -47 | 47 | `BCME_DISABLED` | — | — |  | linux only. For a status of -47 with the error flag set, whd's expression WLAN_ENUM_OFFSET - status gives code number 2047, for which whd has no define (inferred, not stated in whd). Not found in whd (WHD_WLAN_* defines stop at 2046) | `linux/brcmfmac/fwil.c:74` `whd/inc/whd_types.h:1113` `whd/src/whd_cdc_bdc.c:303` |
| -48 | 48 | `BCME_DECERR` | — | — |  | linux only. For a status of -48 with the error flag set, whd's expression WLAN_ENUM_OFFSET - status gives code number 2048, for which whd has no define (inferred, not stated in whd). Not found in whd (WHD_WLAN_* defines stop at 2046) | `linux/brcmfmac/fwil.c:75` `whd/inc/whd_types.h:1113` `whd/src/whd_cdc_bdc.c:303` |
| -49 | 49 | `BCME_ENCERR` | — | — |  | linux only. For a status of -49 with the error flag set, whd's expression WLAN_ENUM_OFFSET - status gives code number 2049, for which whd has no define (inferred, not stated in whd). Not found in whd (WHD_WLAN_* defines stop at 2046) | `linux/brcmfmac/fwil.c:76` `whd/inc/whd_types.h:1113` `whd/src/whd_cdc_bdc.c:303` |
| -50 | 50 | `BCME_MICERR` | — | — |  | linux only. For a status of -50 with the error flag set, whd's expression WLAN_ENUM_OFFSET - status gives code number 2050, for which whd has no define (inferred, not stated in whd). Not found in whd (WHD_WLAN_* defines stop at 2046) | `linux/brcmfmac/fwil.c:77` `whd/inc/whd_types.h:1113` `whd/src/whd_cdc_bdc.c:303` |
| -51 | 51 | `BCME_REPLAY` | — | — |  | linux only. For a status of -51 with the error flag set, whd's expression WLAN_ENUM_OFFSET - status gives code number 2051, for which whd has no define (inferred, not stated in whd). Not found in whd (WHD_WLAN_* defines stop at 2046) | `linux/brcmfmac/fwil.c:78` `whd/inc/whd_types.h:1113` `whd/src/whd_cdc_bdc.c:303` |
| -52 | 52 | `BCME_IE_NOTFOUND` | — | — |  | linux only. For a status of -52 with the error flag set, whd's expression WLAN_ENUM_OFFSET - status gives code number 2052, for which whd has no define (inferred, not stated in whd). Not found in whd (WHD_WLAN_* defines stop at 2046) | `linux/brcmfmac/fwil.c:79` `whd/inc/whd_types.h:1113` `whd/src/whd_cdc_bdc.c:303` |

### How linux handles the status
| Step | What the driver does | Citations |
|---|---|---|
| 1 | before any command is sent, brcmf_fil_cmd_data returns -EIO if the bus state is not BRCMF_BUS_UP; this return is taken before the fwil_fwerr test, so it is the one error that is not replaced by fwerr | `linux/brcmfmac/fwil.c:102` `linux/brcmfmac/fwil.c:104` |
| 2 | BCDC transport: fwerr is set to 0, then set to le32_to_cpu(msg->status) only if flags & BCDC_DCMD_ERROR (0x01); the transport function itself still returns 0. Same in query and set paths. | `linux/brcmfmac/bcdc.c:30` `linux/brcmfmac/bcdc.c:34` `linux/brcmfmac/bcdc.c:169` `linux/brcmfmac/bcdc.c:206` `linux/brcmfmac/bcdc.c:209` `linux/brcmfmac/bcdc.c:210` `linux/brcmfmac/bcdc.c:226` `linux/brcmfmac/bcdc.c:249` `linux/brcmfmac/bcdc.c:250` |
| 3 | msgbuf transport (PCIe, not the CYW43439 buses): fwerr is the completion header's 16-bit status cast to s16, with no separate error flag | `linux/brcmfmac/msgbuf.c:502` `linux/brcmfmac/msgbuf.c:526` `linux/brcmfmac/msgbuf.c:886` `linux/brcmfmac/msgbuf.c:887` |
| 4 | fwil: if the transport returned an error it is logged ('Failed: error=%d') and returned; else if fwerr < 0 linux logs 'Firmware error: <name> (<fwerr>)' at FIL debug level and sets err = -EBADE. A positive fwerr is not treated as an error by this test. | `linux/brcmfmac/fwil.c:116` `linux/brcmfmac/fwil.c:117` `linux/brcmfmac/fwil.c:118` `linux/brcmfmac/fwil.c:119` `linux/brcmfmac/fwil.c:120` `linux/brcmfmac/fwil.c:121` `linux/brcmfmac/fwil.c:126` |
| 5 | if ifp->fwil_fwerr is set, the raw fwerr is returned instead of -EBADE; the flag is documented as 'fwil layer should return firmware error codes' and in these sources is set only around the feature probes in feature.c | `linux/brcmfmac/fwil.c:123` `linux/brcmfmac/fwil.c:124` `linux/brcmfmac/core.h:186` `linux/brcmfmac/core.h:204` `linux/brcmfmac/feature.c:194` `linux/brcmfmac/feature.c:205` `linux/brcmfmac/feature.c:215` `linux/brcmfmac/feature.c:226` |
| 6 | consequence of the order of those two tests (inferred from the code, not stated): with ifp->fwil_fwerr set, the test at `linux/brcmfmac/fwil.c:123-124` returns fwerr even when the transport call itself failed. Both transports set *fwerr = 0 before sending, so a transport failure during a feature probe is returned as 0, and a positive status with the error flag set is returned as that positive number. Neither equals -23, so the probe enables the feature in both cases. | `linux/brcmfmac/fwil.c:116` `linux/brcmfmac/fwil.c:123` `linux/brcmfmac/fwil.c:124` `linux/brcmfmac/bcdc.c:169` `linux/brcmfmac/bcdc.c:171` `linux/brcmfmac/bcdc.c:174` `linux/brcmfmac/bcdc.c:226` `linux/brcmfmac/msgbuf.c:502` `linux/brcmfmac/feature.c:197` `linux/brcmfmac/feature.c:218` |
| 7 | feature probing enables a feature unless the named variable returned exactly -BRCMF_FW_UNSUPPORTED (-23); any other error, including other firmware errors, enables it | `linux/brcmfmac/feature.c:20` `linux/brcmfmac/feature.c:196` `linux/brcmfmac/feature.c:197` `linux/brcmfmac/feature.c:199` `linux/brcmfmac/feature.c:217` `linux/brcmfmac/feature.c:218` |
| 8 | callers that test err == -EBADE (i.e. any firmware error, the specific code is lost) and print '<x> unsupported' once: SET_PROMISC, GET_ASSOCLIST, 'rxchain' | `linux/brcmfmac/core.c:197` `linux/brcmfmac/core.c:200` `linux/brcmfmac/cfg80211.c:3321` `linux/brcmfmac/cfg80211.c:7567` `linux/brcmfmac/cfg80211.c:7570` |
| 9 | name lookup: brcmf_fil_get_errstr returns the table entry, "(unknown)" beyond the table, or "" when built without DEBUG | `linux/brcmfmac/fwil.c:25` `linux/brcmfmac/fwil.c:82` `linux/brcmfmac/fwil.c:84` `linux/brcmfmac/fwil.c:85` `linux/brcmfmac/fwil.c:87` `linux/brcmfmac/fwil.c:92` |

### How whd handles the status
| Step | What the driver does | Citations |
|---|---|---|
| 1 | whd sets the status field to 0 in the command it sends | `whd/src/whd_cdc_bdc.c:243` |
| 2 | CDC path: after the reply arrives whd reads flags and status with dtoh32; status is a uint32_t | `whd/src/whd_cdc_bdc.c:167` `whd/src/whd_cdc_bdc.c:276` `whd/src/whd_cdc_bdc.c:277` `whd/src/include/whd_cdc_bdc.h:76` `whd/src/include/whd_cdc_bdc.h:77` |
| 3 | whd looks at status only when flags & CDCF_IOC_ERROR (0x01) is set; then it releases the response buffer and returns WHD_RESULT_CREATE(WLAN_ENUM_OFFSET - status) if status is non-zero, else WHD_IOCTL_FAIL (WHD_RESULT_CREATE(1008)). With the flag clear it returns WHD_SUCCESS without testing status. | `whd/src/include/whd_cdc_bdc.h:42` `whd/src/whd_cdc_bdc.c:295` `whd/src/whd_cdc_bdc.c:297` `whd/src/whd_cdc_bdc.c:299` `whd/src/whd_cdc_bdc.c:302` `whd/src/whd_cdc_bdc.c:303` `whd/src/whd_cdc_bdc.c:305` `whd/src/whd_cdc_bdc.c:308` `whd/inc/whd_types.h:998` `whd/inc/whd_types.h:1066` |
| 4 | WHD_RESULT_CREATE(x) is CY_RSLT_CREATE(WHD_RESULT_TYPE (0), CY_RSLT_MODULE_DRIVERS_WHD_BASE, x); CY_RSLT_CREATE and the module base are not defined in these sources, so the final 32-bit whd_result_t value is not derivable here, only the code number x (2001..2046) | `whd/inc/whd_types.h:984` `whd/inc/whd_types.h:985` `whd/inc/whd_types.h:987` |
| 5 | a reply timeout is a separate path: the semaphore wait result is returned as-is before any status is read | `whd/src/whd_cdc_bdc.c:265` `whd/src/whd_cdc_bdc.c:266` `whd/src/whd_cdc_bdc.c:271` |
| 6 | msgbuf path (not the CYW43439 buses): the 16-bit completion status is stored with dtoh16 into a uint8_t field, compared to WHD_SUCCESS, and the same 2000 - status expression is returned. Because the field is uint8_t the subtraction is 2000 minus 0..255 (inferred from the declared type; the result would not land on 2001..2046 for a negative 16-bit status). | `whd/src/include/whd_msgbuf.h:183` `whd/src/whd_msgbuf_txrx.c:687` `whd/src/whd_msgbuf_txrx.c:736` `whd/src/whd_msgbuf_txrx.c:466` `whd/src/whd_msgbuf_txrx.c:474` |
| 7 | callers that test a specific code after a command: WHD_WLAN_UNSUPPORTED tolerated (apsta off, tx glomming off, apsta on, join named variable fallback to the older command, CHECK_RETURN_UNSUPPORTED_CONTINUE macro); WHD_WLAN_NOTFOUND from the 'bss' named variable get read as 'AP interface does not exist'. The macro CHECK_RETURN_UNSUPPORTED_OK, despite its name, returns on any result other than WHD_SUCCESS including WHD_WLAN_UNSUPPORTED; it differs from CHECK_RETURN only in not printing (used after WLC_GET_RSSI and two generic get helpers). | `whd/src/whd_ap.c:228` `whd/src/whd_ap.c:229` `whd/src/whd_management.c:472` `whd/src/whd_management.c:473` `whd/src/whd_management.c:490` `whd/src/whd_management.c:491` `whd/src/whd_wifi_api.c:2367` `whd/src/whd_wifi_api.c:2370` `whd/src/include/whd_types_int.h:102` `whd/src/include/whd_types_int.h:103` `whd/src/whd_ap.c:627` `whd/src/whd_ap.c:628` `whd/src/include/whd_types_int.h:96` `whd/src/include/whd_types_int.h:97` `whd/src/include/whd_types_int.h:99` `whd/src/whd_wifi_api.c:1326` `whd/src/whd_wifi_api.c:5085` `whd/src/whd_wifi_api.c:5176` `whd/src/whd_wifi_api.c:2346` |

### How c-driver handles the status
| Step | What the driver does | Citations |
|---|---|---|
| 1 | c-driver's command header record has a 32-bit status field and sets it to 0 on send | `c-driver/cyw43_ll.c:851` `c-driver/cyw43_ll.c:855` `c-driver/cyw43_ll.c:907` |
| 2 | on a control reply c-driver does not read status or the error flag: the only code touching them is commented out, under 'TODO need to handle errors and pass them up' (the commented print would show 2000 - status). It checks only the request id and hands back the payload. No CDCF_IOC_ERROR define found in c-driver (only the ID shift/mask). | `c-driver/cyw43_ll.c:1006` `c-driver/cyw43_ll.c:1007` `c-driver/cyw43_ll.c:1008` `c-driver/cyw43_ll.c:1010` `c-driver/cyw43_ll.c:1011` `c-driver/cyw43_ll.c:1023` `c-driver/cyw43_ll.c:1024` `c-driver/cyw43_ll.c:1026` `c-driver/cyw43_ll.c:160` `c-driver/cyw43_ll.c:161` |
| 3 | cyw43_do_ioctl returns 0 as soon as a control packet with the matching id arrives, copying the payload back into the caller's buffer; its only error returns are the send error and -CYW43_ETIMEDOUT. A non-zero reply status is therefore invisible to callers. | `c-driver/cyw43_ll.c:1294` `c-driver/cyw43_ll.c:1295` `c-driver/cyw43_ll.c:1297` `c-driver/cyw43_ll.c:1304` `c-driver/cyw43_ll.c:1312` `c-driver/cyw43_ll.c:1313` `c-driver/cyw43_ll.c:1324` |
| 4 | a comment in cyw43_ll_wifi_ap_init acknowledges the consequence: the 'bss' get 'can fail with sdpcm status = 0xffffffe2 (NOTASSOCIATED) in such a case the AP is not up and we should not check the result'; the code then reads the buffer regardless | `c-driver/cyw43_ll.c:2359` `c-driver/cyw43_ll.c:2360` `c-driver/cyw43_ll.c:2363` `c-driver/cyw43_ll.c:2364` |

### How embassy handles the status
| Step | What the driver does | Citations |
|---|---|---|
| 1 | embassy's CdcHeader has status: u32 (flags is a u16 followed by id: u16) | `embassy/structs.rs:133` `embassy/structs.rs:136` `embassy/structs.rs:137` `embassy/structs.rs:138` |
| 2 | embassy sets status to 0 in the command it sends | `embassy/runner.rs:1481` `embassy/runner.rs:1486` |
| 3 | when a control reply's id matches the pending command id and status != 0, embassy logs warn!("IOCTL error {}", status as i32) under a 'TODO: propagate error instead' comment; it does not test the error flag bit. A control reply whose id does not match is dropped without any status test. | `embassy/runner.rs:1173` `embassy/runner.rs:1174` `embassy/runner.rs:1175` `embassy/runner.rs:1176` `embassy/runner.rs:1184` `embassy/runner.rs:1186` |
| 4 | the command is then completed exactly as on success: ioctl_done(response) copies the reply payload and the caller gets only a response length; do_ioctl returns usize, with no error channel. If inline_ioctl_pending is set, the flag is cleared and ioctl_done is not called from here; the status warning is the same on both branches. | `embassy/runner.rs:1179` `embassy/runner.rs:1182` `embassy/ioctl.rs:118` `embassy/ioctl.rs:128` `embassy/ioctl.rs:130` `embassy/ioctl.rs:133` `embassy/ioctl.rs:137` `embassy/ioctl.rs:140` `embassy/runner.rs:1180` |

## Event status codes

In the name columns of this and the following sections, — means no name for that value was found in that driver.

### Generic status (event header `status`)

whd's `whd_status_to_string` has a case for each value 0 to 15; the `whd/src/whd_utils.c` line cited in each row is that case. `whd/src/whd_utils.c:365` `whd/src/whd_utils.c:380`

| Value | linux | whd | c-driver | embassy | Meaning (driver comment, shortened) | Citations |
|---|---|---|---|---|---|---|
| 0 | `BRCMF_E_STATUS_SUCCESS` | `WLC_E_STATUS_SUCCESS` | `CYW43_STATUS_SUCCESS` | `EStatus::SUCCESS` | operation was successful | `linux/brcmfmac/fweh.h:118` `c-driver/cyw43_ll.h:69` `whd/inc/whd_events.h:61` `whd/src/include/whd_events_int.h:206` `embassy/consts.rs:257-258` `whd/src/whd_utils.c:365` |
| 1 | `BRCMF_E_STATUS_FAIL` | `WLC_E_STATUS_FAIL` | `CYW43_STATUS_FAIL` | `EStatus::FAIL` | operation failed | `linux/brcmfmac/fweh.h:119` `c-driver/cyw43_ll.h:70` `whd/inc/whd_events.h:62` `whd/src/include/whd_events_int.h:207` `embassy/consts.rs:259-260` `whd/src/whd_utils.c:366` |
| 2 | `BRCMF_E_STATUS_TIMEOUT` | `WLC_E_STATUS_TIMEOUT` | `CYW43_STATUS_TIMEOUT` | `EStatus::TIMEOUT` | operation timed out | `linux/brcmfmac/fweh.h:120` `c-driver/cyw43_ll.h:71` `whd/inc/whd_events.h:63` `whd/src/include/whd_events_int.h:208` `embassy/consts.rs:261-262` `whd/src/whd_utils.c:367` |
| 3 | `BRCMF_E_STATUS_NO_NETWORKS` | `WLC_E_STATUS_NO_NETWORKS` | `CYW43_STATUS_NO_NETWORKS` | `EStatus::NO_NETWORKS` | failed due to no matching network found | `linux/brcmfmac/fweh.h:121` `c-driver/cyw43_ll.h:72` `whd/inc/whd_events.h:64` `whd/src/include/whd_events_int.h:209` `embassy/consts.rs:263-264` `whd/src/whd_utils.c:368` |
| 4 | `BRCMF_E_STATUS_ABORT` | `WLC_E_STATUS_ABORT` | `CYW43_STATUS_ABORT` | `EStatus::ABORT` | operation was aborted | `linux/brcmfmac/fweh.h:122` `c-driver/cyw43_ll.h:73` `whd/inc/whd_events.h:65` `whd/src/include/whd_events_int.h:210` `embassy/consts.rs:265-266` `whd/src/whd_utils.c:369` |
| 5 | `BRCMF_E_STATUS_NO_ACK` | `WLC_E_STATUS_NO_ACK` | `CYW43_STATUS_NO_ACK` | `EStatus::NO_ACK` | protocol failure: packet not ack'd | `linux/brcmfmac/fweh.h:123` `c-driver/cyw43_ll.h:74` `whd/inc/whd_events.h:66` `whd/src/include/whd_events_int.h:211` `embassy/consts.rs:267-268` `whd/src/whd_utils.c:370` |
| 6 | `BRCMF_E_STATUS_UNSOLICITED` | `WLC_E_STATUS_UNSOLICITED` | `CYW43_STATUS_UNSOLICITED` | `EStatus::UNSOLICITED` | AUTH or ASSOC packet was unsolicited | `linux/brcmfmac/fweh.h:124` `c-driver/cyw43_ll.h:75` `whd/inc/whd_events.h:67` `whd/src/include/whd_events_int.h:212` `embassy/consts.rs:269-270` `whd/src/whd_utils.c:371` |
| 7 | `BRCMF_E_STATUS_ATTEMPT` | `WLC_E_STATUS_ATTEMPT` | `CYW43_STATUS_ATTEMPT` | `EStatus::ATTEMPT` | attempt to assoc to an auto auth configuration | `linux/brcmfmac/fweh.h:125` `c-driver/cyw43_ll.h:76` `whd/inc/whd_events.h:68` `whd/src/include/whd_events_int.h:213` `embassy/consts.rs:271-272` `whd/src/whd_utils.c:372` |
| 8 | `BRCMF_E_STATUS_PARTIAL` | `WLC_E_STATUS_PARTIAL` | `CYW43_STATUS_PARTIAL` | `EStatus::PARTIAL` | scan results are incomplete | `linux/brcmfmac/fweh.h:126` `c-driver/cyw43_ll.h:77` `whd/inc/whd_events.h:69` `whd/src/include/whd_events_int.h:214` `embassy/consts.rs:273-274` `whd/src/whd_utils.c:373` |
| 9 | `BRCMF_E_STATUS_NEWSCAN` | `WLC_E_STATUS_NEWSCAN` | `CYW43_STATUS_NEWSCAN` | `EStatus::NEWSCAN` | scan aborted by another scan | `linux/brcmfmac/fweh.h:127` `c-driver/cyw43_ll.h:78` `whd/inc/whd_events.h:70` `whd/src/include/whd_events_int.h:215` `embassy/consts.rs:275-276` `whd/src/whd_utils.c:374` |
| 10 | `BRCMF_E_STATUS_NEWASSOC` | `WLC_E_STATUS_NEWASSOC` | `CYW43_STATUS_NEWASSOC` | `EStatus::NEWASSOC` | scan aborted due to assoc in progress | `linux/brcmfmac/fweh.h:128` `c-driver/cyw43_ll.h:79` `whd/inc/whd_events.h:71` `whd/src/include/whd_events_int.h:216` `embassy/consts.rs:277-278` `whd/src/whd_utils.c:375` |
| 11 | `BRCMF_E_STATUS_11HQUIET` | `WLC_E_STATUS_11HQUIET` | — | `EStatus::_11HQUIET` | 802.11h quiet period started | `linux/brcmfmac/fweh.h:129` `whd/inc/whd_events.h:72` `whd/src/include/whd_events_int.h:217` `embassy/consts.rs:279-280` `whd/src/whd_utils.c:376` |
| 12 | `BRCMF_E_STATUS_SUPPRESS` | `WLC_E_STATUS_SUPPRESS` | — | `EStatus::SUPPRESS` | user disabled scanning (WLC_SET_SCANSUPPRESS) | `linux/brcmfmac/fweh.h:130` `whd/inc/whd_events.h:73` `whd/src/include/whd_events_int.h:218` `embassy/consts.rs:281-282` `whd/src/whd_utils.c:377` |
| 13 | `BRCMF_E_STATUS_NOCHANS` | `WLC_E_STATUS_NOCHANS` | — | `EStatus::NOCHANS` | no allowable channels to scan | `linux/brcmfmac/fweh.h:131` `whd/inc/whd_events.h:74` `whd/src/include/whd_events_int.h:219` `embassy/consts.rs:283-284` `whd/src/whd_utils.c:378` |
| 14 | — | `WLC_E_STATUS_CCXFASTRM` | — | `EStatus::CCXFASTRM` | scan aborted due to CCX fast roam | `whd/inc/whd_events.h:75` `whd/src/include/whd_events_int.h:220` `embassy/consts.rs:285-286` `whd/src/whd_utils.c:379` |
| 15 | `BRCMF_E_STATUS_CS_ABORT` | `WLC_E_STATUS_CS_ABORT` | — | `EStatus::CS_ABORT` | abort channel select | `linux/brcmfmac/fweh.h:132` `whd/inc/whd_events.h:76` `whd/src/include/whd_events_int.h:221` `embassy/consts.rs:287-288` `whd/src/whd_utils.c:380` |
| 16 | `BRCMF_E_STATUS_ERROR` | `WLC_E_STATUS_ERROR` | — | — | request failed due to error | `linux/brcmfmac/fweh.h:133` `whd/inc/whd_events.h:77` |

Where the drivers use these values:

| Value | Use | Citation |
|---|---|---|
| 0 | linux: SET_SSID + SUCCESS starts/finishes link-up (brcmf_is_linkup) | `linux/brcmfmac/cfg80211.c:6255` |
| 0 | linux: SET_SSID with any other status is treated as 'no network' (connect failed) | `linux/brcmfmac/cfg80211.c:6303` |
| 0 | linux: final ESCAN_RESULT: any status other than SUCCESS reports the scan as aborted | `linux/brcmfmac/cfg80211.c:3775` |
| 0 | linux: ROAM + SUCCESS -> roaming done / connect done | `linux/brcmfmac/cfg80211.c:6855` |
| 0 | linux (AP mode): ASSOC_IND/REASSOC_IND new-station path compares the REASON field against BRCMF_E_STATUS_SUCCESS (a status constant, value 0) | `linux/brcmfmac/cfg80211.c:6752-6753` |
| 0 | linux: ACTION_FRAME_COMPLETE + SUCCESS marks the action frame tx completed | `linux/brcmfmac/p2p.c:1538` |
| 0 | linux (cyw vendor): MGMT_FRAME_TXSTATUS + SUCCESS -> ACK, anything else -> NOACK | `linux/brcmfmac/cyw/core.c:348-352` |
| 0 | whd: SET_SSID + SUCCESS sets JOIN_SSID_SET | `whd/src/whd_wifi_api.c:1406` |
| 0 | whd: AUTH + SUCCESS sets JOIN_AUTHENTICATED | `whd/src/whd_wifi_api.c:1440` |
| 0 | whd: REASSOC + SUCCESS sets JOIN_LINK_READY\|JOIN_SSID_SET | `whd/src/whd_wifi_api.c:1465` |
| 0 | whd: ESCAN_RESULT + SUCCESS -> scan completed callback | `whd/src/whd_wifi_api.c:2615` |
| 0 | c-driver: ESCAN_RESULT with literal status 0 -> scan complete | `c-driver/cyw43_ctrl.c:327` |
| 0 | c-driver: literal 'ev->status == 0' gates PRUNE (with reason 8), SET_SSID success, AUTH success, DEAUTH_IND (with reason 2) and LINK handling | `c-driver/cyw43_ctrl.c:349-390` |
| 0 | embassy: join waits for SET_SSID + SUCCESS on an open network; any non-SUCCESS SET_SSID fails the join | `embassy/control.rs:480-482` |
| 0 | embassy: LINK/DEAUTH + SUCCESS -> link down bookkeeping; AUTH SUCCESS sets auth_ok; JOIN + SUCCESS sets join_ok | `embassy/runner.rs:1249-1268` |
| 0 | whd: event-info string helper prints 'WLC_E_STATUS_SUCCESS' when its status argument is the literal 0 | `whd/src/whd_utils.c:1111-1114` |
| 1 | embassy: AUTH + FAIL on a secured network -> JoinError::AuthenticationFailure | `embassy/control.rs:491` |
| 1 | embassy: AUTH + FAIL with reason 16 and auth_type 3 -> link-down bookkeeping (the comment at `embassy/runner.rs:1246` calls it WPA3-specific) | `embassy/runner.rs:1253` |
| 2 | c-driver: AUTH with literal status 2 ('Timeout') is ignored, join keeps trying | `c-driver/cyw43_ctrl.c:373-377` |
| 3 | linux: LINK + NO_NETWORKS is treated as 'no network' (connect failed) | `linux/brcmfmac/cfg80211.c:6297` |
| 3 | whd: SET_SSID + NO_NETWORKS sets JOIN_NO_NETWORKS and does not end the join attempt | `whd/src/whd_wifi_api.c:1412-1414` |
| 3 | c-driver: SET_SSID with literal status 3 and reason 0 -> WIFI_JOIN_STATE_NONET | `c-driver/cyw43_ctrl.c:358-360` |
| 3 | embassy: SET_SSID + NO_NETWORKS -> JoinError::NetworkNotFound | `embassy/control.rs:481` |
| 4 | linux: ESCAN_RESULT + ABORT is dropped without further processing | `linux/brcmfmac/cfg80211.c:3690-3691` |
| 4 | whd: ESCAN_RESULT + ABORT (or NEWSCAN / NEWASSOC) -> WHD_SCAN_ABORTED callback | `whd/src/whd_wifi_api.c:2623-2626` |
| 5 | c-driver: AUTH with literal status 5 ('No ack') is ignored, join keeps trying | `c-driver/cyw43_ctrl.c:373-377` |
| 6 | whd: AUTH + UNSOLICITED is ignored | `whd/src/whd_wifi_api.c:1444-1446` |
| 6 | c-driver: AUTH with literal status 6 ('Unsolicited auth packet') is ignored | `c-driver/cyw43_ctrl.c:373-377` |
| 6 | embassy: AUTH events with status UNSOLICITED do not update auth_ok | `embassy/runner.rs:1262` |
| 6 | embassy: reuses this generic name for PSK_SUP status 6 (see the supplicant state table, value 6) - the name is from the wrong number space, as the embassy comment at `embassy/runner.rs:1274` itself notes | `embassy/control.rs:488-489` |
| 8 | linux: ESCAN_RESULT + PARTIAL carries one batch of scan results | `linux/brcmfmac/cfg80211.c:3699` |
| 8 | whd: ESCAN_RESULT results are parsed only when status is PARTIAL | `whd/src/whd_wifi_api.c:2633` |
| 8 | c-driver: ESCAN_RESULT + CYW43_STATUS_PARTIAL -> parse the scan result in place | `c-driver/cyw43_ll.c:744` |
| 8 | c-driver: ESCAN_RESULT with literal status 8 -> scan callback | `c-driver/cyw43_ctrl.c:321` |
| 8 | embassy: Scanner::next ends the scan on the first ESCAN_RESULT whose status is not PARTIAL | `embassy/control.rs:919` |
| 8 | embassy: ESCAN_RESULT + PARTIAL -> parse BssInfo payload | `embassy/runner.rs:1320` |
| 8 | whd: event-info string helper prints 'WLC_E_STATUS_PARTIAL' when its status argument is the literal 8 | `whd/src/whd_utils.c:1115-1118` |
| 9 | whd: ESCAN_RESULT + NEWSCAN -> WHD_SCAN_ABORTED | `whd/src/whd_wifi_api.c:2623` |
| 10 | whd: ESCAN_RESULT + NEWASSOC -> WHD_SCAN_ABORTED | `whd/src/whd_wifi_api.c:2623` |
| 14 | linux: no name for 14; the list goes from NOCHANS 13 to CS_ABORT 15 | `linux/brcmfmac/fweh.h:131-132` |
| 16 | whd: ERROR=16 exists only in the public header (`whd/inc/whd_events.h:77`); the internal whd_event_status_t enum stops at CS_ABORT=15, and whd_status_to_string (`whd/src/whd_utils.c:361-418`) has no case for it | `whd/src/include/whd_events_int.h:221-223` |

### Host-side sentinels in a status variable

These are values the host stores itself; no driver lists them as received. `whd/inc/whd_events.h:78` `whd/src/include/whd_events_int.h:263` `c-driver/cyw43_ll.c:677-680`

| Value | whd | embassy | Meaning (driver comment, shortened) | Citations |
|---|---|---|---|---|
| 255 | `WLC_E_STATUS_INVALID` | `EStatus::Unknown` | Invalid status code to init variables. | `whd/inc/whd_events.h:78` `embassy/consts.rs:256` |
| 2147483646 (0x7ffffffe) | `WLC_E_STATUS_FORCE_32_BIT` | — | source comment: makes sure a 32 bit variable is what holds the enum | `whd/src/include/whd_events_int.h:263` |
| 4294967295 (0xffffffff) (unverified) | — | — | no comment in source | `c-driver/cyw43_ll.c:677-680` |

Where the drivers use these values:

| Value | Use | Citation |
|---|---|---|
| 255 | embassy: EStatus::from(u8) maps every value not in the enum to Unknown; callers first truncate the 32-bit status with 'as u8' (`embassy/control.rs:477`, `embassy/runner.rs:1229`), so wire status 0x1NN aliases NN | `embassy/util.rs:41-46` |
| 255 | whd: 'Invalid status code to init variables' - a host-side initialiser, not listed as something received | `whd/inc/whd_events.h:78` |
| 2147483646 | whd: forces the enum to 32 bits; not a code | `whd/src/include/whd_events_int.h:263` |
| 2147483646 | whd: whd_status_to_string has a 'case WLC_E_STATUS_FORCE_32_BIT:' label that falls into default and returns "Unknown" | `whd/src/whd_utils.c:418-420` |
| 4294967295 | c-driver: writes (uint32_t)-1 into ev->status itself to mark a scan result whose IE offset/length is out of bounds; host-generated, not received | `c-driver/cyw43_ll.c:677-680` |

Rows marked (unverified):

- value 4294967295: no driver names this value; it appears only as a literal. `c-driver/cyw43_ll.c:677-680`

### 802.11 status codes on DISASSOC and DEAUTH (whd only)

whd names the event header `status` of DISASSOC and DEAUTH events as 802.11 status codes. For those two events whd adds `WLC_DOT11_SC_STATUS_OFFSET` (512) to the received status before dispatch; the msgbuf path does the same. "Value" is the number before the offset. `whd/src/whd_cdc_bdc.c:876-879` `whd/src/whd_msgbuf_txrx.c:834`

No whd code compares against a `WLC_DOT11_SC_*` name; they appear only in `whd_status_to_string`. `whd/src/whd_utils.c:393-417`

| Value | whd value after offset | whd | Meaning (driver comment, shortened) | Citations |
|---|---|---|---|---|
| 0 | 512 | `WLC_DOT11_SC_SUCCESS` | Successful | `whd/src/include/whd_events_int.h:237` `whd/src/whd_cdc_bdc.c:876-879` |
| 1 | 513 | `WLC_DOT11_SC_FAILURE` | Unspecified failure | `whd/src/include/whd_events_int.h:238` `whd/src/whd_cdc_bdc.c:876-879` |
| 10 | 522 | `WLC_DOT11_SC_CAP_MISMATCH` | cannot support all requested capabilities | `whd/src/include/whd_events_int.h:239` `whd/src/whd_cdc_bdc.c:876-879` |
| 11 | 523 | `WLC_DOT11_SC_REASSOC_FAIL` | reassociation denied: association not confirmed | `whd/src/include/whd_events_int.h:240` `whd/src/whd_cdc_bdc.c:876-879` |
| 12 | 524 | `WLC_DOT11_SC_ASSOC_FAIL` | association denied, reason outside the standard | `whd/src/include/whd_events_int.h:241` `whd/src/whd_cdc_bdc.c:876-879` |
| 13 | 525 | `WLC_DOT11_SC_AUTH_MISMATCH` | auth algorithm not supported by responder | `whd/src/include/whd_events_int.h:242` `whd/src/whd_cdc_bdc.c:876-879` |
| 14 | 526 | `WLC_DOT11_SC_AUTH_SEQ` | auth frame sequence number out of order | `whd/src/include/whd_events_int.h:243` `whd/src/whd_cdc_bdc.c:876-879` |
| 15 | 527 | `WLC_DOT11_SC_AUTH_CHALLENGE_FAIL` | auth rejected: challenge failure | `whd/src/include/whd_events_int.h:244` `whd/src/whd_cdc_bdc.c:876-879` |
| 16 | 528 | `WLC_DOT11_SC_AUTH_TIMEOUT` | auth rejected: timeout waiting for next frame | `whd/src/include/whd_events_int.h:245` `whd/src/whd_cdc_bdc.c:876-879` |
| 17 | 529 | `WLC_DOT11_SC_ASSOC_BUSY_FAIL` | association denied: AP cannot take more stations | `whd/src/include/whd_events_int.h:246` `whd/src/whd_cdc_bdc.c:876-879` |
| 18 | 530 | `WLC_DOT11_SC_ASSOC_RATE_MISMATCH` | association denied: basic rates not supported | `whd/src/include/whd_events_int.h:247` `whd/src/whd_cdc_bdc.c:876-879` |
| 19 | 531 | `WLC_DOT11_SC_ASSOC_SHORT_REQUIRED` | association denied: Short Preamble not supported | `whd/src/include/whd_events_int.h:248` `whd/src/whd_cdc_bdc.c:876-879` |
| 20 | 532 | `WLC_DOT11_SC_ASSOC_PBCC_REQUIRED` | association denied: PBCC not supported | `whd/src/include/whd_events_int.h:249` `whd/src/whd_cdc_bdc.c:876-879` |
| 21 | 533 | `WLC_DOT11_SC_ASSOC_AGILITY_REQUIRED` | association denied: Channel Agility not supported | `whd/src/include/whd_events_int.h:250` `whd/src/whd_cdc_bdc.c:876-879` |
| 22 | 534 | `WLC_DOT11_SC_ASSOC_SPECTRUM_REQUIRED` | association denied: Spectrum Management required | `whd/src/include/whd_events_int.h:251` `whd/src/whd_cdc_bdc.c:876-879` |
| 23 | 535 | `WLC_DOT11_SC_ASSOC_BAD_POWER_CAP` | association denied: Power Cap element unacceptable | `whd/src/include/whd_events_int.h:252` `whd/src/whd_cdc_bdc.c:876-879` |
| 24 | 536 | `WLC_DOT11_SC_ASSOC_BAD_SUP_CHANNELS` | association denied: Supported Channel element unacceptable | `whd/src/include/whd_events_int.h:253` `whd/src/whd_cdc_bdc.c:876-879` |
| 25 | 537 | `WLC_DOT11_SC_ASSOC_SHORTSLOT_REQUIRED` | association denied: Short Slot Time not supported | `whd/src/include/whd_events_int.h:254` `whd/src/whd_cdc_bdc.c:876-879` |
| 26 | 538 | `WLC_DOT11_SC_ASSOC_ERPBCC_REQUIRED` | association denied: ER-PBCC not supported | `whd/src/include/whd_events_int.h:255` `whd/src/whd_cdc_bdc.c:876-879` |
| 27 | 539 | `WLC_DOT11_SC_ASSOC_DSSOFDM_REQUIRED` | association denied: DSS-OFDM not supported | `whd/src/include/whd_events_int.h:256` `whd/src/whd_cdc_bdc.c:876-879` |
| 37 | 549 | `WLC_DOT11_SC_DECLINED` | request declined | `whd/src/include/whd_events_int.h:257` `whd/src/whd_cdc_bdc.c:876-879` |
| 38 | 550 | `WLC_DOT11_SC_INVALID_PARAMS` | One or more params have invalid values | `whd/src/include/whd_events_int.h:258` `whd/src/whd_cdc_bdc.c:876-879` |
| 43 | 555 | `WLC_DOT11_SC_INVALID_AKMP` | Association denied due to invalid AKMP | `whd/src/include/whd_events_int.h:259` `whd/src/whd_cdc_bdc.c:876-879` |
| 54 | 566 | `WLC_DOT11_SC_INVALID_MDID` | Association denied due to invalid MDID | `whd/src/include/whd_events_int.h:260` `whd/src/whd_cdc_bdc.c:876-879` |
| 55 | 567 | `WLC_DOT11_SC_INVALID_FTIE` | Association denied due to invalid FTIE | `whd/src/include/whd_events_int.h:261` `whd/src/whd_cdc_bdc.c:876-879` |

Where the drivers use these values:

| Value | Use | Citation |
|---|---|---|
| 0 | whd: a second enum dot11_sc_t names 802.11 status codes without an offset (DOT11_SC_SUCCESS 0, FAILURE 1, TDLS_WAKEUP_SCH_ALT 2, TDLS_WAKEUP_SCH_REJ 3, TDLS_SEC_DISABLED 5, LIFETIME_REJ 6, NOT_SAME_BSS 7, CAP_MISMATCH 10 .. AUTH_TIMEOUT 16). Its only use found is host-side: `whd/src/whd_wifi_api.c:5498` compares the caller's params->flags with DOT11_SC_SUCCESS before writing the auth_status setting. It is not applied to an event field, so its values 2, 3, 5, 6, 7 have no rows in this table | `whd/src/include/whd_types_int.h:348-368` |

## Event reason codes

### Generic / roam reasons (event header `reason`)

whd calls these "roam reason codes". whd's `whd_reason_to_string` returns the name for each value 0 to 8; the `whd/src/whd_utils.c` line cited in each row is that case. `whd/src/whd_utils.c:429` `whd/src/whd_utils.c:437`

| Value | linux | whd | c-driver | Meaning (driver comment, shortened) | Citations |
|---|---|---|---|---|---|
| 0 | `BRCMF_E_REASON_INITIAL_ASSOC` | `WLC_E_REASON_INITIAL_ASSOC` | `CYW43_REASON_INITIAL_ASSOC` | initial assoc | `linux/brcmfmac/fweh.h:146` `c-driver/cyw43_ll.h:99` `whd/src/include/whd_events_int.h:278` `whd/src/whd_utils.c:429` |
| 1 | `BRCMF_E_REASON_LOW_RSSI` | `WLC_E_REASON_LOW_RSSI` | `CYW43_REASON_LOW_RSSI` | roamed due to low RSSI | `linux/brcmfmac/fweh.h:147` `c-driver/cyw43_ll.h:100` `whd/src/include/whd_events_int.h:279` `whd/src/whd_utils.c:430` |
| 2 (unverified) | `BRCMF_E_REASON_DEAUTH` | `WLC_E_REASON_DEAUTH` | `CYW43_REASON_DEAUTH` | roamed due to DEAUTH indication | `linux/brcmfmac/fweh.h:148` `c-driver/cyw43_ll.h:101` `whd/src/include/whd_events_int.h:280` `whd/src/whd_utils.c:431` |
| 3 | `BRCMF_E_REASON_DISASSOC` | `WLC_E_REASON_DISASSOC` | `CYW43_REASON_DISASSOC` | roamed due to DISASSOC indication | `linux/brcmfmac/fweh.h:149` `c-driver/cyw43_ll.h:102` `whd/src/include/whd_events_int.h:281` `whd/src/whd_utils.c:432` |
| 4 | `BRCMF_E_REASON_BCNS_LOST` | `WLC_E_REASON_BCNS_LOST` | `CYW43_REASON_BCNS_LOST` | roamed due to lost beacons | `linux/brcmfmac/fweh.h:150` `c-driver/cyw43_ll.h:103` `whd/src/include/whd_events_int.h:282` `whd/src/whd_utils.c:433` |
| 5 | `BRCMF_E_REASON_FAST_ROAM_FAILED` | `WLC_E_REASON_FAST_ROAM_FAILED` | `CYW43_REASON_FAST_ROAM_FAILED` | roamed due to fast roam failure | `linux/brcmfmac/fweh.h:155` `c-driver/cyw43_ll.h:104` `whd/src/include/whd_events_int.h:283` `whd/src/whd_utils.c:434` |
| 6 | `BRCMF_E_REASON_DIRECTED_ROAM` | `WLC_E_REASON_DIRECTED_ROAM` | `CYW43_REASON_DIRECTED_ROAM` | roamed due to request by AP | `linux/brcmfmac/fweh.h:156` `c-driver/cyw43_ll.h:105` `whd/src/include/whd_events_int.h:284` `whd/src/whd_utils.c:435` |
| 7 | `BRCMF_E_REASON_TSPEC_REJECTED` | `WLC_E_REASON_TSPEC_REJECTED` | `CYW43_REASON_TSPEC_REJECTED` | roamed due to TSPEC rejection | `linux/brcmfmac/fweh.h:157` `c-driver/cyw43_ll.h:106` `whd/src/include/whd_events_int.h:285` `whd/src/whd_utils.c:436` |
| 8 | `BRCMF_E_REASON_BETTER_AP` | `WLC_E_REASON_BETTER_AP` | `CYW43_REASON_BETTER_AP` | roamed due to finding better AP | `linux/brcmfmac/fweh.h:158` `c-driver/cyw43_ll.h:107` `whd/src/include/whd_events_int.h:286` `whd/src/whd_utils.c:437` |
| 9 | `BRCMF_E_REASON_MINTXRATE` | — | — | no comment in source | `linux/brcmfmac/fweh.h:151` |
| 10 | `BRCMF_E_REASON_TXFAIL` | — | — | no comment in source | `linux/brcmfmac/fweh.h:152` |

Where the drivers use these values:

| Value | Use | Citation |
|---|---|---|
| 0 | whd: event-info string helper prints 'WLC_E_REASON_INITIAL_ASSOC' for reason 0 on any event | `whd/src/whd_utils.c:1124-1126` |
| 0 | c-driver: SET_SSID status 3 is 'no network' only when reason is literal 0 | `c-driver/cyw43_ctrl.c:358` |
| 0 | c-driver: the CYW43_REASON_* roam block is captioned 'Values for AP auth setting'; no CYW43_REASON_* name is referenced in c-driver/*.c | `c-driver/cyw43_ll.h:98` |
| 2 | c-driver: DEAUTH_IND with status 0 and literal reason 2 -> 'probably because password was wrong', disassociate. Which table reason 2 belongs to on DEAUTH_IND is not stated in c-driver (this table says DEAUTH, the 802.11 table says 'previous authentication no longer valid'; linux treats DEAUTH_IND reason as an 802.11 reason code, see the 802.11 reason code table) | `c-driver/cyw43_ctrl.c:383-387` |
| 9 | linux: defined only (no use of BRCMF_E_REASON_MINTXRATE found under linux/); whd uses reason 9 for a NAN sub-event name instead (see the NAN sub-event table) | `linux/brcmfmac/fweh.h:151` |
| 10 | linux: defined only; whd uses reason 10 for a NAN sub-event name instead (see the NAN sub-event table) | `linux/brcmfmac/fweh.h:152` |

Rows marked (unverified):

- value 2: defined with this value in 3 drivers (c-driver, linux, whd). Which table the c-driver DEAUTH_IND literal reason 2 belongs to stays unresolved: c-driver does not say; shown under both tables. `linux/brcmfmac/fweh.h:148` `c-driver/cyw43_ll.h:101` `whd/src/include/whd_events_int.h:280`

### Reason when the event is LINK
| Value | linux | whd | Meaning (driver comment, shortened) | Citations |
|---|---|---|---|---|
| 1 | — | `WLC_E_LINK_BCN_LOSS` | Link down because of beacon loss | `whd/inc/whd_events.h:128` `whd/src/include/whd_events_int.h:386` |
| 2 | — | `WLC_E_LINK_DISASSOC` | Link down because of disassoc | `whd/inc/whd_events.h:129` `whd/src/include/whd_events_int.h:387` |
| 3 | — | `WLC_E_LINK_ASSOC_REC` | Link down because assoc recreate failed | `whd/inc/whd_events.h:130` `whd/src/include/whd_events_int.h:388` |
| 4 | `BRCMF_E_REASON_LINK_BSSCFG_DIS` | `WLC_E_LINK_BSSCFG_DIS` | Link down due to bsscfg down | `linux/brcmfmac/fweh.h:154` `whd/inc/whd_events.h:131` `whd/src/include/whd_events_int.h:389` |

Where the drivers use these values:

| Value | Use | Citation |
|---|---|---|
| 1 | whd (msgbuf path, CERT_MULTI_AKM && COMPONENT_CAT5 builds only): rewrites a DISASSOC_IND into LINK with flags 0 and reason WLC_E_LINK_BCN_LOSS - host-generated | `whd/src/whd_msgbuf_txrx.c:876-882` |
| 1 | embassy: comment only - 'reason = 1: loss of signal (e.g. out of range), reason = 2: controlled network shutdown' on LINK down; the match ignores reason | `embassy/runner.rs:1245` |
| 2 | embassy: comment only - LINK down 'reason = 2: controlled network shutdown' | `embassy/runner.rs:1245` |
| 4 | linux (AP mode): LINK with reason LINK_BSSCFG_DIS on a non-primary netdev = 'AP mode link down', completes vif_disabled | `linux/brcmfmac/cfg80211.c:6745-6749` |

### Reason when the event is TDLS_PEER_EVENT (linux only)
| Value | linux | Meaning (driver comment, shortened) | Citations |
|---|---|---|---|
| 0 | `BRCMF_E_REASON_TDLS_PEER_DISCOVERED` | no comment in source | `linux/brcmfmac/fweh.h:160` |
| 1 | `BRCMF_E_REASON_TDLS_PEER_CONNECTED` | no comment in source | `linux/brcmfmac/fweh.h:161` |
| 2 | `BRCMF_E_REASON_TDLS_PEER_DISCONNECTED` | no comment in source | `linux/brcmfmac/fweh.h:162` |

Where the drivers use these values:

| Value | Use | Citation |
|---|---|---|
| 0 | linux: TDLS_PEER_EVENT reason switch - debug print only | `linux/brcmfmac/cfg80211.c:5946-5949` |
| 1 | linux: TDLS_PEER_EVENT -> brcmf_proto_add_tdls_peer | `linux/brcmfmac/cfg80211.c:5950-5953` |
| 2 | linux: TDLS_PEER_EVENT -> brcmf_proto_delete_peer | `linux/brcmfmac/cfg80211.c:5954-5957` |

### 802.11 reason codes (event header `reason`)

whd applies this table to DISASSOC and DEAUTH only: for those two events it adds `WLC_E_DOT11_RC_REASON_OFFSET` (768) to the received reason before dispatch (same in the msgbuf path). DEAUTH_IND and DISASSOC_IND reasons are passed through without an offset. "Value" is the number before the offset. `whd/src/whd_cdc_bdc.c:876-879` `whd/src/whd_msgbuf_txrx.c:835`

linux brcmfmac never compares an event reason with a `WLAN_REASON_*` name. For DEAUTH, DEAUTH_IND and DISASSOC_IND it passes `e->reason` through unchanged as the 802.11 reason code to `brcmf_link_down` -> `cfg80211_disconnected`. The kernel names in the table are the kernel's names for those numbers, not brcmfmac definitions. `linux/brcmfmac/cfg80211.c:1696-1701` `linux/brcmfmac/cfg80211.c:6825-6826` `linux/brcmfmac/cfg80211.c:1767`

| Value | whd value after offset | whd | kernel `ieee80211.h` name | Meaning (driver comment, shortened) | Citations |
|---|---|---|---|---|---|
| 0 | 768 | `DOT11_RC_RESERVED` / `WHD_DOT11_RC_RESERVED` | — | d11 RC reserved | `whd/src/include/whd_events_int.h:346` `whd/inc/whd_types.h:269` `whd/src/whd_cdc_bdc.c:876-879` |
| 1 | 769 | `DOT11_RC_UNSPECIFIED` / `WHD_DOT11_RC_UNSPECIFIED` | `WLAN_REASON_UNSPECIFIED` | Unspecified reason | `whd/src/include/whd_events_int.h:347` `whd/inc/whd_types.h:270` `linux-headers/ieee80211.h:1534` `whd/src/whd_cdc_bdc.c:876-879` `linux/brcmfmac/cfg80211.c:1696-1701` |
| 2 (unverified) | 770 | `DOT11_RC_AUTH_INVAL` | `WLAN_REASON_PREV_AUTH_NOT_VALID` | Previous authentication no longer valid | `whd/src/include/whd_events_int.h:348` `linux-headers/ieee80211.h:1535` `whd/src/whd_cdc_bdc.c:876-879` `linux/brcmfmac/cfg80211.c:1696-1701` |
| 3 | 771 | `DOT11_RC_DEAUTH_LEAVING` | `WLAN_REASON_DEAUTH_LEAVING` | deauthenticated: sender leaving IBSS or ESS | `whd/src/include/whd_events_int.h:349` `linux-headers/ieee80211.h:1536` `whd/src/whd_cdc_bdc.c:876-879` `linux/brcmfmac/cfg80211.c:1696-1701` |
| 4 | 772 | `DOT11_RC_INACTIVITY` | `WLAN_REASON_DISASSOC_DUE_TO_INACTIVITY` | Disassociated due to inactivity | `whd/src/include/whd_events_int.h:350` `linux-headers/ieee80211.h:1537` `whd/src/whd_cdc_bdc.c:876-879` `linux/brcmfmac/cfg80211.c:1696-1701` |
| 5 | 773 | `DOT11_RC_BUSY` | `WLAN_REASON_DISASSOC_AP_BUSY` | disassociated: AP cannot handle all stations | `whd/src/include/whd_events_int.h:351` `linux-headers/ieee80211.h:1538` `whd/src/whd_cdc_bdc.c:876-879` `linux/brcmfmac/cfg80211.c:1696-1701` |
| 6 | 774 | `DOT11_RC_INVAL_CLASS_2` | `WLAN_REASON_CLASS2_FRAME_FROM_NONAUTH_STA` | class 2 frame from nonauthenticated station | `whd/src/include/whd_events_int.h:352` `linux-headers/ieee80211.h:1539` `whd/src/whd_cdc_bdc.c:876-879` `linux/brcmfmac/cfg80211.c:1696-1701` |
| 7 | 775 | `DOT11_RC_INVAL_CLASS_3` | `WLAN_REASON_CLASS3_FRAME_FROM_NONASSOC_STA` | class 3 frame from nonassociated station | `whd/src/include/whd_events_int.h:353` `linux-headers/ieee80211.h:1540` `whd/src/whd_cdc_bdc.c:876-879` `linux/brcmfmac/cfg80211.c:1696-1701` |
| 8 | 776 | `DOT11_RC_DISASSOC_LEAVING` | `WLAN_REASON_DISASSOC_STA_HAS_LEFT` | disassociated: sender leaving BSS | `whd/src/include/whd_events_int.h:354` `linux-headers/ieee80211.h:1541` `whd/src/whd_cdc_bdc.c:876-879` `linux/brcmfmac/cfg80211.c:1696-1701` |
| 9 | 777 | `DOT11_RC_NOT_AUTH` | `WLAN_REASON_STA_REQ_ASSOC_WITHOUT_AUTH` | (re)association requested without authentication | `whd/src/include/whd_events_int.h:355` `linux-headers/ieee80211.h:1542` `whd/src/whd_cdc_bdc.c:876-879` `linux/brcmfmac/cfg80211.c:1696-1701` |
| 10 | 778 | `DOT11_RC_BAD_PC` | `WLAN_REASON_DISASSOC_BAD_POWER` | Unacceptable power capability element | `whd/src/include/whd_events_int.h:356` `linux-headers/ieee80211.h:1544` `whd/src/whd_cdc_bdc.c:876-879` `linux/brcmfmac/cfg80211.c:1696-1701` |
| 11 | 779 | `DOT11_RC_BAD_CHANNELS` | `WLAN_REASON_DISASSOC_BAD_SUPP_CHAN` | Unacceptable supported channels element | `whd/src/include/whd_events_int.h:357` `linux-headers/ieee80211.h:1545` `whd/src/whd_cdc_bdc.c:876-879` `linux/brcmfmac/cfg80211.c:1696-1701` |
| 12 (unverified) | — | — | — | no comment in source | `whd/src/include/whd_events_int.h:358-359` |
| 13 | — | — | `WLAN_REASON_INVALID_IE` | no comment in source | `linux-headers/ieee80211.h:1547` `linux/brcmfmac/cfg80211.c:1696-1701` |
| 14 | — | — | `WLAN_REASON_MIC_FAILURE` | no comment in source | `linux-headers/ieee80211.h:1548` `linux/brcmfmac/cfg80211.c:1696-1701` |
| 15 | — | — | `WLAN_REASON_4WAY_HANDSHAKE_TIMEOUT` | no comment in source | `linux-headers/ieee80211.h:1549` `linux/brcmfmac/cfg80211.c:1696-1701` |
| 16 | — | — | `WLAN_REASON_GROUP_KEY_HANDSHAKE_TIMEOUT` | no comment in source | `linux-headers/ieee80211.h:1550` `linux/brcmfmac/cfg80211.c:1696-1701` |
| 17 | — | — | `WLAN_REASON_IE_DIFFERENT` | no comment in source | `linux-headers/ieee80211.h:1551` `linux/brcmfmac/cfg80211.c:1696-1701` |
| 18 | — | — | `WLAN_REASON_INVALID_GROUP_CIPHER` | no comment in source | `linux-headers/ieee80211.h:1552` `linux/brcmfmac/cfg80211.c:1696-1701` |
| 19 | — | — | `WLAN_REASON_INVALID_PAIRWISE_CIPHER` | no comment in source | `linux-headers/ieee80211.h:1553` `linux/brcmfmac/cfg80211.c:1696-1701` |
| 20 | — | — | `WLAN_REASON_INVALID_AKMP` | no comment in source | `linux-headers/ieee80211.h:1554` `linux/brcmfmac/cfg80211.c:1696-1701` |
| 21 | — | — | `WLAN_REASON_UNSUPP_RSN_VERSION` | no comment in source | `linux-headers/ieee80211.h:1555` `linux/brcmfmac/cfg80211.c:1696-1701` |
| 22 | — | — | `WLAN_REASON_INVALID_RSN_IE_CAP` | no comment in source | `linux-headers/ieee80211.h:1556` `linux/brcmfmac/cfg80211.c:1696-1701` |
| 23 | 791 | `DOT11_RC_MAX` | `WLAN_REASON_IEEE8021X_FAILED` | Reason codes > 23 are reserved | `whd/src/include/whd_events_int.h:369` `linux-headers/ieee80211.h:1557` `whd/src/whd_cdc_bdc.c:876-879` `linux/brcmfmac/cfg80211.c:1696-1701` |
| 24 | — | — | `WLAN_REASON_CIPHER_SUITE_REJECTED` | no comment in source | `linux-headers/ieee80211.h:1558` `linux/brcmfmac/cfg80211.c:1696-1701` |
| 25 | — | — | `WLAN_REASON_TDLS_TEARDOWN_UNREACHABLE` | no comment in source | `linux-headers/ieee80211.h:1560` `linux/brcmfmac/cfg80211.c:1696-1701` |
| 26 | — | — | `WLAN_REASON_TDLS_TEARDOWN_UNSPECIFIED` | no comment in source | `linux-headers/ieee80211.h:1561` `linux/brcmfmac/cfg80211.c:1696-1701` |
| 32 | 800 | `DOT11_RC_UNSPECIFIED_QOS` | `WLAN_REASON_DISASSOC_UNSPECIFIED_QOS` | unspecified QoS-related reason | `whd/src/include/whd_events_int.h:361` `linux-headers/ieee80211.h:1563` `whd/src/whd_cdc_bdc.c:876-879` `linux/brcmfmac/cfg80211.c:1696-1701` |
| 33 | 801 | `DOT11_RC_INSUFFCIENT_BW` | `WLAN_REASON_DISASSOC_QAP_NO_BANDWIDTH` | QAP lacks sufficient bandwidth | `whd/src/include/whd_events_int.h:362` `linux-headers/ieee80211.h:1564` `whd/src/whd_cdc_bdc.c:876-879` `linux/brcmfmac/cfg80211.c:1696-1701` |
| 34 | 802 | `DOT11_RC_EXCESSIVE_FRAMES` | `WLAN_REASON_DISASSOC_LOW_ACK` | excessive number of frames need ack | `whd/src/include/whd_events_int.h:363` `linux-headers/ieee80211.h:1565` `whd/src/whd_cdc_bdc.c:876-879` `linux/brcmfmac/cfg80211.c:1696-1701` |
| 35 | 803 | `DOT11_RC_TX_OUTSIDE_TXOP` | `WLAN_REASON_DISASSOC_QAP_EXCEED_TXOP` | transmitting outside the limits of txop | `whd/src/include/whd_events_int.h:364` `linux-headers/ieee80211.h:1566` `whd/src/whd_cdc_bdc.c:876-879` `linux/brcmfmac/cfg80211.c:1696-1701` |
| 36 | 804 | `DOT11_RC_LEAVING_QBSS` | `WLAN_REASON_QSTA_LEAVE_QBSS` | QSTA is leaving the QBSS (or restting) | `whd/src/include/whd_events_int.h:365` `linux-headers/ieee80211.h:1567` `whd/src/whd_cdc_bdc.c:876-879` `linux/brcmfmac/cfg80211.c:1696-1701` |
| 37 | 805 | `DOT11_RC_BAD_MECHANISM` | `WLAN_REASON_QSTA_NOT_USE` | does not want to use the mechanism | `whd/src/include/whd_events_int.h:366` `linux-headers/ieee80211.h:1568` `whd/src/whd_cdc_bdc.c:876-879` `linux/brcmfmac/cfg80211.c:1696-1701` |
| 38 | 806 | `DOT11_RC_SETUP_NEEDED` | `WLAN_REASON_QSTA_REQUIRE_SETUP` | mechanism needs a setup | `whd/src/include/whd_events_int.h:367` `linux-headers/ieee80211.h:1569` `whd/src/whd_cdc_bdc.c:876-879` `linux/brcmfmac/cfg80211.c:1696-1701` |
| 39 | 807 | `DOT11_RC_TIMEOUT` | `WLAN_REASON_QSTA_TIMEOUT` | timeout | `whd/src/include/whd_events_int.h:368` `linux-headers/ieee80211.h:1570` `whd/src/whd_cdc_bdc.c:876-879` `linux/brcmfmac/cfg80211.c:1696-1701` |
| 45 | — | — | `WLAN_REASON_QSTA_CIPHER_NOT_SUPP` | no comment in source | `linux-headers/ieee80211.h:1571` `linux/brcmfmac/cfg80211.c:1696-1701` |
| 52 | — | — | `WLAN_REASON_MESH_PEER_CANCELED` | no comment in source | `linux-headers/ieee80211.h:1573` `linux/brcmfmac/cfg80211.c:1696-1701` |
| 53 | — | — | `WLAN_REASON_MESH_MAX_PEERS` | no comment in source | `linux-headers/ieee80211.h:1574` `linux/brcmfmac/cfg80211.c:1696-1701` |
| 54 | — | — | `WLAN_REASON_MESH_CONFIG` | no comment in source | `linux-headers/ieee80211.h:1575` `linux/brcmfmac/cfg80211.c:1696-1701` |
| 55 | — | — | `WLAN_REASON_MESH_CLOSE` | no comment in source | `linux-headers/ieee80211.h:1576` `linux/brcmfmac/cfg80211.c:1696-1701` |
| 56 | — | — | `WLAN_REASON_MESH_MAX_RETRIES` | no comment in source | `linux-headers/ieee80211.h:1577` `linux/brcmfmac/cfg80211.c:1696-1701` |
| 57 | — | — | `WLAN_REASON_MESH_CONFIRM_TIMEOUT` | no comment in source | `linux-headers/ieee80211.h:1578` `linux/brcmfmac/cfg80211.c:1696-1701` |
| 58 | — | — | `WLAN_REASON_MESH_INVALID_GTK` | no comment in source | `linux-headers/ieee80211.h:1579` `linux/brcmfmac/cfg80211.c:1696-1701` |
| 59 | — | — | `WLAN_REASON_MESH_INCONSISTENT_PARAM` | no comment in source | `linux-headers/ieee80211.h:1580` `linux/brcmfmac/cfg80211.c:1696-1701` |
| 60 | — | — | `WLAN_REASON_MESH_INVALID_SECURITY` | no comment in source | `linux-headers/ieee80211.h:1581` `linux/brcmfmac/cfg80211.c:1696-1701` |
| 61 | — | — | `WLAN_REASON_MESH_PATH_ERROR` | no comment in source | `linux-headers/ieee80211.h:1582` `linux/brcmfmac/cfg80211.c:1696-1701` |
| 62 | — | — | `WLAN_REASON_MESH_PATH_NOFORWARD` | no comment in source | `linux-headers/ieee80211.h:1583` `linux/brcmfmac/cfg80211.c:1696-1701` |
| 63 | — | — | `WLAN_REASON_MESH_PATH_DEST_UNREACHABLE` | no comment in source | `linux-headers/ieee80211.h:1584` `linux/brcmfmac/cfg80211.c:1696-1701` |
| 64 | — | — | `WLAN_REASON_MAC_EXISTS_IN_MBSS` | no comment in source | `linux-headers/ieee80211.h:1585` `linux/brcmfmac/cfg80211.c:1696-1701` |
| 65 | — | — | `WLAN_REASON_MESH_CHAN_REGULATORY` | no comment in source | `linux-headers/ieee80211.h:1586` `linux/brcmfmac/cfg80211.c:1696-1701` |
| 66 | — | — | `WLAN_REASON_MESH_CHAN` | no comment in source | `linux-headers/ieee80211.h:1587` `linux/brcmfmac/cfg80211.c:1696-1701` |

Where the drivers use these values:

| Value | Use | Citation |
|---|---|---|
| 0 | whd: WHD_DOT11_RC_* is the argument type of whd_wifi_deauth_sta (`whd/inc/whd_wifi_api.h:837`), a value the host sends, listed here because it names the same numbers | `whd/inc/whd_types.h:267-271` |
| 2 | c-driver: DEAUTH_IND with status 0 and literal reason 2 -> disassociate ('probably because password was wrong'); c-driver names no table for it (see also the roam reason table, value 2) | `c-driver/cyw43_ctrl.c:383-387` |
| 12 | whd: no names for 12-23: header comments say '12 is unused' and that proto/wpa.h defines 13-23, which are WPA/802.11i reason codes (that file is not in these sources) | `whd/src/include/whd_events_int.h:358-359` |
| 23 | whd: DOT11_RC_MAX is a bound ('Reason codes > 23 are reserved'), not a code; the same enum nevertheless defines 32-39 | `whd/src/include/whd_events_int.h:369` |
| 23 | whd: whd_reason_to_string treats DOT11_RC_MAX (791 after the offset) as unnamed: its case label falls into default and returns "Unknown" | `whd/src/whd_utils.c:509-512` |

Rows marked (unverified):

- value 2: whd and the kernel 802.11 table both name this number. Which table the c-driver DEAUTH_IND literal reason 2 belongs to stays unresolved: c-driver does not say; shown under both tables. `whd/src/include/whd_events_int.h:348` `linux-headers/ieee80211.h:1535`
- value 12: no driver names this value; the whd header has only comments about it. `whd/src/include/whd_events_int.h:358-359`

### Reason on an AUTH event (number space not stated)

embassy matches a literal reason on AUTH events. No driver names the value or says which table it belongs to. `embassy/runner.rs:1246-1253`

| Value | Meaning (driver comment, shortened) | Citations |
|---|---|---|
| 16 (unverified) | no comment in source | `embassy/runner.rs:1246-1253` |

Where the drivers use these values:

| Value | Use | Citation |
|---|---|---|
| 16 | embassy: matches AUTH with status FAIL, literal reason 16 and auth_type 3 as link-down (comment: 'specific for WPA3 networks'). embassy gives the number no name and does not say which code table it belongs to; no other driver here tests the reason of an AUTH event | `embassy/runner.rs:1246-1253` |

Rows marked (unverified):

- value 16: a literal in one driver, no name, table unknown. Which code table 16 belongs to is not stated anywhere in these sources. `embassy/runner.rs:1246-1253`

### NAN sub-events as the reason of WLC_E_NAN (whd only)

whd's header comment says these arrive as the reason code of event `WLC_E_NAN`. The names are used only in `whd_reason_to_string`. `whd/src/include/whd_events_int.h:288` `whd/src/whd_utils.c:493-508`

linux uses 9 and 10 for `BRCMF_E_REASON_MINTXRATE` and `BRCMF_E_REASON_TXFAIL` in its generic reason list instead (see the roam table). `linux/brcmfmac/fweh.h:151` `linux/brcmfmac/fweh.h:152`

| Value | whd | Meaning (driver comment, shortened) | Citations |
|---|---|---|---|
| 9 | `WLC_E_NAN_EVENT_STATUS_CHG` | generated on any change in nan_mac status | `whd/src/include/whd_events_int.h:289` `whd/src/include/whd_events_int.h:288` |
| 10 | `WLC_E_NAN_EVENT_MERGE` | Merged to a NAN cluster | `whd/src/include/whd_events_int.h:290` `whd/src/include/whd_events_int.h:288` |
| 11 | `WLC_E_NAN_EVENT_STOP` | NAN stopped | `whd/src/include/whd_events_int.h:291` `whd/src/include/whd_events_int.h:288` |
| 12 | `WLC_E_NAN_EVENT_P2P` | NAN P2P EVENT | `whd/src/include/whd_events_int.h:292` `whd/src/include/whd_events_int.h:288` |
| 13 | `WLC_E_NAN_EVENT_WINDOW_BEGIN_P2P` | begin of P2P further availability window | `whd/src/include/whd_events_int.h:295` `whd/src/include/whd_events_int.h:288` |
| 14 | `WLC_E_NAN_EVENT_WINDOW_BEGIN_MESH` | no comment in source | `whd/src/include/whd_events_int.h:296` `whd/src/include/whd_events_int.h:288` |
| 15 | `WLC_E_NAN_EVENT_WINDOW_BEGIN_IBSS` | no comment in source | `whd/src/include/whd_events_int.h:296` `whd/src/include/whd_events_int.h:288` |
| 16 | `WLC_E_NAN_EVENT_WINDOW_BEGIN_RANGING` | no comment of its own; shares a source line with value 17, whose trailing comment follows both | `whd/src/include/whd_events_int.h:297` `whd/src/include/whd_events_int.h:288` |
| 17 | `WLC_E_NAN_EVENT_POST_DISC` | Event for post discovery data (trailing comment on the line shared with value 16) | `whd/src/include/whd_events_int.h:297` `whd/src/include/whd_events_int.h:288` |
| 18 | `WLC_E_NAN_EVENT_DATA_IF_ADD` | Event for Data IF add | `whd/src/include/whd_events_int.h:298` `whd/src/include/whd_events_int.h:288` |
| 19 | `WLC_E_NAN_EVENT_DATA_PEER_ADD` | Event for peer add | `whd/src/include/whd_events_int.h:299` `whd/src/include/whd_events_int.h:288` |
| 20 | `WLC_E_NAN_EVENT_DATA_IND` | Data Indication to Host | `whd/src/include/whd_events_int.h:302` `whd/src/include/whd_events_int.h:288` |
| 21 | `WLC_E_NAN_EVENT_DATA_CONF` | Data Response to Host | `whd/src/include/whd_events_int.h:303` `whd/src/include/whd_events_int.h:288` |
| 22 | `WLC_E_NAN_EVENT_SDF_RX` | entire service discovery frame | `whd/src/include/whd_events_int.h:304` `whd/src/include/whd_events_int.h:288` |
| 23 | `WLC_E_NAN_EVENT_DATA_END` | no comment of its own; shares a source line with value 24, whose trailing comment follows both | `whd/src/include/whd_events_int.h:305` `whd/src/include/whd_events_int.h:288` |
| 24 | `WLC_E_NAN_EVENT_BCN_RX` | received beacon payload (trailing comment on the line shared with value 23) | `whd/src/include/whd_events_int.h:305` `whd/src/include/whd_events_int.h:288` |

A whd header comment above value 13 says not to use the "below four events" and to use `WL_NAN_EVENT_POST_DISC` instead; which four names it covers is not marked. `whd/src/include/whd_events_int.h:294-297`

### Second NAN enum, `whd_nan_events_t` (whd only)

A separate whd enum. No reference to these names found in whd/src/*.c, and the header does not say which field carries them. `whd/src/include/whd_events_int.h:374-383`

| Value | whd | Meaning (driver comment, shortened) | Citations |
|---|---|---|---|
| 1 (unverified) | `WLC_E_NAN_EVENT_START` | NAN cluster started | `whd/src/include/whd_events_int.h:376` `whd/src/include/whd_events_int.h:374-383` |
| 2 (unverified) | `WLC_E_NAN_EVENT_JOIN` | Joined to a NAN cluster | `whd/src/include/whd_events_int.h:377` `whd/src/include/whd_events_int.h:374-383` |
| 3 (unverified) | `WLC_E_NAN_EVENT_ROLE` | Role or State changed | `whd/src/include/whd_events_int.h:378` `whd/src/include/whd_events_int.h:374-383` |
| 4 (unverified) | `WLC_E_NAN_EVENT_SCAN_COMPLETE` | no comment in source | `whd/src/include/whd_events_int.h:379` `whd/src/include/whd_events_int.h:374-383` |
| 5 (unverified) | `WLC_E_NAN_EVENT_DISCOVERY_RESULT` | no comment in source | `whd/src/include/whd_events_int.h:379` `whd/src/include/whd_events_int.h:374-383` |
| 6 (unverified) | `WLC_E_NAN_EVENT_REPLIED` | no comment in source | `whd/src/include/whd_events_int.h:379` `whd/src/include/whd_events_int.h:374-383` |
| 7 (unverified) | `WLC_E_NAN_EVENT_TERMINATED` | source comment: the ev data will carry the instance ID | `whd/src/include/whd_events_int.h:380` `whd/src/include/whd_events_int.h:374-383` |
| 8 (unverified) | `WLC_E_NAN_EVENT_RECEIVE` | no comment in source | `whd/src/include/whd_events_int.h:381` `whd/src/include/whd_events_int.h:374-383` |

Rows marked (unverified):

- values 1, 2, 3, 4, 5, 6, 7, 8: defined in one header, never used, carrier field not stated. No reference in whd/src/*.c. Which field carries these values is not stated in these sources. `whd/src/include/whd_events_int.h:376` `whd/src/include/whd_events_int.h:377` `whd/src/include/whd_events_int.h:378` `whd/src/include/whd_events_int.h:379` `whd/src/include/whd_events_int.h:380` `whd/src/include/whd_events_int.h:381`

### Reason byte inside WLC_E_ICMP_ECHO_REQ event data (whd only)

For event `WLC_E_ICMP_ECHO_REQ` whd casts the `reason` byte of the event data (`wl_icmp_echo_req_event_t`) to this enum. It is not the header reason field. `whd/src/whd_wifi_api.c:7160-7162` `whd/src/include/whd_events_int.h:532-543`

The public enum `IcmpEchoReq_event_reason_e` has implicit values (0, 1, 2). The internal header gives the same three numbers explicitly as `WLC_E_REASON_ICMP_ECHO_REQ_*`; those defines are not referenced in whd/src/*.c. `whd/src/include/whd_events_int.h:524-527`

| Value | whd | Meaning (driver comment, shortened) | Citations |
|---|---|---|---|
| 0 | `WHD_E_REASON_ICMP_ECHO_REQ_SUCCESS` / `WLC_E_REASON_ICMP_ECHO_REQ_SUCCESS` | no comment in source | `whd/inc/whd_types.h:1588` `whd/src/include/whd_events_int.h:525` `whd/src/whd_wifi_api.c:7160-7162` |
| 1 | `WHD_E_REASON_ICMP_ECHO_REQ_TIMEOUT` / `WLC_E_REASON_ICMP_ECHO_REQ_TIMEOUT` | no comment in source | `whd/inc/whd_types.h:1589` `whd/src/include/whd_events_int.h:526` `whd/src/whd_wifi_api.c:7160-7162` |
| 2 | `WHD_E_REASON_ICMP_ECHO_REQ_DISASSOC` / `WLC_E_REASON_ICMP_ECHO_REQ_DISASSOC` | no comment in source | `whd/inc/whd_types.h:1590` `whd/src/include/whd_events_int.h:527` `whd/src/whd_wifi_api.c:7160-7162` |

### Enum-width sentinel
| Value | whd | Meaning (driver comment, shortened) | Citations |
|---|---|---|---|
| 2147483646 (0x7ffffffe) | `WLC_E_REASON_FORCE_32_BIT` | source comment: makes sure a 32 bit variable is what holds the enum | `whd/src/include/whd_events_int.h:371` |

Where the drivers use these values:

| Value | Use | Citation |
|---|---|---|
| 2147483646 | whd: forces the enum to 32 bits; not a code | `whd/src/include/whd_events_int.h:371` |
| 2147483646 | whd: whd_reason_to_string has 'case DOT11_RC_MAX:' and 'case WLC_E_REASON_FORCE_32_BIT:' labels that fall into default and return "Unknown" | `whd/src/whd_utils.c:509-512` |

## Event flags

### Event header `flags` (16-bit bit mask)

whd and c-driver read the field as 16 bits, big-endian (`ntoh16`, `cyw43_be16toh`). `whd/src/whd_cdc_bdc.c:843` `c-driver/cyw43_ll.c:738`

| Value | linux | whd | Meaning (driver comment, shortened) | Citations |
|---|---|---|---|---|
| 1 (0x1) | `BRCMF_EVENT_MSG_LINK` | `WLC_EVENT_MSG_LINK` | link is up | `linux/brcmfmac/fweh.h:113` `whd/src/whd_sdpcm.c:54` `whd/src/whd_ap.c:44` `whd/src/whd_wifi_api.c:58` |
| 2 (0x2) | `BRCMF_EVENT_MSG_FLUSHTXQ` | `WLC_EVENT_MSG_FLUSHTXQ` | flush tx queue on MIC error | `linux/brcmfmac/fweh.h:114` `whd/src/whd_sdpcm.c:55` |
| 4 (0x4) | `BRCMF_EVENT_MSG_GROUP` | `WLC_EVENT_MSG_GROUP` | group MIC error | `linux/brcmfmac/fweh.h:115` `whd/src/whd_sdpcm.c:56` |
| 8 (0x8) | — | `WLC_EVENT_MSG_UNKBSS` | unknown source bsscfg | `whd/src/whd_sdpcm.c:57` |
| 16 (0x10) | — | `WLC_EVENT_MSG_UNKIF` | unknown source OS i/f | `whd/src/whd_sdpcm.c:58` |

Where the drivers use these values:

| Value | Use | Citation |
|---|---|---|
| 1 | linux: a LINK event with this bit clear counts as link-down (brcmf_is_linkdown) | `linux/brcmfmac/cfg80211.c:6282` |
| 1 | linux: only used to print 'up'/'down' when LINK arrives with status NO_NETWORKS | `linux/brcmfmac/cfg80211.c:6297-6299` |
| 1 | linux: LINK with the whole flags word zero (tests !e->flags, not the bit) deletes the peer | `linux/brcmfmac/cfg80211.c:6792` |
| 1 | whd: join handler sets JOIN_LINK_READY on LINK when the bit is set, clears it otherwise | `whd/src/whd_wifi_api.c:1423` |
| 1 | c-driver: no named constant; on LINK with status 0 tests the literal 'ev->flags & 1' for link up / link down | `c-driver/cyw43_ctrl.c:390-401` |
| 1 | embassy: no named constant; matches LINK with status SUCCESS and the whole flags word == 0 as link down | `embassy/runner.rs:1245-1249` |
| 2 | whd: defined only; no reference to this name found in whd/src/*.c beyond the definition | `whd/src/whd_sdpcm.c:54-58` |
| 2 | linux: defined only; no use of BRCMF_EVENT_MSG_FLUSHTXQ found under linux/ | `linux/brcmfmac/fweh.h:114` |
| 4 | linux: on the MIC-error handler, bit set -> NL80211_KEYTYPE_GROUP, clear -> PAIRWISE | `linux/brcmfmac/cfg80211.c:6875-6878` |
| 8 | whd: defined only; no reference to this name found in whd/src/*.c beyond the definition | `whd/src/whd_sdpcm.c:54-58` |
| 16 | whd: defined only; no reference to this name found in whd/src/*.c beyond the definition | `whd/src/whd_sdpcm.c:54-58` |

### Event header `auth_type`

No driver in these sources defines a table for the event field. The names below are the `WL_AUTH_*` constants of the `auth` setting; mapping them onto the event field is (inferred), and every row is (unverified) for that reason. whd defines `WL_AUTH_*` for the `auth` setting (`whd/src/whd_wifi_api.c:1915-1919` picks `WL_AUTH_SAE` or `WL_AUTH_OPEN_SYSTEM`). `whd/src/include/whd_wlioctl.h:4273-4276`

No driver compares the event `auth_type` field with a named constant: linux only converts it with `be32_to_cpu` into its own event struct, whd only byte-swaps it, embassy tests the literal 3. `linux/brcmfmac/fweh.c:293` `whd/src/whd_cdc_bdc.c:847` `whd/src/whd_msgbuf_txrx.c:804` `embassy/runner.rs:1242-1253`

| Value | linux | whd | Meaning (driver comment, shortened) | Citations |
|---|---|---|---|---|
| 0 (unverified) | — | `WL_AUTH_OPEN_SYSTEM` | d11 open authentication | `whd/src/include/whd_wlioctl.h:4273` `whd/src/include_helium/whd_wlioctl.h:4440` `whd/src/include/whd_wlioctl.h:4273-4276` |
| 1 (unverified) | `WL_AUTH_SHARED_KEY` | `WL_AUTH_SHARED_KEY` | d11 shared authentication | `linux/brcmfmac/cfg80211.h:55` `whd/src/include/whd_wlioctl.h:4274` `whd/src/include_helium/whd_wlioctl.h:4441` `whd/src/include/whd_wlioctl.h:4273-4276` |
| 2 (unverified) | — | `WL_AUTH_OPEN_SHARED` | source comment: open is attempted first; shared follows if open fails with rc 13 | `whd/src/include/whd_wlioctl.h:4275` `whd/src/include_helium/whd_wlioctl.h:4442` `whd/src/include/whd_wlioctl.h:4273-4276` |
| 3 (unverified) | — | `WL_AUTH_SAE` | Simultaneous Authentication of Equals (SAE) | `whd/src/include/whd_wlioctl.h:4276` `whd/src/include_helium/whd_wlioctl.h:4443` `whd/src/include/whd_wlioctl.h:4273-4276` |

Where the drivers use these values:

| Value | Use | Citation |
|---|---|---|
| 0 | whd: field comment is 'WLC_E_AUTH: 802.11 AUTH request'; embassy's is 'WLC_E_AUTH' (`embassy/structs.rs:260-261`); c-driver's event struct does not name the field at all (`c-driver/cyw43_ll.h:237-245`, inside _1[30]) | `whd/inc/whd_events.h:167` |
| 1 | linux: WL_AUTH_SHARED_KEY is a value written for shared-key auth, not read from an event; linux converts the event auth_type with be32_to_cpu into its own event struct (`linux/brcmfmac/fweh.c:293`) and no handler reads it | `linux/brcmfmac/cfg80211.c:2344-2346` |
| 3 | embassy: the only reader of the event auth_type found: AUTH + FAIL + reason 16 + literal auth_type 3 ('specific for WPA3 networks') | `embassy/runner.rs:1242-1253` |

Rows marked (unverified):

- values 0, 1, 2, 3: names come from a different field's constants; only embassy reads the event field (literal 3). That the event auth_type field uses the WL_AUTH_* number space is not stated in any of these sources; no driver compares the event field with a named constant (linux only converts it with be32_to_cpu at `linux/brcmfmac/fweh.c:293`, whd only byte-swaps it at `whd/src/whd_cdc_bdc.c:847` and `whd/src/whd_msgbuf_txrx.c:804`). `whd/src/include/whd_wlioctl.h:4273` `whd/src/include_helium/whd_wlioctl.h:4440` `linux/brcmfmac/cfg80211.h:55` `whd/src/include/whd_wlioctl.h:4274` `whd/src/include_helium/whd_wlioctl.h:4441` `whd/src/include/whd_wlioctl.h:4275` `whd/src/include_helium/whd_wlioctl.h:4442` `whd/src/include/whd_wlioctl.h:4276` `whd/src/include_helium/whd_wlioctl.h:4443`

### IF event data: `action` byte (linux only)

The byte is in `struct brcmf_if_event`. `linux/brcmfmac/fweh.h:279-285`

`brcmf_notify_vif_event` switches on `ifevent->action` and wakes the waiter in `brcmf_cfg80211_wait_vif_event` (callers e.g. `linux/brcmfmac/cfg80211.c:855`, `linux/brcmfmac/cfg80211.c:1283`, `linux/brcmfmac/p2p.c:2110`, `linux/brcmfmac/p2p.c:2218`); the `cfg80211.c` line cited in each row is that action's case. `linux/brcmfmac/cfg80211.c:6946` `linux/brcmfmac/cfg80211.c:6964` `linux/brcmfmac/cfg80211.c:6971`

| Value | linux | Meaning (driver comment, shortened) | Citations |
|---|---|---|---|
| 1 | `BRCMF_E_IF_ADD` | no comment in source | `linux/brcmfmac/fweh.h:185` `linux/brcmfmac/cfg80211.c:6946` |
| 2 | `BRCMF_E_IF_DEL` | no comment in source | `linux/brcmfmac/fweh.h:186` `linux/brcmfmac/cfg80211.c:6964` |
| 3 | `BRCMF_E_IF_CHANGE` | no comment in source | `linux/brcmfmac/fweh.h:187` `linux/brcmfmac/cfg80211.c:6971` |

Where the drivers use these values:

| Value | Use | Citation |
|---|---|---|
| 1 | linux: IF event data action ADD -> create the interface | `linux/brcmfmac/fweh.c:164` |
| 2 | linux: IF event data action DEL -> remove the interface | `linux/brcmfmac/fweh.c:184` |
| 3 | linux: IF event data action CHANGE -> reset tx queues / fws | `linux/brcmfmac/fweh.c:178` |

### IF event data: `flags` byte (linux only)
| Value | linux | Meaning (driver comment, shortened) | Citations |
|---|---|---|---|
| 1 (0x1) | `BRCMF_E_IF_FLAG_NOIF` | no comment in source | `linux/brcmfmac/fweh.h:190` |

Where the drivers use these values:

| Value | Use | Citation |
|---|---|---|
| 1 | linux: NOIF set and not a p2p device -> event ignored ('no interface needed') | `linux/brcmfmac/fweh.c:144-148` |

### IF event data: `role` byte (linux only)
| Value | linux | Meaning (driver comment, shortened) | Citations |
|---|---|---|---|
| 0 | `BRCMF_E_IF_ROLE_STA` | no comment in source | `linux/brcmfmac/fweh.h:193` |
| 1 | `BRCMF_E_IF_ROLE_AP` | no comment in source | `linux/brcmfmac/fweh.h:194` |
| 2 | `BRCMF_E_IF_ROLE_WDS` | no comment in source | `linux/brcmfmac/fweh.h:195` |
| 3 | `BRCMF_E_IF_ROLE_P2P_GO` | no comment in source | `linux/brcmfmac/fweh.h:196` |
| 4 | `BRCMF_E_IF_ROLE_P2P_CLIENT` | no comment in source | `linux/brcmfmac/fweh.h:197` |

Where the drivers use these values:

| Value | Use | Citation |
|---|---|---|
| 0 | linux: role STA together with NOIF and p2pdev setup in progress = p2p device interface | `linux/brcmfmac/fweh.c:144-147` |
| 1 | linux: defined only; no use found under linux/ | `linux/brcmfmac/fweh.h:194` |
| 2 | linux: defined only; no use found under linux/ | `linux/brcmfmac/fweh.h:195` |
| 3 | linux: defined only; no use found under linux/ | `linux/brcmfmac/fweh.h:196` |
| 4 | linux: role P2P_CLIENT with NOIF = p2p device interface | `linux/brcmfmac/fweh.c:144-145` |

### WLC_E_ULP event data: `ulp_dongle_action` (whd only)

whd defines these under the header comment "WLC_E_ULP event data", next to `struct wl_ulp_event { uint16_t version; uint16_t ulp_dongle_action; }`. Pairing them with the `ulp_dongle_action` field is by name and position (inferred); the header does not say so. `whd/src/include/whd_wlioctl.h:4141-4151`

Defined only. No file under whd/src or whd/inc references `WL_ULP_*`, `wl_ulp_event_t` or `ulp_dongle_action` outside the two `whd_wlioctl.h` copies. The only mention of `WLC_E_ULP` in code is an unhandled case label in the join handler. `WL_ULP_EVENT_VERSION` (1) in the same block is a structure version, not an action code. Not found in linux, c-driver or embassy. `whd/src/include/whd_wlioctl.h:4141-4151` `whd/src/whd_wifi_api.c:1611` `whd/src/include/whd_wlioctl.h:4142`

| Value | whd | Meaning (driver comment, shortened) | Citations |
|---|---|---|---|
| 1 (unverified) | `WL_ULP_DISABLE_CONSOLE` | Disable console message on ULP entry | `whd/src/include/whd_wlioctl.h:4143` `whd/src/include_helium/whd_wlioctl.h:4310` `whd/src/include/whd_wlioctl.h:4141-4151` |
| 2 (unverified) | `WL_ULP_UCODE_DOWNLOAD` | Download ULP ucode file | `whd/src/include/whd_wlioctl.h:4144` `whd/src/include_helium/whd_wlioctl.h:4311` `whd/src/include/whd_wlioctl.h:4141-4151` |
| 3 (unverified) | `WL_ULP_ENTRY` | inform ulp entry to Host during warmboot | `whd/src/include/whd_wlioctl.h:4145` `whd/src/include_helium/whd_wlioctl.h:4312` `whd/src/include/whd_wlioctl.h:4141-4151` |

Rows marked (unverified):

- values 1, 2, 3: defined in one driver, never used, carrier field inferred from name and position. The link to the ulp_dongle_action field is (inferred). `whd/src/include/whd_wlioctl.h:4143` `whd/src/include_helium/whd_wlioctl.h:4310` `whd/src/include/whd_wlioctl.h:4144` `whd/src/include_helium/whd_wlioctl.h:4311` `whd/src/include/whd_wlioctl.h:4145` `whd/src/include_helium/whd_wlioctl.h:4312`

## Supplicant / prune codes

### Supplicant state: `status` when the event is PSK_SUP

"Value" is the number as linux and c-driver define it and as whd receives it. For event PSK_SUP whd adds `WLC_SUP_STATUS_OFFSET` (256) to the received status before dispatch, so whd's own names and handlers use value+256. The msgbuf path has the same code. `whd/src/whd_cdc_bdc.c:867-870` `whd/src/whd_msgbuf_txrx.c:825`

| Value | whd value after offset | linux | whd | c-driver | Meaning (driver comment, shortened) | Citations |
|---|---|---|---|---|---|---|
| 0 | 256 | — | `WLC_SUP_DISCONNECTED` | `CYW43_SUP_DISCONNECTED` | Disconnected | `c-driver/cyw43_ll.h:82` `whd/src/include/whd_events_int.h:224` `whd/inc/whd_events.h:108` `whd/src/whd_cdc_bdc.c:867-870` |
| 1 | 257 | — | `WLC_SUP_CONNECTING` | `CYW43_SUP_CONNECTING` | Connecting | `c-driver/cyw43_ll.h:83` `whd/src/include/whd_events_int.h:224` `whd/inc/whd_events.h:109` `whd/src/whd_cdc_bdc.c:867-870` |
| 2 | 258 | — | `WLC_SUP_IDREQUIRED` | `CYW43_SUP_IDREQUIRED` | ID Required | `c-driver/cyw43_ll.h:84` `whd/src/include/whd_events_int.h:225` `whd/inc/whd_events.h:110` `whd/src/whd_cdc_bdc.c:867-870` |
| 3 | 259 | — | `WLC_SUP_AUTHENTICATING` | `CYW43_SUP_AUTHENTICATING` | Authenticating | `c-driver/cyw43_ll.h:85` `whd/src/include/whd_events_int.h:225` `whd/inc/whd_events.h:111` `whd/src/whd_cdc_bdc.c:867-870` |
| 4 | 260 | `BRCMF_E_STATUS_FWSUP_WAIT_M1` | `WLC_SUP_AUTHENTICATED` / `WLC_SUP_KEYXCHANGE_WAIT_M1` | `CYW43_SUP_AUTHENTICATED` / `CYW43_SUP_KEYXCHANGE_WAIT_M1` | Authenticated; the alias name: Waiting to receive handshake msg M1 (same comments in whd and c-driver) | `linux/brcmfmac/fweh.h:136` `c-driver/cyw43_ll.h:86` `c-driver/cyw43_ll.h:91` `whd/src/include/whd_events_int.h:226` `whd/src/include/whd_events_int.h:230` `whd/inc/whd_events.h:112` `whd/inc/whd_events.h:117` `whd/src/whd_cdc_bdc.c:867-870` |
| 5 | 261 | `BRCMF_E_STATUS_FWSUP_PREP_M2` | `WLC_SUP_KEYXCHANGE` / `WLC_SUP_KEYXCHANGE_PREP_M2` | `CYW43_SUP_KEYXCHANGE` / `CYW43_SUP_KEYXCHANGE_PREP_M2` | Key Exchange; the alias name: Preparing to send handshake msg M2 (same comments in whd and c-driver) | `linux/brcmfmac/fweh.h:137` `c-driver/cyw43_ll.h:87` `c-driver/cyw43_ll.h:92` `whd/src/include/whd_events_int.h:226` `whd/src/include/whd_events_int.h:231` `whd/inc/whd_events.h:113` `whd/inc/whd_events.h:118` `whd/src/whd_cdc_bdc.c:867-870` |
| 6 | 262 | `BRCMF_E_STATUS_FWSUP_COMPLETED` | `WLC_SUP_KEYED` | `CYW43_SUP_KEYED` | Key Exchanged | `linux/brcmfmac/fweh.h:138` `c-driver/cyw43_ll.h:88` `whd/src/include/whd_events_int.h:227` `whd/inc/whd_events.h:114` `whd/src/whd_cdc_bdc.c:867-870` |
| 7 | 263 | `BRCMF_E_STATUS_FWSUP_TIMEOUT` | `WLC_SUP_TIMEOUT` | `CYW43_SUP_TIMEOUT` | Timeout | `linux/brcmfmac/fweh.h:139` `c-driver/cyw43_ll.h:89` `whd/src/include/whd_events_int.h:227` `whd/inc/whd_events.h:115` `whd/src/whd_cdc_bdc.c:867-870` |
| 8 | 264 | `BRCMF_E_STATUS_FWSUP_WAIT_M3` | `WLC_SUP_LAST_BASIC_STATE` / `WLC_SUP_KEYXCHANGE_WAIT_M3` | `CYW43_SUP_LAST_BASIC_STATE` / `CYW43_SUP_KEYXCHANGE_WAIT_M3` | Last Basic State; the alias name: Waiting to receive handshake msg M3 (same comments in whd and c-driver) | `linux/brcmfmac/fweh.h:140` `c-driver/cyw43_ll.h:90` `c-driver/cyw43_ll.h:93` `whd/src/include/whd_events_int.h:228` `whd/src/include/whd_events_int.h:232` `whd/inc/whd_events.h:116` `whd/inc/whd_events.h:119` `whd/src/whd_cdc_bdc.c:867-870` |
| 9 | 265 | `BRCMF_E_STATUS_FWSUP_PREP_M4` | `WLC_SUP_KEYXCHANGE_PREP_M4` | `CYW43_SUP_KEYXCHANGE_PREP_M4` | Preparing to send handshake msg M4 | `linux/brcmfmac/fweh.h:141` `c-driver/cyw43_ll.h:94` `whd/src/include/whd_events_int.h:233` `whd/inc/whd_events.h:120` `whd/src/whd_cdc_bdc.c:867-870` |
| 10 | 266 | `BRCMF_E_STATUS_FWSUP_WAIT_G1` | `WLC_SUP_KEYXCHANGE_WAIT_G1` | `CYW43_SUP_KEYXCHANGE_WAIT_G1` | Waiting to receive handshake msg G1 | `linux/brcmfmac/fweh.h:142` `c-driver/cyw43_ll.h:95` `whd/src/include/whd_events_int.h:234` `whd/inc/whd_events.h:121` `whd/src/whd_cdc_bdc.c:867-870` |
| 11 | 267 | `BRCMF_E_STATUS_FWSUP_PREP_G2` | `WLC_SUP_KEYXCHANGE_PREP_G2` | `CYW43_SUP_KEYXCHANGE_PREP_G2` | Preparing to send handshake msg G2 | `linux/brcmfmac/fweh.h:143` `c-driver/cyw43_ll.h:96` `whd/src/include/whd_events_int.h:235` `whd/inc/whd_events.h:122` `whd/src/whd_cdc_bdc.c:867-870` |

Where the drivers use these values:

| Value | Use | Citation |
|---|---|---|
| 0 | c-driver: the CYW43_SUP_* block is captioned 'Values used for STA and AP auth settings'; no CYW43_SUP_* name is referenced in c-driver/*.c (the handler uses literals) | `c-driver/cyw43_ll.h:81` |
| 0 | whd: the public header describes WLC_SUP_STATUS_OFFSET as an offset added to status codes so that they agree with the firmware's values, while the receive path's comment says the offset is needed because those who defined the event statuses and the reasons gave them overlapping values, and the code adds the offset to the received status (`whd/src/whd_cdc_bdc.c:866-870`). The two whd comments read differently; the code is what adds 256 on receive | `whd/inc/whd_events.h:80` |
| 4 | whd: PSK_SUP + KEYXCHANGE_WAIT_M1 with reason WPA_PSK_TMO -> JOIN_EAPOL_KEY_M1_TIMEOUT | `whd/src/whd_wifi_api.c:1373-1378` |
| 4 | c-driver: PSK_SUP with literal status 4, 8 or 10 and reason 15 -> 'Timeout waiting for key exchange M1/M3/G1', rejoin | `c-driver/cyw43_ctrl.c:406-410` |
| 4 | embassy: PSK_SUP with literal status 4 and reason 0 is ignored during join ('waiting for M1, not the generic ABORT status') | `embassy/control.rs:485-487` |
| 6 | linux: PSK_SUP + FWSUP_COMPLETED with firmware supplicant (PSK or SAE profile) sets EAP_SUCCESS | `linux/brcmfmac/cfg80211.c:6250-6254` |
| 6 | linux: PSK_SUP with any other status is treated as a failed connection ('failed supplicant state') | `linux/brcmfmac/cfg80211.c:6308-6309` |
| 6 | whd: PSK_SUP + WLC_SUP_KEYED (262 after offset) = successful key exchange, sets JOIN_SECURITY_COMPLETE; any other PSK_SUP status ends the join attempt. Both only when JOIN_LINK_READY is already set; otherwise whd ignores the PSK_SUP event | `whd/src/whd_wifi_api.c:1360-1372` |
| 6 | whd: event-info string helper prints 'WLC_SUP_KEYED' for the literal 262 | `whd/src/whd_utils.c:1119-1121` |
| 6 | c-driver: PSK_SUP with literal status 6 (comment: WLC_SUP_KEYED) sets WIFI_JOIN_STATE_KEYED; CYW43_SUP_KEYED is defined but not used here | `c-driver/cyw43_ctrl.c:404-405` |
| 6 | embassy: PSK_SUP with status 6, spelled EStatus::UNSOLICITED, completes a secured join | `embassy/control.rs:488-489` |
| 6 | embassy: PSK_SUP status 6 with flags 0 and reason 0 sets key_exchange_ok (if auth_ok) | `embassy/runner.rs:1276-1278` |
| 7 | linux: named FWSUP_TIMEOUT; defined only | `linux/brcmfmac/fweh.h:139` |
| 8 | whd: PSK_SUP + KEYXCHANGE_WAIT_M3 with reason WPA_PSK_TMO -> JOIN_EAPOL_KEY_M3_TIMEOUT ('passphrase may be incorrect') | `whd/src/whd_wifi_api.c:1380-1385` |
| 8 | c-driver: see value 4 (literal 8 = M3 wait in the comment) | `c-driver/cyw43_ctrl.c:406-410` |
| 10 | whd: PSK_SUP + KEYXCHANGE_WAIT_G1 with reason WPA_PSK_TMO -> JOIN_EAPOL_KEY_G1_TIMEOUT | `whd/src/whd_wifi_api.c:1387-1392` |
| 10 | c-driver: see value 4 (literal 10 = G1 wait in the comment) | `c-driver/cyw43_ctrl.c:406-410` |

### Supplicant reason: `reason` when the event is PSK_SUP

"Value" is the number as linux and c-driver define it and as whd receives it. For event PSK_SUP whd adds `WLC_E_SUP_REASON_OFFSET` (512) to the received reason before dispatch (same in the msgbuf path), so whd's names equal value+512. `whd/src/whd_cdc_bdc.c:867-870` `whd/src/whd_msgbuf_txrx.c:826`

| Value | whd value after offset | linux | whd | c-driver | Meaning (driver comment, shortened) | Citations |
|---|---|---|---|---|---|---|
| 0 | 512 | `BRCMF_E_REASON_FWSUP_OTHER` | `WLC_E_SUP_OTHER` | `CYW43_REASON_SUP_OTHER` | Other reason | `linux/brcmfmac/fweh.h:165` `c-driver/cyw43_ll.h:131` `whd/src/include/whd_events_int.h:329` `whd/src/whd_cdc_bdc.c:867-870` |
| 1 | 513 | `BRCMF_E_REASON_FWSUP_DECRYPT_KEY_DATA` | `WLC_E_SUP_DECRYPT_KEY_DATA` | `CYW43_REASON_SUP_DECRYPT_KEY_DATA` | Decryption of key data failed | `linux/brcmfmac/fweh.h:166` `c-driver/cyw43_ll.h:132` `whd/src/include/whd_events_int.h:330` `whd/src/whd_cdc_bdc.c:867-870` |
| 2 | 514 | `BRCMF_E_REASON_FWSUP_BAD_UCAST_WEP128` | `WLC_E_SUP_BAD_UCAST_WEP128` | `CYW43_REASON_SUP_BAD_UCAST_WEP128` | Illegal use of ucast WEP128 | `linux/brcmfmac/fweh.h:167` `c-driver/cyw43_ll.h:133` `whd/src/include/whd_events_int.h:331` `whd/src/whd_cdc_bdc.c:867-870` |
| 3 | 515 | `BRCMF_E_REASON_FWSUP_BAD_UCAST_WEP40` | `WLC_E_SUP_BAD_UCAST_WEP40` | `CYW43_REASON_SUP_BAD_UCAST_WEP40` | Illegal use of ucast WEP40 | `linux/brcmfmac/fweh.h:168` `c-driver/cyw43_ll.h:134` `whd/src/include/whd_events_int.h:332` `whd/src/whd_cdc_bdc.c:867-870` |
| 4 | 516 | `BRCMF_E_REASON_FWSUP_UNSUP_KEY_LEN` | `WLC_E_SUP_UNSUP_KEY_LEN` | `CYW43_REASON_SUP_UNSUP_KEY_LEN` | Unsupported key length | `linux/brcmfmac/fweh.h:169` `c-driver/cyw43_ll.h:135` `whd/src/include/whd_events_int.h:333` `whd/src/whd_cdc_bdc.c:867-870` |
| 5 | 517 | `BRCMF_E_REASON_FWSUP_PW_KEY_CIPHER` | `WLC_E_SUP_PW_KEY_CIPHER` | `CYW43_REASON_SUP_PW_KEY_CIPHER` | Unicast cipher mismatch in pairwise key | `linux/brcmfmac/fweh.h:170` `c-driver/cyw43_ll.h:136` `whd/src/include/whd_events_int.h:334` `whd/src/whd_cdc_bdc.c:867-870` |
| 6 | 518 | `BRCMF_E_REASON_FWSUP_MSG3_TOO_MANY_IE` | `WLC_E_SUP_MSG3_TOO_MANY_IE` | `CYW43_REASON_SUP_MSG3_TOO_MANY_IE` | WPA IE contains > 1 RSN IE in key msg 3 | `linux/brcmfmac/fweh.h:171` `c-driver/cyw43_ll.h:137` `whd/src/include/whd_events_int.h:335` `whd/src/whd_cdc_bdc.c:867-870` |
| 7 | 519 | `BRCMF_E_REASON_FWSUP_MSG3_IE_MISMATCH` | `WLC_E_SUP_MSG3_IE_MISMATCH` | `CYW43_REASON_SUP_MSG3_IE_MISMATCH` | WPA IE mismatch in key message 3 | `linux/brcmfmac/fweh.h:172` `c-driver/cyw43_ll.h:138` `whd/src/include/whd_events_int.h:336` `whd/src/whd_cdc_bdc.c:867-870` |
| 8 | 520 | `BRCMF_E_REASON_FWSUP_NO_INSTALL_FLAG` | `WLC_E_SUP_NO_INSTALL_FLAG` | `CYW43_REASON_SUP_NO_INSTALL_FLAG` | INSTALL flag unset in 4-way msg | `linux/brcmfmac/fweh.h:173` `c-driver/cyw43_ll.h:139` `whd/src/include/whd_events_int.h:337` `whd/src/whd_cdc_bdc.c:867-870` |
| 9 | 521 | `BRCMF_E_REASON_FWSUP_MSG3_NO_GTK` | `WLC_E_SUP_MSG3_NO_GTK` | `CYW43_REASON_SUP_MSG3_NO_GTK` | encapsulated GTK missing from msg 3 | `linux/brcmfmac/fweh.h:174` `c-driver/cyw43_ll.h:140` `whd/src/include/whd_events_int.h:338` `whd/src/whd_cdc_bdc.c:867-870` |
| 10 | 522 | `BRCMF_E_REASON_FWSUP_GRP_KEY_CIPHER` | `WLC_E_SUP_GRP_KEY_CIPHER` | `CYW43_REASON_SUP_GRP_KEY_CIPHER` | Multicast cipher mismatch in group key | `linux/brcmfmac/fweh.h:175` `c-driver/cyw43_ll.h:141` `whd/src/include/whd_events_int.h:339` `whd/src/whd_cdc_bdc.c:867-870` |
| 11 | 523 | `BRCMF_E_REASON_FWSUP_GRP_MSG1_NO_GTK` | `WLC_E_SUP_GRP_MSG1_NO_GTK` | `CYW43_REASON_SUP_GRP_MSG1_NO_GTK` | encapsulated GTK missing from group msg 1 | `linux/brcmfmac/fweh.h:176` `c-driver/cyw43_ll.h:142` `whd/src/include/whd_events_int.h:340` `whd/src/whd_cdc_bdc.c:867-870` |
| 12 | 524 | `BRCMF_E_REASON_FWSUP_GTK_DECRYPT_FAIL` | `WLC_E_SUP_GTK_DECRYPT_FAIL` | `CYW43_REASON_SUP_GTK_DECRYPT_FAIL` | GTK decrypt failure | `linux/brcmfmac/fweh.h:177` `c-driver/cyw43_ll.h:143` `whd/src/include/whd_events_int.h:341` `whd/src/whd_cdc_bdc.c:867-870` |
| 13 | 525 | `BRCMF_E_REASON_FWSUP_SEND_FAIL` | `WLC_E_SUP_SEND_FAIL` | `CYW43_REASON_SUP_SEND_FAIL` | message send failure | `linux/brcmfmac/fweh.h:178` `c-driver/cyw43_ll.h:144` `whd/src/include/whd_events_int.h:342` `whd/src/whd_cdc_bdc.c:867-870` |
| 14 | 526 | `BRCMF_E_REASON_FWSUP_DEAUTH` | `WLC_E_SUP_DEAUTH` | `CYW43_REASON_SUP_DEAUTH` | received FC_DEAUTH | `linux/brcmfmac/fweh.h:179` `c-driver/cyw43_ll.h:145` `whd/src/include/whd_events_int.h:343` `whd/src/whd_cdc_bdc.c:867-870` |
| 15 | 527 | `BRCMF_E_REASON_FWSUP_WPA_PSK_TMO` | `WLC_E_SUP_WPA_PSK_TMO` | `CYW43_REASON_SUP_WPA_PSK_TMO` | WPA PSK 4-way handshake timeout | `linux/brcmfmac/fweh.h:180` `c-driver/cyw43_ll.h:146` `whd/src/include/whd_events_int.h:344` `whd/src/whd_cdc_bdc.c:867-870` |
| 16 | — | `BRCMF_E_REASON_FWSUP_WPA_PSK_M1_TMO` | — | — | no comment in source | `linux/brcmfmac/fweh.h:181` |
| 17 | — | `BRCMF_E_REASON_FWSUP_WPA_PSK_M3_TMO` | — | — | no comment in source | `linux/brcmfmac/fweh.h:182` |

Where the drivers use these values:

| Value | Use | Citation |
|---|---|---|
| 0 | whd: event-info string helper prints 'WLC_E_SUP_OTHER' for the literal 512 | `whd/src/whd_utils.c:1128-1130` |
| 0 | embassy: PSK_SUP status 4 is ignored only when reason is literal 0 | `embassy/control.rs:485-487` |
| 0 | embassy: key exchange success requires reason 0 | `embassy/runner.rs:1278` |
| 14 | embassy: PSK_SUP with literal reason 14 is ignored ('often sent when the device roams from one AP to another') | `embassy/runner.rs:1286-1287` |
| 15 | whd: PSK_SUP with reason WPA_PSK_TMO and status WAIT_M1 / WAIT_M3 / WAIT_G1 -> the three JOIN_EAPOL_KEY_*_TIMEOUT flags | `whd/src/whd_wifi_api.c:1373-1388` |
| 15 | c-driver: PSK_SUP with literal reason 15 and status 4/8/10 -> rejoin | `c-driver/cyw43_ctrl.c:406-410` |
| 15 | embassy: comment only - 'reason 15 is a handshake timeout' | `embassy/control.rs:486` |
| 16 | linux: defined only; whd and c-driver tables stop at 15 | `linux/brcmfmac/fweh.h:181` |
| 17 | linux: defined only; whd and c-driver tables stop at 15 | `linux/brcmfmac/fweh.h:182` |

### Prune reason: `reason` when the event is PRUNE

"Value" is the number as c-driver defines it and as whd receives it. For event PRUNE whd adds `WLC_E_PRUNE_REASON_OFFSET` (256) to the received reason before dispatch (same in the msgbuf path), so whd's names equal value+256. whd uses the names only in `whd_reason_to_string`. `whd/src/whd_cdc_bdc.c:872-874` `whd/src/whd_msgbuf_txrx.c:830` `whd/src/whd_utils.c:438-456`

| Value | whd value after offset | whd | c-driver | Meaning (driver comment, shortened) | Citations |
|---|---|---|---|---|---|
| 1 | 257 | `WLC_E_PRUNE_ENCR_MISMATCH` | `CYW43_REASON_PRUNE_ENCR_MISMATCH` | encryption mismatch | `c-driver/cyw43_ll.h:110` `whd/src/include/whd_events_int.h:308` `whd/src/whd_cdc_bdc.c:872-874` |
| 2 | 258 | `WLC_E_PRUNE_BCAST_BSSID` | `CYW43_REASON_PRUNE_BCAST_BSSID` | AP uses a broadcast BSSID | `c-driver/cyw43_ll.h:111` `whd/src/include/whd_events_int.h:309` `whd/src/whd_cdc_bdc.c:872-874` |
| 3 | 259 | `WLC_E_PRUNE_MAC_DENY` | `CYW43_REASON_PRUNE_MAC_DENY` | STA's MAC addr is in AP's MAC deny list | `c-driver/cyw43_ll.h:112` `whd/src/include/whd_events_int.h:310` `whd/src/whd_cdc_bdc.c:872-874` |
| 4 | 260 | `WLC_E_PRUNE_MAC_NA` | `CYW43_REASON_PRUNE_MAC_NA` | STA's MAC addr is not in AP's MAC allow list | `c-driver/cyw43_ll.h:113` `whd/src/include/whd_events_int.h:311` `whd/src/whd_cdc_bdc.c:872-874` |
| 5 | 261 | `WLC_E_PRUNE_REG_PASSV` | `CYW43_REASON_PRUNE_REG_PASSV` | AP not allowed due to regulatory restriction | `c-driver/cyw43_ll.h:114` `whd/src/include/whd_events_int.h:312` `whd/src/whd_cdc_bdc.c:872-874` |
| 6 | 262 | `WLC_E_PRUNE_SPCT_MGMT` | `CYW43_REASON_PRUNE_SPCT_MGMT` | AP does not support STA locale spectrum mgmt | `c-driver/cyw43_ll.h:115` `whd/src/include/whd_events_int.h:313` `whd/src/whd_cdc_bdc.c:872-874` |
| 7 | 263 | `WLC_E_PRUNE_RADAR` | `CYW43_REASON_PRUNE_RADAR` | AP is on a radar channel of STA locale | `c-driver/cyw43_ll.h:116` `whd/src/include/whd_events_int.h:314` `whd/src/whd_cdc_bdc.c:872-874` |
| 8 | 264 | `WLC_E_RSN_MISMATCH` | `CYW43_REASON_RSN_MISMATCH` | STA does not support AP's RSN | `c-driver/cyw43_ll.h:117` `whd/src/include/whd_events_int.h:315` `whd/src/whd_cdc_bdc.c:872-874` |
| 9 | 265 | `WLC_E_PRUNE_NO_COMMON_RATES` | `CYW43_REASON_PRUNE_NO_COMMON_RATES` | No rates in common with AP | `c-driver/cyw43_ll.h:118` `whd/src/include/whd_events_int.h:316` `whd/src/whd_cdc_bdc.c:872-874` |
| 10 | 266 | `WLC_E_PRUNE_BASIC_RATES` | `CYW43_REASON_PRUNE_BASIC_RATES` | STA does not support all basic rates of BSS | `c-driver/cyw43_ll.h:119` `whd/src/include/whd_events_int.h:317` `whd/src/whd_cdc_bdc.c:872-874` |
| 11 | 267 | `WLC_E_PRUNE_CCXFAST_PREVAP` | `CYW43_REASON_PRUNE_CCXFAST_PREVAP` | CCX FAST ROAM: prune previous AP | `c-driver/cyw43_ll.h:120` `whd/src/include/whd_events_int.h:318` `whd/src/whd_cdc_bdc.c:872-874` |
| 12 | 268 | `WLC_E_PRUNE_CIPHER_NA` | `CYW43_REASON_PRUNE_CIPHER_NA` | BSS's cipher not supported | `c-driver/cyw43_ll.h:121` `whd/src/include/whd_events_int.h:319` `whd/src/whd_cdc_bdc.c:872-874` |
| 13 | 269 | `WLC_E_PRUNE_KNOWN_STA` | `CYW43_REASON_PRUNE_KNOWN_STA` | AP is already known to us as a STA | `c-driver/cyw43_ll.h:122` `whd/src/include/whd_events_int.h:320` `whd/src/whd_cdc_bdc.c:872-874` |
| 14 | 270 | `WLC_E_PRUNE_CCXFAST_DROAM` | `CYW43_REASON_PRUNE_CCXFAST_DROAM` | CCX FAST ROAM: prune unqualified AP | `c-driver/cyw43_ll.h:123` `whd/src/include/whd_events_int.h:321` `whd/src/whd_cdc_bdc.c:872-874` |
| 15 | 271 | `WLC_E_PRUNE_WDS_PEER` | `CYW43_REASON_PRUNE_WDS_PEER` | AP is already known to us as a WDS peer | `c-driver/cyw43_ll.h:124` `whd/src/include/whd_events_int.h:322` `whd/src/whd_cdc_bdc.c:872-874` |
| 16 | 272 | `WLC_E_PRUNE_QBSS_LOAD` | `CYW43_REASON_PRUNE_QBSS_LOAD` | QBSS LOAD - AAC is too low | `c-driver/cyw43_ll.h:125` `whd/src/include/whd_events_int.h:323` `whd/src/whd_cdc_bdc.c:872-874` |
| 17 | 273 | `WLC_E_PRUNE_HOME_AP` | `CYW43_REASON_PRUNE_HOME_AP` | prune home AP | `c-driver/cyw43_ll.h:126` `whd/src/include/whd_events_int.h:324` `whd/src/whd_cdc_bdc.c:872-874` |
| 18 | 274 | `WLC_E_PRUNE_AP_BLOCKED` | `CYW43_REASON_PRUNE_AP_BLOCKED` | prune blocked AP | `c-driver/cyw43_ll.h:127` `whd/src/include/whd_events_int.h:325` `whd/src/whd_cdc_bdc.c:872-874` |
| 19 | 275 | `WLC_E_PRUNE_NO_DIAG_SUPPORT` | `CYW43_REASON_PRUNE_NO_DIAG_SUPPORT` | prune due to diagnostic mode not supported | `c-driver/cyw43_ll.h:128` `whd/src/include/whd_events_int.h:326` `whd/src/whd_cdc_bdc.c:872-874` |

Where the drivers use these values:

| Value | Use | Citation |
|---|---|---|
| 8 | c-driver: PRUNE with status 0 and literal reason 8 ('RSN mismatch') -> retry the join with WPA auth; CYW43_REASON_RSN_MISMATCH is defined but not used | `c-driver/cyw43_ctrl.c:348-353` |
