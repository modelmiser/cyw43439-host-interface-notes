# Wire records: linux

Field-by-field layouts of the records linux exchanges with the firmware.

### `brcmf_fil_p2p_if_le` (linux)
Payload of the named variables (iovar) "p2p_ifadd" and "p2p_ifupd"; not packed; 10 bytes; little-endian. `linux/brcmfmac/fwil_types.h:217-221` `linux/brcmfmac/p2p.c:2128-2141` `linux/brcmfmac/p2p.c:2074-2104`

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 6 | addr | u8[6] | interface address. Declared `[ETH_ALEN]`; ETH_ALEN = 6 is (recalled, not in these sources). For "p2p_ifdel" and "p2p_ifdis" linux sends only this 6-byte address, not the record `linux/brcmfmac/p2p.c:2136` `linux/brcmfmac/fwil_types.h:218` `linux/brcmfmac/p2p.c:2163` `linux/brcmfmac/p2p.c:2153` |
| 6 | 2 | type | __le16 | value from enum brcmf_fil_p2p_if_types: CLIENT 0, GO 1, DYNBCN_GO 2, DEV 3 `linux/brcmfmac/fwil_types.h:204-209` `linux/brcmfmac/p2p.c:2137` |
| 8 | 2 | chspec | __le16 | chanspec `linux/brcmfmac/p2p.c:2138` |

Size check: compiled

### `brcmf_fil_chan_info_le` (linux)
Three channel numbers, defined but with no use site found in linux (linux sends command BRCMF_C_GET_CHANNEL but reads a single __le32 into `hw_ch`, not this record; that this record is the full reply to that command is (recalled, not in these sources)); not packed; 12 bytes; little-endian. `linux/brcmfmac/fwil_types.h:223-227` `linux/brcmfmac/cfg80211.c:5746-5748` `linux/brcmfmac/cfg80211.c:5684`

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | hw_channel | __le32 | `linux/brcmfmac/fwil_types.h:224` |
| 4 | 4 | target_channel | __le32 | `linux/brcmfmac/fwil_types.h:225` |
| 8 | 4 | scan_channel | __le32 | `linux/brcmfmac/fwil_types.h:226` |

Size check: compiled

### `brcmf_fil_action_frame_le` (linux)
Action frame body, embedded in `brcmf_fil_af_params_le` for the named variable "actframe" (bsscfg form) and read back by linux in brcmf_p2p_send_action_frame; not packed; 1812 bytes, always sent whole whatever `len` is because the enclosing record is sent with `sizeof(*af_params)`; little-endian. `linux/brcmfmac/fwil_types.h:229-234` `linux/brcmfmac/p2p.c:1584-1585` `linux/brcmfmac/p2p.c:1744-1762`

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 6 | da | u8[6] | destination address, copied from the management frame. Declared `[ETH_ALEN]`; ETH_ALEN = 6 is (recalled, not in these sources) `linux/brcmfmac/cfg80211.c:5736` `linux/brcmfmac/fwil_types.h:230` |
| 6 | 2 | len | __le16 | frame length without the 802.11 management header `linux/brcmfmac/cfg80211.c:5738-5739` |
| 8 | 4 | packet_id | __le32 | linux writes the caller's cookie `linux/brcmfmac/fwil_types.h:232` `linux/brcmfmac/cfg80211.c:5734` |
| 12 | 1800 | data | u8[1800] | fixed array, BRCMF_FIL_ACTION_FRAME_SIZE = 1800; linux copies `len` bytes of frame body into it `linux/brcmfmac/fwil_types.h:13` `linux/brcmfmac/fwil_types.h:233` `linux/brcmfmac/cfg80211.c:5758-5759` |

Size check: compiled

### `brcmf_fil_af_params_le` (linux)
Payload of the named variable "actframe" (bsscfg form), filled by the mgmt-tx path and passed to brcmf_p2p_send_action_frame; not packed; 1828 bytes, sent with length `sizeof(*af_params)`; little-endian. `linux/brcmfmac/fwil_types.h:236-242` `linux/brcmfmac/p2p.c:1573-1585` `linux/brcmfmac/cfg80211.c:5765`

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | channel | __le32 | set by the mgmt-tx path `linux/brcmfmac/cfg80211.c:5755` |
| 4 | 4 | dwell_time | __le32 | set from the caller's wait time `linux/brcmfmac/cfg80211.c:5757` |
| 8 | 6 | bssid | u8[6] | copied from the management frame. Declared `[ETH_ALEN]`; ETH_ALEN = 6 is (recalled, not in these sources) `linux/brcmfmac/cfg80211.c:5737` `linux/brcmfmac/fwil_types.h:239` |
| 14 | 2 | pad | u8[2] | (pad) explicit, declared in the source `linux/brcmfmac/fwil_types.h:240` |
| 16 | 1812 | action_frame | struct brcmf_fil_action_frame_le | see `brcmf_fil_action_frame_le` `linux/brcmfmac/fwil_types.h:241` |

Size check: compiled

### `brcmf_fil_bss_enable_le` (linux)
Payload of the named variable "bss", which linux uses to bring an AP bss up or down; not packed; 8 bytes; little-endian. `linux/brcmfmac/fwil_types.h:244-247` `linux/brcmfmac/cfg80211.c:5479-5482`

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | bsscfgidx | __le32 | linux writes the interface's bsscfg index `linux/brcmfmac/cfg80211.c:5479` |
| 4 | 4 | enable | __le32 | linux sends 1 for up; the down path sends the same record with 0 `linux/brcmfmac/cfg80211.c:5480` `linux/brcmfmac/cfg80211.c:5564-5567` |

Size check: compiled

### `brcmf_fil_bwcap_le` (linux)
Payload of the named variable "bw_cap" (set); not packed; 8 bytes; little-endian. `linux/brcmfmac/fwil_types.h:249-252` `linux/brcmfmac/cfg80211.c:7364-7367`

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | band | __le32 | linux sends WLC_BAND_2G at this call site `linux/brcmfmac/cfg80211.c:7364` |
| 4 | 4 | bw_cap | __le32 | linux sends WLC_BW_CAP_40MHZ at this call site `linux/brcmfmac/cfg80211.c:7365` |

Size check: compiled

### `brcmf_tdls_iovar_le` (linux)
Payload of the named variable "tdls_endpoint", described by the header as the common structure for the tdls variables; not packed; 16 bytes, of which 3 are implicit padding that goes out as 0 because linux zeroes the whole record before filling it; little-endian. `linux/brcmfmac/fwil_types.h:262-267` `linux/brcmfmac/fwil_types.h:254-261` `linux/brcmfmac/cfg80211.c:5991-6005` `linux/brcmfmac/cfg80211.c:5999`

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 6 | ea | u8[6] | peer station address. Declared `[ETH_ALEN]`; ETH_ALEN = 6 is (recalled, not in these sources) `linux/brcmfmac/fwil_types.h:263` `linux/brcmfmac/cfg80211.c:6001-6002` |
| 6 | 1 | mode | u8 | meaning depends on the variable. For "tdls_endpoint" linux sends a brcmf_tdls_manual_ep_ops value: CREATE 1, DELETE 3, DISCOVERY 6 `linux/brcmfmac/fwil_types.h:264` `linux/brcmfmac/fwil_types.h:269-273` `linux/brcmfmac/cfg80211.c:5963-5975` `linux/brcmfmac/cfg80211.c:6000` |
| 7 | 1 | (pad) | - | implicit alignment padding from the compiler; the struct is not packed `linux/brcmfmac/fwil_types.h:262-267` |
| 8 | 2 | chanspec | __le16 | `linux/brcmfmac/fwil_types.h:265` |
| 10 | 2 | (pad) | - | implicit alignment padding from the compiler `linux/brcmfmac/fwil_types.h:262-267` |
| 12 | 4 | pad | __le32 | (pad) explicit field named pad, marked for future use `linux/brcmfmac/fwil_types.h:266` |

Size check: compiled

### `brcmf_pkt_filter_pattern_le` (linux)
Pattern definition inside `brcmf_pkt_filter_le`, which a header comment gives as the parameter of the variable `pkt_filter_add`; no use site found in linux, where the string "pkt_filter" occurs only in these definitions and their comments, so the binding to that variable rests on the header comment alone; not packed; variable, 8 fixed bytes plus a mask and pattern tail, `sizeof` 12 because the tail is declared `[1]` and the struct is padded to a multiple of 4; little-endian. `linux/brcmfmac/fwil_types.h:279-292` `linux/brcmfmac/fwil_types.h:294` `linux/brcmfmac/fwil_types.h:300`

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | offset | __le32 | offset in the received packet where matching starts; 0 is the first byte of the ethernet header `linux/brcmfmac/fwil_types.h:280-284` |
| 4 | 4 | size_bytes | __le32 | pattern size; the mask has the same size `linux/brcmfmac/fwil_types.h:285-286` |
| 8 | variable | mask_and_pattern | u8[1] | flexible tail declared as a 1-element array: mask (size_bytes) then pattern (size_bytes) `linux/brcmfmac/fwil_types.h:287-291` |
| 9 | 3 | (pad) | - | trailing alignment padding, counted in `sizeof` only; the variable tail overlays it on the wire `linux/brcmfmac/fwil_types.h:279-292` |

Size check: compiled

