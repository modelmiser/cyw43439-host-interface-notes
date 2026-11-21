# Wire records: remaining

Records referenced by commands, variables or events and defined outside the main type headers.

### `brcmf_eventmsgs_ext` (linux)
Set payload of the named variable (iovar) "event_msgs_ext" (the header comment spells the name "eventmsgs_ext" `linux/brcmfmac/cyw/fwil_types.h:22`, the string linux sends is "event_msgs_ext" `linux/brcmfmac/cyw/core.c:95`), sent by brcmf_cyw_activate_events `linux/brcmfmac/cyw/core.c:79-99`, which linux installs as the cyw vendor `.activate_events` hook `linux/brcmfmac/cyw/core.c:381`; not packed (all u8, no padding possible, alignment 1); variable size, 4 fixed bytes (sizeof = 4, same on the x86-64 and 32-bit ARM builds compiled) + `len` mask bytes, and linux sends sizeof(struct) + event_mask_len = 4 + event_mask_len bytes `linux/brcmfmac/cyw/core.c:86`; no byte order (single bytes); `linux/brcmfmac/cyw/fwil_types.h:31-37`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 1 | ver | u8 | linux sets EVENTMSGS_VER = 1 `linux/brcmfmac/cyw/fwil_types.h:18` `linux/brcmfmac/cyw/core.c:90` |
| 1 | 1 | command | u8 | enum brcmf_event_msgs_ext_command: NONE 0, SET_BIT 1, RESET_BIT 2, SET_MASK 3; linux only sends SET_MASK `linux/brcmfmac/cyw/fwil_types.h:11-16` `linux/brcmfmac/cyw/core.c:91` |
| 2 | 1 | len | u8 | length of mask[] in bytes; linux sets fweh->event_mask_len `linux/brcmfmac/cyw/core.c:92`. For the cyw vendor, event_mask_len = DIV_ROUND_UP(num_event_codes, 8) with num_event_codes = BRCMF_CYW_E_LAST = 197, which gives 25 mask bytes and a 29-byte payload (inferred: arithmetic from the cited lines, not a constant in the source) `linux/brcmfmac/fweh.c:356` `linux/brcmfmac/cyw/core.c:21` `linux/brcmfmac/cyw/core.c:73` |
| 3 | 1 | maxgetsize | u8 | header comment: maximum mask size that may be returned on a get of the variable; linux leaves it 0 (kzalloc); a get of this variable is not found in linux `linux/brcmfmac/cyw/fwil_types.h:27-28` `linux/brcmfmac/cyw/core.c:87` |
| 4 | variable | mask | u8[] (flexible, __counted_by(len)) | event bit mask copied from fweh->event_mask; one bit per firmware event per the header comment `linux/brcmfmac/cyw/core.c:93` `linux/brcmfmac/cyw/fwil_types.h:29`. The macro EVENTMSGS_EXT_STRUCT_SIZE takes the offset of mask[0] in `struct eventmsgs_ext`, a type not defined in these sources; no file in linux uses the macro `linux/brcmfmac/cyw/fwil_types.h:19` |

Size check: compiled

### `brcmf_auth_req_status_le` (linux)
Event data of BRCMF_E_EXT_AUTH_REQ, which linux maps to cyw event code 187 `linux/brcmfmac/cyw/core.c:17` `linux/brcmfmac/cyw/core.c:54` and handles in a handler that rejects data shorter than sizeof (60) and reads ssid_len, ssid and peer_mac `linux/brcmfmac/cyw/core.c:239-272` (registered at `linux/brcmfmac/cyw/core.c:363-364`), and set payload of the named variable "auth_status", for which linux sends sizeof(auth_status) = 60 bytes `linux/brcmfmac/cyw/core.c:195-231`; not packed (natural alignment 4, no padding); 60 bytes (same on the x86-64 and 32-bit ARM builds compiled); little-endian; `linux/brcmfmac/cyw/fwil_types.h:53-59`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 2 | flags | __le16 | linux sends BRCMF_EXTAUTH_SUCCESS 4 or BRCMF_EXTAUTH_FAIL 3; values START 1, ABORT 2, FAIL 3, SUCCESS 4; not read by linux on the event side `linux/brcmfmac/cyw/core.c:212` `linux/brcmfmac/cyw/core.c:216` `linux/brcmfmac/cyw/fwil_types.h:39-42` |
| 2 | 6 | peer_mac | u8[ETH_ALEN] | copied from/to the cfg80211 bssid `linux/brcmfmac/cyw/core.c:219` `linux/brcmfmac/cyw/core.c:264`. Every later offset assumes ETH_ALEN = 6 (recalled, not in these sources); no file in these sources defines it, brcmu_wifi.h only says where it comes from `linux/include/brcmu_wifi.h:9` |
| 8 | 4 | ssid_len | __le32 | linux clamps to 32 in both directions `linux/brcmfmac/cyw/core.c:220-222` `linux/brcmfmac/cyw/core.c:262` |
| 12 | 32 | ssid | u8[IEEE80211_MAX_SSID_LEN] | IEEE80211_MAX_SSID_LEN = 32 `linux-headers/ieee80211.h:227` |
| 44 | 16 | pmkid | u8[WLAN_PMKID_LEN] | WLAN_PMKID_LEN = 16; linux fills it only on success and only if cfg80211 supplied one; not read on the event side `linux-headers/ieee80211.h:2271` `linux/brcmfmac/cyw/core.c:208-211` |

Size check: compiled
Differences: from whd's `whd_auth_req_status_t`: none in field order or size (60 bytes). `whd/inc/whd_types.h:1168-1175`

### `brcmf_mf_params_le` (linux)
Set payload of the bsscfg named variable "mgmt_frame", which linux uses only for authentication frames (other management frames go to the common brcmf_cfg80211_mgmt_tx `linux/brcmfmac/cyw/core.c:123-124`); not packed (natural alignment 4, 2 bytes of implicit padding before packet_id); variable size, 32 fixed bytes (sizeof = 32, same on the x86-64 and 32-bit ARM builds compiled) + body, and linux sends offsetof(data) + body length = 32 + (frame length - 24) bytes `linux/brcmfmac/cyw/core.c:133-134` `linux/brcmfmac/cyw/core.c:170-171`; little-endian; `linux/brcmfmac/cyw/fwil_types.h:74-84`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | version | __le32 | header comment: version of the variable; linux never assigns it, the buffer is kzalloc'ed, so linux sends 0 `linux/brcmfmac/cyw/fwil_types.h:64` `linux/brcmfmac/cyw/core.c:135-141` |
| 4 | 4 | dwell_time | __le32 | ms; linux sends MGMT_AUTH_FRAME_DWELL_TIME = 4000 `linux/brcmfmac/cyw/core.c:23` `linux/brcmfmac/cyw/core.c:139` |
| 8 | 2 | len | __le16 | length of data[]; linux sends frame length minus DOT11_MGMT_HDR_LEN 24 `linux/brcmfmac/cyw/core.c:140` `linux/brcmfmac/cfg80211.h:16` |
| 10 | 2 | frame_control | __le16 | copied from the frame's 802.11 frame_control (on-air little-endian value) `linux/brcmfmac/cyw/core.c:141` |
| 12 | 2 | channel | __le16 | chan->hw_value if a channel was given, else the first 2 bytes returned by BRCMF_C_GET_CHANNEL `linux/brcmfmac/cyw/core.c:143-153` |
| 14 | 6 | da | u8[ETH_ALEN] | destination address from the 802.11 header `linux/brcmfmac/cyw/core.c:155`. Every later offset assumes ETH_ALEN = 6 (recalled, not in these sources); no file in these sources defines it `linux/include/brcmu_wifi.h:9` |
| 20 | 6 | bssid | u8[ETH_ALEN] | BSSID from the 802.11 header `linux/brcmfmac/cyw/core.c:156` |
| 26 | 2 | (pad) | padding | implicit alignment padding, not declared in the source; linux sends zero (kzalloc) `linux/brcmfmac/cyw/fwil_types.h:81-82` `linux/brcmfmac/cyw/core.c:135-141` |
| 28 | 4 | packet_id | __le32 | linux sends the cfg80211 cookie truncated to 32 bits and keeps it as vif->mgmt_tx_id `linux/brcmfmac/cyw/core.c:157` `linux/brcmfmac/cyw/core.c:167`. This record is not what linux parses for the TX-status events: brcmf_notify_mgmt_tx_status reads only a host-order u32 packet id from the start of the event data `linux/brcmfmac/cyw/core.c:333-346`; those events are BRCMF_E_MGMT_FRAME_TXSTATUS and BRCMF_E_MGMT_FRAME_OFFCHAN_DONE, which linux maps to cyw codes 189 and 190 `linux/brcmfmac/cyw/core.c:19-20` `linux/brcmfmac/cyw/core.c:56-60` |
| 32 | variable | data | u8[] (flexible, __counted_by_le(len)) | frame body after the 24-byte management header `linux/brcmfmac/cyw/core.c:158-159` |

Size check: compiled
Differences: from whd's `whd_auth_params_t`: same field order; whd declares `data[1]` where linux has a flexible array, and names two fields fc and packetId. `whd/inc/whd_types.h:1195-1206`
Differences: the two drivers describe len and data differently: whd's comments say len includes the MAC header and data holds the MAC header plus contents; linux sends len = frame length - 24 and copies only the bytes after the 24-byte header. `whd/inc/whd_types.h:1199` `whd/inc/whd_types.h:1205` `linux/brcmfmac/cyw/core.c:140` `linux/brcmfmac/cyw/core.c:158-159`

### `wl_interface_create_v1` (linux)
Request buffer of a get of the named variable "interface_create", version 1, on the station path `linux/brcmfmac/cfg80211.c:613-705` and the AP path `linux/brcmfmac/cfg80211.c:707-786`, where linux tries v1, then v2, then v3 if a bsscfg int query of "interface_create" returns 3, and reads no field of the response; not packed (natural alignment 4, implicit padding after ver and after mac_addr); 20 bytes (same on the x86-64 and 32-bit ARM builds compiled); host order as linux writes it: ver, flags and wlc_index are plain u16/u32 assigned with no cpu_to_le conversion, not __le types, so a big-endian host would send different bytes `linux/brcmfmac/cfg80211.c:623-625`; `linux/brcmfmac/cfg80211.c:282-287`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 2 | ver | u16 | linux sends 1; WL_INTERFACE_CREATE_VER_1/2/3 = 1/2/3 `linux/brcmfmac/cfg80211.c:623` `linux/brcmfmac/cfg80211.c:720` `linux/brcmfmac/cfg80211.c:271-280` |
| 2 | 2 | (pad) | padding | implicit alignment padding, not declared in the source; zero because linux memsets the struct first `linux/brcmfmac/cfg80211.c:283-284` `linux/brcmfmac/cfg80211.c:622` `linux/brcmfmac/cfg80211.c:719` |
| 4 | 4 | flags | u32 | interface type and MAC flag combined: WL_INTERFACE_CREATE_STA \| WL_INTERFACE_MAC_USE = 2 (0x2) for station, WL_INTERFACE_CREATE_AP \| WL_INTERFACE_MAC_USE = 3 (0x3) for AP `linux/brcmfmac/cfg80211.c:624-625` `linux/brcmfmac/cfg80211.c:721-722`. Constants: WL_INTERFACE_MAC_DONT_USE 0 (0x0), WL_INTERFACE_MAC_USE 2 (0x2), WL_INTERFACE_CREATE_STA 0 (0x0), WL_INTERFACE_CREATE_AP 1 (0x1) `linux/brcmfmac/cfg80211.c:271-280` |
| 8 | 6 | mac_addr | u8[ETH_ALEN] | caller's address or one derived by brcmf_set_vif_sta_macaddr `linux/brcmfmac/cfg80211.c:626-629` `linux/brcmfmac/cfg80211.c:724`. Every later offset assumes ETH_ALEN = 6 (recalled, not in these sources); no file in these sources defines it `linux/include/brcmu_wifi.h:9` |
| 14 | 2 | (pad) | padding | implicit alignment padding, not declared in the source; zero (memset) `linux/brcmfmac/cfg80211.c:285-286` `linux/brcmfmac/cfg80211.c:622` `linux/brcmfmac/cfg80211.c:719` |
| 16 | 4 | wlc_index | u32 | source comment: optional for wlc index; linux leaves 0 (memset) `linux/brcmfmac/cfg80211.c:286` `linux/brcmfmac/cfg80211.c:622` |

Size check: compiled

