# Named variables

Every named variable ("iovar") any of the four drivers sends, alphabetically, merged across drivers.

### `2g_mrate`
| | |
|---|---|
| Used by | embassy, c-driver, whd; no `bsscfg:` prefix `embassy/control.rs:612` `c-driver/cyw43_ll.c:2446` `whd/src/whd_ap.c:522`. Not found in linux. |
| Direction | set (all three) `embassy/control.rs:612` `c-driver/cyw43_ll.c:2446` `whd/src/whd_ap.c:525` |
| Value | u32, 4 bytes, little-endian (embassy `to_le_bytes`, c-driver `cyw43_put_le32`, whd `htod32`); units of 500 kbit/s per the drivers' arithmetic `embassy/control.rs:612` `embassy/control.rs:702-704` `c-driver/cyw43_ll.c:2446` `c-driver/cyw43_ll.c:1538-1544` `whd/src/whd_ap.c:45` `whd/src/whd_ap.c:524` |
| Record | plain integer `embassy/control.rs:702-704` |

- embassy — set — 22 (11000000 / 500000) — in `start_ap`: multicast rate 11 Mbps instead of 1 Mbps — `embassy/control.rs:611-612` `embassy/control.rs:543`
- c-driver — set — 22, on `WWD_AP_INTERFACE` (1) — in `cyw43_ll_wifi_ap_init`: multicast tx rate 11 Mbps — `c-driver/cyw43_ll.c:2445-2446` `c-driver/cyw43_ll.c:152` `c-driver/cyw43_ll.c:2353`
- whd — set — `RATE_SETTING_11_MBPS` = 22, only when the chanspec is 2.4 GHz — in `whd_wifi_init_ap`: multicast rate 11 Mbps — `whd/src/whd_ap.c:519-525` `whd/src/whd_ap.c:45` `whd/src/include/whd_wlioctl.h:1121`

Differences: embassy sends on interface 0 `embassy/control.rs:726`; c-driver sends on the AP interface (1) `c-driver/cyw43_ll.c:2446`; whd sends on the `ifp` given to `whd_wifi_init_ap` `whd/src/whd_ap.c:525`.

Note (layout common to every named variable (iovar) in this chapter): all four drivers send name + NUL + payload as the data of command 263 (set) or 262 (get) `embassy/control.rs:713-728` `c-driver/cyw43_ll.c:1538-1544` `linux/brcmfmac/fwil.c:167-184` `whd/src/whd_cdc_bdc.c:211-230`. Sizes given in the entries of this chapter are payload sizes; they exclude the name and its NUL `embassy/control.rs:725`.

Note (embassy layout): set writes name bytes, one 0 byte, value bytes, with command `SetVar` = 263 on interface 0; `set_iovar` uses a 196-byte buffer `embassy/control.rs:713-728` `embassy/consts.rs:684`. A u32 set sends the value as 4 little-endian bytes `embassy/control.rs:702-704`; a u32 get reads 4 bytes, little-endian `embassy/control.rs:706-711`.

Note (c-driver layout): a u32 set writes name + NUL, then the u32 little-endian, with `WLC_SET_VAR` (263) and length strlen + 1 + 4; the interface is a parameter `c-driver/cyw43_ll.c:1538-1544` `c-driver/cyw43_ll.c:185`.

Note (linux layout): set sends name + NUL + data with `BRCMF_C_SET_VAR` (263) `linux/brcmfmac/fwil.c:167-184` `linux/brcmfmac/fwil.c:201-205` `linux/brcmfmac/fwil.h:81`. An integer set, `brcmf_fil_iovar_int_set`, sends one `__le32`, 4 bytes `linux/brcmfmac/fwil.h:122-128`. On get the request is name + NUL + the caller's buffer contents (same length as the reply buffer) with `BRCMF_C_GET_VAR` (262), and the reply is copied back from the start of the buffer `linux/brcmfmac/fwil.c:225-232` `linux/brcmfmac/fwil.h:80`.

Note (whd layout): on the CDC path the buffer is built as (64 − (strlen + 1)) % 4 zero bytes, then name + NUL, then the payload area; the pad aligns the payload in host memory `whd/src/whd_cdc_bdc.c:349-367`. When sending `WLC_SET_VAR` / `WLC_GET_VAR` the leading zero bytes are skipped and the rest moved to the front, so the buffer sent is name, NUL, payload `whd/src/whd_cdc_bdc.c:211-230`. Set maps to `WLC_SET_VAR` with `CDC_SET`, get to `WLC_GET_VAR` with `CDC_GET` `whd/src/whd_cdc_bdc.c:327-339`. On the msgbuf path the buffer is zeroed, name + NUL is at offset 0 and the payload follows, with no pad `whd/src/whd_msgbuf_txrx.c:202-226`. The interface index is placed in the CDC header flags (`bss_index << CDCF_IOC_IF_SHIFT`) `whd/src/whd_cdc_bdc.c:236-237`. The command-log reader skips the same leading zero bytes `whd/src/whd_chip.c:736-743`.

Note (pass-through functions that take the name as a parameter and add no prefix): linux `brcmf_iovar_data_set(dev, name, data, len)` sets the caller's buffer and length on interface `iflist[0]` `linux/brcmfmac/core.c:1552-1558`; its callers send `bus:txglom`, `bus:txglomalign`, `bus:rxglom` `linux/brcmfmac/sdio.c:3560` `linux/brcmfmac/sdio.c:3567` `linux/brcmfmac/sdio.c:3578`. whd has set and get functions of this kind `whd/src/whd_wifi_api.c:5143-5312`: `whd_wifi_get_iovar_value` requests 4 bytes and returns the first reply word through `dtoh32`, tolerating an "unsupported" result `whd/src/whd_wifi_api.c:5165-5183`; `whd_wifi_get_iovar_buffer_with_param` builds name + parameter bytes in the caller's output buffer and sends the whole `out_length` bytes as `WLC_GET_VAR` through the plain command buffer `whd/src/whd_wifi_api.c:5242-5272`. The other whd functions are described under the variables that use them: `ampdu_ba_wsize`, `arp_hostip`, `arp_hostip_clear`, `arp_ol`.

### `2g_rate`
| | |
|---|---|
| Used by | whd: defined as `IOVAR_STR_2G_RATE`, not used by whd `whd/src/include/whd_wlioctl.h:1122`. Not found in embassy, linux, c-driver. |
| Direction | not found in these sources |
| Value | not found in these sources |
| Record | not found in these sources |

### `a_rate`
| | |
|---|---|
| Used by | whd: defined as `IOVAR_STR_ARATE`, not used by whd `whd/src/include/whd_wlioctl.h:1118`. Not found in embassy, linux, c-driver. |
| Direction | not found in these sources |
| Value | not found in these sources |
| Record | not found in these sources |

### `actframe`
| | |
|---|---|
| Used by | linux with `bsscfg:` prefix when bsscfgidx != 0, bare name when 0 `linux/brcmfmac/p2p.c:1584-1585` `linux/brcmfmac/fwil.c:259-260`; whd without prefix `whd/src/whd_wifi_api.c:4340-4344`. Not found in embassy, c-driver. |
| Direction | set (both) `linux/brcmfmac/p2p.c:1584-1585` `whd/src/whd_wifi_api.c:4340-4344` |
| Value | linux: `struct brcmf_fil_af_params_le`, 1828 bytes (4 + 4 + 6 + 2 + 6 + 2 + 4 + 1800) (computed), little-endian fields, always the full record `linux/brcmfmac/fwil_types.h:229-242` `linux/brcmfmac/fwil_types.h:13` `linux/brcmfmac/p2p.c:1585`. whd: `whd_af_params_t` = `struct wl_af_params`, `sizeof` the record, host byte order, copied from the caller unchanged `whd/src/include/whd_wlioctl.h:60-74` `whd/src/include/whd_wlioctl.h:115` `whd/src/whd_wifi_api.c:4343`; 1068 bytes (4 + 4 + 6 + 2 padding + 6 + 2 + 4 + 1040) (computed) if the compiler aligns `action_frame` to 4 bytes (inferred; the struct has no packing attribute, and the header's first `#pragma pack` is at `whd/src/include/whd_wlioctl.h:3864`). |
| Record | linux `struct brcmf_fil_af_params_le` `linux/brcmfmac/fwil_types.h:236-242`; whd `struct wl_af_params` `whd/src/include/whd_wlioctl.h:68-74`, typedef `whd/inc/whd_types.h:142` |

- linux — record layout — offset 0 `channel` u32; 4 `dwell_time` u32; 8 `bssid` 6 bytes; 14 `pad` 2 bytes; 16 `action_frame`: 16 `da` 6 bytes, 22 `len` u16, 24 `packet_id` u32, 28 `data` 1800 bytes — `linux/brcmfmac/fwil_types.h:229-242` `linux/brcmfmac/fwil_types.h:13`
- whd — record layout — `channel` u32, `dwell_time` i32, `BSSID` 6 bytes, then `action_frame`: `da` 6 bytes, `len` u16, `packetId` u32, `data` 1040 bytes; no explicit pad field, so the 2 bytes after `BSSID` are compiler padding (inferred; same offsets as linux up to `data` if so) — `whd/src/include/whd_wlioctl.h:50-53` `whd/src/include/whd_wlioctl.h:60-74` `whd/src/include/whd_wlioctl.h:38`
- linux — set — full record through `brcmf_fil_bsscfg_data_set` — `brcmf_p2p_tx_action_frame`: transmit an action frame; called from the retry loop in `brcmf_p2p_send_action_frame`, which cfg80211 calls — `linux/brcmfmac/p2p.c:1571-1587` `linux/brcmfmac/p2p.c:1883` `linux/brcmfmac/cfg80211.c:5765`
- whd — set — full record — `whd_wifi_send_action_frame`: transmit an action frame; rejects `action_frame.len` > 1040 before sending — `whd/src/whd_wifi_api.c:4323-4344` `whd/src/include/whd_wlioctl.h:38` `whd/src/include/whd_wlioctl.h:1089`
- whd — the same string is also defined as `IOVAR_STR_ACTFRAME`; that macro is not used by whd — `whd/src/include/whd_wlioctl.h:1066`

Differences: linux sends 1828 bytes with a 1800-byte frame area `linux/brcmfmac/fwil_types.h:13`; whd sends the `sizeof` of a record with a 1040-byte frame area `whd/src/include/whd_wlioctl.h:38`. linux adds `bsscfg:` + u32 index on a non-zero bsscfgidx `linux/brcmfmac/fwil.c:262-289`; whd sends the bare name `whd/src/whd_wifi_api.c:4340-4341`. linux declares the fields little-endian `linux/brcmfmac/fwil_types.h:229-242`; whd copies the caller's record with no conversion `whd/src/whd_wifi_api.c:4343`.

Note (the `bsscfg:` prefix is a naming convention, not a variable; linux): a generic helper applies the prefix to any name when the interface's bsscfgidx is not 0, for set `linux/brcmfmac/fwil.c:294-320` and get `linux/brcmfmac/fwil.c:323-352` `linux/brcmfmac/fwil.c:248-291`. With bsscfgidx != 0 the data is `bsscfg:` (7 bytes, no NUL) + name + NUL + bsscfgidx as u32 little-endian (4 bytes) + payload `linux/brcmfmac/fwil.c:252` `linux/brcmfmac/fwil.c:262-289`. Set sends prefix, name, NUL, `__le32` index, payload with `BRCMF_C_SET_VAR` (263) `linux/brcmfmac/fwil.c:308-312` `linux/brcmfmac/fwil.h:81`; get sends the same layout with `BRCMF_C_GET_VAR` (262) and the reply is copied from the start of the buffer `linux/brcmfmac/fwil.c:333-339` `linux/brcmfmac/fwil.h:80`. With bsscfgidx == 0 no prefix and no index are sent; the buffer is name + NUL + payload `linux/brcmfmac/fwil.c:259-260` `linux/brcmfmac/fwil.c:167-184`. linux sends `actframe` and `actframe_abort` through this helper `linux/brcmfmac/p2p.c:1584-1585` `linux/brcmfmac/p2p.c:1313-1314`.

Note (the `bsscfg:` prefix in the other drivers): whd has no automatic prefix in its helpers; the interface index goes in the CDC header flags `whd/src/whd_cdc_bdc.c:236-237`, and where whd uses the prefix it is a literal at the call site, e.g. `whd/src/whd_ap.c:412`. embassy and c-driver have no prefixing helper; the prefix is written as part of literal names at the call site, e.g. `embassy/control.rs:378` `c-driver/cyw43_ll.c:2240`.

### `actframe_abort`
| | |
|---|---|
| Used by | linux, with `bsscfg:` prefix when bsscfgidx != 0, bare name when 0 `linux/brcmfmac/p2p.c:1313-1314` `linux/brcmfmac/fwil.c:259-260`. Not found in embassy, whd, c-driver. |
| Direction | set `linux/brcmfmac/p2p.c:1313-1314` |
| Value | s32, 4 bytes, host byte order (no `cpu_to_le32`), value 1 `linux/brcmfmac/p2p.c:1305` `linux/brcmfmac/p2p.c:1313-1314` |
| Record | plain integer `linux/brcmfmac/p2p.c:1305` |

- linux — set — 1 — `brcmf_p2p_abort_action_frame`: abort a pending action-frame transmit; uses the P2P device vif, else the primary vif — `linux/brcmfmac/p2p.c:1300-1316`

### `add`
| | |
|---|---|
| Used by | whd: defined as `IOVAR_STR_WOWL_PATTERN_ADD`, not used by whd `whd/src/include/whd_wlioctl.h:1179`. Not found as a variable name in embassy, linux, c-driver. |
| Direction | not found in these sources |
| Value | not found in these sources |
| Record | not found in these sources |

### `allmulti`
| | |
|---|---|
| Used by | embassy, linux; no `bsscfg:` prefix `embassy/runner.rs:1404` `linux/brcmfmac/core.c:191`. c-driver: only inside `#if 0` `c-driver/cyw43_ll.c:1978-1997`. whd: defined as `IOVAR_STR_ALLMULTI`, not used by whd `whd/src/include/whd_wlioctl.h:1072`. |
| Direction | set (embassy, linux, c-driver dead code) `embassy/runner.rs:1408` `linux/brcmfmac/core.c:191` `c-driver/cyw43_ll.c:1978-1997` |
| Value | u32, 4 bytes, little-endian, 0 or 1 `embassy/runner.rs:1407` `linux/brcmfmac/fwil.h:122-128` |
| Record | plain integer `embassy/runner.rs:1407` |

- embassy — set — 1 if the multicast address list overflowed, else 0 — receive all multicast when the addresses do not fit the list; sent only when the flag differs from the runner's cached value (initially false) — `embassy/runner.rs:1401-1410` `embassy/runner.rs:142`
- linux — set — 1 or 0 from `IFF_ALLMULTI`; forced to 1 when the preceding `mcast_list` set failed and the remaining address count is not 0 — `_brcmf_set_multicast_list`: all-multicast receive — `linux/brcmfmac/core.c:156` `linux/brcmfmac/core.c:178-182` `linux/brcmfmac/core.c:191`
- c-driver — set — the monitor-mode flag, with `WLC_SET_MONITOR` (108) — `cyw43_set_monitor_mode`; inside `#if 0`, not compiled — `c-driver/cyw43_ll.c:1978-1997`

### `ampdu_ba_wsize`
| | |
|---|---|
| Used by | embassy, c-driver, whd; no `bsscfg:` prefix `embassy/control.rs:296` `c-driver/cyw43_ll.c:2039` `whd/src/whd_ap.c:118`. Not found in linux. |
| Direction | set (all three) `embassy/control.rs:296` `c-driver/cyw43_ll.c:2039` `whd/src/whd_ap.c:118` |
| Value | u32, 4 bytes, little-endian (whd: `htod32`) `embassy/control.rs:702-704` `c-driver/cyw43_ll.c:1538-1544` `whd/src/whd_wifi_api.c:5153-5163` |
| Record | plain integer `embassy/control.rs:702-704` |

- embassy — set — 8 — in `init` — `embassy/control.rs:296`
- embassy — set — 8 — at the start of `join` — `embassy/control.rs:374` `embassy/control.rs:366`
- c-driver — set — 8, STA interface — in `cyw43_ll_wifi_on` — `c-driver/cyw43_ll.c:2039`
- c-driver — set — 8, STA interface — at the start of `cyw43_ll_wifi_join` — `c-driver/cyw43_ll.c:2212`
- c-driver — set — 2, STA interface — in `cyw43_ll_wifi_ap_init`: window size for the AP — `c-driver/cyw43_ll.c:2378-2379`
- whd — set — `ap_win_size`, or `sta_win_size` when the interface role is STA; nothing sent when the role is already AP — `whd_wifi_set_block_ack_window_size_common` — `whd/src/whd_ap.c:102-118` `whd/src/include/whd_wlioctl.h:1125`
- whd — set — `ba_window_size`; every call in `whd_wifi_set_ampdu_parameters` passes `AMPDU_STA_DEFAULT_BA_WSIZE` = 8 — `whd_wifi_set_ampdu_parameters_common` — `whd/src/whd_ap.c:128` `whd/src/whd_ap.c:47` `whd/src/whd_ap.c:149-163`
- whd — neither function has a caller in the whd `.c` files of these sources; only definitions and `extern` declarations exist — `whd/src/whd_ap.c:102` `whd/src/whd_ap.c:143` `whd/src/include/whd_ap.h:78` `whd/src/include/whd_ap.h:96`

Differences: c-driver writes 2 before starting an AP `c-driver/cyw43_ll.c:2379`; embassy sends only 8 `embassy/control.rs:296` `embassy/control.rs:374`.

Note (whd pass-through): `whd_wifi_set_iovar_value` takes the name as a parameter and sends one u32 through `htod32`, 4 bytes, with no prefix `whd/src/whd_wifi_api.c:5153-5163`.

### `ampdu_hostreorder`
| | |
|---|---|
| Used by | linux, whd; no `bsscfg:` prefix `linux/brcmfmac/fwsignal.c:2405` `whd/src/whd_management.c:618`. Not found in embassy, c-driver. |
| Direction | set (both) `linux/brcmfmac/fwsignal.c:2405` `whd/src/whd_management.c:618` |
| Value | u32, 4 bytes, little-endian (whd: `htod32`) `linux/brcmfmac/fwil.h:122-128` `whd/src/whd_wifi_api.c:5153-5163` |
| Record | plain integer `linux/brcmfmac/fwil.h:122-128` |

- linux — set — 1 — `brcmf_fws_attach`: host does AMPDU receive reordering; sent whether or not the preceding `tlv` set succeeded; failure only logged — `linux/brcmfmac/fwsignal.c:2399-2406`
- whd — set — 0 (`WHD_FALSE`) — `whd_wifi_on`: only for chip ids 55500, 55530, 55572, 55900 — `whd/src/whd_management.c:614-619` `whd/src/include/whd_wlioctl.h:1129`

Differences: linux writes 1 `linux/brcmfmac/fwsignal.c:2405`; whd writes 0 and only for the listed chip ids, which do not include 43439 `whd/src/whd_management.c:615-618`.

### `ampdu_mpdu`
| | |
|---|---|
| Used by | embassy, c-driver, whd; no `bsscfg:` prefix `embassy/control.rs:298` `c-driver/cyw43_ll.c:2040` `whd/src/whd_ap.c:131`. Not found in linux. |
| Direction | set (all three) `embassy/control.rs:298` `c-driver/cyw43_ll.c:2040` `whd/src/whd_ap.c:131` |
| Value | u32, 4 bytes, little-endian (whd: `htod32`) `embassy/control.rs:702-704` `c-driver/cyw43_ll.c:1538-1544` `whd/src/whd_wifi_api.c:5153-5163` |
| Record | plain integer `embassy/control.rs:702-704` |

- embassy — set — 4 — in `init` — `embassy/control.rs:298`
- c-driver — set — 4, STA interface — in `cyw43_ll_wifi_on` — `c-driver/cyw43_ll.c:2040`
- whd — set — `(uint32_t)ampdu_mpdu` from an `int8_t`: `AMPDU_STA_DEFAULT_MPDU` = 4 in the default branch; `AMPDU_MPDU_AUTO` = −1 for chip ids 43012, 0x4373, 43909, 43907, 54907 — `whd_wifi_set_ampdu_parameters_common`: MPDUs per AMPDU — `whd/src/whd_ap.c:125-131` `whd/src/whd_ap.c:48` `whd/src/whd_ap.c:149-163` `whd/src/include/whd_ap.h:39` `whd/src/include/whd_wlioctl.h:1126`
- whd — `whd_wifi_set_ampdu_parameters`, the only caller, has no caller in the whd `.c` files of these sources — `whd/src/whd_ap.c:143` `whd/src/include/whd_ap.h:96`
- whd — set — 16 — `whd_wifi_join_specific` after a join completes, only for chip id 0x4373 or 55560; macro `IOVAR_STR_MPDU_PER_AMPDU`, same string — `whd/src/whd_wifi_api.c:2409-2413` `whd/src/include/whd_wlioctl.h:1163`

### `ampdu_rx`
| | |
|---|---|
| Used by | whd: defined as `IOVAR_STR_AMPDU_RX`, not used by whd `whd/src/include/whd_wlioctl.h:1127`. Not found in embassy, linux, c-driver. |
| Direction | not found in these sources |
| Value | not found in these sources |
| Record | not found in these sources |

### `ampdu_rx_factor`
| | |
|---|---|
| Used by | c-driver, whd; no `bsscfg:` prefix `c-driver/cyw43_ll.c:2041` `whd/src/whd_ap.c:135`. embassy: only in a commented-out line `embassy/control.rs:300`. Not found in linux. |
| Direction | set (both) `c-driver/cyw43_ll.c:2041` `whd/src/whd_ap.c:135` |
| Value | u32, 4 bytes, little-endian (whd: `htod32`) `c-driver/cyw43_ll.c:1538-1544` `whd/src/whd_wifi_api.c:5153-5163` |
| Record | plain integer `c-driver/cyw43_ll.c:1538-1544` |

- c-driver — set — 0, STA interface — in `cyw43_ll_wifi_on` — `c-driver/cyw43_ll.c:2041`
- whd — set — `rx_factor`: `AMPDU_RX_FACTOR_8K` = 0 in the default branch, `AMPDU_RX_FACTOR_64K` = 3 for chip ids 43012 and 0x4373; not sent when the argument is `AMPDU_RX_FACTOR_INVALID` (0xff) — `whd_wifi_set_ampdu_parameters_common` — `whd/src/whd_ap.c:133-136` `whd/src/whd_ap.c:149-163` `whd/src/include/whd_ap.h:34-38` `whd/src/include/whd_wlioctl.h:1128`
- whd — value names: 0 = 8K, 1 = 16K, 2 = 32K, 3 = 64K maximum receive AMPDU length — `whd/src/include/whd_ap.h:34-37`
- whd — `whd_wifi_set_ampdu_parameters`, the only caller, has no caller in the whd `.c` files of these sources — `whd/src/whd_ap.c:143` `whd/src/include/whd_ap.h:96`
- embassy — not sent — the set of 0 in `init` is commented out with the remark "this crashes" — `embassy/control.rs:300`

Differences: c-driver sends 0 at wifi-on `c-driver/cyw43_ll.c:2041`; embassy has the same write disabled `embassy/control.rs:300`.

### `ampdu_tid`
| | |
|---|---|
| Used by | whd: defined as `IOVAR_STR_AMPDU_TID`, not used by whd `whd/src/include/whd_wlioctl.h:1070`. Not found in embassy, linux, c-driver. |
| Direction | not found in these sources |
| Value | not found in these sources |
| Record | not found in these sources |

### `ap_isolate`
| | |
|---|---|
| Used by | linux; no `bsscfg:` prefix `linux/brcmfmac/cfg80211.c:6119`. Not found in embassy, whd, c-driver. |
| Direction | set `linux/brcmfmac/cfg80211.c:6119` |
| Value | u32, 4 bytes, little-endian `linux/brcmfmac/fwil.h:122-128` |
| Record | plain integer `linux/brcmfmac/fwil.h:122-128` |

- linux — set — 0 or 1 from `params->ap_isolate`; nothing sent when that is negative — `brcmf_cfg80211_change_bss`: 1 restricts bridging of frames between associated stations — `linux/brcmfmac/cfg80211.c:6113-6121`

### `apsta`
| | |
|---|---|
| Used by | embassy, linux, whd, c-driver; no `bsscfg:` prefix `embassy/control.rs:271-272` `linux/brcmfmac/p2p.c:460-462` `whd/src/whd_management.c:481-494` `c-driver/cyw43_ll.c:1919` |
| Direction | set (all four) `embassy/control.rs:271-272` `linux/brcmfmac/p2p.c:460-462` `whd/src/whd_management.c:481-494` `c-driver/cyw43_ll.c:1919` |
| Value | u32, 4 bytes. Little-endian in embassy, c-driver, linux `embassy/control.rs:702-704` `c-driver/cyw43_ll.c:1538-1544` `linux/brcmfmac/fwil.h:122-128`. whd: `htod32` at init `whd/src/whd_management.c:488`, host order without conversion in the AP path (value 0) `whd/src/whd_ap.c:227`. |
| Record | plain integer `embassy/control.rs:702-704` |

- embassy — set — 1 — in `init`, after `bus:txglom` — `embassy/control.rs:271-272`
- embassy — set — 0 — in `start_ap`, after bringing the interface down — `embassy/control.rs:560-563`
- embassy — set — 1 — in `close_ap` — `embassy/control.rs:649-650` `embassy/control.rs:639`
- embassy — not sent — a second set of 1 later in `init` is commented out with the remark "this crashes" — `embassy/control.rs:294`
- c-driver — set — 1, STA interface — in `cyw43_ll_bus_init` — `c-driver/cyw43_ll.c:1919`
- c-driver — set — 1, STA interface — again in `cyw43_ll_wifi_on` — `c-driver/cyw43_ll.c:2038`
- linux — set — 0 — `brcmf_cfg80211_start_ap`, after `BRCMF_C_DOWN`; only for the AP role and when ifidx is 0 or neither the RSDB nor the MCHAN feature is enabled; return value ignored — `linux/brcmfmac/cfg80211.c:5354-5364`
- linux — set — 1 — `brcmf_p2p_set_firmware`, between `BRCMF_C_DOWN` and `BRCMF_C_UP`; return value ignored — `linux/brcmfmac/p2p.c:460-462`
- whd — set — 1 — `whd_wifi_on`; an "unsupported" result is tolerated — `whd/src/whd_management.c:481-494` `whd/src/include/whd_wlioctl.h:1071`
- whd — set — 0 — `whd_create_softap_interface`, only when the AP is created on the primary interface, between `WLC_DOWN` and `WLC_UP`; "unsupported" tolerated — `whd/src/whd_ap.c:221-235`

Differences: embassy writes 0 in every `start_ap` `embassy/control.rs:563`; whd writes 0 only when the AP is on the primary interface `whd/src/whd_ap.c:222-227`; linux writes 0 when ifidx is 0 or neither RSDB nor MCHAN is enabled `linux/brcmfmac/cfg80211.c:5354-5364`; c-driver has no write of 0 `c-driver/cyw43_ll.c:1919` `c-driver/cyw43_ll.c:2038`.

### `arp_hostip`
| | |
|---|---|
| Used by | linux, whd; no `bsscfg:` prefix `linux/brcmfmac/core.c:1050-1051` `whd/src/whd_wifi_api.c:5682`. Not found in embassy, c-driver. |
| Direction | both (both drivers) `linux/brcmfmac/core.c:1033-1034` `linux/brcmfmac/core.c:1050-1051` `whd/src/whd_wifi_api.c:5682` `whd/src/whd_wifi_api.c:5796` |
| Value | set: linux one IPv4 address, 4 bytes, network byte order (`__be32`) `linux/brcmfmac/core.c:1050-1051`; whd `count` × u32, `count` × 4 bytes, copied as given `whd/src/whd_wifi_api.c:5682`. get: 8 × u32 = 32 bytes in both `linux/brcmfmac/core.c:998` `linux/brcmfmac/core.c:1009` `linux/brcmfmac/core.c:1033-1034` `whd/src/whd_wifi_api.c:5777` `whd/src/whd_wifi_api.c:5796` `whd/src/include/whd_wlioctl.h:3608` |
| Record | plain array of IPv4 addresses `linux/brcmfmac/core.c:1009` `whd/src/whd_wifi_api.c:5777` |

- linux — get — 32 bytes, 8 `__be32` entries; a zero entry is treated as empty — `brcmf_inetaddr_changed`: read the ARP-offload host address table — `linux/brcmfmac/core.c:1009` `linux/brcmfmac/core.c:1033-1034` `linux/brcmfmac/core.c:1070-1071`
- linux — set — one address, 4 bytes — on `NETDEV_UP` when the address is not already in the table — `linux/brcmfmac/core.c:1040-1051`
- linux — set — one address per call, 4 bytes — on `NETDEV_DOWN`, re-adds each remaining entry after `arp_hostip_clear` — `linux/brcmfmac/core.c:1069-1074`
- whd — set — `count` × 4 bytes — `whd_arp_hostip_list_add`: add host IPv4 address(es) — `whd/src/whd_wifi_api.c:5618` `whd/src/whd_wifi_api.c:5682` `whd/src/include/whd_wlioctl.h:1260`
- whd — get — 32 bytes into `uint32_t temp[8]`; the helper passes the first 4 bytes through `dtoh32` — `whd_arp_hostip_list_get` — `whd/src/whd_wifi_api.c:5777` `whd/src/whd_wifi_api.c:5796` `whd/src/whd_wifi_api.c:5208`
- whd — `whd_arp_hostip_list_clear_id` re-adds entries by calling `whd_arp_hostip_list_add(ifp, &host_ipv4_list[drop], sizeof(uint32_t))`: the third argument is a count, so 4 is passed where the comment says one at a time — `whd/src/whd_wifi_api.c:5741-5744` `whd/src/whd_wifi_api.c:5618`

Differences: linux sets exactly one address (4 bytes) per call `linux/brcmfmac/core.c:1050-1051`; whd sends `count` addresses in one call `whd/src/whd_wifi_api.c:5682`. linux types the entries big-endian `linux/brcmfmac/core.c:1009`; whd uses `uint32_t` with no conversion on set `whd/src/whd_wifi_api.c:5682`.

Note (whd pass-through): `whd_wifi_get_iovar_buffer` takes the name as a parameter; the request carries `out_length` bytes after the name, the first 4 reply bytes are passed through `dtoh32`, then `out_length` bytes are copied out `whd/src/whd_wifi_api.c:5190-5214`.

### `arp_hostip_clear`
| | |
|---|---|
| Used by | linux, whd; no `bsscfg:` prefix `linux/brcmfmac/core.c:1062-1063` `whd/src/whd_wifi_api.c:5719-5720`. Not found in embassy, c-driver. |
| Direction | set (both) `linux/brcmfmac/core.c:1062-1063` `whd/src/whd_wifi_api.c:5719-5720` |
| Value | no payload, 0 bytes `linux/brcmfmac/core.c:1062-1063` `whd/src/whd_wifi_api.c:5143-5151` |
| Record | none `linux/brcmfmac/core.c:1062-1063` |

- linux — set — nothing (NULL, length 0) — `brcmf_inetaddr_changed` on `NETDEV_DOWN`: clear the table before re-adding the remaining addresses — `linux/brcmfmac/core.c:1061-1063`
- whd — set — nothing — `whd_arp_hostip_list_clear_id`: clear the list before rewriting it without one address — `whd/src/whd_wifi_api.c:5719-5720` `whd/src/include/whd_wlioctl.h:1261`
- whd — set — nothing — `whd_arp_hostip_list_clear`: clear all host addresses — `whd/src/whd_wifi_api.c:5768-5772`

Note (whd pass-through): `whd_wifi_set_iovar_void` takes the name as a parameter and sends no payload (0 bytes) `whd/src/whd_wifi_api.c:5143-5151`.

### `arp_ol`
| | |
|---|---|
| Used by | linux, whd; no `bsscfg:` prefix `linux/brcmfmac/core.c:113` `whd/src/whd_wifi_api.c:5583`. Not found in embassy, c-driver. |
| Direction | linux: set `linux/brcmfmac/core.c:113`. whd: both `whd/src/whd_wifi_api.c:5583` `whd/src/whd_wifi_api.c:5596`. |
| Value | u32 bit mask, 4 bytes. linux little-endian `linux/brcmfmac/fwil.h:122-128`. whd set: host order, no `htod32` `whd/src/whd_wifi_api.c:5596` `whd/src/whd_wifi_api.c:5185-5188`; whd get: first word through `dtoh32` `whd/src/whd_wifi_api.c:5208`. |
| Record | plain integer `linux/brcmfmac/fwil.h:122-128` |

- linux, whd — bit names — 0x1 AGENT, 0x2 SNOOP, 0x4 HOST_AUTO_REPLY, 0x8 PEER_AUTO_REPLY — `linux/brcmfmac/fwil_types.h:16-19` `whd/src/include/whd_wlioctl.h:3602-3605`
- linux — set — 0x9 (AGENT | PEER_AUTO_REPLY) to enable, 0 to disable — `brcmf_configure_arp_nd_offload`: ARP offload mode; enabling is skipped while a soft AP is operating; called from the multicast worker with enable = not promiscuous — `linux/brcmfmac/core.c:101-113` `linux/brcmfmac/core.c:206`
- whd — get — 4 bytes, feature mask — `whd_arp_features_get` — `whd/src/whd_wifi_api.c:5583` `whd/src/include/whd_wlioctl.h:1258`
- whd — set — 4 bytes, caller's mask copied as given — `whd_arp_features_set` — `whd/src/whd_wifi_api.c:5592-5597`
- whd — get — 4 bytes into `features_enabled` (`uint32_t`) — `whd_arp_stats_get` — `whd/src/whd_wifi_api.c:5851-5853` `whd/src/include/whd_wlioctl.h:4284`

Note (whd pass-through): `whd_wifi_set_iovar_buffer` takes the name as a parameter and copies the caller's bytes as given, with no byte swap; it calls `whd_wifi_set_iovar_buffers` with one buffer `whd/src/whd_wifi_api.c:5185-5188` `whd/src/whd_wifi_api.c:5284-5312`. `whd_wifi_set_iovar_buffers` advances a `uint32_t *` by `lengths[n]`, so the buffers land back to back only when there is one buffer (inferred from the pointer type); the caller shown passes 1 `whd/src/whd_wifi_api.c:5288` `whd/src/whd_wifi_api.c:5304-5308` `whd/src/whd_wifi_api.c:5187`.

### `arp_peerage`
| | |
|---|---|
| Used by | whd, no "bsscfg:" prefix `whd/src/whd_wifi_api.c:5543`. Not found in embassy, linux, c-driver. whd macro `IOVAR_STR_ARP_PEERAGE` `whd/src/include/whd_wlioctl.h:1256`. |
| Direction | whd: both `whd/src/whd_wifi_api.c:5543` `whd/src/whd_wifi_api.c:5550` |
| Value | whd: uint32, 4 bytes, little-endian (htod32 on set, dtoh32 on get) `whd/src/whd_wifi_api.c:5161` `whd/src/whd_wifi_api.c:5179` |
| Record | plain integer `whd/src/whd_wifi_api.c:5161` `whd/src/whd_wifi_api.c:5179` |

- whd — get, `whd_arp_peerage_get`; the public prototype names the argument `seconds` — 4-byte request buffer, reply read as uint32 — `whd/src/whd_wifi_api.c:5543` `whd/src/whd_wifi_api.c:5175` `whd/inc/whd_wifi_api.h:1250`
- whd — set, `whd_arp_peerage_set` — caller's uint32 — `whd/src/whd_wifi_api.c:5550` `whd/inc/whd_wifi_api.h:1260`
- whd — get, `whd_arp_stats_get` — uint32 stored in the `peerage` field of the stats snapshot — `whd/src/whd_wifi_api.c:5865`

### `arp_stats`
| | |
|---|---|
| Used by | whd, no "bsscfg:" prefix `whd/src/whd_wifi_api.c:5843`. Not found in embassy, linux, c-driver. whd macro `IOVAR_STR_ARP_STATS` `whd/src/include/whd_wlioctl.h:1262`. |
| Direction | whd: get `whd/src/whd_wifi_api.c:5788` `whd/src/whd_wifi_api.c:5843` |
| Value | whd: `arp_ol_stats_t`, 48 bytes (12 x uint32), each field converted with dtoh32 after the read `whd/src/include/whd_wlioctl.h:3609` `whd/src/whd_wifi_api.c:5879` |
| Record | `arp_ol_stats_t` `whd/src/include/whd_wlioctl.h:3609-3623`; all fields uint32: `host_ip_entries`@0, `host_ip_overflow`@4, `arp_table_entries`@8, `arp_table_overflow`@12, `host_request`@16, `host_reply`@20, `host_service`@24, `peer_request`@28, `peer_request_drop`@32, `peer_reply`@36, `peer_reply_drop`@40, `peer_service`@44 (offsets inferred from twelve consecutive uint32 fields) `whd/src/include/whd_wlioctl.h:3611` |

- whd — get, `whd_arp_hostip_list_get` reads the stats before reading `arp_hostip`; this call passes the string literal, not the macro — `arp_ol_stats_t` into a zeroed local, request length 48 — `whd/src/whd_wifi_api.c:5787` `whd/src/whd_wifi_api.c:5788` `whd/src/whd_wifi_api.c:5796`
- whd — get, `whd_arp_stats_get`; the whole snapshot is re-read in a loop until two consecutive reads compare equal — `arp_ol_stats_t` into the caller's snapshot — `whd/src/whd_wifi_api.c:5843` `whd/src/whd_wifi_api.c:5899`

### `arp_stats_clear`
| | |
|---|---|
| Used by | whd, no "bsscfg:" prefix `whd/src/whd_wifi_api.c:5818`. Not found in embassy, linux, c-driver. whd macro `IOVAR_STR_ARP_STATS_CLEAR` `whd/src/include/whd_wlioctl.h:1263`. |
| Direction | whd: set `whd/src/whd_wifi_api.c:5818` |
| Value | whd: no value, 0 bytes after the name `whd/src/whd_wifi_api.c:5148` |
| Record | none (name only) `whd/src/whd_wifi_api.c:5148` |

- whd — set, `whd_arp_stats_clear` — nothing written — `whd/src/whd_wifi_api.c:5818`

### `arp_table_clear`
| | |
|---|---|
| Used by | whd, no "bsscfg:" prefix `whd/src/whd_wifi_api.c:5572`. Not found in embassy, linux, c-driver. whd macro `IOVAR_STR_ARP_TABLE_CLEAR` `whd/src/include/whd_wlioctl.h:1259`. |
| Direction | whd: set `whd/src/whd_wifi_api.c:5572` |
| Value | whd: no value, 0 bytes after the name `whd/src/whd_wifi_api.c:5148` |
| Record | none (name only) `whd/src/whd_wifi_api.c:5148` |

- whd — set, `whd_arp_cache_clear` — nothing written — `whd/src/whd_wifi_api.c:5572`

### `arp_version`
| | |
|---|---|
| Used by | linux and whd, both without "bsscfg:" prefix `linux/brcmfmac/core.c:1026` `whd/src/whd_wifi_api.c:5536`. Not found in embassy, c-driver. whd macro `IOVAR_STR_ARP_VERSION` `whd/src/include/whd_wlioctl.h:1255`; linux uses a string literal `linux/brcmfmac/core.c:1026`. |
| Direction | linux: get `linux/brcmfmac/core.c:1026`. whd: get `whd/src/whd_wifi_api.c:5536` |
| Value | linux: u32, 4 bytes, little-endian `linux/brcmfmac/fwil.h:134`. whd: uint32, 4 bytes, little-endian `whd/src/whd_wifi_api.c:5179` |
| Record | plain integer `linux/brcmfmac/fwil.h:134` `whd/src/whd_wifi_api.c:5179` |

- linux — get, in the IPv4 address notifier; on error the value is taken as 1, and for value 1 linux switches to interface 0 for the host-IP table — u32 — `linux/brcmfmac/core.c:1026` `linux/brcmfmac/core.c:1028` `linux/brcmfmac/core.c:1030`
- whd — get, `whd_arp_version` — uint32 — `whd/src/whd_wifi_api.c:5536`
- whd — get, `whd_arp_stats_get` — uint32 stored in the `version` field of the stats snapshot — `whd/src/whd_wifi_api.c:5859`

### `arpoe`
| | |
|---|---|
| Used by | linux and whd, both without "bsscfg:" prefix `linux/brcmfmac/core.c:118` `whd/src/whd_wifi_api.c:5557`. Not found in embassy, c-driver. whd macro `IOVAR_STR_ARPOE` `whd/src/include/whd_wlioctl.h:1257`; linux uses a string literal `linux/brcmfmac/core.c:118`. |
| Direction | linux: both `linux/brcmfmac/core.c:118` `linux/brcmfmac/core.c:1021`. whd: both `whd/src/whd_wifi_api.c:5557` `whd/src/whd_wifi_api.c:5564` |
| Value | linux: u32, 4 bytes, little-endian `linux/brcmfmac/fwil.h:125`. whd: uint32, 4 bytes, little-endian `whd/src/whd_wifi_api.c:5161` |
| Record | plain integer `linux/brcmfmac/fwil.h:125` `whd/src/whd_wifi_api.c:5161` |

- linux — set, sent only if the preceding `arp_ol` set succeeded — `enable` (0 or 1) — `linux/brcmfmac/core.c:118` `linux/brcmfmac/core.c:113`
- linux — get, probe for ARP offload support before reading the host-IP table — u32, value not used, only the error code — `linux/brcmfmac/core.c:1021`
- whd — get, `whd_arp_arpoe_get` — uint32 — `whd/src/whd_wifi_api.c:5557`
- whd — set, `whd_arp_arpoe_set` — caller's uint32 — `whd/src/whd_wifi_api.c:5564`
- whd — get, `whd_arp_stats_get` — uint32 stored in the `arpoe` field of the stats snapshot — `whd/src/whd_wifi_api.c:5871`
- whd — get, `whd_wifi_start_ap` reads the current state; return value not checked — uint32 — `whd/src/whd_ap.c:555`
- whd — set, `whd_wifi_start_ap` turns the offload off if the read value was non-zero; return value not checked — 0 (`WHD_FALSE`) — `whd/src/whd_ap.c:559`
- whd — set, `whd_wifi_stop_ap` turns it back on when the `WHD_FWCAP_OFFLOADS` capability bit is set; return value not checked — 1 (`WHD_TRUE`) — `whd/src/whd_ap.c:741` `whd/src/whd_ap.c:739`

### `assoc_info`
| | |
|---|---|
| Used by | linux, no "bsscfg:" prefix `linux/brcmfmac/cfg80211.c:6481`. Not found in embassy, whd, c-driver. |
| Direction | linux: get `linux/brcmfmac/cfg80211.c:6481` |
| Value | linux: request buffer of 512 bytes (`WL_ASSOC_INFO_MAX`); the first 8 bytes of the reply are read as two little-endian u32 `linux/brcmfmac/cfg80211.h:23` `linux/brcmfmac/cfg80211.c:6489` |
| Record | `struct brcmf_cfg80211_assoc_ielen_le`: `req_len` le32 @0, `resp_len` le32 @4 `linux/brcmfmac/cfg80211.h:274` |

- linux — get, `brcmf_get_assoc_ies`: lengths of the association request and response IEs, used to decide whether to read `assoc_req_ies` and `assoc_resp_ies`; a length above `WL_EXTRA_BUF_MAX` is rejected — `req_len` and `resp_len` — `linux/brcmfmac/cfg80211.c:6481` `linux/brcmfmac/cfg80211.c:6491`

### `assoc_listen`
| | |
|---|---|
| Used by | embassy, whd, c-driver, all without "bsscfg:" prefix `embassy/control.rs:360` `whd/src/whd_wifi_api.c:4097` `c-driver/cyw43_ll.c:2156`. Not found in linux. whd macro `IOVAR_STR_LISTEN_INTERVAL_ASSOC` `whd/src/include/whd_wlioctl.h:1085`; embassy and c-driver use string literals. |
| Direction | embassy: set `embassy/control.rs:360`. whd: both `whd/src/whd_wifi_api.c:4097` `whd/src/whd_wifi_api.c:4138`. c-driver: both `c-driver/cyw43_ll.c:2156` `c-driver/cyw43_ll.c:2183` |
| Value | embassy: u32, 4 bytes, little-endian `embassy/control.rs:703`. whd: set uint32, 4 bytes, little-endian; get sends 4 zero bytes and uses the first 2 bytes of the reply `whd/src/whd_wifi_api.c:5161` `whd/src/whd_wifi_api.c:4140` `whd/src/whd_wifi_api.c:4144`. c-driver: u32, 4 bytes, little-endian `c-driver/cyw43_ll.c:1542` `c-driver/cyw43_ll.c:1975` |
| Record | plain integer `embassy/control.rs:703` `whd/src/whd_wifi_api.c:5161` `whd/src/whd_wifi_api.c:4140` `whd/src/whd_wifi_api.c:4144` `c-driver/cyw43_ll.c:1542` `c-driver/cyw43_ll.c:1975` |

- embassy — set, `set_power_management`; sent only when the mode number is 2, which is every mode except ThroughputThrottling and None; embassy does not describe the value — 255 (SuperSave), 10 (Aggressive, PowerSave), 1 (Performance) — `embassy/control.rs:360` `embassy/lib.rs:467` `embassy/lib.rs:478`
- whd — set, `whd_wifi_set_listen_interval`, sent for both time units — `listen_interval` (uint8 argument widened to uint32) — `whd/src/whd_wifi_api.c:4097` `whd/src/whd_wifi_api.c:4067`
- whd — get, `whd_wifi_get_listen_interval` — 2 bytes copied into `li->assoc` — `whd/src/whd_wifi_api.c:4138` `whd/src/whd_wifi_api.c:4144`
- c-driver — set, `cyw43_ll_wifi_pm`; source comment: this is the value sent to the AP, while `bcn_li_*` is what the chip does — `li_assoc` from the caller — `c-driver/cyw43_ll.c:2156` `c-driver/cyw43_ll.c:2152`
- c-driver — get, `cyw43_ll_wifi_get_pm`; the request carries 4 zero bytes after the name — u32 — `c-driver/cyw43_ll.c:2183` `c-driver/cyw43_ll.c:1973`

Differences: on get, whd uses 2 bytes of the reply `whd/src/whd_wifi_api.c:4144`; c-driver uses 4 bytes `c-driver/cyw43_ll.c:1975`.

### `assoc_req_ies`
| | |
|---|---|
| Used by | linux, no "bsscfg:" prefix `linux/brcmfmac/cfg80211.c:6497`. Not found in embassy, whd, c-driver. |
| Direction | linux: get `linux/brcmfmac/cfg80211.c:6497` |
| Value | linux: request buffer of 512 bytes (`WL_ASSOC_INFO_MAX`); the first `req_len` bytes of the reply are kept as raw information elements `linux/brcmfmac/cfg80211.h:23` `linux/brcmfmac/cfg80211.c:6506` |
| Record | byte string, no record `linux/brcmfmac/cfg80211.h:23` `linux/brcmfmac/cfg80211.c:6506` |

- linux — get, `brcmf_get_assoc_ies`: association request IEs; read only when `assoc_info` returned a non-zero `req_len` — `req_len` bytes of IEs — `linux/brcmfmac/cfg80211.c:6497` `linux/brcmfmac/cfg80211.c:6496`

### `assoc_resp_ies`
| | |
|---|---|
| Used by | linux, no "bsscfg:" prefix `linux/brcmfmac/cfg80211.c:6515`. Not found in embassy, whd, c-driver. |
| Direction | linux: get `linux/brcmfmac/cfg80211.c:6515` |
| Value | linux: request buffer of 512 bytes (`WL_ASSOC_INFO_MAX`); `resp_len` bytes of the reply are used as raw information elements (length taken from `assoc_info`) `linux/brcmfmac/cfg80211.h:23` `linux/brcmfmac/cfg80211.c:6490` `linux/brcmfmac/cfg80211.c:6524` |
| Record | byte string, no record `linux/brcmfmac/cfg80211.h:23` `linux/brcmfmac/cfg80211.c:6490` `linux/brcmfmac/cfg80211.c:6524` |

- linux — get, `brcmf_get_assoc_ies`: association response IEs; read only when `assoc_info` returned a non-zero `resp_len` — IEs — `linux/brcmfmac/cfg80211.c:6515` `linux/brcmfmac/cfg80211.c:6514`

### `auth`
| | |
|---|---|
| Used by | linux, through the bsscfg helper: plain name when the interface's bsscfg index is 0, otherwise "bsscfg:auth" followed by a le32 index `linux/brcmfmac/cfg80211.c:2020` `linux/brcmfmac/fwil.c:308` `linux/brcmfmac/fwil.c:259` `linux/brcmfmac/fwil.c:282`. Not found in embassy, whd, c-driver. |
| Direction | linux: set `linux/brcmfmac/cfg80211.c:2020` |
| Value | linux: u32, 4 bytes, little-endian (`brcmf_fil_bsscfg_int_set`) `linux/brcmfmac/fwil.h:154` `linux/brcmfmac/fwil.h:156` |
| Record | plain integer `linux/brcmfmac/fwil.h:154` `linux/brcmfmac/fwil.h:156` |

- linux — set, `brcmf_set_auth_type`, on connect — 0 (open system), 1 (shared key), 3 (SAE), 2 (any other type, logged as "automatic") — `linux/brcmfmac/cfg80211.c:2020` `linux/brcmfmac/cfg80211.c:2003` `linux/brcmfmac/cfg80211.c:2007` `linux/brcmfmac/cfg80211.c:2011` `linux/brcmfmac/cfg80211.c:2015`
- linux — set, when the profile's auth type is shared key — 1 (`WL_AUTH_SHARED_KEY`) — `linux/brcmfmac/cfg80211.c:2347` `linux/brcmfmac/cfg80211.h:55`
- linux — set, `brcmf_configure_opensecurity` — 0 — `linux/brcmfmac/cfg80211.c:4554` `linux/brcmfmac/cfg80211.c:4547`
- linux — set, `brcmf_configure_wpaie` — `auth` value computed while parsing the WPA/RSN IE — `linux/brcmfmac/cfg80211.c:4812` `linux/brcmfmac/cfg80211.c:4593`

### `auth_status`
| | |
|---|---|
| Used by | linux (Cypress vendor module) and whd, both without "bsscfg:" prefix `linux/brcmfmac/cyw/core.c:225` `whd/src/whd_wifi_api.c:5495`. Not found in embassy, c-driver. whd macro `IOVAR_STR_AUTH_STATUS` `whd/src/include/whd_wlioctl.h:1251`; linux uses a string literal `linux/brcmfmac/cyw/core.c:225`. |
| Direction | linux: set `linux/brcmfmac/cyw/core.c:225`. whd: set `whd/src/whd_wifi_api.c:5506` |
| Value | linux: `struct brcmf_auth_req_status_le`, `sizeof` the struct; `flags` and `ssid_len` little-endian `linux/brcmfmac/cyw/core.c:226` `linux/brcmfmac/cyw/core.c:212` `linux/brcmfmac/cyw/core.c:222`. whd: `whd_auth_req_status_t`, `sizeof` the struct, copied from the caller with no byte-order conversion `whd/src/whd_wifi_api.c:5494` `whd/src/whd_wifi_api.c:5497`. Flag values in both drivers: START 1, ABORT 2, FAIL 3, SUCCESS 4 `linux/brcmfmac/cyw/fwil_types.h:39` `whd/src/include/whd_wlioctl.h:118` |
| Record | linux: `struct brcmf_auth_req_status_le` `linux/brcmfmac/cyw/fwil_types.h:53-59`. whd: `whd_auth_req_status_t` `whd/inc/whd_types.h:1168-1175`. Fields, same order in both drivers: `flags` 16-bit, `peer_mac` MAC address, `ssid_len` 32-bit, `ssid` bytes, `pmkid` bytes `linux/brcmfmac/cyw/fwil_types.h:54` `whd/inc/whd_types.h:1170`. Array lengths: whd `peer_mac` 6, `ssid` 32, `pmkid` 16 `whd/inc/whd_types.h:553` `whd/inc/whd_types.h:61` `whd/inc/whd_types.h:93`; linux `ssid` 32, `pmkid` 16 `linux-headers/ieee80211.h:227` `linux-headers/ieee80211.h:2271`; `ETH_ALEN` is not found in these sources (6, recalled, not in these sources). Size 60 bytes (compiled on an x86 host; not measured with an ARM compiler); offsets (inferred from the field list with natural alignment, with `ETH_ALEN` = 6 for linux): `flags`@0, `peer_mac`@2, `ssid_len`@8, `ssid`@12, `pmkid`@44 `linux/brcmfmac/cyw/fwil_types.h:53` `whd/inc/whd_types.h:1168` |

- linux — set, reports the result of host-side (external) authentication; installed as the `external_auth` operation — zero-initialised record; `flags` = 4 on success, 3 on failure; `pmkid` copied only on success and only if supplied; `peer_mac` = BSSID; `ssid_len` clamped to `IEEE80211_MAX_SSID_LEN`; `ssid` copied — `linux/brcmfmac/cyw/core.c:225` `linux/brcmfmac/cyw/core.c:201` `linux/brcmfmac/cyw/core.c:208` `linux/brcmfmac/cyw/core.c:219` `linux/brcmfmac/cyw/core.c:220` `linux/brcmfmac/cyw/core.c:236`
- whd — set, `whd_wifi_set_auth_status` — caller's record copied whole, then `flags` overwritten: 4 (`WL_EXTAUTH_SUCCESS`) if the caller's `flags` equals `DOT11_SC_SUCCESS` (0), otherwise 3 (`WL_EXTAUTH_FAIL`) — `whd/src/whd_wifi_api.c:5497` `whd/src/whd_wifi_api.c:5498` `whd/src/whd_wifi_api.c:5506` `whd/src/include/whd_types_int.h:351`

Differences: linux converts `flags` and `ssid_len` to little-endian explicitly `linux/brcmfmac/cyw/core.c:212` `linux/brcmfmac/cyw/core.c:222`; whd writes them in host byte order `whd/src/whd_wifi_api.c:5500`. linux leaves `pmkid` zero on failure `linux/brcmfmac/cyw/core.c:209`; whd sends whatever the caller put there `whd/src/whd_wifi_api.c:5497`.

### `autocountry`
| | |
|---|---|
| Used by | none. whd defines the name as the macro `IOVAR_STR_AUTOCOUNTRY` and does not use it `whd/src/include/whd_wlioctl.h:1161`. Not found in embassy, linux, c-driver. |
| Direction | not shown by any driver `whd/src/include/whd_wlioctl.h:1161` |
| Value | payload not shown by any driver `whd/src/include/whd_wlioctl.h:1161` |
| Record | not shown by any driver `whd/src/include/whd_wlioctl.h:1161` |

- whd — name defined only; the macro name appears only at its `#define` in the whd `.c` and `.h` files — no payload — `whd/src/include/whd_wlioctl.h:1161`

### `avb_timestamp_addr`
| | |
|---|---|
| Used by | none. whd defines the name as the macro `IOVAR_STR_AVB_TIMESTAMP_ADDR` and does not use it `whd/src/include/whd_wlioctl.h:1145`. Not found in embassy, linux, c-driver. |
| Direction | not shown by any driver `whd/src/include/whd_wlioctl.h:1145` |
| Value | payload not shown by any driver `whd/src/include/whd_wlioctl.h:1145` |
| Record | not shown by any driver `whd/src/include/whd_wlioctl.h:1145` |

- whd — name defined only; the macro name appears only at its `#define` in the whd `.c` and `.h` files — no payload — `whd/src/include/whd_wlioctl.h:1145`

### `bcn_li_bcn`
| | |
|---|---|
| Used by | embassy, whd, c-driver, all without "bsscfg:" prefix `embassy/control.rs:358` `whd/src/whd_wifi_api.c:4087` `c-driver/cyw43_ll.c:2154`. Not found in linux. whd macro `IOVAR_STR_LISTEN_INTERVAL_BEACON` `whd/src/include/whd_wlioctl.h:1083`; embassy and c-driver use string literals. |
| Direction | embassy: set `embassy/control.rs:358`. whd: both `whd/src/whd_wifi_api.c:4087` `whd/src/whd_wifi_api.c:4120`. c-driver: both `c-driver/cyw43_ll.c:2154` `c-driver/cyw43_ll.c:2181` |
| Value | embassy: u32, 4 bytes, little-endian `embassy/control.rs:703`. whd: set uint32, 4 bytes, little-endian; get sends a 4-byte buffer with only byte 0 cleared and uses the first byte of the reply `whd/src/whd_wifi_api.c:5161` `whd/src/whd_wifi_api.c:4122` `whd/src/whd_wifi_api.c:4126`. c-driver: u32, 4 bytes, little-endian `c-driver/cyw43_ll.c:1542` `c-driver/cyw43_ll.c:1975` |
| Record | plain integer `embassy/control.rs:703` `whd/src/whd_wifi_api.c:5161` `whd/src/whd_wifi_api.c:4122` `whd/src/whd_wifi_api.c:4126` `c-driver/cyw43_ll.c:1542` `c-driver/cyw43_ll.c:1975` |

- embassy — set, `set_power_management`, only when the mode number is 2; the helper is named `beacon_period`, embassy gives no unit — 255 (SuperSave), 1 (Aggressive, PowerSave, Performance) — `embassy/control.rs:358` `embassy/lib.rs:445` `embassy/lib.rs:478`
- whd — set, `whd_wifi_set_listen_interval`, only when the time unit is BEACON; source comment: wake period in beacon periods — `listen_interval` — `whd/src/whd_wifi_api.c:4087` `whd/src/whd_wifi_api.c:4081`
- whd — get, `whd_wifi_get_listen_interval` — 1 byte copied into `li->beacon` — `whd/src/whd_wifi_api.c:4120` `whd/src/whd_wifi_api.c:4126`
- c-driver — set, `cyw43_ll_wifi_pm`; source comment: used when `bcn_li_dtim` is 0 — `li_bcn` from the caller — `c-driver/cyw43_ll.c:2154` `c-driver/cyw43_ll.c:2153`
- c-driver — get, `cyw43_ll_wifi_get_pm` — u32 — `c-driver/cyw43_ll.c:2181`

Differences: on get, whd uses 1 byte of the reply `whd/src/whd_wifi_api.c:4126`; c-driver uses 4 bytes `c-driver/cyw43_ll.c:1975`. whd's get request leaves bytes 1..3 after the name uncleared `whd/src/whd_wifi_api.c:4122`; c-driver sends 4 zero bytes `c-driver/cyw43_ll.c:1973`.

### `bcn_li_dtim`
| | |
|---|---|
| Used by | embassy, whd, c-driver, all without "bsscfg:" prefix `embassy/control.rs:359` `whd/src/whd_wifi_api.c:4095` `c-driver/cyw43_ll.c:2155`. Not found in linux. whd macro `IOVAR_STR_LISTEN_INTERVAL_DTIM` `whd/src/include/whd_wlioctl.h:1084`; embassy and c-driver use string literals. |
| Direction | embassy: set `embassy/control.rs:359`. whd: both `whd/src/whd_wifi_api.c:4095` `whd/src/whd_wifi_api.c:4129`. c-driver: both `c-driver/cyw43_ll.c:2155` `c-driver/cyw43_ll.c:2182` |
| Value | embassy: u32, 4 bytes, little-endian `embassy/control.rs:703`. whd: set uint32, 4 bytes, little-endian; get sends a 4-byte buffer with only byte 0 cleared and uses the first byte of the reply `whd/src/whd_wifi_api.c:5161` `whd/src/whd_wifi_api.c:4131` `whd/src/whd_wifi_api.c:4135`. c-driver: u32, 4 bytes, little-endian `c-driver/cyw43_ll.c:1542` `c-driver/cyw43_ll.c:1975` |
| Record | plain integer `embassy/control.rs:703` `whd/src/whd_wifi_api.c:5161` `whd/src/whd_wifi_api.c:4131` `whd/src/whd_wifi_api.c:4135` `c-driver/cyw43_ll.c:1542` `c-driver/cyw43_ll.c:1975` |

- embassy — set, `set_power_management`, only when the mode number is 2; the helper is named `dtim_period`, embassy gives no unit — 255 (SuperSave), 1 (Aggressive, PowerSave, Performance) — `embassy/control.rs:359` `embassy/lib.rs:456` `embassy/lib.rs:478`
- whd — set, `whd_wifi_set_listen_interval`; source comment: 0 means the wake interval is measured in beacon periods — `listen_interval` when the time unit is DTIM, 0 when the time unit is BEACON — `whd/src/whd_wifi_api.c:4095` `whd/src/whd_wifi_api.c:4078` `whd/src/whd_wifi_api.c:4084`
- whd — get, `whd_wifi_get_listen_interval` — 1 byte copied into `li->dtim` — `whd/src/whd_wifi_api.c:4129` `whd/src/whd_wifi_api.c:4135`
- c-driver — set, `cyw43_ll_wifi_pm`; source comment: 0 means use `bcn_li_bcn` — `li_dtim` from the caller — `c-driver/cyw43_ll.c:2155` `c-driver/cyw43_ll.c:2153`
- c-driver — get, `cyw43_ll_wifi_get_pm` — u32 — `c-driver/cyw43_ll.c:2182`

Differences: on get, whd uses 1 byte of the reply `whd/src/whd_wifi_api.c:4135`; c-driver uses 4 bytes `c-driver/cyw43_ll.c:1975`. whd's get request leaves bytes 1..3 after the name uncleared `whd/src/whd_wifi_api.c:4131`; c-driver sends 4 zero bytes `c-driver/cyw43_ll.c:1973`.

### `bcn_timeout`
| | |
|---|---|
| Used by | linux, no "bsscfg:" prefix `linux/brcmfmac/cfg80211.c:7120`. Not found in embassy, whd, c-driver. |
| Direction | linux: set `linux/brcmfmac/cfg80211.c:7120` |
| Value | linux: u32, 4 bytes, little-endian `linux/brcmfmac/fwil.h:125` |
| Record | plain integer `linux/brcmfmac/fwil.h:125` |

- linux — set, `brcmf_dongle_roam`; the constants are labelled beacon-loss timeout defaults, no unit given — 4 when the `roamoff` setting is on, 2 otherwise — `linux/brcmfmac/cfg80211.c:7120` `linux/brcmfmac/cfg80211.c:7116` `linux/brcmfmac/cfg80211.h:92`

### `bg_rate`
| | |
|---|---|
| Used by | none. whd defines the name as the macro `IOVAR_STR_BGRATE` and does not use it `whd/src/include/whd_wlioctl.h:1117`. Not found in embassy, linux, c-driver. |
| Direction | not shown by any driver `whd/src/include/whd_wlioctl.h:1117` |
| Value | payload not shown by any driver `whd/src/include/whd_wlioctl.h:1117` |
| Record | not shown by any driver `whd/src/include/whd_wlioctl.h:1117` |

- whd — name defined only; the macro name appears only at its `#define` in the whd `.c` and `.h` files — no payload — `whd/src/include/whd_wlioctl.h:1117`

### `bip`
| | |
|---|---|
| Used by | linux, through the bsscfg helper: plain name when the interface's bsscfg index is 0, otherwise "bsscfg:bip" followed by a le32 index `linux/brcmfmac/cfg80211.c:4799` `linux/brcmfmac/fwil.c:259`. whd, no "bsscfg:" prefix `whd/src/whd_wifi_api.c:1952`. Not found in embassy, c-driver. whd macro `IOVAR_STR_BIP` `whd/src/include/whd_wlioctl.h:1227`; linux uses a string literal. |
| Direction | linux: set `linux/brcmfmac/cfg80211.c:4799`. whd: set `whd/src/whd_wifi_api.c:1952` |
| Value | linux: 4 bytes copied from the RSN IE as they stand `linux/brcmfmac/cfg80211.c:4800` `linux/brcmfmac/cfg80211.c:48`. whd: 4 literal bytes `whd/src/whd_wifi_api.c:1951` |
| Record | byte string, 4 bytes (cipher suite selector: 3-byte OUI then 1-byte type, inferred from the whd literals) `whd/src/whd_wifi_api.c:1951` |

- linux — set, `brcmf_configure_wpaie` (AP mode): sent only if the MFP feature is enabled and the IE still has 4 bytes left; source comment calls it the BIP suite for MFP — the 4 bytes that follow the PMKID count in the RSN IE — `linux/brcmfmac/cfg80211.c:4799` `linux/brcmfmac/cfg80211.c:4796`
- whd — set, `whd_wifi_prepare_join` for `WHD_SECURITY_WPA3_ENT` and `WHD_SECURITY_WPA3_192BIT_ENT`; source comment: group management cipher suite GMAC-256 — 00 0F AC 0C — `whd/src/whd_wifi_api.c:1952` `whd/src/whd_wifi_api.c:1949`
- whd — set, `whd_wifi_prepare_join` for `WHD_SECURITY_WPA3_ENT_AES_CCMP`; source comment: BIP-128 — 00 0F AC 06 — `whd/src/whd_wifi_api.c:1957` `whd/src/whd_wifi_api.c:1954`

Differences: linux may send the name with a "bsscfg:" prefix and index `linux/brcmfmac/fwil.c:259`; whd always sends the plain name `whd/src/whd_wifi_api.c:1952`. linux sends it when acting as AP `linux/brcmfmac/cfg80211.c:4799`; whd sends it before joining as a station `whd/src/whd_wifi_api.c:1952`.

### `brcmapivtwo`
| | |
|---|---|
| Used by | none. whd defines the name as the macro `IOVAR_STR_APIVTW_OVERRIDE` and does not use it `whd/src/include/whd_wlioctl.h:1241`. Not found in embassy, linux, c-driver. |
| Direction | not shown by any driver `whd/src/include/whd_wlioctl.h:1241` |
| Value | payload not shown by any driver `whd/src/include/whd_wlioctl.h:1241` |
| Record | not shown by any driver `whd/src/include/whd_wlioctl.h:1241` |

- whd — name defined only; the macro name appears only at its `#define` in the whd `.c` and `.h` files — no payload — `whd/src/include/whd_wlioctl.h:1241`

### `bss`
| | |
|---|---|
| Used by | embassy, linux, whd, c-driver. All four send the plain name "bss" with no "bsscfg:" prefix `embassy/control.rs:615` `linux/brcmfmac/cfg80211.c:5481` `whd/src/whd_ap.c:571` `c-driver/cyw43_ll.c:2457`. whd macro `IOVAR_STR_BSS` `whd/src/include/whd_wlioctl.h:1067`; the other three use string literals. |
| Direction | embassy: set `embassy/control.rs:615`. linux: set `linux/brcmfmac/cfg80211.c:5481`. whd: both `whd/src/whd_ap.c:248` `whd/src/whd_ap.c:571`. c-driver: both `c-driver/cyw43_ll.c:2363` `c-driver/cyw43_ll.c:2457` |
| Value | Set, all four: two 32-bit little-endian words, 8 bytes `embassy/control.rs:696` `linux/brcmfmac/fwil_types.h:244` `whd/src/whd_ap.c:573` `c-driver/cyw43_ll.c:1550`. Get, whd and c-driver: one 32-bit word in the request, one 32-bit word read from the reply `whd/src/whd_ap.c:250` `c-driver/cyw43_ll.c:2362` `c-driver/cyw43_ll.c:2364`. whd value names: `BSS_AP` 3, `BSS_STA` 2, `BSS_UP` 1, `BSS_DOWN` 0 `whd/src/whd_ap.c:53` |
| Record | linux: `struct brcmf_fil_bss_enable_le`: `bsscfgidx` le32 @0, `enable` le32 @4 `linux/brcmfmac/fwil_types.h:244`. embassy, whd, c-driver: two raw words `embassy/control.rs:697` `whd/src/whd_ap.c:573` `c-driver/cyw43_ll.c:1550` |

- embassy — set, start the access point; source comment: BSS_UP; embassy passes the two words as unnamed positional arguments — words 0, 1 — `embassy/control.rs:615` `embassy/control.rs:695`
- embassy — set, stop the access point; source comment: BSS_DOWN — words 0, 0 — `embassy/control.rs:641`
- linux — set, `brcmf_cfg80211_start_ap`, after setting the SSID — `bsscfgidx` = the interface's bsscfg index, `enable` = 1 — `linux/brcmfmac/cfg80211.c:5481` `linux/brcmfmac/cfg80211.c:5479`
- linux — set, `brcmf_cfg80211_stop_ap`, in the branch that does not issue `BRCMF_C_UP`/down commands — `bsscfgidx` = the interface's bsscfg index, `enable` = 0 — `linux/brcmfmac/cfg80211.c:5566` `linux/brcmfmac/cfg80211.c:5564`
- whd — get, `whd_create_softap_interface`: does the BSS exist and is it up; sent on the primary interface — request word = bsscfg index (htod32); reply word (dtoh32) compared with `BSS_UP` (1) — `whd/src/whd_ap.c:248` `whd/src/whd_ap.c:250` `whd/src/whd_ap.c:252` `whd/src/whd_ap.c:263`
- whd — set, `whd_wifi_start_ap`; then waits up to 10000 ms on a semaphore; sent on the primary interface — word 0 = `ifp->bsscfgidx`, word 1 = `BSS_UP` (1) — `whd/src/whd_ap.c:571` `whd/src/whd_ap.c:573` `whd/src/whd_ap.c:578`
- whd — get, `whd_wifi_stop_ap`: query the BSS state; result `WHD_WLAN_NOTFOUND` is treated as "AP is down" — request word = `ifp->bsscfgidx`, written without htod32 — `whd/src/whd_ap.c:623` `whd/src/whd_ap.c:625` `whd/src/whd_ap.c:628`
- whd — set, `whd_wifi_stop_ap` — word 0 = `ifp->bsscfgidx`, word 1 = `BSS_DOWN` (0) — `whd/src/whd_ap.c:683` `whd/src/whd_ap.c:685`
- c-driver — get, before AP setup; sent on `WWD_STA_INTERFACE`; a source TODO notes the call can fail with status 0xffffffe2 — "bss" + NUL (4 bytes) then le32 `WWD_AP_INTERFACE` (1), command length 8; reply le32, non-zero taken as "AP already up" — `c-driver/cyw43_ll.c:2361` `c-driver/cyw43_ll.c:2363` `c-driver/cyw43_ll.c:2359` `c-driver/cyw43_ll.c:152`
- c-driver — set, `cyw43_ll_wifi_ap_set_up`; sent on `WWD_STA_INTERFACE` — le32 `WWD_AP_INTERFACE` (1), le32 `up` (0 or 1) — `c-driver/cyw43_ll.c:2457` `c-driver/cyw43_ll.c:1546`

Differences: the first word differs. embassy sends 0 `embassy/control.rs:615`; c-driver sends 1 `c-driver/cyw43_ll.c:2457`; linux and whd send the interface's bsscfg index `linux/brcmfmac/cfg80211.c:5479` `whd/src/whd_ap.c:573`. Only whd and c-driver issue a get `whd/src/whd_ap.c:248` `c-driver/cyw43_ll.c:2363`.

### `bss_maxassoc`
| | |
|---|---|
| Used by | none. whd defines the name as the macro `IOVAR_STR_BSS_MAX_ASSOC` and does not use it `whd/src/include/whd_wlioctl.h:1146`. Not found in embassy, linux, c-driver. |
| Direction | not shown by any driver `whd/src/include/whd_wlioctl.h:1146` |
| Value | payload not shown by any driver `whd/src/include/whd_wlioctl.h:1146` |
| Record | not shown by any driver `whd/src/include/whd_wlioctl.h:1146` |

- whd — name defined only; the macro name appears only at its `#define` in the whd `.c` and `.h` files — no payload — `whd/src/include/whd_wlioctl.h:1146`

### `bss_rateset`
| | |
|---|---|
| Used by | none. whd defines the name as the macro `IOVAR_STR_BSS_RATESET` and does not use it `whd/src/include/whd_wlioctl.h:1068`. Not found in embassy, linux, c-driver. |
| Direction | not shown by any driver `whd/src/include/whd_wlioctl.h:1068` |
| Value | payload not shown by any driver `whd/src/include/whd_wlioctl.h:1068` |
| Record | not shown by any driver `whd/src/include/whd_wlioctl.h:1068` |

- whd — name defined only; the macro name appears only at its `#define` in the whd `.c` and `.h` files — no payload — `whd/src/include/whd_wlioctl.h:1068`

### `btc_lescan_params`
| | |
|---|---|
| Used by | whd, no "bsscfg:" prefix `whd/src/whd_wifi_api.c:5453`. Not found in embassy, linux, c-driver. whd macro `IOVAR_STR_BTC_LESCAN_PARAMS` `whd/src/include/whd_wlioctl.h:1253`. |
| Direction | whd: set `whd/src/whd_wifi_api.c:5453` |
| Value | whd: `whd_btc_lescan_params_t`, 12 bytes (6 x uint16), copied from the caller with no byte-order conversion `whd/inc/whd_types.h:1431` `whd/src/whd_wifi_api.c:5454` |
| Record | `whd_btc_lescan_params_t` `whd/inc/whd_types.h:1431-1439`; all fields uint16 (offsets inferred from six consecutive uint16 fields): `priority`@0, `duty_cycle`@2, `max_win`@4, `int_grant`@6, `scan_int`@8, `scan_win`@10 `whd/inc/whd_types.h:1433` |

- whd — set, `whd_wifi_set_coex_config`: Bluetooth-coexistence LE scan parameters — `coex_config->le_scan_params` — `whd/src/whd_wifi_api.c:5453`

### `btc_params`
| | |
|---|---|
| Used by | linux, no "bsscfg:" prefix `linux/brcmfmac/btcoex.c:112`. Not found in embassy, whd, c-driver. |
| Direction | linux: both `linux/brcmfmac/btcoex.c:112` `linux/brcmfmac/btcoex.c:126` |
| Value | linux set: two le32, 8 bytes (register number, value) `linux/brcmfmac/btcoex.c:105`. linux get: le32 register number in the request, le32 value in the same 4 bytes of the reply `linux/brcmfmac/btcoex.c:124` `linux/brcmfmac/fwil.h:144` `linux/brcmfmac/fwil.h:136` |
| Record | anonymous local struct: `addr` le32 @0, `data` le32 @4 `linux/brcmfmac/btcoex.c:105`. Meaning of the individual register numbers: not shown by any driver |

- linux — set, SCO/eSCO override; source comment: "pacify the eSco" — register 50 = 32802 (0x8022), 51 = 0, 64 = 0, 65 = 0, 71 = 0 — `linux/brcmfmac/btcoex.c:164` `linux/brcmfmac/btcoex.c:24`
- linux — set, restore after the override — registers 50, 51, 64, 65, 71 = previously read values — `linux/brcmfmac/btcoex.c:173`
- linux — set, values labelled "BT registers values during DHCP" — register 66 = 10000 (0x2710), 41 = 51 (0x33), 68 = 400 (0x190) — `linux/brcmfmac/btcoex.c:414` `linux/brcmfmac/btcoex.c:23` `linux/brcmfmac/btcoex.c:29`
- linux — set, restore — registers 66, 41, 68 = previously read values — `linux/brcmfmac/btcoex.c:260`
- linux — get, save before the SCO/eSCO override — registers 50, 51, 64, 65, 71 — `linux/brcmfmac/btcoex.c:151`
- linux — get, SCO detection sampling — register 27, up to 12 reads (`BRCMF_BT_SCO_SAMPLES`) — `linux/brcmfmac/btcoex.c:205` `linux/brcmfmac/btcoex.c:34`
- linux — get, save before the DHCP values are written — registers 66, 41, 68 — `linux/brcmfmac/btcoex.c:239`

### `bus:btsdiobufaddr`
| | |
|---|---|
| Used by | whd, no "bsscfg:" prefix. Not found in embassy, linux, c-driver. `whd/src/whd_wifi_api.c:501` |
| Direction | get `whd/src/whd_wifi_api.c:501` |
| Value | uint32_t, 4 bytes; whd passes the first reply word through dtoh32 `whd/src/whd_wifi_api.c:501` `whd/src/whd_wifi_api.c:5208` |
| Record | plain integer `whd/src/whd_wifi_api.c:501` |

- whd — get — reads 4 bytes into `bt_info->wlan_buf_addr` — `whd_get_bt_info`: the WLAN-side address of the shared Bluetooth SDIO buffer — `whd/src/whd_wifi_api.c:501-504`
- whd ignores a failed get: the function returns success either way and leaves the field 0. `whd/src/whd_wifi_api.c:497` `whd/src/whd_wifi_api.c:502-506`
- The other three `bt_info` fields are host constants, not read from the chip: 0x18000c7c, 0x18000d6c, 0x18000c78. `whd/src/whd_wifi_api.c:102-104` `whd/src/whd_wifi_api.c:498-500`
- whd macro `IOVAR_STR_BTADDR`. The "bus:" part is in the macro's string literal. `whd/src/include/whd_wlioctl.h:1065`

### `bus:rxglom`
| | |
|---|---|
| Used by | linux, no "bsscfg:" prefix. Not found in embassy, whd, c-driver. `linux/brcmfmac/sdio.c:3578-3579` |
| Direction | set `linux/brcmfmac/sdio.c:3578-3579` |
| Value | __le32, 4 bytes, little-endian `linux/brcmfmac/sdio.c:3577-3579` |
| Record | plain integer `linux/brcmfmac/sdio.c:3577-3579` |

- linux — set — 1 — enable glomming of host-to-device frames, only when the host controller supports scatter-gather (`sg_support`) — `linux/brcmfmac/sdio.c:3575-3579`
- linux names tx and rx here from the device's side. `linux/brcmfmac/sdio.c:3553-3556`
- linux tolerates failure of this set. On success it turns on its own tx glomming and adds `SDPCM_HWEXT_LEN` to the tx header length. `linux/brcmfmac/sdio.c:3580-3585`
- linux sends it on interface 0 through `brcmf_iovar_data_set`. `linux/brcmfmac/core.c:1552-1558`

### `bus:txglom`
| | |
|---|---|
| Used by | embassy, linux, whd, c-driver; none with a "bsscfg:" prefix `embassy/control.rs:271` `linux/brcmfmac/sdio.c:3560-3561` `whd/src/whd_management.c:465-471` `c-driver/cyw43_ll.c:1918` |
| Direction | set in all four `embassy/control.rs:271` `linux/brcmfmac/sdio.c:3560-3561` `whd/src/whd_management.c:465-471` `c-driver/cyw43_ll.c:1918` |
| Value | 32-bit integer, 4 bytes, value 0 in all four (little-endian where the value is encoded; whd writes a plain 0) `embassy/control.rs:702-704` `linux/brcmfmac/sdio.c:3559-3561` `whd/src/whd_management.c:465-471` `c-driver/cyw43_ll.c:1542-1543` |
| Record | plain integer `embassy/control.rs:702-704` `linux/brcmfmac/sdio.c:3559-3561` `whd/src/whd_management.c:465-471` `c-driver/cyw43_ll.c:1542-1543` |

- embassy — set — 0 — disable tx glomming at the start of init, before reading the MAC address — `embassy/control.rs:271`
- embassy — set — 0 — again after `country` and the antenna command, followed by a 100 ms wait — `embassy/control.rs:292-293`
- embassy sends it with `set_iovar_u32`: name, NUL, 4 little-endian bytes. `embassy/control.rs:702-704` `embassy/control.rs:717-728`
- linux — set — 0 — disable device-to-host glomming, only when the SDIO core revision is below 12 — `linux/brcmfmac/sdio.c:3557-3561`
- linux aborts bus pre-init if this set fails. `linux/brcmfmac/sdio.c:3571-3572`
- linux states that tx and rx in these names are from the device's side: `bus:txglom` affects device-to-host transfers. `linux/brcmfmac/sdio.c:3553-3556`
- whd — set — 0 — init sequence, compiled only when `PROTO_MSGBUF` is not defined; `WHD_WLAN_UNSUPPORTED` is tolerated, any other error aborts init — `whd/src/whd_management.c:460-479`
- whd macro `IOVAR_STR_TX_GLOM`. `whd/src/include/whd_wlioctl.h:1088`
- c-driver — set — 0 — bus init, right after the CLM download — `c-driver/cyw43_ll.c:1918`
- c-driver — set — 0 — again in the wifi-on configuration — `c-driver/cyw43_ll.c:2037`
- c-driver sends it with `cyw43_write_iovar_u32`: name, NUL, le32, length = name length + 1 + 4. `c-driver/cyw43_ll.c:1538-1544`

Differences: none in size or layout. linux sends it only for SDIO core revision < 12 and otherwise sends `bus:txglomalign`; whd sends it only in builds without `PROTO_MSGBUF`; embassy and c-driver send it unconditionally, twice each. `linux/brcmfmac/sdio.c:3557-3569` `whd/src/whd_management.c:460-465` `embassy/control.rs:271` `embassy/control.rs:292` `c-driver/cyw43_ll.c:1918` `c-driver/cyw43_ll.c:2037`

### `bus:txglomalign`
| | |
|---|---|
| Used by | linux, no "bsscfg:" prefix. Not found in embassy, whd, c-driver. `linux/brcmfmac/sdio.c:3567-3568` |
| Direction | set `linux/brcmfmac/sdio.c:3567-3568` |
| Value | __le32, 4 bytes, little-endian `linux/brcmfmac/sdio.c:3566-3568` |
| Record | plain integer `linux/brcmfmac/sdio.c:3566-3568` |

- linux — set — the larger of the `sd_sgentry_align` setting and `ALIGNMENT` — alignment of glommed device-to-host frames, only when the SDIO core revision is 12 or higher — `linux/brcmfmac/sdio.c:3562-3569`
- `ALIGNMENT` in linux is 8 on a 64-bit DMA address build, otherwise 4. `linux/brcmfmac/sdio.c:546-550`
- linux aborts bus pre-init if this set fails. `linux/brcmfmac/sdio.c:3571-3572`

### `bw_cap`
| | |
|---|---|
| Used by | linux, no "bsscfg:" prefix. Not found in embassy, whd, c-driver. `linux/brcmfmac/cfg80211.c:7360` |
| Direction | both `linux/brcmfmac/cfg80211.c:7360` `linux/brcmfmac/cfg80211.c:7366-7367` |
| Value | get: __le32, 4 bytes, band number in the request and capability bits in the reply. set: `struct brcmf_fil_bwcap_le`, 8 bytes, little-endian. `linux/brcmfmac/fwil.h:130-146` `linux/brcmfmac/cfg80211.c:7364-7367` `linux/brcmfmac/fwil_types.h:249-252` |
| Record | set: `struct brcmf_fil_bwcap_le` { __le32 band @0; __le32 bw_cap @4 } `linux/brcmfmac/fwil_types.h:249-252`. get: plain integer. |

- linux — get — request word = `WLC_BAND_5G` (1) — its comment says this verifies support for `bw_cap`; on error linux falls back to `mimo_bw_cap` — `linux/brcmfmac/cfg80211.c:7358-7370`
- linux — set — band = `WLC_BAND_2G` (2), bw_cap = `WLC_BW_CAP_40MHZ` (bits 0 and 1 = 3) — allow 40 MHz on 2.4 GHz — `linux/brcmfmac/cfg80211.c:7362-7367`
- linux — get — request word = 2 (2G) — the reply word is stored as the 2G bandwidth capability — `linux/brcmfmac/cfg80211.c:7435-7438`
- linux — get — request word = 1 (5G) — the reply word is stored as the 5G bandwidth capability — `linux/brcmfmac/cfg80211.c:7439-7442`
- linux's get helper writes the caller's value into the request as le32 and converts the reply from le32 in place. `linux/brcmfmac/fwil.h:130-146`
- linux defines the band and bit constants used here. `linux/include/brcmu_wifi.h:77-78` `linux/include/brcmu_wifi.h:84` `linux/include/brcmu_wifi.h:93-94`
- linux's get and set use different sizes (4 bytes against 8). `linux/brcmfmac/cfg80211.c:7360` `linux/brcmfmac/cfg80211.c:7366-7367`

### `bwte_gci_mask`
| | |
|---|---|
| Used by | defined, not used by whd. Not found in embassy, linux, c-driver. `whd/src/include/whd_wlioctl.h:1243` |
| Direction | not shown by any driver |
| Value | payload not shown by any driver |
| Record | not shown by any driver |

- whd — macro `IOVAR_STR_BWTE_BWTE_GCI_MASK`, no call site in any whd .c file — `whd/src/include/whd_wlioctl.h:1243`

### `bwte_gci_sendm`
| | |
|---|---|
| Used by | defined, not used by whd. Not found in embassy, linux, c-driver. `whd/src/include/whd_wlioctl.h:1244` |
| Direction | not shown by any driver |
| Value | payload not shown by any driver |
| Record | not shown by any driver |

- whd — macro `IOVAR_STR_BWTE_GCI_SENDMSG`, no call site in any whd .c file — `whd/src/include/whd_wlioctl.h:1244`

### `calload`
| | |
|---|---|
| Used by | linux, no "bsscfg:" prefix. Not found in embassy, whd, c-driver. `linux/brcmfmac/common.c:256-261` |
| Direction | set `linux/brcmfmac/common.c:114-115` |
| Value | 12-byte header plus up to 1400 data bytes per send (at most 1412), little-endian fields `linux/brcmfmac/common.c:108-115` `linux/brcmfmac/fwil_types.h:185` |
| Record | `struct brcmf_dload_data_le` { __le16 flag @0; __le16 dload_type @2; __le32 len @4; __le32 crc @8; u8 data[] @12 } `linux/brcmfmac/fwil_types.h:1106-1112` |

- linux — set — a platform-provided calibration blob, in chunks — sent only when the platform settings carry `cal_blob` and `cal_size` — `linux/brcmfmac/common.c:256-261` `linux/brcmfmac/common.c:114-115`
- linux sets flag = (1 << 12) | 0x0002 on the first chunk | 0x0004 on the last chunk: 0x1002 first, 0x1000 middle, 0x1004 last, 0x1006 when the blob fits one chunk. `linux/brcmfmac/common.c:108-109` `linux/brcmfmac/common.c:129` `linux/brcmfmac/common.c:144-155` `linux/brcmfmac/fwil_types.h:187-192`
- linux sets dload_type = `DL_TYPE_CLM` (2), the same value it uses for `clmload`; len = chunk length; crc = 0. `linux/brcmfmac/common.c:110-112` `linux/brcmfmac/fwil_types.h:194`
- linux stops the download at the first chunk that returns an error, then reads `calload_status`. `linux/brcmfmac/common.c:159-169`

### `calload_status`
| | |
|---|---|
| Used by | linux, no "bsscfg:" prefix. Not found in embassy, whd, c-driver. `linux/brcmfmac/common.c:165` |
| Direction | get `linux/brcmfmac/common.c:165` |
| Value | u32, 4 bytes, read as little-endian `linux/brcmfmac/common.c:165` `linux/brcmfmac/fwil.h:130-138` |
| Record | plain integer `linux/brcmfmac/common.c:165` |

- linux — get — one 32-bit status word, printed at debug level and not otherwise used — read only after a `calload` chunk failed — `linux/brcmfmac/common.c:161-169` `linux/brcmfmac/common.c:260-261`
- The 4 request bytes after the name are linux's uninitialised local `status`. `linux/brcmfmac/common.c:130` `linux/brcmfmac/fwil.c:225-232`
- Meaning of the status values: not shown by any driver; linux only prints the word. `linux/brcmfmac/common.c:161-169`

### `cap`
| | |
|---|---|
| Used by | linux, whd; neither with a "bsscfg:" prefix. Not found in embassy, c-driver. `linux/brcmfmac/feature.c:237` `whd/src/whd_chip.c:1001-1007` |
| Direction | get in both `linux/brcmfmac/feature.c:237` `whd/src/whd_chip.c:1001-1007` |
| Value | text. linux: 768-byte buffer, or 769 for the debugfs dump. whd: 768-byte buffer. `linux/brcmfmac/feature.c:229-237` `linux/brcmfmac/feature.c:266-270` `whd/src/whd_chip.c:60` `whd/src/whd_chip.c:1001-1007` |
| Record | character string, no record `linux/brcmfmac/feature.c:245-252` `whd/src/whd_chip.c:1007-1018` |

- linux — get — reads the reply as a string and sets a feature bit for each table substring found with `strnstr` — capability detection — `linux/brcmfmac/feature.c:237` `linux/brcmfmac/feature.c:245-252`
- Substrings linux looks for: "mbss", "mchan", "p2p", "monitor", "rtap" (two features), "802.11h", "sae " (trailing space), "idauth", "sae_ext", "fbt " (trailing space), "okc". `linux/brcmfmac/feature.c:37-50`
- linux — get — debugfs dump; it replaces every space with a newline to print one capability per line, and notes that the string usually ends with a space — `linux/brcmfmac/feature.c:270-284`
- The linux request carries the caller's buffer after the name: uninitialised stack in the first use, zeros in the second. `linux/brcmfmac/feature.c:233` `linux/brcmfmac/feature.c:266` `linux/brcmfmac/fwil.c:225-232`
- whd — get — reads the reply as a string and sets a `fwcap_flags` bit for each table substring found with `strstr` — `whd_wifi_read_fw_capabilities`, called from the init sequence, which only logs a failure and continues — `whd/src/whd_chip.c:1007-1018` `whd/src/whd_management.c:454-458`
- Substrings whd looks for, each with a trailing space: "sae ", "sae_ext ", "offloads ", "gcmp ", "icmp ". `whd/src/whd_chip.c:87-94`
- whd applies dtoh32 to the first 4 reply bytes before copying, which changes nothing on a little-endian host (inferred). `whd/src/whd_wifi_api.c:5208`
- whd macro `IOVAR_STR_CAP`. `whd/src/include/whd_wlioctl.h:1162`

Differences: linux matches "sae_ext" without a trailing space, whd matches "sae_ext " with one. `linux/brcmfmac/feature.c:47` `whd/src/whd_chip.c:90`

### `ccgpioin`
| | |
|---|---|
| Used by | c-driver, no "bsscfg:" prefix. Not found in embassy, linux, whd. `c-driver/cyw43_ll.c:2520-2521` |
| Direction | get `c-driver/cyw43_ll.c:2521` |
| Value | request is the 9-byte name with its NUL, command length 9; reply read as le32, 4 bytes `c-driver/cyw43_ll.c:2520-2526` |
| Record | plain integer `c-driver/cyw43_ll.c:2526` |

- c-driver — get — reads a le32 and tests bit `gpio_n` — input state of one chip GPIO — `c-driver/cyw43_ll.c:2520-2526`
- c-driver compiles this only with `CYW43_GPIO`, and reaches it from `cyw43_ctrl.c`. `c-driver/cyw43_ll.c:2500` `c-driver/cyw43_ctrl.c:808`
- The c-driver request has no bytes after the name's NUL. `c-driver/cyw43_ll.c:2520-2521`

### `chanspec`
| | |
|---|---|
| Used by | linux, whd; neither with a "bsscfg:" prefix. Not found in embassy, c-driver. `linux/brcmfmac/cfg80211.c:5390-5393` `whd/src/whd_wifi_api.c:582-597` |
| Direction | linux: both. whd: set. `linux/brcmfmac/cfg80211.c:5390-5393` `linux/brcmfmac/cfg80211.c:5864` `whd/src/whd_wifi_api.c:582-597` |
| Value | 16-bit chanspec carried in a 32-bit word, 4 bytes, little-endian, in both drivers `linux/brcmfmac/fwil.h:123-138` `whd/src/whd_wifi_api.c:586-589` |
| Record | plain integer `linux/brcmfmac/fwil.h:123-138` `whd/src/whd_wifi_api.c:586-589` |

- linux — set — chanspec — AP channel in `brcmf_cfg80211_start_ap`; the source says firmware 10.x needs it after enabling AP and before bringing the interface up — `linux/brcmfmac/cfg80211.c:5390-5393`
- linux — set — chanspec — P2P group-owner channel — `linux/brcmfmac/cfg80211.c:5459`
- linux — get — current chanspec — `brcmf_cfg80211_get_channel` — `linux/brcmfmac/cfg80211.c:5864`
- linux — set — chanspec built from the requested channel — `brcmf_set_channel` — `linux/brcmfmac/cfg80211.c:8348-8350`
- whd — set — `htod32((uint32_t)chanspec)` — `whd_wifi_set_chanspec`, STA or AP role only; any other role is rejected — `whd/src/whd_wifi_api.c:582-597`
- whd — set — `CH20MHZ_CHSPEC(chanspec)` through the same function — AP channel in `whd_wifi_init_ap` — `whd/src/whd_ap.c:420`
- whd — set — chanspec through the same function — join of an ad-hoc BSS — `whd/src/whd_wifi_api.c:2338-2340`
- whd's `wl_chanspec_t` is 16 bits and is widened to 32 on the wire. `whd/inc/whd_types.h:918` `whd/src/whd_wifi_api.c:589`
- whd macro `IOVAR_STR_CHANSPEC`. `whd/src/include/whd_wlioctl.h:1165`

### `chanspecs`
| | |
|---|---|
| Used by | linux, no "bsscfg:" prefix. Not found in embassy, whd, c-driver. `linux/brcmfmac/cfg80211.c:7232-7233` |
| Direction | get `linux/brcmfmac/cfg80211.c:7232-7233` |
| Value | 1536-byte buffer (`BRCMF_DCMD_MEDLEN`); reply is read as a count and a list of 32-bit entries, little-endian `linux/brcmfmac/cfg80211.c:7232-7233` `linux/brcmfmac/core.h:31` |
| Record | `struct brcmf_chanspec_list` { __le32 count @0; __le32 element[] @4 } `linux/brcmfmac/fwil_types.h:708-711` |

- linux — get — request buffer zeroed; reply read as the list of all supported chanspecs — `brcmf_construct_chaninfo` — `linux/brcmfmac/cfg80211.c:7225` `linux/brcmfmac/cfg80211.c:7230-7233`
- linux — get — first 2 request bytes = an encoded chanspec (2G band, 40 MHz, no sideband, channel 0) as a filter; reply read as the matching list — `brcmf_enable_bw40_2g`; the rest of the zeroed 1536-byte request buffer stays 0 — `linux/brcmfmac/cfg80211.c:7376` `linux/brcmfmac/cfg80211.c:7381-7391`

### `chip_serial`
| | |
|---|---|
| Used by | whd, no "bsscfg:" prefix. Not found in embassy, linux, c-driver. `whd/src/whd_chip.c:1893` |
| Direction | get `whd/src/whd_chip.c:1893` |
| Value | text in a caller-sized buffer; 200 bytes from the one caller found `whd/src/whd_chip.c:1893` `whd/src/whd_wifi_api.c:411` `whd/src/whd_wifi_api.c:426` |
| Record | character string, no record `whd/src/whd_chip.c:1893-1896` |

- whd — get — reads the reply as a C string — `whd_wifi_get_chip_serial` — `whd/src/whd_chip.c:1893-1896`
- whd calls it from `whd_wifi_set_up` right after `WLC_UP`, to print the string; `whd_wifi_set_up` runs in the init sequence. `whd/src/whd_wifi_api.c:424-429` `whd/src/whd_management.c:533`
- whd macro `IOVAR_STR_CHIP_SERIAL`. `whd/src/include/whd_wlioctl.h:1292`
- Content and format of the string: not shown by any driver; whd only prints it. `whd/src/whd_wifi_api.c:424-429`

### `clmload`
| | |
|---|---|
| Used by | embassy, linux, whd, c-driver; none with a "bsscfg:" prefix `embassy/control.rs:250-254` `linux/brcmfmac/common.c:193-194` `whd/src/whd_clm.c:133-140` `c-driver/cyw43_ll.c:1507-1522` |
| Direction | set in all four `embassy/control.rs:254` `linux/brcmfmac/common.c:114-115` `whd/src/whd_clm.c:133-140` `c-driver/cyw43_ll.c:1522` |
| Value | 12-byte header then CLM data. linux and whd convert the header fields to little-endian (whd leaves crc as a plain 0); embassy and c-driver write them in host byte order. Data per send: embassy up to 1024, linux up to 1400, whd up to 1024, c-driver up to 1024 (SPI) or 1536 (SDIO). `linux/brcmfmac/common.c:109-112` `whd/src/whd_clm.c:54-58` `embassy/structs.rs:12-14` `embassy/control.rs:252` `c-driver/cyw43_ll.c:1512-1515` `embassy/control.rs:229` `linux/brcmfmac/fwil_types.h:185` `whd/inc/whd_resource_api.h:35` `c-driver/cyw43_ll.c:1485-1489` |
| Record | embassy `DownloadHeader` `embassy/structs.rs:370-375`; linux `struct brcmf_dload_data_le` `linux/brcmfmac/fwil_types.h:1106-1112`; whd `wl_dload_data_t` `whd/src/include/whd_wlioctl.h:4167-4175`; c-driver has no named record, fields written at fixed offsets `c-driver/cyw43_ll.c:1512-1517`. Layout, the same in all four: flag u16 @0, dload_type u16 @2, len u32 @4, crc u32 @8, data @12. |

- embassy — set — flag = 0x1000 | 0x0002 on the first chunk | 0x0004 on the last; dload_type = 2; len = chunk length; crc = 0 — CLM blob download in `load_clm` — `embassy/control.rs:234-249` `embassy/structs.rs:379-385`
- embassy writes the name as the 8 bytes `clmload\0` itself and sends 8 + 12 + chunk length bytes, at most 1044. Chunk size = `MAX_IOCTL_LEN` - 8 - 12 = 1024. No padding. `embassy/control.rs:229` `embassy/control.rs:250-254` `embassy/ioctl.rs:17`
- linux — set — flag = (1 << 12) | 0x0002 first | 0x0004 last; dload_type = `DL_TYPE_CLM` (2); len = chunk length; crc = 0 — CLM blob download — `linux/brcmfmac/common.c:108-115` `linux/brcmfmac/common.c:193-194` `linux/brcmfmac/fwil_types.h:187-194`
- linux payload is 12 + chunk length, chunk at most `MAX_CHUNK_LEN` = 1400. No padding. `linux/brcmfmac/common.c:114-115` `linux/brcmfmac/common.c:144-149` `linux/brcmfmac/fwil_types.h:185`
- linux skips the download without error when the bus has no CLM blob. `linux/brcmfmac/common.c:186-191`
- whd — set — flag = (1 << 12) | `DL_BEGIN` 0x0002 first | `DL_END` 0x0004 last; dload_type = `DL_TYPE_CLM` (2); len = chunk length; crc = 0 — CLM blob download in `whd_process_clm_data`, called from the init sequence — `whd/src/whd_clm.c:53-58` `whd/src/whd_clm.c:133-140` `whd/src/include/whd_wlioctl.h:4154-4165` `whd/src/whd_management.c:435`
- whd chunk is at most `BLOCK_SIZE` = 1024 data bytes. Without `PROTO_MSGBUF` the payload length is changed to `len + 8 - (len % 8)`, which adds 1 to 8 bytes; a full chunk of 12 + 1024 = 1036 is sent as 1040. `whd/src/whd_clm.c:61-63` `whd/src/whd_clm.c:126-131` `whd/inc/whd_resource_api.h:35`
- whd copies the padded length out of a buffer allocated as 12 + 1024 bytes, so a full chunk's last 4 payload bytes come from past the end of that buffer (inferred). `whd/src/whd_clm.c:110` `whd/src/whd_clm.c:113` `whd/src/whd_clm.c:67`
- whd counts the bytes sent in a uint16_t and sets `DL_END` when that count plus the chunk equals the blob size. `whd/src/whd_clm.c:83` `whd/src/whd_clm.c:133-136`
- whd skips the download when the CLM resource has size 0. `whd/src/whd_clm.c:96-100`
- whd macro `IOVAR_STR_CLMLOAD`. `whd/src/include/whd_wlioctl.h:1231`
- c-driver — set — u16 @0 = (1 << 12) | 2 first | 4 last; u16 @2 = 2; u32 @4 = chunk length; u32 @8 = 0; then the data — CLM blob download at bus init — `c-driver/cyw43_ll.c:1499-1517` `c-driver/cyw43_ll.c:1915-1916`
- c-driver sends length = 8 (name) + 12 + chunk length, rounded up to a multiple of 8; its comment says the padding is junk from the end of its buffer. `c-driver/cyw43_ll.c:1520-1522`
- c-driver chunk size is 1024 with SPI, 1536 with SDIO. `c-driver/cyw43_ll.c:1485-1489`
- c-driver does not name the fields at offsets 2 and 8; the names dload_type and crc come from the other three drivers. `c-driver/cyw43_ll.c:1513-1515`

Differences: chunk size is 1024 in embassy and whd, 1400 in linux, 1024 or 1536 in c-driver `embassy/control.rs:229` `whd/inc/whd_resource_api.h:35` `linux/brcmfmac/fwil_types.h:185` `c-driver/cyw43_ll.c:1485-1489`. Padding: embassy and linux send the exact length; whd pads the payload to the next multiple of 8 strictly above its length; c-driver rounds name plus payload up to a multiple of 8 `embassy/control.rs:254` `linux/brcmfmac/common.c:114-115` `whd/src/whd_clm.c:62` `c-driver/cyw43_ll.c:1522`. The header field values do not differ `embassy/control.rs:234-249` `linux/brcmfmac/common.c:108-112` `whd/src/whd_clm.c:53-58` `c-driver/cyw43_ll.c:1499-1515`.

### `clmload_status`
| | |
|---|---|
| Used by | embassy, linux, whd, c-driver; none with a "bsscfg:" prefix `embassy/control.rs:259` `linux/brcmfmac/common.c:165` `whd/src/whd_clm.c:157-169` `c-driver/cyw43_ll.c:1527-1528` |
| Direction | get in all four `embassy/control.rs:259` `linux/brcmfmac/common.c:165` `whd/src/whd_clm.c:157-169` `c-driver/cyw43_ll.c:1528` |
| Value | embassy: u32, 4 bytes, little-endian. linux: u32, 4 bytes, little-endian. c-driver: u32, 4 bytes, read in host byte order. whd: 4-byte request buffer, only the first reply byte is read. `embassy/control.rs:706-711` `linux/brcmfmac/fwil.h:130-138` `c-driver/cyw43_ll.c:1531` `whd/src/whd_clm.c:157-169` |
| Record | plain integer `embassy/control.rs:706-711` `linux/brcmfmac/fwil.h:130-138` `c-driver/cyw43_ll.c:1531` `whd/src/whd_clm.c:157-169` |

- embassy — get — reads 4 bytes and asserts the value is 0 — after every CLM download — `embassy/control.rs:259` `embassy/control.rs:706-711`
- embassy's request is the name and NUL in a zeroed buffer, length = name length + 1 = 15 (larger than the 4-byte result). `embassy/control.rs:731-741`
- embassy's source comments on its get helper that it always returns zeros. `embassy/control.rs:730`
- linux — get — one 32-bit word, printed at debug level and not otherwise used — read only after a `clmload` chunk failed — `linux/brcmfmac/common.c:161-169` `linux/brcmfmac/common.c:193-194`
- linux's 4 request bytes after the name are the caller's uninitialised local `status`. `linux/brcmfmac/common.c:130` `linux/brcmfmac/fwil.c:225-232`
- whd — get — 4-byte request buffer left unwritten; prints the first reply byte — read only when the CLM download returned an error — `whd/src/whd_clm.c:148-170`
- whd macro `IOVAR_STR_CLMLOAD_STATUS`. `whd/src/include/whd_wlioctl.h:1232`
- c-driver — get — request is 19 bytes: the 14-character name and 5 zero bytes; reads the first 4 reply bytes as a u32 — after every CLM download — `c-driver/cyw43_ll.c:1527-1531`
- c-driver treats nonzero as failure but only prints a warning and continues. `c-driver/cyw43_ll.c:1531-1535`
- Meaning of nonzero values: not shown by any driver; each driver only compares the word with 0 or prints it. `embassy/control.rs:259` `c-driver/cyw43_ll.c:1531-1533` `linux/brcmfmac/common.c:161-169` `whd/src/whd_clm.c:148-170`

Differences: embassy and c-driver read it after every download and treat nonzero as failure; linux and whd read it only after a failed download and only print it `embassy/control.rs:259` `c-driver/cyw43_ll.c:1527-1533` `linux/brcmfmac/common.c:161-169` `whd/src/whd_clm.c:148-170`. Request length after the name's NUL: embassy 0 bytes, c-driver 4 zero bytes, linux 4 uninitialised bytes, whd 4 unwritten bytes `embassy/control.rs:738` `c-driver/cyw43_ll.c:1527-1528` `linux/brcmfmac/common.c:165` `whd/src/whd_clm.c:157`.

### `clmver`
| | |
|---|---|
| Used by | linux, whd, c-driver; none with a "bsscfg:" prefix. Not found in embassy. `linux/brcmfmac/common.c:386-402` `whd/src/whd_wifi_api.c:5325-5344` `c-driver/cyw43_ll.c:2028-2029` |
| Direction | get in all three `linux/brcmfmac/common.c:386-402` `whd/src/whd_wifi_api.c:5325-5344` `c-driver/cyw43_ll.c:2029` |
| Value | text. linux: 256-byte buffer. whd: caller-sized buffer, 200 bytes from the one caller found. c-driver: command length 128. `linux/brcmfmac/common.c:269` `linux/brcmfmac/core.h:30` `whd/src/whd_wifi_api.c:411` `whd/src/whd_wifi_api.c:444` `c-driver/cyw43_ll.c:2029` |
| Record | character string, no record `linux/brcmfmac/common.c:386-402` `whd/src/whd_wifi_api.c:5325-5344` `c-driver/cyw43_ll.c:2030` |

- linux — get — zeroed 256-byte buffer (`BRCMF_DCMD_SMLEN`) — forces a NUL at the end, replaces newlines with spaces, stores the string for the debugfs revinfo file — `linux/brcmfmac/common.c:269` `linux/brcmfmac/common.c:386-402` `linux/brcmfmac/core.h:30`
- linux tolerates failure of this get. `linux/brcmfmac/common.c:388-389`
- whd — get — reads the reply as a string and replaces newlines with spaces — `whd_wifi_get_clm_version` — `whd/src/whd_wifi_api.c:5325-5344`
- whd calls it from `whd_wifi_set_up` with a 200-byte buffer, to print the version; `whd_wifi_set_up` runs in the init sequence. `whd/src/whd_wifi_api.c:411` `whd/src/whd_wifi_api.c:444-446` `whd/src/whd_management.c:533`
- whd macro `IOVAR_STR_CLMVER`. `whd/src/include/whd_wlioctl.h:1233`
- c-driver — get — writes the 7 bytes `clmver\0`, command length 128; prints the reply as a string — wifi-on, only when `NDEBUG` is not defined — `c-driver/cyw43_ll.c:2026-2031`

Differences: buffer sizes 256 (linux), 200 (whd), 128 (c-driver). `linux/brcmfmac/common.c:269` `linux/brcmfmac/common.c:387` `whd/src/whd_wifi_api.c:411` `c-driver/cyw43_ll.c:2029`

### `closednet`
| | |
|---|---|
| Used by | linux, no "bsscfg:" prefix. Defined, not used by whd. Not found in embassy, c-driver. `linux/brcmfmac/cfg80211.c:5447-5449` `whd/src/include/whd_wlioctl.h:1105` |
| Direction | linux: set `linux/brcmfmac/cfg80211.c:5447-5449` |
| Value | linux: 32-bit integer, 4 bytes, little-endian `linux/brcmfmac/fwil.h:123-128` |
| Record | plain integer `linux/brcmfmac/fwil.h:123-128` |

- linux — set — 1 when the AP is configured with a hidden SSID, else 0 — `brcmf_cfg80211_start_ap`, AP role — `linux/brcmfmac/cfg80211.c:5447-5449`
- linux — set — 0 — `brcmf_cfg80211_stop_ap`, only for bsscfg index 0; the return value is not checked — `linux/brcmfmac/cfg80211.c:5538-5540`
- whd — macro `IOVAR_STR_CLOSEDNET`, no call site in any whd .c file — `whd/src/include/whd_wlioctl.h:1105`

### `clr`
| | |
|---|---|
| Used by | defined, not used by whd. Not found as a variable name in embassy, linux, c-driver. `whd/src/include/whd_wlioctl.h:1178` |
| Direction | not shown by any driver |
| Value | payload not shown by any driver |
| Record | not shown by any driver |

- whd — macro `IOVAR_STR_WOWL_PATTERN_CLR`, never referenced in any whd .c file — `whd/src/include/whd_wlioctl.h:1178`
- The literal "clr" does appear in whd and linux, as a wake-pattern sub-command word (compared with `strcmp` in whd, passed as a command argument in linux), not as a variable name. `whd/src/whd_wifi_api.c:6666` `linux/brcmfmac/cfg80211.c:4223`

### `counters`
| | |
|---|---|
| Used by | defined, not used by whd. Not found as a variable name in embassy, linux, c-driver. `whd/src/include/whd_wlioctl.h:1091` |
| Direction | not shown by any driver |
| Value | payload not shown by any driver |
| Record | not shown by any driver |

- whd — macro `IOVAR_STR_COUNTERS`, no call site in any whd .c file — `whd/src/include/whd_wlioctl.h:1091`
- The literal "counters" does appear in linux, as the name of a host debugfs entry for SDIO bus counters, not as a variable name sent to the chip. `linux/brcmfmac/sdio.c:3230-3231`

### `country`
| | |
|---|---|
| Used by | embassy, linux, whd, c-driver; none with a "bsscfg:" prefix `embassy/control.rs:284` `linux/brcmfmac/cfg80211.c:8484` `whd/src/whd_management.c:189-211` `c-driver/cyw43_ll.c:2014-2022` |
| Direction | embassy: set. linux: both. whd: both. c-driver: set. `embassy/control.rs:284` `linux/brcmfmac/cfg80211.c:8484` `linux/brcmfmac/cfg80211.c:8490-8494` `whd/src/whd_management.c:189-211` `whd/src/whd_wifi_api.c:7230-7234` `c-driver/cyw43_ll.c:2022` |
| Value | 12 bytes in all four: 4 bytes of country text, a signed 32-bit revision, 4 bytes of country text. Revision byte order: linux declares it __le32, c-driver writes le32; embassy sends the record's in-memory bytes; whd stores it in host order and applies htod32 only to the -1 case. `linux/brcmfmac/fwil_types.h:764-768` `c-driver/cyw43_ll.c:2015-2022` `embassy/structs.rs:12-14` `embassy/structs.rs:390-394` `whd/src/whd_management.c:189-209` |
| Record | embassy `CountryInfo` `embassy/structs.rs:390-394`; linux `struct brcmf_fil_country_le` `linux/brcmfmac/fwil_types.h:764-768`, array length `BRCMF_COUNTRY_BUF_SZ` = 4 `linux/brcmfmac/fwil_types.h:146`; whd `wl_country_t` `whd/src/include/whd_wlioctl.h:667-673`; c-driver has no named record, three le32 words `c-driver/cyw43_ll.c:2015-2021`. Layout, the same in all four: country_abbrev[4] @0, rev @4, ccode[4] @8 (embassy names the last field `country_code`). |

- embassy — set — country_abbrev and country_code = the two code letters then two zero bytes; rev = -1 when the configured rev is 0, else the configured rev — init, after reading the MAC address — `embassy/control.rs:278-284`
- embassy waits 100 ms after this set; its source says the following commands fail otherwise. `embassy/control.rs:286-287`
- linux — get — 12-byte record — `brcmf_cfg80211_reg_notifier` reads the current setting first — `linux/brcmfmac/cfg80211.c:8484`
- linux — set — the same record after `brcmf_translate_country_code` filled it from the regulatory request — regulatory-domain change — `linux/brcmfmac/cfg80211.c:8490-8494`
- linux documents rev = -1 on set as "unspecified", and both text fields as NUL-terminated. `linux/brcmfmac/fwil_types.h:760-762`
- whd — set — country_abbrev and ccode = low 16 bits of the country code (two letters, two zero bytes); rev = bits 16 to 31, replaced by -1 when 0; the two text fields are written as host-order uint32_t words, so the letter order given holds on a little-endian host (inferred) — `whd_wifi_set_country_code`, called from the init sequence — `whd/src/whd_management.c:189-211` `whd/src/whd_management.c:500`
- whd's source says rev -1 is used so the firmware picks the revision from NVRAM or OTP, and that this is the first command the chip must answer in its normal run mode. `whd/src/whd_management.c:179-181` `whd/src/whd_management.c:204-206`
- whd — get — zeroed 12-byte record; copies out the 4 bytes of country_abbrev — `whd_wifi_get_country_code` — `whd/src/whd_wifi_api.c:7230-7234`
- whd macro `IOVAR_STR_COUNTRY`. `whd/src/include/whd_wlioctl.h:1073`
- c-driver — set — le32 @0 = country & 0xffff; le32 @4 = country >> 16, or 0xFFFFFFFF when that is 0; le32 @8 = country & 0xffff; total length 20 with the 8-byte name — wifi-on — `c-driver/cyw43_ll.c:2014-2022`
- c-driver forces revision 17 for its worldwide country on non-SPI builds. `c-driver/cyw43_ll.c:2005-2011`
- c-driver waits 50 ms after this set; its comment says the set takes about 32 ms. `c-driver/cyw43_ll.c:2013` `c-driver/cyw43_ll.c:2024`

Differences: none in size or layout. Wait after the set: embassy 100 ms, c-driver 50 ms; no wait found at the linux or whd call sites. `embassy/control.rs:287` `c-driver/cyw43_ll.c:2024` `linux/brcmfmac/cfg80211.c:8494-8497` `whd/src/whd_management.c:211-213`

### `csa`
| | |
|---|---|
| Used by | whd, no "bsscfg:" prefix. Not found in embassy, linux, c-driver. `whd/src/whd_wifi_api.c:638-639` |
| Direction | set `whd/src/whd_wifi_api.c:649` |
| Value | `wl_chan_switch_t`, sent as `sizeof(wl_chan_switch_t)`, 6 bytes (computed); chspec is little-endian (htod16) `whd/src/whd_wifi_api.c:638-645` |
| Record | `wl_chan_switch_t` { uint8_t mode @0; uint8_t count @1; wl_chanspec_t chspec @2; uint8_t reg @4 } `whd/src/include/whd_wlioctl.h:3464-3470` |

- whd — set — mode = 1, count = 1, reg = 0, chspec = 20 MHz bandwidth | no sideband | channel | band bits — `whd_wifi_set_channel` in AP role: a channel switch announcement — `whd/src/whd_wifi_api.c:637-649`
- In STA role the same whd function sends the `WLC_SET_CHANNEL` command with a 32-bit channel number instead. `whd/src/whd_wifi_api.c:629-635`
- Record size is 6 bytes (computed): 5 bytes of fields plus 1 trailing pad under natural alignment, since the definition lies outside the header's two `#pragma pack(1)` regions. `whd/src/include/whd_wlioctl.h:3464-3470` `whd/inc/whd_types.h:918` `whd/src/include/whd_wlioctl.h:3864` `whd/src/include/whd_wlioctl.h:3918` `whd/src/include/whd_wlioctl.h:4188` `whd/src/include/whd_wlioctl.h:4289`
- whd does not write the pad byte at offset 5 at this call site. `whd/src/whd_wifi_api.c:640-648`
- whd macro `IOVAR_STR_CSA`. `whd/src/include/whd_wlioctl.h:1069`

### `csi`
| | |
|---|---|
| Used by | whd only, no "bsscfg:" prefix; only in the COMPONENT_WLANSENSE sources `whd/src/include/whd_wlioctl.h:1278` `whd/src/COMPONENT_WLANSENSE/whd_wlansense_api.c:113`. Not found in embassy, linux, c-driver |
| Direction | whd: both |
| Value | whd: `wlc_csi_cfg_t`, 48 bytes with natural alignment (compiled); fields written in host order with no conversion `whd/src/COMPONENT_WLANSENSE/whd_wlansense_api.c:115` |
| Record | `wlc_csi_cfg_t` `whd/src/include/whd_wlioctl.h:4573-4598` |

- whd — set — the caller's `wlc_csi_cfg_t` copied whole, after parameter validation — start CSI capture (`whd_wlansense_start_capture`), sent on the primary interface — `whd/src/COMPONENT_WLANSENSE/whd_wlansense_api.c:113-116`
- whd — set — `wlc_csi_cfg_t` filled with driver defaults and `csi_enable` = 0 — stop CSI capture — `whd/src/COMPONENT_WLANSENSE/whd_wlansense_api.c:152-158`
- whd — get — reply read into a 2048-byte buffer (`WLC_IOCTL_MEDLEN`) and the first `sizeof(wlc_csi_cfg_t)` bytes taken as `wlc_csi_cfg_t` — read back the CSI configuration — `whd/src/COMPONENT_WLANSENSE/whd_wlansense_core.c:325-327` `whd/src/include/whd_wlioctl.h:1300`

### `csi_ifadd`
| | |
|---|---|
| Used by | whd only, no "bsscfg:" prefix; only in the COMPONENT_WLANSENSE sources `whd/src/include/whd_wlioctl.h:1279`. Not found in embassy, linux, c-driver |
| Direction | whd: set |
| Value | whd: `wl_wlan_sense_if_t`, 6 bytes (one MAC address) `whd/src/include/whd_wlioctl.h:4600-4602` |
| Record | `wl_wlan_sense_if_t` `whd/src/include/whd_wlioctl.h:4600-4602`; `whd_mac_t` `whd/inc/whd_types.h:551-554` |

- whd — set — the STA MAC (read first with `cur_etheraddr`) with bit 0x02 of octet 0 toggled — add the CSI virtual interface (`whd_wlansense_create_interface`), sent on the primary interface — `whd/src/COMPONENT_WLANSENSE/whd_wlansense_core.c:288` `whd/src/COMPONENT_WLANSENSE/whd_wlansense_core.c:298-310`

### `cur_etheraddr`
| | |
|---|---|
| Used by | embassy, linux, whd, c-driver; all without "bsscfg:" prefix `embassy/control.rs:849` `linux/brcmfmac/common.c:227` `whd/src/include/whd_wlioctl.h:1078` `c-driver/cyw43_ll.c:1941` |
| Direction | embassy: get. linux: both. whd: both. c-driver: set; get only in builds with `CYW43_USE_OTP_MAC` (default 0) `c-driver/cyw43_config.h:127-128` |
| Value | 6 bytes, MAC address, byte array (no endianness) in every driver `embassy/control.rs:848-849` `linux/brcmfmac/common.c:227` `whd/inc/whd_types.h:551-554` `c-driver/cyw43_ll.c:1941` |
| Record | plain 6-byte array; whd names it `whd_mac_t` `whd/inc/whd_types.h:551-554` |

- embassy — get — 6 bytes read; the driver asserts the reply length is 6 — read the device MAC address (`address()`) — `embassy/control.rs:847-850`. The helper carries a source comment saying it "always returns all zeros" `embassy/control.rs:730-731`
- linux — set — 6 bytes (`ETH_ALEN`) — set the interface MAC (`brcmf_c_set_cur_etheraddr`); called at preinit when the host already holds a valid address — `linux/brcmfmac/common.c:227` `linux/brcmfmac/common.c:277-279`
- linux — get — 6 bytes read into `ifp->mac_addr` — read the MAC at preinit when the host has no valid one; if the reply equals 00:90:4c:c5:12:38 linux generates a random MAC and sets it — `linux/brcmfmac/common.c:284-285` `linux/brcmfmac/common.c:244-246` `linux/brcmfmac/common.c:291-295`
- whd — set — the given MAC with bit 0x02 of octet 0 toggled — `whd_wifi_set_mac_address` on an interface whose role is AP, so the AP differs from the STA — `whd/src/whd_wifi.c:74-92` `whd/src/whd_wifi.c:42`
- whd — set — the given MAC unchanged — `whd_wifi_set_mac_address` on a non-AP interface — `whd/src/whd_wifi.c:106-109`
- whd — get — 6-byte request area, not initialised; 6 bytes of the reply copied out — `whd_wifi_get_mac_address` — `whd/src/whd_wifi_api.c:3590-3594`. Callers: `whd_wifi_set_up` during init `whd/src/whd_wifi_api.c:432` `whd/src/whd_management.c:533`; soft-AP creation when the AP interface has no MAC yet `whd/src/whd_ap.c:310`; CSI interface creation `whd/src/COMPONENT_WLANSENSE/whd_wlansense_core.c:288`
- c-driver — set — 6 bytes — set the MAC at the end of bus init, only if a MAC is supplied or generated — `c-driver/cyw43_ll.c:1940-1942`
- c-driver — get — 20 bytes sent: the 13-character name, its NUL, then 6 zero bytes; first 6 bytes of the reply are the MAC — `cyw43_ll_wifi_get_mac` — `c-driver/cyw43_ll.c:2077-2080`. Both in-tree callers sit inside `#if CYW43_USE_OTP_MAC`: bus init, where a reply equal to 00:A0:50:b5:59:5e is treated as "not set" `c-driver/cyw43_ll.c:1925-1938`, and `c-driver/cyw43_ctrl.c:166-169`

Differences: request size of the get differs. embassy sends name + NUL only, 14 bytes (the larger of name length + 1 and the 6-byte result length) `embassy/control.rs:734-740`; c-driver sends name + NUL + 6 zero bytes (20 bytes) `c-driver/cyw43_ll.c:2077-2078`; whd reserves 6 uninitialised bytes after the name `whd/src/whd_wifi_api.c:3590`; linux sends name + NUL + the 6 bytes its buffer held `linux/brcmfmac/common.c:284-285` `linux/brcmfmac/fwil.c:226-232`. The "default MAC" each driver tests for also differs: linux 00:90:4c:c5:12:38 `linux/brcmfmac/common.c:244-246`, c-driver 00:A0:50:b5:59:5e `c-driver/cyw43_ll.c:1928`.

### `dltro`
| | |
|---|---|
| Used by | defined, not used by whd (`IOVAR_STR_DLTRO`) `whd/src/include/whd_wlioctl.h:1246`. Not found in embassy, linux, c-driver |
| Direction | not shown by any driver |
| Value | payload not shown by any driver |
| Record | none shown |

### `dump`
| | |
|---|---|
| Used by | whd only, no "bsscfg:" prefix; only under `CYCFG_ULP_SUPPORT_ENABLED` `whd/src/include/whd_wlioctl.h:1185` `whd/src/whd_wifi_api.c:6804` `whd/src/whd_wifi_api.c:6824`. Not found in embassy, linux, c-driver |
| Direction | whd: get |
| Value | whd: request is the name, a NUL, then an ASCII sub-name parameter; reply is text in the caller's buffer `whd/src/whd_wifi_api.c:5219-5240` `whd/src/whd_wifi_api.c:6824` |
| Record | none (text) |

- whd — get — caller buffer of `buflen` bytes zeroed, then "dump" at offset 0, NUL at offset 4 (left by the zeroing; the helper copies the name without its NUL), parameter string placed from offset 5 with length `strlen(param)`; the whole `buflen` bytes are sent as a `WLC_GET_VAR` command; reply copied back as text — read ULP (deep sleep) statistics (`whd_wifi_get_deepsleep_stats`); the parameter is "ulpstats" (8 bytes) — `whd/src/whd_wifi_api.c:6810` `whd/src/whd_wifi_api.c:6819-6824` `whd/src/whd_wifi_api.c:5232-5237` `whd/src/whd_wifi_api.c:5263-5270`
- whd — get — same call, reached from the SDIO bus statistics print when a deep-sleep callback is registered — `whd/src/bus_protocols/whd_bus_sdio_protocol.c:1410-1413`

### `dump_obss`
| | |
|---|---|
| Used by | linux only, no "bsscfg:" prefix `linux/brcmfmac/cfg80211.c:8320` `linux/brcmfmac/feature.c:335`. Not found in embassy, whd, c-driver |
| Direction | linux: get |
| Value | linux: request `struct cca_msrmnt_query`, 8 bytes, two u32 in host order (no conversion), at the start of a 1536-byte buffer; reply `struct cca_stats_n_flags`: u32 `msrmnt_time`, u32 `msrmnt_done`, then text `linux/brcmfmac/cfg80211.c:117-126` `linux/brcmfmac/cfg80211.c:8315-8321` `linux/brcmfmac/core.h:31` |
| Record | `struct cca_msrmnt_query` `linux/brcmfmac/cfg80211.c:123-126`; `struct cca_stats_n_flags` `linux/brcmfmac/cfg80211.c:117-121` |

- linux — get — 1536-byte buffer (`BRCMF_DCMD_MEDLEN`) with the 8-byte query copied to its start; reply parsed as time, done flag and text — channel-busy measurement for the survey dump (`brcmf_dump_obss`) — `linux/brcmfmac/cfg80211.c:8315-8321`
- linux — get — 4-byte buffer holding an uninitialised local u32; reply value discarded — feature probe: `BRCMF_FEAT_DUMP_OBSS` is enabled unless the reply is the "unsupported" error — `linux/brcmfmac/feature.c:335` `linux/brcmfmac/feature.c:190-199`

### `dutycycle_cck`
| | |
|---|---|
| Used by | defined, not used by whd (`IOVAR_STR_DUTY_CYCLE_CCK`) `whd/src/include/whd_wlioctl.h:1099`. Not found in embassy, linux, c-driver |
| Direction | not shown by any driver |
| Value | payload not shown by any driver |
| Record | none shown |

### `dutycycle_ofdm`
| | |
|---|---|
| Used by | defined, not used by whd (`IOVAR_STR_DUTY_CYCLE_OFDM`) `whd/src/include/whd_wlioctl.h:1100`. Not found in embassy, linux, c-driver |
| Direction | not shown by any driver |
| Value | payload not shown by any driver |
| Record | none shown |

### `escan`
| | |
|---|---|
| Used by | embassy, linux, whd, c-driver; all without "bsscfg:" prefix `embassy/control.rs:835` `linux/brcmfmac/cfg80211.c:1491` `whd/src/whd_wifi_api.c:3320` `c-driver/cyw43_ll.c:2202` |
| Direction | set in all four |
| Value | embassy: `ScanParams`, 76 bytes, struct memory sent as-is (`to_bytes` is a transmute), so host order `embassy/structs.rs:4-14`. c-driver: `cyw43_wifi_scan_options_t`, 76 bytes, fields written in host order `c-driver/cyw43_ll.c:2191-2202`. whd: `wl_escan_params_t`, 72 + 2 x channel count bytes to start, 76 bytes to abort, little-endian (`htod32`/`htod16`) `whd/src/whd_wifi_api.c:3264` `whd/src/whd_wifi_api.c:3405-3413`. linux: `struct brcmf_escan_params_le`, variable, little-endian: 8 + 72 (version 2) or 8 + 64 (version 1) fixed bytes, plus 4 x ((n_channels + 1) / 2), plus one `brcmf_ssid_le` per SSID `linux/brcmfmac/cfg80211.c:1447-1459` `linux/brcmfmac/fwil_types.h:50-51` |
| Record | embassy `ScanParams` `embassy/structs.rs:454-469`; c-driver `cyw43_wifi_scan_options_t` `c-driver/cyw43_ll.h:255-270`; whd `wl_escan_params_t` `whd/src/include/whd_wlioctl.h:548-554` wrapping `wl_scan_params_t` `whd/src/include/whd_wlioctl.h:506-518`; linux `struct brcmf_escan_params_le` `linux/brcmfmac/fwil_types.h:460-468` |

- embassy — set — `ScanParams`: version u32 @0 = 1, action u16 @4 = 1, sync_id u16 @6 = 1, ssid_len u32 @8 (0 if none), ssid [32] @12 zero-padded, bssid [6] @44 (ff x6 if unset), bss_type u8 @50 = 2, scan_type u8 @51 (0 active, 1 passive), nprobes u32 @52 (65535 (0x0000FFFF) if unset: a u16 all-ones widened), active_time u32 @56, passive_time u32 @60 (the one matching scan_type gets the dwell time in ms, capped at 0xFFFFFFFE; otherwise 0xFFFFFFFF), home_time u32 @64 (ms, 0xFFFFFFFF if unset), channel_num u32 @68 = 0, channel_list [u16;1] @72 = 0, 2 bytes tail padding (offsets and size 76 computed from the `repr(C)` layout) — start an event-driven scan; the driver enables ESCAN_RESULT in its own filter first — `embassy/control.rs:780-835` `embassy/structs.rs:454-469`
- c-driver — set — `cyw43_wifi_scan_options_t`, `sizeof` = 76 (computed): version = 1, action = 1, `_` = 0, bssid = ff x6, bss_type = 2, nprobes / active_time / passive_time / home_time = -1, channel_num = 0, channel_list[0] = 0; ssid_len, ssid and scan_type come from the caller — start a scan — `c-driver/cyw43_ll.c:2191-2202` `c-driver/cyw43_ll.h:255-270`
- whd — set — `wl_escan_params_t`, size = offsetof(params) + 64 + channel-list bytes: version = 1, action = 1 (`WL_SCAN_ACTION_START`), sync_id left 0 by the memset, scan_type and bss_type from the caller; SSID length and bytes if an SSID is given; bssid from the caller or ff x6; nprobes, active_time, passive_time, home_time from the extended parameters or all -1; channel_list entries = `CH20MHZ_CHSPEC(channel)` and channel_num = count when a channel list is given, else left 0 — start a scan (`whd_wifi_scan`) — `whd/src/whd_wifi_api.c:3264` `whd/src/whd_wifi_api.c:3320-3389` `whd/src/include/whd_wlioctl.h:519-524` `whd/src/include/whd_wlioctl.h:547`
- whd — set — `sizeof(wl_escan_params_t)` bytes zeroed, version = 1, action = 3 (`WL_SCAN_ACTION_ABORT`) — abort a scan (`whd_wifi_stop_scan`) — `whd/src/whd_wifi_api.c:3405-3416`
- linux — set — `struct brcmf_escan_params_le`: version = 2 with the v2 parameter block, or version = 1 with the v1 block when feature `BRCMF_FEAT_SCAN_V2` is off; action = 1 (`WL_ESCAN_ACTION_START`); sync_id = 4660 (0x1234) — start a scan (`brcmf_run_escan`) — `linux/brcmfmac/cfg80211.c:1447-1491` `linux/brcmfmac/fwil_types.h:50-51` `linux/brcmfmac/fwil_types.h:73-74` `linux/brcmfmac/cfg80211.h:51`

Differences: sync_id is 1 in embassy `embassy/control.rs:807`, 0 in c-driver `c-driver/cyw43_ll.c:2193`, 0 in whd (memset, never assigned) `whd/src/whd_wifi_api.c:3324`, 4660 (0x1234) in linux `linux/brcmfmac/cfg80211.c:1489`. Unset nprobes is 0x0000FFFF in embassy `embassy/control.rs:820` and -1 (0xFFFFFFFF) in c-driver `c-driver/cyw43_ll.c:2196`. embassy and c-driver always send channel_num = 0 with one zero channel entry (76 bytes) `embassy/control.rs:824-825` `c-driver/cyw43_ll.c:2200-2202`; whd and linux size the record by the channel list `whd/src/whd_wifi_api.c:3264` `linux/brcmfmac/cfg80211.c:1454-1459`. Only linux sends a version 2 layout `linux/brcmfmac/cfg80211.c:1470-1472`. Only whd is shown sending an abort action `whd/src/whd_wifi_api.c:3413`.

### `event_log_tag_control`
| | |
|---|---|
| Used by | whd only, no "bsscfg:" prefix (`IOVAR_STR_EVENT_LOG`) `whd/src/include/whd_wlioctl.h:1272` `whd/src/whd_wifi_api.c:6593`. Not found in embassy, linux, c-driver |
| Direction | whd: set |
| Value | whd: `wl_el_tag_params_s_t`, 4 bytes: u16 tag, u8 set, u8 flags; host order, no conversion `whd/src/whd_wifi_api.c:355-359` `whd/src/whd_wifi_api.c:6592-6595` |
| Record | `wl_el_tag_params_s_t` `whd/src/whd_wifi_api.c:355-359` |

- whd — set — one 4-byte record per tag: tag from a fixed table, set = 1, flags = 192 (0xC0, `EVTLOG_LOG_AND_PRINT_MODE`) — enable event-log tags for a category (`whd_wifi_enable_event_log`) — `whd/src/whd_wifi_api.c:6565-6595` `whd/src/whd_wifi_api.c:112`. The loop runs from the category's start index while the index is below the category's count, with pairs {0,6},{6,4},{10,2},{12,2},{14,3},{17,1},{18,2},{20,2}; as written only category 0 sends anything: tags 28, 29, 30, 31, 113, 128 (inferred from the source) `whd/src/whd_wifi_api.c:6567-6568` `whd/src/whd_wifi_api.c:6586-6590`

### `event_msgs`
| | |
|---|---|
| Used by | embassy: "bsscfg:event_msgs" only `embassy/control.rs:319`. c-driver: "bsscfg:event_msgs" only `c-driver/cyw43_ll.c:2059`. whd: plain at init `whd/src/whd_management.c:516-517` and "bsscfg:event_msgs" for handler registration `whd/src/whd_events.c:290-291`. linux: plain only `linux/brcmfmac/common.c:415` `linux/brcmfmac/fweh.c:462` |
| Direction | embassy: set. c-driver: set. whd: set. linux: both |
| Value | Bitmask, bit (n mod 8) of byte (n / 8) = event n, preceded by a 4-byte bsscfg index in the prefixed form. embassy: 4 + 24 bytes `embassy/structs.rs:437-447`. c-driver: 4 + 19 bytes `c-driver/cyw43_ll.c:2051-2060`. whd: 16 bytes plain `whd/src/whd_management.c:516-517`, 4 + 16 bytes prefixed `whd/src/whd_events.c:290-291`. linux: no index, `event_mask_len` = ceil(num_event_codes / 8) bytes, set per vendor module `linux/brcmfmac/fweh.c:356`: 197 for CYW, giving 25 bytes `linux/brcmfmac/cyw/core.c:21` `linux/brcmfmac/cyw/core.c:73`; 213 for WCC, giving 27 bytes `linux/brcmfmac/wcc/core.c:14` `linux/brcmfmac/wcc/core.c:31` (byte counts computed). The two 43439 SDIO ids map to WCC and CYW `linux/brcmfmac/bcmsdh.c:993` `linux/brcmfmac/bcmsdh.c:1004` |
| Record | embassy `EventMask` `embassy/structs.rs:437-441`; others a plain byte array, length constant `WL_EVENTING_MASK_LEN` = 16 in whd `whd/src/include/whd_wlioctl.h:1932`, computed length in linux `linux/brcmfmac/fweh.c:356` |

- embassy — set ("bsscfg:" form) — `EventMask`, 28 bytes: u32 index = 0, then 24 mask bytes all 0xFF except events RADIO, IF, PROBREQ_MSG, PROBREQ_MSG_RX, PROBRESP_MSG, ROAM cleared (numbers 40, 54, 44, 137, 71, 19) — set the event mask at init — `embassy/control.rs:305-319` `embassy/structs.rs:437-448` `embassy/events.rs:56` `embassy/events.rs:92` `embassy/events.rs:100` `embassy/events.rs:117` `embassy/events.rs:150` `embassy/events.rs:266`
- c-driver — set ("bsscfg:" form) — 41 bytes: 18 bytes name with NUL, 4 index bytes, 19 mask bytes all 0xFF except bits 20, 40, 44, 54, 71 cleared — set a mask with every bit but five, in `cyw43_ll_wifi_on` — `c-driver/cyw43_ll.c:2051-2060`. The 4 index bytes are not written by this code: the fill starts after them and the name copy stops before them, so they hold whatever the shared buffer held (the command path copies each reply back over the request buffer) `c-driver/cyw43_ll.c:2051` `c-driver/cyw43_ll.c:2059` `c-driver/cyw43_ll.c:1312`
- c-driver — set ("bsscfg:" form), commented out, never compiled — 4 zero index bytes + an 18-byte mask — restrict events to a short list — `c-driver/cyw43_ll.c:2291-2294`
- whd — set (plain form) — 16 bytes, all zero — init, all-zero mask, which a source comment describes as wanting no asynchronous events initially; retried up to 3 times (`MAX_POST_SET_COUNTRY_RETRY`) — `whd/src/whd_management.c:513-524` `whd/src/whd_management.c:52`
- whd — set ("bsscfg:" form) — 20 bytes: u32 `ifp->bsscfgidx` in host order (no `htod32`), then a 16-byte mask with one bit set for every event of every registered handler — set the event mask from the registered handlers; used only when no registered event number exceeds 127 (otherwise `event_msgs_ext`); sent on the primary interface — `whd/src/whd_events.c:266-300` `whd/src/whd_events.c:409-421` `whd/src/whd_events.c:505-517`
- linux — get (plain form) — mask of `event_mask_len` bytes read — read the current mask at preinit before adding the interface event — `linux/brcmfmac/common.c:415-416`
- linux — set (plain form) — the same mask with the `BRCMF_E_IF` bit set — write the mask back — `linux/brcmfmac/common.c:427-429`
- linux — set (plain form) — mask with a bit for every event that has a handler, plus `BRCMF_E_IF` — activate events; sent whenever the vendor hook returns non-zero, which covers vendors with no hook and a failed `event_msgs_ext` — `linux/brcmfmac/fweh.c:444-463` `linux/brcmfmac/fwvid.h:73-81`

Differences: prefix — embassy and c-driver send only "bsscfg:event_msgs" `embassy/control.rs:319` `c-driver/cyw43_ll.c:2059`; linux sends only the plain name `linux/brcmfmac/fweh.c:462`; whd sends both `whd/src/whd_management.c:517` `whd/src/whd_events.c:291`. Mask length — 24 bytes in embassy `embassy/structs.rs:439`, 19 in c-driver `c-driver/cyw43_ll.c:2051`, 16 in whd `whd/src/include/whd_wlioctl.h:1932`, 25 or 27 in linux `linux/brcmfmac/fweh.c:356`. Policy — embassy and c-driver enable everything and clear a few bits `embassy/control.rs:305-317` `c-driver/cyw43_ll.c:2051-2057`; whd and linux start from zero and set only handled events `whd/src/whd_events.c:409-419` `linux/brcmfmac/fweh.c:444-456`. Index word — 0 in embassy `embassy/control.rs:306`, interface index in whd `whd/src/whd_events.c:298`, not written in c-driver `c-driver/cyw43_ll.c:2051-2059`.

### `event_msgs_ext`
| | |
|---|---|
| Used by | linux (CYW vendor module only): plain name `linux/brcmfmac/cyw/core.c:95`. whd: "bsscfg:event_msgs_ext" `whd/src/whd_events.c:304-308`. Not found in embassy, c-driver |
| Direction | set in both |
| Value | linux: 4-byte header + mask, 4 + `event_mask_len` bytes (29 with the 25-byte CYW mask, computed). whd: u32 bsscfg index + 4-byte header + mask; buffer size 4 + `sizeof(eventmsgs_ext_t)` + mask_len. All header fields are single bytes `linux/brcmfmac/cyw/core.c:86` `whd/src/whd_events.c:304-307` |
| Record | linux `struct brcmf_eventmsgs_ext` `linux/brcmfmac/cyw/fwil_types.h:31-37`; whd `eventmsgs_ext_t` `whd/src/include/whd_wlioctl.h:1056-1063`. Both: u8 ver, u8 command, u8 len, u8 maxgetsize, then the mask. Command values 0 (none), 1 (set bit), 2 (reset bit) are defined in both headers and not used by either driver `linux/brcmfmac/cyw/fwil_types.h:11-16` `whd/src/include/whd_wlioctl.h:1045-1048` |

- linux — set (plain form) — ver = 1 (`EVENTMSGS_VER`), command = 3 (`CYW_EVENTMSGS_SET_MASK`), len = `event_mask_len`, maxgetsize = 0 (zeroed allocation), then the event mask — activate events in the CYW vendor module; when this returns 0 the plain `event_msgs` set is skipped, when it fails linux falls back to `event_msgs` — `linux/brcmfmac/cyw/core.c:79-98` `linux/brcmfmac/cyw/fwil_types.h:11-18` `linux/brcmfmac/fweh.c:458-463`
- whd — set ("bsscfg:" form) — u32 `ifp->bsscfgidx` in host order, then ver = 1, command = 3 (`EVENTMSGS_SET_MASK`), len = mask_len, maxgetsize = 0, then the mask; mask_len = (highest registered event number + 8) / 8 — used when any registered event number exceeds 127 — `whd/src/whd_events.c:266-323` `whd/src/include/whd_wlioctl.h:1045-1050`. The record is declared with `mask[1]`, so `sizeof(eventmsgs_ext_t)` is 5 and the buffer is one byte longer than index + header + mask `whd/src/include/whd_wlioctl.h:1056-1063` `whd/src/whd_events.c:306-307`. The callers zero only 16 mask bytes before setting bits, although mask_len is at least 17 on this path `whd/src/whd_events.c:409` `whd/src/whd_events.c:505`

Differences: linux sends the plain name with no index word `linux/brcmfmac/cyw/core.c:95`; whd sends "bsscfg:event_msgs_ext" with a 4-byte index before the header `whd/src/whd_events.c:308` `whd/src/whd_events.c:315`. linux sizes the mask from the vendor's event count `linux/brcmfmac/cyw/core.c:86` `linux/brcmfmac/fweh.c:356`; whd sizes it from the highest registered event `whd/src/whd_events.c:304`. A linux header comment spells the name "eventmsgs_ext"; the string sent is "event_msgs_ext" `linux/brcmfmac/cyw/fwil_types.h:22` `linux/brcmfmac/cyw/core.c:95`.

### `extsae_pwe`
| | |
|---|---|
| Used by | linux only (CYW vendor module), no "bsscfg:" prefix `linux/brcmfmac/cyw/core.c:375`. Not found in embassy, whd, c-driver |
| Direction | linux: set |
| Value | linux: u32, 4 bytes, little-endian `linux/brcmfmac/fwil.h:123-127` |
| Record | plain integer |

- linux — set — 0, 1 or 2, which a source comment labels hunting-and-pecking only, H2E only, both; linux derives it from the RSNX and rate elements of the AP beacon it was given: 2 if the RSNX element has the SAE H2E bit, 1 if in addition a rate element carries the H2E-only membership selector, else 0 — set the SAE password-element method value for an AP; sent only when feature `BRCMF_FEAT_SAE_EXT` is on and the `wpa_auth` read back has the SAE bit; reaches this name through the CYW vendor hook `configure_sae_pwe` — `linux/brcmfmac/cfg80211.c:5138-5202` `linux/brcmfmac/fwvid.h:44-51` `linux/brcmfmac/cyw/core.c:373-376` `linux/brcmfmac/cyw/core.c:384`

### `fbt_cap`
| | |
|---|---|
| Used by | defined, not used by whd (`IOVAR_STR_FBT_CAPABILITIES`) `whd/src/include/whd_wlioctl.h:1224`. Not found in embassy, linux, c-driver |
| Direction | not shown by any driver |
| Value | payload not shown by any driver |
| Record | none shown |

### `fbtoverds`
| | |
|---|---|
| Used by | defined, not used by whd (`IOVAR_STR_FBT_OVER_DS`) `whd/src/include/whd_wlioctl.h:1223`. Not found in embassy, linux, c-driver |
| Direction | not shown by any driver |
| Value | payload not shown by any driver |
| Record | none shown |

### `fragthresh`
| | |
|---|---|
| Used by | linux only, no "bsscfg:" prefix `linux/brcmfmac/cfg80211.c:1618`. Not found in embassy, whd, c-driver |
| Direction | linux: set |
| Value | linux: u32, 4 bytes, little-endian `linux/brcmfmac/fwil.h:123-127` |
| Record | plain integer |

- linux — set — the fragmentation threshold passed in by cfg80211 — `brcmf_set_frag` — `linux/brcmfmac/cfg80211.c:1612-1619`

### `gpioout`
| | |
|---|---|
| Used by | embassy and c-driver, no "bsscfg:" prefix `embassy/control.rs:512` `c-driver/cyw43_ll.c:2508`. Not found in linux, whd |
| Direction | set in both |
| Value | two u32, 8 bytes, little-endian: mask, then value `c-driver/cyw43_ll.c:1546-1552` `embassy/control.rs:695-699` |
| Record | plain integers (two) |

- embassy — set — mask = 1 << gpio_n, value = 1 << gpio_n if on, else 0; gpio_n asserted below 3 — drive a GPIO pin of the radio chip (`gpio_set`) — `embassy/control.rs:510-513`
- c-driver — set — mask = 1 << gpio_n, value = 1 << gpio_n if on, else 0; gpio_n checked against `CYW43_NUM_GPIOS` — set a chip GPIO output (`cyw43_ll_gpio_set`); compiled only with `CYW43_GPIO` — `c-driver/cyw43_ll.c:2500-2508` `c-driver/cyw43_config.h:131-132`

### `gtk_key_info`
| | |
|---|---|
| Used by | linux only, no "bsscfg:" prefix `linux/brcmfmac/cfg80211.c:6055`. Not found in embassy, whd, c-driver |
| Direction | linux: set |
| Value | linux: `struct brcmf_gtk_keyinfo_le`, 40 bytes: kck[16], kek[16], replay_counter[8]; byte arrays `linux/brcmfmac/fwil_types.h:1149-1153` `linux/brcmfmac/fwil_types.h:165-167` |
| Record | `struct brcmf_gtk_keyinfo_le` `linux/brcmfmac/fwil_types.h:1149-1153` |

- linux — set — KCK, KEK and replay counter copied from the cfg80211 rekey data — GTK rekey offload (`brcmf_cfg80211_set_rekey_data`) — `linux/brcmfmac/cfg80211.c:6050-6056`

### `he`
| | |
|---|---|
| Used by | whd only, no "bsscfg:" prefix (`IOVAR_STR_HE`) `whd/src/include/whd_wlioctl.h:1268` `whd/src/whd_wifi_api.c:4399`. Not found in embassy, linux, c-driver |
| Direction | whd: both |
| Value | whd: sub-command header u16 id, u16 len (host order, no conversion), then data from offset 4. OMI set: buffer `sizeof(wl_he_omi_t)` + 4 = 13 bytes. BSS colour get/set: buffer `sizeof(whd_xtlv_t)` + 2 = 8 bytes (`sizeof` values 9 and 6, computed) `whd/src/whd_wifi_api.c:4398-4403` `whd/src/whd_wifi_api.c:4880-4885` |
| Record | `whd_xtlv_t` `whd/src/include/whd_wlioctl.h:450-455`; `wl_he_omi_t` = `wl_he_omi_v1_t` `whd/src/include/whd_wlioctl.h:138-152` |

- whd — set — id = 13 (`WL_HE_CMD_OMI`), len = `sizeof(wl_he_omi_t)`, data = `wl_he_omi_t`: version = 1, length = sizeof - 2, rx_nss, chnl_wdth, ul_mu_dis, tx_nsts, er_su_dis, dl_mu_resound, ul_mu_data_dis (one byte each) — send an HE operating mode indication (`whd_wifi_he_omi`) — `whd/src/whd_wifi_api.c:4388-4404` `whd/src/include/whd_wlioctl.h:129` `whd/src/include/whd_wlioctl.h:137` `whd/src/include/whd_wlioctl.h:151`
- whd — get — id = 5 (`WL_HE_CMD_BSSCOLOR`), len = 1; 1 byte of the reply is used — read the BSS colour — `whd/src/whd_wifi_api.c:4880-4894` `whd/src/include/whd_wlioctl.h:127`
- whd — set — id = 5, len = 1, data[0] = colour — set the BSS colour — `whd/src/whd_wifi_api.c:4909-4916`

### `ibss_join_only`
| | |
|---|---|
| Used by | defined, not used by whd (`IOVAR_STR_IBSS_JOIN`); the string in the header is "IBSS_join_only" with upper-case "IBSS" `whd/src/include/whd_wlioctl.h:1124`. Not found in embassy, linux, c-driver |
| Direction | not shown by any driver |
| Value | payload not shown by any driver |
| Record | none shown |

### `icmp_echo_req`
| | |
|---|---|
| Used by | whd only, no "bsscfg:" prefix (`IOVAR_STR_ICMP_ECHO_REQ`) `whd/src/include/whd_wlioctl.h:1289` `whd/src/whd_wifi_api.c:6955`. Not found in embassy, linux, c-driver |
| Direction | whd: both (get only for the INFO sub-command) `whd/src/whd_wifi_api.c:6962-6975` |
| Value | whd: 8-byte header `wl_icmp_echo_req_cmd_t` (u16 version, u16 length, u8 cmd_type, 3 pad) + sub-command data; host order, no conversion. Data sizes (computed): enable 1 byte, peer config 40, peer ip 24, get-peer-info 44 `whd/src/include/whd_wlioctl.h:4669-4675` `whd/src/whd_wifi_api.c:6957-6960` |
| Record | `wl_icmp_echo_req_cmd_t` `whd/src/include/whd_wlioctl.h:4669-4675`; `wl_icmp_echo_req_peer_ip_t` `whd/src/include/whd_wlioctl.h:4677-4686`; `wl_icmp_echo_req_peer_config_t` `whd/src/include/whd_wlioctl.h:4688-4700`; `wl_icmp_echo_req_get_peer_info_t` `whd/src/include/whd_wlioctl.h:4703-4706`; `wl_icmp_echo_req_get_info_t` `whd/src/include/whd_wlioctl.h:4708-4715` |

- whd — set — header with version = 1, length = whole buffer length, cmd_type; data: ENAB (0) one enable byte; ADD (1) `wl_icmp_echo_req_peer_config_t`; DEL (2), START (3), STOP (4) `wl_icmp_echo_req_peer_ip_t` — configure the periodic ICMP echo request offload; the function returns "unsupported" without sending (set or get) unless the capability flags whd holds include `WHD_FWCAP_ICMP` `whd/src/whd_wifi_api.c:6917-6920` — `whd/src/whd_wifi_api.c:6922-6964` `whd/src/include/whd_wlioctl.h:4656` `whd/src/include/whd_wlioctl.h:4659-4666`
- whd — get — same header with cmd_type INFO (5) and a `wl_icmp_echo_req_peer_ip_t` copied in; buffer sized 8 + `sizeof(wl_icmp_echo_req_get_peer_info_t)` (52 with the 44-byte size above); reply read as `wl_icmp_echo_req_get_info_t` followed by peer info — read the offload state for a peer — `whd/src/whd_wifi_api.c:6936-6975`

### `interface_create`
| | |
|---|---|
| Used by | linux only. Record forms: plain name `linux/brcmfmac/cfg80211.c:631`. Version query: sent through the bsscfg helper `linux/brcmfmac/cfg80211.c:666`, which builds the plain name when the interface's bsscfg index is 0 and "bsscfg:interface_create" + NUL + u32 little-endian index + value otherwise `linux/brcmfmac/fwil.c:249-291` `linux/brcmfmac/fwil.c:333-334`. Not found in embassy, whd, c-driver |
| Direction | linux: get in every use, including the ones that create an interface (the record is the input buffer of a get) `linux/brcmfmac/cfg80211.c:631-633` |
| Value | linux: `struct wl_interface_create_v1`, `_v2` or `_v3`; sizes 20, 20, 28 bytes with natural alignment (compiled; the same when computed from the definitions); fields in host order, no conversion. Version query: u32, 4 bytes, little-endian, input value 0 `linux/brcmfmac/cfg80211.c:282-311` `linux/brcmfmac/fwil.h:172-178`. The same name carries three record layouts and a bare u32 query: linux tries v1, then v2, then asks for the version and sends v3 `linux/brcmfmac/cfg80211.c:622-686` |
| Record | `struct wl_interface_create_v1` `linux/brcmfmac/cfg80211.c:282-287`; `_v2` `linux/brcmfmac/cfg80211.c:289-297`; `_v3` `linux/brcmfmac/cfg80211.c:299-311` |

- linux — get — v1 record: ver = 1, flags = STA (0x0) | MAC_USE (0x2), mac_addr set — create a STA interface, first attempt — `linux/brcmfmac/cfg80211.c:622-633` `linux/brcmfmac/cfg80211.c:271-280`
- linux — get — v2 record: ver = 2, flags = MAC_USE (0x2), iftype = STA (0x0), mac_addr set — retry when v1 failed — `linux/brcmfmac/cfg80211.c:643-654`
- linux — get — u32 query, input 0; linux reads the reply as the interface_create version — sent when v1 and v2 both failed — `linux/brcmfmac/cfg80211.c:664-667`
- linux — get — v3 record: ver = 3, flags = MAC_USE, iftype = STA, mac_addr set; `len` and `fixed_len` stay 0 from the memset — used when the query returns 3 — `linux/brcmfmac/cfg80211.c:674-686`
- linux — get — v1 record: ver = 1, flags = AP (0x1) | MAC_USE (0x2) — create an AP interface, first attempt — `linux/brcmfmac/cfg80211.c:722-728`
- linux — get — v2 record: ver = 2, flags = MAC_USE, iftype = AP (0x1), mac_addr set — retry when v1 failed — `linux/brcmfmac/cfg80211.c:738-747`
- linux — get — u32 query, input 0 — version query on the AP path — `linux/brcmfmac/cfg80211.c:758-760`
- linux — get — v3 record: ver = 3, flags = MAC_USE, iftype = AP — used when the query returns 3 — `linux/brcmfmac/cfg80211.c:767-776`

### `interface_remove`
| | |
|---|---|
| Used by | linux (plain name on bsscfg index 0, `bsscfg:` prefix + le32 index otherwise). whd: defined, not used by whd. Not found in embassy, c-driver. |
| Direction | linux: set |
| Value | linux: no value, 0 bytes |
| Record | none |

- linux — set — no payload (NULL, length 0) — `brcmf_cfg80211_del_apsta_iface` removes the AP/STA interface the call is made on — `linux/brcmfmac/cfg80211.c:1276`
- linux — the bsscfg helper sends the bare name when the interface's bsscfgidx is 0; otherwise `bsscfg:` + name + NUL + le32 bsscfgidx + payload — `linux/brcmfmac/fwil.c:259-289`
- whd — macro `IOVAR_STR_INTERFACE_REMOVE` defined, no use site — `whd/src/include/whd_wlioctl.h:1140`

### `intol40`
| | |
|---|---|
| Used by | whd: defined, not used by whd. Not found in embassy, linux, c-driver. |
| Direction | not shown by any driver |
| Value | payload not shown by any driver |
| Record | not shown by any driver |

- whd — macro `IOVAR_STR_HT40_INTOLERANCE` defined, no use site — `whd/src/include/whd_wlioctl.h:1135`

### `join`
| | |
|---|---|
| Used by | c-driver (no prefix), linux (plain name on bsscfg index 0, `bsscfg:` prefix + le32 index otherwise), whd (no prefix, string literal). Not found in embassy. |
| Direction | set in all three |
| Value | c-driver: 70 bytes built by hand, little-endian. linux: `struct brcmf_ext_join_params_le`, 68 bytes without a chanspec or 70 with one, little-endian. whd: `wl_extjoin_params_t`, 70 bytes; only the chanspec goes through `htod16`, the other fields are written in host order. |
| Record | linux: `brcmf_ext_join_params_le` `linux/brcmfmac/fwil_types.h:530-534` (parts: `brcmf_ssid_le` `linux/brcmfmac/fwil_types.h:357-360`, `brcmf_join_scan_params_le` `linux/brcmfmac/fwil_types.h:515-527`, `brcmf_assoc_params_le` `linux/brcmfmac/fwil_types.h:482-490`). whd: `wl_extjoin_params_t` `whd/src/include/whd_wlioctl.h:4259-4267` (parts: `wlc_ssid_t` `whd/src/include/whd_wlioctl.h:496-500`, `wl_join_scan_params_t` `whd/src/include/whd_wlioctl.h:619-632`, `wl_assoc_params_t` `whd/src/include/whd_wlioctl.h:4239-4245`). c-driver: no struct, offsets written inline `c-driver/cyw43_ll.c:2300-2321`. |

- c-driver, linux, whd — layout, offset 0, 4 bytes, SSID length — c-driver: le32 ssid_len; linux: le32, capped at IEEE80211_MAX_SSID_LEN; whd: host-order `ap->SSID.length` — `c-driver/cyw43_ll.c:2301`, `linux/brcmfmac/cfg80211.c:2578-2579`, `whd/src/whd_wifi_api.c:2350`
- c-driver, linux, whd — layout, offset 4, 32 bytes, SSID — all three: ssid bytes, rest zero — `c-driver/cyw43_ll.c:2300-2302`, `linux/brcmfmac/cfg80211.c:2573`, `linux/brcmfmac/cfg80211.c:2580`, `whd/src/whd_wifi_api.c:2348`, `whd/src/whd_wifi_api.c:2352`
- c-driver, linux, whd — layout, offset 36, 1 byte, scan_type — c-driver: 0; linux: 0xFF (assigned -1); whd: 0 — `c-driver/cyw43_ll.c:2305`, `linux/brcmfmac/cfg80211.c:2586`, `whd/src/whd_wifi_api.c:2355`
- c-driver, linux, whd — layout, offset 40, 4 bytes, nprobes — c-driver: -1; linux: -1 without a channel, 320/20 = 16 with one; whd: -1 — `c-driver/cyw43_ll.c:2306`, `linux/brcmfmac/cfg80211.c:2611-2613`, `linux/brcmfmac/cfg80211.c:2617`, `linux/brcmfmac/cfg80211.c:80-82`, `whd/src/whd_wifi_api.c:2358`
- c-driver, linux, whd — layout, offset 44, 4 bytes, active_time — c-driver: -1; linux: -1 without a channel, 320 with one; whd: -1 — `c-driver/cyw43_ll.c:2307`, `linux/brcmfmac/cfg80211.c:2603-2604`, `linux/brcmfmac/cfg80211.c:2615`, `linux/brcmfmac/cfg80211.c:80`, `whd/src/whd_wifi_api.c:2356`
- c-driver, linux, whd — layout, offset 48, 4 bytes, passive_time — c-driver: -1; linux: -1 without a channel, 400 with one; whd: -1 — `c-driver/cyw43_ll.c:2308`, `linux/brcmfmac/cfg80211.c:2605-2606`, `linux/brcmfmac/cfg80211.c:2616`, `linux/brcmfmac/cfg80211.c:81`, `whd/src/whd_wifi_api.c:2359`
- c-driver, linux, whd — layout, offset 52, 4 bytes, home_time — all three: -1 — `c-driver/cyw43_ll.c:2309`, `linux/brcmfmac/cfg80211.c:2587`, `whd/src/whd_wifi_api.c:2357`
- c-driver, linux, whd — layout, offset 56, 6 bytes, bssid — c-driver: target BSSID; linux: target BSSID, or the broadcast address when none is given; whd: AP BSSID — `c-driver/cyw43_ll.c:2316`, `linux/brcmfmac/cfg80211.c:2589-2592`, `whd/src/whd_wifi_api.c:2354`
- c-driver, linux, whd — layout, offset 62, 2 bytes (linux: padding; whd: `bssid_cnt`) — c-driver: zero; linux: zero (kzalloc); whd: 0 — `c-driver/cyw43_ll.c:2300`, `linux/brcmfmac/cfg80211.c:2573`, `whd/src/whd_wifi_api.c:2360`, `whd/src/include/whd_wlioctl.h:4242`
- c-driver, linux, whd — layout, offset 64, 4 bytes, chanspec_num — c-driver: 1 if a channel is given, else 0; linux: 1 if `cfg->channel`, else 0; whd: 1 (host order) if `ap->channel`, else 0 — `c-driver/cyw43_ll.c:2317-2318`, `linux/brcmfmac/cfg80211.c:2594-2595`, `whd/src/whd_wifi_api.c:2362-2364`
- c-driver, linux, whd — layout, offset 68, 2 bytes, chanspec_list[0] — c-driver: le16 `channel | 0x1000` (BW_20, 2G, no sideband) if a channel is given, else 0; linux: le16 chanspec, sent only when `cfg->channel` (length 70), otherwise omitted (length 68); whd: `htod16(chanspec)` if `ap->channel`, else 0 — `c-driver/cyw43_ll.c:2312-2320`, `linux/brcmfmac/cfg80211.c:2569-2572`, `linux/brcmfmac/cfg80211.c:2597-2598`, `whd/src/whd_wifi_api.c:2365`
- c-driver — set — 70 bytes (4 + 32 + 20 + 14) through `cyw43_write_iovar_n` on the STA interface — join a specific BSSID; used only when a bssid is supplied, otherwise the driver sends the `WLC_SET_SSID` command with 36 bytes — `c-driver/cyw43_ll.c:2299-2330`, `c-driver/cyw43_ll.c:1556-1562`
- linux — set — `brcmf_ext_join_params_le`, length `offsetof(assoc_le) + offsetof(chanspec_list)` plus 2 when a channel is known — `brcmf_cfg80211_connect` extended join; on error linux falls back to the set-SSID command — `linux/brcmfmac/cfg80211.c:2569-2630`
- linux — the 68/70 byte totals and the offsets above follow from the non-packed struct definitions with a 32-byte SSID and 6-byte address (inferred; `IEEE80211_MAX_SSID_LEN` is defined as 32; the `ETH_ALEN` value 6 is recalled, not in these sources) — `linux/brcmfmac/fwil_types.h:357-360`, `linux/brcmfmac/fwil_types.h:482-490`, `linux/brcmfmac/fwil_types.h:515-534`, `linux-headers/ieee80211.h:227`
- whd — set — `sizeof(wl_extjoin_params_t)` bytes, zeroed then filled — `whd_wifi_join_specific`, not sent when re-associating; when the result is `WHD_WLAN_UNSUPPORTED` whd falls back to the `WLC_SET_SSID` command with `wl_join_params_t` — `whd/src/whd_wifi_api.c:2342-2386`
- whd — `wl_extjoin_params_t` and `wl_assoc_params_t` are inside a `#pragma pack(1)` region, `wl_join_scan_params_t` is defined outside it; the 70-byte size and the offsets above are from a host GCC build, not an ARM compiler (compiled) — `whd/src/include/whd_wlioctl.h:4188`, `whd/src/include/whd_wlioctl.h:4289`, `whd/src/include/whd_wlioctl.h:619-632`
- whd — macro `IOVAR_STR_JOIN` is defined but the call site uses the literal `"join"` — `whd/src/include/whd_wlioctl.h:1142`, `whd/src/whd_wifi_api.c:2346`

Differences: linux sends scan_type 0xFF, c-driver and whd send 0 `linux/brcmfmac/cfg80211.c:2586`, `c-driver/cyw43_ll.c:2305`, `whd/src/whd_wifi_api.c:2355`. linux sends explicit dwell times and probe count when a channel is known; c-driver and whd always send -1 `linux/brcmfmac/cfg80211.c:2603-2613`, `c-driver/cyw43_ll.c:2306-2308`, `whd/src/whd_wifi_api.c:2356-2359`. linux shortens the record to 68 bytes when no channel is known; c-driver and whd always send 70 `linux/brcmfmac/cfg80211.c:2569-2572`, `c-driver/cyw43_ll.c:2325`, `whd/src/whd_wifi_api.c:2346`. linux may add the `bsscfg:` prefix; c-driver and whd never do `linux/brcmfmac/fwil.c:259-289`, `c-driver/cyw43_ll.c:2325`, `whd/src/whd_wifi_api.c:2346`. Bytes 62-63 are named `bssid_cnt` by whd and are unnamed padding in linux `whd/src/include/whd_wlioctl.h:4242`, `linux/brcmfmac/fwil_types.h:482-490`.

### `join_pref`
| | |
|---|---|
| Used by | linux (no prefix). Not found in embassy, whd, c-driver. |
| Direction | linux: set |
| Value | linux: array of 2 `struct brcmf_join_pref_params`, 8 bytes, all fields single bytes |
| Record | `brcmf_join_pref_params` {u8 type, u8 len, u8 rssi_gain, u8 band} `linux/brcmfmac/fwil_types.h:501-506` |

- linux — set — entry 0 {type 4 (RSSI_DELTA), len 2, rssi_gain 8 (`BRCMF_JOIN_PREF_RSSI_BOOST`), band 1 (5G)}, entry 1 {type 1 (RSSI), len 2, 0, 0} — default join preference: select by RSSI with a boost on 5 GHz; an error is logged, not returned — `linux/brcmfmac/common.c:86-99`, `linux/brcmfmac/common.c:32`, `linux/brcmfmac/fwil_types.h:197-202`, `linux/include/brcmu_wifi.h:93`
- linux — set — per connect request: band preference gives entry 0 {type 3 (BAND), len 2, 0, band}, RSSI adjust gives entry 0 {type 4, len 2, delta, band}; the entry after it is {type 1, len 2, 0, 0}; always 8 bytes — `brcmf_set_join_pref`, BSS selection for the next join — `linux/brcmfmac/cfg80211.c:2366-2408`
- linux — for the RSSI behaviour and any behaviour value not listed in the switch (its `default:` label, not the default setter above) only entry 0 is written ({type 1, len 2, 0, 0}); entry 1 is an uninitialised stack array element and is still sent (inferred from the code path) — `linux/brcmfmac/cfg80211.c:2370-2374`, `linux/brcmfmac/cfg80211.c:2397-2405`
- linux — with no selection attribute the function calls the default setter above instead — `linux/brcmfmac/cfg80211.c:2381-2383`

### `keep_alive`
| | |
|---|---|
| Used by | whd (no prefix). Not found in embassy, linux, c-driver. |
| Direction | whd: set |
| Value | whd: `wl_keep_alive_pkt_t`, variable length; fields written in host order (no `htod`) |
| Record | `wl_keep_alive_pkt_t` {uint32 period_msec, uint16 len_bytes, uint8 data[1]} `whd/src/include/whd_wlioctl.h:3624-3629`; fixed part `WL_KEEP_ALIVE_FIXED_LEN` = offsetof(data) `whd/src/include/whd_wlioctl.h:3630` |

- whd — set — `sizeof(wl_keep_alive_pkt_t)` bytes zeroed, then period_msec from the caller; len_bytes stays 0 — `whd_wifi_keepalive_config` with flag `WHD_KEEPALIVE_NULL` (0): periodic null-frame keepalive — `whd/src/whd_wifi_api.c:1027-1034`, `whd/src/whd_wifi_api.c:1049`, `whd/src/include/whd_wlioctl.h:182`
- whd — set — buffer of `2 * len_bytes + WL_KEEP_ALIVE_FIXED_LEN` bytes: period_msec, len_bytes, then len_bytes of caller data copied once — flag `WHD_KEEPALIVE_NAT` (1): periodic keepalive with a caller-supplied packet — `whd/src/whd_wifi_api.c:1038-1046`, `whd/src/whd_wifi_api.c:1049`, `whd/src/include/whd_wlioctl.h:183`
- whd — the NAT branch requests twice the packet length but writes it once; the remaining bytes are not written in this function — `whd/src/whd_wifi_api.c:1040-1046`
- whd — offsetof(data) = 6 and sizeof = 8 under natural alignment (inferred from the field types) — `whd/src/include/whd_wlioctl.h:3624-3630`
- whd — when the flag is neither value no buffer is requested and the unset buffer handle (NULL) is still passed to the set call — `whd/src/whd_wifi_api.c:1020`, `whd/src/whd_wifi_api.c:1027`, `whd/src/whd_wifi_api.c:1038`, `whd/src/whd_wifi_api.c:1049`
- whd — the name comes from macro `IOVAR_STR_KEEPALIVE_CONFIG`; `WL_KEEP_ALIVE_FIXED_LEN` is also defined a second time earlier in the header — `whd/src/include/whd_wlioctl.h:1273`, `whd/src/include/whd_wlioctl.h:46`

### `ldpc_cap`
| | |
|---|---|
| Used by | whd: defined, not used by whd. Not found in embassy, linux, c-driver. |
| Direction | not shown by any driver |
| Value | payload not shown by any driver |
| Record | not shown by any driver |

- whd — macro `IOVAR_STR_LDPC_CAP` defined, no use site — `whd/src/include/whd_wlioctl.h:1236`

### `ldpc_tx`
| | |
|---|---|
| Used by | whd: defined, not used by whd. Not found in embassy, linux, c-driver. |
| Direction | not shown by any driver |
| Value | payload not shown by any driver |
| Record | not shown by any driver |

- whd — macro `IOVAR_STR_LDPC_TX` defined, no use site — `whd/src/include/whd_wlioctl.h:1237`

### `maxassoc`
| | |
|---|---|
| Used by | c-driver (no prefix; interface number passed as a value word after the name), whd (no prefix). Not found in embassy, linux. |
| Direction | c-driver: get. whd: both. |
| Value | c-driver: request carries le32 interface number (4 bytes) after the name, reply read as le32. whd: uint32, 4 bytes, little-endian (`htod32` / `dtoh32`). |
| Record | plain integer |

- c-driver — get — 9 bytes `maxassoc` + NUL, then le32 `WWD_AP_INTERFACE`; command length 13; sent on the STA interface; reply le32 at offset 0 = maximum associated stations — sizes the station list request that follows — `c-driver/cyw43_ll.c:2467-2475`
- c-driver — the identical get is issued twice in a row; only the second return value is checked — `c-driver/cyw43_ll.c:2470-2471`
- whd — get — 4-byte buffer, reply converted with `dtoh32` — `whd_wifi_ap_get_max_assoc`; also called from the deauth-station path — `whd/src/whd_wifi_api.c:3650`, `whd/src/whd_wifi_api.c:3491`, `whd/src/whd_wifi_api.c:5165-5183`
- whd — set — uint32 `htod32(max_assoc)`, 4 bytes; 0 is rejected by the wrapper — `whd_wifi_ap_set_max_assoc` — `whd/src/whd_wifi_api.c:3653-3663`, `whd/src/whd_wifi_api.c:5153-5162`
- whd — set — value `MAX_CLIENT_SUPPORT` (2) at the end of AP start, only when `PROTO_MSGBUF` is defined; return value ignored — `whd/src/whd_ap.c:583-586`, `whd/src/include/whd_msgbuf.h:117`
- whd — macro `IOVAR_STR_MAX_ASSOC` — `whd/src/include/whd_wlioctl.h:1120`

Differences: c-driver's get request carries 4 bytes holding the AP interface number after the name `c-driver/cyw43_ll.c:2468-2470`; whd's get request buffer is 4 bytes that the helper does not fill `whd/src/whd_wifi_api.c:5175`.

### `mbo`
| | |
|---|---|
| Used by | whd (no prefix). Not found in embassy, linux, c-driver. |
| Direction | whd: set |
| Value | whd: `whd_iov_buf_t` header followed by one sub-command record; fields written in host order |
| Record | `whd_iov_buf_t` {uint16 version, uint16 len, uint16 id, uint16 data[1]} `whd/src/include/whd_wlioctl.h:421-427`; `mbo_xtlv_t` {uint16 id, uint16 len, uint32 data[1]} `whd/src/include/whd_wlioctl.h:429-434`; `mbo_add_chan_pref_t` `whd/src/include/whd_wlioctl.h:437-442`; `mbo_del_chan_pref_t` `whd/src/include/whd_wlioctl.h:445-448` |

- whd — set — header {version `WL_MBO_IOV_VERSION` = 257 (0x0101), len sizeof(mbo_add_chan_pref_t), id `WL_MBO_CMD_ADD_CHAN_PREF` (1)}, then four xtlvs copied at `data`: opclass (id 1), chan (id 2), pref (id 3), reason (id 4) — `whd_wifi_mbo_add_chan_pref`: add a non-preferred channel — `whd/src/whd_wifi_api.c:4956-4981`, `whd/src/include/whd_wlioctl.h:373-381`, `whd/src/include/whd_wlioctl.h:404-408`
- whd — set — header {version 257 (0x0101), len sizeof(mbo_del_chan_pref_t), id `WL_MBO_CMD_DEL_CHAN_PREF` (2)}, then two xtlvs: opclass, chan — `whd_wifi_mbo_del_chan_pref` — `whd/src/whd_wifi_api.c:4995-5012`
- whd — set — header {version 257 (0x0101), len sizeof(mbo_xtlv_t), id `WL_MBO_CMD_SEND_NOTIF` (9)}, then one xtlv {id `WL_MBO_XTLV_SUB_ELEM_TYPE` (8), len 1, data = sub element type} — `whd_wifi_mbo_send_notif`; only the cellular-data-capability and non-preferred-channel-report types are accepted — `whd/src/whd_wifi_api.c:5022-5044`, `whd/src/include/whd_wlioctl.h:388`, `whd/src/include/whd_wlioctl.h:412`
- whd — each buffer is requested as `sizeof(whd_iov_buf_t) + sizeof(record)` while the record is copied at `data`, which is inside the header (offset 6 of 8, inferred from the field types), so the last 2 bytes of each buffer are not written by these functions (inferred) — `whd/src/whd_wifi_api.c:4974-4980`, `whd/src/include/whd_wlioctl.h:421-427`
- whd — sizes with natural alignment (inferred from the field types): header 8, `mbo_xtlv_t` 8, add record 32, delete record 16; buffers 40, 24 and 16 bytes — `whd/src/include/whd_wlioctl.h:421-448`
- whd — macro `IOVAR_STR_MBO` — `whd/src/include/whd_wlioctl.h:1274`

### `mbss`
| | |
|---|---|
| Used by | linux (no prefix). Not found in embassy, whd, c-driver. |
| Direction | linux: set |
| Value | linux: le32, 4 bytes |
| Record | plain integer |

- linux — set — 1 — `brcmf_cfg80211_start_ap`, AP role, when the MBSS feature is enabled and no multi-BSS is already running; sent before the set-AP command; return value ignored — `linux/brcmfmac/cfg80211.c:5379-5381`
- linux — set — 0 — `brcmf_cfg80211_stop_ap`, when the MBSS feature is enabled; return value ignored — `linux/brcmfmac/cfg80211.c:5553-5554`

### `mcast_list`
| | |
|---|---|
| Used by | embassy, linux, whd, c-driver; none uses a `bsscfg:` prefix |
| Direction | embassy: both. c-driver: both. whd: both. linux: set. |
| Value | all: le32 count followed by 6-byte MAC addresses. Set length: embassy fixed `4 + 6 * MULTICAST_FILTER_SIZE`; c-driver fixed 64; linux `4 + 6 * count`; whd `4 + 6 * count`. Get request: c-driver and whd send the name followed by 64 bytes; embassy sends 64 bytes in total including the name. |
| Record | whd: `mcast_list_t` {uint32 entry_count, whd_mac_t macs[1]}, packed(1), `whd/src/whd_wifi_api.c:127-133`. embassy, linux, c-driver: no struct, built inline. |

- embassy — get — request of 64 bytes (name + NUL, rest zero); reply read as u32 LE count then count × 6-byte addresses, at most 10 copied out — `list_multicast_addresses` — `embassy/control.rs:657-669`, `embassy/control.rs:731-746`
- embassy — the get helper carries a source comment saying it returns all zeros — `embassy/control.rs:730`
- embassy — set — 11-byte name `mcast_list\0`, u32 LE count, then the addresses; request size fixed at `11 + 4 + 6 * MULTICAST_FILTER_SIZE`, unused slots zero — `apply_multicast_filter` replaces the whole list in one write, sent from the runner — `embassy/runner.rs:1382-1399`
- embassy — `MULTICAST_FILTER_SIZE` comes from the external embassy-net-driver-channel crate; its value is not found in these sources — `embassy/runner.rs:1393`
- c-driver — get — 11 bytes name + NUL, then 64 zero bytes; command length 75; reply le32 count then count × 6-byte addresses — read the current list before adding or removing one address — `c-driver/cyw43_ll.c:2089-2098`, `c-driver/cyw43_ll.c:253`
- c-driver — set — always 64 bytes: le32 count + 10 address slots; slots past count keep whatever the get reply left there — write the edited list back; returns `-CYW43_EPERM` without writing when 10 addresses are already present; 50 ms delay after the write — `c-driver/cyw43_ll.c:2116-2130`
- linux — set — le32 count + count × 6-byte addresses, `4 + 6 * count` bytes, taken from the netdev multicast list — program the multicast filter; on failure all-multicast is forced on only if the copy loop did not consume the whole count — `linux/brcmfmac/core.c:158-182`
- whd — get — data buffer of `4 + 10 * 6` = 64 bytes after the name, not filled by the caller; reply parsed as `mcast_list_t`, entry_count through `dtoh32` — `whd_wifi_register_multicast_address` and `whd_wifi_unregister_multicast_address` read the current list first — `whd/src/whd_wifi_api.c:3961-3970`, `whd/src/whd_wifi_api.c:4018-4026`, `whd/src/whd_wifi_api.c:57`
- whd — set — `mcast_list_t` with entry_count `htod32(n + 1)` and n + 1 addresses, `4 + 6 * (n + 1)` bytes — register: old list with the new address appended; skipped if the address is already present — `whd/src/whd_wifi_api.c:3971-3995`
- whd — set — entry_count `htod32(n - 1)` and n - 1 addresses, `4 + 6 * (n - 1)` bytes — unregister: list with the address removed; nothing is written when the list is empty or the address is absent — `whd/src/whd_wifi_api.c:4027-4059`
- whd — macro `IOVAR_STR_MCAST_LIST` — `whd/src/include/whd_wlioctl.h:1080`

Differences: set length. embassy sends a fixed size with zeroed unused slots `embassy/runner.rs:1393-1398`; c-driver sends a fixed 64 bytes with unused slots not cleared `c-driver/cyw43_ll.c:2129`; linux and whd send exactly `4 + 6 * count` bytes `linux/brcmfmac/core.c:160`, `whd/src/whd_wifi_api.c:3984-3986`. Get request length: c-driver sends name plus 64 bytes (75 total) `c-driver/cyw43_ll.c:2092`; whd requests 64 data bytes after the name `whd/src/whd_wifi_api.c:3962-3964`, `whd/src/whd_cdc_bdc.c:354-366`; embassy sends 64 bytes in total including the name `embassy/control.rs:738`.

### `memuse`
| | |
|---|---|
| Used by | whd: defined, not used by whd. Not found in embassy, linux, c-driver. |
| Direction | not shown by any driver |
| Value | payload not shown by any driver |
| Record | not shown by any driver |

- whd — macro `IOVAR_STR_MEMUSE` defined, no use site — `whd/src/include/whd_wlioctl.h:1234`

### `mesh_add_route`
| | |
|---|---|
| Used by | whd: defined, not used by whd. Not found in embassy, linux, c-driver. |
| Direction | not shown by any driver |
| Value | payload not shown by any driver |
| Record | not shown by any driver |

- whd — macro `IOVAR_STR_MESH_ADD_ROUTE` defined, no use site — `whd/src/include/whd_wlioctl.h:1214`

### `mesh_del_route`
| | |
|---|---|
| Used by | whd: defined, not used by whd. Not found in embassy, linux, c-driver. |
| Direction | not shown by any driver |
| Value | payload not shown by any driver |
| Record | not shown by any driver |

- whd — macro `IOVAR_STR_MESH_DEL_ROUTE` defined, no use site — `whd/src/include/whd_wlioctl.h:1215`

### `mesh_delfilter`
| | |
|---|---|
| Used by | whd: defined, not used by whd. Not found in embassy, linux, c-driver. |
| Direction | not shown by any driver |
| Value | payload not shown by any driver |
| Record | not shown by any driver |

- whd — macro `IOVAR_STR_MESH_DELFILTER` defined, no use site — `whd/src/include/whd_wlioctl.h:1220`

### `mesh_filter`
| | |
|---|---|
| Used by | whd: defined, not used by whd. Not found in embassy, linux, c-driver. |
| Direction | not shown by any driver |
| Value | payload not shown by any driver |
| Record | not shown by any driver |

- whd — macro `IOVAR_STR_MESH_FILTER` defined, no use site — `whd/src/include/whd_wlioctl.h:1217`

### `mesh_find`
| | |
|---|---|
| Used by | whd: defined, not used by whd. Not found in embassy, linux, c-driver. |
| Direction | not shown by any driver |
| Value | payload not shown by any driver |
| Record | not shown by any driver |

- whd — macro `IOVAR_STR_MESH_FIND` defined, no use site — `whd/src/include/whd_wlioctl.h:1216`

### `mesh_max_peers`
| | |
|---|---|
| Used by | whd: defined, not used by whd. Not found in embassy, linux, c-driver. |
| Direction | not shown by any driver |
| Value | payload not shown by any driver |
| Record | not shown by any driver |

- whd — macro `IOVAR_STR_MESH_MAX_PEERS` defined, no use site — `whd/src/include/whd_wlioctl.h:1221`

### `mesh_peer`
| | |
|---|---|
| Used by | whd: defined, not used by whd. Not found in embassy, linux, c-driver. |
| Direction | not shown by any driver |
| Value | payload not shown by any driver |
| Record | not shown by any driver |

- whd — macro `IOVAR_STR_MESH_PEER` defined, no use site — `whd/src/include/whd_wlioctl.h:1218`

### `mesh_peer_status`
| | |
|---|---|
| Used by | whd: defined, not used by whd. Not found in embassy, linux, c-driver. |
| Direction | not shown by any driver |
| Value | payload not shown by any driver |
| Record | not shown by any driver |

- whd — macro `IOVAR_STR_MESH_PEER_STATUS` defined, no use site — `whd/src/include/whd_wlioctl.h:1219`

### `mfp`
| | |
|---|---|
| Used by | embassy (no prefix), c-driver (no prefix), whd (no prefix), linux (set: plain name on bsscfg index 0, `bsscfg:` prefix + le32 index otherwise; get: no prefix) |
| Direction | embassy: set. c-driver: set. linux: both. whd: both. |
| Value | all: 32-bit little-endian integer, 4 bytes; 0 none, 1 capable, 2 required |
| Record | plain integer |

- embassy, c-driver, linux, whd — value names: embassy `MFP_NONE/CAPABLE/REQUIRED`; c-driver `MFP_*`; linux `BRCMF_MFP_*`; whd `WL_MFP_*` (enum, values follow from order after 0) — `embassy/consts.rs:738-740`, `c-driver/cyw43_ll.c:267-269`, `linux/brcmfmac/fwil_types.h:169-171`, `whd/inc/whd_types.h:438-443`
- embassy — set — 0 for Wpa, 1 for Wpa2 and Wpa2Wpa3, 2 for Wpa3 — station join, after the set-auth command and before the set-WPA-auth command; not sent for an open join — `embassy/control.rs:398-404`, `embassy/control.rs:432-435`
- embassy — set — 0 for Open and Wpa2, 2 for Wpa3, 1 for Wpa2Wpa3 — access point start, after `bsscfg:wsec` — `embassy/control.rs:548-557`, `embassy/control.rs:589-592`
- c-driver — set — 1 when wpa_auth is WPA2-PSK or WPA3-SAE, else 0; STA interface — station join, after the set-auth command — `c-driver/cyw43_ll.c:2275-2276`, `c-driver/cyw43_ll.c:1538-1544`
- c-driver — set — 2 for WPA3 SAE, 1 for WPA3/WPA2 mixed, else 0; sent on the AP interface — access point setup, after `bsscfg:wsec` — `c-driver/cyw43_ll.c:2392-2401`
- linux — set — 2 if the RSN capabilities in the connect IEs have the MFP-required bit, 1 if only MFP-capable, else 0; skipped when the MFP feature is off or no RSN IE is present; return value ignored — `brcmf_set_key_mgmt` — `linux/brcmfmac/cfg80211.c:2241-2273`, `linux/brcmfmac/fwil.h:154-160`
- linux — set — 0/1/2 — `brcmf_configure_wpaie` (AP mode), sent after `wsec` because linux expects the wsec write to overwrite the MFP setting — `linux/brcmfmac/cfg80211.c:4823-4827`
- linux — get — 4-byte buffer, value discarded — feature probe at attach: the MFP feature is enabled unless the reply is `-BRCMF_FW_UNSUPPORTED` — `linux/brcmfmac/feature.c:187-199`, `linux/brcmfmac/feature.c:334`, `linux/brcmfmac/fwil.h:130-138`
- whd — get — 4 bytes — `whd_wifi_prepare_join` saves the current value before the set-wsec command, which whd expects to overwrite it on older firmware; skipped for open security — `whd/src/whd_wifi_api.c:1758-1766`
- whd — set — 2 for WPA3 SAE/FBT/ENT/OWE types, 1 for WPA3/WPA2 mixed and WPA2 types, else the value read earlier; skipped when `is_mfp_auto` is set; a failure is ignored — `whd_wifi_prepare_join`, after the set-auth command — `whd/src/whd_wifi_api.c:1921-1947`
- whd — set — 0 by default, 2 for WPA3 SAE, 1 for WPA3/WPA2 PSK; sent on the AP interface — `whd_wifi_init_ap`, after the wsec write — `whd/src/whd_ap.c:343`, `whd/src/whd_ap.c:434-443`
- whd — macro `IOVAR_STR_MFP` — `whd/src/include/whd_wlioctl.h:1226`

Differences: for a WPA3-only station join embassy and whd send 2 (required), c-driver sends 1 (capable) `embassy/control.rs:402`, `whd/src/whd_wifi_api.c:1930-1934`, `c-driver/cyw43_ll.c:2276`. For a station join linux derives the value from the RSN capability bits of the supplied IEs; embassy, c-driver and whd derive it from the security type `linux/brcmfmac/cfg80211.c:2267-2273`, `embassy/control.rs:398-404`, `c-driver/cyw43_ll.c:2276`, `whd/src/whd_wifi_api.c:1930-1940`. linux may add the `bsscfg:` prefix on set; the other three never do `linux/brcmfmac/fwil.c:259-289`, `embassy/control.rs:434`, `c-driver/cyw43_ll.c:2276`, `whd/src/whd_wifi_api.c:1942`.

### `mgmt_frame`
| | |
|---|---|
| Used by | linux (Cypress/Infineon vendor code; plain name on bsscfg index 0, `bsscfg:` prefix + le32 index otherwise), whd (no prefix). Not found in embassy, c-driver. |
| Direction | set in both |
| Value | linux: `struct brcmf_mf_params_le` + frame body, little-endian. whd: `whd_auth_params_t` header + frame body; header copied from the caller in host order. Both: header up to `data`, then the frame without its 24-byte 802.11 management header. |
| Record | linux: `brcmf_mf_params_le` `linux/brcmfmac/cyw/fwil_types.h:74-84`. whd: `whd_auth_params_t` `whd/inc/whd_types.h:1195-1206`. |

- linux, whd — header fields in declaration order (same order in both records): u32 version, u32 dwell_time, u16 len, u16 frame control, u16 channel, 6-byte da, 6-byte bssid, u32 packet id, then data — `linux/brcmfmac/cyw/fwil_types.h:74-84`, `whd/inc/whd_types.h:1195-1206`
- linux, whd — neither record is packed; with natural alignment data starts at offset 32 (inferred from the field types, 2 padding bytes before the packet id; linux depends on `ETH_ALEN` = 6, recalled, not in these sources) — `linux/brcmfmac/cyw/fwil_types.h:74-84`, `whd/inc/whd_types.h:1195-1206`
- linux — set — length `offsetof(data) + (frame len - 24)`; version left 0 (zeroed allocation), dwell_time 4000, len = body length, frame_control copied from the frame, channel = the given channel's hw value or 2 bytes read with the get-channel command, da and bssid from the frame header, packet_id = low 32 bits of the cfg80211 cookie, data = frame after the management header — transmit a host-built Authentication frame (external SAE); other frame types take the generic path — `linux/brcmfmac/cyw/core.c:123-124`, `linux/brcmfmac/cyw/core.c:133-170`, `linux/brcmfmac/cyw/core.c:23`, `linux/brcmfmac/cfg80211.h:16`
- linux — after the set, linux waits for a TX-status event with timeout argument `MGMT_AUTH_FRAME_WAIT_TIME` = 4000 + 100 = 4100 — `linux/brcmfmac/cyw/core.c:23-24`, `linux/brcmfmac/cyw/core.c:178-179`
- linux — sent through the bsscfg helper, so the name gains the `bsscfg:` prefix and an le32 index on a non-zero bsscfgidx — `linux/brcmfmac/fwil.c:259-289`, `linux/brcmfmac/fwil.c:308-312`
- whd — set — length `OFFSET(whd_auth_params_t, data) + (len - 24)`; header copied from the caller's struct after its len is reduced by 24, data = caller's data after the management header, dwell_time overwritten with `MGMT_AUTH_FRAME_DWELL_TIME` = 100 — `whd_wifi_send_auth_frame`: send an authentication frame — `whd/src/whd_wifi_api.c:4347-4374`, `whd/src/include/whd_wlioctl.h:36`
- whd — macro `IOVAR_STR_MGMT_FRAME` — `whd/src/include/whd_wlioctl.h:1166`

Differences: dwell_time is 4000 in linux and 100 in whd `linux/brcmfmac/cyw/core.c:23`, `linux/brcmfmac/cyw/core.c:139`, `whd/src/include/whd_wlioctl.h:36`, `whd/src/whd_wifi_api.c:4372`. linux always sends version 0; whd sends whatever the caller put in version, channel and packetId `linux/brcmfmac/cyw/core.c:135`, `whd/src/whd_wifi_api.c:4370`. linux may add the `bsscfg:` prefix; whd does not `linux/brcmfmac/fwil.c:259-289`, `whd/src/whd_wifi_api.c:4367-4368`.

### `mimo_bw_cap`
| | |
|---|---|
| Used by | linux (no prefix). whd: defined, not used by whd. Not found in embassy, c-driver. |
| Direction | linux: both |
| Value | linux: le32, 4 bytes |
| Record | plain integer |

- linux — value names: `WLC_N_BW_20ALL` 0, `WLC_N_BW_40ALL` 1, `WLC_N_BW_20IN2G_40IN5G` 2 — `linux/include/brcmu_wifi.h:73-75`
- linux — set — 1 (`WLC_N_BW_40ALL`) — `brcmf_enable_bw40_2g`: fallback used when the `bw_cap` query fails — `linux/brcmfmac/cfg80211.c:7360-7372`
- linux — get — le32 read back — `brcmf_get_bwcap`: fallback used when the `bw_cap` query fails; on error linux assumes 0 (20 MHz everywhere) — `linux/brcmfmac/cfg80211.c:7436-7452`, `linux/brcmfmac/fwil.h:130-138`
- whd — macro `IOVAR_STR_MIMO_BW_CAP` defined, no use site — `whd/src/include/whd_wlioctl.h:1130`

### `mkeep_alive`
| | |
|---|---|
| Used by | embassy (no prefix), linux (no prefix); whd: defined, not used by whd. Not found in c-driver. `embassy/control.rs:692` `linux/brcmfmac/cfg80211.c:4307` `whd/src/include/whd_wlioctl.h:1101` |
| Direction | set (embassy, linux) `embassy/control.rs:692` `linux/brcmfmac/cfg80211.c:4307` |
| Value | 11 bytes, little-endian fields, in both drivers `embassy/control.rs:686-691` `linux/brcmfmac/fwil_types.h:1230-1237` |
| Record | linux: `struct brcmf_mkeep_alive_pkt_le` (packed) `linux/brcmfmac/fwil_types.h:1230-1237`. embassy: hand-packed bytes at the same offsets, no struct `embassy/control.rs:686-691`. Layout: u16 `version` at 0 `linux/brcmfmac/fwil_types.h:1231` `embassy/control.rs:687`, u16 `length` at 2 `linux/brcmfmac/fwil_types.h:1232` `embassy/control.rs:688`, u32 `period_msec` at 4 `linux/brcmfmac/fwil_types.h:1233` `embassy/control.rs:689`, u16 `len_bytes` at 8 `linux/brcmfmac/fwil_types.h:1234` `embassy/control.rs:690`, u8 `keep_alive_id` at 10 `linux/brcmfmac/fwil_types.h:1235` `embassy/control.rs:691`, variable-length `data` (frame bytes) at 11, which neither driver sends `linux/brcmfmac/fwil_types.h:1236` |

- embassy — set — version = 1, length = 11, period_msec = caller's `period_ms`, len_bytes = 0, keep_alive_id = caller's `id` — periodic null-data keepalive sent without host wakeups — `embassy/control.rs:683-692`
- linux — set — version = 1, length = 0 (struct zero-initialised, field never assigned), period_msec = interval × `MSEC_PER_SEC` (kernel constant; value not found in these sources), len_bytes = 0, keep_alive_id = 0 — null-function keepalive in `brcmf_keepalive_start` — `linux/brcmfmac/cfg80211.c:4295-4307`
- whd — defined, not used: macro `IOVAR_STR_MKEEP_ALIVE` only — `whd/src/include/whd_wlioctl.h:1101`

Differences: same 11-byte layout, different `length` value. embassy writes 11 `embassy/control.rs:688`; linux leaves 0 `linux/brcmfmac/cfg80211.c:4297-4305`. embassy takes the slot id from the caller `embassy/control.rs:691`; linux always uses 0 `linux/brcmfmac/cfg80211.c:4305`.

### `mpc`
| | |
|---|---|
| Used by | linux (no prefix), whd (no prefix). Not found in embassy or c-driver. `linux/brcmfmac/cfg80211.c:1038` `whd/src/whd_management.c:556` |
| Direction | set (both drivers) `linux/brcmfmac/cfg80211.c:1038` `whd/src/whd_wifi_api.c:3842` |
| Value | 4-byte little-endian integer in both drivers `linux/brcmfmac/fwil.h:123-127` `whd/src/whd_wifi_api.c:5153-5162` |
| Record | plain integer `linux/brcmfmac/fwil.h:123-127` `whd/src/whd_wifi_api.c:5153-5162` |

- linux — set — 1 — preinit; a failure aborts preinit — `linux/brcmfmac/common.c:406`
- linux — set — caller's 0 or 1, only when the vif is up — `brcmf_set_mpc` helper — `linux/brcmfmac/cfg80211.c:1032-1045`
- linux — set — 1 — before deleting an interface — `linux/brcmfmac/cfg80211.c:1317`
- linux — set — 1 (via `brcmf_set_mpc`) — after a GO-negotiation confirm or provision-discovery response action frame — `linux/brcmfmac/p2p.c:1465-1468`
- linux — set — 0 (via `brcmf_set_mpc`) — before sending an action frame when `mpc_onoff == 0` — `linux/brcmfmac/p2p.c:1836-1838`
- linux — set — 1 (via `brcmf_set_mpc`) — after the action-frame exchange when `mpc_onoff == 1` — `linux/brcmfmac/p2p.c:1942-1944`
- linux — set — 0 (via `brcmf_set_mpc`) — on the P2P connection vif before `p2p_ifupd` — `linux/brcmfmac/p2p.c:2091`
- whd — set — 0 — init, only for chip ids 43909, 43907, 54907 — `whd/src/whd_management.c:548-556`
- whd — set — 1 — init, only for chip id 55900 — `whd/src/whd_management.c:566-568`
- whd — set — 0 — `whd_wifi_config_ulp_mode`, compiled only with `CYCFG_ULP_SUPPORT_ENABLED`; only for chip ids 43022, 43012, when the requested mode is DS1 or DS2 and powersave is currently off — `whd/src/whd_wifi_api.c:3818-3842`
- whd — macro `IOVAR_STR_MPC` — `whd/src/include/whd_wlioctl.h:1123`

Differences: linux sends `mpc` = 1 to every chip at preinit `linux/brcmfmac/common.c:406`. None of the three whd call sites is reached for chip id 43439 (chip-id tests) `whd/src/whd_management.c:548` `whd/src/whd_management.c:566` `whd/src/whd_wifi_api.c:3832`. What the name stands for is not found in these sources; "minimum power consumption" (recalled, not in these sources). `whd/src/include/whd_wlioctl.h:1123`

### `nd_hostip`
| | |
|---|---|
| Used by | linux (no prefix). Not found in embassy, whd, c-driver. `linux/brcmfmac/core.c:225-227` |
| Direction | set `linux/brcmfmac/core.c:225` |
| Value | `struct in6_addr`, `sizeof(struct in6_addr)` bytes (16: recalled, not in these sources) `linux/brcmfmac/core.c:226-227` |
| Record | raw IPv6 address, one per call; no wrapper record `linux/brcmfmac/core.c:225-227` |

- linux — set — one entry of `ifp->ipv6_addr_tbl[]` per call, repeated for each of `ipv6addr_idx` addresses — fills the ND-offload host address table after `nd_hostip_clear`; compiled only with `CONFIG_IPV6` — `linux/brcmfmac/core.c:209-229`

### `nd_hostip_clear`
| | |
|---|---|
| Used by | linux (no prefix). Not found in embassy, whd, c-driver. `linux/brcmfmac/core.c:218` |
| Direction | set `linux/brcmfmac/core.c:218` |
| Value | none: 0 bytes after the name `linux/brcmfmac/core.c:218` |
| Record | no value `linux/brcmfmac/core.c:218` |

- linux — set — NULL, length 0 — clears the ND-offload address table before re-adding addresses with `nd_hostip`; on failure the adds are skipped; compiled only with `CONFIG_IPV6` — `linux/brcmfmac/core.c:209-222`

### `ndoe`
| | |
|---|---|
| Used by | linux (no prefix), whd (no prefix). Not found in embassy or c-driver. `linux/brcmfmac/core.c:128` `whd/src/whd_ap.c:562` |
| Direction | linux: set. whd: both. `linux/brcmfmac/core.c:128` `whd/src/whd_ap.c:562-566` |
| Value | 4-byte little-endian integer in both drivers `linux/brcmfmac/fwil.h:123-127` `whd/src/whd_wifi_api.c:5153-5183` |
| Record | plain integer `linux/brcmfmac/fwil.h:123-127` `whd/src/whd_wifi_api.c:5153-5183` |

- linux — set — 1 or 0 (`enable`) — ND offload on/off, sent after the ARP offload settings in `brcmf_configure_arp_nd_offload` — `linux/brcmfmac/core.c:128`
- whd — get — 4-byte request buffer, reply read as one uint32 — read the current setting during AP start — `whd/src/whd_ap.c:562` `whd/src/whd_wifi_api.c:5165-5183`
- whd — set — 0 — AP start, only if the value read was non-zero; return value not checked — `whd/src/whd_ap.c:563-566`
- whd — set — 1 — AP stop, only when firmware capability `WHD_FWCAP_OFFLOADS` is set; return value not checked — `whd/src/whd_ap.c:738-742`
- whd — macro `IOVAR_STR_NDOE` — `whd/src/include/whd_wlioctl.h:1282`

### `nmode`
| | |
|---|---|
| Used by | linux (no prefix); whd: defined, not used by whd. Not found in embassy or c-driver. `linux/brcmfmac/cfg80211.c:7557` `whd/src/include/whd_wlioctl.h:1119` |
| Direction | get (linux) `linux/brcmfmac/cfg80211.c:7557` |
| Value | 4-byte little-endian integer `linux/brcmfmac/fwil.h:130-138` |
| Record | plain integer `linux/brcmfmac/fwil.h:130-138` |

- linux — get — one uint32 — read while building the wiphy band tables (`brcmf_setup_wiphybands`); an error is logged — `linux/brcmfmac/cfg80211.c:7557-7559`
- whd — defined, not used: macro `IOVAR_STR_NMODE` only — `whd/src/include/whd_wlioctl.h:1119`

### `nphy_antsel`
| | |
|---|---|
| Used by | defined, not used by whd. Not found in embassy, linux, c-driver. `whd/src/include/whd_wlioctl.h:1144` |
| Direction | not shown by any driver `whd/src/include/whd_wlioctl.h:1144` |
| Value | payload not shown by any driver `whd/src/include/whd_wlioctl.h:1144` |
| Record | not shown by any driver `whd/src/include/whd_wlioctl.h:1144` |

- whd — defined, not used: macro `IOVAR_STR_NPHY_ANTSEL` only — `whd/src/include/whd_wlioctl.h:1144`

### `nrate`
| | |
|---|---|
| Used by | defined, not used by whd. Not found in embassy, linux, c-driver. `whd/src/include/whd_wlioctl.h:1116` |
| Direction | not shown by any driver `whd/src/include/whd_wlioctl.h:1116` |
| Value | payload not shown by any driver `whd/src/include/whd_wlioctl.h:1116` |
| Record | not shown by any driver `whd/src/include/whd_wlioctl.h:1116` |

- whd — defined, not used: macro `IOVAR_STR_NRATE` only — `whd/src/include/whd_wlioctl.h:1116`

### `obss_coex`
| | |
|---|---|
| Used by | linux (no prefix). Not found in embassy, whd, c-driver. `linux/brcmfmac/cfg80211.c:8631` |
| Direction | set `linux/brcmfmac/cfg80211.c:8631` |
| Value | 4-byte little-endian integer `linux/brcmfmac/fwil.h:123-127` |
| Record | plain integer; linux names three values: AUTO = -1, OFF = 0, ON = 1 `linux/brcmfmac/fwil_types.h:79-81` |

- linux — set — `BRCMF_OBSS_COEX_AUTO` (-1, sent as 0xFFFFFFFF (inferred from the u32 helper argument)) — at attach, after 40 MHz in the 2.4 GHz band was enabled without error — `linux/brcmfmac/cfg80211.c:8628-8632` `linux/brcmfmac/fwil.h:123-127`

### `oce`
| | |
|---|---|
| Used by | whd (no prefix). Not found in embassy, linux, c-driver. `whd/src/whd_wifi_api.c:4935-4942` |
| Direction | set `whd/src/whd_wifi_api.c:4942` |
| Value | 16-byte buffer: `whd_iov_buf_t` header plus one `mbo_xtlv_t`; fields written in host byte order, no conversion call `whd/src/whd_wifi_api.c:4935-4941` |
| Record | `whd_iov_buf_t` `whd/src/include/whd_wlioctl.h:421-427` carrying `mbo_xtlv_t` `whd/src/include/whd_wlioctl.h:429-434`; both records are 8 bytes and the header's `data` member is at offset 6 (compiled on an x86 host with gcc, not with an ARM compiler) `whd/src/include/whd_wlioctl.h:421-434`. Layout as whd fills it: u16 `version` at 0 = `WL_OCE_IOV_VERSION` = (1 << 8) OR 1 = 257 (0x0101) `whd/src/whd_wifi_api.c:4938` `whd/src/include/whd_wlioctl.h:345-349`; u16 `len` at 2 = `sizeof(mbo_xtlv_t)` = 8 `whd/src/whd_wifi_api.c:4939`; u16 `id` at 4 = `WL_OCE_CMD_ENABLE` = 1 `whd/src/whd_wifi_api.c:4940` `whd/src/include/whd_wlioctl.h:352`; u16 xtlv `id` at 6 = `WL_OCE_XTLV_ENABLE` = 1 `whd/src/whd_wifi_api.c:4931` `whd/src/include/whd_wlioctl.h:364`; u16 xtlv `len` at 8 = `sizeof(value)`, the size of `whd_bool_t` `whd/src/whd_wifi_api.c:4932`; 4-byte xtlv `data` at 10 = caller's enable value `whd/src/whd_wifi_api.c:4933`; the 2 bytes at 14 are not written by this function `whd/src/whd_wifi_api.c:4935-4941` |

- whd — set — the 16-byte buffer described in the Record row — `whd_wifi_oce_enable`: turn Optimized Connectivity Experience on or off — `whd/src/whd_wifi_api.c:4919-4942`
- whd — the xtlv len value depends on the compiler: `whd_bool_t` is `uint8_t` under `__llvm__` and an enum otherwise — `whd/inc/whd_types.h:276-281`
- whd — macro `IOVAR_STR_OCE` — `whd/src/include/whd_wlioctl.h:1276`

### `offload_config`
| | |
|---|---|
| Used by | whd (no prefix). Not found in embassy, linux, c-driver. `whd/src/whd_wifi_api.c:818-844` |
| Direction | set `whd/src/whd_wifi_api.c:844` |
| Value | `wl_ol_cfg_v1_t`, `sizeof` bytes; size is build-dependent: 32 with a 1-byte `whd_bool_t`, 40 with a 4-byte enum (compiled); fields written in host byte order, no conversion call `whd/src/whd_wifi_api.c:818-835` `whd/inc/whd_types.h:276-281` |
| Record | `wl_ol_cfg_v1_t` `whd/src/include/whd_wlioctl.h:4540-4569`, fields in declaration order; the union starts at offset 8 and offsets after `id` depend on the `whd_bool_t` width. uint16 `ver` at 0 = `WL_OL_CFG_VER_1` = 1 `whd/src/include/whd_wlioctl.h:4541` `whd/src/include/whd_wlioctl.h:4520`; uint16 `len` at 2 = `sizeof(wl_ol_cfg_v1_t)` `whd/src/include/whd_wlioctl.h:4542` `whd/src/whd_wifi_api.c:832`; uint32 `id` at 4: 1 PROF, 2 INET_V4, 3 INET_V6, 4 ACTIVATE `whd/src/include/whd_wlioctl.h:4543` `whd/src/include/whd_wlioctl.h:4522-4529`; union member `u.ol_profile`: uint32 `type` (1 low, 2 mid, 3 high power), whd_bool_t `reset`, uint8 `pad[3]` `whd/src/include/whd_wlioctl.h:4546-4550` `whd/src/include/whd_wlioctl.h:4531-4537`; union member `u.ol_inet_v4`: wl_ipv4_addr_t `host_ipv4`, whd_bool_t `del` (1 delete, 0 add), uint8 `pad[3]` `whd/src/include/whd_wlioctl.h:4551-4555`; union member `u.ol_inet_v6`: wl_ipv6_addr_t `host_ipv6`, uint8 `type` (0 unicast, 1 anycast), whd_bool_t `del`, uint8 `pad[2]` `whd/src/include/whd_wlioctl.h:4556-4561`; union member `u.ol_activate`: whd_bool_t `enable`, uint8 `pad[3]` `whd/src/include/whd_wlioctl.h:4562-4565`; uint32 `offload_skip` after the union, a bitmap of offloads to skip `whd/src/include/whd_wlioctl.h:4568` |

- whd — set — id = 1 (PROF), offload_skip = ~ol_feat; reset = 1 and type = -1 when resetting, else reset = 0 and type = 1 (low power) — `whd_wifi_offload_config`: select or reset the offload profile; whd then configures TKO offload — `whd/src/whd_wifi_api.c:805-856`
- whd — set — same call with ol_feat = `OFFLOAD_FEATURE`, reset = 0 — init sequence, only when firmware capability `WHD_FWCAP_OFFLOADS` is set; a failure aborts init — `whd/src/whd_management.c:535-544` `whd/src/include/whd_wlioctl.h:4729`
- whd — set — id = 2 (INET_V4), host_ipv4 = the 4 address bytes taken low byte first from the uint32 argument, del = !is_add, offload_skip = ~ol_feat — `whd_wifi_offload_ipv4_update` — `whd/src/whd_wifi_api.c:858-904`
- whd — set — id = 3 (INET_V6), host_ipv6 = address bytes, type = caller's type, del = !is_add, offload_skip = ~ol_feat — `whd_wifi_offload_ipv6_update` — `whd/src/whd_wifi_api.c:906-958`
- whd — set — id = 4 (ACTIVATE), enable = 1 or 0, offload_skip = ~ol_feat — `whd_wifi_offload_enable` — `whd/src/whd_wifi_api.c:960-998`
- whd — in the `PROTO_MSGBUF` build of `whd_wifi_offload_enable`, `ver` is not assigned before the copy — `whd/src/whd_wifi_api.c:979-983`
- whd — macro `IOVAR_STR_OFFLOAD_CONFIG` — `whd/src/include/whd_wlioctl.h:1270`

### `okc_enable`
| | |
|---|---|
| Used by | linux, through the bsscfg helper: bare name when the interface's bsscfg index is 0, otherwise `bsscfg:okc_enable` + NUL + 4-byte little-endian index before the value. Not found in embassy, whd, c-driver. `linux/brcmfmac/cfg80211.c:2227` `linux/brcmfmac/fwil.c:248-291` |
| Direction | get `linux/brcmfmac/cfg80211.c:2227` |
| Value | 4-byte little-endian integer `linux/brcmfmac/fwil.h:162-170` |
| Record | plain integer `linux/brcmfmac/fwil.h:162-170` |

- linux — get — one uint32 — `brcmf_set_key_mgmt`: read whether opportunistic key caching is enabled, only when the profile uses the firmware supplicant for 802.1X or roaming; the value is stored as the profile's `is_okc`, an error is logged — `linux/brcmfmac/cfg80211.c:2225-2234`

### `okc_info_pmk`
| | |
|---|---|
| Used by | linux (no prefix). Not found in embassy, whd, c-driver. `linux/brcmfmac/cfg80211.c:6084` |
| Direction | set `linux/brcmfmac/cfg80211.c:6084` |
| Value | raw PMK bytes, `pmk_len` bytes, at most 32 `linux/brcmfmac/cfg80211.c:6080-6085` `linux/brcmfmac/fwil_types.h:65` |
| Record | raw bytes, no wrapper record `linux/brcmfmac/cfg80211.c:6084-6085` |

- linux — set — `conf->pmk`, `conf->pmk_len` bytes — `brcmf_cfg80211_set_pmk`, only when the profile has `is_okc` set; a failure is logged — `linux/brcmfmac/cfg80211.c:6083-6088`

### `otpraw`
| | |
|---|---|
| Used by | defined, not used by whd. Not found in embassy, linux, c-driver. `whd/src/include/whd_wlioctl.h:1229` |
| Direction | not shown by any driver `whd/src/include/whd_wlioctl.h:1229` |
| Value | payload not shown by any driver `whd/src/include/whd_wlioctl.h:1229` |
| Record | not shown by any driver `whd/src/include/whd_wlioctl.h:1229` |

- whd — defined, not used: macro `IOVAR_STR_OTPRAW` only — `whd/src/include/whd_wlioctl.h:1229`

### `otptlv`
| | |
|---|---|
| Used by | whd (no prefix). Not found in embassy, linux, c-driver. `whd/src/whd_wifi_api.c:6613` |
| Direction | set `whd/src/whd_wifi_api.c:6616` |
| Value | caller's byte buffer, `len` bytes (`len` is a uint8), copied unchanged `whd/src/whd_wifi_api.c:6606-6615` |
| Record | TLV bytes supplied by the caller; layout not defined in this function `whd/src/whd_wifi_api.c:6606-6615` |

- whd — set — `tlvBuf`, `len` bytes — `whd_wifi_set_mac_addr_via_otp`: writes a caller-built TLV (the function name says a MAC address) to one-time-programmable memory — `whd/src/whd_wifi_api.c:6606-6616`
- whd — macro `IOVAR_STR_OTPTLV` — `whd/src/include/whd_wlioctl.h:1275`

### `p2p_da_override`
| | |
|---|---|
| Used by | linux (no prefix). Not found in embassy, whd, c-driver. `linux/brcmfmac/p2p.c:471-472` |
| Direction | set `linux/brcmfmac/p2p.c:471` |
| Value | MAC address, 6 bytes (`ETH_ALEN`; the value 6 is recalled, not in these sources) `linux/brcmfmac/p2p.c:471-472` |
| Record | raw bytes, no wrapper record `linux/brcmfmac/p2p.c:471-472` |

- linux — set — the P2P device MAC address — `brcmf_p2p_set_firmware`, sent right after `p2p_disc` = 0; a failure is logged — `linux/brcmfmac/p2p.c:464-474`

### `p2p_dev`
| | |
|---|---|
| Used by | linux (no prefix); whd: defined, not used by whd. Not found in embassy or c-driver. `linux/brcmfmac/p2p.c:2235` `whd/src/include/whd_wlioctl.h:1107` |
| Direction | get (linux) `linux/brcmfmac/p2p.c:2235` |
| Value | 4-byte little-endian integer `linux/brcmfmac/fwil.h:130-138` |
| Record | plain integer `linux/brcmfmac/fwil.h:130-138` |

- linux — get — one uint32, used as the bsscfg index of the P2P discovery interface — compared with the driver's own index for the P2P device interface (mismatch only warns) — `linux/brcmfmac/p2p.c:2234-2241`
- whd — defined, not used: macro `IOVAR_STR_P2P_DEV` only — `whd/src/include/whd_wlioctl.h:1107`

### `p2p_disc`
| | |
|---|---|
| Used by | linux (no prefix); whd: defined, not used by whd. Not found in embassy or c-driver. `linux/brcmfmac/p2p.c:469` `whd/src/include/whd_wlioctl.h:1106` |
| Direction | set (linux) `linux/brcmfmac/p2p.c:469` |
| Value | 4-byte little-endian integer `linux/brcmfmac/fwil.h:123-127` |
| Record | plain integer `linux/brcmfmac/fwil.h:123-127` |

- linux — set — 0 — `brcmf_p2p_set_firmware`: discovery off before `p2p_da_override` — `linux/brcmfmac/p2p.c:464-469`
- linux — set — 0 — `brcmf_p2p_deinit_discovery`, sent on the primary interface; result ignored — `linux/brcmfmac/p2p.c:596-598`
- linux — set — 1 — `brcmf_p2p_enable_discovery`, sent on the primary interface — `linux/brcmfmac/p2p.c:629-631`
- linux — set — 1 — creating the P2P device interface; linux then waits for event `BRCMF_E_IF_ADD` — `linux/brcmfmac/p2p.c:2208-2219`
- whd — defined, not used: macro `IOVAR_STR_P2P_DISC` only — `whd/src/include/whd_wlioctl.h:1106`

### `p2p_if`
| | |
|---|---|
| Used by | defined, not used by whd. Not found in embassy, linux, c-driver. `whd/src/include/whd_wlioctl.h:1108` |
| Direction | not shown by any driver `whd/src/include/whd_wlioctl.h:1108` |
| Value | payload not shown by any driver `whd/src/include/whd_wlioctl.h:1108` |
| Record | not shown by any driver `whd/src/include/whd_wlioctl.h:1108` |

- whd — defined, not used: macro `IOVAR_STR_P2P_IF` only — `whd/src/include/whd_wlioctl.h:1108`

### `p2p_ifadd`
| | |
|---|---|
| Used by | linux (no prefix); whd: defined, not used by whd. Not found in embassy or c-driver. `linux/brcmfmac/p2p.c:2140-2141` `whd/src/include/whd_wlioctl.h:1109` |
| Direction | set (linux) `linux/brcmfmac/p2p.c:2140` |
| Value | `struct brcmf_fil_p2p_if_le`, 10 bytes (computed, with `ETH_ALEN` = 6: recalled, not in these sources), little-endian fields `linux/brcmfmac/fwil_types.h:217-221` |
| Record | `struct brcmf_fil_p2p_if_le` `linux/brcmfmac/fwil_types.h:217-221`: u8 `addr[ETH_ALEN]` (MAC address) at 0 `linux/brcmfmac/fwil_types.h:218`, u16 `type` at 6: 0 CLIENT, 1 GO, 2 DYNBCN_GO, 3 DEV `linux/brcmfmac/fwil_types.h:219` `linux/brcmfmac/fwil_types.h:204-209`, u16 `chspec` (chanspec) at 8 `linux/brcmfmac/fwil_types.h:220` |

- linux — set — addr = the new interface's MAC, type = requested interface type, chspec = current chanspec — ask for a new P2P client or GO interface — `linux/brcmfmac/p2p.c:2132-2141`
- whd — defined, not used: macro `IOVAR_STR_P2P_IFADD` only — `whd/src/include/whd_wlioctl.h:1109`

### `p2p_ifdel`
| | |
|---|---|
| Used by | linux (no prefix); whd: defined, not used by whd. Not found in embassy or c-driver. `linux/brcmfmac/p2p.c:2163` `whd/src/include/whd_wlioctl.h:1110` |
| Direction | set (linux) `linux/brcmfmac/p2p.c:2163` |
| Value | MAC address, 6 bytes (`ETH_ALEN`; the value 6 is recalled, not in these sources) `linux/brcmfmac/p2p.c:2163` |
| Record | raw bytes, no wrapper record `linux/brcmfmac/p2p.c:2163` |

- linux — set — MAC address of the P2P interface's net device, sent on the primary interface — `brcmf_p2p_release_p2p_if`: delete the P2P interface — `linux/brcmfmac/p2p.c:2156-2164`
- whd — defined, not used: macro `IOVAR_STR_P2P_IFDEL` only — `whd/src/include/whd_wlioctl.h:1110`

### `p2p_ifdis`
| | |
|---|---|
| Used by | linux (no prefix). Not found in embassy, whd, c-driver. `linux/brcmfmac/p2p.c:2153` |
| Direction | set `linux/brcmfmac/p2p.c:2153` |
| Value | MAC address, 6 bytes (`ETH_ALEN`; the value 6 is recalled, not in these sources) `linux/brcmfmac/p2p.c:2153` |
| Record | raw bytes, no wrapper record `linux/brcmfmac/p2p.c:2153` |

- linux — set — MAC address of the P2P interface's net device, sent on the primary interface — `brcmf_p2p_disable_p2p_if`: disable the P2P interface — `linux/brcmfmac/p2p.c:2146-2154`

### `p2p_ifupd`
| | |
|---|---|
| Used by | linux (no prefix); whd: defined, not used by whd. Not found in embassy or c-driver. `linux/brcmfmac/p2p.c:2103-2104` `whd/src/include/whd_wlioctl.h:1111` |
| Direction | set (linux) `linux/brcmfmac/p2p.c:2103` |
| Value | `struct brcmf_fil_p2p_if_le`, 10 bytes (computed, with `ETH_ALEN` = 6: recalled, not in these sources), little-endian fields (layout under `p2p_ifadd`) `linux/brcmfmac/fwil_types.h:217-221` |
| Record | `struct brcmf_fil_p2p_if_le` `linux/brcmfmac/fwil_types.h:217-221` |

- linux — set — addr = the stored connection interface address, type = new interface type, chspec = current chanspec — change the role of the existing P2P connection interface; sent on that interface with the plain (non-bsscfg) helper, after `mpc` = 0; linux then waits for event `BRCMF_E_IF_CHANGE` — `linux/brcmfmac/p2p.c:2091-2111`
- whd — defined, not used: macro `IOVAR_STR_P2P_IFUPD` only — `whd/src/include/whd_wlioctl.h:1111`

### `p2p_ip_addr`
| | |
|---|---|
| Used by | defined, not used by whd. Not found in embassy, linux, c-driver. `whd/src/include/whd_wlioctl.h:1115` |
| Direction | not shown by any driver `whd/src/include/whd_wlioctl.h:1115` |
| Value | payload not shown by any driver `whd/src/include/whd_wlioctl.h:1115` |
| Record | not shown by any driver `whd/src/include/whd_wlioctl.h:1115` |

- whd — defined, not used: macro `IOVAR_STR_P2P_IP_ADDR` only — `whd/src/include/whd_wlioctl.h:1115`

### `p2p_scan`
| | |
|---|---|
| Used by | linux, through the bsscfg helper: bare name when the interface's bsscfg index is 0, otherwise `bsscfg:p2p_scan` + NUL + 4-byte little-endian index before the value. whd: defined, not used by whd. Not found in embassy or c-driver. `linux/brcmfmac/p2p.c:780` `linux/brcmfmac/fwil.c:248-291` `whd/src/include/whd_wlioctl.h:1112` |
| Direction | set (linux) `linux/brcmfmac/p2p.c:780` |
| Value | `struct brcmf_p2p_scan_le`, variable: offset of the channel list plus 2 bytes per channel; little-endian fields. The fixed part is 76 bytes (computed): 4 (type, reserved) + 8 (escan version, action, sync_id) + 64 (scan parameters up to the channel list: 36 SSID record, 6 bssid, 1 bss_type, 1 scan_type, 5 × 4), with `IEEE80211_MAX_SSID_LEN` = 32 and `ETH_ALEN` = 6 (the 6 is recalled, not in these sources) `linux/brcmfmac/p2p.c:675-685` `linux/brcmfmac/p2p.c:132-139` `linux/brcmfmac/fwil_types.h:460-468` `linux/brcmfmac/fwil_types.h:357-407` `linux-headers/ieee80211.h:227` |
| Record | `struct brcmf_p2p_scan_le` `linux/brcmfmac/p2p.c:132-139`, wrapping `struct brcmf_escan_params_le` `linux/brcmfmac/fwil_types.h:460-468`. Head: u8 `type` at 0, 'E' or 'S' `linux/brcmfmac/p2p.c:133` `linux/brcmfmac/p2p.c:126`; u8 `reserved[3]` at 1 `linux/brcmfmac/p2p.c:134`; from 4, variable length, escan parameters (type 'E') or scan parameters (type 'S') `linux/brcmfmac/p2p.c:135-138` |

- linux — set — type = 'E'; escan version = 1, action = `WL_ESCAN_ACTION_START` (1), sync_id = 0x1234; scan parameters: bss_type = 2 (any), scan_type = 0 (active), bssid = broadcast, home_time = 60, passive_time = -1, active_time and nprobes computed from the channel count, channel_num = count masked with 0x0000ffff, then one 2-byte chanspec per channel — `brcmf_p2p_escan`: start a P2P scan; on success linux marks the scan busy — `linux/brcmfmac/p2p.c:730-782` `linux/brcmfmac/fwil_types.h:57-73` `linux/brcmfmac/cfg80211.h:51` `linux/brcmfmac/p2p.c:27`
- linux — SSID field: 7 bytes "DIRECT-" for search state SCAN; left empty (zeroed buffer) for search state SEARCH — `linux/brcmfmac/p2p.c:699-717` `linux/brcmfmac/p2p.c:33-34`
- linux — sends `p2p_state` on the same interface immediately before this — `linux/brcmfmac/p2p.c:725`
- whd — defined, not used: macro `IOVAR_STR_P2P_SCAN` only — `whd/src/include/whd_wlioctl.h:1112`

### `p2p_ssid`
| | |
|---|---|
| Used by | defined, not used by whd. Not found in embassy, linux, c-driver. `whd/src/include/whd_wlioctl.h:1114` |
| Direction | not shown by any driver `whd/src/include/whd_wlioctl.h:1114` |
| Value | payload not shown by any driver `whd/src/include/whd_wlioctl.h:1114` |
| Record | not shown by any driver `whd/src/include/whd_wlioctl.h:1114` |

- whd — defined, not used: macro `IOVAR_STR_P2P_SSID` only — `whd/src/include/whd_wlioctl.h:1114`

### `p2p_state`
| | |
|---|---|
| Used by | linux, through the bsscfg helper: bare name when the interface's bsscfg index is 0, otherwise `bsscfg:p2p_state` + NUL + 4-byte little-endian index before the value. whd: defined, not used by whd. Not found in embassy or c-driver. `linux/brcmfmac/p2p.c:574-575` `linux/brcmfmac/fwil.c:248-291` `whd/src/include/whd_wlioctl.h:1113` |
| Direction | set (linux) `linux/brcmfmac/p2p.c:574` |
| Value | `struct brcmf_p2p_disc_st_le`, `sizeof` bytes; the struct is not packed, so 6 bytes with one padding byte after `state` (compiled); little-endian fields `linux/brcmfmac/p2p.c:105-109` `linux/brcmfmac/p2p.c:574-575` |
| Record | `struct brcmf_p2p_disc_st_le` `linux/brcmfmac/p2p.c:105-109`, offsets as compiled: u8 `state` at 0: 0 SCAN, 1 LISTEN, 2 SEARCH `linux/brcmfmac/p2p.c:106` `linux/brcmfmac/p2p.c:118-122`; 1 padding byte at 1, which linux does not initialise (local struct, three fields assigned) `linux/brcmfmac/p2p.c:567-573`; u16 `chspec` at 2, used for LISTEN only `linux/brcmfmac/p2p.c:107` `linux/brcmfmac/p2p.c:561`; u16 `dwell` in ms at 4, used for LISTEN only `linux/brcmfmac/p2p.c:108` `linux/brcmfmac/p2p.c:103` |

- linux — set — state = SCAN, chspec = 0, dwell = 0 — `brcmf_p2p_deinit_discovery`, on the P2P device interface; result ignored — `linux/brcmfmac/p2p.c:592-594`
- linux — set — state = SCAN, chspec = 0, dwell = 0 — `brcmf_p2p_enable_discovery`, on the P2P device interface — `linux/brcmfmac/p2p.c:636-637`
- linux — set — state = SCAN or SEARCH (other values rejected first), chspec = 0, dwell = 0 — just before `p2p_scan` — `linux/brcmfmac/p2p.c:699-725`
- linux — set — state = LISTEN, chspec = 20 MHz chanspec of the listen channel, dwell = duration truncated to 16 bits — discovery listen — `linux/brcmfmac/p2p.c:977-981`
- linux — set — state = SCAN, chspec = 0, dwell = 0 — cancel remain-on-channel — `linux/brcmfmac/p2p.c:1074`
- linux — set — state = SCAN, chspec = 0, dwell = 0 — stopping the P2P device; result ignored — `linux/brcmfmac/p2p.c:2509-2511`
- whd — defined, not used: macro `IOVAR_STR_P2P_STATE` only — `whd/src/include/whd_wlioctl.h:1113`

### `per_chan_info`
| | |
|---|---|
| Used by | linux, through the bsscfg helper: bare name when the interface's bsscfg index is 0, otherwise `bsscfg:per_chan_info` + NUL + 4-byte little-endian index before the value. Not found in embassy, whd, c-driver. `linux/brcmfmac/cfg80211.c:7325-7326` `linux/brcmfmac/fwil.c:248-291` |
| Direction | get, with an input value in the request `linux/brcmfmac/cfg80211.c:7325-7326` `linux/brcmfmac/fwil.h:172-178` |
| Value | request: 4-byte little-endian chanspec; reply: 4-byte little-endian flag word `linux/brcmfmac/cfg80211.c:7324-7328` `linux/brcmfmac/fwil.h:162-178` |
| Record | plain integer; linux tests reply bits `WL_CHAN_*` `linux/include/brcmu_wifi.h:64-69` |

- linux — get — sends the channel's 20 MHz chanspec, reads back a flag word and tests `WL_CHAN_RADAR` (bit 3) and `WL_CHAN_PASSIVE` (bit 5); a failed query is ignored — `brcmf_construct_chaninfo`: per-channel radar/passive flags — `linux/brcmfmac/cfg80211.c:7322-7335` `linux/include/brcmu_wifi.h:67` `linux/include/brcmu_wifi.h:69`

### `pfn`
| | |
|---|---|
| Used by | linux (no prefix); whd: defined, not used by whd. Not found in embassy or c-driver. `linux/brcmfmac/pno.c:262` `whd/src/include/whd_wlioctl.h:1188` |
| Direction | linux: both `linux/brcmfmac/pno.c:262` `linux/brcmfmac/feature.c:308` |
| Value | 4-byte little-endian integer `linux/brcmfmac/fwil.h:123-138` |
| Record | plain integer `linux/brcmfmac/fwil.h:123-138` |

- linux — set — 0 — `brcmf_pno_clean`: disable preferred-network offload before clearing its configuration — `linux/brcmfmac/pno.c:261-262`
- linux — set — 1 — enable after configuration — `linux/brcmfmac/pno.c:454-455`
- linux — get — value discarded; the 4 request bytes are an uninitialised local — feature probe for `BRCMF_FEAT_PNO`: the feature is enabled unless the reply is the firmware "unsupported" error — `linux/brcmfmac/feature.c:187-206` `linux/brcmfmac/feature.c:308`
- whd — defined, not used: macro `IOVAR_STR_PNO_ON` only — `whd/src/include/whd_wlioctl.h:1188`

### `pfn_add`
| | |
|---|---|
| Used by | linux, no "bsscfg:" prefix `linux/brcmfmac/pno.c:215`. whd: defined, not used by whd `whd/src/include/whd_wlioctl.h:1189`. Not found in embassy or c-driver |
| Direction | linux: set `linux/brcmfmac/pno.c:215` |
| Value | linux: `struct brcmf_pno_net_param_le`, 56 bytes, all fields little-endian `linux/brcmfmac/fwil_types.h:1037-1044` `linux/brcmfmac/fwil_types.h:357-360` `linux-headers/ieee80211.h:227` |
| Record | `struct brcmf_pno_net_param_le`: `ssid` (`struct brcmf_ssid_le`: u32 `SSID_len` at 0, `SSID[32]` at 4), then u32 `flags` at 36, `infra` at 40, `auth` at 44, `wpa_auth` at 48, `wsec` at 52 (offsets computed from the field list; the struct is not packed) `linux/brcmfmac/fwil_types.h:1037-1044` `linux/brcmfmac/fwil_types.h:357-360` |

- linux — set — `auth` = `WLAN_AUTH_OPEN` (0), `wpa_auth` = `BRCMF_PNO_WPA_AUTH_ANY` (0xFFFFFFFF), `wsec` = 0, `infra` = 1, `flags` = 0, or 4 (bit `BRCMF_PNO_HIDDEN_BIT` = 2) when the SSID is also in the request's `ssids` list (same length, same bytes) — adds one preferred SSID to the PNO list, once per match set with a non-empty SSID — `linux/brcmfmac/pno.c:204-215` `linux/brcmfmac/pno.c:24-25` `linux/brcmfmac/pno.c:238-254` `linux/brcmfmac/pno.c:376-379` `linux-headers/ieee80211.h:1369`
- linux — the record is a stack variable that is not zeroed; only `ssid_len` bytes of `SSID` are written, so the rest of the 32 SSID bytes go out uninitialised — `linux/brcmfmac/pno.c:201` `linux/brcmfmac/pno.c:211-212`
- linux — sent as name, NUL, record with command `BRCMF_C_SET_VAR` (263) — `linux/brcmfmac/fwil.c:166-184` `linux/brcmfmac/fwil.c:204` `linux/brcmfmac/fwil.h:81`
- whd — defined as `IOVAR_STR_PNO_ADD`, no call site in whd; payload not shown by whd — `whd/src/include/whd_wlioctl.h:1189` `whd/src/include_helium/whd_wlioctl.h:1190`

### `pfn_add_bssid`
| | |
|---|---|
| Used by | linux, no "bsscfg:" prefix `linux/brcmfmac/pno.c:231-232`. Not found in embassy, whd or c-driver |
| Direction | linux: set `linux/brcmfmac/pno.c:231-232` |
| Value | linux: `struct brcmf_pno_bssid_le`, 8 bytes; `flags` little-endian `linux/brcmfmac/fwil_types.h:1120-1123` |
| Record | `struct brcmf_pno_bssid_le`: u8 `bssid[ETH_ALEN]` at 0, u16 `flags` at 6 `linux/brcmfmac/fwil_types.h:1120-1123`. `ETH_ALEN` = 6 (recalled, not in these sources) |

- linux — set — `bssid` copied from the match set, `flags` = 0 — adds one BSSID to the PNO list, once per match set with a valid BSSID — `linux/brcmfmac/pno.c:227-232` `linux/brcmfmac/pno.c:381-382`

### `pfn_cfg`
| | |
|---|---|
| Used by | linux, no "bsscfg:" prefix `linux/brcmfmac/pno.c:99`. Not found in embassy, whd or c-driver |
| Direction | linux: set `linux/brcmfmac/pno.c:99` |
| Value | linux: `struct brcmf_pno_config_le`, 140 bytes, all fields little-endian `linux/brcmfmac/fwil_types.h:1020-1025` `linux/brcmfmac/fwil_types.h:157` |
| Record | `struct brcmf_pno_config_le`: u32 `reporttype` at 0, u32 `channel_num` at 4, u16 `channel_list[64]` at 8, u32 `flags` at 136 `linux/brcmfmac/fwil_types.h:1020-1025` `linux/brcmfmac/fwil_types.h:157` |

- linux — set — `reporttype` = 0 and `flags` = 0 forced; `channel_num` and `channel_list` come from the caller — sets the PNO channel list, after `pfn_set` and before `pfn_gscan_cfg` — `linux/brcmfmac/pno.c:96-99` `linux/brcmfmac/pno.c:423-427`

### `pfn_gscan_cfg`
| | |
|---|---|
| Used by | linux, no "bsscfg:" prefix `linux/brcmfmac/pno.c:440` `linux/brcmfmac/feature.c:305-307`. Not found in embassy, whd or c-driver |
| Direction | linux: set `linux/brcmfmac/pno.c:440` |
| Value | linux: `struct brcmf_gscan_config` followed by n `struct brcmf_gscan_bucket_config`, 10 + 8 × n bytes; 16-bit fields little-endian `linux/brcmfmac/fwil_types.h:1208-1218` `linux/brcmfmac/fwil_types.h:1168-1175` `linux/brcmfmac/pno.c:408` |
| Record | `struct brcmf_gscan_config`: u16 `version` at 0, u8 `flags` at 2, u8 `buffer_threshold` at 3, u8 `swc_nbssid_threshold` at 4, u8 `swc_rssi_window_size` at 5, u8 `count_of_channel_buckets` at 6, u8 `retry_threshold` at 7, u16 `lost_ap_window` at 8, `bucket[]` at 10 `linux/brcmfmac/fwil_types.h:1208-1218`. `struct brcmf_gscan_bucket_config`, 8 bytes: u8 `bucket_end_index` at 0, u8 `bucket_freq_multiple` at 1, u8 `flag` at 2, u8 `reserved` at 3, u16 `repeat` at 4, u16 `max_freq_multiple` at 6 `linux/brcmfmac/fwil_types.h:1168-1175` |

- linux — set — `version` = `BRCMF_GSCAN_CFG_VERSION` (2), `retry_threshold` = 3, `buffer_threshold` = 101, `flags` = `BRCMF_GSCAN_CFG_ALL_BUCKETS_IN_1ST_SCAN` (bit 3), `count_of_channel_buckets` = n, then the n bucket records; other fields zero from `kzalloc` — configures the channel buckets for scheduled scans — `linux/brcmfmac/pno.c:408-409` `linux/brcmfmac/pno.c:431-440` `linux/brcmfmac/pno.c:29-30` `linux/brcmfmac/fwil_types.h:1178` `linux/brcmfmac/fwil_types.h:1190`
- linux — set — the 10-byte header alone, all zero — feature probe: any result other than `-BRCMF_FW_UNSUPPORTED` enables `BRCMF_FEAT_GSCAN` — `linux/brcmfmac/feature.c:300` `linux/brcmfmac/feature.c:305-307` `linux/brcmfmac/feature.c:217-220`
- linux — the probe is skipped for chip ids `BRCM_CC_43430_CHIP_ID`, `BRCM_CC_4345_CHIP_ID`, `BRCM_CC_43454_CHIP_ID` and `CY_CC_43439_CHIP_ID`, so linux does not send the probe to a CYW43439 — `linux/brcmfmac/feature.c:301-304`

### `pfn_macaddr`
| | |
|---|---|
| Used by | linux, no "bsscfg:" prefix `linux/brcmfmac/pno.c:189-190` `linux/brcmfmac/feature.c:338-339`. Not found in embassy, whd or c-driver |
| Direction | linux: both; set `linux/brcmfmac/pno.c:189-190`, get `linux/brcmfmac/feature.c:338-339` |
| Value | linux: `struct brcmf_pno_macaddr_le`, 8 bytes, byte fields only `linux/brcmfmac/fwil_types.h:1092-1096` |
| Record | `struct brcmf_pno_macaddr_le`: u8 `version` at 0, u8 `flags` at 1, u8 `mac[ETH_ALEN]` at 2 `linux/brcmfmac/fwil_types.h:1092-1096`. `ETH_ALEN` = 6 (recalled, not in these sources) |

- linux — set — `version` = `BRCMF_PFN_MACADDR_CFG_VER` (1), `flags` = `BRCMF_PFN_MAC_OUI_ONLY` \| `BRCMF_PFN_SET_MAC_UNASSOC` (bits 0 and 1, value 3), `mac` = request address with the unmasked bits randomised, bit 0 of byte 0 cleared and bit 1 of byte 0 set — random MAC for PNO scans; sent only when a scheduled-scan request has `NL80211_SCAN_FLAG_RANDOM_ADDR` — `linux/brcmfmac/pno.c:163-190` `linux/brcmfmac/fwil_types.h:159-161`
- linux — get — request buffer is the 8-byte record with `version` = 1 and the other 7 bytes uninitialised stack; the reply is not examined — feature probe: no error enables `BRCMF_FEAT_SCAN_RANDOM_MAC` — `linux/brcmfmac/feature.c:294` `linux/brcmfmac/feature.c:337-341`
- linux — a get carries input: the caller's buffer is copied after the name before `BRCMF_C_GET_VAR` (262) is sent, and the reply overwrites it — `linux/brcmfmac/fwil.c:226-232` `linux/brcmfmac/fwil.h:80`

### `pfn_set`
| | |
|---|---|
| Used by | linux, no "bsscfg:" prefix `linux/brcmfmac/pno.c:146-147`. whd: defined, not used by whd `whd/src/include/whd_wlioctl.h:1190`. Not found in embassy or c-driver |
| Direction | linux: set `linux/brcmfmac/pno.c:146-147` |
| Value | linux: `struct brcmf_pno_param_le`, 24 bytes, multi-byte fields little-endian `linux/brcmfmac/fwil_types.h:999-1010` |
| Record | `struct brcmf_pno_param_le`: u32 `version` at 0, u32 `scan_freq` at 4, u32 `lost_network_timeout` at 8, u16 `flags` at 12, u16 `rssi_margin` at 14, u8 `bestn` at 16, u8 `mscan` at 17, u8 `repeat` at 18, u8 `exp` at 19, u32 `slow_freq` at 20 `linux/brcmfmac/fwil_types.h:999-1010` |

- linux — set — `version` = `BRCMF_PNO_VERSION` (2), `flags` = bit 3 (`BRCMF_PNO_IMMEDIATE_SCAN_BIT`) \| bit 6 (`BRCMF_PNO_ENABLE_ADAPTSCAN_BIT`) = 72 (0x48), `repeat` = 4, `exp` = 3, `scan_freq` from the caller, everything else zero — PNO scan parameters, first variable sent after the `pfn` = 0 / `pfnclear` clean-up — `linux/brcmfmac/pno.c:111-121` `linux/brcmfmac/pno.c:145-147` `linux/brcmfmac/pno.c:16-21` `linux/brcmfmac/pno.c:416-423`
- linux — when `mscan` is non-zero the code also sets bit 5 (`BRCMF_PNO_ENABLE_BD_SCAN_BIT`) and fills `mscan` and `bestn`; the only caller passes `mscan` = 0 — `linux/brcmfmac/pno.c:123-143` `linux/brcmfmac/pno.c:423`
- whd — defined as `IOVAR_STR_PNO_SET`, no call site in whd; payload not shown by whd — `whd/src/include/whd_wlioctl.h:1190` `whd/src/include_helium/whd_wlioctl.h:1191`

### `pfnclear`
| | |
|---|---|
| Used by | linux, no "bsscfg:" prefix `linux/brcmfmac/pno.c:265`. whd: defined, not used by whd `whd/src/include/whd_wlioctl.h:1191`. Not found in embassy or c-driver |
| Direction | linux: set `linux/brcmfmac/pno.c:265` |
| Value | linux: no value, 0 bytes; only the name and its NUL are sent `linux/brcmfmac/pno.c:265` `linux/brcmfmac/fwil.c:172-183` |
| Record | none |

- linux — set — empty — clears the PNO configuration; sent only if the preceding `pfn` = 0 set returned 0 — `linux/brcmfmac/pno.c:261-266`
- linux — run before each scheduled-scan configuration, on a configuration error, and after a scheduled-scan request is removed — `linux/brcmfmac/pno.c:416` `linux/brcmfmac/pno.c:458-459` `linux/brcmfmac/pno.c:503-507`
- whd — defined as `IOVAR_STR_PNO_CLEAR`, no call site in whd — `whd/src/include/whd_wlioctl.h:1191` `whd/src/include_helium/whd_wlioctl.h:1192`

### `pfnmem`
| | |
|---|---|
| Used by | linux, no "bsscfg:" prefix `linux/brcmfmac/pno.c:127` `linux/brcmfmac/pno.c:133`. Not found in embassy, whd or c-driver |
| Direction | linux: both; set `linux/brcmfmac/pno.c:127`, get `linux/brcmfmac/pno.c:133` |
| Value | linux: u32, 4 bytes, little-endian `linux/brcmfmac/fwil.h:122-138` |
| Record | plain integer |

- linux — set — `bestn` — a source comment reads "set bestn in firmware" — `linux/brcmfmac/pno.c:124-127`
- linux — get — one u32; linux clamps `mscan` to it, and a source comment reads "get max mscan which the firmware supports" — `linux/brcmfmac/pno.c:132-138`
- linux — both calls sit in the `mscan != 0` branch, and the only caller passes `mscan` = 0, so linux sends neither — `linux/brcmfmac/pno.c:123` `linux/brcmfmac/pno.c:423`

### `phyrate_dump`
| | |
|---|---|
| Used by | whd: defined, not used by whd `whd/src/include/whd_wlioctl.h:1155`. Not found in embassy, linux or c-driver |
| Direction | not shown by any driver |
| Value | payload not shown by any driver |
| Record | not shown by any driver |

- whd — defined as `IOVAR_STR_PHYRATE_LOG_DUMP`, no call site in whd — `whd/src/include/whd_wlioctl.h:1155` `whd/src/include_helium/whd_wlioctl.h:1156`

### `phyrate_log`
| | |
|---|---|
| Used by | whd: defined, not used by whd `whd/src/include/whd_wlioctl.h:1153`. Not found in embassy, linux or c-driver |
| Direction | not shown by any driver |
| Value | payload not shown by any driver |
| Record | not shown by any driver |

- whd — defined as `IOVAR_STR_PHYRATE_LOG`, no call site in whd — `whd/src/include/whd_wlioctl.h:1153` `whd/src/include_helium/whd_wlioctl.h:1154`

### `phyrate_log_size`
| | |
|---|---|
| Used by | whd: defined, not used by whd `whd/src/include/whd_wlioctl.h:1154`. Not found in embassy, linux or c-driver |
| Direction | not shown by any driver |
| Value | payload not shown by any driver |
| Record | not shown by any driver |

- whd — defined as `IOVAR_STR_PHYRATE_LOG_SIZE`, no call site in whd — `whd/src/include/whd_wlioctl.h:1154` `whd/src/include_helium/whd_wlioctl.h:1155`

### `pkt_filter_add`
| | |
|---|---|
| Used by | whd, no "bsscfg:" prefix `whd/src/whd_wifi_api.c:6006-6007`. linux: record defined, no call site `linux/brcmfmac/fwil_types.h:294-302`. Not found in embassy or c-driver |
| Direction | whd: set `whd/src/whd_wifi_api.c:6023` |
| Value | whd: `wl_pkt_filter_t` with trailing mask and pattern, 20 + 2 × mask_size bytes; fields assigned without `htod32` (host byte order) `whd/src/whd_wifi_api.c:5999-6000` `whd/src/whd_wifi_api.c:6011-6015` `whd/src/include/whd_wlioctl.h:3652-3653` |
| Record | whd `wl_pkt_filter_t`: u32 `id` at 0, u32 `type` at 4, u32 `negate_match` at 8, then `wl_pkt_filter_pattern_t`: u32 `offset` at 12, u32 `size_bytes` at 16, `mask_and_pattern[]` at 20 `whd/src/include/whd_wlioctl.h:3636-3651`. linux `struct brcmf_pkt_filter_le` has the same three leading `__le32` fields `linux/brcmfmac/fwil_types.h:295-302`, followed by `struct brcmf_pkt_filter_pattern_le` (`__le32 offset`, `__le32 size_bytes`, `mask_and_pattern[1]`) `linux/brcmfmac/fwil_types.h:279-292`; see records `brcmf_pkt_filter_le` (linux), `brcmf_pkt_filter_pattern_le` (linux) and `wl_pkt_filter_t` (whd) |

- whd — set — `id` = caller's id, `type` = 0, `negate_match` = caller's rule (0 positive, 1 negative matching), `offset` = caller's byte offset, `size_bytes` = mask_size, then mask_size mask bytes followed by mask_size pattern bytes — `whd_pf_add_packet_filter`: installs one pattern-match filter — `whd/src/whd_wifi_api.c:5994-6023` `whd/inc/whd_types.h:1456-1457` `whd/inc/whd_types.h:1463-1472`
- whd — the only filter type whd defines is `WL_PKT_FILTER_TYPE_PATTERN_MATCH` (first enumerator, 0) — `whd/src/include/whd_wlioctl.h:3631-3634`
- linux — a header comment names this variable as the user of `struct brcmf_pkt_filter_le`; no linux `.c` file sends it, and no driver defines a bare `pkt_filter` variable — `linux/brcmfmac/fwil_types.h:294-302`

### `pkt_filter_clear_stats`
| | |
|---|---|
| Used by | whd, no "bsscfg:" prefix `whd/src/whd_wifi_api.c:6074`. Not found in embassy, linux or c-driver |
| Direction | whd: set `whd/src/whd_wifi_api.c:6074` |
| Value | whd: u32, 4 bytes, little-endian (`htod32`) `whd/src/whd_wifi_api.c:5153-5162` |
| Record | plain integer |

- whd — set — filter id — `whd_wifi_clear_packet_filter_stats`: clears one filter's counters — `whd/src/whd_wifi_api.c:6071-6075`

### `pkt_filter_delete`
| | |
|---|---|
| Used by | whd, no "bsscfg:" prefix `whd/src/whd_wifi_api.c:6035-6036`. Not found in embassy, linux or c-driver |
| Direction | whd: set `whd/src/whd_wifi_api.c:6039` |
| Value | whd: u32, 4 bytes, assigned without `htod32` (host byte order) `whd/src/whd_wifi_api.c:6035-6038` |
| Record | plain integer |

- whd — set — filter id (a u8 widened to u32) — `whd_pf_remove_packet_filter`: removes one filter — `whd/src/whd_wifi_api.c:6026-6039`

### `pkt_filter_enable`
| | |
|---|---|
| Used by | whd, no "bsscfg:" prefix `whd/src/whd_wifi_api.c:5967-5969`. linux: record defined, no call site `linux/brcmfmac/fwil_types.h:304-308`. Not found in embassy or c-driver |
| Direction | whd: set `whd/src/whd_wifi_api.c:5978` |
| Value | whd: `wl_pkt_filter_enable_t`, 8 bytes, assigned without `htod32` (host byte order) `whd/src/whd_wifi_api.c:5967-5973` |
| Record | whd `wl_pkt_filter_enable_t`: u32 `id` at 0, u32 `enable` at 4 `whd/src/include/whd_wlioctl.h:3654-3658`. linux `struct brcmf_pkt_filter_enable_le`: `__le32 id`, `__le32 enable` `linux/brcmfmac/fwil_types.h:305-308`; see records `brcmf_pkt_filter_enable_le` (linux) and `wl_pkt_filter_enable_t` (whd) |

- whd — set — `id` = filter id, `enable` = 1 or 0 — `whd_wifi_toggle_packet_filter`, reached from `whd_pf_enable_packet_filter` and `whd_pf_disable_packet_filter` — `whd/src/whd_wifi_api.c:5958-5991`
- whd — in `PROTO_MSGBUF` builds the two fields are filled by `memcpy` of the 1-byte id and of `sizeof(whd_bool_t)` bytes instead of u32 assignments; the function does not zero the buffer before the copies — `whd/src/whd_wifi_api.c:5967-5977`
- linux — a header comment names this variable as the user of `struct brcmf_pkt_filter_enable_le`; no linux `.c` file sends it — `linux/brcmfmac/fwil_types.h:304-308`

### `pkt_filter_list`
| | |
|---|---|
| Used by | whd, no "bsscfg:" prefix `whd/src/whd_wifi_api.c:6098-6099`. Not found in embassy, linux or c-driver |
| Direction | whd: get `whd/src/whd_wifi_api.c:6103` |
| Value | whd: request buffer 1000 bytes (`PACKET_FILTER_LIST_BUFFER_MAX_LEN`) with a u32 selector at 0, host byte order; reply `wl_pkt_filter_list_t`, variable length, read without byte swapping `whd/src/whd_wifi_api.c:6098-6107` `whd/inc/whd_types.h:1450` |
| Record | `wl_pkt_filter_list_t`: u32 `num` at 0, then `num` `wl_pkt_filter_t` entries from 4 `whd/src/include/whd_wlioctl.h:3659-3663`; entry layout as in `pkt_filter_add` `whd/src/include/whd_wlioctl.h:3636-3651` |

- whd — get — selector 0, then, if the id was not in that reply, a second get with selector 1; the loop variable is named `enabled_list`, so 0 = disabled filters and 1 = enabled filters (inferred from the name) — `whd_pf_get_packet_filter_mask_and_pattern`: finds the filter with a given id and copies out its mask and pattern — `whd/src/whd_wifi_api.c:6087-6122`
- whd — expects each reply entry to be 20 + 2 × `size_bytes` long, with the next entry starting at the next 4-byte boundary — `whd/src/whd_wifi_api.c:6124-6131`
- whd — only the selector word of the 1000-byte request is written — `whd/src/whd_wifi_api.c:6098-6101`

### `pkt_filter_mode`
| | |
|---|---|
| Used by | whd: defined, not used by whd `whd/src/include/whd_wlioctl.h:1095`. Not found in embassy, linux or c-driver |
| Direction | not shown by any driver |
| Value | payload not shown by any driver |
| Record | not shown by any driver |

- whd — defined as `IOVAR_STR_PKT_FILTER_MODE`, no call site in whd — `whd/src/include/whd_wlioctl.h:1095` `whd/src/include_helium/whd_wlioctl.h:1096`

### `pkt_filter_stats`
| | |
|---|---|
| Used by | whd, no "bsscfg:" prefix `whd/src/whd_wifi_api.c:6054-6056`. Not found in embassy, linux or c-driver |
| Direction | whd: get `whd/src/whd_wifi_api.c:6062` |
| Value | whd: request 16 bytes, zeroed, with the u32 filter id at 0 in host byte order; reply `wl_pkt_filter_stats_t`, 12 bytes, copied without byte swapping `whd/src/whd_wifi_api.c:6054-6065` |
| Record | `wl_pkt_filter_stats_t`: u32 `num_pkts_matched` at 0, u32 `num_pkts_forwarded` at 4, u32 `num_pkts_discarded` at 8 `whd/src/include/whd_wlioctl.h:3665-3670` |

- whd — get — filter id in, three counters out — `whd_pf_get_packet_filter_stats`; the public type `whd_pkt_filter_stats_t` is the same struct — `whd/src/whd_wifi_api.c:6042-6068` `whd/inc/whd_types.h:144`

### `pm2_sleep_ret`
| | |
|---|---|
| Used by | embassy `embassy/control.rs:357`, linux `linux/brcmfmac/cfg80211.c:3381`, whd `whd/src/whd_wifi_api.c:3905`, c-driver `c-driver/cyw43_ll.c:2148`; none uses a "bsscfg:" prefix |
| Direction | embassy: set `embassy/control.rs:357`. linux: set `linux/brcmfmac/cfg80211.c:3381`. whd: set `whd/src/whd_wifi_api.c:3905`. c-driver: both, set `c-driver/cyw43_ll.c:2148`, get `c-driver/cyw43_ll.c:2180` |
| Value | all four: u32, 4 bytes, little-endian `embassy/control.rs:702-704` `linux/brcmfmac/fwil.h:122-128` `whd/src/whd_wifi_api.c:5153-5162` `c-driver/cyw43_ll.c:1538-1544` |
| Record | plain integer |

- embassy — set — 2000 (SuperSave, Aggressive), 200 (PowerSave) or 20 (Performance); the helper is named `sleep_ret_ms` — sent only when the mode number is 2, as the first of four variables, followed by command `SetPm` — `embassy/control.rs:353-362` `embassy/lib.rs:434-443` `embassy/lib.rs:478-484`
- embassy — sent as name, NUL, value with command `SetVar` (263) on interface 0 — `embassy/control.rs:717-727` `embassy/consts.rs:684`
- linux — set — `min(timeout, BRCMF_PS_MAX_TIMEOUT_MS)`, cap 2000 — `brcmf_cfg80211_set_power_mgmt`; sent after command `BRCMF_C_SET_PM`, whether power save was enabled or disabled — `linux/brcmfmac/cfg80211.c:3365-3384` `linux/brcmfmac/cfg80211.c:90`
- whd — set — the argument rounded down to a multiple of 10; arguments below 10 or above 2000 are refused before sending — `whd_wifi_enable_powersave_with_throughput`; followed by command `WLC_SET_PM` with `PM2_POWERSAVE_MODE` (2) — `whd/src/whd_wifi_api.c:3881-3919` `whd/src/whd_wifi_api.c:87-88` `whd/inc/whd_types.h:86` `whd/src/include/whd_wlioctl.h:1081`
- whd — set — 200 (`DEFAULT_PM2_SLEEP_RET_TIME`) — init sequence, for every chip id except 43909, 43907 and 54907 — `whd/src/whd_management.c:548-565` `whd/src/whd_management.c:56`
- c-driver — set — `pm_sleep_ret` × 10 after clamping `pm_sleep_ret` to 1..200, so 10..2000 in steps of 10; a source comment gives the unit as ms — `cyw43_ll_wifi_pm`, interface 0, followed by three more variables and command `WLC_SET_PM` — `c-driver/cyw43_ll.c:2135-2165` `c-driver/cyw43_ll.c:151` `c-driver/cyw43_ctrl.c:510-515`
- c-driver — get — request is name, NUL and four zero bytes with command `WLC_GET_VAR` (262); the reply u32 is read from the start of the buffer — `cyw43_ll_wifi_get_pm` — `c-driver/cyw43_ll.c:1969-1976` `c-driver/cyw43_ll.c:2178-2180` `c-driver/cyw43_ll.c:186` `c-driver/cyw43_ctrl.c:535`
- c-driver — a second read sits in an `#if 0` block and is not compiled — `c-driver/cyw43_ll.c:2158-2163`

Differences: same size and layout in all four. Value ranges differ: embassy sends only 2000, 200 or 20 `embassy/lib.rs:434-443`; linux sends any value up to 2000 without rounding `linux/brcmfmac/cfg80211.c:3381-3382`; whd sends multiples of 10 in 10..2000 `whd/src/whd_wifi_api.c:3893-3906`; c-driver sends multiples of 10 in 10..2000 `c-driver/cyw43_ll.c:2143-2148`. Order differs: linux sends the PM command first `linux/brcmfmac/cfg80211.c:3373-3381`; embassy, whd and c-driver send the variable first `embassy/control.rs:357-362` `whd/src/whd_wifi_api.c:3905-3919` `c-driver/cyw43_ll.c:2148-2165`.

### `pm_limit`
| | |
|---|---|
| Used by | whd, no "bsscfg:" prefix `whd/src/whd_wifi_api.c:3911`. Not found in embassy, linux or c-driver |
| Direction | whd: set `whd/src/whd_wifi_api.c:3911` |
| Value | whd: u32, 4 bytes, little-endian (`htod32`) `whd/src/whd_wifi_api.c:5153-5162` |
| Record | plain integer |

- whd — set — 100 (`NULL_FRAMES_WITH_PM_SET_LIMIT`) — sent between `pm2_sleep_ret` and `WLC_SET_PM`, only when the chip id is 43362; whd does not send it to a CYW43439 — `whd/src/whd_wifi_api.c:3907-3912` `whd/src/whd_wifi_api.c:89`
- whd — reached from the init sequence through the same helper — `whd/src/whd_management.c:565`
- whd — macro `IOVAR_STR_PM_LIMIT` — `whd/src/include/whd_wlioctl.h:1082` `whd/src/include_helium/whd_wlioctl.h:1083`

### `pmkid_clear`
| | |
|---|---|
| Used by | whd, no "bsscfg:" prefix `whd/src/whd_wifi_api.c:1270-1271`. Not found in embassy, linux or c-driver |
| Direction | whd: set `whd/src/whd_wifi_api.c:1272` |
| Value | whd: no value, 0 data bytes `whd/src/whd_wifi_api.c:1270-1271` |
| Record | none |

- whd — set — empty — `whd_wifi_pmkid_clear` — `whd/src/whd_wifi_api.c:1265-1275` `whd/src/include/whd_wlioctl.h:1250`

### `pmkid_info`
| | |
|---|---|
| Used by | linux `linux/brcmfmac/cfg80211.c:4408` `linux/brcmfmac/cfg80211.c:4427`, whd `whd/src/whd_wifi_api.c:1203-1205`; neither uses a "bsscfg:" prefix. Not found in embassy or c-driver |
| Direction | linux: set `linux/brcmfmac/cfg80211.c:4408` `linux/brcmfmac/cfg80211.c:4427`. whd: both, get `whd/src/whd_wifi_api.c:1208`, set `whd/src/whd_wifi_api.c:1262` |
| Value | linux: `struct brcmf_pmk_op_v3_le`, 1800 bytes, or `struct brcmf_pmk_list_le`, 356 bytes; little-endian `linux/brcmfmac/fwil_types.h:974-980` `linux/brcmfmac/fwil_types.h:949-952`. whd: `pmkid_list_t`, 4 + 22 × n bytes; count little-endian `whd/inc/whd_types.h:1152-1162` `whd/src/whd_wifi_api.c:1244` |
| Record | linux v3: `struct brcmf_pmk_op_v3_le` `linux/brcmfmac/fwil_types.h:974-980` with entries `struct brcmf_pmksa_v3` `linux/brcmfmac/fwil_types.h:931-941`. linux legacy: `struct brcmf_pmk_list_le` `linux/brcmfmac/fwil_types.h:949-952` with entries `struct brcmf_pmksa` `linux/brcmfmac/fwil_types.h:893-896`. whd: `pmkid_list_t` with entries `pmkid_t` `whd/inc/whd_types.h:1152-1162` |

- linux — v3 record layout: u16 `version` at 0, u16 `length` at 2, u16 `count` at 4, u16 `pad` at 6, 16 entries from 8. Entry, 112 bytes: `bssid[6]` at 0, `pmkid[16]` at 6, u8 `pmkid_len` at 22, `pmk[48]` at 23, u8 `pmk_len` at 71, u16 `fils_cache_id` at 72, u8 `pad` at 74, `ssid` (u8 length, 32 bytes) at 75, u32 `time_left` at 108 (offsets computed from the field list with natural alignment; the structs are not packed; `ETH_ALEN` = 6 recalled, not in these sources) — `linux/brcmfmac/fwil_types.h:931-941` `linux/brcmfmac/fwil_types.h:974-980` `linux/brcmfmac/fwil_types.h:363-366` `linux/brcmfmac/fwil_types.h:156` `linux-headers/ieee80211.h:227` `linux-headers/ieee80211.h:2271` `linux-headers/ieee80211.h:2274`
- linux — set, v3 — `version` = `BRCMF_PMKSA_VER_3` (3); for one entry `count` = 1, entry 0 holds the BSSID, PMKID, `pmkid_len` = 16 and optional SSID, `time_left` = `BRCMF_PMKSA_NO_EXPIRY` (0xffffffff) to add or 0 to delete; for a flush `count` = 0; everything else zero — `brcmf_pmksa_v3_op`: add, delete or flush — `linux/brcmfmac/cfg80211.c:4372-4408` `linux/brcmfmac/fwil_types.h:178-179`
- linux — set, v3 — the `length` field is 8 for a flush and 8 + 112 for one entry, but the whole 16-entry record is sent — `linux/brcmfmac/cfg80211.c:4377` `linux/brcmfmac/cfg80211.c:4392` `linux/brcmfmac/cfg80211.c:4406-4408`
- linux — set, legacy — u32 `npmk` at 0, then 16 entries of `bssid[6]` + `pmkid[16]` from 4; always the full 16-entry record, with `npmk` saying how many are valid — `brcmf_update_pmklist`: pushes the host's whole cached list after each add, delete or flush — `linux/brcmfmac/cfg80211.c:4413-4428` `linux/brcmfmac/cfg80211.c:4470` `linux/brcmfmac/cfg80211.c:4516` `linux/brcmfmac/cfg80211.c:4539-4540`
- linux — the v3 record is used when feature `BRCMF_FEAT_PMKID_V3` is enabled, otherwise the legacy list; the v2 list struct is defined but not sent ("TODO" in source) — `linux/brcmfmac/cfg80211.c:4449-4452` `linux/brcmfmac/cfg80211.c:4493-4496` `linux/brcmfmac/cfg80211.c:4534-4537` `linux/brcmfmac/fwil_types.h:961-965` `linux/brcmfmac/feature.c:140-141`
- whd — record layout: u32 `npmkid` at 0, then entries of `BSSID` (6 bytes) + `PMKID[16]`, 22 bytes each, from 4; macro `IOVAR_STR_PMKID_INFO` — `whd/inc/whd_types.h:1152-1162` `whd/inc/whd_types.h:551-554` `whd/inc/whd_types.h:93` `whd/src/include/whd_wlioctl.h:1249`
- whd — get — request buffer 4 + 16 × 22 = 356 bytes; the first word is masked with 0x0000FFFF without having been set first; reply is the current list, `npmkid` converted with `dtoh32` — `whd_wifi_set_pmksa`: reads the list to look for the BSSID — `whd/src/whd_wifi_api.c:1203-1221` `whd/src/include/whd_wlioctl.h:851` `whd/src/whd_cdc_bdc.c:349-373`
- whd — set — the list read back with the new entry appended, 4 + 22 × (n + 1) bytes, `npmkid` = n + 1 masked to 16 bits then `htod32` — BSSID not yet in the list — `whd/src/whd_wifi_api.c:1231-1245` `whd/src/whd_wifi_api.c:1262`
- whd — set — the list read back with the matching entry replaced, 4 + 22 × n bytes, `npmkid` = n — BSSID already in the list — `whd/src/whd_wifi_api.c:1246-1262`
- whd — refuses with `WHD_WLAN_NORESOURCE` when the search index reaches `MAXPMKID` (16) — `whd/src/whd_wifi_api.c:1223-1228`
- whd — a source comment on the 16-bit mask of `npmkid` says the mask tells the h1combo that the v1 pmkid_list_t is the one being used — `whd/src/whd_wifi_api.c:1207` `whd/src/whd_wifi_api.c:1240` `whd/src/whd_wifi_api.c:1256`

Differences: three wire layouts under one name. linux v3 sends a fixed 1800-byte versioned record that carries one operation `linux/brcmfmac/cfg80211.c:4408`. linux legacy sends a fixed 356-byte list of 16 entries `linux/brcmfmac/cfg80211.c:4427-4428`. whd sends a list sized to the entry count, 4 + 22 × n bytes, with the same count-then-entries layout as the linux legacy list `whd/src/whd_wifi_api.c:1233-1237` `whd/src/whd_wifi_api.c:1249-1253`. whd gets the variable before each set `whd/src/whd_wifi_api.c:1203-1208`; linux never gets this variable and keeps the list on the host `linux/brcmfmac/cfg80211.c:4420-4421`.

### `pspretend_retry_limit`
| | |
|---|---|
| Used by | whd: defined, not used by whd `whd/src/include/whd_wlioctl.h:1149`. Not found in embassy, linux or c-driver |
| Direction | not shown by any driver |
| Value | payload not shown by any driver |
| Record | not shown by any driver |

- whd — defined as `IOVAR_STR_PSPRETEND_RETRY_LIMIT`, no call site in whd — `whd/src/include/whd_wlioctl.h:1149` `whd/src/include_helium/whd_wlioctl.h:1150`

### `pspretend_threshold`
| | |
|---|---|
| Used by | whd: defined, not used by whd `whd/src/include/whd_wlioctl.h:1150`. Not found in embassy, linux or c-driver |
| Direction | not shown by any driver |
| Value | payload not shown by any driver |
| Record | not shown by any driver |

- whd — defined as `IOVAR_STR_PSPRETEND_THRESHOLD`, no call site in whd — `whd/src/include/whd_wlioctl.h:1150` `whd/src/include_helium/whd_wlioctl.h:1151`

### `qtxpower`
| | |
|---|---|
| Used by | linux, no "bsscfg:" prefix `linux/brcmfmac/cfg80211.c:2733` `linux/brcmfmac/cfg80211.c:2756`. whd: defined, not used by whd `whd/src/include/whd_wlioctl.h:1079`. Not found in embassy or c-driver |
| Direction | linux: both; set `linux/brcmfmac/cfg80211.c:2733`, get `linux/brcmfmac/cfg80211.c:2756` |
| Value | linux: u32, 4 bytes, little-endian `linux/brcmfmac/fwil.h:122-138` |
| Record | plain integer; linux treats bits 0-30 as power in quarter-dBm and bit 31 as `WL_TXPWR_OVERRIDE` `linux/brcmfmac/cfg80211.c:2717-2720` `linux/brcmfmac/cfg80211.c:2761` `linux/include/defs.h:58` |

- linux — set — for `NL80211_TX_POWER_LIMITED` and `NL80211_TX_POWER_FIXED`: the requested power converted to quarter-dBm, capped at 127, with bit 31 set; for `NL80211_TX_POWER_AUTOMATIC`: 127 with bit 31 clear — `brcmf_cfg80211_set_tx_power`, sent after command `BRCMF_C_SET_RADIO` — `linux/brcmfmac/cfg80211.c:2701-2735`
- linux — get — one u32; linux clears bit 31 and divides by 4 to report dBm — `brcmf_cfg80211_get_tx_power` — `linux/brcmfmac/cfg80211.c:2742-2761`
- whd — defined as `IOVAR_STR_QTXPOWER`, no call site in whd — `whd/src/include/whd_wlioctl.h:1079` `whd/src/include_helium/whd_wlioctl.h:1080`

### `rand`
| | |
|---|---|
| Used by | whd: defined, not used by whd `whd/src/include/whd_wlioctl.h:1136`. Not found in embassy, linux or c-driver |
| Direction | not shown by any driver |
| Value | payload not shown by any driver |
| Record | not shown by any driver |

- whd — defined as `IOVAR_STR_RAND`, no call site in whd — `whd/src/include/whd_wlioctl.h:1136` `whd/src/include_helium/whd_wlioctl.h:1137`

### `reset_cnts`
| | |
|---|---|
| Used by | whd: defined, not used by whd `whd/src/include/whd_wlioctl.h:1152`. Not found in embassy, linux or c-driver |
| Direction | not shown by any driver |
| Value | payload not shown by any driver |
| Record | not shown by any driver |

- whd — defined as `IOVAR_STR_RESET_CNTS`, no call site in whd — `whd/src/include/whd_wlioctl.h:1152` `whd/src/include_helium/whd_wlioctl.h:1153`

### `rm_rep`
| | |
|---|---|
| Used by | whd: defined, not used by whd `whd/src/include/whd_wlioctl.h:1148`. Not found in embassy, linux or c-driver |
| Direction | not shown by any driver |
| Value | payload not shown by any driver |
| Record | not shown by any driver |

- whd — defined as `IOVAR_STR_RM_REP`, no call site in whd — `whd/src/include/whd_wlioctl.h:1148` `whd/src/include_helium/whd_wlioctl.h:1149`

### `rm_req`
| | |
|---|---|
| Used by | whd: defined, not used by whd `whd/src/include/whd_wlioctl.h:1147`. Not found in embassy, linux or c-driver |
| Direction | not shown by any driver |
| Value | payload not shown by any driver |
| Record | not shown by any driver |

- whd — defined as `IOVAR_STR_RM_REQ`, no call site in whd — `whd/src/include/whd_wlioctl.h:1147` `whd/src/include_helium/whd_wlioctl.h:1148`

### `rmc_ackreq`
| | |
|---|---|
| Used by | whd: defined, not used by whd `whd/src/include/whd_wlioctl.h:1131`. Not found in embassy, linux or c-driver |
| Direction | not shown by any driver |
| Value | payload not shown by any driver |
| Record | not shown by any driver |

- whd — defined as `IOVAR_STR_RMC_ACKREQ`, no call site in whd — `whd/src/include/whd_wlioctl.h:1131` `whd/src/include_helium/whd_wlioctl.h:1132`

### `rmc_role`
| | |
|---|---|
| Used by | whd: defined, not used by whd `whd/src/include/whd_wlioctl.h:1134`. Not found in embassy, linux or c-driver |
| Direction | not shown by any driver |
| Value | payload not shown by any driver |
| Record | not shown by any driver |

- whd — defined as `IOVAR_STR_RMC_ROLE`, no call site in whd — `whd/src/include/whd_wlioctl.h:1134` `whd/src/include_helium/whd_wlioctl.h:1135`

### `rmc_stats`
| | |
|---|---|
| Used by | whd: defined, not used by whd `whd/src/include/whd_wlioctl.h:1133`. Not found in embassy, linux or c-driver |
| Direction | not shown by any driver |
| Value | payload not shown by any driver |
| Record | not shown by any driver |

- whd — defined as `IOVAR_STR_RMC_COUNTS` (the macro name says "counts", the string is "rmc_stats"), no call site in whd — `whd/src/include/whd_wlioctl.h:1133` `whd/src/include_helium/whd_wlioctl.h:1134`

### `rmc_status`
| | |
|---|---|
| Used by | whd: defined as `IOVAR_STR_RMC_STATUS`, no call site in whd `whd/src/include/whd_wlioctl.h:1132`. Not found in embassy, linux or c-driver |
| Direction | none; whd only defines the name `whd/src/include/whd_wlioctl.h:1132` |
| Value | payload not shown by any driver; whd only defines the name `whd/src/include/whd_wlioctl.h:1132` |
| Record | none shown by any driver; whd only defines the name `whd/src/include/whd_wlioctl.h:1132` |

### `roam_off`
| | |
|---|---|
| Used by | linux, whd, c-driver; none with the "bsscfg:" prefix. Not found in embassy. `linux/brcmfmac/cfg80211.c:7131` `whd/src/whd_wifi_api.c:1786` `c-driver/cyw43_ctrl.c:686` |
| Direction | linux: set. whd: set. c-driver: both. `linux/brcmfmac/cfg80211.c:7131` `whd/src/whd_wifi_api.c:1786` `c-driver/cyw43_ctrl.c:696` `c-driver/cyw43_ctrl.c:714` |
| Value | 32-bit integer, 4 bytes, little-endian, in all three drivers. `linux/brcmfmac/fwil.h:123-127` `whd/src/whd_wifi_api.c:5153-5162` `c-driver/cyw43_ctrl.c:692-695` |
| Record | plain integer `linux/brcmfmac/fwil.h:123-127` `whd/src/whd_wifi_api.c:5153-5162` `c-driver/cyw43_ctrl.c:692-695` |

- linux — set — `settings->roamoff` as le32 — `brcmf_dongle_roam`; the source comment says it enables or disables built-in roaming so the supplicant can take care of roaming — `linux/brcmfmac/cfg80211.c:7126-7132`
- linux — set — value 1 — on a newly created P2P interface (source comment: "Disable firmware roaming for P2P interface"); sent with the plain helper on that interface's `ifp`; return value ignored — `linux/brcmfmac/p2p.c:2369-2370`
- whd — set — value 0 — `whd_wifi_prepare_join`, before a join (source comment: "Enable Roaming in FW by default") — `whd/src/whd_wifi_api.c:1785-1786`
- whd — set — value 1 — `whd_wifi_prepare_join`, WPA3 SAE join when the driver's `fwcap_flags` lack the SAE bit; the source comment gives a limitation of the host-side WPA3 supplicant as the reason — `whd/src/whd_wifi_api.c:1867-1875`
- c-driver — set — 13-byte buffer: the name `roam_off` with its NUL (9 bytes), then 4 bytes le32; 1 = roaming disabled, 0 = enabled; sent on `CYW43_ITF_STA` — `cyw43_wifi_set_roam_enabled` — `c-driver/cyw43_ctrl.c:683-696`
- c-driver — get — request is the name with its NUL (9 bytes) followed by 4 zero bytes (13 bytes); the driver reads a le32 from offset 0 of the returned buffer; nonzero is treated as roaming disabled — `cyw43_wifi_get_roam_enabled` — `c-driver/cyw43_ctrl.c:699-721`
- c-driver — both calls go through the public `cyw43_ioctl` with `CYW43_IOCTL_SET_VAR` (0x20f = 527) and `CYW43_IOCTL_GET_VAR` (0x20c = 524); these are c-driver's doubled public values, command number × 2 plus 1 for a set: 263 × 2 + 1 = 527 and 262 × 2 = 524 (computed) — `c-driver/cyw43_ll.h:46-47`
- c-driver — `cyw43_ll_ioctl` splits the public value: bit 0 selects set or get, the rest shifted right by 1 is the command, giving set 263 and get 262 — `c-driver/cyw43_ll.c:1327-1329`

### `roam_time_thresh`
| | |
|---|---|
| Used by | whd, no "bsscfg:" prefix (`IOVAR_STR_ROAM_TIME_THRESH`). Not found in embassy, linux or c-driver. `whd/src/include/whd_wlioctl.h:1265` |
| Direction | both `whd/src/whd_wifi_api.c:1286` `whd/src/whd_wifi_api.c:1293` |
| Value | uint32_t, 4 bytes, little-endian (htod32 on set, dtoh32 on get) `whd/src/whd_wifi_api.c:5153-5162` `whd/src/whd_wifi_api.c:5165-5179` |
| Record | plain integer `whd/src/whd_wifi_api.c:5153-5162` `whd/src/whd_wifi_api.c:5165-5179` |

- whd — set — caller's `roam_time_threshold`; the host rejects 0 with `WHD_WLAN_BADARG` before sending — `whd_wifi_set_roam_time_threshold` — `whd/src/whd_wifi_api.c:1277-1286`
- whd — get — 4-byte request buffer after the name; reads one uint32_t from the reply into the caller's pointer — `whd_wifi_get_roam_time_threshold` — `whd/src/whd_wifi_api.c:1289-1293` `whd/src/whd_wifi_api.c:5175-5179`
- whd — units are not stated at these call sites — `whd/src/whd_wifi_api.c:1277-1293`

### `rrm`
| | |
|---|---|
| Used by | whd: defined as `IOVAR_STR_RRM`, no call site in whd `whd/src/include/whd_wlioctl.h:1195`. Not found in embassy, linux or c-driver |
| Direction | none; whd only defines the name `whd/src/include/whd_wlioctl.h:1195` |
| Value | payload not shown by any driver; whd only defines the name `whd/src/include/whd_wlioctl.h:1195` |
| Record | none shown by any driver; whd only defines the name `whd/src/include/whd_wlioctl.h:1195` |

### `rrm_bcn_req`
| | |
|---|---|
| Used by | whd: defined as `IOVAR_STR_RRM_BCN_REQ`, no call site in whd `whd/src/include/whd_wlioctl.h:1202`. Not found in embassy, linux or c-driver |
| Direction | none; whd only defines the name `whd/src/include/whd_wlioctl.h:1202` |
| Value | payload not shown by any driver; whd only defines the name `whd/src/include/whd_wlioctl.h:1202` |
| Record | none shown by any driver; whd only defines the name `whd/src/include/whd_wlioctl.h:1202` |

### `rrm_bcn_req_max_off_chan_time`
| | |
|---|---|
| Used by | whd: defined as `IOVAR_STR_RRM_BCNREQ_MAXOFF_TIME`, no call site in whd `whd/src/include/whd_wlioctl.h:1207`. Not found in embassy, linux or c-driver |
| Direction | none; whd only defines the name `whd/src/include/whd_wlioctl.h:1207` |
| Value | payload not shown by any driver; whd only defines the name `whd/src/include/whd_wlioctl.h:1207` |
| Record | none shown by any driver; whd only defines the name `whd/src/include/whd_wlioctl.h:1207` |

### `rrm_bcn_req_thrtl_win`
| | |
|---|---|
| Used by | whd: defined as `IOVAR_STR_RRM_BCNREQ_THRTL_WIN`, no call site in whd `whd/src/include/whd_wlioctl.h:1206`. Not found in embassy, linux or c-driver |
| Direction | none; whd only defines the name `whd/src/include/whd_wlioctl.h:1206` |
| Value | payload not shown by any driver; whd only defines the name `whd/src/include/whd_wlioctl.h:1206` |
| Record | none shown by any driver; whd only defines the name `whd/src/include/whd_wlioctl.h:1206` |

### `rrm_bcn_req_traff_meas_per`
| | |
|---|---|
| Used by | whd: defined as `IOVAR_STR_RRM_BCNREQ_TRFMS_PRD`, no call site in whd `whd/src/include/whd_wlioctl.h:1208`. Not found in embassy, linux or c-driver |
| Direction | none; whd only defines the name `whd/src/include/whd_wlioctl.h:1208` |
| Value | payload not shown by any driver; whd only defines the name `whd/src/include/whd_wlioctl.h:1208` |
| Record | none shown by any driver; whd only defines the name `whd/src/include/whd_wlioctl.h:1208` |

### `rrm_chload_req`
| | |
|---|---|
| Used by | whd: defined as `IOVAR_STR_RRM_CHLOAD_REQ`, no call site in whd `whd/src/include/whd_wlioctl.h:1201`. Not found in embassy, linux or c-driver |
| Direction | none; whd only defines the name `whd/src/include/whd_wlioctl.h:1201` |
| Value | payload not shown by any driver; whd only defines the name `whd/src/include/whd_wlioctl.h:1201` |
| Record | none shown by any driver; whd only defines the name `whd/src/include/whd_wlioctl.h:1201` |

### `rrm_frame_req`
| | |
|---|---|
| Used by | whd: defined as `IOVAR_STR_RRM_FRAME_REQ`, no call site in whd `whd/src/include/whd_wlioctl.h:1200`. Not found in embassy, linux or c-driver |
| Direction | none; whd only defines the name `whd/src/include/whd_wlioctl.h:1200` |
| Value | payload not shown by any driver; whd only defines the name `whd/src/include/whd_wlioctl.h:1200` |
| Record | none shown by any driver; whd only defines the name `whd/src/include/whd_wlioctl.h:1200` |

### `rrm_lm_req`
| | |
|---|---|
| Used by | whd: defined as `IOVAR_STR_RRM_LM_REQ`, no call site in whd `whd/src/include/whd_wlioctl.h:1198`. Not found in embassy, linux or c-driver |
| Direction | none; whd only defines the name `whd/src/include/whd_wlioctl.h:1198` |
| Value | payload not shown by any driver; whd only defines the name `whd/src/include/whd_wlioctl.h:1198` |
| Record | none shown by any driver; whd only defines the name `whd/src/include/whd_wlioctl.h:1198` |

### `rrm_nbr_add_nbr`
| | |
|---|---|
| Used by | whd: defined as `IOVAR_STR_RRM_NBR_ADD`, no call site in whd `whd/src/include/whd_wlioctl.h:1204`. Not found in embassy, linux or c-driver |
| Direction | none; whd only defines the name `whd/src/include/whd_wlioctl.h:1204` |
| Value | payload not shown by any driver; whd only defines the name `whd/src/include/whd_wlioctl.h:1204` |
| Record | none shown by any driver; whd only defines the name `whd/src/include/whd_wlioctl.h:1204` |

### `rrm_nbr_del_nbr`
| | |
|---|---|
| Used by | whd: defined as `IOVAR_STR_RRM_NBR_DEL`, no call site in whd `whd/src/include/whd_wlioctl.h:1205`. Not found in embassy, linux or c-driver |
| Direction | none; whd only defines the name `whd/src/include/whd_wlioctl.h:1205` |
| Value | payload not shown by any driver; whd only defines the name `whd/src/include/whd_wlioctl.h:1205` |
| Record | none shown by any driver; whd only defines the name `whd/src/include/whd_wlioctl.h:1205` |

### `rrm_nbr_list`
| | |
|---|---|
| Used by | whd: defined as `IOVAR_STR_RRM_NBR_LIST`, no call site in whd `whd/src/include/whd_wlioctl.h:1203`. Not found in embassy, linux or c-driver |
| Direction | none; whd only defines the name `whd/src/include/whd_wlioctl.h:1203` |
| Value | payload not shown by any driver; whd only defines the name `whd/src/include/whd_wlioctl.h:1203` |
| Record | none shown by any driver; whd only defines the name `whd/src/include/whd_wlioctl.h:1203` |

### `rrm_nbr_req`
| | |
|---|---|
| Used by | whd: defined as `IOVAR_STR_RRM_NBR_REQ`, no call site in whd `whd/src/include/whd_wlioctl.h:1197`. Not found in embassy, linux or c-driver |
| Direction | none; whd only defines the name `whd/src/include/whd_wlioctl.h:1197` |
| Value | payload not shown by any driver; whd only defines the name `whd/src/include/whd_wlioctl.h:1197` |
| Record | none shown by any driver; whd only defines the name `whd/src/include/whd_wlioctl.h:1197` |

### `rrm_noise_req`
| | |
|---|---|
| Used by | whd: defined as `IOVAR_STR_RRM_NOISE_REQ`, no call site in whd `whd/src/include/whd_wlioctl.h:1196`. Not found in embassy, linux or c-driver |
| Direction | none; whd only defines the name `whd/src/include/whd_wlioctl.h:1196` |
| Value | payload not shown by any driver; whd only defines the name `whd/src/include/whd_wlioctl.h:1196` |
| Record | none shown by any driver; whd only defines the name `whd/src/include/whd_wlioctl.h:1196` |

### `rrm_stat_req`
| | |
|---|---|
| Used by | whd: defined as `IOVAR_STR_RRM_STAT_REQ`, no call site in whd `whd/src/include/whd_wlioctl.h:1199`. Not found in embassy, linux or c-driver |
| Direction | none; whd only defines the name `whd/src/include/whd_wlioctl.h:1199` |
| Value | payload not shown by any driver; whd only defines the name `whd/src/include/whd_wlioctl.h:1199` |
| Record | none shown by any driver; whd only defines the name `whd/src/include/whd_wlioctl.h:1199` |

### `rsdb_mode`
| | |
|---|---|
| Used by | linux, no "bsscfg:" prefix. Not found in embassy, whd or c-driver. `linux/brcmfmac/feature.c:332` |
| Direction | get `linux/brcmfmac/feature.c:196` |
| Value | u32, 4 bytes, read as little-endian; linux discards the value `linux/brcmfmac/fwil.h:129-138` `linux/brcmfmac/feature.c:190-199` |
| Record | plain integer `linux/brcmfmac/fwil.h:129-138` `linux/brcmfmac/feature.c:190-199` |

- linux — get — 4-byte request taken from an uninitialised local `u32 data`; only the error code is used — feature probe: `BRCMF_FEAT_RSDB` is set unless the result is `-BRCMF_FW_UNSUPPORTED` — `linux/brcmfmac/feature.c:187-199` `linux/brcmfmac/feature.c:332`
- linux — sets `ifp->fwil_fwerr = true` for this probe; source comment: "we need to know firmware error" — `linux/brcmfmac/feature.c:193-194`

### `rssi_event`
| | |
|---|---|
| Used by | linux, no "bsscfg:" prefix. Not found in embassy, whd or c-driver. `linux/brcmfmac/cfg80211.c:5811` |
| Direction | set `linux/brcmfmac/cfg80211.c:5811` |
| Value | `struct brcmf_rssi_event_le`, sent as `sizeof(config)`: 13 bytes of fields (computed); the struct is not packed, so `sizeof` is 16 with 3 bytes of tail padding (compiled, equivalent struct on an x86-64 host; not compiled for a 32-bit ARM target); `rate_limit_msec` little-endian `linux/brcmfmac/fwil_types.h:869-873` `linux/brcmfmac/cfg80211.c:5811-5812` |
| Record | `struct brcmf_rssi_event_le`: offset 0 `__le32 rate_limit_msec`; offset 4 `s8 rssi_level_num`; offset 5 `s8 rssi_levels[8]` (`BRCMF_MAX_RSSI_LEVELS` = 8) `linux/brcmfmac/fwil_types.h:860-873` |

- linux — set — `rate_limit_msec` = 0, `rssi_level_num` = 3, `rssi_levels` = { clamp(rssi_low, S8_MIN, S8_MAX-2), clamp(rssi_high, S8_MIN+1, S8_MAX-1), S8_MAX }, remaining levels zero from the initialiser — `brcmf_cfg80211_set_cqm_rssi_range_config`: RSSI threshold levels; the source comment says the third level is set so that the transition from rssi <= `rssi_high` to rssi > `rssi_high` is also detected — `linux/brcmfmac/cfg80211.c:5795-5812`
- linux — the header comment says the levels are given in ascending order — `linux/brcmfmac/fwil_types.h:867`

### `rtsthresh`
| | |
|---|---|
| Used by | linux, no "bsscfg:" prefix. Not found in embassy, whd or c-driver. `linux/brcmfmac/cfg80211.c:1605` |
| Direction | set `linux/brcmfmac/cfg80211.c:1605` |
| Value | u32, 4 bytes, little-endian `linux/brcmfmac/fwil.h:123-127` |
| Record | plain integer `linux/brcmfmac/fwil.h:123-127` |

- linux — set — caller's `rts_threshold` — `brcmf_set_rts`: RTS threshold — `linux/brcmfmac/cfg80211.c:1605`

### `rxchain`
| | |
|---|---|
| Used by | linux, no "bsscfg:" prefix. Not found in embassy, whd or c-driver. `linux/brcmfmac/cfg80211.c:7567` |
| Direction | get `linux/brcmfmac/cfg80211.c:7567` |
| Value | u32, 4 bytes, read as little-endian `linux/brcmfmac/fwil.h:129-138` |
| Record | plain integer `linux/brcmfmac/fwil.h:129-138` |

- linux — get — one u32; linux counts the set bits to get the number of receive chains — `brcmf_setup_wiphybands`; on any error linux assumes 1 chain, and `-EBADE` is logged as "rxchain unsupported" — `linux/brcmfmac/cfg80211.c:7567-7579`

### `sae_max_pwe_loop`
| | |
|---|---|
| Used by | whd, c-driver; neither with the "bsscfg:" prefix. Not found in embassy or linux. `whd/src/include/whd_wlioctl.h:1248` `c-driver/cyw43_ll.c:2439` |
| Direction | set in both `whd/src/whd_ap.c:510-513` `c-driver/cyw43_ll.c:2439` |
| Value | 32-bit integer, 4 bytes, little-endian in both `whd/src/whd_ap.c:510-512` `c-driver/cyw43_ll.c:1538-1543` |
| Record | plain integer `whd/src/whd_ap.c:510-512` `c-driver/cyw43_ll.c:1538-1543` |

- whd — set — value `PWE_LOOP_COUNT` = 5 — `whd_wifi_init_ap` when the auth type has the WPA3 bit: adjust the SAE PWE loop count; a failed set only logs a debug line and is ignored — `whd/src/whd_ap.c:49` `whd/src/whd_ap.c:507-516`
- c-driver — set — the call is `cyw43_write_iovar_u32(self, "sae_max_pwe_loop", WWD_AP_INTERFACE, 5)` and the helper's parameters are `(var, val, iface)`, so as written the value sent is `WWD_AP_INTERFACE` = 1 and the interface argument is 5 — AP start for `CYW43_AUTH_WPA3_SAE_AES_PSK` or `CYW43_AUTH_WPA3_WPA2_AES_PSK` — `c-driver/cyw43_ll.c:2438-2439` `c-driver/cyw43_ll.c:1538` `c-driver/cyw43_ll.c:152`
- c-driver — places the interface argument in the CDC flags as `iface << CDCF_IOC_IF_SHIFT` (shift 12) — `c-driver/cyw43_ll.c:162` `c-driver/cyw43_ll.c:900`

Differences: whd sends value 5 on the AP interface passed in. `whd/src/whd_ap.c:49` `whd/src/whd_ap.c:510-513` c-driver as written sends value 1 with interface number 5. `c-driver/cyw43_ll.c:2439` `c-driver/cyw43_ll.c:1538` The c-driver arguments look swapped relative to the helper's parameter order (inferred); the source does not say so. `c-driver/cyw43_ll.c:2439` `c-driver/cyw43_ll.c:1538`

### `sae_password`
| | |
|---|---|
| Used by | embassy, linux, whd, c-driver; none with the "bsscfg:" prefix `embassy/control.rs:429` `linux/brcmfmac/cyw/core.c:43` `whd/src/whd_wifi_api.c:791-800` `c-driver/cyw43_ll.c:2266` |
| Direction | set in all four `embassy/control.rs:429` `linux/brcmfmac/cyw/core.c:43` `whd/src/whd_wifi_api.c:800` `c-driver/cyw43_ll.c:2266` |
| Value | 130 bytes in all four: 16-bit length at offset 0, then 128 bytes of password at offset 2. linux, whd and c-driver write the length little-endian (cpu_to_le16, htod16, `cyw43_put_le16`); embassy sends the `#[repr(C)]` struct's memory as is, so `len` is in the build target's byte order, little-endian on the Pico W (inferred). `linux/brcmfmac/cyw/core.c:40` `whd/src/whd_wifi_api.c:797` `c-driver/cyw43_ll.c:2263` `embassy/structs.rs:12-14` `embassy/structs.rs:418` embassy `SaePassphraseInfo`; linux `struct brcmf_wsec_sae_pwd_le`; whd `wsec_sae_password_t`; c-driver hand-built buffer of `2 + CYW43_WPA_SAE_MAX_PASSWORD_LEN`. `embassy/structs.rs:419-422` `linux/brcmfmac/fwil_types.h:596-599` `whd/src/include/whd_wlioctl.h:793-798` `c-driver/cyw43_ll.c:2262-2266` `c-driver/cyw43_ll.c:278` |
| Record | embassy `SaePassphraseInfo { len: u16, passphrase: [u8; 128] }` `embassy/structs.rs:419-422`; linux `struct brcmf_wsec_sae_pwd_le { __le16 key_len; u8 key[128]; }` `linux/brcmfmac/fwil_types.h:596-599` `linux/brcmfmac/fwil_types.h:68`; whd `wsec_sae_password_t { uint16_t password_len; uint8_t password[128]; }` `whd/src/include/whd_wlioctl.h:793-798`; c-driver no named record `c-driver/cyw43_ll.c:2262-2264` |

- embassy — set — `len` = passphrase length, `passphrase` zero-padded to 128 — station join inside the `if wpa3` branch; a 3 ms wait precedes the write — `embassy/control.rs:422-429`
- embassy — set — same record — access point SAE password, `set_ap_sae_passphrase`, called for `ApAuth::Wpa3` and `ApAuth::Wpa2Wpa3` — `embassy/control.rs:629-636` `embassy/control.rs:603-605`
- embassy — sends name + NUL + value with `Ioctl::SetVar` (263), `IoctlType::Set`, interface 0 — `embassy/control.rs:713-728` `embassy/consts.rs:684`
- linux — set — `key_len` = cpu_to_le16(password length), first `pwd_len` bytes of `key` copied; the struct is a stack variable with no initialiser, so the bytes of `key` past `pwd_len` are not written by linux before all 130 bytes are sent; lengths above 128 are rejected by the host — `brcmf_cyw_set_sae_pwd` in the CYW vendor module, installed as its `.set_sae_password` op — `linux/brcmfmac/cyw/core.c:26-44` `linux/brcmfmac/cyw/core.c:379`
- linux — the WCC vendor module does not send this variable: its SAE password function calls `brcmf_set_wsec` with `BRCMF_WSEC_PASSPHRASE` — `linux/brcmfmac/wcc/core.c:16-21`
- whd — set — record zeroed, password copied, `password_len` = htod16(key_length); host rejects key_length 0 or above 128; a 1 ms delay precedes the send — `whd_wifi_sae_password` — `whd/src/whd_wifi_api.c:775-800`
- whd — set — station join: called for a WPA3 SAE join only when the driver's `fwcap_flags` include the SAE bit — `whd/src/whd_wifi_api.c:1867-1869`
- whd — set — AP start, `WHD_SECURITY_WPA3_SAE` with the SAE capability flag; return value ignored — `whd/src/whd_ap.c:471-473`
- whd — set — AP start, `WHD_SECURITY_WPA3_WPA2_PSK` with the SAE capability flag; return value ignored — `whd/src/whd_ap.c:477-480`
- c-driver — set — buffer zeroed for 130 bytes, le16 `key_len` at 0, key copied at 2; sent on `WWD_STA_INTERFACE`; a 2 ms delay precedes the send — station join when `wpa_auth == CYW43_WPA3_AUTH_SAE_PSK` — `c-driver/cyw43_ll.c:2261-2266`
- c-driver — set — le16 `key_len` at 0, 128 bytes zeroed at 2, key copied at 2; sent on `WWD_AP_INTERFACE`; a 2 ms delay precedes the send — AP start when the auth value has `CYW43_WPA3_AUTH_SAE_PSK` — `c-driver/cyw43_ll.c:2421-2426`
- c-driver — sends it with `cyw43_write_iovar_n`: name + NUL, then the value bytes, `WLC_SET_VAR` — `c-driver/cyw43_ll.c:1556-1562`

Differences: size and layout are the same in all four (130 bytes, 16-bit length then 128 bytes). `embassy/structs.rs:419-422` `linux/brcmfmac/fwil_types.h:596-599` `whd/src/include/whd_wlioctl.h:793-798` `c-driver/cyw43_ll.c:2262-2266` Padding differs: embassy, whd and c-driver zero the unused password bytes `embassy/control.rs:425` `whd/src/whd_wifi_api.c:795` `c-driver/cyw43_ll.c:2262`; linux does not initialise them `linux/brcmfmac/cyw/core.c:30` `linux/brcmfmac/cyw/core.c:40-41`. Delay before the send differs: embassy 3 ms (station path only) `embassy/control.rs:428`, c-driver 2 ms `c-driver/cyw43_ll.c:2265`, whd 1 ms `whd/src/whd_wifi_api.c:799`, linux none at the call site `linux/brcmfmac/cyw/core.c:40-43`.

### `sae_pwe_h2e_enable`
| | |
|---|---|
| Used by | whd, no "bsscfg:" prefix (macro is `IOV_SAE_PWE_H2E_ENABLE`, not `IOVAR_STR_*`). Not found in embassy, linux or c-driver. `whd/src/include/whd_wlioctl.h:1291` |
| Direction | set `whd/src/whd_wifi_api.c:5462` |
| Value | uint32_t, 4 bytes, little-endian (htod32) `whd/src/whd_wifi_api.c:5153-5162` |
| Record | plain integer `whd/src/whd_wifi_api.c:5153-5162` |

- whd — set — the `bool h2ecap` argument widened to uint32_t (0 or 1) — `whd_wifi_set_auth_h2e_cap`: turn SAE hash-to-element on or off — `whd/src/whd_wifi_api.c:5457-5462`

### `sae_transition_mode`
| | |
|---|---|
| Used by | whd, no "bsscfg:" prefix (macro is spelled `IOVAR_STR_SAE_TRANSITON_MODE`). Not found in embassy, linux or c-driver. `whd/src/include/whd_wlioctl.h:1290` |
| Direction | set `whd/src/whd_wifi_api.c:2055` |
| Value | uint32_t, 4 bytes, little-endian (htod32) `whd/src/whd_wifi_api.c:5153-5162` |
| Record | plain integer `whd/src/whd_wifi_api.c:5153-5162` |

- whd — set — value 0 — `whd_wifi_prepare_join` when `*wpa_auth == WPA2_AUTH_PSK` — `whd/src/whd_wifi_api.c:2053-2055`
- whd — set — value 1 — `whd_wifi_prepare_join` for every other `wpa_auth` — `whd/src/whd_wifi_api.c:2057-2059`
- whd — both sets are compiled only under `CYW89530_AUTO` — `whd/src/whd_wifi_api.c:2052-2061`

### `scan_assoc_time`
| | |
|---|---|
| Used by | whd: defined as `IOVAR_STR_SCAN_ASSOC_TIME`, no call site in whd `whd/src/include/whd_wlioctl.h:1156`. Not found in embassy, linux or c-driver |
| Direction | none; whd only defines the name `whd/src/include/whd_wlioctl.h:1156` |
| Value | payload not shown by any driver; whd only defines the name `whd/src/include/whd_wlioctl.h:1156` |
| Record | none shown by any driver; whd only defines the name `whd/src/include/whd_wlioctl.h:1156` |

### `scan_home_time`
| | |
|---|---|
| Used by | whd: defined as `IOVAR_STR_SCAN_HOME_TIME`, no call site in whd `whd/src/include/whd_wlioctl.h:1159`. Not found in embassy, linux or c-driver |
| Direction | none; whd only defines the name `whd/src/include/whd_wlioctl.h:1159` |
| Value | payload not shown by any driver; whd only defines the name `whd/src/include/whd_wlioctl.h:1159` |
| Record | none shown by any driver; whd only defines the name `whd/src/include/whd_wlioctl.h:1159` |

### `scan_nprobes`
| | |
|---|---|
| Used by | whd: defined as `IOVAR_STR_SCAN_NPROBES`, no call site in whd `whd/src/include/whd_wlioctl.h:1160`. Not found in embassy, linux or c-driver |
| Direction | none; whd only defines the name `whd/src/include/whd_wlioctl.h:1160` |
| Value | payload not shown by any driver; whd only defines the name `whd/src/include/whd_wlioctl.h:1160` |
| Record | none shown by any driver; whd only defines the name `whd/src/include/whd_wlioctl.h:1160` |

### `scan_passive_time`
| | |
|---|---|
| Used by | whd: defined as `IOVAR_STR_SCAN_PASSIVE_TIME`, no call site in whd `whd/src/include/whd_wlioctl.h:1158`. Not found in embassy, linux or c-driver |
| Direction | none; whd only defines the name `whd/src/include/whd_wlioctl.h:1158` |
| Value | payload not shown by any driver; whd only defines the name `whd/src/include/whd_wlioctl.h:1158` |
| Record | none shown by any driver; whd only defines the name `whd/src/include/whd_wlioctl.h:1158` |

### `scan_unassoc_time`
| | |
|---|---|
| Used by | whd: defined as `IOVAR_STR_SCAN_UNASSOC_TIME`, no call site in whd `whd/src/include/whd_wlioctl.h:1157`. Not found in embassy, linux or c-driver |
| Direction | none; whd only defines the name `whd/src/include/whd_wlioctl.h:1157` |
| Value | payload not shown by any driver; whd only defines the name `whd/src/include/whd_wlioctl.h:1157` |
| Record | none shown by any driver; whd only defines the name `whd/src/include/whd_wlioctl.h:1157` |

### `scan_ver`
| | |
|---|---|
| Used by | linux, no "bsscfg:" prefix. Not found in embassy, whd or c-driver. `linux/brcmfmac/feature.c:344` |
| Direction | get `linux/brcmfmac/feature.c:196` |
| Value | u32, 4 bytes, read as little-endian; linux discards the value `linux/brcmfmac/fwil.h:129-138` `linux/brcmfmac/feature.c:190-199` |
| Record | plain integer `linux/brcmfmac/fwil.h:129-138` `linux/brcmfmac/feature.c:190-199` |

- linux — get — 4-byte request taken from an uninitialised local `u32 data`; only the error code is used — feature probe: `BRCMF_FEAT_SCAN_V2` is set unless the result is `-BRCMF_FW_UNSUPPORTED` — `linux/brcmfmac/feature.c:187-199` `linux/brcmfmac/feature.c:344`

### `scancache_clear`
| | |
|---|---|
| Used by | whd: defined as `IOVAR_STR_SCAN_CACHE_CLEAR`, no call site in whd `whd/src/include/whd_wlioctl.h:1192`. Not found in embassy, linux or c-driver |
| Direction | none; whd only defines the name `whd/src/include/whd_wlioctl.h:1192` |
| Value | payload not shown by any driver; whd only defines the name `whd/src/include/whd_wlioctl.h:1192` |
| Record | none shown by any driver; whd only defines the name `whd/src/include/whd_wlioctl.h:1192` |

### `scanmac`
| | |
|---|---|
| Used by | whd, no "bsscfg:" prefix (`IOVAR_STR_SCANMAC`). Not found in embassy, linux or c-driver. `whd/src/include/whd_wlioctl.h:1281` |
| Direction | set `whd/src/whd_wifi_api.c:6902` |
| Value | 8 bytes: `wl_scanmac_t` header (4 bytes) followed by `wl_scanmac_enable_t` (4 bytes); the two 16-bit header fields little-endian (htod16) `whd/src/whd_wifi_api.c:6888-6902` |
| Record | `wl_scanmac_t`: offset 0 `uint16_t subcmd_id`; offset 2 `uint16_t len` (length of `data[]`); offset 4 `data[]`. `wl_scanmac_enable_t`: offset 0 `uint8_t enable` (1 enable, 0 disable); offset 1 `uint8_t pad[3]`. `whd/src/include/whd_wlioctl.h:4620-4624` `whd/src/include/whd_wlioctl.h:4632-4635` |

- whd — set — `subcmd_id` = `WL_SCANMAC_SUBCMD_ENABLE` (0), `len` = 4, `enable` = the `config` argument; `pad[3]` is not written (the buffer is an uninitialised stack array) — `whd_configure_scanmac_randomisation`: turn scan MAC address randomisation on or off — `whd/src/whd_wifi_api.c:6884-6902` `whd/src/include/whd_wlioctl.h:4627`
- whd — set — same helper with `WHD_FALSE` — init sequence, only when the chip id is 55500, so whd does not send it for a 43439 on this path — `whd/src/whd_management.c:602-604`
- whd — the header also defines subcommands `WL_SCANMAC_SUBCMD_BSSCFG` (1, comment: only GET supported) and `WL_SCANMAC_SUBCMD_CONFIG` (2); no whd .c file references either — `whd/src/include/whd_wlioctl.h:4628-4629`

### `sgi_rx`
| | |
|---|---|
| Used by | whd: defined as `IOVAR_STR_SGI_RX`, no call site in whd `whd/src/include/whd_wlioctl.h:1238`. Not found in embassy, linux or c-driver |
| Direction | none; whd only defines the name `whd/src/include/whd_wlioctl.h:1238` |
| Value | payload not shown by any driver; whd only defines the name `whd/src/include/whd_wlioctl.h:1238` |
| Record | none shown by any driver; whd only defines the name `whd/src/include/whd_wlioctl.h:1238` |

### `sgi_tx`
| | |
|---|---|
| Used by | whd: defined as `IOVAR_STR_SGI_TX`, no call site in whd `whd/src/include/whd_wlioctl.h:1239`. Not found in embassy, linux or c-driver |
| Direction | none; whd only defines the name `whd/src/include/whd_wlioctl.h:1239` |
| Value | payload not shown by any driver; whd only defines the name `whd/src/include/whd_wlioctl.h:1239` |
| Record | none shown by any driver; whd only defines the name `whd/src/include/whd_wlioctl.h:1239` |

### `ssid`
| | |
|---|---|
| Used by | embassy (`bsscfg:ssid`), c-driver (`bsscfg:ssid`), whd (`bsscfg:ssid`), linux (`ssid` through the bsscfg helper, and a literal `bsscfg:ssid`) `embassy/control.rs:583` `c-driver/cyw43_ll.c:2386` `whd/src/whd_ap.c:412` `linux/brcmfmac/cfg80211.c:5473` `linux/brcmfmac/cfg80211.c:800` |
| Direction | set in all four; no get found `embassy/control.rs:583` `c-driver/cyw43_ll.c:2386` `whd/src/whd_ap.c:417` `linux/brcmfmac/cfg80211.c:5473` |
| Value | embassy, c-driver, whd: 40 bytes = u32 LE bsscfg index + u32 LE SSID length + 32 SSID bytes `embassy/control.rs:575-583` `c-driver/cyw43_ll.c:2382-2386` `whd/src/whd_ap.c:412-416`. linux `ssid`: 36 bytes (le32 length + SSID[IEEE80211_MAX_SSID_LEN = 32] `linux-headers/ieee80211.h:227`), preceded by a le32 index only when the interface's bsscfgidx is not 0 `linux/brcmfmac/fwil.c:259-289`. linux literal `bsscfg:ssid`: 40 bytes `linux/brcmfmac/cfg80211.c:800-801` |
| Record | embassy `SsidInfoWithIndex` `embassy/structs.rs:428` (inner `SsidInfo` `embassy/structs.rs:400`); linux `struct brcmf_ssid_le` `linux/brcmfmac/fwil_types.h:357` and `struct brcmf_mbss_ssid_le` `linux/brcmfmac/fwil_types.h:751`; c-driver and whd build the bytes by hand, no record type `c-driver/cyw43_ll.c:2382-2385` `whd/src/whd_ap.c:414-416` |

- embassy — set the access point SSID — `bsscfg:ssid`, index 0, len = SSID length, ssid zero-padded to 32 — `embassy/control.rs:575-583`
- c-driver — set the access point SSID; sent on `WWD_STA_INTERFACE` = 0 — `bsscfg:ssid`, le32 index `WWD_AP_INTERFACE` = 1, le32 ssid_len, 32 bytes cleared then SSID copied; length passed is 4 + 4 + 32 — `c-driver/cyw43_ll.c:2382-2386`, `c-driver/cyw43_ll.c:151-152`
- whd — `whd_wifi_init_ap`, set the soft-AP SSID; sent on the primary interface — `"bsscfg:" IOVAR_STR_SSID`, 40-byte buffer, word 0 = htod32(bss_index), word 1 = htod32(ssid->length), then ssid->length SSID bytes — `whd/src/whd_ap.c:412-417`, macro `whd/src/include/whd_wlioctl.h:1137`
- whd — the bytes after the copied SSID are not written at the call site; the CDC buffer helper clears only the name-alignment pad, the msgbuf buffer helper clears the whole buffer — `whd/src/whd_ap.c:416`, `whd/src/whd_cdc_bdc.c:364`, `whd/src/whd_msgbuf_txrx.c:223`
- linux — `brcmf_cfg80211_start_ap`, set, only when the device role is P2P GO — name `ssid` via `brcmf_fil_bsscfg_data_set`, `struct brcmf_ssid_le` — `linux/brcmfmac/cfg80211.c:5458`, `linux/brcmfmac/cfg80211.c:5473-5474`
- linux — the bsscfg helper sends the plain name when the interface's bsscfgidx is 0; otherwise it sends `bsscfg:` + name + NUL + le32 bsscfgidx + data — `linux/brcmfmac/fwil.c:259-289`, `linux/brcmfmac/fwil.c:308-309`
- linux — `brcmf_cfg80211_request_ap_if`, set, fallback when `interface_create` returned an error — literal name `bsscfg:ssid`, `struct brcmf_mbss_ssid_le` with bsscfgidx = first free index, SSID_len = 5, SSID = "ssid" followed by the index digit — `linux/brcmfmac/cfg80211.c:788-801`
- linux — that call is made on interface 0, which is created with bsscfgidx 0, so the helper adds no second prefix and no second index: the name sent is `bsscfg:ssid` followed by the 40-byte record — `linux/brcmfmac/cfg80211.c:826`, `linux/brcmfmac/cfg80211.c:848`, `linux/brcmfmac/cfg80211.h:441-444`, `linux/brcmfmac/core.c:1241`, `linux/brcmfmac/fwil.c:259-260`

Differences: embassy, c-driver, whd and the linux fallback path send 40 bytes with the index first under the name `bsscfg:ssid` `embassy/control.rs:583` `c-driver/cyw43_ll.c:2386` `whd/src/whd_ap.c:412` `linux/brcmfmac/cfg80211.c:800`. The linux P2P GO path sends the 36-byte record under the plain name `ssid` when bsscfgidx is 0 `linux/brcmfmac/cfg80211.c:5473` `linux/brcmfmac/fwil.c:259-260`. The index value differs: embassy writes 0 `embassy/control.rs:576`, c-driver writes `WWD_AP_INTERFACE` = 1 `c-driver/cyw43_ll.c:2382` `c-driver/cyw43_ll.c:152`, whd writes its `bss_index` `whd/src/whd_ap.c:414`, the linux fallback writes the first free bsscfg index `linux/brcmfmac/cfg80211.c:792-796`.

### `sta_info`
| | |
|---|---|
| Used by | linux, no prefix `linux/brcmfmac/cfg80211.c:3212`. Not found in embassy, whd, c-driver |
| Direction | get `linux/brcmfmac/cfg80211.c:3212` |
| Value | `struct brcmf_sta_info_le`, sizeof the struct in both directions `linux/brcmfmac/cfg80211.c:3212-3214`; 296 bytes (compiled, x86-64 host, with ETH_ALEN = 6 (recalled, not in these sources) and 8-byte alignment of the le64 fields; a build with 4-byte le64 alignment could differ) `linux/brcmfmac/fwil_types.h:614-706`. Request: first 6 bytes = station MAC, rest zero `linux/brcmfmac/cfg80211.c:3205-3206` |
| Record | `struct brcmf_sta_info_le` `linux/brcmfmac/fwil_types.h:614-706` |

- linux — `brcmf_cfg80211_get_station`, get station statistics; sent only when `tdls_sta_info` returned an error — buffer zeroed, MAC copied to offset 0, reply overwrites the same buffer — `linux/brcmfmac/cfg80211.c:3205-3214`

### `sup_wpa`
| | |
|---|---|
| Used by | embassy (`bsscfg:sup_wpa`), c-driver (`bsscfg:sup_wpa`), whd (`bsscfg:sup_wpa`), linux (`sup_wpa`, no prefix) `embassy/control.rs:378` `c-driver/cyw43_ll.c:2240` `whd/src/whd_wifi_api.c:705` `linux/brcmfmac/cfg80211.c:2539` |
| Direction | embassy, c-driver, whd: set `embassy/control.rs:378` `c-driver/cyw43_ll.c:2240` `whd/src/whd_wifi_api.c:711`. linux: set and get `linux/brcmfmac/cfg80211.c:2539` `linux/brcmfmac/feature.c:343` |
| Value | embassy, c-driver, whd: 8 bytes = u32 bsscfg index + u32 value (0 or 1) `embassy/control.rs:695-700` `c-driver/cyw43_ll.c:1546-1553` `whd/src/whd_wifi_api.c:705-710`. linux: 4 bytes, le32 `linux/brcmfmac/fwil.h:123-127` |
| Record | plain integer (linux) `linux/brcmfmac/fwil.h:123-127`; index + integer pair (others), no record type `embassy/control.rs:695-700` |

- embassy — open join, set — index 0, value 0 — `embassy/control.rs:378`
- embassy — join with any other auth, set — index 0, value 1 — `embassy/control.rs:392`
- embassy — both u32 are written little-endian by `set_iovar_u32x2` — `embassy/control.rs:695-700`
- c-driver — STA join, set; sent on `WWD_STA_INTERFACE` — index 0, value 0 if auth_type == 0 else 1 — `c-driver/cyw43_ll.c:2240`
- c-driver — both u32 are written little-endian by `cyw43_write_iovar_u32_u32`; payload length is name + NUL + 8 — `c-driver/cyw43_ll.c:1546-1553`
- whd — `whd_wifi_enable_supplicant`, set; return value discarded — {bss_index, 1 if auth_type has WPA, WPA2 or WPA3 bits else 0}, written without htod32 — `whd/src/whd_wifi_api.c:705-711`
- whd — `whd_wifi_enable_sup_set_passphrase`, set, before the passphrase is set; return value discarded — same pair, without htod32 — `whd/src/whd_wifi_api.c:1123-1131`
- whd — `whd_wifi_prepare_join`, set; return value discarded — {htod32(bss_index), htod32(1 if WPA, WPA2, WPA3 or WPA3_OWE bits else 0)} — `whd/src/whd_wifi_api.c:1818-1824`
- whd — `whd_wifi_leave`, set, chip id 43022 only — {htod32(bss_index), htod32(0)} — `whd/src/whd_wifi_api.c:2536-2545`
- whd — macro `IOVAR_STR_SUP_WPA` = "sup_wpa"; the prefix is a string-literal concatenation at each call site — `whd/src/include/whd_wlioctl.h:1077`, `whd/src/whd_wifi_api.c:705`
- linux — `brcmf_cfg80211_connect`, set, when the profile uses the firmware supplicant — le32 1 — `linux/brcmfmac/cfg80211.c:2537-2539`
- linux — `brcmf_cfg80211_connect`, set, otherwise — le32 0 — `linux/brcmfmac/cfg80211.c:2544-2545`
- linux — feature probe for `BRCMF_FEAT_FWSUP`, get: the feature is enabled unless the error is `-BRCMF_FW_UNSUPPORTED` — 4 bytes, value discarded — `linux/brcmfmac/feature.c:343`, `linux/brcmfmac/feature.c:196-199`

Differences: linux sends the plain name with a 4-byte value `linux/brcmfmac/cfg80211.c:2539` `linux/brcmfmac/fwil.h:123-127`. embassy, c-driver and whd send `bsscfg:sup_wpa` with 8 bytes, index first `embassy/control.rs:378` `c-driver/cyw43_ll.c:2240` `whd/src/whd_wifi_api.c:705-707`. Inside whd, two call sites byte-swap the pair and two do not `whd/src/whd_wifi_api.c:707` `whd/src/whd_wifi_api.c:1820`.

### `sup_wpa2_eapver`
| | |
|---|---|
| Used by | embassy (`bsscfg:sup_wpa2_eapver`), c-driver (`bsscfg:sup_wpa2_eapver`), whd (`bsscfg:sup_wpa2_eapver`) `embassy/control.rs:393` `c-driver/cyw43_ll.c:2244` `whd/src/whd_wifi_api.c:1827`. Not found in linux |
| Direction | set `embassy/control.rs:393` `c-driver/cyw43_ll.c:2244` `whd/src/whd_wifi_api.c:1831` |
| Value | 8 bytes = u32 LE bsscfg index + u32 LE value; all three write 0xFFFFFFFF (-1) `embassy/control.rs:393` `c-driver/cyw43_ll.c:2244` `whd/src/whd_wifi_api.c:1829-1830` |
| Record | index + integer pair, no record type `embassy/control.rs:695-700` |

- embassy — non-open join, set; embassy does not state what the value means — index 0, value 0xFFFFFFFF — `embassy/control.rs:393`
- c-driver — STA join, set, on `WWD_STA_INTERFACE`; source comment: use the EAPOL version the AP uses — index 0, value -1 — `c-driver/cyw43_ll.c:2242-2244`
- whd — `whd_wifi_prepare_join`, set; source comment states the same intent; return value discarded — {htod32(bss_index), htod32((uint32_t)-1)} — `whd/src/whd_wifi_api.c:1826-1831`, macro `whd/src/include/whd_wlioctl.h:1103`

### `sup_wpa_tmo`
| | |
|---|---|
| Used by | embassy (`bsscfg:sup_wpa_tmo`), c-driver (`bsscfg:sup_wpa_tmo`), whd (`bsscfg:sup_wpa_tmo`) `embassy/control.rs:394` `c-driver/cyw43_ll.c:2248` `whd/src/whd_wifi_api.c:726`. Not found in linux |
| Direction | set `embassy/control.rs:394` `c-driver/cyw43_ll.c:2248` `whd/src/whd_wifi_api.c:735` |
| Value | 8 bytes = u32 bsscfg index + 32-bit timeout. embassy and c-driver write both little-endian `embassy/control.rs:695-700` `c-driver/cyw43_ll.c:1546-1553`; whd writes both in host order without htod32 `whd/src/whd_wifi_api.c:729-730` |
| Record | index + integer pair, no record type `embassy/control.rs:695-700` |

- embassy — non-open join, set; followed by a 100 ms wait — index 0, value 2500 (unit not stated in embassy) — `embassy/control.rs:394-396`
- c-driver — STA join, set the supplicant EAPOL key timeout, on `WWD_STA_INTERFACE` — index 0, value `CYW_EAPOL_KEY_TIMEOUT` = 5000 — `c-driver/cyw43_ll.c:2248`, `c-driver/cyw43_ll.c:258`
- whd — `whd_wifi_set_supplicant_key_timeout`, set — {(int32_t)bss_index, eapol_key_timeout} in the non-`PROTO_MSGBUF` build — `whd/src/whd_wifi_api.c:726-735`, macro `whd/src/include/whd_wlioctl.h:1141`
- whd — value `DEFAULT_EAPOL_KEY_PACKET_TIMEOUT` = 3000 (ms per its comment) for WPA/WPA2 PSK, WPA3 and OWE joins — `whd/src/whd_wifi_api.c:1851-1852`, `whd/src/whd_wifi_api.c:1865-1866`, `whd/src/whd_wifi_api.c:1881-1882`, `whd/src/whd_wifi_api.c:79`
- whd — value 0 for enterprise security types; source comment: disables the EAPOL timer — `whd/src/whd_wifi_api.c:1894-1895`
- whd — in the `PROTO_MSGBUF` build the second copy targets `data + sizeof(bss_index)` on an `int32_t *`, which is 16 bytes in, not 4 (inferred) — `whd/src/whd_wifi_api.c:719`, `whd/src/whd_wifi_api.c:732-733`

Differences: the timeout value is 2500 in embassy `embassy/control.rs:394`, 5000 in c-driver `c-driver/cyw43_ll.c:258`, 3000 or 0 in whd `whd/src/whd_wifi_api.c:79` `whd/src/whd_wifi_api.c:1895`.

### `swdiv_timeout`
| | |
|---|---|
| Used by | none; whd defines the name and does not use it `whd/src/include/whd_wlioctl.h:1151`. Not found in embassy, linux, c-driver |
| Direction | not shown by any driver |
| Value | not shown by any driver |
| Record | none |

- whd — macro `IOVAR_STR_SWDIV_TIMEOUT` = "swdiv_timeout"; the macro occurs in whd only at its two definitions — `whd/src/include/whd_wlioctl.h:1151`, `whd/src/include_helium/whd_wlioctl.h:1152`

### `tdls_enable`
| | |
|---|---|
| Used by | linux, no prefix `linux/brcmfmac/cfg80211.c:8663`. Not found in embassy, whd, c-driver |
| Direction | set and get `linux/brcmfmac/cfg80211.c:8663` `linux/brcmfmac/feature.c:333` |
| Value | 4 bytes, le32 `linux/brcmfmac/fwil.h:123-127` |
| Record | plain integer `linux/brcmfmac/fwil.h:123-127` |

- linux — feature probe for `BRCMF_FEAT_TDLS`, get: enabled unless the error is `-BRCMF_FW_UNSUPPORTED` — value discarded — `linux/brcmfmac/feature.c:333`, `linux/brcmfmac/feature.c:196-199`
- linux — `brcmf_cfg80211_attach`, set, only when the TDLS feature flag is set; on error linux clears `WIPHY_FLAG_SUPPORTS_TDLS` — le32 1 — `linux/brcmfmac/cfg80211.c:8662-8666`

### `tdls_endpoint`
| | |
|---|---|
| Used by | linux, no prefix `linux/brcmfmac/cfg80211.c:6004`. Not found in embassy, whd, c-driver |
| Direction | set `linux/brcmfmac/cfg80211.c:6004` |
| Value | `struct brcmf_tdls_iovar_le`: ea[ETH_ALEN], u8 mode, le16 chanspec, le32 pad; 16 bytes (compiled, host) with mode at offset 6, chanspec at 8, pad at 12; ETH_ALEN = 6 is (recalled, not in these sources) `linux/brcmfmac/fwil_types.h:262-267` |
| Record | `struct brcmf_tdls_iovar_le` `linux/brcmfmac/fwil_types.h:262-267` |

- linux — `brcmf_cfg80211_tdls_oper`, set — record zeroed, mode = operation, ea = peer address when one is given — `linux/brcmfmac/cfg80211.c:5999-6005`
- linux — mode values: `BRCMF_TDLS_MANUAL_EP_CREATE` = 1 (setup), `BRCMF_TDLS_MANUAL_EP_DELETE` = 3 (teardown), `BRCMF_TDLS_MANUAL_EP_DISCOVERY` = 6 (discovery request) — `linux/brcmfmac/fwil_types.h:269-273`, `linux/brcmfmac/cfg80211.c:5967-5976`

### `tdls_sta_info`
| | |
|---|---|
| Used by | linux, no prefix `linux/brcmfmac/cfg80211.c:3207`. Not found in embassy, whd, c-driver |
| Direction | get `linux/brcmfmac/cfg80211.c:3207` |
| Value | `struct brcmf_sta_info_le`, same buffer and size as `sta_info`. Request: first 6 bytes = peer MAC, rest zero `linux/brcmfmac/cfg80211.c:3205-3209` |
| Record | `struct brcmf_sta_info_le` `linux/brcmfmac/fwil_types.h:614-706` |

- linux — `brcmf_cfg80211_get_station`, get, tried first; success marks the station as a TDLS peer, failure falls back to `sta_info` — buffer zeroed, MAC copied to offset 0 — `linux/brcmfmac/cfg80211.c:3205-3214`

### `tko`
| | |
|---|---|
| Used by | whd, no prefix `whd/src/whd_wifi_api.c:6233`. Not found in embassy, linux, c-driver |
| Direction | set and get `whd/src/whd_wifi_api.c:6153-6182` `whd/src/whd_wifi_api.c:6193-6199` |
| Value | `wl_tko_t` header (u16 subcmd_id, u16 len, both htod16) followed by a sub-command record at offset 4 `whd/src/include/whd_wlioctl.h:4307-4312`. whd allocates 1496 bytes (1500 - strlen("tko") - 1) or 96 bytes (100 - 3 - 1) for every request, regardless of the length field `whd/src/whd_wifi_api.c:6338-6339` `whd/src/whd_wifi_api.c:6232-6233` |
| Record | `wl_tko_t` `whd/src/include/whd_wlioctl.h:4307-4312`; sub-command ids `whd/src/include/whd_wlioctl.h:4315-4322`; sub-records listed per use below |

- whd — macro `IOVAR_STR_TKO` = "tko" — `whd/src/include/whd_wlioctl.h:1264`
- whd — sub-command ids: MAX_TCP 0, PARAM 1, CONNECT 2, ENABLE 3, STATUS 4, AUTOENAB 6, AUTOCONNECT 7, FILTER 8 — `whd/src/include/whd_wlioctl.h:4315-4322`
- whd — `TKO_DATA_OFFSET` = offsetof(wl_tko_t, data); `WHD_PAYLOAD_MTU` = 1500 — `whd/inc/whd_types.h:1569`, `whd/inc/whd_types.h:242`
- whd — `whd_tko_param(set)`, set the keepalive timing — subcmd PARAM (1), len = 4 + sizeof(`wl_tko_param_t`); `wl_tko_param_t` {u16 interval, u16 retry_interval, u16 retry_count, pad[2]}; a zero argument is replaced by the default 20 s, 3 s, 3 retries; the three fields are not byte-swapped — `whd/src/whd_wifi_api.c:6153-6182`, `whd/src/include/whd_wlioctl.h:4332-4338`, `whd/src/include/whd_wlioctl.h:4302-4304`
- whd — `whd_tko_param(get)`, get the keepalive timing — same PARAM request; reply `wl_tko_param_t` read at offset 4 — `whd/src/whd_wifi_api.c:6193-6199`
- whd — `whd_tko_get_status`, get — subcmd STATUS (4), len = 4 + sizeof(`wl_tko_status_t`), 96-byte buffer; if the reply len is at least 5, 5 bytes (MAX_TKO_CONN 4 + 1 count byte) are copied from offset 4 — `whd/src/whd_wifi_api.c:6232-6262`, `whd/src/include/whd_wlioctl.h:4383-4391`, `whd/src/include/whd_wlioctl.h:4299`
- whd — `whd_tko_max_assoc`, get — subcmd MAX_TCP (0), len = 4 + sizeof(`wl_tko_max_tcp_t`) {u8 max, pad[3]}, 96-byte buffer; reply read at offset 4 — `whd/src/whd_wifi_api.c:6287-6312`, `whd/src/include/whd_wlioctl.h:4325-4329`
- whd — `whd_tko_get_FW_connect`, get one offloaded connection — subcmd CONNECT (2), len = 4 (header only), connection index written to the first data byte, which lies beyond that len — `whd/src/whd_wifi_api.c:6338-6352`
- whd — `whd_tko_toggle`, set — subcmd ENABLE (3), len = 4 + sizeof(`wl_tko_enable_t`) {u8 enable, pad[3]}; pad not written — `whd/src/whd_wifi_api.c:6415-6433`, `whd/src/include/whd_wlioctl.h:4375-4379`
- whd — `whd_tko_autoenab`, set — subcmd AUTOENAB (6), len = 4 + sizeof(`wl_tko_autoenab_t`) {u16 version = `WL_TKO_AUTO_VER` 1, u16 length = bytes after the length field, u8 enable, pad[3]}; version and length not byte-swapped — `whd/src/whd_wifi_api.c:6461-6480`, `whd/src/include/whd_wlioctl.h:4456-4461`, `whd/src/include/whd_wlioctl.h:39`, `whd/inc/whd_wifi_api.h:41-42`
- whd — `whd_tko_filter`, set — subcmd FILTER (8), len = 4 + sizeof(`wl_tko_filter_t`) {u16 version = 1, u16 length, u16 sport, u16 dport, ip_src[16], ip_dst[16]}; each of the four filter fields is written only when its flag bit is set — `whd/src/whd_wifi_api.c:6508-6542`, `whd/src/include/whd_wlioctl.h:4481-4488`
- whd — the filter `length` is computed with `REMAINING_LEN(wl_filter, wl_tko_autoenab_t, length)`: sizeof the filter record (40) minus the offset of `length` in the autoenab record (2) minus the size of the filter's `length` (2), giving 36 (computed) — `whd/src/whd_wifi_api.c:6529`, `whd/inc/whd_wifi_api.h:41-42`
- whd — `whd_configure_tko_filter` sends ENABLE(0), AUTOENAB(1), FILTER, ENABLE(1) in that order — `whd/src/whd_wifi_api.c:1053-1079`
- whd — `whd_configure_tko_offload` sends AUTOENAB then, if that succeeded, ENABLE; it is called from `whd_wifi_offload_config`, which the init sequence calls when fwcap `WHD_FWCAP_OFFLOADS` is set — `whd/src/whd_wifi_api.c:1080-1096`, `whd/src/whd_wifi_api.c:846`, `whd/src/whd_management.c:535-537`
- whd — in the CDC path the request buffer is not zeroed beyond the name-alignment pad, so bytes the caller does not write are whatever the buffer held (inferred); the msgbuf helper clears the whole buffer — `whd/src/whd_cdc_bdc.c:349-367`, `whd/src/whd_msgbuf_txrx.c:223`
- whd — sub-record sizes (compiled, x86 host, -m32 and -m64; not compiled for ARM): data offset 4, max_tcp 4, param 8, enable 4, status 2, autoenab 8, filter 40 — `whd/src/include/whd_wlioctl.h:4307-4488`

### `tlv`
| | |
|---|---|
| Used by | linux, no prefix `linux/brcmfmac/fwsignal.c:2399`. whd defines the name and does not use it `whd/src/include/whd_wlioctl.h:1143`. Not found in embassy, c-driver |
| Direction | linux: set `linux/brcmfmac/fwsignal.c:2399` |
| Value | linux: 4 bytes, le32 bit flags `linux/brcmfmac/fwsignal.c:139-145` `linux/brcmfmac/fwil.h:123-127` |
| Record | plain integer `linux/brcmfmac/fwil.h:123-127` |

- linux — enable BDC v2 TLV signalling, set; sent on interface 0 — 0x0001 (`BRCMF_FWS_FLAGS_RSSI_SIGNALS`) always; when fcmode is not NONE also XONXOFF 0x0002, CREDIT_STATUS 0x0004, HOST_PROPTXSTATUS_ACTIVE 0x0008, HOST_RXREORDER_ACTIVE 0x0040, giving 79 (0x004f) — `linux/brcmfmac/fwsignal.c:2341`, `linux/brcmfmac/fwsignal.c:2373-2377`, `linux/brcmfmac/fwsignal.c:2397-2399`, `linux/brcmfmac/fwsignal.c:139-145`
- linux — on failure linux sets fcmode back to NONE and continues — `linux/brcmfmac/fwsignal.c:2399-2403`
- linux — not sent when fcmode is NONE and the bus does not force the FWS queue — `linux/brcmfmac/fwsignal.c:2357-2362`
- whd — macro `IOVAR_STR_TLV` = "tlv"; the macro occurs in whd only at its two definitions — `whd/src/include/whd_wlioctl.h:1143`, `whd/src/include_helium/whd_wlioctl.h:1144`

### `toe_ol`
| | |
|---|---|
| Used by | linux, no prefix `linux/brcmfmac/core.c:621`. Not found in embassy, whd, c-driver |
| Direction | get `linux/brcmfmac/core.c:621` |
| Value | 4 bytes, le32 bit flags `linux/brcmfmac/core.c:621-622` |
| Record | plain integer `linux/brcmfmac/core.c:621` |

- linux — at netdev open, get, decides whether to advertise `NETIF_F_IP_CSUM` — tests bit `TOE_TX_CSUM_OL` = 1 (0x00000001) — `linux/brcmfmac/core.c:620-625`, `linux/brcmfmac/core.h:22`

### `twt`
| | |
|---|---|
| Used by | whd, no prefix `whd/src/whd_wifi_api.c:4788-4789`. Not found in embassy, linux, c-driver |
| Direction | set `whd/src/whd_wifi_api.c:4794` |
| Value | `whd_xtlv_t` header (u16 id, u16 len, written in host order without htod16) followed by a command record at offset 4. Buffer = sizeof(record) + 4 `whd/src/whd_wifi_api.c:4788-4793` |
| Record | `whd_xtlv_t` `whd/src/include/whd_wlioctl.h:450-455`; `wl_twt_setup_t` `whd/src/include/whd_wlioctl.h:260-273`; `wl_twt_teardown_t` `whd/src/include/whd_wlioctl.h:290-304`; `wl_twt_info_t` `whd/src/include/whd_wlioctl.h:332-343` |

- whd — command ids: `WL_TWT_CMD_SETUP` 1, `WL_TWT_CMD_TEARDOWN` 2, `WL_TWT_CMD_INFO` 3 — `whd/src/include/whd_wlioctl.h:158-160`
- whd — every record starts with u16 version = 0 and u16 length = sizeof(record) - 4 — `whd/src/whd_wifi_api.c:4596-4597`, `whd/src/whd_wifi_api.c:4714-4715`, `whd/src/whd_wifi_api.c:4768-4769`, `whd/src/include/whd_wlioctl.h:257`, `whd/src/include/whd_wlioctl.h:278`, `whd/src/include/whd_wlioctl.h:329`
- whd — `whd_wifi_itwt_setup`, set up an individual TWT; then waits on a TWT event semaphore — id SETUP, len = sizeof(`wl_twt_setup_t`); negotiation_type `TWT_CTRL_NEGO_TYPE_0`, flow_flags REQUEST plus trigger/unannounced, wake_dur, wake_int, flow_id — `whd/src/whd_wifi_api.c:4595-4628`
- whd — `whd_wifi_btwt_join`, join a broadcast TWT — id SETUP; negotiation_type `TWT_CTRL_NEGO_TYPE_3`, wake_type `WL_TWT_TIME_TYPE_BSS`, bid — `whd/src/whd_wifi_api.c:4667-4687`
- whd — `whd_wifi_twt_teardown`; then waits on the TWT event semaphore — id TEARDOWN, len = sizeof(`wl_twt_teardown_t`); negotiation_type, flow_id, bid, alltwt from the caller — `whd/src/whd_wifi_api.c:4713-4728`
- whd — `whd_wifi_twt_information_frame`, suspend or resume — id INFO, len = sizeof(`wl_twt_info_t`); flow_id from the caller, next_twt_h = 0; on suspend flow_flags = `WL_TWT_INFO_FLAG_ALL_TWT` (1) in the non-`PROTO_MSGBUF` build or 0 with `PROTO_MSGBUF`, next_twt_l = 0; on resume flow_flags = `WL_TWT_INFO_FLAG_RESUME` (2) only, next_twt_l = resume_time * 1000000 — `whd/src/whd_wifi_api.c:4767-4794`, `whd/src/include/whd_wlioctl.h:320-321`
- whd — `whd_wifi_btwt_config`, configure a broadcast TWT schedule — id SETUP; negotiation_type `TWT_CTRL_NEGO_TYPE_2`, wake_type `WL_TWT_TIME_TYPE_BSS`, bid — `whd/src/whd_wifi_api.c:4842-4860`
- whd — record sizes (compiled, x86 host, -m32 and -m64; not compiled for ARM): setup 52, teardown 18, info 44, so buffers of 56, 22 and 48 bytes — `whd/src/include/whd_wlioctl.h:260-343`
- whd — macro `IOVAR_STR_TWT` = "twt" — `whd/src/include/whd_wlioctl.h:1269`

### `txbf`
| | |
|---|---|
| Used by | linux, no prefix `linux/brcmfmac/common.c:454`. Not found in embassy, whd, c-driver |
| Direction | set `linux/brcmfmac/common.c:454` |
| Value | 4 bytes, le32 `linux/brcmfmac/fwil.h:123-127` |
| Record | plain integer `linux/brcmfmac/fwil.h:123-127` |

- linux — enable TX beamforming during preinit, set; return value discarded — le32 1 — `linux/brcmfmac/common.c:453-454`

### `txbf_bfe_cap`
| | |
|---|---|
| Used by | linux, no prefix `linux/brcmfmac/cfg80211.c:7590`. Not found in embassy, whd, c-driver |
| Direction | get `linux/brcmfmac/cfg80211.c:7590` |
| Value | 4 bytes, le32 `linux/brcmfmac/cfg80211.c:7590-7591` |
| Record | plain integer `linux/brcmfmac/cfg80211.c:7590-7591` |

- linux — `brcmf_setup_wiphybands`, get the beamformee capability, only when `vhtmode` read non-zero; error ignored — 4 bytes — `linux/brcmfmac/cfg80211.c:7588-7591`

### `txbf_bfr_cap`
| | |
|---|---|
| Used by | linux, no prefix `linux/brcmfmac/cfg80211.c:7592`. Not found in embassy, whd, c-driver |
| Direction | get `linux/brcmfmac/cfg80211.c:7592` |
| Value | 4 bytes, le32 `linux/brcmfmac/cfg80211.c:7592-7593` |
| Record | plain integer `linux/brcmfmac/cfg80211.c:7592-7593` |

- linux — `brcmf_setup_wiphybands`, get the beamformer capability, only when `vhtmode` read non-zero; error ignored — 4 bytes — `linux/brcmfmac/cfg80211.c:7588-7593`

### `txcapload`
| | |
|---|---|
| Used by | linux, no prefix `linux/brcmfmac/common.c:216-217`. Not found in embassy, whd, c-driver |
| Direction | set `linux/brcmfmac/common.c:143-159` |
| Value | `struct brcmf_dload_data_le`: le16 flag, le16 dload_type, le32 len, le32 crc (12 bytes), then up to 1400 data bytes; at most 1412 bytes per send `linux/brcmfmac/fwil_types.h:1106-1112` `linux/brcmfmac/fwil_types.h:185` |
| Record | `struct brcmf_dload_data_le` `linux/brcmfmac/fwil_types.h:1106-1112` |

- linux — download the TxCap blob, set — one send per chunk of at most `MAX_CHUNK_LEN` = 1400 bytes; len = chunk length, crc = 0, dload_type = `DL_TYPE_CLM` = 2 — `linux/brcmfmac/common.c:108-115`, `linux/brcmfmac/common.c:143-159`, `linux/brcmfmac/fwil_types.h:185`, `linux/brcmfmac/fwil_types.h:194`
- linux — flag = (`DLOAD_HANDLER_VER` 1 << 12) | `DL_BEGIN` 0x0002 on the first chunk | `DL_END` 0x0004 on the last: 0x1002 first, 0x1000 middle, 0x1004 last, 0x1006 for a single chunk (computed) — `linux/brcmfmac/common.c:108`, `linux/brcmfmac/common.c:129`, `linux/brcmfmac/common.c:148`, `linux/brcmfmac/common.c:155`, `linux/brcmfmac/fwil_types.h:187-192`
- linux — the name is passed as a literal to the shared blob downloader; skipped when the bus has no TxCap blob — `linux/brcmfmac/common.c:209-217`

### `txcapload_status`
| | |
|---|---|
| Used by | linux, no prefix `linux/brcmfmac/common.c:216-217`. Not found in embassy, whd, c-driver |
| Direction | get `linux/brcmfmac/common.c:165` |
| Value | 4 bytes, le32 `linux/brcmfmac/common.c:165` |
| Record | plain integer `linux/brcmfmac/common.c:165` |

- linux — read only after a `txcapload` send failed, get — value printed at debug level only — `linux/brcmfmac/common.c:161-169`, name literal at `linux/brcmfmac/common.c:216-217`

### `txstreams`
| | |
|---|---|
| Used by | linux, no prefix `linux/brcmfmac/cfg80211.c:7589`. Not found in embassy, whd, c-driver |
| Direction | get `linux/brcmfmac/cfg80211.c:7589` |
| Value | 4 bytes, le32 `linux/brcmfmac/cfg80211.c:7589` |
| Record | plain integer `linux/brcmfmac/cfg80211.c:7589` |

- linux — `brcmf_setup_wiphybands`, get the number of TX streams (inferred), only when `vhtmode` read non-zero; error ignored — 4 bytes — `linux/brcmfmac/cfg80211.c:7588-7589`

### `ulp`
| | |
|---|---|
| Used by | whd, no prefix `whd/src/whd_wifi_api.c:3847`. Not found in embassy, linux, c-driver |
| Direction | set and get `whd/src/whd_wifi_api.c:3854` `whd/src/whd_wifi_api.c:3847` |
| Value | 4 bytes, uint32, htod32 on set, dtoh32 on get `whd/src/whd_wifi_api.c:5153-5183` |
| Record | plain integer `whd/src/whd_wifi_api.c:5153-5183` |

- whd — `whd_wifi_config_ulp_mode`, get the current ULP mode; return code not checked — 4 bytes — `whd/src/whd_wifi_api.c:3847`, `whd/src/whd_wifi_api.c:5165-5183`
- whd — set when the mode read back was 0 — `*mode`, `ULP_DS1_SUPPORT` (1) or `ULP_DS2_SUPPORT` (2) — `whd/src/whd_wifi_api.c:3848-3854`, `whd/inc/whd_types.h:96-97`
- whd — set, turn ULP off — `ULP_NO_SUPPORT` (0) — `whd/src/whd_wifi_api.c:3861-3863`, `whd/inc/whd_types.h:95`
- whd — all three run only for chip id 43022 or 43012, and the function is compiled only with `CYCFG_ULP_SUPPORT_ENABLED` — `whd/src/whd_wifi_api.c:3832`, `whd/src/whd_wifi_api.c:3818`
- whd — macro `IOVAR_STR_ULP` = "ulp" — `whd/src/include/whd_wlioctl.h:1182`

### `ulp_host_intr_mode`
| | |
|---|---|
| Used by | whd, no prefix `whd/src/whd_management.c:576`. Not found in embassy, linux, c-driver |
| Direction | set `whd/src/whd_management.c:576` |
| Value | 4 bytes, uint32, htod32 `whd/src/whd_wifi_api.c:5153-5162` |
| Record | plain integer `whd/src/whd_wifi_api.c:5153-5162` |

- whd — init, set, only with `CYCFG_ULP_SUPPORT_ENABLED` and chip id 43022; result ignored — `ULP_OOB_INTR_MODE` = 1 — `whd/src/whd_management.c:572-577`, `whd/inc/whd_types.h:90`, `whd/src/whd_wifi_api.c:5153-5162`
- whd — macro `IOVAR_STR_ULP_HOST_INTR_MODE` = "ulp_host_intr_mode" — `whd/src/include/whd_wlioctl.h:1183`

### `ulp_wait`
| | |
|---|---|
| Used by | whd, no prefix `whd/src/whd_wifi_api.c:3845`. Not found in embassy, linux, c-driver |
| Direction | set `whd/src/whd_wifi_api.c:3845` |
| Value | 4 bytes, uint32, htod32 `whd/src/whd_wifi_api.c:5153-5162` |
| Record | plain integer `whd/src/whd_wifi_api.c:5153-5162` |

- whd — `whd_wifi_config_ulp_mode`, set when mode is DS1 or DS2; chip id 43022 or 43012 only; compiled only with `CYCFG_ULP_SUPPORT_ENABLED` — `*wait_time` from the caller (unit not stated at the call site) — `whd/src/whd_wifi_api.c:3832-3845`, `whd/src/whd_wifi_api.c:3818`, `whd/src/whd_wifi_api.c:5153-5162`
- whd — macro `IOVAR_STR_ULP_WAIT` = "ulp_wait" — `whd/src/include/whd_wlioctl.h:1181`

### `ver`
| | |
|---|---|
| Used by | linux, whd; no prefix `linux/brcmfmac/common.c:364` `whd/src/whd_wifi_api.c:5360`. Not found in embassy, c-driver |
| Direction | get `linux/brcmfmac/common.c:364` `whd/src/whd_wifi_api.c:5360` |
| Value | text string. linux reads into a 256-byte buffer `linux/brcmfmac/common.c:364` `linux/brcmfmac/core.h:30`; whd reads into a caller buffer, 200 bytes at its one internal call `whd/src/whd_wifi_api.c:411` `whd/src/whd_wifi_api.c:438` |
| Record | none (character buffer) `linux/brcmfmac/common.c:269` |

- linux — read the version string during preinit, get; linux cuts it at the first newline, logs it, and keeps the text after the last space as `fwver` — buffer zeroed, 256 bytes (`BRCMF_DCMD_SMLEN`) — `linux/brcmfmac/common.c:269`, `linux/brcmfmac/common.c:363-383`, `linux/brcmfmac/core.h:30`
- whd — `whd_wifi_get_wifi_version`, get — caller buffer of `length` bytes, `length` being a uint8_t — `whd/src/whd_wifi_api.c:5350-5360`, macro `whd/src/include/whd_wlioctl.h:1102`
- whd — called from `whd_wifi_set_up` with a 200-byte buffer after `WLC_UP`, to print the version; skipped when the state is already `WLAN_UP` — `whd/src/whd_wifi_api.c:411`, `whd/src/whd_wifi_api.c:417-424`, `whd/src/whd_wifi_api.c:438`, `whd/src/whd_management.c:533`

Differences: linux requests 256 bytes `linux/brcmfmac/common.c:364`; whd requests the caller's length, 200 at its internal call `whd/src/whd_wifi_api.c:411` `whd/src/whd_wifi_api.c:438`.

### `vht_features`
| | |
|---|---|
| Used by | none; whd defines the name and does not use it `whd/src/include/whd_wlioctl.h:1164`. Not found in embassy, linux, c-driver |
| Direction | not shown by any driver |
| Value | not shown by any driver |
| Record | none |

- whd — macro `IOVAR_STR_VHT_FEATURES` = "vht_features"; the macro occurs in whd only at its two definitions — `whd/src/include/whd_wlioctl.h:1164`, `whd/src/include_helium/whd_wlioctl.h:1165`

### `vhtmode`
| | |
|---|---|
| Used by | linux, no prefix `linux/brcmfmac/cfg80211.c:7556`. Not found in embassy, whd, c-driver |
| Direction | get `linux/brcmfmac/cfg80211.c:7556` |
| Value | 4 bytes, le32 `linux/brcmfmac/cfg80211.c:7556` |
| Record | plain integer `linux/brcmfmac/cfg80211.c:7556` |

- linux — `brcmf_setup_wiphybands`, get; error ignored; non-zero enables the `txstreams`, `txbf_bfe_cap` and `txbf_bfr_cap` reads — 4 bytes — `linux/brcmfmac/cfg80211.c:7556`, `linux/brcmfmac/cfg80211.c:7588-7593`

### `vndr_ie`
| | |
|---|---|
| Used by | linux (through the bsscfg helper: bare `vndr_ie` when the interface's bsscfg index is 0, `bsscfg:vndr_ie` + u32 LE index otherwise `linux/brcmfmac/fwil.c:259-260` `linux/brcmfmac/fwil.c:273-284`); whd (always `bsscfg:vndr_ie` + u32 index `whd/src/whd_wifi_api.c:4289-4292`). Not found in embassy or c-driver |
| Direction | set (linux, whd) |
| Value | linux: one or more records of 12 + IE length bytes each, little-endian `linux/brcmfmac/cfg80211.c:4901-4913`. whd: 4-byte index, then one `vndr_ie_setbuf_t` holding one IE; buffer length `sizeof(vndr_ie_setbuf_t)` + data length + 4 `whd/src/whd_wifi_api.c:4289` = 24 + data length with `sizeof` = 20 (inferred: 18 bytes of fields plus 2 of tail padding under natural alignment `whd/src/include/whd_wlioctl.h:1945-1967`) |
| Record | linux: no struct, offsets by macro: cmd[4] at 0, count at 4, pktflag at 8, IE at 12 `linux/brcmfmac/cfg80211.c:69-75`. whd: `vndr_ie_setbuf_t` { cmd[4], `vndr_ie_buf_t` { iecount, `vndr_ie_info_t` { pktflag, `wl_vndr_ie` { id, len, oui[3], data[] } } } } `whd/src/include/whd_wlioctl.h:1945-1967`; macro `IOVAR_STR_VENDOR_IE` `whd/src/include/whd_wlioctl.h:1087` `whd/src/include_helium/whd_wlioctl.h:1088` |

- linux — set — a run of records, each: cmd = "del" or "add" copied with `strscpy` into 4 bytes, count = 1 (u32 LE) at 4, pktflag (u32 LE) at 8, the whole vendor IE (id, len, body) at 12; "del" records for the previously saved IEs first, then "add" records for the new ones; sent only if at least one record was built — replace the vendor IEs for one management frame type (`brcmf_vif_set_mgmt_ie`) — `linux/brcmfmac/cfg80211.c:4901-4913` `linux/brcmfmac/cfg80211.c:5019-5022` `linux/brcmfmac/cfg80211.c:5054-5057` `linux/brcmfmac/cfg80211.c:5068-5070`
- linux — the pktflag is the frame-type flag the caller passed (probe request, probe response, beacon, association request, association response) — `linux/brcmfmac/cfg80211.c:4949-4974`
- whd — set — u32 bsscfg index written without `htod32`; cmd = "add" or "del" + NUL; iecount = `htod32(1)`; pktflag = `htod32(which_packets)`; IE id 221 (0xdd); len = data length + 3 (OUI) + 1 (subtype); OUI; subtype in data[0]; caller data from data[1] — add or remove one vendor IE in selected management frames (`whd_wifi_manage_custom_ie`) — `whd/src/whd_wifi_api.c:4289-4320`
- whd — byte offsets after the 4-byte index: cmd 0-3, iecount 4-7, pktflag 8-11, id 12, len 13, oui 14-16, subtype 17, data from 18 (from the struct definition; inferred from field order and natural alignment). The function fills 22 + data length bytes of the 24 + data length requested; it does not write the last 2 (inferred from the same sizes) — `whd/src/include/whd_wlioctl.h:1945-1967` `whd/src/whd_wifi_api.c:4289-4318`

Differences: linux can send several records in one buffer and passes the IE verbatim; whd sends exactly one IE and builds it from OUI, subtype and data. linux drops the `bsscfg:` prefix and the index when the index is 0; whd always sends prefix and index. whd writes the index in host order and the other two integers through `htod32`; linux writes all integers little-endian. Both put cmd at 0, count at 4, pktflag at 8 and the IE at 12. `linux/brcmfmac/cfg80211.c:4901-4913` `linux/brcmfmac/fwil.c:259-284` `whd/src/whd_wifi_api.c:4289-4320`

### `wd_disable`
| | |
|---|---|
| Used by | defined, not used by whd. Not found in embassy, linux, c-driver |
| Direction | not shown by any driver |
| Value | payload not shown by any driver |
| Record | macro `IOVAR_STR_WD_DISABLE` only `whd/src/include/whd_wlioctl.h:1245` `whd/src/include_helium/whd_wlioctl.h:1246` |

- whd — no `.c` file under `whd/` references `IOVAR_STR_WD_DISABLE` — `whd/src/include/whd_wlioctl.h:1245`

### `wlc_ver`
| | |
|---|---|
| Used by | linux, no `bsscfg:` prefix. Not found in embassy, whd, c-driver |
| Direction | get |
| Value | `struct brcmf_wlc_version_le`, 16 bytes, eight u16 LE |
| Record | `struct brcmf_wlc_version_le` { version, length, epi_ver_major, epi_ver_minor, epi_ver_rc, epi_ver_incr, wlc_ver_major, wlc_ver_minor } `linux/brcmfmac/fwil_types.h:823-834` |

- linux — get — reads the record and uses `wlc_ver_major` (offset 12) and `wlc_ver_minor` (offset 14): major.minor >= 12.0 enables `BRCMF_FEAT_PMKID_V2`, >= 13.0 enables `BRCMF_FEAT_PMKID_V3`; on an error return the function returns without enabling either — feature detection — `linux/brcmfmac/feature.c:139-142` `linux/brcmfmac/feature.c:152-167`
- linux — the GET request carries name + NUL + the caller's 16-byte buffer as it stood (an uninitialised local here) — `linux/brcmfmac/fwil.c:166-184` `linux/brcmfmac/fwil.c:226-232` `linux/brcmfmac/feature.c:148`

### `wlfc_mode`
| | |
|---|---|
| Used by | linux, no `bsscfg:` prefix. Not found in embassy, whd, c-driver |
| Direction | both |
| Value | u32 LE, 4 bytes |
| Record | plain integer |

- linux — get — reads one u32 and tests bit 3 (`BRCMF_FWS_MODE_REUSESEQ_SHIFT`); the 4 request bytes are the uninitialised local `mode` — ask whether sequence-number reuse is supported — `linux/brcmfmac/fwsignal.c:2409-2410` `linux/brcmfmac/fwsignal.c:164-169` `linux/brcmfmac/fwsignal.c:2343` `linux/brcmfmac/fwil.h:129-138`
- linux — set — u32 LE value 8 (0x8): `mode` zeroed, then bit 3 set; sent only when the get reported bit 3 — enable sequence-number reuse — `linux/brcmfmac/fwsignal.c:2411-2414` `linux/brcmfmac/fwil.h:122-127`

### `wme_ac_sta`
| | |
|---|---|
| Used by | linux, whd; no `bsscfg:` prefix in either. Not found in embassy, c-driver |
| Direction | get (linux, whd) |
| Value | 4 records of 4 bytes = 16 bytes. linux asks with a 16-byte buffer; whd asks with a 64-byte zeroed buffer and copies 16 bytes of the reply |
| Record | linux `struct brcmf_cfg80211_edcf_acparam` { u8 ACI, u8 ECW, u16 TXOP } `linux/brcmfmac/cfg80211.h:279-283`, array of `EDCF_AC_COUNT` = 4 `linux/brcmfmac/cfg80211.h:33`. whd `edcf_acparam_t` { u8 ACI, u8 ECW, u16 TXOP } `whd/src/include/whd_wlioctl.h:3909-3915`; macro `IOVAR_STR_AC_PARAMS_STA` `whd/src/include/whd_wlioctl.h:1090` `whd/src/include_helium/whd_wlioctl.h:1091` |

- linux — get — reads 4 AC parameter records after association and passes them to `brcmf_wifi_prioritize_acparams` to build the AC priority map — `linux/brcmfmac/cfg80211.c:6474` `linux/brcmfmac/cfg80211.c:6529-6538`
- whd — get — 64-byte buffer set to 0, reply copied as 4 x `edcf_acparam_t` to the caller (`whd_wifi_get_acparams`) — `whd/src/whd_wifi_api.c:4197-4204`

Differences: request length is 16 bytes (linux) against 64 bytes (whd). Both read the same 16-byte layout. Both headers comment TXOP as stored least-significant octet first `linux/brcmfmac/cfg80211.h:282` `whd/src/include/whd_wlioctl.h:3913`.

### `wme_bss_disable`
| | |
|---|---|
| Used by | linux, through the bsscfg helper (bare name at bsscfg index 0, `bsscfg:wme_bss_disable` + u32 LE index otherwise `linux/brcmfmac/fwil.c:259-284`). Not found in embassy, whd, c-driver |
| Direction | set |
| Value | u32 LE, 4 bytes, 0 or 1 |
| Record | plain integer |

- linux — set — 1 when an RSN IE is present, changed to 0 when its RSN capabilities have the PTK replay-counter bits set; sent only on the RSN IE path — AP-mode WPA/RSN IE configuration (`brcmf_configure_wpaie`) — `linux/brcmfmac/cfg80211.c:4750-4755` `linux/brcmfmac/cfg80211.c:4785-4787` `linux/brcmfmac/fwil.h:153-160`

### `wnm`
| | |
|---|---|
| Used by | defined, not used by whd. Not found in embassy, linux, c-driver |
| Direction | not shown by any driver |
| Value | payload not shown by any driver |
| Record | macro `IOVAR_STR_WNM` only `whd/src/include/whd_wlioctl.h:1210` `whd/src/include_helium/whd_wlioctl.h:1211` |

- whd — no `.c` file under `whd/` references `IOVAR_STR_WNM` — `whd/src/include/whd_wlioctl.h:1210`

### `wnm_bsstrans_query`
| | |
|---|---|
| Used by | defined, not used by whd. Not found in embassy, linux, c-driver |
| Direction | not shown by any driver |
| Value | payload not shown by any driver |
| Record | macro `IOVAR_STR_BSSTRANS_QUERY` only `whd/src/include/whd_wlioctl.h:1211` `whd/src/include_helium/whd_wlioctl.h:1212` |

- whd — no `.c` file under `whd/` references `IOVAR_STR_BSSTRANS_QUERY` — `whd/src/include/whd_wlioctl.h:1211`

### `wnm_bsstrans_resp`
| | |
|---|---|
| Used by | defined, not used by whd. Not found in embassy, linux, c-driver |
| Direction | not shown by any driver |
| Value | payload not shown by any driver |
| Record | macro `IOVAR_STR_BSSTRANS_RESP` only `whd/src/include/whd_wlioctl.h:1212` `whd/src/include_helium/whd_wlioctl.h:1213` |

- whd — no `.c` file under `whd/` references `IOVAR_STR_BSSTRANS_RESP` — `whd/src/include/whd_wlioctl.h:1212`

### `wnm_maxidle`
| | |
|---|---|
| Used by | whd, no `bsscfg:` prefix. Not found in embassy, linux, c-driver |
| Direction | set |
| Value | two u32, 8 bytes, written in host order (no `htod32`) |
| Record | no struct; macro `IOVAR_WNM_MAXIDLE` (not `IOVAR_STR_*`) `whd/src/include/whd_wlioctl.h:1267` `whd/src/include_helium/whd_wlioctl.h:1268` |

- whd — set — word 0 = period (a u16 argument widened to u32), word 1 = 1 (commented as the idle option) — set the BSS max idle period (`whd_wifi_bss_max_idle`) — `whd/src/whd_wifi_api.c:4407` `whd/src/whd_wifi_api.c:4417-4423`

### `wowl`
| | |
|---|---|
| Used by | linux, whd; no `bsscfg:` prefix in either. Not found in embassy, c-driver |
| Direction | both (linux, whd) |
| Value | u32 LE, 4 bytes, bit mask of wake triggers |
| Record | plain integer. Bit names: linux `BRCMF_WOWL_*` `linux/brcmfmac/fwil_types.h:85-137`; whd `WL_WOWL_*` `whd/src/include/whd_wlioctl.h:3747-3759`; whd macro `IOVAR_STR_WOWL` `whd/src/include/whd_wlioctl.h:1168` `whd/src/include_helium/whd_wlioctl.h:1169` |

- linux — get — value discarded; `BRCMF_FEAT_WOWL` is set unless the call returns `-BRCMF_FW_UNSUPPORTED` (any other result, including other errors, enables it); only tried when the bus reports `wowl_supported`; request bytes are an uninitialised local — feature probe — `linux/brcmfmac/feature.c:309-310` `linux/brcmfmac/feature.c:187-199`
- linux — set — mask built before suspend: DIS (bit 2) + BCN (bit 4) + RETR (bit 3) for wake on disconnect, MAGIC (bit 0), NET (bit 1) when patterns are given, PFN_FOUND (bit 27), GTK_FAILURE (bit 10), UNASSOC (bit 24) when not connected — choose wake events (`brcmf_configure_wowl`) — `linux/brcmfmac/cfg80211.c:4255-4285` `linux/brcmfmac/cfg80211.c:4290` `linux/brcmfmac/fwil_types.h:85-93` `linux/brcmfmac/fwil_types.h:105` `linux/brcmfmac/fwil_types.h:133` `linux/brcmfmac/fwil_types.h:137`
- whd — get then set — reads the current mask and writes current OR requested (`whd_configure_wowl`) — `whd/src/whd_wifi_api.c:1001-1009`
- whd — callers of that helper: `WL_WOWL_KEYROT` (bit 14) in `whd_wifi_prepare_join` for chip id 43022; `WL_WOWL_MAGIC` (bit 0) in `whd_wifi_config_ulp_mode`; `WL_WOWL_ARPOFFLOAD` (bit 12) in `whd_arp_hostip_list_add` under `CYCFG_ULP_SUPPORT_ENABLED` — `whd/src/whd_wifi_api.c:1791-1814` `whd/src/whd_wifi_api.c:3851` `whd/src/whd_wifi_api.c:5674-5675` `whd/src/include/whd_wlioctl.h:3747-3754`
- whd — get — 4-byte request, reply passed through `dtoh32` into the caller's u32 (`whd_get_wowl_cap`; despite the function name it reads `wowl`, not `wowl_cap`) — `whd/src/whd_wifi_api.c:6622-6625` `whd/src/whd_wifi_api.c:5165-5179`
- whd — set — caller's u32 through `htod32` (`whd_set_wowl_cap`) — `whd/src/whd_wifi_api.c:6631-6634` `whd/src/whd_wifi_api.c:5153-5162`

### `wowl_activate`
| | |
|---|---|
| Used by | linux, whd; no `bsscfg:` prefix. Not found in embassy, c-driver |
| Direction | set |
| Value | u32 LE, 4 bytes |
| Record | plain integer; whd macro `IOVAR_STR_WOWL_ACTIVATE` `whd/src/include/whd_wlioctl.h:1170` `whd/src/include_helium/whd_wlioctl.h:1171` |

- linux — set — 1, right after writing `wowl`, before telling the bus about wake-on-WLAN — arm wake-on-WLAN at suspend — `linux/brcmfmac/cfg80211.c:4290-4292`
- whd — set — `WHD_TRUE`, after enabling the magic-packet bit and before setting `ulp`; only in ULP builds, for chip id 43022 or 43012, when the requested mode is DS1 or DS2 and the `ulp` value read back is 0 (`whd_wifi_config_ulp_mode`) — `whd/src/whd_wifi_api.c:3818-3832` `whd/src/whd_wifi_api.c:3837` `whd/src/whd_wifi_api.c:3847-3854`
- whd — set — caller's value (`whd_wowl_activate`); also called with 1 after a successful `wowl_activate_secure` — `whd/src/whd_wifi_api.c:6646-6649` `whd/src/whd_wifi_api.c:6759`

### `wowl_activate_secure`
| | |
|---|---|
| Used by | whd, no `bsscfg:` prefix. Not found in embassy, linux, c-driver |
| Direction | set |
| Value | `tls_param_info_t`, `sizeof(tls_param_info_t)` bytes, copied from the caller without byte-order conversion. 1360 bytes when `bool` is 1 byte and alignment is natural (inferred from the field list: 1359 bytes of fields rounded up to a multiple of 4, with `ProtocolVersion` = 4, `TLS_MAX_KEY_LENGTH` = 48, IV and MAC key 32, sequence 8, payload 1024, `IPV4_ADDR_LEN` = 4, `ETHER_ADDR_LEN` = 6 `whd/inc/whd_types.h:101` `whd/inc/whd_types.h:104` `whd/inc/whd_types.h:1481-1485` `whd/inc/whd_types.h:1526-1530`); the struct ends in a `bool`, so the size depends on the compiler |
| Record | `struct tls_param_info` `whd/inc/whd_types.h:1532-1567`, typedef `whd/inc/whd_types.h:150`; macro `IOVAR_STR_WOWL_ACTIVATE_SECURE` `whd/src/include/whd_wlioctl.h:1173` `whd/src/include_helium/whd_wlioctl.h:1174` |

- whd — set — the caller's TLS session parameters (protocol version, cipher and MAC selectors, keepalive interval, read/write keys, IVs, MAC keys and sequence numbers, TCP ack/seq, IPs, ports, MAC addresses, a payload of up to 1024 bytes); on success followed by `wowl_activate` = 1 — secure wake-on-WLAN (`whd_wowl_activate_secure`) — `whd/src/whd_wifi_api.c:6746-6760` `whd/inc/whd_types.h:1532-1567` `whd/inc/whd_types.h:1485`
- whd — the buffer pointer returned by `whd_proto_get_iovar_buffer` is not checked before the copy — `whd/src/whd_wifi_api.c:6753-6755`

### `wowl_arp_hostip`
| | |
|---|---|
| Used by | whd, no `bsscfg:` prefix, only under `CYCFG_ULP_SUPPORT_ENABLED`. Not found in embassy, linux, c-driver |
| Direction | set |
| Value | count x u32 IPv4 address, count * 4 bytes, passed as the caller's array (no conversion at this call site) |
| Record | no struct; macro `IOVAR_STR_WOWL_ARP_HOST_IP` `whd/src/include/whd_wlioctl.h:1180` `whd/src/include_helium/whd_wlioctl.h:1181` |

- whd — set — the host IPv4 list, after OR-ing `WL_WOWL_ARPOFFLOAD` into `wowl`; a failure is logged and the function goes on to set `arp_hostip` with the same list — ARP offload while in wake-on-WLAN (`whd_arp_hostip_list_add`) — `whd/src/whd_wifi_api.c:5674-5682`

### `wowl_cap`
| | |
|---|---|
| Used by | linux, no `bsscfg:` prefix. Not found in embassy, whd, c-driver; whd's `whd_get_wowl_cap` reads `wowl` instead `whd/src/whd_wifi_api.c:6625` |
| Direction | get |
| Value | u32 LE, 4 bytes, bit mask |
| Record | plain integer; bits use the `BRCMF_WOWL_*` names `linux/brcmfmac/fwil_types.h:105` `linux/brcmfmac/fwil_types.h:137` |

- linux — get — only when `BRCMF_FEAT_WOWL` was enabled; success sets `BRCMF_FEAT_WOWL_ARP_ND`; bit 27 (`BRCMF_WOWL_PFN_FOUND`) sets `BRCMF_FEAT_WOWL_ND`; bit 10 (`BRCMF_WOWL_GTK_FAILURE`) sets `BRCMF_FEAT_WOWL_GTK` — feature detection — `linux/brcmfmac/feature.c:311-321`

### `wowl_clear`
| | |
|---|---|
| Used by | linux, whd; no `bsscfg:` prefix. Not found in embassy, c-driver |
| Direction | set |
| Value | u32 LE, 4 bytes, value 0 in both drivers |
| Record | plain integer; whd macro `IOVAR_STR_WOWL_CLEAR` `whd/src/include/whd_wlioctl.h:1172` `whd/src/include_helium/whd_wlioctl.h:1173` |

- linux — set — 0, on resume when wake-on-WLAN was active, after reading `wowl_wakeind` and before `wowl_pattern` "clr" — `linux/brcmfmac/cfg80211.c:4220-4223`
- whd — set — 0 (`whd_wowl_clear`) — `whd/src/whd_wifi_api.c:6638-6642`

### `wowl_keepalive`
| | |
|---|---|
| Used by | defined, not used by whd. Not found in embassy, linux, c-driver |
| Direction | not shown by any driver |
| Value | payload not shown by any driver |
| Record | macro `IOVAR_STR_WOWL_KEEP_ALIVE` only `whd/src/include/whd_wlioctl.h:1176` `whd/src/include_helium/whd_wlioctl.h:1177` |

- whd — no `.c` file under `whd/` references `IOVAR_STR_WOWL_KEEP_ALIVE` — `whd/src/include/whd_wlioctl.h:1176`

### `wowl_os`
| | |
|---|---|
| Used by | whd, no `bsscfg:` prefix, only under `CYCFG_ULP_SUPPORT_ENABLED`. Not found in embassy, linux, c-driver |
| Direction | set |
| Value | u32 LE, 4 bytes |
| Record | plain integer; macro `IOVAR_STR_WOWL_OS` `whd/src/include/whd_wlioctl.h:1169` `whd/src/include_helium/whd_wlioctl.h:1170` |

- whd — set — the same mask just written to `wowl` (current OR requested) — `whd_configure_wowl` — `whd/src/whd_wifi_api.c:1007-1013`

### `wowl_pattern`
| | |
|---|---|
| Used by | linux, whd; no `bsscfg:` prefix. Not found in embassy, c-driver |
| Direction | linux: set. whd: both |
| Value | set: 4-byte command, 28-byte header of seven u32, mask bytes, pattern bytes = 32 + mask size + pattern size. linux writes the header little-endian; whd writes it in host order. whd get: reply read as `wl_wowl_pattern_list_t`, request buffer `WHD_PAYLOAD_MTU` bytes |
| Record | linux `struct brcmf_fil_wowl_pattern_le` { cmd[4], masksize, offset, patternoffset, patternsize, id, reasonsize, type } `linux/brcmfmac/fwil_types.h:738-750`. whd `wl_wowl_pattern_t` { masksize, offset, patternoffset, patternsize, id, reasonsize, type } `whd/src/include/whd_wlioctl.h:3770-3781` preceded by the command string; list `wl_wowl_pattern_list_t` { count, pattern[] } `whd/src/include/whd_wlioctl.h:3783-3787`; macro `IOVAR_STR_WOWL_PATTERN` `whd/src/include/whd_wlioctl.h:1177` `whd/src/include_helium/whd_wlioctl.h:1178` |

- linux — set "add" — cmd = "add" (4 bytes copied from the string, so the 4th is its NUL); masksize = (pattern length + 7) / 8; offset = packet offset; patternoffset = 28 + masksize (struct size minus the 4-byte cmd, plus masksize); patternsize; id and reasonsize left 0 by `kzalloc`; type = `BRCMF_WOWL_PATTERN_TYPE_BITMAP` (0); then mask, then pattern — one call per wake pattern at suspend — `linux/brcmfmac/cfg80211.c:4046-4078` `linux/brcmfmac/cfg80211.c:4260-4268` `linux/brcmfmac/fwil_types.h:212` `linux/brcmfmac/fwil_types.h:738-746`
- linux — set "clr" — cmd = "clr"; masksize, offset, patternsize, id, reasonsize, type all 0; patternoffset = 28 (the same formula with masksize 0); no mask or pattern; 32 bytes — remove all patterns on resume — `linux/brcmfmac/cfg80211.c:4223` `linux/brcmfmac/cfg80211.c:4057-4071`
- linux — limits it advertises: 16 patterns, 128 bytes per pattern — `linux/brcmfmac/fwil_types.h:143-144`
- whd — set — command "add", "del" or "clr" (anything else is rejected): 3 characters copied with `strncpy`, the pointer then advanced by 4, so this function does not write the 4th byte; then, except for "clr", `wl_wowl_pattern_t` with masksize, offset, patternoffset = 28 + mask size, patternsize, id = 0, reasonsize = 0, type = caller's type; then mask; then pattern. Length = 3 + 1 + 28 + mask size + pattern size. For "clr" the header area is allocated but not filled — `whd_set_wowl_pattern` — `whd/src/whd_wifi_api.c:6653-6715`
- whd — pattern type values: BITMAP 0, ARP 1, NA 2, SECWOWL 3 — `whd/src/include/whd_wlioctl.h:3763-3768`
- whd — get — request buffer of `WHD_PAYLOAD_MTU` (1500) bytes, not initialised and not NULL-checked; reply read as `wl_wowl_pattern_list_t`: count, then entries, each taken as header + mask + pattern; count and the size fields are used without `dtoh32`; whd sums the sizes of min(requested, count) entries and copies that many bytes from the first entry to the caller. The walk to the next entry adds the running byte total to a `wl_wowl_pattern_t *`, so it steps in units of 28 bytes, not bytes — `whd_get_wowl_pattern` — `whd/src/whd_wifi_api.c:6718-6744` `whd/inc/whd_types.h:242`

Differences: same 32-byte prefix layout in both. linux converts every header field to little-endian and zeroes the buffer; whd writes host-order fields and leaves the byte after the 3-character command, and the whole header for "clr", unwritten. For "clr" linux sends patternoffset = 28 in a zeroed header. linux only sends "add" and "clr" with type 0; whd also accepts "del" and a caller-chosen type. Only whd reads the variable. `linux/brcmfmac/cfg80211.c:4046-4078` `linux/brcmfmac/cfg80211.c:4223` `whd/src/whd_wifi_api.c:6653-6744`

### `wowl_secure_sess_info`
| | |
|---|---|
| Used by | whd, no `bsscfg:` prefix. Not found in embassy, linux, c-driver |
| Direction | get |
| Value | `struct secure_sess_info`, 24 bytes (4 + 4 + 8 + 8, with `TLS_MAX_SEQUENCE_LENGTH` = 8 `whd/inc/whd_types.h:1484`); copied to the caller without byte-order conversion |
| Record | `struct secure_sess_info` { u32 tcp_seq, u32 tcp_ack, u8 read_seq[8], u8 write_seq[8] } `whd/src/include/whd_wlioctl.h:4613-4618`, typedef `whd/inc/whd_types.h:151`; macro `IOVAR_STR_WOWL_SEC_SESS_INFO` `whd/src/include/whd_wlioctl.h:1174` `whd/src/include_helium/whd_wlioctl.h:1175` |

- whd — get — 24-byte request buffer (not initialised), reply copied whole to the caller — read the secure wake-on-WLAN TLS session state (`whd_wowl_get_secure_session_status`) — `whd/src/whd_wifi_api.c:6769-6786`

### `wowl_wakeind`
| | |
|---|---|
| Used by | linux, no `bsscfg:` prefix. Not found in embassy, whd, c-driver |
| Direction | both |
| Value | get: `struct brcmf_wowl_wakeind_le`, 8 bytes, two u32 LE. set: the same 8-byte buffer used as a string buffer |
| Record | `struct brcmf_wowl_wakeind_le` { pci_wakeind, ucode_wakeind } `linux/brcmfmac/fwil_types.h:882-885` |

- linux — get — reads the two wake indicators on resume to report the wake reason (`brcmf_report_wowl_wakeind`) — `linux/brcmfmac/cfg80211.c:4146-4147`
- linux — set — 8 bytes: 6 bytes copied into the struct (the 5 characters "clear" and a NUL), the last 2 bytes left as the uninitialised stack contents — clear the wake indication before arming (`brcmf_configure_wowl`) — `linux/brcmfmac/cfg80211.c:4245` `linux/brcmfmac/cfg80211.c:4287-4289`

### `wpa_auth`
| | |
|---|---|
| Used by | embassy as `bsscfg:wpa_auth` (AP only) `embassy/control.rs:595`; c-driver as `bsscfg:wpa_auth` (AP only) `c-driver/cyw43_ll.c:2418`; whd as `bsscfg:wpa_auth` `whd/src/whd_wifi_api.c:1796` `whd/src/whd_ap.c:447`; linux through the bsscfg helper: bare `wpa_auth` at bsscfg index 0, `bsscfg:wpa_auth` + u32 LE index otherwise `linux/brcmfmac/fwil.c:259-284` |
| Direction | embassy, c-driver, whd: set. linux: both |
| Value | with prefix: two u32, 8 bytes: bsscfg index, value. linux at index 0: one u32 LE, 4 bytes. embassy, c-driver, linux write little-endian; whd writes host order in one path and `htod32` in the other |
| Record | plain integer(s). Value bits: 0x0004 WPA PSK, 0x0080 WPA2 PSK, 0x40000 WPA3 SAE PSK in all four `embassy/consts.rs:743-745` `c-driver/cyw43_ll.c:272-274` `whd/src/include/whd_wlioctl.h:827` `whd/src/include/whd_wlioctl.h:831` `whd/src/include/whd_wlioctl.h:844` `linux/include/brcmu_wifi.h:217-234`; whd macro `IOVAR_STR_WPA_AUTH` `whd/src/include/whd_wlioctl.h:1139` `whd/src/include_helium/whd_wlioctl.h:1140` |

- embassy — set — index 0, value 0 (Open), 0x84 (Wpa2: WPA2 PSK + WPA PSK), 0x40000 (Wpa3), 0x40080 (Wpa2Wpa3) — AP key management in `start_ap` — `embassy/control.rs:548-557` `embassy/control.rs:595` `embassy/control.rs:695-700`
- embassy — the station path uses the `SetWpaAuth` command instead of this variable — `embassy/control.rs:381` `embassy/control.rs:435`
- c-driver — set — index `WWD_AP_INTERFACE` (1), value 0x0004 (WPA TKIP), 0x0084 (WPA2 AES or WPA2 mixed), 0x40000 (WPA3 SAE), 0x40080 (WPA3/WPA2); not sent for open auth; sent on interface `WWD_STA_INTERFACE` — AP auth mode — `c-driver/cyw43_ll.c:2403-2418` `c-driver/cyw43_ll.c:151-152` `c-driver/cyw43_ll.c:1546-1553`
- c-driver — the station path uses the `WLC_SET_WPA_AUTH` command instead — `c-driver/cyw43_ll.c:2280`
- whd — set — { bsscfg index, 0x0004 if `WHD_SECURITY_WPA_TKIP_PSK` else 0x0080 }, both in host order (no `htod32`); only for chip id 43022, in `whd_wifi_prepare_join` — `whd/src/whd_wifi_api.c:1791-1802`
- whd — set — { `htod32`(bsscfg index), value }: 0 for open (written without `htod32`), 0x40000 for WPA3 SAE, 0x40080 for WPA3/WPA2, 0x0004 for WPA TKIP, otherwise 0x0084; sent on the primary interface — AP start (`whd_wifi_init_ap`) — `whd/src/whd_ap.c:446-468` `whd/inc/whd_types.h:303`
- whd — the general station path uses the `WLC_SET_WPA_AUTH` command instead — `whd/src/whd_wifi_api.c:2049-2050`
- linux — set — WPA version for connect: 0x0006 (WPA PSK + unspecified) for WPA1; for WPA2 0x40000 when the firmware vendor is CYW and the first AKM is SAE, else 0x00c0 (WPA2 PSK + unspecified); 0x40000 for WPA3; 0 otherwise — `linux/brcmfmac/cfg80211.c:1967-1981` `linux/include/brcmu_wifi.h:217-234`
- linux — get — read back before refining by AKM suite — `linux/brcmfmac/cfg80211.c:2134-2135`
- linux — set — the AKM-refined value — `linux/brcmfmac/cfg80211.c:2277`
- linux — set — open security: 0x0001 (`WPA_AUTH_NONE`) in IBSS mode, else 0 — `linux/brcmfmac/cfg80211.c:4566-4570`
- linux — set — AP mode, value derived from the parsed RSN/WPA IE — `linux/brcmfmac/cfg80211.c:4834`
- linux — get — test bit 0x40000 before configuring SAE PWE — `linux/brcmfmac/cfg80211.c:5152-5153`

Differences: embassy sends the `bsscfg:` form with index 0; linux at index 0 sends the bare name with a 4-byte value and no index `linux/brcmfmac/fwil.c:259-260`. c-driver hard-codes index 1. whd writes the 8 bytes in host order in `whd_wifi_prepare_join` and through `htod32` in `whd_wifi_init_ap`. For WPA-TKIP-only AP, c-driver and whd send 0x0004; embassy has no such mode. Only linux reads the variable. `embassy/control.rs:595` `c-driver/cyw43_ll.c:2403-2418` `whd/src/whd_wifi_api.c:1791-1802` `whd/src/whd_ap.c:446-468`

### `wpaie`
| | |
|---|---|
| Used by | linux, plain (not through the bsscfg helper). Not found in embassy, whd, c-driver |
| Direction | set |
| Value | one raw WPA or RSN information element (2-byte header + body), variable length; or 0 bytes |
| Record | no struct; raw IE bytes |

- linux — set — the WPA or RSN IE found in the connect request's IEs, length = IE len field + header; NULL / 0 bytes if neither was found; sent only when the interface is the primary (non-P2P) one; return value ignored — `brcmf_cfg80211_connect` — `linux/brcmfmac/cfg80211.c:2446-2465`
- linux — set — NULL, 0 bytes — clear the user-space RSN IE before the SAE password is handed over (firmware-supplicant SAE path) — `linux/brcmfmac/cfg80211.c:2550-2554`

### `wsec`
| | |
|---|---|
| Used by | embassy as `bsscfg:wsec` (AP only) `embassy/control.rs:589`; c-driver as `bsscfg:wsec` (AP only) `c-driver/cyw43_ll.c:2392`; whd as `bsscfg:wsec` `whd/src/whd_wifi_api.c:1806` `whd/src/whd_ap.c:422`; linux both ways: plain `wsec` at one site `linux/brcmfmac/cfg80211.c:1853`, elsewhere through the bsscfg helper (bare name at bsscfg index 0, `bsscfg:wsec` + u32 LE index otherwise `linux/brcmfmac/fwil.c:259-284`) |
| Direction | embassy, c-driver, whd: set. linux: both |
| Value | with prefix: two u32, 8 bytes: bsscfg index, value. linux plain or at index 0: one u32 LE, 4 bytes. embassy, c-driver, linux write little-endian; whd host order in one path, `htod32` in the other |
| Record | plain integer(s). Cipher bits: 0x0001 WEP, 0x0002 TKIP, 0x0004 AES, 0x0040 SES_OW `linux/include/brcmu_wifi.h:206-211` `embassy/consts.rs:166` `whd/src/include/whd_wlioctl.h:815`; whd macro `IOVAR_STR_WSEC` `whd/src/include/whd_wlioctl.h:1138` `whd/src/include_helium/whd_wlioctl.h:1139` |

- embassy — set — index 0, value = security & 0xFF: 0 for Open, 4 (AES) for Wpa2, Wpa3 and Wpa2Wpa3 (the WPA2/WPA3 marker bits are above bit 7) — AP cipher in `start_ap` — `embassy/control.rs:589` `embassy/consts.rs:166-168` `embassy/consts.rs:244-249`
- embassy — the station path uses the `SetWsec` command instead — `embassy/control.rs:377` `embassy/control.rs:390`
- c-driver — set — index `WWD_AP_INTERFACE` (1), value = the full `auth` argument, not masked; sent on interface `WWD_STA_INTERFACE` — AP security type — `c-driver/cyw43_ll.c:2392` `c-driver/cyw43_ll.c:1546-1553`
- c-driver — the station path uses the `WLC_SET_WSEC` command with `auth_type & 0xff` instead — `c-driver/cyw43_ll.c:2236`
- whd — set — { bsscfg index, `auth_type & 0xFF` }, host order (no `htod32`); only for chip id 43022, in `whd_wifi_prepare_join` — `whd/src/whd_wifi_api.c:1791` `whd/src/whd_wifi_api.c:1804-1811`
- whd — set — { `htod32`(bsscfg index), `htod32`(value) }: `auth_type & 0xFF`, or, when `WPS_ENABLED` (0x10000000) is set, (auth_type without that bit) OR 0x0040; sent on the primary interface — AP start (`whd_wifi_init_ap`) — `whd/src/whd_ap.c:422-434` `whd/inc/whd_types.h:77` `whd/src/include/whd_wlioctl.h:815`
- whd — the general station path uses the `WLC_SET_WSEC` command with `auth_type & 0xFF` instead — `whd/src/whd_wifi_api.c:1766`
- linux — set (plain form, no bsscfg helper) — 0, or 0x0001 (WEP) when privacy is requested — IBSS join — `linux/brcmfmac/cfg80211.c:1850-1853`
- linux — set — pairwise OR group cipher bits — connect (`brcmf_set_wsec_mode`) — `linux/brcmfmac/cfg80211.c:2093-2094`
- linux — get — check for WEP before selecting the default key — `linux/brcmfmac/cfg80211.c:2784`
- linux — get then set — read, OR in the new key's cipher bit, write back — `brcmf_cfg80211_add_key` — `linux/brcmfmac/cfg80211.c:2948-2954`
- linux — get — report the cipher in use (`brcmf_cfg80211_get_key`) — `linux/brcmfmac/cfg80211.c:2989`
- linux — get then set — read, OR in 0x0001 (WEP), write back — `brcmf_cfg80211_reconfigure_wep` — `linux/brcmfmac/cfg80211.c:3063-3069`
- linux — set — 0 — open security — `linux/brcmfmac/cfg80211.c:4560`
- linux — set — AP-mode cipher bits from the parsed IE; a linux comment says this must precede `mfp` because the wsec command overwrites the MFP values — `linux/brcmfmac/cfg80211.c:4818` `linux/brcmfmac/cfg80211.c:4823-4825`
- linux — set — 0x0004 (AES) on the P2P device interface, so that P2P probe responses carry the privacy bit — `linux/brcmfmac/p2p.c:643-649` `linux/include/brcmu_wifi.h:208`

Differences: embassy and whd mask the value to the low 8 bits (whd except in the WPS case); c-driver sends the unmasked auth value. embassy sends the `bsscfg:` form with index 0; linux at index 0 sends the bare name with 4 bytes, and at one site always sends the plain form. c-driver hard-codes index 1. whd writes host order in `whd_wifi_prepare_join` and `htod32` in `whd_wifi_init_ap`. Only linux reads the variable. `embassy/control.rs:589` `c-driver/cyw43_ll.c:2392` `whd/src/whd_wifi_api.c:1804-1811` `whd/src/whd_ap.c:422-434` `linux/brcmfmac/cfg80211.c:1853` `linux/brcmfmac/fwil.c:259-284`

### `wsec_info`
| | |
|---|---|
| Used by | whd, no `bsscfg:` prefix. Not found in embassy, linux, c-driver |
| Direction | set |
| Value | 16 bytes: 4-byte header + one TLV (2-byte id, 2-byte length, 8 bytes of data). id and length through `htod16`; the two data words copied in host order |
| Record | `wl_wsec_info_t` { u8 version, u8 pad[2], u8 num_tlvs, tlvs[] } `whd/src/include/whd_wlioctl.h:93-98`; TLV `wl_wsec_info_tlv_t` { u16 type, u16 len, data[] } `whd/src/include/whd_wlioctl.h:86-90`, written through `whd_xtlv_t` { u16 id, u16 len, data[] } `whd/src/include/whd_wlioctl.h:450-455`; macro `IOVAR_STR_WSEC_INFO` `whd/src/include/whd_wlioctl.h:1271` `whd/src/include_helium/whd_wlioctl.h:1272` |

- whd — set — byte 0 version = 1 (`WL_WSEC_INFO_VERSION`); bytes 1-2 pad, not written; byte 3 num_tlvs incremented in place (the buffer is not zeroed first in this function); bytes 4-5 id = 0x0106 (`WL_WSEC_INFO_BSS_ALGOS`); bytes 6-7 len = 8; bytes 8-11 algos; bytes 12-15 mask (offsets inferred from the struct definitions) — `whd_set_wsec_info_algos` — `whd/src/whd_wifi_api.c:1693-1712` `whd/src/include/whd_wlioctl.h:103` `whd/src/include/whd_wlioctl.h:112-113`
- whd — values: algos = 1 << 16 (AES GCM256) for WPA3 enterprise and WPA3 192-bit enterprise, or 1 << 4 (AES CCM) for WPA3 enterprise AES-CCMP; mask = both bits in each case; sent from `whd_wifi_prepare_join` only when the firmware capability flag `WHD_FWCAP_GCMP` is set — `whd/src/whd_wifi_api.c:1768-1783` `whd/src/include/whd_wlioctl.h:101` `whd/src/include/whd_wlioctl.h:106` `whd/src/include/whd_wlioctl.h:747`

### `wsec_key`
| | |
|---|---|
| Used by | linux, through the bsscfg helper (bare name at bsscfg index 0, `bsscfg:wsec_key` + u32 LE index otherwise `linux/brcmfmac/fwil.c:259-284`). Not found in embassy, whd, c-driver |
| Direction | set |
| Value | `struct brcmf_wsec_key_le`, `sizeof` bytes, little-endian. 164 bytes with `WLAN_MAX_KEY_LEN` = 32 `linux-headers/ieee80211.h:2267` and `ETH_ALEN` = 6 (recalled, not in these sources); size computed from the field list (inferred, natural alignment) |
| Record | `struct brcmf_wsec_key_le` { index, len, data[`WLAN_MAX_KEY_LEN`], pad_1[18], algo, flags, pad_2[3], iv_initialized, pad_3, rxiv { u32 hi, u16 lo }, pad_4[2], ea[`ETH_ALEN`] } `linux/brcmfmac/fwil_types.h:558-575` |

- linux — set — index, len, algo, flags, rxiv.hi, rxiv.lo and iv_initialized converted to little-endian; key data and station address copied; the pad fields are not written by the conversion routine and the struct is an uninitialised local, so they carry stack contents — install or remove a key (`send_key_to_dongle`, the only sender; waits for pending 802.1X frames first) — `linux/brcmfmac/cfg80211.c:533-545` `linux/brcmfmac/cfg80211.c:548-559`