### `brcmf_pkt_filter_le` (linux)
Parameter of the variable `pkt_filter_add` according to the header comment, used to install packet filters; no use site found in linux, where the string "pkt_filter" occurs only in these definitions and their comments; not packed; variable, 20 fixed bytes plus a mask and pattern tail, `sizeof` 24; little-endian. `linux/brcmfmac/fwil_types.h:295-302` `linux/brcmfmac/fwil_types.h:294`

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | id | __le32 | filter id chosen by the caller `linux/brcmfmac/fwil_types.h:296` |
| 4 | 4 | type | __le32 | the comment names WL_PKT_FILTER_TYPE_xxx; those constants are not defined in linux `linux/brcmfmac/fwil_types.h:297` |
| 8 | 4 | negate_match | __le32 | negates the match result `linux/brcmfmac/fwil_types.h:298` |
| 12 | 4 | u.pattern.offset | __le32 | `u` is a single-member union holding a `brcmf_pkt_filter_pattern_le`, 12 bytes at offset 12 `linux/brcmfmac/fwil_types.h:299-301` `linux/brcmfmac/fwil_types.h:284` |
| 16 | 4 | u.pattern.size_bytes | __le32 | `linux/brcmfmac/fwil_types.h:286` |
| 20 | variable | u.pattern.mask_and_pattern | u8[1] | mask then pattern, size_bytes each `linux/brcmfmac/fwil_types.h:287-291` |
| 21 | 3 | (pad) | - | trailing alignment padding of the inner record, counted in `sizeof` only (inferred from the inner record's layout and `sizeof` 24) `linux/brcmfmac/fwil_types.h:279-292` |

Size check: compiled

### `brcmf_pkt_filter_enable_le` (linux)
Parameter of the variable `pkt_filter_enable` according to the header comment; no use site found in linux, where the string "pkt_filter" occurs only in these definitions and their comments; not packed; 8 bytes; little-endian. `linux/brcmfmac/fwil_types.h:305-308` `linux/brcmfmac/fwil_types.h:304`

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | id | __le32 | filter id `linux/brcmfmac/fwil_types.h:306` |
| 4 | 4 | enable | __le32 | enable/disable flag `linux/brcmfmac/fwil_types.h:307` |

Size check: compiled

### `brcmf_bss_info_le` (linux)
One BSS description, the reply to command BRCMF_C_GET_BSS_INFO (136) and the element type of scan and escan results; not packed, with six runs of implicit padding (offsets 51, 77, 82-83, 89-91, 118-119, 126-127); variable, 128 fixed bytes (`sizeof` 128) then information elements, the record's length being its `length` field; little-endian. `linux/brcmfmac/fwil_types.h:314-348` `linux/brcmfmac/fwil.h:65` `linux/brcmfmac/fwil_types.h:457` `linux/brcmfmac/fwil_types.h:470-476`

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | version | __le32 | BRCMF_BSS_INFO_VERSION = 109. linux checks the `version` of the enclosing `brcmf_scan_results` list against this constant `linux/brcmfmac/fwil_types.h:21` `linux/brcmfmac/fwil_types.h:315` `linux/brcmfmac/cfg80211.c:3474` |
| 4 | 4 | length | __le32 | byte length of this record, counted from `version` and including the IEs. linux walks a list of records by adding `length` to the current record's address `linux/brcmfmac/fwil_types.h:316-318` `linux/brcmfmac/cfg80211.c:3455-3462` |
| 8 | 6 | BSSID | u8[6] | declared `[ETH_ALEN]`; ETH_ALEN = 6 is (recalled, not in these sources) `linux/brcmfmac/fwil_types.h:319` |
| 14 | 2 | beacon_period | __le16 | units Kusec `linux/brcmfmac/fwil_types.h:320` |
| 16 | 2 | capability | __le16 | capability information `linux/brcmfmac/fwil_types.h:321` |
| 18 | 1 | SSID_len | u8 | `linux/brcmfmac/fwil_types.h:322` |
| 19 | 32 | SSID | u8[32] | `linux/brcmfmac/fwil_types.h:323` |
| 51 | 1 | (pad) | - | implicit alignment padding from the compiler `linux/brcmfmac/fwil_types.h:323-325` |
| 52 | 4 | rateset.count | __le32 | number of rates. `rateset` is an anonymous inner struct, 20 bytes at 52 `linux/brcmfmac/fwil_types.h:324-327` |
| 56 | 16 | rateset.rates | u8[16] | 500 kbps units, high bit set if basic `linux/brcmfmac/fwil_types.h:326` |
| 72 | 2 | chanspec | __le16 | `linux/brcmfmac/fwil_types.h:328` |
| 74 | 2 | atim_window | __le16 | units Kusec `linux/brcmfmac/fwil_types.h:329` |
| 76 | 1 | dtim_period | u8 | `linux/brcmfmac/fwil_types.h:330` |
| 77 | 1 | (pad) | - | implicit alignment padding from the compiler `linux/brcmfmac/fwil_types.h:330-331` |
| 78 | 2 | RSSI | __le16 | dBm. Declared __le16; linux reads it as signed, `(s16)le16_to_cpu(bi->RSSI)` `linux/brcmfmac/fwil_types.h:331` `linux/brcmfmac/cfg80211.c:3432` `linux/brcmfmac/cfg80211.c:3543` |
| 80 | 1 | phy_noise | s8 | dBm `linux/brcmfmac/fwil_types.h:332` |
| 81 | 1 | n_cap | u8 | 802.11n capable `linux/brcmfmac/fwil_types.h:334` |
| 82 | 2 | (pad) | - | implicit alignment padding from the compiler `linux/brcmfmac/fwil_types.h:334-336` |
| 84 | 4 | nbss_cap | __le32 | 802.11n BSS capabilities `linux/brcmfmac/fwil_types.h:335-336` |
| 88 | 1 | ctl_ch | u8 | 802.11n control channel number `linux/brcmfmac/fwil_types.h:337` |
| 89 | 3 | (pad) | - | implicit alignment padding from the compiler `linux/brcmfmac/fwil_types.h:337-338` |
| 92 | 4 | reserved32 | __le32[1] | reserved `linux/brcmfmac/fwil_types.h:338` |
| 96 | 1 | flags | u8 | linux tests bit BRCMF_BSS_RSSI_ON_CHANNEL 0x0004 `linux/brcmfmac/fwil_types.h:339` `linux/brcmfmac/fwil_types.h:22` `linux/brcmfmac/cfg80211.c:3649-3650` |
| 97 | 3 | reserved | u8[3] | reserved `linux/brcmfmac/fwil_types.h:340` |
| 100 | 16 | basic_mcs | u8[16] | BRCMF_MCSSET_LEN = 16 `linux/brcmfmac/fwil_types.h:341` `linux/brcmfmac/fwil_types.h:163` |
| 116 | 2 | ie_offset | __le16 | offset of the IEs from the start of the record; linux uses `(u8 *)bi + ie_offset`. The header says consumers must use `ie_offset` and `length`, not `sizeof`, to reach the IEs and the next record `linux/brcmfmac/fwil_types.h:343` `linux/brcmfmac/cfg80211.c:3430` `linux/brcmfmac/fwil_types.h:310-313` |
| 118 | 2 | (pad) | - | implicit alignment padding from the compiler `linux/brcmfmac/fwil_types.h:343-344` |
| 120 | 4 | ie_length | __le32 | byte length of the IEs `linux/brcmfmac/fwil_types.h:344` `linux/brcmfmac/cfg80211.c:3431` |
| 124 | 2 | SNR | __le16 | average SNR `linux/brcmfmac/fwil_types.h:345` |
| 126 | 2 | (pad) | - | trailing alignment padding `linux/brcmfmac/fwil_types.h:345-348` |
| ie_offset | variable | (information elements) | u8[] | ie_length bytes. Not a declared member; the header comment says variable-length IEs follow `linux/brcmfmac/fwil_types.h:347` |

Size check: compiled

Differences: for command BRCMF_C_GET_BSS_INFO the record is not at the start of the buffer: linux writes a 4-byte __le32 buffer length at offset 0 of the request buffer and reads the record at offset 4 of the reply. `linux/brcmfmac/cfg80211.c:3098-3111` `linux/brcmfmac/cfg80211.c:3516-3525` `linux/brcmfmac/p2p.c:2044-2047` `linux/brcmfmac/cfg80211.c:6622-6629`
Differences: the buffer for that command is WL_BSS_INFO_MAX = 2048 bytes at those call sites; one further call site uses WL_EXTRA_BUF_MAX = 2048 with the same 4-byte prefix. `linux/brcmfmac/cfg80211.h:22` `linux/brcmfmac/cfg80211.h:24` `linux/brcmfmac/cfg80211.c:3583-3590`

### `brcm_rateset_le` (linux)
Rate set, defined but with no use site found in linux (linux defines BRCM_GET_CURR_RATESET 114 and BRCMF_C_GET_CURR_RATESET 114, but nothing in linux uses either or ties that command to this record); not packed; 20 bytes; little-endian. `linux/brcmfmac/fwil_types.h:350-355` `linux/include/defs.h:47` `linux/brcmfmac/fwil.h:56`

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | count | __le32 | number of rates in the set `linux/brcmfmac/fwil_types.h:351-352` |
| 4 | 16 | rates | u8[16] | BRCMF_MAXRATES_IN_SET = 16; 500 kbps units, high bit set if basic `linux/brcmfmac/fwil_types.h:353-354` `linux/brcmfmac/fwil_types.h:76` |

Size check: compiled

Differences: same layout as the anonymous `rateset` member of `brcmf_bss_info_le` (linux). `linux/brcmfmac/fwil_types.h:324-327`

### `brcmf_ssid_le` (linux)
SSID with a 32-bit length, payload of the named variable "ssid" (bsscfg form) and a member of the join, scan and pno records; not packed; 36 bytes; little-endian. `linux/brcmfmac/fwil_types.h:357-360` `linux/brcmfmac/cfg80211.c:5473-5474`

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | SSID_len | __le32 | `linux/brcmfmac/fwil_types.h:358` |
| 4 | 32 | SSID | unsigned char[32] | array length is IEEE80211_MAX_SSID_LEN = 32 `linux/brcmfmac/fwil_types.h:359` `linux-headers/ieee80211.h:227` |

Size check: compiled

Differences: as a member it is the first field of `brcmf_join_params`, which linux sends with command BRCMF_C_SET_SSID, and a field of `brcmf_ext_join_params_le`, `brcmf_scan_params_le`, `brcmf_scan_params_v2_le` and `brcmf_pno_net_param_le`. `linux/brcmfmac/fwil_types.h:509-512` `linux/brcmfmac/cfg80211.c:1921` `linux/brcmfmac/fwil_types.h:530-531` `linux/brcmfmac/fwil_types.h:369` `linux/brcmfmac/fwil_types.h:412` `linux/brcmfmac/fwil_types.h:1037-1038`
Differences: linux also appends one such record per requested SSID after the channel list of the scan parameters. `linux/brcmfmac/cfg80211.c:1157-1171`

### `brcmf_ssid8_le` (linux)
SSID with an 8-bit length, called an alternate SSID structure by the header and a member of `brcmf_pmksa_v2` and `brcmf_pmksa_v3`; not packed (alignment 1, no padding); 33 bytes, which depends on IEEE80211_MAX_SSID_LEN = 32; no byte order (all u8). `linux/brcmfmac/fwil_types.h:363-366` `linux/brcmfmac/fwil_types.h:362` `linux/brcmfmac/fwil_types.h:909-915` `linux/brcmfmac/fwil_types.h:931-939`

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 1 | SSID_len | u8 | `linux/brcmfmac/fwil_types.h:364` |
| 1 | 32 | SSID | unsigned char[32] | array length is IEEE80211_MAX_SSID_LEN = 32 `linux/brcmfmac/fwil_types.h:365` `linux-headers/ieee80211.h:227` |

Size check: compiled

### `brcmf_scan_params_le` (linux)
Version 1 scan parameters: payload of command BRCMF_C_SCAN (50), sent on the scan-abort path with length `sizeof` = 68 when BRCMF_FEAT_SCAN_V2 is off; the `params_le` arm of the "escan" named variable payload, built by converting from the v2 record when BRCMF_FEAT_SCAN_V2 is off; and part of the "p2p_scan" named variable payload (bsscfg form); not packed; variable, 64 fixed bytes (BRCMF_SCAN_PARAMS_FIXED_SIZE, equal to the compiled offset of `channel_list`) plus a channel and ssid tail, `sizeof` 68; little-endian. `linux/brcmfmac/fwil_types.h:368-407` `linux/brcmfmac/fwil_types.h:50` `linux/brcmfmac/fwil.h:40` `linux/brcmfmac/fwil_types.h:460-468` `linux/brcmfmac/cfg80211.c:1215-1221` `linux/brcmfmac/cfg80211.c:1472-1485` `linux/brcmfmac/cfg80211.c:1491` `linux/brcmfmac/p2p.c:134-139` `linux/brcmfmac/p2p.c:697` `linux/brcmfmac/p2p.c:780`

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 36 | ssid_le | struct brcmf_ssid_le | see `brcmf_ssid_le`; the header comment says it is ignored when the ssid count in `channel_num` is not 0 `linux/brcmfmac/fwil_types.h:369` `linux/brcmfmac/fwil_types.h:397-399` |
| 36 | 6 | bssid | u8[6] | comment gives broadcast as the default. Declared `[ETH_ALEN]`; ETH_ALEN = 6 is (recalled, not in these sources) `linux/brcmfmac/fwil_types.h:370` |
| 42 | 1 | bss_type | s8 | DOT11_BSSTYPE_ANY = 2 `linux/brcmfmac/fwil_types.h:371-373` `linux/brcmfmac/fwil_types.h:72` |
| 43 | 1 | scan_type | u8 | BRCMF_SCANTYPE_DEFAULT 255 (0xFF), ACTIVE 0, PASSIVE 1. The field comment says "flags, 0 use default" while the constants make 0 ACTIVE and 0xFF DEFAULT; the source does not reconcile the two `linux/brcmfmac/fwil_types.h:374` `linux/brcmfmac/fwil_types.h:61-63` |
| 44 | 4 | nprobes | __le32 | probes per channel; -1 = default `linux/brcmfmac/fwil_types.h:375` |
| 48 | 4 | active_time | __le32 | active dwell time per channel; -1 = default `linux/brcmfmac/fwil_types.h:376-378` |
| 52 | 4 | passive_time | __le32 | passive dwell time per channel; -1 = default `linux/brcmfmac/fwil_types.h:379-381` |
| 56 | 4 | home_time | __le32 | home channel dwell time between channel scans; -1 = default `linux/brcmfmac/fwil_types.h:382-384` |
| 60 | 4 | channel_num | __le32 | low 16 bits: channel count (0 = all channels); high 16 bits: ssid count. Mask 0x0000ffff, shift 16 `linux/brcmfmac/fwil_types.h:385-400` `linux/brcmfmac/fwil_types.h:57-58` |
| 64 | variable | channel_list | __le16[] | flexible array of chanspecs, in a union with a 2-byte `__le16 padding` member that reserves one entry. After the list, aligned to 4 bytes, comes an array of `brcmf_ssid_le`, so an odd channel count means a 2-byte pad between the end of `channel_list` and the first ssid `linux/brcmfmac/fwil_types.h:401-406` `linux/brcmfmac/fwil_types.h:391-395` |
| 66 | 2 | (pad) | - | trailing alignment padding, counted in `sizeof` only `linux/brcmfmac/fwil_types.h:401-407` |

Size check: compiled

### `brcmf_scan_params_v2_le` (linux)
Version 2 scan parameters, used when BRCMF_FEAT_SCAN_V2 is enabled as the `params_v2_le` arm of `brcmf_escan_params_le` (payload of the "escan" named variable) and sent alone with command BRCMF_C_SCAN (50), length `sizeof` = 76, to abort a scan; not packed; variable, 72 fixed bytes (BRCMF_SCAN_PARAMS_V2_FIXED_SIZE) plus a channel and ssid tail, `sizeof` 76; little-endian. `linux/brcmfmac/fwil_types.h:409-451` `linux/brcmfmac/fwil_types.h:51` `linux/brcmfmac/fwil_types.h:460-468` `linux/brcmfmac/fwil.h:40` `linux/brcmfmac/cfg80211.c:1208-1214` `linux/brcmfmac/cfg80211.c:1468-1472` `linux/brcmfmac/cfg80211.c:1491`

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 2 | version | __le16 | structure version; linux sets BRCMF_SCAN_PARAMS_VERSION_V2 = 2 `linux/brcmfmac/fwil_types.h:410` `linux/brcmfmac/fwil_types.h:54` `linux/brcmfmac/cfg80211.c:1113` |
| 2 | 2 | length | __le16 | structure length; linux sets 72 + the channel list rounded up to 4 + 36 per ssid, and 74 in the abort form `linux/brcmfmac/fwil_types.h:411` `linux/brcmfmac/cfg80211.c:1111` `linux/brcmfmac/cfg80211.c:1139` `linux/brcmfmac/cfg80211.c:1157` `linux/brcmfmac/cfg80211.c:1177` `linux/brcmfmac/cfg80211.c:1125-1128` |
| 4 | 36 | ssid_le | struct brcmf_ssid_le | see `brcmf_ssid_le` (__le32 SSID_len + 32 bytes SSID); linux zeroes it `linux/brcmfmac/fwil_types.h:412` `linux/brcmfmac/fwil_types.h:357-360` `linux/brcmfmac/cfg80211.c:1121` |
| 40 | 6 | bssid | u8[6] | comment gives broadcast as the default; linux fills in the broadcast address. Declared `[ETH_ALEN]`; ETH_ALEN = 6 is (recalled, not in these sources), and the fixed size 72 implies it (inferred) `linux/brcmfmac/fwil_types.h:413` `linux/brcmfmac/cfg80211.c:1109` `linux/brcmfmac/fwil_types.h:51` |
| 46 | 1 | bss_type | s8 | linux sets DOT11_BSSTYPE_ANY (2) `linux/brcmfmac/fwil_types.h:414-416` `linux/brcmfmac/fwil_types.h:72` `linux/brcmfmac/cfg80211.c:1114` |
| 47 | 1 | pad | u8 | (pad) explicit, declared in the source `linux/brcmfmac/fwil_types.h:417` |
| 48 | 4 | scan_type | __le32 | comment: flags, 0 = default. linux sets BRCMF_SCANTYPE_ACTIVE (0), or BRCMF_SCANTYPE_PASSIVE (1) for a scan request with no ssids. 32 bits here, u8 in v1; linux truncates it to u8 when converting to v1 `linux/brcmfmac/fwil_types.h:418` `linux/brcmfmac/fwil_types.h:62-63` `linux/brcmfmac/cfg80211.c:1115` `linux/brcmfmac/cfg80211.c:1173-1175` `linux/brcmfmac/cfg80211.c:1075` |
| 52 | 4 | nprobes | __le32 | number of probes per channel; -1 = default, which linux sets `linux/brcmfmac/fwil_types.h:419` `linux/brcmfmac/cfg80211.c:1117` |
| 56 | 4 | active_time | __le32 | active dwell time per channel; -1 = default, which linux sets `linux/brcmfmac/fwil_types.h:420-422` `linux/brcmfmac/cfg80211.c:1118` |
| 60 | 4 | passive_time | __le32 | passive dwell time per channel; -1 = default, which linux sets `linux/brcmfmac/fwil_types.h:423-425` `linux/brcmfmac/cfg80211.c:1119` |
| 64 | 4 | home_time | __le32 | home channel dwell time between channel scans; -1 = default, which linux sets `linux/brcmfmac/fwil_types.h:426-428` `linux/brcmfmac/cfg80211.c:1120` |
| 68 | 4 | channel_num | __le32 | same split as v1: low 16 bits channel count (0 = all channels), high 16 bits ssid count; mask 0x0000ffff, shift 16. linux sets 1 in the abort form `linux/brcmfmac/fwil_types.h:429-444` `linux/brcmfmac/fwil_types.h:57-58` `linux/brcmfmac/cfg80211.c:1179-1181` `linux/brcmfmac/cfg80211.c:1126` |
| 72 | variable | channel_list | __le16[] | flexible array of chanspecs, in a union with a 2-byte `__le16 padding` member that reserves one entry for the abort form. After the list, aligned to 4 bytes, comes an array of `brcmf_ssid_le`; linux places it at the offset of `channel_list` plus 2 bytes per channel, rounded up to 4. Abort form: `channel_list[0]` = 0xFFFF `linux/brcmfmac/fwil_types.h:445-450` `linux/brcmfmac/fwil_types.h:435-439` `linux/brcmfmac/cfg80211.c:1154-1156` `linux/brcmfmac/cfg80211.c:1127` |
| 74 | 2 | (pad) | - | trailing alignment padding, counted in `sizeof` only `linux/brcmfmac/fwil_types.h:445-451` |

Size check: compiled

Differences: against `brcmf_scan_params_le` (linux) this record adds `version` and `length` (4 bytes) at the front, adds an explicit `pad` byte after `bss_type`, and widens `scan_type` from u8 to __le32; fixed part 72 bytes against 64. linux always builds the scan parameters in this form first; when BRCMF_FEAT_SCAN_V2 is off it converts them to v1 field by field, then copies the channel and ssid tail, for both the "escan" payload and the abort command. `linux/brcmfmac/cfg80211.c:1062-1094` `linux/brcmfmac/cfg80211.c:1468-1485` `linux/brcmfmac/cfg80211.c:1215-1221`

### `brcmf_scan_results` (linux)
Host-side accumulation buffer for escan results, a 65000-byte (BRCMF_ESCAN_BUF_SIZE) allocation that no use site sends or receives as a whole; not packed; variable, 12 fixed bytes plus a tail of `brcmf_bss_info_le` records; header fields in host order (plain u32), the records inside little-endian. `linux/brcmfmac/fwil_types.h:453-458` `linux/brcmfmac/cfg80211.c:1519-1522` `linux/brcmfmac/cfg80211.c:3749-3768` `linux/brcmfmac/cfg80211.h:48` `linux/brcmfmac/cfg80211.c:7062` `linux/brcmfmac/fwil_types.h:314` `linux/brcmfmac/cfg80211.c:3461`

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `buflen` | `u32` | linux initialises it to WL_ESCAN_RESULTS_FIXED_SIZE, so the 12-byte header has the same size as the fixed part of `brcmf_escan_result_le`; linux appends each partial result's bss_info at escan_buf[buflen] and updates version, buflen and count in host order `linux/brcmfmac/fwil_types.h:454` `linux/brcmfmac/cfg80211.c:1522` `linux/brcmfmac/fwil_types.h:478-479` `linux/brcmfmac/cfg80211.c:3764-3768` |
| 4 | 4 | `version` | `u32` | compared with BRCMF_BSS_INFO_VERSION (109) when count is non-zero `linux/brcmfmac/fwil_types.h:455` `linux/brcmfmac/cfg80211.c:3472-3474` `linux/brcmfmac/cfg80211.c:3473-3474` `linux/brcmfmac/fwil_types.h:21` |
| 8 | 4 | `count` | `u32` | number of bss_info records `linux/brcmfmac/fwil_types.h:456` |
| 12 | variable | `bss_info_le` | `struct brcmf_bss_info_le[]` | flexible array; records are variable length, and linux walks them by adding each record's own length field `linux/brcmfmac/fwil_types.h:457` `linux/brcmfmac/cfg80211.c:3456-3461` |

Size check: compiled

### `brcmf_escan_params_le` (linux)
Payload of the "escan" named variable (iovar) (set), also embedded in `brcmf_p2p_scan_le` for the "p2p_scan" named variable set with the bsscfg prefix; not packed; variable, 8 fixed bytes plus version 1 or version 2 scan parameters and their channel and ssid tail, `sizeof` 84, sent length computed by linux (not `sizeof`) as 8 + 72 (64 for v1) + 4 * ((n_channels + 1) / 2) + 36 * n_ssids; little-endian. `linux/brcmfmac/fwil_types.h:460-468` `linux/brcmfmac/cfg80211.c:1447-1491` `linux/brcmfmac/p2p.c:132-139` `linux/brcmfmac/p2p.c:776-780` `linux/brcmfmac/cfg80211.c:1447-1459` `linux/brcmfmac/cfg80211.c:1475-1476`

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `version` | `__le32` | BRCMF_ESCAN_REQ_VERSION (1) or BRCMF_ESCAN_REQ_VERSION_V2 (2); linux sets 2 with the v2 alternative, or 1 with the v1 alternative when feature SCAN_V2 is absent; the p2p_scan path uses 1 with the v1 alternative (params_le) `linux/brcmfmac/fwil_types.h:461` `linux/brcmfmac/fwil_types.h:73-74` `linux/brcmfmac/cfg80211.c:1470-1483` `linux/brcmfmac/p2p.c:697` `linux/brcmfmac/p2p.c:776-778` |
| 4 | 2 | `action` | `__le16` | linux sets WL_ESCAN_ACTION_START (1) on both paths `linux/brcmfmac/fwil_types.h:462` `linux/brcmfmac/cfg80211.c:1488-1489` `linux/brcmfmac/p2p.c:777-778` `linux/brcmfmac/cfg80211.h:51` |
| 6 | 2 | `sync_id` | `__le16` | linux sets 0x1234 (4660) on both paths `linux/brcmfmac/fwil_types.h:463` `linux/brcmfmac/cfg80211.c:1488-1489` `linux/brcmfmac/p2p.c:777-778` |
| 8 | 76 | `params_le / params_v2_le` | `union { struct brcmf_scan_params_le; struct brcmf_scan_params_v2_le }` | union alternatives: v1 (sizeof 68, fixed part 64) or v2 (sizeof 76, fixed part 72); each ends in a flexible channel list `linux/brcmfmac/fwil_types.h:464-467` |

Size check: compiled

### `brcmf_escan_result_le` (linux)
Event data of BRCMF_E_ESCAN_RESULT (69) carrying one partial scan result; not packed; variable, 12 fixed bytes (WL_ESCAN_RESULTS_FIXED_SIZE = sizeof(record) - sizeof(bss_info) = 12 (compiled)) plus one variable-length `brcmf_bss_info_le` (128 fixed bytes, then information elements), `sizeof` the whole record 140; little-endian. `linux/brcmfmac/fwil_types.h:470-476` `linux/brcmfmac/fwil_types.h:478-479` `linux/brcmfmac/fweh.h:89` `linux/brcmfmac/cfg80211.c:3787-3788` `linux/brcmfmac/cfg80211.c:3699-3738`

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `buflen` | `__le32` | total length of this result; linux rejects event data shorter than `sizeof` (140), and buflen below 140, above the event datalen, or above 65000 `linux/brcmfmac/fwil_types.h:471` `linux/brcmfmac/cfg80211.c:3701` `linux/brcmfmac/cfg80211.c:3711-3713` `linux/brcmfmac/cfg80211.h:48` |
| 4 | 4 | `version` | `__le32` | `linux/brcmfmac/fwil_types.h:472` |
| 8 | 2 | `sync_id` | `__le16` | `linux/brcmfmac/fwil_types.h:473` |
| 10 | 2 | `bss_count` | `__le16` | linux requires 1 `linux/brcmfmac/fwil_types.h:474` `linux/brcmfmac/cfg80211.c:3718` |
| 12 | 128 | `bss_info_le` | `struct brcmf_bss_info_le` | fixed part is 128 bytes as compiled; information elements follow, real length is bss_info_le.length, which linux requires to equal buflen - 12 `linux/brcmfmac/fwil_types.h:475` `linux/brcmfmac/cfg80211.c:3733-3734` |

Size check: compiled

### `brcmf_assoc_params_le` (linux)
BSSID and chanspec list for association, the tail of `brcmf_join_params` (command BRCMF_C_SET_SSID) and of `brcmf_ext_join_params_le` ("join" named variable); not packed; variable, 12 fixed bytes plus a chanspec list, `sizeof` 16 with one entry and tail padding; little-endian. `linux/brcmfmac/fwil_types.h:481-490` `linux/brcmfmac/cfg80211.c:1880-1905` `linux/brcmfmac/cfg80211.c:2569-2598` `linux/brcmfmac/cfg80211.c:2636-2647`

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 6 | `bssid` | `u8[6]` | all zero = broadcast scan (source comment); declared `[ETH_ALEN]`; ETH_ALEN = 6 is (recalled, not in these sources) `linux/brcmfmac/fwil_types.h:483-484` |
| 6 | 2 | (pad) | - | alignment padding before __le32; from the compiled layout `linux/brcmfmac/fwil_types.h:484-487` |
| 8 | 4 | `chanspec_num` | `__le32` | 0 = all channels, else count of chanspecs `linux/brcmfmac/fwil_types.h:487` |
| 12 | 2 | `chanspec_list` | `__le16[1]` | declared [1], used as a variable-length list `linux/brcmfmac/fwil_types.h:489` |
| 14 | 2 | (pad) | - | trailing padding in sizeof; from the compiled layout `linux/brcmfmac/fwil_types.h:489-490` |

Size check: compiled

Differences: BRCMF_ASSOC_PARAMS_FIXED_SIZE = sizeof(record) - sizeof(u16) = 14 is 2 more than offsetof(chanspec_list) = 12, because `sizeof` includes the 2 tail padding bytes; the only use of that constant is the IBSS join, where linux adds it to the sent length when a BSSID is given, while the "join" named variable path uses offsetof(chanspec_list) = 12 instead. `linux/brcmfmac/cfg80211.c:102-103` `linux/brcmfmac/cfg80211.c:1883` `linux/brcmfmac/cfg80211.c:2569-2570`

### `brcmf_join_pref_params` (linux)
One entry of the "join_pref" named variable (set), which linux always sends as an array of 2 entries (`sizeof`, 8 bytes); not packed; 4 bytes; single-byte fields, no byte order. `linux/brcmfmac/fwil_types.h:492-506` `linux/brcmfmac/common.c:83-97` `linux/brcmfmac/cfg80211.c:2370-2406`

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 1 | `type` | `u8` | enum brcmf_join_pref_types `linux/brcmfmac/fwil_types.h:197` `linux/brcmfmac/fwil_types.h:502` |
| 1 | 1 | `len` | `u8` | length of bytes following, always 2 `linux/brcmfmac/fwil_types.h:503` |
| 2 | 1 | `rssi_gain` | `u8` | used when type is RSSI_DELTA `linux/brcmfmac/fwil_types.h:504` |
| 3 | 1 | `band` | `u8` | used when type is BAND or RSSI_DELTA `linux/brcmfmac/fwil_types.h:505` |

Size check: compiled

Differences: the two linux call sites fill the array differently. At init the default is entry 0 = RSSI_DELTA, len 2, rssi_gain BRCMF_JOIN_PREF_RSSI_BOOST (8), band WLC_BAND_5G, and entry 1 = RSSI, len 2, rssi_gain 0, band 0. `linux/brcmfmac/common.c:87-95` `linux/brcmfmac/common.c:32`

Differences: the connect path builds the array from the BSS selection, an optional first entry of type BAND or RSSI_DELTA and then an RSSI entry; with no first entry, entry 1 of the on-stack array is not written by this code, yet 8 bytes are still sent. `linux/brcmfmac/cfg80211.c:2370-2406`

### `brcmf_join_params` (linux)
Payload of command BRCMF_C_SET_SSID (26), used by linux for the IBSS join, the connect fallback after the "join" named variable fails, AP start and AP stop; not packed; `sizeof` 52, sent length varies by use site; little-endian. `linux/brcmfmac/fwil_types.h:508-512` `linux/brcmfmac/fwil.h:25` `linux/brcmfmac/cfg80211.c:1872-1922` `linux/brcmfmac/cfg80211.c:2630-2647` `linux/brcmfmac/cfg80211.c:5436-5441` `linux/brcmfmac/cfg80211.c:5542-5544`

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 36 | `ssid_le` | `struct brcmf_ssid_le` | __le32 SSID_len + 32 bytes SSID; 32 is IEEE80211_MAX_SSID_LEN `linux/brcmfmac/fwil_types.h:510` `linux/brcmfmac/fwil_types.h:357-360` `linux-headers/ieee80211.h:227` |
| 36 | 16 | `params_le` | `struct brcmf_assoc_params_le` | bssid at 36, 2 pad bytes at 42, chanspec_num at 44, chanspec_list[0] at 48, 2 tail pad bytes at 50; the bssid size rests on ETH_ALEN = 6 (recalled, not in these sources) `linux/brcmfmac/fwil_types.h:511` |

Size check: compiled

Differences: AP start sends `sizeof` (52) and AP stop sends an all-zero record of `sizeof` (52). `linux/brcmfmac/cfg80211.c:5436-5441` `linux/brcmfmac/cfg80211.c:5542-5544`

Differences: the connect fallback sends 36 bytes (ssid_le only, so the bssid written just before is not included), or 52 when a channel is set. `linux/brcmfmac/cfg80211.c:2631` `linux/brcmfmac/cfg80211.c:2636-2647`

Differences: the IBSS join starts at 36, adds 14 (BRCMF_ASSOC_PARAMS_FIXED_SIZE) when a BSSID is given and 16 (sizeof params_le) when the channel is fixed; with both the length is 66, larger than `sizeof` (52) (computed from the arithmetic, not observed running). `linux/brcmfmac/cfg80211.c:1878` `linux/brcmfmac/cfg80211.c:1883` `linux/brcmfmac/cfg80211.c:1904` `linux/brcmfmac/cfg80211.c:102-103` `linux/brcmfmac/cfg80211.c:1878-1922`

### `brcmf_join_scan_params_le` (linux)
Scan parameters inside `brcmf_ext_join_params_le` (member scan_le) for the "join" named variable, with no standalone use found in linux; not packed; 20 bytes; little-endian. `linux/brcmfmac/fwil_types.h:514-527` `linux/brcmfmac/fwil_types.h:532` `linux/brcmfmac/cfg80211.c:2586-2617`

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 1 | `scan_type` | `u8` | source comment: '0 use default'; linux writes -1, stored as 0xFF = BRCMF_SCANTYPE_DEFAULT `linux/brcmfmac/fwil_types.h:516` `linux/brcmfmac/fwil_types.h:61` `linux/brcmfmac/cfg80211.c:2586` `linux/brcmfmac/cfg80211.c:2586-2587` |
| 1 | 3 | (pad) | - | alignment padding before __le32; from the compiled layout `linux/brcmfmac/fwil_types.h:516-517` |
| 4 | 4 | `nprobes` | `__le32` | -1 = default; linux writes -1 unless a channel is set, then 320 / 20 = 16 `linux/brcmfmac/fwil_types.h:517` `linux/brcmfmac/cfg80211.c:2594-2618` `linux/brcmfmac/cfg80211.c:80-82` `linux/brcmfmac/cfg80211.c:2603-2613` |
| 8 | 4 | `active_time` | `__le32` | -1 = default; linux writes -1 unless a channel is set, then 320 `linux/brcmfmac/fwil_types.h:518` `linux/brcmfmac/cfg80211.c:2594-2618` `linux/brcmfmac/cfg80211.c:80-82` `linux/brcmfmac/cfg80211.c:2603-2613` |
| 12 | 4 | `passive_time` | `__le32` | -1 = default; linux writes -1 unless a channel is set, then 400 `linux/brcmfmac/fwil_types.h:521` `linux/brcmfmac/cfg80211.c:2594-2618` `linux/brcmfmac/cfg80211.c:80-82` `linux/brcmfmac/cfg80211.c:2603-2613` |
| 16 | 4 | `home_time` | `__le32` | -1 = default, which linux writes `linux/brcmfmac/fwil_types.h:524` `linux/brcmfmac/cfg80211.c:2586-2587` |

Size check: compiled

### `brcmf_ext_join_params_le` (linux)
Payload of the "join" named variable, set with the bsscfg prefix, after whose failure linux falls back to BRCMF_C_SET_SSID with `brcmf_join_params`; not packed; `sizeof` 72, sent length offsetof(assoc_le) + offsetof(chanspec_list) = 56 + 12 = 68, or 70 when a channel is set (one chanspec), so the 2 tail padding bytes are never sent; little-endian. `linux/brcmfmac/fwil_types.h:529-534` `linux/brcmfmac/cfg80211.c:2569-2623` `linux/brcmfmac/cfg80211.c:2569-2572` `linux/brcmfmac/cfg80211.c:2622-2623` `linux/brcmfmac/cfg80211.c:2629-2647`

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 36 | `ssid_le` | `struct brcmf_ssid_le` | {0, ""} = wildcard scan (source comment); 32-byte SSID from IEEE80211_MAX_SSID_LEN `linux/brcmfmac/fwil_types.h:531` `linux/brcmfmac/fwil_types.h:357-360` `linux-headers/ieee80211.h:227` |
| 36 | 20 | `scan_le` | `struct brcmf_join_scan_params_le` | scan_type at 36, 3 pad bytes, nprobes 40, active_time 44, passive_time 48, home_time 52 `linux/brcmfmac/fwil_types.h:532` |
| 56 | 16 | `assoc_le` | `struct brcmf_assoc_params_le` | bssid at 56, 2 pad bytes at 62, chanspec_num at 64, chanspec_list at 68, 2 tail pad bytes at 70; the bssid size rests on ETH_ALEN = 6 (recalled, not in these sources) `linux/brcmfmac/fwil_types.h:533` |

Size check: compiled

### `brcmf_wsec_key_le` (linux)
Payload of the "wsec_key" named variable, set with the bsscfg prefix and sent with length `sizeof`; not packed; 164 bytes; little-endian. `linux/brcmfmac/fwil_types.h:555-575` `linux/brcmfmac/cfg80211.c:548-559`

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `index` | `__le32` | key index `linux/brcmfmac/fwil_types.h:559` |
| 4 | 4 | `len` | `__le32` | key length `linux/brcmfmac/fwil_types.h:560` |
| 8 | 32 | `data` | `u8[WLAN_MAX_KEY_LEN]` | key data; WLAN_MAX_KEY_LEN = 32, which fwil_types.h does not define; the record size and every later offset depend on it `linux/brcmfmac/fwil_types.h:561` `linux-headers/ieee80211.h:2267` |
| 40 | 72 | `pad_1` | `__le32[18]` | named pad member in source `linux/brcmfmac/fwil_types.h:562` |
| 112 | 4 | `algo` | `__le32` | CRYPTO_ALGO_* `linux/brcmfmac/fwil_types.h:563` |
| 116 | 4 | `flags` | `__le32` | `linux/brcmfmac/fwil_types.h:564` |
| 120 | 12 | `pad_2` | `__le32[3]` | named pad member in source `linux/brcmfmac/fwil_types.h:565` |
| 132 | 4 | `iv_initialized` | `__le32` | `linux/brcmfmac/fwil_types.h:566` |
| 136 | 4 | `pad_3` | `__le32` | named pad member in source `linux/brcmfmac/fwil_types.h:567` |
| 140 | 4 | `rxiv.hi` | `__le32` | upper 32 bits of Rx IV `linux/brcmfmac/fwil_types.h:570` |
| 144 | 2 | `rxiv.lo` | `__le16` | lower 16 bits of Rx IV `linux/brcmfmac/fwil_types.h:571` |
| 146 | 2 | (pad) | - | tail padding of the anonymous rxiv struct; from the compiled layout `linux/brcmfmac/fwil_types.h:569-572` |
| 148 | 8 | `pad_4` | `__le32[2]` | named pad member in source `linux/brcmfmac/fwil_types.h:573` |
| 156 | 6 | `ea` | `u8[6]` | per-station address; declared `[ETH_ALEN]`; ETH_ALEN = 6 is (recalled, not in these sources) `linux/brcmfmac/fwil_types.h:574` |
| 162 | 2 | (pad) | - | trailing padding to 4-byte alignment; from the compiled layout `linux/brcmfmac/fwil_types.h:574-575` |

Size check: compiled

Differences: the host-order twin `brcmf_wsec_key` has the same member list with u32/u16 fields and is not sent directly; linux converts it field by field. `linux/brcmfmac/fwil_types.h:536-553` `linux/brcmfmac/cfg80211.c:533-545`

Differences: the conversion writes only index, len, algo, flags, rxiv.hi, rxiv.lo, iv_initialized, data and ea; key_le is an on-stack variable with no memset, so pad_1..pad_4 and the padding bytes are not set by this code. `linux/brcmfmac/cfg80211.c:536-544` `linux/brcmfmac/cfg80211.c:552-554`

### `brcmf_wsec_pmk_le` (linux)
Payload of command BRCMF_C_SET_WSEC_PMK (268), sent with length `sizeof` after linux zeroes the record; not packed; 132 bytes; little-endian. `linux/brcmfmac/fwil_types.h:577-588` `linux/brcmfmac/fwil.h:82` `linux/brcmfmac/cfg80211.c:1710-1731`

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 2 | `key_len` | `__le16` | number of octets in key; linux rejects a key_len above 128 `linux/brcmfmac/fwil_types.h:585` `linux/brcmfmac/cfg80211.c:1716-1727` |
| 2 | 2 | `flags` | `__le16` | key handling qualifiers, e.g. BRCMF_WSEC_PASSPHRASE = BIT(0); linux passes 0 for a PMK, and BRCMF_WSEC_PASSPHRASE for an SAE password in the wcc vendor code `linux/brcmfmac/fwil_types.h:586` `linux/brcmfmac/fwil_types.h:66` `linux/brcmfmac/cfg80211.c:1740-1742` `linux/brcmfmac/wcc/core.c:16-20` |
| 4 | 128 | `key` | `u8[BRCMF_WSEC_MAX_SAE_PASSWORD_LEN]` | BRCMF_WSEC_MAX_SAE_PASSWORD_LEN = 128; linux copies key_len bytes `linux/brcmfmac/fwil_types.h:587` `linux/brcmfmac/fwil_types.h:68` `linux/brcmfmac/cfg80211.c:1716-1727` |

Size check: compiled

### `brcmf_wsec_sae_pwd_le` (linux)
Payload of the "sae_password" named variable (set), sent with length `sizeof`; not packed; 130 bytes; little-endian. `linux/brcmfmac/fwil_types.h:590-599` `linux/brcmfmac/cyw/core.c:30-44`

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 2 | `key_len` | `__le16` | number of octets in key; linux rejects passwords longer than 128 bytes `linux/brcmfmac/fwil_types.h:597` `linux/brcmfmac/cyw/core.c:34-38` |
| 2 | 128 | `key` | `u8[BRCMF_WSEC_MAX_SAE_PASSWORD_LEN]` | SAE password, 128 bytes max; the record is an on-stack variable with no memset, and only key_len and the first key_len bytes of key are written `linux/brcmfmac/fwil_types.h:598` `linux/brcmfmac/fwil_types.h:68` `linux/brcmfmac/cyw/core.c:30` `linux/brcmfmac/cyw/core.c:40-41` |

Size check: compiled

### `brcmf_scb_val_le` (linux)
Payload of commands BRCMF_C_DISASSOC (52), BRCMF_C_GET_RSSI (127) and BRCMF_C_SCB_DEAUTHENTICATE_FOR_REASON (201); not packed; 12 bytes; little-endian. `linux/brcmfmac/fwil_types.h:601-605` `linux/brcmfmac/fwil.h:42` `linux/brcmfmac/fwil.h:61` `linux/brcmfmac/fwil.h:73`

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `val` | `__le32` | reason code on DISASSOC and SCB_DEAUTHENTICATE_FOR_REASON; on GET_RSSI linux zeroes the record, sends it, and reads the RSSI back from val `linux/brcmfmac/fwil_types.h:603` `linux/brcmfmac/cfg80211.c:2679-2682` `linux/brcmfmac/cfg80211.c:5611-5614` `linux/brcmfmac/cfg80211.c:3151-3158` `linux/brcmfmac/cfg80211.c:3283-3285` |
| 4 | 6 | `ea` | `u8[6]` | DISASSOC: the current BSSID; SCB_DEAUTHENTICATE_FOR_REASON: the station address; GET_RSSI: all zero; declared `[ETH_ALEN]`; ETH_ALEN = 6 is (recalled, not in these sources) `linux/brcmfmac/fwil_types.h:604` `linux/brcmfmac/cfg80211.c:2679-2682` `linux/brcmfmac/cfg80211.c:5611-5614` `linux/brcmfmac/cfg80211.c:3151-3158` |
| 10 | 2 | (pad) | - | trailing padding to 4-byte alignment; from the compiled layout `linux/brcmfmac/fwil_types.h:603-605` |

Size check: compiled

### `brcmf_channel_info_le` (linux)
Channel record with no use found: the type name appears only at its definition in the linux sources, under the sole source comment "channel encoding"; not packed; 12 bytes (three __le32, no padding); little-endian. `linux/brcmfmac/fwil_types.h:607-612`

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `hw_channel` | `__le32` | `linux/brcmfmac/fwil_types.h:609` |
| 4 | 4 | `target_channel` | `__le32` | `linux/brcmfmac/fwil_types.h:610` |
| 8 | 4 | `scan_channel` | `__le32` | `linux/brcmfmac/fwil_types.h:611` |

Size check: compiled

Differences: linux calls BRCMF_C_GET_CHANNEL (29) with a bare __le32 (4 bytes) in one place and a bare __le16 (2 bytes) in another, never with this record. `linux/brcmfmac/fwil.h:27` `linux/brcmfmac/cfg80211.c:5684` `linux/brcmfmac/cfg80211.c:5746-5748` `linux/brcmfmac/cyw/core.c:114` `linux/brcmfmac/cyw/core.c:146-147`

Differences: a link between this record and BRCMF_C_GET_CHANNEL rests only on the field name hw_channel (inferred); no driver source here states or shows it. `linux/brcmfmac/fwil_types.h:609`

### `brcmf_sta_info_le` (linux)
Reply of the "tdls_sta_info" named variable and, when that fails, of "sta_info" (get), for which linux zeroes the buffer, writes the 6-byte station MAC at offset 0 and passes `sizeof` (296) as the buffer length; not packed (alignment 8 because of the __le64 members); 296 bytes; little-endian. `linux/brcmfmac/fwil_types.h:614-706` `linux/brcmfmac/cfg80211.c:3205-3214`

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 2 | `ver` | `__le16` | version of this struct; linux reads it `linux/brcmfmac/fwil_types.h:615` `linux/brcmfmac/cfg80211.c:3220` `linux/brcmfmac/cfg80211.c:3254` |
| 2 | 2 | `len` | `__le16` | length in bytes of this structure; linux never reads it and does not check the reported length against `sizeof` `linux/brcmfmac/fwil_types.h:616` `linux/brcmfmac/cfg80211.c:3220` `linux/brcmfmac/cfg80211.c:3254` |
| 4 | 2 | `cap` | `__le16` | advertised capabilities `linux/brcmfmac/fwil_types.h:617` |
| 6 | 2 | (pad) | - | alignment padding; from the compiled layout `linux/brcmfmac/fwil_types.h:617-618` |
| 8 | 4 | `flags` | `__le32` | BRCMF_STA_* `linux/brcmfmac/fwil_types.h:24-47` `linux/brcmfmac/fwil_types.h:618` |
| 12 | 4 | `idle` | `__le32` | time since data pkt rx'd `linux/brcmfmac/fwil_types.h:619` |
| 16 | 6 | `ea` | `u8[6]` | station address; declared `[ETH_ALEN]`; ETH_ALEN = 6 is (recalled, not in these sources), and the offsets from count on depend on it `linux/brcmfmac/fwil_types.h:620` |
| 22 | 2 | (pad) | - | alignment padding; from the compiled layout `linux/brcmfmac/fwil_types.h:620-621` |
| 24 | 4 | `count` | `__le32` | # rates in this set `linux/brcmfmac/fwil_types.h:621` |
| 28 | 16 | `rates` | `u8[16]` | BRCMF_MAXRATES_IN_SET = 16 `linux/brcmfmac/fwil_types.h:76` `linux/brcmfmac/fwil_types.h:622` |
| 44 | 4 | `in` | `__le32` | seconds since associated `linux/brcmfmac/fwil_types.h:624` |
| 48 | 4 | `listen_interval_inms` | `__le32` | `linux/brcmfmac/fwil_types.h:625` |
| 52 | 4 | `tx_pkts` | `__le32` | first field valid for ver >= 3 (source comment) `linux/brcmfmac/fwil_types.h:627` `linux/brcmfmac/fwil_types.h:628` |
| 56 | 4 | `tx_failures` | `__le32` | `linux/brcmfmac/fwil_types.h:629` |
| 60 | 4 | `rx_ucast_pkts` | `__le32` | `linux/brcmfmac/fwil_types.h:630` |
| 64 | 4 | `rx_mcast_pkts` | `__le32` | `linux/brcmfmac/fwil_types.h:631` |
| 68 | 4 | `tx_rate` | `__le32` | `linux/brcmfmac/fwil_types.h:632` |
| 72 | 4 | `rx_rate` | `__le32` | `linux/brcmfmac/fwil_types.h:633` |
| 76 | 4 | `rx_decrypt_succeeds` | `__le32` | `linux/brcmfmac/fwil_types.h:634` |
| 80 | 4 | `rx_decrypt_failures` | `__le32` | `linux/brcmfmac/fwil_types.h:635` |
| 84 | 4 | `tx_tot_pkts` | `__le32` | first field valid for ver >= 4 (source comment) `linux/brcmfmac/fwil_types.h:637` `linux/brcmfmac/fwil_types.h:638` |
| 88 | 4 | `rx_tot_pkts` | `__le32` | `linux/brcmfmac/fwil_types.h:639` |
| 92 | 4 | `tx_mcast_pkts` | `__le32` | `linux/brcmfmac/fwil_types.h:640` |
| 96 | 8 | `tx_tot_bytes` | `__le64` | no padding is needed before it; with 4-byte u64 alignment the layout is the same (computed): this member already falls at 96, later members follow without gaps, and 296 is a multiple of 4 and 8 `linux/brcmfmac/fwil_types.h:640-641` |
| 104 | 8 | `rx_tot_bytes` | `__le64` | `linux/brcmfmac/fwil_types.h:642` |
| 112 | 8 | `tx_ucast_bytes` | `__le64` | `linux/brcmfmac/fwil_types.h:643` |
| 120 | 8 | `tx_mcast_bytes` | `__le64` | `linux/brcmfmac/fwil_types.h:644` |
| 128 | 8 | `rx_ucast_bytes` | `__le64` | `linux/brcmfmac/fwil_types.h:645` |
| 136 | 8 | `rx_mcast_bytes` | `__le64` | `linux/brcmfmac/fwil_types.h:646` |
| 144 | 4 | `rssi` | `s8[4]` | per antenna, BRCMF_ANT_MAX = 4 `linux/brcmfmac/fwil_types.h:147` `linux/brcmfmac/fwil_types.h:647` |
| 148 | 4 | `nf` | `s8[4]` | per antenna noise floor `linux/brcmfmac/fwil_types.h:648` |
| 152 | 2 | `aid` | `__le16` | `linux/brcmfmac/fwil_types.h:649` |
| 154 | 2 | `ht_capabilities` | `__le16` | `linux/brcmfmac/fwil_types.h:650` |
| 156 | 2 | `vht_flags` | `__le16` | `linux/brcmfmac/fwil_types.h:651` |
| 158 | 2 | (pad) | - | alignment padding; from the compiled layout `linux/brcmfmac/fwil_types.h:651-652` |
| 160 | 4 | `tx_pkts_retry_cnt` | `__le32` | `linux/brcmfmac/fwil_types.h:652` |
| 164 | 4 | `tx_pkts_retry_exhausted` | `__le32` | `linux/brcmfmac/fwil_types.h:655` |
| 168 | 4 | `rx_lastpkt_rssi` | `s8[4]` | `linux/brcmfmac/fwil_types.h:658` |
| 172 | 4 | `tx_pkts_total` | `__le32` | `linux/brcmfmac/fwil_types.h:665` |
| 176 | 4 | `tx_pkts_retries` | `__le32` | `linux/brcmfmac/fwil_types.h:666` |
| 180 | 4 | `tx_pkts_fw_total` | `__le32` | `linux/brcmfmac/fwil_types.h:667` |
| 184 | 4 | `tx_pkts_fw_retries` | `__le32` | `linux/brcmfmac/fwil_types.h:668` |
| 188 | 4 | `tx_pkts_fw_retry_exhausted` | `__le32` | `linux/brcmfmac/fwil_types.h:669` |
| 192 | 4 | `rx_pkts_retried` | `__le32` | `linux/brcmfmac/fwil_types.h:672` |
| 196 | 4 | `tx_rate_fallback` | `__le32` | `linux/brcmfmac/fwil_types.h:673` |
| 200 | 96 | `v5 / v7` | `union` | union alternatives named v5 (52 bytes) and v7 (96 bytes) (compiled); sub-fields listed below with absolute offsets `linux/brcmfmac/fwil_types.h:675-705` `linux/brcmfmac/fwil_types.h:676-683` `linux/brcmfmac/fwil_types.h:685-704` |
| 200 | 4 | `v5.rateset_adv.count` | `__le32` | v5 alternative `linux/brcmfmac/fwil_types.h:678` |
| 204 | 16 | `v5.rateset_adv.rates` | `u8[16]` | v5 alternative `linux/brcmfmac/fwil_types.h:679` |
| 220 | 16 | `v5.rateset_adv.mcs` | `u8[16]` | BRCMF_MCSSET_LEN = 16 `linux/brcmfmac/fwil_types.h:163`; v5 alternative `linux/brcmfmac/fwil_types.h:680` |
| 236 | 16 | `v5.rateset_adv.vht_mcs` | `__le16[8]` | 8 spatial streams max `linux/brcmfmac/fwil_types.h:173`; v5 alternative `linux/brcmfmac/fwil_types.h:681` |
| 200 | 4 | `v7.rx_dur_total` | `__le32` | v7 alternative `linux/brcmfmac/fwil_types.h:686` |
| 204 | 2 | `v7.chanspec` | `__le16` | v7 alternative `linux/brcmfmac/fwil_types.h:687` |
| 206 | 2 | `v7.pad_1` | `__le16` | named pad member in source; v7 alternative `linux/brcmfmac/fwil_types.h:688` |
| 208 | 2 | `v7.rateset_adv.version` | `__le16` | v7 alternative `linux/brcmfmac/fwil_types.h:690` |
| 210 | 2 | `v7.rateset_adv.len` | `__le16` | v7 alternative `linux/brcmfmac/fwil_types.h:691` |
| 212 | 4 | `v7.rateset_adv.count` | `__le32` | v7 alternative `linux/brcmfmac/fwil_types.h:692` |
| 216 | 16 | `v7.rateset_adv.rates` | `u8[16]` | v7 alternative `linux/brcmfmac/fwil_types.h:693` |
| 232 | 16 | `v7.rateset_adv.mcs` | `u8[16]` | BRCMF_MCSSET_LEN = 16 `linux/brcmfmac/fwil_types.h:163`; v7 alternative `linux/brcmfmac/fwil_types.h:694` |
| 248 | 16 | `v7.rateset_adv.vht_mcs` | `__le16[8]` | 8 spatial streams max `linux/brcmfmac/fwil_types.h:173`; v7 alternative `linux/brcmfmac/fwil_types.h:695` |
| 264 | 16 | `v7.rateset_adv.he_mcs` | `__le16[8]` | 8 spatial streams max `linux/brcmfmac/fwil_types.h:175`; v7 alternative `linux/brcmfmac/fwil_types.h:696` |
| 280 | 2 | `v7.wpauth` | `__le16` | v7 alternative `linux/brcmfmac/fwil_types.h:698` |
| 282 | 1 | `v7.algo` | `u8` | crypto algorithm; v7 alternative `linux/brcmfmac/fwil_types.h:699` |
| 283 | 1 | `v7.pad_2` | `u8` | named pad member in source; v7 alternative `linux/brcmfmac/fwil_types.h:700` |
| 284 | 4 | `v7.tx_rspec` | `__le32` | v7 alternative `linux/brcmfmac/fwil_types.h:701` |
| 288 | 4 | `v7.rx_rspec` | `__le32` | v7 alternative `linux/brcmfmac/fwil_types.h:702` |
| 292 | 4 | `v7.wnm_cap` | `__le32` | v7 alternative `linux/brcmfmac/fwil_types.h:703` |
| 252 | 44 | (pad) | - | v5 alternative only: unused remainder of the union up to 296; from the compiled layout `linux/brcmfmac/fwil_types.h:675-705` |

Size check: compiled

### `brcmf_chanspec_list` (linux)
Reply of the "chanspecs" named variable (get), read by linux into a BRCMF_DCMD_MEDLEN (1536) byte buffer at two call sites, the second of which writes a __le16 chanspec at offset 0 of the buffer as the query before the get; not packed; variable, 4 fixed bytes plus a tail of __le32; little-endian. `linux/brcmfmac/fwil_types.h:708-711` `linux/brcmfmac/core.h:31` `linux/brcmfmac/cfg80211.c:7230-7233` `linux/brcmfmac/cfg80211.c:7232-7233` `linux/brcmfmac/cfg80211.c:7388-7391` `linux/brcmfmac/cfg80211.c:7390-7391`

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `count` | `__le32` | number of entries; linux bounds it by BRCMF_MAX_CHANSPEC_LIST = 1536 / 4 - 1 = 383 `linux/brcmfmac/fwil_types.h:709` `linux/brcmfmac/cfg80211.c:105-106` `linux/brcmfmac/cfg80211.c:7400-7401` |
| 4 | variable | `element` | `__le32[]` | flexible array; each element holds a chanspec in a 32-bit slot `linux/brcmfmac/fwil_types.h:710` |

Size check: compiled

### `brcmf_rx_mgmt_data` (linux)
Event data header in front of a received management frame, parsed by the registered linux handlers of BRCMF_E_P2P_PROBEREQ_MSG (72), BRCMF_E_ACTION_FRAME_RX (75) and BRCMF_E_EXT_AUTH_FRAME_RX (an abstract code in linux, mapped to 188 in the cyw vendor code), all of which reject event data shorter than 16 bytes; not packed; 16 fixed bytes followed immediately by the 802.11 frame (event datalen - 16); big-endian (`__be16`/`__be32` members). `linux/brcmfmac/fwil_types.h:713-724` `linux/brcmfmac/p2p.c:1423-1425` `linux/brcmfmac/fweh.h:92` `linux/brcmfmac/cfg80211.c:7015-7016` `linux/brcmfmac/p2p.c:1964-1979` `linux/brcmfmac/fweh.h:95` `linux/brcmfmac/cfg80211.c:7019-7020` `linux/brcmfmac/p2p.c:1423-1439` `linux/brcmfmac/fweh.h:99` `linux/brcmfmac/cyw/core.c:18` `linux/brcmfmac/cyw/core.c:55` `linux/brcmfmac/cyw/core.c:365-366` `linux/brcmfmac/cyw/core.c:281-320` `linux/brcmfmac/p2p.c:1425` `linux/brcmfmac/p2p.c:2007` `linux/brcmfmac/cyw/core.c:283` `linux/brcmfmac/p2p.c:1434` `linux/brcmfmac/p2p.c:1974` `linux/brcmfmac/cyw/core.c:291`

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 2 | `version` | `__be16` | `linux/brcmfmac/fwil_types.h:719` |
| 2 | 2 | `chanspec` | `__be16` | read with be16_to_cpu; the three handlers read only this field, so version, rssi, mactime and rate are not used `linux/brcmfmac/fwil_types.h:720` `linux/brcmfmac/p2p.c:1439` `linux/brcmfmac/p2p.c:1979` `linux/brcmfmac/cyw/core.c:306` |
| 4 | 4 | `rssi` | `__be32` | `linux/brcmfmac/fwil_types.h:721` |
| 8 | 4 | `mactime` | `__be32` | `linux/brcmfmac/fwil_types.h:722` |
| 12 | 4 | `rate` | `__be32` | `linux/brcmfmac/fwil_types.h:723` |

Size check: compiled

Differences: the source comment names WLC_E_PROBRESP_MSG, WLC_E_P2P_PROBREQ_MSG and WLC_E_ACTION_FRAME_RX, but a handler for BRCMF_E_PROBERESP_MSG (71) is not found in these sources. `linux/brcmfmac/fwil_types.h:713-717` `linux/brcmfmac/fweh.h:91`

### `brcmf_fil_wowl_pattern_le` (linux)
Payload of the "wowl_pattern" named variable (set), which linux callers send with cmd "clr" and "add"; not packed; variable, 32 fixed bytes plus mask and pattern, sent length 32 + patternsize + masksize; little-endian. `linux/brcmfmac/fwil_types.h:726-749` `linux/brcmfmac/cfg80211.c:4046-4078` `linux/brcmfmac/cfg80211.c:4223` `linux/brcmfmac/cfg80211.c:4263` `linux/brcmfmac/cfg80211.c:4060` `linux/brcmfmac/cfg80211.c:4078`

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `cmd` | `u8[4]` | "add", "del" or "clr" `linux/brcmfmac/fwil_types.h:739` |
| 4 | 4 | `masksize` | `__le32` | mask size in bytes; linux sets (patternsize + 7) / 8 `linux/brcmfmac/fwil_types.h:740` `linux/brcmfmac/cfg80211.c:4057-4058` |
| 8 | 4 | `offset` | `__le32` | pattern byte offset in packet `linux/brcmfmac/fwil_types.h:741` |
| 12 | 4 | `patternoffset` | `__le32` | offset of pattern start, counted from field masksize; linux sets sizeof(record) - sizeof(cmd) + masksize = 28 + masksize `linux/brcmfmac/fwil_types.h:742` `linux/brcmfmac/cfg80211.c:4057-4058` |
| 16 | 4 | `patternsize` | `__le32` | pattern size in bytes `linux/brcmfmac/fwil_types.h:743` |
| 20 | 4 | `id` | `__le32` | linux leaves it zero (zeroed allocation, never written) `linux/brcmfmac/fwil_types.h:744` `linux/brcmfmac/cfg80211.c:4061-4071` |
| 24 | 4 | `reasonsize` | `__le32` | size of the wakeup reason code; linux leaves it zero (zeroed allocation, never written) `linux/brcmfmac/fwil_types.h:745` `linux/brcmfmac/cfg80211.c:4061-4071` |
| 28 | 4 | `type` | `__le32` | enum brcmf_wowl_pattern_type; linux sets BRCMF_WOWL_PATTERN_TYPE_BITMAP (0) `linux/brcmfmac/fwil_types.h:746` `linux/brcmfmac/fwil_types.h:211` `linux/brcmfmac/fwil_types.h:212` `linux/brcmfmac/cfg80211.c:4061-4071` |
| 32 | variable | `mask` | `u8[masksize]` | not a declared member: comment at line 747, bytes appended by the use site `linux/brcmfmac/fwil_types.h:747` |
| 32+masksize | variable | `pattern` | `u8[patternsize]` | not a declared member: comment at line 748 `linux/brcmfmac/fwil_types.h:748` |

Size check: compiled

### `brcmf_mbss_ssid_le` (linux)
Payload of the "bsscfg:ssid" named variable, set with the bsscfg prefix and sent with length `sizeof` after linux zeroes the record; not packed; 40 bytes; little-endian. `linux/brcmfmac/fwil_types.h:751-755` `linux/brcmfmac/cfg80211.c:791-801`

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `bsscfgidx` | `__le32` | linux sets the first free index `linux/brcmfmac/fwil_types.h:752` `linux/brcmfmac/cfg80211.c:791-798` |
| 4 | 4 | `SSID_len` | `__le32` | linux sets 5 `linux/brcmfmac/fwil_types.h:753` `linux/brcmfmac/cfg80211.c:791-798` |
| 8 | 32 | `SSID` | `unsigned char[32]` | linux writes "ssid" followed by the index in decimal `linux/brcmfmac/fwil_types.h:754` `linux/brcmfmac/cfg80211.c:791-798` |

Size check: compiled

### `brcmf_fil_country_le` (linux)
Payload of the "country" named variable (get, then set), with length `sizeof` both ways; not packed; 12 bytes; rev little-endian, the other fields char arrays. `linux/brcmfmac/fwil_types.h:757-768` `linux/brcmfmac/cfg80211.c:8484-8494`

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `country_abbrev` | `char[4]` | null-terminated country code used in the country IE; BRCMF_COUNTRY_BUF_SZ = 4 `linux/brcmfmac/fwil_types.h:146` `linux/brcmfmac/fwil_types.h:765` |
| 4 | 4 | `rev` | `__le32` | revision for ccode; on set -1 = unspecified `linux/brcmfmac/fwil_types.h:766` |
| 8 | 4 | `ccode` | `char[4]` | null-terminated built-in country code `linux/brcmfmac/fwil_types.h:767` |

Size check: compiled

Differences: linux fills the set request in brcmf_translate_country_code in one of two ways. Its ISO3166 fallback zeroes the record and sets two characters in country_abbrev and in ccode, leaving rev 0. `linux/brcmfmac/cfg80211.c:8490` `linux/brcmfmac/cfg80211.c:8196-8203`

Differences: with a country-code table configured, linux zeroes the record, sets rev and the 4 bytes of ccode from the matching table entry, and sets two characters in country_abbrev. `linux/brcmfmac/cfg80211.c:8225-8231`

### `brcmf_rev_info_le` (linux)
Reply of command BRCMF_C_GET_REVINFO (98), requested with length `sizeof`; not packed; 68 bytes (17 x __le32); little-endian. `linux/brcmfmac/fwil_types.h:770-809` `linux/brcmfmac/fwil.h:53` `linux/brcmfmac/common.c:271` `linux/brcmfmac/common.c:307-308`

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `vendorid` | `__le32` | PCI vendor id `linux/brcmfmac/fwil_types.h:792` |
| 4 | 4 | `deviceid` | `__le32` | device id of chip `linux/brcmfmac/fwil_types.h:793` |
| 8 | 4 | `radiorev` | `__le32` | radio revision `linux/brcmfmac/fwil_types.h:794` |
| 12 | 4 | `chiprev` | `__le32` | chip revision `linux/brcmfmac/fwil_types.h:795` |
| 16 | 4 | `corerev` | `__le32` | core revision `linux/brcmfmac/fwil_types.h:796` |
| 20 | 4 | `boardid` | `__le32` | board identifier `linux/brcmfmac/fwil_types.h:797` |
| 24 | 4 | `boardvendor` | `__le32` | board vendor `linux/brcmfmac/fwil_types.h:798` |
| 28 | 4 | `boardrev` | `__le32` | board revision `linux/brcmfmac/fwil_types.h:799` |
| 32 | 4 | `driverrev` | `__le32` | driver version `linux/brcmfmac/fwil_types.h:800` |
| 36 | 4 | `ucoderev` | `__le32` | microcode version `linux/brcmfmac/fwil_types.h:801` |
| 40 | 4 | `bus` | `__le32` | bus type `linux/brcmfmac/fwil_types.h:802` |
| 44 | 4 | `chipnum` | `__le32` | chip number `linux/brcmfmac/fwil_types.h:803` |
| 48 | 4 | `phytype` | `__le32` | phy type `linux/brcmfmac/fwil_types.h:804` |
| 52 | 4 | `phyrev` | `__le32` | phy revision `linux/brcmfmac/fwil_types.h:805` |
| 56 | 4 | `anarev` | `__le32` | anacore rev `linux/brcmfmac/fwil_types.h:806` |
| 60 | 4 | `chippkg` | `__le32` | chip package info `linux/brcmfmac/fwil_types.h:807` |
| 64 | 4 | `nvramrev` | `__le32` | nvram revision number `linux/brcmfmac/fwil_types.h:808` |

Size check: compiled

### `brcmf_wlc_version_le` (linux)
Reply of the "wlc_ver" named variable (get), requested with length `sizeof`, from which linux reads only `wlc_ver_major` and `wlc_ver_minor`; not packed (alignment 2); 16 bytes; little-endian. `linux/brcmfmac/fwil_types.h:823-834` `linux/brcmfmac/fwil_types.h:811-822` `linux/brcmfmac/feature.c:148-157`

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 2 | `version` | `__le16` | structure version `linux/brcmfmac/fwil_types.h:824` `linux/brcmfmac/fwil_types.h:814` |
| 2 | 2 | `length` | `__le16` | structure length `linux/brcmfmac/fwil_types.h:825` `linux/brcmfmac/fwil_types.h:815` |
| 4 | 2 | `epi_ver_major` | `__le16` | EPI major version `linux/brcmfmac/fwil_types.h:827` `linux/brcmfmac/fwil_types.h:816` |
| 6 | 2 | `epi_ver_minor` | `__le16` | EPI minor version `linux/brcmfmac/fwil_types.h:828` `linux/brcmfmac/fwil_types.h:817` |
| 8 | 2 | `epi_ver_rc` | `__le16` | EPI rc version `linux/brcmfmac/fwil_types.h:829` `linux/brcmfmac/fwil_types.h:818` |
| 10 | 2 | `epi_ver_incr` | `__le16` | EPI increment version `linux/brcmfmac/fwil_types.h:830` `linux/brcmfmac/fwil_types.h:819` |
| 12 | 2 | `wlc_ver_major` | `__le16` | WLC major version; read by linux `linux/brcmfmac/fwil_types.h:832` `linux/brcmfmac/fwil_types.h:820` `linux/brcmfmac/feature.c:156` |
| 14 | 2 | `wlc_ver_minor` | `__le16` | WLC minor version; read by linux `linux/brcmfmac/fwil_types.h:833` `linux/brcmfmac/fwil_types.h:821` `linux/brcmfmac/feature.c:157` |

Size check: compiled

### `brcmf_assoclist_le` (linux)
Command BRCMF_C_GET_ASSOCLIST (get), `linux/brcmfmac/cfg80211.c:3316-3318`; the buffer is cfg->assoclist (`linux/brcmfmac/cfg80211.h:400`); not packed; 772 bytes; little-endian (__le16/__le32 fields; u8 fields have no byte order); defined at `linux/brcmfmac/fwil_types.h:842-845`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `count` | `__le32` | number of stations; host presets it to BRCMF_MAX_ASSOCLIST before the get (`linux/brcmfmac/cfg80211.c:3315`) |
| 4 | 768 | `mac` | `u8[128][6]` | BRCMF_MAX_ASSOCLIST = 128 (`linux/brcmfmac/fwil_types.h:149`) x ETH_ALEN; ETH_ALEN = 6 (recalled, not in these sources); whd has ETHER_ADDR_LEN 6 `whd/inc/whd_types.h:101` |

Size check: compiled (gcc, x86-64; sizeof = 772, alignment = 4)

### `brcmf_rssi_be` (linux)
Event data of BRCMF_E_RSSI: handler brcmf_notify_rssi `linux/brcmfmac/cfg80211.c:6886-6896`, registered at `linux/brcmfmac/cfg80211.c:7027`; kernel-doc calls it the RSSI threshold event format `linux/brcmfmac/fwil_types.h:847-853`; linux reads snr and noise only when datalen >= 12 `linux/brcmfmac/cfg80211.c:6894`; linux accepts a shorter payload of at least 4 bytes and reads rssi only `linux/brcmfmac/cfg80211.c:6898`; not packed; 12 bytes; big-endian (__be32 fields); defined at `linux/brcmfmac/fwil_types.h:854-858`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `rssi` | `__be32` | dBm `linux/brcmfmac/fwil_types.h:854-858` |
| 4 | 4 | `snr` | `__be32` | `linux/brcmfmac/fwil_types.h:854-858` |
| 8 | 4 | `noise` | `__be32` | dBm `linux/brcmfmac/fwil_types.h:854-858` |

Size check: compiled (gcc, x86-64; sizeof = 12, alignment = 4)

### `brcmf_rssi_event_le` (linux)
Named variable "rssi_event" (set), `linux/brcmfmac/cfg80211.c:5801-5812`; 13 bytes of fields round up to 16, and linux sends sizeof(config) = 16 bytes `linux/brcmfmac/cfg80211.c:5811-5812`; whether the firmware's own record is 13 or 16 bytes is not stated in these sources; not packed; 16 bytes; little-endian (__le16/__le32 fields; u8 fields have no byte order); defined at `linux/brcmfmac/fwil_types.h:869-873`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `rate_limit_msec` | `__le32` | `linux/brcmfmac/fwil_types.h:869-873` |
| 4 | 1 | `rssi_level_num` | `s8` | `linux/brcmfmac/fwil_types.h:869-873` |
| 5 | 8 | `rssi_levels` | `s8[8]` | BRCMF_MAX_RSSI_LEVELS = 8 (`linux/brcmfmac/fwil_types.h:860`); ascending order |
| 13 | 3 | (pad) | `u8[3]` | trailing padding to the struct alignment of 4 `linux/brcmfmac/fwil_types.h:869-873` |

Size check: compiled (gcc, x86-64; sizeof = 16, alignment = 4)

### `brcmf_wowl_wakeind_le` (linux)
Named variable "wowl_wakeind" (get), `linux/brcmfmac/cfg80211.c:4139`, `linux/brcmfmac/cfg80211.c:4146-4147`; the same 8-byte buffer is also used for a set whose content is the string "clear" (variable declared at `linux/brcmfmac/cfg80211.c:4245`, used at `linux/brcmfmac/cfg80211.c:4287-4289`); kernel-doc wording is "note both fields contain same information"; whether "not" was meant is not settled by these sources `linux/brcmfmac/fwil_types.h:877`; for the set, linux copies 6 bytes ("clear" and its NUL) into the 8-byte record and sends all 8; the last 2 bytes are uninitialised stack memory `linux/brcmfmac/cfg80211.c:4245`, `linux/brcmfmac/cfg80211.c:4287-4289`; not packed; 8 bytes; little-endian (__le16/__le32 fields; u8 fields have no byte order); defined at `linux/brcmfmac/fwil_types.h:882-885`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `pci_wakeind` | `__le32` | `linux/brcmfmac/fwil_types.h:882-885` |
| 4 | 4 | `ucode_wakeind` | `__le32` | `linux/brcmfmac/fwil_types.h:882-885` |

Size check: compiled (gcc, x86-64; sizeof = 8, alignment = 4)

### `brcmf_pmksa` (linux)
Element of brcmf_pmk_list_le, sent with named variable "pmkid_info" (`linux/brcmfmac/cfg80211.c:4427-4428`); the host list lives in cfg->pmk_list (`linux/brcmfmac/cfg80211.h:381`) and entries are edited in set_pmksa / del_pmksa (`linux/brcmfmac/cfg80211.c:4437`, `linux/brcmfmac/cfg80211.c:4454-4460`, `linux/brcmfmac/cfg80211.c:4482`) when BRCMF_FEAT_PMKID_V3 is not enabled (`linux/brcmfmac/cfg80211.c:4449-4452`); the size 22 is confirmed only given the recalled ETH_ALEN; the other array length is defined in the source set `linux-headers/ieee80211.h:2271`; not packed; 22 bytes; endianness not stated (byte arrays only); defined at `linux/brcmfmac/fwil_types.h:893-896`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 6 | `bssid` | `u8[6]` | `linux/brcmfmac/fwil_types.h:893-896`; ETH_ALEN = 6 (recalled, not in these sources); whd has ETHER_ADDR_LEN 6 `whd/inc/whd_types.h:101` |
| 6 | 16 | `pmkid` | `u8[16]` | `linux/brcmfmac/fwil_types.h:893-896`; WLAN_PMKID_LEN = 16 `linux-headers/ieee80211.h:2271` |

Size check: compiled (gcc, x86-64; sizeof = 22, alignment = 1)

### `brcmf_pmksa_v2` (linux)
Element of brcmf_pmk_list_v2_le (`linux/brcmfmac/fwil_types.h:964`); no use site in linux/brcmfmac (only the definitions occur); the size 110 is confirmed only given the recalled ETH_ALEN; the other array lengths are defined in the source set `linux-headers/ieee80211.h:227`, `linux-headers/ieee80211.h:2271-2274`; cfg80211.c carries a PMKID_V2 TODO `linux/brcmfmac/cfg80211.c:4452`, `linux/brcmfmac/cfg80211.c:4496`; not packed; 110 bytes; endianness mixed as written: __le16 length and pmk_len, but fils_cache_id is declared plain u16 (no endian annotation); defined at `linux/brcmfmac/fwil_types.h:909-917`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 2 | `length` | `__le16` | `linux/brcmfmac/fwil_types.h:909-917` |
| 2 | 6 | `bssid` | `u8[6]` | `linux/brcmfmac/fwil_types.h:909-917`; ETH_ALEN = 6 (recalled, not in these sources); whd has ETHER_ADDR_LEN 6 `whd/inc/whd_types.h:101` |
| 8 | 16 | `pmkid` | `u8[16]` | `linux/brcmfmac/fwil_types.h:909-917`; WLAN_PMKID_LEN = 16 `linux-headers/ieee80211.h:2271` |
| 24 | 48 | `pmk` | `u8[48]` | `linux/brcmfmac/fwil_types.h:909-917`; WLAN_PMK_LEN_SUITE_B_192 = 48 `linux-headers/ieee80211.h:2274` |
| 72 | 2 | `pmk_len` | `__le16` | `linux/brcmfmac/fwil_types.h:909-917` |
| 74 | 33 | `ssid` | `struct brcmf_ssid8_le` | u8 SSID_len + u8 SSID[32], 33 bytes (`linux/brcmfmac/fwil_types.h:363-366`); IEEE80211_MAX_SSID_LEN = 32 `linux-headers/ieee80211.h:227` |
| 107 | 1 | (pad) | `u8[1]` | alignment padding inserted by the compiler `linux/brcmfmac/fwil_types.h:909-917` |
| 108 | 2 | `fils_cache_id` | `u16` | declared u16, not __le16 `linux/brcmfmac/fwil_types.h:909-917` |

Size check: compiled (gcc, x86-64; sizeof = 110, alignment = 2)

### `brcmf_pmksa_v3` (linux)
Element of brcmf_pmk_op_v3_le, named variable "pmkid_info" (set), filled in brcmf_pmksa_v3_op `linux/brcmfmac/cfg80211.c:4373-4408`; the size 112 is confirmed only given the recalled ETH_ALEN; the other array lengths are defined in the source set `linux-headers/ieee80211.h:227`, `linux-headers/ieee80211.h:2271-2274`; not packed; 112 bytes; little-endian (__le16/__le32 fields; u8 fields have no byte order); defined at `linux/brcmfmac/fwil_types.h:931-941`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 6 | `bssid` | `u8[6]` | `linux/brcmfmac/fwil_types.h:931-941`; ETH_ALEN = 6 (recalled, not in these sources); whd has ETHER_ADDR_LEN 6 `whd/inc/whd_types.h:101` |
| 6 | 16 | `pmkid` | `u8[16]` | `linux/brcmfmac/fwil_types.h:931-941`; WLAN_PMKID_LEN = 16 `linux-headers/ieee80211.h:2271` |
| 22 | 1 | `pmkid_len` | `u8` | `linux/brcmfmac/fwil_types.h:931-941` |
| 23 | 48 | `pmk` | `u8[48]` | `linux/brcmfmac/fwil_types.h:931-941`; WLAN_PMK_LEN_SUITE_B_192 = 48 `linux-headers/ieee80211.h:2274` |
| 71 | 1 | `pmk_len` | `u8` | `linux/brcmfmac/fwil_types.h:931-941` |
| 72 | 2 | `fils_cache_id` | `__le16` | `linux/brcmfmac/fwil_types.h:931-941` |
| 74 | 1 | `pad` | `u8` | explicit pad member named 'pad' in the source `linux/brcmfmac/fwil_types.h:931-941` |
| 75 | 33 | `ssid` | `struct brcmf_ssid8_le` | u8 SSID_len + u8 SSID[32], 33 bytes (`linux/brcmfmac/fwil_types.h:363-366`); IEEE80211_MAX_SSID_LEN = 32 `linux-headers/ieee80211.h:227` |
| 108 | 4 | `time_left` | `__le32` | 0 = expired, ~0 = no expiry (`linux/brcmfmac/fwil_types.h:929`; BRCMF_PMKSA_NO_EXPIRY 0xffffffff `linux/brcmfmac/fwil_types.h:179`) |

Size check: compiled (gcc, x86-64; sizeof = 112, alignment = 4)

### `brcmf_pmk_list_le` (linux)
Named variable "pmkid_info" (set), whole struct sent, `linux/brcmfmac/cfg80211.c:4416-4428`; 4 + 16 x 22 = 356, no padding; the element size rests on ETH_ALEN = 6 (recalled, not in these sources) and WLAN_PMKID_LEN = 16 `linux-headers/ieee80211.h:2271`, `linux/brcmfmac/fwil_types.h:893-896`; not packed; 356 bytes; little-endian (__le16/__le32 fields; u8 fields have no byte order); defined at `linux/brcmfmac/fwil_types.h:949-952`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `npmk` | `__le32` | `linux/brcmfmac/fwil_types.h:949-952` |
| 4 | 352 | `pmk` | `struct brcmf_pmksa[16]` | BRCMF_MAXPMKID = 16 (`linux/brcmfmac/fwil_types.h:156`); 22 bytes each |

Size check: compiled (gcc, x86-64; sizeof = 356, alignment = 4)

### `brcmf_pmk_list_v2_le` (linux)
No use site in linux/brcmfmac (only BRCMF_PMKSA_VER_2 = 2 is defined, `linux/brcmfmac/fwil_types.h:177`); cfg80211.c carries "TODO: implement PMKID_V2" (`linux/brcmfmac/cfg80211.c:4452`, `linux/brcmfmac/cfg80211.c:4496`); kernel-doc at `linux/brcmfmac/fwil_types.h:954-960`; the element size 110 rests on ETH_ALEN = 6 (recalled, not in these sources) and on WLAN_PMKID_LEN = 16, WLAN_PMK_LEN_SUITE_B_192 = 48 and IEEE80211_MAX_SSID_LEN = 32 `linux-headers/ieee80211.h:2271`, `linux-headers/ieee80211.h:2274`, `linux-headers/ieee80211.h:227`, `linux/brcmfmac/fwil_types.h:909-917`; not packed; 1764 bytes; little-endian (__le16/__le32 fields; u8 fields have no byte order); defined at `linux/brcmfmac/fwil_types.h:961-965`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 2 | `version` | `__le16` | `linux/brcmfmac/fwil_types.h:961-965` |
| 2 | 2 | `length` | `__le16` | `linux/brcmfmac/fwil_types.h:961-965` |
| 4 | 1760 | `pmk` | `struct brcmf_pmksa_v2[16]` | BRCMF_MAXPMKID = 16 (`linux/brcmfmac/fwil_types.h:156`); 110 bytes each |

Size check: compiled (gcc, x86-64; sizeof = 1764, alignment = 2)

### `brcmf_pmk_op_v3_le` (linux)
Named variable "pmkid_info" (set), `linux/brcmfmac/cfg80211.c:4376-4408`; callers: set_pmksa (`linux/brcmfmac/cfg80211.c:4449-4450`), del_pmksa (`linux/brcmfmac/cfg80211.c:4493-4494`) and flush (`linux/brcmfmac/cfg80211.c:4535`), all gated on BRCMF_FEAT_PMKID_V3; linux always sends sizeof(*pmk_op), the full 16-entry record of 1800 bytes, while the length field describes only the used part `linux/brcmfmac/cfg80211.c:4406-4408`; the element size 112 rests on ETH_ALEN = 6 (recalled, not in these sources) and on WLAN_PMKID_LEN = 16, WLAN_PMK_LEN_SUITE_B_192 = 48 and IEEE80211_MAX_SSID_LEN = 32 `linux-headers/ieee80211.h:2271`, `linux-headers/ieee80211.h:2274`, `linux-headers/ieee80211.h:227`, `linux/brcmfmac/fwil_types.h:931-941`; not packed; 1800 bytes; little-endian (__le16/__le32 fields; u8 fields have no byte order); defined at `linux/brcmfmac/fwil_types.h:974-980`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 2 | `version` | `__le16` | BRCMF_PMKSA_VER_3 = 3 (`linux/brcmfmac/fwil_types.h:178`, set at `linux/brcmfmac/cfg80211.c:4384`) |
| 2 | 2 | `length` | `__le16` | offsetof(pmk) + one entry when a single PMK is operated on (`linux/brcmfmac/cfg80211.c:4377`, `linux/brcmfmac/cfg80211.c:4392`, `linux/brcmfmac/cfg80211.c:4406`) |
| 4 | 2 | `count` | `__le16` | 0 = flush whole list, 1 = single entry (`linux/brcmfmac/cfg80211.c:4386-4391`) |
| 6 | 2 | `pad` | `__le16` | explicit member named 'pad' `linux/brcmfmac/fwil_types.h:974-980` |
| 8 | 1792 | `pmk` | `struct brcmf_pmksa_v3[16]` | BRCMF_MAXPMKID = 16 (`linux/brcmfmac/fwil_types.h:156`); 112 bytes each |

Size check: compiled (gcc, x86-64; sizeof = 1800, alignment = 4)

### `brcmf_pno_param_le` (linux)
Named variable "pfn_set" (set), `linux/brcmfmac/pno.c:106-147`; field meanings are in the kernel-doc `linux/brcmfmac/fwil_types.h:982-998`; not packed; 24 bytes; little-endian (__le16/__le32 fields; u8 fields have no byte order); defined at `linux/brcmfmac/fwil_types.h:999-1010`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `version` | `__le32` | `linux/brcmfmac/fwil_types.h:999-1010`; BRCMF_PNO_VERSION = 2 `linux/brcmfmac/pno.c:16` |
| 4 | 4 | `scan_freq` | `__le32` | `linux/brcmfmac/fwil_types.h:999-1010` |
| 8 | 4 | `lost_network_timeout` | `__le32` | seconds `linux/brcmfmac/fwil_types.h:999-1010` |
| 12 | 2 | `flags` | `__le16` | `linux/brcmfmac/fwil_types.h:999-1010` |
| 14 | 2 | `rssi_margin` | `__le16` | `linux/brcmfmac/fwil_types.h:999-1010` |
| 16 | 1 | `bestn` | `u8` | `linux/brcmfmac/fwil_types.h:999-1010` |
| 17 | 1 | `mscan` | `u8` | `linux/brcmfmac/fwil_types.h:999-1010` |
| 18 | 1 | `repeat` | `u8` | `linux/brcmfmac/fwil_types.h:999-1010` |
| 19 | 1 | `exp` | `u8` | `linux/brcmfmac/fwil_types.h:999-1010` |
| 20 | 4 | `slow_freq` | `__le32` | `linux/brcmfmac/fwil_types.h:999-1010` |

Size check: compiled (gcc, x86-64; sizeof = 24, alignment = 4)

### `brcmf_pno_config_le` (linux)
Named variable "pfn_cfg" (set), `linux/brcmfmac/pno.c:93-99`; not packed; 140 bytes; little-endian (__le16/__le32 fields; u8 fields have no byte order); defined at `linux/brcmfmac/fwil_types.h:1020-1025`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `reporttype` | `__le32` | `linux/brcmfmac/fwil_types.h:1020-1025` |
| 4 | 4 | `channel_num` | `__le32` | `linux/brcmfmac/fwil_types.h:1020-1025` |
| 8 | 128 | `channel_list` | `__le16[64]` | BRCMF_NUMCHANNELS = 64 (`linux/brcmfmac/fwil_types.h:157`) |
| 136 | 4 | `flags` | `__le32` | reserved `linux/brcmfmac/fwil_types.h:1020-1025` |

Size check: compiled (gcc, x86-64; sizeof = 140, alignment = 4)

### `brcmf_pno_net_param_le` (linux)
Named variable "pfn_add" (set), `linux/brcmfmac/pno.c:201-215`; 36 + 5 x 4 = 56, no padding; the size depends on no constant outside the source set `linux/brcmfmac/fwil_types.h:357-360`, `linux/brcmfmac/fwil_types.h:1037-1044`; linux fills every field and sends sizeof(pfn) = 56 bytes; SSID bytes past ssid_len are uninitialised stack memory `linux/brcmfmac/pno.c:201-215`; not packed; 56 bytes; little-endian (__le16/__le32 fields; u8 fields have no byte order); defined at `linux/brcmfmac/fwil_types.h:1037-1044`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 36 | `ssid` | `struct brcmf_ssid_le` | __le32 SSID_len + SSID[32], 36 bytes (`linux/brcmfmac/fwil_types.h:357-360`); IEEE80211_MAX_SSID_LEN = 32 `linux-headers/ieee80211.h:227` |
| 36 | 4 | `flags` | `__le32` | bit2: hidden (`linux/brcmfmac/fwil_types.h:1031`; BRCMF_PNO_HIDDEN_BIT 2 `linux/brcmfmac/pno.c:25`) |
| 40 | 4 | `infra` | `__le32` | `linux/brcmfmac/fwil_types.h:1037-1044` |
| 44 | 4 | `auth` | `__le32` | `linux/brcmfmac/fwil_types.h:1037-1044` |
| 48 | 4 | `wpa_auth` | `__le32` | `linux/brcmfmac/fwil_types.h:1037-1044` |
| 52 | 4 | `wsec` | `__le32` | `linux/brcmfmac/fwil_types.h:1037-1044` |

Size check: compiled (gcc, x86-64; sizeof = 56, alignment = 4)

### `brcmf_pno_net_info_le` (linux)
Entries appended after brcmf_pno_scanresults_le (v1) or brcmf_pno_scanresults_v2_le (v2) in the BRCMF_E_PFN_NET_FOUND event data, `linux/brcmfmac/cfg80211.c:3881-3900`; second consumer: brcmf_wowl_nd_results (`linux/brcmfmac/cfg80211.c:4085-4117`), which replaces the BRCMF_E_PFN_NET_FOUND handler while WoWL net-detect is armed (`linux/brcmfmac/cfg80211.c:4277-4280`); both handlers ignore event data shorter than one header plus one net_info entry (`linux/brcmfmac/cfg80211.c:3927`, `linux/brcmfmac/cfg80211.c:4095`); SSID/bssid compared against the host requests in brcmf_pno_get_bucket_map (`linux/brcmfmac/pno.c:565-590`, declared `linux/brcmfmac/pno.h:69-70`); not packed; 44 bytes; little-endian (__le16/__le32 fields; u8 fields have no byte order); defined at `linux/brcmfmac/fwil_types.h:1056-1063`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 6 | `bssid` | `u8[6]` | `linux/brcmfmac/fwil_types.h:1056-1063`; ETH_ALEN = 6 (recalled, not in these sources); whd has ETHER_ADDR_LEN 6 `whd/inc/whd_types.h:101` |
| 6 | 1 | `channel` | `u8` | channel number only `linux/brcmfmac/fwil_types.h:1056-1063` |
| 7 | 1 | `SSID_len` | `u8` | `linux/brcmfmac/fwil_types.h:1056-1063` |
| 8 | 32 | `SSID` | `u8[32]` | literal 32 in the source `linux/brcmfmac/fwil_types.h:1056-1063` |
| 40 | 2 | `RSSI` | `__le16` | dBm `linux/brcmfmac/fwil_types.h:1056-1063` |
| 42 | 2 | `timestamp` | `__le16` | age in seconds `linux/brcmfmac/fwil_types.h:1056-1063` |

Size check: compiled (gcc, x86-64; sizeof = 44, alignment = 2)

### `brcmf_pno_scanresults_le` (linux)
Event data of BRCMF_E_PFN_NET_FOUND, `linux/brcmfmac/cfg80211.c:3937-3945` (handler registered `linux/brcmfmac/cfg80211.c:7011`); second consumer: brcmf_wowl_nd_results (`linux/brcmfmac/cfg80211.c:4085-4117`), which replaces the BRCMF_E_PFN_NET_FOUND handler while WoWL net-detect is armed (`linux/brcmfmac/cfg80211.c:4277-4280`); both handlers ignore event data shorter than one header plus one net_info entry (`linux/brcmfmac/cfg80211.c:3927`, `linux/brcmfmac/cfg80211.c:4095`); header only; count entries of brcmf_pno_net_info_le (44 bytes each) follow `linux/brcmfmac/cfg80211.c:3881-3900`; a linux source comment says the PFN event is limited to fit 512 bytes, so several NET_FOUND events may arrive `linux/brcmfmac/cfg80211.c:3941-3943`; not packed; 12 bytes; little-endian (__le16/__le32 fields; u8 fields have no byte order); defined at `linux/brcmfmac/fwil_types.h:1072-1076`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `version` | `__le32` | 1 or 2 selects where the net_info array starts (`linux/brcmfmac/cfg80211.c:3887-3898`) |
| 4 | 4 | `status` | `__le32` | BRCMF_PNO_SCAN_COMPLETE = 1 (`linux/brcmfmac/pno.h:8`) expected, `linux/brcmfmac/cfg80211.c:3944` |
| 8 | 4 | `count` | `__le32` | number of brcmf_pno_net_info_le entries that follow `linux/brcmfmac/fwil_types.h:1072-1076` |

Size check: compiled (gcc, x86-64; sizeof = 12, alignment = 4)

### `brcmf_pno_scanresults_v2_le` (linux)
Version-2 form of the BRCMF_E_PFN_NET_FOUND event data header, `linux/brcmfmac/cfg80211.c:3894-3897`; no kernel-doc in the source `linux/brcmfmac/fwil_types.h:1078-1083`; not packed; 16 bytes; little-endian (__le16/__le32 fields; u8 fields have no byte order); defined at `linux/brcmfmac/fwil_types.h:1078-1083`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `version` | `__le32` | `linux/brcmfmac/fwil_types.h:1078-1083` |
| 4 | 4 | `status` | `__le32` | `linux/brcmfmac/fwil_types.h:1078-1083` |
| 8 | 4 | `count` | `__le32` | `linux/brcmfmac/fwil_types.h:1078-1083` |
| 12 | 4 | `scan_ch_bucket` | `__le32` | `linux/brcmfmac/fwil_types.h:1078-1083` |

Size check: compiled (gcc, x86-64; sizeof = 16, alignment = 4)

### `brcmf_pno_macaddr_le` (linux)
Named variable "pfn_macaddr" (set), `linux/brcmfmac/pno.c:158-190`; also issued as a GET with only version filled in, as the feature probe for BRCMF_FEAT_SCAN_RANDOM_MAC (`linux/brcmfmac/feature.c:294`, `linux/brcmfmac/feature.c:337-341`); not packed; 8 bytes; endianness not stated (u8 fields only); defined at `linux/brcmfmac/fwil_types.h:1092-1096`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 1 | `version` | `u8` | BRCMF_PFN_MACADDR_CFG_VER = 1 (`linux/brcmfmac/fwil_types.h:159`; set at `linux/brcmfmac/pno.c:174` and `linux/brcmfmac/feature.c:337`) |
| 1 | 1 | `flags` | `u8` | BRCMF_PFN_MAC_OUI_ONLY BIT(0), BRCMF_PFN_SET_MAC_UNASSOC BIT(1) (`linux/brcmfmac/fwil_types.h:160-161`); both set at `linux/brcmfmac/pno.c:175` |
| 2 | 6 | `mac` | `u8[6]` | randomised under the request mask, multicast bit cleared, locally-administered bit set (`linux/brcmfmac/pno.c:177-185`); ETH_ALEN = 6 (recalled, not in these sources); whd has ETHER_ADDR_LEN 6 `whd/inc/whd_types.h:101` |

Size check: compiled (gcc, x86-64; sizeof = 8, alignment = 1)

### `brcmf_dload_data_le` (linux)
Download named variables "clmload" (`linux/brcmfmac/common.c:193-194`), "txcapload" (`linux/brcmfmac/common.c:216-217`) and "calload" (`linux/brcmfmac/common.c:260-261`), sent in chunks by brcmf_c_download / brcmf_c_download_blob `linux/brcmfmac/common.c:102-159`; linux sends struct_size(dload_buf, data, len) = 12 + len bytes `linux/brcmfmac/common.c:114-115`; linux puts at most MAX_CHUNK_LEN = 1400 data bytes in a chunk `linux/brcmfmac/fwil_types.h:185`, `linux/brcmfmac/common.c:144-145`; not packed; variable size (12 fixed + flexible tail); little-endian (__le16/__le32 fields; u8 fields have no byte order); defined at `linux/brcmfmac/fwil_types.h:1106-1112`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 2 | `flag` | `__le16` | DLOAD_HANDLER_VER << DLOAD_FLAG_VER_SHIFT ORed with DL_BEGIN/DL_END (`linux/brcmfmac/common.c:108`, `linux/brcmfmac/common.c:129`, `linux/brcmfmac/common.c:148`); linux sets DL_BEGIN only on the first chunk and DL_END only on the last `linux/brcmfmac/common.c:129`, `linux/brcmfmac/common.c:144-155`; flag constants: DLOAD_HANDLER_VER 1, DLOAD_FLAG_VER_SHIFT 12, DL_BEGIN 2 (0x0002), DL_END 4 (0x0004), DL_TYPE_CLM 2 `linux/brcmfmac/fwil_types.h:187-194` |
| 2 | 2 | `dload_type` | `__le16` | DL_TYPE_CLM for all three named variables (`linux/brcmfmac/common.c:110`) |
| 4 | 4 | `len` | `__le32` | bytes of data in this chunk `linux/brcmfmac/fwil_types.h:1106-1112` |
| 8 | 4 | `crc` | `__le32` | set to 0 (`linux/brcmfmac/common.c:112`) |
| 12 | variable | `data` | `u8[]` | flexible array `linux/brcmfmac/fwil_types.h:1106-1112` |

Size check: compiled (gcc, x86-64; sizeof = 12, alignment = 4)

### `brcmf_pno_bssid_le` (linux)
Named variable "pfn_add_bssid" (set), `linux/brcmfmac/pno.c:224-232`; not packed; 8 bytes; little-endian (__le16/__le32 fields; u8 fields have no byte order); defined at `linux/brcmfmac/fwil_types.h:1120-1123`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 6 | `bssid` | `u8[6]` | `linux/brcmfmac/fwil_types.h:1120-1123`; ETH_ALEN = 6 (recalled, not in these sources); whd has ETHER_ADDR_LEN 6 `whd/inc/whd_types.h:101` |
| 6 | 2 | `flags` | `__le16` | `linux/brcmfmac/fwil_types.h:1120-1123` |

Size check: compiled (gcc, x86-64; sizeof = 8, alignment = 2)

### `brcmf_pktcnt_le` (linux)
Command BRCMF_C_GET_GET_PKTCNTS (get), `linux/brcmfmac/cfg80211.c:3137`, `linux/brcmfmac/cfg80211.c:3162-3175`; not packed; 20 bytes; little-endian (__le16/__le32 fields; u8 fields have no byte order); defined at `linux/brcmfmac/fwil_types.h:1134-1140`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `rx_good_pkt` | `__le32` | `linux/brcmfmac/fwil_types.h:1134-1140` |
| 4 | 4 | `rx_bad_pkt` | `__le32` | `linux/brcmfmac/fwil_types.h:1134-1140` |
| 8 | 4 | `tx_good_pkt` | `__le32` | `linux/brcmfmac/fwil_types.h:1134-1140` |
| 12 | 4 | `tx_bad_pkt` | `__le32` | `linux/brcmfmac/fwil_types.h:1134-1140` |
| 16 | 4 | `rx_ocast_good_pkt` | `__le32` | unicast packets destined for others `linux/brcmfmac/fwil_types.h:1134-1140` |

Size check: compiled (gcc, x86-64; sizeof = 20, alignment = 4)

### `brcmf_gtk_keyinfo_le` (linux)
Named variable "gtk_key_info" (set), `linux/brcmfmac/cfg80211.c:6045-6056`; not packed; 40 bytes; endianness not stated (byte arrays only); defined at `linux/brcmfmac/fwil_types.h:1149-1153`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 16 | `kck` | `u8[16]` | BRCMF_RSN_KCK_LENGTH = 16 (`linux/brcmfmac/fwil_types.h:165`) |
| 16 | 16 | `kek` | `u8[16]` | BRCMF_RSN_KEK_LENGTH = 16 (`linux/brcmfmac/fwil_types.h:166`) |
| 32 | 8 | `replay_counter` | `u8[8]` | BRCMF_RSN_REPLAY_LEN = 8 (`linux/brcmfmac/fwil_types.h:167`) |

Size check: compiled (gcc, x86-64; sizeof = 40, alignment = 1)

### `brcmf_gscan_bucket_config` (linux)
Element of brcmf_gscan_config.bucket, named variable "pfn_gscan_cfg", `linux/brcmfmac/pno.c:436-440`; not packed; 8 bytes; little-endian (__le16/__le32 fields; u8 fields have no byte order); defined at `linux/brcmfmac/fwil_types.h:1168-1175`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 1 | `bucket_end_index` | `u8` | last channel index in brcmf_pno_config_le.channel_list `linux/brcmfmac/fwil_types.h:1168-1175` |
| 1 | 1 | `bucket_freq_multiple` | `u8` | `linux/brcmfmac/fwil_types.h:1168-1175` |
| 2 | 1 | `flag` | `u8` | `linux/brcmfmac/fwil_types.h:1168-1175` |
| 3 | 1 | `reserved` | `u8` | `linux/brcmfmac/fwil_types.h:1168-1175` |
| 4 | 2 | `repeat` | `__le16` | `linux/brcmfmac/fwil_types.h:1168-1175` |
| 6 | 2 | `max_freq_multiple` | `__le16` | `linux/brcmfmac/fwil_types.h:1168-1175` |

Size check: compiled (gcc, x86-64; sizeof = 8, alignment = 2)

### `brcmf_gscan_config` (linux)
Named variable "pfn_gscan_cfg" (set), `linux/brcmfmac/pno.c:395-440`; also sent zeroed with zero buckets as a feature probe at `linux/brcmfmac/feature.c:300-307`; linux skips the pfn_gscan_cfg probe for chip CY_CC_43439_CHIP_ID (and 43430, 4345, 43454), so linux does not send this record to a CYW43439 from the feature probe `linux/brcmfmac/feature.c:301-304`; where it does probe, linux sends sizeof(gscan_cfg) = 10 bytes, all zero `linux/brcmfmac/feature.c:300`, `linux/brcmfmac/feature.c:305-307`; not packed; variable size (10 fixed + flexible tail); little-endian (__le16/__le32 fields; u8 fields have no byte order); defined at `linux/brcmfmac/fwil_types.h:1208-1218`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 2 | `version` | `__le16` | BRCMF_GSCAN_CFG_VERSION = 2 (`linux/brcmfmac/fwil_types.h:1178`, set at `linux/brcmfmac/pno.c:431`) |
| 2 | 1 | `flags` | `u8` | enum brcmf_gscan_cfg_flags `linux/brcmfmac/fwil_types.h:1188-1192` |
| 3 | 1 | `buffer_threshold` | `u8` | `linux/brcmfmac/fwil_types.h:1208-1218` |
| 4 | 1 | `swc_nbssid_threshold` | `u8` | `linux/brcmfmac/fwil_types.h:1208-1218` |
| 5 | 1 | `swc_rssi_window_size` | `u8` | `linux/brcmfmac/fwil_types.h:1208-1218` |
| 6 | 1 | `count_of_channel_buckets` | `u8` | `linux/brcmfmac/fwil_types.h:1208-1218` |
| 7 | 1 | `retry_threshold` | `u8` | documented as '!unknown!' (`linux/brcmfmac/fwil_types.h:1204`) |
| 8 | 2 | `lost_ap_window` | `__le16` | documented as '!unknown!' (`linux/brcmfmac/fwil_types.h:1205`) |
| 10 | variable | `bucket` | `struct brcmf_gscan_bucket_config[]` | flexible array, 8 bytes per element, counted by count_of_channel_buckets `linux/brcmfmac/fwil_types.h:1208-1218` |

Size check: compiled (gcc, x86-64; sizeof = 10, alignment = 2)

### `brcmf_mkeep_alive_pkt_le` (linux)
Named variable "mkeep_alive" (set), `linux/brcmfmac/cfg80211.c:4296-4307`; the only record marked __packed in fwil_types.h (`linux/brcmfmac/fwil_types.h:1237`); without it the size would round to 12 (inferred) `linux/brcmfmac/fwil_types.h:1230-1237`; the only caller sends sizeof(kalive) = 11 bytes with no data `linux/brcmfmac/cfg80211.c:4307`; packed (__packed); variable size (11 fixed + flexible tail); little-endian (__le16/__le32 fields; u8 fields have no byte order); defined at `linux/brcmfmac/fwil_types.h:1230-1237`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 2 | `version` | `__le16` | set to 1 (`linux/brcmfmac/cfg80211.c:4302`) |
| 2 | 2 | `length` | `__le16` | length of fixed parameters; left 0 by the only caller (`linux/brcmfmac/cfg80211.c:4298-4305`) |
| 4 | 4 | `period_msec` | `__le32` | `linux/brcmfmac/fwil_types.h:1230-1237` |
| 8 | 2 | `len_bytes` | `__le16` | size of data; 0 = null-function keepalive (`linux/brcmfmac/cfg80211.c:4301-4304`) |
| 10 | 1 | `keep_alive_id` | `u8` | ID 0-3 (`linux/brcmfmac/fwil_types.h:1227`) |
| 11 | variable | `data` | `u8[]` | flexible array `linux/brcmfmac/fwil_types.h:1230-1237` |

Size check: compiled (gcc, x86-64; sizeof = 11, alignment = 1)

### `brcm_ethhdr` (linux)
Second header of every firmware event packet (member hdr of struct brcmf_event, `linux/brcmfmac/fweh.h:246`); packed (__packed); 10 bytes; big-endian (__be16 fields); defined at `linux/brcmfmac/fweh.h:215-221`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 2 | `subtype` | `__be16` | checked against the caller's stype when non-zero (`linux/brcmfmac/fweh.h:382-385`) |
| 2 | 2 | `length` | `__be16` | kernel-doc: 'TODO: length of appended data' (`linux/brcmfmac/fweh.h:210`); not read by linux's validation (`linux/brcmfmac/fweh.h:365-399`) |
| 4 | 1 | `version` | `u8` | `linux/brcmfmac/fweh.h:215-221` |
| 5 | 3 | `oui` | `u8[3]` | must equal BRCM_OUI "\x00\x10\x18" (`linux/brcmfmac/fweh.h:202`, `linux/brcmfmac/fweh.h:389-391`) |
| 8 | 2 | `usr_subtype` | `__be16` | must equal BCMILCP_BCM_SUBTYPE_EVENT = 1 (`linux/brcmfmac/fweh.h:203`, `linux/brcmfmac/fweh.h:394-396`) |

Size check: compiled (gcc, x86-64; sizeof = 10, alignment = 1)

### `brcmf_event_msg_be` (linux)
Common part of every firmware event (member msg of struct brcmf_event, `linux/brcmfmac/fweh.h:247`); event_type and datalen are read big-endian straight from the packet (`linux/brcmfmac/fweh.c:491-492`), the 48 bytes are copied into the queue item (`linux/brcmfmac/fweh.c:35`, `linux/brcmfmac/fweh.c:514`) and converted field by field to the host-order struct brcmf_event_msg in the worker (`linux/brcmfmac/fweh.c:286-298`); the size 48 is confirmed only given the recalled ETH_ALEN = 6 and IFNAMSIZ = 16 `linux/brcmfmac/fweh.h:223-235`; field meanings are in the kernel-doc of the host-order twin struct brcmf_event_msg `linux/brcmfmac/fweh.h:250-264`; packed (__packed); 48 bytes; big-endian (__be16/__be32 fields); defined at `linux/brcmfmac/fweh.h:223-235`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 2 | `version` | `__be16` | `linux/brcmfmac/fweh.h:223-235` |
| 2 | 2 | `flags` | `__be16` | BRCMF_EVENT_MSG_LINK 0x01, FLUSHTXQ 0x02, GROUP 0x04 (`linux/brcmfmac/fweh.h:113-115`) |
| 4 | 4 | `event_type` | `__be32` | firmware event code; read at `linux/brcmfmac/fweh.c:491` and bounds-checked against num_event_codes (`linux/brcmfmac/fweh.c:495`) |
| 8 | 4 | `status` | `__be32` | `linux/brcmfmac/fweh.h:223-235` |
| 12 | 4 | `reason` | `__be32` | `linux/brcmfmac/fweh.h:223-235` |
| 16 | 4 | `auth_type` | `__be32` | `linux/brcmfmac/fweh.h:223-235` |
| 20 | 4 | `datalen` | `__be32` | length of the event data that follows; rejected when > BRCMF_DCMD_MAXLEN or when datalen + 72 exceeds the packet (`linux/brcmfmac/fweh.c:492`, `linux/brcmfmac/fweh.c:501-503`) |
| 24 | 6 | `addr` | `u8[6]` | `linux/brcmfmac/fweh.h:223-235`; ETH_ALEN = 6 (recalled, not in these sources); whd has ETHER_ADDR_LEN 6 `whd/inc/whd_types.h:101` |
| 30 | 16 | `ifname` | `char[16]` | IFNAMSIZ `linux/brcmfmac/fweh.h:223-235`; IFNAMSIZ = 16 (recalled, not in these sources); whd has WHD_MSG_IFNAME_MAX 16 `whd/src/include/whd_events_int.h:444` |
| 46 | 1 | `ifidx` | `u8` | `linux/brcmfmac/fweh.h:223-235` |
| 47 | 1 | `bsscfgidx` | `u8` | `linux/brcmfmac/fweh.h:223-235` |

Size check: compiled (gcc, x86-64; sizeof = 48, alignment = 1)

Differences: none found against whd's record struct whd_event_msg: same field order and widths, declared under `#pragma pack(1)`, ifname is char[WHD_MSG_IFNAME_MAX] with WHD_MSG_IFNAME_MAX 16; whd's fields are plain uint16_t/uint32_t with no byte-order annotation in the declaration `whd/src/include/whd_events_int.h:444`, `whd/src/include/whd_events_int.h:466`, `whd/src/include/whd_events_int.h:483-496`.

### `brcmf_event` (linux)
The whole firmware event packet as received on the event/data path, validated in brcmf_fweh_process_skb `linux/brcmfmac/fweh.h:365-399`; then brcmf_fweh_process_event (`linux/brcmfmac/fweh.c:480-519`): event data starts at &event_packet[1], i.e. byte 72 (`linux/brcmfmac/fweh.c:493`), and eth.h_dest is kept as the interface address (`linux/brcmfmac/fweh.c:516`); the size 72 is confirmed only given the recalled 14-byte struct ethhdr `linux/brcmfmac/fweh.h:244-248`; minimum accepted packet length is sizeof(struct brcmf_event) `linux/brcmfmac/fweh.h:376`; packed (__packed); 72 bytes; big-endian (all multi-byte fields are __be); defined at `linux/brcmfmac/fweh.h:244-248`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 14 | `eth` | `struct ethhdr` | standard Ethernet header: dest[6], source[6], __be16 proto (layout recalled, not in these sources; whd's twin has the same three members, `whd/src/include/whd_events_int.h:476-481`); linux requires proto ETH_P_LINK_CTL, value not defined in these sources (`linux/brcmfmac/fweh.h:373`); struct ethhdr = 14 bytes (recalled, not in these sources); linux shows only the member name eth.h_dest `linux/brcmfmac/fweh.c:516` and ETH_HLEN `linux/brcmfmac/fweh.h:376` |
| 14 | 10 | `hdr` | `struct brcm_ethhdr` | 10 bytes `linux/brcmfmac/fweh.h:244-248` |
| 24 | 48 | `msg` | `struct brcmf_event_msg_be` | 48 bytes; event data (msg.datalen bytes) follows the struct `linux/brcmfmac/fweh.h:244-248` |

Size check: compiled (gcc, x86-64; sizeof = 72, alignment = 1)

### `brcmf_if_event` (linux)
Event data of BRCMF_E_IF: `linux/brcmfmac/fweh.c:131` and `linux/brcmfmac/cfg80211.c:6933` (registered `linux/brcmfmac/cfg80211.c:7013`); not packed; 5 bytes; endianness not stated (u8 fields only); defined at `linux/brcmfmac/fweh.h:279-285`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 1 | `ifidx` | `u8` | `linux/brcmfmac/fweh.h:279-285` |
| 1 | 1 | `action` | `u8` | BRCMF_E_IF_ADD 1, DEL 2, CHANGE 3 (`linux/brcmfmac/fweh.h:185-187`) |
| 2 | 1 | `flags` | `u8` | BRCMF_E_IF_FLAG_NOIF 1 (`linux/brcmfmac/fweh.h:190`) |
| 3 | 1 | `bsscfgidx` | `u8` | `linux/brcmfmac/fweh.h:279-285` |
| 4 | 1 | `role` | `u8` | BRCMF_E_IF_ROLE_STA 0, AP 1, WDS 2, P2P_GO 3, P2P_CLIENT 4 (`linux/brcmfmac/fweh.h:193-197`) |

Size check: compiled (gcc, x86-64; sizeof = 5, alignment = 1)

### `brcmf_proto_bcdc_dcmd` (linux)
Header of every control (command / named variable) message and its response on the control channel; built in brcmf_proto_bcdc_msg `linux/brcmfmac/bcdc.c:108-127`, response read into the same buffer at `linux/brcmfmac/bcdc.c:146-152`, checked in query_dcmd (`linux/brcmfmac/bcdc.c:157-213`) and set_dcmd (`linux/brcmfmac/bcdc.c:215-250`); the command payload follows the header directly `linux/brcmfmac/bcdc.c:108-127`; not packed; 16 bytes; little-endian (__le16/__le32 fields; u8 fields have no byte order); defined at `linux/brcmfmac/bcdc.c:25-31`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `cmd` | `__le32` | dongle command value `linux/brcmfmac/bcdc.c:25-31` |
| 4 | 4 | `len` | `__le32` | lower 16: output buflen; upper 16: input buflen (excludes header) (`linux/brcmfmac/bcdc.c:27-28`) |
| 8 | 4 | `flags` | `__le32` | BCDC_DCMD_ERROR 0x01, BCDC_DCMD_SET 0x02, interface index mask 0xF000 shift 12, request id mask 0xFFFF0000 shift 16 (`linux/brcmfmac/bcdc.c:34-39`); request id is ++reqid on send and must match in the response (`linux/brcmfmac/bcdc.c:122`, `linux/brcmfmac/bcdc.c:152`, `linux/brcmfmac/bcdc.c:183-194`, `linux/brcmfmac/bcdc.c:235-244`) |
| 12 | 4 | `status` | `__le32` | status code returned from the device; only read when BCDC_DCMD_ERROR is set in flags (`linux/brcmfmac/bcdc.c:209-210`, `linux/brcmfmac/bcdc.c:249-250`) |

Size check: compiled (gcc, x86-64; sizeof = 16, alignment = 4)

### `brcmf_proto_bcdc_header` (linux)
Header pushed on every data packet: brcmf_proto_bcdc_hdrpush `linux/brcmfmac/bcdc.c:256-278`; stripped on receive by brcmf_proto_bcdc_hdrpull `linux/brcmfmac/bcdc.c:280-330`, which rejects packets of <= 4 bytes and any version nibble other than BCDC_PROTO_VER 2 (`linux/brcmfmac/bcdc.c:290-294`, `linux/brcmfmac/bcdc.c:304-309`); BCDC_HEADER_LEN 4 (`linux/brcmfmac/bcdc.c:47`); not packed; 4 bytes; endianness not stated (u8 fields only); defined at `linux/brcmfmac/bcdc.c:71-76`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 1 | `flags` | `u8` | protocol version in the high nibble (BCDC_PROTO_VER 2, mask 0xf0, shift 4), BCDC_FLAG_SUM_GOOD 0x04, BCDC_FLAG_SUM_NEEDED 0x08 (`linux/brcmfmac/bcdc.c:48-52`) |
| 1 | 1 | `priority` | `u8` | 802.1d priority in bits 0-2 (BCDC_PRIORITY_MASK 0x7, `linux/brcmfmac/bcdc.c:53`); bits 4-7 USB flow control info (`linux/brcmfmac/bcdc.c:67`) |
| 2 | 1 | `flags2` | `u8` | dongle interface index in the low nibble (BCDC_FLAG2_IF_MASK 0x0f, `linux/brcmfmac/bcdc.c:54-55`) |
| 3 | 1 | `data_offset` | `u8` | kernel-doc: start of packet data, header is followed by firmware signals (`linux/brcmfmac/bcdc.c:69`). Unit is 4-byte words: receive skips data_offset << 2 bytes after the header (`linux/brcmfmac/bcdc.c:319-323`), and the tx signal header length is rounded to 4 and passed as data_offset >> 2 (`linux/brcmfmac/fwsignal.c:876-877`, `linux/brcmfmac/fwsignal.c:906`, `linux/brcmfmac/fwsignal.c:946-949`) |

Size check: compiled (gcc, x86-64; sizeof = 4, alignment = 1)

### `rte_log_le` (linux)
Console log descriptor inside struct rte_console, read from device RAM at console_addr + offsetof(struct rte_console, log_le): `linux/brcmfmac/sdio.c:2871-2873` and field by field at `linux/brcmfmac/sdio.c:2992-3006`; defined only under `#ifdef DEBUG` `linux/brcmfmac/sdio.c:62-109`; offsets in the table are for a 64-bit host (size 24); on a 32-bit host (compiled with -m32) the size is 16, no padding, _buf_compat at offset 12 `linux/brcmfmac/sdio.c:71-76`; only the first three __le32 words (12 bytes) have a device-side meaning that linux shows (inferred); linux reads sizeof(c->log_le), the host size `linux/brcmfmac/sdio.c:2872-2873`; the device-side record cannot be established from linux beyond those three words; the console poll that reads it is DEBUG-only `linux/brcmfmac/sdio.c:2856-2934`; not packed; 24 bytes; little-endian (__le16/__le32 fields; u8 fields have no byte order); plus one host pointer member; defined at `linux/brcmfmac/sdio.c:71-76`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `buf` | `__le32` | address of the log ring buffer in device memory (comment: can't be pointer on 64-bit hosts) `linux/brcmfmac/sdio.c:71-76` |
| 4 | 4 | `buf_size` | `__le32` | `linux/brcmfmac/sdio.c:71-76` |
| 8 | 4 | `idx` | `__le32` | write index into the ring buffer `linux/brcmfmac/sdio.c:71-76` |
| 12 | 4 | (pad) | `u8[4]` | alignment padding inserted by the compiler `linux/brcmfmac/sdio.c:71-76` |
| 16 | 8 | `_buf_compat` | `char *` | host pointer, 'Redundant pointer for backward compat.'; host-size dependent: 8 bytes at offset 16 on a 64-bit host (after 4 pad bytes), 4 bytes at offset 12 on a 32-bit host `linux/brcmfmac/sdio.c:71-76` |

Size check: compiled (gcc, x86-64; sizeof = 24, alignment = 8)

### `rte_console` (linux)
Firmware console structure in device RAM, located through sdpcm_shared_le.console_addr (`linux/brcmfmac/sdio.c:383`); the driver only reads at offsetof(log_le) = 8, log_le.buf_size = 12 and log_le.idx = 16 (`linux/brcmfmac/sdio.c:2871`, `linux/brcmfmac/sdio.c:2992`, `linux/brcmfmac/sdio.c:2999`, `linux/brcmfmac/sdio.c:3006`), all host-independent; defined only under `#ifdef DEBUG` `linux/brcmfmac/sdio.c:62-109`; offsets in the table are for a 64-bit host (size 168, 4 trailing pad bytes); on a 32-bit host (compiled with -m32) the size is 156, cbuf_idx at 24, cbuf at 28 `linux/brcmfmac/sdio.c:78-107`; only the first 20 bytes (vcons_in, vcons_out, the three __le32 log words) have a host-independent layout; the positions of cbuf_idx and cbuf in device memory are not established by linux `linux/brcmfmac/sdio.c:71-76`, `linux/brcmfmac/sdio.c:78-107`; not packed; 168 bytes; endianness not stated for vcons_in/vcons_out/cbuf_idx (plain uint); log_le is little endian; defined at `linux/brcmfmac/sdio.c:78-107`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `vcons_in` | `uint` | virtual UART: host writes the input length here after writing a line into cbuf `linux/brcmfmac/sdio.c:78-107` |
| 4 | 4 | `vcons_out` | `uint` | currently unused per the source comment `linux/brcmfmac/sdio.c:78-107` |
| 8 | 24 | `log_le` | `struct rte_log_le` | output ring buffer descriptor; host-size dependent (24 bytes on 64-bit, 16 on 32-bit) `linux/brcmfmac/sdio.c:78-107` |
| 32 | 4 | `cbuf_idx` | `uint` | offset 32 on a 64-bit host, 24 on a 32-bit host `linux/brcmfmac/sdio.c:78-107` |
| 36 | 128 | `cbuf` | `char[128]` | CBUF_LEN 128 (`linux/brcmfmac/sdio.c:66`); console input line buffer; offset 36 on 64-bit host, 28 on 32-bit host |
| 164 | 4 | (pad) | `u8[4]` | trailing padding to the struct alignment of 8 `linux/brcmfmac/sdio.c:78-107` |

Size check: compiled (gcc, x86-64; sizeof = 168, alignment = 8)

### `brcmf_trap_info` (linux)
Trap record read from device RAM at sdpcm_shared.trap_addr when SDPCM_SHARED_TRAP (0x0400) is set in flags: `linux/brcmfmac/sdio.c:3040-3052`; defined only under `#ifdef DEBUG` `linux/brcmfmac/sdio.c:330-363`; BRCMF_TRAP_INFO_SIZE = 80 matches the size `linux/brcmfmac/sdio.c:64`; not packed; 80 bytes; little-endian (__le16/__le32 fields; u8 fields have no byte order); defined at `linux/brcmfmac/sdio.c:341-362`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `type` | `__le32` | `linux/brcmfmac/sdio.c:341-362` |
| 4 | 4 | `epc` | `__le32` | `linux/brcmfmac/sdio.c:341-362` |
| 8 | 4 | `cpsr` | `__le32` | `linux/brcmfmac/sdio.c:341-362` |
| 12 | 4 | `spsr` | `__le32` | `linux/brcmfmac/sdio.c:341-362` |
| 16 | 4 | `r0` | `__le32` | a1 `linux/brcmfmac/sdio.c:341-362` |
| 20 | 4 | `r1` | `__le32` | a2 `linux/brcmfmac/sdio.c:341-362` |
| 24 | 4 | `r2` | `__le32` | a3 `linux/brcmfmac/sdio.c:341-362` |
| 28 | 4 | `r3` | `__le32` | a4 `linux/brcmfmac/sdio.c:341-362` |
| 32 | 4 | `r4` | `__le32` | v1 `linux/brcmfmac/sdio.c:341-362` |
| 36 | 4 | `r5` | `__le32` | v2 `linux/brcmfmac/sdio.c:341-362` |
| 40 | 4 | `r6` | `__le32` | v3 `linux/brcmfmac/sdio.c:341-362` |
| 44 | 4 | `r7` | `__le32` | v4 `linux/brcmfmac/sdio.c:341-362` |
| 48 | 4 | `r8` | `__le32` | v5 `linux/brcmfmac/sdio.c:341-362` |
| 52 | 4 | `r9` | `__le32` | sb/v6 `linux/brcmfmac/sdio.c:341-362` |
| 56 | 4 | `r10` | `__le32` | sl/v7 `linux/brcmfmac/sdio.c:341-362` |
| 60 | 4 | `r11` | `__le32` | fp/v8 `linux/brcmfmac/sdio.c:341-362` |
| 64 | 4 | `r12` | `__le32` | ip `linux/brcmfmac/sdio.c:341-362` |
| 68 | 4 | `r13` | `__le32` | sp `linux/brcmfmac/sdio.c:341-362` |
| 72 | 4 | `r14` | `__le32` | lr `linux/brcmfmac/sdio.c:341-362` |
| 76 | 4 | `pc` | `__le32` | r15 `linux/brcmfmac/sdio.c:341-362` |

Size check: compiled (gcc, x86-64; sizeof = 80, alignment = 4)

### `sdpcm_shared_le` (linux)
Shared structure read from device RAM; linux reads its address from the last 32-bit word of RAM (at rambase + ramsize - 4, less srsize when save-restore capable with rambase 0), then reads sizeof(struct sdpcm_shared_le) = 64 bytes at that address: `linux/brcmfmac/sdio.c:1040-1066`; the record is defined unconditionally, but its only reader, brcmf_sdio_readshared, exists only under `#ifdef DEBUG`; a non-DEBUG linux build never reads it `linux/brcmfmac/sdio.c:1021-1103`; linux rejects the address word when it is 0 or when its high half is the inverse of its low half (the NVRAM length token) `linux/brcmfmac/sdio.c:1022-1025`, `linux/brcmfmac/sdio.c:1051-1060`; linux rejects a version above SDPCM_SHARED_VERSION `linux/brcmfmac/sdio.c:1081-1085`; linux copies flags, trap_addr, assert_exp_addr, assert_file_addr, assert_line, console_addr and msgtrace_addr into its host-order twin; tag and brpt_addr are not copied `linux/brcmfmac/sdio.c:1073-1079`; the host-order twin struct sdpcm_shared is host-internal `linux/brcmfmac/sdio.c:365`; not packed; 64 bytes; little-endian (__le16/__le32 fields; u8 fields have no byte order); defined at `linux/brcmfmac/sdio.c:377-387`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `flags` | `__le32` | low byte = version (SDPCM_SHARED_VERSION 0x0003, mask 0x00FF); ASSERT_BUILT 0x0100, ASSERT 0x0200, TRAP 0x0400 (`linux/brcmfmac/sdio.c:296-300`) |
| 4 | 4 | `trap_addr` | `__le32` | `linux/brcmfmac/sdio.c:377-387` |
| 8 | 4 | `assert_exp_addr` | `__le32` | `linux/brcmfmac/sdio.c:377-387` |
| 12 | 4 | `assert_file_addr` | `__le32` | `linux/brcmfmac/sdio.c:377-387` |
| 16 | 4 | `assert_line` | `__le32` | `linux/brcmfmac/sdio.c:377-387` |
| 20 | 4 | `console_addr` | `__le32` | address of struct rte_console `linux/brcmfmac/sdio.c:377-387` |
| 24 | 4 | `msgtrace_addr` | `__le32` | `linux/brcmfmac/sdio.c:377-387` |
| 28 | 32 | `tag` | `u8[32]` | `linux/brcmfmac/sdio.c:377-387` |
| 60 | 4 | `brpt_addr` | `__le32` | `linux/brcmfmac/sdio.c:377-387` |

Size check: compiled (gcc, x86-64; sizeof = 64, alignment = 4)

### `brcmf_p2p_disc_st_le` (linux)
Bsscfg named variable "p2p_state" (set), `linux/brcmfmac/p2p.c:564-575`; one pad byte follows state, and linux sends sizeof(discover_state) = 6 bytes `linux/brcmfmac/p2p.c:574-575`; the pad byte is uninitialised stack memory in that function `linux/brcmfmac/p2p.c:564-575`; not packed; 6 bytes; little-endian (__le16/__le32 fields; u8 fields have no byte order); defined at `linux/brcmfmac/p2p.c:105-109`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 1 | `state` | `u8` | enum brcmf_p2p_disc_state: SCAN 0, LISTEN 1, SEARCH 2 (`linux/brcmfmac/p2p.c:118-122`) |
| 1 | 1 | (pad) | `u8[1]` | alignment padding inserted by the compiler `linux/brcmfmac/p2p.c:105-109` |
| 2 | 2 | `chspec` | `__le16` | channel for LISTEN state `linux/brcmfmac/p2p.c:105-109` |
| 4 | 2 | `dwell` | `__le16` | dwell time in ms for LISTEN state `linux/brcmfmac/p2p.c:105-109` |

Size check: compiled (gcc, x86-64; sizeof = 6, alignment = 2)

### `brcmf_p2p_scan_le` (linux)
Bsscfg named variable "p2p_scan" (set), `linux/brcmfmac/p2p.c:675-780`; variable in practice: linux allocates offsetof(struct brcmf_p2p_scan_le, eparams.params_le.channel_list) + num_chans x 2 bytes; that offset is 76 (compiled) `linux/brcmfmac/p2p.c:675-685`; the 88-byte sizeof comes from the larger union member, brcmf_escan_params_le (84 bytes), which contains the v2 scan params `linux/brcmfmac/fwil_types.h:460-468`; compiled sizes: brcmf_scan_params_le 68, brcmf_scan_params_v2_le 76, brcmf_escan_params_le 84 `linux/brcmfmac/fwil_types.h:368-407`, `linux/brcmfmac/fwil_types.h:409-451`, `linux/brcmfmac/fwil_types.h:460-468`; linux only ever sets type 'E' `linux/brcmfmac/p2p.c:730`; IEEE80211_MAX_SSID_LEN = 32 `linux-headers/ieee80211.h:227`; ETH_ALEN = 6 (recalled, not in these sources); whd has ETHER_ADDR_LEN 6 `whd/inc/whd_types.h:101`; the sizes are confirmed only given the recalled ETH_ALEN and the recalled shape of the DECLARE_FLEX_ARRAY macro (used at `linux/brcmfmac/fwil_types.h:405`, defined in no file of the source set); not packed; 88 bytes; little-endian (__le16/__le32 fields; u8 fields have no byte order); defined at `linux/brcmfmac/p2p.c:132-139`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 1 | `type` | `u8` | 'E' or 'S' (`linux/brcmfmac/p2p.c:127`) |
| 1 | 3 | `reserved` | `u8[3]` | reserved (ignored) `linux/brcmfmac/p2p.c:132-139` |
| 4 | 84 | `eparams` | `struct brcmf_escan_params_le` | union alternative for type 'E'; `linux/brcmfmac/fwil_types.h:460-468` (version, action, sync_id, then scan params) |
| 4 | 68 | `sparams` | `struct brcmf_scan_params_le` | union alternative for type 'S'; `linux/brcmfmac/fwil_types.h:368-407` |

Size check: compiled (gcc, x86-64; sizeof = 88, alignment = 4)

### `brcmf_p2p_pub_act_frame` (linux)
802.11 P2P public action frame body inspected by the driver, never built: classifiers `linux/brcmfmac/p2p.c:218-264` (P2P and DPP), debug print `linux/brcmfmac/p2p.c:338-347`, received action frames `linux/brcmfmac/p2p.c:1426-1452`, and frames about to be transmitted `linux/brcmfmac/p2p.c:1638-1643` with offsetof(elts) = 8 used at `linux/brcmfmac/p2p.c:1697`; over-the-air 802.11 frame body carried through the firmware, not a firmware-specific record (inferred from the WLAN_* constants in the kernel-doc field values) `linux/brcmfmac/p2p.c:142-151`; linux inspects this frame and never builds it `linux/brcmfmac/p2p.c:218-264`; not packed; variable size (8 fixed + flexible tail); endianness not stated (u8 fields only); defined at `linux/brcmfmac/p2p.c:152-160`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 1 | `category` | `u8` | WLAN_CATEGORY_PUBLIC `linux/brcmfmac/p2p.c:152-160` |
| 1 | 1 | `action` | `u8` | WLAN_PUB_ACTION_VENDOR_SPECIFIC `linux/brcmfmac/p2p.c:152-160` |
| 2 | 3 | `oui` | `u8[3]` | P2P_OUI "\x50\x6F\x9A" (`linux/brcmfmac/p2p.c:49`) |
| 5 | 1 | `oui_type` | `u8` | WLAN_OUI_TYPE_WFA_P2P `linux/brcmfmac/p2p.c:152-160` |
| 6 | 1 | `subtype` | `u8` | P2P_PAF_* 0-8 (`linux/brcmfmac/p2p.c:70-79`) |
| 7 | 1 | `dialog_token` | `u8` | `linux/brcmfmac/p2p.c:152-160` |
| 8 | variable | `elts` | `u8[]` | flexible array of information elements `linux/brcmfmac/p2p.c:152-160` |

Size check: compiled (gcc, x86-64; sizeof = 8, alignment = 1)

### `brcmf_p2p_action_frame` (linux)
802.11 P2P action frame body parsed at `linux/brcmfmac/p2p.c:276-281` and `linux/brcmfmac/p2p.c:390`; over-the-air 802.11 frame body carried through the firmware, not a firmware-specific record (inferred from the kernel-doc field values) `linux/brcmfmac/p2p.c:163-171`; not packed; variable size (7 fixed + flexible tail); endianness not stated (u8 fields only); defined at `linux/brcmfmac/p2p.c:172-179`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 1 | `category` | `u8` | P2P_AF_CATEGORY 0x7f (`linux/brcmfmac/p2p.c:48`) |
| 1 | 3 | `oui` | `u8[3]` | P2P_OUI `linux/brcmfmac/p2p.c:172-179` |
| 4 | 1 | `type` | `u8` | WLAN_OUI_TYPE_WFA_P2P `linux/brcmfmac/p2p.c:172-179` |
| 5 | 1 | `subtype` | `u8` | P2P_AF_* 0-3 (`linux/brcmfmac/p2p.c:82-85`) |
| 6 | 1 | `dialog_token` | `u8` | `linux/brcmfmac/p2p.c:172-179` |
| 7 | variable | `elts` | `u8[]` | flexible array of information elements `linux/brcmfmac/p2p.c:172-179` |

Size check: compiled (gcc, x86-64; sizeof = 7, alignment = 1)

### `brcmf_p2psd_gas_pub_act_frame` (linux)
802.11 GAS public action frame body (P2P service discovery) parsed at `linux/brcmfmac/p2p.c:303-308`, `linux/brcmfmac/p2p.c:414`, `linux/brcmfmac/p2p.c:1474`; over-the-air 802.11 frame body carried through the firmware, not a firmware-specific record (inferred from the kernel-doc, which names it a GAS public action frame) `linux/brcmfmac/p2p.c:182-187`; not packed; variable size (3 fixed + flexible tail); endianness not stated (u8 fields only); defined at `linux/brcmfmac/p2p.c:189-194`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 1 | `category` | `u8` | 0x04 public action (P2PSD_ACTION_CATEGORY, `linux/brcmfmac/p2p.c:88`) |
| 1 | 1 | `action` | `u8` | GAS action ids 0x0a-0x0d (`linux/brcmfmac/p2p.c:89-92`); the struct kernel-doc instead says "0x6c Advertisement Protocol" (`linux/brcmfmac/p2p.c:185`), the code switches on the 0x0a-0x0d constants (`linux/brcmfmac/p2p.c:415-416`) |
| 2 | 1 | `dialog_token` | `u8` | `linux/brcmfmac/p2p.c:189-194` |
| 3 | variable | `query_data` | `u8[]` | flexible array `linux/brcmfmac/p2p.c:189-194` |

Size check: compiled (gcc, x86-64; sizeof = 3, alignment = 1)

### `SDPCM hardware header (frame tag)` (linux)
First 4 bytes of every SDIO frame in both directions; SDPCM_HWHDR_LEN 4 (`linux/brcmfmac/sdio.c:1330`); parsed in brcmf_sdio_hdparse `linux/brcmfmac/sdio.c:1381-1408`, written in brcmf_sdio_update_hwhdr `linux/brcmfmac/sdio.c:1482-1486`; field names are descriptive, the source has none (layout from the block comment `linux/brcmfmac/sdio.c:1303-1329` and the pack/parse code); an all-zero length and checksum means no more frames to read `linux/brcmfmac/sdio.c:1384-1388`; not a struct (byte layout from comment and accessor code); 4 bytes; little-endian (get_unaligned_le16 / cpu_to_le16, `linux/brcmfmac/sdio.c:1382-1383`, `linux/brcmfmac/sdio.c:1484-1485`); defined at `linux/brcmfmac/sdio.c:1311-1313`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 2 | `frame_length` | `le16` | frame length (`linux/brcmfmac/sdio.c:1312`); must be >= SDPCM_HDRLEN 12 (`linux/brcmfmac/sdio.c:1395`) |
| 2 | 2 | `checksum` | `le16` | bit-wise inverse of frame length (`linux/brcmfmac/sdio.c:1313`); verified as (u16)~(len ^ checksum) == 0 (`linux/brcmfmac/sdio.c:1389`); written as ~frm_length (`linux/brcmfmac/sdio.c:1485`) |

Size check: computed

### `SDPCM hardware extension header (tx glom only)` (linux)
Inserted between hardware header and software header on transmit only when bus->txglom is set (`linux/brcmfmac/sdio.c:1497-1503`); SDPCM_HWEXT_LEN 8 (`linux/brcmfmac/sdio.c:1331`); 'N/A for Rx or normal Tx' (`linux/brcmfmac/sdio.c:1315`); field names are descriptive, the source has none (layout from the block comment `linux/brcmfmac/sdio.c:1303-1329` and the pack/parse code); after transmit linux reads the tail padding back from the two bytes just before the software header to trim the packet `linux/brcmfmac/sdio.c:2290-2292`; not a struct (byte layout from comment and accessor code); 8 bytes; little-endian (two cpu_to_le32 words, `linux/brcmfmac/sdio.c:1498-1501`); defined at `linux/brcmfmac/sdio.c:1314-1320`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 2 | `packet_length` | `le16` | packet length excluding the hw frame tag (`linux/brcmfmac/sdio.c:1316`; hd_info->len - 4 at `linux/brcmfmac/sdio.c:1498`) |
| 2 | 1 | `reserved` | `u8` | reserved (`linux/brcmfmac/sdio.c:1317`) |
| 3 | 1 | `frame_flags` | `u8` | bit 0: last frame indication (`linux/brcmfmac/sdio.c:1318`; lastfrm << 24 at `linux/brcmfmac/sdio.c:1498`) |
| 4 | 2 | `reserved2` | `u8[2]` | reserved (`linux/brcmfmac/sdio.c:1319`) |
| 6 | 2 | `tail_pad` | `le16` | tail padding length (`linux/brcmfmac/sdio.c:1320`; tail_pad << 16 in the second word at `linux/brcmfmac/sdio.c:1500-1501`) |

Size check: computed

### `SDPCM software header` (linux)
Follows the hardware header (or the hardware extension header in tx glom mode) on every SDIO frame; SDPCM_SWHDR_LEN 8, SDPCM_HDRLEN 12 (`linux/brcmfmac/sdio.c:1332-1333`); parsed `linux/brcmfmac/sdio.c:1410-1479`, packed `linux/brcmfmac/sdio.c:1505-1511`; field names are descriptive, the source has none (layout from the block comment `linux/brcmfmac/sdio.c:1303-1329` and the pack/parse code); on transmit linux fills only sequence, channel and data_offset; every other bit of the 8 bytes is sent as 0 `linux/brcmfmac/sdio.c:1505-1511`; the source disagrees with itself on byte 1: the comment puts the channel in the 4 MSB `linux/brcmfmac/sdio.c:1323`; the mask macro puts it in bits 8-11 of the little-endian word, the low nibble of byte 1 `linux/brcmfmac/sdio.c:1337-1338`; the code uses the macro `linux/brcmfmac/sdio.c:1419`; linux expects SDPCM_PROT_VERSION 4 from the firmware-to-host mailbox `linux/brcmfmac/sdio.c:290`, `linux/brcmfmac/sdio.c:1155`; not a struct (byte layout from comment, mask macros and accessor code); 8 bytes; little-endian (two __le32 words read with le32_to_cpu, `linux/brcmfmac/sdio.c:1412`, `linux/brcmfmac/sdio.c:1462`); defined at `linux/brcmfmac/sdio.c:1321-1328`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 1 | `sequence` | `u8` | rx/tx sequence number; SDPCM_SEQ_MASK 0x000000ff of word 0 (`linux/brcmfmac/sdio.c:1335`, `linux/brcmfmac/sdio.c:1418`); wraps at 256 (`linux/brcmfmac/sdio.c:1336`) |
| 1 | 1 | `channel_and_flags` | `u8` | comment says '4 MSB Channel number, 4 LSB arbitrary flag' (`linux/brcmfmac/sdio.c:1323`), but the code masks the channel with SDPCM_CHANNEL_MASK 0x00000f00 shift 8, i.e. the LOW nibble of this byte (`linux/brcmfmac/sdio.c:1337-1338`, `linux/brcmfmac/sdio.c:1419`), and SDPCM_GLOMDESC tests bit 7 of this byte (`linux/brcmfmac/sdio.c:1344`). Channels: 0 control, 1 event, 2 data, 3 glom, 15 test (`linux/brcmfmac/sdio.c:1339-1343`); event-channel test helper `linux/brcmfmac/sdio.c:1360-1369`; channel 3 with bit 7 set carries the glom descriptor (`linux/brcmfmac/sdio.c:2020-2029`) |
| 2 | 1 | `next_length` | `u8` | length of next data frame, reserved for tx; SDPCM_NEXTLEN_MASK 0x00ff0000 shift 16 (`linux/brcmfmac/sdio.c:1345-1346`, `linux/brcmfmac/sdio.c:1455`). Unit is 16 bytes: the driver uses value << 4 as the next read length (`linux/brcmfmac/sdio.c:1456`, `linux/brcmfmac/sdio.c:1653`, `linux/brcmfmac/sdio.c:1923`, `linux/brcmfmac/sdio.c:2038`) |
| 3 | 1 | `data_offset` | `u8` | offset of the payload from the start of the frame; SDPCM_DOFFSET_MASK 0xff000000 shift 24 (`linux/brcmfmac/sdio.c:1347-1348`); must be >= 12 and <= frame length (`linux/brcmfmac/sdio.c:1440`); accessor brcmf_sdio_getdatoffset `linux/brcmfmac/sdio.c:1353-1358` |
| 4 | 1 | `flow_control` | `u8` | flow control bits, reserved for tx; SDPCM_FCMASK_MASK 0x000000ff of word 1 (`linux/brcmfmac/sdio.c:1349`, `linux/brcmfmac/sdio.c:1462-1463`) |
| 5 | 1 | `max_tx_sequence` | `u8` | maximum sequence number allowed by firmware for tx (credit window), N/A for tx packets; SDPCM_WINDOW_MASK 0x0000ff00 shift 8 (`linux/brcmfmac/sdio.c:1350-1351`, `linux/brcmfmac/sdio.c:1472`); a window more than 0x40 ahead of tx_seq is replaced by tx_seq + 2 (`linux/brcmfmac/sdio.c:1473-1476`) |
| 6 | 2 | `reserved` | `u8[2]` | reserved (`linux/brcmfmac/sdio.c:1328`); on tx the whole second word is written as 0 (`linux/brcmfmac/sdio.c:1511`) |

Size check: computed

### `SDPCM glom descriptor (superframe descriptor)` (linux)
Payload, after the 12-byte SDPCM header, of a received frame on SDPCM_GLOM_CHANNEL 3 whose software-header byte 1 has bit 7 set (SDPCM_GLOMDESC, `linux/brcmfmac/sdio.c:1344`, `linux/brcmfmac/sdio.c:2020-2029`); consumed by brcmf_sdio_rxglom `linux/brcmfmac/sdio.c:1534-1601`; not a C struct in linux and no comment block: defined only by the parsing code; the field name is the local variable name `linux/brcmfmac/sdio.c:1534-1601`; receive only in linux `linux/brcmfmac/sdio.c:1534-1601`; not a struct (byte layout from parsing code); variable size (0 fixed + flexible tail of 2-byte entries); little-endian (get_unaligned_le16, `linux/brcmfmac/sdio.c:1546`); defined at `linux/brcmfmac/sdio.c:1534-1601`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | variable | `sublen` | `le16[]` | one length per sub-frame of the superframe that follows; total descriptor length must be non-zero and even (`linux/brcmfmac/sdio.c:1536-1542`); each length must be >= SDPCM_HDRLEN 12 and the first >= 24 (`linux/brcmfmac/sdio.c:1549-1555`); the driver warns when a length is not a multiple of the scatter-gather alignment (`linux/brcmfmac/sdio.c:1556-1559`) and rounds the last read up to a block multiple (`linux/brcmfmac/sdio.c:1562-1568`) |

Size check: computed