### `wl_interface_create_v2` (linux)
Request buffer of a get of the named variable "interface_create", version 2; the try order, the unread response `linux/brcmfmac/cfg80211.c:613-705` `linux/brcmfmac/cfg80211.c:707-786`, the constants `linux/brcmfmac/cfg80211.c:271-280` and the host-order assignment `linux/brcmfmac/cfg80211.c:623-625` are as for `wl_interface_create_v1`; not packed (natural alignment 4, padding declared as pad1/pad2); 20 bytes (same on the x86-64 and 32-bit ARM builds compiled); host order as linux writes it (u16/u32, no conversion); `linux/brcmfmac/cfg80211.c:289-297`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 2 | ver | u16 | linux sends 2 `linux/brcmfmac/cfg80211.c:644` `linux/brcmfmac/cfg80211.c:739` |
| 2 | 2 | pad1 | u8[2] | (pad) declared in the source `linux/brcmfmac/cfg80211.c:291` |
| 4 | 4 | flags | u32 | WL_INTERFACE_MAC_USE = 2 (0x2) only; the interface type moved to iftype `linux/brcmfmac/cfg80211.c:645` `linux/brcmfmac/cfg80211.c:740` |
| 8 | 6 | mac_addr | u8[ETH_ALEN] | as v1 `linux/brcmfmac/cfg80211.c:647-650` `linux/brcmfmac/cfg80211.c:743`. Every later offset assumes ETH_ALEN = 6 (recalled, not in these sources); no file in these sources defines it `linux/include/brcmu_wifi.h:9` |
| 14 | 1 | iftype | u8 | WL_INTERFACE_CREATE_STA 0 or WL_INTERFACE_CREATE_AP 1 `linux/brcmfmac/cfg80211.c:646` `linux/brcmfmac/cfg80211.c:741` |
| 15 | 1 | pad2 | u8 | (pad) declared in the source `linux/brcmfmac/cfg80211.c:295` |
| 16 | 4 | wlc_index | u32 | linux leaves 0 `linux/brcmfmac/cfg80211.c:296` |

Size check: compiled
Differences: from `wl_interface_create_v1`: same 20-byte size and same offsets for ver, flags, mac_addr and wlc_index; linux changes the ver value and carries the interface type in iftype instead of flags. `linux/brcmfmac/cfg80211.c:289-297`

### `wl_interface_create_v3` (linux)
Request buffer of a get of the named variable "interface_create", version 3; the try order, the unread response `linux/brcmfmac/cfg80211.c:613-705` `linux/brcmfmac/cfg80211.c:707-786`, the constants `linux/brcmfmac/cfg80211.c:271-280` and the host-order assignment `linux/brcmfmac/cfg80211.c:623-625` are as for `wl_interface_create_v1`; not packed (natural alignment 4, no implicit padding, pad[3] declared); variable size, 28 fixed bytes (sizeof = 28, same on the x86-64 and 32-bit ARM builds compiled) + optional data, and linux sends exactly 28; host order as linux writes it (u16/u32, no conversion); `linux/brcmfmac/cfg80211.c:299-311`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 2 | ver | u16 | linux sends 3 `linux/brcmfmac/cfg80211.c:676` `linux/brcmfmac/cfg80211.c:769` |
| 2 | 2 | len | u16 | source comment: length of structure + data; linux leaves 0 (memset) although the comment describes a length `linux/brcmfmac/cfg80211.c:301` `linux/brcmfmac/cfg80211.c:675` `linux/brcmfmac/cfg80211.c:768` |
| 4 | 2 | fixed_len | u16 | source comment: length of structure; linux leaves 0 although the comment describes a length `linux/brcmfmac/cfg80211.c:302` `linux/brcmfmac/cfg80211.c:301-302` `linux/brcmfmac/cfg80211.c:675` |
| 6 | 1 | iftype | u8 | WL_INTERFACE_CREATE_STA 0 or WL_INTERFACE_CREATE_AP 1 `linux/brcmfmac/cfg80211.c:678` `linux/brcmfmac/cfg80211.c:771` |
| 7 | 1 | wlc_index | u8 | linux leaves 0 `linux/brcmfmac/cfg80211.c:304` |
| 8 | 4 | flags | u32 | WL_INTERFACE_MAC_USE = 2 (0x2) `linux/brcmfmac/cfg80211.c:677` `linux/brcmfmac/cfg80211.c:770` |
| 12 | 6 | mac_addr | u8[ETH_ALEN] | as v1 `linux/brcmfmac/cfg80211.c:679-682` `linux/brcmfmac/cfg80211.c:772`. Every later offset assumes ETH_ALEN = 6 (recalled, not in these sources); no file in these sources defines it `linux/include/brcmu_wifi.h:9` |
| 18 | 6 | bssid | u8[ETH_ALEN] | source comment: optional for BSSID; linux leaves 0 `linux/brcmfmac/cfg80211.c:307` |
| 24 | 1 | if_index | u8 | source comment: interface index request; linux leaves 0 `linux/brcmfmac/cfg80211.c:308` |
| 25 | 3 | pad | u8[3] | (pad) declared in the source `linux/brcmfmac/cfg80211.c:309` |
| 28 | variable | data | u8[] (flexible) | source comment: optional for specific data; linux sends none (request length is sizeof = 28) `linux/brcmfmac/cfg80211.c:310` `linux/brcmfmac/cfg80211.c:684-686` |

Size check: compiled

### `cca_msrmnt_query` (linux)
Request header of a get of the named variable "dump_obss": linux copies it to the start of a BRCMF_DCMD_MEDLEN (1536) byte buffer and sends that buffer as the get buffer `linux/brcmfmac/core.h:31` `linux/brcmfmac/cfg80211.c:8307-8321`, and brcmf_cfg80211_dump_survey issues the get twice per channel `linux/brcmfmac/cfg80211.c:8421-8435`; not packed (two u32, no padding, alignment 4); 8 bytes (same on the x86-64 and 32-bit ARM builds compiled); host order as linux writes it (no cpu_to_le32) `linux/brcmfmac/cfg80211.c:8319` `linux/brcmfmac/cfg80211.c:8422-8423`; `linux/brcmfmac/cfg80211.c:123-126`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | msrmnt_query | u32 | as linux uses it: 0 = start a measurement, 1 = collect results `linux/brcmfmac/cfg80211.c:8421-8422` `linux/brcmfmac/cfg80211.c:8431-8432` |
| 4 | 4 | time_req | u32 | requested measurement time; linux sends ACS_MSRMNT_DELAY = 80 and treats it as ms; the second call changes only msrmnt_query, so time_req is still 80 `linux/brcmfmac/cfg80211.c:93` `linux/brcmfmac/cfg80211.c:8423` `linux/brcmfmac/cfg80211.c:8429` `linux/brcmfmac/cfg80211.c:8432` |

Size check: compiled

### `cca_stats_n_flags` (linux)
Response of a get of the named variable "dump_obss": linux casts the response buffer to this record, uses only buf, and parses buf on the second call unconditionally, ignoring msrmnt_done `linux/brcmfmac/cfg80211.c:8327-8330`; not packed (natural alignment 4); variable size, 8 fixed bytes + text (sizeof = 12, counting buf[1] and 3 trailing padding bytes; same on the x86-64 and 32-bit ARM builds compiled); byte order of the two u32 not shown by linux (never read); `linux/brcmfmac/cfg80211.c:117-121`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | msrmnt_time | u32 | source comment: time for measurement (msec); not read by linux `linux/brcmfmac/cfg80211.c:118` |
| 4 | 4 | msrmnt_done | u32 | source comment: flag set when measurement complete; not read by linux `linux/brcmfmac/cfg80211.c:119` |
| 8 | variable | buf | char[1] (variable tail) | text that linux passes to brcmf_parse_dump_obss when msrmnt_query was 1; declared size 1 `linux/brcmfmac/cfg80211.c:120` `linux/brcmfmac/cfg80211.c:8329-8330`. The parsed text fills the host-only struct brcmf_dump_survey `linux/brcmfmac/cfg80211.c:108-115` |
| 9 | 3 | (pad) | padding | trailing alignment padding counted by sizeof, not declared in the source; overlaps the variable tail `linux/brcmfmac/cfg80211.c:117-121` |

Size check: compiled

### `brcmf_cfg80211_assoc_ielen_le` (linux)
Start of the response of a get of the named variable "assoc_info": the get buffer is WL_ASSOC_INFO_MAX = 512 bytes `linux/brcmfmac/cfg80211.h:23`, linux reads only these first 8 bytes of the response and no linux type describes what follows them `linux/brcmfmac/cfg80211.c:6481-6490`, then fetches the IEs with "assoc_req_ies" / "assoc_resp_ies" when the matching length is non-zero `linux/brcmfmac/cfg80211.c:6496-6517`; not packed (two __le32, no padding, alignment 4); 8 bytes (same on the x86-64 and 32-bit ARM builds compiled); little-endian, both fields read with le32_to_cpu `linux/brcmfmac/cfg80211.c:6489-6490`; `linux/brcmfmac/cfg80211.h:274-277`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | req_len | __le32 | length of the association request IEs; linux rejects values above WL_EXTRA_BUF_MAX 2048 `linux/brcmfmac/cfg80211.c:6491` `linux/brcmfmac/cfg80211.h:24` |
| 4 | 4 | resp_len | __le32 | length of the association response IEs; same bound `linux/brcmfmac/cfg80211.c:6491` `linux/brcmfmac/cfg80211.h:24` |

Size check: compiled

### `brcmf_cfg80211_edcf_acparam` (linux)
Element of the response of a get of the named variable "wme_ac_sta", which linux issues only when the "assoc_info" resp_len is non-zero `linux/brcmfmac/cfg80211.c:6514-6531`; the response is an array of EDCF_AC_COUNT = 4 records, 16 bytes `linux/brcmfmac/cfg80211.h:33` `linux/brcmfmac/cfg80211.c:6474` `linux/brcmfmac/cfg80211.c:6529-6531`, which linux walks by index aci = 0..3 in brcmf_wifi_prioritize_acparams, where the comment on the neighbouring aci_prio array names the order AC_BE, AC_BK, AC_VI, AC_VO `linux/brcmfmac/cfg80211.c:6386-6400` `linux/brcmfmac/cfg80211.c:6395`; not packed (natural alignment 2, no padding); 4 bytes (same on the x86-64 and 32-bit ARM builds compiled); TXOP byte order not shown by linux (never read); `linux/brcmfmac/cfg80211.h:279-283`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 1 | ACI | u8 | linux reads AIFSN = ACI & 0x0f and ACM = ACI & 0x10 `linux/brcmfmac/cfg80211.c:6399-6400` `linux/brcmfmac/cfg80211.h:36-41` |
| 1 | 1 | ECW | u8 | ECWmin = low nibble, ECWmax = high nibble: EDCF_ECWMIN_MASK 0x0f, EDCF_ECWMAX_MASK 0xf0, shift 4 `linux/brcmfmac/cfg80211.h:39-43` |
| 2 | 2 | TXOP | u16 | source comment: stored in network order (ls octet first); not read by linux `linux/brcmfmac/cfg80211.h:282` |

Size check: compiled
Differences: from whd's `edcf_acparam`: same three fields and 4-byte size; whd defines its record inside `#pragma pack(1)`, linux's is not packed but has no padding. `whd/src/include/whd_wlioctl.h:3909-3914`

### `brcmf_tlv` (linux)
Generic 802.11 information-element header linux uses when walking IE buffers (the on-air IE format, carried inside the payloads linux exchanges, not a record specific to this interface): brcmf_parse_tlvs steps by len + TLV_HDR_LEN (2) `linux/brcmfmac/cfg80211.c:419-433` `linux/brcmfmac/cfg80211.h:60`, and brcmf_parse_vndr_ies walks a vendor-IE buffer as a sequence of `brcmf_tlv` with the same step `linux/brcmfmac/cfg80211.c:4849-4896`; not packed (all u8, alignment 1); variable size, 2 fixed bytes (sizeof = 2, same on the x86-64 and 32-bit ARM builds compiled) + `len`; no byte order (single bytes); `linux/brcmfmac/cfg80211.h:413-417`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 1 | id | u8 | element ID `linux/brcmfmac/cfg80211.h:414` |
| 1 | 1 | len | u8 | number of bytes in data[] `linux/brcmfmac/cfg80211.h:415` |
| 2 | variable | data | u8[] (flexible) | value `linux/brcmfmac/cfg80211.h:416` |

Size check: compiled

### `brcmf_vs_tlv` (linux)
Header of a vendor-specific information element as linux reads it (IE format carried inside the payloads linux exchanges): brcmf_find_wpaie and brcmf_find_wpsie cast a `brcmf_tlv` to it `linux/brcmfmac/cfg80211.c:466-487`, vendor IE parsing also uses it `linux/brcmfmac/cfg80211.c:4848-4895`, and it is embedded in the host-only struct parsed_vndr_ie_info `linux/brcmfmac/cfg80211.c:260-264`; not packed (all u8, alignment 1); 6 bytes (same on the x86-64 and 32-bit ARM builds compiled); no byte order (single bytes); `linux/brcmfmac/cfg80211.c:253-258`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 1 | id | u8 | source comment: vendor-specific IE, id = 221 `linux/brcmfmac/cfg80211.c:252` `linux/brcmfmac/cfg80211.c:254` |
| 1 | 1 | len | u8 | `linux/brcmfmac/cfg80211.c:255` |
| 2 | 3 | oui | u8[3] | `linux/brcmfmac/cfg80211.c:256` |
| 5 | 1 | oui_type | u8 | `linux/brcmfmac/cfg80211.c:257` |

