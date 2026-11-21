# Commands

Every command number the four drivers define: names per driver, direction, who sends it, payload. Numbers 0-319 follow embassy's list; the last section holds numbers other drivers define that embassy's list lacks.

### 0 GetMagic
| | |
|---|---|
| Names | embassy `GetMagic` `embassy/consts.rs:448` / linux not defined / whd `WLC_GET_MAGIC` `whd/src/include/whd_wlioctl.h:1303` `whd/src/include_helium/whd_wlioctl.h:1303` / c-driver not defined |
| Direction | get (from the name only; no call site to check against) `embassy/consts.rs:448` |
| Sent by | no driver in these sources sends it. whd lists it only in its number-to-name debug table `whd/src/whd_utils.c:522` and in the macro `WL_SEQ_CMDS_GET_IOCTL_FILTER`, which is defined and never used `whd/src/include/whd_wlioctl.h:3677-3681` `whd/src/include_helium/whd_wlioctl.h:3836-3840` |
| Payload | not shown by any driver. whd defines `WLC_IOCTL_MAGIC` 0x14e46c77 next to the command list `whd/src/include/whd_wlioctl.h:1297`; no code in these sources compares a reply with it, so the link to this command is (inferred) from adjacency |

### 1 GetVersion
| | |
|---|---|
| Names | embassy `GetVersion` `embassy/consts.rs:449` / linux `BRCMF_C_GET_VERSION` `linux/brcmfmac/fwil.h:14` / whd `WLC_GET_VERSION` `whd/src/include/whd_wlioctl.h:1304` `whd/src/include_helium/whd_wlioctl.h:1304` / c-driver not defined |
| Direction | get `linux/brcmfmac/cfg80211.c:8576` |
| Sent by | linux `linux/brcmfmac/cfg80211.c:8576`. embassy, whd and c-driver do not send it; whd has it only in the debug name table `whd/src/whd_utils.c:523` and in the unused macro `WL_SEQ_CMDS_GET_IOCTL_FILTER` `whd/src/include/whd_wlioctl.h:3677-3681` `whd/src/include_helium/whd_wlioctl.h:3836-3840` |
| Payload | linux reads one u32, 4 bytes, little-endian `linux/brcmfmac/fwil.h:98-104`. linux treats the value as the D11 io type: 1 = `BRCMU_D11N_IOTYPE`, 2 = `BRCMU_D11AC_IOTYPE` `linux/include/brcmu_d11.h:10-11`. whd defines `WLC_IOCTL_VERSION` as 1 in `include/` and 2 in `include_helium/` `whd/src/include/whd_wlioctl.h:1298` `whd/src/include_helium/whd_wlioctl.h:1298` |

- linux — find the D11 io type before wiphy setup; the result is stored as a u8 in `cfg->d11inf.io_type` and selects the chanspec encode/decode routines — get, u32 LE, 4 bytes — `linux/brcmfmac/cfg80211.c:8576` `linux/brcmfmac/cfg80211.c:8581` `linux/brcmutil/d11.c:239`

### 2 Up
| | |
|---|---|
| Names | embassy `Up` `embassy/consts.rs:450` / linux `BRCMF_C_UP` `linux/brcmfmac/fwil.h:15` / whd `WLC_UP` `whd/src/include/whd_wlioctl.h:1305` `whd/src/include_helium/whd_wlioctl.h:1305` / c-driver `WLC_UP` `c-driver/cyw43_ll.c:167` |
| Direction | set `embassy/control.rs:344` `c-driver/cyw43_ll.c:2065` |
| Sent by | embassy, c-driver, whd, linux `embassy/control.rs:344` `c-driver/cyw43_ll.c:2065` `whd/src/whd_wifi_api.c:424` `linux/brcmfmac/p2p.c:462`. Also listed in the c-driver debug table `c-driver/cyw43_ll.c:865` and the whd debug name table `whd/src/whd_utils.c:524`; whd names it by raw number 2 in `whd_ioctl_info_to_string` `whd/src/whd_utils.c:1029-1031` |
| Payload | embassy, c-driver and whd send 0 bytes `embassy/control.rs:344` `c-driver/cyw43_ll.c:2065` `whd/src/whd_wifi_api.c:424`. linux sends one u32 LE, 4 bytes, because it uses `brcmf_fil_cmd_int_set` `linux/brcmfmac/fwil.h:87-93`; the value is 1 at four sites and 0 at one `linux/brcmfmac/p2p.c:462` `linux/brcmfmac/cfg80211.c:8017` |

- embassy — `up()`: set the interface up — 0 bytes, set, interface 0 — `embassy/control.rs:344`
- c-driver — end of WiFi init — NULL buffer, length 0, `SDPCM_SET`, STA interface — `c-driver/cyw43_ll.c:2065`
- whd — `whd_wifi_set_up` — NULL buffer, length 0 — `whd/src/whd_wifi_api.c:424`
- whd — bring the primary interface back up after turning APSTA off for AP mode — NULL buffer, length 0 — `whd/src/whd_ap.c:234`
- linux — P2P firmware setup: UP after DOWN and `apsta`=1 — u32 LE value 1, 4 bytes — `linux/brcmfmac/p2p.c:462`
- linux — start AP: bring up after configuration — u32 LE value 1, 4 bytes — `linux/brcmfmac/cfg80211.c:5400`
- linux — stop AP: bring the device back up — u32 LE value 1, 4 bytes — `linux/brcmfmac/cfg80211.c:5558`
- linux — `brcmf_config_dongle` — u32 LE value 0, 4 bytes — `linux/brcmfmac/cfg80211.c:8017` `linux/brcmfmac/cfg80211.c:8000`
- linux — survey dump (`brcmf_cfg80211_dump_survey`), after setting the channel and disabling mpc — u32 LE value 1, 4 bytes — `linux/brcmfmac/cfg80211.c:8408` `linux/brcmfmac/cfg80211.c:8364`

Differences: payload length is 0 bytes (embassy, c-driver, whd) against 4 bytes (linux) `embassy/control.rs:344` `c-driver/cyw43_ll.c:2065` `whd/src/whd_wifi_api.c:424` `linux/brcmfmac/fwil.h:87-93`. linux is not consistent about the value (0 or 1) `linux/brcmfmac/cfg80211.c:8017` `linux/brcmfmac/p2p.c:462`; that the value is ignored is (inferred), no source says so.

### 3 Down
| | |
|---|---|
| Names | embassy `Down` `embassy/consts.rs:451` / linux `BRCMF_C_DOWN` `linux/brcmfmac/fwil.h:16` / whd `WLC_DOWN` `whd/src/include/whd_wlioctl.h:1306` `whd/src/include_helium/whd_wlioctl.h:1306` / c-driver not defined |
| Direction | set `embassy/control.rs:349` |
| Sent by | embassy, whd, linux `embassy/control.rs:349` `whd/src/whd_wifi_api.c:479` `linux/brcmfmac/p2p.c:460`. c-driver has no define and no use. Also listed in the whd debug name table `whd/src/whd_utils.c:525` |
| Payload | embassy and whd send 0 bytes `embassy/control.rs:349` `whd/src/whd_wifi_api.c:479`. linux sends one u32 LE, 4 bytes, value 1 `linux/brcmfmac/p2p.c:460` |

- embassy — `down()`: set the interface down (used before changing `apsta` when starting an AP) — 0 bytes — `embassy/control.rs:349`
- whd — `whd_wifi_set_down` — NULL buffer, length 0 — `whd/src/whd_wifi_api.c:479`
- whd — set wlc down before turning the device off — NULL buffer, length 0 — `whd/src/whd_management.c:658`
- whd — down the primary interface before turning APSTA off for AP mode — NULL buffer, length 0 — `whd/src/whd_ap.c:224`
- linux — P2P firmware setup: DOWN before `apsta`=1 — u32 LE value 1, 4 bytes — `linux/brcmfmac/p2p.c:460`
- linux — start AP: DOWN before `apsta`=0; a linux comment says the firmware removes the WEP keys on DOWN, and linux reconfigures them afterwards — u32 LE value 1, 4 bytes — `linux/brcmfmac/cfg80211.c:5358` `linux/brcmfmac/cfg80211.c:5431-5434`
- linux — stop AP on an MBSS interface — u32 LE value 1, 4 bytes — `linux/brcmfmac/cfg80211.c:5534`
- linux — stop AP: DOWN after clearing the SSID — u32 LE value 1, 4 bytes — `linux/brcmfmac/cfg80211.c:5547`

Differences: payload length is 0 bytes (embassy, whd) against 4 bytes (linux) `embassy/control.rs:349` `whd/src/whd_wifi_api.c:479` `linux/brcmfmac/p2p.c:460`.

### 4 GetLoop
| | |
|---|---|
| Names | embassy `GetLoop` `embassy/consts.rs:452` / linux not defined / whd `WLC_GET_LOOP` `whd/src/include/whd_wlioctl.h:1307` `whd/src/include_helium/whd_wlioctl.h:1307` / c-driver not defined |
| Direction | get (from the name only) `embassy/consts.rs:452` |
| Sent by | no driver in these sources sends it; whd lists it only in its debug name table `whd/src/whd_utils.c:526` |
| Payload | not shown by any driver |

### 5 SetLoop
| | |
|---|---|
| Names | embassy `SetLoop` `embassy/consts.rs:453` / linux not defined / whd `WLC_SET_LOOP` `whd/src/include/whd_wlioctl.h:1308` `whd/src/include_helium/whd_wlioctl.h:1308` / c-driver not defined |
| Direction | set (from the name only) `embassy/consts.rs:453` |
| Sent by | no driver in these sources sends it; whd lists it only in its debug name table `whd/src/whd_utils.c:527` |
| Payload | not shown by any driver |

### 6 Dump
| | |
|---|---|
| Names | embassy `Dump` `embassy/consts.rs:454` / linux not defined / whd `WLC_DUMP` `whd/src/include/whd_wlioctl.h:1309` `whd/src/include_helium/whd_wlioctl.h:1309` / c-driver not defined |
| Direction | not found in these sources |
| Sent by | no driver in these sources sends it; whd lists it only in its debug name table `whd/src/whd_utils.c:528` |
| Payload | not shown by any driver |

### 7 GetMsglevel
| | |
|---|---|
| Names | embassy `GetMsglevel` `embassy/consts.rs:455` / linux not defined / whd `WLC_GET_MSGLEVEL` `whd/src/include/whd_wlioctl.h:1310` `whd/src/include_helium/whd_wlioctl.h:1310` / c-driver not defined |
| Direction | get (from the name only) `embassy/consts.rs:455` |
| Sent by | no driver in these sources sends it; whd lists it only in its debug name table `whd/src/whd_utils.c:529` |
| Payload | not shown by any driver |

### 8 SetMsglevel
| | |
|---|---|
| Names | embassy `SetMsglevel` `embassy/consts.rs:456` / linux not defined / whd `WLC_SET_MSGLEVEL` `whd/src/include/whd_wlioctl.h:1311` `whd/src/include_helium/whd_wlioctl.h:1311` / c-driver not defined |
| Direction | set (from the name only) `embassy/consts.rs:456` |
| Sent by | no driver in these sources sends it; whd lists it only in its debug name table `whd/src/whd_utils.c:530` |
| Payload | not shown by any driver |

### 9 GetPromisc
| | |
|---|---|
| Names | embassy `GetPromisc` `embassy/consts.rs:457` / linux not defined / whd `WLC_GET_PROMISC` `whd/src/include/whd_wlioctl.h:1312` `whd/src/include_helium/whd_wlioctl.h:1312` / c-driver not defined |
| Direction | get (from the name only) `embassy/consts.rs:457` |
| Sent by | no driver in these sources sends it; whd lists it only in its debug name table `whd/src/whd_utils.c:531` |
| Payload | not shown by any driver |

### 10 SetPromisc
| | |
|---|---|
| Names | embassy `SetPromisc` `embassy/consts.rs:458` / linux `BRCMF_C_SET_PROMISC` `linux/brcmfmac/fwil.h:17` / whd `WLC_SET_PROMISC` `whd/src/include/whd_wlioctl.h:1313` `whd/src/include_helium/whd_wlioctl.h:1313` / c-driver not defined |
| Direction | set `linux/brcmfmac/core.c:197` |
| Sent by | linux `linux/brcmfmac/core.c:197`. embassy, whd and c-driver do not send it; whd has it only in the debug name table `whd/src/whd_utils.c:532` |
| Payload | linux sends one u32 LE, 4 bytes: 1 for promiscuous on, 0 for off `linux/brcmfmac/core.c:196-197` |

- linux — multicast/rx-mode worker: apply the netdev `IFF_PROMISC` flag; error -EBADE is treated as "unsupported" and reported once, and a linux comment says the firmware of older chips does not support PROMISC — u32 LE, 4 bytes, value 1 or 0 — `linux/brcmfmac/core.c:197` `linux/brcmfmac/core.c:196` `linux/brcmfmac/core.c:199-201`

### 12 GetRate
| | |
|---|---|
| Names | embassy `GetRate` `embassy/consts.rs:459` / linux `BRCMF_C_GET_RATE` `linux/brcmfmac/fwil.h:18` / whd `WLC_GET_RATE` `whd/src/include/whd_wlioctl.h:1314` `whd/src/include_helium/whd_wlioctl.h:1314` / c-driver not defined |
| Direction | get `linux/brcmfmac/cfg80211.c:3143` |
| Sent by | linux `linux/brcmfmac/cfg80211.c:3143`. embassy, whd and c-driver do not send it; whd has it only in the debug name table `whd/src/whd_utils.c:533` |
| Payload | linux reads one u32 LE, 4 bytes, and uses it as the current tx rate `linux/brcmfmac/cfg80211.c:3143`. linux multiplies it by 5 to fill cfg80211's `txrate.legacy` `linux/brcmfmac/cfg80211.c:3149`; a unit of 500 kbit/s is (inferred) from that multiplication, no source states the unit |

- linux — station info in IBSS mode only (`brcmf_cfg80211_get_station_ibss`, reached when `brcmf_is_ibssmode`) — get, u32 LE, 4 bytes — `linux/brcmfmac/cfg80211.c:3143` `linux/brcmfmac/cfg80211.c:3132` `linux/brcmfmac/cfg80211.c:3202-3203`

### 14 GetInstance
| | |
|---|---|
| Names | embassy `GetInstance` `embassy/consts.rs:460` / linux not defined / whd `WLC_GET_INSTANCE` `whd/src/include/whd_wlioctl.h:1315` `whd/src/include_helium/whd_wlioctl.h:1315` / c-driver not defined |
| Direction | get (from the name only) `embassy/consts.rs:460` |
| Sent by | no driver in these sources sends it. whd lists it in its debug name table `whd/src/whd_utils.c:534`, in the unused macro `WL_SEQ_CMDS_GET_IOCTL_FILTER` `whd/src/include/whd_wlioctl.h:3677-3681` `whd/src/include_helium/whd_wlioctl.h:3836-3840`, and derives `OID_WL_GETINSTANCE` = `WL_OID_BASE` (0xFFE41420) + `WLC_GET_INSTANCE`, also never used `whd/src/include/whd_wlioctl.h:1589-1590` `whd/src/include_helium/whd_wlioctl.h:1589-1590` |
| Payload | not shown by any driver |

### 19 GetInfra
| | |
|---|---|
| Names | embassy `GetInfra` `embassy/consts.rs:461` / linux `BRCMF_C_GET_INFRA` `linux/brcmfmac/fwil.h:19` / whd `WLC_GET_INFRA` `whd/src/include/whd_wlioctl.h:1316` `whd/src/include_helium/whd_wlioctl.h:1316` / c-driver not defined |
| Direction | get (from the name only) `embassy/consts.rs:461` |
| Sent by | no driver in these sources sends it. linux defines it with no call site `linux/brcmfmac/fwil.h:19`; whd lists it only in its debug name table `whd/src/whd_utils.c:535` |
| Payload | not shown by any driver. A u32 mirroring 20 SetInfra is (inferred), not shown `linux/brcmfmac/cfg80211.c:1423` |

### 20 SetInfra
| | |
|---|---|
| Names | embassy `SetInfra` `embassy/consts.rs:462` / linux `BRCMF_C_SET_INFRA` `linux/brcmfmac/fwil.h:20` / whd `WLC_SET_INFRA` `whd/src/include/whd_wlioctl.h:1317` `whd/src/include_helium/whd_wlioctl.h:1317` / c-driver `WLC_SET_INFRA` `c-driver/cyw43_ll.c:168` |
| Direction | set `embassy/control.rs:748-751` `c-driver/cyw43_ll.c:1956-1959` |
| Sent by | embassy, c-driver, whd, linux `embassy/control.rs:379` `c-driver/cyw43_ll.c:2271` `whd/src/whd_wifi_api.c:1910` `linux/brcmfmac/cfg80211.c:1423`. Also listed in the c-driver debug table `c-driver/cyw43_ll.c:866` and the whd debug name table `whd/src/whd_utils.c:536`; whd names it by raw number 20 `whd/src/whd_utils.c:1033-1035` |
| Payload | all four send one u32 LE, 4 bytes. whd and linux send 1 for an infrastructure BSS and 0 for IBSS/ad-hoc `whd/src/whd_wifi_api.c:1910` `linux/brcmfmac/cfg80211.c:1399-1404` `linux/brcmfmac/cfg80211.c:1423`; embassy and c-driver only ever send 1 `embassy/control.rs:379` `c-driver/cyw43_ll.c:2271` |

- embassy — join, open network: infrastructure mode on — u32 LE value 1, 4 bytes (`ioctl_set_u32`) — `embassy/control.rs:379` `embassy/control.rs:748-751`
- embassy — join, secured network: infrastructure mode on — u32 LE value 1, 4 bytes — `embassy/control.rs:432`
- c-driver — join: set infrastructure mode — u32 LE value 1, 4 bytes (`cyw43_set_ioctl_u32`) — `c-driver/cyw43_ll.c:2271` `c-driver/cyw43_ll.c:1956-1959`
- whd — prepare join: 1, or 0 when the auth type has `IBSS_ENABLED` — u32 (htod32), 4 bytes (`whd_wifi_set_ioctl_value`) — `whd/src/whd_wifi_api.c:1910` `whd/src/whd_wifi_api.c:5048-5062`
- linux — change interface type: 0 for ADHOC, 1 for station — u32 LE, 4 bytes — `linux/brcmfmac/cfg80211.c:1423` `linux/brcmfmac/cfg80211.c:1399-1404`
- linux — start AP: set infra 1 — u32 LE value 1, 4 bytes — `linux/brcmfmac/cfg80211.c:5367`

### 21 GetAuth
| | |
|---|---|
| Names | embassy `GetAuth` `embassy/consts.rs:463` / linux `BRCMF_C_GET_AUTH` `linux/brcmfmac/fwil.h:21` / whd `WLC_GET_AUTH` `whd/src/include/whd_wlioctl.h:1318` `whd/src/include_helium/whd_wlioctl.h:1318` / c-driver not defined |
| Direction | get `whd/src/whd_wifi_api.c:3744` |
| Sent by | whd `whd/src/whd_wifi_api.c:3744`. linux defines it with no call site `linux/brcmfmac/fwil.h:21`; embassy and c-driver do not send it. Also listed in the whd debug name table `whd/src/whd_utils.c:537` |
| Payload | whd reads one u32 LE (dtoh32), 4 bytes `whd/src/whd_wifi_api.c:5068-5088`, and compares it with `SHARED_AUTH` = 1 `whd/src/whd_wifi_api.c:3746` `whd/src/include/whd_wlioctl.h:801` |

- whd — get security: for WEP, read the auth setting to tell shared-key from open — get, u32, 4 bytes (`whd_wifi_get_ioctl_value`) — `whd/src/whd_wifi_api.c:3744`

### 22 SetAuth
| | |
|---|---|
| Names | embassy `SetAuth` `embassy/consts.rs:464` / linux `BRCMF_C_SET_AUTH` `linux/brcmfmac/fwil.h:22` / whd `WLC_SET_AUTH` `whd/src/include/whd_wlioctl.h:1319` `whd/src/include_helium/whd_wlioctl.h:1319` / c-driver `WLC_SET_AUTH` `c-driver/cyw43_ll.c:169` |
| Direction | set `embassy/control.rs:748-751` `c-driver/cyw43_ll.c:1956-1959` |
| Sent by | embassy, c-driver, whd `embassy/control.rs:380` `c-driver/cyw43_ll.c:2275` `whd/src/whd_wifi_api.c:1921`. linux defines it with no call site `linux/brcmfmac/fwil.h:22`. Also listed in the c-driver debug table `c-driver/cyw43_ll.c:867` and the whd debug name table `whd/src/whd_utils.c:538`; whd names it by raw number 22 `whd/src/whd_utils.c:1037-1039` |
| Payload | one u32 LE, 4 bytes, the 802.11 authentication type. Values defined by the drivers: 0 open system, 1 shared key, 2 open then shared (whd only), 3 SAE `whd/src/include/whd_wlioctl.h:4273-4276` `embassy/consts.rs:735-736` `c-driver/cyw43_ll.c:263-264` |

- embassy — join, open network: auth 0 (open) — u32 LE value 0, 4 bytes — `embassy/control.rs:380`
- embassy — join, secured: `AUTH_OPEN` (0) for WPA/WPA2, `AUTH_SAE` (3) for WPA3 and WPA2/WPA3 — u32 LE, 4 bytes — `embassy/control.rs:433` `embassy/control.rs:400-403`
- embassy — start AP: `AUTH_OPEN` — u32 LE value 0, 4 bytes — `embassy/control.rs:569`
- c-driver — join: `AUTH_TYPE_SAE` (3) when wpa_auth is WPA3 SAE, else `AUTH_TYPE_OPEN` (0) — u32 LE, 4 bytes — `c-driver/cyw43_ll.c:2275`
- whd — prepare join: `WL_AUTH_SAE` for WPA3 security types, else `WL_AUTH_OPEN_SYSTEM` — u32 (htod32), 4 bytes — `whd/src/whd_wifi_api.c:1921`

Differences: embassy, c-driver and whd send this command; linux does not, and sets the per-BSS named variable (iovar) `auth` instead `linux/brcmfmac/cfg80211.c:2020` `linux/brcmfmac/cfg80211.c:2347` `linux/brcmfmac/cfg80211.c:4554` `linux/brcmfmac/cfg80211.c:4812`.

### 23 GetBssid
| | |
|---|---|
| Names | embassy `GetBssid` `embassy/consts.rs:465` / linux `BRCMF_C_GET_BSSID` `linux/brcmfmac/fwil.h:23` / whd `WLC_GET_BSSID` `whd/src/include/whd_wlioctl.h:1320` `whd/src/include_helium/whd_wlioctl.h:1320` / c-driver `WLC_GET_BSSID` `c-driver/cyw43_ll.c:170` |
| Direction | get `c-driver/cyw43_ll.c:2347` |
| Sent by | c-driver, whd, linux `c-driver/cyw43_ll.c:2347` `whd/src/whd_wifi_api.c:3621` `linux/brcmfmac/p2p.c:1494-1495`. embassy defines it and never sends it `embassy/consts.rs:465`. Also listed in the c-driver debug table `c-driver/cyw43_ll.c:868` and the whd debug name table `whd/src/whd_utils.c:539` |
| Payload | all three read 6 bytes, a raw MAC address with no length prefix `c-driver/cyw43_ll.c:2347` `whd/src/whd_wifi_api.c:3619` `linux/brcmfmac/p2p.c:1494-1495` |

- c-driver — `cyw43_ll_wifi_get_bssid`: read the BSSID of the STA interface — 6 bytes, `SDPCM_GET` — `c-driver/cyw43_ll.c:2347`
- whd — `whd_wifi_get_bssid`, STA or AP role — `whd_mac_t`, 6 bytes — `whd/src/whd_wifi_api.c:3621` `whd/src/whd_wifi_api.c:3619`
- linux — fill the BSSID field of a received action frame passed to cfg80211 — 6 bytes (`ETH_ALEN`) read straight into `mgmt_frame->bssid` — `linux/brcmfmac/p2p.c:1494-1495`
- linux — P2P: a zero return is taken as "associated", and linux then fetches the bss info for the channel; that the command fails when not associated is (inferred) from that use — 6 bytes (`ETH_ALEN`) — `linux/brcmfmac/p2p.c:2040-2041` `linux/brcmfmac/p2p.c:2040`
- linux — fill the BSSID field of a received external-auth management frame — 6 bytes (`ETH_ALEN`) — `linux/brcmfmac/cyw/core.c:316-317`

### 24 SetBssid
| | |
|---|---|
| Names | embassy `SetBssid` `embassy/consts.rs:466` / linux not defined / whd `WLC_SET_BSSID` `whd/src/include/whd_wlioctl.h:1321` `whd/src/include_helium/whd_wlioctl.h:1321` / c-driver not defined |
| Direction | set (from the name only) `embassy/consts.rs:466` |
| Sent by | no driver in these sources sends it; whd lists it only in its debug name table `whd/src/whd_utils.c:540` |
| Payload | not shown by any driver. A 6-byte MAC, mirroring 23 GetBssid, is (inferred), not shown `c-driver/cyw43_ll.c:2347` |

### 25 GetSsid
| | |
|---|---|
| Names | embassy `GetSsid` `embassy/consts.rs:467` / linux `BRCMF_C_GET_SSID` `linux/brcmfmac/fwil.h:24` / whd `WLC_GET_SSID` `whd/src/include/whd_wlioctl.h:1322` `whd/src/include_helium/whd_wlioctl.h:1322` / c-driver `WLC_GET_SSID` `c-driver/cyw43_ll.c:171` and the public `CYW43_IOCTL_GET_SSID` = 0x32 `c-driver/cyw43_ll.h:31` |
| Direction | get (from the name only) `embassy/consts.rs:467` |
| Sent by | no driver in these sources sends it. linux defines it with no call site `linux/brcmfmac/fwil.h:24`; it appears in the debug tables `c-driver/cyw43_ll.c:869` `whd/src/whd_utils.c:541`. c-driver exports `CYW43_IOCTL_GET_SSID` (0x32) for applications to pass to `cyw43_ioctl` `c-driver/cyw43_ll.h:29-31`; `cyw43_ll_ioctl` decodes that public form as command = value >> 1, with bit 0 selecting set, so 0x32 is a get of command 25 `c-driver/cyw43_ll.c:1327-1329`; nothing inside c-driver calls it |
| Payload | not shown by any driver. That the reply has the 36-byte layout of 26 SetSsid (u32 LE length + 32 bytes SSID `embassy/structs.rs:400-403`) is (recalled, not in these sources) |

### 26 SetSsid
| | |
|---|---|
| Names | embassy `SetSsid` `embassy/consts.rs:468` / linux `BRCMF_C_SET_SSID` `linux/brcmfmac/fwil.h:25` / whd `WLC_SET_SSID` `whd/src/include/whd_wlioctl.h:1323` `whd/src/include_helium/whd_wlioctl.h:1323` / c-driver `WLC_SET_SSID` `c-driver/cyw43_ll.c:172` |
| Direction | set `embassy/control.rs:469` `c-driver/cyw43_ll.c:2329` |
| Sent by | embassy, c-driver, whd, linux `embassy/control.rs:469` `c-driver/cyw43_ll.c:2329` `whd/src/whd_wifi_api.c:2483` `linux/brcmfmac/cfg80211.c:1921-1922`. Also listed in the c-driver debug table `c-driver/cyw43_ll.c:870` and the whd debug name table `whd/src/whd_utils.c:542`; whd names it by raw number 26 `whd/src/whd_utils.c:1041-1043` |
| Payload | every driver starts with 36 bytes: offset 0 u32 LE SSID length, offset 4 SSID, 32 bytes `embassy/structs.rs:400-403` `whd/src/include/whd_wlioctl.h:496-500` `linux/brcmfmac/fwil_types.h:357-360`. whd and linux optionally append association parameters: BSSID (6 bytes), a chanspec count (u32) and a chanspec list (u16 each); the two layouts differ, see Differences `whd/src/include/whd_wlioctl.h:4239-4255` `linux/brcmfmac/fwil_types.h:482-490` `linux/brcmfmac/fwil_types.h:509-512` |

- embassy — join: the command that starts the join; afterwards embassy waits for the `SET_SSID` event (open network) or `PSK_SUP` (secured); a unit-test helper also matches `Ioctl::SetSsid` in a mocked join, which is not a transmission — `SsidInfo { len: u32, ssid: [u8; 32] }`, 36 bytes — `embassy/control.rs:469` `embassy/structs.rs:400-403` `embassy/control.rs:438-442` `embassy/control.rs:464-490` `embassy/control.rs:964`
- c-driver — join by SSID only (with a BSSID it uses the named variable `join` instead) — 36 bytes: u32 LE ssid_len + 32 bytes SSID, from `last_ssid_joined[36]` — `c-driver/cyw43_ll.c:2329` `c-driver/cyw43_internal.h:37` `c-driver/cyw43_ll.c:2296-2297` `c-driver/cyw43_ll.c:2325`
- c-driver — `cyw43_ll_wifi_rejoin`: resend the last SSID — 36 bytes, same buffer — `c-driver/cyw43_ll.c:2342`
- whd — join a specific AP: fallback when the named variable `join` is unsupported — `wl_join_params_t`, 50 bytes: `wlc_ssid_t` (36) + `wl_assoc_params` (bssid 6, bssid_cnt u16, chanspec_num u32, chanspec_list[1] u16), packed with `#pragma pack(1)`. bssid is copied from the AP record; bssid_cnt is 0; chanspec_num is 1 with one chanspec only if the AP channel is known. `SSID_len` and `chanspec_num` are stored without htod32 on this path — `whd/src/whd_wifi_api.c:2386` `whd/src/whd_wifi_api.c:2373` `whd/src/include/whd_wlioctl.h:4239-4255` `whd/src/include/whd_wlioctl.h:4188` `whd/src/whd_wifi_api.c:2379-2385` `whd/src/whd_wifi_api.c:2350` `whd/src/whd_wifi_api.c:2377`
- whd — `whd_wifi_join` by SSID — `wlc_ssid_t { uint32_t SSID_len; uint8_t SSID[32]; }`, 36 bytes, `SSID_len` htod32 — `whd/src/whd_wifi_api.c:2483` `whd/src/whd_wifi_api.c:2478-2481` `whd/src/include/whd_wlioctl.h:496-500`
- linux — join IBSS — `struct brcmf_join_params`; the length passed starts at 36 (`sizeof(ssid_le)`), adds 14 (`BRCMF_ASSOC_PARAMS_FIXED_SIZE`) when a BSSID is given, and adds 16 (`sizeof(params_le)`) when the channel is fixed: 36, 50, 52 or 66 (computed); 66 is more than the 52-byte struct it points at — `linux/brcmfmac/cfg80211.c:1921-1922` `linux/brcmfmac/cfg80211.c:1878` `linux/brcmfmac/cfg80211.c:1881-1883` `linux/brcmfmac/cfg80211.c:102-103` `linux/brcmfmac/cfg80211.c:1897-1904`
- linux — connect: fallback join when the path through the named variable `join` is not taken — 36 bytes, or 52 when a channel is known — `linux/brcmfmac/cfg80211.c:2646-2647` `linux/brcmfmac/cfg80211.c:2631` `linux/brcmfmac/cfg80211.c:2641-2644`
- linux — start AP ("create softap") — full `struct brcmf_join_params`, 52 bytes, SSID filled, rest zero — `linux/brcmfmac/cfg80211.c:5440` `linux/brcmfmac/cfg80211.c:5436-5441`
- linux — stop AP — full `struct brcmf_join_params`, 52 bytes, all zero (empty SSID) — `linux/brcmfmac/cfg80211.c:5542-5544`

Differences: embassy and c-driver always send 36 bytes `embassy/control.rs:469` `c-driver/cyw43_ll.c:2329`. whd sends 36 or 50 `whd/src/whd_wifi_api.c:2478` `whd/src/whd_wifi_api.c:2373`. linux sends 36 or 52, and its IBSS join can also pass 50 or 66 `linux/brcmfmac/cfg80211.c:1878` `linux/brcmfmac/cfg80211.c:1883` `linux/brcmfmac/cfg80211.c:1904`. The optional tail is laid out differently: whd's `wl_assoc_params` is packed and has a u16 `bssid_cnt` after the BSSID, 14 bytes `whd/src/include/whd_wlioctl.h:4239-4255`; linux's `brcmf_assoc_params_le` has no `bssid_cnt` and is not packed (bssid[6], `__le32 chanspec_num`, `__le16 chanspec_list[1]`), 16 bytes with natural alignment, the last 2 being struct padding `linux/brcmfmac/fwil_types.h:482-490`. In both, `chanspec_num` is at tail offset 8 and `chanspec_list` at tail offset 12. The sizes 14, 50, 16, 52 and 66 are (computed) from the field lists; no source line states them. whd's `chanspec_t` is a uint16_t `whd/src/include/whd_wlioctl.h:48`. linux sizes the SSID array with `IEEE80211_MAX_SSID_LEN` `linux/brcmfmac/fwil_types.h:359`, defined as 32 `linux-headers/ieee80211.h:227`. A whd comment says some firmware (it names the 4390) does not support the named variable `join`, hence the fallback to this command `whd/src/whd_wifi_api.c:2369`.

### 27 Restart
| | |
|---|---|
| Names | embassy `Restart` `embassy/consts.rs:469` / linux not defined / whd `WLC_RESTART` `whd/src/include/whd_wlioctl.h:1324` `whd/src/include_helium/whd_wlioctl.h:1324` / c-driver not defined |
| Direction | not found in these sources |
| Sent by | no driver in these sources sends it; whd lists it only in its debug name table `whd/src/whd_utils.c:543` |
| Payload | not shown by any driver |

### 29 GetChannel
| | |
|---|---|
| Names | embassy `GetChannel` `embassy/consts.rs:470` / linux `BRCMF_C_GET_CHANNEL` `linux/brcmfmac/fwil.h:27` / whd `WLC_GET_CHANNEL` `whd/src/include/whd_wlioctl.h:1325` `whd/src/include_helium/whd_wlioctl.h:1325` / c-driver has no `WLC_` define, only the public `CYW43_IOCTL_GET_CHANNEL` = 0x3a `c-driver/cyw43_ll.h:32` |
| Direction | get `whd/src/whd_wifi_api.c:679` |
| Sent by | whd, linux `whd/src/whd_wifi_api.c:679` `linux/brcmfmac/cfg80211.c:5746-5748`. embassy defines it and never sends it `embassy/consts.rs:470`. c-driver exports the public value for applications and does not call it itself `c-driver/cyw43_ll.h:32` `c-driver/cyw43_ll.c:1327-1329`. Also listed in the whd debug name table `whd/src/whd_utils.c:544` |
| Payload | whd expects `channel_info_t`, 12 bytes: offset 0 int32 hw_channel, offset 4 int32 target_channel, offset 8 int32 scan_channel `whd/src/include/whd_wlioctl.h:978-983`. linux asks for 4 bytes at one site and 2 bytes at another and uses them as the hw channel `linux/brcmfmac/cfg80211.c:5684` `linux/brcmfmac/cfg80211.c:5746-5748` `linux/brcmfmac/cyw/core.c:114` `linux/brcmfmac/cyw/core.c:146-147` |

- whd — `whd_wifi_get_channel`: returns hw_channel — `channel_info_t`, 12 bytes; hw_channel is read without a byte swap — `whd/src/whd_wifi_api.c:679` `whd/src/whd_wifi_api.c:677` `whd/src/whd_wifi_api.c:683`
- linux — mgmt tx (action frame) with no channel given: get the current hw channel — `__le32 hw_ch`, 4 bytes — `linux/brcmfmac/cfg80211.c:5746-5748` `linux/brcmfmac/cfg80211.c:5684`
- linux — Cypress external-auth mgmt frame tx with no channel given — `__le16 hw_ch`, 2 bytes — `linux/brcmfmac/cyw/core.c:146-147` `linux/brcmfmac/cyw/core.c:114`

Differences: the requested length is 12 bytes (whd), 4 bytes (linux `cfg80211.c`) and 2 bytes (linux `cyw/core.c`) `whd/src/whd_wifi_api.c:677-679` `linux/brcmfmac/cfg80211.c:5746-5748` `linux/brcmfmac/cyw/core.c:146-147`. All three use the start of the reply as the current channel. That a short buffer returns a prefix of the 12-byte record is (inferred) from the linux call sites, not stated.

### 30 SetChannel
| | |
|---|---|
| Names | embassy `SetChannel` `embassy/consts.rs:471` / linux `BRCMF_C_SET_CHANNEL` `linux/brcmfmac/fwil.h:28` / whd `WLC_SET_CHANNEL` `whd/src/include/whd_wlioctl.h:1326` `whd/src/include_helium/whd_wlioctl.h:1326` / c-driver `WLC_SET_CHANNEL` `c-driver/cyw43_ll.c:173` |
| Direction | set (embassy, c-driver, linux); whd sends it with the get flag `embassy/control.rs:586` `c-driver/cyw43_ll.c:2389` `linux/brcmfmac/cfg80211.c:1909-1910` `whd/src/whd_wifi_api.c:633` |
| Sent by | embassy, c-driver, whd, linux `embassy/control.rs:586` `c-driver/cyw43_ll.c:2389` `whd/src/whd_wifi_api.c:633` `linux/brcmfmac/cfg80211.c:1909-1910`. Also listed in the c-driver debug table `c-driver/cyw43_ll.c:871` and the whd debug name table `whd/src/whd_utils.c:545` |
| Payload | all four send one u32 LE, 4 bytes, a plain channel number (not a chanspec) `embassy/control.rs:586` `c-driver/cyw43_ll.c:2389` `whd/src/whd_wifi_api.c:630-633` `linux/brcmfmac/cfg80211.c:1909-1910` |

- embassy — start AP: set the channel number — u32 LE, 4 bytes, set — `embassy/control.rs:586`
- c-driver — AP init: set the channel — u32 LE, 4 bytes, `SDPCM_SET` — `c-driver/cyw43_ll.c:2389`
- whd — `whd_wifi_set_channel`, STA role (the AP role uses the named variable `csa` instead) — uint32 (htod32), 4 bytes, sent through `whd_proto_get_ioctl` — `whd/src/whd_wifi_api.c:633` `whd/src/whd_wifi_api.c:630-632` `whd/src/whd_wifi_api.c:637-649`
- linux — join IBSS with a given channel ("set channel for starter") — u32 LE, 4 bytes, set — `linux/brcmfmac/cfg80211.c:1909-1910`

Differences: payload is the same in all four. The direction flag differs: whd sends the command with `whd_proto_get_ioctl`, which for CDC/BDC is `whd_cdc_get_ioctl` and passes `CDC_GET` = 0x00 `whd/src/whd_wifi_api.c:633` `whd/src/whd_cdc_bdc.c:118-122` `whd/src/whd_cdc_bdc.c:597` `whd/src/include/whd_cdc_bdc.h:64`; whd's msgbuf protocol installs a different `get_ioctl`, not examined here `whd/src/whd_msgbuf_txrx.c:2259`. embassy, c-driver and linux send it as a set. The sources do not say whether this is a whd defect or whether both flags are accepted.

### 31 GetSrl
| | |
|---|---|
| Names | embassy `GetSrl` `embassy/consts.rs:472` / linux `BRCMF_C_GET_SRL` `linux/brcmfmac/fwil.h:29` / whd `WLC_GET_SRL` `whd/src/include/whd_wlioctl.h:1327` `whd/src/whd_utils.c:546` / c-driver not defined |
| Direction | get |
| Sent by | no driver in these sources sends it |
| Payload | Not shown by any driver. One little-endian u32 retry count by symmetry with 32 (inferred). |

### 32 SetSrl
| | |
|---|---|
| Names | embassy `SetSrl` `embassy/consts.rs:473` / linux `BRCMF_C_SET_SRL` `linux/brcmfmac/fwil.h:30` / whd `WLC_SET_SRL` `whd/src/include/whd_wlioctl.h:1328` `whd/src/whd_utils.c:547` / c-driver not defined |
| Direction | set |
| Sent by | linux `linux/brcmfmac/cfg80211.c:1633` |
| Payload | One u32, little-endian, 4 bytes: the short retry limit. `linux/brcmfmac/cfg80211.c:1633` `linux/brcmfmac/fwil.h:87-93` |

- linux — `brcmf_set_retry` with l=false: short retry limit from `wiphy->retry_short` — u32 count as one `__le32`, 4 bytes — `linux/brcmfmac/cfg80211.c:1633` `linux/brcmfmac/cfg80211.c:1631` `linux/brcmfmac/cfg80211.c:1677` `linux/brcmfmac/fwil.h:87-93`

### 33 GetLrl
| | |
|---|---|
| Names | embassy `GetLrl` `embassy/consts.rs:474` / linux `BRCMF_C_GET_LRL` `linux/brcmfmac/fwil.h:31` / whd `WLC_GET_LRL` `whd/src/include/whd_wlioctl.h:1329` `whd/src/whd_utils.c:548` / c-driver not defined |
| Direction | get |
| Sent by | no driver in these sources sends it |
| Payload | Not shown by any driver. One little-endian u32 by symmetry with 34 (inferred). |

### 34 SetLrl
| | |
|---|---|
| Names | embassy `SetLrl` `embassy/consts.rs:475` / linux `BRCMF_C_SET_LRL` `linux/brcmfmac/fwil.h:32` / whd `WLC_SET_LRL` `whd/src/include/whd_wlioctl.h:1330` `whd/src/whd_utils.c:549` / c-driver not defined |
| Direction | set |
| Sent by | linux `linux/brcmfmac/cfg80211.c:1633` |
| Payload | One u32, little-endian, 4 bytes: the long retry limit. `linux/brcmfmac/cfg80211.c:1633` `linux/brcmfmac/fwil.h:87-93` |

- linux — `brcmf_set_retry` with l=true: long retry limit from `wiphy->retry_long` — u32 count as one `__le32`, 4 bytes — `linux/brcmfmac/cfg80211.c:1633` `linux/brcmfmac/cfg80211.c:1631` `linux/brcmfmac/cfg80211.c:1670` `linux/brcmfmac/fwil.h:87-93`

### 35 GetPlcphdr
| | |
|---|---|
| Names | embassy `GetPlcphdr` `embassy/consts.rs:476` / linux not defined / whd `WLC_GET_PLCPHDR` `whd/src/include/whd_wlioctl.h:1331` `whd/src/whd_utils.c:550` / c-driver not defined |
| Direction | get |
| Sent by | no driver in these sources sends it |
| Payload | Not shown by any driver. |

### 36 SetPlcphdr
| | |
|---|---|
| Names | embassy `SetPlcphdr` `embassy/consts.rs:477` / linux not defined / whd `WLC_SET_PLCPHDR` `whd/src/include/whd_wlioctl.h:1332` `whd/src/whd_utils.c:551` / c-driver not defined |
| Direction | set |
| Sent by | no driver in these sources sends it |
| Payload | Not shown by any driver. |

### 37 GetRadio
| | |
|---|---|
| Names | embassy `GetRadio` `embassy/consts.rs:478` / linux `BRCMF_C_GET_RADIO` `linux/brcmfmac/fwil.h:33` / whd `WLC_GET_RADIO` `whd/src/include/whd_wlioctl.h:1333` `whd/src/whd_utils.c:552` / c-driver not defined |
| Direction | get |
| Sent by | no driver in these sources sends it |
| Payload | Not shown by any driver; width of the returned value not shown. A linux header comment says the `WL_RADIO_*` masks are the radio-disabled status returned by this command: SW_DISABLE bit 0, HW_DISABLE bit 1, COUNTRY_DISABLE bit 3 `linux/include/defs.h:50-55`. whd defines the same bits plus MPC_DISABLE bit 2 `whd/src/include/whd_wlioctl.h:1628-1631` |

### 38 SetRadio
| | |
|---|---|
| Names | embassy `SetRadio` `embassy/consts.rs:479` / linux `BRCMF_C_SET_RADIO` `linux/brcmfmac/fwil.h:34` / whd `WLC_SET_RADIO` `whd/src/include/whd_wlioctl.h:1334` `whd/src/whd_utils.c:553` / c-driver not defined |
| Direction | set |
| Sent by | linux `linux/brcmfmac/cfg80211.c:2729` |
| Payload | One u32, little-endian, 4 bytes. The only call site sends 65536 (0x00010000) = `WL_RADIO_SW_DISABLE` (bit 0) shifted left 16 `linux/brcmfmac/cfg80211.c:2728` `linux/include/defs.h:52` `linux/brcmfmac/fwil.h:87-93`. Meaning of the two 16-bit halves is not stated in these sources. |

- linux — `brcmf_cfg80211_set_tx_power`: software radio on/off state before setting the `qtxpower` named variable (iovar) — s32 65536 (0x00010000) as one `__le32`, 4 bytes; the constant does not depend on the requested power — `linux/brcmfmac/cfg80211.c:2729` `linux/brcmfmac/cfg80211.c:2727` `linux/brcmfmac/cfg80211.c:2728` `linux/brcmfmac/fwil.h:87-93`

### 39 GetPhytype
| | |
|---|---|
| Names | embassy `GetPhytype` `embassy/consts.rs:480` / linux `BRCMF_C_GET_PHYTYPE` `linux/brcmfmac/fwil.h:35` / whd `WLC_GET_PHYTYPE` `whd/src/include/whd_wlioctl.h:1335` `whd/src/whd_utils.c:554` / c-driver not defined |
| Direction | get |
| Sent by | no driver in these sources sends it |
| Payload | Not shown by any driver. |

### 40 DumpRate
| | |
|---|---|
| Names | embassy `DumpRate` `embassy/consts.rs:481` / linux not defined / whd `WLC_DUMP_RATE` `whd/src/include/whd_wlioctl.h:1336` `whd/src/whd_utils.c:555` / c-driver not defined |
| Direction | unknown |
| Sent by | no driver in these sources sends it |
| Payload | Not shown by any driver. |

### 41 SetRateParams
| | |
|---|---|
| Names | embassy `SetRateParams` `embassy/consts.rs:482` / linux not defined / whd `WLC_SET_RATE_PARAMS` `whd/src/include/whd_wlioctl.h:1337` `whd/src/whd_utils.c:556` / c-driver not defined |
| Direction | set |
| Sent by | no driver in these sources sends it |
| Payload | Not shown by any driver. |

### 44 GetKey
| | |
|---|---|
| Names | embassy `GetKey` `embassy/consts.rs:483` / linux not defined / whd `WLC_GET_KEY` `whd/src/include/whd_wlioctl.h:1338` `whd/src/whd_utils.c:557` / c-driver not defined. Numbers 42 and 43 are absent from the embassy enum `embassy/consts.rs:482` `embassy/consts.rs:483`. |
| Direction | get |
| Sent by | no driver in these sources sends it |
| Payload | Not shown by any driver. |

### 45 SetKey
| | |
|---|---|
| Names | embassy `SetKey` `embassy/consts.rs:484` / linux `BRCMF_C_SET_KEY` `linux/brcmfmac/fwil.h:36` / whd `WLC_SET_KEY` `whd/src/include/whd_wlioctl.h:1339` `whd/src/whd_utils.c:558` / c-driver not defined |
| Direction | set |
| Sent by | no driver in these sources sends it |
| Payload | Not shown by any driver. |

### 46 GetRegulatory
| | |
|---|---|
| Names | embassy `GetRegulatory` `embassy/consts.rs:485` / linux `BRCMF_C_GET_REGULATORY` `linux/brcmfmac/fwil.h:37` / whd `WLC_GET_REGULATORY` `whd/src/include/whd_wlioctl.h:1340` `whd/src/whd_utils.c:559` / c-driver not defined |
| Direction | get |
| Sent by | linux `linux/brcmfmac/cfg80211.c:5290` |
| Payload | One u32, little-endian, 4 bytes: the 802.11d (regulatory) setting; linux stores it as a flag in `is_11d` `linux/brcmfmac/cfg80211.c:5290` `linux/brcmfmac/fwil.h:98-104` `linux/brcmfmac/cfg80211.h:259` |

- linux — `brcmf_cfg80211_start_ap`: save the current 802.11d setting in `vif->is_11d` before starting an AP; linux takes a failure to mean 802.11d is unsupported — reads one `__le32`, 4 bytes, converted to host order — `linux/brcmfmac/cfg80211.c:5290` `linux/brcmfmac/cfg80211.c:5289` `linux/brcmfmac/fwil.h:98-104` `linux/brcmfmac/cfg80211.h:259`

### 47 SetRegulatory
| | |
|---|---|
| Names | embassy `SetRegulatory` `embassy/consts.rs:486` / linux `BRCMF_C_SET_REGULATORY` `linux/brcmfmac/fwil.h:38` / whd `WLC_SET_REGULATORY` `whd/src/include/whd_wlioctl.h:1341` `whd/src/whd_utils.c:560` / c-driver not defined |
| Direction | set |
| Sent by | linux `linux/brcmfmac/cfg80211.c:5327` `linux/brcmfmac/cfg80211.c:5555` |
| Payload | One u32, little-endian, 4 bytes: 802.11d enable flag, 0 or 1 as sent by linux `linux/brcmfmac/cfg80211.c:5327` `linux/brcmfmac/cfg80211.c:5555` |

- linux — `brcmf_cfg80211_start_ap`: on a non-mbss interface, set 802.11d to 1 if the beacon tail carries a Country IE, else 0; sent only when the read at 46 succeeded and the value differs from the saved one — int `is_11d` (0 or 1) as one `__le32`, 4 bytes — `linux/brcmfmac/cfg80211.c:5327` `linux/brcmfmac/cfg80211.c:5297` `linux/brcmfmac/cfg80211.c:5325-5326`
- linux — `brcmf_cfg80211_stop_ap`: restore the 802.11d setting saved before the AP started — int `vif->is_11d` as one `__le32`, 4 bytes — `linux/brcmfmac/cfg80211.c:5555`

### 48 GetPassiveScan
| | |
|---|---|
| Names | embassy `GetPassiveScan` `embassy/consts.rs:487` / linux not defined / whd `WLC_GET_PASSIVE_SCAN` `whd/src/include/whd_wlioctl.h:1342` `whd/src/whd_utils.c:561` / c-driver not defined |
| Direction | get |
| Sent by | no driver in these sources sends it |
| Payload | Not shown by any driver. |

### 49 SetPassiveScan
| | |
|---|---|
| Names | embassy `SetPassiveScan` `embassy/consts.rs:488` / linux `BRCMF_C_SET_PASSIVE_SCAN` `linux/brcmfmac/fwil.h:39` / whd `WLC_SET_PASSIVE_SCAN` `whd/src/include/whd_wlioctl.h:1343` `whd/src/whd_utils.c:562` / c-driver not defined |
| Direction | set |
| Sent by | no driver in these sources sends it |
| Payload | Not shown by any driver. |

### 50 Scan
| | |
|---|---|
| Names | embassy `Scan` `embassy/consts.rs:489` / linux `BRCMF_C_SCAN` `linux/brcmfmac/fwil.h:40` / whd `WLC_SCAN` `whd/src/include/whd_wlioctl.h:1344` `whd/src/whd_utils.c:563` / c-driver not defined |
| Direction | set |
| Sent by | linux `linux/brcmfmac/cfg80211.c:1212` `linux/brcmfmac/cfg80211.c:1219` |
| Payload | Scan-parameters record, all fields little-endian. v1 `linux/brcmfmac/fwil_types.h:368-407`: ssid {le32 len, 32 bytes}, bssid[6], s8 bss_type, u8 scan_type, le32 nprobes, le32 active_time, le32 passive_time, le32 home_time, le32 channel_num, then le16 chanspec list; fixed part 64 bytes `linux/brcmfmac/fwil_types.h:50`. v2 `linux/brcmfmac/fwil_types.h:409-451`: le16 version and le16 length in front, scan_type widened to le32 after a pad byte; fixed part 72 bytes `linux/brcmfmac/fwil_types.h:51`. The SSID array length is `IEEE80211_MAX_SSID_LEN` = 32 `linux/brcmfmac/fwil_types.h:359` `linux-headers/ieee80211.h:227`. Abort values linux fills in: bssid broadcast, bss_type any, active scan, times and nprobes -1, channel_num = 1, channel_list[0] = 65535 (0xFFFF) `linux/brcmfmac/cfg80211.c:1109-1129`. The record's comment says the padding entry exists for this on-stack abort use `linux/brcmfmac/fwil_types.h:402-404`. |

- linux — `brcmf_notify_escan_complete` with fw_abort, SCAN_V2 feature present: abort a running scan — `struct brcmf_scan_params_v2_le`, `sizeof` = 76 bytes sent (72 fixed + one 2-byte channel entry + 2 bytes tail padding of an on-stack record; the padding follows from the record's 4-byte alignment (computed)); version = 2; the length field is set to 74, not 76 — `linux/brcmfmac/cfg80211.c:1212` `linux/brcmfmac/cfg80211.c:1184` `linux/brcmfmac/cfg80211.c:1189` `linux/brcmfmac/cfg80211.c:1111` `linux/brcmfmac/cfg80211.c:1113` `linux/brcmfmac/cfg80211.c:1125` `linux/brcmfmac/cfg80211.c:1128` `linux/brcmfmac/fwil_types.h:54`
- linux — `brcmf_notify_escan_complete` with fw_abort, no SCAN_V2 feature: abort a running scan after converting the v2 record to v1 — `struct brcmf_scan_params_le`, `sizeof` = 68 bytes sent (64 fixed + one 2-byte channel entry + 2 bytes tail padding of an on-stack record (computed)) — `linux/brcmfmac/cfg80211.c:1219` `linux/brcmfmac/cfg80211.c:1216` `linux/brcmfmac/cfg80211.c:1218` `linux/brcmfmac/cfg80211.c:1062-1094`

Differences: only linux sends this command, and only to abort a scan `linux/brcmfmac/cfg80211.c:1212` `linux/brcmfmac/cfg80211.c:1219`. linux and embassy start scans with the `escan` named variable `linux/brcmfmac/cfg80211.c:1491` `embassy/control.rs:835`. whd mentions the command only in a P2P record comment (type S for `WLC_SCAN`, E for escan) `whd/src/include/whd_wlioctl.h:3931`

### 51 ScanResults
| | |
|---|---|
| Names | embassy `ScanResults` `embassy/consts.rs:490` / linux `BRCMF_C_SCAN_RESULTS` `linux/brcmfmac/fwil.h:41` / whd `WLC_SCAN_RESULTS` `whd/src/include/whd_wlioctl.h:1345` `whd/src/whd_utils.c:564` / c-driver not defined |
| Direction | unknown |
| Sent by | no driver in these sources sends it |
| Payload | Not shown by any driver. |

### 52 Disassoc
| | |
|---|---|
| Names | embassy `Disassoc` `embassy/consts.rs:491` / linux `BRCMF_C_DISASSOC` `linux/brcmfmac/fwil.h:42` / whd `WLC_DISASSOC` `whd/src/include/whd_wlioctl.h:1346` `whd/src/whd_utils.c:565`, also in the trace helper `whd/src/whd_utils.c:1047` / c-driver `WLC_DISASSOC` (52), public alias `CYW43_IOCTL_SET_DISASSOC` (0x69 = 52*2+1) `c-driver/cyw43_ll.c:174` `c-driver/cyw43_ll.h:33`, also in the debug name table `c-driver/cyw43_ll.c:872`. c-driver public values are command number * 2 + set bit `c-driver/cyw43_ll.h:30` `c-driver/cyw43_ll.c:1329` |
| Direction | set |
| Sent by | embassy `embassy/control.rs:841`, linux `linux/brcmfmac/cfg80211.c:1759` `linux/brcmfmac/cfg80211.c:2681`, whd `whd/src/whd_wifi_api.c:2529`, c-driver `c-driver/cyw43_ctrl.c:220` `c-driver/cyw43_ctrl.c:678` |
| Payload | Two forms. Empty, 0 bytes (embassy, whd, c-driver, one linux site) `embassy/control.rs:841` `whd/src/whd_wifi_api.c:2529` `c-driver/cyw43_ctrl.c:220` `c-driver/cyw43_ctrl.c:678` `linux/brcmfmac/cfg80211.c:1759`. Or 12 bytes (other linux site): le32 reason code at 0, BSSID[6] at 4, 2 bytes record tail padding at 10 `linux/brcmfmac/fwil_types.h:602-605` `linux/brcmfmac/cfg80211.c:2681` |

- embassy — `Control::leave`: leave the current network; also run by `join()` when a previous join was started — empty slice, 0 bytes, interface 0; the other embassy references are unit tests `embassy/control.rs:962` `embassy/control.rs:991` — `embassy/control.rs:841` `embassy/control.rs:369-370`
- linux — `brcmf_link_down`: disassociate when a connected interface goes down and the bus is up; the debug message says this stops excess roaming `linux/brcmfmac/cfg80211.c:1757` — NULL, 0 bytes — `linux/brcmfmac/cfg80211.c:1759`
- linux — `brcmf_cfg80211_disconnect`: disconnect from the profile BSSID with the cfg80211 reason code — `struct brcmf_scb_val_le` { `__le32 val` = reason code, `u8 ea[6]` = BSSID }, 12 bytes sent; the record is on the stack and not zeroed, so the driver does not set the 2 padding bytes — `linux/brcmfmac/cfg80211.c:2681` `linux/brcmfmac/cfg80211.c:2666` `linux/brcmfmac/cfg80211.c:2679-2680` `linux/brcmfmac/fwil_types.h:602-605`
- whd — `whd_wifi_leave`: disassociate from the AP — NULL, 0 bytes — `whd/src/whd_wifi_api.c:2529` `whd/src/whd_wifi_api.c:5095-5106`
- c-driver — `cyw43_poll_func`: host-initiated disassociation on the STA interface when `pend_disassoc` is set (raised in the async event handler) — NULL, 0 bytes — `c-driver/cyw43_ctrl.c:220` `c-driver/cyw43_ctrl.c:194` `c-driver/cyw43_ctrl.c:386`
- c-driver — `cyw43_wifi_leave`: disassociate on the given interface — NULL, 0 bytes — `c-driver/cyw43_ctrl.c:678`

Differences: embassy, whd, c-driver and one linux site send 0 bytes; the other linux site sends 12 bytes (reason code + BSSID + padding). Both forms go to the same command number `embassy/control.rs:841` `whd/src/whd_wifi_api.c:2529` `c-driver/cyw43_ctrl.c:678` `linux/brcmfmac/cfg80211.c:1759` `linux/brcmfmac/cfg80211.c:2681`

### 53 Reassoc
| | |
|---|---|
| Names | embassy `Reassoc` `embassy/consts.rs:492` / linux `BRCMF_C_REASSOC` `linux/brcmfmac/fwil.h:43` / whd `WLC_REASSOC` `whd/src/include/whd_wlioctl.h:1347` `whd/src/whd_utils.c:566` / c-driver not defined |
| Direction | set |
| Sent by | whd `whd/src/whd_wifi_api.c:2397` |
| Payload | whd `wl_assoc_params_t`, packed, 14 bytes: bssid[6] at 0, u16 bssid_cnt at 6, u32 chanspec_num at 8, u16 chanspec_list[1] at 12 `whd/src/include/whd_wlioctl.h:4239-4247` `whd/src/include/whd_wlioctl.h:4188` `whd/src/include/whd_wlioctl.h:48`. whd zeroes the record and then copies in the AP's BSSID; byte order of the multi-byte fields (bssid_cnt, chanspec_num, chanspec_list) is not exercised, since those stay zero `whd/src/whd_wifi_api.c:2391-2394` |

- whd — `whd_wifi_join_specific`: when already associated to an AP with the same SSID, reassociate to the given BSSID instead of a fresh join — `wl_reassoc_params_t` (= `wl_assoc_params_t`), 14 bytes, bssid = AP BSSID, every other field zero — `whd/src/whd_wifi_api.c:2397` `whd/src/whd_wifi_api.c:2239` `whd/src/whd_wifi_api.c:2320-2326` `whd/src/whd_wifi_api.c:2342` `whd/src/whd_wifi_api.c:2391-2394`

Differences: layout only, not a send-side disagreement: linux `struct brcmf_assoc_params_le` has no bssid_cnt field after the BSSID, but linux never sends this command `linux/brcmfmac/fwil_types.h:482-490` `whd/src/include/whd_wlioctl.h:4239-4247`

### 54 GetRoamTrigger
| | |
|---|---|
| Names | embassy `GetRoamTrigger` `embassy/consts.rs:493` / linux not defined / whd `WLC_GET_ROAM_TRIGGER` `whd/src/include/whd_wlioctl.h:1348` `whd/src/whd_utils.c:567` / c-driver `CYW43_IOCTL_GET_ROAM_TRIGGER` (0x6c = 54*2) `c-driver/cyw43_ll.h:34`. c-driver public values are command number * 2 + set bit `c-driver/cyw43_ll.h:30` `c-driver/cyw43_ll.c:1329` |
| Direction | get |
| Sent by | c-driver `c-driver/cyw43.h:501` |
| Payload | As read by c-driver: 4 bytes, signed 32-bit RSSI threshold in dBm, raw host memory, no byte swap `c-driver/cyw43.h:501` `c-driver/cyw43_ctrl.c:450-452`. Host little-endian (recalled, not in these sources). Whether the reply also carries a band word (see 55) is not shown. A c-driver doc comment gives the firmware default as -75 dBm `c-driver/cyw43.h:456-457` |

- c-driver — `cyw43_wifi_get_roam_params`: read the RSSI roam trigger for the STA interface — reads 4 bytes into `int32_t *trigger_dbm` cast to `uint32_t *`, host memory as-is — `c-driver/cyw43.h:501` `c-driver/cyw43.h:498` `c-driver/cyw43_ctrl.c:450-452`

### 55 SetRoamTrigger
| | |
|---|---|
| Names | embassy `SetRoamTrigger` `embassy/consts.rs:494` / linux `BRCMF_C_SET_ROAM_TRIGGER` `linux/brcmfmac/fwil.h:44` / whd `WLC_SET_ROAM_TRIGGER` `whd/src/include/whd_wlioctl.h:1349` `whd/src/whd_utils.c:568`, also in the trace helper `whd/src/whd_utils.c:1051` / c-driver `CYW43_IOCTL_SET_ROAM_TRIGGER` (0x6f = 55*2+1) `c-driver/cyw43_ll.h:35`. c-driver public values are command number * 2 + set bit `c-driver/cyw43_ll.h:30` `c-driver/cyw43_ll.c:1329` |
| Direction | set |
| Sent by | linux `linux/brcmfmac/cfg80211.c:7140`, c-driver `c-driver/cyw43.h:472` |
| Payload | Signed 32-bit RSSI threshold in dBm. linux: 8 bytes, le32 level at 0, le32 band at 4 `linux/brcmfmac/cfg80211.c:7138-7140`. c-driver: 4 bytes, level only, raw host memory, no byte swap `c-driver/cyw43.h:472` `c-driver/cyw43_ctrl.c:446-448`. A c-driver doc comment says the firmware default is -75 dBm and the value must be negative `c-driver/cyw43.h:456-461` |

- linux — `brcmf_dongle_roam`: roam trigger level for all bands during dongle setup — `__le32 roamtrigger[2]` = { `WL_ROAM_TRIGGER_LEVEL` (-75), `BRCM_BAND_ALL` (3) }, 8 bytes — `linux/brcmfmac/cfg80211.c:7140` `linux/brcmfmac/cfg80211.c:7112` `linux/brcmfmac/cfg80211.c:7138-7139` `linux/brcmfmac/cfg80211.h:25` `linux/include/defs.h:64`
- c-driver — `cyw43_wifi_set_roam_params`: RSSI threshold below which roam scanning begins, STA interface — `int32_t trigger_dbm` cast to `uint32_t`, 4 bytes — `c-driver/cyw43.h:472` `c-driver/cyw43_ctrl.c:446-448`

Differences: size. linux sends 8 bytes {level, band}; c-driver sends 4 bytes {level} `linux/brcmfmac/cfg80211.c:7140` `c-driver/cyw43.h:472`

### 56 GetRoamDelta
| | |
|---|---|
| Names | embassy `GetRoamDelta` `embassy/consts.rs:495` / linux not defined / whd `WLC_GET_ROAM_DELTA` `whd/src/include/whd_wlioctl.h:1350` `whd/src/whd_utils.c:569` / c-driver `CYW43_IOCTL_GET_ROAM_DELTA` (0x70 = 56*2) `c-driver/cyw43_ll.h:36`. c-driver public values are command number * 2 + set bit `c-driver/cyw43_ll.h:30` `c-driver/cyw43_ll.c:1329` |
| Direction | get |
| Sent by | c-driver `c-driver/cyw43.h:507` |
| Payload | As read by c-driver: 4 bytes, minimum RSSI improvement in dB a candidate AP must offer, raw host memory, no byte swap `c-driver/cyw43.h:507` `c-driver/cyw43_ctrl.c:450-452`. Host little-endian (recalled, not in these sources). Whether the reply also carries a band word is not shown; linux sends the set counterpart (57) as 8 bytes {delta, band} `linux/brcmfmac/cfg80211.c:7145-7148`. A c-driver doc comment gives the firmware default as 20 dB `c-driver/cyw43.h:456-457` `c-driver/cyw43.h:462-464` |

- c-driver — `cyw43_wifi_get_roam_params`: read the roam delta for the STA interface — reads 4 bytes into `int32_t *candidate_delta_db` cast to `uint32_t *`, host memory as-is — `c-driver/cyw43.h:507` `c-driver/cyw43.h:498` `c-driver/cyw43_ctrl.c:450-452`

### 57 SetRoamDelta
| | |
|---|---|
| Names | embassy `SetRoamDelta` `embassy/consts.rs:496` / linux `BRCMF_C_SET_ROAM_DELTA` `linux/brcmfmac/fwil.h:45` / whd `WLC_SET_ROAM_DELTA` `whd/src/include/whd_wlioctl.h:1351` / c-driver `CYW43_IOCTL_SET_ROAM_DELTA` (0x73 = 57*2+1) `c-driver/cyw43_ll.h:37`. c-driver public command values are (number*2 \| set-bit); `cyw43_ll_ioctl` splits them into direction and number before sending `c-driver/cyw43_ll.h:29-30` `c-driver/cyw43_ll.c:1329` |
| Direction | set `linux/brcmfmac/cfg80211.c:7147` `c-driver/cyw43.h:476` |
| Sent by | linux `linux/brcmfmac/cfg80211.c:7147`, c-driver `c-driver/cyw43.h:476`. whd: debug name tables only `whd/src/whd_utils.c:570` `whd/src/whd_utils.c:1053-1055`. embassy: constant only `embassy/consts.rs:496` |
| Payload | linux: 8 bytes, two little-endian u32: delta, then band selector `linux/brcmfmac/cfg80211.c:7113` `linux/brcmfmac/cfg80211.c:7145-7148`. c-driver: 4 bytes, one 32-bit delta in host byte order, no explicit conversion `c-driver/cyw43_ctrl.c:446-447`. A c-driver comment gives 20 dB as the firmware default delta `c-driver/cyw43.h:456-457` |

- linux — `brcmf_dongle_roam`: sets roam delta to `WL_ROAM_DELTA` (20) for all bands; failure is logged only — `__le32 roam_delta[2]` = { 20, `BRCM_BAND_ALL` (3) }, 8 bytes — `linux/brcmfmac/cfg80211.c:7147` `linux/brcmfmac/cfg80211.h:26` `linux/include/defs.h:64` `linux/brcmfmac/cfg80211.c:7149-7150`
- c-driver — `cyw43_wifi_set_roam_params`: sets the RSSI improvement in dB a candidate AP must offer, on the STA interface — `uint32_t` (cast from `int32_t`), 4 bytes, host order — `c-driver/cyw43.h:476` `c-driver/cyw43.h:451-454` `c-driver/cyw43_ctrl.c:446-447`

Differences: linux sends 8 bytes {delta, band}; c-driver sends 4 bytes {delta} only. `linux/brcmfmac/cfg80211.c:7145-7148` `c-driver/cyw43_ctrl.c:446-447`

### 58 GetRoamScanPeriod
| | |
|---|---|
| Names | embassy `GetRoamScanPeriod` `embassy/consts.rs:497` / linux: not defined / whd `WLC_GET_ROAM_SCAN_PERIOD` `whd/src/include/whd_wlioctl.h:1352` / c-driver `CYW43_IOCTL_GET_ROAM_SCAN_PERIOD` (0x74 = 58*2) `c-driver/cyw43_ll.h:38` |
| Direction | get `c-driver/cyw43.h:513` |
| Sent by | c-driver `c-driver/cyw43.h:513`. whd: debug name table only `whd/src/whd_utils.c:571`. embassy: constant only `embassy/consts.rs:497` |
| Payload | c-driver: 4 bytes, one 32-bit value read in host byte order `c-driver/cyw43_ctrl.c:450-451`. Unit not documented; a c-driver comment says it is believed to be seconds, default 10 `c-driver/cyw43.h:456-457` `c-driver/cyw43.h:465-468` |

- c-driver — `cyw43_wifi_get_roam_params`: reads back the roam scan period on the STA interface — `uint32_t` out buffer (cast from `int32_t*`), 4 bytes, host order — `c-driver/cyw43.h:513` `c-driver/cyw43_ctrl.c:450-451`

### 59 SetRoamScanPeriod
| | |
|---|---|
| Names | embassy `SetRoamScanPeriod` `embassy/consts.rs:498` / linux: not defined / whd `WLC_SET_ROAM_SCAN_PERIOD` `whd/src/include/whd_wlioctl.h:1353` / c-driver `CYW43_IOCTL_SET_ROAM_SCAN_PERIOD` (0x77 = 59*2+1) `c-driver/cyw43_ll.h:39` |
| Direction | set `c-driver/cyw43.h:480` |
| Sent by | c-driver `c-driver/cyw43.h:480`. whd: debug name tables only `whd/src/whd_utils.c:572` `whd/src/whd_utils.c:1057-1059`. embassy: constant only `embassy/consts.rs:498` |
| Payload | c-driver: 4 bytes, one 32-bit value in host byte order `c-driver/cyw43_ctrl.c:446-447`. Unit not documented; a c-driver comment says it is believed to be seconds, default 10 `c-driver/cyw43.h:456-457` `c-driver/cyw43.h:465-468` |

- c-driver — `cyw43_wifi_set_roam_params`: sets how often scans for a better AP run while below the roam trigger — `uint32_t` (cast from `int32_t`), 4 bytes, host order — `c-driver/cyw43.h:480` `c-driver/cyw43_ctrl.c:446-447`

### 60 Evm
| | |
|---|---|
| Names | embassy `Evm` `embassy/consts.rs:499` / linux: not defined / whd `WLC_EVM` `whd/src/include/whd_wlioctl.h:1354` / c-driver: not defined |
| Direction | not found in these sources; the name gives no direction `embassy/consts.rs:499` |
| Sent by | no driver in these sources sends it. whd: debug name table only `whd/src/whd_utils.c:573` |
| Payload | not found in these sources |

### 61 GetTxant
| | |
|---|---|
| Names | embassy `GetTxant` `embassy/consts.rs:500` / linux: not defined / whd `WLC_GET_TXANT` `whd/src/include/whd_wlioctl.h:1355` / c-driver: not defined |
| Direction | get (inferred from the name) `embassy/consts.rs:500` |
| Sent by | no driver in these sources sends it. whd: debug name table only `whd/src/whd_utils.c:574` |
| Payload | not found in these sources |

### 62 SetTxant
| | |
|---|---|
| Names | embassy `SetTxant` `embassy/consts.rs:501` / linux: not defined / whd `WLC_SET_TXANT` `whd/src/include/whd_wlioctl.h:1356` / c-driver: not defined |
| Direction | set (inferred from the name) `embassy/consts.rs:501` |
| Sent by | no driver in these sources sends it. whd: debug name table only `whd/src/whd_utils.c:575` |
| Payload | not found in these sources |

### 63 GetAntdiv
| | |
|---|---|
| Names | embassy `GetAntdiv` `embassy/consts.rs:502` / linux: not defined / whd `WLC_GET_ANTDIV` `whd/src/include/whd_wlioctl.h:1357` / c-driver `WLC_GET_ANTDIV` (63) `c-driver/cyw43_ll.c:175` and `CYW43_IOCTL_GET_ANTDIV` (0x7e = 63*2) `c-driver/cyw43_ll.h:40` |
| Direction | get (inferred from the name) `embassy/consts.rs:502` |
| Sent by | no driver in these sources sends it. c-driver: debug name table `c-driver/cyw43_ll.c:873` and an exported constant with no caller in these sources `c-driver/cyw43_ll.h:40`. whd: debug name table only `whd/src/whd_utils.c:576` |
| Payload | not found in these sources. One 4-byte little-endian u32, by symmetry with command 64 (inferred) `embassy/control.rs:748-751` `c-driver/cyw43_ll.c:1956-1960` |

### 64 SetAntdiv
| | |
|---|---|
| Names | embassy `SetAntdiv` `embassy/consts.rs:503` / linux: not defined / whd `WLC_SET_ANTDIV` `whd/src/include/whd_wlioctl.h:1358` / c-driver `WLC_SET_ANTDIV` (64) `c-driver/cyw43_ll.c:176` and `CYW43_IOCTL_SET_ANTDIV` (0x81 = 64*2+1) `c-driver/cyw43_ll.h:41` |
| Direction | set `embassy/control.rs:290` `c-driver/cyw43_ll.c:2034` |
| Sent by | embassy `embassy/control.rs:290`, c-driver `c-driver/cyw43_ll.c:2034`. whd: debug name table only `whd/src/whd_utils.c:577`. c-driver also has a debug name table entry `c-driver/cyw43_ll.c:874` |
| Payload | 4 bytes, one little-endian u32 antenna selector `embassy/control.rs:748-751` `c-driver/cyw43_ll.c:1956-1960`. Both senders use 0, which their comments call the chip antenna `embassy/control.rs:289` `c-driver/cyw43_ll.c:2033`. Other values not found in these sources. |

- embassy — init, after the `country` named variable (iovar) and a 100 ms wait: selects the chip antenna on interface 0 — u32 = 0, 4 bytes little-endian — `embassy/control.rs:290` `embassy/control.rs:284-287` `embassy/control.rs:748-751`
- c-driver — wifi init: selects the chip antenna on `WWD_STA_INTERFACE` — u32 = 0, 4 bytes little-endian via `cyw43_put_le32` — `c-driver/cyw43_ll.c:2034` `c-driver/cyw43_ll.c:1956-1960`

### 67 GetClosed
| | |
|---|---|
| Names | embassy `GetClosed` `embassy/consts.rs:504` / linux: not defined / whd `WLC_GET_CLOSED` `whd/src/include/whd_wlioctl.h:1359` / c-driver: not defined |
| Direction | get (inferred from the name) `embassy/consts.rs:504` |
| Sent by | no driver in these sources sends it. whd: debug name table only `whd/src/whd_utils.c:578` |
| Payload | not found in these sources. whd defines a named-variable string `closednet`; nothing in these sources links it to this command `whd/src/include/whd_wlioctl.h:1105` |

### 68 SetClosed
| | |
|---|---|
| Names | embassy `SetClosed` `embassy/consts.rs:505` / linux: not defined / whd `WLC_SET_CLOSED` `whd/src/include/whd_wlioctl.h:1360` / c-driver: not defined |
| Direction | set (inferred from the name) `embassy/consts.rs:505` |
| Sent by | no driver in these sources sends it. whd: debug name table only `whd/src/whd_utils.c:579` |
| Payload | not found in these sources. whd defines a named-variable string `closednet`; nothing in these sources links it to this command `whd/src/include/whd_wlioctl.h:1105` |

### 69 GetMaclist
| | |
|---|---|
| Names | embassy `GetMaclist` `embassy/consts.rs:506` / linux: not defined / whd `WLC_GET_MACLIST` `whd/src/include/whd_wlioctl.h:1361` / c-driver: not defined |
| Direction | get (inferred from the name) `embassy/consts.rs:506` |
| Sent by | no driver in these sources sends it. whd: debug name table only `whd/src/whd_utils.c:580` |
| Payload | not found in these sources |

### 70 SetMaclist
| | |
|---|---|
| Names | embassy `SetMaclist` `embassy/consts.rs:507` / linux: not defined / whd `WLC_SET_MACLIST` `whd/src/include/whd_wlioctl.h:1362` / c-driver: not defined |
| Direction | set (inferred from the name) `embassy/consts.rs:507` |
| Sent by | no driver in these sources sends it. whd: debug name table only `whd/src/whd_utils.c:581` |
| Payload | not found in these sources |

### 71 GetRateset
| | |
|---|---|
| Names | embassy `GetRateset` `embassy/consts.rs:508` / linux: not defined / whd `WLC_GET_RATESET` `whd/src/include/whd_wlioctl.h:1363` / c-driver: not defined |
| Direction | get (inferred from the name) `embassy/consts.rs:508` |
| Sent by | no driver in these sources sends it. whd: debug name table only `whd/src/whd_utils.c:582` |
| Payload | not found in these sources. whd defines the record `wl_rateset_t` { u32 count; u8 rates[16] }, 20 bytes (computed), rates in 500 kbps units with the high bit marking a basic rate; no call site ties it to this command (association by name only, inferred) `whd/src/include/whd_wlioctl.h:572-577` |

### 72 SetRateset
| | |
|---|---|
| Names | embassy `SetRateset` `embassy/consts.rs:509` / linux: not defined / whd `WLC_SET_RATESET` `whd/src/include/whd_wlioctl.h:1364` / c-driver: not defined |
| Direction | set (inferred from the name) `embassy/consts.rs:509` |
| Sent by | no driver in these sources sends it. whd: debug name table only `whd/src/whd_utils.c:583` |
| Payload | not found in these sources. whd's record `wl_rateset_t` (20 bytes, see 71) exists but no call site ties it to this command `whd/src/include/whd_wlioctl.h:572-577` |

### 74 Longtrain
| | |
|---|---|
| Names | embassy `Longtrain` `embassy/consts.rs:510` / linux: not defined / whd `WLC_LONGTRAIN` `whd/src/include/whd_wlioctl.h:1365` / c-driver: not defined |
| Direction | not found in these sources; the name gives no direction `embassy/consts.rs:510` |
| Sent by | no driver in these sources sends it. whd: debug name table only `whd/src/whd_utils.c:584` |
| Payload | not found in these sources |

### 75 GetBcnprd
| | |
|---|---|
| Names | embassy `GetBcnprd` `embassy/consts.rs:511` / linux `BRCMF_C_GET_BCNPRD` `linux/brcmfmac/fwil.h:46` / whd `WLC_GET_BCNPRD` `whd/src/include/whd_wlioctl.h:1366` / c-driver: not defined |
| Direction | get (inferred from the name) `embassy/consts.rs:511` |
| Sent by | no driver in these sources sends it. linux: constant only `linux/brcmfmac/fwil.h:46`. whd: debug name table only `whd/src/whd_utils.c:585` |
| Payload | not found in these sources. One 4-byte little-endian u32 beacon period, by symmetry with command 76 (inferred) `linux/brcmfmac/fwil.h:87-93` `whd/src/whd_wifi_api.c:5048-5063`. Unit not stated in these sources. |

### 76 SetBcnprd
| | |
|---|---|
| Names | embassy `SetBcnprd` `embassy/consts.rs:512` / linux `BRCMF_C_SET_BCNPRD` `linux/brcmfmac/fwil.h:47`, also `BRCM_SET_BCNPRD` (76), a define with no use in these sources `linux/include/defs.h:45` / whd `WLC_SET_BCNPRD` `whd/src/include/whd_wlioctl.h:1367`, also public `WHD_IOCTL_SET_BCNPRD` (76) `whd/inc/whd_types.h:477` / c-driver: not defined |
| Direction | set `linux/brcmfmac/cfg80211.c:1865` `whd/src/whd_wifi_api.c:5404` |
| Sent by | linux `linux/brcmfmac/cfg80211.c:1865` `linux/brcmfmac/cfg80211.c:5336`, whd `whd/src/whd_wifi_api.c:5404`. embassy: constant only `embassy/consts.rs:512`. whd also has a debug name table entry `whd/src/whd_utils.c:586`, and lists `WHD_IOCTL_SET_BCNPRD` in its enum of commands exposed to applications (`whd_usr_ioctl_set_list_t`), which no caller in these sources uses `whd/inc/whd_types.h:468-483` `whd/inc/whd_wifi_api.h:1531` |
| Payload | 4 bytes, one little-endian u32 beacon period; linux converts with `cpu_to_le32`, whd with `htod32` (a byte swap only when `IL_BIGENDIAN` is defined) `linux/brcmfmac/fwil.h:87-93` `whd/src/whd_wifi_api.c:5048-5063` `whd/src/include/whd_endian.h:44-54`. Unit: whd documents its `interval` argument as time units, 100 time units = 102.4 ms `whd/inc/whd_wifi_api.h:855`; linux states no unit. |

- linux — `brcmf_cfg80211_join_ibss`: sets the beacon interval for an IBSS starter, from `params->beacon_interval` or default 100 — u32 as `__le32`, 4 bytes — `linux/brcmfmac/cfg80211.c:1865` `linux/brcmfmac/cfg80211.c:1859-1863` `linux/brcmfmac/fwil.h:87-93`
- linux — `brcmf_cfg80211_start_ap`: sets the AP beacon interval from `settings->beacon_interval` when non-zero, inside the `if (!mbss)` block — u32 as `__le32`, 4 bytes — `linux/brcmfmac/cfg80211.c:5336` `linux/brcmfmac/cfg80211.c:5325` `linux/brcmfmac/fwil.h:87-93`
- whd — `whd_wifi_ap_set_beacon_interval`: sets the AP beacon interval — `uint16_t` widened to `uint32_t`, 4 bytes via `htod32` — `whd/src/whd_wifi_api.c:5404` `whd/src/whd_wifi_api.c:5048-5063`

### 77 GetDtimprd
| | |
|---|---|
| Names | embassy `GetDtimprd` `embassy/consts.rs:513` / linux `BRCMF_C_GET_DTIMPRD` `linux/brcmfmac/fwil.h:48` / whd `WLC_GET_DTIMPRD` `whd/src/include/whd_wlioctl.h:1368` / c-driver: not defined |
| Direction | get (inferred from the name) `embassy/consts.rs:513` |
| Sent by | no driver in these sources sends it. linux: constant only `linux/brcmfmac/fwil.h:48`. whd: debug name table only `whd/src/whd_utils.c:587` |
| Payload | not found in these sources. One 4-byte little-endian u32 DTIM period, by symmetry with command 78 (inferred) `linux/brcmfmac/fwil.h:87-93` `whd/src/whd_wifi_api.c:5048-5063` `c-driver/cyw43_ll.c:1956-1960` |

### 78 SetDtimprd
| | |
|---|---|
| Names | embassy `SetDtimprd` `embassy/consts.rs:514` / linux `BRCMF_C_SET_DTIMPRD` `linux/brcmfmac/fwil.h:49` / whd `WLC_SET_DTIMPRD` `whd/src/include/whd_wlioctl.h:1369`, also public `WHD_IOCTL_SET_DTIMPRD` (78) `whd/inc/whd_types.h:478` / c-driver `WLC_SET_DTIMPRD` (78) `c-driver/cyw43_ll.c:177` |
| Direction | set `linux/brcmfmac/cfg80211.c:5345` `whd/src/whd_wifi_api.c:5412` `c-driver/cyw43_ll.c:2449` |
| Sent by | linux `linux/brcmfmac/cfg80211.c:5345`, whd `whd/src/whd_wifi_api.c:5412`, c-driver `c-driver/cyw43_ll.c:2449`. embassy: constant only `embassy/consts.rs:514`. Debug name table entries also exist: c-driver `c-driver/cyw43_ll.c:875`, whd `whd/src/whd_utils.c:588`. whd lists `WHD_IOCTL_SET_DTIMPRD` in its enum of commands exposed to applications (`whd_usr_ioctl_set_list_t`), which no caller in these sources uses `whd/inc/whd_types.h:468-483` `whd/inc/whd_wifi_api.h:1531` |
| Payload | 4 bytes, one little-endian u32 DTIM period; linux converts with `cpu_to_le32`, whd with `htod32` (a byte swap only when `IL_BIGENDIAN` is defined), c-driver with `cyw43_put_le32` `linux/brcmfmac/fwil.h:87-93` `whd/src/whd_wifi_api.c:5048-5063` `whd/src/include/whd_endian.h:44-54` `c-driver/cyw43_ll.c:1956-1960` |

- linux — `brcmf_cfg80211_start_ap`: sets the DTIM period from `settings->dtim_period` when non-zero, inside the `if (!mbss)` block — u32 as `__le32`, 4 bytes — `linux/brcmfmac/cfg80211.c:5345` `linux/brcmfmac/cfg80211.c:5325` `linux/brcmfmac/fwil.h:87-93`
- whd — `whd_wifi_ap_set_dtim_interval`: sets the AP DTIM interval on the interface the caller passes — `uint16_t` widened to `uint32_t`, 4 bytes via `htod32` — `whd/src/whd_wifi_api.c:5412` `whd/src/whd_wifi_api.c:5408-5414` `whd/src/whd_wifi_api.c:5048-5063`
- c-driver — AP setup: sets the DTIM period to 1 on `WWD_AP_INTERFACE` — u32 = 1, 4 bytes little-endian — `c-driver/cyw43_ll.c:2449` `c-driver/cyw43_ll.c:1956-1960`

Differences: linux and whd send a caller-supplied period; c-driver always sends 1. `linux/brcmfmac/cfg80211.c:5345` `whd/src/whd_wifi_api.c:5412` `c-driver/cyw43_ll.c:2449`

### 79 GetSrom
| | |
|---|---|
| Names | embassy `GetSrom` `embassy/consts.rs:515` / linux: not defined / whd `WLC_GET_SROM` `whd/src/include/whd_wlioctl.h:1370` / c-driver: not defined |
| Direction | get (inferred from the name) `embassy/consts.rs:515` |
| Sent by | no driver in these sources sends it. whd: debug name table only `whd/src/whd_utils.c:589` |
| Payload | not found in these sources. whd defines the record `srom_rw_t` { u32 byteoff; u32 nbytes; u16 buf[1] }; no call site ties it to this command (association by name only, inferred) `whd/src/include/whd_wlioctl.h:890-895` |

### 80 SetSrom
| | |
|---|---|
| Names | embassy `SetSrom` `embassy/consts.rs:516` / linux: not defined / whd `WLC_SET_SROM` `whd/src/include/whd_wlioctl.h:1371` / c-driver: not defined |
| Direction | set (inferred from the name) `embassy/consts.rs:516` |
| Sent by | no driver in these sources sends it. whd: debug name table only `whd/src/whd_utils.c:590` |
| Payload | not found in these sources. whd's record `srom_rw_t` (see 79) exists but no call site ties it to this command `whd/src/include/whd_wlioctl.h:890-895` |

### 81 GetWepRestrict
| | |
|---|---|
| Names | embassy `GetWepRestrict` `embassy/consts.rs:517` / linux: not defined / whd `WLC_GET_WEP_RESTRICT` `whd/src/include/whd_wlioctl.h:1372` / c-driver: not defined |
| Direction | get (inferred from the name) `embassy/consts.rs:517` |
| Sent by | no driver in these sources sends it. whd: debug name table only `whd/src/whd_utils.c:591` |
| Payload | not found in these sources |

### 82 SetWepRestrict
| | |
|---|---|
| Names | embassy `SetWepRestrict` `embassy/consts.rs:518` / linux: not defined / whd `WLC_SET_WEP_RESTRICT` `whd/src/include/whd_wlioctl.h:1373` / c-driver: not defined |
| Direction | set (inferred from the name) `embassy/consts.rs:518` |
| Sent by | no driver in these sources sends it. whd: debug name table only `whd/src/whd_utils.c:592` |
| Payload | not found in these sources |

### 83 GetCountry
| | |
|---|---|
| Names | embassy `GetCountry` `embassy/consts.rs:519` / linux: not defined / whd `WLC_GET_COUNTRY` `whd/src/include/whd_wlioctl.h:1374`, also public `WHD_IOCTL_GET_COUNTRY` (83) `whd/inc/whd_types.h:452` / c-driver: not defined |
| Direction | get (inferred from the name) `embassy/consts.rs:519` |
| Sent by | no driver in these sources sends it. whd: debug name table `whd/src/whd_utils.c:593` and an entry in its enum of commands exposed to applications (`whd_usr_ioctl_get_list_t`), which no caller in these sources uses `whd/inc/whd_types.h:449-463` `whd/inc/whd_wifi_api.h:1541` `whd/inc/whd_wifi_api.h:1563` |
| Payload | not found in these sources. whd and embassy set the country through the `country` named variable, not this command `whd/src/whd_management.c:173-196` `whd/src/include/whd_wlioctl.h:668-673` `embassy/control.rs:280-284` |

### 84 SetCountry
| | |
|---|---|
| Names | embassy `SetCountry` `embassy/consts.rs:520` / linux `BRCMF_C_SET_COUNTRY` `linux/brcmfmac/fwil.h:50` / whd `WLC_SET_COUNTRY` `whd/src/include/whd_wlioctl.h:1375` `whd/src/include_helium/whd_wlioctl.h:1375` / c-driver not defined |
| Direction | set (inferred from the name) `embassy/consts.rs:520` |
| Sent by | no driver in these sources sends it. whd lists the name only in its debug string table `whd/src/whd_utils.c:594`. embassy, linux and whd set the country with the named variable (iovar) "country" instead `embassy/control.rs:284` `linux/brcmfmac/cfg80211.c:8494` `whd/src/whd_management.c:190` |
| Payload | not shown by any driver |

### 85 GetPm
| | |
|---|---|
| Names | embassy `GetPm` `embassy/consts.rs:521` / linux `BRCMF_C_GET_PM` `linux/brcmfmac/fwil.h:51` / whd `WLC_GET_PM` `whd/src/include/whd_wlioctl.h:1376` `whd/src/include_helium/whd_wlioctl.h:1376`, also `WHD_IOCTL_GET_PM` = 85 in the public enum `whd_usr_ioctl_get_list_t`, which no code in these sources references `whd/inc/whd_types.h:457` `whd/inc/whd_types.h:449-463` / c-driver `WLC_GET_PM` `c-driver/cyw43_ll.c:178` |
| Direction | get `linux/brcmfmac/cfg80211.c:4252` `c-driver/cyw43_ll.c:1962-1966` |
| Sent by | linux `linux/brcmfmac/cfg80211.c:4252`, whd `whd/src/whd_wifi_api.c:3815`, c-driver `c-driver/cyw43_ll.c:2184`. embassy defines it but never sends it `embassy/consts.rs:521`. Debug string tables list the name: `whd/src/whd_utils.c:595` `c-driver/cyw43_ll.c:876` |
| Payload | 4 bytes, little-endian u32 power-save mode. Values named by the drivers (linux / whd; c-driver uses the whd names with a `CYW43_` prefix): 0 = `PM_OFF` / `NO_POWERSAVE_MODE`, 1 = `PM_MAX` / `PM1_POWERSAVE_MODE`, 2 = `PM_FAST` / `PM2_POWERSAVE_MODE` `linux/include/defs.h:76-78` `whd/inc/whd_types.h:85-87` `c-driver/cyw43_ll.h:187-189` |

- linux — `brcmf_configure_wowl`: saves the current mode into `cfg->wowl.pre_pmmode` before suspend — u32 received, 4 bytes, `le32_to_cpu` via `brcmf_fil_cmd_int_get` — `linux/brcmfmac/cfg80211.c:4252` `linux/brcmfmac/fwil.h:98-104`
- whd — `whd_wifi_get_powersave_mode`: reads the current mode — uint32_t received, 4 bytes, `dtoh32` via `whd_wifi_get_ioctl_value` — `whd/src/whd_wifi_api.c:3815` `whd/src/whd_wifi_api.c:5068-5088`
- whd — `whd_wifi_config_ulp_mode`, inside `#ifdef CYCFG_ULP_SUPPORT_ENABLED`: reads the current mode through `whd_wifi_get_powersave_mode` — same 4-byte uint32_t reply — `whd/src/whd_wifi_api.c:3835` `whd/src/whd_wifi_api.c:3818`
- c-driver — `cyw43_ll_wifi_get_pm`: reads the current mode on the STA interface; the caller `cyw43_wifi_get_pm` packs the result into the low nibble of one word with `cyw43_pm_value` — 4-byte buffer pre-zeroed, `SDPCM_GET` len 4, result read as LE u32 via `cyw43_get_ioctl_u32` — `c-driver/cyw43_ll.c:2184` `c-driver/cyw43_ll.c:1962-1966` `c-driver/cyw43_ctrl.c:535` `c-driver/cyw43_ctrl.c:538` `c-driver/cyw43.h:784-790`

Differences: size and layout agree (4-byte LE u32). c-driver zeroes the request buffer `c-driver/cyw43_ll.c:1964`; linux sends whatever the caller's u32 holds `linux/brcmfmac/fwil.h:102`.

### 86 SetPm
| | |
|---|---|
| Names | embassy `SetPm` `embassy/consts.rs:522` / linux `BRCMF_C_SET_PM` `linux/brcmfmac/fwil.h:52` / whd `WLC_SET_PM` `whd/src/include/whd_wlioctl.h:1377` `whd/src/include_helium/whd_wlioctl.h:1377`, also `WHD_IOCTL_SET_PM` = 86 in the public enum `whd_usr_ioctl_set_list_t`, which no code in these sources references `whd/inc/whd_types.h:475` / c-driver `WLC_SET_PM` `c-driver/cyw43_ll.c:179` |
| Direction | set `embassy/control.rs:362` `c-driver/cyw43_ll.c:1956-1959` |
| Sent by | embassy `embassy/control.rs:362`, linux `linux/brcmfmac/cfg80211.c:3373`, whd `whd/src/whd_wifi_api.c:3799`, c-driver `c-driver/cyw43_ll.c:2165`. Debug string tables list the name: `whd/src/whd_utils.c:596` `c-driver/cyw43_ll.c:877` |
| Payload | 4 bytes, little-endian u32 power-save mode: 0 = off, 1 = PM1 / `PM_MAX`, 2 = PM2 / `PM_FAST` `linux/include/defs.h:76-78` `whd/inc/whd_types.h:85-87` `c-driver/cyw43_ll.h:187-189`. whd and c-driver comments describe 1 as power save "without regard for throughput reduction" and 2 as "with High throughput" `whd/inc/whd_types.h:85-86` `c-driver/cyw43_ll.h:188-189`. A c-driver comment says PM1 is aggressive and reduces throughput, and PM2 saves power only after a period with no wifi activity `c-driver/cyw43_ll.c:2139-2140` |

- embassy — `set_power_management`: sets the mode after the `pm2_sleep_ret`, `bcn_li_bcn`, `bcn_li_dtim`, `assoc_listen` named variables (those only when the mode is 2) — u32 `to_le_bytes`, 4 bytes, iface 0 via `ioctl_set_u32`; value from `PowerManagementMode::mode()`: `ThroughputThrottling` = 1, `None` = 0, all others = 2 — `embassy/control.rs:362` `embassy/control.rs:748-750` `embassy/lib.rs:478-483`
- linux — `brcmf_cfg80211_set_power_mgmt`: `PM_FAST` when enabled, `PM_OFF` when disabled or on a P2P client interface (power save is not enabled after association there); sent only when the vif is up, otherwise the preference is stored — s32 passed as u32, sent as `__le32`, 4 bytes via `brcmf_fil_cmd_int_set` — `linux/brcmfmac/cfg80211.c:3373` `linux/brcmfmac/cfg80211.c:3358-3363` `linux/brcmfmac/cfg80211.c:3366` `linux/brcmfmac/fwil.h:87-93`
- linux — `brcmf_cfg80211_resume`: restores the mode saved before WoWL suspend, only when `cfg->wowl.active` — `__le32`, 4 bytes — `linux/brcmfmac/cfg80211.c:4226` `linux/brcmfmac/cfg80211.c:4220`
- linux — `brcmf_configure_wowl`: forces `PM_MAX` (1) for suspend — `__le32`, 4 bytes — `linux/brcmfmac/cfg80211.c:4253`
- linux — `brcmf_config_dongle`, run once until `dongle_up`: `PM_FAST` or `PM_OFF` from `cfg->pwr_save`, right after `BRCMF_C_UP` and the scan-time setup — `__le32`, 4 bytes — `linux/brcmfmac/cfg80211.c:8022` `linux/brcmfmac/cfg80211.c:8000`
- whd — `whd_wifi_enable_powersave`: sets PM1 — uint32_t `htod32(PM1_POWERSAVE_MODE)`, 4-byte command buffer — `whd/src/whd_wifi_api.c:3799` `whd/src/whd_wifi_api.c:3795-3797`
- whd — `whd_wifi_enable_powersave_with_throughput`: sets PM2 after the `pm2_sleep_ret` named variable. Start-up (`whd_wifi_on`) calls it with `DEFAULT_PM2_SLEEP_RET_TIME` for every chip id other than 43909, 43907 and 54907, so whd sends value 2 during start-up on any chip whose id is not one of those three (inferred for this chip: its id is not shown at these lines). `whd_wifi_config_ulp_mode` also calls it, inside `#ifdef CYCFG_ULP_SUPPORT_ENABLED` — uint32_t `htod32(PM2_POWERSAVE_MODE)`, 4 bytes — `whd/src/whd_wifi_api.c:3919` `whd/src/whd_wifi_api.c:3915-3917` `whd/src/whd_management.c:548-550` `whd/src/whd_management.c:565` `whd/src/whd_wifi_api.c:3843` `whd/src/whd_wifi_api.c:3818`
- whd — `whd_wifi_disable_powersave`: sets no power save; start-up (`whd_wifi_on`) calls it for chip ids 43909, 43907, 54907 — uint32_t `htod32(NO_POWERSAVE_MODE)`, 4 bytes — `whd/src/whd_wifi_api.c:3937` `whd/src/whd_wifi_api.c:3933-3936` `whd/src/whd_management.c:548-550`
- c-driver — `cyw43_ll_wifi_pm`: sets the mode on the STA interface after the `pm2_sleep_ret`, `bcn_li_*`, `assoc_listen` named variables. Its caller `cyw43_wifi_pm` takes the mode from the low 4 bits of its packed argument; `cyw43_wifi_set_up` calls `cyw43_wifi_pm(self, CYW43_DEFAULT_PM)` after `cyw43_wifi_on` succeeds, when no interface was up before — LE u32, `SDPCM_SET` len 4 via `cyw43_set_ioctl_u32` — `c-driver/cyw43_ll.c:2165` `c-driver/cyw43_ll.c:1956-1959` `c-driver/cyw43_ctrl.c:509` `c-driver/cyw43_ctrl.c:515` `c-driver/cyw43_ctrl.c:562-567`

Differences: size and layout agree (4-byte LE u32). Naming differs for the same numbers: linux calls 1 `PM_MAX` and 2 `PM_FAST`; whd and c-driver call them PM1 and PM2 `linux/include/defs.h:76-78` `whd/inc/whd_types.h:85-87` `c-driver/cyw43_ll.h:187-189`. Ordering differs: embassy, whd (PM2 path) and c-driver send `pm2_sleep_ret` before this command `embassy/control.rs:357` `embassy/control.rs:362` `whd/src/whd_wifi_api.c:3905-3906` `whd/src/whd_wifi_api.c:3919` `c-driver/cyw43_ll.c:2148` `c-driver/cyw43_ll.c:2165`; linux sends it after `linux/brcmfmac/cfg80211.c:3373` `linux/brcmfmac/cfg80211.c:3381`. Condition differs: embassy sends the named variables only when the mode is 2; c-driver sends them for every mode `embassy/control.rs:356-361` `c-driver/cyw43_ll.c:2148-2156`.

### 87 GetWake
| | |
|---|---|
| Names | embassy `GetWake` `embassy/consts.rs:523` / linux not defined / whd `WLC_GET_WAKE` `whd/src/include/whd_wlioctl.h:1378` `whd/src/include_helium/whd_wlioctl.h:1378` / c-driver not defined |
| Direction | get (inferred from the name) `embassy/consts.rs:523` |
| Sent by | no driver in these sources sends it. whd lists the name only in its debug string table `whd/src/whd_utils.c:597` |
| Payload | not shown by any driver |

### 88 SetWake
| | |
|---|---|
| Names | embassy `SetWake` `embassy/consts.rs:524` / linux not defined / whd `WLC_SET_WAKE` `whd/src/include/whd_wlioctl.h:1379` `whd/src/include_helium/whd_wlioctl.h:1379` / c-driver not defined |
| Direction | set (inferred from the name) `embassy/consts.rs:524` |
| Sent by | no driver in these sources sends it. whd lists the name only in its debug string table `whd/src/whd_utils.c:598` |
| Payload | not shown by any driver |

### 90 GetForcelink
| | |
|---|---|
| Names | embassy `GetForcelink` `embassy/consts.rs:525` / linux not defined / whd `WLC_GET_FORCELINK` `whd/src/include/whd_wlioctl.h:1380` `whd/src/include_helium/whd_wlioctl.h:1380` / c-driver not defined |
| Direction | get (inferred from the name) `embassy/consts.rs:525` |
| Sent by | no driver in these sources sends it. whd lists the name in its debug string table `whd/src/whd_utils.c:599` and derives `OID_WL_GET_FORCELINK` = `WL_OID_BASE` (0xFFE41420) + `WLC_GET_FORCELINK`, which nothing in these sources uses `whd/src/include/whd_wlioctl.h:1589` `whd/src/include/whd_wlioctl.h:1591` `whd/src/include_helium/whd_wlioctl.h:1591` |
| Payload | not shown by any driver |

### 91 SetForcelink
| | |
|---|---|
| Names | embassy `SetForcelink` `embassy/consts.rs:526` / linux not defined / whd `WLC_SET_FORCELINK` `whd/src/include/whd_wlioctl.h:1381` `whd/src/include_helium/whd_wlioctl.h:1381` / c-driver not defined |
| Direction | set (inferred from the name) `embassy/consts.rs:526` |
| Sent by | no driver in these sources sends it. whd lists the name in its debug string table `whd/src/whd_utils.c:600` and derives `OID_WL_SET_FORCELINK` = `WL_OID_BASE` (0xFFE41420) + `WLC_SET_FORCELINK`, which nothing in these sources uses `whd/src/include/whd_wlioctl.h:1589` `whd/src/include/whd_wlioctl.h:1592` `whd/src/include_helium/whd_wlioctl.h:1592` |
| Payload | not shown by any driver |

### 92 FreqAccuracy
| | |
|---|---|
| Names | embassy `FreqAccuracy` `embassy/consts.rs:527` / linux not defined / whd `WLC_FREQ_ACCURACY` `whd/src/include/whd_wlioctl.h:1382` `whd/src/include_helium/whd_wlioctl.h:1382` / c-driver not defined |
| Direction | unknown (the name does not say) `embassy/consts.rs:527` |
| Sent by | no driver in these sources sends it. whd lists the name only in its debug string table `whd/src/whd_utils.c:601` |
| Payload | not shown by any driver |

### 93 CarrierSuppress
| | |
|---|---|
| Names | embassy `CarrierSuppress` `embassy/consts.rs:528` / linux not defined / whd `WLC_CARRIER_SUPPRESS` `whd/src/include/whd_wlioctl.h:1383` `whd/src/include_helium/whd_wlioctl.h:1383` / c-driver not defined |
| Direction | unknown (the name does not say) `embassy/consts.rs:528` |
| Sent by | no driver in these sources sends it. whd lists the name only in its debug string table `whd/src/whd_utils.c:602` |
| Payload | not shown by any driver |

### 94 GetPhyreg
| | |
|---|---|
| Names | embassy `GetPhyreg` `embassy/consts.rs:529` / linux not defined / whd `WLC_GET_PHYREG` `whd/src/include/whd_wlioctl.h:1384` `whd/src/include_helium/whd_wlioctl.h:1384` / c-driver not defined |
| Direction | get (inferred from the name) `embassy/consts.rs:529` |
| Sent by | no driver in these sources sends it. whd lists the name only in its debug string table `whd/src/whd_utils.c:603` |
| Payload | not shown by any driver |

### 95 SetPhyreg
| | |
|---|---|
| Names | embassy `SetPhyreg` `embassy/consts.rs:530` / linux not defined / whd `WLC_SET_PHYREG` `whd/src/include/whd_wlioctl.h:1385` `whd/src/include_helium/whd_wlioctl.h:1385` / c-driver not defined |
| Direction | set (inferred from the name) `embassy/consts.rs:530` |
| Sent by | no driver in these sources sends it. whd lists the name only in its debug string table `whd/src/whd_utils.c:604` |
| Payload | not shown by any driver |

### 96 GetRadioreg
| | |
|---|---|
| Names | embassy `GetRadioreg` `embassy/consts.rs:531` / linux not defined / whd `WLC_GET_RADIOREG` `whd/src/include/whd_wlioctl.h:1386` `whd/src/include_helium/whd_wlioctl.h:1386` / c-driver not defined |
| Direction | get (inferred from the name) `embassy/consts.rs:531` |
| Sent by | no driver in these sources sends it. whd lists the name only in its debug string table `whd/src/whd_utils.c:605` |
| Payload | not shown by any driver |

### 97 SetRadioreg
| | |
|---|---|
| Names | embassy `SetRadioreg` `embassy/consts.rs:532` / linux not defined / whd `WLC_SET_RADIOREG` `whd/src/include/whd_wlioctl.h:1387` `whd/src/include_helium/whd_wlioctl.h:1387` / c-driver not defined |
| Direction | set (inferred from the name) `embassy/consts.rs:532` |
| Sent by | no driver in these sources sends it. whd lists the name only in its debug string table `whd/src/whd_utils.c:606` |
| Payload | not shown by any driver |

### 98 GetRevinfo
| | |
|---|---|
| Names | embassy `GetRevinfo` `embassy/consts.rs:533` / linux `BRCMF_C_GET_REVINFO` `linux/brcmfmac/fwil.h:53` / whd `WLC_GET_REVINFO` `whd/src/include/whd_wlioctl.h:1388` `whd/src/include_helium/whd_wlioctl.h:1388` / c-driver not defined |
| Direction | get `linux/brcmfmac/common.c:307` |
| Sent by | linux `linux/brcmfmac/common.c:307`. whd defines a record for it but sends nothing (debug string table only `whd/src/whd_utils.c:607`). embassy and c-driver never send it `embassy/consts.rs:533` |
| Payload | Record of 32-bit fields, no padding (inferred: every member is 4 bytes). linux declares each field `__le32`; whd declares each `uint32_t` and has no code that converts them. linux record `brcmf_rev_info_le`: 17 fields, 68 bytes (computed) `linux/brcmfmac/fwil_types.h:791-809`. whd record `wlc_rev_info_t`: 15 fields, 60 bytes (computed) `whd/src/include/whd_wlioctl.h:1006-1023` `whd/src/include_helium/whd_wlioctl.h:1007-1024`. Fields, each 4 bytes, as offset `name` (meaning per the linux kerneldoc `linux/brcmfmac/fwil_types.h:771-789`); offsets are field index times 4 (computed): 0 `vendorid` (PCI vendor id); 4 `deviceid` (device id of chip); 8 `radiorev` (radio revision); 12 `chiprev` (chip revision); 16 `corerev` (core revision); 20 `boardid` (board identifier); 24 `boardvendor` (board vendor); 28 `boardrev` (board revision); 32 `driverrev` (driver version); 36 `ucoderev` (microcode version); 40 `bus` (bus type); 44 `chipnum` (chip number); 48 `phytype` (phy type); 52 `phyrev` (phy revision); 56 `anarev` (anacore rev); then in the linux record only: 60 `chippkg` (chip package info); 64 `nvramrev` (nvram revision number) `linux/brcmfmac/fwil_types.h:791-809` `whd/src/include/whd_wlioctl.h:1006-1023` |

- linux — `brcmf_c_preinit_dcmds`: reads device revision info at start-up. It copies 15 of the fields into `drvr->revinfo`, converting each with `le32_to_cpu`; `chiprev` and `chipnum` are the two not copied there, and are used only to fill `bus->chip` and `bus->chiprev` when not already known. On failure it sets the chip name to "UNKNOWN" and continues — record `brcmf_rev_info_le` received, request length `sizeof(revinfo)` = 68 bytes — `linux/brcmfmac/common.c:307` `linux/brcmfmac/common.c:271` `linux/brcmfmac/common.c:308` `linux/brcmfmac/common.c:313-327` `linux/brcmfmac/common.c:330-333` `linux/brcmfmac/common.c:309-311`

Differences: linux's record has two more trailing fields (`chippkg`, `nvramrev`) than whd's: 68 bytes against 60 `linux/brcmfmac/fwil_types.h:791-809` `whd/src/include/whd_wlioctl.h:1006-1023`. whd also defines `WL_REV_INFO_LEGACY_LENGTH` 48 `whd/src/include/whd_wlioctl.h:1024` `whd/src/include_helium/whd_wlioctl.h:1025`; 48 bytes equals the first 12 fields, through `chipnum` (inferred, arithmetic only). No driver in these sources shows the length of the reply actually received.

### 99 GetUcantdiv
| | |
|---|---|
| Names | embassy `GetUcantdiv` `embassy/consts.rs:534` / linux not defined / whd `WLC_GET_UCANTDIV` `whd/src/include/whd_wlioctl.h:1389` `whd/src/include_helium/whd_wlioctl.h:1389` / c-driver not defined |
| Direction | get (inferred from the name) `embassy/consts.rs:534` |
| Sent by | no driver in these sources sends it. whd lists the name only in its debug string table `whd/src/whd_utils.c:608` |
| Payload | not shown by any driver |

### 100 SetUcantdiv
| | |
|---|---|
| Names | embassy `SetUcantdiv` `embassy/consts.rs:535` / linux not defined / whd `WLC_SET_UCANTDIV` `whd/src/include/whd_wlioctl.h:1390` `whd/src/include_helium/whd_wlioctl.h:1390` / c-driver not defined |
| Direction | set (inferred from the name) `embassy/consts.rs:535` |
| Sent by | no driver in these sources sends it. whd lists the name only in its debug string table `whd/src/whd_utils.c:609` |
| Payload | not shown by any driver |

### 101 RReg
| | |
|---|---|
| Names | embassy `RReg` `embassy/consts.rs:536` / linux not defined / whd `WLC_R_REG` `whd/src/include/whd_wlioctl.h:1391` `whd/src/include_helium/whd_wlioctl.h:1391` / c-driver not defined |
| Direction | unknown; get is a guess from the `R_` prefix only (inferred) `whd/src/include/whd_wlioctl.h:1391` |
| Sent by | no driver in these sources sends it. whd lists the name only in its debug string table `whd/src/whd_utils.c:610` |
| Payload | not shown by any driver |

### 102 WReg
| | |
|---|---|
| Names | embassy `WReg` `embassy/consts.rs:537` / linux not defined / whd `WLC_W_REG` `whd/src/include/whd_wlioctl.h:1392` `whd/src/include_helium/whd_wlioctl.h:1392` / c-driver not defined |
| Direction | unknown; set is a guess from the `W_` prefix only (inferred) `whd/src/include/whd_wlioctl.h:1392` |
| Sent by | no driver in these sources sends it. whd lists the name only in its debug string table `whd/src/whd_utils.c:611` |
| Payload | not shown by any driver |

### 105 GetMacmode
| | |
|---|---|
| Names | embassy `GetMacmode` `embassy/consts.rs:538` / linux not defined / whd `WLC_GET_MACMODE` `whd/src/include/whd_wlioctl.h:1393` `whd/src/include_helium/whd_wlioctl.h:1393` / c-driver not defined |
| Direction | get (inferred from the name) `embassy/consts.rs:538` |
| Sent by | no driver in these sources sends it. whd lists the name only in its debug string table `whd/src/whd_utils.c:612` |
| Payload | not shown by any driver. whd defines `WLC_MACMODE_DISABLED` 0, `WLC_MACMODE_DENY` 1, `WLC_MACMODE_ALLOW` 2, used by no code in these sources; that they are this command's values is (inferred) from the name only `whd/src/include/whd_wlioctl.h:1670-1672` `whd/src/include_helium/whd_wlioctl.h:1684-1686` |

### 106 SetMacmode
| | |
|---|---|
| Names | embassy `SetMacmode` `embassy/consts.rs:539` / linux not defined / whd `WLC_SET_MACMODE` `whd/src/include/whd_wlioctl.h:1394` `whd/src/include_helium/whd_wlioctl.h:1394` / c-driver not defined |
| Direction | set (inferred from the name) `embassy/consts.rs:539` |
| Sent by | no driver in these sources sends it. whd lists the name only in its debug string table `whd/src/whd_utils.c:613` |
| Payload | not shown by any driver. whd defines `WLC_MACMODE_DISABLED` 0, `WLC_MACMODE_DENY` 1, `WLC_MACMODE_ALLOW` 2, used by no code in these sources; that they are this command's values is (inferred) from the name only `whd/src/include/whd_wlioctl.h:1670-1672` `whd/src/include_helium/whd_wlioctl.h:1684-1686` |

### 107 GetMonitor
| | |
|---|---|
| Names | embassy `GetMonitor` `embassy/consts.rs:540` / linux `BRCMF_C_GET_MONITOR` `linux/brcmfmac/fwil.h:54` / whd `WLC_GET_MONITOR` `whd/src/include/whd_wlioctl.h:1395` `whd/src/include_helium/whd_wlioctl.h:1395` / c-driver not defined |
| Direction | get `linux/brcmfmac/core.c:711` |
| Sent by | linux only `linux/brcmfmac/core.c:711`. whd lists the name only in its debug string table `whd/src/whd_utils.c:614`. embassy and c-driver have no call site `embassy/consts.rs:540` |
| Payload | 4 bytes, little-endian u32. linux treats 0 as monitor mode off and non-zero as on `linux/brcmfmac/core.c:715` |

- linux — `brcmf_net_mon_open`: checks whether monitor mode is already on; non-zero returns `-EEXIST` — u32 received, 4 bytes, `le32_to_cpu` via `brcmf_fil_cmd_int_get` — `linux/brcmfmac/core.c:711` `linux/brcmfmac/fwil.h:98-104`

### 108 SetMonitor
| | |
|---|---|
| Names | embassy `SetMonitor` `embassy/consts.rs:541` / linux `BRCMF_C_SET_MONITOR` `linux/brcmfmac/fwil.h:55` / whd `WLC_SET_MONITOR` `whd/src/include/whd_wlioctl.h:1396` `whd/src/include_helium/whd_wlioctl.h:1396` / c-driver `WLC_SET_MONITOR` (inside `#if 0`) `c-driver/cyw43_ll.c:1979` and `CYW43_IOCTL_SET_MONITOR` (0xd9 = 108 * 2 + 1) `c-driver/cyw43_ll.h:42`. c-driver's `CYW43_IOCTL_*` numbers for the generic `cyw43_ll_ioctl` entry point use the bottom bit as the "set" flag and the remaining bits as the command number: 0xd9 >> 1 = 108, low bit 1 = set `c-driver/cyw43_ll.h:30` `c-driver/cyw43_ll.c:1329`. No call site of `CYW43_IOCTL_SET_MONITOR` was found in c-driver or pico-sdk `c-driver/cyw43_ll.h:42` |
| Direction | set `linux/brcmfmac/core.c:721` |
| Sent by | linux `linux/brcmfmac/core.c:721`. c-driver has a call site only in compiled-out code `c-driver/cyw43_ll.c:1978`. whd lists the name only in its debug string table `whd/src/whd_utils.c:615`. embassy has no call site `embassy/consts.rs:541` |
| Payload | 4 bytes, little-endian u32. linux sends 3 for on and 0 for off `linux/brcmfmac/core.c:720` `linux/brcmfmac/core.c:737`. The meaning of the individual bits of 3 is not stated in these sources |

- linux — `brcmf_net_mon_open`: turns monitor mode on — u32 value 3 sent as `__le32`, 4 bytes via `brcmf_fil_cmd_int_set` — `linux/brcmfmac/core.c:721` `linux/brcmfmac/fwil.h:87-93`
- linux — `brcmf_net_mon_stop`: turns monitor mode off — u32 value 0 sent as `__le32`, 4 bytes — `linux/brcmfmac/core.c:738`
- c-driver (compiled out, `#if 0` to `#endif`) — `cyw43_set_monitor_mode`: sets monitor mode after the "allmulti" named variable; it also sets `self->is_monitor_mode`, which appears nowhere else in c-driver — caller's int sent unchanged as LE u32, `SDPCM_SET` len 4 on the STA interface via `cyw43_set_ioctl_u32` — `c-driver/cyw43_ll.c:1991` `c-driver/cyw43_ll.c:1978` `c-driver/cyw43_ll.c:1997` `c-driver/cyw43_ll.c:1989` `c-driver/cyw43_ll.c:1956-1959`

Differences: size and layout agree (4-byte LE u32). linux sends fixed values 3 and 0; the disabled c-driver code passes the caller's value through `linux/brcmfmac/core.c:720` `c-driver/cyw43_ll.c:1991`.

### 109 GetGmode
| | |
|---|---|
| Names | embassy `GetGmode` `embassy/consts.rs:542` / linux not defined / whd `WLC_GET_GMODE` `whd/src/include/whd_wlioctl.h:1397` `whd/src/include_helium/whd_wlioctl.h:1397` / c-driver not defined |
| Direction | get (inferred from the name) `embassy/consts.rs:542` |
| Sent by | no driver in these sources sends it. whd lists the name only in its debug string table `whd/src/whd_utils.c:616` |
| Payload | not shown by any driver. The same 4-byte gmode value as command 110 is a pairing guess (inferred) |

### 110 SetGmode
| | |
|---|---|
| Names | embassy `SetGmode` `embassy/consts.rs:543` / linux not defined / whd `WLC_SET_GMODE` `whd/src/include/whd_wlioctl.h:1398` `whd/src/include_helium/whd_wlioctl.h:1398` / c-driver `WLC_SET_GMODE` `c-driver/cyw43_ll.c:180` |
| Direction | set `embassy/control.rs:328` `c-driver/cyw43_ll.c:2170` |
| Sent by | embassy `embassy/control.rs:328`, whd `whd/src/whd_management.c:589`, c-driver `c-driver/cyw43_ll.c:2170` `c-driver/cyw43_ll.c:2443`. linux has no constant for 110 (its list goes from 108 to 114) `linux/brcmfmac/fwil.h:55-56`. Debug string tables list the name: `whd/src/whd_utils.c:617`, `whd/src/whd_utils.c:1061-1063` (matched by the literal 110), `c-driver/cyw43_ll.c:878` |
| Payload | 4 bytes, little-endian u32 802.11g mode. whd names the values: 0 `GMODE_LEGACY_B`, 1 `GMODE_AUTO`, 2 `GMODE_ONLY`, 3 `GMODE_B_DEFERRED`, 4 `GMODE_PERFORMANCE`, 5 `GMODE_LRS`, 6 `GMODE_MAX` `whd/src/include/whd_wlioctl.h:1673-1679` `whd/src/include_helium/whd_wlioctl.h:1687-1693`. Every call site sends 1 `embassy/control.rs:328` `whd/src/whd_management.c:588` `c-driver/cyw43_ll.c:2169` `c-driver/cyw43_ll.c:2443` |

- embassy — init, after bringing the interface up: gmode auto, followed by `SetBand` = 0 — u32 value 1, `to_le_bytes`, 4 bytes, iface 0 via `ioctl_set_u32` — `embassy/control.rs:328` `embassy/control.rs:329` `embassy/control.rs:748-750`
- whd — `whd_wifi_on`: sets `GMODE_AUTO`; only when `PROTO_MSGBUF` is not defined. A whd comment at the call site warns that if the bus interrupts do not work, this is a point where the system can hit a timeout — uint32_t `htod32(GMODE_AUTO)` = 1, 4-byte command buffer — `whd/src/whd_management.c:589` `whd/src/whd_management.c:580` `whd/src/whd_management.c:582-588` `whd/src/whd_management.c:592`
- c-driver — `cyw43_ll_wifi_pm`: sets `GMODE_AUTO` on the STA interface right after `WLC_SET_PM`, followed by `WLC_SET_BAND` = 0 — LE u32 value 1, `SDPCM_SET` len 4 — `c-driver/cyw43_ll.c:2170` `c-driver/cyw43_ll.c:2168-2170` `c-driver/cyw43_ll.c:2172-2173`
- c-driver — `cyw43_ll_wifi_ap_init`, reached from `cyw43_wifi_ap_init`: sets gmode auto on the AP interface — LE u32 value 1, `SDPCM_SET` len 4 via `cyw43_set_ioctl_u32` — `c-driver/cyw43_ll.c:2443` `c-driver/cyw43_ll.c:1956-1959` `c-driver/cyw43_ctrl.c:749`

Differences: none in size, layout or value (all send 4-byte LE u32 = 1). When it is sent differs: embassy and whd send it once at start-up `embassy/control.rs:328` `whd/src/whd_management.c:589`; c-driver sends it on every `cyw43_wifi_pm` call, because that calls `cyw43_ll_wifi_pm` `c-driver/cyw43_ctrl.c:515` `c-driver/cyw43_ll.c:2170`; one such call is in `cyw43_wifi_set_up` at first bring-up `c-driver/cyw43_ctrl.c:567`. Interface differs: embassy sends on iface 0 `embassy/control.rs:328`; c-driver sends on the STA interface in the PM path and on the AP interface in AP init `c-driver/cyw43_ll.c:2170` `c-driver/cyw43_ll.c:2443`.

### 111 GetLegacyErp
| | |
|---|---|
| Names | embassy `GetLegacyErp` / linux not defined / whd `WLC_GET_LEGACY_ERP` / c-driver not defined. `embassy/consts.rs:544` `whd/src/include/whd_wlioctl.h:1399` `whd/src/include_helium/whd_wlioctl.h:1399` `whd/src/whd_utils.c:618` |
| Direction | get (inferred from the name; no call site) |
| Sent by | no driver in these sources sends it |
| Payload | not shown by any driver |

### 112 SetLegacyErp
| | |
|---|---|
| Names | embassy `SetLegacyErp` / linux not defined / whd `WLC_SET_LEGACY_ERP` / c-driver not defined. `embassy/consts.rs:545` `whd/src/include/whd_wlioctl.h:1400` `whd/src/include_helium/whd_wlioctl.h:1400` `whd/src/whd_utils.c:619` |
| Direction | set (inferred from the name; no call site) |
| Sent by | no driver in these sources sends it |
| Payload | not shown by any driver |

### 113 GetRxAnt
| | |
|---|---|
| Names | embassy `GetRxAnt` / linux not defined / whd `WLC_GET_RX_ANT` / c-driver not defined. `embassy/consts.rs:546` `whd/src/include/whd_wlioctl.h:1401` `whd/src/include_helium/whd_wlioctl.h:1401` `whd/src/whd_utils.c:620` |
| Direction | get (inferred from the name; no call site) |
| Sent by | no driver in these sources sends it |
| Payload | not shown by any driver |

### 114 GetCurrRateset
| | |
|---|---|
| Names | embassy `GetCurrRateset` / linux `BRCMF_C_GET_CURR_RATESET` / whd `WLC_GET_CURR_RATESET` / c-driver not defined. `embassy/consts.rs:547` `linux/brcmfmac/fwil.h:56` `whd/src/include/whd_wlioctl.h:1402` `whd/src/include_helium/whd_wlioctl.h:1402` `whd/src/whd_utils.c:621` |
| Direction | get (inferred from the name; no call site) |
| Sent by | no driver in these sources sends it. linux defines the constant and does not use it. `linux/brcmfmac/fwil.h:56` |
| Payload | not shown by any driver |

### 115 GetScansuppress
| | |
|---|---|
| Names | embassy `GetScansuppress` / linux not defined / whd `WLC_GET_SCANSUPPRESS` / c-driver not defined. `embassy/consts.rs:548` `whd/src/include/whd_wlioctl.h:1403` `whd/src/include_helium/whd_wlioctl.h:1403` `whd/src/whd_utils.c:622` |
| Direction | get (inferred from the name; no call site) |
| Sent by | no driver in these sources sends it |
| Payload | not shown by any driver |

### 116 SetScansuppress
| | |
|---|---|
| Names | embassy `SetScansuppress` / linux not defined / whd `WLC_SET_SCANSUPPRESS` / c-driver not defined. `embassy/consts.rs:549` `whd/src/include/whd_wlioctl.h:1404` `whd/src/include_helium/whd_wlioctl.h:1404` `whd/src/whd_utils.c:623` |
| Direction | set (inferred from the name; no call site) |
| Sent by | no driver in these sources sends it. whd has a second name table, `whd_ioctl_info_to_string`, that maps the number 116 to the string "WLC_SET_SCANSUPPRESS". whd and embassy comments on event status SUPPRESS (12) name this command as the cause: scanning disabled by the user. `whd/src/whd_utils.c:1065-1067` `whd/inc/whd_events.h:73` `whd/src/include/whd_events_int.h:218` `embassy/consts.rs:281-282` |
| Payload | not shown by any driver |

### 117 GetAp
| | |
|---|---|
| Names | embassy `GetAp` / linux `BRCMF_C_GET_AP` / whd `WLC_GET_AP` / c-driver not defined. `embassy/consts.rs:550` `linux/brcmfmac/fwil.h:57` `whd/src/include/whd_wlioctl.h:1405` `whd/src/include_helium/whd_wlioctl.h:1405` `whd/src/whd_utils.c:624` |
| Direction | get (inferred from the name; no call site) |
| Sent by | no driver in these sources sends it. linux defines the constant and does not use it. whd lists it in the macro `WL_SEQ_CMDS_GET_IOCTL_FILTER` with `WLC_GET_MAGIC`, `WLC_GET_VERSION` and `WLC_GET_INSTANCE`; the macro is defined and not used in the whd tree. `linux/brcmfmac/fwil.h:57` `whd/src/include/whd_wlioctl.h:3677-3681` `whd/src/include_helium/whd_wlioctl.h:3836-3840` |
| Payload | not shown by any driver |

### 118 SetAp
| | |
|---|---|
| Names | embassy `SetAp` / linux `BRCMF_C_SET_AP` / whd `WLC_SET_AP` / c-driver not defined. `embassy/consts.rs:551` `linux/brcmfmac/fwil.h:58` `whd/src/include/whd_wlioctl.h:1406` `whd/src/include_helium/whd_wlioctl.h:1406` `whd/src/whd_utils.c:625` |
| Direction | set |
| Sent by | embassy, linux, whd. c-driver does not define or send it. `embassy/control.rs:572` `linux/brcmfmac/cfg80211.c:5383` `whd/src/whd_ap.c:303` |
| Payload | 32-bit integer, 4 bytes, little-endian as sent by embassy and linux; whd writes it in host byte order. The senders use 1 to turn AP mode on and 0 to turn it off. All three senders send exactly 4 bytes. `embassy/control.rs:748-750` `linux/brcmfmac/fwil.h:87-93` `whd/src/whd_ap.c:300-302` |

- embassy — `start_ap`: turn AP mode on, after `apsta` = 0, up, and SetAuth = open — u32 = 1, 4 bytes little-endian (`ioctl_set_u32`), interface 0 — `embassy/control.rs:572` `embassy/control.rs:563-569` `embassy/control.rs:748-750`
- embassy — `close_ap`: turn AP mode off, after bss down — u32 = 0, 4 bytes little-endian, interface 0 — `embassy/control.rs:644` `embassy/control.rs:641`
- linux — `brcmf_cfg80211_start_ap`: enable AP mode when the device role is `NL80211_IFTYPE_AP` — `__le32` = 1, 4 bytes (`brcmf_fil_cmd_int_set`); a linux comment after the call says firmware 10.x requires the channel to be set after enabling AP and before bringing the interface up — `linux/brcmfmac/cfg80211.c:5383` `linux/brcmfmac/fwil.h:87-93` `linux/brcmfmac/cfg80211.c:5390-5391`
- linux — `brcmf_cfg80211_stop_ap`: leave AP mode, after SET_SSID (empty) and DOWN; not reached for an MBSS vif, which returns after DOWN — `__le32` = 0, 4 bytes — `linux/brcmfmac/cfg80211.c:5550` `linux/brcmfmac/cfg80211.c:5533-5536`
- whd — `whd_create_softap_interface`: turn AP on, only when the AP is on the primary interface — `uint32_t` = 1 in a 4-byte command buffer, host byte order, no `htod32` at this site — `whd/src/whd_ap.c:303` `whd/src/whd_ap.c:300-302`
- whd — `whd_wifi_stop_ap`: turn AP off, only when the AP is on the primary interface; skipped under `COMPONENT_SDIO_HM` — `uint32_t` = 0 in a 4-byte command buffer, host byte order — `whd/src/whd_ap.c:704` `whd/src/whd_ap.c:701-703`

Differences: size and layout agree (4 bytes). whd writes the value without `htod32`, unlike its generic helper `whd_wifi_set_ioctl_value`; the bytes are the same on a little-endian host, where whd defines `htod32` as the identity. `whd/src/whd_ap.c:300-302` `whd/src/whd_wifi_api.c:5062` `whd/src/include/whd_endian.h:54`

### 119 GetEapRestrict
| | |
|---|---|
| Names | embassy `GetEapRestrict` / linux not defined / whd `WLC_GET_EAP_RESTRICT` / c-driver not defined. `embassy/consts.rs:552` `whd/src/include/whd_wlioctl.h:1407` `whd/src/include_helium/whd_wlioctl.h:1407` `whd/src/whd_utils.c:626` |
| Direction | get (inferred from the name; no call site) |
| Sent by | no driver in these sources sends it |
| Payload | not shown by any driver |

### 120 SetEapRestrict
| | |
|---|---|
| Names | embassy `SetEapRestrict` / linux not defined / whd `WLC_SET_EAP_RESTRICT` / c-driver not defined. `embassy/consts.rs:553` `whd/src/include/whd_wlioctl.h:1408` `whd/src/include_helium/whd_wlioctl.h:1408` `whd/src/whd_utils.c:627` |
| Direction | set (inferred from the name; no call site) |
| Sent by | no driver in these sources sends it |
| Payload | not shown by any driver |

### 121 ScbAuthorize
| | |
|---|---|
| Names | embassy `ScbAuthorize` / linux `BRCMF_C_SET_SCB_AUTHORIZE` (linux adds `SET_`) / whd `WLC_SCB_AUTHORIZE` / c-driver not defined. `embassy/consts.rs:554` `linux/brcmfmac/fwil.h:59` `whd/src/include/whd_wlioctl.h:1409` `whd/src/include_helium/whd_wlioctl.h:1409` `whd/src/whd_utils.c:628` |
| Direction | set |
| Sent by | linux only. whd defines it and lists it in its name table but does not send it; embassy and c-driver do not send it. `linux/brcmfmac/cfg80211.c:5643` `whd/src/whd_utils.c:628` |
| Payload | station MAC address, 6 bytes, in address byte order (as sent by linux, the only sender). `linux/brcmfmac/cfg80211.c:5643` |

- linux — `brcmf_cfg80211_change_station`: authorize a station when `NL80211_STA_FLAG_AUTHORIZED` is set; the call is skipped for an all-zero MAC — 6-byte MAC (`ETH_ALEN`) via `brcmf_fil_cmd_data_set` — `linux/brcmfmac/cfg80211.c:5643` `linux/brcmfmac/cfg80211.c:5635-5637`

### 122 ScbDeauthorize
| | |
|---|---|
| Names | embassy `ScbDeauthorize` / linux `BRCMF_C_SET_SCB_DEAUTHORIZE` (linux adds `SET_`) / whd `WLC_SCB_DEAUTHORIZE` / c-driver not defined. `embassy/consts.rs:555` `linux/brcmfmac/fwil.h:60` `whd/src/include/whd_wlioctl.h:1410` `whd/src/include_helium/whd_wlioctl.h:1410` `whd/src/whd_utils.c:629` |
| Direction | set |
| Sent by | linux only. whd defines it and lists it in its name table but does not send it; embassy and c-driver do not send it. `linux/brcmfmac/cfg80211.c:5646` `whd/src/whd_utils.c:629` |
| Payload | station MAC address, 6 bytes, in address byte order (as sent by linux, the only sender). `linux/brcmfmac/cfg80211.c:5646` |

- linux — `brcmf_cfg80211_change_station`: de-authorize a station when `NL80211_STA_FLAG_AUTHORIZED` is cleared; the call is skipped for an all-zero MAC — 6-byte MAC (`ETH_ALEN`) via `brcmf_fil_cmd_data_set` — `linux/brcmfmac/cfg80211.c:5646` `linux/brcmfmac/cfg80211.c:5635-5637`

### 123 GetWdslist
| | |
|---|---|
| Names | embassy `GetWdslist` / linux not defined / whd `WLC_GET_WDSLIST` / c-driver not defined. `embassy/consts.rs:556` `whd/src/include/whd_wlioctl.h:1411` `whd/src/include_helium/whd_wlioctl.h:1411` `whd/src/whd_utils.c:630` |
| Direction | get (inferred from the name; no call site) |
| Sent by | no driver in these sources sends it |
| Payload | not shown by any driver |

### 124 SetWdslist
| | |
|---|---|
| Names | embassy `SetWdslist` / linux not defined / whd `WLC_SET_WDSLIST` / c-driver not defined. `embassy/consts.rs:557` `whd/src/include/whd_wlioctl.h:1412` `whd/src/include_helium/whd_wlioctl.h:1412` `whd/src/whd_utils.c:631` |
| Direction | set (inferred from the name; no call site) |
| Sent by | no driver in these sources sends it |
| Payload | not shown by any driver |

### 125 GetAtim
| | |
|---|---|
| Names | embassy `GetAtim` / linux not defined / whd `WLC_GET_ATIM` / c-driver not defined. `embassy/consts.rs:558` `whd/src/include/whd_wlioctl.h:1413` `whd/src/include_helium/whd_wlioctl.h:1413` `whd/src/whd_utils.c:632` |
| Direction | get (inferred from the name; no call site) |
| Sent by | no driver in these sources sends it |
| Payload | not shown by any driver |

### 126 SetAtim
| | |
|---|---|
| Names | embassy `SetAtim` / linux not defined / whd `WLC_SET_ATIM` / c-driver not defined. `embassy/consts.rs:559` `whd/src/include/whd_wlioctl.h:1414` `whd/src/include_helium/whd_wlioctl.h:1414` `whd/src/whd_utils.c:633` |
| Direction | set (inferred from the name; no call site) |
| Sent by | no driver in these sources sends it |
| Payload | not shown by any driver |

### 127 GetRssi
| | |
|---|---|
| Names | embassy `GetRssi` / linux `BRCMF_C_GET_RSSI` / whd `WLC_GET_RSSI` / c-driver `CYW43_IOCTL_GET_RSSI` = 254 (0xfe), which is 127 << 1 with the low bit clear for get; `cyw43_ll_ioctl` turns it into an SDPCM get of command 127. `embassy/consts.rs:560` `linux/brcmfmac/fwil.h:61` `whd/src/include/whd_wlioctl.h:1415` `whd/src/include_helium/whd_wlioctl.h:1415` `whd/src/whd_utils.c:634` `c-driver/cyw43_ll.h:43` `c-driver/cyw43_ll.h:30` `c-driver/cyw43_ll.c:1329` |
| Direction | get |
| Sent by | embassy, c-driver, whd, linux. `embassy/control.rs:674` `c-driver/cyw43_ctrl.c:728` `whd/src/whd_wifi_api.c:1304` `whd/src/whd_wifi_api.c:1326` `linux/brcmfmac/cfg80211.c:3152` `linux/brcmfmac/cfg80211.c:3284` |
| Payload | Every driver reads a 32-bit value from offset 0 of the reply, as a signed integer except in linux `get_station_ibss`, which holds it in a `u32`; linux and the whd STA form convert it from little-endian, the others read it in host order. Two request shapes are sent. (a) 4 bytes: a bare 32-bit integer (embassy, c-driver, whd STA form). (b) 12 bytes: offset 0 32-bit value, offset 4 6-byte MAC, offsets 10-11 trailing bytes that linux sends as zero and whd does not write (linux, whd AP-client form). `embassy/control.rs:673-676` `c-driver/cyw43_ctrl.c:728` `whd/src/whd_wifi_api.c:5124` `whd/src/whd_wifi_api.c:5133` `whd/src/whd_wifi_api.c:135-139` `whd/src/whd_wifi_api.c:1318-1320` `whd/src/whd_wifi_api.c:1329` `linux/brcmfmac/fwil_types.h:602-605` `linux/brcmfmac/cfg80211.c:3140` `linux/brcmfmac/cfg80211.c:3151` `linux/brcmfmac/cfg80211.c:3158` |

- embassy — `get_rssi`: read the latest RSSI — 4-byte buffer, zeroed on send; asserts 4 bytes returned; decoded with `i32::from_ne_bytes`; interface 0 — `embassy/control.rs:674` `embassy/control.rs:673-676`
- c-driver — `cyw43_wifi_get_rssi`: read RSSI on the STA interface; returns `-CYW43_EPERM` if STA is not active — `int32_t`, 4 bytes, the caller's variable used as the buffer in place (not zeroed by the driver), host byte order; sent as `CYW43_IOCTL_GET_RSSI` = 254 (0xfe) through `cyw43_ioctl`, which calls `cyw43_ll_ioctl`; the c-driver documentation says the value is zero if the function is called before a network is connected — `c-driver/cyw43_ctrl.c:728` `c-driver/cyw43_ctrl.c:440` `c-driver/cyw43_ll.h:43` `c-driver/cyw43_ll.c:1329` `c-driver/cyw43.h:525`
- whd — `whd_wifi_get_rssi`: RSSI of the link, only when the interface role is STA; documented by whd as the latest RSSI value — `int32_t`, 4 bytes, via `whd_wifi_get_ioctl_buffer`, which copies the caller's buffer in and applies `dtoh32` to the first word of the reply — `whd/src/whd_wifi_api.c:1304` `whd/src/whd_wifi_api.c:5124` `whd/src/whd_wifi_api.c:5133` `whd/inc/whd_wifi_api.h:679`
- whd — `whd_wifi_get_ap_client_rssi`: RSSI of one client of the soft AP; documented by whd as the associated STA's RSSI value — `client_rssi_t { int32_t rssi; whd_mac_t macs; }` declared under `#pragma pack(1)`: 10 bytes, rssi at offset 0, MAC at offset 4, no padding. The command buffer is `ROUND_UP(10, 4)` = 12 bytes; the last 2 bytes are not written by this function. Sent with rssi = 0 and the client MAC filled in. The first 4 bytes of the reply are copied out as int32 with no `dtoh32`. whd also declares `scb_val_t { uint32_t val; wl_ether_addr_t ea; }` but uses its own packed `client_rssi_t` here — `whd/src/whd_wifi_api.c:1326` `whd/src/whd_wifi_api.c:127` `whd/src/whd_wifi_api.c:135-139` `whd/src/whd_wifi_api.c:149` `whd/src/whd_wifi_api.c:1318-1320` `whd/src/include/whd_types_int.h:134` `whd/src/whd_wifi_api.c:1323-1324` `whd/src/whd_wifi_api.c:1329` `whd/inc/whd_wifi_api.h:699` `whd/src/include/whd_wlioctl.h:936-940`
- linux — `brcmf_cfg80211_get_station_ibss`: signal level in IBSS mode — `struct brcmf_scb_val_le { __le32 val; u8 ea[6]; }`, not packed, 12 bytes with 2 bytes of tail padding, all zero on send; result = `le32_to_cpu(val)` — `linux/brcmfmac/cfg80211.c:3152` `linux/brcmfmac/fwil_types.h:602-605` `linux/brcmfmac/cfg80211.c:3151` `linux/brcmfmac/cfg80211.c:3158`
- linux — `brcmf_cfg80211_get_station`: fallback when `sta_info` gave no per-chain RSSI and the vif is connected — `struct brcmf_scb_val_le`, 12 bytes, all zero on send; rssi = `le32_to_cpu(scb_val.val)`; the unit "dBm" appears only in the debug string that follows — `linux/brcmfmac/cfg80211.c:3284` `linux/brcmfmac/cfg80211.c:3281-3283` `linux/brcmfmac/cfg80211.c:3291-3294`

Differences: (a) Request size: 4 bytes (embassy, c-driver, whd `whd_wifi_get_rssi`) versus 12 bytes (linux, whd `whd_wifi_get_ap_client_rssi`). `embassy/control.rs:673-676` `c-driver/cyw43_ctrl.c:728` `whd/src/whd_wifi_api.c:1304` `linux/brcmfmac/cfg80211.c:3152` `whd/src/whd_wifi_api.c:1318-1320` (b) Origin of the 2 trailing bytes in the 12-byte form: tail padding of an unpacked 12-byte struct in linux; round-up of a packed 10-byte struct in whd. A whd comment says WLAN expects the buffer size to be 4-byte aligned. `linux/brcmfmac/fwil_types.h:602-605` `whd/src/whd_wifi_api.c:127` `whd/src/whd_wifi_api.c:1317` `whd/src/whd_wifi_api.c:1318-1320` (c) MAC field: whd's AP-client form fills it with the client address; linux sends it zero. That the MAC selects the station is inferred from whd's per-client call; no source states it. (inferred) `whd/src/whd_wifi_api.c:1323-1324` `linux/brcmfmac/cfg80211.c:3151` (d) Byte order of the reply: linux and whd's STA form convert from little-endian; embassy decodes native-endian; c-driver and whd's AP-client form read the bytes in place. The results are the same on a little-endian host. `linux/brcmfmac/cfg80211.c:3158` `whd/src/whd_wifi_api.c:5133` `embassy/control.rs:673-676` `c-driver/cyw43_ctrl.c:728` `whd/src/whd_wifi_api.c:1329` (e) Signedness in linux: `get_station_ibss` holds the value in a `u32` named rssi and assigns it to the signed `sinfo->signal`; `get_station` uses an `int`. `linux/brcmfmac/cfg80211.c:3140` `linux/brcmfmac/cfg80211.c:3195`

### 128 GetPhyantdiv
| | |
|---|---|
| Names | embassy `GetPhyantdiv` / linux not defined / whd `WLC_GET_PHYANTDIV` / c-driver not defined. `embassy/consts.rs:561` `whd/src/include/whd_wlioctl.h:1416` `whd/src/include_helium/whd_wlioctl.h:1416` `whd/src/whd_utils.c:635` |
| Direction | get (inferred from the name; no call site) |
| Sent by | no driver in these sources sends it |
| Payload | not shown by any driver |

### 129 SetPhyantdiv
| | |
|---|---|
| Names | embassy `SetPhyantdiv` / linux not defined / whd `WLC_SET_PHYANTDIV` / c-driver not defined. `embassy/consts.rs:562` `whd/src/include/whd_wlioctl.h:1417` `whd/src/include_helium/whd_wlioctl.h:1417` `whd/src/whd_utils.c:636` |
| Direction | set (inferred from the name; no call site) |
| Sent by | no driver in these sources sends it |
| Payload | not shown by any driver |

### 130 ApRxOnly
| | |
|---|---|
| Names | embassy `ApRxOnly` / linux not defined / whd `WLC_AP_RX_ONLY` / c-driver not defined. `embassy/consts.rs:563` `whd/src/include/whd_wlioctl.h:1418` `whd/src/include_helium/whd_wlioctl.h:1418` `whd/src/whd_utils.c:637` |
| Direction | not found in these sources (no call site; the name gives no direction) |
| Sent by | no driver in these sources sends it |
| Payload | not shown by any driver |

### 131 GetTxPathPwr
| | |
|---|---|
| Names | embassy `GetTxPathPwr` / linux not defined / whd `WLC_GET_TX_PATH_PWR` / c-driver not defined. `embassy/consts.rs:564` `whd/src/include/whd_wlioctl.h:1419` `whd/src/include_helium/whd_wlioctl.h:1419` `whd/src/whd_utils.c:638` |
| Direction | get (inferred from the name; no call site) |
| Sent by | no driver in these sources sends it |
| Payload | not shown by any driver |

### 132 SetTxPathPwr
| | |
|---|---|
| Names | embassy `SetTxPathPwr` / linux not defined / whd `WLC_SET_TX_PATH_PWR` / c-driver not defined. `embassy/consts.rs:565` `whd/src/include/whd_wlioctl.h:1420` `whd/src/include_helium/whd_wlioctl.h:1420` `whd/src/whd_utils.c:639` |
| Direction | set (inferred from the name; no call site) |
| Sent by | no driver in these sources sends it |
| Payload | not shown by any driver |

### 133 GetWsec
| | |
|---|---|
| Names | embassy `GetWsec` / linux `BRCMF_C_GET_WSEC` / whd `WLC_GET_WSEC` / c-driver not defined. `embassy/consts.rs:566` `linux/brcmfmac/fwil.h:62` `whd/src/include/whd_wlioctl.h:1421` `whd/src/include_helium/whd_wlioctl.h:1421` `whd/src/whd_utils.c:640` |
| Direction | get |
| Sent by | whd only. linux defines the constant and does not send it; embassy and c-driver do not send it. `whd/src/whd_wifi_api.c:3737` `linux/brcmfmac/fwil.h:62` |
| Payload | 32-bit integer, 4 bytes, little-endian (whd applies `dtoh32` to the reply). whd treats it as a cipher bitmask: `WEP_ENABLED` 1 (0x1), `TKIP_ENABLED` 2 (0x2), `AES_ENABLED` 4 (0x4), and masks it with `SECURITY_MASK`. `whd/src/whd_wifi_api.c:5084-5088` `whd/inc/whd_types.h:63-65` `whd/inc/whd_types.h:72` |

- whd — `whd_wifi_get_ap_info`: read the wsec setting of the current association, then mask with `SECURITY_MASK` — `uint32_t`, 4 bytes, `dtoh32` on the reply (`whd_wifi_get_ioctl_value`) — `whd/src/whd_wifi_api.c:3737` `whd/src/whd_wifi_api.c:5084-5088` `whd/inc/whd_types.h:72`

Differences: linux does not send this command. It reads the bsscfg named variable (iovar) "wsec" instead, and its error text at two of those sites still says "WLC_GET_WSEC error". `linux/brcmfmac/cfg80211.c:2784` `linux/brcmfmac/cfg80211.c:2948` `linux/brcmfmac/cfg80211.c:2989` `linux/brcmfmac/cfg80211.c:3063` `linux/brcmfmac/cfg80211.c:2786` `linux/brcmfmac/cfg80211.c:2991`

### 134 SetWsec
| | |
|---|---|
| Names | embassy `SetWsec` / linux `BRCMF_C_SET_WSEC` / whd `WLC_SET_WSEC` / c-driver `WLC_SET_WSEC`. `embassy/consts.rs:567` `linux/brcmfmac/fwil.h:63` `whd/src/include/whd_wlioctl.h:1422` `whd/src/include_helium/whd_wlioctl.h:1422` `whd/src/whd_utils.c:641` `whd/src/whd_utils.c:1069-1071` `c-driver/cyw43_ll.c:181` `c-driver/cyw43_ll.c:879` |
| Direction | set |
| Sent by | embassy, c-driver, whd. linux defines the constant and does not send it. `embassy/control.rs:377` `embassy/control.rs:390` `c-driver/cyw43_ll.c:2236` `whd/src/whd_wifi_api.c:1766` `linux/brcmfmac/fwil.h:63` |
| Payload | 32-bit integer, 4 bytes, little-endian, used by the senders as a bitmask of ciphers to enable: 1 (0x1) WEP, 2 (0x2) TKIP, 4 (0x4) AES; embassy sends 0 for an open network. c-driver and whd send the low 8 bits of their security-type value, whose low bits are these flags. `embassy/consts.rs:732-733` `embassy/control.rs:377` `c-driver/cyw43_ll.h:149-151` `whd/inc/whd_types.h:63-65` `c-driver/cyw43_ll.c:1956-1960` `whd/src/whd_wifi_api.c:5060-5062` |

- embassy — join with open auth: clear wsec — u32 = 0, 4 bytes little-endian (`ioctl_set_u32`), interface 0 — `embassy/control.rs:377`
- embassy — join with WPA/WPA2/WPA3: set cipher bits — u32 = `WSEC_AES` 4 (0x04) and/or `WSEC_TKIP` 2 (0x02), or 0 if neither option is set, 4 bytes little-endian, interface 0 — `embassy/control.rs:383-390` `embassy/consts.rs:732-733`
- c-driver — `cyw43_ll_wifi_join`: set wsec from the low byte of `auth_type`, on the STA interface — u32 = `auth_type & 0xff`, 4 bytes little-endian (`cyw43_set_ioctl_u32` uses `cyw43_put_le32`) — `c-driver/cyw43_ll.c:2236` `c-driver/cyw43_ll.c:1956-1960`
- whd — `whd_wifi_prepare_join`: set the wireless security type — `uint32_t` = `auth_type & 0xFF`, 4 bytes, `htod32` (`whd_wifi_set_ioctl_value`); a whd comment says setting wsec overwrites the mfp setting in older branches, so whd stores the mfp value before sending this command — `whd/src/whd_wifi_api.c:1766` `whd/src/whd_wifi_api.c:5060-5062` `whd/src/whd_wifi_api.c:1761`

Differences: size and layout agree (4 bytes, little-endian). linux does not send this command; it sets the named variable "wsec" instead. `linux/brcmfmac/cfg80211.c:1853` `linux/brcmfmac/cfg80211.c:2094` `linux/brcmfmac/cfg80211.c:2954` `linux/brcmfmac/cfg80211.c:3069` `linux/brcmfmac/cfg80211.c:4560` `linux/brcmfmac/cfg80211.c:4818` `linux/brcmfmac/p2p.c:649`

### 135 GetPhyNoise
| | |
|---|---|
| Names | embassy `GetPhyNoise` `embassy/consts.rs:568` / linux `BRCMF_C_GET_PHY_NOISE` `linux/brcmfmac/fwil.h:64` / whd `WLC_GET_PHY_NOISE` `whd/src/include/whd_wlioctl.h:1423` / c-driver: not defined |
| Direction | get `linux/brcmfmac/cfg80211.c:8415` |
| Sent by | linux `linux/brcmfmac/cfg80211.c:8415`. whd has the name only in its command-name string table `whd/src/whd_utils.c:642`. embassy and c-driver do not send it. |
| Payload | 4 bytes, one little-endian 32-bit integer: the noise value. linux reads it into a `u32` `linux/brcmfmac/cfg80211.c:8373` `linux/brcmfmac/fwil.h:98-108`. Unit not stated at the call site. |

- linux — `brcmf_cfg80211_dump_survey`: read the noise value for the current channel before an OBSS measurement — 4-byte reply read into a `u32`, converted from little-endian by `brcmf_fil_cmd_int_get` — `linux/brcmfmac/cfg80211.c:8415` `linux/brcmfmac/cfg80211.c:8373` `linux/brcmfmac/fwil.h:98-108`
- linux substitutes `CHAN_NOISE_DUMMY` (-80) when the command fails. `linux/brcmfmac/cfg80211.c:94` `linux/brcmfmac/cfg80211.c:8415-8419`
- The value is a negative dBm figure carried in the 32-bit word (inferred, from the -80 fallback and from the `phy_noise` field comment in the BSS record; not stated for this command). `linux/brcmfmac/cfg80211.c:94` `linux/brcmfmac/fwil_types.h:332`

### 136 GetBssInfo
| | |
|---|---|
| Names | embassy `GetBssInfo` `embassy/consts.rs:569` / linux `BRCMF_C_GET_BSS_INFO` `linux/brcmfmac/fwil.h:65` / whd `WLC_GET_BSS_INFO` `whd/src/include/whd_wlioctl.h:1424` / c-driver: not defined |
| Direction | get `linux/brcmfmac/cfg80211.c:3110` `whd/src/whd_wifi_api.c:3730` |
| Sent by | linux (5 call sites) `linux/brcmfmac/p2p.c:2045` `linux/brcmfmac/cfg80211.c:3110` `linux/brcmfmac/cfg80211.c:3518` `linux/brcmfmac/cfg80211.c:3584` `linux/brcmfmac/cfg80211.c:6623`, whd (2 call sites) `whd/src/whd_wifi_api.c:3730` `whd/src/whd_wifi_api.c:5436`. embassy and c-driver do not send it. |
| Payload | Request: the first 4 bytes of the buffer hold a 32-bit buffer length. Reply: both drivers read one BSS record at reply offset 4; neither reads reply bytes 0-3 (a length word there is inferred from linux's `len` member). Record layout in the bullets below. `linux/brcmfmac/cfg80211.c:3098-3109` `linux/brcmfmac/cfg80211.c:3525` `whd/src/whd_wifi_api.c:3729-3733` |

- linux — `brcmf_p2p_get_current_chanspec`: read the chanspec of the BSS the primary interface is associated to — 2048-byte buffer (`WL_BSS_INFO_MAX`), first `__le32` preset to 2048, record read at buffer+4 — `linux/brcmfmac/p2p.c:2045` `linux/brcmfmac/p2p.c:2044` `linux/brcmfmac/p2p.c:2047` `linux/brcmfmac/cfg80211.h:22`
- linux — `brcmf_fill_bss_param`: beacon interval, DTIM period and capability flags for station info — `struct { __le32 len; struct brcmf_bss_info_le bss_le; }` in a 2048-byte allocation, `len` preset to 2048 — `linux/brcmfmac/cfg80211.c:3110` `linux/brcmfmac/cfg80211.c:3098-3105` `linux/brcmfmac/cfg80211.c:3109`
- linux — `brcmf_inform_ibss`: get the current IBSS record to report to cfg80211 — 2048-byte buffer, first `__le32` preset to 2048, record at buffer+4 — `linux/brcmfmac/cfg80211.c:3518` `linux/brcmfmac/cfg80211.c:3516` `linux/brcmfmac/cfg80211.c:3525`
- linux — `brcmf_update_bss_info`: refresh the associated BSS record (skipped in IBSS mode) — `cfg->extra_buf`, 2048 bytes (`WL_EXTRA_BUF_MAX`), first `__le32` preset to 2048, record at buffer+4 — `linux/brcmfmac/cfg80211.c:3584` `linux/brcmfmac/cfg80211.c:3583` `linux/brcmfmac/cfg80211.c:3590` `linux/brcmfmac/cfg80211.h:24`
- linux — `brcmf_bss_roaming_done`: get the new BSS chanspec after a roam — 2048-byte buffer, first `__le32` preset to 2048, record at buffer+4 — `linux/brcmfmac/cfg80211.c:6623` `linux/brcmfmac/cfg80211.c:6622` `linux/brcmfmac/cfg80211.c:6629`
- whd — `whd_wifi_get_ap_info`: read the BSS record of the associated AP — 256-byte command buffer (`WLC_IOCTL_SMLEN`), first `uint32` set to 256 with no `htod32`, `sizeof(wl_bss_info_t)` copied from reply+4 — `whd/src/whd_wifi_api.c:3730` `whd/src/whd_wifi_api.c:3729` `whd/src/whd_wifi_api.c:3733` `whd/src/include/whd_wlioctl.h:1299`
- whd — `whd_wifi_get_bss_info`: return the BSS record to the caller — 256-byte command buffer, first `uint32` set to 256 with no `htod32`, `sizeof(wl_bss_info_t)` copied from reply+4 — `whd/src/whd_wifi_api.c:5436` `whd/src/whd_wifi_api.c:5435` `whd/src/whd_wifi_api.c:5439`
- whd also lists `WHD_IOCTL_GET_BSS_INFO` = 136 in its public enum of get commands; the enum value is not used inside `whd/src`. `whd/inc/whd_types.h:460`
- whd has the name in its command-name string table; that is not a send. `whd/src/whd_utils.c:643`
- linux, whd — BSS record layout: records `brcmf_bss_info_le` (linux) and `wl_bss_info_t` (whd), multi-byte fields little-endian, fixed part 128 bytes with natural alignment (compiled; same size and offsets in both) — `linux/brcmfmac/fwil_types.h:314-348` `whd/inc/whd_types.h:926-964`
- Fields as offset/size: 0/4 `version` u32; 4/4 `length` u32, bytes of this record counted from `version`, including IEs; 8/6 `BSSID`; 14/2 `beacon_period` u16; 16/2 `capability` u16; 18/1 `SSID_len` u8; 19/32 `SSID` u8[32]; 52/20 `rateset`, u32 count then u8 rates[16]; 72/2 `chanspec` u16; 74/2 `atim_window` u16; 76/1 `dtim_period` u8; 78/2 `RSSI`; 80/1 `phy_noise` s8; 81/1 `n_cap` u8; 84/4 `nbss_cap` u32; 88/1 `ctl_ch` u8; 92/4 `reserved32[1]` u32; 96/1 `flags` u8; 97/3 `reserved[3]`; 100/16 `basic_mcs` u8[16]; 116/2 `ie_offset` u16; 120/4 `ie_length` u32; 124/2 `SNR`; at `ie_offset`, `ie_length` bytes of IEs, variable length. `linux/brcmfmac/fwil_types.h:314-348` `whd/inc/whd_types.h:926-964`
- `RSSI` (offset 78) and `SNR` (offset 124): linux declares `__le16`; whd declares `int16_t`. `linux/brcmfmac/fwil_types.h:331` `linux/brcmfmac/fwil_types.h:345` `whd/inc/whd_types.h:945` `whd/inc/whd_types.h:961`
- `phy_noise` (offset 80): a linux comment says dBm. `linux/brcmfmac/fwil_types.h:332`
- Byte 97: linux `reserved[0]`, whd `vht_cap`. `linux/brcmfmac/fwil_types.h:340` `whd/inc/whd_types.h:955`
- Gaps at 51, 77, 82-83, 89-91, 118-119 and 126-127 are alignment padding in the linux struct. The whd struct declares the first four gaps as `reserved1`..`reserved4`, declares bytes 98-99 as `reserved5` (linux `reserved[1..2]`), leaves 118-119 and 126-127 to the compiler, and lies outside the `pragma pack(1)` regions. `BRCMF_MCSSET_LEN` and `MCSSET_LEN` are both 16. `linux/brcmfmac/fwil_types.h:163` `whd/inc/whd_types.h:919` `linux/brcmfmac/fwil_types.h:314-348` `whd/inc/whd_types.h:926-964` `whd/inc/whd_types.h:880-904` `whd/inc/whd_types.h:1120-1147`
- whd expects `WL_BSS_INFO_VERSION` = 109 in scan-result records. No `version` check follows this command's reply at the whd call sites or in linux `brcmf_fill_bss_param`. `whd/src/include/whd_wlioctl.h:493` `whd/src/whd_wifi_api.c:2642-2646` `whd/src/whd_wifi_api.c:3733-3734` `whd/src/whd_wifi_api.c:5439-5441` `linux/brcmfmac/cfg80211.c:3110-3119`
- Do not confuse with whd `WLC_GET_WLC_BSS_INFO` = 286. `whd/src/include/whd_wlioctl.h:1562`

Differences: linux asks with a 2048-byte buffer and writes the length word as `__le32`; whd asks with a 256-byte buffer and writes the length word in host order (no `htod32`), although it uses `htod32` elsewhere. `linux/brcmfmac/cfg80211.c:3109` `linux/brcmfmac/cfg80211.c:6621-6622` `whd/src/whd_wifi_api.c:3729` `whd/src/whd_wifi_api.c:5435` `whd/src/whd_wifi_api.c:589`. linux declares RSSI and SNR unsigned (`__le16`), whd signed (`int16_t`). `linux/brcmfmac/fwil_types.h:331` `linux/brcmfmac/fwil_types.h:345` `whd/inc/whd_types.h:945` `whd/inc/whd_types.h:961`. Byte 97 is `reserved[0]` in linux and `vht_cap` in whd. `linux/brcmfmac/fwil_types.h:340` `whd/inc/whd_types.h:955`

### 137 GetPktcnts
| | |
|---|---|
| Names | embassy `GetPktcnts` `embassy/consts.rs:570` / linux `BRCMF_C_GET_GET_PKTCNTS` (doubled GET in the source) `linux/brcmfmac/fwil.h:66` / whd `WLC_GET_PKTCNTS` `whd/src/include/whd_wlioctl.h:1425` / c-driver: not defined |
| Direction | get `linux/brcmfmac/cfg80211.c:3162` |
| Sent by | linux `linux/brcmfmac/cfg80211.c:3162`. whd has the name only in its command-name string table `whd/src/whd_utils.c:644`. embassy and c-driver do not send it. |
| Payload | 20 bytes, five little-endian u32, in order: `rx_good_pkt` (0), `rx_bad_pkt` (4), `tx_good_pkt` (8), `tx_bad_pkt` (12), `rx_ocast_good_pkt` (16). `linux/brcmfmac/fwil_types.h:1134-1140` |

- linux — `brcmf_cfg80211_get_station_ibss`: rx/tx good and bad packet counters for station info in IBSS mode — `struct brcmf_pktcnt_le`, 20 bytes; the struct is declared without an initialiser, so the request content is not set — `linux/brcmfmac/cfg80211.c:3162` `linux/brcmfmac/cfg80211.c:3137` `linux/brcmfmac/fwil_types.h:1134-1140`
- linux field comments: `rx_good_pkt` and `tx_good_pkt` count MSDUs and MMPDUs received from / transmitted to this station; `rx_bad_pkt` and `tx_bad_pkt` count failed packets; `rx_ocast_good_pkt` counts unicast packets destined for others. `linux/brcmfmac/fwil_types.h:1128-1132`
- linux uses only the first four fields. `linux/brcmfmac/cfg80211.c:3172-3175`

### 138 GetLazywds
| | |
|---|---|
| Names | embassy `GetLazywds` `embassy/consts.rs:571` / linux: not defined (`fwil.h` goes from 137 to 140) `linux/brcmfmac/fwil.h:64-69` / whd `WLC_GET_LAZYWDS` `whd/src/include/whd_wlioctl.h:1426` / c-driver: not defined `c-driver/cyw43_ll.c:167-187` |
| Direction | unknown (the name says get; no driver shows it) |
| Sent by | no driver in these sources sends it. whd has the name only in its command-name string table `whd/src/whd_utils.c:645` |
| Payload | not shown by any driver |

### 139 SetLazywds
| | |
|---|---|
| Names | embassy `SetLazywds` `embassy/consts.rs:572` / linux: not defined (`fwil.h` goes from 137 to 140) `linux/brcmfmac/fwil.h:64-69` / whd `WLC_SET_LAZYWDS` `whd/src/include/whd_wlioctl.h:1427` / c-driver: not defined `c-driver/cyw43_ll.c:167-187` |
| Direction | unknown (the name says set; no driver shows it) |
| Sent by | no driver in these sources sends it. whd has the name only in its command-name string table `whd/src/whd_utils.c:646` |
| Payload | not shown by any driver |

### 140 GetBandlist
| | |
|---|---|
| Names | embassy `GetBandlist` `embassy/consts.rs:573` / linux `BRCMF_C_GET_BANDLIST` `linux/brcmfmac/fwil.h:67` / whd `WLC_GET_BANDLIST` `whd/src/include/whd_wlioctl.h:1428` / c-driver: not defined |
| Direction | get `linux/brcmfmac/cfg80211.c:7943` `whd/src/whd_wifi_api.c:516` |
| Sent by | linux `linux/brcmfmac/cfg80211.c:7943`, whd `whd/src/whd_wifi_api.c:516`. embassy and c-driver do not send it. whd also has the name in its command-name string table; that is not a send `whd/src/whd_utils.c:647` |
| Payload | Array of little-endian u32. Element 0 is the number of bands; the following elements are band identifiers. linux uses 3 elements (12 bytes), whd 4 (16 bytes). `linux/brcmfmac/cfg80211.c:7859` `linux/brcmfmac/cfg80211.c:7949` `whd/src/whd_wifi_api.c:511` |

- linux — `brcmf_setup_wiphy`: find which bands the chip supports, to build the wiphy band tables — `__le32 bandlist[3]`, 12 bytes — `linux/brcmfmac/cfg80211.c:7943` `linux/brcmfmac/cfg80211.c:7859`
- whd — `whd_wifi_platform_supports_triband`: returns true if a 6 GHz band is in the list — `uint32_t band_list[4]`, all zero, 16 bytes, sent through `whd_wifi_get_ioctl_buffer`, which copies the caller's array into the request — `whd/src/whd_wifi_api.c:516` `whd/src/whd_wifi_api.c:511` `whd/src/whd_wifi_api.c:5124`
- whd applies `dtoh32` to the first 32-bit word of the reply only (the count). The band identifiers in elements 1..3 are used as received, with no `dtoh32`. `whd/src/whd_wifi_api.c:5133` `whd/src/whd_wifi_api.c:526-531`
- Band identifiers in linux: `WLC_BAND_AUTO` 0, `WLC_BAND_5G` 1, `WLC_BAND_2G` 2, `WLC_BAND_ALL` 3. `linux/include/brcmu_wifi.h:92-95`
- Band identifiers in whd: `WLC_BAND_AUTO` 0, `WLC_BAND_5G` 1, `WLC_BAND_2G` 2, `WLC_BAND_6G` 3, `WLC_BAND_ALL` 4. `whd/src/include/whd_wlioctl.h:1654-1658`
- A whd comment says the count is 2 or more on any chip that supports 5 GHz; the code does not check it. `whd/src/whd_wifi_api.c:522-529`

Differences: buffer size is 12 bytes in linux and 16 bytes in whd. `linux/brcmfmac/cfg80211.c:7859` `whd/src/whd_wifi_api.c:511`. Band value 3 is `WLC_BAND_ALL` in linux and `WLC_BAND_6G` in whd, where ALL is 4. `linux/include/brcmu_wifi.h:95` `whd/src/include/whd_wlioctl.h:1657-1658`

### 141 GetBand
| | |
|---|---|
| Names | embassy `GetBand` `embassy/consts.rs:574` / linux: not defined (`fwil.h` goes from 140 to 158) `linux/brcmfmac/fwil.h:64-69` / whd `WLC_GET_BAND` `whd/src/include/whd_wlioctl.h:1429` / c-driver: not defined `c-driver/cyw43_ll.c:167-187` |
| Direction | unknown (the name says get; no driver shows it) |
| Sent by | no driver in these sources sends it. whd has the name only in its command-name string table `whd/src/whd_utils.c:648` |
| Payload | not shown by any driver. One little-endian u32 band selector, by analogy with 142 SetBand (inferred). |

### 142 SetBand
| | |
|---|---|
| Names | embassy `SetBand` `embassy/consts.rs:575` / linux: not defined (`fwil.h` goes from 140 to 158) `linux/brcmfmac/fwil.h:64-69` / whd `WLC_SET_BAND` `whd/src/include/whd_wlioctl.h:1430` / c-driver `WLC_SET_BAND` `c-driver/cyw43_ll.c:182` |
| Direction | set `c-driver/cyw43_ll.c:2173` `embassy/control.rs:748-751` |
| Sent by | c-driver `c-driver/cyw43_ll.c:2173`, embassy `embassy/control.rs:329`. whd defines it and has it in its command-name string table but does not send it `whd/src/whd_utils.c:649`. linux does not send it. |
| Payload | 4 bytes, one little-endian u32 band selector. Both senders send 0. `c-driver/cyw43_ll.c:2172` `embassy/control.rs:748-751` |

- c-driver — `cyw43_ll_wifi_pm`: after setting power management and GMODE, select band "any" — u32 little-endian 0, length 4, `SDPCM_SET`, STA interface — `c-driver/cyw43_ll.c:2173` `c-driver/cyw43_ll.c:2172`
- embassy — `Control::init`: after bringing the interface up and setting GMODE auto, select band "any" — u32 little-endian 0, 4 bytes, interface 0, via `ioctl_set_u32` — `embassy/control.rs:329` `embassy/control.rs:748-751`
- c-driver also has the name in its command-name string table; that is not a send. `c-driver/cyw43_ll.c:880`
- Band constants in the headers: `WLC_BAND_AUTO` 0, `WLC_BAND_5G` 1, `WLC_BAND_2G` 2; values 3 and 4 differ between linux and whd (see 140 GetBandlist). `linux/include/brcmu_wifi.h:92-94` `whd/src/include/whd_wlioctl.h:1654-1656`
- That the 0 sent here is `WLC_BAND_AUTO` is inferred from the matching number; both call sites only comment it as "any". `c-driver/cyw43_ll.c:2172` `embassy/control.rs:329` `linux/include/brcmu_wifi.h:92`

### 143 ScbDeauthenticate
| | |
|---|---|
| Names | embassy `ScbDeauthenticate` `embassy/consts.rs:576` / linux: not defined (`fwil.h` goes from 140 to 158) `linux/brcmfmac/fwil.h:64-69` / whd `WLC_SCB_DEAUTHENTICATE` `whd/src/include/whd_wlioctl.h:1431` / c-driver: not defined `c-driver/cyw43_ll.c:167-187` |
| Direction | unknown |
| Sent by | no driver in these sources sends it. whd has the name only in its command-name string table `whd/src/whd_utils.c:650` |
| Payload | not shown by any driver. Different commands with similar names: whd `WHD_IOCTL_SCB_DEAUTHENTICATE_FOR_REASON` = 201 `whd/inc/whd_types.h:474`; linux `BRCMF_C_SET_SCB_DEAUTHORIZE` = 122 `linux/brcmfmac/fwil.h:60` |

### 144 GetShortslot
| | |
|---|---|
| Names | embassy `GetShortslot` `embassy/consts.rs:577` / linux: not defined (`fwil.h` goes from 140 to 158) `linux/brcmfmac/fwil.h:64-69` / whd `WLC_GET_SHORTSLOT` `whd/src/include/whd_wlioctl.h:1432` / c-driver: not defined `c-driver/cyw43_ll.c:167-187` |
| Direction | unknown (the name says get; no driver shows it) |
| Sent by | no driver in these sources sends it. whd has the name only in its command-name string table `whd/src/whd_utils.c:651` |
| Payload | not shown by any driver |

### 145 GetShortslotOverride
| | |
|---|---|
| Names | embassy `GetShortslotOverride` `embassy/consts.rs:578` / linux: not defined (`fwil.h` goes from 140 to 158) `linux/brcmfmac/fwil.h:64-69` / whd `WLC_GET_SHORTSLOT_OVERRIDE` `whd/src/include/whd_wlioctl.h:1433` / c-driver: not defined `c-driver/cyw43_ll.c:167-187` |
| Direction | unknown (the name says get; no driver shows it) |
| Sent by | no driver in these sources sends it. whd has the name only in its command-name string table `whd/src/whd_utils.c:652` |
| Payload | not shown by any driver |

### 146 SetShortslotOverride
| | |
|---|---|
| Names | embassy `SetShortslotOverride` `embassy/consts.rs:579` / linux: not defined (`fwil.h` goes from 140 to 158) `linux/brcmfmac/fwil.h:64-69` / whd `WLC_SET_SHORTSLOT_OVERRIDE` `whd/src/include/whd_wlioctl.h:1434` / c-driver: not defined `c-driver/cyw43_ll.c:167-187` |
| Direction | unknown (the name says set; no driver shows it) |
| Sent by | no driver in these sources sends it. whd has the name only in its command-name string table `whd/src/whd_utils.c:653` |
| Payload | not shown by any driver |

### 147 GetShortslotRestrict
| | |
|---|---|
| Names | embassy `GetShortslotRestrict` `embassy/consts.rs:580` / linux: not defined (`fwil.h` goes from 140 to 158) `linux/brcmfmac/fwil.h:64-69` / whd `WLC_GET_SHORTSLOT_RESTRICT` `whd/src/include/whd_wlioctl.h:1435` / c-driver: not defined `c-driver/cyw43_ll.c:167-187` |
| Direction | unknown (the name says get; no driver shows it) |
| Sent by | no driver in these sources sends it. whd has the name only in its command-name string table `whd/src/whd_utils.c:654` |
| Payload | not shown by any driver |

### 148 SetShortslotRestrict
| | |
|---|---|
| Names | embassy `SetShortslotRestrict` `embassy/consts.rs:581` / linux: not defined (`fwil.h` goes from 140 to 158) `linux/brcmfmac/fwil.h:64-69` / whd `WLC_SET_SHORTSLOT_RESTRICT` `whd/src/include/whd_wlioctl.h:1436` / c-driver: not defined `c-driver/cyw43_ll.c:167-187` |
| Direction | unknown (the name says set; no driver shows it) |
| Sent by | no driver in these sources sends it. whd has the name only in its command-name string table `whd/src/whd_utils.c:655` |
| Payload | not shown by any driver |

### 149 GetGmodeProtection
| | |
|---|---|
| Names | embassy `GetGmodeProtection` `embassy/consts.rs:582` / linux: not defined (`fwil.h` goes from 140 to 158) `linux/brcmfmac/fwil.h:64-69` / whd `WLC_GET_GMODE_PROTECTION` `whd/src/include/whd_wlioctl.h:1437` / c-driver: not defined `c-driver/cyw43_ll.c:167-187` |
| Direction | unknown (the name says get; no driver shows it) |
| Sent by | no driver in these sources sends it. whd has the name only in its command-name string table `whd/src/whd_utils.c:656` |
| Payload | not shown by any driver |

### 150 GetGmodeProtectionOverride
| | |
|---|---|
| Names | embassy `GetGmodeProtectionOverride` `embassy/consts.rs:583` / linux: not defined (`fwil.h` goes from 140 to 158) `linux/brcmfmac/fwil.h:64-69` / whd `WLC_GET_GMODE_PROTECTION_OVERRIDE` `whd/src/include/whd_wlioctl.h:1438` / c-driver: not defined `c-driver/cyw43_ll.c:167-187` |
| Direction | unknown (the name says get; no driver shows it) |
| Sent by | no driver in these sources sends it. whd has the name only in its command-name string table `whd/src/whd_utils.c:657` |
| Payload | not shown by any driver |

### 151 SetGmodeProtectionOverride
| | |
|---|---|
| Names | embassy `SetGmodeProtectionOverride` `embassy/consts.rs:584` / linux: not defined (`fwil.h` goes from 140 to 158) `linux/brcmfmac/fwil.h:64-69` / whd `WLC_SET_GMODE_PROTECTION_OVERRIDE` `whd/src/include/whd_wlioctl.h:1439` / c-driver: not defined `c-driver/cyw43_ll.c:167-187` |
| Direction | unknown (the name says set; no driver shows it) |
| Sent by | no driver in these sources sends it. whd has the name only in its command-name string table `whd/src/whd_utils.c:658` |
| Payload | not shown by any driver |

### 152 Upgrade
| | |
|---|---|
| Names | embassy `Upgrade` `embassy/consts.rs:585` / linux: not defined (`fwil.h` goes from 140 to 158) `linux/brcmfmac/fwil.h:64-69` / whd `WLC_UPGRADE` `whd/src/include/whd_wlioctl.h:1440` / c-driver: not defined `c-driver/cyw43_ll.c:167-187` |
| Direction | unknown |
| Sent by | no driver in these sources sends it. whd has the name only in its command-name string table `whd/src/whd_utils.c:659` |
| Payload | not shown by any driver. Related whd definitions that are not uses of 152: `WLC_UPGRADE_STATUS` = 255 `whd/src/include/whd_wlioctl.h:1531`; `WLC_UPGRADE_SUCCESS` 0 and `WLC_UPGRADE_PENDING` 1 `whd/src/include/whd_wlioctl.h:1615-1616` |

- Numbers 153 and 154 are not defined by embassy or whd: both go from 152 to 155. `embassy/consts.rs:585-586` `whd/src/include/whd_wlioctl.h:1440-1441`

### 155 GetIgnoreBcns
| | |
|---|---|
| Names | embassy `GetIgnoreBcns` `embassy/consts.rs:586` / linux: not defined (`fwil.h` goes from 140 to 158) `linux/brcmfmac/fwil.h:64-69` / whd `WLC_GET_IGNORE_BCNS` `whd/src/include/whd_wlioctl.h:1441` / c-driver: not defined `c-driver/cyw43_ll.c:167-187` |
| Direction | unknown (the name says get; no driver shows it) |
| Sent by | no driver in these sources sends it. whd has the name only in its command-name string table `whd/src/whd_utils.c:660` |
| Payload | not shown by any driver |

### 156 SetIgnoreBcns
| | |
|---|---|
| Names | embassy `SetIgnoreBcns` `embassy/consts.rs:587` / linux: not defined (`fwil.h` goes from 140 to 158) `linux/brcmfmac/fwil.h:64-69` / whd `WLC_SET_IGNORE_BCNS` `whd/src/include/whd_wlioctl.h:1442` / c-driver: not defined `c-driver/cyw43_ll.c:167-187` |
| Direction | unknown (the name says set; no driver shows it) |
| Sent by | no driver in these sources sends it. whd has the name only in its command-name string table `whd/src/whd_utils.c:661` |
| Payload | not shown by any driver |

### 157 GetScbTimeout
| | |
|---|---|
| Names | embassy `GetScbTimeout` `embassy/consts.rs:588` / linux: not defined (`fwil.h` goes from 140 to 158) `linux/brcmfmac/fwil.h:64-69` / whd `WLC_GET_SCB_TIMEOUT` `whd/src/include/whd_wlioctl.h:1443` / c-driver: not defined `c-driver/cyw43_ll.c:167-187` |
| Direction | unknown (the name says get; no driver shows it) |
| Sent by | no driver in these sources sends it. whd has the name only in its command-name string table `whd/src/whd_utils.c:662` |
| Payload | not shown by any driver. One little-endian u32, by analogy with 158 SetScbTimeout (inferred). |

### 158 SetScbTimeout
| | |
|---|---|
| Names | embassy `SetScbTimeout` `embassy/consts.rs:589` / linux `BRCMF_C_SET_SCB_TIMEOUT` `linux/brcmfmac/fwil.h:68` / whd `WLC_SET_SCB_TIMEOUT` `whd/src/include/whd_wlioctl.h:1444` / c-driver: not defined |
| Direction | set `linux/brcmfmac/p2p.c:2118` |
| Sent by | linux (2 call sites) `linux/brcmfmac/p2p.c:2118` `linux/brcmfmac/p2p.c:2373`. whd has the name only in its command-name string table `whd/src/whd_utils.c:663`. embassy and c-driver do not send it. |
| Payload | 4 bytes, one little-endian u32: a per-station (SCB) timeout. linux always sends 20. Unit not stated in these sources; seconds (recalled, not in these sources). `linux/brcmfmac/p2p.c:46` `linux/brcmfmac/fwil.h:87-96` |

- linux — `brcmf_p2p_ifchange`: after the P2P interface type change is confirmed, set the station timeout — u32 `BRCMF_SCB_TIMEOUT_VALUE` = 20, 4 bytes little-endian via `brcmf_fil_cmd_int_set` — `linux/brcmfmac/p2p.c:2118` `linux/brcmfmac/p2p.c:46` `linux/brcmfmac/fwil.h:87-96`
- linux — `brcmf_p2p_add_vif`: for a P2P group-owner interface, set the station timeout — u32 20, 4 bytes little-endian, same helper — `linux/brcmfmac/p2p.c:2373` `linux/brcmfmac/p2p.c:2372` `linux/brcmfmac/fwil.h:87-96`

### 159 GetAssoclist
| | |
|---|---|
| Names | embassy `GetAssoclist` `embassy/consts.rs:590` / linux `BRCMF_C_GET_ASSOCLIST` `linux/brcmfmac/fwil.h:69` / whd `WLC_GET_ASSOCLIST` `whd/src/include/whd_wlioctl.h:1445` / c-driver `WLC_GET_ASSOCLIST` `c-driver/cyw43_ll.c:183` |
| Direction | get `linux/brcmfmac/cfg80211.c:3316` `whd/src/whd_wifi_api.c:3689` `c-driver/cyw43_ll.c:2490` |
| Sent by | linux `linux/brcmfmac/cfg80211.c:3316`, whd `whd/src/whd_wifi_api.c:3689`, c-driver `c-driver/cyw43_ll.c:2490`. embassy does not send it. |
| Payload | Request: little-endian u32 at offset 0 = maximum number of MAC addresses the buffer can hold, then room for that many 6-byte addresses. Reply: little-endian u32 count at offset 0, then 6-byte MAC addresses from offset 4, no padding. Size 4 + 6×N. `linux/brcmfmac/fwil_types.h:842-845` `whd/inc/whd_types.h:1141-1145` `c-driver/cyw43_ll.c:2489-2496` |

- linux — `brcmf_cfg80211_dump_station`: on index 0, fetch the list of associated stations, then serve entries from the cached copy — `struct brcmf_assoclist_le`: `__le32 count` + `u8 mac[128][6]`, 772 bytes, `count` preset to `BRCMF_MAX_ASSOCLIST` = 128 — `linux/brcmfmac/cfg80211.c:3316` `linux/brcmfmac/cfg80211.c:3315` `linux/brcmfmac/fwil_types.h:842-845` `linux/brcmfmac/fwil_types.h:149`
- whd — `whd_wifi_get_associated_client_list`: list soft-AP clients; sent only when the interface is up and in AP role — `whd_maclist_t` (packed): `uint32 count` + 6-byte MACs; buffer is the caller's `buffer_length` bytes, zeroed, `count` = `htod32` of the caller's count; the reply is copied back whole and its count is not byte-swapped — `whd/src/whd_wifi_api.c:3689` `whd/src/whd_wifi_api.c:3682-3687` `whd/src/whd_wifi_api.c:3692-3693` `whd/inc/whd_types.h:1141-1145`
- c-driver — `cyw43_ll_wifi_ap_get_stas`: get MACs of stations associated to the soft AP; sent on the AP interface — 4 + maxassoc×6 bytes: u32 little-endian maxassoc written first; reply u32 little-endian count, then 6-byte MACs from offset 4 — `c-driver/cyw43_ll.c:2490` `c-driver/cyw43_ll.c:2489` `c-driver/cyw43_ll.c:2494` `c-driver/cyw43_ll.c:2496`
- c-driver takes maxassoc from the named variable (iovar) `maxassoc`, capped by buffer room and by the caller's `num_stas`. It reads that variable twice on the STA interface before this command. `c-driver/cyw43_ll.c:2468-2486` `c-driver/cyw43_ll.c:2470-2471`
- c-driver clamps the returned count to the maximum it requested before copying MACs, so it does not rely on the reply count staying within that maximum. `c-driver/cyw43_ll.c:2495-2496`
- linux treats `-EBADE` as "not supported by the firmware of older chips", and on any error sets its cached count to 0 and returns `-EOPNOTSUPP`. `linux/brcmfmac/cfg80211.c:3320-3328`
- whd sets the caller's count to 0 without sending when the interface is not up. `whd/src/whd_wifi_api.c:3697-3701`
- whd also lists `WHD_IOCTL_GET_ASSOCLIST` = 159 in its public enum of get commands; the enum value is not used inside `whd/src`. `whd/inc/whd_types.h:459`
- whd and c-driver have the name in their command-name string tables; those are not sends. `whd/src/whd_utils.c:664` `c-driver/cyw43_ll.c:881`

Differences: the record layout is the same; buffer size and the handling of the reply count differ. Buffer size: linux fixed at 772 bytes (N = 128), whd the caller's buffer, c-driver 4 + 6×maxassoc. `linux/brcmfmac/fwil_types.h:842-845` `whd/src/whd_wifi_api.c:3684-3687` `c-driver/cyw43_ll.c:2468-2489`. whd does not byte-swap the reply count; linux and c-driver read it as little-endian. `whd/src/whd_wifi_api.c:3692-3693` `linux/brcmfmac/cfg80211.c:3331` `c-driver/cyw43_ll.c:2494`

### 160 GetClk
| | |
|---|---|
| Names | embassy `GetClk` `embassy/consts.rs:591` / linux: not defined (`fwil.h` goes from 159 to 180) `linux/brcmfmac/fwil.h:69-70` / whd `WLC_GET_CLK` `whd/src/include/whd_wlioctl.h:1446`, public `WHD_IOCTL_GET_CLK` = 160 `whd/inc/whd_types.h:453` / c-driver: not defined `c-driver/cyw43_ll.c:167-187` |
| Direction | get (whd header classification only: it is in the public enum headed "Enumeration of ioctl get"; no call site) `whd/inc/whd_types.h:446-463` |
| Sent by | no driver in these sources sends it. whd lists it in a public enum of get commands that nothing in whd references; whd's generic `whd_wifi_get_ioctl_value` / `whd_wifi_get_ioctl_buffer` take a plain `uint32_t` command number, so an application could pass it (inferred). whd also has the name in its command-name string table. `whd/inc/whd_types.h:453` `whd/inc/whd_types.h:463` `whd/inc/whd_wifi_api.h:1541` `whd/inc/whd_wifi_api.h:1563` `whd/src/whd_utils.c:665` |
| Payload | not shown by any driver |

### 161 SetClk
| | |
|---|---|
| Names | embassy `SetClk` `embassy/consts.rs:592` / linux not defined / whd `WLC_SET_CLK` `whd/src/include/whd_wlioctl.h:1447`, name table `whd/src/whd_utils.c:666` / c-driver not defined |
| Direction | set (inferred from the name) `whd/src/include/whd_wlioctl.h:1447` |
| Sent by | no driver in these sources sends it |
| Payload | not shown by any driver |

### 162 GetUp
| | |
|---|---|
| Names | embassy `GetUp` `embassy/consts.rs:593` / linux not defined / whd `WLC_GET_UP` `whd/src/include/whd_wlioctl.h:1448`, name table `whd/src/whd_utils.c:667` / c-driver not defined |
| Direction | get (inferred from the name) `whd/src/include/whd_wlioctl.h:1448` |
| Sent by | no driver in these sources sends it |
| Payload | not shown by any driver |

Differences: this is not command 2 (`WLC_UP` / `BRCMF_C_UP`), which linux sends. `linux/brcmfmac/cfg80211.c:8017`

### 163 Out
| | |
|---|---|
| Names | embassy `Out` `embassy/consts.rs:594` / linux not defined / whd `WLC_OUT` `whd/src/include/whd_wlioctl.h:1449`, name table `whd/src/whd_utils.c:668` / c-driver not defined |
| Direction | unknown (the name carries no GET/SET) `whd/src/include/whd_wlioctl.h:1449` |
| Sent by | no driver in these sources sends it |
| Payload | not shown by any driver |

### 164 GetWpaAuth
| | |
|---|---|
| Names | embassy `GetWpaAuth` `embassy/consts.rs:595` / linux not defined / whd `WLC_GET_WPA_AUTH` `whd/src/include/whd_wlioctl.h:1450`, name table `whd/src/whd_utils.c:669`, public alias `WHD_IOCTL_GET_WPA_AUTH` = 164 `whd/inc/whd_types.h:456` / c-driver not defined |
| Direction | get `whd/src/whd_wifi_api.c:3754` |
| Sent by | whd `whd/src/whd_wifi_api.c:3754` |
| Payload | One 32-bit little-endian word, 4 bytes: a bitmask of WPA authentication modes, same value space as command 165. whd requests 4 bytes and converts the result with `dtoh32`. `whd/src/whd_wifi_api.c:5084` `whd/src/whd_wifi_api.c:5088` |

- whd — `whd_wifi_get_ap_info`: after `WLC_GET_WSEC` shows TKIP or AES enabled, reads the WPA auth mode to classify the current AP's security — `uint32_t`, 4 bytes requested and returned, through `whd_wifi_get_ioctl_value` — `whd/src/whd_wifi_api.c:3754`

Differences: whd compares the returned word for equality with `WPA2_AUTH_PSK` 128 (0x0080), `WPA_AUTH_PSK` 4 (0x0004), `WPA3_AUTH_SAE_PSK` 262144 (0x40000) and `WPA3_AUTH_OWE` 1048576 (0x100000). `whd/src/whd_wifi_api.c:3756` `whd/src/include/whd_wlioctl.h:827` `whd/src/include/whd_wlioctl.h:831` `whd/src/include/whd_wlioctl.h:844` `whd/src/include/whd_wlioctl.h:847` The comparison is by equality, so a combined mask (for example WPA and WPA2 together) matches none of whd's branches (inferred). `whd/src/whd_wifi_api.c:3756` linux has no `BRCMF_C_` constant for 164; it reads a `wpa_auth` bsscfg named variable (iovar) instead. `linux/brcmfmac/fwil.h:70` `linux/brcmfmac/cfg80211.c:2135` `linux/brcmfmac/cfg80211.c:5152` embassy defines the enum value and never sends it. `embassy/consts.rs:595` whd exports `WHD_IOCTL_GET_WPA_AUTH` in `whd_usr_ioctl_get_list_t` for the public pass-through `whd_wifi_get_ioctl_value`; no code in these sources uses that enum name. `whd/inc/whd_types.h:456` `whd/inc/whd_wifi_api.h:1541`

### 165 SetWpaAuth
| | |
|---|---|
| Names | embassy `SetWpaAuth` `embassy/consts.rs:596` / linux not defined / whd `WLC_SET_WPA_AUTH` `whd/src/include/whd_wlioctl.h:1451`, name tables `whd/src/whd_utils.c:670` and `whd/src/whd_utils.c:1075`, public alias `WHD_IOCTL_SET_WPA_AUTH` = 165 `whd/inc/whd_types.h:473` / c-driver `WLC_SET_WPA_AUTH` `c-driver/cyw43_ll.c:184`, name table `c-driver/cyw43_ll.c:882` |
| Direction | set `embassy/control.rs:435` `c-driver/cyw43_ll.c:2280` `whd/src/whd_wifi_api.c:2050` |
| Sent by | embassy `embassy/control.rs:435`, c-driver `c-driver/cyw43_ll.c:2280`, whd `whd/src/whd_wifi_api.c:2050` |
| Payload | One 32-bit little-endian word, 4 bytes: a bitmask of WPA authentication (key management) modes. Values sent by all three: 0 disabled/open, 4 (0x0004) WPA-PSK, 128 (0x0080) WPA2-PSK, 262144 (0x40000) WPA3-SAE. whd's full value table: `whd/src/include/whd_wlioctl.h:824`. `embassy/control.rs:748-751` `embassy/consts.rs:742-745` `c-driver/cyw43_ll.c:1956-1959` `whd/src/whd_wifi_api.c:2049` |

- embassy — `join()` to an open network: clears WPA auth after SetWsec 0, SetInfra 1, SetAuth 0 — u32 little-endian, 4 bytes, value 0, interface 0, through `ioctl_set_u32` — `embassy/control.rs:381`
- embassy — `join()` to a secured network: last step before SetSsid, after SetInfra, SetAuth and the `mfp` named variable — u32 little-endian, 4 bytes: 4 (0x0004) for Wpa, 128 (0x0080) for Wpa2, 262144 (0x40000) for Wpa3 and Wpa2Wpa3 — `embassy/control.rs:435` `embassy/control.rs:400-403` `embassy/consts.rs:743-745` `embassy/control.rs:469`
- c-driver — `cyw43_ll_wifi_join`: sets the WPA auth mode on the STA interface after `WLC_SET_INFRA`, `WLC_SET_AUTH` and `mfp` — uint32 little-endian, 4 bytes, through `cyw43_set_ioctl_u32`: 0 open, 128 (0x0080) WPA2, 4 (0x0004) WPA-TKIP, 262144 (0x40000) WPA3 and WPA3/WPA2 — `c-driver/cyw43_ll.c:2280` `c-driver/cyw43_ll.c:2214` `c-driver/cyw43_ll.c:272`
- c-driver — `cyw43_ll_wifi_set_wpa_auth`: forces WPA (v1) PSK before a rejoin, called when a PRUNE event with reason 8 set `pend_rejoin_wpa` — uint32 little-endian, 4 bytes, value `CYW43_WPA_AUTH_PSK` = 4 (0x0004) — `c-driver/cyw43_ll.c:2337` `c-driver/cyw43_ctrl.c:225` `c-driver/cyw43_ctrl.c:348`
- whd — `whd_wifi_prepare_join`: sets the WPA authentication mode chosen from the `whd_security_t` auth type — `uint32_t`, 4 bytes, converted with `htod32`; values include `WPA_AUTH_DISABLED` 0, `WPA_AUTH_PSK` 4 (0x0004), `WPA2_AUTH_PSK` 128 (0x0080), `WPA2_AUTH_PSK_SHA256` 32768 (0x8000), `WPA3_AUTH_SAE_PSK` 262144 (0x40000), `WPA3_AUTH_OWE` 1048576 (0x100000), plus enterprise and FT combinations — `whd/src/whd_wifi_api.c:2050` `whd/src/whd_wifi_api.c:1961` `whd/src/whd_wifi_api.c:1964` `whd/src/whd_wifi_api.c:2049`

Differences: none in size or layout; all three send 4 bytes little-endian. For a plain WPA2 station join all three send 128 (0x0080). `embassy/control.rs:401` `c-driver/cyw43_ll.c:2217` `whd/src/whd_wifi_api.c:1988` For a mixed WPA3/WPA2 station join all three send 262144 (0x40000) alone. `embassy/control.rs:403` `c-driver/cyw43_ll.c:2221` `whd/src/whd_wifi_api.c:2000` whd sends values the other two never send (for example 32768 (0x8000) and 1048576 (0x100000)). `whd/src/whd_wifi_api.c:1996` `whd/src/whd_wifi_api.c:2039` linux has no `BRCMF_C_` constant for 165; it sets a `wpa_auth` bsscfg named variable instead. `linux/brcmfmac/fwil.h:70` `linux/brcmfmac/cfg80211.c:1981` `linux/brcmfmac/cfg80211.c:2277` `linux/brcmfmac/cfg80211.c:4570` `linux/brcmfmac/cfg80211.c:4834` embassy and c-driver use the command form for the STA interface only; for the access point both use the `bsscfg:wpa_auth` named variable. `embassy/control.rs:595` `embassy/control.rs:549` `c-driver/cyw43_ll.c:2418` whd also uses the `bsscfg:wpa_auth` named variable (8-byte buffer) elsewhere. `whd/src/whd_ap.c:447` `whd/src/whd_wifi_api.c:1796` whd exports `WHD_IOCTL_SET_WPA_AUTH` in `whd_usr_ioctl_set_list_t` for the public pass-through `whd_wifi_set_ioctl_value`; no code in these sources uses that enum name. `whd/inc/whd_types.h:473` `whd/inc/whd_wifi_api.h:1531` `whd/src/whd_wifi_api.c:5048`

### 166 GetUcflags
| | |
|---|---|
| Names | embassy `GetUcflags` `embassy/consts.rs:597` / linux not defined / whd `WLC_GET_UCFLAGS` `whd/src/include/whd_wlioctl.h:1452`, name table `whd/src/whd_utils.c:671` / c-driver not defined |
| Direction | get (inferred from the name) `whd/src/include/whd_wlioctl.h:1452` |
| Sent by | no driver in these sources sends it |
| Payload | not shown by any driver |

### 167 SetUcflags
| | |
|---|---|
| Names | embassy `SetUcflags` `embassy/consts.rs:598` / linux not defined / whd `WLC_SET_UCFLAGS` `whd/src/include/whd_wlioctl.h:1453`, name table `whd/src/whd_utils.c:672` / c-driver not defined |
| Direction | set (inferred from the name) `whd/src/include/whd_wlioctl.h:1453` |
| Sent by | no driver in these sources sends it |
| Payload | not shown by any driver |

### 168 GetPwridx
| | |
|---|---|
| Names | embassy `GetPwridx` `embassy/consts.rs:599` / linux not defined / whd `WLC_GET_PWRIDX` `whd/src/include/whd_wlioctl.h:1454`, name table `whd/src/whd_utils.c:673` / c-driver not defined |
| Direction | get (inferred from the name) `whd/src/include/whd_wlioctl.h:1454` |
| Sent by | no driver in these sources sends it |
| Payload | not shown by any driver |

Differences: whd defines `WL_PWRIDX_PCL_OFF` -2, `WL_PWRIDX_PCL_ON` -1, `WL_PWRIDX_LOWER_LIMIT` -2 and `WL_PWRIDX_UPPER_LIMIT` 63. They are unused and nothing in the source ties them to this command; only the PWRIDX name is shared. `whd/src/include/whd_wlioctl.h:932`

### 169 SetPwridx
| | |
|---|---|
| Names | embassy `SetPwridx` `embassy/consts.rs:600` / linux not defined / whd `WLC_SET_PWRIDX` `whd/src/include/whd_wlioctl.h:1455`, name table `whd/src/whd_utils.c:674` / c-driver not defined |
| Direction | set (inferred from the name) `whd/src/include/whd_wlioctl.h:1455` |
| Sent by | no driver in these sources sends it |
| Payload | not shown by any driver |

Differences: the unused whd `WL_PWRIDX_*` constants listed under 168 share the name; nothing ties them to this command. `whd/src/include/whd_wlioctl.h:932`

### 170 GetTssi
| | |
|---|---|
| Names | embassy `GetTssi` `embassy/consts.rs:601` / linux not defined / whd `WLC_GET_TSSI` `whd/src/include/whd_wlioctl.h:1456`, name table `whd/src/whd_utils.c:675` / c-driver not defined |
| Direction | get (inferred from the name) `whd/src/include/whd_wlioctl.h:1456` |
| Sent by | no driver in these sources sends it |
| Payload | not shown by any driver |

### 171 GetSupRatesetOverride
| | |
|---|---|
| Names | embassy `GetSupRatesetOverride` `embassy/consts.rs:602` / linux not defined / whd `WLC_GET_SUP_RATESET_OVERRIDE` `whd/src/include/whd_wlioctl.h:1457`, name table `whd/src/whd_utils.c:676` / c-driver not defined |
| Direction | get (inferred from the name) `whd/src/include/whd_wlioctl.h:1457` |
| Sent by | no driver in these sources sends it |
| Payload | not shown by any driver |

### 172 SetSupRatesetOverride
| | |
|---|---|
| Names | embassy `SetSupRatesetOverride` `embassy/consts.rs:603` / linux not defined / whd `WLC_SET_SUP_RATESET_OVERRIDE` `whd/src/include/whd_wlioctl.h:1458`, name table `whd/src/whd_utils.c:677` / c-driver not defined |
| Direction | set (inferred from the name) `whd/src/include/whd_wlioctl.h:1458` |
| Sent by | no driver in these sources sends it |
| Payload | not shown by any driver |

### 178 GetProtectionControl
| | |
|---|---|
| Names | embassy `GetProtectionControl` `embassy/consts.rs:604` / linux not defined / whd `WLC_GET_PROTECTION_CONTROL` `whd/src/include/whd_wlioctl.h:1459`, name table `whd/src/whd_utils.c:678` / c-driver not defined |
| Direction | get (inferred from the name) `whd/src/include/whd_wlioctl.h:1459` |
| Sent by | no driver in these sources sends it |
| Payload | not shown by any driver |

### 179 SetProtectionControl
| | |
|---|---|
| Names | embassy `SetProtectionControl` `embassy/consts.rs:605` / linux not defined / whd `WLC_SET_PROTECTION_CONTROL` `whd/src/include/whd_wlioctl.h:1460`, name table `whd/src/whd_utils.c:679` / c-driver not defined |
| Direction | set (inferred from the name) `whd/src/include/whd_wlioctl.h:1460` |
| Sent by | no driver in these sources sends it |
| Payload | not shown by any driver |

### 180 GetPhylist
| | |
|---|---|
| Names | embassy `GetPhylist` `embassy/consts.rs:606` / linux `BRCMF_C_GET_PHYLIST` `linux/brcmfmac/fwil.h:70`, also `BRCM_GET_PHYLIST` `linux/include/defs.h:48` / whd `WLC_GET_PHYLIST` `whd/src/include/whd_wlioctl.h:1461`, name table `whd/src/whd_utils.c:680` / c-driver not defined |
| Direction | get (inferred from the name) `whd/src/include/whd_wlioctl.h:1461` |
| Sent by | no driver in these sources sends it |
| Payload | not shown by any driver |

Differences: linux defines the number twice and uses neither name in the brcmfmac or brcmutil files in these sources. `linux/brcmfmac/fwil.h:70` `linux/include/defs.h:48`

### 181 EncryptStrength
| | |
|---|---|
| Names | embassy `EncryptStrength` `embassy/consts.rs:607` / linux not defined / whd `WLC_ENCRYPT_STRENGTH` `whd/src/include/whd_wlioctl.h:1462`, name table `whd/src/whd_utils.c:681`, unused `OID_WL_*` alias (`WL_OID_BASE` + command number) `whd/src/include/whd_wlioctl.h:1593` / c-driver not defined |
| Direction | unknown (the name carries no GET/SET) `whd/src/include/whd_wlioctl.h:1462` |
| Sent by | no driver in these sources sends it |
| Payload | not shown by any driver |

### 182 DecryptStatus
| | |
|---|---|
| Names | embassy `DecryptStatus` `embassy/consts.rs:608` / linux not defined / whd `WLC_DECRYPT_STATUS` `whd/src/include/whd_wlioctl.h:1463`, name table `whd/src/whd_utils.c:682`, unused `OID_WL_*` alias (`WL_OID_BASE` + command number) `whd/src/include/whd_wlioctl.h:1594` / c-driver not defined |
| Direction | unknown (the name carries no GET/SET) `whd/src/include/whd_wlioctl.h:1463` |
| Sent by | no driver in these sources sends it |
| Payload | not shown by any driver |

Differences: whd defines `WL_DECRYPT_STATUS_SUCCESS` 1, `WL_DECRYPT_STATUS_FAILURE` 2 and `WL_DECRYPT_STATUS_UNKNOWN` 3. They are unused and nothing ties them to this command beyond the shared name. `whd/src/include/whd_wlioctl.h:1612`

### 183 GetKeySeq
| | |
|---|---|
| Names | embassy `GetKeySeq` `embassy/consts.rs:609` / linux not defined / whd `WLC_GET_KEY_SEQ` `whd/src/include/whd_wlioctl.h:1464`, name table `whd/src/whd_utils.c:683` / c-driver not defined |
| Direction | get (inferred from the name) `whd/src/include/whd_wlioctl.h:1464` |
| Sent by | no driver in these sources sends it |
| Payload | not shown by any driver |

### 184 GetScanChannelTime
| | |
|---|---|
| Names | embassy `GetScanChannelTime` `embassy/consts.rs:610` / linux not defined / whd `WLC_GET_SCAN_CHANNEL_TIME` `whd/src/include/whd_wlioctl.h:1465`, name table `whd/src/whd_utils.c:684` / c-driver not defined |
| Direction | get (inferred from the name) `whd/src/include/whd_wlioctl.h:1465` |
| Sent by | no driver in these sources sends it |
| Payload | not shown by any driver. The SET counterpart 185 carries one 4-byte little-endian word as linux sends it; the same word returned here is (inferred). `linux/brcmfmac/common.c:436` |

### 185 SetScanChannelTime
| | |
|---|---|
| Names | embassy `SetScanChannelTime` `embassy/consts.rs:611` / linux `BRCMF_C_SET_SCAN_CHANNEL_TIME` `linux/brcmfmac/fwil.h:71` / whd `WLC_SET_SCAN_CHANNEL_TIME` `whd/src/include/whd_wlioctl.h:1466`, name table `whd/src/whd_utils.c:685` / c-driver not defined |
| Direction | set `linux/brcmfmac/common.c:436` |
| Sent by | linux `linux/brcmfmac/common.c:436` `linux/brcmfmac/cfg80211.c:7164` |
| Payload | One 32-bit little-endian word, 4 bytes. linux always sends 40. The unit is not stated in these sources (milliseconds: recalled, not in these sources). `linux/brcmfmac/fwil.h:87` `linux/brcmfmac/common.c:28` `linux/brcmfmac/cfg80211.c:84` |

- linux — `brcmf_c_preinit_dcmds`: sets the default scan channel time once at firmware bring-up, right after `event_msgs` — u32 as `__le32`, 4 bytes, value `BRCMF_DEFAULT_SCAN_CHANNEL_TIME` = 40, through `brcmf_fil_cmd_int_set` — `linux/brcmfmac/common.c:436` `linux/brcmfmac/common.c:28` `linux/brcmfmac/fwil.h:87`
- linux — `brcmf_dongle_scantime`, called from `brcmf_config_dongle`: sets the scan channel time again when the interface is configured — u32 as `__le32`, 4 bytes, value `BRCMF_SCAN_CHANNEL_TIME` = 40 — `linux/brcmfmac/cfg80211.c:7164` `linux/brcmfmac/cfg80211.c:84` `linux/brcmfmac/cfg80211.c:8019`

Differences: linux's error text at the second site calls the value "Scan assoc time"; that it is the per-channel dwell while associated is (inferred) from that one string. `linux/brcmfmac/cfg80211.c:7167` whd defines the command and never sends it; it has a named variable name `scan_assoc_time` that may be the same setting (unverified). `whd/src/include/whd_wlioctl.h:1466` `whd/src/include/whd_wlioctl.h:1156` embassy and c-driver do not send it; they pass a per-scan `active_time` in the scan parameters instead (c-driver: in the scan block of the `join` named variable). `embassy/control.rs:821` `c-driver/cyw43_ll.c:2307`

### 186 GetScanUnassocTime
| | |
|---|---|
| Names | embassy `GetScanUnassocTime` `embassy/consts.rs:612` / linux not defined / whd `WLC_GET_SCAN_UNASSOC_TIME` `whd/src/include/whd_wlioctl.h:1467`, name table `whd/src/whd_utils.c:686` / c-driver not defined |
| Direction | get (inferred from the name) `whd/src/include/whd_wlioctl.h:1467` |
| Sent by | no driver in these sources sends it |
| Payload | not shown by any driver. The SET counterpart 187 carries one 4-byte little-endian word as linux sends it; the same word returned here is (inferred). `linux/brcmfmac/common.c:445` |

### 187 SetScanUnassocTime
| | |
|---|---|
| Names | embassy `SetScanUnassocTime` `embassy/consts.rs:613` / linux `BRCMF_C_SET_SCAN_UNASSOC_TIME` `linux/brcmfmac/fwil.h:72` / whd `WLC_SET_SCAN_UNASSOC_TIME` `whd/src/include/whd_wlioctl.h:1468`, name table `whd/src/whd_utils.c:687` / c-driver not defined |
| Direction | set `linux/brcmfmac/common.c:445` |
| Sent by | linux `linux/brcmfmac/common.c:445` `linux/brcmfmac/cfg80211.c:7170` |
| Payload | One 32-bit little-endian word, 4 bytes. linux always sends 40. The unit is not stated in these sources (milliseconds: recalled, not in these sources). `linux/brcmfmac/fwil.h:87` `linux/brcmfmac/common.c:29` `linux/brcmfmac/cfg80211.c:85` |

- linux — `brcmf_c_preinit_dcmds`: sets the default scan unassoc time once at firmware bring-up — u32 as `__le32`, 4 bytes, value `BRCMF_DEFAULT_SCAN_UNASSOC_TIME` = 40, through `brcmf_fil_cmd_int_set` — `linux/brcmfmac/common.c:445` `linux/brcmfmac/common.c:29` `linux/brcmfmac/fwil.h:87`
- linux — `brcmf_dongle_scantime`, called from `brcmf_config_dongle`: sets the scan unassoc time again when the interface is configured — u32 as `__le32`, 4 bytes, value `BRCMF_SCAN_UNASSOC_TIME` = 40 — `linux/brcmfmac/cfg80211.c:7170` `linux/brcmfmac/cfg80211.c:85` `linux/brcmfmac/cfg80211.c:8019`

Differences: whd defines the command and never sends it; it has a named variable name `scan_unassoc_time`. `whd/src/include/whd_wlioctl.h:1468` `whd/src/include/whd_wlioctl.h:1157` embassy defines the enum value and never sends it. `embassy/consts.rs:613` 187 is also the value of the unrelated event `WLC_E_EXT_AUTH_REQ` in whd; command and event numbers are separate spaces. `whd/inc/whd_events.h:55`

### 188 GetScanHomeTime
| | |
|---|---|
| Names | embassy `GetScanHomeTime` `embassy/consts.rs:614` / linux not defined / whd `WLC_GET_SCAN_HOME_TIME` `whd/src/include/whd_wlioctl.h:1469`, name table `whd/src/whd_utils.c:688` / c-driver not defined |
| Direction | get (inferred from the name) `whd/src/include/whd_wlioctl.h:1469` |
| Sent by | no driver in these sources sends it |
| Payload | not shown by any driver |

Differences: whd has a named variable name `scan_home_time`. `whd/src/include/whd_wlioctl.h:1159` embassy, c-driver and linux carry a per-scan `home_time` field in the scan parameters rather than using this command. `embassy/control.rs:823` `c-driver/cyw43_ll.c:2309` `linux/brcmfmac/cfg80211.c:1120` 188 is also an unrelated event value in whd. `whd/inc/whd_events.h:56`

### 189 SetScanHomeTime
| | |
|---|---|
| Names | embassy `SetScanHomeTime` `embassy/consts.rs:615` / linux not defined / whd `WLC_SET_SCAN_HOME_TIME` `whd/src/include/whd_wlioctl.h:1470`, name table `whd/src/whd_utils.c:689` / c-driver not defined |
| Direction | set (inferred from the name) `whd/src/include/whd_wlioctl.h:1470` |
| Sent by | no driver in these sources sends it |
| Payload | not shown by any driver |

Differences: the `scan_home_time` named variable name and the per-scan `home_time` field listed under 188 apply here too. `whd/src/include/whd_wlioctl.h:1159` `embassy/control.rs:823` `c-driver/cyw43_ll.c:2309` `linux/brcmfmac/cfg80211.c:1120` 189 is also an unrelated event value in whd. `whd/inc/whd_events.h:57`

### 190 GetScanNprobes
| | |
|---|---|
| Names | embassy `GetScanNprobes` `embassy/consts.rs:616` / linux: not defined / whd `WLC_GET_SCAN_NPROBES` `whd/src/include/whd_wlioctl.h:1471` `whd/src/include_helium/whd_wlioctl.h:1471` / c-driver: not defined |
| Direction | get (inferred from the name; no call site) `whd/src/include/whd_wlioctl.h:1471` |
| Sent by | no driver in these sources sends it. whd lists the name in its debug string table only `whd/src/whd_utils.c:690` |
| Payload | not shown by any driver. whd also defines a named variable (iovar) `"scan_nprobes"`, a separate mechanism from this numbered command `whd/src/include/whd_wlioctl.h:1160` `whd/src/include_helium/whd_wlioctl.h:1161` |

### 191 SetScanNprobes
| | |
|---|---|
| Names | embassy `SetScanNprobes` `embassy/consts.rs:617` / linux: not defined / whd `WLC_SET_SCAN_NPROBES` `whd/src/include/whd_wlioctl.h:1472` `whd/src/include_helium/whd_wlioctl.h:1472` / c-driver: not defined |
| Direction | set (inferred from the name; no call site) `whd/src/include/whd_wlioctl.h:1472` |
| Sent by | no driver in these sources sends it. whd lists the name in its debug string table only `whd/src/whd_utils.c:691` |
| Payload | not shown by any driver. whd also defines a named variable `"scan_nprobes"`, a separate mechanism from this numbered command `whd/src/include/whd_wlioctl.h:1160` `whd/src/include_helium/whd_wlioctl.h:1161` |

### 192 GetPrbRespTimeout
| | |
|---|---|
| Names | embassy `GetPrbRespTimeout` `embassy/consts.rs:618` / linux: not defined / whd `WLC_GET_PRB_RESP_TIMEOUT` `whd/src/include/whd_wlioctl.h:1473` `whd/src/include_helium/whd_wlioctl.h:1473` / c-driver: not defined |
| Direction | get (inferred from the name; no call site) `whd/src/include/whd_wlioctl.h:1473` |
| Sent by | no driver in these sources sends it. whd lists the name in its debug string table only `whd/src/whd_utils.c:692` |
| Payload | not shown by any driver |

### 193 SetPrbRespTimeout
| | |
|---|---|
| Names | embassy `SetPrbRespTimeout` `embassy/consts.rs:619` / linux: not defined / whd `WLC_SET_PRB_RESP_TIMEOUT` `whd/src/include/whd_wlioctl.h:1474` `whd/src/include_helium/whd_wlioctl.h:1474` / c-driver: not defined |
| Direction | set (inferred from the name; no call site) `whd/src/include/whd_wlioctl.h:1474` |
| Sent by | no driver in these sources sends it. whd lists the name in its debug string table only `whd/src/whd_utils.c:693` |
| Payload | not shown by any driver |

### 194 GetAtten
| | |
|---|---|
| Names | embassy `GetAtten` `embassy/consts.rs:620` / linux: not defined / whd `WLC_GET_ATTEN` `whd/src/include/whd_wlioctl.h:1475` `whd/src/include_helium/whd_wlioctl.h:1475` / c-driver: not defined |
| Direction | get (inferred from the name; no call site) `whd/src/include/whd_wlioctl.h:1475` |
| Sent by | no driver in these sources sends it. whd lists the name in its debug string table only `whd/src/whd_utils.c:694` |
| Payload | not shown by any driver |

### 195 SetAtten
| | |
|---|---|
| Names | embassy `SetAtten` `embassy/consts.rs:621` / linux: not defined / whd `WLC_SET_ATTEN` `whd/src/include/whd_wlioctl.h:1476` `whd/src/include_helium/whd_wlioctl.h:1476` / c-driver: not defined |
| Direction | set (inferred from the name; no call site) `whd/src/include/whd_wlioctl.h:1476` |
| Sent by | no driver in these sources sends it. whd lists the name in its debug string table only `whd/src/whd_utils.c:695` |
| Payload | not shown by any driver |

### 196 GetShmem
| | |
|---|---|
| Names | embassy `GetShmem` `embassy/consts.rs:622` / linux: not defined / whd `WLC_GET_SHMEM` `whd/src/include/whd_wlioctl.h:1477` `whd/src/include_helium/whd_wlioctl.h:1477` / c-driver: not defined |
| Direction | get (inferred from the name; no call site) `whd/src/include/whd_wlioctl.h:1477` |
| Sent by | no driver in these sources sends it. whd lists the name in its debug string table only `whd/src/whd_utils.c:696` |
| Payload | not shown by any driver |

### 197 SetShmem
| | |
|---|---|
| Names | embassy `SetShmem` `embassy/consts.rs:623` / linux: not defined / whd `WLC_SET_SHMEM` `whd/src/include/whd_wlioctl.h:1478` `whd/src/include_helium/whd_wlioctl.h:1478` / c-driver: not defined |
| Direction | set (inferred from the name; no call site) `whd/src/include/whd_wlioctl.h:1478` |
| Sent by | no driver in these sources sends it. whd lists the name in its debug string table only `whd/src/whd_utils.c:697` |
| Payload | not shown by any driver |

### 200 SetWsecTest
| | |
|---|---|
| Names | embassy `SetWsecTest` `embassy/consts.rs:624` / linux: not defined / whd `WLC_SET_WSEC_TEST` `whd/src/include/whd_wlioctl.h:1479` `whd/src/include_helium/whd_wlioctl.h:1479` / c-driver: not defined |
| Direction | set (inferred from the name; no call site) `whd/src/include/whd_wlioctl.h:1479` |
| Sent by | no driver in these sources sends it. whd lists the name in its debug string table only `whd/src/whd_utils.c:698` |
| Payload | not shown by any driver |

### 201 ScbDeauthenticateForReason
| | |
|---|---|
| Names | embassy `ScbDeauthenticateForReason` `embassy/consts.rs:625` / linux `BRCMF_C_SCB_DEAUTHENTICATE_FOR_REASON` `linux/brcmfmac/fwil.h:73` / whd `WLC_SCB_DEAUTHENTICATE_FOR_REASON` `whd/src/include/whd_wlioctl.h:1480` `whd/src/include_helium/whd_wlioctl.h:1480`, also `WHD_IOCTL_SCB_DEAUTHENTICATE_FOR_REASON` `whd/inc/whd_types.h:474` / c-driver: not defined |
| Direction | set `linux/brcmfmac/cfg80211.c:5613` `whd/src/whd_wifi_api.c:3570` |
| Sent by | linux `linux/brcmfmac/cfg80211.c:5613`, whd `whd/src/whd_wifi_api.c:3548` `whd/src/whd_wifi_api.c:3570`. whd also has the name in its debug string table `whd/src/whd_utils.c:699` and lists 201 in the enum `whd_usr_ioctl_set_list_t`, which nothing else in whd references `whd/inc/whd_types.h:465-483`. embassy defines the name only `embassy/consts.rs:625`; c-driver: not found |
| Payload | 12 bytes. Offset 0, 4 bytes: reason code, 32-bit. Offset 4, 6 bytes: station MAC address. Offset 10, 2 bytes: tail padding (neither record is packed; the size 12 follows from C layout and is not written in the source (computed)). linux converts the reason with `cpu_to_le32`; whd writes a host-native `uint32_t`. `linux/brcmfmac/fwil_types.h:602-605` `linux/brcmfmac/cfg80211.c:5611-5614` `whd/src/include/whd_wlioctl.h:936-940` `whd/src/include_helium/whd_wlioctl.h:937-941` `whd/src/include/whd_wlioctl.h:50-53` `whd/src/whd_wifi_api.c:3567-3570` |

- linux — `brcmf_cfg80211_del_station`: AP side, deauthenticate one station (`params->mac`) with `params->reason_code` — `struct brcmf_scb_val_le`, `sizeof(scbval)` sent: `__le32 val` = reason code, `u8 ea[6]` = station MAC; the 2 padding bytes are not written by this function — `linux/brcmfmac/cfg80211.c:5611-5614` `linux/brcmfmac/fwil_types.h:602-605`
- whd — `whd_wifi_deauth_sta` with `mac == NULL`: loops over the associated-client list and deauthenticates each client whose MAC is not the AP BSSID; a failure is logged and the loop continues — `scb_val_t`, buffer of `sizeof(scb_val_t)` zeroed first: `val` = reason, `ea` = client MAC — `whd/src/whd_wifi_api.c:3538-3553` `whd/src/whd_wifi_api.c:3481`
- whd — `whd_wifi_deauth_sta` with a given `mac`: deauthenticate that one station with the given reason code — `scb_val_t`, buffer of `sizeof(scb_val_t)` zeroed first: `val` = reason, `ea` = `mac` — `whd/src/whd_wifi_api.c:3565-3570`

Differences: layout and size agree (reason first, then MAC, 12 bytes). Byte order of the reason: linux converts to little-endian explicitly `linux/brcmfmac/cfg80211.c:5612`; whd stores host-native `whd/src/whd_wifi_api.c:3569`. Padding bytes 10-11: whd zeroes the whole buffer `whd/src/whd_wifi_api.c:3567`; linux does not set them at the call site `linux/brcmfmac/cfg80211.c:5611-5614`. linux uses the same record with other commands (for example `BRCMF_C_DISASSOC`), so the comment on its definition is not specific to 201 `linux/brcmfmac/fwil_types.h:601` `linux/brcmfmac/cfg80211.c:2679-2682`.

### 202 TkipCountermeasures
| | |
|---|---|
| Names | embassy `TkipCountermeasures` `embassy/consts.rs:626` / linux: not defined / whd `WLC_TKIP_COUNTERMEASURES` `whd/src/include/whd_wlioctl.h:1481` `whd/src/include_helium/whd_wlioctl.h:1481` / c-driver: not defined |
| Direction | unknown (the name has neither GET nor SET; no call site) `whd/src/include/whd_wlioctl.h:1481` |
| Sent by | no driver in these sources sends it. whd lists the name in its debug string table only `whd/src/whd_utils.c:700` |
| Payload | not shown by any driver |

### 203 GetPiomode
| | |
|---|---|
| Names | embassy `GetPiomode` `embassy/consts.rs:627` / linux: not defined / whd `WLC_GET_PIOMODE` `whd/src/include/whd_wlioctl.h:1482` `whd/src/include_helium/whd_wlioctl.h:1482` / c-driver: not defined |
| Direction | get (inferred from the name; no call site) `whd/src/include/whd_wlioctl.h:1482` |
| Sent by | no driver in these sources sends it. whd lists the name in its debug string table only `whd/src/whd_utils.c:701` |
| Payload | not shown by any driver |

### 204 SetPiomode
| | |
|---|---|
| Names | embassy `SetPiomode` `embassy/consts.rs:628` / linux: not defined / whd `WLC_SET_PIOMODE` `whd/src/include/whd_wlioctl.h:1483` `whd/src/include_helium/whd_wlioctl.h:1483` / c-driver: not defined |
| Direction | set (inferred from the name; no call site) `whd/src/include/whd_wlioctl.h:1483` |
| Sent by | no driver in these sources sends it. whd lists the name in its debug string table only `whd/src/whd_utils.c:702` |
| Payload | not shown by any driver |

### 205 SetAssocPrefer
| | |
|---|---|
| Names | embassy `SetAssocPrefer` `embassy/consts.rs:629` / linux `BRCMF_C_SET_ASSOC_PREFER` `linux/brcmfmac/fwil.h:74` / whd `WLC_SET_ASSOC_PREFER` `whd/src/include/whd_wlioctl.h:1484` `whd/src/include_helium/whd_wlioctl.h:1484` / c-driver: not defined |
| Direction | set `linux/brcmfmac/cfg80211.c:2378` |
| Sent by | linux `linux/brcmfmac/cfg80211.c:2378`. whd has the name and debug string table only `whd/src/whd_utils.c:703`; embassy defines the name only `embassy/consts.rs:629`; c-driver: not found |
| Payload | 4 bytes, one little-endian 32-bit integer holding a band type, as linux sends it via `brcmf_fil_cmd_int_set`. The only value any driver sends is `WLC_BAND_AUTO` = 0 `linux/brcmfmac/fwil.h:87-96` `linux/include/brcmu_wifi.h:92`. The same linux header defines the other band type values 1 = 5 GHz, 2 = 2.4 GHz, 3 = all; no driver sends them with this command `linux/include/brcmu_wifi.h:93-95` |

- linux — `brcmf_set_join_pref`: when the requested BSS selection is not a band preference, reset the association band preference to auto; the return value is ignored — one `__le32`, value `WLC_BAND_AUTO` (0) — `linux/brcmfmac/cfg80211.c:2377-2378` `linux/include/brcmu_wifi.h:92`

### 206 GetAssocPrefer
| | |
|---|---|
| Names | embassy `GetAssocPrefer` `embassy/consts.rs:630` / linux: not defined / whd `WLC_GET_ASSOC_PREFER` `whd/src/include/whd_wlioctl.h:1485` `whd/src/include_helium/whd_wlioctl.h:1485` / c-driver: not defined |
| Direction | get (inferred from the name; no call site) `whd/src/include/whd_wlioctl.h:1485` |
| Sent by | no driver in these sources sends it. whd lists the name in its debug string table only `whd/src/whd_utils.c:704` |
| Payload | not shown by any driver. Its set counterpart 205 carries a 4-byte band type in linux `linux/brcmfmac/cfg80211.c:2378`; that this get returns the same is not shown |

### 207 SetRoamPrefer
| | |
|---|---|
| Names | embassy `SetRoamPrefer` `embassy/consts.rs:631` / linux: not defined / whd `WLC_SET_ROAM_PREFER` `whd/src/include/whd_wlioctl.h:1486` `whd/src/include_helium/whd_wlioctl.h:1486` / c-driver: not defined |
| Direction | set (inferred from the name; no call site) `whd/src/include/whd_wlioctl.h:1486` |
| Sent by | no driver in these sources sends it. whd lists the name in its debug string table only `whd/src/whd_utils.c:705` |
| Payload | not shown by any driver |

### 208 GetRoamPrefer
| | |
|---|---|
| Names | embassy `GetRoamPrefer` `embassy/consts.rs:632` / linux: not defined / whd `WLC_GET_ROAM_PREFER` `whd/src/include/whd_wlioctl.h:1487` `whd/src/include_helium/whd_wlioctl.h:1487` / c-driver: not defined |
| Direction | get (inferred from the name; no call site) `whd/src/include/whd_wlioctl.h:1487` |
| Sent by | no driver in these sources sends it. whd lists the name in its debug string table only `whd/src/whd_utils.c:706` |
| Payload | not shown by any driver |

### 209 SetLed
| | |
|---|---|
| Names | embassy `SetLed` `embassy/consts.rs:633` / linux: not defined / whd `WLC_SET_LED` `whd/src/include/whd_wlioctl.h:1488` `whd/src/include_helium/whd_wlioctl.h:1488` / c-driver: not defined |
| Direction | set (inferred from the name; no call site) `whd/src/include/whd_wlioctl.h:1488` |
| Sent by | no driver in these sources sends it. whd lists the name in its debug string table only `whd/src/whd_utils.c:707` |
| Payload | not shown by any driver |

### 210 GetLed
| | |
|---|---|
| Names | embassy `GetLed` `embassy/consts.rs:634` / linux: not defined / whd `WLC_GET_LED` `whd/src/include/whd_wlioctl.h:1489` `whd/src/include_helium/whd_wlioctl.h:1489` / c-driver: not defined |
| Direction | get (inferred from the name; no call site) `whd/src/include/whd_wlioctl.h:1489` |
| Sent by | no driver in these sources sends it. whd lists the name in its debug string table only `whd/src/whd_utils.c:708` |
| Payload | not shown by any driver |

### 211 GetInterferenceMode
| | |
|---|---|
| Names | embassy `GetInterferenceMode` `embassy/consts.rs:635` / linux: not defined / whd `WLC_GET_INTERFERENCE_MODE` `whd/src/include/whd_wlioctl.h:1490` `whd/src/include_helium/whd_wlioctl.h:1490` / c-driver `CYW43_IOCTL_GET_INTERFERENCE_MODE` = 422 (0x1a6) = 211 << 1 `c-driver/cyw43_ll.h:44`; c-driver encodes a command as (number << 1) \| set-bit and splits it with `cmd & 1` / `cmd >> 1` `c-driver/cyw43_ll.h:30` `c-driver/cyw43_ll.c:1329` |
| Direction | get `c-driver/cyw43.h:254` |
| Sent by | c-driver `c-driver/cyw43.h:254`. whd has the name and debug string table only `whd/src/whd_utils.c:709`; embassy defines the name only `embassy/consts.rs:635`; linux: not found |
| Payload | 4 bytes, one `uint32_t` in host byte order (no conversion in the source; little-endian on the hosts c-driver runs on (inferred)): interference mitigation mode. Values in c-driver: 0 none/disabled, 1 non-WLAN, 2 WLAN manual (adjacent channel interference), 3 auto, 4 auto with noise reduction `c-driver/cyw43.h:90-94` `c-driver/cyw43_ctrl.c:450-452`. c-driver's doc comment describes the mode as how aggressively interference on 2.4 GHz is mitigated, says higher modes cost RX sensitivity, gives `CYW43_INTERFERE_AUTO_NOISE` (4) as the firmware default, and says the setting applies to both STA and AP `c-driver/cyw43.h:226-236` `c-driver/cyw43.h:85` |

- c-driver — `cyw43_wifi_get_interference_mode` (inline wrapper): read the current interference mitigation mode, on the STA interface (`CYW43_ITF_STA`) — 4-byte `uint32_t` reply buffer via `cyw43_ioctl_get_u32` — `c-driver/cyw43.h:253-255` `c-driver/cyw43_ctrl.c:450-452`

### 212 SetInterferenceMode
| | |
|---|---|
| Names | embassy `SetInterferenceMode` `embassy/consts.rs:636` / linux: not defined / whd `WLC_SET_INTERFERENCE_MODE` `whd/src/include/whd_wlioctl.h:1491` `whd/src/include_helium/whd_wlioctl.h:1491` / c-driver `CYW43_IOCTL_SET_INTERFERENCE_MODE` = 425 (0x1a9) = (212 << 1) \| 1 `c-driver/cyw43_ll.h:45`; c-driver encodes a command as (number << 1) \| set-bit and splits it with `cmd & 1` / `cmd >> 1` `c-driver/cyw43_ll.h:30` `c-driver/cyw43_ll.c:1329` |
| Direction | set `c-driver/cyw43.h:243` |
| Sent by | c-driver `c-driver/cyw43.h:243`. whd has the name and debug string table only `whd/src/whd_utils.c:710`; embassy defines the name only `embassy/consts.rs:636`; linux: not found |
| Payload | 4 bytes, one `uint32_t` in host byte order (no conversion in the source; little-endian on the hosts c-driver runs on (inferred)): interference mitigation mode. Values in c-driver: 0 none/disabled, 1 non-WLAN, 2 WLAN manual (adjacent channel interference), 3 auto, 4 auto with noise reduction `c-driver/cyw43.h:90-94` `c-driver/cyw43_ctrl.c:446-448`. The c-driver doc comment on the mode is summarised under 211 `c-driver/cyw43.h:226-236` |

- c-driver — `cyw43_wifi_set_interference_mode` (inline wrapper): set the interference mitigation mode, on the STA interface (`CYW43_ITF_STA`) — 4-byte `uint32_t` mode via `cyw43_ioctl_set_u32` — `c-driver/cyw43.h:242-244` `c-driver/cyw43_ctrl.c:446-448`

### 213 GetChannelQa
| | |
|---|---|
| Names | embassy `GetChannelQa` `embassy/consts.rs:637` / linux: not defined / whd `WLC_GET_CHANNEL_QA` `whd/src/include/whd_wlioctl.h:1492` `whd/src/include_helium/whd_wlioctl.h:1492` / c-driver: not defined |
| Direction | get (inferred from the name; no call site) `whd/src/include/whd_wlioctl.h:1492` |
| Sent by | no driver in these sources sends it. whd lists the name in its debug string table only `whd/src/whd_utils.c:711` |
| Payload | not shown by any driver |

### 214 StartChannelQa
| | |
|---|---|
| Names | embassy `StartChannelQa` `embassy/consts.rs:638` / linux: not defined / whd `WLC_START_CHANNEL_QA` `whd/src/include/whd_wlioctl.h:1493` `whd/src/include_helium/whd_wlioctl.h:1493` / c-driver: not defined |
| Direction | unknown (the name has neither GET nor SET; no call site) `whd/src/include/whd_wlioctl.h:1493` |
| Sent by | no driver in these sources sends it. whd lists the name in its debug string table only `whd/src/whd_utils.c:712` |
| Payload | not shown by any driver |

### 215 GetChannelSel
| | |
|---|---|
| Names | embassy `GetChannelSel` `embassy/consts.rs:639` / linux: not defined / whd `WLC_GET_CHANNEL_SEL` `whd/src/include/whd_wlioctl.h:1494` `whd/src/include_helium/whd_wlioctl.h:1494` / c-driver: not defined |
| Direction | get (inferred from the name; no call site) `whd/src/include/whd_wlioctl.h:1494` |
| Sent by | no driver in these sources sends it. whd lists the name in its debug string table only `whd/src/whd_utils.c:713` |
| Payload | not shown by any driver |

### 216 StartChannelSel
| | |
|---|---|
| Names | embassy `StartChannelSel` `embassy/consts.rs:640` / linux: not defined / whd `WLC_START_CHANNEL_SEL` `whd/src/include/whd_wlioctl.h:1495` `whd/src/include_helium/whd_wlioctl.h:1495` / c-driver: not defined |
| Direction | unknown (the name gives no direction; no driver sends it) |
| Sent by | no driver in these sources sends it; whd lists it in its debug name table only `whd/src/whd_utils.c:714` |
| Payload | not shown by any driver |

### 217 GetValidChannels
| | |
|---|---|
| Names | embassy `GetValidChannels` `embassy/consts.rs:641` / linux `BRCMF_C_GET_VALID_CHANNELS` `linux/brcmfmac/fwil.h:75` / whd `WLC_GET_VALID_CHANNELS` `whd/src/include/whd_wlioctl.h:1496` `whd/src/include_helium/whd_wlioctl.h:1496` / c-driver: not defined |
| Direction | get |
| Sent by | whd `whd/src/whd_wifi_api.c:4242` (also in whd's debug name table `whd/src/whd_utils.c:715`); linux defines the constant and never uses it `linux/brcmfmac/fwil.h:75` |
| Payload | As whd sends it: 4-byte count, then count 4-byte elements (`whd_list_t`, 8 bytes as declared: count at 0, element[0] at 4). The request is a zeroed 948-byte buffer (4 × (236 + 1)) with count = 236 written through `htod32` (identity unless `IL_BIGENDIAN` is defined, then a byte swap: little-endian on the wire). whd reads the response as the same layout. What an element encodes (channel number or chanspec) is not stated in these sources. `MAXCHANNEL` is 236 in both whd header sets. whd also declares an identically shaped `wl_uint32_list_t`. `whd/inc/whd_types.h:575-579` `whd/src/whd_wifi_api.c:4235` `whd/src/whd_wifi_api.c:4240-4242` `whd/src/whd_wifi_api.c:4244` `whd/src/include/whd_wlioctl.h:1934` `whd/src/include_helium/whd_wlioctl.h:1948` `whd/src/include/whd_endian.h:45` `whd/src/include/whd_endian.h:54` `whd/src/include/whd_wlioctl.h:613-617` |

- whd — `whd_wifi_get_channels`: fetch the list of supported channels; rejects a caller list whose count is 0 — request: zeroed 948-byte buffer, count = `htod32(236)`; response: whd copies min(response size, 4 × (caller count + 1)) bytes to the caller with a plain memcpy, so the returned count and elements are not converted to host order; the bound uses the count the caller passed in — `whd/src/whd_wifi_api.c:4210` `whd/src/whd_wifi_api.c:4224-4229` `whd/src/whd_wifi_api.c:4235` `whd/src/whd_wifi_api.c:4240-4242` `whd/src/whd_wifi_api.c:4244-4247` `whd/inc/whd_wifi_api.h:505`

### 218 GetFakefrag
| | |
|---|---|
| Names | embassy `GetFakefrag` `embassy/consts.rs:642` / linux: not defined / whd `WLC_GET_FAKEFRAG` `whd/src/include/whd_wlioctl.h:1497` `whd/src/include_helium/whd_wlioctl.h:1497` / c-driver: not defined |
| Direction | get (inferred from the name; no driver sends it) |
| Sent by | no driver in these sources sends it; whd lists it in its debug name table only `whd/src/whd_utils.c:716` |
| Payload | not shown by any driver |

### 219 SetFakefrag
| | |
|---|---|
| Names | embassy `SetFakefrag` `embassy/consts.rs:643` / linux `BRCMF_C_SET_FAKEFRAG` `linux/brcmfmac/fwil.h:76` / whd `WLC_SET_FAKEFRAG` `whd/src/include/whd_wlioctl.h:1498` `whd/src/include_helium/whd_wlioctl.h:1498` / c-driver: not defined |
| Direction | set |
| Sent by | linux `linux/brcmfmac/cfg80211.c:8038`; whd lists it in its debug name table only `whd/src/whd_utils.c:717` |
| Payload | As linux sends it: 4 bytes, little-endian integer. The only value any driver sends is 1 (linux). Meaning of other values not shown by any driver. `linux/brcmfmac/cfg80211.c:8038` `linux/brcmfmac/fwil.h:87-96` |

- linux — `brcmf_config_dongle`: sent once during dongle bring-up, after the ARP/ND offload configuration and before the dongle is marked up — u32 value 1 as `__le32`, 4 bytes, via `brcmf_fil_cmd_int_set` — `linux/brcmfmac/cfg80211.c:8000` `linux/brcmfmac/cfg80211.c:8036-8044` `linux/brcmfmac/fwil.h:87-96`

Differences: naming inside linux disagrees: the constant is `BRCMF_C_SET_FAKEFRAG`, the call site's error text says "frameburst mode". whd and embassy both name 219 FAKEFRAG. `linux/brcmfmac/fwil.h:76` `linux/brcmfmac/cfg80211.c:8038-8040` `whd/src/include/whd_wlioctl.h:1498` `embassy/consts.rs:643`

### 220 GetPwroutPercentage
| | |
|---|---|
| Names | embassy `GetPwroutPercentage` `embassy/consts.rs:644` / linux: not defined / whd `WLC_GET_PWROUT_PERCENTAGE` `whd/src/include/whd_wlioctl.h:1499` `whd/src/include_helium/whd_wlioctl.h:1499` / c-driver: not defined |
| Direction | get (inferred from the name; no driver sends it) |
| Sent by | no driver in these sources sends it; whd lists it in its debug name table only `whd/src/whd_utils.c:718` |
| Payload | not shown by any driver |

### 221 SetPwroutPercentage
| | |
|---|---|
| Names | embassy `SetPwroutPercentage` `embassy/consts.rs:645` / linux: not defined / whd `WLC_SET_PWROUT_PERCENTAGE` `whd/src/include/whd_wlioctl.h:1500` `whd/src/include_helium/whd_wlioctl.h:1500` / c-driver: not defined |
| Direction | set (inferred from the name; no driver sends it) |
| Sent by | no driver in these sources sends it; whd lists it in its debug name table only `whd/src/whd_utils.c:719` |
| Payload | not shown by any driver |

### 222 SetBadFramePreempt
| | |
|---|---|
| Names | embassy `SetBadFramePreempt` `embassy/consts.rs:646` / linux: not defined / whd `WLC_SET_BAD_FRAME_PREEMPT` `whd/src/include/whd_wlioctl.h:1501` `whd/src/include_helium/whd_wlioctl.h:1501` / c-driver: not defined |
| Direction | set (inferred from the name; no driver sends it) |
| Sent by | no driver in these sources sends it; whd lists it in its debug name table only `whd/src/whd_utils.c:720` |
| Payload | not shown by any driver |

### 223 GetBadFramePreempt
| | |
|---|---|
| Names | embassy `GetBadFramePreempt` `embassy/consts.rs:647` / linux: not defined / whd `WLC_GET_BAD_FRAME_PREEMPT` `whd/src/include/whd_wlioctl.h:1502` `whd/src/include_helium/whd_wlioctl.h:1502` / c-driver: not defined |
| Direction | get (inferred from the name; no driver sends it) |
| Sent by | no driver in these sources sends it; whd lists it in its debug name table only `whd/src/whd_utils.c:721` |
| Payload | not shown by any driver |

### 224 SetLeapList
| | |
|---|---|
| Names | embassy `SetLeapList` `embassy/consts.rs:648` / linux: not defined / whd `WLC_SET_LEAP_LIST` `whd/src/include/whd_wlioctl.h:1503` `whd/src/include_helium/whd_wlioctl.h:1503` / c-driver: not defined |
| Direction | set (inferred from the name; no driver sends it) |
| Sent by | no driver in these sources sends it; whd lists it in its debug name table only `whd/src/whd_utils.c:722` |
| Payload | not shown by any driver |

### 225 GetLeapList
| | |
|---|---|
| Names | embassy `GetLeapList` `embassy/consts.rs:649` / linux: not defined / whd `WLC_GET_LEAP_LIST` `whd/src/include/whd_wlioctl.h:1504` `whd/src/include_helium/whd_wlioctl.h:1504` / c-driver: not defined |
| Direction | get (inferred from the name; no driver sends it) |
| Sent by | no driver in these sources sends it; whd lists it in its debug name table only `whd/src/whd_utils.c:723` |
| Payload | not shown by any driver |

### 226 GetCwmin
| | |
|---|---|
| Names | embassy `GetCwmin` `embassy/consts.rs:650` / linux: not defined / whd `WLC_GET_CWMIN` `whd/src/include/whd_wlioctl.h:1505` `whd/src/include_helium/whd_wlioctl.h:1505` / c-driver: not defined |
| Direction | get (inferred from the name; no driver sends it) |
| Sent by | no driver in these sources sends it; whd lists it in its debug name table only `whd/src/whd_utils.c:724` |
| Payload | not shown by any driver |

### 227 SetCwmin
| | |
|---|---|
| Names | embassy `SetCwmin` `embassy/consts.rs:651` / linux: not defined / whd `WLC_SET_CWMIN` `whd/src/include/whd_wlioctl.h:1506` `whd/src/include_helium/whd_wlioctl.h:1506` / c-driver: not defined |
| Direction | set (inferred from the name; no driver sends it) |
| Sent by | no driver in these sources sends it; whd lists it in its debug name table only `whd/src/whd_utils.c:725` |
| Payload | not shown by any driver |

### 228 GetCwmax
| | |
|---|---|
| Names | embassy `GetCwmax` `embassy/consts.rs:652` / linux: not defined / whd `WLC_GET_CWMAX` `whd/src/include/whd_wlioctl.h:1507` `whd/src/include_helium/whd_wlioctl.h:1507` / c-driver: not defined |
| Direction | get (inferred from the name; no driver sends it) |
| Sent by | no driver in these sources sends it; whd lists it in its debug name table only `whd/src/whd_utils.c:726` |
| Payload | not shown by any driver |

### 229 SetCwmax
| | |
|---|---|
| Names | embassy `SetCwmax` `embassy/consts.rs:653` / linux: not defined / whd `WLC_SET_CWMAX` `whd/src/include/whd_wlioctl.h:1508` `whd/src/include_helium/whd_wlioctl.h:1508` / c-driver: not defined |
| Direction | set (inferred from the name; no driver sends it) |
| Sent by | no driver in these sources sends it; whd lists it in its debug name table only `whd/src/whd_utils.c:727` |
| Payload | not shown by any driver |

### 230 GetWet
| | |
|---|---|
| Names | embassy `GetWet` `embassy/consts.rs:654` / linux: not defined / whd `WLC_GET_WET` `whd/src/include/whd_wlioctl.h:1509` `whd/src/include_helium/whd_wlioctl.h:1509` / c-driver: not defined |
| Direction | get (inferred from the name; no driver sends it) |
| Sent by | no driver in these sources sends it; whd lists it in its debug name table only `whd/src/whd_utils.c:728` |
| Payload | not shown by any driver |

### 231 SetWet
| | |
|---|---|
| Names | embassy `SetWet` `embassy/consts.rs:655` / linux: not defined / whd `WLC_SET_WET` `whd/src/include/whd_wlioctl.h:1510` `whd/src/include_helium/whd_wlioctl.h:1510` / c-driver: not defined |
| Direction | set (inferred from the name; no driver sends it) |
| Sent by | no driver in these sources sends it; whd lists it in its debug name table only `whd/src/whd_utils.c:729` |
| Payload | not shown by any driver |

### 232 GetPub
| | |
|---|---|
| Names | embassy `GetPub` `embassy/consts.rs:656` / linux: not defined / whd `WLC_GET_PUB` `whd/src/include/whd_wlioctl.h:1511` `whd/src/include_helium/whd_wlioctl.h:1511` / c-driver: not defined |
| Direction | get (inferred from the name; no driver sends it) |
| Sent by | no driver in these sources sends it; absent from the whd debug name table `whd/src/whd_utils.c:729-730` |
| Payload | not shown by any driver |

Command numbers 233 and 234 are not defined by embassy, whd or linux and have no entry. `embassy/consts.rs:656-657` `whd/src/include/whd_wlioctl.h:1511-1512` `whd/src/include_helium/whd_wlioctl.h:1511-1512` `linux/brcmfmac/fwil.h:76-77`

### 235 GetKeyPrimary
| | |
|---|---|
| Names | embassy `GetKeyPrimary` `embassy/consts.rs:657` / linux `BRCMF_C_GET_KEY_PRIMARY` `linux/brcmfmac/fwil.h:77` / whd `WLC_GET_KEY_PRIMARY` `whd/src/include/whd_wlioctl.h:1512` `whd/src/include_helium/whd_wlioctl.h:1512` / c-driver: not defined |
| Direction | get (inferred from the name; no driver sends it) |
| Sent by | no driver in these sources sends it; whd lists it in its debug name table only `whd/src/whd_utils.c:730`; linux defines the constant and never uses it `linux/brcmfmac/fwil.h:77` |
| Payload | not shown by any driver. The set counterpart 236 carries a 4-byte little-endian key index in linux; the same shape here is not shown. `linux/brcmfmac/cfg80211.c:2793-2794` |

### 236 SetKeyPrimary
| | |
|---|---|
| Names | embassy `SetKeyPrimary` `embassy/consts.rs:658` / linux `BRCMF_C_SET_KEY_PRIMARY` `linux/brcmfmac/fwil.h:78` / whd `WLC_SET_KEY_PRIMARY` `whd/src/include/whd_wlioctl.h:1513` `whd/src/include_helium/whd_wlioctl.h:1513` / c-driver: not defined |
| Direction | set |
| Sent by | linux `linux/brcmfmac/cfg80211.c:2793-2794`; whd lists it in its debug name table only `whd/src/whd_utils.c:731` |
| Payload | As linux sends it: 4 bytes, little-endian integer holding the key index to make primary. No other layout shown by any driver. `linux/brcmfmac/cfg80211.c:2793-2794` `linux/brcmfmac/fwil.h:87-96` |

- linux — `brcmf_cfg80211_config_default_key`: select `key_idx` as the current WEP transmit key; sent only when the value read from the per-interface named variable `wsec` has `WEP_ENABLED` set, nothing is sent for other ciphers — u32 key index (widened from the u8 `key_idx` argument) as `__le32`, 4 bytes, via `brcmf_fil_cmd_int_set` — `linux/brcmfmac/cfg80211.c:2793-2794` `linux/brcmfmac/cfg80211.c:2769` `linux/brcmfmac/cfg80211.c:2784-2790` `linux/brcmfmac/fwil.h:87-96`

Command number 237 is not defined by embassy, whd or linux and has no entry. `embassy/consts.rs:658-659` `whd/src/include/whd_wlioctl.h:1513-1514` `whd/src/include_helium/whd_wlioctl.h:1513-1514` `linux/brcmfmac/fwil.h:78-79`

### 238 GetAciArgs
| | |
|---|---|
| Names | embassy `GetAciArgs` `embassy/consts.rs:659` / linux: not defined / whd `WLC_GET_ACI_ARGS` `whd/src/include/whd_wlioctl.h:1514` `whd/src/include_helium/whd_wlioctl.h:1514` / c-driver: not defined |
| Direction | get (inferred from the name; no driver sends it) |
| Sent by | no driver in these sources sends it; whd lists it in its debug name table only `whd/src/whd_utils.c:732` |
| Payload | not shown by any driver |

### 239 SetAciArgs
| | |
|---|---|
| Names | embassy `SetAciArgs` `embassy/consts.rs:660` / linux: not defined / whd `WLC_SET_ACI_ARGS` `whd/src/include/whd_wlioctl.h:1515` `whd/src/include_helium/whd_wlioctl.h:1515` / c-driver: not defined |
| Direction | set (inferred from the name; no driver sends it) |
| Sent by | no driver in these sources sends it; whd lists it in its debug name table only `whd/src/whd_utils.c:733` |
| Payload | not shown by any driver |

### 240 UnsetCallback
| | |
|---|---|
| Names | embassy `UnsetCallback` `embassy/consts.rs:661` / linux: not defined / whd `WLC_UNSET_CALLBACK` `whd/src/include/whd_wlioctl.h:1516` `whd/src/include_helium/whd_wlioctl.h:1516` / c-driver: not defined |
| Direction | unknown (the name gives no direction; no driver sends it) |
| Sent by | no driver in these sources sends it; whd lists it in its debug name table only `whd/src/whd_utils.c:734` |
| Payload | not shown by any driver |

### 241 SetCallback
| | |
|---|---|
| Names | embassy `SetCallback` `embassy/consts.rs:662` / linux: not defined / whd `WLC_SET_CALLBACK` `whd/src/include/whd_wlioctl.h:1517` `whd/src/include_helium/whd_wlioctl.h:1517` / c-driver: not defined |
| Direction | set (inferred from the name; no driver sends it) |
| Sent by | no driver in these sources sends it; whd lists it in its debug name table only `whd/src/whd_utils.c:735` |
| Payload | not shown by any driver |

### 242 GetRadar
| | |
|---|---|
| Names | embassy `GetRadar` `embassy/consts.rs:663` / linux: not defined / whd `WLC_GET_RADAR` `whd/src/include/whd_wlioctl.h:1518` `whd/src/include_helium/whd_wlioctl.h:1518` / c-driver: not defined |
| Direction | get (inferred from the name; no driver sends it) |
| Sent by | no driver in these sources sends it; whd lists it in its debug name table only `whd/src/whd_utils.c:736` |
| Payload | not shown by any driver |

### 243 SetRadar
| | |
|---|---|
| Names | embassy `SetRadar` `embassy/consts.rs:664` / linux not defined / whd `WLC_SET_RADAR` `whd/src/include/whd_wlioctl.h:1519` (also in whd's number-to-name debug table `whd/src/whd_utils.c:737`) / c-driver not defined |
| Direction | set (inferred from the name; no call site) |
| Sent by | no driver in these sources sends it |
| Payload | not shown by any driver |

### 244 SetSpectManagment
| | |
|---|---|
| Names | embassy `SetSpectManagment` `embassy/consts.rs:665` / linux not defined / whd `WLC_SET_SPECT_MANAGMENT` `whd/src/include/whd_wlioctl.h:1520` (debug name table `whd/src/whd_utils.c:738`) / c-driver not defined |
| Direction | set (inferred from the name; no call site) |
| Sent by | no driver in these sources sends it |
| Payload | not shown by any driver |

### 245 GetSpectManagment
| | |
|---|---|
| Names | embassy `GetSpectManagment` `embassy/consts.rs:666` / linux not defined / whd `WLC_GET_SPECT_MANAGMENT` `whd/src/include/whd_wlioctl.h:1521` (debug name table `whd/src/whd_utils.c:739`) / c-driver not defined |
| Direction | get (inferred from the name; no call site) |
| Sent by | no driver in these sources sends it |
| Payload | not shown by any driver |

### 246 WdsGetRemoteHwaddr
| | |
|---|---|
| Names | embassy `WdsGetRemoteHwaddr` `embassy/consts.rs:667` / linux not defined / whd `WLC_WDS_GET_REMOTE_HWADDR` `whd/src/include/whd_wlioctl.h:1522` (debug name table `whd/src/whd_utils.c:740`) / c-driver not defined |
| Direction | get (inferred from the name; no call site) |
| Sent by | no driver in these sources sends it |
| Payload | not shown by any driver |

### 247 WdsGetWpaSup
| | |
|---|---|
| Names | embassy `WdsGetWpaSup` `embassy/consts.rs:668` / linux not defined / whd `WLC_WDS_GET_WPA_SUP` `whd/src/include/whd_wlioctl.h:1523` (debug name table `whd/src/whd_utils.c:741`) / c-driver not defined |
| Direction | get (inferred from the name; no call site) |
| Sent by | no driver in these sources sends it |
| Payload | not shown by any driver |

### 248 SetCsScanTimer
| | |
|---|---|
| Names | embassy `SetCsScanTimer` `embassy/consts.rs:669` / linux not defined / whd `WLC_SET_CS_SCAN_TIMER` `whd/src/include/whd_wlioctl.h:1524` (debug name table `whd/src/whd_utils.c:742`) / c-driver not defined |
| Direction | set (inferred from the name; no call site) |
| Sent by | no driver in these sources sends it |
| Payload | not shown by any driver |

### 249 GetCsScanTimer
| | |
|---|---|
| Names | embassy `GetCsScanTimer` `embassy/consts.rs:670` / linux not defined / whd `WLC_GET_CS_SCAN_TIMER` `whd/src/include/whd_wlioctl.h:1525` (debug name table `whd/src/whd_utils.c:743`) / c-driver not defined |
| Direction | get (inferred from the name; no call site) |
| Sent by | no driver in these sources sends it |
| Payload | not shown by any driver |

### 250 MeasureRequest
| | |
|---|---|
| Names | embassy `MeasureRequest` `embassy/consts.rs:671` / linux not defined / whd `WLC_MEASURE_REQUEST` `whd/src/include/whd_wlioctl.h:1526` (debug name table `whd/src/whd_utils.c:744`) / c-driver not defined |
| Direction | unknown |
| Sent by | no driver in these sources sends it |
| Payload | not shown by any driver |

### 251 Init
| | |
|---|---|
| Names | embassy `Init` `embassy/consts.rs:672` / linux not defined / whd `WLC_INIT` `whd/src/include/whd_wlioctl.h:1527` (debug name table `whd/src/whd_utils.c:745`) / c-driver not defined |
| Direction | unknown |
| Sent by | no driver in these sources sends it |
| Payload | not shown by any driver |

### 252 SendQuiet
| | |
|---|---|
| Names | embassy `SendQuiet` `embassy/consts.rs:673` / linux not defined / whd `WLC_SEND_QUIET` `whd/src/include/whd_wlioctl.h:1528` (debug name table `whd/src/whd_utils.c:746`) / c-driver not defined |
| Direction | unknown |
| Sent by | no driver in these sources sends it |
| Payload | not shown by any driver |

### 253 Keepalive
| | |
|---|---|
| Names | embassy `Keepalive` `embassy/consts.rs:674` / linux not defined / whd `WLC_KEEPALIVE` `whd/src/include/whd_wlioctl.h:1529` (debug name table `whd/src/whd_utils.c:747`) / c-driver not defined |
| Direction | unknown |
| Sent by | no driver in these sources sends it |
| Payload | not shown by any driver |

### 254 SendPwrConstraint
| | |
|---|---|
| Names | embassy `SendPwrConstraint` `embassy/consts.rs:675` / linux not defined / whd `WLC_SEND_PWR_CONSTRAINT` `whd/src/include/whd_wlioctl.h:1530` (debug name table `whd/src/whd_utils.c:748`) / c-driver not defined |
| Direction | unknown |
| Sent by | no driver in these sources sends it |
| Payload | not shown by any driver |

### 255 UpgradeStatus
| | |
|---|---|
| Names | embassy `UpgradeStatus` `embassy/consts.rs:676` / linux not defined / whd `WLC_UPGRADE_STATUS` `whd/src/include/whd_wlioctl.h:1531` (debug name table `whd/src/whd_utils.c:749`) / c-driver not defined |
| Direction | unknown |
| Sent by | no driver in these sources sends it |
| Payload | not shown by any driver |

### 256 CurrentPwr
| | |
|---|---|
| Names | embassy `CurrentPwr` `embassy/consts.rs:677` / linux not defined / whd `WLC_CURRENT_PWR` `whd/src/include/whd_wlioctl.h:1532` / c-driver not defined. Unlike its neighbours it is absent from whd's debug name table, which goes from 255 straight to 257 `whd/src/whd_utils.c:749-750` |
| Direction | unknown |
| Sent by | no driver in these sources sends it |
| Payload | not shown by any driver |

### 257 GetScanPassiveTime
| | |
|---|---|
| Names | embassy `GetScanPassiveTime` `embassy/consts.rs:678` / linux not defined / whd `WLC_GET_SCAN_PASSIVE_TIME` `whd/src/include/whd_wlioctl.h:1533` (debug name table `whd/src/whd_utils.c:750`) / c-driver not defined |
| Direction | get (inferred from the name; no call site) |
| Sent by | no driver in these sources sends it |
| Payload | not shown by any driver. The set counterpart 258 is sent by linux as one little-endian u32 `linux/brcmfmac/cfg80211.c:7177`; the same layout for the get is (inferred) |

### 258 SetScanPassiveTime
| | |
|---|---|
| Names | embassy `SetScanPassiveTime` `embassy/consts.rs:679` / linux `BRCMF_C_SET_SCAN_PASSIVE_TIME` `linux/brcmfmac/fwil.h:79` / whd `WLC_SET_SCAN_PASSIVE_TIME` `whd/src/include/whd_wlioctl.h:1534` (debug name table `whd/src/whd_utils.c:751`) / c-driver not defined |
| Direction | set `linux/brcmfmac/cfg80211.c:7177` |
| Sent by | linux `linux/brcmfmac/cfg80211.c:7177` |
| Payload | One u32, little-endian, 4 bytes: passive scan time per channel `linux/brcmfmac/cfg80211.c:7177` `linux/brcmfmac/fwil.h:87-96`. Unit not stated at the call site |

- linux — `brcmf_dongle_scantime()` sets the passive-scan dwell time during dongle configuration (called from `linux/brcmfmac/cfg80211.c:8019`) and logs "Scan passive time error" when the command fails (`linux/brcmfmac/cfg80211.c:7180`) — `__le32`, 4 bytes, value 120 (`BRCMF_SCAN_PASSIVE_TIME`, `linux/brcmfmac/cfg80211.c:86`), built by `brcmf_fil_cmd_int_set` (`cpu_to_le32`, then sent with `sizeof(data_le)`, `linux/brcmfmac/fwil.h:87-96`) — `linux/brcmfmac/cfg80211.c:7177`

Differences: linux is the only sender `linux/brcmfmac/cfg80211.c:7177`. whd defines the command but never sends it; whd sets a passive time per scan inside its scan/join parameter structs instead, which is a different mechanism `whd/src/whd_wifi_api.c:2359` `whd/src/whd_wifi_api.c:3355-3365`. The whd per-scan field carries an `_ms` suffix (`scan_passive_dwell_time_per_channel_ms`); that names the unit of the per-scan parameter, not of command 258 `whd/inc/whd_types.h:873` `whd/src/whd_wifi_api.c:3355-3356`. embassy has the enum entry only and does not send it `embassy/consts.rs:679`; c-driver has no use of it, not found in these sources.

### 259 LegacyLinkBehavior
| | |
|---|---|
| Names | embassy `LegacyLinkBehavior` `embassy/consts.rs:680` / linux not defined / whd `WLC_LEGACY_LINK_BEHAVIOR` `whd/src/include/whd_wlioctl.h:1535` (debug name table `whd/src/whd_utils.c:752` / derived constant `OID_LEGACY_LINK_BEHAVIOR` = `WL_OID_BASE` + this number, itself unused, `whd/src/include/whd_wlioctl.h:1595`) / c-driver not defined |
| Direction | unknown |
| Sent by | no driver in these sources sends it |
| Payload | not shown by any driver |

### 260 GetChannelsInCountry
| | |
|---|---|
| Names | embassy `GetChannelsInCountry` `embassy/consts.rs:681` / linux not defined / whd `WLC_GET_CHANNELS_IN_COUNTRY` `whd/src/include/whd_wlioctl.h:1536` (debug name table `whd/src/whd_utils.c:753`) / c-driver not defined |
| Direction | get (inferred from the name; no call site) |
| Sent by | no driver in these sources sends it |
| Payload | not shown by any driver. whd declares a struct with a matching name, `wl_channels_in_country_t`: u32 `buflen` (offset 0), u32 `band` (4), int8 `country_abbrev[4]` (8; `WLC_CNTRY_BUF_SZ` = 4), u32 `count` (12), u32 `channel[1]` (16, variable-length list); 20 bytes with one channel slot `whd/src/include/whd_wlioctl.h:674-681` `whd/src/include/whd_wlioctl.h:667`. The struct is used nowhere in whd; that it is this command's payload is (inferred) from the name only |

### 261 GetCountryList
| | |
|---|---|
| Names | embassy `GetCountryList` `embassy/consts.rs:682` / linux not defined / whd `WLC_GET_COUNTRY_LIST` `whd/src/include/whd_wlioctl.h:1537` (debug name table `whd/src/whd_utils.c:754`) / c-driver not defined |
| Direction | get (the request buffer carries input fields) `whd/src/whd_wifi_api.c:7270` |
| Sent by | whd `whd/src/whd_wifi_api.c:7270` |
| Payload | `wl_country_list_t`, same buffer for request and response: u32 `buflen` (offset 0), u32 `band_set` (4), u32 `band` (8), u32 `count` (12), int8 `country_abbrev[]` (16, variable) `whd/src/include/whd_wlioctl.h:682-689`. u32 fields little-endian on the wire (whd applies `htod32` on send, `dtoh32` on `count`) `whd/src/whd_wifi_api.c:7265-7268` `whd/src/whd_wifi_api.c:7272-7273`. whd reads `count` entries of 4 bytes each (`WLC_CNTRY_BUF_SZ`) starting at offset 16 `whd/src/include/whd_wlioctl.h:667` `whd/src/whd_wifi_api.c:7272`. whd sends and receives 256 bytes `whd/src/include/whd_wlioctl.h:1299`. `sizeof(wl_country_list_t)` is 20 with tail padding (computed); the entries start at offset 16 `whd/src/include/whd_wlioctl.h:682-689` |

- whd — `whd_wifi_get_country_list()` retrieves the supported country codes, optionally for one band (`whd/inc/whd_wifi_api.h:1900-1908`) — header built in a 512-byte stack buffer (`whd/src/whd_wifi_api.c:7242-7244`); length passed is `WLC_IOCTL_SMLEN` = 256 (`whd/src/include/whd_wlioctl.h:1299`) through `whd_wifi_get_ioctl_buffer` (`whd/src/whd_wifi_api.c:5111-5126`); request fields `buflen` = 256, `band_set` = 1 and `band` = the band when band > 0, else `band_set` = 0, `count` = 0, each `htod32` (`whd/src/whd_wifi_api.c:7251-7268`); response: `count` (`dtoh32`) and `count` × 4 bytes of `country_abbrev` copied out (`whd/src/whd_wifi_api.c:7272-7273`) — `whd/src/whd_wifi_api.c:7270`
- whd — buffer size at the same call site — 512 bytes are allocated but only 256 are declared, in `buflen` and in the command length — `whd/src/whd_wifi_api.c:7242-7244` `whd/src/include/whd_wlioctl.h:1299`
- whd — request `band` field at the same call site — when band is 0, whd never assigns `band` before byte-swapping and sending it, so it carries uninitialised stack bytes — `whd/src/whd_wifi_api.c:7242` `whd/src/whd_wifi_api.c:7254-7263` `whd/src/whd_wifi_api.c:7267`
- whd — copy-out at the same call site — trusts the returned `count`; it is not bounded against the caller's buffer or the 256 bytes requested — `whd/src/whd_wifi_api.c:7272`
- whd — `whd_wifi_get_ioctl_buffer`, the helper that sends it — applies `dtoh32` to the first 4 bytes of the response (the `buflen` field) before copying it back — `whd/src/whd_wifi_api.c:5133-5134`

Differences: whd is the only sender `whd/src/whd_wifi_api.c:7270`. linux and c-driver do not define or send it, not found in these sources; embassy has the enum entry only `embassy/consts.rs:682`.

### 262 GetVar
| | |
|---|---|
| Names | embassy `GetVar` `embassy/consts.rs:683` / linux `BRCMF_C_GET_VAR` `linux/brcmfmac/fwil.h:80` / whd `WLC_GET_VAR` `whd/src/include/whd_wlioctl.h:1538` (debug name table `whd/src/whd_utils.c:755`) / c-driver `WLC_GET_VAR` (internal, value 262) `c-driver/cyw43_ll.c:186` (name table `c-driver/cyw43_ll.c:884`), public `CYW43_IOCTL_GET_VAR` = 524 (0x20c) = 262 shifted left by 1, low bit 0 = get `c-driver/cyw43_ll.h:46` (decoded at `c-driver/cyw43_ll.c:1329`) |
| Direction | get `linux/brcmfmac/fwil.c:229` |
| Sent by | linux, whd, c-driver, embassy `linux/brcmfmac/fwil.c:229` `whd/src/whd_cdc_bdc.c:337` `c-driver/cyw43_ll.c:1974` `embassy/control.rs:740`. whd's per-variable call sites do not name the constant; they call `whd_proto_get_iovar` (23 calls) or `whd_proto_set_iovar` (74 calls), which reach the two transport functions listed below `whd/src/whd_cdc_bdc.c:337`. linux's many callers of `brcmf_fil_iovar_*`, `brcmf_fil_bsscfg_*` and `brcmf_fil_xtlv_*` are represented by the three funnel functions listed below `linux/brcmfmac/fwil.c:229`. pico-sdk: no reference to this command, not found in these sources |
| Payload | Request: variable name, ASCII, NUL-terminated, followed directly by optional input bytes or zero space for the reply. Response: every driver reads the value from offset 0 of the returned buffer, where it had written the name. Variable size: strlen(name) + 1 + value length. Integers little-endian. `linux/brcmfmac/fwil.c:166-184` `linux/brcmfmac/fwil.c:226-232` `c-driver/cyw43_ctrl.c:703-705` `embassy/control.rs:731-746`. The value layout of each named variable is given in the variables chapters. linux builds name + NUL, then appends the caller's data `linux/brcmfmac/fwil.c:166-184`. c-driver documents the payload as name, NUL, le32 value; on a get the name is written into the buffer and, per the c-driver comment, the le32 value replaces it on return `c-driver/cyw43_ctrl.c:684-685` `c-driver/cyw43_ctrl.c:703-705`. embassy sends name, 0 byte, then zero fill; length sent is max(name length + 1, result length) `embassy/control.rs:731-746` `embassy/control.rs:738`. whd (CDC path) builds the buffer with leading zero bytes so the value is 4-byte aligned in host memory, then strips those bytes before sending; the bytes on the wire are name + NUL + value like the others `whd/src/whd_cdc_bdc.c:354-366` `whd/src/whd_cdc_bdc.c:211-229`. Per-BSS variant: name prefixed with `bsscfg:` and a le32 bss index as the first value bytes `linux/brcmfmac/fwil.c:248-291` `c-driver/cyw43_ll.c:2392` `c-driver/cyw43_ll.c:1546-1553`. linux XTLV variant: name + NUL, then a packed XTLV header and value `linux/brcmfmac/fwil.c:354-373`. Integer encoding: c-driver `cyw43_put_le32` `c-driver/cyw43_ll.c:1542`; embassy `to_le_bytes` `embassy/control.rs:703`; linux `cpu_to_le32` for the bss index `linux/brcmfmac/fwil.c:282`. Size caps: linux 8192-byte `proto_buf` `linux/brcmfmac/core.h:32` `linux/brcmfmac/core.h:123`; embassy `get_iovar` uses a 64-byte buffer `embassy/control.rs:731-746`. linux copies the first `len` bytes of the reply back to the caller `linux/brcmfmac/fwil.c:231-232`. c-driver's public API encodes every command as (number << 1) with the low bit set for a set `c-driver/cyw43_ll.h:46` `c-driver/cyw43_ll.c:1327-1329` |

- linux — `brcmf_fil_iovar_data_get()`, the generic "get named variable" entry used by the whole driver — request name + NUL + caller data (`len` bytes) in `proto_buf`, buflen = strlen(name) + 1 + len; response: first `len` bytes copied back (`linux/brcmfmac/fwil.c:226-232`) — `linux/brcmfmac/fwil.c:229`
- linux — `brcmf_fil_bsscfg_data_get()`, per-BSS variable — name + NUL + data when bsscfgidx is 0, else `bsscfg:` + name + NUL + le32 bsscfgidx + data (`linux/brcmfmac/fwil.c:259-290`); response: `len` bytes copied back (`linux/brcmfmac/fwil.c:338-339`) — `linux/brcmfmac/fwil.c:336`
- linux — `brcmf_fil_xtlv_data_get()`, variable whose value is an XTLV — name + NUL + XTLV header (id, len) + data, 32-bit aligned (`linux/brcmfmac/fwil.c:354-373`); response: `len` bytes copied back (`linux/brcmfmac/fwil.c:418-419`) — `linux/brcmfmac/fwil.c:416`
- whd — `whd_cdc_send_iovar()` GET branch, the CDC/BDC transport's `get_iovar` (installed at `whd/src/whd_cdc_bdc.c:599` via `whd_cdc_get_iovar`, `whd/src/whd_cdc_bdc.c:132-137`); every `whd_proto_get_iovar` caller on SDIO/SPI goes through it — name + NUL, then `data_length` bytes of value space (`whd/src/whd_cdc_bdc.c:349-366`); variable size — `whd/src/whd_cdc_bdc.c:337`
- whd — `whd_msgbuf_get_iovar()`, the msgbuf transport's `get_iovar` (installed at `whd/src/whd_msgbuf_txrx.c:2261`) — name + NUL, then `data_length` bytes, no alignment padding (`whd/src/whd_msgbuf_txrx.c:202-225`); the buffer is zeroed first and may be enlarged to `IOCTL_TX_PAYLOAD_THRESH` + 1 when `wl_cmd_in_prog` is set (`whd/src/whd_msgbuf_txrx.c:208-213`, `whd/src/whd_msgbuf_txrx.c:223`) — `whd/src/whd_msgbuf_txrx.c:569`
- whd — `whd_wifi_get_iovar_buffer_with_param()`, a variable that needs input parameters, sent as a raw command instead of through `get_iovar` — name + NUL + param (`paramlen` bytes) formatted by `whd_iovar_mkbuf` (`whd/src/whd_wifi_api.c:5219-5239`); `out_length` bytes sent; response copied back up to `out_length` (`whd/src/whd_wifi_api.c:5261-5277`). `whd_iovar_mkbuf` copies the name with `strncpy(..., strlen(name))`, which writes no NUL; the NUL is there only if the caller's buffer was already zero at that byte (`whd/src/whd_wifi_api.c:5224`, `whd/src/whd_wifi_api.c:5237`) — `whd/src/whd_wifi_api.c:5272`
- c-driver — `cyw43_clm_load()` reads `clmload_status` after the CLM download — 19 bytes: `clmload_status\0` (15) + 4 zero bytes; response u32 at bytes 0..4, non-zero = failure (`c-driver/cyw43_ll.c:1527-1533`) — `c-driver/cyw43_ll.c:1528`
- c-driver — `cyw43_read_iovar_u32()`, generic u32 read; callers read `pm2_sleep_ret`, `bcn_li_bcn`, `bcn_li_dtim`, `assoc_listen` (`c-driver/cyw43_ll.c:2180-2183`; the same four reads at `c-driver/cyw43_ll.c:2159-2162` sit inside `#if 0`, `c-driver/cyw43_ll.c:2158-2163`, and are not compiled) — strlen(name) + 1 + 4 bytes: name + NUL + le32 0; response le32 at bytes 0..4 (`c-driver/cyw43_ll.c:1969-1976`) — `c-driver/cyw43_ll.c:1974`
- c-driver — builds without `NDEBUG`: get and print the CLM version string `clmver` — 128 bytes sent and received, `clmver\0` (7) at the start, the other 121 bytes not written at this site; response printed as a text string (`c-driver/cyw43_ll.c:2026-2031`) — `c-driver/cyw43_ll.c:2029`
- c-driver — `cyw43_ll_wifi_get_mac()` reads `cur_etheraddr` — 20 bytes: `cur_etheraddr\0` (14) + 6 zero bytes; response 6-byte MAC at bytes 0..6 (`c-driver/cyw43_ll.c:2077-2081`) — `c-driver/cyw43_ll.c:2078`
- c-driver — `cyw43_ll_wifi_update_multicast_filter()` reads the current `mcast_list` — 11 + 4 + 10 × 6 = 75 bytes: `mcast_list\0` + zeros; response le32 count, then count 6-byte addresses (`c-driver/cyw43_ll.c:2090-2099`; `MAX_MULTICAST_REGISTERED_ADDRESS` = 10, `c-driver/cyw43_ll.c:253`) — `c-driver/cyw43_ll.c:2092`
- c-driver — `cyw43_ll_wifi_ap_init()` reads `bss` for the AP interface to see whether the AP is already up — 8 bytes: `bss\0` + le32 interface index (`WWD_AP_INTERFACE`); response le32 at bytes 0..4, non-zero = up (`c-driver/cyw43_ll.c:2361-2369`); the source carries a "le or be?" remark (`c-driver/cyw43_ll.c:2364`) and a TODO that the call can fail with NOTASSOCIATED (`c-driver/cyw43_ll.c:2359-2360`) — `c-driver/cyw43_ll.c:2363`
- c-driver — `cyw43_ll_wifi_ap_get_stas()` reads `maxassoc`; the call is made twice in a row and only the second result is checked — 13 bytes: `maxassoc\0` (9) + le32 `WWD_AP_INTERFACE`; response le32 maximum associated stations (`c-driver/cyw43_ll.c:2468-2475`) — `c-driver/cyw43_ll.c:2470` `c-driver/cyw43_ll.c:2471`
- c-driver — `cyw43_ll_gpio_get()` (compiled only with `CYW43_GPIO`, `c-driver/cyw43_ll.c:2500`) reads chip GPIO inputs through `ccgpioin` — 9 bytes: `ccgpioin\0` only; response le32 bitmask, bit n = GPIO n (`c-driver/cyw43_ll.c:2520-2526`) — `c-driver/cyw43_ll.c:2521`
- c-driver — `cyw43_wifi_get_roam_enabled()` reads `roam_off` through the public `cyw43_ioctl` with `CYW43_IOCTL_GET_VAR` — 13 bytes: `roam_off\0` (9) + 4 zero bytes; response le32 at bytes 0..4, non-zero = roaming disabled (`c-driver/cyw43_ctrl.c:703-720`) — `c-driver/cyw43_ctrl.c:714`
- embassy — `get_iovar()`, generic "get named variable"; called from three places: `mcast_list` with a 64-byte result (`embassy/control.rs:659`), `get_iovar_u32` (`embassy/control.rs:706-711`, whose only caller reads `clmload_status` at `embassy/control.rs:259`) and `cur_etheraddr` with 6 bytes (`embassy/control.rs:849`) — 64-byte local buffer holding name + NUL, zero filled; length sent = max(name length + 1, result length); response copied from the start of the buffer, min(result length, response length) bytes (`embassy/control.rs:731-746`) — `embassy/control.rs:740`
- whd — reference that does not send: `whd_cdc_send_ioctl()` detects GET_VAR/SET_VAR — strips the leading alignment zeros before the name, adjusting `data_length` and the buffer size (`whd/src/whd_cdc_bdc.c:214-229`) — `whd/src/whd_cdc_bdc.c:212`
- whd — reference that does not send: the command log dump — treats logged GET_VAR/SET_VAR entries as name + value and prints the name with a hexdump (`whd/src/whd_chip.c:766-769`) — `whd/src/whd_chip.c:736` `whd/src/whd_chip.c:766`
- c-driver — reference that does not send: `cyw43_send_ioctl` debug trace — prints the variable name for GET_VAR/SET_VAR — `c-driver/cyw43_ll.c:914`

Differences: Request length against reply length: embassy sends max(name + 1, result length) `embassy/control.rs:738`; c-driver usually appends zero bytes for the result (`c-driver/cyw43_ll.c:1969-1976`) but sends `ccgpioin` as 9 bytes and reads 4 back (`c-driver/cyw43_ll.c:2520-2526`); linux sends strlen(name) + 1 + len `linux/brcmfmac/fwil.c:226-232`. Host-side buffer: whd's CDC path prepends alignment zeros and strips them before sending `whd/src/whd_cdc_bdc.c:354-366` `whd/src/whd_cdc_bdc.c:211-229`; whd's msgbuf path, linux, c-driver and embassy build name + NUL + value with no prefix `whd/src/whd_msgbuf_txrx.c:202-225` `linux/brcmfmac/fwil.c:166-184` `c-driver/cyw43_ll.c:1969-1976` `embassy/control.rs:731-746`. Inside embassy: a TODO above `get_iovar` says it "always returns all zeros" `embassy/control.rs:730`; the driver still relies on its results: it asserts that `clmload_status` reads 0 `embassy/control.rs:259` (an all-zero result also passes this) and that `cur_etheraddr` returns 6 bytes, which it hands out as the MAC address `embassy/control.rs:847-850`; the source does not resolve this.

### 263 SetVar
| | |
|---|---|
| Names | embassy `SetVar` `embassy/consts.rs:684` / linux `BRCMF_C_SET_VAR` `linux/brcmfmac/fwil.h:81` / whd `WLC_SET_VAR` `whd/src/include/whd_wlioctl.h:1539` (debug name table `whd/src/whd_utils.c:756`) / c-driver `WLC_SET_VAR` (internal, value 263) `c-driver/cyw43_ll.c:185` (name table `c-driver/cyw43_ll.c:883`), public `CYW43_IOCTL_SET_VAR` = 527 (0x20f) = 263 shifted left by 1, low bit 1 = set `c-driver/cyw43_ll.h:47` (decoded at `c-driver/cyw43_ll.c:1329`) |
| Direction | set `linux/brcmfmac/fwil.c:204` |
| Sent by | linux, whd, c-driver, embassy `linux/brcmfmac/fwil.c:204` `whd/src/whd_cdc_bdc.c:333` `c-driver/cyw43_ll.c:1543` `embassy/control.rs:726`. whd's per-variable call sites do not name the constant; they call `whd_proto_set_iovar` (74 calls) or `whd_proto_get_iovar` (23 calls), which reach the two transport functions listed below `whd/src/whd_cdc_bdc.c:333`. linux's many callers of the `brcmf_fil_iovar_*`, `brcmf_fil_bsscfg_*` and `brcmf_fil_xtlv_*` set helpers are represented by the three funnel functions listed below `linux/brcmfmac/fwil.c:204`. pico-sdk: no reference to this command, not found in these sources |
| Payload | Variable name, ASCII, NUL-terminated, followed directly by the value bytes; no padding between name and value on the wire. No driver reads data back. Variable size: strlen(name) + 1 + value length. Integers little-endian. `linux/brcmfmac/fwil.c:166-184` `c-driver/cyw43_ll.c:1538-1562` `embassy/control.rs:717-726`. The value layout of each named variable is given in the variables chapters. linux builds name + NUL, then appends the data `linux/brcmfmac/fwil.c:166-184`. c-driver documents the payload as name, NUL, le32 value `c-driver/cyw43_ctrl.c:684-685` `c-driver/cyw43_ll.c:1538-1562`. embassy sends name, 0 byte, value `embassy/control.rs:717-726`. whd (CDC path) builds the buffer with leading zero bytes so the value is 4-byte aligned in host memory, then strips them before sending `whd/src/whd_cdc_bdc.c:354-366` `whd/src/whd_cdc_bdc.c:211-229`. whd's comment on this path says the value must be in the structure appropriate to the variable and that those structures are found only in the DHD source `whd/src/whd_cdc_bdc.c:311-315`. Per-BSS variant: name prefixed with `bsscfg:` and a le32 bss index as the first value bytes `linux/brcmfmac/fwil.c:248-291` `c-driver/cyw43_ll.c:2392` `c-driver/cyw43_ll.c:1546-1553`. linux XTLV variant: name + NUL, then a packed XTLV header and value `linux/brcmfmac/fwil.c:354-373`. Integer encoding: c-driver `cyw43_put_le32` `c-driver/cyw43_ll.c:1542`; embassy `to_le_bytes` `embassy/control.rs:703`; linux `cpu_to_le32` for the bss index `linux/brcmfmac/fwil.c:282`. Size caps: linux 8192-byte `proto_buf` `linux/brcmfmac/core.h:32` `linux/brcmfmac/core.h:123`; embassy 196 bytes by default and 256 for `escan` `embassy/control.rs:714` `embassy/control.rs:835`, with the CLM path bounded by `MAX_IOCTL_LEN` = 8 + 12 + 1024 `embassy/ioctl.rs:17`. c-driver's public API encodes every command as (number << 1) with the low bit set for a set `c-driver/cyw43_ll.h:47` `c-driver/cyw43_ll.c:1327-1329` |

- linux — `brcmf_fil_iovar_data_set()`, the generic "set named variable" entry used by the whole driver — name + NUL + data, buflen = strlen(name) + 1 + len, built in the 8192-byte `proto_buf` (`linux/brcmfmac/fwil.c:201-205`; `linux/brcmfmac/core.h:32`, `linux/brcmfmac/core.h:123`) — `linux/brcmfmac/fwil.c:204`
- linux — `brcmf_fil_bsscfg_data_set()`, per-BSS variable — name + NUL + data when bsscfgidx is 0, else `bsscfg:` + name + NUL + le32 bsscfgidx + data; iolen = 7 + strlen(name) + 1 + 4 + len (`linux/brcmfmac/fwil.c:259-290`, `linux/brcmfmac/fwil.c:308-312`) — `linux/brcmfmac/fwil.c:311`
- linux — `brcmf_fil_xtlv_data_set()`, variable whose value is an XTLV — name + NUL + XTLV (id, len, data) with a 32-bit alignment option (`linux/brcmfmac/fwil.c:354-373`, `linux/brcmfmac/fwil.c:389-393`) — `linux/brcmfmac/fwil.c:392`
- whd — `whd_cdc_send_iovar()` SET branch, the CDC/BDC transport's `set_iovar` (installed at `whd/src/whd_cdc_bdc.c:598` via `whd_cdc_set_iovar`, `whd/src/whd_cdc_bdc.c:125-130`); every `whd_proto_set_iovar` caller on SDIO/SPI goes through it — name + NUL, then `data_length` bytes of value (`whd/src/whd_cdc_bdc.c:349-366`); variable size; for example `whd_wifi_set_iovar_value` reserves 4 value bytes (`whd/src/whd_wifi_api.c:5153-5159`) and `whd_wifi_set_iovar_void` 0 (`whd/src/whd_wifi_api.c:5143-5150`) — `whd/src/whd_cdc_bdc.c:333`
- whd — `whd_msgbuf_set_iovar()`, the msgbuf transport's `set_iovar` (installed at `whd/src/whd_msgbuf_txrx.c:2260`) — name + NUL, then `data_length` bytes (`whd/src/whd_msgbuf_txrx.c:202-225`); variable size — `whd/src/whd_msgbuf_txrx.c:545`
- c-driver — `cyw43_clm_load()` downloads the CLM blob in chunks through `clmload` — `clmload\0` (8) + u16 flag + u16 constant 2 + u32 len + u32 constant 0 (12-byte header, `c-driver/cyw43_ll.c:1508-1515`; c-driver does not name the two constants, embassy's matching struct calls them `dload_type` and `crc`, `embassy/structs.rs:370-375`) + chunk; length sent = (20 + len) rounded up to a multiple of 8, the padding being whatever is at the end of the buffer (`c-driver/cyw43_ll.c:1521`); chunk 1024 bytes when `CYW43_USE_SPI` is set, otherwise 1024 + 512 = 1536 (`c-driver/cyw43_ll.c:1485-1489`); flag bits: 1 << 12 handler version, 2 begin, 4 end (`c-driver/cyw43_ll.c:1500-1506`); header fields stored with native-endian pointer writes, so little-endian only on a little-endian host (`c-driver/cyw43_ll.c:1512-1515`) — `c-driver/cyw43_ll.c:1522`
- c-driver — `cyw43_write_iovar_u32()`, set a u32 variable. Callers: `bus:txglom`, `apsta` (`c-driver/cyw43_ll.c:1918-1919`, `c-driver/cyw43_ll.c:2037-2038`), `allmulti` (`c-driver/cyw43_ll.c:1990`, inside `#if 0`, `c-driver/cyw43_ll.c:1978-1997`, so not compiled), `ampdu_ba_wsize` (`c-driver/cyw43_ll.c:2039`, `c-driver/cyw43_ll.c:2212`, `c-driver/cyw43_ll.c:2379`), `ampdu_mpdu` (`c-driver/cyw43_ll.c:2040`), `ampdu_rx_factor` (`c-driver/cyw43_ll.c:2041`), `pm2_sleep_ret` (`c-driver/cyw43_ll.c:2148`), `bcn_li_bcn`, `bcn_li_dtim`, `assoc_listen` (`c-driver/cyw43_ll.c:2154-2156`), `mfp` (`c-driver/cyw43_ll.c:2276`, `c-driver/cyw43_ll.c:2401`), `sae_max_pwe_loop` (`c-driver/cyw43_ll.c:2439`), `2g_mrate` (`c-driver/cyw43_ll.c:2446`) — strlen(name) + 1 + 4 bytes: name + NUL + le32 value (`c-driver/cyw43_ll.c:1538-1544`) — `c-driver/cyw43_ll.c:1543`
- c-driver — `cyw43_write_iovar_u32_u32()`, set a variable taking two u32s. Callers: `bsscfg:sup_wpa` (`c-driver/cyw43_ll.c:2240`), `bsscfg:sup_wpa2_eapver` (`c-driver/cyw43_ll.c:2244`), `bsscfg:sup_wpa_tmo` (`c-driver/cyw43_ll.c:2248`), `bsscfg:wsec` (`c-driver/cyw43_ll.c:2392`), `bsscfg:wpa_auth` (`c-driver/cyw43_ll.c:2418`), `bss` (`c-driver/cyw43_ll.c:2457`), `gpioout` (`c-driver/cyw43_ll.c:2508`, compiled only with `CYW43_GPIO`, `c-driver/cyw43_ll.c:2500`) — strlen(name) + 1 + 8 bytes: name + NUL + le32 val0 + le32 val1 (`c-driver/cyw43_ll.c:1546-1553`) — `c-driver/cyw43_ll.c:1552`
- c-driver — `cyw43_write_iovar_n()`, set a variable with an arbitrary byte value. Callers: `cur_etheraddr` 6 bytes (`c-driver/cyw43_ll.c:1941`), `mcast_list` 4 + 10 × 6 = 64 bytes (`c-driver/cyw43_ll.c:2129`), `escan` sizeof(`cyw43_wifi_scan_options_t`) (`c-driver/cyw43_ll.c:2202`), `sae_password` 2 + `CYW43_WPA_SAE_MAX_PASSWORD_LEN` (`c-driver/cyw43_ll.c:2266`, `c-driver/cyw43_ll.c:2426`), `join` 4 + 32 + 20 + 14 = 70 bytes (`c-driver/cyw43_ll.c:2325`), `bsscfg:ssid` 4 + 4 + 32 = 40 bytes (`c-driver/cyw43_ll.c:2386`) — strlen(name) + 1 + len bytes: name + NUL + value (`c-driver/cyw43_ll.c:1556-1562`) — `c-driver/cyw43_ll.c:1561`
- c-driver — `cyw43_ll_wifi_on()` sets `country` — 20 bytes: `country\0` (8) + le32 (country & 0xffff) + le32 revision (-1 if the upper 16 bits are 0, else country >> 16) + le32 (country & 0xffff) (`c-driver/cyw43_ll.c:2013-2022`) — `c-driver/cyw43_ll.c:2022`
- c-driver — `cyw43_ll_wifi_on()` sets the async event mask `bsscfg:event_msgs` (all enabled except events 20, 40, 44, 54, 71) — 18 + 4 + 19 = 41 bytes: `bsscfg:event_msgs\0` (18) + 4 bytes (bss index slot, not written at this site, left as whatever is in the buffer) + 19-byte event bitmask (`c-driver/cyw43_ll.c:2050-2060`) — `c-driver/cyw43_ll.c:2060`
- c-driver — `cyw43_wifi_set_roam_enabled()` sets `roam_off` through the public `cyw43_ioctl` with `CYW43_IOCTL_SET_VAR` — 13 bytes: `roam_off\0` (9) + le32 (1 = roaming disabled, 0 = enabled) written byte-wise (`c-driver/cyw43_ctrl.c:683-696`) — `c-driver/cyw43_ctrl.c:696`
- embassy — `load_clm()` downloads the CLM blob in chunks through `clmload` — 8 + 12 + chunk bytes: `clmload\0` + `DownloadHeader` {flag u16, dload_type u16, len u32, crc u32} (12 bytes, `embassy/structs.rs:370-375`) + chunk; chunk at most `MAX_IOCTL_LEN` - 8 - 12 = 1024 (`embassy/control.rs:229`; `embassy/ioctl.rs:17`); length not rounded; header serialised by `to_bytes()` of a `repr(C)` struct, so host byte order; flag constants at `embassy/structs.rs:380-385` — `embassy/control.rs:254`
- embassy — `set_iovar_v()`, generic "set named variable"; reached from `set_iovar` (196-byte buffer, `embassy/control.rs:713-715`), `set_iovar_u32` (`embassy/control.rs:702-704`), `set_iovar_u32x2` (`embassy/control.rs:695-700`) and directly for `escan` with a 256-byte buffer (`embassy/control.rs:835`). `set_iovar` callers: `country` (`embassy/control.rs:284`), `bsscfg:event_msgs` (`embassy/control.rs:319`), `sae_password` (`embassy/control.rs:429`, `embassy/control.rs:635`), `bsscfg:ssid` (`embassy/control.rs:583`), `mkeep_alive` (`embassy/control.rs:692`). The `apsta` and `ampdu_rx_factor` writes are commented out with the remark "this crashes" (`embassy/control.rs:294`, `embassy/control.rs:300`) — name length + 1 + value length bytes: name, 0 byte, value (`embassy/control.rs:717-726`); u32 values little-endian (`embassy/control.rs:695-704`) — `embassy/control.rs:726`
- embassy — `apply_multicast_filter()`: the runner writes `mcast_list`, replacing the whole list in one write — 11 + 4 + 6 × `MULTICAST_FILTER_SIZE` bytes: `mcast_list\0` + le32 count + 6-byte addresses; the full fixed-size buffer is sent, unused slots zero (`embassy/runner.rs:1390-1399`). `MULTICAST_FILTER_SIZE` comes from a crate outside these sources, so the byte total cannot be stated — `embassy/runner.rs:1399`
- embassy — `apply_multicast_filter()` sets `allmulti` when the filter overflowed or stopped overflowing — 9 + 4 = 13 bytes: `allmulti\0` + le32 0 or 1 (`embassy/runner.rs:1403-1408`) — `embassy/runner.rs:1408`
- whd — reference that does not send: `whd_cdc_send_ioctl()` detects GET_VAR/SET_VAR — strips the leading alignment zeros before the name (`whd/src/whd_cdc_bdc.c:214-229`) — `whd/src/whd_cdc_bdc.c:212`
- whd — reference that does not send: the command log dump — prints the name and a hexdump of the value for logged SET_VAR entries (`whd/src/whd_chip.c:761-764`) — `whd/src/whd_chip.c:735` `whd/src/whd_chip.c:761`
- c-driver — reference that does not send: `cyw43_send_ioctl` debug trace — prints the variable name for GET_VAR/SET_VAR — `c-driver/cyw43_ll.c:914`
- c-driver — reference that does not send: a second `bsscfg:event_msgs` write inside a block comment, never compiled — 4 + 18 = 22 value bytes, explicit zero index — `c-driver/cyw43_ll.c:2291-2294`
- embassy — reference that does not send: unit tests — assert that the pending command during join/scan is `SetVar` — `embassy/control.rs:996` `embassy/control.rs:1157` `embassy/control.rs:1203` `embassy/control.rs:1251`

Differences: `clmload` length: c-driver rounds the length up to a multiple of 8 and lets the padding be whatever is in the buffer `c-driver/cyw43_ll.c:1521-1522`; embassy sends the exact length `embassy/control.rs:254`. `clmload` chunk size: c-driver 1024 bytes when `CYW43_USE_SPI` is set and 1536 otherwise `c-driver/cyw43_ll.c:1485-1489`; embassy at most 1024 `embassy/control.rs:229` `embassy/ioctl.rs:17`. `allmulti`: embassy's runner sets it `embassy/runner.rs:1403-1408`; c-driver's only write is inside `#if 0` `c-driver/cyw43_ll.c:1978-1997`. `bsscfg:event_msgs` in c-driver: the only live write never fills the 4-byte bss index between the name and the 19-byte mask `c-driver/cyw43_ll.c:2051-2060`. `sae_max_pwe_loop` in c-driver: the call passes (name, `WWD_AP_INTERFACE`, 5) against the helper's signature (var, val, iface), so as written the value sent is 1 (`WWD_AP_INTERFACE` = 1) and the interface is 5 `c-driver/cyw43_ll.c:2439` `c-driver/cyw43_ll.c:1538` `c-driver/cyw43_ll.c:152`. Host-side buffer: whd's CDC path prepends alignment zeros and strips them before sending `whd/src/whd_cdc_bdc.c:354-366` `whd/src/whd_cdc_bdc.c:211-229`; the other drivers build name + NUL + value directly `linux/brcmfmac/fwil.c:166-184` `c-driver/cyw43_ll.c:1538-1562` `embassy/control.rs:717-726`.

### 264 NvramGet
| | |
|---|---|
| Names | embassy `NvramGet` `embassy/consts.rs:685` / linux not defined / whd `WLC_NVRAM_GET` `whd/src/include/whd_wlioctl.h:1540` (debug name table `whd/src/whd_utils.c:757`) / c-driver not defined |
| Direction | get (inferred from the name; no call site) |
| Sent by | no driver in these sources sends it |
| Payload | not shown by any driver |

### 265 NvramSet
| | |
|---|---|
| Names | embassy `NvramSet` `embassy/consts.rs:686` / linux not defined / whd `WLC_NVRAM_SET` `whd/src/include/whd_wlioctl.h:1541` (debug name table `whd/src/whd_utils.c:758`) / c-driver not defined |
| Direction | set (inferred from the name; no call site) |
| Sent by | no driver in these sources sends it |
| Payload | not shown by any driver |

### 266 NvramDump
| | |
|---|---|
| Names | embassy `NvramDump` `embassy/consts.rs:687` / linux not defined / whd `WLC_NVRAM_DUMP` `whd/src/include/whd_wlioctl.h:1542` (debug name table `whd/src/whd_utils.c:759`) / c-driver not defined |
| Direction | unknown |
| Sent by | no driver in these sources sends it |
| Payload | not shown by any driver |

### 267 Reboot
| | |
|---|---|
| Names | embassy `Reboot` `embassy/consts.rs:688` / linux: not defined (`BRCMF_C_` list has 263 then 268, its last) `linux/brcmfmac/fwil.h:81-82` / whd `WLC_REBOOT` `whd/src/include/whd_wlioctl.h:1543` `whd/src/include_helium/whd_wlioctl.h:1543` `whd/src/whd_utils.c:760` / c-driver: not defined (only 268 in this range) `c-driver/cyw43_ll.c:187` / pico-sdk: not found in these sources |
| Direction | unknown; the name gives no direction and no call site was found in these sources `embassy/consts.rs:688` `whd/src/include/whd_wlioctl.h:1543` |
| Sent by | none; a call site is not found in these sources, the number is only defined `embassy/consts.rs:688` `whd/src/include/whd_wlioctl.h:1543` |
| Payload | not found in these sources (no call site; the number is only defined) `embassy/consts.rs:688` `whd/src/include/whd_wlioctl.h:1543` |

### 268 SetWsecPmk
| | |
|---|---|
| Names | embassy `SetWsecPmk` `embassy/consts.rs:689` / linux `BRCMF_C_SET_WSEC_PMK` `linux/brcmfmac/fwil.h:82` / whd `WLC_SET_WSEC_PMK` `whd/src/include/whd_wlioctl.h:1544` `whd/src/include_helium/whd_wlioctl.h:1544`, also public enumerator `WHD_IOCTL_SET_WSEC_PMK` = 268 `whd/inc/whd_types.h:471` (no user in these sources), debug name tables `whd/src/whd_utils.c:761` `whd/src/whd_utils.c:1077-1080` / c-driver `WLC_SET_WSEC_PMK` `c-driver/cyw43_ll.c:187`, debug name table `c-driver/cyw43_ll.c:885` / pico-sdk: not found in these sources |
| Direction | set `embassy/control.rs:418` `linux/brcmfmac/cfg80211.c:1730` `whd/src/whd_wifi_api.c:770` `c-driver/cyw43_ll.c:2258` |
| Sent by | embassy `embassy/control.rs:418` `embassy/control.rs:625` / linux `linux/brcmfmac/cfg80211.c:1730` / whd `whd/src/whd_wifi_api.c:770` `whd/src/whd_wifi_api.c:1176` `whd/src/whd_ap.c:502` / c-driver `c-driver/cyw43_ll.c:2258` `c-driver/cyw43_ll.c:2434` |
| Payload | Key record, all drivers: offset 0 u16 key length in bytes; offset 2 u16 flags, bit 0 named `WSEC_PASSPHRASE` / `BRCMF_WSEC_PASSPHRASE`, set by the drivers for a passphrase and left 0 for a raw key; offset 4 key bytes. Both u16 are written little-endian by linux (`__le16`), whd (`htod16`) and c-driver (`cyw43_put_le16`); embassy sends the `repr(C)` struct in host byte order, which is little-endian on its targets (inferred) `embassy/structs.rs:12-13` `whd/src/include/whd_wlioctl.h:785` `whd/src/whd_wifi_api.c:761-765` `c-driver/cyw43_ll.c:2252-2253` `embassy/control.rs:407-410` `linux/brcmfmac/cfg80211.c:1742`. Total size sent differs by driver: embassy 68 (64-byte key field) `embassy/structs.rs:408-414`; c-driver 68 (4 + 64) `c-driver/cyw43_ll.c:2258` `c-driver/cyw43_ll.c:277`; whd `sizeof(wsec_pmk_t)`, 65-byte key field, 70 on a host compiler with 2-byte alignment (struct is outside the header's `#pragma pack(1)` regions) `whd/src/include/whd_wlioctl.h:781` `whd/src/include/whd_wlioctl.h:786-791` `whd/src/include/whd_wlioctl.h:3864` `whd/src/whd_wifi_api.c:756`; linux 132 (128-byte key field) `linux/brcmfmac/fwil_types.h:584-588` `linux/brcmfmac/fwil_types.h:68` `linux/brcmfmac/fwil_types.h:66` |

- embassy — `join()`: sets the passphrase or pre-hashed key when the join uses WPA, WPA2 or WPA2/WPA3 mixed; sent on interface 0 after a 3 ms delay — `PassphraseInfo { len: u16, flags: u16, passphrase: [u8; 64] }`, 68 bytes; flags bit 0 set unless `options.passphrase_is_prehashed` — `embassy/control.rs:418` `embassy/control.rs:407-417` `embassy/structs.rs:408-414`
- embassy — `set_ap_wpa2_passphrase()`: WPA2 passphrase when starting an access point (called from `start_ap`, which waits 100 ms before this step; no delay inside the function); sent with iface argument 0 — `PassphraseInfo`, 68 bytes, flags 1 — `embassy/control.rs:625` `embassy/control.rs:619-624` `embassy/control.rs:602` `embassy/control.rs:606` `embassy/control.rs:598`
- linux — `brcmf_set_wsec(ifp, key, key_len, flags)`: the only place linux sends the command; rejects `key_len` larger than the key field — `struct brcmf_wsec_pmk_le { __le16 key_len; __le16 flags; u8 key[128]; }`, zero-filled, whole struct sent, 132 bytes — `linux/brcmfmac/cfg80211.c:1730` `linux/brcmfmac/cfg80211.c:1716` `linux/brcmfmac/cfg80211.c:1722` `linux/brcmfmac/cfg80211.h:501`
- linux — `brcmf_set_pmk()`: wrapper, raw key — 132 bytes, flags 0 — `linux/brcmfmac/cfg80211.c:1742`
- linux — `brcmf_link_down()`: clears the key on link down when the profile's `use_fwsup` is not `BRCMF_PROFILE_FWSUP_NONE` and the bus is up — 132 bytes, key_len 0, flags 0, key all zero — `linux/brcmfmac/cfg80211.c:1775-1777`
- linux — `brcmf_cfg80211_connect()`: PSK offload, when the profile's `use_fwsup` is `BRCMF_PROFILE_FWSUP_PSK` — 132 bytes, key_len 32 (`BRCMF_WSEC_MAX_PSK_LEN`), flags 0, 32-byte PSK — `linux/brcmfmac/cfg80211.c:2547-2548` `linux/brcmfmac/fwil_types.h:65`
- linux — `brcmf_cfg80211_connect()`: SAE offload path, sets the 32-byte PSK (if one was given) after the vendor set_sae_password call — 132 bytes, key_len 32, flags 0 — `linux/brcmfmac/cfg80211.c:2560`
- linux — `brcmf_cfg80211_start_ap()`: AP PSK offload — 132 bytes, key_len 32, flags 0 — `linux/brcmfmac/cfg80211.c:5409` `linux/brcmfmac/cfg80211.c:5407`
- linux — `brcmf_cfg80211_stop_ap()`: clears the PSK if the profile's `use_fwauth` has the `BRCMF_PROFILE_FWAUTH_PSK` bit — 132 bytes, key_len 0, flags 0 — `linux/brcmfmac/cfg80211.c:5526-5527`
- linux — `brcmf_cfg80211_set_pmk()`: 802.1X PMK from cfg80211; rejects `pmk_len` above 32 — 132 bytes, key_len = `conf->pmk_len`, flags 0 — `linux/brcmfmac/cfg80211.c:6091` `linux/brcmfmac/cfg80211.c:6080` `linux/brcmfmac/fwil_types.h:65`
- linux — `brcmf_cfg80211_del_pmk()`: clears the PMK; only when the profile's `use_fwsup` is `BRCMF_PROFILE_FWSUP_1X` — 132 bytes, key_len 0, flags 0 — `linux/brcmfmac/cfg80211.c:6104` `linux/brcmfmac/cfg80211.c:6101`
- linux — `brcmf_wcc_set_sae_pwd()`: WCC vendor path sends the SAE password through this command — 132 bytes, key_len = password length (up to 128), flags 1 (`BRCMF_WSEC_PASSPHRASE`) — `linux/brcmfmac/wcc/core.c:19` `linux/brcmfmac/fwil_types.h:66`
- whd — `whd_wifi_set_passphrase()`: key length checked 8..64 (`KEY_MIN_LEN`, `KEY_MAX_LEN`); 1 ms delay before sending; called from `whd_wifi_enable_sup_set_passphrase` and `whd_wifi_prepare_join` — `wsec_pmk_t { uint16_t key_len; uint16_t flags; uint8_t key[65]; }`, zero-filled, key_len and flags through `htod16`; flags 0 if the interface has `WHD_SEC_JOIN_OP_PMK`, else `WSEC_PASSPHRASE` — `whd/src/whd_wifi_api.c:770` `whd/src/whd_wifi_api.c:746` `whd/src/whd_wifi_api.c:96-97` `whd/src/whd_wifi_api.c:756` `whd/src/whd_wifi_api.c:759` `whd/src/whd_wifi_api.c:762-768` `whd/src/whd_wifi_api.c:1131` `whd/src/whd_wifi_api.c:1853`
- whd — `whd_wifi_set_pmk()`: accepts only 32- or 48-byte keys; 1 ms delay before sending — `wsec_pmk_t`; a 48-byte key is copied raw with flags 0; a 32-byte key is converted to 64 lower-case hex characters, key_len 64, flags `WSEC_PASSPHRASE` — `whd/src/whd_wifi_api.c:1176` `whd/src/whd_wifi_api.c:1143` `whd/src/whd_wifi_api.c:1153` `whd/src/whd_wifi_api.c:1156-1170` `whd/src/whd_wifi_api.c:1174`
- whd — `whd_wifi_init_ap()`: passphrase for a secured soft AP; 1 ms delay before sending — `wsec_pmk_t`, not zero-filled at this call site (bytes past the key are whatever the buffer held); flags 0 with `WHD_SEC_JOIN_OP_PMK`, else `WSEC_PASSPHRASE` — `whd/src/whd_ap.c:502` `whd/src/whd_ap.c:483-500` `whd/src/whd_ap.c:333`
- c-driver — station join, any auth type except open and WPA3-SAE-only; sent on `WWD_STA_INTERFACE` after a 2 ms delay — raw buffer, 68 bytes: key_len LE16, flags LE16 = 1, key at offset 4; the buffer is a 130-byte stack array not cleared before this use, so bytes between the end of the key and offset 68 are whatever the stack held — `c-driver/cyw43_ll.c:2258` `c-driver/cyw43_ll.c:2250-2255` `c-driver/cyw43_ll.c:2210` `c-driver/cyw43_ll.c:277`
- c-driver — access point start, when `wpa_auth` has a PSK bit; sent on `WWD_AP_INTERFACE` after a 2 ms delay — raw buffer, 2 + 2 + 64 = 68 bytes: key_len LE16, flags 1, key area zeroed then key copied — `c-driver/cyw43_ll.c:2434` `c-driver/cyw43_ll.c:2428-2433`

Differences: Record size: embassy 68, c-driver 68, whd 70 (`sizeof`, host-compiler value), linux 132. `embassy/structs.rs:408-414` `c-driver/cyw43_ll.c:2258` `whd/src/include/whd_wlioctl.h:786-791` `linux/brcmfmac/fwil_types.h:584-588` whd length in the CDC header: the CDC layer takes the data length from the buffer size minus `sizeof(bus_common_header_t)` and `sizeof(cdc_header_t)`, and the buffer is allocated as `IOCTL_OFFSET + sizeof(wsec_pmk_t)`. `IOCTL_OFFSET` is `sizeof(whd_buffer_header_t) + 12 + 16`; `bus_common_header_t` is a `whd_buffer_header_t` plus a 12-byte array and `cdc_header_t` is four packed u32 (16 bytes), so the length sent is `sizeof(wsec_pmk_t)`, 70. `whd/src/whd_cdc_bdc.c:202-205` `whd/src/whd_cdc_bdc.c:234` `whd/src/whd_cdc_bdc.c:391` `whd/src/whd_cdc_bdc.c:57` `whd/src/include/whd_sdpcm.h:54` `whd/src/include/whd_sdpcm.h:75-79` `whd/src/include/whd_cdc_bdc.h:71-78` The include_helium copy of `wsec_pmk_t` has the same three fields plus a commented-out BSSID line, so the same size. `whd/src/include_helium/whd_wlioctl.h:786-792` Raw 32-byte key: linux sends it raw with flags 0; whd `whd_wifi_set_pmk` hex-encodes it to 64 characters and sends key_len 64 with flags 1. `linux/brcmfmac/cfg80211.c:2548` `whd/src/whd_wifi_api.c:1165-1170` SAE password: linux's WCC vendor path sends it through this command with flags 1; linux's CYW vendor path, c-driver, embassy and whd send it with the separate `sae_password` named variable. `linux/brcmfmac/wcc/core.c:19-20` `linux/brcmfmac/cyw/core.c:43` `c-driver/cyw43_ll.c:2426` `embassy/control.rs:635` `whd/src/whd_wifi_api.c:791-800` `whd/src/include/whd_wlioctl.h:1247` AP interface: c-driver sends on the AP interface; embassy passes iface 0. `c-driver/cyw43_ll.c:2434` `embassy/control.rs:625` Delay before sending: whd 1 ms at all three sites, c-driver 2 ms at both sites, embassy 3 ms in `join()` and none inside `set_ap_wpa2_passphrase()`; linux has no delay inside `brcmf_set_wsec` (its callers were not checked for delays). `whd/src/whd_wifi_api.c:767-768` `whd/src/whd_wifi_api.c:1174` `whd/src/whd_ap.c:500` `c-driver/cyw43_ll.c:2255` `c-driver/cyw43_ll.c:2433` `embassy/control.rs:417` `embassy/control.rs:618-627` `linux/brcmfmac/cfg80211.c:1710-1737` Clearing: linux sends key_len 0 with an all-zero key from its link-down, stop-AP and del-PMK paths; no call site in embassy, whd or c-driver sends a zero-length key (whd rejects lengths below 8 in `whd_wifi_set_passphrase` and anything but 32 or 48 in `whd_wifi_set_pmk`). `whd/src/whd_wifi_api.c:746` `whd/src/whd_wifi_api.c:1143` `linux/brcmfmac/cfg80211.c:1777` `linux/brcmfmac/cfg80211.c:5527` `linux/brcmfmac/cfg80211.c:6104`

### 269 GetAuthMode
| | |
|---|---|
| Names | embassy `GetAuthMode` `embassy/consts.rs:690` / linux: not defined (`BRCMF_C_` list has 263 then 268, its last) `linux/brcmfmac/fwil.h:81-82` / whd `WLC_GET_AUTH_MODE` `whd/src/include/whd_wlioctl.h:1545` `whd/src/include_helium/whd_wlioctl.h:1545` `whd/src/whd_utils.c:762` / c-driver: not defined (only 268 in this range) `c-driver/cyw43_ll.c:187` / pico-sdk: not found in these sources |
| Direction | get (inferred from the name) `embassy/consts.rs:690` `whd/src/include/whd_wlioctl.h:1545` |
| Sent by | none; a call site is not found in these sources, the number is only defined `embassy/consts.rs:690` `whd/src/include/whd_wlioctl.h:1545` |
| Payload | not found in these sources (no call site; the number is only defined) `embassy/consts.rs:690` `whd/src/include/whd_wlioctl.h:1545` |

### 270 SetAuthMode
| | |
|---|---|
| Names | embassy `SetAuthMode` `embassy/consts.rs:691` / linux: not defined (`BRCMF_C_` list has 263 then 268, its last) `linux/brcmfmac/fwil.h:81-82` / whd `WLC_SET_AUTH_MODE` `whd/src/include/whd_wlioctl.h:1546` `whd/src/include_helium/whd_wlioctl.h:1546` `whd/src/whd_utils.c:763` / c-driver: not defined (only 268 in this range) `c-driver/cyw43_ll.c:187` / pico-sdk: not found in these sources |
| Direction | set (inferred from the name) `embassy/consts.rs:691` `whd/src/include/whd_wlioctl.h:1546` |
| Sent by | none; a call site is not found in these sources, the number is only defined `embassy/consts.rs:691` `whd/src/include/whd_wlioctl.h:1546` |
| Payload | not found in these sources (no call site; the number is only defined) `embassy/consts.rs:691` `whd/src/include/whd_wlioctl.h:1546` |

### 271 GetWakeentry
| | |
|---|---|
| Names | embassy `GetWakeentry` `embassy/consts.rs:692` / linux: not defined (`BRCMF_C_` list has 263 then 268, its last) `linux/brcmfmac/fwil.h:81-82` / whd `WLC_GET_WAKEENTRY` `whd/src/include/whd_wlioctl.h:1547` `whd/src/include_helium/whd_wlioctl.h:1547` `whd/src/whd_utils.c:764` / c-driver: not defined (only 268 in this range) `c-driver/cyw43_ll.c:187` / pico-sdk: not found in these sources |
| Direction | get (inferred from the name) `embassy/consts.rs:692` `whd/src/include/whd_wlioctl.h:1547` |
| Sent by | none; a call site is not found in these sources, the number is only defined `embassy/consts.rs:692` `whd/src/include/whd_wlioctl.h:1547` |
| Payload | not found in these sources (no call site; the number is only defined) `embassy/consts.rs:692` `whd/src/include/whd_wlioctl.h:1547` |

### 272 SetWakeentry
| | |
|---|---|
| Names | embassy `SetWakeentry` `embassy/consts.rs:693` / linux: not defined (`BRCMF_C_` list has 263 then 268, its last) `linux/brcmfmac/fwil.h:81-82` / whd `WLC_SET_WAKEENTRY` `whd/src/include/whd_wlioctl.h:1548` `whd/src/include_helium/whd_wlioctl.h:1548` `whd/src/whd_utils.c:765` / c-driver: not defined (only 268 in this range) `c-driver/cyw43_ll.c:187` / pico-sdk: not found in these sources |
| Direction | set (inferred from the name) `embassy/consts.rs:693` `whd/src/include/whd_wlioctl.h:1548` |
| Sent by | none; a call site is not found in these sources, the number is only defined `embassy/consts.rs:693` `whd/src/include/whd_wlioctl.h:1548` |
| Payload | not found in these sources (no call site; the number is only defined) `embassy/consts.rs:693` `whd/src/include/whd_wlioctl.h:1548` |

### 273 NdconfigItem
| | |
|---|---|
| Names | embassy `NdconfigItem` `embassy/consts.rs:694` / linux: not defined (`BRCMF_C_` list has 263 then 268, its last) `linux/brcmfmac/fwil.h:81-82` / whd `WLC_NDCONFIG_ITEM` `whd/src/include/whd_wlioctl.h:1549` `whd/src/include_helium/whd_wlioctl.h:1549` `whd/src/whd_utils.c:766`, unused OID alias `OID_WL_NDCONFIG_ITEM` `whd/src/include/whd_wlioctl.h:1596` / c-driver: not defined (only 268 in this range) `c-driver/cyw43_ll.c:187` / pico-sdk: not found in these sources |
| Direction | unknown; the name gives no direction and no call site was found in these sources `embassy/consts.rs:694` `whd/src/include/whd_wlioctl.h:1549` |
| Sent by | none; a call site is not found in these sources, the number is only defined `embassy/consts.rs:694` `whd/src/include/whd_wlioctl.h:1549` |
| Payload | not found in these sources (no call site; the number is only defined) `embassy/consts.rs:694` `whd/src/include/whd_wlioctl.h:1549` |

### 274 Nvotpw
| | |
|---|---|
| Names | embassy `Nvotpw` `embassy/consts.rs:695` / linux: not defined (`BRCMF_C_` list has 263 then 268, its last) `linux/brcmfmac/fwil.h:81-82` / whd `WLC_NVOTPW` `whd/src/include/whd_wlioctl.h:1550` `whd/src/include_helium/whd_wlioctl.h:1550` `whd/src/whd_utils.c:767` / c-driver: not defined (only 268 in this range) `c-driver/cyw43_ll.c:187` / pico-sdk: not found in these sources |
| Direction | unknown; the name gives no direction and no call site was found in these sources `embassy/consts.rs:695` `whd/src/include/whd_wlioctl.h:1550` |
| Sent by | none; a call site is not found in these sources, the number is only defined `embassy/consts.rs:695` `whd/src/include/whd_wlioctl.h:1550` |
| Payload | not found in these sources (no call site; the number is only defined) `embassy/consts.rs:695` `whd/src/include/whd_wlioctl.h:1550` |

### 275 Otpw
| | |
|---|---|
| Names | embassy `Otpw` `embassy/consts.rs:696` / linux: not defined (`BRCMF_C_` list has 263 then 268, its last) `linux/brcmfmac/fwil.h:81-82` / whd `WLC_OTPW` `whd/src/include/whd_wlioctl.h:1551` `whd/src/include_helium/whd_wlioctl.h:1551` `whd/src/whd_utils.c:768` / c-driver: not defined (only 268 in this range) `c-driver/cyw43_ll.c:187` / pico-sdk: not found in these sources |
| Direction | unknown; the name gives no direction and no call site was found in these sources `embassy/consts.rs:696` `whd/src/include/whd_wlioctl.h:1551` |
| Sent by | none; a call site is not found in these sources, the number is only defined `embassy/consts.rs:696` `whd/src/include/whd_wlioctl.h:1551` |
| Payload | not found in these sources (no call site; the number is only defined) `embassy/consts.rs:696` `whd/src/include/whd_wlioctl.h:1551` |

### 276 IovBlockGet
| | |
|---|---|
| Names | embassy `IovBlockGet` `embassy/consts.rs:697` / linux: not defined (`BRCMF_C_` list has 263 then 268, its last) `linux/brcmfmac/fwil.h:81-82` / whd `WLC_IOV_BLOCK_GET` `whd/src/include/whd_wlioctl.h:1552` `whd/src/include_helium/whd_wlioctl.h:1552` `whd/src/whd_utils.c:769` / c-driver: not defined (only 268 in this range) `c-driver/cyw43_ll.c:187` / pico-sdk: not found in these sources |
| Direction | get (inferred from the name) `embassy/consts.rs:697` `whd/src/include/whd_wlioctl.h:1552` |
| Sent by | none; a call site is not found in these sources, the number is only defined `embassy/consts.rs:697` `whd/src/include/whd_wlioctl.h:1552` |
| Payload | not found in these sources (no call site; the number is only defined) `embassy/consts.rs:697` `whd/src/include/whd_wlioctl.h:1552` |

### 277 IovModulesGet
| | |
|---|---|
| Names | embassy `IovModulesGet` `embassy/consts.rs:698` / linux: not defined (`BRCMF_C_` list has 263 then 268, its last) `linux/brcmfmac/fwil.h:81-82` / whd `WLC_IOV_MODULES_GET` `whd/src/include/whd_wlioctl.h:1553` `whd/src/include_helium/whd_wlioctl.h:1553` `whd/src/whd_utils.c:770` / c-driver: not defined (only 268 in this range) `c-driver/cyw43_ll.c:187` / pico-sdk: not found in these sources |
| Direction | get (inferred from the name) `embassy/consts.rs:698` `whd/src/include/whd_wlioctl.h:1553` |
| Sent by | none; a call site is not found in these sources, the number is only defined `embassy/consts.rs:698` `whd/src/include/whd_wlioctl.h:1553` |
| Payload | not found in these sources (no call site; the number is only defined) `embassy/consts.rs:698` `whd/src/include/whd_wlioctl.h:1553` |

### 278 SoftReset
| | |
|---|---|
| Names | embassy `SoftReset` `embassy/consts.rs:699` / linux: not defined (`BRCMF_C_` list has 263 then 268, its last) `linux/brcmfmac/fwil.h:81-82` / whd `WLC_SOFT_RESET` `whd/src/include/whd_wlioctl.h:1554` `whd/src/include_helium/whd_wlioctl.h:1554` `whd/src/whd_utils.c:771` / c-driver: not defined (only 268 in this range) `c-driver/cyw43_ll.c:187` / pico-sdk: not found in these sources |
| Direction | unknown; the name gives no direction and no call site was found in these sources `embassy/consts.rs:699` `whd/src/include/whd_wlioctl.h:1554` |
| Sent by | none; a call site is not found in these sources, the number is only defined `embassy/consts.rs:699` `whd/src/include/whd_wlioctl.h:1554` |
| Payload | not found in these sources (no call site; the number is only defined) `embassy/consts.rs:699` `whd/src/include/whd_wlioctl.h:1554` |

### 279 GetAllowMode
| | |
|---|---|
| Names | embassy `GetAllowMode` `embassy/consts.rs:700` / linux: not defined (`BRCMF_C_` list has 263 then 268, its last) `linux/brcmfmac/fwil.h:81-82` / whd `WLC_GET_ALLOW_MODE` `whd/src/include/whd_wlioctl.h:1555` `whd/src/include_helium/whd_wlioctl.h:1555` `whd/src/whd_utils.c:772` / c-driver: not defined (only 268 in this range) `c-driver/cyw43_ll.c:187` / pico-sdk: not found in these sources |
| Direction | get (inferred from the name) `embassy/consts.rs:700` `whd/src/include/whd_wlioctl.h:1555` |
| Sent by | none; a call site is not found in these sources, the number is only defined `embassy/consts.rs:700` `whd/src/include/whd_wlioctl.h:1555` |
| Payload | not found in these sources (no call site; the number is only defined) `embassy/consts.rs:700` `whd/src/include/whd_wlioctl.h:1555` |

### 280 SetAllowMode
| | |
|---|---|
| Names | embassy `SetAllowMode` `embassy/consts.rs:701` / linux: not defined (`BRCMF_C_` list has 263 then 268, its last) `linux/brcmfmac/fwil.h:81-82` / whd `WLC_SET_ALLOW_MODE` `whd/src/include/whd_wlioctl.h:1556` `whd/src/include_helium/whd_wlioctl.h:1556` `whd/src/whd_utils.c:773` / c-driver: not defined (only 268 in this range) `c-driver/cyw43_ll.c:187` / pico-sdk: not found in these sources |
| Direction | set (inferred from the name) `embassy/consts.rs:701` `whd/src/include/whd_wlioctl.h:1556` |
| Sent by | none; a call site is not found in these sources, the number is only defined `embassy/consts.rs:701` `whd/src/include/whd_wlioctl.h:1556` |
| Payload | not found in these sources (no call site; the number is only defined) `embassy/consts.rs:701` `whd/src/include/whd_wlioctl.h:1556` |

### 281 GetDesiredBssid
| | |
|---|---|
| Names | embassy `GetDesiredBssid` `embassy/consts.rs:702` / linux: not defined (`BRCMF_C_` list has 263 then 268, its last) `linux/brcmfmac/fwil.h:81-82` / whd `WLC_GET_DESIRED_BSSID` `whd/src/include/whd_wlioctl.h:1557` `whd/src/include_helium/whd_wlioctl.h:1557` `whd/src/whd_utils.c:774` / c-driver: not defined (only 268 in this range) `c-driver/cyw43_ll.c:187` / pico-sdk: not found in these sources |
| Direction | get (inferred from the name) `embassy/consts.rs:702` `whd/src/include/whd_wlioctl.h:1557` |
| Sent by | none; a call site is not found in these sources, the number is only defined `embassy/consts.rs:702` `whd/src/include/whd_wlioctl.h:1557` |
| Payload | not found in these sources (no call site; the number is only defined) `embassy/consts.rs:702` `whd/src/include/whd_wlioctl.h:1557` |

### 282 SetDesiredBssid
| | |
|---|---|
| Names | embassy `SetDesiredBssid` `embassy/consts.rs:703` / linux: not defined (`BRCMF_C_` list has 263 then 268, its last) `linux/brcmfmac/fwil.h:81-82` / whd `WLC_SET_DESIRED_BSSID` `whd/src/include/whd_wlioctl.h:1558` `whd/src/include_helium/whd_wlioctl.h:1558` `whd/src/whd_utils.c:775` / c-driver: not defined (only 268 in this range) `c-driver/cyw43_ll.c:187` / pico-sdk: not found in these sources |
| Direction | set (inferred from the name) `embassy/consts.rs:703` `whd/src/include/whd_wlioctl.h:1558` |
| Sent by | none; a call site is not found in these sources, the number is only defined `embassy/consts.rs:703` `whd/src/include/whd_wlioctl.h:1558` |
| Payload | not found in these sources (no call site; the number is only defined) `embassy/consts.rs:703` `whd/src/include/whd_wlioctl.h:1558` |

### 283 DisassocMyap
| | |
|---|---|
| Names | embassy `DisassocMyap` `embassy/consts.rs:704` / linux: not defined (`BRCMF_C_` list has 263 then 268, its last) `linux/brcmfmac/fwil.h:81-82` / whd `WLC_DISASSOC_MYAP` `whd/src/include/whd_wlioctl.h:1559` `whd/src/include_helium/whd_wlioctl.h:1559` `whd/src/whd_utils.c:776` / c-driver: not defined (only 268 in this range) `c-driver/cyw43_ll.c:187` / pico-sdk: not found in these sources |
| Direction | unknown; the name gives no direction and no call site was found in these sources `embassy/consts.rs:704` `whd/src/include/whd_wlioctl.h:1559` |
| Sent by | none; a call site is not found in these sources, the number is only defined `embassy/consts.rs:704` `whd/src/include/whd_wlioctl.h:1559` |
| Payload | not found in these sources (no call site; the number is only defined) `embassy/consts.rs:704` `whd/src/include/whd_wlioctl.h:1559` |

### 284 GetNbands
| | |
|---|---|
| Names | embassy `GetNbands` `embassy/consts.rs:705` / linux: not defined (`BRCMF_C_` list has 263 then 268, its last) `linux/brcmfmac/fwil.h:81-82` / whd `WLC_GET_NBANDS` `whd/src/include/whd_wlioctl.h:1560` `whd/src/include_helium/whd_wlioctl.h:1560` `whd/src/whd_utils.c:777`, unused OID alias `OID_STA_NBANDS` `whd/src/include/whd_wlioctl.h:1598` / c-driver: not defined (only 268 in this range) `c-driver/cyw43_ll.c:187` / pico-sdk: not found in these sources |
| Direction | get (inferred from the name) `embassy/consts.rs:705` `whd/src/include/whd_wlioctl.h:1560` |
| Sent by | none; a call site is not found in these sources, the number is only defined `embassy/consts.rs:705` `whd/src/include/whd_wlioctl.h:1560` |
| Payload | not found in these sources (no call site; the number is only defined) `embassy/consts.rs:705` `whd/src/include/whd_wlioctl.h:1560` |

### 285 GetBandstates
| | |
|---|---|
| Names | embassy `GetBandstates` `embassy/consts.rs:706` / linux: not defined (`BRCMF_C_` list has 263 then 268, its last) `linux/brcmfmac/fwil.h:81-82` / whd `WLC_GET_BANDSTATES` `whd/src/include/whd_wlioctl.h:1561` `whd/src/include_helium/whd_wlioctl.h:1561` `whd/src/whd_utils.c:778` / c-driver: not defined (only 268 in this range) `c-driver/cyw43_ll.c:187` / pico-sdk: not found in these sources |
| Direction | get (inferred from the name) `embassy/consts.rs:706` `whd/src/include/whd_wlioctl.h:1561` |
| Sent by | none; a call site is not found in these sources, the number is only defined `embassy/consts.rs:706` `whd/src/include/whd_wlioctl.h:1561` |
| Payload | not found in these sources (no call site; the number is only defined) `embassy/consts.rs:706` `whd/src/include/whd_wlioctl.h:1561` |

### 286 GetWlcBssInfo
| | |
|---|---|
| Names | embassy `GetWlcBssInfo` `embassy/consts.rs:707` / linux: not defined (`BRCMF_C_` list has 263 then 268, its last) `linux/brcmfmac/fwil.h:81-82` / whd `WLC_GET_WLC_BSS_INFO` `whd/src/include/whd_wlioctl.h:1562` `whd/src/include_helium/whd_wlioctl.h:1562` `whd/src/whd_utils.c:779` / c-driver: not defined (only 268 in this range) `c-driver/cyw43_ll.c:187` / pico-sdk: not found in these sources |
| Direction | get (inferred from the name) `embassy/consts.rs:707` `whd/src/include/whd_wlioctl.h:1562` |
| Sent by | none; a call site is not found in these sources, the number is only defined `embassy/consts.rs:707` `whd/src/include/whd_wlioctl.h:1562` |
| Payload | not found in these sources (no call site; the number is only defined) `embassy/consts.rs:707` `whd/src/include/whd_wlioctl.h:1562` |

### 287 GetAssocInfo
| | |
|---|---|
| Names | embassy `GetAssocInfo` `embassy/consts.rs:708` / linux: not defined (`BRCMF_C_` list has 263 then 268, its last) `linux/brcmfmac/fwil.h:81-82` / whd `WLC_GET_ASSOC_INFO` `whd/src/include/whd_wlioctl.h:1563` `whd/src/include_helium/whd_wlioctl.h:1563` `whd/src/whd_utils.c:780` / c-driver: not defined (only 268 in this range) `c-driver/cyw43_ll.c:187` / pico-sdk: not found in these sources |
| Direction | get (inferred from the name) `embassy/consts.rs:708` `whd/src/include/whd_wlioctl.h:1563` |
| Sent by | none; a call site is not found in these sources, the number is only defined `embassy/consts.rs:708` `whd/src/include/whd_wlioctl.h:1563` |
| Payload | not found in these sources (no call site; the number is only defined) `embassy/consts.rs:708` `whd/src/include/whd_wlioctl.h:1563` |

### 288 GetOidPhy
| | |
|---|---|
| Names | embassy `GetOidPhy` `embassy/consts.rs:709` / linux: not defined (`BRCMF_C_` list has 263 then 268, its last) `linux/brcmfmac/fwil.h:81-82` / whd `WLC_GET_OID_PHY` `whd/src/include/whd_wlioctl.h:1564` `whd/src/include_helium/whd_wlioctl.h:1564` `whd/src/whd_utils.c:781`, unused OID alias `OID_STA_GET_PHY` `whd/src/include/whd_wlioctl.h:1599` / c-driver: not defined (only 268 in this range) `c-driver/cyw43_ll.c:187` / pico-sdk: not found in these sources |
| Direction | get (inferred from the name) `embassy/consts.rs:709` `whd/src/include/whd_wlioctl.h:1564` |
| Sent by | none; a call site is not found in these sources, the number is only defined `embassy/consts.rs:709` `whd/src/include/whd_wlioctl.h:1564` |
| Payload | not found in these sources (no call site; the number is only defined) `embassy/consts.rs:709` `whd/src/include/whd_wlioctl.h:1564` |

### 289 SetOidPhy
| | |
|---|---|
| Names | embassy `SetOidPhy` `embassy/consts.rs:710` / linux: not defined (`BRCMF_C_` list has 263 then 268, its last) `linux/brcmfmac/fwil.h:81-82` / whd `WLC_SET_OID_PHY` `whd/src/include/whd_wlioctl.h:1565` `whd/src/include_helium/whd_wlioctl.h:1565` `whd/src/whd_utils.c:782`, unused OID alias `OID_STA_SET_PHY` `whd/src/include/whd_wlioctl.h:1600` / c-driver: not defined (only 268 in this range) `c-driver/cyw43_ll.c:187` / pico-sdk: not found in these sources |
| Direction | set (inferred from the name) `embassy/consts.rs:710` `whd/src/include/whd_wlioctl.h:1565` |
| Sent by | none; a call site is not found in these sources, the number is only defined `embassy/consts.rs:710` `whd/src/include/whd_wlioctl.h:1565` |
| Payload | not found in these sources (no call site; the number is only defined) `embassy/consts.rs:710` `whd/src/include/whd_wlioctl.h:1565` |

### 290 SetAssocTime
| | |
|---|---|
| Names | embassy `SetAssocTime` `embassy/consts.rs:711` / linux: not defined (`BRCMF_C_` list has 263 then 268, its last) `linux/brcmfmac/fwil.h:81-82` / whd `WLC_SET_ASSOC_TIME` `whd/src/include/whd_wlioctl.h:1566` `whd/src/include_helium/whd_wlioctl.h:1566` `whd/src/whd_utils.c:783`, unused OID alias `OID_STA_ASSOC_TIME` `whd/src/include/whd_wlioctl.h:1601` / c-driver: not defined (only 268 in this range) `c-driver/cyw43_ll.c:187` / pico-sdk: not found in these sources |
| Direction | set (inferred from the name) `embassy/consts.rs:711` `whd/src/include/whd_wlioctl.h:1566` |
| Sent by | none; a call site is not found in these sources, the number is only defined `embassy/consts.rs:711` `whd/src/include/whd_wlioctl.h:1566` |
| Payload | not found in these sources (no call site; the number is only defined) `embassy/consts.rs:711` `whd/src/include/whd_wlioctl.h:1566` |

### 291 GetDesiredSsid
| | |
|---|---|
| Names | embassy `Ioctl::GetDesiredSsid` `embassy/consts.rs:712` / linux: not defined (highest `BRCMF_C_` constant is 268) `linux/brcmfmac/fwil.h:82` / whd `WLC_GET_DESIRED_SSID` `whd/src/include/whd_wlioctl.h:1567` `whd/src/include_helium/whd_wlioctl.h:1567`, alias `OID_STA_DESIRED_SSID` = `WL_OID_BASE` + this number, with no use `whd/src/include/whd_wlioctl.h:1602` `whd/src/include/whd_wlioctl.h:1589` / c-driver: not defined (highest `WLC_` define is 268) `c-driver/cyw43_ll.c:187` / pico-sdk: not found |
| Direction | get (inferred from the name prefix only; no call site confirms it) `whd/src/include/whd_wlioctl.h:1567` |
| Sent by | no driver in these sources sends it; embassy: enum variant only `embassy/consts.rs:712`; whd: debug name table `whd_ioctl_to_string` only, compiled under `WPRINT_ENABLE_WHD_DEBUG` `whd/src/whd_utils.c:784` `whd/src/whd_utils.c:179`; absent from whd's public command lists, whose highest value is 268 `whd/inc/whd_types.h:471`; linux, c-driver, pico-sdk: not found in these sources |
| Payload | not shown by any driver |

### 292 GetChanspec
| | |
|---|---|
| Names | embassy `Ioctl::GetChanspec` `embassy/consts.rs:713` / linux: not defined (highest `BRCMF_C_` constant is 268) `linux/brcmfmac/fwil.h:82` / whd `WLC_GET_CHANSPEC` `whd/src/include/whd_wlioctl.h:1568` `whd/src/include_helium/whd_wlioctl.h:1568`, alias `OID_STA_CHANSPEC` = `WL_OID_BASE` + this number, with no use `whd/src/include/whd_wlioctl.h:1597` `whd/src/include/whd_wlioctl.h:1589` / c-driver: not defined (highest `WLC_` define is 268) `c-driver/cyw43_ll.c:187` / pico-sdk: not found |
| Direction | get (inferred from the name prefix only; no call site confirms it) `whd/src/include/whd_wlioctl.h:1568` |
| Sent by | no driver in these sources sends it; embassy: enum variant only `embassy/consts.rs:713`; whd: debug name table `whd_ioctl_to_string` only, compiled under `WPRINT_ENABLE_WHD_DEBUG` `whd/src/whd_utils.c:785` `whd/src/whd_utils.c:179`; absent from whd's public command lists, whose highest value is 268 `whd/inc/whd_types.h:471`; linux, c-driver, pico-sdk: not found in these sources |
| Payload | not shown by any driver |

### 293 GetAssocState
| | |
|---|---|
| Names | embassy `Ioctl::GetAssocState` `embassy/consts.rs:714` / linux: not defined (highest `BRCMF_C_` constant is 268) `linux/brcmfmac/fwil.h:82` / whd `WLC_GET_ASSOC_STATE` `whd/src/include/whd_wlioctl.h:1569` `whd/src/include_helium/whd_wlioctl.h:1569` / c-driver: not defined (highest `WLC_` define is 268) `c-driver/cyw43_ll.c:187` / pico-sdk: not found |
| Direction | get (inferred from the name prefix only; no call site confirms it) `whd/src/include/whd_wlioctl.h:1569` |
| Sent by | no driver in these sources sends it; embassy: enum variant only `embassy/consts.rs:714`; whd: debug name table `whd_ioctl_to_string` only, compiled under `WPRINT_ENABLE_WHD_DEBUG` `whd/src/whd_utils.c:786` `whd/src/whd_utils.c:179`; absent from whd's public command lists, whose highest value is 268 `whd/inc/whd_types.h:471`; linux, c-driver, pico-sdk: not found in these sources |
| Payload | not shown by any driver |

### 294 SetPhyState
| | |
|---|---|
| Names | embassy `Ioctl::SetPhyState` `embassy/consts.rs:715` / linux: not defined (highest `BRCMF_C_` constant is 268) `linux/brcmfmac/fwil.h:82` / whd `WLC_SET_PHY_STATE` `whd/src/include/whd_wlioctl.h:1570` `whd/src/include_helium/whd_wlioctl.h:1570`, alias `OID_STA_SET_PHY_STATE` = `WL_OID_BASE` + this number, with no use `whd/src/include/whd_wlioctl.h:1603` `whd/src/include/whd_wlioctl.h:1589` / c-driver: not defined (highest `WLC_` define is 268) `c-driver/cyw43_ll.c:187` / pico-sdk: not found |
| Direction | set (inferred from the name prefix only; no call site confirms it) `whd/src/include/whd_wlioctl.h:1570` |
| Sent by | no driver in these sources sends it; embassy: enum variant only `embassy/consts.rs:715`; whd: debug name table `whd_ioctl_to_string` only, compiled under `WPRINT_ENABLE_WHD_DEBUG` `whd/src/whd_utils.c:787` `whd/src/whd_utils.c:179`; absent from whd's public command lists, whose highest value is 268 `whd/inc/whd_types.h:471`; linux, c-driver, pico-sdk: not found in these sources |
| Payload | not shown by any driver |

### 295 GetScanPending
| | |
|---|---|
| Names | embassy `Ioctl::GetScanPending` `embassy/consts.rs:716` / linux: not defined (highest `BRCMF_C_` constant is 268) `linux/brcmfmac/fwil.h:82` / whd `WLC_GET_SCAN_PENDING` `whd/src/include/whd_wlioctl.h:1571` `whd/src/include_helium/whd_wlioctl.h:1571`, alias `OID_STA_SCAN_PENDING` = `WL_OID_BASE` + this number, with no use `whd/src/include/whd_wlioctl.h:1604` `whd/src/include/whd_wlioctl.h:1589` / c-driver: not defined (highest `WLC_` define is 268) `c-driver/cyw43_ll.c:187` / pico-sdk: not found |
| Direction | get (inferred from the name prefix only; no call site confirms it) `whd/src/include/whd_wlioctl.h:1571` |
| Sent by | no driver in these sources sends it; embassy: enum variant only `embassy/consts.rs:716`; whd: debug name table `whd_ioctl_to_string` only, compiled under `WPRINT_ENABLE_WHD_DEBUG` `whd/src/whd_utils.c:788` `whd/src/whd_utils.c:179`; absent from whd's public command lists, whose highest value is 268 `whd/inc/whd_types.h:471`; linux, c-driver, pico-sdk: not found in these sources |
| Payload | not shown by any driver |

### 296 GetScanreqPending
| | |
|---|---|
| Names | embassy `Ioctl::GetScanreqPending` `embassy/consts.rs:717` / linux: not defined (highest `BRCMF_C_` constant is 268) `linux/brcmfmac/fwil.h:82` / whd `WLC_GET_SCANREQ_PENDING` `whd/src/include/whd_wlioctl.h:1572` `whd/src/include_helium/whd_wlioctl.h:1572`, alias `OID_STA_SCANREQ_PENDING` = `WL_OID_BASE` + this number, with no use `whd/src/include/whd_wlioctl.h:1605` `whd/src/include/whd_wlioctl.h:1589` / c-driver: not defined (highest `WLC_` define is 268) `c-driver/cyw43_ll.c:187` / pico-sdk: not found |
| Direction | get (inferred from the name prefix only; no call site confirms it) `whd/src/include/whd_wlioctl.h:1572` |
| Sent by | no driver in these sources sends it; embassy: enum variant only `embassy/consts.rs:717`; whd: debug name table `whd_ioctl_to_string` only, compiled under `WPRINT_ENABLE_WHD_DEBUG` `whd/src/whd_utils.c:789` `whd/src/whd_utils.c:179`; absent from whd's public command lists, whose highest value is 268 `whd/inc/whd_types.h:471`; linux, c-driver, pico-sdk: not found in these sources |
| Payload | not shown by any driver |

### 297 GetPrevRoamReason
| | |
|---|---|
| Names | embassy `Ioctl::GetPrevRoamReason` `embassy/consts.rs:718` / linux: not defined (highest `BRCMF_C_` constant is 268) `linux/brcmfmac/fwil.h:82` / whd `WLC_GET_PREV_ROAM_REASON` `whd/src/include/whd_wlioctl.h:1573` `whd/src/include_helium/whd_wlioctl.h:1573`, alias `OID_STA_GET_ROAM_REASON` = `WL_OID_BASE` + this number, with no use `whd/src/include/whd_wlioctl.h:1606` `whd/src/include/whd_wlioctl.h:1589` / c-driver: not defined (highest `WLC_` define is 268) `c-driver/cyw43_ll.c:187` / pico-sdk: not found |
| Direction | get (inferred from the name prefix only; no call site confirms it) `whd/src/include/whd_wlioctl.h:1573` |
| Sent by | no driver in these sources sends it; embassy: enum variant only `embassy/consts.rs:718`; whd: debug name table `whd_ioctl_to_string` only, compiled under `WPRINT_ENABLE_WHD_DEBUG` `whd/src/whd_utils.c:790` `whd/src/whd_utils.c:179`; absent from whd's public command lists, whose highest value is 268 `whd/inc/whd_types.h:471`; linux, c-driver, pico-sdk: not found in these sources |
| Payload | not shown by any driver |

### 298 SetPrevRoamReason
| | |
|---|---|
| Names | embassy `Ioctl::SetPrevRoamReason` `embassy/consts.rs:719` / linux: not defined (highest `BRCMF_C_` constant is 268) `linux/brcmfmac/fwil.h:82` / whd `WLC_SET_PREV_ROAM_REASON` `whd/src/include/whd_wlioctl.h:1574` `whd/src/include_helium/whd_wlioctl.h:1574`, alias `OID_STA_SET_ROAM_REASON` = `WL_OID_BASE` + this number, with no use `whd/src/include/whd_wlioctl.h:1607` `whd/src/include/whd_wlioctl.h:1589` / c-driver: not defined (highest `WLC_` define is 268) `c-driver/cyw43_ll.c:187` / pico-sdk: not found |
| Direction | set (inferred from the name prefix only; no call site confirms it) `whd/src/include/whd_wlioctl.h:1574` |
| Sent by | no driver in these sources sends it; embassy: enum variant only `embassy/consts.rs:719`; whd: debug name table `whd_ioctl_to_string` only, compiled under `WPRINT_ENABLE_WHD_DEBUG` `whd/src/whd_utils.c:791` `whd/src/whd_utils.c:179`; absent from whd's public command lists, whose highest value is 268 `whd/inc/whd_types.h:471`; linux, c-driver, pico-sdk: not found in these sources |
| Payload | not shown by any driver |

### 299 GetBandstatesPi
| | |
|---|---|
| Names | embassy `Ioctl::GetBandstatesPi` `embassy/consts.rs:720` / linux: not defined (highest `BRCMF_C_` constant is 268) `linux/brcmfmac/fwil.h:82` / whd `WLC_GET_BANDSTATES_PI` `whd/src/include/whd_wlioctl.h:1575` `whd/src/include_helium/whd_wlioctl.h:1575` / c-driver: not defined (highest `WLC_` define is 268) `c-driver/cyw43_ll.c:187` / pico-sdk: not found |
| Direction | get (inferred from the name prefix only; no call site confirms it) `whd/src/include/whd_wlioctl.h:1575` |
| Sent by | no driver in these sources sends it; embassy: enum variant only `embassy/consts.rs:720`; whd: debug name table `whd_ioctl_to_string` only, compiled under `WPRINT_ENABLE_WHD_DEBUG` `whd/src/whd_utils.c:792` `whd/src/whd_utils.c:179`; absent from whd's public command lists, whose highest value is 268 `whd/inc/whd_types.h:471`; linux, c-driver, pico-sdk: not found in these sources |
| Payload | not shown by any driver |

### 300 GetPhyState
| | |
|---|---|
| Names | embassy `Ioctl::GetPhyState` `embassy/consts.rs:721` / linux: not defined (highest `BRCMF_C_` constant is 268) `linux/brcmfmac/fwil.h:82` / whd `WLC_GET_PHY_STATE` `whd/src/include/whd_wlioctl.h:1576` `whd/src/include_helium/whd_wlioctl.h:1576`, alias `OID_STA_GET_PHY_STATE` = `WL_OID_BASE` + this number, with no use `whd/src/include/whd_wlioctl.h:1608` `whd/src/include/whd_wlioctl.h:1589` / c-driver: not defined (highest `WLC_` define is 268) `c-driver/cyw43_ll.c:187` / pico-sdk: not found |
| Direction | get (inferred from the name prefix only; no call site confirms it) `whd/src/include/whd_wlioctl.h:1576` |
| Sent by | no driver in these sources sends it; embassy: enum variant only `embassy/consts.rs:721`; whd: debug name table `whd_ioctl_to_string` only, compiled under `WPRINT_ENABLE_WHD_DEBUG` `whd/src/whd_utils.c:793` `whd/src/whd_utils.c:179`; absent from whd's public command lists, whose highest value is 268 `whd/inc/whd_types.h:471`; linux, c-driver, pico-sdk: not found in these sources |
| Payload | not shown by any driver |

### 301 GetBssWpaRsn
| | |
|---|---|
| Names | embassy `Ioctl::GetBssWpaRsn` `embassy/consts.rs:722` / linux: not defined (highest `BRCMF_C_` constant is 268) `linux/brcmfmac/fwil.h:82` / whd `WLC_GET_BSS_WPA_RSN` `whd/src/include/whd_wlioctl.h:1577` `whd/src/include_helium/whd_wlioctl.h:1577` / c-driver: not defined (highest `WLC_` define is 268) `c-driver/cyw43_ll.c:187` / pico-sdk: not found |
| Direction | get (inferred from the name prefix only; no call site confirms it) `whd/src/include/whd_wlioctl.h:1577` |
| Sent by | no driver in these sources sends it; embassy: enum variant only `embassy/consts.rs:722`; whd: debug name table `whd_ioctl_to_string` only, compiled under `WPRINT_ENABLE_WHD_DEBUG` `whd/src/whd_utils.c:794` `whd/src/whd_utils.c:179`; absent from whd's public command lists, whose highest value is 268 `whd/inc/whd_types.h:471`; linux, c-driver, pico-sdk: not found in these sources |
| Payload | not shown by any driver |

### 302 GetBssWpa2Rsn
| | |
|---|---|
| Names | embassy `Ioctl::GetBssWpa2Rsn` `embassy/consts.rs:723` / linux: not defined (highest `BRCMF_C_` constant is 268) `linux/brcmfmac/fwil.h:82` / whd `WLC_GET_BSS_WPA2_RSN` `whd/src/include/whd_wlioctl.h:1578` `whd/src/include_helium/whd_wlioctl.h:1578` / c-driver: not defined (highest `WLC_` define is 268) `c-driver/cyw43_ll.c:187` / pico-sdk: not found |
| Direction | get (inferred from the name prefix only; no call site confirms it) `whd/src/include/whd_wlioctl.h:1578` |
| Sent by | no driver in these sources sends it; embassy: enum variant only `embassy/consts.rs:723`; whd: debug name table `whd_ioctl_to_string` only, compiled under `WPRINT_ENABLE_WHD_DEBUG` `whd/src/whd_utils.c:795` `whd/src/whd_utils.c:179`; absent from whd's public command lists, whose highest value is 268 `whd/inc/whd_types.h:471`; linux, c-driver, pico-sdk: not found in these sources |
| Payload | not shown by any driver |

### 303 GetBssBcnTs
| | |
|---|---|
| Names | embassy `Ioctl::GetBssBcnTs` `embassy/consts.rs:724` / linux: not defined (highest `BRCMF_C_` constant is 268) `linux/brcmfmac/fwil.h:82` / whd `WLC_GET_BSS_BCN_TS` `whd/src/include/whd_wlioctl.h:1579` `whd/src/include_helium/whd_wlioctl.h:1579` / c-driver: not defined (highest `WLC_` define is 268) `c-driver/cyw43_ll.c:187` / pico-sdk: not found |
| Direction | get (inferred from the name prefix only; no call site confirms it) `whd/src/include/whd_wlioctl.h:1579` |
| Sent by | no driver in these sources sends it; embassy: enum variant only `embassy/consts.rs:724`; whd: debug name table `whd_ioctl_to_string` only, compiled under `WPRINT_ENABLE_WHD_DEBUG` `whd/src/whd_utils.c:796` `whd/src/whd_utils.c:179`; absent from whd's public command lists, whose highest value is 268 `whd/inc/whd_types.h:471`; linux, c-driver, pico-sdk: not found in these sources |
| Payload | not shown by any driver |

### 304 GetIntDisassoc
| | |
|---|---|
| Names | embassy `Ioctl::GetIntDisassoc` `embassy/consts.rs:725` / linux: not defined (highest `BRCMF_C_` constant is 268) `linux/brcmfmac/fwil.h:82` / whd `WLC_GET_INT_DISASSOC` `whd/src/include/whd_wlioctl.h:1580` `whd/src/include_helium/whd_wlioctl.h:1580`, alias `OID_STA_INT_DISASSOC` = `WL_OID_BASE` + this number, with no use `whd/src/include/whd_wlioctl.h:1609` `whd/src/include/whd_wlioctl.h:1589` / c-driver: not defined (highest `WLC_` define is 268) `c-driver/cyw43_ll.c:187` / pico-sdk: not found |
| Direction | get (inferred from the name prefix only; no call site confirms it) `whd/src/include/whd_wlioctl.h:1580` |
| Sent by | no driver in these sources sends it; embassy: enum variant only `embassy/consts.rs:725`; whd: debug name table `whd_ioctl_to_string` only, compiled under `WPRINT_ENABLE_WHD_DEBUG` `whd/src/whd_utils.c:797` `whd/src/whd_utils.c:179`; absent from whd's public command lists, whose highest value is 268 `whd/inc/whd_types.h:471`; linux, c-driver, pico-sdk: not found in these sources |
| Payload | not shown by any driver |

### 305 SetNumPeers
| | |
|---|---|
| Names | embassy `Ioctl::SetNumPeers` `embassy/consts.rs:726` / linux: not defined (highest `BRCMF_C_` constant is 268) `linux/brcmfmac/fwil.h:82` / whd `WLC_SET_NUM_PEERS` `whd/src/include/whd_wlioctl.h:1581` `whd/src/include_helium/whd_wlioctl.h:1581`, alias `OID_STA_SET_NUM_PEERS` = `WL_OID_BASE` + this number, with no use `whd/src/include/whd_wlioctl.h:1610` `whd/src/include/whd_wlioctl.h:1589` / c-driver: not defined (highest `WLC_` define is 268) `c-driver/cyw43_ll.c:187` / pico-sdk: not found |
| Direction | set (inferred from the name prefix only; no call site confirms it) `whd/src/include/whd_wlioctl.h:1581` |
| Sent by | no driver in these sources sends it; embassy: enum variant only `embassy/consts.rs:726`; whd: debug name table `whd_ioctl_to_string` only, compiled under `WPRINT_ENABLE_WHD_DEBUG` `whd/src/whd_utils.c:798` `whd/src/whd_utils.c:179`; absent from whd's public command lists, whose highest value is 268 `whd/inc/whd_types.h:471`; linux, c-driver, pico-sdk: not found in these sources |
| Payload | not shown by any driver |

### 306 GetNumBss
| | |
|---|---|
| Names | embassy `Ioctl::GetNumBss` `embassy/consts.rs:727`, numbers 307-317 skipped, next variant is 318 `embassy/consts.rs:728` / linux: not defined (highest `BRCMF_C_` constant is 268) `linux/brcmfmac/fwil.h:82` / whd `WLC_GET_NUM_BSS` `whd/src/include/whd_wlioctl.h:1582` `whd/src/include_helium/whd_wlioctl.h:1582`, alias `OID_STA_GET_NUM_BSS` = `WL_OID_BASE` + this number, with no use `whd/src/include/whd_wlioctl.h:1611` `whd/src/include/whd_wlioctl.h:1589`, numbers 307-317 skipped, next define is 318 `whd/src/include/whd_wlioctl.h:1583` / c-driver: not defined (highest `WLC_` define is 268) `c-driver/cyw43_ll.c:187` / pico-sdk: not found |
| Direction | get (inferred from the name prefix only; no call site confirms it) `whd/src/include/whd_wlioctl.h:1582` |
| Sent by | no driver in these sources sends it; embassy: enum variant only `embassy/consts.rs:727`; whd: debug name table `whd_ioctl_to_string` only, compiled under `WPRINT_ENABLE_WHD_DEBUG` `whd/src/whd_utils.c:799` `whd/src/whd_utils.c:179`; absent from whd's public command lists, whose highest value is 268 `whd/inc/whd_types.h:471`; linux, c-driver, pico-sdk: not found in these sources |
| Payload | not shown by any driver |

### 318 GetWsecPmk
| | |
|---|---|
| Names | embassy `Ioctl::GetWsecPmk` `embassy/consts.rs:728` / linux: not defined (highest `BRCMF_C_` constant is 268) `linux/brcmfmac/fwil.h:82` / whd `WLC_GET_WSEC_PMK` `whd/src/include/whd_wlioctl.h:1583` `whd/src/include_helium/whd_wlioctl.h:1583` / c-driver: not defined (highest `WLC_` define is 268) `c-driver/cyw43_ll.c:187` / pico-sdk: not found |
| Direction | get (inferred from the name prefix only; no call site confirms it) `whd/src/include/whd_wlioctl.h:1583` |
| Sent by | no driver in these sources sends it; embassy: enum variant only `embassy/consts.rs:728`; whd: debug name table `whd_ioctl_to_string` only, compiled under `WPRINT_ENABLE_WHD_DEBUG` `whd/src/whd_utils.c:800` `whd/src/whd_utils.c:179`; absent from whd's public command lists, whose highest value is 268 `whd/inc/whd_types.h:471`; linux, c-driver, pico-sdk: not found in these sources |
| Payload | not shown by any driver; the set form, 268, is the one drivers send `embassy/control.rs:418` `embassy/control.rs:625` `linux/brcmfmac/cfg80211.c:1730` `c-driver/cyw43_ll.c:2258` `c-driver/cyw43_ll.c:2434` `whd/src/whd_wifi_api.c:770` `whd/src/whd_wifi_api.c:1176` `whd/src/whd_ap.c:502`; no source shows that this get form returns the same layout |

### 319 GetRandomBytes
| | |
|---|---|
| Names | embassy `Ioctl::GetRandomBytes` `embassy/consts.rs:729`, last variant of the `Ioctl` enum / linux: not defined (highest `BRCMF_C_` constant is 268) `linux/brcmfmac/fwil.h:82` / whd `WLC_GET_RANDOM_BYTES` `whd/src/include/whd_wlioctl.h:1584` `whd/src/include_helium/whd_wlioctl.h:1584`, last command before `WLC_LAST` = 320 `whd/src/include/whd_wlioctl.h:1585` / c-driver: not defined (highest `WLC_` define is 268) `c-driver/cyw43_ll.c:187` / pico-sdk: not found |
| Direction | get (inferred from the name prefix only; no call site confirms it) `whd/src/include/whd_wlioctl.h:1584` |
| Sent by | no driver in these sources sends it; embassy: enum variant only `embassy/consts.rs:729`; whd: debug name table `whd_ioctl_to_string` only, compiled under `WPRINT_ENABLE_WHD_DEBUG` `whd/src/whd_utils.c:801` `whd/src/whd_utils.c:179`; absent from whd's public command lists, whose highest value is 268 `whd/inc/whd_types.h:471`; linux, c-driver, pico-sdk: not found in these sources |
| Payload | not shown by any driver |

## Commands outside embassy's list

### 28 BRCMF_C_TERMINATED
| | |
|---|---|
| Names | embassy not defined: the enum goes from `Restart` = 27 to `GetChannel` = 29 `embassy/consts.rs:469-470` / linux `BRCMF_C_TERMINATED` `linux/brcmfmac/fwil.h:26` / whd not defined: its list goes from `WLC_RESTART` = 27 to `WLC_GET_CHANNEL` = 29 in both headers `whd/src/include/whd_wlioctl.h:1324-1325` `whd/src/include_helium/whd_wlioctl.h:1324-1325` / c-driver not defined `c-driver/cyw43_ll.c:167-187` |
| Direction | set `linux/brcmfmac/core.c:1437` |
| Sent by | linux only, and only from its USB bus code `linux/brcmfmac/usb.c:1585`. embassy, whd, c-driver and pico-sdk have no definition and no use `embassy/consts.rs:469-470` `whd/src/include/whd_wlioctl.h:1324-1325` `c-driver/cyw43_ll.c:167-187` |
| Payload | one u32, 4 bytes, little-endian, value 1, because linux uses `brcmf_fil_cmd_int_set` `linux/brcmfmac/core.c:1437` `linux/brcmfmac/fwil.h:87-93` |

- linux — `brcmf_dev_reset`: sent on interface 0 (`drvr->iflist[0]`) when that interface exists; the return value is discarded — set, u32 little-endian value 1, 4 bytes — `linux/brcmfmac/core.c:1428-1437`
- linux — only caller of `brcmf_dev_reset`: `brcmf_usb_reset_device`, run once per bound USB device by `brcmf_usb_exit` just before the USB driver is deregistered — same payload — `linux/brcmfmac/usb.c:1580-1585` `linux/brcmfmac/usb.c:1589-1600`
- linux — `brcmf_usb_exit` is called at module exit and on the error path of module init when PCIe registration fails; without `CONFIG_BRCMFMAC_USB` it is an empty inline, so the SDIO and PCIe paths never send this command — nothing sent on those paths — `linux/brcmfmac/core.c:1626-1627` `linux/brcmfmac/core.c:1633-1637` `linux/brcmfmac/bus.h:332-336`

Differences: only linux defines or sends number 28. A linux comment on the declaration of `brcmf_dev_reset` calls it an "Indication from bus module that dongle should be reset" `linux/brcmfmac/bus.h:311-312`; no comment describes the command itself, and that it resets or stops the device is (inferred) from that comment, the name and the single call site in the USB unload path.

### 320 WLC_SET_CUSTOM_COUNTRY / WLC_LAST
| | |
|---|---|
| Names | embassy not defined: the last enum entry is `GetRandomBytes` = 319 `embassy/consts.rs:729` / linux not defined: the highest `BRCMF_C_` constant is 268 `linux/brcmfmac/fwil.h:82` / whd `WLC_SET_CUSTOM_COUNTRY` `whd/src/include/whd_wlioctl.h:4270` `whd/src/include_helium/whd_wlioctl.h:4437` and `WLC_LAST` `whd/src/include/whd_wlioctl.h:1585` `whd/src/include_helium/whd_wlioctl.h:1585` / c-driver not defined: the highest `WLC_` define is 268 `c-driver/cyw43_ll.c:187` |
| Direction | set `whd/src/whd_chip.c:810` |
| Sent by | whd only, and only when the chip id is 43362 `whd/src/whd_chip.c:796-797`. embassy, linux, c-driver and pico-sdk have no definition and no use `embassy/consts.rs:729` `linux/brcmfmac/fwil.h:82` `c-driver/cyw43_ll.c:187` |
| Payload | whd copies one `whd_country_info_t` record, 68 bytes (computed: `abbrev[3]` + `rev` u8 + `data[64]`, pack(1)), byte fields only, into a command buffer requested with 78 bytes (record size + 10) `whd/src/whd_chip.c:801-809` `whd/src/include/whd_chip.h:368-377`. The 10 bytes after the record are not written by this function `whd/src/whd_chip.c:809-810`. The length field of the command is taken from the buffer size, so 78 bytes are sent (inferred) `whd/src/whd_cdc_bdc.c:202-205` `whd/src/whd_cdc_bdc.c:234` |

- whd — `whd_wifi_set_custom_country_code`: for chip id 43362, send the caller's country record; for every other chip id, including 43439, return `WHD_UNSUPPORTED` without sending anything — set, `whd_country_info_t` 68 bytes in a 78-byte buffer, no response buffer requested (NULL) — `whd/src/whd_chip.c:791-818`
- whd — `whd_wifi_set_custom_country_code` is declared in an internal header; a caller, or a declaration in the public API headers under `whd/inc`, is not found in these sources — nothing sent — `whd/src/include/whd_chip.h:395`
- whd — `WLC_LAST` is listed in the number-to-name debug table `whd_ioctl_to_string`, compiled only with `WPRINT_ENABLE_WHD_DEBUG`, so number 320 prints as "WLC_LAST", never as "WLC_SET_CUSTOM_COUNTRY" — nothing sent — `whd/src/whd_utils.c:518-520` `whd/src/whd_utils.c:802` `whd/src/whd_utils.c:807`

Differences: only whd defines number 320, and it gives it two names. `WLC_LAST` closes the numbered command list, directly after `WLC_GET_RANDOM_BYTES` = 319 `whd/src/include/whd_wlioctl.h:1584-1585`; `WLC_SET_CUSTOM_COUNTRY` is defined separately, about 2700 lines later, between the join-parameter records and the `WL_AUTH_*` values `whd/src/include/whd_wlioctl.h:4268-4273`. `WLC_LAST` is never sent `whd/src/whd_utils.c:802`. whd's CYW43439 path cannot reach the send, because the chip-id test admits only 43362 `whd/src/whd_chip.c:797` `whd/src/whd_chip.c:813-817`.

No other command number outside embassy's enum is defined in these sources: every other `BRCMF_C_*` constant `linux/brcmfmac/fwil.h:14-82`, every other `WLC_*` command number `whd/src/include/whd_wlioctl.h:1303-1584` `whd/src/include_helium/whd_wlioctl.h:1303-1584`, every `WHD_IOCTL_*` enumerator `whd/inc/whd_types.h:451-461` `whd/inc/whd_types.h:470-481` and every c-driver `WLC_*` define `c-driver/cyw43_ll.c:167-187` `c-driver/cyw43_ll.c:1979` has a number that embassy's enum also has `embassy/consts.rs:447-729`. The c-driver `CYW43_IOCTL_*` constants hold twice the command number, plus 1 for a set (for example `CYW43_IOCTL_GET_SSID` 0x32 = 2 × 25, `CYW43_IOCTL_SET_VAR` 0x20f = 2 × 263 + 1), and all 17 decode to numbers in embassy's enum `c-driver/cyw43_ll.h:31-47` `c-driver/cyw43_ll.c:1329`. The numbers 11, 13, 15-18, 42, 43, 65, 66, 73, 89, 103, 104, 153, 154, 173-177, 198, 199, 233, 234, 237 and 307-317 are defined by no driver in these sources `embassy/consts.rs:447-729` `whd/src/include/whd_wlioctl.h:1303-1585`.