Size check: compiled
Differences: from whd's `wl_vndr_ie`: same first five bytes (id, len, oui[3]); whd's sixth byte is `data[1]`, linux names it oui_type. `whd/src/include/whd_wlioctl.h:1945-1951`

### `whd_af_params_t` (whd)
Set payload of the named variable "actframe"; a public alias of `struct wl_af_params` `whd/inc/whd_types.h:142`, not a separate layout, so the same record is also described under its other name, `wl_af_params_t`; whd_wifi_send_action_frame first checks action_frame.len <= 1040 `whd/src/whd_wifi_api.c:4334`, then copies WL_WIFI_AF_PARAMS_SIZE = sizeof(struct wl_af_params) bytes into the set buffer of "actframe" `whd/src/whd_wifi_api.c:4323-4344` `whd/src/whd_wifi_api.c:4343` `whd/src/include/whd_wlioctl.h:115` `whd/src/include/whd_wlioctl.h:1089`; not packed (alignment 4); 1068 bytes (same on the x86-64 and 32-bit ARM builds compiled), always sent in full whatever action_frame.len is; not converted by whd (the caller's struct is copied whole into the buffer); `whd/src/include/whd_wlioctl.h:68-74`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | channel | uint32_t | `whd/src/include/whd_wlioctl.h:70` |
| 4 | 4 | dwell_time | int32_t | `whd/src/include/whd_wlioctl.h:71` |
| 8 | 6 | BSSID | struct ether_addr | `whd/src/include/whd_wlioctl.h:72` |
| 14 | 2 | (pad) | padding | implicit alignment padding inserted by the compiler `whd/src/include/whd_wlioctl.h:72-73` |
| 16 | 1052 | action_frame | wl_action_frame_t | da[6] at 16, len uint16 at 22, packetId uint32 at 24, data[ACTION_FRAME_SIZE = 1040] at 28 `whd/src/include/whd_wlioctl.h:38` `whd/src/include/whd_wlioctl.h:60-66` |

Size check: compiled

### `wl_el_tag_params_s_t` (whd)
Set payload of the named variable "event_log_tag_control" (IOVAR_STR_EVENT_LOG `whd/src/include/whd_wlioctl.h:1272`), one record per set, sent by whd_wifi_enable_event_log `whd/src/whd_wifi_api.c:6562-6600` `whd/src/whd_wifi_api.c:6592-6595`; the type is an anonymous struct typedef local to whd_wifi_api.c; not packed (natural alignment 2, no padding); 4 bytes (same on the x86-64 and 32-bit ARM builds compiled); not converted by whd (elements passed as they sit in host memory); `whd/src/whd_wifi_api.c:355-359`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 2 | tag | uint16_t | event-log tag number; whd's table uses 28-35, 73, 77, 78, 113, 127, 128, 131, 136, 137, 143, 287, 288, 312, 313 `whd/src/whd_wifi_api.c:6565-6584`. As written, the sending loop compares the index with the category's count, not with start + count; with table entries {start, count} = {0,6}, {6,4}, {10,2}, {12,2}, {14,3}, {17,1}, {18,2}, {20,2}, only category 0 (tags 28, 29, 30, 31, 113, 128) produces any set (inferred: a reading of the cited lines, not something run) `whd/src/whd_wifi_api.c:6586-6590` |
| 2 | 1 | set | uint8_t | always 1 in whd's table `whd/src/whd_wifi_api.c:6565-6584` |
| 3 | 1 | flags | uint8_t | always EVTLOG_LOG_AND_PRINT_MODE = 192 (0xC0) in whd's table `whd/src/whd_wifi_api.c:112` `whd/src/whd_wifi_api.c:6565-6584` |

Size check: compiled

### `client_rssi_t` (whd)
Request and reply buffer of command WLC_GET_RSSI (127) `whd/src/include/whd_wlioctl.h:1415` when whd asks a softAP for one client's RSSI `whd/src/whd_wifi_api.c:1309-1333`; the type is local to whd_wifi_api.c; pragma pack(1) (`whd/src/whd_wifi_api.c:127-149`), so no padding; 10 bytes (same on the x86-64 and 32-bit ARM builds compiled), while the buffer length is ROUND_UP(sizeof, 4) = 12 (`whd/src/include/whd_types_int.h:134`), a source comment saying the buffer size must be 4-byte aligned `whd/src/whd_wifi_api.c:1317-1320`; not converted by whd; `whd/src/whd_wifi_api.c:135-139`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | rssi | int32_t | whd sends 0; in the reply whd reads the first 4 bytes of the buffer as the RSSI, copying them into an int32_t with no dtoh32 `whd/src/whd_wifi_api.c:1324` `whd/src/whd_wifi_api.c:1327-1329` `whd/src/whd_wifi_api.c:1329` |
| 4 | 6 | macs | whd_mac_t | the associated client's MAC address `whd/src/whd_wifi_api.c:1323` |
| 10 | 2 | (buffer tail) | - | not part of the struct (sizeof is 10 under pack(1)): the 2 bytes by which ROUND_UP lengthens the command buffer to 12; sent, not initialised by this function `whd/src/whd_wifi_api.c:135-139` `whd/src/whd_wifi_api.c:1317-1324`. whd's CDC buffer getter, whd_cdc_get_ioctl_buffer, obtains a packet with whd_host_buffer_get and returns its data pointer plus IOCTL_OFFSET without clearing the buffer `whd/src/whd_cdc_bdc.c:382-401` `whd/src/whd_cdc_bdc.c:594`; whether the host's packet-buffer implementation hands out zeroed memory is not found in these sources, so the two tail bytes whd sends are unspecified |

Size check: compiled

### `wl_he_omi_t` (whd)
Value of the xtlv with id WL_HE_CMD_OMI = 13 `whd/src/include/whd_wlioctl.h:129` inside a set of the named variable "he" `whd/src/include/whd_wlioctl.h:1268`, sent with xtlv len 9 `whd/src/whd_wifi_api.c:4376-4404`; an alias of `wl_he_omi_v1_t` `whd/src/include/whd_wlioctl.h:152` (the identical alias line is in the helium header `whd/src/include_helium/whd_wlioctl.h:151`); whd copies the fields one by one from the host API record `whd_he_omi_params_t` `whd/src/whd_wifi_api.c:4390-4396`; not packed (all uint8_t, outside any pragma pack region, alignment 1); 9 bytes (same on the x86-64 and 32-bit ARM builds compiled); no byte order (single bytes); `whd/src/include/whd_wlioctl.h:138-149`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 1 | version | uint8_t | WL_HE_OMI_VER = WL_HE_OMI_V1 = 1 `whd/src/include/whd_wlioctl.h:137` `whd/src/include/whd_wlioctl.h:151` `whd/src/whd_wifi_api.c:4388` |
| 1 | 1 | length | uint8_t | whd sets sizeof - 2 = 7 `whd/src/whd_wifi_api.c:4389` |
| 2 | 1 | rx_nss | uint8_t | `whd/src/include/whd_wlioctl.h:142` |
| 3 | 1 | chnl_wdth | uint8_t | `whd/src/include/whd_wlioctl.h:143` |
| 4 | 1 | ul_mu_dis | uint8_t | `whd/src/include/whd_wlioctl.h:144` |
| 5 | 1 | tx_nsts | uint8_t | `whd/src/include/whd_wlioctl.h:145` |
| 6 | 1 | er_su_dis | uint8_t | `whd/src/include/whd_wlioctl.h:146` |
| 7 | 1 | dl_mu_resound | uint8_t | `whd/src/include/whd_wlioctl.h:147` |
| 8 | 1 | ul_mu_data_dis | uint8_t | `whd/src/include/whd_wlioctl.h:148` |

Size check: compiled

### `wl_chanspec_t` (whd)
Scalar typedef for the channel word (chanspec) in `wl_bss_info_t` `whd/inc/whd_types.h:941`, in other whd records `whd/src/include/whd_wlioctl.h:702` `whd/src/include/whd_wlioctl.h:721` `whd/src/include/whd_wlioctl.h:1775` `whd/src/include/whd_wlioctl.h:1817-1818` `whd/src/include/whd_wlioctl.h:3468` and as the argument of whd_wifi_set_chanspec `whd/src/whd_wifi_api.c:556`, which sends the value widened to 32 bits with htod32 `whd/src/whd_wifi_api.c:589`; a second, identical typedef `chanspec_t` is used for chanspec_list[] in wl_assoc_params `whd/src/include/whd_wlioctl.h:48` `whd/src/include/whd_wlioctl.h:4244`; not a struct (packing not applicable); 2 bytes (on every build compiled); little-endian as whd treats it: written with htod16 into join parameters and read with dtoh16 from a scan result `whd/src/whd_wifi_api.c:2365` `whd/src/whd_wifi_api.c:2384` `whd/src/whd_wifi_api.c:2680` `whd/src/include/whd_endian.h:44-57`; `whd/inc/whd_types.h:918`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 2 | (value) | uint16_t | bits 0-7 channel number, WL_CHANSPEC_CHAN_MASK 0x00ff `whd/src/include/whd_chip_constants.h:75` `whd/src/include/whd_chip_constants.h:85`. The band, bandwidth and sideband bit positions are not fixed constants in whd: they are looked up per chip id through GET_C_VAR / get_whd_var `whd/src/whd_chip_constants.c:163-228` |

Size check: compiled
Differences: between chip ids in whd (these are the values whd's lookup functions return per chip id, not a statement about any firmware): for every chip id other than 43362, 4334, 43340 and 43342 (so including 43439) whd's getters return band mask 0xc000, 2G 0x0000, 5G 0xc000, band shift 14 `whd/src/whd_chip_constants.c:430-498`; bandwidth mask 0x3800, shift 11, 10 MHz 0x0800, 20 MHz 0x1000, 40 MHz 0x1800, 80 MHz 0x2000, 160 MHz 0x2800 `whd/src/whd_chip_constants.c:500-596`; sideband values WL_CHANSPEC_CTL_SB_LLL 0x0000 through UUU 0x0700, sideband mask 0x0700 `whd/src/whd_chip_constants.c:598-722` `whd/src/include/whd_wlioctl.h:4215-4222` `whd/src/whd_chip_constants.c:724-736`. The 43362/4334/43340/43342 branch returns the older layout: band mask 0xf000, 2G 0x2000, 5G 0x1000, bandwidth mask 0x0c00, 20 MHz 0x0800, sideband mask 0x0300 `whd/src/whd_chip_constants.c:430-736`
Differences: from linux's chanspec definitions: linux defines two encodings, BRCMU_CHSPEC_D11N_* (band at bits 12-13) and BRCMU_CHSPEC_D11AC_* (band at bits 14-15); the D11AC values equal what whd returns for chip ids outside its older branch, so including 43439 (band mask 0xc000, 2G 0x0000, 5G 0xc000, bandwidth mask 0x3800, 20 MHz 0x1000) `linux/include/brcmu_d11.h:23-86` `whd/src/whd_chip_constants.c:430-596`. The D11N values equal whd's older branch for 2G 0x2000, 5G 0x1000, bandwidth mask 0x0c00 and 20 MHz 0x0800; the band mask differs: linux 0x3000, whd 0xf000 `linux/include/brcmu_d11.h:41-49` `whd/src/whd_chip_constants.c:430-442`. Which encoding linux selects at run time (d11inf io_type) is not traced in this entry.

### `wl_vndr_ie` (whd)
Innermost record of the "vndr_ie" set buffer, sent as "bsscfg:vndr_ie" `whd/src/whd_wifi_api.c:4288-4320`: its place in the buffer is vndr_ie_setbuf_t.vndr_ie_buffer.vndr_ie_list[0].vndr_ie_data, with a 4-byte bsscfg index in front `whd/src/include/whd_wlioctl.h:1953-1967` `whd/src/include/whd_wlioctl.h:1087`; the same struct has the typedef name `wl_vndr_ie_t` `whd/src/include/whd_wlioctl.h:1952`; not packed (all uint8_t, alignment 1, outside the pragma pack(1) regions, which are lines 3864-3918 and 4188-4289 `whd/src/include/whd_wlioctl.h:3864-3918` `whd/src/include/whd_wlioctl.h:4188-4289`); variable size, 5 fixed bytes + data (sizeof = 6, same on the x86-64 and 32-bit ARM builds compiled); no byte order (single bytes); `whd/src/include/whd_wlioctl.h:1945-1951`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 1 | id | uint8_t | whd writes 221 (0xdd) `whd/src/whd_wifi_api.c:4308` |
| 1 | 1 | len | uint8_t | whd writes data length + 3 (OUI) + 1 (subtype) `whd/src/whd_wifi_api.c:4309-4310` |
| 2 | 3 | oui | uint8_t[3] | `whd/src/whd_wifi_api.c:4314` |
| 5 | variable | data | uint8_t[1] (variable tail) | declared size 1; data[0] = subtype, caller's bytes from data[1] `whd/src/whd_wifi_api.c:4316-4318` |

Size check: compiled
Differences: from linux's `brcmf_vs_tlv`: see that record. `linux/brcmfmac/cfg80211.c:253-258`

### `edcf_acparam` (whd)
Element of the response of a get of the named variable "wme_ac_sta": whd_wifi_get_acparams sends 64 zero bytes and copies 4 records = 16 bytes from the reply `whd/src/whd_wifi_api.c:4180-4205` `whd/src/whd_wifi_api.c:4204` `whd/src/include/whd_wlioctl.h:1090`; the same struct has the typedef name `edcf_acparam_t` and the public alias `whd_edcf_ac_param_t` `whd/src/include/whd_wlioctl.h:3915` `whd/inc/whd_types.h:141`; packed (pragma pack(1) region `whd/src/include/whd_wlioctl.h:3864-3918`, alignment 1); 4 bytes (same on the x86-64 and 32-bit ARM builds compiled); TXOP copied by whd without any swap; `whd/src/include/whd_wlioctl.h:3909-3914`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 1 | ACI | uint8_t | `whd/src/include/whd_wlioctl.h:3911` |
| 1 | 1 | ECW | uint8_t | EDCF_ECWMIN_MASK 0x0f, EDCF_ECWMAX_MASK 0xf0, shift 4 `whd/src/include/whd_wlioctl.h:3899-3901` |
| 2 | 2 | TXOP | uint16_t | source comment: stored in network order (ls octet first); EDCF_TXOP2USEC(txop) = txop << 5 `whd/src/include/whd_wlioctl.h:3913` `whd/src/include/whd_wlioctl.h:3906` |

Size check: compiled
Differences: from linux's `brcmf_cfg80211_edcf_acparam`: see that record. `linux/brcmfmac/cfg80211.h:279`

### `wl_dload_data` (whd)
Header of each chunk of a set of the named variable "clmload" (IOVAR_STR_CLMLOAD `whd/src/include/whd_wlioctl.h:1231`) `whd/src/whd_clm.c:43-70`; the same struct has the typedef name `wl_dload_data_t` `whd/src/include/whd_wlioctl.h:4175`; not packed (alignment 4; defined between the two pragma pack(1) regions, which end at line 3918 and restart at line 4188 `whd/src/include/whd_wlioctl.h:3918` `whd/src/include/whd_wlioctl.h:4188`); variable size, 12 fixed bytes + payload (sizeof = 16, counting data[1] and 3 trailing padding bytes; same on the x86-64 and 32-bit ARM builds compiled), and without PROTO_MSGBUF whd rounds the sent length with len + 8 - (len % 8), which adds 8 when len is already a multiple of 8 `whd/src/whd_clm.c:61-63`; little-endian: whd converts flag, dload_type and len with htod16/htod32 `whd/src/whd_clm.c:54-56` `whd/src/include/whd_endian.h:44-57`; `whd/src/include/whd_wlioctl.h:4167-4174`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 2 | flag | uint16_t | (DLOAD_HANDLER_VER 1 << DLOAD_FLAG_VER_SHIFT 12) \| flag, with DL_BEGIN 0x0002 / DL_END 0x0004 `whd/src/whd_clm.c:54` `whd/src/include/whd_wlioctl.h:4154-4160` |
| 2 | 2 | dload_type | uint16_t | DL_TYPE_UCODE 1, DL_TYPE_CLM 2 `whd/src/include/whd_wlioctl.h:4162-4165` |
| 4 | 4 | len | uint32_t | total length minus the 12-byte header `whd/src/whd_clm.c:53` `whd/src/whd_clm.c:56` |
| 8 | 4 | crc | uint32_t | whd writes 0 `whd/src/whd_clm.c:58` |
| 12 | variable | data | uint8_t[1] (variable tail) | declared size 1; payload starts at offsetof(data) = 12 `whd/src/whd_clm.c:53` `whd/src/whd_clm.c:109` |
| 13 | 3 | (pad) | padding | trailing alignment padding counted by sizeof, not declared in the source; overlaps the variable tail `whd/src/include/whd_wlioctl.h:4167-4174` |

Size check: compiled

### `wl_clm_dload_info` (whd)
Declared, never used by whd: only the definition and the typedef `wl_clm_dload_info_t` exist `whd/src/include/whd_wlioctl.h:4177-4186` `whd/src/include/whd_wlioctl.h:4186`, so its command or variable, and whether it is a wire record at all, are not found in these sources; whd's CLM download uses `wl_dload_data` instead `whd/src/whd_clm.c:47`; the source gives no field meanings (no comments, only the names); not packed (alignment 4, outside the pragma pack(1) regions); variable size, 20 fixed bytes + chunk (sizeof = 24, counting data_chunk[1] and 3 trailing padding bytes; same on the x86-64 and 32-bit ARM builds compiled); byte order not shown by whd; `whd/src/include/whd_wlioctl.h:4177-4185`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | ds_id | uint32_t | `whd/src/include/whd_wlioctl.h:4179` |
| 4 | 4 | clm_total_len | uint32_t | `whd/src/include/whd_wlioctl.h:4180` |
| 8 | 4 | num_chunks | uint32_t | `whd/src/include/whd_wlioctl.h:4181` |
| 12 | 4 | chunk_len | uint32_t | `whd/src/include/whd_wlioctl.h:4182` |
| 16 | 4 | chunk_offset | uint32_t | `whd/src/include/whd_wlioctl.h:4183` |
| 20 | variable | data_chunk | uint8_t[1] (variable tail) | declared size 1 `whd/src/include/whd_wlioctl.h:4184` |
| 21 | 3 | (pad) | padding | trailing alignment padding counted by sizeof, not declared in the source; overlaps the variable tail `whd/src/include/whd_wlioctl.h:4177-4185` |

Size check: compiled

### `whd_arp_stats_s` (whd)
Host-side output record of whd_arp_stats_get, public typedef `whd_arp_stats_t` `whd/inc/whd_types.h:143`; not a wire record as a whole, only the member `stats` is one named variable's payload ("arp_stats"): the record is never sent or received as one block, whd fills it from five separate gets plus the host-IP list `whd/src/whd_wifi_api.c:5822-5908`, and repeats the whole read until memcmp finds two consecutive passes equal `whd/src/whd_wifi_api.c:5835-5905`; packed (pragma pack(1) region `whd/src/include/whd_wlioctl.h:4188-4289`, alignment 1; all members are 4-byte multiples, so packing changes only the alignment); 96 bytes (same on the x86-64 and 32-bit ARM builds compiled); byte-order handling differs per member, as the Notes column says; `whd/src/include/whd_wlioctl.h:4279-4287`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | version | uint32_t | from a get of "arp_version" `whd/src/whd_wifi_api.c:5859` `whd/src/include/whd_wlioctl.h:1255`; fetched with whd_wifi_get_iovar_value, which applies dtoh32 to the 4-byte reply `whd/src/whd_wifi_api.c:5165-5182` `whd/src/whd_wifi_api.c:5179` |
| 4 | 4 | peerage | uint32_t | from a get of "arp_peerage", fetched and converted like version `whd/src/whd_wifi_api.c:5865` `whd/src/include/whd_wlioctl.h:1256` |
| 8 | 4 | arpoe | uint32_t | from a get of "arpoe", fetched and converted like version `whd/src/whd_wifi_api.c:5871` `whd/src/include/whd_wlioctl.h:1257` |
| 12 | 4 | features_enabled | uint32_t | from a get of "arp_ol", 4 bytes, fetched with whd_wifi_get_iovar_buffer straight into the member with no conversion; flag bits ARP_OL_AGENT 0x1, ARP_OL_SNOOP 0x2, ARP_OL_HOST_AUTO_REPLY 0x4, ARP_OL_PEER_AUTO_REPLY 0x8 `whd/src/whd_wifi_api.c:5851-5853` `whd/src/include/whd_wlioctl.h:1258` `whd/src/include/whd_wlioctl.h:3602-3605` |
| 16 | 48 | stats | arp_ol_stats_t | the wire part: 48-byte response of a get of "arp_stats" read straight into this member. Twelve uint32_t in order: host_ip_entries, host_ip_overflow, arp_table_entries, arp_table_overflow, host_request, host_reply, host_service, peer_request, peer_request_drop, peer_reply, peer_reply_drop, peer_service, at record offsets 16, 20, ... 60 `whd/src/whd_wifi_api.c:5842-5844` `whd/src/include/whd_wlioctl.h:1262` `whd/src/include/whd_wlioctl.h:3609-3623`. whd converts the block with dtoh32 `whd/src/whd_wifi_api.c:5879-5890`. `arp_ol_stats_t` itself is defined outside the pack regions (sizeof 48, alignment 4, compiled) `whd/src/include/whd_wlioctl.h:3609-3623` |
| 64 | 32 | host_ip_list | uint32_t[ARP_MULTIHOMING_MAX] | ARP_MULTIHOMING_MAX = 8; filled by whd_arp_hostip_list_get `whd/src/include/whd_wlioctl.h:3608` `whd/src/whd_wifi_api.c:5892` |

Size check: compiled

### `wl_ioctl_t` (whd)
Host-only record, unused by whd: the name occurs only at its definition in whd/src and whd/inc, so no command, variable or event is tied to it in whd; it contains a host pointer, so it cannot be a wire layout as declared `whd/src/include/whd_wlioctl.h:1000`, and it reads as a host-OS ioctl argument record (inferred from the member names, not stated in the source); not packed (alignment 4 on 32-bit ARM, outside the pragma pack(1) regions); 24 bytes on the 32-bit ARM builds (compiled; host-dependent); not serialised by whd; `whd/src/include/whd_wlioctl.h:997-1005`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | cmd | uint32_t | `whd/src/include/whd_wlioctl.h:999` |
| 4 | 4 | buf | void * | host pointer `whd/src/include/whd_wlioctl.h:1000` |
| 8 | 4 | len | uint32_t | `whd/src/include/whd_wlioctl.h:1001` |
| 12 | 1 | set | uint8_t | `whd/src/include/whd_wlioctl.h:1002` |
| 13 | 3 | (pad) | padding | implicit alignment padding, not declared in the source `whd/src/include/whd_wlioctl.h:1002-1003` |
| 16 | 4 | used | uint32_t | `whd/src/include/whd_wlioctl.h:1003` |
| 20 | 4 | needed | uint32_t | `whd/src/include/whd_wlioctl.h:1004` |

Size check: compiled
Differences: between builds (compiled): the table is the clang arm-none-eabi layout (sizeof 24, alignment 4; the same with -fno-short-enums and on the other 32-bit ARM variants compiled); the x86-64 builds (gcc, gcc -fshort-enums, clang) give sizeof 32, alignment 8: cmd at 0 (4), buf at 8 (8), len at 16 (4), set at 20 (1), used at 24 (4), needed at 28 (4). `whd/src/include/whd_wlioctl.h:997-1005`

### `ndconfig_item_t` (whd)
Host-only record, unused by whd: the name occurs only at its definition in whd/src and whd/inc, and nothing in these sources ties it to a payload; two host pointers, so not a wire layout `whd/src/include/whd_wlioctl.h:1619-1620`; not packed (alignment 4 on 32-bit ARM); 8 bytes on the 32-bit ARM builds (compiled; host-dependent); not serialised by whd; `whd/src/include/whd_wlioctl.h:1617-1621`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | name | int8_t * | host pointer `whd/src/include/whd_wlioctl.h:1619` |
| 4 | 4 | param | void * | host pointer `whd/src/include/whd_wlioctl.h:1620` |

Size check: compiled
Differences: between builds (compiled): the table is the clang arm-none-eabi layout (sizeof 8, alignment 4; the same with -fno-short-enums and on the other 32-bit ARM variants compiled); the x86-64 builds give sizeof 16, alignment 8: name at 0 (8), param at 8 (8). `whd/src/include/whd_wlioctl.h:1617-1621`

### `wl_assoc_result_t` (whd)
Host-dependent record, unused by whd: the name occurs only at its definition in whd/src and whd/inc, so no command, variable or event is tied to it in whd; `unsigned long` is 4 bytes on the 32-bit ARM builds and 8 on x86-64, so the source does not fix a wire layout `whd/src/include/whd_wlioctl.h:1624-1626`; not packed (alignment 4 on 32-bit ARM); 12 bytes on the 32-bit ARM builds (compiled; host-dependent); not serialised by whd; `whd/src/include/whd_wlioctl.h:1622-1627`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | associated | unsigned long | size depends on the host ABI `whd/src/include/whd_wlioctl.h:1624` |
| 4 | 4 | NDIS_auth | unsigned long | `whd/src/include/whd_wlioctl.h:1625` |
| 8 | 4 | NDIS_infra | unsigned long | `whd/src/include/whd_wlioctl.h:1626` |

Size check: compiled
Differences: between builds (compiled): the table is the clang arm-none-eabi layout (sizeof 12, alignment 4; the same with -fno-short-enums and on the other 32-bit ARM variants compiled); the x86-64 builds give sizeof 24, alignment 8: associated at 0 (8), NDIS_auth at 8 (8), NDIS_infra at 16 (8). `whd/src/include/whd_wlioctl.h:1622-1627`

### `whd_tko_retry` (whd)
Host API record of whd_tko_param (named variable "tko", sub-command PARAM), public typedef `whd_tko_retry_t` `whd/inc/whd_types.h:145`; not the wire form: what whd sends is wl_tko_t {subcmd_id = WL_TKO_SUBCMD_PARAM 1, len} followed by `wl_tko_param_t` inside "tko" `whd/src/whd_wifi_api.c:6139-6214` `whd/src/whd_wifi_api.c:6153-6168` `whd/src/include/whd_wlioctl.h:1264` `whd/src/include/whd_wlioctl.h:4307-4312` `whd/src/include/whd_wlioctl.h:4316` `whd/src/include/whd_wlioctl.h:4332-4338`; not packed (alignment 2; a source comment says the TKO definitions must stay outside pragma pack, and the last `#pragma pack()` is at line 4289 `whd/src/include/whd_wlioctl.h:4291-4293` `whd/src/include/whd_wlioctl.h:4289`); 6 bytes (same on the x86-64 and 32-bit ARM builds compiled); host-side: whd copies the three fields to and from `wl_tko_param_t` field by field with no htod16/dtoh16 `whd/src/whd_wifi_api.c:6175-6180` `whd/src/whd_wifi_api.c:6203-6205`; `whd/src/include/whd_wlioctl.h:4393-4398`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 2 | tko_interval | uint16_t | seconds; 0 selects the default TCP_KEEPALIVE_OFFLOAD_INTERVAL_SEC 20 `whd/src/whd_wifi_api.c:6175-6176` `whd/src/include/whd_wlioctl.h:4302` |
| 2 | 2 | tko_retry_count | uint16_t | 0 selects TCP_KEEPALIVE_OFFLOAD_RETRY_COUNT 3 `whd/src/whd_wifi_api.c:6177-6178` `whd/src/include/whd_wlioctl.h:4303` |
| 4 | 2 | tko_retry_interval | uint16_t | seconds; 0 selects TCP_KEEPALIVE_OFFLOAD_RETRY_INTERVAL_SEC 3 `whd/src/whd_wifi_api.c:6179-6180` `whd/src/include/whd_wlioctl.h:4304` |

Size check: compiled
Differences: from `wl_tko_param_t`: field order. This record is interval, retry_count, retry_interval (6 bytes); `wl_tko_param_t` is interval, retry_interval, retry_count, pad[2] (8 bytes). whd maps by name, so the difference does not reach the wire. `whd/src/include/whd_wlioctl.h:4332-4338`

### `whd_tko_auto_filter` (whd)
Host API record of whd_tko_filter / whd_configure_tko_filter (named variable "tko", sub-command FILTER) `whd/src/whd_wifi_api.c:6494-6545` `whd/src/whd_wifi_api.c:1053-1078`, public typedef `whd_tko_auto_filter_t` `whd/inc/whd_types.h:148`; the wire form is the identically laid out `wl_tko_filter_t`, which whd sends after wl_tko_t {subcmd_id = WL_TKO_SUBCMD_FILTER 8} in a set of "tko" `whd/src/whd_wifi_api.c:6518-6525` `whd/src/whd_wifi_api.c:6542` `whd/src/include/whd_wlioctl.h:4322`, and fields not selected by filter_flag keep whatever the buffer held, there being no memset of the wl_tko_filter_t area between lines 6509 and 6542 `whd/src/whd_wifi_api.c:6509-6542`; not packed (alignment 2, outside pragma pack); 40 bytes (same on the x86-64 and 32-bit ARM builds compiled); host-side: sport/dport assigned with no byte swap; `whd/src/include/whd_wlioctl.h:4490-4498`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 2 | version | uint16_t | not read from the caller: whd writes WL_TKO_AUTO_VER 1 into the wire record itself `whd/src/whd_wifi_api.c:6528` `whd/src/include/whd_wlioctl.h:39` |
| 2 | 2 | length | uint16_t | not read from the caller: whd computes it `whd/src/whd_wifi_api.c:6529` |
| 4 | 2 | sport | uint16_t | copied only if filter_flag has TKO_FILTER_SRC_PORT 0x4 `whd/src/whd_wifi_api.c:6530-6531` `whd/src/include/whd_wlioctl.h:42` |
| 6 | 2 | dport | uint16_t | copied only if TKO_FILTER_DST_PORT 0x8 `whd/src/whd_wifi_api.c:6533-6534` |
| 8 | 16 | ip_src | uint8_t[IPV6_ADDR_LEN] | copied only if TKO_FILTER_SRC_IP 0x1; IPV6_ADDR_LEN = 16 `whd/src/whd_wifi_api.c:6536-6537` `whd/inc/whd_types.h:106-108` |
| 24 | 16 | ip_dst | uint8_t[IPV6_ADDR_LEN] | copied only if TKO_FILTER_DST_IP 0x2 `whd/src/whd_wifi_api.c:6539-6540` |

Size check: compiled
Differences: from `wl_tko_filter_t`: none; identical field list, and it compiled to the same 40-byte layout. `whd/src/include/whd_wlioctl.h:4481-4488`

### `whd_tko_autoconnect` (whd)
Declared, never used by whd: the struct and its public typedef `whd_tko_autoconnect_t` are only declared `whd/inc/whd_types.h:149`; (inferred) the reply of "tko" sub-command WL_TKO_SUBCMD_AUTOCONNECT = 7, from the names and the comment on that constant, which is defined but sent by no whd function `whd/src/include/whd_wlioctl.h:4321`, the sub-commands whd sends being PARAM, STATUS, MAX_TCP, CONNECT, ENABLE, AUTOENAB, FILTER `whd/src/whd_wifi_api.c:6162` `whd/src/whd_wifi_api.c:6238` `whd/src/whd_wifi_api.c:6293` `whd/src/whd_wifi_api.c:6344` `whd/src/whd_wifi_api.c:6421` `whd/src/whd_wifi_api.c:6467` `whd/src/whd_wifi_api.c:6519`, so whether it is a wire record is not found in these sources; not packed (alignment 4, outside pragma pack; `bool` members 1 byte on every build compiled); 56 bytes (same on the x86-64 and 32-bit ARM builds compiled); byte order not shown by whd; `whd/src/include/whd_wlioctl.h:4500-4517`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 2 | version | uint16_t | `whd/src/include/whd_wlioctl.h:4502` |
| 2 | 2 | length | uint16_t | `whd/src/include/whd_wlioctl.h:4503` |
| 4 | 1 | index | uint8_t | `whd/src/include/whd_wlioctl.h:4504` |
| 5 | 1 | is_enabled | bool | source comment: is auto tko enabled or not `whd/src/include/whd_wlioctl.h:4505` |
| 6 | 1 | filter | uint8_t | source comment: the tx packets field to be filtered `whd/src/include/whd_wlioctl.h:4506` |
| 7 | 1 | ip_addr_type | uint8_t | source comment: valid only if allocated is TRUE; either ipv4 or ipv6 `whd/src/include/whd_wlioctl.h:4507` |
| 8 | 1 | allocated | bool | source comment: this wildcard has been allocated `whd/src/include/whd_wlioctl.h:4508` |
| 9 | 1 | pkt_created | bool | source comment: the ready packets for tx/rx are created `whd/src/include/whd_wlioctl.h:4509` |
| 10 | 2 | pad | uint8_t[2] | (pad) declared in the source `whd/src/include/whd_wlioctl.h:4510` |
| 12 | 16 | src_ip | uint8_t[IPV6_ADDR_LEN] | source comment: src ip for offload, ipv6/ipv4 shared `whd/src/include/whd_wlioctl.h:4511` |
| 28 | 16 | dst_ip | uint8_t[IPV6_ADDR_LEN] | source comment: dst ip for offload, ipv6/ipv4 shared `whd/src/include/whd_wlioctl.h:4512` |
| 44 | 2 | local_port | uint16_t | `whd/src/include/whd_wlioctl.h:4513` |
| 46 | 2 | remote_port | uint16_t | `whd/src/include/whd_wlioctl.h:4514` |
| 48 | 4 | local_seq | uint32_t | source comment: the local seq got `whd/src/include/whd_wlioctl.h:4515` |
| 52 | 4 | remote_seq | uint32_t | source comment: the remote seq got `whd/src/include/whd_wlioctl.h:4516` |

Size check: compiled
Differences: from `wl_tko_autoconnect_t`: none; identical field list, compiled to the identical 56-byte layout; that twin is unused too. `whd/src/include/whd_wlioctl.h:4463-4479`

### `whd_ssid_t` (whd)
Host API SSID record (whd_wifi_join, whd_wifi_scan, scan results); not sent or received as a block, the wire form is `wlc_ssid_t`: whd copies length and value into `wlc_ssid_t` for command WLC_SET_SSID in whd_wifi_join, after a 1..32 length check `whd/src/whd_wifi_api.c:2478-2483` `whd/src/whd_wifi_api.c:2454`, and into scan_params->params.ssid in whd_wifi_scan `whd/src/whd_wifi_api.c:3250-3253` `whd/src/whd_wifi_api.c:3333-3336`; it is also the SSID member of `whd_scan_result_t`, `whd_sync_scan_result_t` and `whd_ap_info_t` `whd/inc/whd_types.h:883` `whd/inc/whd_types.h:911` `whd/inc/whd_types.h:1127`; not packed (all uint8_t, alignment 1); 33 bytes (same on the x86-64 and 32-bit ARM builds compiled); no byte order (single bytes); `whd/inc/whd_types.h:584-588`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 1 | length | uint8_t | 1 byte here; the wire record `wlc_ssid_t` carries the length as a 32-bit value, written by whd with htod32 `whd/inc/whd_types.h:586` `whd/src/whd_wifi_api.c:2481` `whd/src/whd_wifi_api.c:3335` |
| 1 | 32 | value | uint8_t[SSID_NAME_SIZE] | SSID_NAME_SIZE = 32 `whd/inc/whd_types.h:587` `whd/inc/whd_types.h:61` |

Size check: compiled
Differences: from `wlc_ssid_t`: this record is a 1-byte length + 32 bytes (33 bytes); `wlc_ssid_t` is a uint32_t length followed by 32 bytes. `whd/src/include/whd_wlioctl.h:496-500`

### `whd_scan_extended_params_t` (whd)
Host API record, optional argument of whd_wifi_scan, used only when the argument is non-NULL `whd/src/whd_wifi_api.c:3250-3256` `whd/src/whd_wifi_api.c:3350`; not sent or received as a block; not packed (alignment 4); 16 bytes (same on the x86-64 and 32-bit ARM builds compiled); host-side: whd converts each field with htod32 as it copies it into the scan parameters `whd/src/whd_wifi_api.c:3352-3358`; `whd/inc/whd_types.h:869-875`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | number_of_probes_per_channel | int32_t | copied to scan_params->params.nprobes `whd/src/whd_wifi_api.c:3352` |
| 4 | 4 | scan_active_dwell_time_per_channel_ms | int32_t | copied to params.active_time `whd/src/whd_wifi_api.c:3353-3354` |
| 8 | 4 | scan_passive_dwell_time_per_channel_ms | int32_t | copied to params.passive_time `whd/src/whd_wifi_api.c:3355-3356` |
| 12 | 4 | scan_home_channel_dwell_time_between_channels_ms | int32_t | copied to params.home_time `whd/src/whd_wifi_api.c:3357-3358` |

Size check: compiled

### `whd_listen_interval_t` (whd)
Host API record, output of whd_wifi_get_listen_interval, assembled from three gets of named variables, each with a 4-byte request buffer `whd/src/whd_wifi_api.c:4103-4148`; not sent or received as a block; not packed (alignment 2); 4 bytes (same on the x86-64 and 32-bit ARM builds compiled); host-side: the three values are copied from the replies with memcpy, with no dtoh16 on assoc `whd/src/whd_wifi_api.c:4126` `whd/src/whd_wifi_api.c:4135` `whd/src/whd_wifi_api.c:4144`; `whd/inc/whd_types.h:969-974`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 1 | beacon | uint8_t | first byte of the reply to a get of "bcn_li_bcn" `whd/src/whd_wifi_api.c:4120-4126` `whd/src/include/whd_wlioctl.h:1083` |
| 1 | 1 | dtim | uint8_t | first byte of the reply to a get of "bcn_li_dtim" `whd/src/whd_wifi_api.c:4129-4135` `whd/src/include/whd_wlioctl.h:1084` |
| 2 | 2 | assoc | uint16_t | first 2 bytes of the reply to a get of "assoc_listen" `whd/src/whd_wifi_api.c:4138-4144` `whd/src/include/whd_wlioctl.h:1085` |

Size check: compiled

### `whd_scan_result_t` (whd)
Host API scan record handed to the application's scan callback; not sent or received as a block, the wire form is `wl_bss_info_t`: whd fills it per BSS in the escan event handler from the wire records wl_escan_result_t / wl_bss_info_t `whd/src/whd_wifi_api.c:2587-2590` `whd/src/whd_wifi_api.c:2686-3067`; packed (pragma pack(1) `whd/inc/whd_types.h:880-904`, alignment 1); 344 bytes on the clang 32-bit ARM build (compiled; host-dependent because of two pointers and three enums, and these sources do not fix the compiler or enum flag of a real embedded build, so the table is one possible build); host-side only, so none of the build differences reaches the wire; `whd/inc/whd_types.h:881-903`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 33 | SSID | whd_ssid_t | `whd/inc/whd_types.h:883` |
| 33 | 6 | BSSID | whd_mac_t | `whd/inc/whd_types.h:884` |
| 39 | 2 | signal_strength | int16_t | `whd/inc/whd_types.h:885` |
| 41 | 4 | max_data_rate | uint32_t | kbit/s `whd/inc/whd_types.h:886` |
| 45 | 4 | bss_type | whd_bss_type_t | enum; size is compiler-dependent `whd/inc/whd_types.h:887` |
| 49 | 8 | security | whd_security_t | enum; 8 bytes on every build compiled `whd/inc/whd_types.h:888` |
| 57 | 4 | fbtbitmap | uint32_t | `whd/inc/whd_types.h:889` |
| 61 | 1 | channel | uint8_t | chanspec & 0xff or the control channel `whd/src/whd_wifi_api.c:2680-2698` |
| 62 | 4 | band | whd_802_11_band_t | enum; from the chanspec band bits `whd/src/whd_wifi_api.c:3008-3009` |
| 66 | 2 | ccode | uint8_t[2] | `whd/inc/whd_types.h:892` |
| 68 | 1 | flags | uint8_t | `whd/inc/whd_types.h:893` |
| 69 | 4 | next | struct whd_scan_result * | host pointer `whd/inc/whd_types.h:894` |
| 73 | 4 | ie_ptr | uint8_t * | host pointer `whd/inc/whd_types.h:895` |
| 77 | 4 | ie_len | uint32_t | `whd/inc/whd_types.h:896` |
| 81 | 1 | current_operating_class | uint8_t | `whd/inc/whd_types.h:897` |
| 82 | 1 | num_supported_operating_classes | uint8_t | `whd/inc/whd_types.h:898` |
| 83 | 255 | supported_operating_classes | uint8_t[255] | `whd/inc/whd_types.h:899` |
| 338 | 2 | snr | int16_t | `whd/inc/whd_types.h:900` |
| 340 | 2 | beacon_period | uint16_t | `whd/inc/whd_types.h:901` |
| 342 | 2 | capability | uint16_t | `whd/inc/whd_types.h:902` |

Size check: compiled
Differences: between builds (compiled): the table is the clang arm-none-eabi layout (sizeof 344, alignment 1; the same with -fno-short-enums). gcc x86-64 = clang x86-64: sizeof 352; as the table through flags at 68, then next at 69 (8), ie_ptr at 77 (8), ie_len at 85 (4), current_operating_class at 89, num_supported_operating_classes at 90, supported_operating_classes at 91 (255), snr at 346, beacon_period at 348, capability at 350. `whd/inc/whd_types.h:881-903`
Differences: between builds (compiled): gcc x86-64 -fshort-enums: sizeof 346; bss_type at 45 (1), security at 46 (8), fbtbitmap at 54, channel at 58, band at 59 (1), ccode at 60, flags at 62, next at 63 (8), ie_ptr at 71 (8), ie_len at 79, current_operating_class at 83, num_supported_operating_classes at 84, supported_operating_classes at 85, snr at 340, beacon_period at 342, capability at 344. `whd/inc/whd_types.h:881-903`
Differences: between builds (compiled): a non-LLVM ARM build emulated with clang arm-none-eabi -U__llvm__ and -fshort-enums: sizeof 338; bss_type at 45 (1), security at 46 (8), fbtbitmap at 54, channel at 58, band at 59 (1), ccode at 60, flags at 62, next at 63 (4), ie_ptr at 67 (4), ie_len at 71, current_operating_class at 75, num_supported_operating_classes at 76, supported_operating_classes at 77, snr at 332, beacon_period at 334, capability at 336; with -fno-short-enums: sizeof 344, same as the table. Under clang, whd_types.h takes its `__llvm__` branch, where whd_bool_t is uint8_t. `whd/inc/whd_types.h:276-286`

### `whd_sync_scan_result_t` (whd)
Host API record of the synchronous scan API; not sent or received as a block: whd_scan_result_handler copies it field by field from `whd_scan_result_t` `whd/src/whd_wifi_api.c:3118-3169` `whd/inc/whd_wifi_api.h:258`; not packed (natural alignment 8; padding after BSSID, after signal_strength and at the end because whd_security_t is 8 bytes wide); 64 bytes (same on the x86-64 and 32-bit ARM builds compiled); host-side; `whd/inc/whd_types.h:909-916`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 33 | SSID | whd_ssid_t | `whd/inc/whd_types.h:911` |
| 33 | 6 | BSSID | whd_mac_t | `whd/inc/whd_types.h:912` |
| 39 | 1 | (pad) | padding | implicit alignment padding, not declared in the source `whd/inc/whd_types.h:912-913` |
| 40 | 2 | signal_strength | int16_t | `whd/inc/whd_types.h:913` |
| 42 | 6 | (pad) | padding | implicit alignment padding, not declared in the source `whd/inc/whd_types.h:913-914` |
| 48 | 8 | security | whd_security_t | enum, 8 bytes and 8-byte aligned on every build compiled `whd/inc/whd_types.h:914` |
| 56 | 1 | channel | uint8_t | `whd/inc/whd_types.h:915` |
| 57 | 7 | (pad) | padding | trailing alignment padding counted by sizeof, not declared in the source `whd/inc/whd_types.h:915-916` |

Size check: compiled

### `whd_ap_info_t` (whd)
Host API record, only declared: no use found in whd/src or the other whd/inc headers; not a wire record; packed (pragma pack(1) `whd/inc/whd_types.h:1120-1147`, alignment 1); 66 bytes on the clang 32-bit ARM build (compiled; host-dependent because of a pointer and enums, and these sources do not fix the compiler or enum flag of a real embedded build, so the table is one possible build); host-side only, so none of the build differences reaches the wire; `whd/inc/whd_types.h:1125-1136`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 33 | SSID | whd_ssid_t | `whd/inc/whd_types.h:1127` |
| 33 | 6 | BSSID | whd_mac_t | `whd/inc/whd_types.h:1128` |
| 39 | 2 | signal_strength | int16_t | `whd/inc/whd_types.h:1129` |
| 41 | 4 | max_data_rate | uint32_t | `whd/inc/whd_types.h:1130` |
| 45 | 4 | bss_type | whd_bss_type_t | enum `whd/inc/whd_types.h:1131` |
| 49 | 8 | security | whd_security_t | enum, 8 bytes `whd/inc/whd_types.h:1132` |
| 57 | 1 | channel | uint8_t | `whd/inc/whd_types.h:1133` |
| 58 | 4 | band | whd_802_11_band_t | enum `whd/inc/whd_types.h:1134` |
| 62 | 4 | next | struct whd_ap_info * | host pointer `whd/inc/whd_types.h:1135` |

Size check: compiled
Differences: between builds (compiled): the table is the clang arm-none-eabi layout (sizeof 66, alignment 1; the same with -fno-short-enums). gcc x86-64 = clang x86-64: sizeof 70, as the table but next is 8 bytes at 62. gcc x86-64 -fshort-enums: sizeof 64; bss_type at 45 (1), security at 46 (8), channel at 54, band at 55 (1), next at 56 (8). A non-LLVM ARM build emulated with clang arm-none-eabi -U__llvm__ and -fshort-enums: sizeof 60; bss_type at 45 (1), security at 46 (8), channel at 54, band at 55 (1), next at 56 (4); with -fno-short-enums: sizeof 66, same as the table. `whd/inc/whd_types.h:1125-1136`

### `whd_wep_key_t` (whd)
Declared, never used by whd: no use found in whd/src or the other whd/inc headers, so whether this layout is ever put on the wire is not found in these sources; a security check in whd returns WHD_WEP_NOT_ALLOWED when auth_type has WEP_ENABLED set `whd/src/whd_wifi_api.c:1738-1740`; not packed (all uint8_t, alignment 1); 34 bytes (same on the x86-64 and 32-bit ARM builds compiled); no byte order (single bytes); `whd/inc/whd_types.h:1185-1190`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 1 | index | uint8_t | source comment: WEP key index 0-3 `whd/inc/whd_types.h:1187` |
| 1 | 1 | length | uint8_t | source comment: 5 or 13 `whd/inc/whd_types.h:1188` |
| 2 | 32 | data | uint8_t[32] | `whd/inc/whd_types.h:1189` |

Size check: compiled

### `whd_he_omi_params_t` (whd)
Host API record, argument of whd_wifi_he_omi (named variable "he"); not sent or received as a block, the wire form is `wl_he_omi_t`: whd copies the first seven fields by name into `wl_he_omi_t`, which is what it sends `whd/src/whd_wifi_api.c:4376-4404`; not packed (all uint8_t, alignment 1); 8 bytes (same on the x86-64 and 32-bit ARM builds compiled); no byte order (single bytes); `whd/inc/whd_types.h:1211-1221`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 1 | rx_nss | uint8_t | `whd/inc/whd_types.h:1213` |
| 1 | 1 | chnl_wdth | uint8_t | `whd/inc/whd_types.h:1214` |
| 2 | 1 | ul_mu_dis | uint8_t | `whd/inc/whd_types.h:1215` |
| 3 | 1 | tx_nsts | uint8_t | `whd/inc/whd_types.h:1216` |
| 4 | 1 | er_su_dis | uint8_t | `whd/inc/whd_types.h:1217` |
| 5 | 1 | dl_mu_resound | uint8_t | `whd/inc/whd_types.h:1218` |
| 6 | 1 | ul_mu_data_dis | uint8_t | `whd/inc/whd_types.h:1219` |
| 7 | 1 | reserved | uint8_t | not copied to the wire record `whd/inc/whd_types.h:1220` `whd/src/whd_wifi_api.c:4376-4404` |

Size check: compiled
Differences: from `wl_he_omi_t`: 8 bytes here against 9 on the wire; the wire record adds version and length in front and has no reserved byte. `whd/src/include/whd_wlioctl.h:138-149`

### `whd_itwt_setup_params_t` (whd)
Host API record, argument of whd_wifi_itwt_setup (named variable "twt"), where a NULL argument selects built-in defaults `whd/src/whd_wifi_api.c:4600-4608`; not sent or received as a block, the wire form is `wl_twt_setup_t`: whd translates it into `wl_twt_setup_t`, carried as an xtlv value (id WL_TWT_CMD_SETUP, negotiation_type TWT_CTRL_NEGO_TYPE_0) in a set of "twt" `whd/src/whd_wifi_api.c:4577-4627` `whd/src/include/whd_wlioctl.h:1269`; not packed (alignment 4); 16 bytes (same on the x86-64 and 32-bit ARM builds compiled); host-side: values assigned with no htod conversion `whd/src/whd_wifi_api.c:4612-4619`; `whd/inc/whd_types.h:1226-1237`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 1 | setup_cmd | uint8_t | copied to desc.setup_cmd `whd/src/whd_wifi_api.c:4612` |
| 1 | 1 | trigger | uint8_t | non-zero sets WL_TWT_FLOW_FLAG_TRIGGER `whd/src/whd_wifi_api.c:4616` |
| 2 | 1 | flow_type | uint8_t | non-zero sets WL_TWT_FLOW_FLAG_UNANNOUNCED `whd/src/whd_wifi_api.c:4617` |
| 3 | 1 | flow_id | uint8_t | copied to desc.flow_id; source comment: 0xFF means any `whd/src/whd_wifi_api.c:4615` `whd/inc/whd_types.h:1231` |
| 4 | 1 | wake_duration | uint8_t | desc.wake_dur = value * 256 `whd/src/whd_wifi_api.c:4613` |
| 5 | 1 | exponent | uint8_t | desc.wake_int = mantissa * (1 << exponent) `whd/src/whd_wifi_api.c:4614` |
| 6 | 2 | mantissa | uint16_t | see exponent `whd/src/whd_wifi_api.c:4614` |
| 8 | 4 | wake_time_h | uint32_t | copied to desc.wake_time_h `whd/src/whd_wifi_api.c:4618` |
| 12 | 4 | wake_time_l | uint32_t | copied to desc.wake_time_l `whd/src/whd_wifi_api.c:4619` |

Size check: compiled

### `whd_btwt_join_params_t` (whd)
Host API record, argument of whd_wifi_btwt_join (named variable "twt"); not sent or received as a block, the wire form is `wl_twt_setup_t`: whd translates it into `wl_twt_setup_t` with negotiation_type TWT_CTRL_NEGO_TYPE_3 and wake_type WL_TWT_TIME_TYPE_BSS, forcing desc.flow_id to 0 `whd/src/whd_wifi_api.c:4671`, then allocates sizeof(wl_twt_setup_t) + 4, sets xtlv id WL_TWT_CMD_SETUP (1) and len sizeof(wl_twt_setup_t), copies the record and issues the set of "twt" `whd/src/whd_wifi_api.c:4651-4688` `whd/src/whd_wifi_api.c:4681-4687` `whd/src/include/whd_wlioctl.h:158` `whd/src/include/whd_wlioctl.h:1269`; not packed (alignment 4); 16 bytes (same on the x86-64 and 32-bit ARM builds compiled); host-side: no htod conversion at the assignments `whd/src/whd_wifi_api.c:4674-4679`; `whd/inc/whd_types.h:1242-1253`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 1 | setup_cmd | uint8_t | copied to desc.setup_cmd `whd/src/whd_wifi_api.c:4674` |
| 1 | 1 | trigger | uint8_t | WL_TWT_FLOW_FLAG_TRIGGER `whd/src/whd_wifi_api.c:4675` |
| 2 | 1 | flow_type | uint8_t | WL_TWT_FLOW_FLAG_UNANNOUNCED `whd/src/whd_wifi_api.c:4676` |
| 3 | 1 | bid | uint8_t | copied to desc.bid `whd/src/whd_wifi_api.c:4679` |
| 4 | 1 | wake_duration | uint8_t | desc.wake_dur = value * 256 `whd/src/whd_wifi_api.c:4677` |
| 5 | 1 | exponent | uint8_t | desc.wake_int = mantissa * (1 << exponent) `whd/src/whd_wifi_api.c:4678` |
| 6 | 2 | mantissa | uint16_t | see exponent `whd/src/whd_wifi_api.c:4678` |
| 8 | 4 | wake_time_h | uint32_t | never read by whd_wifi_btwt_join `whd/src/whd_wifi_api.c:4651-4688` |
| 12 | 4 | wake_time_l | uint32_t | never read by whd_wifi_btwt_join `whd/src/whd_wifi_api.c:4651-4688` |

Size check: compiled

### `whd_twt_teardown_params_t` (whd)
Host API record, argument of whd_wifi_twt_teardown (named variable "twt"); not sent or received as a block, the wire form is `wl_twt_teardown_t`: whd translates it into `wl_twt_teardown_t`, carried as an xtlv value (id WL_TWT_CMD_TEARDOWN) in a set of "twt" `whd/src/whd_wifi_api.c:4690-4727` `whd/src/include/whd_wlioctl.h:1269`; not packed (all uint8_t, alignment 1); 4 bytes (same on the x86-64 and 32-bit ARM builds compiled); no byte order (single bytes); `whd/inc/whd_types.h:1258-1264`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 1 | negotiation_type | uint8_t | copied to teardesc.negotiation_type `whd/src/whd_wifi_api.c:4716` |
| 1 | 1 | flow_id | uint8_t | copied to teardesc.flow_id `whd/src/whd_wifi_api.c:4717` |
| 2 | 1 | bcast_twt_id | uint8_t | copied to teardesc.bid `whd/src/whd_wifi_api.c:4718` |
| 3 | 1 | teardown_all_twt | uint8_t | copied to teardesc.alltwt `whd/src/whd_wifi_api.c:4719` |

Size check: compiled

### `whd_btwt_config_params_t` (whd)
Host API record, argument of whd_wifi_btwt_config (named variable "twt"); not sent or received as a block, the wire form is `wl_twt_setup_t`: whd translates it into `wl_twt_setup_t` with negotiation_type TWT_CTRL_NEGO_TYPE_2 and xtlv id WL_TWT_CMD_SETUP, in a set of "twt" `whd/src/whd_wifi_api.c:4826-4860` `whd/src/include/whd_wlioctl.h:1269`; not packed (alignment 2); 8 bytes (same on the x86-64 and 32-bit ARM builds compiled); host-side: the assignments carry no htod conversion `whd/src/whd_wifi_api.c:4847-4852`; `whd/inc/whd_types.h:1269-1278`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 1 | setup_cmd | uint8_t | copied to desc.setup_cmd `whd/src/whd_wifi_api.c:4847` |
| 1 | 1 | trigger | uint8_t | WL_TWT_FLOW_FLAG_TRIGGER `whd/src/whd_wifi_api.c:4851` |
| 2 | 1 | flow_type | uint8_t | WL_TWT_FLOW_FLAG_UNANNOUNCED `whd/src/whd_wifi_api.c:4852` |
| 3 | 1 | bid | uint8_t | copied to desc.bid `whd/src/whd_wifi_api.c:4850` |
| 4 | 1 | wake_duration | uint8_t | desc.wake_dur = value * 256 `whd/src/whd_wifi_api.c:4848` |
| 5 | 1 | exponent | uint8_t | desc.wake_int = mantissa * (1 << exponent) `whd/src/whd_wifi_api.c:4849` |
| 6 | 2 | mantissa | uint16_t | see exponent `whd/src/whd_wifi_api.c:4849` |

Size check: compiled

### `whd_twt_information_params_t` (whd)
Host API record, argument of whd_wifi_twt_information_frame (named variable "twt"); not sent or received as a block, the wire form is `wl_twt_info_t`: whd translates it into `wl_twt_info_t`, carried as an xtlv value in a set of "twt" `whd/src/whd_wifi_api.c:4751-4790` `whd/src/include/whd_wlioctl.h:1269`; not packed (all uint8_t, alignment 1); 4 bytes (same on the x86-64 and 32-bit ARM builds compiled); no byte order (single bytes); `whd/inc/whd_types.h:1283-1289`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 1 | flow_id | uint8_t | copied to infodesc.flow_id `whd/src/whd_wifi_api.c:4775` |
| 1 | 1 | suspend | uint8_t | 1 = suspend (next_twt 0); otherwise whd sets WL_TWT_INFO_FLAG_RESUME `whd/src/whd_wifi_api.c:4776-4786` |
| 2 | 1 | resume_time | uint8_t | seconds; infodesc.next_twt_l = value * 1000000. The source comment says 0 to 4095 seconds but the field is one byte `whd/src/whd_wifi_api.c:4785` `whd/inc/whd_types.h:1287` |
| 3 | 1 | reserved | uint8_t | `whd/inc/whd_types.h:1288` |

Size check: compiled

### `whd_itwt_negotiated_params_t` (whd)
Host record derived from the TWT setup event (WLC_E_TWT_SETUP) `whd/src/whd_wifi_api.c:4430-4476`; not sent or received as a block: it is the member twt_negotiated_info of the interface record `whd/src/include/whd_int.h:91`, and whd_wifi_itwt_get_negotiated_info returns it with a memcpy `whd/src/whd_wifi_api.c:4797-4809`; not packed (natural alignment 8, forced by the uint64_t member); 40 bytes on the clang 32-bit ARM build, between 40 and 48 bytes by compiler (compiled; host-dependent because of the enum and whd_bool_t members, and these sources do not fix the compiler or enum flag of a real embedded build, so the table is one possible build); host-side only, so none of the build differences reaches the wire: filled with dtoh32 from the event's wl_twt_sdesc_t `whd/src/whd_wifi_api.c:4452-4454`; `whd/inc/whd_types.h:1314-1325`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | session_state | whd_twt_session_state_t | enum; size is compiler-dependent `whd/inc/whd_types.h:1291-1297` |
| 4 | 1 | flow_id | uint8_t | desc->flow_id `whd/src/whd_wifi_api.c:4450` |
| 5 | 1 | dialog_token | uint8_t | twt_setup_cplt->dialog `whd/src/whd_wifi_api.c:4451` |
| 6 | 6 | peer_mac | whd_mac_t | no assignment found in the handler lines cited `whd/src/whd_wifi_api.c:4444-4476` |
| 12 | 4 | (pad) | padding | implicit alignment padding, not declared in the source `whd/inc/whd_types.h:1318-1319` |
| 16 | 8 | target_wake_time | uint64_t | (wake_time_h << 32) \| wake_time_l `whd/src/whd_wifi_api.c:4452` |
| 24 | 4 | wake_duration | uint32_t | desc->wake_dur `whd/src/whd_wifi_api.c:4453` |
| 28 | 4 | wake_interval | uint32_t | desc->wake_int `whd/src/whd_wifi_api.c:4454` |
| 32 | 1 | is_implicit | whd_bool_t | WL_TWT_FLOW_FLAG_IMPLICIT set; whd_bool_t is uint8_t under `__llvm__` and an enum otherwise `whd/src/whd_wifi_api.c:4455` `whd/inc/whd_types.h:276-286` |
| 33 | 1 | is_triggered | whd_bool_t | WL_TWT_FLOW_FLAG_TRIGGER set `whd/src/whd_wifi_api.c:4456` |
| 34 | 1 | is_announced | whd_bool_t | WL_TWT_FLOW_FLAG_UNANNOUNCED clear `whd/src/whd_wifi_api.c:4457` |
| 35 | 5 | (pad) | padding | trailing alignment padding counted by sizeof, not declared in the source `whd/inc/whd_types.h:1324-1325` |

Size check: compiled
Differences: between builds (compiled): the table is the clang arm-none-eabi layout (sizeof 40, alignment 8; the same with -fno-short-enums and with clang x86-64). gcc x86-64: sizeof 48; as the table through wake_interval at 28, then is_implicit at 32 (4), is_triggered at 36 (4), is_announced at 40 (4). gcc x86-64 -fshort-enums: sizeof 40; session_state at 0 (1), flow_id at 1, dialog_token at 2, peer_mac at 3 (6), target_wake_time at 16, then as the table. A non-LLVM ARM build emulated with clang arm-none-eabi -U__llvm__ and -fshort-enums: sizeof 40, same offsets as the gcc x86-64 -fshort-enums build; with -fno-short-enums: sizeof 48, same offsets as the gcc x86-64 build. `whd/inc/whd_types.h:1314-1325`

### `whd_mbo_add_chan_pref_params_t` (whd)
Host API record, argument of whd_wifi_mbo_add_chan_pref (named variable "mbo", IOVAR_STR_MBO `whd/src/include/whd_wlioctl.h:1274`); not sent or received as a block, the wire form is `mbo_add_chan_pref_t`: each byte becomes the value of its own xtlv inside `mbo_add_chan_pref_t`, which whd sends in a set of "mbo" `whd/src/whd_wifi_api.c:4974-4975` after a whd_iov_buf_t header {version WL_MBO_IOV_VERSION, len, id WL_MBO_CMD_ADD_CHAN_PREF} `whd/src/whd_wifi_api.c:4945-4980`, with WL_MBO_IOV_VERSION = (1 << 8) | 1 = 257 (0x0101) and WL_MBO_CMD_ADD_CHAN_PREF = 1 `whd/src/include/whd_wlioctl.h:373-377` `whd/src/include/whd_wlioctl.h:380`; not packed (all uint8_t, alignment 1); 4 bytes (same on the x86-64 and 32-bit ARM builds compiled); no byte order (single bytes), and whd assigns the header's version, len and id as host-order values with no htod16 `whd/src/whd_wifi_api.c:4977-4979`; `whd/inc/whd_types.h:1342-1348`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 1 | opclass | uint8_t | value of xtlv WL_MBO_XTLV_OPCLASS (id 1) `whd/src/whd_wifi_api.c:4958-4960` `whd/src/include/whd_wlioctl.h:405-408` |
| 1 | 1 | chan | uint8_t | value of xtlv WL_MBO_XTLV_CHAN (id 2) `whd/src/whd_wifi_api.c:4962-4964` `whd/src/include/whd_wlioctl.h:405-408` |
| 2 | 1 | pref | uint8_t | value of xtlv WL_MBO_XTLV_PREFERENCE (id 3); source comment: 0 non operable, 1 non preferred, 255 preferred `whd/src/whd_wifi_api.c:4966-4968` `whd/inc/whd_types.h:1346` `whd/src/include/whd_wlioctl.h:405-408` |
| 3 | 1 | reason | uint8_t | value of xtlv WL_MBO_XTLV_REASON_CODE (id 4) `whd/src/whd_wifi_api.c:4970-4972` `whd/src/include/whd_wlioctl.h:405-408` |

Size check: compiled

### `whd_mbo_del_chan_pref_params_t` (whd)
Host API record, argument of whd_wifi_mbo_del_chan_pref (named variable "mbo"); not sent or received as a block, the wire form is `mbo_del_chan_pref_t`: each byte becomes the value of its own xtlv inside `mbo_del_chan_pref_t`, sent after a whd_iov_buf_t header {version WL_MBO_IOV_VERSION, len, id WL_MBO_CMD_DEL_CHAN_PREF} in a set of "mbo" `whd/src/whd_wifi_api.c:4984-5012` `whd/src/include/whd_wlioctl.h:1274`, with WL_MBO_IOV_VERSION = 257 (0x0101) and WL_MBO_CMD_DEL_CHAN_PREF = 2 `whd/src/include/whd_wlioctl.h:373-377` `whd/src/include/whd_wlioctl.h:381`; not packed (all uint8_t, alignment 1); 2 bytes (same on the x86-64 and 32-bit ARM builds compiled); no byte order (single bytes), and whd applies no htod16 to the header's version, len or id `whd/src/whd_wifi_api.c:5008-5010`; `whd/inc/whd_types.h:1353-1357`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 1 | opclass | uint8_t | value of xtlv WL_MBO_XTLV_OPCLASS (id 1) `whd/src/whd_wifi_api.c:4997-4999` `whd/src/include/whd_wlioctl.h:405-406` |
| 1 | 1 | chan | uint8_t | value of xtlv WL_MBO_XTLV_CHAN (id 2) `whd/src/whd_wifi_api.c:5001-5003` `whd/src/include/whd_wlioctl.h:405-406` |

Size check: compiled

### `whd_coex_config_t` (whd)
Wrapper holding exactly one `whd_btc_lescan_params_t`; whd_wifi_set_coex_config sends the inner struct, &coex_config->le_scan_params, 12 bytes, as a set of the named variable "btc_lescan_params", so the wrapper's bytes equal the payload and the record sent is the inner struct `whd/src/whd_wifi_api.c:5446-5455` `whd/src/include/whd_wlioctl.h:1253`; not packed (alignment 2); 12 bytes (same on the x86-64 and 32-bit ARM builds compiled); not converted by whd: the inner struct is passed straight to whd_wifi_set_iovar_buffer `whd/src/whd_wifi_api.c:5453-5454`; `whd/inc/whd_types.h:1444-1447`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 12 | le_scan_params | whd_btc_lescan_params_t | six uint16_t in order: priority, duty_cycle, max_win, int_grant, scan_int, scan_win `whd/inc/whd_types.h:1431-1439` |

Size check: compiled

### `whd_packet_filter_t` (whd)
Host API record, argument of whd_pf_add_packet_filter (named variable "pkt_filter_add"); not sent or received as a block, the wire form is `wl_pkt_filter_t`, which whd builds with length 2 * mask_size + WL_PKT_FILTER_FIXED_LEN + WL_PKT_FILTER_PATTERN_FIXED_LEN and with packet_filter->type = 0 `whd/src/whd_wifi_api.c:5994-6021` `whd/src/whd_wifi_api.c:6012` `whd/src/include/whd_wlioctl.h:1092`; not packed (alignment 4 on 32-bit ARM); 24 bytes on the clang 32-bit ARM build (compiled; host-dependent because of pointers, an enum and whd_bool_t, and these sources do not fix the compiler or enum flag of a real embedded build, so the table is one possible build); host-side only, so none of the build differences reaches the wire: fields assigned one by one with no htod conversion `whd/src/whd_wifi_api.c:6011-6015`; `whd/inc/whd_types.h:1463-1472`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | id | uint32_t | copied to packet_filter->id `whd/src/whd_wifi_api.c:6011` |
| 4 | 4 | rule | whd_packet_filter_rule_t | enum, POSITIVE 0 / NEGATIVE 1; copied to negate_match `whd/inc/whd_types.h:1454-1458` `whd/src/whd_wifi_api.c:6013` |
| 8 | 2 | offset | uint16_t | copied to u.pattern.offset, widened to 32 bits `whd/src/whd_wifi_api.c:6014` |
| 10 | 2 | mask_size | uint16_t | copied to u.pattern.size_bytes `whd/src/whd_wifi_api.c:6015` |
| 12 | 4 | mask | uint8_t * | host pointer; mask_size bytes copied to mask_and_pattern `whd/src/whd_wifi_api.c:6018` |
| 16 | 4 | pattern | uint8_t * | host pointer; mask_size bytes copied after the mask `whd/src/whd_wifi_api.c:6021` |
| 20 | 1 | enabled_status | whd_bool_t | output only per the source comment `whd/inc/whd_types.h:1471` |
| 21 | 3 | (pad) | padding | trailing alignment padding counted by sizeof, not declared in the source `whd/inc/whd_types.h:1471-1472` |

Size check: compiled
Differences: between builds (compiled): the table is the clang arm-none-eabi layout (sizeof 24, alignment 4; the same with -fno-short-enums). gcc x86-64: sizeof 40, alignment 8: id at 0 (4), rule at 4 (4), offset at 8 (2), mask_size at 10 (2), mask at 16 (8), pattern at 24 (8), enabled_status at 32 (4); clang x86-64: the same but enabled_status is 1 byte. gcc x86-64 -fshort-enums: sizeof 40: id at 0 (4), rule at 4 (1), offset at 6 (2), mask_size at 8 (2), mask at 16 (8), pattern at 24 (8), enabled_status at 32 (1). A non-LLVM ARM build emulated with clang arm-none-eabi -U__llvm__ and -fshort-enums: sizeof 24: id at 0 (4), rule at 4 (1), offset at 6 (2), mask_size at 8 (2), mask at 12 (4), pattern at 16 (4), enabled_status at 20 (1); with -fno-short-enums: sizeof 24, as the table but enabled_status is 4 bytes at 20. `whd/inc/whd_types.h:1463-1472`

### `whd_keep_alive_t` (whd)
Host API record, argument of whd_wifi_keepalive_config (named variable "keep_alive"); not sent or received as a block, the wire form is `wl_keep_alive_pkt_t`, which whd builds for a set of "keep_alive" `whd/src/whd_wifi_api.c:1018-1051` `whd/src/include/whd_wlioctl.h:1273`: WHD_KEEPALIVE_NULL sends sizeof(wl_keep_alive_pkt_t) zeroed bytes with only period_msec set, WHD_KEEPALIVE_NAT allocates 2 * len_bytes + WL_KEEP_ALIVE_FIXED_LEN and copies len_bytes of data, and in the NAT branch whd does not memset the buffer before the three assignments, unlike the NULL branch `whd/src/whd_wifi_api.c:1040-1046` `whd/src/whd_wifi_api.c:1032`; not packed (alignment 4 on 32-bit ARM); 12 bytes on the 32-bit ARM builds (compiled; host-dependent because of the pointer); host-side: period_msec and len_bytes assigned with no htod conversion; `whd/inc/whd_types.h:1474-1479`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | period_msec | uint32_t | copied to keepalive_cfg->period_msec `whd/src/whd_wifi_api.c:1034` `whd/src/whd_wifi_api.c:1044-1045` |
| 4 | 2 | len_bytes | uint16_t | copied to keepalive_cfg->len_bytes; not used for the NULL-packet variant `whd/src/whd_wifi_api.c:1044-1045` |
| 6 | 2 | (pad) | padding | implicit alignment padding, not declared in the source `whd/inc/whd_types.h:1477-1478` |
| 8 | 4 | data | uint8_t * | host pointer; len_bytes bytes copied to keepalive_cfg->data `whd/src/whd_wifi_api.c:1046` |

Size check: compiled
Differences: between builds (compiled): the table is the clang arm-none-eabi layout (sizeof 12, alignment 4; the same with -fno-short-enums and on the other 32-bit ARM variants compiled); the x86-64 builds give sizeof 16, alignment 8: period_msec at 0 (4), len_bytes at 4 (2), data at 8 (8). `whd/inc/whd_types.h:1474-1479`

### `whd_icmp_echo_req_info_t` (whd)
Host API record, output of whd_wifi_icmp_echo_req_get_info (named variable "icmp_echo_req", sub-command WL_ICMP_ECHO_REQ_INFO) `whd/src/whd_wifi_api.c:6907-6975` `whd/src/whd_wifi_api.c:7110-7133`; not sent or received as a block: the wire reply whd reads is wl_icmp_echo_req_get_info_t / wl_icmp_echo_req_get_peer_info_t `whd/src/whd_wifi_api.c:6952` `whd/src/whd_wifi_api.c:6968-6971` `whd/src/include/whd_wlioctl.h:1289`, with enable and count coming from wl_icmp_echo_req_get_info_t and state, periodicity, duration, ip_ver, the address and mac_addr from the wl_icmp_echo_req_get_peer_info_t that follows in its data[] `whd/src/whd_wifi_api.c:6977-6992`; not packed (natural alignment 4: 2 bytes of padding after count, 1 trailing byte); 40 bytes (same on the x86-64 and 32-bit ARM builds compiled); host-side: filled field by field with no dtoh32 `whd/src/whd_wifi_api.c:6976-6992`; `whd/inc/whd_types.h:1572-1584`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 1 | enable | uint8_t | source comment: offload enable `whd/inc/whd_types.h:1573` |
| 1 | 1 | count | uint8_t | source comment: peer count `whd/inc/whd_types.h:1574` |
| 2 | 2 | (pad) | padding | implicit alignment padding, not declared in the source `whd/inc/whd_types.h:1574-1575` |
| 4 | 4 | state | uint32_t | source comment: state of the peer `whd/inc/whd_types.h:1575` |
| 8 | 4 | periodicity | uint32_t | seconds `whd/inc/whd_types.h:1576` |
| 12 | 4 | duration | uint32_t | seconds `whd/inc/whd_types.h:1577` |
| 16 | 1 | ip_ver | uint8_t | IPv4 = 1, IPv6 = 2 per the source comment `whd/inc/whd_types.h:1578` |
| 17 | 16 | u | union { uint8_t ipv4[4]; uint8_t ipv6[16]; } | IPV4_ADDR_LEN 4, IPV6_ADDR_LEN 16 `whd/inc/whd_types.h:103-108` |
| 33 | 6 | mac_addr | uint8_t[ETHER_ADDR_LEN] | ETHER_ADDR_LEN = 6 `whd/inc/whd_types.h:100-102` |
| 39 | 1 | (pad) | padding | trailing alignment padding counted by sizeof, not declared in the source `whd/inc/whd_types.h:1583-1584` |

Size check: compiled

### `whd_icmp_echo_req_event_data_t` (whd)
Host callback record built from the wire event record `wl_icmp_echo_req_event_t` of event WLC_E_ICMP_ECHO_REQ; not sent or received as a block: whd builds it in whd_wifi_icmp_echo_req_events_handler only when the event record's version equals WL_ICMP_ECHO_REQ_EVENT_VER, and passes it to the application's ICMP echo callback `whd/src/whd_wifi_api.c:7146-7178`; not packed (natural alignment 4, 3 trailing padding bytes); 28 bytes on every build compiled (host-dependent because of the enum member, and these sources do not fix the compiler or enum flag of a real embedded build); host-side only, so none of the build differences reaches the wire: reason and echo_req_cnt copied from the event record with no dtoh32 `whd/src/whd_wifi_api.c:7162-7163`; `whd/inc/whd_types.h:1594-1602`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | reason | IcmpEchoReq_event_reason_e | enum SUCCESS 0, TIMEOUT 1, DISASSOC 2; from wl_event_data->reason `whd/inc/whd_types.h:1587-1591` `whd/src/whd_wifi_api.c:7162` |
| 4 | 4 | echo_req_cnt | uint32_t | from wl_event_data->echo_req_cnt `whd/src/whd_wifi_api.c:7163` |
| 8 | 1 | ip_ver | uint8_t | from wl_event_data->ip_ver `whd/src/whd_wifi_api.c:7164` |
| 9 | 16 | u | union { uint8_t ipv4[4]; uint8_t ipv6[16]; } | from wl_event_data->u `whd/src/whd_wifi_api.c:7165-7173` |
| 25 | 3 | (pad) | padding | trailing alignment padding counted by sizeof, not declared in the source `whd/inc/whd_types.h:1598-1602` |

Size check: compiled
Differences: between builds (compiled): the table is the clang arm-none-eabi layout (sizeof 28, alignment 4); gcc x86-64, clang x86-64 and clang arm-none-eabi -fno-short-enums give the same. With gcc x86-64 -fshort-enums, and with a non-LLVM ARM build emulated with clang arm-none-eabi -U__llvm__ and -fshort-enums, reason is 1 byte but echo_req_cnt stays at offset 4, so sizeof is 28 on every build compiled. `whd/inc/whd_types.h:1594-1602`
