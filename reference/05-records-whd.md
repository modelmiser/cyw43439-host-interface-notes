# Wire records: whd

Field-by-field layouts of the records in Infineon's driver.

### `wl_ether_addr_t` (whd)
Building block: 6-byte MAC address embedded in other records in this header (for example wl_scan_params.bssid at `whd/src/include/whd_wlioctl.h:509`, scb_val_t.ea at `whd/src/include/whd_wlioctl.h:939`); struct tag is "ether_addr"; not packed (no packed attribute; the header's first `#pragma pack` is at `whd/src/include/whd_wlioctl.h:3864`, after the definition); 6 bytes (alignment 1; same on x86-64 and 32-bit ARM); single bytes only, so byte order does not apply; defined at `whd/src/include/whd_wlioctl.h:50-53`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 6 | `octet` | `uint8_t[ETHER_ADDR_LEN]` | ETHER_ADDR_LEN = 6 (`whd/inc/whd_types.h:101`) |

Size check: compiled

### `wl_ether_header` (whd)
No use site in whd/src or whd/inc outside this header by type name or struct tag (include_helium not covered; use in linux, c-driver and embassy unverified), so the command it belongs to is not stated in whd; not packed (no packed attribute; the header's first `#pragma pack` is at `whd/src/include/whd_wlioctl.h:3864`, after the definition); 14 bytes (alignment 2; same on x86-64 and 32-bit ARM); little-endian as whd treats it (inferred: plain uintN_t types, and whd's htod16/htod32/dtoh16/dtoh32 are identity unless IL_BIGENDIAN is defined `whd/src/include/whd_endian.h:20` `whd/src/include/whd_endian.h:45-48` `whd/src/include/whd_endian.h:54-57`); defined at `whd/src/include/whd_wlioctl.h:54-59`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 6 | `ether_dhost` | `uint8_t[ETHER_ADDR_LEN]` | |
| 6 | 6 | `ether_shost` | `uint8_t[ETHER_ADDR_LEN]` | |
| 12 | 2 | `ether_type` | `uint16_t` | ether_type byte order is not stated in the definition; an Ethernet header carries it big-endian on the air (recalled, not in these sources) |

Size check: compiled

### `wl_action_frame_t` (whd)
Embedded in wl_af_params (`whd/src/include/whd_wlioctl.h:73`), which is the "actframe" named variable (iovar) payload (see wl_af_params_t); WL_WIFI_ACTION_FRAME_SIZE = sizeof(struct wl_action_frame) (`whd/src/include/whd_wlioctl.h:466`); not packed (no packed attribute; the header's first `#pragma pack` is at `whd/src/include/whd_wlioctl.h:3864`, after the definition); 1052 bytes (alignment 4; same on x86-64 and 32-bit ARM); little-endian as whd treats it (inferred: plain uintN_t types, and whd's htod16/htod32/dtoh16/dtoh32 are identity unless IL_BIGENDIAN is defined `whd/src/include/whd_endian.h:20` `whd/src/include/whd_endian.h:45-48` `whd/src/include/whd_endian.h:54-57`); defined at `whd/src/include/whd_wlioctl.h:60-66`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 6 | `da` | `wl_ether_addr_t` | |
| 6 | 2 | `len` | `uint16_t` | |
| 8 | 4 | `packetId` | `uint32_t` | |
| 12 | 1040 | `data` | `uint8_t[ACTION_FRAME_SIZE]` | data is a fixed 1040-byte array (ACTION_FRAME_SIZE, `whd/src/include/whd_wlioctl.h:38`), not a flexible tail |

Size check: compiled

### `wl_af_params_t` (whd)
Set payload of named variable "actframe": buffer of WL_WIFI_AF_PARAMS_SIZE = sizeof(struct wl_af_params) (`whd/src/include/whd_wlioctl.h:115`) obtained for IOVAR_STR_ACTION_FRAME and memcpy-filled at `whd/src/whd_wifi_api.c:4340-4344`; IOVAR_STR_ACTION_FRAME = "actframe" at `whd/src/include/whd_wlioctl.h:1089`; public alias whd_af_params_t at `whd/inc/whd_types.h:142`; not packed (no packed attribute; the header's first `#pragma pack` is at `whd/src/include/whd_wlioctl.h:3864`, after the definition); 1068 bytes (alignment 4; same on x86-64 and 32-bit ARM); little-endian as whd treats it (inferred: plain uintN_t types, and whd's htod16/htod32/dtoh16/dtoh32 are identity unless IL_BIGENDIAN is defined `whd/src/include/whd_endian.h:20` `whd/src/include/whd_endian.h:45-48` `whd/src/include/whd_endian.h:54-57`); defined at `whd/src/include/whd_wlioctl.h:68-74`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `channel` | `uint32_t` | |
| 4 | 4 | `dwell_time` | `int32_t` | |
| 8 | 6 | `BSSID` | `struct ether_addr` | |
| 14 | 2 | (pad) | `uint8_t[2]` | implicit alignment padding inserted by the compiler; 2 bytes of implicit padding after BSSID because action_frame is 4-byte aligned |
| 16 | 1052 | `action_frame` | `wl_action_frame_t` | |

Size check: compiled

### `wl_rx_mgmt_data_t` (whd)
whd reads the event data of WLC_E_EXT_AUTH_FRAME_RX (188, `whd/src/include/whd_events_int.h:174`) as this header followed immediately by the management frame (`whd/src/whd_wifi_api.c:3077-3085`: frame = rxframe + 1, length = datalen - sizeof); not packed (no packed attribute; the header's first `#pragma pack` is at `whd/src/include/whd_wlioctl.h:3864`, after the definition); 16 bytes (alignment 4; same on x86-64 and 32-bit ARM); little-endian as whd treats it (inferred: plain uintN_t types, and whd's htod16/htod32/dtoh16/dtoh32 are identity unless IL_BIGENDIAN is defined `whd/src/include/whd_endian.h:20` `whd/src/include/whd_endian.h:45-48` `whd/src/include/whd_endian.h:54-57`); defined at `whd/src/include/whd_wlioctl.h:76-83`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 2 | `version` | `uint16_t` | |
| 2 | 2 | `channel` | `uint16_t` | |
| 4 | 4 | `rssi` | `int32_t` | |
| 8 | 4 | `mactime` | `uint32_t` | |
| 12 | 4 | `rate` | `uint32_t` | |

Size check: compiled

### `wl_wsec_info_tlv_t` (whd)
TLV element inside the "wsec_info" named variable payload (comment `whd/src/include/whd_wlioctl.h:85`); only offsetof(wl_wsec_info_tlv_t, data) is used, for the length calculation at `whd/src/whd_wifi_api.c:1695-1696`; the TLV itself is written through whd_xtlv_t (`whd/src/whd_wifi_api.c:1703-1710`); not packed (no packed attribute; the header's first `#pragma pack` is at `whd/src/include/whd_wlioctl.h:3864`, after the definition); variable size, 4 fixed bytes plus tail (sizeof = 6 counts one placeholder element of the tail; alignment 2; same on x86-64 and 32-bit ARM); little-endian as whd treats it (inferred: plain uintN_t types, and whd's htod16/htod32/dtoh16/dtoh32 are identity unless IL_BIGENDIAN is defined `whd/src/include/whd_endian.h:20` `whd/src/include/whd_endian.h:45-48` `whd/src/include/whd_endian.h:54-57`); defined at `whd/src/include/whd_wlioctl.h:86-90`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 2 | `type` | `uint16_t` | |
| 2 | 2 | `len` | `uint16_t` | |
| 4 | variable | `data` | `uint8_t[1]` | flexible tail declared as a one-element placeholder array; one element is 1 byte; data[1] is a one-element placeholder for a variable tail; sizeof (6) includes 1 placeholder byte and 1 tail pad byte; whd uses offsetof(..., data) = 4 as the fixed length |
| 5 | 1 | (pad) | `uint8_t[1]` | implicit tail padding to the struct alignment (2); counted by sizeof only, after the placeholder element |

Size check: compiled

### `wl_wsec_info_t` (whd)
Input/output data of named variable "wsec_info" (comment `whd/src/include/whd_wlioctl.h:92`; IOVAR_STR_WSEC_INFO = "wsec_info" at `whd/src/include/whd_wlioctl.h:1271`); set at `whd/src/whd_wifi_api.c:1698-1713` with version = WL_WSEC_INFO_VERSION (0x01, `whd/src/include/whd_wlioctl.h:103`) and one TLV of id WL_WSEC_INFO_BSS_ALGOS (`whd/src/include/whd_wlioctl.h:113`); not packed (no packed attribute; the header's first `#pragma pack` is at `whd/src/include/whd_wlioctl.h:3864`, after the definition); variable size, 4 fixed bytes plus tail (sizeof = 10 counts one placeholder element of the tail; alignment 2; same on x86-64 and 32-bit ARM); little-endian as whd treats it (inferred: plain uintN_t types, and whd's htod16/htod32/dtoh16/dtoh32 are identity unless IL_BIGENDIAN is defined `whd/src/include/whd_endian.h:20` `whd/src/include/whd_endian.h:45-48` `whd/src/include/whd_endian.h:54-57`); defined at `whd/src/include/whd_wlioctl.h:93-98`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 1 | `version` | `uint8_t` | |
| 1 | 2 | `pad` | `uint8_t[2]` | declared pad/reserved member (explicit in the source), not compiler padding; the sender does not clear the buffer itself: pad is never written and num_tlvs is incremented rather than assigned (`whd/src/whd_wifi_api.c:1698-1705`) |
| 3 | 1 | `num_tlvs` | `uint8_t` | |
| 4 | variable | `tlvs` | `wl_wsec_info_tlv_t[1]` | flexible tail declared as a one-element placeholder array; one element is 6 bytes; tlvs[1] is a one-element placeholder; fixed header is offsetof(tlvs) = 4 bytes, used as such at `whd/src/whd_wifi_api.c:1695` |

Size check: compiled

### `wl_he_omi_v1_t` (whd)
Payload of sub-command WL_HE_CMD_OMI (13, `whd/src/include/whd_wlioctl.h:129`) of named variable "he" (IOVAR_STR_HE at `whd/src/include/whd_wlioctl.h:1268`), carried inside a whd_xtlv_t: `whd/src/whd_wifi_api.c:4388-4404` (version = WL_HE_OMI_VER, length = sizeof - 2, xtlv id = WL_HE_CMD_OMI, xtlv len = sizeof); aliased as wl_he_omi_t at `whd/src/include/whd_wlioctl.h:152`; all single bytes, so no padding and no byte-order question; not packed (no packed attribute; the header's first `#pragma pack` is at `whd/src/include/whd_wlioctl.h:3864`, after the definition); 9 bytes (alignment 1; same on x86-64 and 32-bit ARM); single bytes only, so byte order does not apply; defined at `whd/src/include/whd_wlioctl.h:138-149`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 1 | `version` | `uint8_t` | |
| 1 | 1 | `length` | `uint8_t` | whd sets length = sizeof - 2 = 7 (`whd/src/whd_wifi_api.c:4389`) |
| 2 | 1 | `rx_nss` | `uint8_t` | |
| 3 | 1 | `chnl_wdth` | `uint8_t` | |
| 4 | 1 | `ul_mu_dis` | `uint8_t` | |
| 5 | 1 | `tx_nsts` | `uint8_t` | |
| 6 | 1 | `er_su_dis` | `uint8_t` | |
| 7 | 1 | `dl_mu_resound` | `uint8_t` | |
| 8 | 1 | `ul_mu_data_dis` | `uint8_t` | |

Size check: compiled

### `wl_twt_sdesc_t` (whd)
TWT setup descriptor (comment `whd/src/include/whd_wlioctl.h:194`), embedded in wl_twt_setup_t (`whd/src/include/whd_wlioctl.h:269`) for named variable "twt" sub-command WL_TWT_CMD_SETUP and in wl_twt_setup_cplt_t (`whd/src/include/whd_wlioctl.h:223`) for event WLC_E_TWT_SETUP; read from the event at `whd/src/whd_wifi_api.c:4434`; filled for the three setup senders at `whd/src/whd_wifi_api.c:4598-4619` `whd/src/whd_wifi_api.c:4670-4679` `whd/src/whd_wifi_api.c:4845-4852`; the event reader converts wake_time_h/l, wake_dur and wake_int with dtoh32 (`whd/src/whd_wifi_api.c:4452-4454`); no implicit padding; not packed (no packed attribute; the header's first `#pragma pack` is at `whd/src/include/whd_wlioctl.h:3864`, after the definition); 36 bytes (alignment 4; same on x86-64 and 32-bit ARM); little-endian as whd treats it (inferred: plain uintN_t types, and whd's htod16/htod32/dtoh16/dtoh32 are identity unless IL_BIGENDIAN is defined `whd/src/include/whd_endian.h:20` `whd/src/include/whd_endian.h:45-48` `whd/src/include/whd_endian.h:54-57`); defined at `whd/src/include/whd_wlioctl.h:195-216`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 1 | `setup_cmd` | `uint8_t` | |
| 1 | 1 | `flow_flags` | `uint8_t` | |
| 2 | 1 | `flow_id` | `uint8_t` | |
| 3 | 1 | `wake_type` | `uint8_t` | |
| 4 | 4 | `wake_time_h` | `uint32_t` | |
| 8 | 4 | `wake_time_l` | `uint32_t` | |
| 12 | 4 | `wake_dur` | `uint32_t` | |
| 16 | 4 | `wake_int` | `uint32_t` | |
| 20 | 4 | `btwt_persistence` | `uint32_t` | |
| 24 | 4 | `wake_int_max` | `uint32_t` | |
| 28 | 1 | `duty_cycle_min` | `uint8_t` | |
| 29 | 1 | `pad` | `uint8_t` | declared pad/reserved member (explicit in the source), not compiler padding |
| 30 | 1 | `bid` | `uint8_t` | |
| 31 | 1 | `channel` | `uint8_t` | |
| 32 | 1 | `negotiation_type` | `uint8_t` | |
| 33 | 1 | `frame_recomm` | `uint8_t` | |
| 34 | 2 | `li` | `uint16_t` | |

Size check: compiled

### `wl_twt_setup_cplt_t` (whd)
Event data of WLC_E_TWT_SETUP (157, `whd/src/include/whd_events_int.h:172`) as whd reads it: cast from event_data at `whd/src/whd_wifi_api.c:4430-4434`; anonymous struct; name is the typedef; not packed (no packed attribute; the header's first `#pragma pack` is at `whd/src/include/whd_wlioctl.h:3864`, after the definition); 48 bytes (alignment 4; same on x86-64 and 32-bit ARM); little-endian as whd treats it (inferred: plain uintN_t types, and whd's htod16/htod32/dtoh16/dtoh32 are identity unless IL_BIGENDIAN is defined `whd/src/include/whd_endian.h:20` `whd/src/include/whd_endian.h:45-48` `whd/src/include/whd_endian.h:54-57`); defined at `whd/src/include/whd_wlioctl.h:218-224`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 2 | `version` | `uint16_t` | |
| 2 | 2 | `length` | `uint16_t` | |
| 4 | 1 | `dialog` | `uint8_t` | |
| 5 | 3 | (pad) | `uint8_t[3]` | implicit alignment padding inserted by the compiler; 3 bytes of implicit padding after the 1-byte dialog because status is 4-byte aligned |
| 8 | 4 | `status` | `int32_t` | |
| 12 | 36 | `desc` | `wl_twt_sdesc_t` | |

Size check: compiled

### `wl_twt_setup_t` (whd)
Payload of sub-command WL_TWT_CMD_SETUP (1, `whd/src/include/whd_wlioctl.h:158`) of named variable "twt" (IOVAR_STR_TWT at `whd/src/include/whd_wlioctl.h:1269`), carried inside a whd_xtlv_t: `whd/src/whd_wifi_api.c:4596-4627` (individual TWT) and `whd/src/whd_wifi_api.c:4668-4687` (broadcast TWT join, negotiation type 3) and `whd/src/whd_wifi_api.c:4842-4860` (whd_wifi_btwt_config, negotiation type 2); version = WL_TWT_SETUP_VER (0, `whd/src/include/whd_wlioctl.h:257`); length = sizeof(wl_twt_setup_t) - 4; multi-byte members (version, length, desc.wake_dur, desc.wake_int, desc.wake_time_h/l) are assigned without htod16/htod32 at these sites (`whd/src/whd_wifi_api.c:4596-4619`); not packed (no packed attribute; the header's first `#pragma pack` is at `whd/src/include/whd_wlioctl.h:3864`, after the definition); 52 bytes (alignment 4; same on x86-64 and 32-bit ARM); little-endian as whd treats it (inferred: plain uintN_t types, and whd's htod16/htod32/dtoh16/dtoh32 are identity unless IL_BIGENDIAN is defined `whd/src/include/whd_endian.h:20` `whd/src/include/whd_endian.h:45-48` `whd/src/include/whd_endian.h:54-57`); defined at `whd/src/include/whd_wlioctl.h:260-273`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 2 | `version` | `uint16_t` | |
| 2 | 2 | `length` | `uint16_t` | length is "data length (starting after this field)" (`whd/src/include/whd_wlioctl.h:264`); whd sets sizeof - 4 = 48 (`whd/src/whd_wifi_api.c:4597`) |
| 4 | 6 | `peer` | `wl_ether_addr_t` | |
| 10 | 2 | `pad` | `uint8_t[2]` | declared pad/reserved member (explicit in the source), not compiler padding |
| 12 | 36 | `desc` | `wl_twt_sdesc_t` | |
| 48 | 2 | `dialog` | `uint16_t` | |
| 50 | 2 | `pad1` | `uint8_t[2]` | declared pad/reserved member (explicit in the source), not compiler padding |

Size check: compiled

### `wl_twt_teardesc_t` (whd)
TWT teardown descriptor (comment `whd/src/include/whd_wlioctl.h:280`), embedded in wl_twt_teardown_t (`whd/src/include/whd_wlioctl.h:297`); its flow_id is read from the WLC_E_TWT_TEARDOWN event at `whd/src/whd_wifi_api.c:4479-4480`; not packed (no packed attribute; the header's first `#pragma pack` is at `whd/src/include/whd_wlioctl.h:3864`, after the definition); 4 bytes (alignment 1; same on x86-64 and 32-bit ARM); single bytes only, so byte order does not apply; defined at `whd/src/include/whd_wlioctl.h:281-287`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 1 | `negotiation_type` | `uint8_t` | |
| 1 | 1 | `flow_id` | `uint8_t` | |
| 2 | 1 | `bid` | `uint8_t` | |
| 3 | 1 | `alltwt` | `uint8_t` | |

Size check: compiled

### `wl_twt_teardown_t` (whd)
Payload of sub-command WL_TWT_CMD_TEARDOWN (2, `whd/src/include/whd_wlioctl.h:159`) of named variable "twt", inside a whd_xtlv_t: `whd/src/whd_wifi_api.c:4714-4727`; whd also casts the event data of WLC_E_TWT_TEARDOWN (195, `whd/src/include/whd_events_int.h:177`) to this record: `whd/src/whd_wifi_api.c:4477-4479`; alignment is 2, so there is no padding: 18 bytes; the last four members are marked deprecated (`whd/src/include/whd_wlioctl.h:299`); not packed (no packed attribute; the header's first `#pragma pack` is at `whd/src/include/whd_wlioctl.h:3864`, after the definition); 18 bytes (alignment 2; same on x86-64 and 32-bit ARM); little-endian as whd treats it (inferred: plain uintN_t types, and whd's htod16/htod32/dtoh16/dtoh32 are identity unless IL_BIGENDIAN is defined `whd/src/include/whd_endian.h:20` `whd/src/include/whd_endian.h:45-48` `whd/src/include/whd_endian.h:54-57`); defined at `whd/src/include/whd_wlioctl.h:290-304`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 2 | `version` | `uint16_t` | |
| 2 | 2 | `length` | `uint16_t` | length set to sizeof - 4 = 14 (`whd/src/whd_wifi_api.c:4715`) |
| 4 | 6 | `peer` | `wl_ether_addr_t` | |
| 10 | 4 | `teardesc` | `wl_twt_teardesc_t` | |
| 14 | 1 | `flow_flags` | `uint8_t` | |
| 15 | 1 | `flow_id` | `uint8_t` | |
| 16 | 1 | `bid` | `uint8_t` | |
| 17 | 1 | `pad` | `uint8_t` | declared pad/reserved member (explicit in the source), not compiler padding |

Size check: compiled

### `wl_twt_infodesc_t` (whd)
TWT information descriptor (comment `whd/src/include/whd_wlioctl.h:306`), embedded twice in wl_twt_info_t (`whd/src/include/whd_wlioctl.h:340` and, through the alias wl_twt_idesc_t at `whd/src/include/whd_wlioctl.h:327`, `whd/src/include/whd_wlioctl.h:342`); aliased as wl_twt_idesc_t (`whd/src/include/whd_wlioctl.h:327`); not packed (no packed attribute; the header's first `#pragma pack` is at `whd/src/include/whd_wlioctl.h:3864`, after the definition); 16 bytes (alignment 4; same on x86-64 and 32-bit ARM); little-endian as whd treats it (inferred: plain uintN_t types, and whd's htod16/htod32/dtoh16/dtoh32 are identity unless IL_BIGENDIAN is defined `whd/src/include/whd_endian.h:20` `whd/src/include/whd_endian.h:45-48` `whd/src/include/whd_endian.h:54-57`); defined at `whd/src/include/whd_wlioctl.h:307-317`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 1 | `flow_flags` | `uint8_t` | |
| 1 | 1 | `flow_id` | `uint8_t` | |
| 2 | 2 | `pad` | `uint8_t[2]` | declared pad/reserved member (explicit in the source), not compiler padding |
| 4 | 4 | `next_twt_h` | `uint32_t` | |
| 8 | 4 | `next_twt_l` | `uint32_t` | |
| 12 | 1 | `wake_type` | `uint8_t` | |
| 13 | 3 | `pad1` | `uint8_t[3]` | declared pad/reserved member (explicit in the source), not compiler padding |

Size check: compiled

### `wl_twt_info_t` (whd)
Payload of sub-command WL_TWT_CMD_INFO (3, `whd/src/include/whd_wlioctl.h:160`) of named variable "twt", inside a whd_xtlv_t: `whd/src/whd_wifi_api.c:4768-4794`; version = WL_TWT_INFO_VER (0, `whd/src/include/whd_wlioctl.h:329`); length = sizeof(wl_twt_info_t) - 4; not packed (no packed attribute; the header's first `#pragma pack` is at `whd/src/include/whd_wlioctl.h:3864`, after the definition); 44 bytes (alignment 4; same on x86-64 and 32-bit ARM); little-endian as whd treats it (inferred: plain uintN_t types, and whd's htod16/htod32/dtoh16/dtoh32 are identity unless IL_BIGENDIAN is defined `whd/src/include/whd_endian.h:20` `whd/src/include/whd_endian.h:45-48` `whd/src/include/whd_endian.h:54-57`); defined at `whd/src/include/whd_wlioctl.h:332-343`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 2 | `version` | `uint16_t` | |
| 2 | 2 | `length` | `uint16_t` | length set to sizeof - 4 = 40 (`whd/src/whd_wifi_api.c:4769`) |
| 4 | 6 | `peer` | `wl_ether_addr_t` | |
| 10 | 2 | `pad` | `uint8_t[2]` | declared pad/reserved member (explicit in the source), not compiler padding |
| 12 | 16 | `infodesc` | `wl_twt_infodesc_t` | |
| 28 | 16 | `desc` | `wl_twt_idesc_t` | the trailing desc member is marked deprecated (`whd/src/include/whd_wlioctl.h:341`) |

Size check: compiled

### `whd_iov_buf_t` (whd)
Header of the "oce" and "mbo" named variable payloads (IOVAR_STR_OCE at `whd/src/include/whd_wlioctl.h:1276`, IOVAR_STR_MBO at `whd/src/include/whd_wlioctl.h:1274`): version / len / id set, then the XTLV body copied to data, at `whd/src/whd_wifi_api.c:4935-4942` (oce, WL_OCE_CMD_ENABLE), `whd/src/whd_wifi_api.c:4974-4981` (mbo add chan pref), `whd/src/whd_wifi_api.c:5005-5012` (mbo del chan pref), `whd/src/whd_wifi_api.c:5038-5045` (mbo send notif); version/len/id are assigned without htod16 at `whd/src/whd_wifi_api.c:4938-4940`; not packed (no packed attribute; the header's first `#pragma pack` is at `whd/src/include/whd_wlioctl.h:3864`, after the definition); variable size, 6 fixed bytes plus tail (sizeof = 8 counts one placeholder element of the tail; alignment 2; same on x86-64 and 32-bit ARM); little-endian as whd treats it (inferred: plain uintN_t types, and whd's htod16/htod32/dtoh16/dtoh32 are identity unless IL_BIGENDIAN is defined `whd/src/include/whd_endian.h:20` `whd/src/include/whd_endian.h:45-48` `whd/src/include/whd_endian.h:54-57`); defined at `whd/src/include/whd_wlioctl.h:421-427`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 2 | `version` | `uint16_t` | |
| 2 | 2 | `len` | `uint16_t` | |
| 4 | 2 | `id` | `uint16_t` | |
| 6 | variable | `data` | `uint16_t[1]` | flexible tail declared as a one-element placeholder array; one element is 2 bytes; data[1] of uint16_t is a placeholder for the body; fixed header = offsetof(data) = 6 bytes; whd sizes the buffer as sizeof(whd_iov_buf_t) + sizeof(body) = 8 + body (`whd/src/whd_wifi_api.c:4935` `whd/src/whd_wifi_api.c:4974`), that is, 2 bytes more than header + body, while the body is copied starting at offset 6 |

Size check: compiled

### `mbo_xtlv_t` (whd)
One XTLV with a single 32-bit value, used as the body after whd_iov_buf_t for named variable "oce" WL_OCE_CMD_ENABLE (`whd/src/whd_wifi_api.c:4924-4941`) and named variable "mbo" WL_MBO_CMD_SEND_NOTIF (`whd/src/whd_wifi_api.c:5020-5044`); also the element type of mbo_add_chan_pref_t / mbo_del_chan_pref_t; not packed (no packed attribute; the header's first `#pragma pack` is at `whd/src/include/whd_wlioctl.h:3864`, after the definition); 8 bytes (alignment 4; same on x86-64 and 32-bit ARM); little-endian as whd treats it (inferred: plain uintN_t types, and whd's htod16/htod32/dtoh16/dtoh32 are identity unless IL_BIGENDIAN is defined `whd/src/include/whd_endian.h:20` `whd/src/include/whd_endian.h:45-48` `whd/src/include/whd_endian.h:54-57`); defined at `whd/src/include/whd_wlioctl.h:429-434`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 2 | `id` | `uint16_t` | |
| 2 | 2 | `len` | `uint16_t` | |
| 4 | 4 | `data` | `uint32_t[1]` | data is uint32_t[1] and is used as one 32-bit value, so in whd this record is a fixed 8 bytes rather than a variable one |

Size check: compiled

### `mbo_add_chan_pref_t` (whd)
Body after whd_iov_buf_t for named variable "mbo" sub-command WL_MBO_CMD_ADD_CHAN_PREF (1, `whd/src/include/whd_wlioctl.h:380`): `whd/src/whd_wifi_api.c:4950-4981`; not packed (no packed attribute; the header's first `#pragma pack` is at `whd/src/include/whd_wlioctl.h:3864`, after the definition); 32 bytes (alignment 4; same on x86-64 and 32-bit ARM); little-endian as whd treats it (inferred: plain uintN_t types, and whd's htod16/htod32/dtoh16/dtoh32 are identity unless IL_BIGENDIAN is defined `whd/src/include/whd_endian.h:20` `whd/src/include/whd_endian.h:45-48` `whd/src/include/whd_endian.h:54-57`); defined at `whd/src/include/whd_wlioctl.h:437-442`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 8 | `opclass` | `mbo_xtlv_t` | |
| 8 | 8 | `chan` | `mbo_xtlv_t` | |
| 16 | 8 | `pref` | `mbo_xtlv_t` | |
| 24 | 8 | `reason` | `mbo_xtlv_t` | |

Size check: compiled

### `mbo_del_chan_pref_t` (whd)
Body after whd_iov_buf_t for named variable "mbo" sub-command WL_MBO_CMD_DEL_CHAN_PREF (2, `whd/src/include/whd_wlioctl.h:381`): `whd/src/whd_wifi_api.c:4989-5012`; not packed (no packed attribute; the header's first `#pragma pack` is at `whd/src/include/whd_wlioctl.h:3864`, after the definition); 16 bytes (alignment 4; same on x86-64 and 32-bit ARM); little-endian as whd treats it (inferred: plain uintN_t types, and whd's htod16/htod32/dtoh16/dtoh32 are identity unless IL_BIGENDIAN is defined `whd/src/include/whd_endian.h:20` `whd/src/include/whd_endian.h:45-48` `whd/src/include/whd_endian.h:54-57`); defined at `whd/src/include/whd_wlioctl.h:445-448`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 8 | `opclass` | `mbo_xtlv_t` | |
| 8 | 8 | `chan` | `mbo_xtlv_t` | |

Size check: compiled

### `whd_xtlv_t` (whd)
Generic id/len/data wrapper for sub-command named variables: "he" WL_HE_CMD_OMI (`whd/src/whd_wifi_api.c:4398-4404`); "he" WL_HE_CMD_BSSCOLOR (5, `whd/src/include/whd_wlioctl.h:127`) get at `whd/src/whd_wifi_api.c:4880-4886` and set at `whd/src/whd_wifi_api.c:4909-4916`, both with len = 1 and a buffer of sizeof(whd_xtlv_t) + 1 + 1 = 8 bytes; "twt" setup (`whd/src/whd_wifi_api.c:4621-4626` `whd/src/whd_wifi_api.c:4681-4686` `whd/src/whd_wifi_api.c:4854-4859`), teardown (`whd/src/whd_wifi_api.c:4721-4726`) and info (`whd/src/whd_wifi_api.c:4788-4793`); and the TLV inside "wsec_info" (`whd/src/whd_wifi_api.c:1703-1711`); not packed (no packed attribute; the header's first `#pragma pack` is at `whd/src/include/whd_wlioctl.h:3864`, after the definition); variable size, 4 fixed bytes plus tail (sizeof = 6 counts one placeholder element of the tail; alignment 2; same on x86-64 and 32-bit ARM); little-endian as whd treats it (inferred: plain uintN_t types, and whd's htod16/htod32/dtoh16/dtoh32 are identity unless IL_BIGENDIAN is defined `whd/src/include/whd_endian.h:20` `whd/src/include/whd_endian.h:45-48` `whd/src/include/whd_endian.h:54-57`); defined at `whd/src/include/whd_wlioctl.h:450-455`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 2 | `id` | `uint16_t` | id/len are assigned without htod16 in the he/twt paths (`whd/src/whd_wifi_api.c:4401-4402` `whd/src/whd_wifi_api.c:4624-4625`) and with htod16 in the wsec_info path (`whd/src/whd_wifi_api.c:1709-1710`) |
| 2 | 2 | `len` | `uint16_t` | |
| 4 | variable | `data` | `uint8_t[1]` | flexible tail declared as a one-element placeholder array; one element is 1 byte; data[1] is a placeholder; fixed header = 4 bytes (whd adds a literal "+ 4" to the payload size, for example `whd/src/whd_wifi_api.c:4621`); sizeof (6) includes the placeholder byte and one tail pad byte |
| 5 | 1 | (pad) | `uint8_t[1]` | implicit tail padding to the struct alignment (2); counted by sizeof only, after the placeholder element |

Size check: compiled

### `ssid_info_t` (whd)
No use site in whd/src or whd/inc outside this header by type name or struct tag (include_helium not covered; use in linux, c-driver and embassy unverified), so the command it belongs to is not stated in whd; 1-byte length, unlike wlc_ssid_t which has a 32-bit length (`whd/src/include/whd_wlioctl.h:496-500`); not packed (no packed attribute; the header's first `#pragma pack` is at `whd/src/include/whd_wlioctl.h:3864`, after the definition); 33 bytes (alignment 1; same on x86-64 and 32-bit ARM); single bytes only, so byte order does not apply; defined at `whd/src/include/whd_wlioctl.h:479-483`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 1 | `ssid_len` | `uint8_t` | |
| 1 | 32 | `ssid` | `uint8_t[32]` | |

Size check: compiled

### `cnt_rx_t` (whd)
No use site in whd/src or whd/inc outside this header by type name or struct tag (include_helium not covered; use in linux, c-driver and embassy unverified), so the command it belongs to is not stated in whd; not packed (no packed attribute; the header's first `#pragma pack` is at `whd/src/include/whd_wlioctl.h:3864`, after the definition); 8 bytes (alignment 4; same on x86-64 and 32-bit ARM); little-endian as whd treats it (inferred: plain uintN_t types, and whd's htod16/htod32/dtoh16/dtoh32 are identity unless IL_BIGENDIAN is defined `whd/src/include/whd_endian.h:20` `whd/src/include/whd_endian.h:45-48` `whd/src/include/whd_endian.h:54-57`); defined at `whd/src/include/whd_wlioctl.h:484-488`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `cnt_rxundec` | `uint32_t` | |
| 4 | 4 | `cnt_rxframe` | `uint32_t` | |

Size check: compiled

### `wlc_ssid_t` (whd)
Set payload of command WLC_SET_SSID (26, `whd/src/include/whd_wlioctl.h:1323`): `whd/src/whd_wifi_api.c:2478-2483` (SSID_len assigned with htod32 at `whd/src/whd_wifi_api.c:2481`); also the first member of wl_extjoin_params_t (`whd/src/include/whd_wlioctl.h:4261`), the "join" named variable payload, filled at `whd/src/whd_wifi_api.c:2350-2352` (SSID_len assigned without htod32); the first member of wl_join_params_t (`whd/src/include/whd_wlioctl.h:4253`), sent with WLC_SET_SSID as the fallback when "join" is unsupported (`whd/src/whd_wifi_api.c:2370-2386`, ssid copied at `whd/src/whd_wifi_api.c:2377`); and the first member of wl_scan_params_t (`whd/src/include/whd_wlioctl.h:508`); not packed (no packed attribute; the header's first `#pragma pack` is at `whd/src/include/whd_wlioctl.h:3864`, after the definition); 36 bytes (alignment 4; same on x86-64 and 32-bit ARM); little-endian as whd treats it (inferred: plain uintN_t types, and whd's htod16/htod32/dtoh16/dtoh32 are identity unless IL_BIGENDIAN is defined `whd/src/include/whd_endian.h:20` `whd/src/include/whd_endian.h:45-48` `whd/src/include/whd_endian.h:54-57`); defined at `whd/src/include/whd_wlioctl.h:496-500`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `SSID_len` | `uint32_t` | |
| 4 | 32 | `SSID` | `uint8_t[32]` | |

Size check: compiled

### `wl_scan_params_t` (whd)
Embedded as "params" in wl_escan_params_t (`whd/src/include/whd_wlioctl.h:553`), the "escan" named variable payload; fields filled at `whd/src/whd_wifi_api.c:3335-3381`; also embedded in wl_iscan_params_t (`whd/src/include/whd_wlioctl.h:531`); not packed (no packed attribute; the header's first `#pragma pack` is at `whd/src/include/whd_wlioctl.h:3864`, after the definition); variable size, 64 fixed bytes plus tail (sizeof = 68 counts one placeholder element of the tail; alignment 4; same on x86-64 and 32-bit ARM); little-endian as whd treats it (inferred: plain uintN_t types, and whd's htod16/htod32/dtoh16/dtoh32 are identity unless IL_BIGENDIAN is defined `whd/src/include/whd_endian.h:20` `whd/src/include/whd_endian.h:45-48` `whd/src/include/whd_endian.h:54-57`); defined at `whd/src/include/whd_wlioctl.h:506-518`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 36 | `ssid` | `wlc_ssid_t` | |
| 36 | 6 | `bssid` | `wl_ether_addr_t` | |
| 42 | 1 | `bss_type` | `int8_t` | |
| 43 | 1 | `scan_type` | `int8_t` | |
| 44 | 4 | `nprobes` | `int32_t` | |
| 48 | 4 | `active_time` | `int32_t` | |
| 52 | 4 | `passive_time` | `int32_t` | |
| 56 | 4 | `home_time` | `int32_t` | |
| 60 | 4 | `channel_num` | `int32_t` | |
| 64 | variable | `channel_list` | `uint16_t[1]` | flexible tail declared as a one-element placeholder array; one element is 2 bytes; channel_list[1] is a placeholder for channel_num chanspecs (and, per the count masks at `whd/src/include/whd_wlioctl.h:520-521`, SSIDs may follow; that layout is not spelled out in the definition); WL_SCAN_PARAMS_FIXED_SIZE = 64 (`whd/src/include/whd_wlioctl.h:519`) equals the compiled offsetof(channel_list); sizeof = 68 includes one placeholder entry and 2 tail pad bytes |
| 66 | 2 | (pad) | `uint8_t[2]` | implicit tail padding to the struct alignment (4); counted by sizeof only, after the placeholder element |

Size check: compiled

### `wl_iscan_params_t` (whd)
No use site in whd/src or whd/inc outside this header by type name or struct tag (include_helium not covered; use in linux, c-driver and embassy unverified), so the command it belongs to is not stated in whd; not packed (no packed attribute; the header's first `#pragma pack` is at `whd/src/include/whd_wlioctl.h:3864`, after the definition); variable size, 72 fixed bytes plus tail (sizeof = 76 counts one placeholder element of the tail; alignment 4; same on x86-64 and 32-bit ARM); little-endian as whd treats it (inferred: plain uintN_t types, and whd's htod16/htod32/dtoh16/dtoh32 are identity unless IL_BIGENDIAN is defined `whd/src/include/whd_endian.h:20` `whd/src/include/whd_endian.h:45-48` `whd/src/include/whd_endian.h:54-57`); defined at `whd/src/include/whd_wlioctl.h:526-532`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `version` | `uint32_t` | |
| 4 | 2 | `action` | `uint16_t` | |
| 6 | 2 | `scan_duration` | `uint16_t` | |
| 8 | variable | `params` | `wl_scan_params_t` | nested record that itself ends in a variable tail; 68 bytes in sizeof (one placeholder element counted); variable because params ends in channel_list; the 72 fixed bytes are offsetof(params) = 8 plus the 64 bytes of wl_scan_params_t before channel_list (`whd/src/include/whd_wlioctl.h:519`); the header's own WL_ISCAN_PARAMS_FIXED_SIZE is a different measure: offsetof(params) + sizeof(wlc_ssid_t) = 8 + 36 = 44, which ends after params.ssid (`whd/src/include/whd_wlioctl.h:533`) |

Size check: compiled

### `wl_scan_results_t` (whd)
Embedded in wl_iscan_results_t (`whd/src/include/whd_wlioctl.h:568`); no use site in whd/src or whd/inc outside this header by type name or struct tag (include_helium not covered; use in linux, c-driver and embassy unverified), so the command it belongs to is not stated in whd; not packed (no packed attribute; the header's first `#pragma pack` is at `whd/src/include/whd_wlioctl.h:3864`, after the definition); variable size, 12 fixed bytes plus tail (sizeof = 140 counts one placeholder element of the tail; alignment 4; same on x86-64 and 32-bit ARM); little-endian as whd treats it (inferred: plain uintN_t types, and whd's htod16/htod32/dtoh16/dtoh32 are identity unless IL_BIGENDIAN is defined `whd/src/include/whd_endian.h:20` `whd/src/include/whd_endian.h:45-48` `whd/src/include/whd_endian.h:54-57`); defined at `whd/src/include/whd_wlioctl.h:534-540`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `buflen` | `uint32_t` | |
| 4 | 4 | `version` | `uint32_t` | |
| 8 | 4 | `count` | `uint32_t` | |
| 12 | variable | `bss_info` | `wl_bss_info_t[1]` | flexible tail declared as a one-element placeholder array; one element is 128 bytes; bss_info[1] is a placeholder for count records of wl_bss_info_t (`whd/inc/whd_types.h:926-964`, compiled size 128, each record self-describing through its length field); WL_SCAN_RESULTS_FIXED_SIZE = 12 (`whd/src/include/whd_wlioctl.h:541`) equals offsetof(bss_info) |

Size check: compiled

### `wl_escan_params_t` (whd)
Set payload of named variable "escan" (IOVAR_STR_ESCAN at `whd/src/include/whd_wlioctl.h:1076`): start at `whd/src/whd_wifi_api.c:3264-3389` (version = ESCAN_REQ_VERSION, action = WL_SCAN_ACTION_START; size = offsetof(params) + WL_SCAN_PARAMS_FIXED_SIZE + channels*2), abort at `whd/src/whd_wifi_api.c:3405-3416` (sizeof(wl_escan_params_t), action = WL_SCAN_ACTION_ABORT); not packed (no packed attribute; the header's first `#pragma pack` is at `whd/src/include/whd_wlioctl.h:3864`, after the definition); variable size, 72 fixed bytes plus tail (sizeof = 76 counts one placeholder element of the tail; alignment 4; same on x86-64 and 32-bit ARM); little-endian as whd treats it (inferred: plain uintN_t types, and whd's htod16/htod32/dtoh16/dtoh32 are identity unless IL_BIGENDIAN is defined `whd/src/include/whd_endian.h:20` `whd/src/include/whd_endian.h:45-48` `whd/src/include/whd_endian.h:54-57`); defined at `whd/src/include/whd_wlioctl.h:548-554`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `version` | `uint32_t` | |
| 4 | 2 | `action` | `uint16_t` | |
| 6 | 2 | `sync_id` | `uint16_t` | |
| 8 | variable | `params` | `wl_scan_params_t` | nested record that itself ends in a variable tail; 68 bytes in sizeof (one placeholder element counted); variable because params ends in channel_list; whd sizes the start request as 8 + 64 + 2*channels (`whd/src/whd_wifi_api.c:3264` `whd/src/whd_wifi_api.c:3303`), so the 72 fixed bytes are offsetof(params) = 8 plus WL_SCAN_PARAMS_FIXED_SIZE = 64 (`whd/src/include/whd_wlioctl.h:519`); the header's own WL_ESCAN_PARAMS_FIXED_SIZE is a different measure: offsetof(params) + sizeof(wlc_ssid_t) = 8 + 36 = 44, which ends after params.ssid (`whd/src/include/whd_wlioctl.h:555`); whd/src *.c does not use it for the request size (`whd/src/whd_wifi_api.c:3264`); the abort request sends the full sizeof = 76 (`whd/src/whd_wifi_api.c:3405`) |

Size check: compiled

### `wl_escan_result_t` (whd)
Event data of WLC_E_ESCAN_RESULT (69, `whd/src/include/whd_events_int.h:105`) as whd reads it: the scan event list is { WLC_E_ESCAN_RESULT } at `whd/src/whd_wifi_api.c:161` and the handler casts event_data at `whd/src/whd_wifi_api.c:2638-2642`; bss_count read with dtoh16 and bss_info->version with dtoh32 at `whd/src/whd_wifi_api.c:2640-2642`; not packed (no packed attribute; the header's first `#pragma pack` is at `whd/src/include/whd_wlioctl.h:3864`, after the definition); variable size, 12 fixed bytes plus tail (sizeof = 140 counts one placeholder element of the tail; alignment 4; same on x86-64 and 32-bit ARM); little-endian as whd treats it (inferred: plain uintN_t types, and whd's htod16/htod32/dtoh16/dtoh32 are identity unless IL_BIGENDIAN is defined `whd/src/include/whd_endian.h:20` `whd/src/include/whd_endian.h:45-48` `whd/src/include/whd_endian.h:54-57`); defined at `whd/src/include/whd_wlioctl.h:556-563`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `buflen` | `uint32_t` | |
| 4 | 4 | `version` | `uint32_t` | |
| 8 | 2 | `sync_id` | `uint16_t` | |
| 10 | 2 | `bss_count` | `uint16_t` | |
| 12 | variable | `bss_info` | `wl_bss_info_t[1]` | flexible tail declared as a one-element placeholder array; one element is 128 bytes; bss_info[1] is a placeholder for bss_count records of wl_bss_info_t (`whd/inc/whd_types.h:926-964`, compiled size 128 before IEs); WL_ESCAN_RESULTS_FIXED_SIZE = sizeof - sizeof(wl_bss_info_t) = 12 (`whd/src/include/whd_wlioctl.h:564`) |

Size check: compiled

### `wl_iscan_results_t` (whd)
No use site in whd/src or whd/inc outside this header by type name or struct tag (include_helium not covered; use in linux, c-driver and embassy unverified), so the command it belongs to is not stated in whd; not packed (no packed attribute; the header's first `#pragma pack` is at `whd/src/include/whd_wlioctl.h:3864`, after the definition); variable size, 16 fixed bytes plus tail (sizeof = 144 counts one placeholder element of the tail; alignment 4; same on x86-64 and 32-bit ARM); little-endian as whd treats it (inferred: plain uintN_t types, and whd's htod16/htod32/dtoh16/dtoh32 are identity unless IL_BIGENDIAN is defined `whd/src/include/whd_endian.h:20` `whd/src/include/whd_endian.h:45-48` `whd/src/include/whd_endian.h:54-57`); defined at `whd/src/include/whd_wlioctl.h:565-569`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `status` | `uint32_t` | |
| 4 | variable | `results` | `wl_scan_results_t` | nested record that itself ends in a variable tail; 140 bytes in sizeof (one placeholder element counted); variable because results ends in bss_info; WL_ISCAN_RESULTS_FIXED_SIZE = 12 + offsetof(results) = 16 (`whd/src/include/whd_wlioctl.h:570-571`) |

Size check: compiled

### `wl_rateset_t` (whd)
Embedded in sta_info_t (`whd/src/include/whd_wlioctl.h:950`); no direct command use found in whd/src (include_helium not covered; use in linux, c-driver and embassy unverified); not packed (no packed attribute; the header's first `#pragma pack` is at `whd/src/include/whd_wlioctl.h:3864`, after the definition); 20 bytes (alignment 4; same on x86-64 and 32-bit ARM); little-endian as whd treats it (inferred: plain uintN_t types, and whd's htod16/htod32/dtoh16/dtoh32 are identity unless IL_BIGENDIAN is defined `whd/src/include/whd_endian.h:20` `whd/src/include/whd_endian.h:45-48` `whd/src/include/whd_endian.h:54-57`); defined at `whd/src/include/whd_wlioctl.h:573-577`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `count` | `uint32_t` | |
| 4 | 16 | `rates` | `uint8_t[WL_MAXRATES_IN_SET]` | |

Size check: compiled

### `wl_rateset_args_t` (whd)
No use site in whd/src or whd/inc outside this header by type name or struct tag (include_helium not covered; use in linux, c-driver and embassy unverified), so the command it belongs to is not stated in whd; not packed (no packed attribute; the header's first `#pragma pack` is at `whd/src/include/whd_wlioctl.h:3864`, after the definition); 36 bytes (alignment 4; same on x86-64 and 32-bit ARM); little-endian as whd treats it (inferred: plain uintN_t types, and whd's htod16/htod32/dtoh16/dtoh32 are identity unless IL_BIGENDIAN is defined `whd/src/include/whd_endian.h:20` `whd/src/include/whd_endian.h:45-48` `whd/src/include/whd_endian.h:54-57`); defined at `whd/src/include/whd_wlioctl.h:579-584`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `count` | `uint32_t` | |
| 4 | 16 | `rates` | `uint8_t[WL_MAXRATES_IN_SET]` | |
| 20 | 16 | `mcs` | `uint8_t[WL_MAXRATES_IN_SET]` | |

Size check: compiled

### `wl_uint32_list_t` (whd)
No use site in whd/src or whd/inc outside this header by type name or struct tag (include_helium not covered; use in linux, c-driver and embassy unverified), so the command it belongs to is not stated in whd; not packed (no packed attribute; the header's first `#pragma pack` is at `whd/src/include/whd_wlioctl.h:3864`, after the definition); variable size, 4 fixed bytes plus tail (sizeof = 8 counts one placeholder element of the tail; alignment 4; same on x86-64 and 32-bit ARM); little-endian as whd treats it (inferred: plain uintN_t types, and whd's htod16/htod32/dtoh16/dtoh32 are identity unless IL_BIGENDIAN is defined `whd/src/include/whd_endian.h:20` `whd/src/include/whd_endian.h:45-48` `whd/src/include/whd_endian.h:54-57`); defined at `whd/src/include/whd_wlioctl.h:613-617`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `count` | `uint32_t` | |
| 4 | variable | `element` | `uint32_t[1]` | flexible tail declared as a one-element placeholder array; one element is 4 bytes; element[1] is a placeholder for count entries |

Size check: compiled

### `wl_join_scan_params_t` (whd)
Member scan_params of wl_extjoin_params_t (`whd/src/include/whd_wlioctl.h:4259-4262`, inside the #pragma pack(1) region `whd/src/include/whd_wlioctl.h:4188-4289`), which is the set payload of named variable "join": buffer obtained with the literal "join" at `whd/src/whd_wifi_api.c:2345-2346` (IOVAR_STR_JOIN = "join" at `whd/src/include/whd_wlioctl.h:1142`), scan_type = 0 and nprobes / active_time / passive_time / home_time = -1 at `whd/src/whd_wifi_api.c:2355-2359`, sent at `whd/src/whd_wifi_api.c:2367`; this type is embedded at `whd/src/include/whd_wlioctl.h:4262` inside a #pragma pack(1) region (`whd/src/include/whd_wlioctl.h:4188-4289`); pack(1) there does not change this struct's own internal layout (it was defined outside the pragma), only its placement in the container; the -1 defaults are assigned without htod32 (`whd/src/whd_wifi_api.c:2356-2359`); in the packed container scan_params sits at offset 36, directly after the 36-byte ssid; not packed (no packed attribute; the header's first `#pragma pack` is at `whd/src/include/whd_wlioctl.h:3864`, after the definition); 20 bytes (alignment 4; same on x86-64 and 32-bit ARM); little-endian as whd treats it (inferred: plain uintN_t types, and whd's htod16/htod32/dtoh16/dtoh32 are identity unless IL_BIGENDIAN is defined `whd/src/include/whd_endian.h:20` `whd/src/include/whd_endian.h:45-48` `whd/src/include/whd_endian.h:54-57`); defined at `whd/src/include/whd_wlioctl.h:619-632`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 1 | `scan_type` | `uint8_t` | |
| 1 | 3 | (pad) | `uint8_t[3]` | implicit alignment padding inserted by the compiler; 3 bytes of implicit padding after the 1-byte scan_type when compiled standalone |
| 4 | 4 | `nprobes` | `int32_t` | |
| 8 | 4 | `active_time` | `int32_t` | |
| 12 | 4 | `passive_time` | `int32_t` | |
| 16 | 4 | `home_time` | `int32_t` | |

Size check: compiled

### `wlc_antselcfg_t` (whd)
No use site in whd/src or whd/inc outside this header by type name or struct tag (include_helium not covered; use in linux, c-driver and embassy unverified), so the command it belongs to is not stated in whd; anonymous struct; name is the typedef; ANT_SELCFG_MAX = 4 (`whd/src/include/whd_wlioctl.h:656`); not packed (no packed attribute; the header's first `#pragma pack` is at `whd/src/include/whd_wlioctl.h:3864`, after the definition); 5 bytes (alignment 1; same on x86-64 and 32-bit ARM); single bytes only, so byte order does not apply; defined at `whd/src/include/whd_wlioctl.h:661-665`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `ant_config` | `uint8_t[ANT_SELCFG_MAX]` | |
| 4 | 1 | `num_antcfg` | `uint8_t` | |

Size check: compiled

### `wl_country_t` (whd)
Payload of named variable "country" (IOVAR_STR_COUNTRY at `whd/src/include/whd_wlioctl.h:1073`): set at `whd/src/whd_management.c:189-211`, get at `whd/src/whd_wifi_api.c:7223-7234`; WLC_CNTRY_BUF_SZ = 4 (`whd/src/include/whd_wlioctl.h:667`); whd writes the two country letters as a 32-bit word into both ccode and country_abbrev and takes rev from the upper 16 bits of its country code, using -1 when that is 0 (`whd/src/whd_management.c:198-209`); not packed (no packed attribute; the header's first `#pragma pack` is at `whd/src/include/whd_wlioctl.h:3864`, after the definition); 12 bytes (alignment 4; same on x86-64 and 32-bit ARM); little-endian as whd treats it (inferred: plain uintN_t types, and whd's htod16/htod32/dtoh16/dtoh32 are identity unless IL_BIGENDIAN is defined `whd/src/include/whd_endian.h:20` `whd/src/include/whd_endian.h:45-48` `whd/src/include/whd_endian.h:54-57`); defined at `whd/src/include/whd_wlioctl.h:668-673`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `country_abbrev` | `char[WLC_CNTRY_BUF_SZ]` | |
| 4 | 4 | `rev` | `int32_t` | |
| 8 | 4 | `ccode` | `char[WLC_CNTRY_BUF_SZ]` | |

Size check: compiled

### `wl_channels_in_country_t` (whd)
No use site in whd/src or whd/inc outside this header by type name or struct tag (include_helium not covered; use in linux, c-driver and embassy unverified), so the command it belongs to is not stated in whd; not packed (no packed attribute; the header's first `#pragma pack` is at `whd/src/include/whd_wlioctl.h:3864`, after the definition); variable size, 16 fixed bytes plus tail (sizeof = 20 counts one placeholder element of the tail; alignment 4; same on x86-64 and 32-bit ARM); little-endian as whd treats it (inferred: plain uintN_t types, and whd's htod16/htod32/dtoh16/dtoh32 are identity unless IL_BIGENDIAN is defined `whd/src/include/whd_endian.h:20` `whd/src/include/whd_endian.h:45-48` `whd/src/include/whd_endian.h:54-57`); defined at `whd/src/include/whd_wlioctl.h:674-681`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `buflen` | `uint32_t` | |
| 4 | 4 | `band` | `uint32_t` | |
| 8 | 4 | `country_abbrev` | `int8_t[WLC_CNTRY_BUF_SZ]` | |
| 12 | 4 | `count` | `uint32_t` | |
| 16 | variable | `channel` | `uint32_t[1]` | flexible tail declared as a one-element placeholder array; one element is 4 bytes; channel[1] is a placeholder for count entries |

Size check: compiled

### `wl_country_list_t` (whd)
Request/response buffer of command WLC_GET_COUNTRY_LIST (261, `whd/src/include/whd_wlioctl.h:1537`): request fields filled at `whd/src/whd_wifi_api.c:7244-7268`, command issued at `whd/src/whd_wifi_api.c:7270`, returned count and 4-byte country entries read at `whd/src/whd_wifi_api.c:7272-7273`; not packed (no packed attribute; the header's first `#pragma pack` is at `whd/src/include/whd_wlioctl.h:3864`, after the definition); variable size, 16 fixed bytes plus tail (sizeof = 20 counts one placeholder element of the tail; alignment 4; same on x86-64 and 32-bit ARM); little-endian as whd treats it (inferred: plain uintN_t types, and whd's htod16/htod32/dtoh16/dtoh32 are identity unless IL_BIGENDIAN is defined `whd/src/include/whd_endian.h:20` `whd/src/include/whd_endian.h:45-48` `whd/src/include/whd_endian.h:54-57`); defined at `whd/src/include/whd_wlioctl.h:682-689`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `buflen` | `uint32_t` | |
| 4 | 4 | `band_set` | `uint32_t` | |
| 8 | 4 | `band` | `uint32_t` | |
| 12 | 4 | `count` | `uint32_t` | fields converted with htod32 before sending and count read back with dtoh32 (`whd/src/whd_wifi_api.c:7265-7273`); the returned entries are consumed as WLC_CNTRY_BUF_SZ (4) bytes each |
| 16 | variable | `country_abbrev` | `int8_t[1]` | flexible tail declared as a one-element placeholder array; one element is 1 byte; country_abbrev[1] is a placeholder for the returned list; sizeof (20) includes the placeholder byte and 3 tail pad bytes |
| 17 | 3 | (pad) | `uint8_t[3]` | implicit tail padding to the struct alignment (4); counted by sizeof only, after the placeholder element |

Size check: compiled

### `wl_rm_req_elt_t` (whd)
Element of wl_rm_req_t (`whd/src/include/whd_wlioctl.h:714`); no use site in whd/src or whd/inc outside this header by type name or struct tag (include_helium not covered; use in linux, c-driver and embassy unverified), so the command it belongs to is not stated in whd; not packed (no packed attribute; the header's first `#pragma pack` is at `whd/src/include/whd_wlioctl.h:3864`, after the definition); 20 bytes (alignment 4; same on x86-64 and 32-bit ARM); little-endian as whd treats it (inferred: plain uintN_t types, and whd's htod16/htod32/dtoh16/dtoh32 are identity unless IL_BIGENDIAN is defined `whd/src/include/whd_endian.h:20` `whd/src/include/whd_endian.h:45-48` `whd/src/include/whd_endian.h:54-57`); defined at `whd/src/include/whd_wlioctl.h:698-707`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 1 | `type` | `int8_t` | |
| 1 | 1 | `flags` | `int8_t` | |
| 2 | 2 | `chanspec` | `wl_chanspec_t` | |
| 4 | 4 | `token` | `uint32_t` | |
| 8 | 4 | `tsf_h` | `uint32_t` | |
| 12 | 4 | `tsf_l` | `uint32_t` | |
| 16 | 4 | `dur` | `uint32_t` | |

Size check: compiled

### `wl_rm_req_t` (whd)
No use site in whd/src or whd/inc outside this header by type name or struct tag (include_helium not covered; use in linux, c-driver and embassy unverified), so the command it belongs to is not stated in whd; holds two host pointers (cb, cb_arg), so the layout depends on pointer size and the record is probably not sent as-is (inferred); not packed (no packed attribute; the header's first `#pragma pack` is at `whd/src/include/whd_wlioctl.h:3864`, after the definition); variable size, 16 fixed bytes plus tail on a 32-bit target and 24 fixed on a 64-bit host (sizeof = 36 on 32-bit ARM and 48 on x86-64, counting one placeholder element of the tail; alignment 4 on the 32-bit target); little-endian as whd treats it (inferred: plain uintN_t types, and whd's htod16/htod32/dtoh16/dtoh32 are identity unless IL_BIGENDIAN is defined `whd/src/include/whd_endian.h:20` `whd/src/include/whd_endian.h:45-48` `whd/src/include/whd_endian.h:54-57`); defined at `whd/src/include/whd_wlioctl.h:708-715`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `token` | `uint32_t` | |
| 4 | 4 | `count` | `uint32_t` | |
| 8 | 4 | `cb` | `void *` | host pointer; size shown for a 32-bit target (8 on a 64-bit host) |
| 12 | 4 | `cb_arg` | `void *` | host pointer; size shown for a 32-bit target (8 on a 64-bit host) |
| 16 | variable | `req` | `wl_rm_req_elt_t[1]` | flexible tail declared as a one-element placeholder array; one element is 20 bytes; WL_RM_REQ_FIXED_LEN = offsetof(req) (`whd/src/include/whd_wlioctl.h:716`); on a 64-bit host cb is at offset 8, cb_arg at 16 and req at 24 |

Size check: compiled

### `wl_rm_rep_elt_t` (whd)
Element of wl_rm_rep_t (`whd/src/include/whd_wlioctl.h:740`); no use site in whd/src or whd/inc outside this header by type name or struct tag (include_helium not covered; use in linux, c-driver and embassy unverified), so the command it belongs to is not stated in whd; not packed (no packed attribute; the header's first `#pragma pack` is at `whd/src/include/whd_wlioctl.h:3864`, after the definition); variable size, 24 fixed bytes plus tail (sizeof = 28 counts one placeholder element of the tail; alignment 4; same on x86-64 and 32-bit ARM); little-endian as whd treats it (inferred: plain uintN_t types, and whd's htod16/htod32/dtoh16/dtoh32 are identity unless IL_BIGENDIAN is defined `whd/src/include/whd_endian.h:20` `whd/src/include/whd_endian.h:45-48` `whd/src/include/whd_endian.h:54-57`); defined at `whd/src/include/whd_wlioctl.h:717-728`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 1 | `type` | `int8_t` | |
| 1 | 1 | `flags` | `int8_t` | |
| 2 | 2 | `chanspec` | `wl_chanspec_t` | |
| 4 | 4 | `token` | `uint32_t` | |
| 8 | 4 | `tsf_h` | `uint32_t` | |
| 12 | 4 | `tsf_l` | `uint32_t` | |
| 16 | 4 | `dur` | `uint32_t` | |
| 20 | 4 | `len` | `uint32_t` | |
| 24 | variable | `data` | `uint8_t[1]` | flexible tail declared as a one-element placeholder array; one element is 1 byte; data[1] is a placeholder for len bytes; WL_RM_REP_ELT_FIXED_LEN = 24 (`whd/src/include/whd_wlioctl.h:729`) equals offsetof(data) |
| 25 | 3 | (pad) | `uint8_t[3]` | implicit tail padding to the struct alignment (4); counted by sizeof only, after the placeholder element |

Size check: compiled

### `wl_rm_rpi_rep_t` (whd)
No use site in whd/src or whd/inc outside this header by type name or struct tag (include_helium not covered; use in linux, c-driver and embassy unverified), so the command it belongs to is not stated in whd; not packed (no packed attribute; the header's first `#pragma pack` is at `whd/src/include/whd_wlioctl.h:3864`, after the definition); 16 bytes (alignment 1; same on x86-64 and 32-bit ARM); single bytes only, so byte order does not apply; defined at `whd/src/include/whd_wlioctl.h:731-735`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 8 | `rpi` | `uint8_t[WL_RPI_REP_BIN_NUM]` | |
| 8 | 8 | `rpi_max` | `int8_t[WL_RPI_REP_BIN_NUM]` | |

Size check: compiled

### `wl_rm_rep_t` (whd)
No use site in whd/src or whd/inc outside this header by type name or struct tag (include_helium not covered; use in linux, c-driver and embassy unverified), so the command it belongs to is not stated in whd; not packed (no packed attribute; the header's first `#pragma pack` is at `whd/src/include/whd_wlioctl.h:3864`, after the definition); variable size, 8 fixed bytes plus tail (sizeof = 36 counts one placeholder element of the tail; alignment 4; same on x86-64 and 32-bit ARM); little-endian as whd treats it (inferred: plain uintN_t types, and whd's htod16/htod32/dtoh16/dtoh32 are identity unless IL_BIGENDIAN is defined `whd/src/include/whd_endian.h:20` `whd/src/include/whd_endian.h:45-48` `whd/src/include/whd_endian.h:54-57`); defined at `whd/src/include/whd_wlioctl.h:736-741`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `token` | `uint32_t` | |
| 4 | 4 | `len` | `uint32_t` | |
| 8 | variable | `rep` | `wl_rm_rep_elt_t[1]` | flexible tail declared as a one-element placeholder array; one element is 28 bytes; rep[1] is a placeholder; WL_RM_REP_FIXED_LEN = 8 (`whd/src/include/whd_wlioctl.h:742`) equals offsetof(rep) |

Size check: compiled

### `wl_wsec_key_t` (whd)
No use site in whd/src or whd/inc outside this header by type name or struct tag (include_helium not covered; use in linux, c-driver and embassy unverified), so the command it belongs to is not stated in whd; DOT11_MAX_KEY_SIZE = 32 (`whd/src/include/whd_wlioctl.h:759`); not packed (no packed attribute; the header's first `#pragma pack` is at `whd/src/include/whd_wlioctl.h:3864`, after the definition); 164 bytes (alignment 4; same on x86-64 and 32-bit ARM); little-endian as whd treats it (inferred: plain uintN_t types, and whd's htod16/htod32/dtoh16/dtoh32 are identity unless IL_BIGENDIAN is defined `whd/src/include/whd_endian.h:20` `whd/src/include/whd_endian.h:45-48` `whd/src/include/whd_endian.h:54-57`); defined at `whd/src/include/whd_wlioctl.h:760-779`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `index` | `uint32_t` | |
| 4 | 4 | `len` | `uint32_t` | |
| 8 | 32 | `data` | `uint8_t[DOT11_MAX_KEY_SIZE]` | |
| 40 | 72 | `pad_1` | `uint32_t[18]` | declared pad/reserved member (explicit in the source), not compiler padding |
| 112 | 4 | `algo` | `uint32_t` | |
| 116 | 4 | `flags` | `uint32_t` | |
| 120 | 8 | `pad_2` | `uint32_t[2]` | declared pad/reserved member (explicit in the source), not compiler padding |
| 128 | 4 | `pad_3` | `int32_t` | declared pad/reserved member (explicit in the source), not compiler padding |
| 132 | 4 | `iv_initialized` | `int32_t` | |
| 136 | 4 | `pad_4` | `int32_t` | declared pad/reserved member (explicit in the source), not compiler padding |
| 140 | 8 | `rxiv` | `struct (anonymous)` | anonymous nested struct { uint32_t hi @0 (4 bytes); uint16_t lo @4 (2 bytes); 2 bytes tail padding }; rxiv is an anonymous nested struct { uint32_t hi; uint16_t lo; } of size 8 (2 tail pad bytes) |
| 148 | 8 | `pad_5` | `uint32_t[2]` | declared pad/reserved member (explicit in the source), not compiler padding |
| 156 | 6 | `ea` | `wl_ether_addr_t` | |
| 162 | 2 | (pad) | `uint8_t[2]` | implicit tail padding to the struct alignment (4); 2 bytes of tail padding after ea |

Size check: compiled

### `wsec_pmk_t` (whd)
Set payload of command WLC_SET_WSEC_PMK (268, `whd/src/include/whd_wlioctl.h:1544`): passphrase at `whd/src/whd_wifi_api.c:756-770`, PMK at `whd/src/whd_wifi_api.c:1153-1176`; also filled for the soft AP at `whd/src/whd_ap.c:484-503` (same command, issued at line 502; no memset of the buffer on this path); flags = WSEC_PASSPHRASE (bit 0, `whd/src/include/whd_wlioctl.h:785`) or 0; anonymous struct; name is the typedef; not packed (no packed attribute; the header's first `#pragma pack` is at `whd/src/include/whd_wlioctl.h:3864`, after the definition); 70 bytes (alignment 2; same on x86-64 and 32-bit ARM); little-endian as whd treats it (inferred: plain uintN_t types, and whd's htod16/htod32/dtoh16/dtoh32 are identity unless IL_BIGENDIAN is defined `whd/src/include/whd_endian.h:20` `whd/src/include/whd_endian.h:45-48` `whd/src/include/whd_endian.h:54-57`); defined at `whd/src/include/whd_wlioctl.h:786-791`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 2 | `key_len` | `uint16_t` | |
| 2 | 2 | `flags` | `uint16_t` | |
| 4 | 65 | `key` | `uint8_t[WSEC_MAX_PSK_LEN + 1]` | key is WSEC_MAX_PSK_LEN + 1 = 65 bytes (`whd/src/include/whd_wlioctl.h:781` `whd/src/include/whd_wlioctl.h:790`); 1 tail pad byte makes sizeof 70 and whd sends sizeof(wsec_pmk_t) |
| 69 | 1 | (pad) | `uint8_t[1]` | implicit tail padding to the struct alignment (2) |

Size check: compiled

### `wsec_sae_password_t` (whd)
Set payload of named variable "sae_password" (IOVAR_STR_SAE_PASSWORD at `whd/src/include/whd_wlioctl.h:1247`): `whd/src/whd_wifi_api.c:791-800`; WSEC_MAX_SAE_PASSWORD_LEN = 128 (`whd/src/include/whd_wlioctl.h:793`); anonymous struct; name is the typedef; not packed (no packed attribute; the header's first `#pragma pack` is at `whd/src/include/whd_wlioctl.h:3864`, after the definition); 130 bytes (alignment 2; same on x86-64 and 32-bit ARM); little-endian as whd treats it (inferred: plain uintN_t types, and whd's htod16/htod32/dtoh16/dtoh32 are identity unless IL_BIGENDIAN is defined `whd/src/include/whd_endian.h:20` `whd/src/include/whd_endian.h:45-48` `whd/src/include/whd_endian.h:54-57`); defined at `whd/src/include/whd_wlioctl.h:794-798`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 2 | `password_len` | `uint16_t` | |
| 2 | 128 | `password` | `uint8_t[WSEC_MAX_SAE_PASSWORD_LEN]` | |

Size check: compiled

### `pmkid_cand_t` (whd)
Element of pmkid_cand_list_t (`whd/src/include/whd_wlioctl.h:861`); no use site in whd/src or whd/inc outside this header by type name or struct tag (include_helium not covered; use in linux, c-driver and embassy unverified), so the command it belongs to is not stated in whd; not packed (no packed attribute; the header's first `#pragma pack` is at `whd/src/include/whd_wlioctl.h:3864`, after the definition); 7 bytes (alignment 1; same on x86-64 and 32-bit ARM); single bytes only, so byte order does not apply; defined at `whd/src/include/whd_wlioctl.h:853-857`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 6 | `BSSID` | `wl_ether_addr_t` | |
| 6 | 1 | `preauth` | `uint8_t` | |

Size check: compiled

### `pmkid_cand_list_t` (whd)
No use site in whd/src or whd/inc outside this header by type name or struct tag (include_helium not covered; use in linux, c-driver and embassy unverified), so the command it belongs to is not stated in whd; not packed (no packed attribute; the header's first `#pragma pack` is at `whd/src/include/whd_wlioctl.h:3864`, after the definition); variable size, 4 fixed bytes plus tail (sizeof = 12 counts one placeholder element of the tail; alignment 4; same on x86-64 and 32-bit ARM); little-endian as whd treats it (inferred: plain uintN_t types, and whd's htod16/htod32/dtoh16/dtoh32 are identity unless IL_BIGENDIAN is defined `whd/src/include/whd_endian.h:20` `whd/src/include/whd_endian.h:45-48` `whd/src/include/whd_endian.h:54-57`); defined at `whd/src/include/whd_wlioctl.h:858-862`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `npmkid_cand` | `uint32_t` | |
| 4 | variable | `pmkid_cand` | `pmkid_cand_t[1]` | flexible tail declared as a one-element placeholder array; one element is 7 bytes; pmkid_cand[1] is a placeholder for npmkid_cand 7-byte entries; sizeof (12) includes one entry and 1 tail pad byte |
| 11 | 1 | (pad) | `uint8_t[1]` | implicit tail padding to the struct alignment (4); counted by sizeof only, after the placeholder element |

Size check: compiled

### `wl_led_info_t` (whd)
No use site in whd/src or whd/inc outside this header by type name or struct tag (include_helium not covered; use in linux, c-driver and embassy unverified), so the command it belongs to is not stated in whd; not packed (no packed attribute; the header's first `#pragma pack` is at `whd/src/include/whd_wlioctl.h:3864`, after the definition); 12 bytes (alignment 4; same on x86-64 and 32-bit ARM); little-endian as whd treats it (inferred: plain uintN_t types, and whd's htod16/htod32/dtoh16/dtoh32 are identity unless IL_BIGENDIAN is defined `whd/src/include/whd_endian.h:20` `whd/src/include/whd_endian.h:45-48` `whd/src/include/whd_endian.h:54-57`); defined at `whd/src/include/whd_wlioctl.h:863-868`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `index` | `uint32_t` | |
| 4 | 4 | `behavior` | `uint32_t` | |
| 8 | 1 | `activehi` | `uint8_t` | |
| 9 | 3 | (pad) | `uint8_t[3]` | implicit tail padding to the struct alignment (4); 3 bytes of tail padding after the 1-byte activehi |

Size check: compiled

### `wl_dot11_assoc_req` (whd)
Embedded in wl_assoc_info_t (`whd/src/include/whd_wlioctl.h:885`); no use site in whd/src or whd/inc outside this header by type name or struct tag (include_helium not covered; use in linux, c-driver and embassy unverified), so the command it belongs to is not stated in whd; not packed (no packed attribute; the header's first `#pragma pack` is at `whd/src/include/whd_wlioctl.h:3864`, after the definition); 4 bytes (alignment 2; same on x86-64 and 32-bit ARM); little-endian as whd treats it (inferred: plain uintN_t types, and whd's htod16/htod32/dtoh16/dtoh32 are identity unless IL_BIGENDIAN is defined `whd/src/include/whd_endian.h:20` `whd/src/include/whd_endian.h:45-48` `whd/src/include/whd_endian.h:54-57`); defined at `whd/src/include/whd_wlioctl.h:869-873`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 2 | `capability` | `uint16_t` | |
| 2 | 2 | `listen` | `uint16_t` | |

Size check: compiled

### `wl_dot11_assoc_resp` (whd)
Embedded in wl_assoc_info_t (`whd/src/include/whd_wlioctl.h:887`); no use site in whd/src or whd/inc outside this header by type name or struct tag (include_helium not covered; use in linux, c-driver and embassy unverified), so the command it belongs to is not stated in whd; not packed (no packed attribute; the header's first `#pragma pack` is at `whd/src/include/whd_wlioctl.h:3864`, after the definition); 6 bytes (alignment 2; same on x86-64 and 32-bit ARM); little-endian as whd treats it (inferred: plain uintN_t types, and whd's htod16/htod32/dtoh16/dtoh32 are identity unless IL_BIGENDIAN is defined `whd/src/include/whd_endian.h:20` `whd/src/include/whd_endian.h:45-48` `whd/src/include/whd_endian.h:54-57`); defined at `whd/src/include/whd_wlioctl.h:874-879`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 2 | `capability` | `uint16_t` | |
| 2 | 2 | `status` | `uint16_t` | |
| 4 | 2 | `aid` | `uint16_t` | |

Size check: compiled

### `wl_assoc_info_t` (whd)
No use site in whd/src or whd/inc outside this header by type name or struct tag (include_helium not covered; use in linux, c-driver and embassy unverified), so the command it belongs to is not stated in whd; no implicit padding (all members have 2-byte or 4-byte alignment and fall on aligned offsets); not packed (no packed attribute; the header's first `#pragma pack` is at `whd/src/include/whd_wlioctl.h:3864`, after the definition); 28 bytes (alignment 4; same on x86-64 and 32-bit ARM); little-endian as whd treats it (inferred: plain uintN_t types, and whd's htod16/htod32/dtoh16/dtoh32 are identity unless IL_BIGENDIAN is defined `whd/src/include/whd_endian.h:20` `whd/src/include/whd_endian.h:45-48` `whd/src/include/whd_endian.h:54-57`); defined at `whd/src/include/whd_wlioctl.h:880-888`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `req_len` | `uint32_t` | |
| 4 | 4 | `resp_len` | `uint32_t` | |
| 8 | 4 | `flags` | `uint32_t` | WLC_ASSOC_REQ_IS_REASSOC = 0x01 is the flags bit (`whd/src/include/whd_wlioctl.h:889`) |
| 12 | 4 | `req` | `struct wl_dot11_assoc_req` | |
| 16 | 6 | `reassoc_bssid` | `wl_ether_addr_t` | |
| 22 | 6 | `resp` | `struct wl_dot11_assoc_resp` | |

Size check: compiled

### `srom_rw_t` (whd)
No use site in whd/src or whd/inc outside this header by type name or struct tag (include_helium not covered; use in linux, c-driver and embassy unverified), so the command it belongs to is not stated in whd; not packed (no packed attribute; the header's first `#pragma pack` is at `whd/src/include/whd_wlioctl.h:3864`, after the definition); variable size, 8 fixed bytes plus tail (sizeof = 12 counts one placeholder element of the tail; alignment 4; same on x86-64 and 32-bit ARM); little-endian as whd treats it (inferred: plain uintN_t types, and whd's htod16/htod32/dtoh16/dtoh32 are identity unless IL_BIGENDIAN is defined `whd/src/include/whd_endian.h:20` `whd/src/include/whd_endian.h:45-48` `whd/src/include/whd_endian.h:54-57`); defined at `whd/src/include/whd_wlioctl.h:890-895`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `byteoff` | `uint32_t` | |
| 4 | 4 | `nbytes` | `uint32_t` | |
| 8 | variable | `buf` | `uint16_t[1]` | flexible tail declared as a one-element placeholder array; one element is 2 bytes; buf[1] of uint16_t is a placeholder for the data words; sizeof (12) includes one word and 2 tail pad bytes |
| 10 | 2 | (pad) | `uint8_t[2]` | implicit tail padding to the struct alignment (4); counted by sizeof only, after the placeholder element |

Size check: compiled

### `cis_rw_t` (whd)
No use site in whd/src or whd/inc outside this header by type name or struct tag (include_helium not covered; use in linux, c-driver and embassy unverified), so the command it belongs to is not stated in whd; not packed (no packed attribute; the header's first `#pragma pack` is at `whd/src/include/whd_wlioctl.h:3864`, after the definition); 12 bytes (alignment 4; same on x86-64 and 32-bit ARM); little-endian as whd treats it (inferred: plain uintN_t types, and whd's htod16/htod32/dtoh16/dtoh32 are identity unless IL_BIGENDIAN is defined `whd/src/include/whd_endian.h:20` `whd/src/include/whd_endian.h:45-48` `whd/src/include/whd_endian.h:54-57`); defined at `whd/src/include/whd_wlioctl.h:896-901`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `source` | `uint32_t` | source values WLC_CIS_DEFAULT 0 / WLC_CIS_SROM 1 / WLC_CIS_OTP 2 (`whd/src/include/whd_wlioctl.h:902-904`) |
| 4 | 4 | `byteoff` | `uint32_t` | |
| 8 | 4 | `nbytes` | `uint32_t` | |

Size check: compiled

### `rw_reg_t` (whd)
No use site in whd/src or whd/inc outside this header by type name or struct tag (include_helium not covered; use in linux, c-driver and embassy unverified), so the command it belongs to is not stated in whd; not packed (no packed attribute; the header's first `#pragma pack` is at `whd/src/include/whd_wlioctl.h:3864`, after the definition); 16 bytes (alignment 4; same on x86-64 and 32-bit ARM); little-endian as whd treats it (inferred: plain uintN_t types, and whd's htod16/htod32/dtoh16/dtoh32 are identity unless IL_BIGENDIAN is defined `whd/src/include/whd_endian.h:20` `whd/src/include/whd_endian.h:45-48` `whd/src/include/whd_endian.h:54-57`); defined at `whd/src/include/whd_wlioctl.h:905-911`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `byteoff` | `uint32_t` | |
| 4 | 4 | `val` | `uint32_t` | |
| 8 | 4 | `size` | `uint32_t` | |
| 12 | 4 | `band` | `uint32_t` | |

Size check: compiled

### `atten_t` (whd)
No use site in whd/src or whd/inc outside this header by type name or struct tag (include_helium not covered; use in linux, c-driver and embassy unverified), so the command it belongs to is not stated in whd; not packed (no packed attribute; the header's first `#pragma pack` is at `whd/src/include/whd_wlioctl.h:3864`, after the definition); 8 bytes (alignment 2; same on x86-64 and 32-bit ARM); little-endian as whd treats it (inferred: plain uintN_t types, and whd's htod16/htod32/dtoh16/dtoh32 are identity unless IL_BIGENDIAN is defined `whd/src/include/whd_endian.h:20` `whd/src/include/whd_endian.h:45-48` `whd/src/include/whd_endian.h:54-57`); defined at `whd/src/include/whd_wlioctl.h:915-921`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 2 | `auto_ctrl` | `uint16_t` | |
| 2 | 2 | `bb` | `uint16_t` | |
| 4 | 2 | `radio` | `uint16_t` | |
| 6 | 2 | `txctl1` | `uint16_t` | |

Size check: compiled

### `wme_tx_params_s` (whd)
No use site found in whd/src *.c; the header defines WL_WME_TX_PARAMS_IO_BYTES = sizeof(wme_tx_params_t) * AC_COUNT (`whd/src/include/whd_wlioctl.h:931`; AC_COUNT = 4 at `whd/src/include/whd_wlioctl.h:3285`), that is, the I/O unit is an array of 4 of these (24 bytes); the command is not stated (include_helium not covered; use in linux, c-driver and embassy unverified); also typedef wme_tx_params_t (`whd/src/include/whd_wlioctl.h:930`); not packed (no packed attribute; the header's first `#pragma pack` is at `whd/src/include/whd_wlioctl.h:3864`, after the definition); 6 bytes (alignment 2; same on x86-64 and 32-bit ARM); little-endian as whd treats it (inferred: plain uintN_t types, and whd's htod16/htod32/dtoh16/dtoh32 are identity unless IL_BIGENDIAN is defined `whd/src/include/whd_endian.h:20` `whd/src/include/whd_endian.h:45-48` `whd/src/include/whd_endian.h:54-57`); defined at `whd/src/include/whd_wlioctl.h:922-929`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 1 | `short_retry` | `uint8_t` | |
| 1 | 1 | `short_fallback` | `uint8_t` | |
| 2 | 1 | `long_retry` | `uint8_t` | |
| 3 | 1 | `long_fallback` | `uint8_t` | |
| 4 | 2 | `max_rate` | `uint16_t` | |

Size check: compiled

### `scb_val_t` (whd)
Set payload of command WLC_SCB_DEAUTHENTICATE_FOR_REASON (201, `whd/src/include/whd_wlioctl.h:1480`): `whd/src/whd_wifi_api.c:3538-3548` and `whd/src/whd_wifi_api.c:3565-3570` (ea = station MAC); not packed (no packed attribute; the header's first `#pragma pack` is at `whd/src/include/whd_wlioctl.h:3864`, after the definition); 12 bytes (alignment 4; same on x86-64 and 32-bit ARM); little-endian as whd treats it (inferred: plain uintN_t types, and whd's htod16/htod32/dtoh16/dtoh32 are identity unless IL_BIGENDIAN is defined `whd/src/include/whd_endian.h:20` `whd/src/include/whd_endian.h:45-48` `whd/src/include/whd_endian.h:54-57`); defined at `whd/src/include/whd_wlioctl.h:936-940`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `val` | `uint32_t` | |
| 4 | 6 | `ea` | `wl_ether_addr_t` | the record is zeroed by memset (`whd/src/whd_wifi_api.c:3545` `whd/src/whd_wifi_api.c:3567`), then ea is copied in and val is set to the deauthentication reason code, without htod32 (`whd/src/whd_wifi_api.c:3546-3547` `whd/src/whd_wifi_api.c:3568-3569`) |
| 10 | 2 | (pad) | `uint8_t[2]` | implicit tail padding to the struct alignment (4); 2 bytes of tail padding after ea |

Size check: compiled

### `sta_info_t` (whd)
Station information record, with no command or named variable tied to it in whd: it is only a member (`sta`) of `dpt_status_t` and the operand of `WL_OLD_STAINFO_SIZE`, no whd `.c` file uses it, and linux reads the same leading layout with the named variables `tdls_sta_info` and `sta_info`; not packed (no packed attribute, and the header's first `#pragma pack` is at line 3864, after the definition); 76 bytes; little-endian as whd treats it (inferred: the definition uses plain uintN_t types, and whd's htod16/htod32/dtoh16/dtoh32 are identity unless IL_BIGENDIAN is defined). `whd/src/include/whd_wlioctl.h:942-959` `whd/src/include/whd_wlioctl.h:3386` `whd/src/include/whd_wlioctl.h:960` `whd/src/include/whd_wlioctl.h:3864` `whd/src/include/whd_endian.h:44-57` `linux/brcmfmac/cfg80211.c:3189` `linux/brcmfmac/cfg80211.c:3207-3214`

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 2 | `ver` | `uint16_t` | `WL_STA_VER` = 2 `whd/src/include/whd_wlioctl.h:944` `whd/src/include/whd_wlioctl.h:961` |
| 2 | 2 | `len` | `uint16_t` | `whd/src/include/whd_wlioctl.h:945` |
| 4 | 2 | `cap` | `uint16_t` | `whd/src/include/whd_wlioctl.h:946` |
| 6 | 2 | (pad) | - | implicit alignment padding inserted by the compiler before `flags` `whd/src/include/whd_wlioctl.h:946-947` |
| 8 | 4 | `flags` | `uint32_t` | `WL_STA_*` bits `whd/src/include/whd_wlioctl.h:947` `whd/src/include/whd_wlioctl.h:962-976` |
| 12 | 4 | `idle` | `uint32_t` | `whd/src/include/whd_wlioctl.h:948` |
| 16 | 6 | `ea` | `wl_ether_addr_t` | 6 octets `whd/src/include/whd_wlioctl.h:949` `whd/src/include/whd_wlioctl.h:50-53` `whd/inc/whd_types.h:101` |
| 22 | 2 | (pad) | - | implicit alignment padding inserted by the compiler before `rateset`, which contains a `uint32_t` `whd/src/include/whd_wlioctl.h:949-950` |
| 24 | 20 | `rateset` | `wl_rateset_t` | `uint32_t count`, then `uint8_t rates[16]` (`WL_MAXRATES_IN_SET`) `whd/src/include/whd_wlioctl.h:950` `whd/src/include/whd_wlioctl.h:572-577` |
| 44 | 4 | `in` | `uint32_t` | `whd/src/include/whd_wlioctl.h:951` |
| 48 | 4 | `listen_interval_inms` | `uint32_t` | `whd/src/include/whd_wlioctl.h:952` |
| 52 | 4 | `tx_pkts` | `uint32_t` | `WL_OLD_STAINFO_SIZE` = offsetof(sta_info_t, tx_pkts) = 52 marks the shorter, older form `whd/src/include/whd_wlioctl.h:953` `whd/src/include/whd_wlioctl.h:960` |
| 56 | 4 | `tx_failures` | `uint32_t` | `whd/src/include/whd_wlioctl.h:954` |
| 60 | 4 | `rx_ucast_pkts` | `uint32_t` | `whd/src/include/whd_wlioctl.h:955` |
| 64 | 4 | `rx_mcast_pkts` | `uint32_t` | `whd/src/include/whd_wlioctl.h:956` |
| 68 | 4 | `tx_rate` | `uint32_t` | `whd/src/include/whd_wlioctl.h:957` |
| 72 | 4 | `rx_rate` | `uint32_t` | `whd/src/include/whd_wlioctl.h:958` |

Size check: compiled

Differences: linux's `struct brcmf_sta_info_le` lists the same fields in the same order, every multi-byte integer `__le16`/`__le32`, with the rate set written out as `count` + `rates[]`, and then continues with further fields that whd's definition lacks, from `rx_decrypt_succeeds` to the end of the struct. linux marks `tx_pkts` through `rx_decrypt_failures` as valid for version 3 and above and `tx_tot_pkts` onward as valid for version 4 and above, while whd defines `WL_STA_VER` as 2. linux puts the peer MAC address in the first 6 bytes of the buffer before the get. The record name is not found in embassy, c-driver or pico-sdk. `linux/brcmfmac/fwil_types.h:614-633` `linux/brcmfmac/fwil_types.h:634-706` `linux/brcmfmac/fwil_types.h:627` `linux/brcmfmac/fwil_types.h:637` `whd/src/include/whd_wlioctl.h:961` `linux/brcmfmac/cfg80211.c:3205-3206`

### `channel_info_t` (whd)
Reply of command `WLC_GET_CHANNEL` (29) `whd/src/include/whd_wlioctl.h:1325`, for which whd allocates `sizeof(channel_info_t)`, issues the command and returns `hw_channel` `whd/src/whd_wifi_api.c:677-683`; struct tag `channel_info`; not packed (no `#pragma pack` is in force at the definition: the first one in the file is at `whd/src/include/whd_wlioctl.h:3864`, the header has no `#include` of its own so pack state comes from the including file, and the pragmas in whd's public types header are balanced `whd/inc/whd_types.h:880`, `whd/inc/whd_types.h:904`, `whd/inc/whd_types.h:1120`, `whd/inc/whd_types.h:1147`; the full include chain was not compiled); total size 12 bytes; byte order not stated in the definition (plain C integer types), though whd converts multi-byte values at other use sites with `htod32`/`dtoh32`, i.e. dongle byte order `whd/src/whd_wifi_api.c:589`, `whd/src/whd_wifi_api.c:1213`; definition `whd/src/include/whd_wlioctl.h:978-983`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `hw_channel` | `int32_t` | the field whd returns, read without a `dtoh32` conversion `whd/src/whd_wifi_api.c:683`; `whd/src/include/whd_wlioctl.h:980` |
| 4 | 4 | `target_channel` | `int32_t` | `whd/src/include/whd_wlioctl.h:981` |
| 8 | 4 | `scan_channel` | `int32_t` | `whd/src/include/whd_wlioctl.h:982` |

Size check: compiled (x86-64 gcc from an extract of the header, asserted again for arm-none-eabi cortex-m0plus and i386, all three agree; supplied by hand: `ETHER_ADDR_LEN` = 6 `whd/inc/whd_types.h:101`, `wl_chanspec_t` = `uint16_t` `whd/inc/whd_types.h:918`)

Differences: linux `struct brcmf_channel_info_le` has the same layout, the same three fields declared `__le32` `linux/brcmfmac/fwil_types.h:608-612`. No linux use site of that struct was found; linux's `BRCMF_C_GET_CHANNEL` calls pass a bare `hw_ch` variable instead `linux/brcmfmac/cyw/core.c:146-147`, `linux/brcmfmac/cfg80211.c:5746-5748`.

### `struct mac_list` (whd)
MAC address list with no use site found in whd, matching by name only the commands `WLC_GET_MACLIST` (69) and `WLC_SET_MACLIST` (70) `whd/src/include/whd_wlioctl.h:1361-1362`, which whd lists only in its command-name table `whd/src/whd_utils.c:580-581`; struct tag only, no typedef; not packed (no `#pragma pack` is in force at the definition: the first one in the file is at `whd/src/include/whd_wlioctl.h:3864`, the header has no `#include` of its own so pack state comes from the including file, and the pragmas in whd's public types header are balanced `whd/inc/whd_types.h:880`, `whd/inc/whd_types.h:904`, `whd/inc/whd_types.h:1120`, `whd/inc/whd_types.h:1147`; the full include chain was not compiled); total size variable, 4 fixed + 6 per address (`sizeof` with the one-element array is 12); byte order not stated in the definition (plain C integer types), though whd converts multi-byte values at other use sites with `htod32`/`dtoh32`, i.e. dongle byte order `whd/src/whd_wifi_api.c:589`, `whd/src/whd_wifi_api.c:1213`; definition `whd/src/include/whd_wlioctl.h:984-988`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `count` | `uint32_t` | `whd/src/include/whd_wlioctl.h:986` |
| 4 | variable (6 declared) | `ea` | `wl_ether_addr_t[1]` | variable: `count` entries of 6 bytes; declared as a one-element array; `whd/src/include/whd_wlioctl.h:987` |
| 10 | 2 | (pad) | - | trailing padding counted by `sizeof` only (struct alignment 4), not between array elements; compiled layout `whd/src/include/whd_wlioctl.h:984-988` |

Size check: compiled (x86-64 gcc from an extract of the header, asserted again for arm-none-eabi cortex-m0plus and i386, all three agree; supplied by hand: `ETHER_ADDR_LEN` = 6 `whd/inc/whd_types.h:101`, `wl_chanspec_t` = `uint16_t` `whd/inc/whd_types.h:918`)

Differences: whd's own association-list call uses a different type, `whd_maclist_t` `whd/inc/whd_types.h:1141-1145`, with `WLC_GET_ASSOCLIST` `whd/src/whd_wifi_api.c:3684-3689`. Not found by name in linux, embassy, c-driver or pico-sdk.

### `get_pktcnt_t` (whd)
Packet counters with no use site found in whd, matching by name the command `WLC_GET_PKTCNTS` (137) `whd/src/include/whd_wlioctl.h:1425`, which whd lists only in its command-name table `whd/src/whd_utils.c:644`; struct tag `get_pktcnt`; not packed (no `#pragma pack` is in force at the definition: the first one in the file is at `whd/src/include/whd_wlioctl.h:3864`, the header has no `#include` of its own so pack state comes from the including file, and the pragmas in whd's public types header are balanced `whd/inc/whd_types.h:880`, `whd/inc/whd_types.h:904`, `whd/inc/whd_types.h:1120`, `whd/inc/whd_types.h:1147`; the full include chain was not compiled); total size 20 bytes; byte order not stated in the definition (plain C integer types), though whd converts multi-byte values at other use sites with `htod32`/`dtoh32`, i.e. dongle byte order `whd/src/whd_wifi_api.c:589`, `whd/src/whd_wifi_api.c:1213`; definition `whd/src/include/whd_wlioctl.h:989-996`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `rx_good_pkt` | `uint32_t` | `whd/src/include/whd_wlioctl.h:991` |
| 4 | 4 | `rx_bad_pkt` | `uint32_t` | `whd/src/include/whd_wlioctl.h:992` |
| 8 | 4 | `tx_good_pkt` | `uint32_t` | `whd/src/include/whd_wlioctl.h:993` |
| 12 | 4 | `tx_bad_pkt` | `uint32_t` | `whd/src/include/whd_wlioctl.h:994` |
| 16 | 4 | `rx_ocast_good_pkt` | `uint32_t` | `whd/src/include/whd_wlioctl.h:995` |

Size check: compiled (x86-64 gcc from an extract of the header, asserted again for arm-none-eabi cortex-m0plus and i386, all three agree; supplied by hand: `ETHER_ADDR_LEN` = 6 `whd/inc/whd_types.h:101`, `wl_chanspec_t` = `uint16_t` `whd/inc/whd_types.h:918`)

Differences: linux fetches the same record with command 137 `linux/brcmfmac/fwil.h:66`, `linux/brcmfmac/cfg80211.c:3137`, `linux/brcmfmac/cfg80211.c:3162-3163`; its `struct brcmf_pktcnt_le` has the same layout, the same five fields in the same order, all `__le32` `linux/brcmfmac/fwil_types.h:1134-1140`.

### `wlc_rev_info_t` (whd)
Revision information with no use site found in whd, matching by name the command `WLC_GET_REVINFO` (98) `whd/src/include/whd_wlioctl.h:1388`, which whd lists only in its command-name table `whd/src/whd_utils.c:607`; struct tag `wlc_rev_info`; not packed (no `#pragma pack` is in force at the definition: the first one in the file is at `whd/src/include/whd_wlioctl.h:3864`, the header has no `#include` of its own so pack state comes from the including file, and the pragmas in whd's public types header are balanced `whd/inc/whd_types.h:880`, `whd/inc/whd_types.h:904`, `whd/inc/whd_types.h:1120`, `whd/inc/whd_types.h:1147`; the full include chain was not compiled); total size 60 bytes; byte order not stated in the definition (plain C integer types), though whd converts multi-byte values at other use sites with `htod32`/`dtoh32`, i.e. dongle byte order `whd/src/whd_wifi_api.c:589`, `whd/src/whd_wifi_api.c:1213`; definition `whd/src/include/whd_wlioctl.h:1006-1023`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `vendorid` | `uint32_t` | `whd/src/include/whd_wlioctl.h:1008` |
| 4 | 4 | `deviceid` | `uint32_t` | `whd/src/include/whd_wlioctl.h:1009` |
| 8 | 4 | `radiorev` | `uint32_t` | `whd/src/include/whd_wlioctl.h:1010` |
| 12 | 4 | `chiprev` | `uint32_t` | `whd/src/include/whd_wlioctl.h:1011` |
| 16 | 4 | `corerev` | `uint32_t` | `whd/src/include/whd_wlioctl.h:1012` |
| 20 | 4 | `boardid` | `uint32_t` | `whd/src/include/whd_wlioctl.h:1013` |
| 24 | 4 | `boardvendor` | `uint32_t` | `whd/src/include/whd_wlioctl.h:1014` |
| 28 | 4 | `boardrev` | `uint32_t` | `whd/src/include/whd_wlioctl.h:1015` |
| 32 | 4 | `driverrev` | `uint32_t` | `whd/src/include/whd_wlioctl.h:1016` |
| 36 | 4 | `ucoderev` | `uint32_t` | `whd/src/include/whd_wlioctl.h:1017` |
| 40 | 4 | `bus` | `uint32_t` | `whd/src/include/whd_wlioctl.h:1018` |
| 44 | 4 | `chipnum` | `uint32_t` | last field inside `WL_REV_INFO_LEGACY_LENGTH` = 48 `whd/src/include/whd_wlioctl.h:1024`, the length of the first 12 fields, `vendorid` to `chipnum` (inferred); `whd/src/include/whd_wlioctl.h:1019` |
| 48 | 4 | `phytype` | `uint32_t` | `whd/src/include/whd_wlioctl.h:1020` |
| 52 | 4 | `phyrev` | `uint32_t` | `whd/src/include/whd_wlioctl.h:1021` |
| 56 | 4 | `anarev` | `uint32_t` | `whd/src/include/whd_wlioctl.h:1022` |

Size check: compiled (x86-64 gcc from an extract of the header, asserted again for arm-none-eabi cortex-m0plus and i386, all three agree; supplied by hand: `ETHER_ADDR_LEN` = 6 `whd/inc/whd_types.h:101`, `wl_chanspec_t` = `uint16_t` `whd/inc/whd_types.h:918`)

Differences: linux fetches its counterpart with command 98 `linux/brcmfmac/fwil.h:53`, `linux/brcmfmac/common.c:271`, `linux/brcmfmac/common.c:307-308`. linux `struct brcmf_rev_info_le` has the same 15 leading fields, all `__le32`, then two more, `chippkg` and `nvramrev` `linux/brcmfmac/fwil_types.h:791-809`: 68 bytes in linux (computed: 17 fields of 4 bytes) against 60 in whd. The two drivers disagree on length; these sources do not say which length this chip returns.

### `wl_instance_info_t` (whd)
Instance information with no use site found in whd, matching by name only the command `WLC_GET_INSTANCE` (14) `whd/src/include/whd_wlioctl.h:1315`, listed in whd's command-name table `whd/src/whd_utils.c:534`; struct tag `wl_instance_info`; not packed (no `#pragma pack` is in force at the definition: the first one in the file is at `whd/src/include/whd_wlioctl.h:3864`, the header has no `#include` of its own so pack state comes from the including file, and the pragmas in whd's public types header are balanced `whd/inc/whd_types.h:880`, `whd/inc/whd_types.h:904`, `whd/inc/whd_types.h:1120`, `whd/inc/whd_types.h:1147`; the full include chain was not compiled); total size 16 bytes; byte order not stated in the definition (plain C integer types), though whd converts multi-byte values at other use sites with `htod32`/`dtoh32`, i.e. dongle byte order `whd/src/whd_wifi_api.c:589`, `whd/src/whd_wifi_api.c:1213`; definition `whd/src/include/whd_wlioctl.h:1026-1030`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `instance` | `uint32_t` | `whd/src/include/whd_wlioctl.h:1028` |
| 4 | 10 | `brand` | `int8_t[10]` | `WL_BRAND_MAX` = 10 `whd/src/include/whd_wlioctl.h:1025`; `whd/src/include/whd_wlioctl.h:1029` |
| 14 | 2 | (pad) | - | trailing compiler padding to 4-byte struct alignment; compiled layout `whd/src/include/whd_wlioctl.h:1026-1030` |

Size check: compiled (x86-64 gcc from an extract of the header, asserted again for arm-none-eabi cortex-m0plus and i386, all three agree; supplied by hand: `ETHER_ADDR_LEN` = 6 `whd/inc/whd_types.h:101`, `wl_chanspec_t` = `uint16_t` `whd/inc/whd_types.h:918`)

Differences: not found by name in linux, embassy, c-driver or pico-sdk.

### `wl_txfifo_sz_t` (whd)
Transmit FIFO size pair for which only the definition exists, with no use site and no command or named variable tied to it found in whd; struct tag `wl_txfifo_sz`; not packed (no `#pragma pack` is in force at the definition: the first one in the file is at `whd/src/include/whd_wlioctl.h:3864`, the header has no `#include` of its own so pack state comes from the including file, and the pragmas in whd's public types header are balanced `whd/inc/whd_types.h:880`, `whd/inc/whd_types.h:904`, `whd/inc/whd_types.h:1120`, `whd/inc/whd_types.h:1147`; the full include chain was not compiled); total size 2 bytes; byte order does not apply (every field is a single byte or byte array); definition `whd/src/include/whd_wlioctl.h:1031-1035`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 1 | `fifo` | `uint8_t` | `whd/src/include/whd_wlioctl.h:1033` |
| 1 | 1 | `size` | `uint8_t` | `whd/src/include/whd_wlioctl.h:1034` |

Size check: compiled (x86-64 gcc from an extract of the header, asserted again for arm-none-eabi cortex-m0plus and i386, all three agree; supplied by hand: `ETHER_ADDR_LEN` = 6 `whd/inc/whd_types.h:101`, `wl_chanspec_t` = `uint16_t` `whd/inc/whd_types.h:918`)

Differences: not found by name in linux, embassy, c-driver or pico-sdk.

### `wlc_iov_trx_t` (whd)
Named-variable descriptor (module, type, name) with no use site found in whd; commands `WLC_IOV_BLOCK_GET` (276) and `WLC_IOV_MODULES_GET` (277) are defined in the same header `whd/src/include/whd_wlioctl.h:1552-1553`, but the source does not connect them to this record; struct tag `wlc_iov_trx_s`; not packed (no `#pragma pack` is in force at the definition: the first one in the file is at `whd/src/include/whd_wlioctl.h:3864`, the header has no `#include` of its own so pack state comes from the including file, and the pragmas in whd's public types header are balanced `whd/inc/whd_types.h:880`, `whd/inc/whd_types.h:904`, `whd/inc/whd_types.h:1120`, `whd/inc/whd_types.h:1147`; the full include chain was not compiled), and no padding either way since all fields are bytes; total size 32 bytes; byte order does not apply (every field is a single byte or byte array); definition `whd/src/include/whd_wlioctl.h:1037-1042`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 1 | `module` | `uint8_t` | `whd/src/include/whd_wlioctl.h:1039` |
| 1 | 1 | `type` | `uint8_t` | `whd/src/include/whd_wlioctl.h:1040` |
| 2 | 30 | `name` | `int8_t[30]` | `WLC_IOV_NAME_LEN` = 30 `whd/src/include/whd_wlioctl.h:1036`; `whd/src/include/whd_wlioctl.h:1041` |

Size check: compiled (x86-64 gcc from an extract of the header, asserted again for arm-none-eabi cortex-m0plus and i386, all three agree; supplied by hand: `ETHER_ADDR_LEN` = 6 `whd/inc/whd_types.h:101`, `wl_chanspec_t` = `uint16_t` `whd/inc/whd_types.h:918`)

Differences: not found by name in linux, embassy, c-driver or pico-sdk.

### `eventmsgs_ext_t` (whd)
Payload of the named variable `event_msgs_ext` `whd/src/include/whd_wlioctl.h:1075`, which whd sends as `bsscfg:event_msgs_ext` with a `uint32_t` bsscfg index in front of the record `whd/src/whd_events.c:305-317` (the index is stored without an `htod32` conversion `whd/src/whd_events.c:315`) and sets with `whd_proto_set_iovar` `whd/src/whd_events.c:421`, `whd/src/whd_events.c:517`, only when a registered event number is above 127, otherwise sending the 16-byte `event_msgs` mask `whd/src/whd_events.c:274`, `whd/src/whd_events.c:287-300`, `whd/src/include/whd_wlioctl.h:1932`; struct tag `eventmsgs_ext`; not packed (no `#pragma pack` is in force at the definition: the first one in the file is at `whd/src/include/whd_wlioctl.h:3864`, the header has no `#include` of its own so pack state comes from the including file, and the pragmas in whd's public types header are balanced `whd/inc/whd_types.h:880`, `whd/inc/whd_types.h:904`, `whd/inc/whd_types.h:1120`, `whd/inc/whd_types.h:1147`; the full include chain was not compiled); total size variable, 4 fixed + `len` mask bytes (`sizeof` with the one-element array is 5); byte order does not apply (every field is a single byte or byte array); definition `whd/src/include/whd_wlioctl.h:1056-1063`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 1 | `ver` | `uint8_t` | `EVENTMSGS_VER` = 1 `whd/src/include/whd_wlioctl.h:1050`, which is what whd writes `whd/src/whd_events.c:320`; `whd/src/include/whd_wlioctl.h:1058` |
| 1 | 1 | `command` | `uint8_t` | NONE = 0, SET_BIT = 1, RESET_BIT = 2, SET_MASK = 3 `whd/src/include/whd_wlioctl.h:1045-1048`; whd writes `EVENTMSGS_SET_MASK` `whd/src/whd_events.c:321`; `whd/src/include/whd_wlioctl.h:1059` |
| 2 | 1 | `len` | `uint8_t` | header comment: on set, the mask size sent; on get, the firmware's mask size `whd/src/include/whd_wlioctl.h:1052-1053`; whd writes (max_event + 8) / 8 `whd/src/whd_events.c:304`, `whd/src/whd_events.c:322`; `whd/src/include/whd_wlioctl.h:1060` |
| 3 | 1 | `maxgetsize` | `uint8_t` | header comment: get only, largest mask the caller can read `whd/src/include/whd_wlioctl.h:1054-1055`; whd leaves it 0 after clearing the header `whd/src/whd_events.c:319-322`; `whd/src/include/whd_wlioctl.h:1061` |
| 4 | variable (1 declared) | `mask` | `uint8_t[1]` | variable: `len` bytes of event bit mask; declared as a one-element array; whd requests the buffer as `sizeof(eventmsgs_ext_t) + mask_len + 4` `whd/src/whd_events.c:305-308`, one byte more than 4 (bsscfg index) + 4 (fixed header) + mask length because `sizeof` counts the one-element `mask` (inferred from the compiled size of 5); `whd/src/include/whd_wlioctl.h:1062` |

Size check: compiled (x86-64 gcc from an extract of the header, asserted again for arm-none-eabi cortex-m0plus and i386, all three agree; supplied by hand: `ETHER_ADDR_LEN` = 6 `whd/inc/whd_types.h:101`, `wl_chanspec_t` = `uint16_t` `whd/inc/whd_types.h:918`)

Differences: the two set calls are in whd's two set-event-handler functions, which get the buffer from `whd_management_alloc_event_msgs_buffer` `whd/src/whd_events.c:255`, `whd/src/whd_events.c:396`, `whd/src/whd_events.c:492`. linux `struct brcmf_eventmsgs_ext` has the same four header bytes, but `mask` is a true flexible array, so the linux struct is 4 bytes with no mask (computed: four `u8`) `linux/brcmfmac/cyw/fwil_types.h:31-37`. linux sets `event_msgs_ext` with length 4 + mask length, `ver` = `EVENTMSGS_VER` (1), `command` = `CYW_EVENTMSGS_SET_MASK` (3), and no bsscfg prefix `linux/brcmfmac/cyw/core.c:86-96`, `linux/brcmfmac/cyw/fwil_types.h:11-18`. Not found in embassy, c-driver or pico-sdk.

### `wl_aci_args_t` (whd)
Interference-mitigation arguments with no use site found in whd, matching by name only the commands `WLC_GET_ACI_ARGS` (238) and `WLC_SET_ACI_ARGS` (239) `whd/src/include/whd_wlioctl.h:1514-1515`, listed in whd's command-name table `whd/src/whd_utils.c:732-733`; struct tag `wl_aci_args`; not packed (no `#pragma pack` is in force at the definition: the first one in the file is at `whd/src/include/whd_wlioctl.h:3864`, the header has no `#include` of its own so pack state comes from the including file, and the pragmas in whd's public types header are balanced `whd/inc/whd_types.h:880`, `whd/inc/whd_types.h:904`, `whd/inc/whd_types.h:1120`, `whd/inc/whd_types.h:1147`; the full include chain was not compiled); total size 32 bytes; byte order not stated in the definition (plain C integer types), though whd converts multi-byte values at other use sites with `htod32`/`dtoh32`, i.e. dongle byte order `whd/src/whd_wifi_api.c:589`, `whd/src/whd_wifi_api.c:1213`; definition `whd/src/include/whd_wlioctl.h:1713-1727`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `enter_aci_thresh` | `int32_t` | `whd/src/include/whd_wlioctl.h:1715` |
| 4 | 4 | `exit_aci_thresh` | `int32_t` | `whd/src/include/whd_wlioctl.h:1716` |
| 8 | 4 | `usec_spin` | `int32_t` | `whd/src/include/whd_wlioctl.h:1717` |
| 12 | 4 | `glitch_delay` | `int32_t` | last field inside `WL_ACI_ARGS_LEGACY_LENGTH` = 16 `whd/src/include/whd_wlioctl.h:1728`, the length of the four `int32_t` fields (inferred); `whd/src/include/whd_wlioctl.h:1718` |
| 16 | 2 | `nphy_adcpwr_enter_thresh` | `uint16_t` | `whd/src/include/whd_wlioctl.h:1719` |
| 18 | 2 | `nphy_adcpwr_exit_thresh` | `uint16_t` | `whd/src/include/whd_wlioctl.h:1720` |
| 20 | 2 | `nphy_repeat_ctr` | `uint16_t` | `whd/src/include/whd_wlioctl.h:1721` |
| 22 | 2 | `nphy_num_samples` | `uint16_t` | `whd/src/include/whd_wlioctl.h:1722` |
| 24 | 2 | `nphy_undetect_window_sz` | `uint16_t` | `whd/src/include/whd_wlioctl.h:1723` |
| 26 | 2 | `nphy_b_energy_lo_aci` | `uint16_t` | `whd/src/include/whd_wlioctl.h:1724` |
| 28 | 2 | `nphy_b_energy_md_aci` | `uint16_t` | `whd/src/include/whd_wlioctl.h:1725` |
| 30 | 2 | `nphy_b_energy_hi_aci` | `uint16_t` | `whd/src/include/whd_wlioctl.h:1726` |

Size check: compiled (x86-64 gcc from an extract of the header, asserted again for arm-none-eabi cortex-m0plus and i386, all three agree; supplied by hand: `ETHER_ADDR_LEN` = 6 `whd/inc/whd_types.h:101`, `wl_chanspec_t` = `uint16_t` `whd/inc/whd_types.h:918`)

Differences: not found by name in linux, embassy, c-driver or pico-sdk.

### `wl_radar_args_t` (whd)
Radar detection arguments with no use site and no command or named variable tied to it found in whd; commands `WLC_GET_RADAR` (242) and `WLC_SET_RADAR` (243) exist `whd/src/include/whd_wlioctl.h:1518-1519`, `whd/src/whd_utils.c:736-737`, but the source does not connect them to this record; anonymous struct typedef; not packed (no `#pragma pack` is in force at the definition: the first one in the file is at `whd/src/include/whd_wlioctl.h:3864`, the header has no `#include` of its own so pack state comes from the including file, and the pragmas in whd's public types header are balanced `whd/inc/whd_types.h:880`, `whd/inc/whd_types.h:904`, `whd/inc/whd_types.h:1120`, `whd/inc/whd_types.h:1147`; the full include chain was not compiled); total size 64 bytes; byte order not stated in the definition (plain C integer types), though whd converts multi-byte values at other use sites with `htod32`/`dtoh32`, i.e. dongle byte order `whd/src/whd_wifi_api.c:589`, `whd/src/whd_wifi_api.c:1213`; definition `whd/src/include/whd_wlioctl.h:1729-1750`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `npulses` | `int32_t` | `whd/src/include/whd_wlioctl.h:1731` |
| 4 | 4 | `ncontig` | `int32_t` | `whd/src/include/whd_wlioctl.h:1732` |
| 8 | 4 | `min_pw` | `int32_t` | `whd/src/include/whd_wlioctl.h:1733` |
| 12 | 4 | `max_pw` | `int32_t` | `whd/src/include/whd_wlioctl.h:1734` |
| 16 | 2 | `thresh0` | `uint16_t` | `whd/src/include/whd_wlioctl.h:1735` |
| 18 | 2 | `thresh1` | `uint16_t` | `whd/src/include/whd_wlioctl.h:1736` |
| 20 | 2 | `blank` | `uint16_t` | `whd/src/include/whd_wlioctl.h:1737` |
| 22 | 2 | `fmdemodcfg` | `uint16_t` | `whd/src/include/whd_wlioctl.h:1738` |
| 24 | 4 | `npulses_lp` | `int32_t` | `whd/src/include/whd_wlioctl.h:1739` |
| 28 | 4 | `min_pw_lp` | `int32_t` | `whd/src/include/whd_wlioctl.h:1740` |
| 32 | 4 | `max_pw_lp` | `int32_t` | `whd/src/include/whd_wlioctl.h:1741` |
| 36 | 4 | `min_fm_lp` | `int32_t` | `whd/src/include/whd_wlioctl.h:1742` |
| 40 | 4 | `max_deltat_lp` | `int32_t` | `whd/src/include/whd_wlioctl.h:1743` |
| 44 | 4 | `min_deltat` | `int32_t` | `whd/src/include/whd_wlioctl.h:1744` |
| 48 | 4 | `max_deltat` | `int32_t` | `whd/src/include/whd_wlioctl.h:1745` |
| 52 | 2 | `autocorr` | `uint16_t` | `whd/src/include/whd_wlioctl.h:1746` |
| 54 | 2 | `st_level_time` | `uint16_t` | `whd/src/include/whd_wlioctl.h:1747` |
| 56 | 2 | `t2_min` | `uint16_t` | `whd/src/include/whd_wlioctl.h:1748` |
| 58 | 2 | (pad) | - | compiler padding, aligns `version`; compiled layout `whd/src/include/whd_wlioctl.h:1729-1750` |
| 60 | 4 | `version` | `uint32_t` | `WL_RADAR_ARGS_VERSION` = 1 `whd/src/include/whd_wlioctl.h:1751`; `whd/src/include/whd_wlioctl.h:1749` |

Size check: compiled (x86-64 gcc from an extract of the header, asserted again for arm-none-eabi cortex-m0plus and i386, all three agree; supplied by hand: `ETHER_ADDR_LEN` = 6 `whd/inc/whd_types.h:101`, `wl_chanspec_t` = `uint16_t` `whd/inc/whd_types.h:918`)

Differences: not found by name in linux, embassy, c-driver or pico-sdk.

### `wl_rssi_ant_t` (whd)
Per-antenna signal strength with no use site and no command or named variable tied to it found in whd (a link to a named variable `phy_rssi_ant` is recalled, not in these sources); anonymous struct typedef; not packed (no `#pragma pack` is in force at the definition: the first one in the file is at `whd/src/include/whd_wlioctl.h:3864`, the header has no `#include` of its own so pack state comes from the including file, and the pragmas in whd's public types header are balanced `whd/inc/whd_types.h:880`, `whd/inc/whd_types.h:904`, `whd/inc/whd_types.h:1120`, `whd/inc/whd_types.h:1147`; the full include chain was not compiled); total size 12 bytes; byte order not stated in the definition (plain C integer types), though whd converts multi-byte values at other use sites with `htod32`/`dtoh32`, i.e. dongle byte order `whd/src/whd_wifi_api.c:589`, `whd/src/whd_wifi_api.c:1213`; definition `whd/src/include/whd_wlioctl.h:1757-1762`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `version` | `uint32_t` | `WL_RSSI_ANT_VERSION` = 1 `whd/src/include/whd_wlioctl.h:1755`; `whd/src/include/whd_wlioctl.h:1759` |
| 4 | 4 | `count` | `uint32_t` | `whd/src/include/whd_wlioctl.h:1760` |
| 8 | 4 | `rssi_ant` | `int8_t[4]` | `WL_RSSI_ANT_MAX` = 4 `whd/src/include/whd_wlioctl.h:1756`; `whd/src/include/whd_wlioctl.h:1761` |

Size check: compiled (x86-64 gcc from an extract of the header, asserted again for arm-none-eabi cortex-m0plus and i386, all three agree; supplied by hand: `ETHER_ADDR_LEN` = 6 `whd/inc/whd_types.h:101`, `wl_chanspec_t` = `uint16_t` `whd/inc/whd_types.h:918`)

Differences: no occurrence of `rssi_ant` in linux, embassy, c-driver or pico-sdk.

### `wl_dfs_status_t` (whd)
DFS status with no use site and no command or named variable tied to it found in whd; anonymous struct typedef; not packed (no `#pragma pack` is in force at the definition: the first one in the file is at `whd/src/include/whd_wlioctl.h:3864`, the header has no `#include` of its own so pack state comes from the including file, and the pragmas in whd's public types header are balanced `whd/inc/whd_types.h:880`, `whd/inc/whd_types.h:904`, `whd/inc/whd_types.h:1120`, `whd/inc/whd_types.h:1147`; the full include chain was not compiled); total size 12 bytes; byte order not stated in the definition (plain C integer types), though whd converts multi-byte values at other use sites with `htod32`/`dtoh32`, i.e. dongle byte order `whd/src/whd_wifi_api.c:589`, `whd/src/whd_wifi_api.c:1213`; definition `whd/src/include/whd_wlioctl.h:1771-1777`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `state` | `uint32_t` | `WL_DFS_CACSTATE_*` values 0 to 6 `whd/src/include/whd_wlioctl.h:1763-1769`; `WL_DFS_CACSTATES` = 7 is the count `whd/src/include/whd_wlioctl.h:1770`; `whd/src/include/whd_wlioctl.h:1773` |
| 4 | 4 | `duration` | `uint32_t` | `whd/src/include/whd_wlioctl.h:1774` |
| 8 | 2 | `chanspec_cleared` | `wl_chanspec_t (uint16_t)` | `wl_chanspec_t` is `uint16_t` `whd/inc/whd_types.h:918`; `whd/src/include/whd_wlioctl.h:1775` |
| 10 | 2 | `pad` | `uint16_t` | declared member named `pad`, not compiler padding, so the layout is the same packed or not (inferred from the field sizes) `whd/src/include/whd_wlioctl.h:1771-1777`; `whd/src/include/whd_wlioctl.h:1776` |

Size check: compiled (x86-64 gcc from an extract of the header, asserted again for arm-none-eabi cortex-m0plus and i386, all three agree; supplied by hand: `ETHER_ADDR_LEN` = 6 `whd/inc/whd_types.h:101`, `wl_chanspec_t` = `uint16_t` `whd/inc/whd_types.h:918`)

Differences: not found by name in linux, embassy, c-driver or pico-sdk.

### `tx_power_legacy_t` (whd)
Legacy transmit power report with no use site and no command or named variable tied to it found in whd; anonymous struct typedef; not packed (no `#pragma pack` is in force at the definition: the first one in the file is at `whd/src/include/whd_wlioctl.h:3864`, the header has no `#include` of its own so pack state comes from the including file, and the pragmas in whd's public types header are balanced `whd/inc/whd_types.h:880`, `whd/inc/whd_types.h:904`, `whd/inc/whd_types.h:1120`, `whd/inc/whd_types.h:1147`; the full include chain was not compiled), and no padding either way since all fields are bytes (alignment 1); total size 93 bytes; byte order does not apply (every field is a single byte or byte array); definition `whd/src/include/whd_wlioctl.h:1779-1794`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 12 | `txpwr_band_max` | `uint8_t[12]` | `NUM_PWRCTRL_RATES` = 12 `whd/src/include/whd_wlioctl.h:1778`; `whd/src/include/whd_wlioctl.h:1781` |
| 12 | 12 | `txpwr_limit` | `uint8_t[12]` | `whd/src/include/whd_wlioctl.h:1782` |
| 24 | 1 | `txpwr_local_max` | `uint8_t` | `whd/src/include/whd_wlioctl.h:1783` |
| 25 | 1 | `txpwr_local_constraint` | `uint8_t` | `whd/src/include/whd_wlioctl.h:1784` |
| 26 | 1 | `txpwr_chan_reg_max` | `uint8_t` | `whd/src/include/whd_wlioctl.h:1785` |
| 27 | 24 | `txpwr_target` | `uint8_t[2][12]` | `whd/src/include/whd_wlioctl.h:1786` |
| 51 | 2 | `txpwr_est_Pout` | `uint8_t[2]` | `whd/src/include/whd_wlioctl.h:1787` |
| 53 | 12 | `txpwr_opo` | `uint8_t[12]` | `whd/src/include/whd_wlioctl.h:1788` |
| 65 | 12 | `txpwr_bphy_cck_max` | `uint8_t[12]` | `whd/src/include/whd_wlioctl.h:1789` |
| 77 | 1 | `txpwr_bphy_ofdm_max` | `uint8_t` | `whd/src/include/whd_wlioctl.h:1790` |
| 78 | 12 | `txpwr_aphy_max` | `uint8_t[12]` | `whd/src/include/whd_wlioctl.h:1791` |
| 90 | 2 | `txpwr_antgain` | `int8_t[2]` | `whd/src/include/whd_wlioctl.h:1792` |
| 92 | 1 | `txpwr_est_Pout_gofdm` | `uint8_t` | `whd/src/include/whd_wlioctl.h:1793` |

Size check: compiled (x86-64 gcc from an extract of the header, asserted again for arm-none-eabi cortex-m0plus and i386, all three agree; supplied by hand: `ETHER_ADDR_LEN` = 6 `whd/inc/whd_types.h:101`, `wl_chanspec_t` = `uint16_t` `whd/inc/whd_types.h:918`)

Differences: not found by name in linux, embassy, c-driver or pico-sdk.

### `tx_power_t` (whd)
Transmit power report with no use site found in whd; command `WLC_CURRENT_PWR` (256) is defined `whd/src/include/whd_wlioctl.h:1532` but the source does not connect it to this record (that link is recalled, not in these sources); anonymous struct typedef; not packed (no `#pragma pack` is in force at the definition: the first one in the file is at `whd/src/include/whd_wlioctl.h:3864`, the header has no `#include` of its own so pack state comes from the including file, and the pragmas in whd's public types header are balanced `whd/inc/whd_types.h:880`, `whd/inc/whd_types.h:904`, `whd/inc/whd_types.h:1120`, `whd/inc/whd_types.h:1147`; the full include chain was not compiled); total size 200 bytes; byte order not stated in the definition (plain C integer types), though whd converts multi-byte values at other use sites with `htod32`/`dtoh32`, i.e. dongle byte order `whd/src/whd_wifi_api.c:589`, `whd/src/whd_wifi_api.c:1213`; definition `whd/src/include/whd_wlioctl.h:1814-1829`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `flags` | `uint32_t` | `WL_TX_POWER_F_*` bits `whd/src/include/whd_wlioctl.h:1807-1811`; `whd/src/include/whd_wlioctl.h:1816` |
| 4 | 2 | `chanspec` | `wl_chanspec_t (uint16_t)` | `wl_chanspec_t` is `uint16_t` `whd/inc/whd_types.h:918`; `whd/src/include/whd_wlioctl.h:1817` |
| 6 | 2 | `local_chanspec` | `wl_chanspec_t (uint16_t)` | `wl_chanspec_t` is `uint16_t` `whd/inc/whd_types.h:918`; `whd/src/include/whd_wlioctl.h:1818` |
| 8 | 1 | `local_max` | `uint8_t` | `whd/src/include/whd_wlioctl.h:1819` |
| 9 | 1 | `local_constraint` | `uint8_t` | `whd/src/include/whd_wlioctl.h:1820` |
| 10 | 2 | `antgain` | `int8_t[2]` | `whd/src/include/whd_wlioctl.h:1821` |
| 12 | 1 | `rf_cores` | `uint8_t` | `whd/src/include/whd_wlioctl.h:1822` |
| 13 | 4 | `est_Pout` | `uint8_t[4]` | `whd/src/include/whd_wlioctl.h:1823` |
| 17 | 1 | `est_Pout_cck` | `uint8_t` | `whd/src/include/whd_wlioctl.h:1824` |
| 18 | 45 | `user_limit` | `uint8_t[45]` | `WL_TX_POWER_RATES` = 45 `whd/src/include/whd_wlioctl.h:1795`; `whd/src/include/whd_wlioctl.h:1825` |
| 63 | 45 | `reg_limit` | `uint8_t[45]` | `whd/src/include/whd_wlioctl.h:1826` |
| 108 | 45 | `board_limit` | `uint8_t[45]` | `whd/src/include/whd_wlioctl.h:1827` |
| 153 | 45 | `target` | `uint8_t[45]` | `whd/src/include/whd_wlioctl.h:1828` |
| 198 | 2 | (pad) | - | trailing compiler padding to 4-byte struct alignment, from natural alignment only: a build with 1-byte packing would give 198 (inferred); the sources do not say which the firmware uses, and no driver here uses the record, so the length on the wire is not confirmed; compiled layout `whd/src/include/whd_wlioctl.h:1814-1829` |

Size check: compiled (x86-64 gcc from an extract of the header, asserted again for arm-none-eabi cortex-m0plus and i386, all three agree; supplied by hand: `ETHER_ADDR_LEN` = 6 `whd/inc/whd_types.h:101`, `wl_chanspec_t` = `uint16_t` `whd/inc/whd_types.h:918`)

Differences: `CURRENT_PWR`, `curpower` and `tx_power_t` are not found in linux, embassy, c-driver or pico-sdk.

### `tx_inst_power_t` (whd)
Instantaneous transmit power estimate with no use site and no command or named variable tied to it found in whd; struct tag `tx_inst_power`; not packed (no `#pragma pack` is in force at the definition: the first one in the file is at `whd/src/include/whd_wlioctl.h:3864`, the header has no `#include` of its own so pack state comes from the including file, and the pragmas in whd's public types header are balanced `whd/inc/whd_types.h:880`, `whd/inc/whd_types.h:904`, `whd/inc/whd_types.h:1120`, `whd/inc/whd_types.h:1147`; the full include chain was not compiled), and no padding either way since all fields are bytes; total size 3 bytes; byte order does not apply (every field is a single byte or byte array); definition `whd/src/include/whd_wlioctl.h:1830-1834`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 2 | `txpwr_est_Pout` | `uint8_t[2]` | `whd/src/include/whd_wlioctl.h:1832` |
| 2 | 1 | `txpwr_est_Pout_gofdm` | `uint8_t` | `whd/src/include/whd_wlioctl.h:1833` |

Size check: compiled (x86-64 gcc from an extract of the header, asserted again for arm-none-eabi cortex-m0plus and i386, all three agree; supplied by hand: `ETHER_ADDR_LEN` = 6 `whd/inc/whd_types.h:101`, `wl_chanspec_t` = `uint16_t` `whd/inc/whd_types.h:918`)

Differences: not found by name in linux, embassy, c-driver or pico-sdk.

### `wl_vndr_ie_t` (whd)
Vendor-specific information element carried inside the named variable (iovar) `vndr_ie`, embedded in `vndr_ie_info_t` and filled by whd's `whd_wifi_manage_custom_ie`; not packed (`BWL_DEFAULT_PACKING` is defined empty and the header's first `#pragma pack` is at line 3864, after the definition; alignment 1, no padding); 5 fixed bytes plus a variable tail, `sizeof` 6 with the `data[1]` placeholder (compiled on an x86-64 host; the 32-bit ARM layout is inferred from member types, all 1-, 2- or 4-byte integers); byte fields only, so no endianness question; the struct tag is `struct wl_vndr_ie` and the typedef is on line 1952. `whd/src/include/whd_wlioctl.h:1945-1951` `whd/src/include/whd_wlioctl.h:1952` `whd/src/include/whd_wlioctl.h:1087` `whd/src/include/whd_wlioctl.h:1956` `whd/src/include/whd_wlioctl.h:467` `whd/src/include/whd_wlioctl.h:3864` `whd/src/whd_wifi_api.c:4308-4318`

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 1 | `id` | `uint8_t` | 221 (0xdd) at the use site `whd/src/whd_wifi_api.c:4308`. `whd/src/include/whd_wlioctl.h:1947` |
| 1 | 1 | `len` | `uint8_t` | covers oui + data: whd sets it to payload length + 3 + 1 `whd/src/whd_wifi_api.c:4309-4310`. `whd/src/include/whd_wlioctl.h:1948` |
| 2 | 3 | `oui` | `uint8_t[3]` | `whd/src/include/whd_wlioctl.h:1949` |
| 5 | variable (1 declared) | `data` | `uint8_t[1]` | flexible array declared as [1]; first byte is the subtype at the use site `whd/src/whd_wifi_api.c:4316`, payload follows from `data[1]` `whd/src/whd_wifi_api.c:4318`. `whd/src/include/whd_wlioctl.h:1950` |

Size check: compiled

Differences: no layout difference from linux, which has no struct for the IE and copies a ready-made IE to offset 12 of the set buffer `linux/brcmfmac/cfg80211.c:72-75` `linux/brcmfmac/cfg80211.c:4902-4913`. embassy, c-driver, pico-sdk: not found in these sources.

### `vndr_ie_info_t` (whd)
One list element of the `vndr_ie` variable's buffer, packet-type flags plus one vendor IE; not packed (`BWL_DEFAULT_PACKING` is defined empty and the header's first `#pragma pack` is at line 3864, after the definition; alignment 4); 9 fixed bytes plus a variable tail, `sizeof` 12 with 1 placeholder byte and 2 bytes of tail padding (compiled on an x86-64 host; the 32-bit ARM layout is inferred from member types, all 1-, 2- or 4-byte integers); endianness not stated in the definition, little-endian as whd writes it (`htod32` is the identity unless `IL_BIGENDIAN` is defined). `whd/src/include/whd_wlioctl.h:1953-1957` `whd/src/include/whd_wlioctl.h:467` `whd/src/include/whd_wlioctl.h:3864` `whd/src/include/whd_endian.h:44-56` `whd/src/whd_wifi_api.c:4307` `whd/src/whd_wifi_api.c:4311`

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `pktflag` | `uint32_t` | written with htod32(which_packets) `whd/src/whd_wifi_api.c:4307`; flag bits are the `VNDR_IE_*_FLAG` constants: beacon 1 (0x1), probe response 2 (0x2), association response 4 (0x4), authentication response 8 (0x8), probe request 16 (0x10), association request 32 (0x20), custom 256 (0x100) `whd/src/include/whd_wlioctl.h:1937-1943`; `VNDR_IE_INFO_HDR_LEN` is `sizeof(uint32_t)`, this word `whd/src/include/whd_wlioctl.h:1944`. `whd/src/include/whd_wlioctl.h:1955` |
| 4 | variable (6 in sizeof) | `vndr_ie_data` | `wl_vndr_ie_t` | nested wl_vndr_ie_t at offset 4: id@4, len@5, oui@6..8, data@9 (flexible). `whd/src/include/whd_wlioctl.h:1956` |
| 10 | 2 | (pad) | (pad) | tail padding counted by sizeof (struct alignment 4); not meaningful on the wire because the preceding member is a flexible tail; on the wire the IE data runs through these 2 bytes (inferred) `whd/src/include/whd_wlioctl.h:1950` `whd/src/include/whd_wlioctl.h:1956`. `whd/src/include/whd_wlioctl.h:1953-1957` |

Size check: compiled

Differences: no layout difference from linux, which has no struct and writes the same bytes by offset: command string at 0 (4 bytes), count at 4, packet flags at 8, IE at 12, with `put_unaligned_le32` `linux/brcmfmac/cfg80211.c:69-75` `linux/brcmfmac/cfg80211.c:4902-4913`. embassy, c-driver, pico-sdk: not found in these sources.

### `vndr_ie_buf_t` (whd)
Body of the `vndr_ie` variable after the command word, an IE count followed by the list; not packed (`BWL_DEFAULT_PACKING` is defined empty and the header's first `#pragma pack` is at line 3864, after the definition; alignment 4); 13 fixed bytes plus a variable tail, `sizeof` 16 (compiled on an x86-64 host; the 32-bit ARM layout is inferred from member types, all 1-, 2- or 4-byte integers); endianness not stated in the definition, little-endian as whd writes it (`htod32` is the identity unless `IL_BIGENDIAN` is defined). `whd/src/include/whd_wlioctl.h:1958-1962` `whd/src/include/whd_wlioctl.h:467` `whd/src/include/whd_wlioctl.h:3864` `whd/src/include/whd_endian.h:44-56` `whd/src/whd_wifi_api.c:4307` `whd/src/whd_wifi_api.c:4311`

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `iecount` | `int32_t` | written with htod32(1) `whd/src/whd_wifi_api.c:4311`; whd only ever sends one element, `iecount` = 1 and `vndr_ie_list[0]` `whd/src/whd_wifi_api.c:4307-4318`. `whd/src/include/whd_wlioctl.h:1960` |
| 4 | variable (12 in sizeof) | `vndr_ie_list` | `vndr_ie_info_t[1]` | array declared as [1] of a variable-length element: pktflag@4, id@8, len@9, oui@10..12, data@13 (flexible); sizeof includes 2 tail padding bytes at 14..15. `whd/src/include/whd_wlioctl.h:1961` |

Size check: compiled

Differences: no layout difference from linux, which has no struct and writes the same bytes by offset: command string at 0 (4 bytes), count at 4, packet flags at 8, IE at 12, with `put_unaligned_le32` `linux/brcmfmac/cfg80211.c:69-75` `linux/brcmfmac/cfg80211.c:4902-4913`; linux also always writes a count of 1 `linux/brcmfmac/cfg80211.c:4906`. embassy, c-driver, pico-sdk: not found in these sources.

### `vndr_ie_setbuf_t` (whd)
Payload of the set of named variable `bsscfg:vndr_ie`, built in whd's `whd_wifi_manage_custom_ie`, where it follows the 4-byte bsscfg index that starts the variable's data; not packed (`BWL_DEFAULT_PACKING` is defined empty and the header's first `#pragma pack` is at line 3864, after the definition; alignment 4); 17 fixed bytes plus a variable tail, `sizeof` 20 (compiled on an x86-64 host; the 32-bit ARM layout is inferred from member types, all 1-, 2- or 4-byte integers); endianness not stated in the definition, little-endian as whd writes it (`htod32` is the identity unless `IL_BIGENDIAN` is defined), except that whd stores the bsscfg index without `htod32`. `whd/src/include/whd_wlioctl.h:1963-1967` `whd/src/whd_wifi_api.c:4254-4321` `whd/src/whd_wifi_api.c:4289-4293` `whd/src/whd_wifi_api.c:4292` `whd/src/include/whd_wlioctl.h:467` `whd/src/include/whd_wlioctl.h:3864` `whd/src/include/whd_endian.h:44-56` `whd/src/whd_wifi_api.c:4307` `whd/src/whd_wifi_api.c:4311`

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `cmd` | `int8_t[VNDR_IE_CMD_LEN]` | "add" or "del", NUL at index 3 `whd/src/whd_wifi_api.c:4298-4304`; VNDR_IE_CMD_LEN = 4 `whd/src/include/whd_wlioctl.h:1936`. `whd/src/include/whd_wlioctl.h:1965` |
| 4 | variable (16 in sizeof) | `vndr_ie_buffer` | `vndr_ie_buf_t` | nested vndr_ie_buf_t at offset 4: iecount@4, pktflag@8, id@12, len@13, oui@14..16, data@17 (flexible; subtype byte then payload); sizeof includes 2 tail padding bytes at 18..19; whd requests a buffer of `sizeof(vndr_ie_setbuf_t)` + length + 4 = 24 + length bytes `whd/src/whd_wifi_api.c:4289` and writes 4 (index) + 17 (fixed part) + 1 (subtype) + length = 22 + length bytes, the 2 extra requested bytes being the `sizeof` tail padding `whd/src/whd_wifi_api.c:4292-4318`; whether those 2 trailing bytes go on the wire depends on `whd_proto_set_iovar` sending the whole requested length (not traced) `whd/src/whd_wifi_api.c:4320`; whd rejects the call if 3 + 1 + length exceeds `VNDR_IE_MAX_LEN` = 255 `whd/src/whd_wifi_api.c:4270` `whd/inc/whd_types.h:183-184` or if the packet flags fall outside its `VENDOR_IE_*` set `whd/src/whd_wifi_api.c:4276` `whd/inc/whd_types.h:1423`. `whd/src/include/whd_wlioctl.h:1966` |

Size check: compiled

Differences: no layout difference from linux, which builds the same body by byte offset with no struct: `cmd` at 0 (`VNDR_IE_CMD_LEN` 4), count at 4, packet flags at 8, IE at 12 `linux/brcmfmac/cfg80211.c:69-75` `linux/brcmfmac/cfg80211.c:4902-4913`; linux writes count and flags with `put_unaligned_le32`, stating little-endian explicitly `linux/brcmfmac/cfg80211.c:4906-4908`, and sends the body as bsscfg variable `vndr_ie` `linux/brcmfmac/cfg80211.c:5069`. embassy, c-driver, pico-sdk: not found in these sources (no `vndr_ie` or vendor IE code).

### `tsinfo_arg` (whd)
3-byte array embedded in `struct ts_list` and `tspec_arg`, with no command, named variable or event in whd's .c files using it, so its place among wire records rests only on the two embeddings; not packed (`BWL_DEFAULT_PACKING` is defined empty and the header's first `#pragma pack` is at line 3864, after the definition; alignment 1); 3 bytes (compiled on an x86-64 host; the 32-bit ARM layout is inferred from member types, all 1-, 2- or 4-byte integers); byte array, so no endianness question; struct tag only, no typedef. `whd/src/include/whd_wlioctl.h:1973-1976` `whd/src/include/whd_wlioctl.h:3407` `whd/src/include/whd_wlioctl.h:3414` `whd/src/include/whd_wlioctl.h:467` `whd/src/include/whd_wlioctl.h:3864`

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 3 | `octets` | `uint8_t[3]` | the header has no comment saying what the bytes mean; reading them as the 802.11 TS Info field is from the name (recalled, not in these sources). `whd/src/include/whd_wlioctl.h:1975` |

Size check: compiled

### `wl_cnt_info_t` (whd)
Header of a versioned counters report, with no command, named variable or event tied to it: the header defines the variable name "counters" (`IOVAR_STR_COUNTERS`), but no `.c` or `.rs` file of whd, embassy, c-driver or pico-sdk refers to that name or to this type; not packed (`BWL_DEFAULT_PACKING` is defined empty and the header's first `#pragma pack` is at line 3864, after the definition; alignment 2); 4 fixed bytes plus a variable tail, `sizeof` 6 with 1 placeholder byte and 1 byte of tail padding (compiled on an x86-64 host; the 32-bit ARM layout is inferred from member types, all 1-, 2- or 4-byte integers); endianness not stated in the definition. `whd/src/include/whd_wlioctl.h:1987-1996` `whd/src/include/whd_wlioctl.h:1091` `whd/src/include/whd_wlioctl.h:467` `whd/src/include/whd_wlioctl.h:3864`

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 2 | `version` | `uint16_t` | see WL_CNT_T_VERSION (= 6) `whd/src/include/whd_wlioctl.h:1984`. `whd/src/include/whd_wlioctl.h:1989` |
| 2 | 2 | `datalen` | `uint16_t` | length of data including all paddings. `whd/src/include/whd_wlioctl.h:1990` |
| 4 | variable (1 declared) | `data` | `uint8_t[1]` | flexible array declared as [1]: the header comment says it holds one or more `bcm_xtlv_t` tuples, each padded to a multiple of 4 bytes, and that `datalen` includes the padding `whd/src/include/whd_wlioctl.h:1989-1995`. `whd/src/include/whd_wlioctl.h:1991` |
| 5 | 1 | (pad) | (pad) | tail padding counted by sizeof (struct alignment 2); not meaningful on the wire because the preceding member is a flexible tail (inferred) `whd/src/include/whd_wlioctl.h:1991`. `whd/src/include/whd_wlioctl.h:1987-1996` |

Size check: compiled

Differences: the type name is not found in linux, embassy, c-driver or pico-sdk; the only other "counters" name in these sources is a linux debugfs entry, unrelated to this variable. `linux/brcmfmac/sdio.c:3230`

### `wl_cnt_ver_30_t` (whd)
"wlc layer counters" per the header comment, with no command, named variable or event tied to it: which command, variable or xtlv id carries it is not stated in these sources, and no `.c` or `.rs` file of whd, embassy, c-driver or pico-sdk refers to this type or to `IOVAR_STR_COUNTERS` (that it is the payload of an xtlv inside `wl_cnt_info_t` is recalled, not in these sources; the header does not explain the "30" in the name either); not packed (`BWL_DEFAULT_PACKING` is defined empty and the header's first `#pragma pack` is at line 3864, after the definition; alignment 4); 772 bytes (compiled on an x86-64 host; the 32-bit ARM layout is inferred from member types, all 1-, 2- or 4-byte integers); endianness not stated in the definition; it has no version or length field, unlike the six, seven and eight variants, which each start with `version` and `length`; the header says every counter must be `uint32_t` and none may be removed or renamed mid-struct; the field notes are the header's own comments, whd's names for the counters. `whd/src/include/whd_wlioctl.h:1998-2214` `whd/src/include/whd_wlioctl.h:1997` `whd/src/include/whd_wlioctl.h:2211-2213` `whd/src/include/whd_wlioctl.h:2217-2218` `whd/src/include/whd_wlioctl.h:2449-2450` `whd/src/include/whd_wlioctl.h:2682-2683` `whd/src/include/whd_wlioctl.h:467` `whd/src/include/whd_wlioctl.h:3864`

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `txframe` | `uint32_t` | tx data frames. `whd/src/include/whd_wlioctl.h:2001` |
| 4 | 4 | `txbyte` | `uint32_t` | tx data bytes. `whd/src/include/whd_wlioctl.h:2002` |
| 8 | 4 | `txretrans` | `uint32_t` | tx mac retransmits. `whd/src/include/whd_wlioctl.h:2003` |
| 12 | 4 | `txerror` | `uint32_t` | tx data errors (derived: sum of others). `whd/src/include/whd_wlioctl.h:2004` |
| 16 | 4 | `txctl` | `uint32_t` | tx management frames. `whd/src/include/whd_wlioctl.h:2005` |
| 20 | 4 | `txprshort` | `uint32_t` | tx short preamble frames. `whd/src/include/whd_wlioctl.h:2006` |
| 24 | 4 | `txserr` | `uint32_t` | tx status errors. `whd/src/include/whd_wlioctl.h:2007` |
| 28 | 4 | `txnobuf` | `uint32_t` | tx out of buffers errors. `whd/src/include/whd_wlioctl.h:2008` |
| 32 | 4 | `txnoassoc` | `uint32_t` | tx discard because we're not associated. `whd/src/include/whd_wlioctl.h:2009` |
| 36 | 4 | `txrunt` | `uint32_t` | tx runt frames. `whd/src/include/whd_wlioctl.h:2010` |
| 40 | 4 | `txchit` | `uint32_t` | tx header cache hit (fastpath). `whd/src/include/whd_wlioctl.h:2011` |
| 44 | 4 | `txcmiss` | `uint32_t` | tx header cache miss (slowpath). `whd/src/include/whd_wlioctl.h:2012` |
| 48 | 4 | `txuflo` | `uint32_t` | tx fifo underflows. `whd/src/include/whd_wlioctl.h:2015` |
| 52 | 4 | `txphyerr` | `uint32_t` | tx phy errors (indicated in tx status). `whd/src/include/whd_wlioctl.h:2016` |
| 56 | 4 | `txphycrs` | `uint32_t` | PR8861/8963 counter. `whd/src/include/whd_wlioctl.h:2017` |
| 60 | 4 | `rxframe` | `uint32_t` | rx data frames. `whd/src/include/whd_wlioctl.h:2020` |
| 64 | 4 | `rxbyte` | `uint32_t` | rx data bytes. `whd/src/include/whd_wlioctl.h:2021` |
| 68 | 4 | `rxerror` | `uint32_t` | rx data errors (derived: sum of others). `whd/src/include/whd_wlioctl.h:2022` |
| 72 | 4 | `rxctl` | `uint32_t` | rx management frames. `whd/src/include/whd_wlioctl.h:2023` |
| 76 | 4 | `rxnobuf` | `uint32_t` | rx out of buffers errors. `whd/src/include/whd_wlioctl.h:2024` |
| 80 | 4 | `rxnondata` | `uint32_t` | error count for non-data frames received on the data channel. `whd/src/include/whd_wlioctl.h:2025` |
| 84 | 4 | `rxbadds` | `uint32_t` | rx bad DS errors. `whd/src/include/whd_wlioctl.h:2026` |
| 88 | 4 | `rxbadcm` | `uint32_t` | rx bad control or management frames. `whd/src/include/whd_wlioctl.h:2027` |
| 92 | 4 | `rxfragerr` | `uint32_t` | rx fragmentation errors. `whd/src/include/whd_wlioctl.h:2028` |
| 96 | 4 | `rxrunt` | `uint32_t` | rx runt frames. `whd/src/include/whd_wlioctl.h:2029` |
| 100 | 4 | `rxgiant` | `uint32_t` | rx giant frames. `whd/src/include/whd_wlioctl.h:2030` |
| 104 | 4 | `rxnoscb` | `uint32_t` | rx no scb error. `whd/src/include/whd_wlioctl.h:2031` |
| 108 | 4 | `rxbadproto` | `uint32_t` | rx invalid frames. `whd/src/include/whd_wlioctl.h:2032` |
| 112 | 4 | `rxbadsrcmac` | `uint32_t` | rx frames with Invalid Src Mac. `whd/src/include/whd_wlioctl.h:2033` |
| 116 | 4 | `rxbadda` | `uint32_t` | rx frames tossed for invalid da. `whd/src/include/whd_wlioctl.h:2034` |
| 120 | 4 | `rxfilter` | `uint32_t` | rx frames filtered out. `whd/src/include/whd_wlioctl.h:2035` |
| 124 | 4 | `rxoflo` | `uint32_t` | rx fifo overflow errors. `whd/src/include/whd_wlioctl.h:2038` |
| 128 | 24 | `rxuflo` | `uint32_t[NFIFO]` | rx dma descriptor underflow errors; array of NFIFO = 6 `whd/src/include/whd_wlioctl.h:1983`. `whd/src/include/whd_wlioctl.h:2039` |
| 152 | 4 | `d11cnt_txrts_off` | `uint32_t` | d11cnt txrts value when reset d11cnt. `whd/src/include/whd_wlioctl.h:2041` |
| 156 | 4 | `d11cnt_rxcrc_off` | `uint32_t` | d11cnt rxcrc value when reset d11cnt. `whd/src/include/whd_wlioctl.h:2042` |
| 160 | 4 | `d11cnt_txnocts_off` | `uint32_t` | d11cnt txnocts value when reset d11cnt. `whd/src/include/whd_wlioctl.h:2043` |
| 164 | 4 | `dmade` | `uint32_t` | tx/rx dma descriptor errors. `whd/src/include/whd_wlioctl.h:2046` |
| 168 | 4 | `dmada` | `uint32_t` | tx/rx dma data errors. `whd/src/include/whd_wlioctl.h:2047` |
| 172 | 4 | `dmape` | `uint32_t` | tx/rx dma descriptor protocol errors. `whd/src/include/whd_wlioctl.h:2048` |
| 176 | 4 | `reset` | `uint32_t` | reset count. `whd/src/include/whd_wlioctl.h:2049` |
| 180 | 4 | `tbtt` | `uint32_t` | cnts the TBTT int's. `whd/src/include/whd_wlioctl.h:2050` |
| 184 | 4 | `txdmawar` | `uint32_t` | # occurrences of PR15420 workaround. `whd/src/include/whd_wlioctl.h:2051` |
| 188 | 4 | `pkt_callback_reg_fail` | `uint32_t` | callbacks register failure. `whd/src/include/whd_wlioctl.h:2052` |
| 192 | 4 | `txfrag` | `uint32_t` | dot11TransmittedFragmentCount. `whd/src/include/whd_wlioctl.h:2055` |
| 196 | 4 | `txmulti` | `uint32_t` | dot11MulticastTransmittedFrameCount. `whd/src/include/whd_wlioctl.h:2056` |
| 200 | 4 | `txfail` | `uint32_t` | dot11FailedCount. `whd/src/include/whd_wlioctl.h:2057` |
| 204 | 4 | `txretry` | `uint32_t` | dot11RetryCount. `whd/src/include/whd_wlioctl.h:2058` |
| 208 | 4 | `txretrie` | `uint32_t` | dot11MultipleRetryCount. `whd/src/include/whd_wlioctl.h:2059` |
| 212 | 4 | `rxdup` | `uint32_t` | dot11FrameduplicateCount. `whd/src/include/whd_wlioctl.h:2060` |
| 216 | 4 | `txrts` | `uint32_t` | dot11RTSSuccessCount. `whd/src/include/whd_wlioctl.h:2061` |
| 220 | 4 | `txnocts` | `uint32_t` | dot11RTSFailureCount. `whd/src/include/whd_wlioctl.h:2062` |
| 224 | 4 | `txnoack` | `uint32_t` | dot11ACKFailureCount. `whd/src/include/whd_wlioctl.h:2063` |
| 228 | 4 | `rxfrag` | `uint32_t` | dot11ReceivedFragmentCount. `whd/src/include/whd_wlioctl.h:2064` |
| 232 | 4 | `rxmulti` | `uint32_t` | dot11MulticastReceivedFrameCount. `whd/src/include/whd_wlioctl.h:2065` |
| 236 | 4 | `rxcrc` | `uint32_t` | dot11FCSErrorCount. `whd/src/include/whd_wlioctl.h:2066` |
| 240 | 4 | `txfrmsnt` | `uint32_t` | dot11TransmittedFrameCount (bogus MIB?). `whd/src/include/whd_wlioctl.h:2067` |
| 244 | 4 | `rxundec` | `uint32_t` | dot11WEPUndecryptableCount. `whd/src/include/whd_wlioctl.h:2068` |
| 248 | 4 | `tkipmicfaill` | `uint32_t` | TKIPLocalMICFailures. `whd/src/include/whd_wlioctl.h:2071` |
| 252 | 4 | `tkipcntrmsr` | `uint32_t` | TKIPCounterMeasuresInvoked. `whd/src/include/whd_wlioctl.h:2072` |
| 256 | 4 | `tkipreplay` | `uint32_t` | TKIPReplays. `whd/src/include/whd_wlioctl.h:2073` |
| 260 | 4 | `ccmpfmterr` | `uint32_t` | CCMPFormatErrors. `whd/src/include/whd_wlioctl.h:2074` |
| 264 | 4 | `ccmpreplay` | `uint32_t` | CCMPReplays. `whd/src/include/whd_wlioctl.h:2075` |
| 268 | 4 | `ccmpundec` | `uint32_t` | CCMPDecryptErrors. `whd/src/include/whd_wlioctl.h:2076` |
| 272 | 4 | `fourwayfail` | `uint32_t` | FourWayHandshakeFailures. `whd/src/include/whd_wlioctl.h:2077` |
| 276 | 4 | `wepundec` | `uint32_t` | dot11WEPUndecryptableCount. `whd/src/include/whd_wlioctl.h:2078` |
| 280 | 4 | `wepicverr` | `uint32_t` | dot11WEPICVErrorCount. `whd/src/include/whd_wlioctl.h:2079` |
| 284 | 4 | `decsuccess` | `uint32_t` | DecryptSuccessCount. `whd/src/include/whd_wlioctl.h:2080` |
| 288 | 4 | `tkipicverr` | `uint32_t` | TKIPICVErrorCount. `whd/src/include/whd_wlioctl.h:2081` |
| 292 | 4 | `wepexcluded` | `uint32_t` | dot11WEPExcludedCount. `whd/src/include/whd_wlioctl.h:2082` |
| 296 | 4 | `txchanrej` | `uint32_t` | Tx frames suppressed due to channel rejection. `whd/src/include/whd_wlioctl.h:2084` |
| 300 | 4 | `psmwds` | `uint32_t` | Count PSM watchdogs. `whd/src/include/whd_wlioctl.h:2085` |
| 304 | 4 | `phywatchdog` | `uint32_t` | Count Phy watchdogs (triggered by ucode). `whd/src/include/whd_wlioctl.h:2086` |
| 308 | 4 | `prq_entries_handled` | `uint32_t` | PRQ entries read in. `whd/src/include/whd_wlioctl.h:2089` |
| 312 | 4 | `prq_undirected_entries` | `uint32_t` | which were bcast bss & ssid. `whd/src/include/whd_wlioctl.h:2090` |
| 316 | 4 | `prq_bad_entries` | `uint32_t` | which could not be translated to info. `whd/src/include/whd_wlioctl.h:2091` |
| 320 | 4 | `atim_suppress_count` | `uint32_t` | TX suppressions on ATIM fifo. `whd/src/include/whd_wlioctl.h:2092` |
| 324 | 4 | `bcn_template_not_ready` | `uint32_t` | Template marked in use on send bcn . `whd/src/include/whd_wlioctl.h:2093` |
| 328 | 4 | `bcn_template_not_ready_done` | `uint32_t` | ...but "DMA done" interrupt rcvd. `whd/src/include/whd_wlioctl.h:2094` |
| 332 | 4 | `late_tbtt_dpc` | `uint32_t` | TBTT DPC did not happen in time. `whd/src/include/whd_wlioctl.h:2095` |
| 336 | 4 | `rx1mbps` | `uint32_t` | packets rx at 1Mbps. `whd/src/include/whd_wlioctl.h:2098` |
| 340 | 4 | `rx2mbps` | `uint32_t` | packets rx at 2Mbps. `whd/src/include/whd_wlioctl.h:2099` |
| 344 | 4 | `rx5mbps5` | `uint32_t` | packets rx at 5.5Mbps. `whd/src/include/whd_wlioctl.h:2100` |
| 348 | 4 | `rx6mbps` | `uint32_t` | packets rx at 6Mbps. `whd/src/include/whd_wlioctl.h:2101` |
| 352 | 4 | `rx9mbps` | `uint32_t` | packets rx at 9Mbps. `whd/src/include/whd_wlioctl.h:2102` |
| 356 | 4 | `rx11mbps` | `uint32_t` | packets rx at 11Mbps. `whd/src/include/whd_wlioctl.h:2103` |
| 360 | 4 | `rx12mbps` | `uint32_t` | packets rx at 12Mbps. `whd/src/include/whd_wlioctl.h:2104` |
| 364 | 4 | `rx18mbps` | `uint32_t` | packets rx at 18Mbps. `whd/src/include/whd_wlioctl.h:2105` |
| 368 | 4 | `rx24mbps` | `uint32_t` | packets rx at 24Mbps. `whd/src/include/whd_wlioctl.h:2106` |
| 372 | 4 | `rx36mbps` | `uint32_t` | packets rx at 36Mbps. `whd/src/include/whd_wlioctl.h:2107` |
| 376 | 4 | `rx48mbps` | `uint32_t` | packets rx at 48Mbps. `whd/src/include/whd_wlioctl.h:2108` |
| 380 | 4 | `rx54mbps` | `uint32_t` | packets rx at 54Mbps. `whd/src/include/whd_wlioctl.h:2109` |
| 384 | 4 | `rx108mbps` | `uint32_t` | packets rx at 108mbps. `whd/src/include/whd_wlioctl.h:2110` |
| 388 | 4 | `rx162mbps` | `uint32_t` | packets rx at 162mbps. `whd/src/include/whd_wlioctl.h:2111` |
| 392 | 4 | `rx216mbps` | `uint32_t` | packets rx at 216 mbps. `whd/src/include/whd_wlioctl.h:2112` |
| 396 | 4 | `rx270mbps` | `uint32_t` | packets rx at 270 mbps. `whd/src/include/whd_wlioctl.h:2113` |
| 400 | 4 | `rx324mbps` | `uint32_t` | packets rx at 324 mbps. `whd/src/include/whd_wlioctl.h:2114` |
| 404 | 4 | `rx378mbps` | `uint32_t` | packets rx at 378 mbps. `whd/src/include/whd_wlioctl.h:2115` |
| 408 | 4 | `rx432mbps` | `uint32_t` | packets rx at 432 mbps. `whd/src/include/whd_wlioctl.h:2116` |
| 412 | 4 | `rx486mbps` | `uint32_t` | packets rx at 486 mbps. `whd/src/include/whd_wlioctl.h:2117` |
| 416 | 4 | `rx540mbps` | `uint32_t` | packets rx at 540 mbps. `whd/src/include/whd_wlioctl.h:2118` |
| 420 | 4 | `rfdisable` | `uint32_t` | count of radio disables. `whd/src/include/whd_wlioctl.h:2120` |
| 424 | 4 | `txexptime` | `uint32_t` | Tx frames suppressed due to timer expiration. `whd/src/include/whd_wlioctl.h:2122` |
| 428 | 4 | `txmpdu_sgi` | `uint32_t` | count for sgi transmit. `whd/src/include/whd_wlioctl.h:2124` |
| 432 | 4 | `rxmpdu_sgi` | `uint32_t` | count for sgi received. `whd/src/include/whd_wlioctl.h:2125` |
| 436 | 4 | `txmpdu_stbc` | `uint32_t` | count for stbc transmit. `whd/src/include/whd_wlioctl.h:2126` |
| 440 | 4 | `rxmpdu_stbc` | `uint32_t` | count for stbc received. `whd/src/include/whd_wlioctl.h:2127` |
| 444 | 4 | `rxundec_mcst` | `uint32_t` | dot11WEPUndecryptableCount. `whd/src/include/whd_wlioctl.h:2129` |
| 448 | 4 | `tkipmicfaill_mcst` | `uint32_t` | TKIPLocalMICFailures. `whd/src/include/whd_wlioctl.h:2132` |
| 452 | 4 | `tkipcntrmsr_mcst` | `uint32_t` | TKIPCounterMeasuresInvoked. `whd/src/include/whd_wlioctl.h:2133` |
| 456 | 4 | `tkipreplay_mcst` | `uint32_t` | TKIPReplays. `whd/src/include/whd_wlioctl.h:2134` |
| 460 | 4 | `ccmpfmterr_mcst` | `uint32_t` | CCMPFormatErrors. `whd/src/include/whd_wlioctl.h:2135` |
| 464 | 4 | `ccmpreplay_mcst` | `uint32_t` | CCMPReplays. `whd/src/include/whd_wlioctl.h:2136` |
| 468 | 4 | `ccmpundec_mcst` | `uint32_t` | CCMPDecryptErrors. `whd/src/include/whd_wlioctl.h:2137` |
| 472 | 4 | `fourwayfail_mcst` | `uint32_t` | FourWayHandshakeFailures. `whd/src/include/whd_wlioctl.h:2138` |
| 476 | 4 | `wepundec_mcst` | `uint32_t` | dot11WEPUndecryptableCount. `whd/src/include/whd_wlioctl.h:2139` |
| 480 | 4 | `wepicverr_mcst` | `uint32_t` | dot11WEPICVErrorCount. `whd/src/include/whd_wlioctl.h:2140` |
| 484 | 4 | `decsuccess_mcst` | `uint32_t` | DecryptSuccessCount. `whd/src/include/whd_wlioctl.h:2141` |
| 488 | 4 | `tkipicverr_mcst` | `uint32_t` | TKIPICVErrorCount. `whd/src/include/whd_wlioctl.h:2142` |
| 492 | 4 | `wepexcluded_mcst` | `uint32_t` | dot11WEPExcludedCount. `whd/src/include/whd_wlioctl.h:2143` |
| 496 | 4 | `dma_hang` | `uint32_t` | count for dma hang. `whd/src/include/whd_wlioctl.h:2145` |
| 500 | 4 | `reinit` | `uint32_t` | count for reinit. `whd/src/include/whd_wlioctl.h:2146` |
| 504 | 4 | `pstatxucast` | `uint32_t` | ucast frames transmitted, summed over every psta assoc. `whd/src/include/whd_wlioctl.h:2148` |
| 508 | 4 | `pstatxnoassoc` | `uint32_t` | txnoassoc frames transmitted, summed over every psta assoc. `whd/src/include/whd_wlioctl.h:2149` |
| 512 | 4 | `pstarxucast` | `uint32_t` | ucast frames received, summed over every psta assoc. `whd/src/include/whd_wlioctl.h:2150` |
| 516 | 4 | `pstarxbcmc` | `uint32_t` | bcmc frames received, summed over every psta. `whd/src/include/whd_wlioctl.h:2151` |
| 520 | 4 | `pstatxbcmc` | `uint32_t` | bcmc frames transmitted, summed over every psta. `whd/src/include/whd_wlioctl.h:2152` |
| 524 | 4 | `cso_passthrough` | `uint32_t` | hw cso required but passthrough. `whd/src/include/whd_wlioctl.h:2154` |
| 528 | 4 | `cso_normal` | `uint32_t` | hw cso hdr for normal process. `whd/src/include/whd_wlioctl.h:2155` |
| 532 | 4 | `chained` | `uint32_t` | number of frames chained. `whd/src/include/whd_wlioctl.h:2156` |
| 536 | 4 | `chainedsz1` | `uint32_t` | number of chain size 1 frames. `whd/src/include/whd_wlioctl.h:2157` |
| 540 | 4 | `unchained` | `uint32_t` | number of frames not chained. `whd/src/include/whd_wlioctl.h:2158` |
| 544 | 4 | `maxchainsz` | `uint32_t` | max chain size so far. `whd/src/include/whd_wlioctl.h:2159` |
| 548 | 4 | `currchainsz` | `uint32_t` | current chain size. `whd/src/include/whd_wlioctl.h:2160` |
| 552 | 4 | `pciereset` | `uint32_t` | Secondary Bus Reset issued by driver. `whd/src/include/whd_wlioctl.h:2161` |
| 556 | 4 | `cfgrestore` | `uint32_t` | configspace restore by driver. `whd/src/include/whd_wlioctl.h:2162` |
| 560 | 32 | `reinitreason` | `uint32_t[NREINITREASONCOUNT]` | reinitreason counters; 0: Unknown reason; array of NREINITREASONCOUNT = 8 `whd/src/include/whd_wlioctl.h:1977`. `whd/src/include/whd_wlioctl.h:2163` |
| 592 | 4 | `rxrtry` | `uint32_t` | `whd/src/include/whd_wlioctl.h:2164` |
| 596 | 4 | `rxmpdu_mu` | `uint32_t` | Number of MU MPDUs received. `whd/src/include/whd_wlioctl.h:2165` |
| 600 | 4 | `txbar` | `uint32_t` | Number of TX BAR. `whd/src/include/whd_wlioctl.h:2168` |
| 604 | 4 | `rxbar` | `uint32_t` | Number of RX BAR. `whd/src/include/whd_wlioctl.h:2169` |
| 608 | 4 | `txpspoll` | `uint32_t` | Number of TX PS-poll. `whd/src/include/whd_wlioctl.h:2170` |
| 612 | 4 | `rxpspoll` | `uint32_t` | Number of RX PS-poll. `whd/src/include/whd_wlioctl.h:2171` |
| 616 | 4 | `txnull` | `uint32_t` | Number of TX NULL_DATA. `whd/src/include/whd_wlioctl.h:2172` |
| 620 | 4 | `rxnull` | `uint32_t` | Number of RX NULL_DATA. `whd/src/include/whd_wlioctl.h:2173` |
| 624 | 4 | `txqosnull` | `uint32_t` | Number of TX NULL_QoSDATA. `whd/src/include/whd_wlioctl.h:2174` |
| 628 | 4 | `rxqosnull` | `uint32_t` | Number of RX NULL_QoSDATA. `whd/src/include/whd_wlioctl.h:2175` |
| 632 | 4 | `txassocreq` | `uint32_t` | Number of TX ASSOC request. `whd/src/include/whd_wlioctl.h:2176` |
| 636 | 4 | `rxassocreq` | `uint32_t` | Number of RX ASSOC request. `whd/src/include/whd_wlioctl.h:2177` |
| 640 | 4 | `txreassocreq` | `uint32_t` | Number of TX REASSOC request. `whd/src/include/whd_wlioctl.h:2178` |
| 644 | 4 | `rxreassocreq` | `uint32_t` | Number of RX REASSOC request. `whd/src/include/whd_wlioctl.h:2179` |
| 648 | 4 | `txdisassoc` | `uint32_t` | Number of TX DISASSOC. `whd/src/include/whd_wlioctl.h:2180` |
| 652 | 4 | `rxdisassoc` | `uint32_t` | Number of RX DISASSOC. `whd/src/include/whd_wlioctl.h:2181` |
| 656 | 4 | `txassocrsp` | `uint32_t` | Number of TX ASSOC response. `whd/src/include/whd_wlioctl.h:2182` |
| 660 | 4 | `rxassocrsp` | `uint32_t` | Number of RX ASSOC response. `whd/src/include/whd_wlioctl.h:2183` |
| 664 | 4 | `txreassocrsp` | `uint32_t` | Number of TX REASSOC response. `whd/src/include/whd_wlioctl.h:2184` |
| 668 | 4 | `rxreassocrsp` | `uint32_t` | Number of RX REASSOC response. `whd/src/include/whd_wlioctl.h:2185` |
| 672 | 4 | `txauth` | `uint32_t` | Number of TX AUTH. `whd/src/include/whd_wlioctl.h:2186` |
| 676 | 4 | `rxauth` | `uint32_t` | Number of RX AUTH. `whd/src/include/whd_wlioctl.h:2187` |
| 680 | 4 | `txdeauth` | `uint32_t` | Number of TX DEAUTH. `whd/src/include/whd_wlioctl.h:2188` |
| 684 | 4 | `rxdeauth` | `uint32_t` | Number of RX DEAUTH. `whd/src/include/whd_wlioctl.h:2189` |
| 688 | 4 | `txprobereq` | `uint32_t` | Number of TX probe request. `whd/src/include/whd_wlioctl.h:2190` |
| 692 | 4 | `rxprobereq` | `uint32_t` | Number of RX probe request. `whd/src/include/whd_wlioctl.h:2191` |
| 696 | 4 | `txprobersp` | `uint32_t` | Number of TX probe response. `whd/src/include/whd_wlioctl.h:2192` |
| 700 | 4 | `rxprobersp` | `uint32_t` | Number of RX probe response. `whd/src/include/whd_wlioctl.h:2193` |
| 704 | 4 | `txaction` | `uint32_t` | Number of TX action frame. `whd/src/include/whd_wlioctl.h:2194` |
| 708 | 4 | `rxaction` | `uint32_t` | Number of RX action frame. `whd/src/include/whd_wlioctl.h:2195` |
| 712 | 4 | `ampdu_wds` | `uint32_t` | Number of AMPDU watchdogs. `whd/src/include/whd_wlioctl.h:2196` |
| 716 | 4 | `txlost` | `uint32_t` | Number of lost packets reported in txs. `whd/src/include/whd_wlioctl.h:2197` |
| 720 | 4 | `txdatamcast` | `uint32_t` | Number of TX multicast data packets. `whd/src/include/whd_wlioctl.h:2198` |
| 724 | 4 | `txdatabcast` | `uint32_t` | Number of TX broadcast data packets. `whd/src/include/whd_wlioctl.h:2199` |
| 728 | 4 | `psmxwds` | `uint32_t` | Number of PSMx watchdogs. `whd/src/include/whd_wlioctl.h:2200` |
| 732 | 4 | `rxback` | `uint32_t` | `whd/src/include/whd_wlioctl.h:2201` |
| 736 | 4 | `txback` | `uint32_t` | `whd/src/include/whd_wlioctl.h:2202` |
| 740 | 4 | `p2p_tbtt` | `uint32_t` | Number of P2P TBTT Events. `whd/src/include/whd_wlioctl.h:2203` |
| 744 | 4 | `p2p_tbtt_miss` | `uint32_t` | Number of P2P TBTT Events Miss. `whd/src/include/whd_wlioctl.h:2204` |
| 748 | 4 | `txqueue_start` | `uint32_t` | `whd/src/include/whd_wlioctl.h:2205` |
| 752 | 4 | `txqueue_end` | `uint32_t` | `whd/src/include/whd_wlioctl.h:2206` |
| 756 | 4 | `txbcast` | `uint32_t` | Broadcast TransmittedFrameCount. `whd/src/include/whd_wlioctl.h:2207` |
| 760 | 4 | `txdropped` | `uint32_t` | tx dropped pkts. `whd/src/include/whd_wlioctl.h:2208` |
| 764 | 4 | `rxbcast` | `uint32_t` | BroadcastReceivedFrameCount. `whd/src/include/whd_wlioctl.h:2209` |
| 768 | 4 | `rxdropped` | `uint32_t` | rx dropped pkts (derived: sum of others). `whd/src/include/whd_wlioctl.h:2210` |

Size check: compiled

Differences: the type name is not found in linux, embassy, c-driver or pico-sdk; the only other "counters" name in these sources is a linux debugfs entry, unrelated to this variable. `linux/brcmfmac/sdio.c:3230`

### `wl_cnt_ver_six_t` (whd)
Counters report, version-6 layout by typedef name, with no command, named variable or event tied to it: the header defines the variable name "counters" (`IOVAR_STR_COUNTERS`), but no `.c` or `.rs` file of whd, embassy, c-driver or pico-sdk refers to that name or to this type; not packed (`BWL_DEFAULT_PACKING` is defined empty and the header's first `#pragma pack` is at line 3864, after the definition; alignment 4); 740 bytes (compiled on an x86-64 host; the 32-bit ARM layout is inferred from member types, all 1-, 2- or 4-byte integers); endianness not stated in the definition; the field notes are the header's own comments, whd's names for the counters. `whd/src/include/whd_wlioctl.h:2215-2445` `whd/src/include/whd_wlioctl.h:1091` `whd/src/include/whd_wlioctl.h:467` `whd/src/include/whd_wlioctl.h:3864`

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 2 | `version` | `uint16_t` | see definition of WL_CNT_T_VERSION, which the header defines as 6. `whd/src/include/whd_wlioctl.h:2217` `whd/src/include/whd_wlioctl.h:1984` |
| 2 | 2 | `length` | `uint16_t` | length of entire structure. `whd/src/include/whd_wlioctl.h:2218` |
| 4 | 4 | `txframe` | `uint32_t` | tx data frames. `whd/src/include/whd_wlioctl.h:2221` |
| 8 | 4 | `txbyte` | `uint32_t` | tx data bytes. `whd/src/include/whd_wlioctl.h:2222` |
| 12 | 4 | `txretrans` | `uint32_t` | tx mac retransmits. `whd/src/include/whd_wlioctl.h:2223` |
| 16 | 4 | `txerror` | `uint32_t` | tx data errors (derived: sum of others). `whd/src/include/whd_wlioctl.h:2224` |
| 20 | 4 | `txctl` | `uint32_t` | tx management frames. `whd/src/include/whd_wlioctl.h:2225` |
| 24 | 4 | `txprshort` | `uint32_t` | tx short preamble frames. `whd/src/include/whd_wlioctl.h:2226` |
| 28 | 4 | `txserr` | `uint32_t` | tx status errors. `whd/src/include/whd_wlioctl.h:2227` |
| 32 | 4 | `txnobuf` | `uint32_t` | tx out of buffers errors. `whd/src/include/whd_wlioctl.h:2228` |
| 36 | 4 | `txnoassoc` | `uint32_t` | tx discard because we're not associated. `whd/src/include/whd_wlioctl.h:2229` |
| 40 | 4 | `txrunt` | `uint32_t` | tx runt frames. `whd/src/include/whd_wlioctl.h:2230` |
| 44 | 4 | `txchit` | `uint32_t` | tx header cache hit (fastpath). `whd/src/include/whd_wlioctl.h:2231` |
| 48 | 4 | `txcmiss` | `uint32_t` | tx header cache miss (slowpath). `whd/src/include/whd_wlioctl.h:2232` |
| 52 | 4 | `txuflo` | `uint32_t` | tx fifo underflows. `whd/src/include/whd_wlioctl.h:2235` |
| 56 | 4 | `txphyerr` | `uint32_t` | tx phy errors (indicated in tx status). `whd/src/include/whd_wlioctl.h:2236` |
| 60 | 4 | `txphycrs` | `uint32_t` | PR8861/8963 counter. `whd/src/include/whd_wlioctl.h:2237` |
| 64 | 4 | `rxframe` | `uint32_t` | rx data frames. `whd/src/include/whd_wlioctl.h:2240` |
| 68 | 4 | `rxbyte` | `uint32_t` | rx data bytes. `whd/src/include/whd_wlioctl.h:2241` |
| 72 | 4 | `rxerror` | `uint32_t` | rx data errors (derived: sum of others). `whd/src/include/whd_wlioctl.h:2242` |
| 76 | 4 | `rxctl` | `uint32_t` | rx management frames. `whd/src/include/whd_wlioctl.h:2243` |
| 80 | 4 | `rxnobuf` | `uint32_t` | rx out of buffers errors. `whd/src/include/whd_wlioctl.h:2244` |
| 84 | 4 | `rxnondata` | `uint32_t` | error count for non-data frames received on the data channel. `whd/src/include/whd_wlioctl.h:2245` |
| 88 | 4 | `rxbadds` | `uint32_t` | rx bad DS errors. `whd/src/include/whd_wlioctl.h:2246` |
| 92 | 4 | `rxbadcm` | `uint32_t` | rx bad control or management frames. `whd/src/include/whd_wlioctl.h:2247` |
| 96 | 4 | `rxfragerr` | `uint32_t` | rx fragmentation errors. `whd/src/include/whd_wlioctl.h:2248` |
| 100 | 4 | `rxrunt` | `uint32_t` | rx runt frames. `whd/src/include/whd_wlioctl.h:2249` |
| 104 | 4 | `rxgiant` | `uint32_t` | rx giant frames. `whd/src/include/whd_wlioctl.h:2250` |
| 108 | 4 | `rxnoscb` | `uint32_t` | rx no scb error. `whd/src/include/whd_wlioctl.h:2251` |
| 112 | 4 | `rxbadproto` | `uint32_t` | rx invalid frames. `whd/src/include/whd_wlioctl.h:2252` |
| 116 | 4 | `rxbadsrcmac` | `uint32_t` | rx frames with Invalid Src Mac. `whd/src/include/whd_wlioctl.h:2253` |
| 120 | 4 | `rxbadda` | `uint32_t` | rx frames tossed for invalid da. `whd/src/include/whd_wlioctl.h:2254` |
| 124 | 4 | `rxfilter` | `uint32_t` | rx frames filtered out. `whd/src/include/whd_wlioctl.h:2255` |
| 128 | 4 | `rxoflo` | `uint32_t` | rx fifo overflow errors. `whd/src/include/whd_wlioctl.h:2258` |
| 132 | 24 | `rxuflo` | `uint32_t[NFIFO]` | rx dma descriptor underflow errors; array of NFIFO = 6 `whd/src/include/whd_wlioctl.h:1983`. `whd/src/include/whd_wlioctl.h:2259` |
| 156 | 4 | `d11cnt_txrts_off` | `uint32_t` | d11cnt txrts value when reset d11cnt. `whd/src/include/whd_wlioctl.h:2261` |
| 160 | 4 | `d11cnt_rxcrc_off` | `uint32_t` | d11cnt rxcrc value when reset d11cnt. `whd/src/include/whd_wlioctl.h:2262` |
| 164 | 4 | `d11cnt_txnocts_off` | `uint32_t` | d11cnt txnocts value when reset d11cnt. `whd/src/include/whd_wlioctl.h:2263` |
| 168 | 4 | `dmade` | `uint32_t` | tx/rx dma descriptor errors. `whd/src/include/whd_wlioctl.h:2266` |
| 172 | 4 | `dmada` | `uint32_t` | tx/rx dma data errors. `whd/src/include/whd_wlioctl.h:2267` |
| 176 | 4 | `dmape` | `uint32_t` | tx/rx dma descriptor protocol errors. `whd/src/include/whd_wlioctl.h:2268` |
| 180 | 4 | `reset` | `uint32_t` | reset count. `whd/src/include/whd_wlioctl.h:2269` |
| 184 | 4 | `tbtt` | `uint32_t` | cnts the TBTT int's. `whd/src/include/whd_wlioctl.h:2270` |
| 188 | 4 | `txdmawar` | `uint32_t` | # occurrences of PR15420 workaround. `whd/src/include/whd_wlioctl.h:2271` |
| 192 | 4 | `pkt_callback_reg_fail` | `uint32_t` | callbacks register failure. `whd/src/include/whd_wlioctl.h:2272` |
| 196 | 4 | `txallfrm` | `uint32_t` | every frame transmitted (retransmissions counted too), among them Data, ACK, RTS, CTS, Control Management (comment spans lines 2275-2277). `whd/src/include/whd_wlioctl.h:2275` |
| 200 | 4 | `txrtsfrm` | `uint32_t` | how many RTS the MAC transmitted. `whd/src/include/whd_wlioctl.h:2278` |
| 204 | 4 | `txctsfrm` | `uint32_t` | how many CTS the MAC transmitted. `whd/src/include/whd_wlioctl.h:2279` |
| 208 | 4 | `txackfrm` | `uint32_t` | number of ACK frames sent out. `whd/src/include/whd_wlioctl.h:2280` |
| 212 | 4 | `txdnlfrm` | `uint32_t` | Not used. `whd/src/include/whd_wlioctl.h:2281` |
| 216 | 4 | `txbcnfrm` | `uint32_t` | beacons transmitted. `whd/src/include/whd_wlioctl.h:2282` |
| 220 | 32 | `txfunfl` | `uint32_t[8]` | per-fifo tx underflows; array of 8. `whd/src/include/whd_wlioctl.h:2283` |
| 252 | 4 | `txtplunfl` | `uint32_t` | underflows of the template (ACK/CTS or BCN not transmitted in time by the mac) (comment spans lines 2284-2286). `whd/src/include/whd_wlioctl.h:2284` |
| 256 | 4 | `txphyerror` | `uint32_t` | phy error on transmit; for frames the driver enqueued, tx-status reports which kind of error (comment spans lines 2287-2289). `whd/src/include/whd_wlioctl.h:2287` |
| 260 | 4 | `rxfrmtoolong` | `uint32_t` | frame received whose length exceeds the legal maximum (2346 bytes). `whd/src/include/whd_wlioctl.h:2290` |
| 264 | 4 | `rxfrmtooshrt` | `uint32_t` | frame received that was too short, in bytes, for its type of frame. `whd/src/include/whd_wlioctl.h:2291` |
| 268 | 4 | `rxinvmachdr` | `uint32_t` | protocol version != 0, or else a frame type other than data/control/management (comment spans lines 2292-2294). `whd/src/include/whd_wlioctl.h:2292` |
| 272 | 4 | `rxbadfcs` | `uint32_t` | frames that failed the CRC check done in the MAC. `whd/src/include/whd_wlioctl.h:2295` |
| 276 | 4 | `rxbadplcp` | `uint32_t` | parity check of the PLCP header failed. `whd/src/include/whd_wlioctl.h:2296` |
| 280 | 4 | `rxcrsglitch` | `uint32_t` | the PHY correlated the preamble yet could not correlate the header. `whd/src/include/whd_wlioctl.h:2297` |
| 284 | 4 | `rxstrt` | `uint32_t` | frames received whose PLCP was good (that is, the parity check passed) (comment spans lines 2298-2300). `whd/src/include/whd_wlioctl.h:2298` |
| 288 | 4 | `rxdfrmucastmbss` | `uint32_t` | DATA frames received whose FCS was good and whose RA matched. `whd/src/include/whd_wlioctl.h:2301` |
| 292 | 4 | `rxmfrmucastmbss` | `uint32_t` | mgmt frames received whose FCS was good and whose RA matched. `whd/src/include/whd_wlioctl.h:2302` |
| 296 | 4 | `rxcfrmucast` | `uint32_t` | CNTRL frames received whose FCS was good and whose RA matched. `whd/src/include/whd_wlioctl.h:2303` |
| 300 | 4 | `rxrtsucast` | `uint32_t` | unicast RTS whose destination is the MAC (FCS good). `whd/src/include/whd_wlioctl.h:2304` |
| 304 | 4 | `rxctsucast` | `uint32_t` | unicast CTS whose destination is the MAC (FCS good). `whd/src/include/whd_wlioctl.h:2305` |
| 308 | 4 | `rxackucast` | `uint32_t` | number of ucast ACKS received (good FCS). `whd/src/include/whd_wlioctl.h:2306` |
| 312 | 4 | `rxdfrmocast` | `uint32_t` | DATA frames received (FCS good, RA not matching). `whd/src/include/whd_wlioctl.h:2307` |
| 316 | 4 | `rxmfrmocast` | `uint32_t` | MGMT frames received (FCS good, RA not matching). `whd/src/include/whd_wlioctl.h:2308` |
| 320 | 4 | `rxcfrmocast` | `uint32_t` | CNTRL frames received (FCS good, RA not matching). `whd/src/include/whd_wlioctl.h:2309` |
| 324 | 4 | `rxrtsocast` | `uint32_t` | RTS received whose destination was not the MAC. `whd/src/include/whd_wlioctl.h:2310` |
| 328 | 4 | `rxctsocast` | `uint32_t` | CTS received whose destination was not the MAC. `whd/src/include/whd_wlioctl.h:2311` |
| 332 | 4 | `rxdfrmmcast` | `uint32_t` | multicast RX Data frames the MAC received. `whd/src/include/whd_wlioctl.h:2312` |
| 336 | 4 | `rxmfrmmcast` | `uint32_t` | multicast RX Management frames the MAC received. `whd/src/include/whd_wlioctl.h:2313` |
| 340 | 4 | `rxcfrmmcast` | `uint32_t` | multicast RX Control frames the MAC received (seeing these is unlikely) (comment spans lines 2314-2316). `whd/src/include/whd_wlioctl.h:2314` |
| 344 | 4 | `rxbeaconmbss` | `uint32_t` | beacons received from member of BSS. `whd/src/include/whd_wlioctl.h:2317` |
| 348 | 4 | `rxdfrmucastobss` | `uint32_t` | unicast frames from another BSS whose destination is the MAC (WDS FRAME) (comment spans lines 2318-2320). `whd/src/include/whd_wlioctl.h:2318` |
| 352 | 4 | `rxbeaconobss` | `uint32_t` | beacons received from other BSS. `whd/src/include/whd_wlioctl.h:2321` |
| 356 | 4 | `rxrsptmout` | `uint32_t` | timeouts waiting on a response, for transmitted frames that expected one (comment spans lines 2322-2324). `whd/src/include/whd_wlioctl.h:2322` |
| 360 | 4 | `bcntxcancl` | `uint32_t` | beacon transmissions canceled because a beacon was received (IBSS). `whd/src/include/whd_wlioctl.h:2325` |
| 364 | 4 | `rxf0ovfl` | `uint32_t` | Number of receive fifo 0 overflows. `whd/src/include/whd_wlioctl.h:2326` |
| 368 | 4 | `rxf1ovfl` | `uint32_t` | Number of receive fifo 1 overflows (obsolete). `whd/src/include/whd_wlioctl.h:2327` |
| 372 | 4 | `rxf2ovfl` | `uint32_t` | Number of receive fifo 2 overflows (obsolete). `whd/src/include/whd_wlioctl.h:2328` |
| 376 | 4 | `txsfovfl` | `uint32_t` | Number of transmit status fifo overflows (obsolete). `whd/src/include/whd_wlioctl.h:2329` |
| 380 | 4 | `pmqovfl` | `uint32_t` | Number of PMQ overflows. `whd/src/include/whd_wlioctl.h:2330` |
| 384 | 4 | `rxcgprqfrm` | `uint32_t` | Probe requests received that reached the PRQ fifo (comment spans lines 2331-2333). `whd/src/include/whd_wlioctl.h:2331` |
| 388 | 4 | `rxcgprsqovfl` | `uint32_t` | overflow of the AP's Rx Probe Request Que. `whd/src/include/whd_wlioctl.h:2334` |
| 392 | 4 | `txcgprsfail` | `uint32_t` | Tx Probe Response failure: no ACK came back for a probe response the AP sent (comment spans lines 2335-2337). `whd/src/include/whd_wlioctl.h:2335` |
| 396 | 4 | `txcgprssuc` | `uint32_t` | Tx Probe Response Success (ACK was received). `whd/src/include/whd_wlioctl.h:2338` |
| 400 | 4 | `prs_timeout` | `uint32_t` | probe requests dropped from the PRQ fifo because no probe response could go out inside the time limit that M_PRS_MAXTIME defines (comment spans lines 2339-2342). `whd/src/include/whd_wlioctl.h:2339` |
| 404 | 4 | `rxnack` | `uint32_t` | XXX Number of NACKS received (Afterburner). `whd/src/include/whd_wlioctl.h:2343` |
| 408 | 4 | `frmscons` | `uint32_t` | frames that an Afterburner re-queue caused to complete without being transmitted (marked XXX in the source) (comment spans lines 2344-2346). `whd/src/include/whd_wlioctl.h:2344` |
| 412 | 4 | `txnack` | `uint32_t` | XXX Number of NACKs transmitted (Afterburner). `whd/src/include/whd_wlioctl.h:2347` |
| 416 | 4 | `txglitch_nack` | `uint32_t` | obsolete. `whd/src/include/whd_wlioctl.h:2348` |
| 420 | 4 | `txburst` | `uint32_t` | obsolete. `whd/src/include/whd_wlioctl.h:2349` |
| 424 | 4 | `txfrag` | `uint32_t` | dot11TransmittedFragmentCount. `whd/src/include/whd_wlioctl.h:2352` |
| 428 | 4 | `txmulti` | `uint32_t` | dot11MulticastTransmittedFrameCount. `whd/src/include/whd_wlioctl.h:2353` |
| 432 | 4 | `txfail` | `uint32_t` | dot11FailedCount. `whd/src/include/whd_wlioctl.h:2354` |
| 436 | 4 | `txretry` | `uint32_t` | dot11RetryCount. `whd/src/include/whd_wlioctl.h:2355` |
| 440 | 4 | `txretrie` | `uint32_t` | dot11MultipleRetryCount. `whd/src/include/whd_wlioctl.h:2356` |
| 444 | 4 | `rxdup` | `uint32_t` | dot11FrameduplicateCount. `whd/src/include/whd_wlioctl.h:2357` |
| 448 | 4 | `txrts` | `uint32_t` | dot11RTSSuccessCount. `whd/src/include/whd_wlioctl.h:2358` |
| 452 | 4 | `txnocts` | `uint32_t` | dot11RTSFailureCount. `whd/src/include/whd_wlioctl.h:2359` |
| 456 | 4 | `txnoack` | `uint32_t` | dot11ACKFailureCount. `whd/src/include/whd_wlioctl.h:2360` |
| 460 | 4 | `rxfrag` | `uint32_t` | dot11ReceivedFragmentCount. `whd/src/include/whd_wlioctl.h:2361` |
| 464 | 4 | `rxmulti` | `uint32_t` | dot11MulticastReceivedFrameCount. `whd/src/include/whd_wlioctl.h:2362` |
| 468 | 4 | `rxcrc` | `uint32_t` | dot11FCSErrorCount. `whd/src/include/whd_wlioctl.h:2363` |
| 472 | 4 | `txfrmsnt` | `uint32_t` | dot11TransmittedFrameCount (bogus MIB?). `whd/src/include/whd_wlioctl.h:2364` |
| 476 | 4 | `rxundec` | `uint32_t` | dot11WEPUndecryptableCount. `whd/src/include/whd_wlioctl.h:2365` |
| 480 | 4 | `tkipmicfaill` | `uint32_t` | TKIPLocalMICFailures. `whd/src/include/whd_wlioctl.h:2368` |
| 484 | 4 | `tkipcntrmsr` | `uint32_t` | TKIPCounterMeasuresInvoked. `whd/src/include/whd_wlioctl.h:2369` |
| 488 | 4 | `tkipreplay` | `uint32_t` | TKIPReplays. `whd/src/include/whd_wlioctl.h:2370` |
| 492 | 4 | `ccmpfmterr` | `uint32_t` | CCMPFormatErrors. `whd/src/include/whd_wlioctl.h:2371` |
| 496 | 4 | `ccmpreplay` | `uint32_t` | CCMPReplays. `whd/src/include/whd_wlioctl.h:2372` |
| 500 | 4 | `ccmpundec` | `uint32_t` | CCMPDecryptErrors. `whd/src/include/whd_wlioctl.h:2373` |
| 504 | 4 | `fourwayfail` | `uint32_t` | FourWayHandshakeFailures. `whd/src/include/whd_wlioctl.h:2374` |
| 508 | 4 | `wepundec` | `uint32_t` | dot11WEPUndecryptableCount. `whd/src/include/whd_wlioctl.h:2375` |
| 512 | 4 | `wepicverr` | `uint32_t` | dot11WEPICVErrorCount. `whd/src/include/whd_wlioctl.h:2376` |
| 516 | 4 | `decsuccess` | `uint32_t` | DecryptSuccessCount. `whd/src/include/whd_wlioctl.h:2377` |
| 520 | 4 | `tkipicverr` | `uint32_t` | TKIPICVErrorCount. `whd/src/include/whd_wlioctl.h:2378` |
| 524 | 4 | `wepexcluded` | `uint32_t` | dot11WEPExcludedCount. `whd/src/include/whd_wlioctl.h:2379` |
| 528 | 4 | `rxundec_mcst` | `uint32_t` | dot11WEPUndecryptableCount. `whd/src/include/whd_wlioctl.h:2381` |
| 532 | 4 | `tkipmicfaill_mcst` | `uint32_t` | TKIPLocalMICFailures. `whd/src/include/whd_wlioctl.h:2384` |
| 536 | 4 | `tkipcntrmsr_mcst` | `uint32_t` | TKIPCounterMeasuresInvoked. `whd/src/include/whd_wlioctl.h:2385` |
| 540 | 4 | `tkipreplay_mcst` | `uint32_t` | TKIPReplays. `whd/src/include/whd_wlioctl.h:2386` |
| 544 | 4 | `ccmpfmterr_mcst` | `uint32_t` | CCMPFormatErrors. `whd/src/include/whd_wlioctl.h:2387` |
| 548 | 4 | `ccmpreplay_mcst` | `uint32_t` | CCMPReplays. `whd/src/include/whd_wlioctl.h:2388` |
| 552 | 4 | `ccmpundec_mcst` | `uint32_t` | CCMPDecryptErrors. `whd/src/include/whd_wlioctl.h:2389` |
| 556 | 4 | `fourwayfail_mcst` | `uint32_t` | FourWayHandshakeFailures. `whd/src/include/whd_wlioctl.h:2390` |
| 560 | 4 | `wepundec_mcst` | `uint32_t` | dot11WEPUndecryptableCount. `whd/src/include/whd_wlioctl.h:2391` |
| 564 | 4 | `wepicverr_mcst` | `uint32_t` | dot11WEPICVErrorCount. `whd/src/include/whd_wlioctl.h:2392` |
| 568 | 4 | `decsuccess_mcst` | `uint32_t` | DecryptSuccessCount. `whd/src/include/whd_wlioctl.h:2393` |
| 572 | 4 | `tkipicverr_mcst` | `uint32_t` | TKIPICVErrorCount. `whd/src/include/whd_wlioctl.h:2394` |
| 576 | 4 | `wepexcluded_mcst` | `uint32_t` | dot11WEPExcludedCount. `whd/src/include/whd_wlioctl.h:2395` |
| 580 | 4 | `txchanrej` | `uint32_t` | Tx frames suppressed due to channel rejection. `whd/src/include/whd_wlioctl.h:2397` |
| 584 | 4 | `txexptime` | `uint32_t` | Tx frames suppressed due to timer expiration. `whd/src/include/whd_wlioctl.h:2398` |
| 588 | 4 | `psmwds` | `uint32_t` | Count PSM watchdogs. `whd/src/include/whd_wlioctl.h:2399` |
| 592 | 4 | `phywatchdog` | `uint32_t` | Count Phy watchdogs (triggered by ucode). `whd/src/include/whd_wlioctl.h:2400` |
| 596 | 4 | `prq_entries_handled` | `uint32_t` | PRQ entries read in. `whd/src/include/whd_wlioctl.h:2403` |
| 600 | 4 | `prq_undirected_entries` | `uint32_t` | which were bcast bss & ssid. `whd/src/include/whd_wlioctl.h:2404` |
| 604 | 4 | `prq_bad_entries` | `uint32_t` | which could not be translated to info. `whd/src/include/whd_wlioctl.h:2405` |
| 608 | 4 | `atim_suppress_count` | `uint32_t` | TX suppressions on ATIM fifo. `whd/src/include/whd_wlioctl.h:2406` |
| 612 | 4 | `bcn_template_not_ready` | `uint32_t` | Template marked in use on send bcn . `whd/src/include/whd_wlioctl.h:2407` |
| 616 | 4 | `bcn_template_not_ready_done` | `uint32_t` | ...but "DMA done" interrupt rcvd. `whd/src/include/whd_wlioctl.h:2408` |
| 620 | 4 | `late_tbtt_dpc` | `uint32_t` | TBTT DPC did not happen in time. `whd/src/include/whd_wlioctl.h:2409` |
| 624 | 4 | `rx1mbps` | `uint32_t` | packets rx at 1Mbps. `whd/src/include/whd_wlioctl.h:2412` |
| 628 | 4 | `rx2mbps` | `uint32_t` | packets rx at 2Mbps. `whd/src/include/whd_wlioctl.h:2413` |
| 632 | 4 | `rx5mbps5` | `uint32_t` | packets rx at 5.5Mbps. `whd/src/include/whd_wlioctl.h:2414` |
| 636 | 4 | `rx6mbps` | `uint32_t` | packets rx at 6Mbps. `whd/src/include/whd_wlioctl.h:2415` |
| 640 | 4 | `rx9mbps` | `uint32_t` | packets rx at 9Mbps. `whd/src/include/whd_wlioctl.h:2416` |
| 644 | 4 | `rx11mbps` | `uint32_t` | packets rx at 11Mbps. `whd/src/include/whd_wlioctl.h:2417` |
| 648 | 4 | `rx12mbps` | `uint32_t` | packets rx at 12Mbps. `whd/src/include/whd_wlioctl.h:2418` |
| 652 | 4 | `rx18mbps` | `uint32_t` | packets rx at 18Mbps. `whd/src/include/whd_wlioctl.h:2419` |
| 656 | 4 | `rx24mbps` | `uint32_t` | packets rx at 24Mbps. `whd/src/include/whd_wlioctl.h:2420` |
| 660 | 4 | `rx36mbps` | `uint32_t` | packets rx at 36Mbps. `whd/src/include/whd_wlioctl.h:2421` |
| 664 | 4 | `rx48mbps` | `uint32_t` | packets rx at 48Mbps. `whd/src/include/whd_wlioctl.h:2422` |
| 668 | 4 | `rx54mbps` | `uint32_t` | packets rx at 54Mbps. `whd/src/include/whd_wlioctl.h:2423` |
| 672 | 4 | `rx108mbps` | `uint32_t` | packets rx at 108mbps. `whd/src/include/whd_wlioctl.h:2424` |
| 676 | 4 | `rx162mbps` | `uint32_t` | packets rx at 162mbps. `whd/src/include/whd_wlioctl.h:2425` |
| 680 | 4 | `rx216mbps` | `uint32_t` | packets rx at 216 mbps. `whd/src/include/whd_wlioctl.h:2426` |
| 684 | 4 | `rx270mbps` | `uint32_t` | packets rx at 270 mbps. `whd/src/include/whd_wlioctl.h:2427` |
| 688 | 4 | `rx324mbps` | `uint32_t` | packets rx at 324 mbps. `whd/src/include/whd_wlioctl.h:2428` |
| 692 | 4 | `rx378mbps` | `uint32_t` | packets rx at 378 mbps. `whd/src/include/whd_wlioctl.h:2429` |
| 696 | 4 | `rx432mbps` | `uint32_t` | packets rx at 432 mbps. `whd/src/include/whd_wlioctl.h:2430` |
| 700 | 4 | `rx486mbps` | `uint32_t` | packets rx at 486 mbps. `whd/src/include/whd_wlioctl.h:2431` |
| 704 | 4 | `rx540mbps` | `uint32_t` | packets rx at 540 mbps. `whd/src/include/whd_wlioctl.h:2432` |
| 708 | 4 | `pktengrxducast` | `uint32_t` | unicast frames rxed by the pkteng code. `whd/src/include/whd_wlioctl.h:2435` |
| 712 | 4 | `pktengrxdmcast` | `uint32_t` | multicast frames rxed by the pkteng code. `whd/src/include/whd_wlioctl.h:2436` |
| 716 | 4 | `rfdisable` | `uint32_t` | count of radio disables. `whd/src/include/whd_wlioctl.h:2438` |
| 720 | 4 | `bphy_rxcrsglitch` | `uint32_t` | PHY count of bphy glitches. `whd/src/include/whd_wlioctl.h:2439` |
| 724 | 4 | `txmpdu_sgi` | `uint32_t` | count for sgi transmit. `whd/src/include/whd_wlioctl.h:2441` |
| 728 | 4 | `rxmpdu_sgi` | `uint32_t` | count for sgi received. `whd/src/include/whd_wlioctl.h:2442` |
| 732 | 4 | `txmpdu_stbc` | `uint32_t` | count for stbc transmit. `whd/src/include/whd_wlioctl.h:2443` |
| 736 | 4 | `rxmpdu_stbc` | `uint32_t` | count for stbc received. `whd/src/include/whd_wlioctl.h:2444` |

Size check: compiled

Differences: the type name is not found in linux, embassy, c-driver or pico-sdk; the only other "counters" name in these sources is a linux debugfs entry, unrelated to this variable. `linux/brcmfmac/sdio.c:3230`

### `wl_cnt_ver_seven_t` (whd)
Counters report, version-7 layout by typedef name, with no command, named variable or event tied to it: the header defines the variable name "counters" (`IOVAR_STR_COUNTERS`), but no `.c` or `.rs` file of whd, embassy, c-driver or pico-sdk refers to that name or to this type; not packed (`BWL_DEFAULT_PACKING` is defined empty and the header's first `#pragma pack` is at line 3864, after the definition; alignment 4); 744 bytes (compiled on an x86-64 host; the 32-bit ARM layout is inferred from member types, all 1-, 2- or 4-byte integers); endianness not stated in the definition; the field notes are the header's own comments, whd's names for the counters. `whd/src/include/whd_wlioctl.h:2447-2678` `whd/src/include/whd_wlioctl.h:1091` `whd/src/include/whd_wlioctl.h:467` `whd/src/include/whd_wlioctl.h:3864`

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 2 | `version` | `uint16_t` | see definition of WL_CNT_T_VERSION. `whd/src/include/whd_wlioctl.h:2449` |
| 2 | 2 | `length` | `uint16_t` | length of entire structure. `whd/src/include/whd_wlioctl.h:2450` |
| 4 | 4 | `txframe` | `uint32_t` | tx data frames. `whd/src/include/whd_wlioctl.h:2453` |
| 8 | 4 | `txbyte` | `uint32_t` | tx data bytes. `whd/src/include/whd_wlioctl.h:2454` |
| 12 | 4 | `txretrans` | `uint32_t` | tx mac retransmits. `whd/src/include/whd_wlioctl.h:2455` |
| 16 | 4 | `txerror` | `uint32_t` | tx data errors (derived: sum of others). `whd/src/include/whd_wlioctl.h:2456` |
| 20 | 4 | `txctl` | `uint32_t` | tx management frames. `whd/src/include/whd_wlioctl.h:2457` |
| 24 | 4 | `txprshort` | `uint32_t` | tx short preamble frames. `whd/src/include/whd_wlioctl.h:2458` |
| 28 | 4 | `txserr` | `uint32_t` | tx status errors. `whd/src/include/whd_wlioctl.h:2459` |
| 32 | 4 | `txnobuf` | `uint32_t` | tx out of buffers errors. `whd/src/include/whd_wlioctl.h:2460` |
| 36 | 4 | `txnoassoc` | `uint32_t` | tx discard because we're not associated. `whd/src/include/whd_wlioctl.h:2461` |
| 40 | 4 | `txrunt` | `uint32_t` | tx runt frames. `whd/src/include/whd_wlioctl.h:2462` |
| 44 | 4 | `txchit` | `uint32_t` | tx header cache hit (fastpath). `whd/src/include/whd_wlioctl.h:2463` |
| 48 | 4 | `txcmiss` | `uint32_t` | tx header cache miss (slowpath). `whd/src/include/whd_wlioctl.h:2464` |
| 52 | 4 | `txuflo` | `uint32_t` | tx fifo underflows. `whd/src/include/whd_wlioctl.h:2467` |
| 56 | 4 | `txphyerr` | `uint32_t` | tx phy errors (indicated in tx status). `whd/src/include/whd_wlioctl.h:2468` |
| 60 | 4 | `txphycrs` | `uint32_t` | PR8861/8963 counter. `whd/src/include/whd_wlioctl.h:2469` |
| 64 | 4 | `rxframe` | `uint32_t` | rx data frames. `whd/src/include/whd_wlioctl.h:2472` |
| 68 | 4 | `rxbyte` | `uint32_t` | rx data bytes. `whd/src/include/whd_wlioctl.h:2473` |
| 72 | 4 | `rxerror` | `uint32_t` | rx data errors (derived: sum of others). `whd/src/include/whd_wlioctl.h:2474` |
| 76 | 4 | `rxctl` | `uint32_t` | rx management frames. `whd/src/include/whd_wlioctl.h:2475` |
| 80 | 4 | `rxnobuf` | `uint32_t` | rx out of buffers errors. `whd/src/include/whd_wlioctl.h:2476` |
| 84 | 4 | `rxnondata` | `uint32_t` | error count for non-data frames received on the data channel. `whd/src/include/whd_wlioctl.h:2477` |
| 88 | 4 | `rxbadds` | `uint32_t` | rx bad DS errors. `whd/src/include/whd_wlioctl.h:2478` |
| 92 | 4 | `rxbadcm` | `uint32_t` | rx bad control or management frames. `whd/src/include/whd_wlioctl.h:2479` |
| 96 | 4 | `rxfragerr` | `uint32_t` | rx fragmentation errors. `whd/src/include/whd_wlioctl.h:2480` |
| 100 | 4 | `rxrunt` | `uint32_t` | rx runt frames. `whd/src/include/whd_wlioctl.h:2481` |
| 104 | 4 | `rxgiant` | `uint32_t` | rx giant frames. `whd/src/include/whd_wlioctl.h:2482` |
| 108 | 4 | `rxnoscb` | `uint32_t` | rx no scb error. `whd/src/include/whd_wlioctl.h:2483` |
| 112 | 4 | `rxbadproto` | `uint32_t` | rx invalid frames. `whd/src/include/whd_wlioctl.h:2484` |
| 116 | 4 | `rxbadsrcmac` | `uint32_t` | rx frames with Invalid Src Mac. `whd/src/include/whd_wlioctl.h:2485` |
| 120 | 4 | `rxbadda` | `uint32_t` | rx frames tossed for invalid da. `whd/src/include/whd_wlioctl.h:2486` |
| 124 | 4 | `rxfilter` | `uint32_t` | rx frames filtered out. `whd/src/include/whd_wlioctl.h:2487` |
| 128 | 4 | `rxoflo` | `uint32_t` | rx fifo overflow errors. `whd/src/include/whd_wlioctl.h:2490` |
| 132 | 24 | `rxuflo` | `uint32_t[NFIFO]` | rx dma descriptor underflow errors; array of NFIFO = 6 `whd/src/include/whd_wlioctl.h:1983`. `whd/src/include/whd_wlioctl.h:2491` |
| 156 | 4 | `d11cnt_txrts_off` | `uint32_t` | d11cnt txrts value when reset d11cnt. `whd/src/include/whd_wlioctl.h:2493` |
| 160 | 4 | `d11cnt_rxcrc_off` | `uint32_t` | d11cnt rxcrc value when reset d11cnt. `whd/src/include/whd_wlioctl.h:2494` |
| 164 | 4 | `d11cnt_txnocts_off` | `uint32_t` | d11cnt txnocts value when reset d11cnt. `whd/src/include/whd_wlioctl.h:2495` |
| 168 | 4 | `dmade` | `uint32_t` | tx/rx dma descriptor errors. `whd/src/include/whd_wlioctl.h:2498` |
| 172 | 4 | `dmada` | `uint32_t` | tx/rx dma data errors. `whd/src/include/whd_wlioctl.h:2499` |
| 176 | 4 | `dmape` | `uint32_t` | tx/rx dma descriptor protocol errors. `whd/src/include/whd_wlioctl.h:2500` |
| 180 | 4 | `reset` | `uint32_t` | reset count. `whd/src/include/whd_wlioctl.h:2501` |
| 184 | 4 | `tbtt` | `uint32_t` | cnts the TBTT int's. `whd/src/include/whd_wlioctl.h:2502` |
| 188 | 4 | `txdmawar` | `uint32_t` | # occurrences of PR15420 workaround. `whd/src/include/whd_wlioctl.h:2503` |
| 192 | 4 | `pkt_callback_reg_fail` | `uint32_t` | callbacks register failure. `whd/src/include/whd_wlioctl.h:2504` |
| 196 | 4 | `txallfrm` | `uint32_t` | every frame transmitted (retransmissions counted too), among them Data, ACK, RTS, CTS, Control Management (comment spans lines 2507-2509). `whd/src/include/whd_wlioctl.h:2507` |
| 200 | 4 | `txrtsfrm` | `uint32_t` | how many RTS the MAC transmitted. `whd/src/include/whd_wlioctl.h:2510` |
| 204 | 4 | `txctsfrm` | `uint32_t` | how many CTS the MAC transmitted. `whd/src/include/whd_wlioctl.h:2511` |
| 208 | 4 | `txackfrm` | `uint32_t` | number of ACK frames sent out. `whd/src/include/whd_wlioctl.h:2512` |
| 212 | 4 | `txdnlfrm` | `uint32_t` | Not used. `whd/src/include/whd_wlioctl.h:2513` |
| 216 | 4 | `txbcnfrm` | `uint32_t` | beacons transmitted. `whd/src/include/whd_wlioctl.h:2514` |
| 220 | 32 | `txfunfl` | `uint32_t[8]` | per-fifo tx underflows; array of 8. `whd/src/include/whd_wlioctl.h:2515` |
| 252 | 4 | `txtplunfl` | `uint32_t` | underflows of the template (ACK/CTS or BCN not transmitted in time by the mac) (comment spans lines 2516-2518). `whd/src/include/whd_wlioctl.h:2516` |
| 256 | 4 | `txphyerror` | `uint32_t` | phy error on transmit; for frames the driver enqueued, tx-status reports which kind of error (comment spans lines 2519-2521). `whd/src/include/whd_wlioctl.h:2519` |
| 260 | 4 | `rxfrmtoolong` | `uint32_t` | frame received whose length exceeds the legal maximum (2346 bytes). `whd/src/include/whd_wlioctl.h:2522` |
| 264 | 4 | `rxfrmtooshrt` | `uint32_t` | frame received that was too short, in bytes, for its type of frame. `whd/src/include/whd_wlioctl.h:2523` |
| 268 | 4 | `rxinvmachdr` | `uint32_t` | protocol version != 0, or else a frame type other than data/control/management (comment spans lines 2524-2526). `whd/src/include/whd_wlioctl.h:2524` |
| 272 | 4 | `rxbadfcs` | `uint32_t` | frames that failed the CRC check done in the MAC. `whd/src/include/whd_wlioctl.h:2527` |
| 276 | 4 | `rxbadplcp` | `uint32_t` | parity check of the PLCP header failed. `whd/src/include/whd_wlioctl.h:2528` |
| 280 | 4 | `rxcrsglitch` | `uint32_t` | the PHY correlated the preamble yet could not correlate the header. `whd/src/include/whd_wlioctl.h:2529` |
| 284 | 4 | `rxstrt` | `uint32_t` | frames received whose PLCP was good (that is, the parity check passed) (comment spans lines 2530-2532). `whd/src/include/whd_wlioctl.h:2530` |
| 288 | 4 | `rxdfrmucastmbss` | `uint32_t` | DATA frames received whose FCS was good and whose RA matched. `whd/src/include/whd_wlioctl.h:2533` |
| 292 | 4 | `rxmfrmucastmbss` | `uint32_t` | mgmt frames received whose FCS was good and whose RA matched. `whd/src/include/whd_wlioctl.h:2534` |
| 296 | 4 | `rxcfrmucast` | `uint32_t` | CNTRL frames received whose FCS was good and whose RA matched. `whd/src/include/whd_wlioctl.h:2535` |
| 300 | 4 | `rxrtsucast` | `uint32_t` | unicast RTS whose destination is the MAC (FCS good). `whd/src/include/whd_wlioctl.h:2536` |
| 304 | 4 | `rxctsucast` | `uint32_t` | unicast CTS whose destination is the MAC (FCS good). `whd/src/include/whd_wlioctl.h:2537` |
| 308 | 4 | `rxackucast` | `uint32_t` | number of ucast ACKS received (good FCS). `whd/src/include/whd_wlioctl.h:2538` |
| 312 | 4 | `rxdfrmocast` | `uint32_t` | DATA frames received (FCS good, RA not matching). `whd/src/include/whd_wlioctl.h:2539` |
| 316 | 4 | `rxmfrmocast` | `uint32_t` | MGMT frames received (FCS good, RA not matching). `whd/src/include/whd_wlioctl.h:2540` |
| 320 | 4 | `rxcfrmocast` | `uint32_t` | CNTRL frames received (FCS good, RA not matching). `whd/src/include/whd_wlioctl.h:2541` |
| 324 | 4 | `rxrtsocast` | `uint32_t` | RTS received whose destination was not the MAC. `whd/src/include/whd_wlioctl.h:2542` |
| 328 | 4 | `rxctsocast` | `uint32_t` | CTS received whose destination was not the MAC. `whd/src/include/whd_wlioctl.h:2543` |
| 332 | 4 | `rxdfrmmcast` | `uint32_t` | multicast RX Data frames the MAC received. `whd/src/include/whd_wlioctl.h:2544` |
| 336 | 4 | `rxmfrmmcast` | `uint32_t` | multicast RX Management frames the MAC received. `whd/src/include/whd_wlioctl.h:2545` |
| 340 | 4 | `rxcfrmmcast` | `uint32_t` | multicast RX Control frames the MAC received (seeing these is unlikely) (comment spans lines 2546-2548). `whd/src/include/whd_wlioctl.h:2546` |
| 344 | 4 | `rxbeaconmbss` | `uint32_t` | beacons received from member of BSS. `whd/src/include/whd_wlioctl.h:2549` |
| 348 | 4 | `rxdfrmucastobss` | `uint32_t` | unicast frames from another BSS whose destination is the MAC (WDS FRAME) (comment spans lines 2550-2552). `whd/src/include/whd_wlioctl.h:2550` |
| 352 | 4 | `rxbeaconobss` | `uint32_t` | beacons received from other BSS. `whd/src/include/whd_wlioctl.h:2553` |
| 356 | 4 | `rxrsptmout` | `uint32_t` | timeouts waiting on a response, for transmitted frames that expected one (comment spans lines 2554-2556). `whd/src/include/whd_wlioctl.h:2554` |
| 360 | 4 | `bcntxcancl` | `uint32_t` | beacon transmissions canceled because a beacon was received (IBSS). `whd/src/include/whd_wlioctl.h:2557` |
| 364 | 4 | `rxf0ovfl` | `uint32_t` | Number of receive fifo 0 overflows. `whd/src/include/whd_wlioctl.h:2558` |
| 368 | 4 | `rxf1ovfl` | `uint32_t` | Number of receive fifo 1 overflows (obsolete). `whd/src/include/whd_wlioctl.h:2559` |
| 372 | 4 | `rxf2ovfl` | `uint32_t` | Number of receive fifo 2 overflows (obsolete). `whd/src/include/whd_wlioctl.h:2560` |
| 376 | 4 | `txsfovfl` | `uint32_t` | Number of transmit status fifo overflows (obsolete). `whd/src/include/whd_wlioctl.h:2561` |
| 380 | 4 | `pmqovfl` | `uint32_t` | Number of PMQ overflows. `whd/src/include/whd_wlioctl.h:2562` |
| 384 | 4 | `rxcgprqfrm` | `uint32_t` | Probe requests received that reached the PRQ fifo (comment spans lines 2563-2565). `whd/src/include/whd_wlioctl.h:2563` |
| 388 | 4 | `rxcgprsqovfl` | `uint32_t` | overflow of the AP's Rx Probe Request Que. `whd/src/include/whd_wlioctl.h:2566` |
| 392 | 4 | `txcgprsfail` | `uint32_t` | Tx Probe Response failure: no ACK came back for a probe response the AP sent (comment spans lines 2567-2569). `whd/src/include/whd_wlioctl.h:2567` |
| 396 | 4 | `txcgprssuc` | `uint32_t` | Tx Probe Response Success (ACK was received). `whd/src/include/whd_wlioctl.h:2570` |
| 400 | 4 | `prs_timeout` | `uint32_t` | probe requests dropped from the PRQ fifo because no probe response could go out inside the time limit that M_PRS_MAXTIME defines (comment spans lines 2571-2574). `whd/src/include/whd_wlioctl.h:2571` |
| 404 | 4 | `rxnack` | `uint32_t` | obsolete. `whd/src/include/whd_wlioctl.h:2575` |
| 408 | 4 | `frmscons` | `uint32_t` | obsolete. `whd/src/include/whd_wlioctl.h:2576` |
| 412 | 4 | `txnack` | `uint32_t` | obsolete. `whd/src/include/whd_wlioctl.h:2577` |
| 416 | 4 | `txglitch_nack` | `uint32_t` | obsolete. `whd/src/include/whd_wlioctl.h:2578` |
| 420 | 4 | `txburst` | `uint32_t` | obsolete. `whd/src/include/whd_wlioctl.h:2579` |
| 424 | 4 | `txfrag` | `uint32_t` | dot11TransmittedFragmentCount. `whd/src/include/whd_wlioctl.h:2582` |
| 428 | 4 | `txmulti` | `uint32_t` | dot11MulticastTransmittedFrameCount. `whd/src/include/whd_wlioctl.h:2583` |
| 432 | 4 | `txfail` | `uint32_t` | dot11FailedCount. `whd/src/include/whd_wlioctl.h:2584` |
| 436 | 4 | `txretry` | `uint32_t` | dot11RetryCount. `whd/src/include/whd_wlioctl.h:2585` |
| 440 | 4 | `txretrie` | `uint32_t` | dot11MultipleRetryCount. `whd/src/include/whd_wlioctl.h:2586` |
| 444 | 4 | `rxdup` | `uint32_t` | dot11FrameduplicateCount. `whd/src/include/whd_wlioctl.h:2587` |
| 448 | 4 | `txrts` | `uint32_t` | dot11RTSSuccessCount. `whd/src/include/whd_wlioctl.h:2588` |
| 452 | 4 | `txnocts` | `uint32_t` | dot11RTSFailureCount. `whd/src/include/whd_wlioctl.h:2589` |
| 456 | 4 | `txnoack` | `uint32_t` | dot11ACKFailureCount. `whd/src/include/whd_wlioctl.h:2590` |
| 460 | 4 | `rxfrag` | `uint32_t` | dot11ReceivedFragmentCount. `whd/src/include/whd_wlioctl.h:2591` |
| 464 | 4 | `rxmulti` | `uint32_t` | dot11MulticastReceivedFrameCount. `whd/src/include/whd_wlioctl.h:2592` |
| 468 | 4 | `rxcrc` | `uint32_t` | dot11FCSErrorCount. `whd/src/include/whd_wlioctl.h:2593` |
| 472 | 4 | `txfrmsnt` | `uint32_t` | dot11TransmittedFrameCount (bogus MIB?). `whd/src/include/whd_wlioctl.h:2594` |
| 476 | 4 | `rxundec` | `uint32_t` | dot11WEPUndecryptableCount. `whd/src/include/whd_wlioctl.h:2595` |
| 480 | 4 | `tkipmicfaill` | `uint32_t` | TKIPLocalMICFailures. `whd/src/include/whd_wlioctl.h:2598` |
| 484 | 4 | `tkipcntrmsr` | `uint32_t` | TKIPCounterMeasuresInvoked. `whd/src/include/whd_wlioctl.h:2599` |
| 488 | 4 | `tkipreplay` | `uint32_t` | TKIPReplays. `whd/src/include/whd_wlioctl.h:2600` |
| 492 | 4 | `ccmpfmterr` | `uint32_t` | CCMPFormatErrors. `whd/src/include/whd_wlioctl.h:2601` |
| 496 | 4 | `ccmpreplay` | `uint32_t` | CCMPReplays. `whd/src/include/whd_wlioctl.h:2602` |
| 500 | 4 | `ccmpundec` | `uint32_t` | CCMPDecryptErrors. `whd/src/include/whd_wlioctl.h:2603` |
| 504 | 4 | `fourwayfail` | `uint32_t` | FourWayHandshakeFailures. `whd/src/include/whd_wlioctl.h:2604` |
| 508 | 4 | `wepundec` | `uint32_t` | dot11WEPUndecryptableCount. `whd/src/include/whd_wlioctl.h:2605` |
| 512 | 4 | `wepicverr` | `uint32_t` | dot11WEPICVErrorCount. `whd/src/include/whd_wlioctl.h:2606` |
| 516 | 4 | `decsuccess` | `uint32_t` | DecryptSuccessCount. `whd/src/include/whd_wlioctl.h:2607` |
| 520 | 4 | `tkipicverr` | `uint32_t` | TKIPICVErrorCount. `whd/src/include/whd_wlioctl.h:2608` |
| 524 | 4 | `wepexcluded` | `uint32_t` | dot11WEPExcludedCount. `whd/src/include/whd_wlioctl.h:2609` |
| 528 | 4 | `txchanrej` | `uint32_t` | Tx frames suppressed due to channel rejection. `whd/src/include/whd_wlioctl.h:2611` |
| 532 | 4 | `psmwds` | `uint32_t` | Count PSM watchdogs. `whd/src/include/whd_wlioctl.h:2612` |
| 536 | 4 | `phywatchdog` | `uint32_t` | Count Phy watchdogs (triggered by ucode). `whd/src/include/whd_wlioctl.h:2613` |
| 540 | 4 | `prq_entries_handled` | `uint32_t` | PRQ entries read in. `whd/src/include/whd_wlioctl.h:2616` |
| 544 | 4 | `prq_undirected_entries` | `uint32_t` | which were bcast bss & ssid. `whd/src/include/whd_wlioctl.h:2617` |
| 548 | 4 | `prq_bad_entries` | `uint32_t` | which could not be translated to info. `whd/src/include/whd_wlioctl.h:2618` |
| 552 | 4 | `atim_suppress_count` | `uint32_t` | TX suppressions on ATIM fifo. `whd/src/include/whd_wlioctl.h:2619` |
| 556 | 4 | `bcn_template_not_ready` | `uint32_t` | Template marked in use on send bcn . `whd/src/include/whd_wlioctl.h:2620` |
| 560 | 4 | `bcn_template_not_ready_done` | `uint32_t` | ...but "DMA done" interrupt rcvd. `whd/src/include/whd_wlioctl.h:2621` |
| 564 | 4 | `late_tbtt_dpc` | `uint32_t` | TBTT DPC did not happen in time. `whd/src/include/whd_wlioctl.h:2622` |
| 568 | 4 | `rx1mbps` | `uint32_t` | packets rx at 1Mbps. `whd/src/include/whd_wlioctl.h:2625` |
| 572 | 4 | `rx2mbps` | `uint32_t` | packets rx at 2Mbps. `whd/src/include/whd_wlioctl.h:2626` |
| 576 | 4 | `rx5mbps5` | `uint32_t` | packets rx at 5.5Mbps. `whd/src/include/whd_wlioctl.h:2627` |
| 580 | 4 | `rx6mbps` | `uint32_t` | packets rx at 6Mbps. `whd/src/include/whd_wlioctl.h:2628` |
| 584 | 4 | `rx9mbps` | `uint32_t` | packets rx at 9Mbps. `whd/src/include/whd_wlioctl.h:2629` |
| 588 | 4 | `rx11mbps` | `uint32_t` | packets rx at 11Mbps. `whd/src/include/whd_wlioctl.h:2630` |
| 592 | 4 | `rx12mbps` | `uint32_t` | packets rx at 12Mbps. `whd/src/include/whd_wlioctl.h:2631` |
| 596 | 4 | `rx18mbps` | `uint32_t` | packets rx at 18Mbps. `whd/src/include/whd_wlioctl.h:2632` |
| 600 | 4 | `rx24mbps` | `uint32_t` | packets rx at 24Mbps. `whd/src/include/whd_wlioctl.h:2633` |
| 604 | 4 | `rx36mbps` | `uint32_t` | packets rx at 36Mbps. `whd/src/include/whd_wlioctl.h:2634` |
| 608 | 4 | `rx48mbps` | `uint32_t` | packets rx at 48Mbps. `whd/src/include/whd_wlioctl.h:2635` |
| 612 | 4 | `rx54mbps` | `uint32_t` | packets rx at 54Mbps. `whd/src/include/whd_wlioctl.h:2636` |
| 616 | 4 | `rx108mbps` | `uint32_t` | packets rx at 108mbps. `whd/src/include/whd_wlioctl.h:2637` |
| 620 | 4 | `rx162mbps` | `uint32_t` | packets rx at 162mbps. `whd/src/include/whd_wlioctl.h:2638` |
| 624 | 4 | `rx216mbps` | `uint32_t` | packets rx at 216 mbps. `whd/src/include/whd_wlioctl.h:2639` |
| 628 | 4 | `rx270mbps` | `uint32_t` | packets rx at 270 mbps. `whd/src/include/whd_wlioctl.h:2640` |
| 632 | 4 | `rx324mbps` | `uint32_t` | packets rx at 324 mbps. `whd/src/include/whd_wlioctl.h:2641` |
| 636 | 4 | `rx378mbps` | `uint32_t` | packets rx at 378 mbps. `whd/src/include/whd_wlioctl.h:2642` |
| 640 | 4 | `rx432mbps` | `uint32_t` | packets rx at 432 mbps. `whd/src/include/whd_wlioctl.h:2643` |
| 644 | 4 | `rx486mbps` | `uint32_t` | packets rx at 486 mbps. `whd/src/include/whd_wlioctl.h:2644` |
| 648 | 4 | `rx540mbps` | `uint32_t` | packets rx at 540 mbps. `whd/src/include/whd_wlioctl.h:2645` |
| 652 | 4 | `pktengrxducast` | `uint32_t` | unicast frames rxed by the pkteng code. `whd/src/include/whd_wlioctl.h:2648` |
| 656 | 4 | `pktengrxdmcast` | `uint32_t` | multicast frames rxed by the pkteng code. `whd/src/include/whd_wlioctl.h:2649` |
| 660 | 4 | `rfdisable` | `uint32_t` | count of radio disables. `whd/src/include/whd_wlioctl.h:2651` |
| 664 | 4 | `bphy_rxcrsglitch` | `uint32_t` | PHY count of bphy glitches. `whd/src/include/whd_wlioctl.h:2652` |
| 668 | 4 | `txexptime` | `uint32_t` | Tx frames suppressed due to timer expiration. `whd/src/include/whd_wlioctl.h:2654` |
| 672 | 4 | `txmpdu_sgi` | `uint32_t` | count for sgi transmit. `whd/src/include/whd_wlioctl.h:2656` |
| 676 | 4 | `rxmpdu_sgi` | `uint32_t` | count for sgi received. `whd/src/include/whd_wlioctl.h:2657` |
| 680 | 4 | `txmpdu_stbc` | `uint32_t` | count for stbc transmit. `whd/src/include/whd_wlioctl.h:2658` |
| 684 | 4 | `rxmpdu_stbc` | `uint32_t` | count for stbc received. `whd/src/include/whd_wlioctl.h:2659` |
| 688 | 4 | `rxundec_mcst` | `uint32_t` | dot11WEPUndecryptableCount. `whd/src/include/whd_wlioctl.h:2661` |
| 692 | 4 | `tkipmicfaill_mcst` | `uint32_t` | TKIPLocalMICFailures. `whd/src/include/whd_wlioctl.h:2664` |
| 696 | 4 | `tkipcntrmsr_mcst` | `uint32_t` | TKIPCounterMeasuresInvoked. `whd/src/include/whd_wlioctl.h:2665` |
| 700 | 4 | `tkipreplay_mcst` | `uint32_t` | TKIPReplays. `whd/src/include/whd_wlioctl.h:2666` |
| 704 | 4 | `ccmpfmterr_mcst` | `uint32_t` | CCMPFormatErrors. `whd/src/include/whd_wlioctl.h:2667` |
| 708 | 4 | `ccmpreplay_mcst` | `uint32_t` | CCMPReplays. `whd/src/include/whd_wlioctl.h:2668` |
| 712 | 4 | `ccmpundec_mcst` | `uint32_t` | CCMPDecryptErrors. `whd/src/include/whd_wlioctl.h:2669` |
| 716 | 4 | `fourwayfail_mcst` | `uint32_t` | FourWayHandshakeFailures. `whd/src/include/whd_wlioctl.h:2670` |
| 720 | 4 | `wepundec_mcst` | `uint32_t` | dot11WEPUndecryptableCount. `whd/src/include/whd_wlioctl.h:2671` |
| 724 | 4 | `wepicverr_mcst` | `uint32_t` | dot11WEPICVErrorCount. `whd/src/include/whd_wlioctl.h:2672` |
| 728 | 4 | `decsuccess_mcst` | `uint32_t` | DecryptSuccessCount. `whd/src/include/whd_wlioctl.h:2673` |
| 732 | 4 | `tkipicverr_mcst` | `uint32_t` | TKIPICVErrorCount. `whd/src/include/whd_wlioctl.h:2674` |
| 736 | 4 | `wepexcluded_mcst` | `uint32_t` | dot11WEPExcludedCount. `whd/src/include/whd_wlioctl.h:2675` |
| 740 | 4 | `dma_hang` | `uint32_t` | source comment reads 'count for stbc received', which looks like a copy-paste slip (inferred): the same-named field in wl_cnt_ver_eight_t is commented 'count for dma hang' `whd/src/include/whd_wlioctl.h:2913`. `whd/src/include/whd_wlioctl.h:2677` |

Size check: compiled

Differences: the type name is not found in linux, embassy, c-driver or pico-sdk; the only other "counters" name in these sources is a linux debugfs entry, unrelated to this variable. `linux/brcmfmac/sdio.c:3230`

### `wl_cnt_ver_eight_t` (whd)
Counters report, version-8 layout by typedef name, with no command, named variable or event tied to it: the header defines the variable name "counters" (`IOVAR_STR_COUNTERS`), but no `.c` or `.rs` file of whd, embassy, c-driver or pico-sdk refers to that name or to this type; not packed (`BWL_DEFAULT_PACKING` is defined empty and the header's first `#pragma pack` is at line 3864, after the definition; alignment 4); 804 bytes; byte order not stated in the definition, little-endian as whd treats it (inferred: plain uintN_t types, and whd's htod16/htod32/dtoh16/dtoh32 are identity unless IL_BIGENDIAN is defined); the field notes are the header's own comments. `whd/src/include/whd_wlioctl.h:2680-2932` `whd/src/include/whd_wlioctl.h:1091` `whd/src/include/whd_wlioctl.h:467` `whd/src/include/whd_wlioctl.h:3864` `whd/src/include/whd_endian.h:44-57`

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 2 | `version` | `uint16_t` | see definition of WL_CNT_T_VERSION, which the header defines as 6. `whd/src/include/whd_wlioctl.h:2682` `whd/src/include/whd_wlioctl.h:1984` |
| 2 | 2 | `length` | `uint16_t` | length of entire structure. `whd/src/include/whd_wlioctl.h:2683` |
| 4 | 4 | `txframe` | `uint32_t` | tx data frames. `whd/src/include/whd_wlioctl.h:2686` |
| 8 | 4 | `txbyte` | `uint32_t` | tx data bytes. `whd/src/include/whd_wlioctl.h:2687` |
| 12 | 4 | `txretrans` | `uint32_t` | tx mac retransmits. `whd/src/include/whd_wlioctl.h:2688` |
| 16 | 4 | `txerror` | `uint32_t` | tx data errors (derived: sum of others). `whd/src/include/whd_wlioctl.h:2689` |
| 20 | 4 | `txctl` | `uint32_t` | tx management frames. `whd/src/include/whd_wlioctl.h:2690` |
| 24 | 4 | `txprshort` | `uint32_t` | tx short preamble frames. `whd/src/include/whd_wlioctl.h:2691` |
| 28 | 4 | `txserr` | `uint32_t` | tx status errors. `whd/src/include/whd_wlioctl.h:2692` |
| 32 | 4 | `txnobuf` | `uint32_t` | tx out of buffers errors. `whd/src/include/whd_wlioctl.h:2693` |
| 36 | 4 | `txnoassoc` | `uint32_t` | tx discard because we're not associated. `whd/src/include/whd_wlioctl.h:2694` |
| 40 | 4 | `txrunt` | `uint32_t` | tx runt frames. `whd/src/include/whd_wlioctl.h:2695` |
| 44 | 4 | `txchit` | `uint32_t` | tx header cache hit (fastpath). `whd/src/include/whd_wlioctl.h:2696` |
| 48 | 4 | `txcmiss` | `uint32_t` | tx header cache miss (slowpath). `whd/src/include/whd_wlioctl.h:2697` |
| 52 | 4 | `txuflo` | `uint32_t` | tx fifo underflows. `whd/src/include/whd_wlioctl.h:2700` |
| 56 | 4 | `txphyerr` | `uint32_t` | tx phy errors (indicated in tx status). `whd/src/include/whd_wlioctl.h:2701` |
| 60 | 4 | `txphycrs` | `uint32_t` | PR8861/8963 counter. `whd/src/include/whd_wlioctl.h:2702` |
| 64 | 4 | `rxframe` | `uint32_t` | rx data frames. `whd/src/include/whd_wlioctl.h:2705` |
| 68 | 4 | `rxbyte` | `uint32_t` | rx data bytes. `whd/src/include/whd_wlioctl.h:2706` |
| 72 | 4 | `rxerror` | `uint32_t` | rx data errors (derived: sum of others). `whd/src/include/whd_wlioctl.h:2707` |
| 76 | 4 | `rxctl` | `uint32_t` | rx management frames. `whd/src/include/whd_wlioctl.h:2708` |
| 80 | 4 | `rxnobuf` | `uint32_t` | rx out of buffers errors. `whd/src/include/whd_wlioctl.h:2709` |
| 84 | 4 | `rxnondata` | `uint32_t` | error count for non-data frames received on the data channel. `whd/src/include/whd_wlioctl.h:2710` |
| 88 | 4 | `rxbadds` | `uint32_t` | rx bad DS errors. `whd/src/include/whd_wlioctl.h:2711` |
| 92 | 4 | `rxbadcm` | `uint32_t` | rx bad control or management frames. `whd/src/include/whd_wlioctl.h:2712` |
| 96 | 4 | `rxfragerr` | `uint32_t` | rx fragmentation errors. `whd/src/include/whd_wlioctl.h:2713` |
| 100 | 4 | `rxrunt` | `uint32_t` | rx runt frames. `whd/src/include/whd_wlioctl.h:2714` |
| 104 | 4 | `rxgiant` | `uint32_t` | rx giant frames. `whd/src/include/whd_wlioctl.h:2715` |
| 108 | 4 | `rxnoscb` | `uint32_t` | rx no scb error. `whd/src/include/whd_wlioctl.h:2716` |
| 112 | 4 | `rxbadproto` | `uint32_t` | rx invalid frames. `whd/src/include/whd_wlioctl.h:2717` |
| 116 | 4 | `rxbadsrcmac` | `uint32_t` | rx frames with Invalid Src Mac. `whd/src/include/whd_wlioctl.h:2718` |
| 120 | 4 | `rxbadda` | `uint32_t` | rx frames tossed for invalid da. `whd/src/include/whd_wlioctl.h:2719` |
| 124 | 4 | `rxfilter` | `uint32_t` | rx frames filtered out. `whd/src/include/whd_wlioctl.h:2720` |
| 128 | 4 | `rxoflo` | `uint32_t` | rx fifo overflow errors. `whd/src/include/whd_wlioctl.h:2723` |
| 132 | 24 | `rxuflo` | `uint32_t[NFIFO]` | rx dma descriptor underflow errors; array of NFIFO = 6 `whd/src/include/whd_wlioctl.h:1983`. `whd/src/include/whd_wlioctl.h:2724` |
| 156 | 4 | `d11cnt_txrts_off` | `uint32_t` | d11cnt txrts value when reset d11cnt. `whd/src/include/whd_wlioctl.h:2726` |
| 160 | 4 | `d11cnt_rxcrc_off` | `uint32_t` | d11cnt rxcrc value when reset d11cnt. `whd/src/include/whd_wlioctl.h:2727` |
| 164 | 4 | `d11cnt_txnocts_off` | `uint32_t` | d11cnt txnocts value when reset d11cnt. `whd/src/include/whd_wlioctl.h:2728` |
| 168 | 4 | `dmade` | `uint32_t` | tx/rx dma descriptor errors. `whd/src/include/whd_wlioctl.h:2731` |
| 172 | 4 | `dmada` | `uint32_t` | tx/rx dma data errors. `whd/src/include/whd_wlioctl.h:2732` |
| 176 | 4 | `dmape` | `uint32_t` | tx/rx dma descriptor protocol errors. `whd/src/include/whd_wlioctl.h:2733` |
| 180 | 4 | `reset` | `uint32_t` | reset count. `whd/src/include/whd_wlioctl.h:2734` |
| 184 | 4 | `tbtt` | `uint32_t` | cnts the TBTT int's. `whd/src/include/whd_wlioctl.h:2735` |
| 188 | 4 | `txdmawar` | `uint32_t` | # occurrences of PR15420 workaround. `whd/src/include/whd_wlioctl.h:2736` |
| 192 | 4 | `pkt_callback_reg_fail` | `uint32_t` | callbacks register failure. `whd/src/include/whd_wlioctl.h:2737` |
| 196 | 4 | `txallfrm` | `uint32_t` | every frame transmitted (retransmissions counted too), among them Data, ACK, RTS, CTS, Control Management (comment spans lines 2740-2742). `whd/src/include/whd_wlioctl.h:2740` |
| 200 | 4 | `txrtsfrm` | `uint32_t` | how many RTS the MAC transmitted. `whd/src/include/whd_wlioctl.h:2743` |
| 204 | 4 | `txctsfrm` | `uint32_t` | how many CTS the MAC transmitted. `whd/src/include/whd_wlioctl.h:2744` |
| 208 | 4 | `txackfrm` | `uint32_t` | number of ACK frames sent out. `whd/src/include/whd_wlioctl.h:2745` |
| 212 | 4 | `txdnlfrm` | `uint32_t` | Not used. `whd/src/include/whd_wlioctl.h:2746` |
| 216 | 4 | `txbcnfrm` | `uint32_t` | beacons transmitted. `whd/src/include/whd_wlioctl.h:2747` |
| 220 | 24 | `txfunfl` | `uint32_t[6]` | per-fifo tx underflows; array of 6 here (8 in the six/seven variants), followed by rxtoolate and txfbw. `whd/src/include/whd_wlioctl.h:2748` |
| 244 | 4 | `rxtoolate` | `uint32_t` | receive too late. `whd/src/include/whd_wlioctl.h:2749` |
| 248 | 4 | `txfbw` | `uint32_t` | transmit at fallback bw (dynamic bw). `whd/src/include/whd_wlioctl.h:2750` |
| 252 | 4 | `txtplunfl` | `uint32_t` | underflows of the template (ACK/CTS or BCN not transmitted in time by the mac) (comment spans lines 2751-2753). `whd/src/include/whd_wlioctl.h:2751` |
| 256 | 4 | `txphyerror` | `uint32_t` | phy error on transmit; for frames the driver enqueued, tx-status reports which kind of error (comment spans lines 2754-2756). `whd/src/include/whd_wlioctl.h:2754` |
| 260 | 4 | `rxfrmtoolong` | `uint32_t` | frame received whose length exceeds the legal maximum (2346 bytes). `whd/src/include/whd_wlioctl.h:2757` |
| 264 | 4 | `rxfrmtooshrt` | `uint32_t` | frame received that was too short, in bytes, for its type of frame. `whd/src/include/whd_wlioctl.h:2758` |
| 268 | 4 | `rxinvmachdr` | `uint32_t` | protocol version != 0, or else a frame type other than data/control/management (comment spans lines 2759-2761). `whd/src/include/whd_wlioctl.h:2759` |
| 272 | 4 | `rxbadfcs` | `uint32_t` | frames that failed the CRC check done in the MAC. `whd/src/include/whd_wlioctl.h:2762` |
| 276 | 4 | `rxbadplcp` | `uint32_t` | parity check of the PLCP header failed. `whd/src/include/whd_wlioctl.h:2763` |
| 280 | 4 | `rxcrsglitch` | `uint32_t` | the PHY correlated the preamble yet could not correlate the header. `whd/src/include/whd_wlioctl.h:2764` |
| 284 | 4 | `rxstrt` | `uint32_t` | frames received whose PLCP was good (that is, the parity check passed) (comment spans lines 2765-2767). `whd/src/include/whd_wlioctl.h:2765` |
| 288 | 4 | `rxdfrmucastmbss` | `uint32_t` | DATA frames received whose FCS was good and whose RA matched. `whd/src/include/whd_wlioctl.h:2768` |
| 292 | 4 | `rxmfrmucastmbss` | `uint32_t` | mgmt frames received whose FCS was good and whose RA matched. `whd/src/include/whd_wlioctl.h:2769` |
| 296 | 4 | `rxcfrmucast` | `uint32_t` | CNTRL frames received whose FCS was good and whose RA matched. `whd/src/include/whd_wlioctl.h:2770` |
| 300 | 4 | `rxrtsucast` | `uint32_t` | unicast RTS whose destination is the MAC (FCS good). `whd/src/include/whd_wlioctl.h:2771` |
| 304 | 4 | `rxctsucast` | `uint32_t` | unicast CTS whose destination is the MAC (FCS good). `whd/src/include/whd_wlioctl.h:2772` |
| 308 | 4 | `rxackucast` | `uint32_t` | number of ucast ACKS received (good FCS). `whd/src/include/whd_wlioctl.h:2773` |
| 312 | 4 | `rxdfrmocast` | `uint32_t` | DATA frames received (FCS good, RA not matching). `whd/src/include/whd_wlioctl.h:2774` |
| 316 | 4 | `rxmfrmocast` | `uint32_t` | MGMT frames received (FCS good, RA not matching). `whd/src/include/whd_wlioctl.h:2775` |
| 320 | 4 | `rxcfrmocast` | `uint32_t` | CNTRL frames received (FCS good, RA not matching). `whd/src/include/whd_wlioctl.h:2776` |
| 324 | 4 | `rxrtsocast` | `uint32_t` | RTS received whose destination was not the MAC. `whd/src/include/whd_wlioctl.h:2777` |
| 328 | 4 | `rxctsocast` | `uint32_t` | CTS received whose destination was not the MAC. `whd/src/include/whd_wlioctl.h:2778` |
| 332 | 4 | `rxdfrmmcast` | `uint32_t` | multicast RX Data frames the MAC received. `whd/src/include/whd_wlioctl.h:2779` |
| 336 | 4 | `rxmfrmmcast` | `uint32_t` | multicast RX Management frames the MAC received. `whd/src/include/whd_wlioctl.h:2780` |
| 340 | 4 | `rxcfrmmcast` | `uint32_t` | multicast RX Control frames the MAC received (seeing these is unlikely) (comment spans lines 2781-2783). `whd/src/include/whd_wlioctl.h:2781` |
| 344 | 4 | `rxbeaconmbss` | `uint32_t` | beacons received from member of BSS. `whd/src/include/whd_wlioctl.h:2784` |
| 348 | 4 | `rxdfrmucastobss` | `uint32_t` | unicast frames from another BSS whose destination is the MAC (WDS FRAME) (comment spans lines 2785-2787). `whd/src/include/whd_wlioctl.h:2785` |
| 352 | 4 | `rxbeaconobss` | `uint32_t` | beacons received from other BSS. `whd/src/include/whd_wlioctl.h:2788` |
| 356 | 4 | `rxrsptmout` | `uint32_t` | timeouts waiting on a response, for transmitted frames that expected one (comment spans lines 2789-2791). `whd/src/include/whd_wlioctl.h:2789` |
| 360 | 4 | `bcntxcancl` | `uint32_t` | beacon transmissions canceled because a beacon was received (IBSS). `whd/src/include/whd_wlioctl.h:2792` |
| 364 | 4 | `rxf0ovfl` | `uint32_t` | Number of receive fifo 0 overflows. `whd/src/include/whd_wlioctl.h:2793` |
| 368 | 4 | `rxf1ovfl` | `uint32_t` | Number of receive fifo 1 overflows (obsolete). `whd/src/include/whd_wlioctl.h:2794` |
| 372 | 4 | `rxf2ovfl` | `uint32_t` | Number of receive fifo 2 overflows (obsolete). `whd/src/include/whd_wlioctl.h:2795` |
| 376 | 4 | `txsfovfl` | `uint32_t` | Number of transmit status fifo overflows (obsolete). `whd/src/include/whd_wlioctl.h:2796` |
| 380 | 4 | `pmqovfl` | `uint32_t` | Number of PMQ overflows. `whd/src/include/whd_wlioctl.h:2797` |
| 384 | 4 | `rxcgprqfrm` | `uint32_t` | Probe requests received that reached the PRQ fifo (comment spans lines 2798-2800). `whd/src/include/whd_wlioctl.h:2798` |
| 388 | 4 | `rxcgprsqovfl` | `uint32_t` | overflow of the AP's Rx Probe Request Que. `whd/src/include/whd_wlioctl.h:2801` |
| 392 | 4 | `txcgprsfail` | `uint32_t` | Tx Probe Response failure: no ACK came back for a probe response the AP sent (comment spans lines 2802-2804). `whd/src/include/whd_wlioctl.h:2802` |
| 396 | 4 | `txcgprssuc` | `uint32_t` | Tx Probe Response Success (ACK was received). `whd/src/include/whd_wlioctl.h:2805` |
| 400 | 4 | `prs_timeout` | `uint32_t` | probe requests dropped from the PRQ fifo because no probe response could go out inside the time limit that M_PRS_MAXTIME defines (comment spans lines 2806-2809). `whd/src/include/whd_wlioctl.h:2806` |
| 404 | 4 | `rxnack` | `uint32_t` | obsolete. `whd/src/include/whd_wlioctl.h:2810` |
| 408 | 4 | `frmscons` | `uint32_t` | obsolete. `whd/src/include/whd_wlioctl.h:2811` |
| 412 | 4 | `txnack` | `uint32_t` | obsolete. `whd/src/include/whd_wlioctl.h:2812` |
| 416 | 4 | `rxback` | `uint32_t` | blockack rxcnt. `whd/src/include/whd_wlioctl.h:2813` |
| 420 | 4 | `txback` | `uint32_t` | blockack txcnt. `whd/src/include/whd_wlioctl.h:2814` |
| 424 | 4 | `txfrag` | `uint32_t` | dot11TransmittedFragmentCount. `whd/src/include/whd_wlioctl.h:2817` |
| 428 | 4 | `txmulti` | `uint32_t` | dot11MulticastTransmittedFrameCount. `whd/src/include/whd_wlioctl.h:2818` |
| 432 | 4 | `txfail` | `uint32_t` | dot11FailedCount. `whd/src/include/whd_wlioctl.h:2819` |
| 436 | 4 | `txretry` | `uint32_t` | dot11RetryCount. `whd/src/include/whd_wlioctl.h:2820` |
| 440 | 4 | `txretrie` | `uint32_t` | dot11MultipleRetryCount. `whd/src/include/whd_wlioctl.h:2821` |
| 444 | 4 | `rxdup` | `uint32_t` | dot11FrameduplicateCount. `whd/src/include/whd_wlioctl.h:2822` |
| 448 | 4 | `txrts` | `uint32_t` | dot11RTSSuccessCount. `whd/src/include/whd_wlioctl.h:2823` |
| 452 | 4 | `txnocts` | `uint32_t` | dot11RTSFailureCount. `whd/src/include/whd_wlioctl.h:2824` |
| 456 | 4 | `txnoack` | `uint32_t` | dot11ACKFailureCount. `whd/src/include/whd_wlioctl.h:2825` |
| 460 | 4 | `rxfrag` | `uint32_t` | dot11ReceivedFragmentCount. `whd/src/include/whd_wlioctl.h:2826` |
| 464 | 4 | `rxmulti` | `uint32_t` | dot11MulticastReceivedFrameCount. `whd/src/include/whd_wlioctl.h:2827` |
| 468 | 4 | `rxcrc` | `uint32_t` | dot11FCSErrorCount. `whd/src/include/whd_wlioctl.h:2828` |
| 472 | 4 | `txfrmsnt` | `uint32_t` | dot11TransmittedFrameCount (bogus MIB?). `whd/src/include/whd_wlioctl.h:2829` |
| 476 | 4 | `rxundec` | `uint32_t` | dot11WEPUndecryptableCount. `whd/src/include/whd_wlioctl.h:2830` |
| 480 | 4 | `tkipmicfaill` | `uint32_t` | TKIPLocalMICFailures. `whd/src/include/whd_wlioctl.h:2833` |
| 484 | 4 | `tkipcntrmsr` | `uint32_t` | TKIPCounterMeasuresInvoked. `whd/src/include/whd_wlioctl.h:2834` |
| 488 | 4 | `tkipreplay` | `uint32_t` | TKIPReplays. `whd/src/include/whd_wlioctl.h:2835` |
| 492 | 4 | `ccmpfmterr` | `uint32_t` | CCMPFormatErrors. `whd/src/include/whd_wlioctl.h:2836` |
| 496 | 4 | `ccmpreplay` | `uint32_t` | CCMPReplays. `whd/src/include/whd_wlioctl.h:2837` |
| 500 | 4 | `ccmpundec` | `uint32_t` | CCMPDecryptErrors. `whd/src/include/whd_wlioctl.h:2838` |
| 504 | 4 | `fourwayfail` | `uint32_t` | FourWayHandshakeFailures. `whd/src/include/whd_wlioctl.h:2839` |
| 508 | 4 | `wepundec` | `uint32_t` | dot11WEPUndecryptableCount. `whd/src/include/whd_wlioctl.h:2840` |
| 512 | 4 | `wepicverr` | `uint32_t` | dot11WEPICVErrorCount. `whd/src/include/whd_wlioctl.h:2841` |
| 516 | 4 | `decsuccess` | `uint32_t` | DecryptSuccessCount. `whd/src/include/whd_wlioctl.h:2842` |
| 520 | 4 | `tkipicverr` | `uint32_t` | TKIPICVErrorCount. `whd/src/include/whd_wlioctl.h:2843` |
| 524 | 4 | `wepexcluded` | `uint32_t` | dot11WEPExcludedCount. `whd/src/include/whd_wlioctl.h:2844` |
| 528 | 4 | `txchanrej` | `uint32_t` | Tx frames suppressed due to channel rejection. `whd/src/include/whd_wlioctl.h:2846` |
| 532 | 4 | `psmwds` | `uint32_t` | Count PSM watchdogs. `whd/src/include/whd_wlioctl.h:2847` |
| 536 | 4 | `phywatchdog` | `uint32_t` | Count Phy watchdogs (triggered by ucode). `whd/src/include/whd_wlioctl.h:2848` |
| 540 | 4 | `prq_entries_handled` | `uint32_t` | PRQ entries read in. `whd/src/include/whd_wlioctl.h:2851` |
| 544 | 4 | `prq_undirected_entries` | `uint32_t` | which were bcast bss & ssid. `whd/src/include/whd_wlioctl.h:2852` |
| 548 | 4 | `prq_bad_entries` | `uint32_t` | which could not be translated to info. `whd/src/include/whd_wlioctl.h:2853` |
| 552 | 4 | `atim_suppress_count` | `uint32_t` | TX suppressions on ATIM fifo. `whd/src/include/whd_wlioctl.h:2854` |
| 556 | 4 | `bcn_template_not_ready` | `uint32_t` | Template marked in use on send bcn . `whd/src/include/whd_wlioctl.h:2855` |
| 560 | 4 | `bcn_template_not_ready_done` | `uint32_t` | ...but "DMA done" interrupt rcvd. `whd/src/include/whd_wlioctl.h:2856` |
| 564 | 4 | `late_tbtt_dpc` | `uint32_t` | TBTT DPC did not happen in time. `whd/src/include/whd_wlioctl.h:2857` |
| 568 | 4 | `rx1mbps` | `uint32_t` | packets rx at 1Mbps. `whd/src/include/whd_wlioctl.h:2860` |
| 572 | 4 | `rx2mbps` | `uint32_t` | packets rx at 2Mbps. `whd/src/include/whd_wlioctl.h:2861` |
| 576 | 4 | `rx5mbps5` | `uint32_t` | packets rx at 5.5Mbps. `whd/src/include/whd_wlioctl.h:2862` |
| 580 | 4 | `rx6mbps` | `uint32_t` | packets rx at 6Mbps. `whd/src/include/whd_wlioctl.h:2863` |
| 584 | 4 | `rx9mbps` | `uint32_t` | packets rx at 9Mbps. `whd/src/include/whd_wlioctl.h:2864` |
| 588 | 4 | `rx11mbps` | `uint32_t` | packets rx at 11Mbps. `whd/src/include/whd_wlioctl.h:2865` |
| 592 | 4 | `rx12mbps` | `uint32_t` | packets rx at 12Mbps. `whd/src/include/whd_wlioctl.h:2866` |
| 596 | 4 | `rx18mbps` | `uint32_t` | packets rx at 18Mbps. `whd/src/include/whd_wlioctl.h:2867` |
| 600 | 4 | `rx24mbps` | `uint32_t` | packets rx at 24Mbps. `whd/src/include/whd_wlioctl.h:2868` |
| 604 | 4 | `rx36mbps` | `uint32_t` | packets rx at 36Mbps. `whd/src/include/whd_wlioctl.h:2869` |
| 608 | 4 | `rx48mbps` | `uint32_t` | packets rx at 48Mbps. `whd/src/include/whd_wlioctl.h:2870` |
| 612 | 4 | `rx54mbps` | `uint32_t` | packets rx at 54Mbps. `whd/src/include/whd_wlioctl.h:2871` |
| 616 | 4 | `rx108mbps` | `uint32_t` | packets rx at 108mbps. `whd/src/include/whd_wlioctl.h:2872` |
| 620 | 4 | `rx162mbps` | `uint32_t` | packets rx at 162mbps. `whd/src/include/whd_wlioctl.h:2873` |
| 624 | 4 | `rx216mbps` | `uint32_t` | packets rx at 216 mbps. `whd/src/include/whd_wlioctl.h:2874` |
| 628 | 4 | `rx270mbps` | `uint32_t` | packets rx at 270 mbps. `whd/src/include/whd_wlioctl.h:2875` |
| 632 | 4 | `rx324mbps` | `uint32_t` | packets rx at 324 mbps. `whd/src/include/whd_wlioctl.h:2876` |
| 636 | 4 | `rx378mbps` | `uint32_t` | packets rx at 378 mbps. `whd/src/include/whd_wlioctl.h:2877` |
| 640 | 4 | `rx432mbps` | `uint32_t` | packets rx at 432 mbps. `whd/src/include/whd_wlioctl.h:2878` |
| 644 | 4 | `rx486mbps` | `uint32_t` | packets rx at 486 mbps. `whd/src/include/whd_wlioctl.h:2879` |
| 648 | 4 | `rx540mbps` | `uint32_t` | packets rx at 540 mbps. `whd/src/include/whd_wlioctl.h:2880` |
| 652 | 4 | `pktengrxducast` | `uint32_t` | unicast frames rxed by the pkteng code. `whd/src/include/whd_wlioctl.h:2883` |
| 656 | 4 | `pktengrxdmcast` | `uint32_t` | multicast frames rxed by the pkteng code. `whd/src/include/whd_wlioctl.h:2884` |
| 660 | 4 | `rfdisable` | `uint32_t` | count of radio disables. `whd/src/include/whd_wlioctl.h:2886` |
| 664 | 4 | `bphy_rxcrsglitch` | `uint32_t` | PHY count of bphy glitches. `whd/src/include/whd_wlioctl.h:2887` |
| 668 | 4 | `bphy_badplcp` | `uint32_t` | `whd/src/include/whd_wlioctl.h:2888` |
| 672 | 4 | `txexptime` | `uint32_t` | Tx frames suppressed due to timer expiration. `whd/src/include/whd_wlioctl.h:2890` |
| 676 | 4 | `txmpdu_sgi` | `uint32_t` | count for sgi transmit. `whd/src/include/whd_wlioctl.h:2892` |
| 680 | 4 | `rxmpdu_sgi` | `uint32_t` | count for sgi received. `whd/src/include/whd_wlioctl.h:2893` |
| 684 | 4 | `txmpdu_stbc` | `uint32_t` | count for stbc transmit. `whd/src/include/whd_wlioctl.h:2894` |
| 688 | 4 | `rxmpdu_stbc` | `uint32_t` | count for stbc received. `whd/src/include/whd_wlioctl.h:2895` |
| 692 | 4 | `rxundec_mcst` | `uint32_t` | dot11WEPUndecryptableCount. `whd/src/include/whd_wlioctl.h:2897` |
| 696 | 4 | `tkipmicfaill_mcst` | `uint32_t` | TKIPLocalMICFailures. `whd/src/include/whd_wlioctl.h:2900` |
| 700 | 4 | `tkipcntrmsr_mcst` | `uint32_t` | TKIPCounterMeasuresInvoked. `whd/src/include/whd_wlioctl.h:2901` |
| 704 | 4 | `tkipreplay_mcst` | `uint32_t` | TKIPReplays. `whd/src/include/whd_wlioctl.h:2902` |
| 708 | 4 | `ccmpfmterr_mcst` | `uint32_t` | CCMPFormatErrors. `whd/src/include/whd_wlioctl.h:2903` |
| 712 | 4 | `ccmpreplay_mcst` | `uint32_t` | CCMPReplays. `whd/src/include/whd_wlioctl.h:2904` |
| 716 | 4 | `ccmpundec_mcst` | `uint32_t` | CCMPDecryptErrors. `whd/src/include/whd_wlioctl.h:2905` |
| 720 | 4 | `fourwayfail_mcst` | `uint32_t` | FourWayHandshakeFailures. `whd/src/include/whd_wlioctl.h:2906` |
| 724 | 4 | `wepundec_mcst` | `uint32_t` | dot11WEPUndecryptableCount. `whd/src/include/whd_wlioctl.h:2907` |
| 728 | 4 | `wepicverr_mcst` | `uint32_t` | dot11WEPICVErrorCount. `whd/src/include/whd_wlioctl.h:2908` |
| 732 | 4 | `decsuccess_mcst` | `uint32_t` | DecryptSuccessCount. `whd/src/include/whd_wlioctl.h:2909` |
| 736 | 4 | `tkipicverr_mcst` | `uint32_t` | TKIPICVErrorCount. `whd/src/include/whd_wlioctl.h:2910` |
| 740 | 4 | `wepexcluded_mcst` | `uint32_t` | dot11WEPExcludedCount. `whd/src/include/whd_wlioctl.h:2911` |
| 744 | 4 | `dma_hang` | `uint32_t` | count for dma hang. `whd/src/include/whd_wlioctl.h:2913` |
| 748 | 4 | `reinit` | `uint32_t` | count for reinit. `whd/src/include/whd_wlioctl.h:2914` |
| 752 | 4 | `pstatxucast` | `uint32_t` | ucast frames transmitted, summed over every psta assoc. `whd/src/include/whd_wlioctl.h:2916` |
| 756 | 4 | `pstatxnoassoc` | `uint32_t` | txnoassoc frames transmitted, summed over every psta assoc. `whd/src/include/whd_wlioctl.h:2917` |
| 760 | 4 | `pstarxucast` | `uint32_t` | ucast frames received, summed over every psta assoc. `whd/src/include/whd_wlioctl.h:2918` |
| 764 | 4 | `pstarxbcmc` | `uint32_t` | bcmc frames received, summed over every psta. `whd/src/include/whd_wlioctl.h:2919` |
| 768 | 4 | `pstatxbcmc` | `uint32_t` | bcmc frames transmitted, summed over every psta. `whd/src/include/whd_wlioctl.h:2920` |
| 772 | 4 | `cso_passthrough` | `uint32_t` | hw cso required but passthrough. `whd/src/include/whd_wlioctl.h:2922` |
| 776 | 4 | `cso_normal` | `uint32_t` | hw cso hdr for normal process. `whd/src/include/whd_wlioctl.h:2923` |
| 780 | 4 | `chained` | `uint32_t` | number of frames chained. `whd/src/include/whd_wlioctl.h:2924` |
| 784 | 4 | `chainedsz1` | `uint32_t` | number of chain size 1 frames. `whd/src/include/whd_wlioctl.h:2925` |
| 788 | 4 | `unchained` | `uint32_t` | number of frames not chained. `whd/src/include/whd_wlioctl.h:2926` |
| 792 | 4 | `maxchainsz` | `uint32_t` | max chain size so far. `whd/src/include/whd_wlioctl.h:2927` |
| 796 | 4 | `currchainsz` | `uint32_t` | current chain size. `whd/src/include/whd_wlioctl.h:2928` |
| 800 | 4 | `rxdrop20s` | `uint32_t` | drop secondary cnt. `whd/src/include/whd_wlioctl.h:2930` |

Size check: compiled

Differences: the type name is not found in linux, embassy, c-driver or pico-sdk; the only other "counters" name in these sources is a linux debugfs entry, unrelated to this variable. `linux/brcmfmac/sdio.c:3230`

### `whd_phyrate_counters_t` (whd)
Sixteen per-rate receive packet counters, commented as the receive statistics counters kept per rate, a subset of the full counter set, at `whd/src/include/whd_wlioctl.h:2934`, with no use site in whd outside the header and no command or named variable (iovar) given for it there, and the name not found in linux, embassy, c-driver or pico-sdk; whether it goes on the wire as-is cannot be told from these sources; (unverified) as a wire record: the name appears only in the two whd copies of the header and nothing in these sources shows it crossing the bus; not packed (the header's first `#pragma pack(1)` is at line 3864, after the definition; alignment 4); 64 bytes; byte order not stated in the definition, little-endian as whd treats it (inferred: plain uintN_t types, and whd's htod16/htod32/dtoh16/dtoh32 are identity unless IL_BIGENDIAN is defined). `whd/src/include/whd_wlioctl.h:2935-2953` `whd/src/include/whd_wlioctl.h:3864` `whd/src/include/whd_endian.h:44-57`

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `rx1mbps` | `uint32_t` | `whd/src/include/whd_wlioctl.h:2937` |
| 4 | 4 | `rx2mbps` | `uint32_t` | `whd/src/include/whd_wlioctl.h:2938` |
| 8 | 4 | `rx5mbps5` | `uint32_t` | `whd/src/include/whd_wlioctl.h:2939` |
| 12 | 4 | `rx6mbps` | `uint32_t` | `whd/src/include/whd_wlioctl.h:2940` |
| 16 | 4 | `rx9mbps` | `uint32_t` | `whd/src/include/whd_wlioctl.h:2941` |
| 20 | 4 | `rx11mbps` | `uint32_t` | `whd/src/include/whd_wlioctl.h:2942` |
| 24 | 4 | `rx12mbps` | `uint32_t` | `whd/src/include/whd_wlioctl.h:2943` |
| 28 | 4 | `rx18mbps` | `uint32_t` | `whd/src/include/whd_wlioctl.h:2944` |
| 32 | 4 | `rx24mbps` | `uint32_t` | `whd/src/include/whd_wlioctl.h:2945` |
| 36 | 4 | `rx36mbps` | `uint32_t` | `whd/src/include/whd_wlioctl.h:2946` |
| 40 | 4 | `rx48mbps` | `uint32_t` | `whd/src/include/whd_wlioctl.h:2947` |
| 44 | 4 | `rx54mbps` | `uint32_t` | `whd/src/include/whd_wlioctl.h:2948` |
| 48 | 4 | `rx108mbps` | `uint32_t` | `whd/src/include/whd_wlioctl.h:2949` |
| 52 | 4 | `rx162mbps` | `uint32_t` | `whd/src/include/whd_wlioctl.h:2950` |
| 56 | 4 | `rx216mbps` | `uint32_t` | `whd/src/include/whd_wlioctl.h:2951` |
| 60 | 4 | `rx270mbps` | `uint32_t` | `whd/src/include/whd_wlioctl.h:2952` |

Size check: compiled

### `whd_phyrate_log_t` (whd)
Count word followed by a 1200-byte log array, with no use site in whd outside the header and no command or named variable given for it there, and the name not found in linux, embassy, c-driver or pico-sdk; whether it is a record exchanged with the chip or host-side bookkeeping cannot be told from these sources; (unverified) as a wire record: the name appears only in the two whd copies of the header and nothing in these sources shows it crossing the bus; not packed (the header's first `#pragma pack(1)` is at line 3864, after the definition; alignment 4); 1204 bytes; byte order not stated in the definition, little-endian as whd treats it (inferred: plain uintN_t types, and whd's htod16/htod32/dtoh16/dtoh32 are identity unless IL_BIGENDIAN is defined). `whd/src/include/whd_wlioctl.h:2955-2959` `whd/src/include/whd_wlioctl.h:3864` `whd/src/include/whd_endian.h:44-57`

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `count` | `uint32_t` | `whd/src/include/whd_wlioctl.h:2957` |
| 4 | 1200 | `log` | `uint8_t[WL_PHYRATE_LOG_SIZE]` | `whd/src/include/whd_wlioctl.h:2958`; WL_PHYRATE_LOG_SIZE = 1200 `whd/src/include/whd_wlioctl.h:1986` |

Size check: compiled

### `wl_cnt_ver_ten_t` (whd)
Counters block with a version and length header (the type name says version ten), with no use site in whd outside the header and no command or named variable given for it there, and the name not found in linux, embassy, c-driver or pico-sdk; IOVAR_STR_COUNTERS "counters" is defined at `whd/src/include/whd_wlioctl.h:1091` but no code in these sources ties this record to it; not packed (the header's first `#pragma pack(1)` is at line 3864, after the definition; alignment 4); 848 bytes; byte order not stated in the definition, little-endian as whd treats it (inferred: plain uintN_t types, and whd's htod16/htod32/dtoh16/dtoh32 are identity unless IL_BIGENDIAN is defined). `whd/src/include/whd_wlioctl.h:2961-3215` `whd/src/include/whd_wlioctl.h:3864` `whd/src/include/whd_endian.h:44-57`

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 2 | `version` | `uint16_t` | `whd/src/include/whd_wlioctl.h:2963` |
| 2 | 2 | `length` | `uint16_t` | `whd/src/include/whd_wlioctl.h:2964` |
| 4 | 4 | `txframe` | `uint32_t` | `whd/src/include/whd_wlioctl.h:2967` |
| 8 | 4 | `txbyte` | `uint32_t` | `whd/src/include/whd_wlioctl.h:2968` |
| 12 | 4 | `txretrans` | `uint32_t` | `whd/src/include/whd_wlioctl.h:2969` |
| 16 | 4 | `txerror` | `uint32_t` | `whd/src/include/whd_wlioctl.h:2970` |
| 20 | 4 | `txctl` | `uint32_t` | `whd/src/include/whd_wlioctl.h:2971` |
| 24 | 4 | `txprshort` | `uint32_t` | `whd/src/include/whd_wlioctl.h:2972` |
| 28 | 4 | `txserr` | `uint32_t` | `whd/src/include/whd_wlioctl.h:2973` |
| 32 | 4 | `txnobuf` | `uint32_t` | `whd/src/include/whd_wlioctl.h:2974` |
| 36 | 4 | `txnoassoc` | `uint32_t` | `whd/src/include/whd_wlioctl.h:2975` |
| 40 | 4 | `txrunt` | `uint32_t` | `whd/src/include/whd_wlioctl.h:2976` |
| 44 | 4 | `txchit` | `uint32_t` | `whd/src/include/whd_wlioctl.h:2977` |
| 48 | 4 | `txcmiss` | `uint32_t` | `whd/src/include/whd_wlioctl.h:2978` |
| 52 | 4 | `txuflo` | `uint32_t` | `whd/src/include/whd_wlioctl.h:2981` |
| 56 | 4 | `txphyerr` | `uint32_t` | `whd/src/include/whd_wlioctl.h:2982` |
| 60 | 4 | `txphycrs` | `uint32_t` | `whd/src/include/whd_wlioctl.h:2983` |
| 64 | 4 | `rxframe` | `uint32_t` | `whd/src/include/whd_wlioctl.h:2986` |
| 68 | 4 | `rxbyte` | `uint32_t` | `whd/src/include/whd_wlioctl.h:2987` |
| 72 | 4 | `rxerror` | `uint32_t` | `whd/src/include/whd_wlioctl.h:2988` |
| 76 | 4 | `rxctl` | `uint32_t` | `whd/src/include/whd_wlioctl.h:2989` |
| 80 | 4 | `rxnobuf` | `uint32_t` | `whd/src/include/whd_wlioctl.h:2990` |
| 84 | 4 | `rxnondata` | `uint32_t` | `whd/src/include/whd_wlioctl.h:2991` |
| 88 | 4 | `rxbadds` | `uint32_t` | `whd/src/include/whd_wlioctl.h:2992` |
| 92 | 4 | `rxbadcm` | `uint32_t` | `whd/src/include/whd_wlioctl.h:2993` |
| 96 | 4 | `rxfragerr` | `uint32_t` | `whd/src/include/whd_wlioctl.h:2994` |
| 100 | 4 | `rxrunt` | `uint32_t` | `whd/src/include/whd_wlioctl.h:2995` |
| 104 | 4 | `rxgiant` | `uint32_t` | `whd/src/include/whd_wlioctl.h:2996` |
| 108 | 4 | `rxnoscb` | `uint32_t` | `whd/src/include/whd_wlioctl.h:2997` |
| 112 | 4 | `rxbadproto` | `uint32_t` | `whd/src/include/whd_wlioctl.h:2998` |
| 116 | 4 | `rxbadsrcmac` | `uint32_t` | `whd/src/include/whd_wlioctl.h:2999` |
| 120 | 4 | `rxbadda` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3000` |
| 124 | 4 | `rxfilter` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3001` |
| 128 | 4 | `rxoflo` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3004` |
| 132 | 24 | `rxuflo` | `uint32_t[NFIFO]` | `whd/src/include/whd_wlioctl.h:3005`; NFIFO = 6 `whd/src/include/whd_wlioctl.h:1983` |
| 156 | 4 | `d11cnt_txrts_off` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3007` |
| 160 | 4 | `d11cnt_rxcrc_off` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3008` |
| 164 | 4 | `d11cnt_txnocts_off` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3009` |
| 168 | 4 | `dmade` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3012` |
| 172 | 4 | `dmada` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3013` |
| 176 | 4 | `dmape` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3014` |
| 180 | 4 | `reset` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3015` |
| 184 | 4 | `tbtt` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3016` |
| 188 | 4 | `txdmawar` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3017` |
| 192 | 4 | `pkt_callback_reg_fail` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3018` |
| 196 | 4 | `txallfrm` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3021` |
| 200 | 4 | `txrtsfrm` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3024` |
| 204 | 4 | `txctsfrm` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3025` |
| 208 | 4 | `txackfrm` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3026` |
| 212 | 4 | `txdnlfrm` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3027` |
| 216 | 4 | `txbcnfrm` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3028` |
| 220 | 24 | `txfunfl` | `uint32_t[6]` | `whd/src/include/whd_wlioctl.h:3029` |
| 244 | 4 | `rxtoolate` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3030` |
| 248 | 4 | `txfbw` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3031` |
| 252 | 4 | `txtplunfl` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3032` |
| 256 | 4 | `txphyerror` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3035` |
| 260 | 4 | `rxfrmtoolong` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3038` |
| 264 | 4 | `rxfrmtooshrt` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3039` |
| 268 | 4 | `rxinvmachdr` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3040` |
| 272 | 4 | `rxbadfcs` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3043` |
| 276 | 4 | `rxbadplcp` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3044` |
| 280 | 4 | `rxcrsglitch` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3045` |
| 284 | 4 | `rxstrt` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3046` |
| 288 | 4 | `rxdfrmucastmbss` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3049` |
| 292 | 4 | `rxmfrmucastmbss` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3050` |
| 296 | 4 | `rxcfrmucast` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3051` |
| 300 | 4 | `rxrtsucast` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3052` |
| 304 | 4 | `rxctsucast` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3053` |
| 308 | 4 | `rxackucast` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3054` |
| 312 | 4 | `rxdfrmocast` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3055` |
| 316 | 4 | `rxmfrmocast` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3056` |
| 320 | 4 | `rxcfrmocast` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3057` |
| 324 | 4 | `rxrtsocast` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3058` |
| 328 | 4 | `rxctsocast` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3059` |
| 332 | 4 | `rxdfrmmcast` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3060` |
| 336 | 4 | `rxmfrmmcast` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3061` |
| 340 | 4 | `rxcfrmmcast` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3062` |
| 344 | 4 | `rxbeaconmbss` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3065` |
| 348 | 4 | `rxdfrmucastobss` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3066` |
| 352 | 4 | `rxbeaconobss` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3069` |
| 356 | 4 | `rxrsptmout` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3070` |
| 360 | 4 | `bcntxcancl` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3073` |
| 364 | 4 | `rxf0ovfl` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3074` |
| 368 | 4 | `rxf1ovfl` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3075` |
| 372 | 4 | `rxf2ovfl` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3076` |
| 376 | 4 | `txsfovfl` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3077` |
| 380 | 4 | `pmqovfl` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3078` |
| 384 | 4 | `rxcgprqfrm` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3079` |
| 388 | 4 | `rxcgprsqovfl` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3082` |
| 392 | 4 | `txcgprsfail` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3083` |
| 396 | 4 | `txcgprssuc` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3086` |
| 400 | 4 | `prs_timeout` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3087` |
| 404 | 4 | `rxnack` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3091` |
| 408 | 4 | `frmscons` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3092` |
| 412 | 4 | `txnack` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3093` |
| 416 | 4 | `rxback` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3094` |
| 420 | 4 | `txback` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3095` |
| 424 | 4 | `txfrag` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3098` |
| 428 | 4 | `txmulti` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3099` |
| 432 | 4 | `txfail` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3100` |
| 436 | 4 | `txretry` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3101` |
| 440 | 4 | `txretrie` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3102` |
| 444 | 4 | `rxdup` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3103` |
| 448 | 4 | `txrts` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3104` |
| 452 | 4 | `txnocts` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3105` |
| 456 | 4 | `txnoack` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3106` |
| 460 | 4 | `rxfrag` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3107` |
| 464 | 4 | `rxmulti` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3108` |
| 468 | 4 | `rxcrc` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3109` |
| 472 | 4 | `txfrmsnt` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3110` |
| 476 | 4 | `rxundec` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3111` |
| 480 | 4 | `tkipmicfaill` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3114` |
| 484 | 4 | `tkipcntrmsr` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3115` |
| 488 | 4 | `tkipreplay` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3116` |
| 492 | 4 | `ccmpfmterr` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3117` |
| 496 | 4 | `ccmpreplay` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3118` |
| 500 | 4 | `ccmpundec` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3119` |
| 504 | 4 | `fourwayfail` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3120` |
| 508 | 4 | `wepundec` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3121` |
| 512 | 4 | `wepicverr` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3122` |
| 516 | 4 | `decsuccess` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3123` |
| 520 | 4 | `tkipicverr` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3124` |
| 524 | 4 | `wepexcluded` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3125` |
| 528 | 4 | `txchanrej` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3127` |
| 532 | 4 | `psmwds` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3128` |
| 536 | 4 | `phywatchdog` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3129` |
| 540 | 4 | `prq_entries_handled` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3132` |
| 544 | 4 | `prq_undirected_entries` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3133` |
| 548 | 4 | `prq_bad_entries` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3134` |
| 552 | 4 | `atim_suppress_count` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3135` |
| 556 | 4 | `bcn_template_not_ready` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3136` |
| 560 | 4 | `bcn_template_not_ready_done` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3137` |
| 564 | 4 | `late_tbtt_dpc` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3138` |
| 568 | 4 | `rx1mbps` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3141` |
| 572 | 4 | `rx2mbps` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3142` |
| 576 | 4 | `rx5mbps5` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3143` |
| 580 | 4 | `rx6mbps` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3144` |
| 584 | 4 | `rx9mbps` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3145` |
| 588 | 4 | `rx11mbps` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3146` |
| 592 | 4 | `rx12mbps` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3147` |
| 596 | 4 | `rx18mbps` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3148` |
| 600 | 4 | `rx24mbps` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3149` |
| 604 | 4 | `rx36mbps` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3150` |
| 608 | 4 | `rx48mbps` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3151` |
| 612 | 4 | `rx54mbps` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3152` |
| 616 | 4 | `rx108mbps` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3153` |
| 620 | 4 | `rx162mbps` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3154` |
| 624 | 4 | `rx216mbps` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3155` |
| 628 | 4 | `rx270mbps` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3156` |
| 632 | 4 | `rx324mbps` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3157` |
| 636 | 4 | `rx378mbps` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3158` |
| 640 | 4 | `rx432mbps` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3159` |
| 644 | 4 | `rx486mbps` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3160` |
| 648 | 4 | `rx540mbps` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3161` |
| 652 | 4 | `pktengrxducast` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3164` |
| 656 | 4 | `pktengrxdmcast` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3165` |
| 660 | 4 | `rfdisable` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3167` |
| 664 | 4 | `bphy_rxcrsglitch` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3168` |
| 668 | 4 | `bphy_badplcp` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3169` |
| 672 | 4 | `txexptime` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3171` |
| 676 | 4 | `txmpdu_sgi` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3173` |
| 680 | 4 | `rxmpdu_sgi` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3174` |
| 684 | 4 | `txmpdu_stbc` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3175` |
| 688 | 4 | `rxmpdu_stbc` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3176` |
| 692 | 4 | `rxundec_mcst` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3178` |
| 696 | 4 | `tkipmicfaill_mcst` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3181` |
| 700 | 4 | `tkipcntrmsr_mcst` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3182` |
| 704 | 4 | `tkipreplay_mcst` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3183` |
| 708 | 4 | `ccmpfmterr_mcst` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3184` |
| 712 | 4 | `ccmpreplay_mcst` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3185` |
| 716 | 4 | `ccmpundec_mcst` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3186` |
| 720 | 4 | `fourwayfail_mcst` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3187` |
| 724 | 4 | `wepundec_mcst` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3188` |
| 728 | 4 | `wepicverr_mcst` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3189` |
| 732 | 4 | `decsuccess_mcst` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3190` |
| 736 | 4 | `tkipicverr_mcst` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3191` |
| 740 | 4 | `wepexcluded_mcst` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3192` |
| 744 | 4 | `dma_hang` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3194` |
| 748 | 4 | `reinit` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3195` |
| 752 | 4 | `pstatxucast` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3197` |
| 756 | 4 | `pstatxnoassoc` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3198` |
| 760 | 4 | `pstarxucast` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3199` |
| 764 | 4 | `pstarxbcmc` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3200` |
| 768 | 4 | `pstatxbcmc` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3201` |
| 772 | 4 | `cso_passthrough` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3203` |
| 776 | 4 | `cso_normal` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3204` |
| 780 | 4 | `chained` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3205` |
| 784 | 4 | `chainedsz1` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3206` |
| 788 | 4 | `unchained` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3207` |
| 792 | 4 | `maxchainsz` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3208` |
| 796 | 4 | `currchainsz` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3209` |
| 800 | 4 | `rxdrop20s` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3210` |
| 804 | 4 | `pciereset` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3211` |
| 808 | 4 | `cfgrestore` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3212` |
| 812 | 32 | `reinitreason` | `uint32_t[8]` | `whd/src/include/whd_wlioctl.h:3213` |
| 844 | 4 | `rxrtry` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3214` |

Size check: compiled

### `wl_cnt_ext_t` (whd)
Extended counters block with a version and length header: SGI and STBC receive counts, 40 MHz MCS receive counts and per-bandwidth transmit counts (inferred from the field names), with no use site in whd outside the header and no command or named variable given for it there, and the name not found in linux, embassy, c-driver or pico-sdk; not packed (the header's first `#pragma pack(1)` is at line 3864, after the definition; alignment 4); 72 bytes; byte order not stated in the definition, little-endian as whd treats it (inferred: plain uintN_t types, and whd's htod16/htod32/dtoh16/dtoh32 are identity unless IL_BIGENDIAN is defined). `whd/src/include/whd_wlioctl.h:3217-3238` `whd/src/include/whd_wlioctl.h:3864` `whd/src/include/whd_endian.h:44-57`

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 2 | `version` | `uint16_t` | `whd/src/include/whd_wlioctl.h:3219` |
| 2 | 2 | `length` | `uint16_t` | `whd/src/include/whd_wlioctl.h:3220` |
| 4 | 4 | `rxampdu_sgi` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3221` |
| 8 | 4 | `rxampdu_stbc` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3222` |
| 12 | 4 | `rxmpdu_sgi` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3223` |
| 16 | 4 | `rxmpdu_stbc` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3224` |
| 20 | 4 | `rxmcs0_40M` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3225` |
| 24 | 4 | `rxmcs1_40M` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3226` |
| 28 | 4 | `rxmcs2_40M` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3227` |
| 32 | 4 | `rxmcs3_40M` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3228` |
| 36 | 4 | `rxmcs4_40M` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3229` |
| 40 | 4 | `rxmcs5_40M` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3230` |
| 44 | 4 | `rxmcs6_40M` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3231` |
| 48 | 4 | `rxmcs7_40M` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3232` |
| 52 | 4 | `rxmcs32_40M` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3233` |
| 56 | 4 | `txfrmsnt_20Mlo` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3234` |
| 60 | 4 | `txfrmsnt_20Mup` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3235` |
| 64 | 4 | `txfrmsnt_40M` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3236` |
| 68 | 4 | `rx_20ul` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3237` |

Size check: compiled

### `wl_rxdiv_stats_t` (whd)
Four per-antenna receive counts with a version and length header (inferred from the field names), with no use site in whd outside the header and no command or named variable given for it there, and the name not found in linux, embassy, c-driver or pico-sdk; not packed (the header's first `#pragma pack(1)` is at line 3864, after the definition; alignment 4); 20 bytes; byte order not stated in the definition, little-endian as whd treats it (inferred: plain uintN_t types, and whd's htod16/htod32/dtoh16/dtoh32 are identity unless IL_BIGENDIAN is defined). `whd/src/include/whd_wlioctl.h:3240-3245` `whd/src/include/whd_wlioctl.h:3864` `whd/src/include/whd_endian.h:44-57`

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 2 | `version` | `uint16_t` | `whd/src/include/whd_wlioctl.h:3242`; WL_RXDIV_STATS_T_VERSION = 1 `whd/src/include/whd_wlioctl.h:3239` |
| 2 | 2 | `length` | `uint16_t` | `whd/src/include/whd_wlioctl.h:3243` |
| 4 | 16 | `rxant` | `uint32_t[4]` | `whd/src/include/whd_wlioctl.h:3244` |

Size check: compiled

### `wl_delta_stats_t` (whd)
Delta statistics with a version and length header: frame and byte totals and per-rate receive counts (inferred from the names), with no use site in whd outside the header and no command or named variable given for it there, and the name not found in linux, embassy, c-driver or pico-sdk; not packed (the header's first `#pragma pack(1)` is at line 3864, after the definition; alignment 4); 112 bytes; byte order not stated in the definition, little-endian as whd treats it (inferred: plain uintN_t types, and whd's htod16/htod32/dtoh16/dtoh32 are identity unless IL_BIGENDIAN is defined). `whd/src/include/whd_wlioctl.h:3247-3278` `whd/src/include/whd_wlioctl.h:3864` `whd/src/include/whd_endian.h:44-57`

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 2 | `version` | `uint16_t` | `whd/src/include/whd_wlioctl.h:3249`; WL_DELTA_STATS_T_VERSION = 1 `whd/src/include/whd_wlioctl.h:3246` |
| 2 | 2 | `length` | `uint16_t` | `whd/src/include/whd_wlioctl.h:3250` |
| 4 | 4 | `txframe` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3251` |
| 8 | 4 | `txbyte` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3252` |
| 12 | 4 | `txretrans` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3253` |
| 16 | 4 | `txfail` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3254` |
| 20 | 4 | `rxframe` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3255` |
| 24 | 4 | `rxbyte` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3256` |
| 28 | 4 | `rx1mbps` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3257` |
| 32 | 4 | `rx2mbps` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3258` |
| 36 | 4 | `rx5mbps5` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3259` |
| 40 | 4 | `rx6mbps` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3260` |
| 44 | 4 | `rx9mbps` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3261` |
| 48 | 4 | `rx11mbps` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3262` |
| 52 | 4 | `rx12mbps` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3263` |
| 56 | 4 | `rx18mbps` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3264` |
| 60 | 4 | `rx24mbps` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3265` |
| 64 | 4 | `rx36mbps` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3266` |
| 68 | 4 | `rx48mbps` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3267` |
| 72 | 4 | `rx54mbps` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3268` |
| 76 | 4 | `rx108mbps` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3269` |
| 80 | 4 | `rx162mbps` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3270` |
| 84 | 4 | `rx216mbps` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3271` |
| 88 | 4 | `rx270mbps` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3272` |
| 92 | 4 | `rx324mbps` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3273` |
| 96 | 4 | `rx378mbps` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3274` |
| 100 | 4 | `rx432mbps` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3275` |
| 104 | 4 | `rx486mbps` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3276` |
| 108 | 4 | `rx540mbps` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3277` |

Size check: compiled

### `wl_traffic_stats_t` (whd)
Packet count and byte count pair, the element type of the arrays in `wl_wme_cnt_t` `whd/src/include/whd_wlioctl.h:3290-3295`, with no use site in whd outside the header and no command or named variable given for it there, and the name not found in linux, embassy, c-driver or pico-sdk; not packed (the header's first `#pragma pack(1)` is at line 3864, after the definition; alignment 4); 8 bytes; byte order not stated in the definition, little-endian as whd treats it (inferred: plain uintN_t types, and whd's htod16/htod32/dtoh16/dtoh32 are identity unless IL_BIGENDIAN is defined). `whd/src/include/whd_wlioctl.h:3280-3284` `whd/src/include/whd_wlioctl.h:3864` `whd/src/include/whd_endian.h:44-57`

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `packets` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3282` |
| 4 | 4 | `bytes` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3283` |

Size check: compiled

### `wl_wme_cnt_t` (whd)
Six arrays of per-access-category traffic counters with a version and length header, with no use site in whd outside the header and no command or named variable given for it there, and the name not found in linux, embassy, c-driver or pico-sdk; not packed (the header's first `#pragma pack(1)` is at line 3864, after the definition; alignment 4); 196 bytes; byte order not stated in the definition, little-endian as whd treats it (inferred: plain uintN_t types, and whd's htod16/htod32/dtoh16/dtoh32 are identity unless IL_BIGENDIAN is defined). `whd/src/include/whd_wlioctl.h:3286-3296` `whd/src/include/whd_wlioctl.h:3864` `whd/src/include/whd_endian.h:44-57`

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 2 | `version` | `uint16_t` | `whd/src/include/whd_wlioctl.h:3288`; WL_WME_CNT_VERSION = 1 `whd/src/include/whd_wlioctl.h:3279` |
| 2 | 2 | `length` | `uint16_t` | `whd/src/include/whd_wlioctl.h:3289` |
| 4 | 32 | `tx` | `wl_traffic_stats_t[AC_COUNT]` | `whd/src/include/whd_wlioctl.h:3290`; AC_COUNT = 4 `whd/src/include/whd_wlioctl.h:3285` |
| 36 | 32 | `tx_failed` | `wl_traffic_stats_t[AC_COUNT]` | `whd/src/include/whd_wlioctl.h:3291` |
| 68 | 32 | `rx` | `wl_traffic_stats_t[AC_COUNT]` | `whd/src/include/whd_wlioctl.h:3292` |
| 100 | 32 | `rx_failed` | `wl_traffic_stats_t[AC_COUNT]` | `whd/src/include/whd_wlioctl.h:3293` |
| 132 | 32 | `forward` | `wl_traffic_stats_t[AC_COUNT]` | `whd/src/include/whd_wlioctl.h:3294` |
| 164 | 32 | `tx_expired` | `wl_traffic_stats_t[AC_COUNT]` | `whd/src/include/whd_wlioctl.h:3295` |

Size check: compiled

### `wlc_ba_cnt_t` (whd)
Block-ack counters with a version and length header (inferred from the names) (struct tag `wlc_ba_cnt`), with no use site in whd outside the header and no command or named variable given for it there, and the name not found in linux, embassy, c-driver or pico-sdk; not packed (the header's first `#pragma pack(1)` is at line 3864, after the definition; alignment 4); 132 bytes; byte order not stated in the definition, little-endian as whd treats it (inferred: plain uintN_t types, and whd's htod16/htod32/dtoh16/dtoh32 are identity unless IL_BIGENDIAN is defined). `whd/src/include/whd_wlioctl.h:3303-3333` `whd/src/include/whd_wlioctl.h:3864` `whd/src/include/whd_endian.h:44-57`

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 2 | `version` | `uint16_t` | `whd/src/include/whd_wlioctl.h:3305`; WLC_BA_CNT_VERSION = 1 `whd/src/include/whd_wlioctl.h:3302` |
| 2 | 2 | `length` | `uint16_t` | `whd/src/include/whd_wlioctl.h:3306` |
| 4 | 4 | `txpdu` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3307` |
| 8 | 4 | `txsdu` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3308` |
| 12 | 4 | `txfc` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3309` |
| 16 | 4 | `txfci` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3310` |
| 20 | 4 | `txretrans` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3311` |
| 24 | 4 | `txbatimer` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3312` |
| 28 | 4 | `txdrop` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3313` |
| 32 | 4 | `txaddbareq` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3314` |
| 36 | 4 | `txaddbaresp` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3315` |
| 40 | 4 | `txdelba` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3316` |
| 44 | 4 | `txba` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3317` |
| 48 | 4 | `txbar` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3318` |
| 52 | 16 | `txpad` | `uint32_t[4]` | `whd/src/include/whd_wlioctl.h:3319` |
| 68 | 4 | `rxpdu` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3320` |
| 72 | 4 | `rxqed` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3321` |
| 76 | 4 | `rxdup` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3322` |
| 80 | 4 | `rxnobuf` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3323` |
| 84 | 4 | `rxaddbareq` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3324` |
| 88 | 4 | `rxaddbaresp` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3325` |
| 92 | 4 | `rxdelba` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3326` |
| 96 | 4 | `rxba` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3327` |
| 100 | 4 | `rxbar` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3328` |
| 104 | 4 | `rxinvba` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3329` |
| 108 | 4 | `rxbaholes` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3330` |
| 112 | 4 | `rxunexp` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3331` |
| 116 | 16 | `rxpad` | `uint32_t[4]` | `whd/src/include/whd_wlioctl.h:3332` |

Size check: compiled

### `struct ampdu_tid_control` (whd)
TID byte and enable byte, with no use site in whd outside the header and no command or named variable given for it there, and the name not found in linux, embassy, c-driver or pico-sdk; not packed (the header's first `#pragma pack(1)` is at line 3864, after the definition; alignment 1); 2 bytes; all fields are single bytes or byte arrays, so there is no byte order. `whd/src/include/whd_wlioctl.h:3334-3338` `whd/src/include/whd_wlioctl.h:3864`

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 1 | `tid` | `uint8_t` | `whd/src/include/whd_wlioctl.h:3336` |
| 1 | 1 | `enable` | `uint8_t` | `whd/src/include/whd_wlioctl.h:3337` |

Size check: compiled

### `struct wl_msglevel2` (whd)
Two 32-bit words, low and high, with no use site in whd outside the header and no command or named variable given for it there, and the name not found in linux, embassy, c-driver or pico-sdk; not packed (the header's first `#pragma pack(1)` is at line 3864, after the definition; alignment 4); 8 bytes; byte order not stated in the definition, little-endian as whd treats it (inferred: plain uintN_t types, and whd's htod16/htod32/dtoh16/dtoh32 are identity unless IL_BIGENDIAN is defined). `whd/src/include/whd_wlioctl.h:3339-3343` `whd/src/include/whd_wlioctl.h:3864` `whd/src/include/whd_endian.h:44-57`

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `low` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3341` |
| 4 | 4 | `high` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3342` |

Size check: compiled

### `struct ampdu_ea_tid` (whd)
Station address and TID byte, with no use site in whd outside the header and no command or named variable given for it there, and the name not found in linux, embassy, c-driver or pico-sdk; not packed (the header's first `#pragma pack(1)` is at line 3864, after the definition; alignment 1); 7 bytes; all fields are single bytes or byte arrays, so there is no byte order. `whd/src/include/whd_wlioctl.h:3344-3348` `whd/src/include/whd_wlioctl.h:3864`

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 6 | `ea` | `wl_ether_addr_t` | `whd/src/include/whd_wlioctl.h:3346` |
| 6 | 1 | `tid` | `uint8_t` | `whd/src/include/whd_wlioctl.h:3347` |

Size check: compiled

### `struct ampdu_retry_tid` (whd)
TID byte and retry byte, with no use site in whd outside the header and no command or named variable given for it there, and the name not found in linux, embassy, c-driver or pico-sdk; not packed (the header's first `#pragma pack(1)` is at line 3864, after the definition; alignment 1); 2 bytes; all fields are single bytes or byte arrays, so there is no byte order. `whd/src/include/whd_wlioctl.h:3349-3353` `whd/src/include/whd_wlioctl.h:3864`

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 1 | `tid` | `uint8_t` | `whd/src/include/whd_wlioctl.h:3351` |
| 1 | 1 | `retry` | `uint8_t` | `whd/src/include/whd_wlioctl.h:3352` |

Size check: compiled

### `struct ampdu_ba_sizes` (whd)
Block-ack transmit and receive window size bytes (inferred from the field names), with no use site in whd outside the header and no command or named variable given for it there, and the name not found in linux, embassy, c-driver or pico-sdk; not packed (the header's first `#pragma pack(1)` is at line 3864, after the definition; alignment 1); 2 bytes; all fields are single bytes or byte arrays, so there is no byte order. `whd/src/include/whd_wlioctl.h:3354-3358` `whd/src/include/whd_wlioctl.h:3864`

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 1 | `ba_tx_wsize` | `uint8_t` | `whd/src/include/whd_wlioctl.h:3356` |
| 1 | 1 | `ba_rx_wsize` | `uint8_t` | `whd/src/include/whd_wlioctl.h:3357` |

Size check: compiled

### `dpt_iovar_t` (whd)
Station address and mode byte, by its type name the argument of a named variable (inferred) (struct tag `dpt_iovar`), with no use site in whd outside the header and no command or named variable given for it there, and the name not found in linux, embassy, c-driver or pico-sdk; not packed (the header's first `#pragma pack(1)` is at line 3864, after the definition; alignment 4); 12 bytes; byte order not stated in the definition, little-endian as whd treats it (inferred: plain uintN_t types, and whd's htod16/htod32/dtoh16/dtoh32 are identity unless IL_BIGENDIAN is defined). `whd/src/include/whd_wlioctl.h:3370-3375` `whd/src/include/whd_wlioctl.h:3864` `whd/src/include/whd_endian.h:44-57`

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 6 | `ea` | `wl_ether_addr_t` | `whd/src/include/whd_wlioctl.h:3372` |
| 6 | 1 | `mode` | `uint8_t` | `whd/src/include/whd_wlioctl.h:3373`; mode values DPT_* at `whd/src/include/whd_wlioctl.h:3359-3369` |
| 7 | 1 | (pad) | `uint8_t[1]` | compiler alignment padding, not a declared member `whd/src/include/whd_wlioctl.h:3370-3375` |
| 8 | 4 | `pad` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3374`; a real declared member named 'pad' (not compiler padding) |

Size check: compiled

### `dpt_status_t` (whd)
Status entry: status flags, a name and its length, RSSI and an embedded `sta_info_t` (struct tag `dpt_status`), with no use site in whd outside the header and no command or named variable given for it there, and the name not found in linux, embassy, c-driver or pico-sdk; not packed (the header's first `#pragma pack(1)` is at line 3864, after the definition; alignment 4); 132 bytes; byte order not stated in the definition, little-endian as whd treats it (inferred: plain uintN_t types, and whd's htod16/htod32/dtoh16/dtoh32 are identity unless IL_BIGENDIAN is defined). `whd/src/include/whd_wlioctl.h:3380-3387` `whd/src/include/whd_wlioctl.h:3864` `whd/src/include/whd_endian.h:44-57`

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 1 | `status` | `uint8_t` | `whd/src/include/whd_wlioctl.h:3382`; flag values DPT_STATUS_* at `whd/src/include/whd_wlioctl.h:3376-3378` |
| 1 | 1 | `fnlen` | `uint8_t` | `whd/src/include/whd_wlioctl.h:3383` |
| 2 | 48 | `name` | `uint8_t[DPT_FNAME_LEN]` | `whd/src/include/whd_wlioctl.h:3384`; DPT_FNAME_LEN = 48 `whd/src/include/whd_wlioctl.h:3379` |
| 50 | 2 | (pad) | `uint8_t[2]` | compiler alignment padding, not a declared member `whd/src/include/whd_wlioctl.h:3380-3387` |
| 52 | 4 | `rssi` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3385` |
| 56 | 76 | `sta` | `sta_info_t` | `whd/src/include/whd_wlioctl.h:3386`; `sta_info_t` is defined at `whd/src/include/whd_wlioctl.h:942-959`, 76 bytes (compiled) |

Size check: compiled

### `dpt_list_t` (whd)
Count followed by `dpt_status_t` entries (struct tag `dpt_list`), with no use site in whd outside the header and no command or named variable given for it there, and the name not found in linux, embassy, c-driver or pico-sdk; not packed (the header's first `#pragma pack(1)` is at line 3864, after the definition; alignment 4); variable size: 4 fixed bytes plus a flexible tail (sizeof 136 as compiled); byte order not stated in the definition, little-endian as whd treats it (inferred: plain uintN_t types, and whd's htod16/htod32/dtoh16/dtoh32 are identity unless IL_BIGENDIAN is defined). `whd/src/include/whd_wlioctl.h:3388-3392` `whd/src/include/whd_wlioctl.h:3864` `whd/src/include/whd_endian.h:44-57`

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `num` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3390` |
| 4 | variable | `status` | `dpt_status_t[1]` | `whd/src/include/whd_wlioctl.h:3391`; flexible tail: status[1] is a one-element placeholder for num entries; 132 bytes in sizeof |

Size check: compiled

### `dpt_fname_t` (whd)
Length byte and 48-byte name (struct tag `dpt_fname`), with no use site in whd outside the header and no command or named variable given for it there, and the name not found in linux, embassy, c-driver or pico-sdk; not packed (the header's first `#pragma pack(1)` is at line 3864, after the definition; alignment 1); 49 bytes; all fields are single bytes or byte arrays, so there is no byte order. `whd/src/include/whd_wlioctl.h:3393-3397` `whd/src/include/whd_wlioctl.h:3864`

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 1 | `len` | `uint8_t` | `whd/src/include/whd_wlioctl.h:3395` |
| 1 | 48 | `name` | `uint8_t[DPT_FNAME_LEN]` | `whd/src/include/whd_wlioctl.h:3396`; DPT_FNAME_LEN = 48 `whd/src/include/whd_wlioctl.h:3379` |

Size check: compiled

### `bdd_fname_t` (whd)
Length byte and 32-byte name (struct tag `bdd_fname`), with no use site in whd outside the header and no command or named variable given for it there, and the name not found in linux, embassy, c-driver or pico-sdk; not packed (the header's first `#pragma pack(1)` is at line 3864, after the definition; alignment 1); 33 bytes; all fields are single bytes or byte arrays, so there is no byte order. `whd/src/include/whd_wlioctl.h:3399-3403` `whd/src/include/whd_wlioctl.h:3864`

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 1 | `len` | `uint8_t` | `whd/src/include/whd_wlioctl.h:3401` |
| 1 | 32 | `name` | `uint8_t[BDD_FNAME_LEN]` | `whd/src/include/whd_wlioctl.h:3402`; BDD_FNAME_LEN = 32 `whd/src/include/whd_wlioctl.h:3398` |

Size check: compiled

### `struct ts_list` (whd)
Count followed by `struct tsinfo_arg` entries, with no use site in whd outside the header and no command or named variable given for it there, and the name not found in linux, embassy, c-driver or pico-sdk; not packed (the header's first `#pragma pack(1)` is at line 3864, after the definition; alignment 4); variable size: 4 fixed bytes plus a flexible tail (sizeof 8 as compiled); byte order not stated in the definition, little-endian as whd treats it (inferred: plain uintN_t types, and whd's htod16/htod32/dtoh16/dtoh32 are identity unless IL_BIGENDIAN is defined). `whd/src/include/whd_wlioctl.h:3404-3408` `whd/src/include/whd_wlioctl.h:3864` `whd/src/include/whd_endian.h:44-57`

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `count` | `int32_t` | `whd/src/include/whd_wlioctl.h:3406` |
| 4 | variable | `tsinfo` | `struct tsinfo_arg[1]` | `whd/src/include/whd_wlioctl.h:3407`; flexible tail: tsinfo[1] is a one-element placeholder for count entries; 3 bytes in sizeof |
| 7 | 1 | (pad) | `uint8_t[1]` | trailing padding to struct alignment 4; position as counted by sizeof with the placeholder element `whd/src/include/whd_wlioctl.h:3404-3408` |

Size check: compiled

### `tspec_arg_t` (whd)
Traffic specification argument with a version and length header (inferred from the name) (struct tag `tspec_arg`), with no use site in whd outside the header and no command or named variable given for it there, and the name not found in linux, embassy, c-driver or pico-sdk; not packed (the header's first `#pragma pack(1)` is at line 3864, after the definition; alignment 4); 68 bytes; byte order not stated in the definition, little-endian as whd treats it (inferred: plain uintN_t types, and whd's htod16/htod32/dtoh16/dtoh32 are identity unless IL_BIGENDIAN is defined). `whd/src/include/whd_wlioctl.h:3409-3431` `whd/src/include/whd_wlioctl.h:3864` `whd/src/include/whd_endian.h:44-57`

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 2 | `version` | `uint16_t` | `whd/src/include/whd_wlioctl.h:3411`; TSPEC_ARG_VERSION = 2 `whd/src/include/whd_wlioctl.h:3442` |
| 2 | 2 | `length` | `uint16_t` | `whd/src/include/whd_wlioctl.h:3412`; TSPEC_ARG_LENGTH = 55 `whd/src/include/whd_wlioctl.h:3443`; sizeof is 68 and the member sizes without padding sum to 64, neither equal to 55, and the header does not say what the 55 counts; (computed) the members from tsinfo through medium_time, summed without padding, are 3 + 2 + 2 + 11*4 + 2 + 2 = 55 bytes, leaving version, length, flag (8 bytes) and dialog_token (1 byte) outside the count; whether that is what the constant means is not stated in these sources |
| 4 | 4 | `flag` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3413` |
| 8 | 3 | `tsinfo` | `struct tsinfo_arg` | `whd/src/include/whd_wlioctl.h:3414`; struct tsinfo_arg { uint8_t octets[3]; } `whd/src/include/whd_wlioctl.h:1973-1976` |
| 11 | 1 | (pad) | `uint8_t[1]` | compiler alignment padding, not a declared member `whd/src/include/whd_wlioctl.h:3409-3431` |
| 12 | 2 | `nom_msdu_size` | `uint16_t` | `whd/src/include/whd_wlioctl.h:3415` |
| 14 | 2 | `max_msdu_size` | `uint16_t` | `whd/src/include/whd_wlioctl.h:3416` |
| 16 | 4 | `min_srv_interval` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3417` |
| 20 | 4 | `max_srv_interval` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3418` |
| 24 | 4 | `inactivity_interval` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3419` |
| 28 | 4 | `suspension_interval` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3420` |
| 32 | 4 | `srv_start_time` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3421` |
| 36 | 4 | `min_data_rate` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3422` |
| 40 | 4 | `mean_data_rate` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3423` |
| 44 | 4 | `peak_data_rate` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3424` |
| 48 | 4 | `max_burst_size` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3425` |
| 52 | 4 | `delay_bound` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3426` |
| 56 | 4 | `min_phy_rate` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3427` |
| 60 | 2 | `surplus_bw` | `uint16_t` | `whd/src/include/whd_wlioctl.h:3428` |
| 62 | 2 | `medium_time` | `uint16_t` | `whd/src/include/whd_wlioctl.h:3429` |
| 64 | 1 | `dialog_token` | `uint8_t` | `whd/src/include/whd_wlioctl.h:3430` |
| 65 | 3 | (pad) | `uint8_t[3]` | trailing padding to struct alignment 4 `whd/src/include/whd_wlioctl.h:3409-3431` |

Size check: compiled

### `tspec_per_sta_arg_t` (whd)
Station address followed by a `struct tspec_arg` (struct tag `tspec_per_sta_arg`), with no use site in whd outside the header and no command or named variable given for it there, and the name not found in linux, embassy, c-driver or pico-sdk; not packed (the header's first `#pragma pack(1)` is at line 3864, after the definition; alignment 4); 76 bytes; byte order not stated in the definition, little-endian as whd treats it (inferred: plain uintN_t types, and whd's htod16/htod32/dtoh16/dtoh32 are identity unless IL_BIGENDIAN is defined). `whd/src/include/whd_wlioctl.h:3432-3436` `whd/src/include/whd_wlioctl.h:3864` `whd/src/include/whd_endian.h:44-57`

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 6 | `ea` | `wl_ether_addr_t` | `whd/src/include/whd_wlioctl.h:3434` |
| 6 | 2 | (pad) | `uint8_t[2]` | compiler alignment padding, not a declared member `whd/src/include/whd_wlioctl.h:3432-3436` |
| 8 | 68 | `ts` | `struct tspec_arg` | `whd/src/include/whd_wlioctl.h:3435` |

Size check: compiled

### `wme_max_bandwidth_t` (whd)
One 32-bit value per access category (struct tag `wme_max_bandwidth`), with no use site in whd outside the header and no command or named variable given for it there, and the name not found in linux, embassy, c-driver or pico-sdk; WL_WME_MBW_PARAMS_IO_BYTES = sizeof(wme_max_bandwidth_t) `whd/src/include/whd_wlioctl.h:3441` marks it as an I/O buffer (inferred), but the variable name is not given; not packed (the header's first `#pragma pack(1)` is at line 3864, after the definition; alignment 4); 16 bytes; byte order not stated in the definition, little-endian as whd treats it (inferred: plain uintN_t types, and whd's htod16/htod32/dtoh16/dtoh32 are identity unless IL_BIGENDIAN is defined). `whd/src/include/whd_wlioctl.h:3437-3440` `whd/src/include/whd_wlioctl.h:3864` `whd/src/include/whd_endian.h:44-57`

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 16 | `ac` | `uint32_t[AC_COUNT]` | `whd/src/include/whd_wlioctl.h:3439`; AC_COUNT = 4 `whd/src/include/whd_wlioctl.h:3285` |

Size check: compiled

### `wl_lifetime_t` (whd)
Access category and lifetime pair (struct tag `wl_lifetime`), with no use site in whd outside the header and no command or named variable given for it there, and the name not found in linux, embassy, c-driver or pico-sdk; not packed (the header's first `#pragma pack(1)` is at line 3864, after the definition; alignment 4); 8 bytes; byte order not stated in the definition, little-endian as whd treats it (inferred: plain uintN_t types, and whd's htod16/htod32/dtoh16/dtoh32 are identity unless IL_BIGENDIAN is defined). `whd/src/include/whd_wlioctl.h:3459-3463` `whd/src/include/whd_wlioctl.h:3864` `whd/src/include/whd_endian.h:44-57`

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `ac` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3461` |
| 4 | 4 | `lifetime` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3462`; WL_LIFETIME_MAX = 0xFFFF `whd/src/include/whd_wlioctl.h:3458` |

Size check: compiled

### `wl_chan_switch_t` (whd)
Channel switch request (struct tag `wl_chan_switch`): the value of the named variable "csa" (IOVAR_STR_CSA `whd/src/include/whd_wlioctl.h:1069`), set by whd_wifi_set_channel for the AP role with chspec written through htod16, count = 1, mode = 1 and reg = 0 `whd/src/whd_wifi_api.c:638-649`, and the event data of WLC_E_CSA_COMPLETE_IND, read with dtoh16(chspec) `whd/src/whd_wifi_api.c:1455-1460`; not packed (the header's first `#pragma pack(1)` is at line 3864, after the definition; alignment 2); 6 bytes; byte order not stated in the definition, little-endian as whd treats it (inferred: plain uintN_t types, and whd's htod16/htod32/dtoh16/dtoh32 are identity unless IL_BIGENDIAN is defined). `whd/src/include/whd_wlioctl.h:3464-3470` `whd/src/include/whd_wlioctl.h:3864` `whd/src/include/whd_endian.h:44-57`

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 1 | `mode` | `uint8_t` | `whd/src/include/whd_wlioctl.h:3466` |
| 1 | 1 | `count` | `uint8_t` | `whd/src/include/whd_wlioctl.h:3467` |
| 2 | 2 | `chspec` | `wl_chanspec_t` | `whd/src/include/whd_wlioctl.h:3468`; wl_chanspec_t = uint16_t `whd/inc/whd_types.h:918` |
| 4 | 1 | `reg` | `uint8_t` | `whd/src/include/whd_wlioctl.h:3469` |
| 5 | 1 | (pad) | `uint8_t[1]` | trailing padding to struct alignment 2 `whd/src/include/whd_wlioctl.h:3464-3470`; the event handler requires datalen >= sizeof = 6 `whd/src/whd_wifi_api.c:1456` |

Size check: compiled

### `wl_pfn_subnet_info_t` (whd)
BSSID, channel and SSID of a preferred-network (PFN) entry, commented 'PFN network info structure' at `whd/src/include/whd_wlioctl.h:3494` (struct tag `wl_pfn_subnet_info`), with no use site in whd outside the header and no command or named variable given for it there, and the name not found in linux, embassy, c-driver or pico-sdk; not packed (the header's first `#pragma pack(1)` is at line 3864, after the definition; alignment 1); 40 bytes; all fields are single bytes or byte arrays, so there is no byte order. `whd/src/include/whd_wlioctl.h:3495-3501` `whd/src/include/whd_wlioctl.h:3864`

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 6 | `BSSID` | `struct ether_addr` | `whd/src/include/whd_wlioctl.h:3497` |
| 6 | 1 | `channel` | `uint8_t` | `whd/src/include/whd_wlioctl.h:3498` |
| 7 | 1 | `SSID_len` | `uint8_t` | `whd/src/include/whd_wlioctl.h:3499` |
| 8 | 32 | `SSID` | `uint8_t[32]` | `whd/src/include/whd_wlioctl.h:3500` |

Size check: compiled

Differences: linux has no separate struct for this; the same four members are the first four members of struct brcmf_pno_net_info_le `linux/brcmfmac/fwil_types.h:1056-1060`.

### `wl_pfn_net_info_t` (whd)
`wl_pfn_subnet_info_t` followed by RSSI and timestamp (struct tag `wl_pfn_net_info`), with no use site in whd outside the header and no command or named variable given for it there, and the name not found in linux, embassy, c-driver or pico-sdk; not packed (the header's first `#pragma pack(1)` is at line 3864, after the definition; alignment 2); 44 bytes; byte order not stated in the definition, little-endian as whd treats it (inferred: plain uintN_t types, and whd's htod16/htod32/dtoh16/dtoh32 are identity unless IL_BIGENDIAN is defined). `whd/src/include/whd_wlioctl.h:3503-3508` `whd/src/include/whd_wlioctl.h:3864` `whd/src/include/whd_endian.h:44-57`

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 40 | `pfnsubnet` | `wl_pfn_subnet_info_t` | `whd/src/include/whd_wlioctl.h:3505` |
| 40 | 2 | `RSSI` | `int16_t` | `whd/src/include/whd_wlioctl.h:3506` |
| 42 | 2 | `timestamp` | `uint16_t` | `whd/src/include/whd_wlioctl.h:3507` |

Size check: compiled

Differences: linux struct brcmf_pno_net_info_le has the same members flattened `linux/brcmfmac/fwil_types.h:1056-1063`; linux reads an array of them after the 12-byte struct brcmf_pno_scanresults_le in the BRCMF_E_PFN_NET_FOUND event data `linux/brcmfmac/cfg80211.c:3881-3892` `linux/brcmfmac/cfg80211.c:3937` `linux/brcmfmac/cfg80211.c:7011-7012`.

### `wl_pfn_scanresult_t` (whd)
PFN scan result, commented as serving to report a single scan result, no more and no fewer, with the detailed scan information also reported in bss_info, at `whd/src/include/whd_wlioctl.h:3510-3511` (struct tag `wl_pfn_scanresult`), with no use site in whd outside the header and no command or named variable given for it there, and the name not found in linux, embassy, c-driver or pico-sdk; not packed (the header's first `#pragma pack(1)` is at line 3864, after the definition; alignment 4); variable size: 184 fixed bytes plus a flexible tail (sizeof 184 as compiled); byte order not stated in the definition, little-endian as whd treats it (inferred: plain uintN_t types, and whd's htod16/htod32/dtoh16/dtoh32 are identity unless IL_BIGENDIAN is defined). `whd/src/include/whd_wlioctl.h:3512-3519` `whd/src/include/whd_wlioctl.h:3864` `whd/src/include/whd_endian.h:44-57`

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `version` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3514` |
| 4 | 4 | `status` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3515` |
| 8 | 4 | `count` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3516` |
| 12 | 44 | `netinfo` | `wl_pfn_net_info_t` | `whd/src/include/whd_wlioctl.h:3517` |
| 56 | 128 + variable | `bss_info` | `wl_bss_info_t` | `whd/src/include/whd_wlioctl.h:3518`; flexible tail: wl_bss_info_t `whd/inc/whd_types.h:964` is itself followed by variable-length information elements per its own comments |

Size check: compiled

Differences: linux struct brcmf_pno_scanresults_le is only the first three members (version, status, count; `linux/brcmfmac/fwil_types.h:1072-1076`), described as the 'result returned in PNO NET FOUND event' `linux/brcmfmac/fwil_types.h:1066`, with count net-info entries appended `linux/brcmfmac/fwil_types.h:1070`; linux does not have the trailing bss_info member, so the whd single-result-plus-bss_info shape is not corroborated by another driver. `whd/src/include/whd_wlioctl.h:3512-3519`

### `wl_pfn_param_t` (whd)
PFN parameters, commented 'PFN data structure' at `whd/src/include/whd_wlioctl.h:3521` (struct tag `wl_pfn_param`), with no use site in whd outside the header and no command or named variable given for it there, and the name not found in linux, embassy, c-driver or pico-sdk; the PNO variable names "pfn", "pfn_add", "pfn_set" and "pfnclear" are defined at `whd/src/include/whd_wlioctl.h:1188-1191` but no code in these sources uses this record with them; not packed (the header's first `#pragma pack(1)` is at line 3864, after the definition; alignment 4); 24 bytes; byte order not stated in the definition, little-endian as whd treats it (inferred: plain uintN_t types, and whd's htod16/htod32/dtoh16/dtoh32 are identity unless IL_BIGENDIAN is defined). `whd/src/include/whd_wlioctl.h:3522-3544` `whd/src/include/whd_wlioctl.h:3864` `whd/src/include/whd_endian.h:44-57`

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `version` | `int32_t` | `whd/src/include/whd_wlioctl.h:3524`; PFN_VERSION = 2 `whd/src/include/whd_wlioctl.h:3492` |
| 4 | 4 | `scan_freq` | `int32_t` | `whd/src/include/whd_wlioctl.h:3525` |
| 8 | 4 | `lost_network_timeout` | `int32_t` | `whd/src/include/whd_wlioctl.h:3526` |
| 12 | 2 | `flags` | `int16_t` | `whd/src/include/whd_wlioctl.h:3529`; flag bit positions at `whd/src/include/whd_wlioctl.h:3479-3491` |
| 14 | 2 | `rssi_margin` | `int16_t` | `whd/src/include/whd_wlioctl.h:3533` |
| 16 | 1 | `bestn` | `uint8_t` | `whd/src/include/whd_wlioctl.h:3536` |
| 17 | 1 | `mscan` | `uint8_t` | `whd/src/include/whd_wlioctl.h:3537` |
| 18 | 1 | `repeat` | `uint8_t` | `whd/src/include/whd_wlioctl.h:3538` |
| 19 | 1 | `exp` | `uint8_t` | `whd/src/include/whd_wlioctl.h:3541` |
| 20 | 4 | `slow_freq` | `int32_t` | `whd/src/include/whd_wlioctl.h:3543` |

Size check: compiled

Differences: linux struct brcmf_pno_param_le has the same member list and order `linux/brcmfmac/fwil_types.h:999-1010`; whd declares the 32- and 16-bit members signed (int32_t, int16_t) where linux uses __le32 and __le16 `whd/src/include/whd_wlioctl.h:3524-3543`; linux's record is sent with the named variable "pfn_set" `linux/brcmfmac/pno.c:106` `linux/brcmfmac/pno.c:146`.

### `wl_pfn_bssid_t` (whd)
Address and flags pair for PFN (struct tag `wl_pfn_bssid`), with no use site in whd outside the header and no command or named variable given for it there, and the name not found in linux, embassy, c-driver or pico-sdk; not packed (the header's first `#pragma pack(1)` is at line 3864, after the definition; alignment 2); 8 bytes; byte order not stated in the definition, little-endian as whd treats it (inferred: plain uintN_t types, and whd's htod16/htod32/dtoh16/dtoh32 are identity unless IL_BIGENDIAN is defined). `whd/src/include/whd_wlioctl.h:3546-3551` `whd/src/include/whd_wlioctl.h:3864` `whd/src/include/whd_endian.h:44-57`

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 6 | `macaddr` | `struct ether_addr` | `whd/src/include/whd_wlioctl.h:3548` |
| 6 | 2 | `flags` | `uint16_t` | `whd/src/include/whd_wlioctl.h:3550`; comment at `whd/src/include/whd_wlioctl.h:3549`: Bit4 suppress_lost, Bit3 suppress_found |

Size check: compiled

Differences: linux struct brcmf_pno_bssid_le has the same two members in the same order, with the address named bssid where whd names it macaddr `linux/brcmfmac/fwil_types.h:1120-1123` `whd/src/include/whd_wlioctl.h:3548`, and is sent with the named variable "pfn_add_bssid" `linux/brcmfmac/pno.c:224` `linux/brcmfmac/pno.c:231`.

### `wl_pfn_cfg_t` (whd)
PFN configuration: report type, channel count, channel list and flags (struct tag `wl_pfn_cfg`), with no use site in whd outside the header and no command or named variable given for it there, and the name not found in linux, embassy, c-driver or pico-sdk; the PNO variable names "pfn", "pfn_add", "pfn_set" and "pfnclear" are defined at `whd/src/include/whd_wlioctl.h:1188-1191` but no code in these sources uses this record with them; not packed (the header's first `#pragma pack(1)` is at line 3864, after the definition; alignment 4); 140 bytes; byte order not stated in the definition, little-endian as whd treats it (inferred: plain uintN_t types, and whd's htod16/htod32/dtoh16/dtoh32 are identity unless IL_BIGENDIAN is defined). `whd/src/include/whd_wlioctl.h:3553-3559` `whd/src/include/whd_wlioctl.h:3864` `whd/src/include/whd_endian.h:44-57`

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `reporttype` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3555` |
| 4 | 4 | `channel_num` | `int32_t` | `whd/src/include/whd_wlioctl.h:3556` |
| 8 | 128 | `channel_list` | `uint16_t[WL_NUMCHANNELS]` | `whd/src/include/whd_wlioctl.h:3557`; WL_NUMCHANNELS = 64 `whd/src/include/whd_wlioctl.h:1927` |
| 136 | 4 | `flags` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3558` |

Size check: compiled

Differences: linux struct brcmf_pno_config_le has the same field list (`linux/brcmfmac/fwil_types.h:1020-1025`; BRCMF_NUMCHANNELS = 64 at `linux/brcmfmac/fwil_types.h:157`; whd declares channel_num as int32_t `whd/src/include/whd_wlioctl.h:3556`, linux as __le32) and is sent with the named variable "pfn_cfg" `linux/brcmfmac/pno.c:93-99`. whd itself does not define or use a "pfn_cfg" name. `whd/src/include/whd_wlioctl.h:3553-3559`

### `wl_pfn_t` (whd)
PFN network entry: SSID and security settings (struct tag `wl_pfn`), with no use site in whd outside the header and no command or named variable given for it there, and the name not found in linux, embassy, c-driver or pico-sdk; not packed (the header's first `#pragma pack(1)` is at line 3864, after the definition; alignment 4); 56 bytes; byte order not stated in the definition, little-endian as whd treats it (inferred: plain uintN_t types, and whd's htod16/htod32/dtoh16/dtoh32 are identity unless IL_BIGENDIAN is defined). `whd/src/include/whd_wlioctl.h:3565-3573` `whd/src/include/whd_wlioctl.h:3864` `whd/src/include/whd_endian.h:44-57`

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 36 | `ssid` | `wlc_ssid_t` | `whd/src/include/whd_wlioctl.h:3567`; `wlc_ssid_t` is uint32 SSID_len plus 32 bytes `whd/src/include/whd_wlioctl.h:496-500` |
| 36 | 4 | `flags` | `int32_t` | `whd/src/include/whd_wlioctl.h:3568`; masks WL_PFN_HIDDEN_MASK 0x4 and WL_PFN_SUPPRESSLOST_MASK 0x10 `whd/src/include/whd_wlioctl.h:3562-3563` |
| 40 | 4 | `infra` | `int32_t` | `whd/src/include/whd_wlioctl.h:3569` |
| 44 | 4 | `auth` | `int32_t` | `whd/src/include/whd_wlioctl.h:3570` |
| 48 | 4 | `wpa_auth` | `int32_t` | `whd/src/include/whd_wlioctl.h:3571` |
| 52 | 4 | `wsec` | `int32_t` | `whd/src/include/whd_wlioctl.h:3572` |

Size check: compiled

Differences: linux struct brcmf_pno_net_param_le has the same member list and order `linux/brcmfmac/fwil_types.h:1037-1044`; whd declares flags, infra, auth, wpa_auth and wsec as int32_t where linux uses __le32 `whd/src/include/whd_wlioctl.h:3568-3572`; linux's record is sent with the named variable "pfn_add" `linux/brcmfmac/pno.c:201` `linux/brcmfmac/pno.c:215`.

### `struct toe_ol_stats_t` (whd)
Nineteen 32-bit checksum-offload counters (inferred from the names), with no use site in whd outside the header and no command or named variable given for it there, and the name not found in linux, embassy, c-driver or pico-sdk; not packed (the header's first `#pragma pack(1)` is at line 3864, after the definition; alignment 4); 76 bytes; byte order not stated in the definition, little-endian as whd treats it (inferred: plain uintN_t types, and whd's htod16/htod32/dtoh16/dtoh32 are identity unless IL_BIGENDIAN is defined). `whd/src/include/whd_wlioctl.h:3580-3601` `whd/src/include/whd_wlioctl.h:3864` `whd/src/include/whd_endian.h:44-57`

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `tx_summed` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3582` |
| 4 | 4 | `tx_iph_fill` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3583` |
| 8 | 4 | `tx_tcp_fill` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3584` |
| 12 | 4 | `tx_udp_fill` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3585` |
| 16 | 4 | `tx_icmp_fill` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3586` |
| 20 | 4 | `rx_iph_good` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3587` |
| 24 | 4 | `rx_iph_bad` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3588` |
| 28 | 4 | `rx_tcp_good` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3589` |
| 32 | 4 | `rx_tcp_bad` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3590` |
| 36 | 4 | `rx_udp_good` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3591` |
| 40 | 4 | `rx_udp_bad` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3592` |
| 44 | 4 | `rx_icmp_good` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3593` |
| 48 | 4 | `rx_icmp_bad` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3594` |
| 52 | 4 | `tx_tcp_errinj` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3595` |
| 56 | 4 | `tx_udp_errinj` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3596` |
| 60 | 4 | `tx_icmp_errinj` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3597` |
| 64 | 4 | `rx_tcp_errinj` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3598` |
| 68 | 4 | `rx_udp_errinj` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3599` |
| 72 | 4 | `rx_icmp_errinj` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3600` |

Size check: compiled

### `arp_ol_stats_t` (whd)
ARP offload statistics (struct tag `arp_ol_stats`): the value read from the named variable "arp_stats" (IOVAR_STR_ARP_STATS `whd/src/include/whd_wlioctl.h:1262`) at `whd/src/whd_wifi_api.c:5788` and `whd/src/whd_wifi_api.c:5843-5844`, also embedded in the host-side struct whd_arp_stats_s at `whd/src/include/whd_wlioctl.h:4285`; not packed (the header's first `#pragma pack(1)` is at line 3864, after the definition; alignment 4); 48 bytes; byte order not stated in the definition, little-endian as whd treats it (inferred: plain uintN_t types, and whd's htod16/htod32/dtoh16/dtoh32 are identity unless IL_BIGENDIAN is defined). `whd/src/include/whd_wlioctl.h:3609-3623` `whd/src/include/whd_wlioctl.h:3864` `whd/src/include/whd_endian.h:44-57`

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `host_ip_entries` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3611` |
| 4 | 4 | `host_ip_overflow` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3612` |
| 8 | 4 | `arp_table_entries` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3613` |
| 12 | 4 | `arp_table_overflow` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3614` |
| 16 | 4 | `host_request` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3615` |
| 20 | 4 | `host_reply` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3616` |
| 24 | 4 | `host_service` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3617` |
| 28 | 4 | `peer_request` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3618` |
| 32 | 4 | `peer_request_drop` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3619` |
| 36 | 4 | `peer_reply` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3620` |
| 40 | 4 | `peer_reply_drop` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3621` |
| 44 | 4 | `peer_service` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3622` |

Size check: compiled

### `wl_keep_alive_pkt_t` (whd)
Keep-alive packet description (struct tag `wl_keep_alive_pkt`): the value of the named variable "keep_alive" (IOVAR_STR_KEEPALIVE_CONFIG `whd/src/include/whd_wlioctl.h:1273`), set by whd_wifi_keepalive_config `whd/src/whd_wifi_api.c:1029-1049`, where the NULL keep-alive sends sizeof = 8 zeroed bytes with only period_msec set and the NAT keep-alive sends 2*len_bytes + WL_KEEP_ALIVE_FIXED_LEN bytes `whd/src/whd_wifi_api.c:1040` with the data copied at offset 6; not packed (the header's first `#pragma pack(1)` is at line 3864, after the definition; alignment 4); variable size: 6 fixed bytes plus a flexible tail (sizeof 8 as compiled); byte order not stated in the definition, little-endian as whd treats it (inferred: plain uintN_t types, and whd's htod16/htod32/dtoh16/dtoh32 are identity unless IL_BIGENDIAN is defined). `whd/src/include/whd_wlioctl.h:3624-3629` `whd/src/include/whd_wlioctl.h:3864` `whd/src/include/whd_endian.h:44-57`

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `period_msec` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3626`; period_msec and len_bytes are stored without htod32/htod16 at the use site `whd/src/whd_wifi_api.c:1034` `whd/src/whd_wifi_api.c:1044-1045` |
| 4 | 2 | `len_bytes` | `uint16_t` | `whd/src/include/whd_wlioctl.h:3627` |
| 6 | variable | `data` | `uint8_t[1]` | `whd/src/include/whd_wlioctl.h:3628`; flexible tail: data[1] is a placeholder for len_bytes bytes; fixed part is WL_KEEP_ALIVE_FIXED_LEN = offsetof(data) = 6 `whd/src/include/whd_wlioctl.h:3630`; 1 byte in sizeof; WL_KEEP_ALIVE_FIXED_LEN is defined twice with the same text, at `whd/src/include/whd_wlioctl.h:46` and `whd/src/include/whd_wlioctl.h:3630`; the NAT path allocates 2*len_bytes + 6, twice the data length, though only len_bytes bytes are copied `whd/src/whd_wifi_api.c:1040-1046` |
| 7 | 1 | (pad) | `uint8_t[1]` | trailing padding to struct alignment 4; position as counted by sizeof with the placeholder element `whd/src/include/whd_wlioctl.h:3624-3629`; sizeof is 8 because of this byte, but the fixed length used on the wire is 6 (offsetof data) |

Size check: compiled

### `wl_pkt_filter_pattern_t` (whd)
Packet filter pattern (struct tag `wl_pkt_filter_pattern`): member u.pattern of `wl_pkt_filter_t` `whd/src/include/whd_wlioctl.h:3649`, written for the named variable "pkt_filter_add" at `whd/src/whd_wifi_api.c:6014-6021` and read from the "pkt_filter_list" reply at `whd/src/whd_wifi_api.c:6113-6115`; not packed (the header's first `#pragma pack(1)` is at line 3864, after the definition; alignment 4); variable size: 8 fixed bytes plus a flexible tail (sizeof 12 as compiled); byte order not stated in the definition, little-endian as whd treats it (inferred: plain uintN_t types, and whd's htod16/htod32/dtoh16/dtoh32 are identity unless IL_BIGENDIAN is defined). `whd/src/include/whd_wlioctl.h:3636-3641` `whd/src/include/whd_wlioctl.h:3864` `whd/src/include/whd_endian.h:44-57`

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `offset` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3638` |
| 4 | 4 | `size_bytes` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3639` |
| 8 | variable | `mask_and_pattern` | `uint8_t[1]` | `whd/src/include/whd_wlioctl.h:3640`; flexible tail: mask_and_pattern[1] is a placeholder: size_bytes of mask followed by size_bytes of pattern; fixed part WL_PKT_FILTER_PATTERN_FIXED_LEN = 8 `whd/src/include/whd_wlioctl.h:3653`; 1 byte in sizeof |
| 9 | 3 | (pad) | `uint8_t[3]` | trailing padding to struct alignment 4; position as counted by sizeof with the placeholder element `whd/src/include/whd_wlioctl.h:3636-3641` |

Size check: compiled

Differences: linux has the same three members in struct brcmf_pkt_filter_pattern_le `linux/brcmfmac/fwil_types.h:279-292`.

### `wl_pkt_filter_t` (whd)
Packet filter definition (struct tag `wl_pkt_filter`): the value of the named variable "pkt_filter_add" (IOVAR_STR_PKT_FILTER_ADD `whd/src/include/whd_wlioctl.h:1092`), set by whd_pf_add_packet_filter `whd/src/whd_wifi_api.c:5996-6021` with buffer length 2*mask_size + WL_PKT_FILTER_FIXED_LEN + WL_PKT_FILTER_PATTERN_FIXED_LEN `whd/src/whd_wifi_api.c:6000`, type written as 0, and the mask then the pattern (each mask_size bytes) copied into u.pattern.mask_and_pattern, and also the element type of the "pkt_filter_list" reply `whd/src/whd_wifi_api.c:6105-6131`; not packed (the header's first `#pragma pack(1)` is at line 3864, after the definition; alignment 4); variable size: 20 fixed bytes plus a flexible tail (sizeof 24 as compiled); byte order not stated in the definition, little-endian as whd treats it (inferred: plain uintN_t types, and whd's htod16/htod32/dtoh16/dtoh32 are identity unless IL_BIGENDIAN is defined). `whd/src/include/whd_wlioctl.h:3642-3651` `whd/src/include/whd_wlioctl.h:3864` `whd/src/include/whd_endian.h:44-57`

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `id` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3644` |
| 4 | 4 | `type` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3645` |
| 8 | 4 | `negate_match` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3646`; whd fills it from settings->rule `whd/src/whd_wifi_api.c:6013` |
| 12 | 8 + variable | `u` | `union { wl_pkt_filter_pattern_t pattern; }` | `whd/src/include/whd_wlioctl.h:3650`; flexible tail: union with the single alternative wl_pkt_filter_pattern_t pattern; ends in the flexible mask_and_pattern tail. WL_PKT_FILTER_FIXED_LEN = offsetof(u) = 12 `whd/src/include/whd_wlioctl.h:3652`; fixed header before the mask is 12 + 8 = 20; 12 bytes in sizeof; whd copies settings->mask_size bytes for both the mask and the pattern `whd/src/whd_wifi_api.c:6018-6021` |

Size check: compiled

Differences: linux's counterpart is struct brcmf_pkt_filter_le, commented 'IOVAR "pkt_filter_add" parameter' `linux/brcmfmac/fwil_types.h:294-302`.

### `wl_pkt_filter_enable_t` (whd)
Packet filter enable switch (struct tag `wl_pkt_filter_enable`): the value of the named variable "pkt_filter_enable" (IOVAR_STR_PKT_FILTER_ENABLE `whd/src/include/whd_wlioctl.h:1094`), set at `whd/src/whd_wifi_api.c:5967-5979`; not packed (the header's first `#pragma pack(1)` is at line 3864, after the definition; alignment 4); 8 bytes; byte order not stated in the definition, little-endian as whd treats it (inferred: plain uintN_t types, and whd's htod16/htod32/dtoh16/dtoh32 are identity unless IL_BIGENDIAN is defined). `whd/src/include/whd_wlioctl.h:3654-3658` `whd/src/include/whd_wlioctl.h:3864` `whd/src/include/whd_endian.h:44-57`

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `id` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3656`; under PROTO_MSGBUF id and enable are filled by memcpy of sizeof(filter_id) and sizeof(enable) bytes from the caller's variables `whd/src/whd_wifi_api.c:5975-5976`; filter_id is uint8_t `whd/src/whd_wifi_api.c:5959`, so fewer than 4 bytes of id are written on that path |
| 4 | 4 | `enable` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3657`; the source variable is whd_bool_t, a uint8_t or an enum depending on the compiler `whd/inc/whd_types.h:276-281` |

Size check: compiled

Differences: linux's counterpart is struct brcmf_pkt_filter_enable_le, commented 'IOVAR "pkt_filter_enable" parameter' `linux/brcmfmac/fwil_types.h:304-308`.

### `wl_pkt_filter_list_t` (whd)
Packet filter list (struct tag `wl_pkt_filter_list`): the reply of the named variable "pkt_filter_list" (IOVAR_STR_PKT_FILTER_LIST `whd/src/include/whd_wlioctl.h:1096`) `whd/src/whd_wifi_api.c:6098-6131`, whose request is one uint32 (0 = disabled list, 1 = enabled list) `whd/src/whd_wifi_api.c:6101`; not packed (the header's first `#pragma pack(1)` is at line 3864, after the definition; alignment 4); variable size: 4 fixed bytes plus a flexible tail (sizeof 28 as compiled); byte order not stated in the definition, little-endian as whd treats it (inferred: plain uintN_t types, and whd's htod16/htod32/dtoh16/dtoh32 are identity unless IL_BIGENDIAN is defined). `whd/src/include/whd_wlioctl.h:3659-3663` `whd/src/include/whd_wlioctl.h:3864` `whd/src/include/whd_endian.h:44-57`

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `num` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3661` |
| 4 | variable | `filter` | `wl_pkt_filter_t[1]` | `whd/src/include/whd_wlioctl.h:3662`; flexible tail: filter[1] is a placeholder for num variable-length wl_pkt_filter_t entries; WL_PKT_FILTER_LIST_FIXED_LEN = 4 `whd/src/include/whd_wlioctl.h:3664`; 24 bytes in sizeof; whd walks the entries by adding WL_PKT_FILTER_FIXED_LEN + WL_PKT_FILTER_PATTERN_FIXED_LEN + 2*size_bytes and rounding up to 4 (whd comment: "WLAN returns word-aligned filter list") `whd/src/whd_wifi_api.c:6130-6131` |

Size check: compiled

### `wl_pkt_filter_stats_t` (whd)
Packet filter statistics (struct tag `wl_pkt_filter_stats`; public alias whd_pkt_filter_stats_t `whd/inc/whd_types.h:144`): the reply of the named variable "pkt_filter_stats" (IOVAR_STR_PKT_FILTER_STATS `whd/src/include/whd_wlioctl.h:1097`) `whd/src/whd_wifi_api.c:6054-6065`, where the request buffer is a uint32 filter id followed by space for this record and the reply is copied out as this record from offset 0; not packed (the header's first `#pragma pack(1)` is at line 3864, after the definition; alignment 4); 12 bytes; byte order not stated in the definition, little-endian as whd treats it (inferred: plain uintN_t types, and whd's htod16/htod32/dtoh16/dtoh32 are identity unless IL_BIGENDIAN is defined). `whd/src/include/whd_wlioctl.h:3665-3670` `whd/src/include/whd_wlioctl.h:3864` `whd/src/include/whd_endian.h:44-57`

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `num_pkts_matched` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3667` |
| 4 | 4 | `num_pkts_forwarded` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3668` |
| 8 | 4 | `num_pkts_discarded` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3669` |

Size check: compiled

### `wl_seq_cmd_ioctl_t` (whd)
Command number and length pair (struct tag `wl_seq_cmd_ioctl`), with no use site in whd outside the header and no command or named variable given for it there, and the name not found in linux, embassy, c-driver or pico-sdk; not packed (the header's first `#pragma pack(1)` is at line 3864, after the definition; alignment 4); 8 bytes; byte order not stated in the definition, little-endian as whd treats it (inferred: plain uintN_t types, and whd's htod16/htod32/dtoh16/dtoh32 are identity unless IL_BIGENDIAN is defined). `whd/src/include/whd_wlioctl.h:3671-3675` `whd/src/include/whd_wlioctl.h:3864` `whd/src/include/whd_endian.h:44-57`

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `cmd` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3673` |
| 4 | 4 | `len` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3674`; WL_SEQ_CMD_ALIGN_BYTES = 4 `whd/src/include/whd_wlioctl.h:3676` |

Size check: compiled

### `wl_pkteng_t` (whd)
Packet engine parameters: flags, delay, frame count, length, sequence number, destination and source addresses (struct tag `wl_pkteng`), with no use site in whd outside the header and no command or named variable given for it there, and the name not found in linux, embassy, c-driver or pico-sdk; not packed (the header's first `#pragma pack(1)` is at line 3864, after the definition; alignment 4); 32 bytes; byte order not stated in the definition, little-endian as whd treats it (inferred: plain uintN_t types, and whd's htod16/htod32/dtoh16/dtoh32 are identity unless IL_BIGENDIAN is defined). `whd/src/include/whd_wlioctl.h:3690-3699` `whd/src/include/whd_wlioctl.h:3864` `whd/src/include/whd_endian.h:44-57`

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `flags` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3692`; flag values WL_PKTENG_PER_* at `whd/src/include/whd_wlioctl.h:3682-3689` |
| 4 | 4 | `delay` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3693` |
| 8 | 4 | `nframes` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3694` |
| 12 | 4 | `length` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3695` |
| 16 | 1 | `seqno` | `uint8_t` | `whd/src/include/whd_wlioctl.h:3696` |
| 17 | 6 | `dest` | `wl_ether_addr_t` | `whd/src/include/whd_wlioctl.h:3697` |
| 23 | 6 | `src` | `wl_ether_addr_t` | `whd/src/include/whd_wlioctl.h:3698` |
| 29 | 3 | (pad) | `uint8_t[3]` | trailing padding to struct alignment 4 `whd/src/include/whd_wlioctl.h:3690-3699` |

Size check: compiled

Differences: whd's include_helium copy of the header declares two more members after src (uint8 sweep_steps; uint8 PAD[2]) `whd/src/include_helium/whd_wlioctl.h:3849-3860`; the table above is the src/include definition `whd/src/include/whd_wlioctl.h:3690-3699`.

### `wl_pkteng_stats_t` (whd)
Packet engine statistics: lost frame count, RSSI, SNR and per-rate receive packet counts (struct tag `wl_pkteng_stats`), with no use site in whd outside the header and no command or named variable given for it there, and the name not found in linux, embassy, c-driver or pico-sdk; not packed (the header's first `#pragma pack(1)` is at line 3864, after the definition; alignment 4); 104 bytes; byte order not stated in the definition, little-endian as whd treats it (inferred: plain uintN_t types, and whd's htod16/htod32/dtoh16/dtoh32 are identity unless IL_BIGENDIAN is defined). `whd/src/include/whd_wlioctl.h:3704-3710` `whd/src/include/whd_wlioctl.h:3864` `whd/src/include/whd_endian.h:44-57`

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `lostfrmcnt` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3706` |
| 4 | 4 | `rssi` | `int32_t` | `whd/src/include/whd_wlioctl.h:3707` |
| 8 | 4 | `snr` | `int32_t` | `whd/src/include/whd_wlioctl.h:3708` |
| 12 | 90 | `rxpktcnt` | `uint16_t[NUM_80211_RATES + 1]` | `whd/src/include/whd_wlioctl.h:3709`; NUM_80211_RATES = 4 + 8 + 32 = 44 `whd/src/include/whd_wlioctl.h:3700-3703`, so the array has 45 entries |
| 102 | 2 | (pad) | `uint8_t[2]` | trailing padding to struct alignment 4 `whd/src/include/whd_wlioctl.h:3704-3710` |

Size check: compiled

Differences: whd's include_helium copy of the header uses plain int for rssi and snr and appends rssi_qdb, version, length, pad, rssi_per_core[WL_RSSI_ANT_MAX] and rssi_per_core_qdb[WL_RSSI_ANT_MAX] `whd/src/include_helium/whd_wlioctl.h:3865-3877`; the table above is the src/include definition `whd/src/include/whd_wlioctl.h:3704-3710`.

### `wl_sslpnphy_papd_debug_data_t` (whd)
SSLPN PHY PAPD debug data (name only; the header has no comment) (struct tag `wl_sslpnphy_papd_debug_data`), with no use site in whd outside the header and no command or named variable given for it there, and the name not found in linux, embassy, c-driver or pico-sdk; not packed (the header's first `#pragma pack(1)` is at line 3864, after the definition; alignment 4); 16 bytes; byte order not stated in the definition, little-endian as whd treats it (inferred: plain uintN_t types, and whd's htod16/htod32/dtoh16/dtoh32 are identity unless IL_BIGENDIAN is defined). `whd/src/include/whd_wlioctl.h:3711-3720` `whd/src/include/whd_wlioctl.h:3864` `whd/src/include/whd_endian.h:44-57`

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 1 | `psat_pwr` | `uint8_t` | `whd/src/include/whd_wlioctl.h:3713` |
| 1 | 1 | `psat_indx` | `uint8_t` | `whd/src/include/whd_wlioctl.h:3714` |
| 2 | 1 | `final_idx` | `uint8_t` | `whd/src/include/whd_wlioctl.h:3715` |
| 3 | 1 | `start_idx` | `uint8_t` | `whd/src/include/whd_wlioctl.h:3716` |
| 4 | 4 | `min_phase` | `int32_t` | `whd/src/include/whd_wlioctl.h:3717` |
| 8 | 4 | `voltage` | `int32_t` | `whd/src/include/whd_wlioctl.h:3718` |
| 12 | 1 | `temperature` | `int8_t` | `whd/src/include/whd_wlioctl.h:3719` |
| 13 | 3 | (pad) | `uint8_t[3]` | trailing padding to struct alignment 4 `whd/src/include/whd_wlioctl.h:3711-3720` |

Size check: compiled

### `wl_sslpnphy_debug_data_t` (whd)
SSLPN PHY debug data: two arrays of 64 16-bit values, papdcompRe and papdcompIm (struct tag `wl_sslpnphy_debug_data`), with no use site in whd outside the header and no command or named variable given for it there, and the name not found in linux, embassy, c-driver or pico-sdk; not packed (the header's first `#pragma pack(1)` is at line 3864, after the definition; alignment 2); 256 bytes; byte order not stated in the definition, little-endian as whd treats it (inferred: plain uintN_t types, and whd's htod16/htod32/dtoh16/dtoh32 are identity unless IL_BIGENDIAN is defined). `whd/src/include/whd_wlioctl.h:3721-3725` `whd/src/include/whd_wlioctl.h:3864` `whd/src/include/whd_endian.h:44-57`

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 128 | `papdcompRe` | `int16_t[64]` | `whd/src/include/whd_wlioctl.h:3723` |
| 128 | 128 | `papdcompIm` | `int16_t[64]` | `whd/src/include/whd_wlioctl.h:3724` |

Size check: compiled

### `wl_sslpnphy_spbdump_data_t` (whd)
SSLPN PHY dump data: a table length and two arrays of 256 16-bit values, spbreal and spbimg (struct tag `wl_sslpnphy_spbdump_data`), with no use site in whd outside the header and no command or named variable given for it there, and the name not found in linux, embassy, c-driver or pico-sdk; not packed (the header's first `#pragma pack(1)` is at line 3864, after the definition; alignment 2); 1026 bytes; byte order not stated in the definition, little-endian as whd treats it (inferred: plain uintN_t types, and whd's htod16/htod32/dtoh16/dtoh32 are identity unless IL_BIGENDIAN is defined). `whd/src/include/whd_wlioctl.h:3726-3731` `whd/src/include/whd_wlioctl.h:3864` `whd/src/include/whd_endian.h:44-57`

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 2 | `tbl_length` | `uint16_t` | `whd/src/include/whd_wlioctl.h:3728` |
| 2 | 512 | `spbreal` | `int16_t[256]` | `whd/src/include/whd_wlioctl.h:3729` |
| 514 | 512 | `spbimg` | `int16_t[256]` | `whd/src/include/whd_wlioctl.h:3730` |

Size check: compiled

### `wl_sslpnphy_percal_debug_data_t` (whd)
SSLPN PHY periodic-calibration debug data (inferred from the name; the header has no comment) (struct tag `wl_sslpnphy_percal_debug_data`), with no use site in whd outside the header and no command or named variable given for it there, and the name not found in linux, embassy, c-driver or pico-sdk; not packed (the header's first `#pragma pack(1)` is at line 3864, after the definition; alignment 4); 48 bytes; byte order not stated in the definition, little-endian as whd treats it (inferred: plain uintN_t types, and whd's htod16/htod32/dtoh16/dtoh32 are identity unless IL_BIGENDIAN is defined). `whd/src/include/whd_wlioctl.h:3732-3746` `whd/src/include/whd_wlioctl.h:3864` `whd/src/include/whd_endian.h:44-57`

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `cur_idx` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3734` |
| 4 | 4 | `tx_drift` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3735` |
| 8 | 1 | `prev_cal_idx` | `uint8_t` | `whd/src/include/whd_wlioctl.h:3736` |
| 9 | 3 | (pad) | `uint8_t[3]` | compiler alignment padding, not a declared member `whd/src/include/whd_wlioctl.h:3732-3746` |
| 12 | 4 | `percal_ctr` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3737` |
| 16 | 4 | `nxt_cal_idx` | `int32_t` | `whd/src/include/whd_wlioctl.h:3738` |
| 20 | 4 | `force_1idxcal` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3739` |
| 24 | 4 | `onedxacl_req` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3740` |
| 28 | 4 | `last_cal_volt` | `int32_t` | `whd/src/include/whd_wlioctl.h:3741` |
| 32 | 1 | `last_cal_temp` | `int8_t` | `whd/src/include/whd_wlioctl.h:3742` |
| 33 | 3 | (pad) | `uint8_t[3]` | compiler alignment padding, not a declared member `whd/src/include/whd_wlioctl.h:3732-3746` |
| 36 | 4 | `vbat_ripple` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3743` |
| 40 | 4 | `exit_route` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3744` |
| 44 | 4 | `volt_winner` | `int32_t` | `whd/src/include/whd_wlioctl.h:3745` |

Size check: compiled

### `wl_wowl_pattern_t` (whd)
Wake-on-wireless pattern (struct tag `wl_wowl_pattern`): the value of the named variable "wowl_pattern" (IOVAR_STR_WOWL_PATTERN `whd/src/include/whd_wlioctl.h:1177`), set at `whd/src/whd_wifi_api.c:6673-6711` as the operation string ("add"/"del"/"clr") plus one byte that whd skips without writing (strncpy of strlen bytes, then advance by strlen + 1 `whd/src/whd_wifi_api.c:6681-6682`), then this record, then masksize bytes of mask, then patternsize bytes of pattern, and also the element of the get reply `whd/src/whd_wifi_api.c:6733-6741`; not packed (the header's first `#pragma pack(1)` is at line 3864, after the definition; alignment 4); variable size: 28 fixed bytes plus the mask and pattern bytes that follow the struct (sizeof 28 as compiled); byte order not stated in the definition, little-endian as whd treats it (inferred: plain uintN_t types, and whd's htod16/htod32/dtoh16/dtoh32 are identity unless IL_BIGENDIAN is defined). `whd/src/include/whd_wlioctl.h:3770-3781` `whd/src/include/whd_wlioctl.h:3864` `whd/src/include/whd_endian.h:44-57`

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `masksize` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3772`; no htod32 is applied to any member; under PROTO_MSGBUF the record is built in a local copy and memcpy'd `whd/src/whd_wifi_api.c:6688-6696` |
| 4 | 4 | `offset` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3773` |
| 8 | 4 | `patternoffset` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3774`; whd writes sizeof(wl_wowl_pattern_t) + mask_size `whd/src/whd_wifi_api.c:6701` |
| 12 | 4 | `patternsize` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3775` |
| 16 | 4 | `id` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3776` |
| 20 | 4 | `reasonsize` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3777` |
| 24 | 4 | `type` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3778`; pattern types enum wowl_pattern_type_t at `whd/src/include/whd_wlioctl.h:3763-3768` |
| 28 | variable | (mask, then pattern) | `uint8_t[]` | not a declared member: masksize bytes of mask follow the struct, then patternsize bytes of pattern at patternoffset from the start `whd/src/include/whd_wlioctl.h:3779-3780`; for "clr" the record, mask and pattern bytes are still allocated but not written `whd/src/whd_wifi_api.c:6686-6712` |

Size check: compiled

Differences: linux's counterpart is struct brcmf_fil_wowl_pattern_le `linux/brcmfmac/fwil_types.h:738-749` has the same seven __le32 members preceded by u8 cmd[4] ("add"/"del"/"clr" plus NUL), sent with the named variable "wowl_pattern" `linux/brcmfmac/cfg80211.c:4046-4078`; linux sets patternoffset = sizeof(*filter) - sizeof(filter->cmd) + masksize `linux/brcmfmac/cfg80211.c:4058`, i.e. 28 + masksize counted from the masksize member (comment at `linux/brcmfmac/fwil_types.h:732`), the same value whd writes as sizeof(wl_wowl_pattern_t) + mask_size. `whd/src/include/whd_wlioctl.h:3770-3781`

### `wl_wowl_pattern_list_t` (whd)
Wake-on-wireless pattern list (struct tag `wl_wowl_pattern_list`): the reply of the named variable "wowl_pattern" get `whd/src/whd_wifi_api.c:6730-6741`, a count followed by count entries each of sizeof(wl_wowl_pattern_t) + masksize + patternsize bytes; not packed (the header's first `#pragma pack(1)` is at line 3864, after the definition; alignment 4); variable size: 4 fixed bytes plus a flexible tail (sizeof 32 as compiled); byte order not stated in the definition, little-endian as whd treats it (inferred: plain uintN_t types, and whd's htod16/htod32/dtoh16/dtoh32 are identity unless IL_BIGENDIAN is defined). `whd/src/include/whd_wlioctl.h:3783-3787` `whd/src/include/whd_wlioctl.h:3864` `whd/src/include/whd_endian.h:44-57`

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `count` | `uint32_t` | `whd/src/include/whd_wlioctl.h:3785` |
| 4 | variable | `pattern` | `wl_wowl_pattern_t[1]` | `whd/src/include/whd_wlioctl.h:3786`; flexible tail: pattern[1] is a placeholder for count variable-length entries (struct + mask + pattern each); 28 bytes in sizeof; the walk at `whd/src/whd_wifi_api.c:6738` computes (wl_wowl_pattern_t *)ptr + tot, so tot is scaled by sizeof(wl_wowl_pattern_t) rather than used as a byte offset, which affects only entries after the first |

Size check: compiled

### `wl_wowl_wakeind_t` (whd)
Wake-on-wireless wake indication (struct tag `wl_wowl_wakeind`), with no use site in whd outside the header and no command or named variable given for it there; not packed (the header's first `#pragma pack` is at line 3864, after the definition; alignment 2); 4 bytes; byte order not stated in the definition, little-endian as whd treats it (inferred: plain uintN_t types, and whd's htod16/htod32/dtoh16/dtoh32 are identity unless IL_BIGENDIAN is defined). `whd/src/include/whd_wlioctl.h:3789-3793` `whd/src/include/whd_wlioctl.h:3864` `whd/src/include/whd_endian.h:44-57`

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 1 | `pci_wakeind` | `uint8_t` | comment: whether PCI PMECSR PMEStatus bit was set `whd/src/include/whd_wlioctl.h:3791` |
| 1 | 1 | (pad) | - | implicit alignment padding inserted by the compiler, not a declared member `whd/src/include/whd_wlioctl.h:3791-3792` |
| 2 | 2 | `ucode_wakeind` | `uint16_t` | comment: what wakeup-event indication was set by ucode `whd/src/include/whd_wlioctl.h:3792` |

Size check: compiled

Differences: linux reads the named variable "wowl_wakeind" into `struct brcmf_wowl_wakeind_le`, which has the same two member names as `__le32` each (8 bytes), and also sets that variable with the string "clear" copied into the same record. The whd definition is 4 bytes and has no use site, so its layout as the wire form of that variable is (unverified); linux's is the only definition with a use site. The record name is not found in embassy, c-driver or pico-sdk. `linux/brcmfmac/fwil_types.h:876-885` `linux/brcmfmac/cfg80211.c:4139` `linux/brcmfmac/cfg80211.c:4146-4147` `linux/brcmfmac/cfg80211.c:4245` `linux/brcmfmac/cfg80211.c:4287-4289`


### `wl_txrate_class_t` (whd)
Transmit rate class of three rate bytes (struct tag `wl_txrate_class`), with no use site in whd outside the header and no command or named variable given for it there, and not found in linux, embassy, c-driver or pico-sdk; not packed (the header's first `#pragma pack` is at line 3864, after the definition; alignment 1); 3 bytes; all fields are single bytes, so there is no byte order. `whd/src/include/whd_wlioctl.h:3795-3800` `whd/src/include/whd_wlioctl.h:3864`

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 1 | `init_rate` | `uint8_t` | `whd/src/include/whd_wlioctl.h:3797` |
| 1 | 1 | `min_rate` | `uint8_t` | `whd/src/include/whd_wlioctl.h:3798` |
| 2 | 1 | `max_rate` | `uint8_t` | `whd/src/include/whd_wlioctl.h:3799` |

Size check: compiled

### `wl_obss_scan_arg_t` (whd)
Not used in whd/inc or whd/src (include_helium excluded), and the header names no command or named variable (iovar) for it; WL_OBSS_SCAN_PARAM_LEN is sizeof this record `whd/src/include/whd_wlioctl.h:3836`, WL_MIN_NUM_OBSS_SCAN_ARG is 7 `whd/src/include/whd_wlioctl.h:3837`; not packed (outside any `#pragma pack` region, natural alignment); 14 bytes, alignment 2, same on x86-64 and 32-bit ARM; little-endian (inferred: not stated at the definition, whd converts with htod16/htod32, which are identity on little-endian hosts and byte swaps on big-endian hosts `whd/src/include/whd_endian.h:45-55`); defined at `whd/src/include/whd_wlioctl.h:3826-3835`.
| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 2 | `passive_dwell` | `int16_t` |  |
| 2 | 2 | `active_dwell` | `int16_t` |  |
| 4 | 2 | `bss_widthscan_interval` | `int16_t` |  |
| 6 | 2 | `passive_total` | `int16_t` |  |
| 8 | 2 | `active_total` | `int16_t` |  |
| 10 | 2 | `chanwidth_transition_delay` | `int16_t` |  |
| 12 | 2 | `activity_threshold` | `int16_t` |  |

Size check: compiled

### `wl_action_obss_coex_req_t` (whd)
Not used in whd/inc or whd/src (include_helium excluded), and the header names no command or named variable for it; not packed (outside any `#pragma pack` region, natural alignment); variable size, 2 fixed bytes + flexible tail, sizeof 3, alignment 1, same on x86-64 and 32-bit ARM; no multi-byte integers, so no endianness; defined at `whd/src/include/whd_wlioctl.h:3842-3847`.
| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 1 | `info` | `uint8_t` | WL_COEX_* bits, `whd/src/include/whd_wlioctl.h:3838-3841` |
| 1 | 1 | `num` | `uint8_t` |  |
| 2 | variable | `ch_list` | `uint8_t[1]` | flexible tail declared as [1]; sizeof counts one element (1 byte) `whd/src/include/whd_wlioctl.h:3846` |

Size check: compiled

### `wl_rssi_event_t` (whd)
Not used in whd/inc or whd/src (include_helium excluded), and the header names no command or named variable for it; not packed (outside any `#pragma pack` region, natural alignment); 16 bytes, alignment 4, same on x86-64 and 32-bit ARM; little-endian (inferred: not stated at the definition, whd converts with htod16/htod32, which are identity on little-endian hosts and byte swaps on big-endian hosts `whd/src/include/whd_endian.h:45-55`); defined at `whd/src/include/whd_wlioctl.h:3849-3854`.
| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `rate_limit_msec` | `uint32_t` |  |
| 4 | 1 | `num_rssi_levels` | `uint8_t` |  |
| 5 | 8 | `rssi_levels` | `int8_t[8]` | MAX_RSSI_LEVELS = 8 `whd/src/include/whd_wlioctl.h:3848` |
| 13 | 3 | (pad) |  | trailing alignment padding inserted by the compiler |

Size check: compiled

### `sta_prbreq_wps_ie_hdr_t` (whd)
Not used in whd/inc or whd/src (include_helium excluded), and the header names no command or named variable for it; packed, inside the `#pragma pack(1)` region `whd/src/include/whd_wlioctl.h:3864-3918`; 8 bytes, alignment 1, same on x86-64 and 32-bit ARM; little-endian (inferred: not stated at the definition, whd converts with htod16/htod32, which are identity on little-endian hosts and byte swaps on big-endian hosts `whd/src/include/whd_endian.h:45-55`); defined at `whd/src/include/whd_wlioctl.h:3866-3870`.
| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 6 | `staAddr` | `wl_ether_addr_t` | 6 octets `whd/src/include/whd_wlioctl.h:50-53` |
| 6 | 2 | `ieLen` | `uint16_t` |  |

Size check: compiled

### `sta_prbreq_wps_ie_data_t` (whd)
Not used in whd/inc or whd/src (include_helium excluded), and the header names no command or named variable for it; packed, inside the `#pragma pack(1)` region `whd/src/include/whd_wlioctl.h:3864-3918`; variable size, 8 fixed bytes + flexible tail, sizeof 9, alignment 1, same on x86-64 and 32-bit ARM; little-endian (inferred: not stated at the definition, whd converts with htod16/htod32, which are identity on little-endian hosts and byte swaps on big-endian hosts `whd/src/include/whd_endian.h:45-55`); defined at `whd/src/include/whd_wlioctl.h:3872-3876`.
| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 8 | `hdr` | `sta_prbreq_wps_ie_hdr_t` | 8 bytes `whd/src/include/whd_wlioctl.h:3874` |
| 8 | variable | `ieData` | `uint8_t[1]` | flexible tail declared as [1]; sizeof counts one element (1 byte) `whd/src/include/whd_wlioctl.h:3875` |

Size check: compiled

### `sta_prbreq_wps_ie_list_t` (whd)
Not used in whd/inc or whd/src (include_helium excluded), and the header names no command or named variable for it; packed, inside the `#pragma pack(1)` region `whd/src/include/whd_wlioctl.h:3864-3918`; variable size, 4 fixed bytes + flexible tail, sizeof 5, alignment 1, same on x86-64 and 32-bit ARM; little-endian (inferred: not stated at the definition, whd converts with htod16/htod32, which are identity on little-endian hosts and byte swaps on big-endian hosts `whd/src/include/whd_endian.h:45-55`); defined at `whd/src/include/whd_wlioctl.h:3878-3882`.
| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `totLen` | `uint32_t` |  |
| 4 | variable | `ieDataList` | `uint8_t[1]` | flexible tail declared as [1]; sizeof counts one element (1 byte) `whd/src/include/whd_wlioctl.h:3881` |

Size check: compiled

### `edcf_acparam_t` (whd)
Response of named variable "wme_ac_sta" (IOVAR_STR_AC_PARAMS_STA, `whd/src/include/whd_wlioctl.h:1090`): whd_wifi_get_acparams copies 4 consecutive edcf_acparam_t from the response `whd/src/whd_wifi_api.c:4197-4204`; public alias whd_edcf_ac_param_t `whd/inc/whd_types.h:141`; the response is an array of 4 records (16 bytes) and the request buffer is 64 zero bytes `whd/src/whd_wifi_api.c:4197-4200`; packed, inside the `#pragma pack(1)` region `whd/src/include/whd_wlioctl.h:3864-3918`; 4 bytes, alignment 1, same on x86-64 and 32-bit ARM; TXOP is little-endian per the source comment 'stored in network order (ls octet first)' `whd/src/include/whd_wlioctl.h:3913`, read as least-significant octet first (inferred), and whd applies no byte swap at the use site `whd/src/whd_wifi_api.c:4197-4204`; defined at `whd/src/include/whd_wlioctl.h:3909-3915`.
| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 1 | `ACI` | `uint8_t` | EDCF_AIFSN/ACM/ACI masks at `whd/src/include/whd_wlioctl.h:3887-3893` |
| 1 | 1 | `ECW` | `uint8_t` | EDCF_ECWMIN/ECWMAX masks at `whd/src/include/whd_wlioctl.h:3899-3901` |
| 2 | 2 | `TXOP` | `uint16_t` | source comment: 'stored in network order (ls octet first)' `whd/src/include/whd_wlioctl.h:3913` |

Size check: compiled

### `wl_p2p_disc_st_t` (whd)
Not used in whd/inc or whd/src (include_helium excluded), and the header names no command or named variable for it; not packed (outside any `#pragma pack` region, natural alignment); 6 bytes, alignment 2, same on x86-64 and 32-bit ARM; little-endian (inferred: not stated at the definition, whd converts with htod16/htod32, which are identity on little-endian hosts and byte swaps on big-endian hosts `whd/src/include/whd_endian.h:45-55`); defined at `whd/src/include/whd_wlioctl.h:3921-3926`.
| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 1 | `state` | `uint8_t` | see p2p_discovery_state_t `whd/src/include/whd_wlioctl.h:3923` |
| 1 | 1 | (pad) |  | alignment padding inserted by the compiler |
| 2 | 2 | `chanspec` | `uint16_t` | valid in listen state `whd/src/include/whd_wlioctl.h:3924` |
| 4 | 2 | `dwell_time_ms` | `uint16_t` | valid in listen state, in ms `whd/src/include/whd_wlioctl.h:3925` |

Size check: compiled

### `wl_p2p_scan_t` (whd)
Not used in whd/inc or whd/src (include_helium excluded), and the header names no command or named variable for it; source comment: scan or escan params follow this header `whd/src/include/whd_wlioctl.h:3933`; not packed (outside any `#pragma pack` region, natural alignment); 4 bytes, alignment 1, same on x86-64 and 32-bit ARM; no multi-byte integers, so no endianness; defined at `whd/src/include/whd_wlioctl.h:3929-3934`.
| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 1 | `type` | `uint8_t` | 'S' for WLC_SCAN, 'E' for "escan" `whd/src/include/whd_wlioctl.h:3931` |
| 1 | 3 | `reserved` | `uint8_t[3]` |  |

Size check: compiled

### `wl_p2p_escan_t` (whd)
Not used in whd/inc or whd/src (include_helium excluded), and the header names no command or named variable for it; anonymous struct typedef; the nested records are shown by their top-level offsets only; not packed (outside any `#pragma pack` region, natural alignment); variable size, 76 fixed bytes + channel list tail, sizeof 80, alignment 4, same on x86-64 and 32-bit ARM; little-endian (inferred: not stated at the definition, whd converts with htod16/htod32, which are identity on little-endian hosts and byte swaps on big-endian hosts `whd/src/include/whd_endian.h:45-55`); defined at `whd/src/include/whd_wlioctl.h:3937-3944`.
| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 1 | `type` | `uint8_t` | 'S' for WLC_SCAN, 'E' for "escan" `whd/src/include/whd_wlioctl.h:3939` |
| 1 | 3 | `reserved` | `uint8_t[3]` |  |
| 4 | 76 | `escan` | `wl_escan_params_t` | defined at `whd/src/include/whd_wlioctl.h:548-554`; its params member ends in a uint16_t channel_list[1] variable-length list |
| 4 | 4 | `escan.version` | `uint32_t` |  |
| 8 | 2 | `escan.action` | `uint16_t` |  |
| 10 | 2 | `escan.sync_id` | `uint16_t` |  |
| 12 | 68 | `escan.params` | `wl_scan_params_t` | defined at `whd/src/include/whd_wlioctl.h:506-518`; 68 bytes by sizeof, channel_list[1] at +64 within it (WL_SCAN_PARAMS_FIXED_SIZE = 64, `whd/src/include/whd_wlioctl.h:519`) |

Size check: compiled

### `wl_p2p_if_t` (whd)
Not used in whd/inc or whd/src (include_helium excluded), and the header names no command or named variable for it; not packed (outside any `#pragma pack` region, natural alignment); 10 bytes, alignment 2, same on x86-64 and 32-bit ARM; little-endian (inferred: not stated at the definition, whd converts with htod16/htod32, which are identity on little-endian hosts and byte swaps on big-endian hosts `whd/src/include/whd_endian.h:45-55`); defined at `whd/src/include/whd_wlioctl.h:3947-3952`.
| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 6 | `mac_address` | `struct ether_addr` | 6 octets `whd/src/include/whd_wlioctl.h:3949` |
| 6 | 1 | `interface_type` | `uint8_t` |  |
| 7 | 1 | (pad) |  | alignment padding inserted by the compiler |
| 8 | 2 | `chan_spec` | `uint16_t` |  |

Size check: compiled

### `wl_p2p_ifq_t` (whd)
Not used in whd/inc or whd/src (include_helium excluded), and the header names no command or named variable for it; not packed (outside any `#pragma pack` region, natural alignment); 20 bytes, alignment 4, same on x86-64 and 32-bit ARM; little-endian (inferred: not stated at the definition, whd converts with htod16/htod32, which are identity on little-endian hosts and byte swaps on big-endian hosts `whd/src/include/whd_endian.h:45-55`); defined at `whd/src/include/whd_wlioctl.h:3955-3959`.
| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `bsscfgidx` | `uint32_t` |  |
| 4 | 16 | `ifname` | `char[16]` |  |

Size check: compiled

### `wl_p2p_ops_t` (whd)
Not used in whd/inc or whd/src (include_helium excluded), and the header names no command or named variable for it; not packed (outside any `#pragma pack` region, natural alignment); 2 bytes, alignment 1, same on x86-64 and 32-bit ARM; no multi-byte integers, so no endianness; defined at `whd/src/include/whd_wlioctl.h:3962-3966`.
| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 1 | `ops` | `uint8_t` | 0: disable 1: enable `whd/src/include/whd_wlioctl.h:3964` |
| 1 | 1 | `ctw` | `uint8_t` | >= 10 `whd/src/include/whd_wlioctl.h:3965` |

Size check: compiled

### `wl_p2p_sched_desc_t` (whd)
Not used in whd/inc or whd/src (include_helium excluded), and the header names no command or named variable for it; not packed (outside any `#pragma pack` region, natural alignment); 16 bytes, alignment 4, same on x86-64 and 32-bit ARM; little-endian (inferred: not stated at the definition, whd converts with htod16/htod32, which are identity on little-endian hosts and byte swaps on big-endian hosts `whd/src/include/whd_endian.h:45-55`); defined at `whd/src/include/whd_wlioctl.h:3969-3975`.
| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `start` | `uint32_t` |  |
| 4 | 4 | `interval` | `uint32_t` |  |
| 8 | 4 | `duration` | `uint32_t` |  |
| 12 | 4 | `count` | `uint32_t` |  |

Size check: compiled

### `wl_p2p_sched_t` (whd)
Not used in whd/inc or whd/src (include_helium excluded), and the header names no command or named variable for it; not packed (outside any `#pragma pack` region, natural alignment); variable size, 4 fixed bytes + flexible tail, sizeof 20, alignment 4, same on x86-64 and 32-bit ARM; little-endian (inferred: not stated at the definition, whd converts with htod16/htod32, which are identity on little-endian hosts and byte swaps on big-endian hosts `whd/src/include/whd_endian.h:45-55`); defined at `whd/src/include/whd_wlioctl.h:3977-3983`.
| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 1 | `type` | `uint8_t` | WL_P2P_SCHED_TYPE_* `whd/src/include/whd_wlioctl.h:3986-3988` |
| 1 | 1 | `action` | `uint8_t` | WL_P2P_SCHED_ACTION_* `whd/src/include/whd_wlioctl.h:3991-3993` |
| 2 | 1 | `option` | `uint8_t` | WL_P2P_SCHED_OPTION_* `whd/src/include/whd_wlioctl.h:3996-3997` |
| 3 | 1 | (pad) |  | alignment padding inserted by the compiler |
| 4 | variable | `desc` | `wl_p2p_sched_desc_t[1]` | flexible tail declared as [1]; sizeof counts one element (16 bytes); each element 16 bytes `whd/src/include/whd_wlioctl.h:3982` |

Size check: compiled

### `wl_p2p_wfds_hash_t` (whd)
Not used in whd/inc or whd/src (include_helium excluded), and the header names no command or named variable for it; not packed (outside any `#pragma pack` region, natural alignment); 216 bytes, alignment 4, same on x86-64 and 32-bit ARM; little-endian (inferred: not stated at the definition, whd converts with htod16/htod32, which are identity on little-endian hosts and byte swaps on big-endian hosts `whd/src/include/whd_endian.h:45-55`); defined at `whd/src/include/whd_wlioctl.h:3999-4006`.
| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `advt_id` | `uint32_t` |  |
| 4 | 2 | `nw_cfg_method` | `uint16_t` |  |
| 6 | 6 | `wfds_hash` | `uint8_t[6]` |  |
| 12 | 1 | `name_len` | `uint8_t` |  |
| 13 | 200 | `service_name` | `uint8_t[200]` | MAX_WFDS_SVC_NAME_LEN = 200 `whd/src/include/whd_wlioctl.h:34` |
| 213 | 3 | (pad) |  | trailing alignment padding inserted by the compiler |

Size check: compiled

### `wl_relmcast_client_t` (whd)
Not used in whd/inc or whd/src (include_helium excluded), and the header names no command or named variable for it; not packed (outside any `#pragma pack` region, natural alignment), source comment 'RMC structures should not be packed' `whd/src/include/whd_wlioctl.h:4010`; 10 bytes, alignment 2, same on x86-64 and 32-bit ARM; little-endian (inferred: not stated at the definition, whd converts with htod16/htod32, which are identity on little-endian hosts and byte swaps on big-endian hosts `whd/src/include/whd_endian.h:45-55`); defined at `whd/src/include/whd_wlioctl.h:4051-4056`.
| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 1 | `flag` | `uint8_t` | WL_RMC_FLAG_* `whd/src/include/whd_wlioctl.h:4015-4018` |
| 1 | 1 | (pad) |  | alignment padding inserted by the compiler |
| 2 | 2 | `rssi` | `int16_t` |  |
| 4 | 6 | `addr` | `struct ether_addr` | 6 octets `whd/src/include/whd_wlioctl.h:4055` |

Size check: compiled

### `wl_rmc_cnts_t` (whd)
Not used in whd/inc or whd/src (include_helium excluded), and the header names no command or named variable for it; not packed (outside any `#pragma pack` region, natural alignment), source comment 'RMC structures should not be packed' `whd/src/include/whd_wlioctl.h:4010`; 60 bytes, alignment 4, same on x86-64 and 32-bit ARM; little-endian (inferred: not stated at the definition, whd converts with htod16/htod32, which are identity on little-endian hosts and byte swaps on big-endian hosts `whd/src/include/whd_endian.h:45-55`); defined at `whd/src/include/whd_wlioctl.h:4059-4087`.
| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 2 | `version` | `uint16_t` | WL_RMC_CNT_VERSION = 1 `whd/src/include/whd_wlioctl.h:4012` |
| 2 | 2 | `length` | `uint16_t` | length of entire structure `whd/src/include/whd_wlioctl.h:4062` |
| 4 | 2 | `dupcnt` | `uint16_t` |  |
| 6 | 2 | `ackreq_err` | `uint16_t` |  |
| 8 | 2 | `af_tx_err` | `uint16_t` |  |
| 10 | 2 | `null_tx_err` | `uint16_t` |  |
| 12 | 2 | `af_unicast_tx_err` | `uint16_t` |  |
| 14 | 2 | `mc_no_amt_slot` | `uint16_t` |  |
| 16 | 2 | `mc_no_glb_slot` | `uint16_t` | unused, kept for rom compatibility `whd/src/include/whd_wlioctl.h:4070` |
| 18 | 2 | `mc_not_mirrored` | `uint16_t` |  |
| 20 | 2 | `mc_existing_tr` | `uint16_t` |  |
| 22 | 2 | `mc_exist_in_amt` | `uint16_t` |  |
| 24 | 2 | `mc_not_exist_in_gbl` | `uint16_t` | unused, kept for rom compatibility `whd/src/include/whd_wlioctl.h:4075` |
| 26 | 2 | `mc_not_exist_in_amt` | `uint16_t` |  |
| 28 | 2 | `mc_utilized` | `uint16_t` |  |
| 30 | 2 | `mc_taken_other_tr` | `uint16_t` |  |
| 32 | 4 | `rmc_rx_frames_mac` | `uint32_t` |  |
| 36 | 4 | `rmc_tx_frames_mac` | `uint32_t` |  |
| 40 | 4 | `mc_null_ar_cnt` | `uint32_t` |  |
| 44 | 4 | `mc_ar_role_selected` | `uint32_t` |  |
| 48 | 4 | `mc_ar_role_deleted` | `uint32_t` |  |
| 52 | 4 | `mc_noacktimer_expired` | `uint32_t` |  |
| 56 | 2 | `mc_no_wl_clk` | `uint16_t` |  |
| 58 | 2 | `mc_tr_cnt_exceeded` | `uint16_t` |  |

Size check: compiled

### `wl_relmcast_status_t` (whd)
Not used in whd/inc or whd/src (include_helium excluded), and the header names no command or named variable for it; the struct tag is wl_relmcast_st `whd/src/include/whd_wlioctl.h:4090`; not packed (outside any `#pragma pack` region, natural alignment), source comment 'RMC structures should not be packed' `whd/src/include/whd_wlioctl.h:4010`; 326 bytes, alignment 2, same on x86-64 and 32-bit ARM; little-endian (inferred: not stated at the definition, whd converts with htod16/htod32, which are identity on little-endian hosts and byte swaps on big-endian hosts `whd/src/include/whd_endian.h:45-55`); defined at `whd/src/include/whd_wlioctl.h:4090-4097`.
| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 1 | `ver` | `uint8_t` |  |
| 1 | 1 | `num` | `uint8_t` | number of clients detected by transmitter `whd/src/include/whd_wlioctl.h:4093` |
| 2 | 320 | `clients` | `wl_relmcast_client_t[32]` | WL_RMC_MAX_CLIENT = 32 `whd/src/include/whd_wlioctl.h:4014`; each element 10 bytes |
| 322 | 2 | `err` | `uint16_t` |  |
| 324 | 2 | `actf_time` | `uint16_t` |  |

Size check: compiled

### `wl_rmc_entry_t` (whd)
Not used in whd/inc or whd/src (include_helium excluded), and the header names no command or named variable for it; not packed (outside any `#pragma pack` region, natural alignment), source comment 'RMC structures should not be packed' `whd/src/include/whd_wlioctl.h:4010`; 7 bytes, alignment 1, same on x86-64 and 32-bit ARM; no multi-byte integers, so no endianness; defined at `whd/src/include/whd_wlioctl.h:4100-4107`.
| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 1 | `flag` | `int8_t` | operation on multicast entry `whd/src/include/whd_wlioctl.h:4105` |
| 1 | 6 | `addr` | `struct ether_addr` | 6 octets `whd/src/include/whd_wlioctl.h:4106` |

Size check: compiled

### `wl_rmc_entry_table_t` (whd)
Not used in whd/inc or whd/src (include_helium excluded), and the header names no command or named variable for it; not packed (outside any `#pragma pack` region, natural alignment), source comment 'RMC structures should not be packed' `whd/src/include/whd_wlioctl.h:4010`; 58 bytes, alignment 1, same on x86-64 and 32-bit ARM; no multi-byte integers, so no endianness; defined at `whd/src/include/whd_wlioctl.h:4110-4115`.
| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 1 | `index` | `uint8_t` |  |
| 1 | 1 | `opcode` | `uint8_t` | enum rmc_opcodes `whd/src/include/whd_wlioctl.h:4034-4040` |
| 2 | 56 | `entry` | `wl_rmc_entry_t[8]` | WL_RMC_MAX_TABLE_ENTRY = 8 `whd/src/include/whd_wlioctl.h:4019`; each element 7 bytes |

Size check: compiled

### `wl_rmc_trans_elem_t` (whd)
Not used in whd/inc or whd/src (include_helium excluded), and the header names no command or named variable for it; not packed (outside any `#pragma pack` region, natural alignment), source comment 'RMC structures should not be packed' `whd/src/include/whd_wlioctl.h:4010`; 18 bytes, alignment 2, same on x86-64 and 32-bit ARM; little-endian (inferred: not stated at the definition, whd converts with htod16/htod32, which are identity on little-endian hosts and byte swaps on big-endian hosts `whd/src/include/whd_endian.h:45-55`); defined at `whd/src/include/whd_wlioctl.h:4117-4124`.
| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 6 | `tr_mac` | `struct ether_addr` | 6 octets `whd/src/include/whd_wlioctl.h:4119` |
| 6 | 6 | `ar_mac` | `struct ether_addr` | 6 octets `whd/src/include/whd_wlioctl.h:4120` |
| 12 | 2 | `artmo` | `uint16_t` | AR timeout `whd/src/include/whd_wlioctl.h:4121` |
| 14 | 1 | `amt_idx` | `uint8_t` |  |
| 15 | 1 | (pad) |  | alignment padding inserted by the compiler |
| 16 | 2 | `flag` | `uint16_t` |  |

Size check: compiled

### `wl_rmc_trans_in_network_t` (whd)
Not used in whd/inc or whd/src (include_helium excluded), and the header names no command or named variable for it; not packed (outside any `#pragma pack` region, natural alignment), source comment 'RMC structures should not be packed' `whd/src/include/whd_wlioctl.h:4010`; 578 bytes, alignment 2, same on x86-64 and 32-bit ARM; little-endian (inferred: not stated at the definition, whd converts with htod16/htod32, which are identity on little-endian hosts and byte swaps on big-endian hosts `whd/src/include/whd_endian.h:45-55`); defined at `whd/src/include/whd_wlioctl.h:4127-4132`.
| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 1 | `ver` | `uint8_t` |  |
| 1 | 1 | `num_tr` | `uint8_t` |  |
| 2 | 576 | `trs` | `wl_rmc_trans_elem_t[32]` | WL_RMC_MAX_NUM_TRS = 32 `whd/src/include/whd_wlioctl.h:4030`; each element 18 bytes |

Size check: compiled

### `wl_rmc_vsie_t` (whd)
Not used in whd/inc or whd/src (include_helium excluded), and the header names no command or named variable for it; not packed (outside any `#pragma pack` region, natural alignment), source comment 'RMC structures should not be packed' `whd/src/include/whd_wlioctl.h:4010`; 6 bytes, alignment 2, same on x86-64 and 32-bit ARM; little-endian (inferred: not stated at the definition, whd converts with htod16/htod32, which are identity on little-endian hosts and byte swaps on big-endian hosts `whd/src/include/whd_endian.h:45-55`); defined at `whd/src/include/whd_wlioctl.h:4135-4139`.
| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 3 | `oui` | `uint8_t[3]` |  |
| 3 | 1 | (pad) |  | alignment padding inserted by the compiler |
| 4 | 2 | `payload` | `uint16_t` | IE Data Payload `whd/src/include/whd_wlioctl.h:4138` |

Size check: compiled

### `wl_ulp_event_t` (whd)
Event data of WLC_E_ULP per the source comment at `whd/src/include/whd_wlioctl.h:4141` only; WLC_E_ULP = 146 `whd/src/include/whd_events_int.h:170`; no code in whd/ references the typedef or its fields; the one handler that names WLC_E_ULP `whd/src/whd_wifi_api.c:1611` lists it among events that hit the 'Received event which was not registered' assert `whd/src/whd_wifi_api.c:1613-1614`; not packed (outside any `#pragma pack` region, natural alignment); 4 bytes, alignment 2, same on x86-64 and 32-bit ARM; little-endian (inferred: not stated at the definition, whd converts with htod16/htod32, which are identity on little-endian hosts and byte swaps on big-endian hosts `whd/src/include/whd_endian.h:45-55`); defined at `whd/src/include/whd_wlioctl.h:4147-4151`.
| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 2 | `version` | `uint16_t` | WL_ULP_EVENT_VERSION = 1 `whd/src/include/whd_wlioctl.h:4142` |
| 2 | 2 | `ulp_dongle_action` | `uint16_t` | WL_ULP_DISABLE_CONSOLE 1, WL_ULP_UCODE_DOWNLOAD 2, WL_ULP_ENTRY 3 `whd/src/include/whd_wlioctl.h:4143-4145` |

Size check: compiled

### `wl_dload_data_t` (whd)
Payload of SET named variable "clmload" (IOVAR_STR_CLMLOAD, `whd/src/include/whd_wlioctl.h:1231`), sent per chunk by whd_download_wifi_clm_image `whd/src/whd_clm.c:44-69` called from whd_process_clm_data `whd/src/whd_clm.c:138`; without PROTO_MSGBUF the total length is rounded up with len + 8 - (len % 8) before sending `whd/src/whd_clm.c:61-63`, which adds 8 when len is already a multiple of 8; not packed (outside any `#pragma pack` region, natural alignment); variable size, 12 fixed bytes + flexible tail, sizeof 16, alignment 4, same on x86-64 and 32-bit ARM; little-endian: the use site applies htod16/htod32, identity on little-endian hosts and swap on big-endian `whd/src/include/whd_endian.h:45-55`; defined at `whd/src/include/whd_wlioctl.h:4167-4175`.
| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 2 | `flag` | `uint16_t` | (DLOAD_HANDLER_VER << DLOAD_FLAG_VER_SHIFT) \| flag, i.e. 0x1000 \| DL_BEGIN 0x0002 / DL_END 0x0004 (`whd/src/whd_clm.c:54`; constants at `whd/src/include/whd_wlioctl.h:4154-4160`; DL_CRC_NOT_INUSE 0x0001 is defined but not set by whd_clm.c); DL_BEGIN is set on the first chunk and DL_END on the last `whd/src/whd_clm.c:78` `whd/src/whd_clm.c:133-140` |
| 2 | 2 | `dload_type` | `uint16_t` | DL_TYPE_UCODE = 1, DL_TYPE_CLM = 2 `whd/src/include/whd_wlioctl.h:4164` |
| 4 | 4 | `len` | `uint32_t` | payload length excluding this header `whd/src/whd_clm.c:56` |
| 8 | 4 | `crc` | `uint32_t` | set to 0 by whd `whd/src/whd_clm.c:58` |
| 12 | variable | `data` | `uint8_t[1]` | flexible tail declared as [1]; sizeof counts one element (1 byte); payload starts at offsetof(data) = 12 `whd/src/whd_clm.c:53` |
| 13 | 3 | (pad) |  | trailing alignment padding inserted by the compiler |

Size check: compiled

### `wl_clm_dload_info_t` (whd)
Not used in whd/inc or whd/src (include_helium excluded), and the header names no command or named variable for it; not packed (outside any `#pragma pack` region, natural alignment); variable size, 20 fixed bytes + flexible tail, sizeof 24, alignment 4, same on x86-64 and 32-bit ARM; little-endian (inferred: not stated at the definition, whd converts with htod16/htod32, which are identity on little-endian hosts and byte swaps on big-endian hosts `whd/src/include/whd_endian.h:45-55`); defined at `whd/src/include/whd_wlioctl.h:4177-4186`.
| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `ds_id` | `uint32_t` |  |
| 4 | 4 | `clm_total_len` | `uint32_t` |  |
| 8 | 4 | `num_chunks` | `uint32_t` |  |
| 12 | 4 | `chunk_len` | `uint32_t` |  |
| 16 | 4 | `chunk_offset` | `uint32_t` |  |
| 20 | variable | `data_chunk` | `uint8_t[1]` | flexible tail declared as [1]; sizeof counts one element (1 byte) `whd/src/include/whd_wlioctl.h:4184` |
| 21 | 3 | (pad) |  | trailing alignment padding inserted by the compiler |

Size check: compiled

### `mesh_peer_info_t` (whd)
Not used in whd/inc or whd/src (include_helium excluded), and the header names no command or named variable for it; packed, inside the `#pragma pack(1)` region `whd/src/include/whd_wlioctl.h:4188-4289`; 9 bytes, alignment 1, same on x86-64 and 32-bit ARM; little-endian (inferred: not stated at the definition, whd converts with htod16/htod32, which are identity on little-endian hosts and byte swaps on big-endian hosts `whd/src/include/whd_endian.h:45-55`); defined at `whd/src/include/whd_wlioctl.h:4189-4196`.
| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 2 | `mesh_peer_prot_id` | `uint16_t` |  |
| 2 | 2 | `local_link_id` | `uint16_t` |  |
| 4 | 2 | `peer_link_id` | `uint16_t` |  |
| 6 | 2 | `peer_aid` | `uint16_t` |  |
| 8 | 1 | `state` | `uint8_t` |  |

Size check: compiled

### `mesh_peer_info_ext_t` (whd)
Not used in whd/inc or whd/src (include_helium excluded), and the header names no command or named variable for it; packed, inside the `#pragma pack(1)` region `whd/src/include/whd_wlioctl.h:4188-4289`; 25 bytes, alignment 1, same on x86-64 and 32-bit ARM; little-endian (inferred: not stated at the definition, whd converts with htod16/htod32, which are identity on little-endian hosts and byte swaps on big-endian hosts `whd/src/include/whd_endian.h:45-55`); defined at `whd/src/include/whd_wlioctl.h:4198-4205`.
| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 9 | `peer_info` | `mesh_peer_info_t` | 9 bytes `whd/src/include/whd_wlioctl.h:4200` |
| 9 | 2 | `local_aid` | `uint16_t` |  |
| 11 | 6 | `ea` | `struct ether_addr` | 6 octets `whd/src/include/whd_wlioctl.h:4202` |
| 17 | 4 | `entry_state` | `uint32_t` |  |
| 21 | 4 | `rssi` | `int32_t` |  |

Size check: compiled

### `mesh_peer_info_dump_t` (whd)
Not used in whd/inc or whd/src (include_helium excluded), and the header names no command or named variable for it; packed, inside the `#pragma pack(1)` region `whd/src/include/whd_wlioctl.h:4188-4289`; variable size, 12 fixed bytes + flexible tail, sizeof 37, alignment 1, same on x86-64 and 32-bit ARM; little-endian (inferred: not stated at the definition, whd converts with htod16/htod32, which are identity on little-endian hosts and byte swaps on big-endian hosts `whd/src/include/whd_endian.h:45-55`); defined at `whd/src/include/whd_wlioctl.h:4207-4213`.
| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `buflen` | `uint32_t` |  |
| 4 | 4 | `version` | `uint32_t` |  |
| 8 | 4 | `count` | `uint32_t` | number of results `whd/src/include/whd_wlioctl.h:4211` |
| 12 | variable | `mpi_ext` | `mesh_peer_info_ext_t[1]` | flexible tail declared as [1]; sizeof counts one element (25 bytes); each element 25 bytes `whd/src/include/whd_wlioctl.h:4212` |

Size check: compiled

### `wl_assoc_params_t` (whd)
As wl_reassoc_params_t: payload of command WLC_REASSOC (53, `whd/src/include/whd_wlioctl.h:1347`) at `whd/src/whd_wifi_api.c:2391-2397`; embedded in wl_join_params_t (WLC_SET_SSID) and wl_extjoin_params_t (named variable "join"); aliases wl_reassoc_params_t `whd/src/include/whd_wlioctl.h:4247` and wl_join_assoc_params_t `whd/src/include/whd_wlioctl.h:4249`; whd sends the full sizeof (14) for WLC_REASSOC with only bssid filled `whd/src/whd_wifi_api.c:2391-2397`; packed, inside the `#pragma pack(1)` region `whd/src/include/whd_wlioctl.h:4188-4289`, which is opened at `whd/src/include/whd_wlioctl.h:4188` for the mesh records and not closed until `whd/src/include/whd_wlioctl.h:4289`, so the packing comes only from the enclosing region; variable size, 12 fixed bytes + flexible tail, sizeof 14, alignment 1, same on x86-64 and 32-bit ARM; with natural alignment the size would be 16, 2 tail pad bytes (computed); WL_ASSOC_PARAMS_FIXED_SIZE = sizeof - sizeof(wl_chanspec_t) = 12 `whd/src/include/whd_wlioctl.h:4246`; little-endian: chanspec_list[0] is written with htod16 at the use sites `whd/src/whd_wifi_api.c:2365` `whd/src/whd_wifi_api.c:2384`; chanspec_num and bssid_cnt are assigned without a swap `whd/src/whd_wifi_api.c:2360-2364`, see `whd/src/include/whd_endian.h:45-55`; defined at `whd/src/include/whd_wlioctl.h:4239-4245`.
| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 6 | `bssid` | `struct ether_addr` | 6 octets `whd/src/include/whd_wlioctl.h:4241` |
| 6 | 2 | `bssid_cnt` | `uint16_t` |  |
| 8 | 4 | `chanspec_num` | `uint32_t` |  |
| 12 | variable | `chanspec_list` | `chanspec_t[1]` | flexible tail declared as [1]; sizeof counts one element (2 bytes); chanspec_t is uint16_t `whd/src/include/whd_wlioctl.h:48` |

Size check: compiled

### `wl_join_params_t` (whd)
Payload of command WLC_SET_SSID (26, `whd/src/include/whd_wlioctl.h:1323`), used as fallback when named variable "join" returns WHD_WLAN_UNSUPPORTED `whd/src/whd_wifi_api.c:2369-2386`; whd sends the full sizeof (50) `whd/src/whd_wifi_api.c:2369-2386`; packed, inside the `#pragma pack(1)` region `whd/src/include/whd_wlioctl.h:4188-4289`; variable size, 48 fixed bytes + flexible tail, sizeof 50, alignment 1, same on x86-64 and 32-bit ARM; WL_JOIN_PARAMS_FIXED_SIZE = sizeof - sizeof(wl_chanspec_t) = 48 `whd/src/include/whd_wlioctl.h:4256`; little-endian: chanspec_list[0] written with htod16 `whd/src/whd_wifi_api.c:2384`; other integers assigned without swap; `whd/src/include/whd_endian.h:45-55`; defined at `whd/src/include/whd_wlioctl.h:4251-4255`.
| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 36 | `ssid` | `wlc_ssid_t` | 36 bytes: uint32_t SSID_len + uint8_t SSID[32] `whd/src/include/whd_wlioctl.h:496-500` |
| 36 | 14 | `params` | `struct wl_assoc_params` | 14 bytes as packed here `whd/src/include/whd_wlioctl.h:4254` |
| 36 | 6 | `params.bssid` | `struct ether_addr` |  |
| 42 | 2 | `params.bssid_cnt` | `uint16_t` |  |
| 44 | 4 | `params.chanspec_num` | `uint32_t` |  |
| 48 | variable | `params.chanspec_list` | `chanspec_t[1]` | flexible tail declared as [1]; sizeof counts one element (2 bytes) `whd/src/include/whd_wlioctl.h:4244` |

Size check: compiled

### `wl_extjoin_params_t` (whd)
Payload of SET named variable "join" (string literal at `whd/src/whd_wifi_api.c:2346`), built at `whd/src/whd_wifi_api.c:2345-2367`; whd sends the full sizeof (70) with the scan_params fields set to the 0 / -1 defaults `whd/src/whd_wifi_api.c:2355-2359`; packed, inside the `#pragma pack(1)` region `whd/src/include/whd_wlioctl.h:4188-4289`, but the embedded wl_join_scan_params was laid out before the region and keeps 3 pad bytes after scan_type; variable size, 68 fixed bytes + flexible tail, sizeof 70, alignment 1, same on x86-64 and 32-bit ARM; WL_EXTJOIN_PARAMS_FIXED_SIZE = sizeof - sizeof(chanspec_t) = 68 `whd/src/include/whd_wlioctl.h:4268`; little-endian: chanspec_list[0] written with htod16 `whd/src/whd_wifi_api.c:2365`; other integers assigned without swap; `whd/src/include/whd_endian.h:45-55`; defined at `whd/src/include/whd_wlioctl.h:4259-4267`.
| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 36 | `ssid` | `wlc_ssid_t` | 36 bytes; source comment: {0, ""} = wildcard scan `whd/src/include/whd_wlioctl.h:4261` |
| 36 | 20 | `scan_params` | `struct wl_join_scan_params` | 20 bytes; defined at `whd/src/include/whd_wlioctl.h:619-632` outside the pack region, so it keeps its internal natural-alignment padding (3 bytes after scan_type) |
| 36 | 1 | `scan_params.scan_type` | `uint8_t` | 0 use default `whd/src/include/whd_wlioctl.h:621` |
| 37 | 3 | (pad) |  | alignment padding inside scan_params (struct defined outside the pack region) |
| 40 | 4 | `scan_params.nprobes` | `int32_t` | -1 use default `whd/src/include/whd_wlioctl.h:622` |
| 44 | 4 | `scan_params.active_time` | `int32_t` | -1 use default `whd/src/include/whd_wlioctl.h:623-625` |
| 48 | 4 | `scan_params.passive_time` | `int32_t` | -1 use default `whd/src/include/whd_wlioctl.h:626-628` |
| 52 | 4 | `scan_params.home_time` | `int32_t` | -1 use default `whd/src/include/whd_wlioctl.h:629-631` |
| 56 | 14 | `assoc_params` | `wl_join_assoc_params_t` | 14 bytes as packed here; source comment: optional, but must include the fixed portion when present `whd/src/include/whd_wlioctl.h:4263` |
| 56 | 6 | `assoc_params.bssid` | `struct ether_addr` |  |
| 62 | 2 | `assoc_params.bssid_cnt` | `uint16_t` |  |
| 64 | 4 | `assoc_params.chanspec_num` | `uint32_t` |  |
| 68 | variable | `assoc_params.chanspec_list` | `chanspec_t[1]` | flexible tail declared as [1]; sizeof counts one element (2 bytes) `whd/src/include/whd_wlioctl.h:4244` |

Size check: compiled

### `wl_tko_t` (whd)
Common header of named variable "tko" (IOVAR_STR_TKO, `whd/src/include/whd_wlioctl.h:1264`), GET and SET; all use sites in whd/src/whd_wifi_api.c: whd_tko_param (`whd/src/whd_wifi_api.c:6154-6168`, SET or GET), whd_tko_get_status (`whd/src/whd_wifi_api.c:6233-6244`, GET), whd_tko_max_assoc (`whd/src/whd_wifi_api.c:6288-6300`, GET), whd_tko_get_FW_connect (`whd/src/whd_wifi_api.c:6339-6350`, GET), whd_tko_toggle (`whd/src/whd_wifi_api.c:6416-6430`, SET), whd_tko_autoenab (`whd/src/whd_wifi_api.c:6462-6477`, SET), whd_tko_filter (`whd/src/whd_wifi_api.c:6509-6525`, SET); not packed (outside any `#pragma pack` region, natural alignment), defined after the `#pragma pack()` at `whd/src/include/whd_wlioctl.h:4289`; the source comment at `whd/src/include/whd_wlioctl.h:4291-4293` says TKO definitions must not be inside pragma pack; variable size, 4 fixed bytes + flexible tail, sizeof 6, alignment 2, same on x86-64 and 32-bit ARM; sizeof is 6 because of the [1] tail plus alignment, the header proper is 4 bytes; little-endian: the use site applies htod16/htod32, identity on little-endian hosts and swap on big-endian `whd/src/include/whd_endian.h:45-55`; defined at `whd/src/include/whd_wlioctl.h:4307-4312`.
| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 2 | `subcmd_id` | `uint16_t` | WL_TKO_SUBCMD_* `whd/src/include/whd_wlioctl.h:4315-4322`: MAX_TCP 0, PARAM 1, CONNECT 2, ENABLE 3, STATUS 4, AUTOENAB 6, AUTOCONNECT 7, FILTER 8 |
| 2 | 2 | `len` | `uint16_t` | source comment 'total length of data[]'; whd instead sets offsetof(data) + sizeof(sub-record), i.e. header included, for PARAM `whd/src/whd_wifi_api.c:6163-6165`, STATUS (`whd/src/whd_wifi_api.c:6239-6241`, = 6), MAX_TCP `whd/src/whd_wifi_api.c:6294-6297`, ENABLE `whd/src/whd_wifi_api.c:6422-6427`, AUTOENAB `whd/src/whd_wifi_api.c:6468-6474`, FILTER `whd/src/whd_wifi_api.c:6520-6522`; for the CONNECT GET it sets only offsetof(data) = 4 although one index byte is written into data `whd/src/whd_wifi_api.c:6345-6347`. On replies whd reads len back (`whd/src/whd_wifi_api.c:6258`, `whd/src/whd_wifi_api.c:6360`) and compares it with payload sizes (>= 5 at `whd/src/whd_wifi_api.c:6260`; >= sizeof(wl_tko_connect_t) at `whd/src/whd_wifi_api.c:6368`). |
| 4 | variable | `data` | `uint8_t[1]` | flexible tail declared as [1]; sizeof counts one element (1 byte); sub-record starts at offset 4 = TKO_DATA_OFFSET `whd/inc/whd_types.h:1569` |
| 5 | 1 | (pad) |  | trailing alignment padding inserted by the compiler |

Size check: compiled

### `wl_tko_max_tcp_t` (whd)
Sub-record carried in wl_tko_t.data of named variable "tko" (IOVAR_STR_TKO, `whd/src/include/whd_wlioctl.h:1264`), subcommand WL_TKO_SUBCMD_MAX_TCP (0): whd_tko_max_assoc, `whd/src/whd_wifi_api.c:6293-6313`; GET only, the reply sub-record is copied from response offset 4 `whd/src/whd_wifi_api.c:6302-6316`; not packed (outside any `#pragma pack` region, natural alignment); 4 bytes, alignment 1, same on x86-64 and 32-bit ARM; no multi-byte integers, so no endianness; defined at `whd/src/include/whd_wlioctl.h:4325-4329`.
| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 1 | `max` | `uint8_t` | max TCP connections supported `whd/src/include/whd_wlioctl.h:4327` |
| 1 | 3 | `pad` | `uint8_t[3]` | explicit padding (declared field) `whd/src/include/whd_wlioctl.h:4328` |

Size check: compiled

### `wl_tko_param_t` (whd)
Sub-record carried in wl_tko_t.data of named variable "tko" (IOVAR_STR_TKO, `whd/src/include/whd_wlioctl.h:1264`), subcommand WL_TKO_SUBCMD_PARAM (1): whd_tko_param, `whd/src/whd_wifi_api.c:6162-6205`; on GET the reply sub-record is copied from offset TKO_DATA_OFFSET (4) of the response `whd/src/whd_wifi_api.c:6193-6199`; defaults when the caller passes 0 are interval 20 s, retry count 3, retry interval 3 s `whd/src/include/whd_wlioctl.h:4302-4304` `whd/src/whd_wifi_api.c:6175-6180`; not packed (outside any `#pragma pack` region, natural alignment); 8 bytes, alignment 2, same on x86-64 and 32-bit ARM; endianness not stated at the definition; interval/retry_count/retry_interval are assigned without htod on SET `whd/src/whd_wifi_api.c:6175-6180` and read without dtoh on GET `whd/src/whd_wifi_api.c:6203-6205`; defined at `whd/src/include/whd_wlioctl.h:4332-4338`.
| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 2 | `interval` | `uint16_t` | keepalive tx interval (secs) `whd/src/include/whd_wlioctl.h:4334` |
| 2 | 2 | `retry_interval` | `uint16_t` | keepalive retry interval (secs) `whd/src/include/whd_wlioctl.h:4335` |
| 4 | 2 | `retry_count` | `uint16_t` |  |
| 6 | 2 | `pad` | `uint8_t[2]` | explicit padding (declared field) `whd/src/include/whd_wlioctl.h:4337`; never written by whd on SET `whd/src/whd_wifi_api.c:6175-6180` |

Size check: compiled

### `wl_tko_connect_t` (whd)
Sub-record carried in wl_tko_t.data of named variable "tko" (IOVAR_STR_TKO, `whd/src/include/whd_wlioctl.h:1264`), subcommand WL_TKO_SUBCMD_CONNECT (2); whd only issues the GET: whd_tko_get_FW_connect, `whd/src/whd_wifi_api.c:6344-6395`; in the GET request wl_tko_t.len is set to 4 and only index is written at data[0] `whd/src/whd_wifi_api.c:6345-6347`; the reply is parsed only if tko->len >= sizeof(wl_tko_connect_t) (24) `whd/src/whd_wifi_api.c:6368`; a non-zero ip_addr_type (IPv6) is rejected by whd `whd/src/whd_wifi_api.c:6374-6378`; whd computes the IPv4 record length as sizeof(wl_tko_connect_t) + 8 + request_len + response_len `whd/src/whd_wifi_api.c:6383`, using sizeof (24, includes one data byte and 3 trailing pad bytes) rather than offsetof(data) (20); not packed (outside any `#pragma pack` region, natural alignment); variable size, 20 fixed bytes + flexible tail, sizeof 24, alignment 4, same on x86-64 and 32-bit ARM; little-endian for local_port, remote_port, local_seq, remote_seq: whd applies dtoh16/dtoh32 to them on the reply (`whd/src/whd_wifi_api.c:6370-6373`; macros at `whd/src/include/whd_endian.h:45-57`); request_len and response_len are used without dtoh `whd/src/whd_wifi_api.c:6383`; defined at `whd/src/include/whd_wlioctl.h:4343-4366`.
| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 1 | `index` | `uint8_t` | TCP connection index, 0 to max-1 `whd/src/include/whd_wlioctl.h:4345` |
| 1 | 1 | `ip_addr_type` | `uint8_t` | 0 - IPv4, 1 - IPv6 `whd/src/include/whd_wlioctl.h:4346` |
| 2 | 2 | `local_port` | `uint16_t` |  |
| 4 | 2 | `remote_port` | `uint16_t` |  |
| 6 | 2 | (pad) |  | alignment padding inserted by the compiler |
| 8 | 4 | `local_seq` | `uint32_t` |  |
| 12 | 4 | `remote_seq` | `uint32_t` |  |
| 16 | 2 | `request_len` | `uint16_t` | TCP keepalive request packet length `whd/src/include/whd_wlioctl.h:4351` |
| 18 | 2 | `response_len` | `uint16_t` | TCP keepalive response packet length `whd/src/include/whd_wlioctl.h:4352` |
| 20 | variable | `data` | `uint8_t[1]` | flexible tail declared as [1]; sizeof counts one element (1 byte); IPv4: local IP at +0, remote IP at +4, request packet at +8, response packet at +8+request_len; IPv6: local at +0, remote at +16, request at +32, response at +32+request_len (source comment) `whd/src/include/whd_wlioctl.h:4353` |
| 21 | 3 | (pad) |  | trailing alignment padding inserted by the compiler |

Size check: compiled

### `wl_tko_get_connect_t` (whd)
Sub-record carried in wl_tko_t.data of named variable "tko" (IOVAR_STR_TKO, `whd/src/include/whd_wlioctl.h:1264`), GET request for WL_TKO_SUBCMD_CONNECT per the source comment at `whd/src/include/whd_wlioctl.h:4368`; the typedef itself is not referenced in whd/src (whd casts tko->data to wl_tko_connect_t instead, `whd/src/whd_wifi_api.c:6346`); not packed (outside any `#pragma pack` region, natural alignment); 4 bytes, alignment 1, same on x86-64 and 32-bit ARM; no multi-byte integers, so no endianness; defined at `whd/src/include/whd_wlioctl.h:4369-4373`.
| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 1 | `index` | `uint8_t` |  |
| 1 | 3 | `pad` | `uint8_t[3]` | explicit padding (declared field) `whd/src/include/whd_wlioctl.h:4372` |

Size check: compiled

### `wl_tko_enable_t` (whd)
Sub-record carried in wl_tko_t.data of named variable "tko" (IOVAR_STR_TKO, `whd/src/include/whd_wlioctl.h:1264`), subcommand WL_TKO_SUBCMD_ENABLE (3): whd_tko_toggle, `whd/src/whd_wifi_api.c:6421-6427`; callers of whd_tko_toggle: `whd/src/whd_wifi_api.c:1057` `whd/src/whd_wifi_api.c:1072` `whd/src/whd_wifi_api.c:1089`; not packed (outside any `#pragma pack` region, natural alignment); 4 bytes, alignment 1, same on x86-64 and 32-bit ARM; no multi-byte integers, so no endianness; defined at `whd/src/include/whd_wlioctl.h:4375-4379`.
| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 1 | `enable` | `uint8_t` | 1 - enable, 0 - disable `whd/src/include/whd_wlioctl.h:4377` |
| 1 | 3 | `pad` | `uint8_t[3]` | explicit padding (declared field) `whd/src/include/whd_wlioctl.h:4378` |

Size check: compiled

### `wl_tko_status_t` (whd)
Sub-record carried in wl_tko_t.data of named variable "tko" (IOVAR_STR_TKO, `whd/src/include/whd_wlioctl.h:1264`), subcommand WL_TKO_SUBCMD_STATUS (4): whd_tko_get_status, `whd/src/whd_wifi_api.c:6238-6262`; the request sets wl_tko_t.len = 4 + sizeof(wl_tko_status_t) = 6 `whd/src/whd_wifi_api.c:6239-6241`; the reply is accepted when len >= MAX_TKO_CONN + 1 = 5 `whd/src/whd_wifi_api.c:6260`; source comment: the status cannot be had once tko is disabled, so the call has to be made before that `whd/src/include/whd_wlioctl.h:4382`; not packed (outside any `#pragma pack` region, natural alignment); variable size, 1 fixed bytes + flexible tail, sizeof 2, alignment 1, same on x86-64 and 32-bit ARM; no multi-byte integers, so no endianness; defined at `whd/src/include/whd_wlioctl.h:4383-4391`.
| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 1 | `count` | `uint8_t` | number of status entries (equals max TCP connections supported) `whd/src/include/whd_wlioctl.h:4385` |
| 1 | variable | `status` | `uint8_t[1]` | flexible tail declared as [1]; sizeof counts one element (1 byte); one tko_status_t value per connection index (enum at `whd/src/include/whd_wlioctl.h:4401-4411`: 0 normal, 1 no response, 2 no TCP ACK flag, 3 unexpected TCP flag, 4 seq num invalid, 5 remote seq num invalid, 6 TCP data, 255 unavailable) |

Size check: compiled

### `whd_tko_status` (whd)
Host-side fixed-size image of wl_tko_status_t: whd_tko_get_status memcpy's MAX_TKO_CONN + 1 = 5 bytes of the "tko" STATUS response data straight into it `whd/src/whd_wifi_api.c:6260-6262`; public alias whd_tko_status_t `whd/inc/whd_types.h:147`; not packed (outside any `#pragma pack` region, natural alignment); 5 bytes, alignment 1, same on x86-64 and 32-bit ARM; no multi-byte integers, so no endianness; defined at `whd/src/include/whd_wlioctl.h:4414-4418`.
| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 1 | `count` | `uint8_t` | number of status entries `whd/src/include/whd_wlioctl.h:4416` |
| 1 | 4 | `status` | `uint8_t[4]` | MAX_TKO_CONN = 4 `whd/src/include/whd_wlioctl.h:4299` |

Size check: compiled

### `whd_tko_connect` (whd)
Host-side copy of wl_tko_connect_t: the "tko" CONNECT response is memcpy'd into it; source comment 'Assumes whd_tko_connect_t and wl_tko_connect_t are the same' `whd/src/whd_wifi_api.c:6390-6395`; public alias whd_tko_connect_t `whd/inc/whd_types.h:146`; not packed (outside any `#pragma pack` region, natural alignment); variable size, 20 fixed bytes + flexible tail, sizeof 24, alignment 4, same on x86-64 and 32-bit ARM; host order for local_port, remote_port, local_seq, remote_seq, because whd applies dtoh16/dtoh32 to the reply in place before the copy `whd/src/whd_wifi_api.c:6370-6373`; request_len and response_len are copied as received `whd/src/whd_wifi_api.c:6395`; defined at `whd/src/include/whd_wlioctl.h:4421-4444`.
| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 1 | `index` | `uint8_t` | TCP connection index, 0 to max-1 `whd/src/include/whd_wlioctl.h:4423` |
| 1 | 1 | `ip_addr_type` | `uint8_t` | 0 - IPv4, 1 - IPv6 `whd/src/include/whd_wlioctl.h:4424` |
| 2 | 2 | `local_port` | `uint16_t` |  |
| 4 | 2 | `remote_port` | `uint16_t` |  |
| 6 | 2 | (pad) |  | alignment padding inserted by the compiler |
| 8 | 4 | `local_seq` | `uint32_t` |  |
| 12 | 4 | `remote_seq` | `uint32_t` |  |
| 16 | 2 | `request_len` | `uint16_t` | TCP keepalive request packet length `whd/src/include/whd_wlioctl.h:4429` |
| 18 | 2 | `response_len` | `uint16_t` | TCP keepalive response packet length `whd/src/include/whd_wlioctl.h:4430` |
| 20 | variable | `data` | `uint8_t[1]` | flexible tail declared as [1]; sizeof counts one element (1 byte); IPv4: local IP at +0, remote IP at +4, request packet at +8, response packet at +8+request_len; IPv6: local at +0, remote at +16, request at +32, response at +32+request_len (source comment) `whd/src/include/whd_wlioctl.h:4431` |
| 21 | 3 | (pad) |  | trailing alignment padding inserted by the compiler |

Size check: compiled

### `wl_ipv4_addr_t` (whd)
Embedded in wl_ol_cfg_v1_t.u.ol_inet_v4 and the wl_icmp_echo_req_* records `whd/src/include/whd_wlioctl.h:4552` `whd/src/include/whd_wlioctl.h:4683` `whd/src/include/whd_wlioctl.h:4696`; not packed (outside any `#pragma pack` region, natural alignment); 4 bytes, alignment 1, same on x86-64 and 32-bit ARM; no multi-byte integers, so no endianness; defined at `whd/src/include/whd_wlioctl.h:4447-4449`.
| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `addr` | `uint8_t[4]` | IPV4_ADDR_LEN = 4 `whd/inc/whd_types.h:104` |

Size check: compiled

### `wl_ipv6_addr_t` (whd)
Embedded in wl_ol_cfg_v1_t.u.ol_inet_v6 and the wl_icmp_echo_req_* records `whd/src/include/whd_wlioctl.h:4557` `whd/src/include/whd_wlioctl.h:4684` `whd/src/include/whd_wlioctl.h:4697`; not packed (outside any `#pragma pack` region, natural alignment); 16 bytes, alignment 1, same on x86-64 and 32-bit ARM; no multi-byte integers, so no endianness; defined at `whd/src/include/whd_wlioctl.h:4452-4454`.
| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 16 | `addr` | `uint8_t[16]` | IPV6_ADDR_LEN = 16 `whd/inc/whd_types.h:107` |

Size check: compiled

### `wl_tko_autoenab_t` (whd)
Sub-record carried in wl_tko_t.data of named variable "tko" (IOVAR_STR_TKO, `whd/src/include/whd_wlioctl.h:1264`), subcommand WL_TKO_SUBCMD_AUTOENAB (6): whd_tko_autoenab, `whd/src/whd_wifi_api.c:6467-6474`; Callers: whd_configure_tko_filter `whd/src/whd_wifi_api.c:1062` and whd_configure_tko_offload `whd/src/whd_wifi_api.c:1083`, the latter called from whd_wifi_offload_config `whd/src/whd_wifi_api.c:846`; not packed (outside any `#pragma pack` region, natural alignment); 8 bytes, alignment 2, same on x86-64 and 32-bit ARM; endianness not stated at the definition; version and length are assigned without htod at the use site `whd/src/whd_wifi_api.c:6472-6473`; defined at `whd/src/include/whd_wlioctl.h:4456-4461`.
| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 2 | `version` | `uint16_t` | WL_TKO_AUTO_VER = 1 `whd/src/include/whd_wlioctl.h:39` |
| 2 | 2 | `length` | `uint16_t` | remaining length after this field: REMAINING_LEN(tko_autoenab, wl_tko_autoenab_t, length) = 8 - 2 - 2 = 4 (`whd/src/whd_wifi_api.c:6473`; macro at `whd/inc/whd_wifi_api.h:41-42`; value compiled) |
| 4 | 1 | `enable` | `uint8_t` | 0: disable, 1: enable `whd/src/include/whd_wlioctl.h:4459` |
| 5 | 3 | `pad` | `uint8_t[3]` | explicit padding (declared field) `whd/src/include/whd_wlioctl.h:4460` |

Size check: compiled

### `wl_tko_autoconnect_t` (whd)
Sub-record carried in wl_tko_t.data of named variable "tko" (IOVAR_STR_TKO, `whd/src/include/whd_wlioctl.h:1264`), subcommand WL_TKO_SUBCMD_AUTOCONNECT (7) by name and by the comment 'get TCP auto connect info' `whd/src/include/whd_wlioctl.h:4321`; no use site in whd/src; not packed (outside any `#pragma pack` region, natural alignment); 56 bytes, alignment 4, same on x86-64 and 32-bit ARM; three fields use C 'bool', the header does not include stdbool.h itself, and the layout assumes sizeof(bool) == 1; little-endian (inferred: not stated at the definition, whd converts with htod16/htod32, which are identity on little-endian hosts and byte swaps on big-endian hosts `whd/src/include/whd_endian.h:45-55`); defined at `whd/src/include/whd_wlioctl.h:4463-4479`.
| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 2 | `version` | `uint16_t` |  |
| 2 | 2 | `length` | `uint16_t` |  |
| 4 | 1 | `index` | `uint8_t` |  |
| 5 | 1 | `is_enabled` | `bool` | C bool; 1 byte on the compilers tried `whd/src/include/whd_wlioctl.h:4467` |
| 6 | 1 | `filter` | `uint8_t` | the tx packets field to be filtered (TKO_FILTER_* bits, `whd/src/include/whd_wlioctl.h:40-44`) |
| 7 | 1 | `ip_addr_type` | `uint8_t` | source comment: valid only if allocated is TRUE; either ipv4 or ipv6 `whd/src/include/whd_wlioctl.h:4469` |
| 8 | 1 | `allocated` | `bool` | this wildcard has been allocated `whd/src/include/whd_wlioctl.h:4470` |
| 9 | 1 | `pkt_created` | `bool` |  |
| 10 | 2 | `pad` | `uint8_t[2]` | explicit padding (declared field) `whd/src/include/whd_wlioctl.h:4472` |
| 12 | 16 | `src_ip` | `uint8_t[16]` | ipv6/ipv4 shared `whd/src/include/whd_wlioctl.h:4473` |
| 28 | 16 | `dst_ip` | `uint8_t[16]` | ipv6/ipv4 shared `whd/src/include/whd_wlioctl.h:4474` |
| 44 | 2 | `local_port` | `uint16_t` |  |
| 46 | 2 | `remote_port` | `uint16_t` |  |
| 48 | 4 | `local_seq` | `uint32_t` |  |
| 52 | 4 | `remote_seq` | `uint32_t` |  |

Size check: compiled

### `wl_tko_filter_t` (whd)
Sub-record carried in wl_tko_t.data of named variable "tko" (IOVAR_STR_TKO, `whd/src/include/whd_wlioctl.h:1264`), subcommand WL_TKO_SUBCMD_FILTER (8): whd_tko_filter, `whd/src/whd_wifi_api.c:6509-6534`; public wrapper whd_configure_tko_filter `whd/src/whd_wifi_api.c:1053-1078` sends ENABLE(0), AUTOENAB(1), FILTER, ENABLE(1) in that order; fields not selected by filter_flag keep whatever the variable buffer held, since whd_tko_filter has no memset `whd/src/whd_wifi_api.c:6509-6540`; not packed (outside any `#pragma pack` region, natural alignment); 40 bytes, alignment 2, same on x86-64 and 32-bit ARM; endianness not stated at the definition; version/length/sport/dport are assigned without htod at the use site `whd/src/whd_wifi_api.c:6528-6534`, so host order (little-endian on a little-endian host; no swap would happen on a big-endian host); defined at `whd/src/include/whd_wlioctl.h:4481-4488`.
| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 2 | `version` | `uint16_t` | WL_TKO_AUTO_VER = 1 `whd/src/include/whd_wlioctl.h:39`, set at `whd/src/whd_wifi_api.c:6528` |
| 2 | 2 | `length` | `uint16_t` | remaining length after this field; whd writes 36 with REMAINING_LEN(wl_filter, wl_tko_autoenab_t, length) `whd/src/whd_wifi_api.c:6529`; the macro is sizeof(*(ptr)) - offsetof(type, member) - sizeof((ptr)->member) `whd/inc/whd_wifi_api.h:41-42`, so sizeof comes from the pointee (wl_tko_filter_t, 40) and only offsetof uses the named type; offsetof(length) is 2 in both records, giving 40 - 2 - 2 = 36 (compiled); naming wl_tko_autoenab_t there does not change the value (inferred) |
| 4 | 2 | `sport` | `uint16_t` | 0: wild card, else filter local port `whd/src/include/whd_wlioctl.h:4484` |
| 6 | 2 | `dport` | `uint16_t` | 0: wild card, else filter remote port `whd/src/include/whd_wlioctl.h:4485` |
| 8 | 16 | `ip_src` | `uint8_t[16]` | {0}: wild card, else filter src ip `whd/src/include/whd_wlioctl.h:4486` |
| 24 | 16 | `ip_dst` | `uint8_t[16]` | {0}: wild card, else filter dst ip `whd/src/include/whd_wlioctl.h:4487` |

Size check: compiled

### `wl_ol_cfg_v1_t` (whd)
Payload of SET named variable "offload_config" (IOVAR_STR_OFFLOAD_CONFIG, `whd/src/include/whd_wlioctl.h:1270`): whd_wifi_offload_config, profile `whd/src/whd_wifi_api.c:805-844`; whd_wifi_offload_ipv4_update `whd/src/whd_wifi_api.c:858-902`; whd_wifi_offload_ipv6_update `whd/src/whd_wifi_api.c:906-956`; whd_wifi_offload_enable, activate `whd/src/whd_wifi_api.c:960-997`; under PROTO_MSGBUF whd builds the header in an uninitialised stack copy and memcpy's it over the zeroed buffer, so union and pad bytes not set afterwards are indeterminate `whd/src/whd_wifi_api.c:825-829` `whd/src/whd_wifi_api.c:887-891` `whd/src/whd_wifi_api.c:940-944` `whd/src/whd_wifi_api.c:979-983`; not packed (outside any `#pragma pack` region, natural alignment); 32 bytes with a 1-byte whd_bool_t (the layout in the table; the declared pad[3]/pad[2] fields only fit that case), 40 bytes with a 4-byte enum whd_bool_t, alignment 4 in both; whd_bool_t is uint8_t when `__llvm__` is defined and an enum otherwise `whd/inc/whd_types.h:276-286`; compiled results are x86-64 clang 32 (the `__llvm__` branch), gcc -fshort-enums 32, gcc default 40, and 32-bit ARM clang 32 via the `__llvm__` branch, 32 with -U__llvm__ (enum branch, 1-byte enums by default on that target), 40 with -U__llvm__ -fno-short-enums; with the 4-byte whd_bool_t the (offset, size) pairs in table row order become (0,2) (2,2) (4,4) (8,28) (8,4) (12,4) (16,3) (8,4) (12,4) (16,3) (8,16) (24,1) (28,4) (32,2) (8,4) (12,3) (36,4) (compiled); which layout the firmware expects is not stated in these sources; bare-metal ARM GCC toolchains default to short enums (recalled, not in these sources); endianness not stated; fields assigned in host order without htod at the use sites `whd/src/whd_wifi_api.c:831-834`; defined at `whd/src/include/whd_wlioctl.h:4540-4569`.
| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 2 | `ver` | `uint16_t` | WL_OL_CFG_VER_1 = 1 `whd/src/include/whd_wlioctl.h:4520`; the activate path under PROTO_MSGBUF never sets ver `whd/src/whd_wifi_api.c:979-983` |
| 2 | 2 | `len` | `uint16_t` | sizeof(wl_ol_cfg_v1_t) `whd/src/whd_wifi_api.c:832` |
| 4 | 4 | `id` | `uint32_t` | wl_ol_cfg_id_t: PROF 1, INET_V4 2, INET_V6 3, ACTIVATE 4 `whd/src/include/whd_wlioctl.h:4522-4529` |
| 8 | 20 | `u` | `union` | union of the four alternatives below; all start at the same offset `whd/src/include/whd_wlioctl.h:4545-4566` |
| 8 | 4 | `u.ol_profile.type` | `uint32_t` | union alternative ol_profile (id PROF): wl_ol_prof_type_t LOW_PWR 1, MID_PWR 2, HIGH_PWR 3 `whd/src/include/whd_wlioctl.h:4531-4537`; for a profile reset whd sends type = -1 (0xFFFFFFFF) with reset = WHD_TRUE, otherwise type = WL_OL_PROF_TYPE_LOW_PWR `whd/src/whd_wifi_api.c:837-843` |
| 12 | 1 | `u.ol_profile.reset` | `whd_bool_t` | union alternative ol_profile `whd/src/include/whd_wlioctl.h:4548` |
| 13 | 3 | `u.ol_profile.pad` | `uint8_t[3]` | union alternative ol_profile; declared pad `whd/src/include/whd_wlioctl.h:4549` |
| 8 | 4 | `u.ol_inet_v4.host_ipv4` | `wl_ipv4_addr_t` | union alternative ol_inet_v4 (id INET_V4) `whd/src/include/whd_wlioctl.h:4552`; whd takes the address bytes least-significant byte first from its uint32_t argument `whd/src/whd_wifi_api.c:874-878` |
| 12 | 1 | `u.ol_inet_v4.del` | `whd_bool_t` | union alternative ol_inet_v4; 1: del 0: add `whd/src/include/whd_wlioctl.h:4553` |
| 13 | 3 | `u.ol_inet_v4.pad` | `uint8_t[3]` | union alternative ol_inet_v4; declared pad `whd/src/include/whd_wlioctl.h:4554` |
| 8 | 16 | `u.ol_inet_v6.host_ipv6` | `wl_ipv6_addr_t` | union alternative ol_inet_v6 (id INET_V6) `whd/src/include/whd_wlioctl.h:4557` |
| 24 | 1 | `u.ol_inet_v6.type` | `uint8_t` | union alternative ol_inet_v6; 0: unicast 1: anycast `whd/src/include/whd_wlioctl.h:4558` |
| 25 | 1 | `u.ol_inet_v6.del` | `whd_bool_t` | union alternative ol_inet_v6; 1: del 0: add `whd/src/include/whd_wlioctl.h:4559` |
| 26 | 2 | `u.ol_inet_v6.pad` | `uint8_t[2]` | union alternative ol_inet_v6; declared pad `whd/src/include/whd_wlioctl.h:4560` |
| 8 | 1 | `u.ol_activate.enable` | `whd_bool_t` | union alternative ol_activate (id ACTIVATE) `whd/src/include/whd_wlioctl.h:4563` |
| 9 | 3 | `u.ol_activate.pad` | `uint8_t[3]` | union alternative ol_activate; declared pad `whd/src/include/whd_wlioctl.h:4564` |
| 28 | 4 | `offload_skip` | `uint32_t` | bitmap of offloads to skip: WL_OL_ARP bit0, ND 1, BDO 2, ICMP 3, TKO 4, DLTRO 5, PNO 6, KEEPALIVE 7, GTKOE 8, WOWLPF 9 `whd/src/include/whd_wlioctl.h:4718-4727` |

Size check: compiled

### `wlc_csi_cfg_t` (whd)
Payload of named variable "csi" (IOVAR_STR_CSI, `whd/src/include/whd_wlioctl.h:1278`): SET at `whd/src/COMPONENT_WLANSENSE/whd_wlansense_api.c:113-115` `whd/src/COMPONENT_WLANSENSE/whd_wlansense_api.c:154-157`; GET at `whd/src/COMPONENT_WLANSENSE/whd_wlansense_core.c:321-327`; only compiled when COMPONENT_WLANSENSE is defined `whd/src/include/whd_wlioctl.h:4571-4603`; public alias whd_csi_cfg_t `whd/src/COMPONENT_WLANSENSE/whd_wlansense_api.h:62`; not packed (outside any `#pragma pack` region, natural alignment); 48 bytes, alignment 4, same on x86-64 and 32-bit ARM; endianness not stated at the definition; whd copies the caller's struct into the named variable buffer and the reply back out with memcpy, no htod/dtoh `whd/src/COMPONENT_WLANSENSE/whd_wlansense_api.c:115` `whd/src/COMPONENT_WLANSENSE/whd_wlansense_core.c:327`; defined at `whd/src/include/whd_wlioctl.h:4573-4598`.
| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 1 | `csi_enable` | `uint8_t` | 1: Enable CSI 0: Disable CSI `whd/src/include/whd_wlioctl.h:4574` |
| 1 | 3 | (pad) |  | alignment padding inserted by the compiler |
| 4 | 4 | `capture_period_ms` | `int32_t` | -1: disable periodic CSI capture `whd/src/include/whd_wlioctl.h:4576` |
| 8 | 2 | `capture_window_dur_ms` | `uint16_t` |  |
| 10 | 1 | `solicit_mode` | `uint8_t` | 0: Unsolicited 1: Solicited `whd/src/include/whd_wlioctl.h:4578` |
| 11 | 1 | `assoc_mode` | `uint8_t` | 0: Unassociated 1: Associated `whd/src/include/whd_wlioctl.h:4579` |
| 12 | 1 | `bss_mode` | `uint8_t` | source comment: 0 = all Rx allowed, 1 = my BSS, 2 = other BSS `whd/src/include/whd_wlioctl.h:4581` |
| 13 | 1 | `ignore_fcs` | `uint8_t` | also capture badfcs packets `whd/src/include/whd_wlioctl.h:4582` |
| 14 | 24 | `rx_macaddr` | `whd_mac_t[4]` | CSI_MAX_RX_MACADDR = 4 `whd/src/include/whd_wlioctl.h:4572`; unassociated mode only |
| 38 | 2 | `chanspec` | `chanspec_t` | unassociated mode only `whd/src/include/whd_wlioctl.h:4586` |
| 40 | 1 | `multi_csi_per_mac` | `uint8_t` | unsolicited mode only `whd/src/include/whd_wlioctl.h:4589` |
| 41 | 1 | `link_protection` | `uint8_t` | associated mode only `whd/src/include/whd_wlioctl.h:4592` |
| 42 | 1 | `subcarriers` | `uint8_t` | not implemented (source comment) `whd/src/include/whd_wlioctl.h:4595` |
| 43 | 2 | `frmtyp_subtyp` | `uint8_t[2]` | FrameType & SubType `whd/src/include/whd_wlioctl.h:4597` |
| 45 | 3 | (pad) |  | trailing alignment padding inserted by the compiler |

Size check: compiled

### `wl_wlan_sense_if_t` (whd)
Payload of SET named variable "csi_ifadd" (IOVAR_STR_CSI_IFADD, `whd/src/include/whd_wlioctl.h:1279`) at `whd/src/COMPONENT_WLANSENSE/whd_wlansense_core.c:307-310`; only compiled when COMPONENT_WLANSENSE is defined `whd/src/include/whd_wlioctl.h:4571-4603`; not packed (outside any `#pragma pack` region, natural alignment); 6 bytes, alignment 1, same on x86-64 and 32-bit ARM; no multi-byte integers, so no endianness; defined at `whd/src/include/whd_wlioctl.h:4600-4602`.
| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 6 | `csi_macaddr` | `whd_mac_t` | 6 octets `whd/inc/whd_types.h:551-554` |

Size check: compiled

### `wl_vif_event_t` (whd)
Event data of WLC_E_IF: handler registered for { WLC_E_IF } casts event_data to wl_vif_event_t `whd/src/COMPONENT_WLANSENSE/whd_wlansense_core.c:44` `whd/src/COMPONENT_WLANSENSE/whd_wlansense_core.c:231` `whd/src/COMPONENT_WLANSENSE/whd_wlansense_core.c:247`; not packed (outside any `#pragma pack` region, natural alignment); 5 bytes, alignment 1, same on x86-64 and 32-bit ARM; no multi-byte integers, so no endianness; defined at `whd/src/include/whd_wlioctl.h:4605-4611`.
| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 1 | `ifidx` | `uint8_t` |  |
| 1 | 1 | `action` | `uint8_t` | compared with WHD_IF_E_ADD `whd/src/COMPONENT_WLANSENSE/whd_wlansense_core.c:247` |
| 2 | 1 | `flags` | `uint8_t` |  |
| 3 | 1 | `bsscfgidx` | `uint8_t` |  |
| 4 | 1 | `role` | `uint8_t` |  |

Size check: compiled

### `secure_sess_info` (whd)
Response of GET named variable "wowl_secure_sess_info" (IOVAR_STR_WOWL_SEC_SESS_INFO, `whd/src/include/whd_wlioctl.h:1174`): whd_wowl_get_secure_session_status copies sizeof(struct secure_sess_info) from the response `whd/src/whd_wifi_api.c:6769-6785`; public alias secure_sess_info_t `whd/inc/whd_types.h:151`; not packed (outside any `#pragma pack` region, natural alignment); 24 bytes, alignment 4, same on x86-64 and 32-bit ARM; endianness not stated; response copied without dtoh swaps `whd/src/whd_wifi_api.c:6783`; defined at `whd/src/include/whd_wlioctl.h:4613-4618`.
| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `tcp_seq` | `uint32_t` |  |
| 4 | 4 | `tcp_ack` | `uint32_t` |  |
| 8 | 8 | `read_seq` | `uint8_t[8]` | TLS_MAX_SEQUENCE_LENGTH = 8 `whd/inc/whd_types.h:1484` |
| 16 | 8 | `write_seq` | `uint8_t[8]` | TLS_MAX_SEQUENCE_LENGTH = 8 `whd/src/include/whd_wlioctl.h:4617` |

Size check: compiled

### `wl_scanmac_t` (whd)
Header of named variable "scanmac" (IOVAR_STR_SCANMAC, `whd/src/include/whd_wlioctl.h:1281`): whd_configure_scanmac_randomisation, `whd/src/whd_wifi_api.c:6883-6904`; not packed (outside any `#pragma pack` region, natural alignment); variable size, 4 fixed bytes + flexible tail, sizeof 4, alignment 2, same on x86-64 and 32-bit ARM; little-endian: the use site applies htod16/htod32, identity on little-endian hosts and swap on big-endian `whd/src/include/whd_endian.h:45-55`; defined at `whd/src/include/whd_wlioctl.h:4620-4624`.
| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 2 | `subcmd_id` | `uint16_t` | WL_SCANMAC_SUBCMD_ENABLE 0, BSSCFG 1 (GET only), CONFIG 2 `whd/src/include/whd_wlioctl.h:4627-4629` |
| 2 | 2 | `len` | `uint16_t` | length of data[] only: whd sets sizeof(sub-record) `whd/src/whd_wifi_api.c:6895`; unlike wl_tko_t, len here excludes the 4-byte header, and the total sent is offsetof(data) + len `whd/src/whd_wifi_api.c:6899` |
| 4 | variable | `data` | `uint8_t[]` | C99 flexible array member; sub-record; contributes 0 bytes to sizeof `whd/src/include/whd_wlioctl.h:4623` |

Size check: compiled

### `wl_scanmac_enable_t` (whd)
Sub-record carried in wl_scanmac_t.data of named variable "scanmac", subcommand WL_SCANMAC_SUBCMD_ENABLE (0): `whd/src/whd_wifi_api.c:6893-6902`; not packed (outside any `#pragma pack` region, natural alignment); 4 bytes, alignment 1, same on x86-64 and 32-bit ARM; no multi-byte integers, so no endianness; defined at `whd/src/include/whd_wlioctl.h:4632-4635`.
| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 1 | `enable` | `uint8_t` | 1 - enable, 0 - disable `whd/src/include/whd_wlioctl.h:4633` |
| 1 | 3 | `pad` | `uint8_t[3]` | explicit padding (declared field) `whd/src/include/whd_wlioctl.h:4634`; whd builds the record in an uninitialised stack buffer and sets only enable, so the 3 pad bytes are not zeroed by the host `whd/src/whd_wifi_api.c:6888-6896` |

Size check: compiled

### `wl_scanmac_bsscfg_t` (whd)
Sub-record carried in wl_scanmac_t.data of named variable "scanmac", subcommand WL_SCANMAC_SUBCMD_BSSCFG (1, only GET supported) by name and comment `whd/src/include/whd_wlioctl.h:4628` `whd/src/include/whd_wlioctl.h:4637`; no use site in whd/src; not packed (outside any `#pragma pack` region, natural alignment); 4 bytes, alignment 4, same on x86-64 and 32-bit ARM; little-endian (inferred: not stated at the definition, whd converts with htod16/htod32, which are identity on little-endian hosts and byte swaps on big-endian hosts `whd/src/include/whd_endian.h:45-55`); defined at `whd/src/include/whd_wlioctl.h:4638-4640`.
| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `bsscfg` | `uint32_t` | bsscfg index `whd/src/include/whd_wlioctl.h:4639` |

Size check: compiled

### `wl_scanmac_config_t` (whd)
Sub-record carried in wl_scanmac_t.data of named variable "scanmac", subcommand WL_SCANMAC_SUBCMD_CONFIG (2) by name and comment `whd/src/include/whd_wlioctl.h:4629` `whd/src/include/whd_wlioctl.h:4642`; no use site in whd/src; not packed (outside any `#pragma pack` region, natural alignment); 16 bytes, alignment 2, same on x86-64 and 32-bit ARM; little-endian (inferred: not stated at the definition, whd converts with htod16/htod32, which are identity on little-endian hosts and byte swaps on big-endian hosts `whd/src/include/whd_endian.h:45-55`); defined at `whd/src/include/whd_wlioctl.h:4643-4648`.
| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 6 | `mac` | `struct ether_addr` | source comment: a MAC address or a MAC prefix (OUI), 6 bytes long `whd/src/include/whd_wlioctl.h:4644` |
| 6 | 6 | `random_mask` | `struct ether_addr` | randomized bits on each scan `whd/src/include/whd_wlioctl.h:4645` |
| 12 | 2 | `scan_bitmap` | `uint16_t` | WL_SCANMAC_SCAN_UNASSOC bit0, ASSOC_ROAM bit1, ASSOC_PNO bit2, ASSOC_HOST bit3 `whd/src/include/whd_wlioctl.h:4651-4654` |
| 14 | 2 | `pad` | `uint8_t[2]` | explicit padding (declared field) `whd/src/include/whd_wlioctl.h:4647` |

Size check: compiled

### `wl_icmp_echo_req_cmd_t` (whd)
Header of named variable "icmp_echo_req" (IOVAR_STR_ICMP_ECHO_REQ, `whd/src/include/whd_wlioctl.h:1289`), built in whd_wifi_icmp_echo_req_cmd_handler `whd/src/whd_wifi_api.c:6907-6965`; sub-record: 1 byte enable for ENAB, wl_icmp_echo_req_peer_config_t for ADD, wl_icmp_echo_req_peer_ip_t for DEL/START/STOP/INFO `whd/src/whd_wifi_api.c:6922-6940`; public entry points are whd_wifi_icmp_echo_req_enable `whd/src/whd_wifi_api.c:6999-7004`, _add `whd/src/whd_wifi_api.c:7006-7033`, _del `whd/src/whd_wifi_api.c:7035-7058`, _start `whd/src/whd_wifi_api.c:7060-7083`, _stop `whd/src/whd_wifi_api.c:7085-7108`, _get_info `whd/src/whd_wifi_api.c:7110-7134`; anonymous struct typedef; whd returns WHD_UNSUPPORTED unless its fwcap flag WHD_FWCAP_ICMP is set `whd/src/whd_wifi_api.c:6917-6920`; not packed (outside any `#pragma pack` region, natural alignment); variable size, 8 fixed bytes + flexible tail, sizeof 8, alignment 2, same on x86-64 and 32-bit ARM; endianness not stated; version/length assigned without htod at the use site `whd/src/whd_wifi_api.c:6957-6958`; defined at `whd/src/include/whd_wlioctl.h:4669-4675`.
| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 2 | `version` | `uint16_t` | WL_ICMP_ECHO_REQ_VER = 1 `whd/src/include/whd_wlioctl.h:4656` |
| 2 | 2 | `length` | `uint16_t` | whd sets header size + sub-record size `whd/src/whd_wifi_api.c:6948-6958`; that is sizeof(wl_icmp_echo_req_cmd_t) (8) + sub-record size: ENAB 9 (1-byte enable, `whd/src/whd_wifi_api.c:168` `whd/src/whd_wifi_api.c:6925`), ADD 48, DEL/START/STOP 32; for INFO 8 + sizeof(wl_icmp_echo_req_get_peer_info_t) = 52 while only 24 sub-record bytes are copied in `whd/src/whd_wifi_api.c:6948-6960` |
| 4 | 1 | `cmd_type` | `uint8_t` | wl_icmp_echo_req_cmd_type_t: ENAB 0, ADD 1, DEL 2, START 3, STOP 4, INFO 5 `whd/src/include/whd_wlioctl.h:4659-4666` |
| 5 | 3 | `pad` | `uint8_t[3]` | explicit padding (declared field) `whd/src/include/whd_wlioctl.h:4673` |
| 8 | variable | `data` | `uint8_t[]` | C99 flexible array member; sub-command record; contributes 0 bytes to sizeof `whd/src/include/whd_wlioctl.h:4674` |

Size check: compiled

### `wl_icmp_echo_req_peer_ip_t` (whd)
Sub-record of named variable "icmp_echo_req" (IOVAR_STR_ICMP_ECHO_REQ, `whd/src/include/whd_wlioctl.h:1289`) for DEL, START, STOP and INFO (`whd/src/whd_wifi_api.c:6934-6940`; static instance at `whd/src/whd_wifi_api.c:176-180`); filled by the del/start/stop/get_info wrappers, which set ip_ver, zero u over 16 bytes, then copy ipv4 or ipv6, e.g. `whd/src/whd_wifi_api.c:7042-7055`; not packed (outside any `#pragma pack` region, natural alignment); 24 bytes, alignment 2, same on x86-64 and 32-bit ARM; endianness not stated; no htod at the use site; defined at `whd/src/include/whd_wlioctl.h:4677-4686`.
| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 2 | `version` | `uint16_t` |  |
| 2 | 2 | `length` | `uint16_t` | sizeof this record `whd/src/whd_wifi_api.c:179` |
| 4 | 1 | `ip_ver` | `uint8_t` | IPv4:1 IPv6:2 `whd/src/include/whd_wlioctl.h:4680` |
| 5 | 3 | `pad` | `uint8_t[3]` | explicit padding (declared field) `whd/src/include/whd_wlioctl.h:4681` |
| 8 | 16 | `u` | `union` | union: ipv4 or ipv6, same offset `whd/src/include/whd_wlioctl.h:4682-4685` |
| 8 | 4 | `u.ipv4` | `wl_ipv4_addr_t` | union alternative, 4 bytes `whd/src/include/whd_wlioctl.h:4683` |
| 8 | 16 | `u.ipv6` | `wl_ipv6_addr_t` | union alternative, 16 bytes `whd/src/include/whd_wlioctl.h:4684` |

Size check: compiled

### `wl_icmp_echo_req_peer_config_t` (whd)
Sub-record of named variable "icmp_echo_req" (IOVAR_STR_ICMP_ECHO_REQ, `whd/src/include/whd_wlioctl.h:1289`) for ADD (`whd/src/whd_wifi_api.c:6929-6932`; static instance at `whd/src/whd_wifi_api.c:170-174`); also embedded in the INFO reply wl_icmp_echo_req_get_peer_info_t; filled by whd_wifi_icmp_echo_req_add with ip_ver, u zeroed over 16 bytes then ipv4 or ipv6 copied, mac_addr, periodicity, duration, no htod `whd/src/whd_wifi_api.c:7014-7030`; not packed (outside any `#pragma pack` region, natural alignment); 40 bytes, alignment 4, same on x86-64 and 32-bit ARM; endianness not stated; no htod at the use site; defined at `whd/src/include/whd_wlioctl.h:4688-4700`.
| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 2 | `version` | `uint16_t` |  |
| 2 | 2 | `length` | `uint16_t` | sizeof this record `whd/src/whd_wifi_api.c:173` |
| 4 | 1 | `ip_ver` | `uint8_t` | IPv4:1 IPv6:2 `whd/src/include/whd_wlioctl.h:4691` |
| 5 | 3 | `pad` | `uint8_t[3]` | explicit padding (declared field) `whd/src/include/whd_wlioctl.h:4692` |
| 8 | 4 | `periodicity` | `uint32_t` | period of ping in sec `whd/src/include/whd_wlioctl.h:4693` |
| 12 | 4 | `duration` | `uint32_t` | duration in sec `whd/src/include/whd_wlioctl.h:4694` |
| 16 | 16 | `u` | `union` | union: ipv4 or ipv6, same offset `whd/src/include/whd_wlioctl.h:4695-4698` |
| 16 | 4 | `u.ipv4` | `wl_ipv4_addr_t` | union alternative, 4 bytes `whd/src/include/whd_wlioctl.h:4696` |
| 16 | 16 | `u.ipv6` | `wl_ipv6_addr_t` | union alternative, 16 bytes `whd/src/include/whd_wlioctl.h:4697` |
| 32 | 6 | `mac_addr` | `uint8_t[6]` | peer MAC address `whd/src/include/whd_wlioctl.h:4699` |
| 38 | 2 | (pad) |  | trailing alignment padding inserted by the compiler |

Size check: compiled

### `wl_icmp_echo_req_get_peer_info_t` (whd)
Per-peer element of the INFO reply of named variable "icmp_echo_req" (IOVAR_STR_ICMP_ECHO_REQ, `whd/src/include/whd_wlioctl.h:1289`), read from wl_icmp_echo_req_get_info_t.data `whd/src/whd_wifi_api.c:6979-6992`; not packed (outside any `#pragma pack` region, natural alignment); 44 bytes, alignment 4, same on x86-64 and 32-bit ARM; endianness not stated; fields read without dtoh `whd/src/whd_wifi_api.c:6980-6983`; defined at `whd/src/include/whd_wlioctl.h:4703-4706`.
| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `state` | `uint32_t` | state of the peer `whd/src/include/whd_wlioctl.h:4704` |
| 4 | 40 | `config` | `wl_icmp_echo_req_peer_config_t` | 40 bytes including its 2 trailing pad bytes (at offsets 42-43 of this record); see that record `whd/src/include/whd_wlioctl.h:4705` |

Size check: compiled

### `wl_icmp_echo_req_get_info_t` (whd)
Reply of GET named variable "icmp_echo_req" (IOVAR_STR_ICMP_ECHO_REQ, `whd/src/include/whd_wlioctl.h:1289`) with cmd_type INFO `whd/src/whd_wifi_api.c:6969-6979`; whd reads enable, count and only the first peer entry `whd/src/whd_wifi_api.c:6977-6992`; not packed (outside any `#pragma pack` region, natural alignment); variable size, 8 fixed bytes + flexible tail, sizeof 8, alignment 2, same on x86-64 and 32-bit ARM; endianness not stated; fields read without dtoh `whd/src/whd_wifi_api.c:6977-6983`; defined at `whd/src/include/whd_wlioctl.h:4708-4715`.
| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 2 | `version` | `uint16_t` |  |
| 2 | 2 | `length` | `uint16_t` |  |
| 4 | 1 | `enable` | `uint8_t` | offload enable `whd/src/include/whd_wlioctl.h:4711` |
| 5 | 1 | `count` | `uint8_t` | peer count `whd/src/include/whd_wlioctl.h:4712` |
| 6 | 2 | `pad` | `uint8_t[2]` | explicit padding (declared field) `whd/src/include/whd_wlioctl.h:4713` |
| 8 | variable | `data` | `uint8_t[]` | C99 flexible array member; wl_icmp_echo_req_get_peer_info_t entries; contributes 0 bytes to sizeof `whd/src/include/whd_wlioctl.h:4714` |

Size check: compiled

### `whd_mac_t` (whd)
MAC address building block embedded in other records, e.g. whd_event_msg.addr (`whd/src/include/whd_events_int.h:492`), ethernet_header_t (`whd/src/include/whd_cdc_bdc.h:91-92`), whd_maclist_t (`whd/inc/whd_types.h:1144`) and pmkid_t (`whd/inc/whd_types.h:1154`), and sent or received on its own as the 6-byte payload of named variable (iovar) "cur_etheraddr" (IOVAR_STR_CUR_ETHERADDR, `whd/src/whd_wifi_api.c:3590-3594`) and as the reply of command WLC_GET_BSSID (`whd/src/whd_wifi_api.c:3619-3625`); not packed (single uint8_t array, alignment 1); 6 bytes; byte array, no multi-byte fields; defined at `whd/inc/whd_types.h:551-554`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 6 | `octet` | `uint8_t[6]` |  |

Size check: compiled (gcc 13.3, x86-64).

### `whd_ipv4_addr_t` (whd)
Union member of wl_icmp_echo_req_event_t (`whd/src/include/whd_events_int.h:540`); not packed (single uint8_t array, alignment 1); 4 bytes; byte array, no multi-byte fields; defined at `whd/inc/whd_types.h:559-562`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `addr` | `uint8_t[4]` | IPV4_ADDR_LEN = 4 (`whd/inc/whd_types.h:104`) |

Size check: compiled (gcc 13.3, x86-64).

### `whd_ipv6_addr_t` (whd)
Union member of wl_icmp_echo_req_event_t (`whd/src/include/whd_events_int.h:541`); not packed (single uint8_t array, alignment 1); 16 bytes; byte array, no multi-byte fields; defined at `whd/inc/whd_types.h:567-570`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 16 | `addr` | `uint8_t[16]` | IPV6_ADDR_LEN = 16 (`whd/inc/whd_types.h:107`) |

Size check: compiled (gcc 13.3, x86-64).

### `whd_list_t` (whd)
Request and reply buffer of command WLC_GET_VALID_CHANNELS: cast at `whd/src/whd_wifi_api.c:4237`, command issued at `whd/src/whd_wifi_api.c:4242`, reply cast at `whd/src/whd_wifi_api.c:4244`, buffer length sizeof(uint32_t) * (MAXCHANNEL + 1) (`whd/src/whd_wifi_api.c:4235`); not packed; variable size, 4 fixed bytes plus a flexible tail (sizeof with the one declared element is 8); little-endian for multi-byte fields, converted with htod*/dtoh*, which are identity unless IL_BIGENDIAN (`whd/src/include/whd_endian.h:44-62`); defined at `whd/inc/whd_types.h:575-579`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `count` | `uint32_t` | on request: maximum number of elements, htod32(MAXCHANNEL) (`whd/src/whd_wifi_api.c:4241`) |
| 4 | variable | `element` | `uint32_t[1]` | flexible tail, declared with length 1 (4 bytes as declared); one uint32 per channel; the reply is copied to the caller without byte swapping of the elements (`whd/src/whd_wifi_api.c:4245-4247`) |

Size check: compiled (gcc 13.3, x86-64).

### `whd_band_list_t` (whd)
Host-side copy of the WLC_GET_BANDLIST reply, never cast onto the command buffer: the command is issued with a plain uint32_t band_list[4] (`whd/src/whd_wifi_api.c:511`, `whd/src/whd_wifi_api.c:516`), which has the same 16-byte shape, and only number_of_bands is then copied from band_list[0] (`whd/src/whd_wifi_api.c:526`); not packed; 16 bytes; byte order not stated (band_list words are read with no conversion, `whd/src/whd_wifi_api.c:526` and `whd/src/whd_wifi_api.c:531`); defined at `whd/inc/whd_types.h:418-423`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `number_of_bands` | `uint32_t` | per the source comment, how many bands are supported, at present 1 or 2 |
| 4 | 4 | `current_band` | `uint32_t` | WLC_BAND_2G / 5G / 6G per the field comment; whd compares words band_list[1..number_of_bands] with WLC_BAND_6G/5G/2G (`whd/src/whd_wifi_api.c:529-539`), which supports reading the words after the count as band types |
| 8 | 8 | `other_band` | `uint32_t[2]` | the split of reply words 1..3 into current_band and other_band rests on the field comments only (inferred) |

Size check: compiled (gcc 13.3, x86-64).

### `wl_bss_info_t` (whd)
Scan result record inside wl_escan_result_t event data, bss_info = &eresult->bss_info[0] (`whd/src/whd_wifi_api.c:2639`), and reply to command WLC_GET_BSS_INFO, located 4 bytes into the reply (`whd/src/whd_wifi_api.c:3730` and `whd/src/whd_wifi_api.c:3733`; also `whd/src/whd_wifi_api.c:5436` and `whd/src/whd_wifi_api.c:5439`); not packed (defined after the '#pragma pack()' at `whd/inc/whd_types.h:904`; explicit reserved bytes keep natural alignment); variable size, 128 fixed bytes plus variable-length IEs; little-endian for multi-byte fields, converted with htod*/dtoh*, which are identity unless IL_BIGENDIAN (`whd/src/include/whd_endian.h:44-62`): dtoh32 on version (`whd/src/whd_wifi_api.c:2642`), dtoh16 on ie_offset and dtoh32 on ie_length (`whd/src/whd_wifi_api.c:2662-2663`); defined at `whd/inc/whd_types.h:926-964`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `version` | `uint32_t` | checked against WL_BSS_INFO_VERSION (`whd/src/whd_wifi_api.c:2643`) |
| 4 | 4 | `length` | `uint32_t` | 'byte length of data in this record, starting at version and including IEs' |
| 8 | 6 | `BSSID` | `whd_mac_t` |  |
| 14 | 2 | `beacon_period` | `uint16_t` | units Kusec per comment |
| 16 | 2 | `capability` | `uint16_t` |  |
| 18 | 1 | `SSID_len` | `uint8_t` |  |
| 19 | 32 | `SSID` | `uint8_t[32]` |  |
| 51 | 1 | `reserved1` | `uint8_t[1]` | explicit padding |
| 52 | 4 | `rateset.count` | `uint32_t` | anonymous struct 'rateset' (20 bytes) |
| 56 | 16 | `rateset.rates` | `uint8_t[16]` | rates in 500kbps units, high bit set if basic |
| 72 | 2 | `chanspec` | `wl_chanspec_t (uint16_t)` | typedef at `whd/inc/whd_types.h:918` |
| 74 | 2 | `atim_window` | `uint16_t` |  |
| 76 | 1 | `dtim_period` | `uint8_t` |  |
| 77 | 1 | `reserved2` | `uint8_t[1]` | explicit padding |
| 78 | 2 | `RSSI` | `int16_t` | dBm |
| 80 | 1 | `phy_noise` | `int8_t` | dBm |
| 81 | 1 | `n_cap` | `uint8_t` |  |
| 82 | 2 | `reserved3` | `uint8_t[2]` | explicit padding |
| 84 | 4 | `nbss_cap` | `uint32_t` |  |
| 88 | 1 | `ctl_ch` | `uint8_t` |  |
| 89 | 3 | `reserved4` | `uint8_t[3]` | explicit padding |
| 92 | 4 | `reserved32` | `uint32_t[1]` |  |
| 96 | 1 | `flags` | `uint8_t` |  |
| 97 | 1 | `vht_cap` | `uint8_t` |  |
| 98 | 2 | `reserved5` | `uint8_t[2]` | explicit padding |
| 100 | 16 | `basic_mcs` | `uint8_t[16]` | MCSSET_LEN = 16 (`whd/inc/whd_types.h:919`) |
| 116 | 2 | `ie_offset` | `uint16_t` | 'offset at which IEs start, from beginning'; the variable-length IEs follow the fixed part (comment at `whd/inc/whd_types.h:963`); the bounds check requires ie_offset >= sizeof(wl_bss_info_t) (`whd/src/whd_wifi_api.c:2664-2665`) |
| 118 | 2 | (pad) | `compiler padding` | padding inserted by natural alignment before ie_length |
| 120 | 4 | `ie_length` | `uint32_t` |  |
| 124 | 2 | `SNR` | `int16_t` |  |
| 126 | 2 | (pad) | `compiler tail padding` | tail padding to the struct alignment; counted in the 128 fixed bytes |

Size check: compiled (gcc 13.3, x86-64).

### `whd_maclist_t` (whd)
Request and reply of command WLC_GET_ASSOCLIST: buffer cast at `whd/src/whd_wifi_api.c:3684`, command at `whd/src/whd_wifi_api.c:3689`, the caller sizing the buffer as sizeof(uint32_t) + max_clients * sizeof(whd_mac_t) (`whd/src/whd_wifi_api.c:3498`), and a second caller building the same buffer in `whd/src/whd_ap.c:651-662` (PROTO_MSGBUF builds only, `whd/src/whd_ap.c:649`); pragma pack(1) (`whd/inc/whd_types.h:1120-1147`); variable size, 4 fixed bytes plus a flexible tail (sizeof with the one declared element is 10); little-endian for multi-byte fields, converted with htod*/dtoh*, which are identity unless IL_BIGENDIAN (`whd/src/include/whd_endian.h:44-62`); defined at `whd/inc/whd_types.h:1141-1145`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `count` | `uint32_t` | on request: capacity, htod32 of the caller's count (`whd/src/whd_wifi_api.c:3687`) |
| 4 | variable | `mac_list` | `whd_mac_t[1]` | flexible tail, declared with length 1 (6 bytes as declared); 6 bytes per entry |

Size check: compiled (gcc 13.3, x86-64).

### `mcast_list_t` (whd)
Value of the named variable "mcast_list" (IOVAR_STR_MCAST_LIST, `whd/src/include/whd_wlioctl.h:1080`), local to `whd/src/whd_wifi_api.c`: the get reply is cast to it in whd_wifi_register_multicast_address and whd_wifi_unregister_multicast_address (`whd/src/whd_wifi_api.c:3968`, `whd/src/whd_wifi_api.c:4025`), the get buffer being sized sizeof(uint32_t) + MAX_SUPPORTED_MCAST_ENTRIES (10) * sizeof(whd_mac_t) = 64 bytes (`whd/src/whd_wifi_api.c:3962-3964`, `whd/src/whd_wifi_api.c:4019-4021`, `whd/src/whd_wifi_api.c:57`), and the set value is built in it with one address added or removed (`whd/src/whd_wifi_api.c:3983-3995`, `whd/src/whd_wifi_api.c:4029-4055`); pragma pack(1) (`whd/src/whd_wifi_api.c:127-149`); variable size, 4 fixed bytes plus 6 bytes per address (sizeof with the one declared element is 10); little-endian entry_count, converted with dtoh32/htod32, which are identity unless IL_BIGENDIAN (`whd/src/include/whd_endian.h:44-62`); defined at `whd/src/whd_wifi_api.c:129-133`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `entry_count` | `uint32_t` | number of addresses that follow; dtoh32 on the reply (`whd/src/whd_wifi_api.c:3970`, `whd/src/whd_wifi_api.c:4026`), htod32 on the value sent (`whd/src/whd_wifi_api.c:3994`, `whd/src/whd_wifi_api.c:4054`); the set buffer is sized sizeof(uint32_t) + (entry_count ± 1) * sizeof(whd_mac_t) (`whd/src/whd_wifi_api.c:3983-3987`, `whd/src/whd_wifi_api.c:4029-4034`) |
| 4 | variable | `macs` | `whd_mac_t[1]` | flexible tail, declared with length 1 (6 bytes as declared); 6 bytes per entry (`whd/inc/whd_types.h:551-554`); both callers require a multicast address, ETHER_ISMULTI (`whd/src/whd_wifi_api.c:3950`, `whd/src/whd_wifi_api.c:4007`, `whd/src/whd_wifi_api.c:94`) |

Size check: compiled (gcc 13.3, x86-64).

### `pmkid_t` (whd)
Element of pmkid_list_t, the payload of named variable "pmkid_info" (`whd/src/whd_wifi_api.c:1203-1205`; name at `whd/src/include/whd_wlioctl.h:1249`); not packed (all members have alignment 1); 22 bytes; byte arrays, no multi-byte fields; defined at `whd/inc/whd_types.h:1152-1156`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 6 | `BSSID` | `whd_mac_t` |  |
| 6 | 16 | `PMKID` | `uint8_t[16]` | PMKID_LEN = 16 (`whd/inc/whd_types.h:93`) |

Size check: compiled (gcc 13.3, x86-64).

### `pmkid_list_t` (whd)
Payload of named variable "pmkid_info", get and set (IOVAR_STR_PMKID_INFO, `whd/src/include/whd_wlioctl.h:1249`): get buffer of sizeof(uint32_t) + MAXPMKID * sizeof(pmkid_t) at `whd/src/whd_wifi_api.c:1203-1205`, set buffer of sizeof(uint32_t) + n * sizeof(pmkid_t) at `whd/src/whd_wifi_api.c:1233-1237`; not packed; variable size, 4 fixed bytes plus a flexible tail (sizeof with the one declared element is 28: 4 + 22 rounded up to 4-byte alignment); little-endian for multi-byte fields, converted with htod*/dtoh*, which are identity unless IL_BIGENDIAN (`whd/src/include/whd_endian.h:44-62`): dtoh32 on npmkid at `whd/src/whd_wifi_api.c:1213`, htod32 at `whd/src/whd_wifi_api.c:1244`; defined at `whd/inc/whd_types.h:1158-1162`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `npmkid` | `uint32_t` | count; whd masks it with 0x0000FFFF, which its comment says tells the h1combo that the v1 pmkid_list_t is the one being used (`whd/src/whd_wifi_api.c:1207`, `whd/src/whd_wifi_api.c:1240`) |
| 4 | variable | `pmkid` | `pmkid_t[1]` | flexible tail, declared with length 1 (22 bytes as declared); 22 bytes per entry |
| 26 | 2 | (pad) | `compiler tail padding` | tail padding to the struct alignment; not sent, because whd sizes buffers as 4 + n * 22 (`whd/src/whd_wifi_api.c:1234-1236`) |

Size check: compiled (gcc 13.3, x86-64).

### `whd_auth_req_status_t` (whd)
Used in both directions: event data of WLC_E_EXT_AUTH_REQ (event 187, `whd/src/include/whd_events_int.h:173`), passed to the callback with length sizeof(whd_auth_req_status_t) at `whd/src/whd_wifi_api.c:3061-3074`, and payload that whd sets with named variable "auth_status" (IOVAR_STR_AUTH_STATUS, `whd/src/include/whd_wlioctl.h:1251`) at `whd/src/whd_wifi_api.c:5493-5497`, the header comment saying that the dongle and the host both use this structure: the dongle requests that the host begin auth(SAE), and the host reports the auth status back to the dongle (`whd/inc/whd_types.h:1164-1166`); not packed, with no compiler padding because flags (2) + peer_mac (6) puts ssid_len at offset 8; 60 bytes; byte order not stated (the struct is copied to the variable buffer without conversion, `whd/src/whd_wifi_api.c:5497`); defined at `whd/inc/whd_types.h:1168-1175`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 2 | `flags` | `uint16_t` | set to WL_EXTAUTH_SUCCESS or WL_EXTAUTH_FAIL before sending (`whd/src/whd_wifi_api.c:5498-5505`) |
| 2 | 6 | `peer_mac` | `whd_mac_t` |  |
| 8 | 4 | `ssid_len` | `uint32_t` |  |
| 12 | 32 | `ssid` | `uint8_t[32]` | SSID_NAME_SIZE = 32 (`whd/inc/whd_types.h:61`) |
| 44 | 16 | `pmkid` | `uint8_t[16]` | PMKID_LEN = 16 (`whd/inc/whd_types.h:93`) |

Size check: compiled (gcc 13.3, x86-64).

### `whd_auth_params_t` (whd)
Payload set with named variable "mgmt_frame" (IOVAR_STR_MGMT_FRAME, `whd/src/include/whd_wlioctl.h:1166`): buffer of OFFSET(whd_auth_params_t, data) + len at `whd/src/whd_wifi_api.c:4366-4368`, sent at `whd/src/whd_wifi_api.c:4373`, so whd sends 32 + len bytes; not packed; variable size, 32 fixed bytes plus a flexible tail (sizeof with the one declared element is 36); byte order not stated (the header is copied without conversion, `whd/src/whd_wifi_api.c:4370`); defined at `whd/inc/whd_types.h:1195-1206`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `version` | `uint32_t` |  |
| 4 | 4 | `dwell_time` | `uint32_t` | overwritten with MGMT_AUTH_FRAME_DWELL_TIME before sending (`whd/src/whd_wifi_api.c:4372`) |
| 8 | 2 | `len` | `uint16_t` | as sent: contents length with DOT11_MGMT_HDR_LEN subtracted, 'FW doesn't need MAC Header Length' (`whd/src/whd_wifi_api.c:4364-4365`) |
| 10 | 2 | `fc` | `uint16_t` |  |
| 12 | 2 | `channel` | `uint16_t` |  |
| 14 | 6 | `da` | `whd_mac_t` |  |
| 20 | 6 | `bssid` | `whd_mac_t` |  |
| 26 | 2 | (pad) | `compiler padding` | padding inserted by natural alignment between bssid and packetId |
| 28 | 4 | `packetId` | `uint32_t` |  |
| 32 | variable | `data` | `uint8_t[1]` | flexible tail, declared with length 1 (1 byte as declared); as sent it holds the frame body after the MAC header (`whd/src/whd_wifi_api.c:4371`) |
| 33 | 3 | (pad) | `compiler tail padding` | tail padding to the struct alignment; not sent, because whd sizes the buffer from the flexible member's offset (`whd/src/whd_wifi_api.c:4366`) |

Size check: compiled (gcc 13.3, x86-64).

### `whd_btc_lescan_params_t` (whd)
Payload set with named variable "btc_lescan_params" (IOVAR_STR_BTC_LESCAN_PARAMS, `whd/src/include/whd_wlioctl.h:1253`) at `whd/src/whd_wifi_api.c:5453-5454`, where only this inner struct of the host wrapper whd_coex_config_t (`whd/inc/whd_types.h:1444`) is sent; not packed (all uint16_t, no padding); 12 bytes; byte order not stated (passed straight to whd_wifi_set_iovar_buffer, `whd/src/whd_wifi_api.c:5453`); defined at `whd/inc/whd_types.h:1431-1439`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 2 | `priority` | `uint16_t` | LE scan priority |
| 2 | 2 | `duty_cycle` | `uint16_t` |  |
| 4 | 2 | `max_win` | `uint16_t` |  |
| 6 | 2 | `int_grant` | `uint16_t` |  |
| 8 | 2 | `scan_int` | `uint16_t` |  |
| 10 | 2 | `scan_win` | `uint16_t` |  |

Size check: compiled (gcc 13.3, x86-64).

### `ProtocolVersion` (whd)
First member of struct tls_param_info (`whd/inc/whd_types.h:1533`); not packed (all uint8_t); 4 bytes; byte fields only; defined at `whd/inc/whd_types.h:1526-1530`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 1 | `major` | `uint8_t` |  |
| 1 | 1 | `minor` | `uint8_t` |  |
| 2 | 2 | `padding` | `uint8_t[2]` | explicit padding |

Size check: compiled (gcc 13.3, x86-64).

### `tls_param_info_t` (whd)
Payload set with named variable "wowl_activate_secure" (IOVAR_STR_WOWL_ACTIVATE_SECURE, `whd/src/include/whd_wlioctl.h:1173`) at `whd/src/whd_wifi_api.c:6752-6756`, struct tag tls_param_info, a secure wake-on-WLAN feature (whether the CYW43439 firmware accepts it is not stated in these sources); not packed; 1360 bytes; byte order not stated (copied to the variable buffer without conversion, `whd/src/whd_wifi_api.c:6755`); defined at `whd/inc/whd_types.h:1532-1567`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `version` | `ProtocolVersion` |  |
| 4 | 4 | `compression_algorithm` | `uint32_t` |  |
| 8 | 4 | `cipher_algorithm` | `uint32_t` |  |
| 12 | 4 | `cipher_type` | `uint32_t` |  |
| 16 | 4 | `mac_algorithm` | `uint32_t` |  |
| 20 | 4 | `keepalive_interval` | `uint32_t` | seconds |
| 24 | 48 | `read_master_key` | `uint8_t[48]` | TLS_MAX_KEY_LENGTH (`whd/inc/whd_types.h:1481`) |
| 72 | 4 | `read_master_key_len` | `uint32_t` |  |
| 76 | 32 | `read_iv` | `uint8_t[32]` | TLS_MAX_IV_LENGTH (`whd/inc/whd_types.h:1483`) |
| 108 | 4 | `read_iv_len` | `uint32_t` |  |
| 112 | 32 | `read_mac_key` | `uint8_t[32]` | TLS_MAX_MAC_KEY_LENGTH (`whd/inc/whd_types.h:1482`) |
| 144 | 4 | `read_mac_key_len` | `uint32_t` |  |
| 148 | 8 | `read_sequence` | `uint8_t[8]` | TLS_MAX_SEQUENCE_LENGTH (`whd/inc/whd_types.h:1484`) |
| 156 | 4 | `read_sequence_len` | `uint32_t` |  |
| 160 | 48 | `write_master_key` | `uint8_t[48]` |  |
| 208 | 4 | `write_master_key_len` | `uint32_t` |  |
| 212 | 32 | `write_iv` | `uint8_t[32]` |  |
| 244 | 4 | `write_iv_len` | `uint32_t` |  |
| 248 | 32 | `write_mac_key` | `uint8_t[32]` |  |
| 280 | 4 | `write_mac_key_len` | `uint32_t` |  |
| 284 | 8 | `write_sequence` | `uint8_t[8]` |  |
| 292 | 4 | `write_sequence_len` | `uint32_t` |  |
| 296 | 4 | `tcp_ack_num` | `uint32_t` |  |
| 300 | 4 | `tcp_seq_num` | `uint32_t` |  |
| 304 | 4 | `local_ip` | `uint8_t[4]` |  |
| 308 | 4 | `remote_ip` | `uint8_t[4]` |  |
| 312 | 2 | `local_port` | `uint16_t` |  |
| 314 | 2 | `remote_port` | `uint16_t` |  |
| 316 | 6 | `local_mac_addr` | `uint8_t[6]` |  |
| 322 | 6 | `remote_mac_addr` | `uint8_t[6]` |  |
| 328 | 4 | `app_syncid` | `uint32_t` |  |
| 332 | 1024 | `payload` | `uint8_t[1024]` | TLS_MAX_PAYLOAD_LEN (`whd/inc/whd_types.h:1485`) |
| 1356 | 2 | `payload_len` | `uint16_t` |  |
| 1358 | 1 | `encrypt_then_mac` | `bool` | C99 bool; sizeof(bool) is implementation-defined, 1 byte in the compiled layout |
| 1359 | 1 | (pad) | `compiler tail padding` | tail padding to the struct alignment |

Size check: compiled (gcc 13.3, x86-64; a gcc -m32 compile gives the same 1360 bytes with bool = 1 byte).

### `whd_buffer_header_t` (whd)
Prefix of every packet buffer whd sends or receives, stripped on receive together with the SDPCM header (`whd/src/whd_sdpcm.c:413-414`), of which only the bus_header bytes reach the bus; pragma pack(1) (`whd/src/include/whd_types_int.h:194-210`); 8 bytes for a 4-byte host pointer and a 4-byte bus header, in the non-PROTO_MSGBUF variant shown (`whd/src/include/whd_types_int.h:196-201`; the PROTO_MSGBUF variant replaces bus_header with char pad[2], `whd/src/include/whd_types_int.h:203-207`); no byte order (host pointer and raw bytes); defined at `whd/src/include/whd_types_int.h:197-201`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `queue_next` | `whd_buffer_queue_ptr_t (void *)` | host only, not sent: next-packet link for the send queue (`whd/src/whd_sdpcm.c:679-696`); whd_buffer_queue_ptr_t is whd_buffer_t (`whd/inc/whd_types.h:1118`), which is void * (`whd/inc/whd_types.h:139`); size is the host pointer size, 4 bytes on a 32-bit MCU |
| 4 | 4 | `bus_header` | `char[MAX_BUS_HEADER_SIZE]` | space for the bus-specific header; MAX_BUS_HEADER_SIZE is 4 for SDIO and SPI builds (`whd/inc/whd_types.h:200` and `whd/inc/whd_types.h:202`), 8 for M2M/OCI (`whd/inc/whd_types.h:204` and `whd/inc/whd_types.h:206`); the gSPI command word is placed at the end of this area (`whd/src/bus_protocols/whd_bus_spi_protocol.c:335-337`) |

Size check: computed (for a 32-bit target with 4-byte pointers and MAX_BUS_HEADER_SIZE = 4; an x86-64 compile with 8-byte pointers gives 12; a gcc -m32 compile with _Static_assert gives 8).

### `whd_event_eth_hdr_t` (whd)
Second header of an event frame, member eth_evt_hdr of whd_event_t (`whd/src/include/whd_events_int.h:502`), defined a second time with identical members in the public header (`whd/inc/whd_events.h:138-145`; the two headers have different include guards, `whd/inc/whd_events.h:24` and `whd/src/include/whd_events_int.h:27`) and a third time as sdpcm_bcmeth_header_t ('Broadcom OUI', `whd/src/whd_sdpcm.c:105-112`); pragma pack(1) (`whd/src/include/whd_events_int.h:466-507`; `whd/inc/whd_events.h:133-186`); 10 bytes; byte order not stated for subtype, length and usr_subtype, which whd_process_bdc_event never reads, while whd's comment on the event message that follows says 'event data is stored in network endianness' (`whd/src/whd_cdc_bdc.c:841`); defined at `whd/src/include/whd_events_int.h:467-474`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 2 | `subtype` | `uint16_t` | 'Vendor specific..32769' |
| 2 | 2 | `length` | `uint16_t` | the public header comments it as 'Length of ethernet header' (`whd/inc/whd_events.h:141`) |
| 4 | 1 | `version` | `uint8_t` | 'Version is 0' |
| 5 | 3 | `oui` | `uint8_t[3]` | compared with BRCM_OUI "\x00\x10\x18" (`whd/src/whd_cdc_bdc.c:829`, `whd/src/whd_cdc_bdc.c:52`) |
| 8 | 2 | `usr_subtype` | `uint16_t` | 'user specific Data' |

Size check: compiled (gcc 13.3, x86-64).

### `whd_event_ether_header_t` (whd)
Ethernet header at the start of an event frame, member eth of whd_event_t (`whd/src/include/whd_events_int.h:501`), defined a second time with identical members in the public header (`whd/inc/whd_events.h:150-155`; the two headers have different include guards, `whd/inc/whd_events.h:24` and `whd/src/include/whd_events_int.h:27`); pragma pack(1) (`whd/src/include/whd_events_int.h:466-507`); 14 bytes; big-endian ethertype, read with ntoh16 at `whd/src/whd_cdc_bdc.c:812`; defined at `whd/src/include/whd_events_int.h:476-481`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 6 | `destination_address` | `whd_mac_t` |  |
| 6 | 6 | `source_address` | `whd_mac_t` |  |
| 12 | 2 | `ethertype` | `uint16_t` | must equal ETHER_TYPE_BRCM 0x886C for an event (`whd/src/whd_cdc_bdc.c:815`, `whd/src/whd_cdc_bdc.c:51`) |

Size check: compiled (gcc 13.3, x86-64).

### `whd_event_header_t` (whd)
Event message header, struct tag whd_event_msg, member whd_event of whd_event_t, delivered on the ASYNCEVENT_HEADER channel (`whd/src/whd_sdpcm.c:445-453`) and parsed in whd_process_bdc_event (`whd/src/whd_cdc_bdc.c:837-848`), defined a second time with identical members in the public header (`whd/inc/whd_events.h:160-173`; typedef at `whd/inc/whd_types.h:545`; the two headers have different include guards, `whd/inc/whd_events.h:24` and `whd/src/include/whd_events_int.h:27`); pragma pack(1) (`whd/src/include/whd_events_int.h:466-507`); 48 bytes; big-endian (network order) per whd's comment 'event data is stored in network endianness' (`whd/src/whd_cdc_bdc.c:841`), with ntoh16 on flags and ntoh32 on event_type, status, reason, auth_type and datalen at `whd/src/whd_cdc_bdc.c:843-848`, while version is not converted there; defined at `whd/src/include/whd_events_int.h:483-496`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 2 | `version` | `uint16_t` | not byte-swapped by whd_process_bdc_event (`whd/src/whd_cdc_bdc.c:843-848` convert only the six fields below); the twin struct sdpcm_raw_event_header_t, unioned with whd_event_header_t at `whd/src/whd_sdpcm.c:137-141`, carries the comment 'these fields are stored in network order' (`whd/src/whd_sdpcm.c:114`), which covers version too, and a comment saying that version 1 ends at ifname while version 2 carries every field, ifidx and bss_cfg_idx included (`whd/src/whd_sdpcm.c:118-119`) |
| 2 | 2 | `flags` | `uint16_t` |  |
| 4 | 4 | `event_type` | `uint32_t` | whd_event_num_t values |
| 8 | 4 | `status` | `uint32_t` | whd adds offsets for WLC_E_PSK_SUP, WLC_E_PRUNE, WLC_E_DISASSOC/DEAUTH after receipt (`whd/src/whd_cdc_bdc.c:867-880`); those offsets are host-side only |
| 12 | 4 | `reason` | `uint32_t` |  |
| 16 | 4 | `auth_type` | `uint32_t` | 'WLC_E_AUTH' |
| 20 | 4 | `datalen` | `uint32_t` | length of event data that follows; validated against the frame size (`whd/src/whd_cdc_bdc.c:851-852`) |
| 24 | 6 | `addr` | `whd_mac_t` | station address if applicable |
| 30 | 16 | `ifname` | `char[16]` | WHD_MSG_IFNAME_MAX = 16 (`whd/src/include/whd_events_int.h:444`) |
| 46 | 1 | `ifidx` | `uint8_t` | destination OS i/f index |
| 47 | 1 | `bsscfgidx` | `uint8_t` | source bsscfg index |

Size check: compiled (gcc 13.3, x86-64).

### `whd_event_t` (whd)
Whole event frame as it follows the BDC header, event = (whd_event_t *)&bdc_header[bdc_header->data_offset + 1] (`whd/src/whd_cdc_bdc.c:810`), with datalen bytes of event data after the struct ('data portion follows', `whd/src/include/whd_events_int.h:504`; DATA_AFTER_HEADER(event) at `whd/src/whd_cdc_bdc.c:897`), defined a second time with identical members in the public header (`whd/inc/whd_events.h:178-184`; the two headers have different include guards, `whd/inc/whd_events.h:24` and `whd/src/include/whd_events_int.h:27`); pragma pack(1) (`whd/src/include/whd_events_int.h:466-507`); variable size, 72 fixed bytes plus the event data; big-endian (network order), see the members (`whd/src/whd_cdc_bdc.c:841`); defined at `whd/src/include/whd_events_int.h:499-505`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 14 | `eth` | `whd_event_ether_header_t` |  |
| 14 | 10 | `eth_evt_hdr` | `whd_event_eth_hdr_t` |  |
| 24 | 48 | `whd_event` | `whd_event_header_t` |  |

Size check: compiled (gcc 13.3, x86-64).

### `wl_icmp_echo_req_event_t` (whd)
Event data of WLC_E_ICMP_ECHO_REQ (event 202, `whd/src/include/whd_events_int.h:183`), cast at `whd/src/whd_wifi_api.c:7151` and checked at `whd/src/whd_wifi_api.c:7160`, part of ICMP echo offload, which whd gates on the capability flag WHD_FWCAP_ICMP (`whd/src/whd_wifi_api.c:6917`; whether the CYW43439 firmware has it is not stated in these sources); not packed (defined after the '#pragma pack()' at `whd/src/include/whd_events_int.h:507`); 28 bytes; byte order not stated (version and echo_req_cnt are read without conversion, `whd/src/whd_wifi_api.c:7160` and `whd/src/whd_wifi_api.c:7163`); defined at `whd/src/include/whd_events_int.h:532-543`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 2 | `version` | `uint16_t` | must equal WL_ICMP_ECHO_REQ_EVENT_VER = 1 (`whd/src/include/whd_events_int.h:529`) |
| 2 | 2 | `length` | `uint16_t` |  |
| 4 | 1 | `ip_ver` | `uint8_t` | IPv4:1 IPv6:2 |
| 5 | 1 | `reason` | `uint8_t` | WLC_E_REASON_ICMP_ECHO_REQ_* 0/1/2 (`whd/src/include/whd_events_int.h:525-527`) |
| 6 | 2 | `pad` | `uint8_t[2]` | explicit padding |
| 8 | 4 | `echo_req_cnt` | `uint32_t` |  |
| 12 | 16 | `u` | `union { whd_ipv4_addr_t ipv4; whd_ipv6_addr_t ipv6; }` | union alternatives: 4-byte IPv4 or 16-byte IPv6 peer address; the union is 16 bytes (`whd/src/include/whd_events_int.h:539-542`) |

Size check: compiled (gcc 13.3, x86-64).

### `cdc_header_t` (whd)
Header of every command and named-variable request and response on the control channel: built at `whd/src/whd_cdc_bdc.c:207-243` and sent with CONTROL_HEADER (`whd/src/whd_cdc_bdc.c:261`), response parsed at `whd/src/whd_cdc_bdc.c:274-277` and `whd/src/whd_cdc_bdc.c:618-630`; for WLC_SET_VAR/WLC_GET_VAR whd builds the payload after the header as the NUL-terminated variable name followed by the data (`whd/src/whd_cdc_bdc.c:354-366`) and removes the zero bytes it put before the name for alignment before sending (`whd/src/whd_cdc_bdc.c:211-229`); pragma pack(1) (`whd/src/include/whd_cdc_bdc.h:71-96`); 16 bytes; little-endian for multi-byte fields, converted with htod*/dtoh*, which are identity unless IL_BIGENDIAN (`whd/src/include/whd_endian.h:44-62`): htod32 on cmd, len, flags at `whd/src/whd_cdc_bdc.c:233-238`, dtoh32 on flags, status at `whd/src/whd_cdc_bdc.c:276-277`; defined at `whd/src/include/whd_cdc_bdc.h:72-78`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `cmd` | `uint32_t` | 'ioctl command value' |
| 4 | 4 | `len` | `uint32_t` | 'lower 16: output buflen; upper 16: input buflen (excludes header)'; whd writes the plain data length (`whd/src/whd_cdc_bdc.c:234`) |
| 8 | 4 | `flags` | `uint32_t` | (id << 16) \| type \| (bss_index << 12) (`whd/src/whd_cdc_bdc.c:236-237`); CDCF_IOC_ERROR 0x01, CDCF_IOC_SET 0x02, IF mask 0xF000, ID mask 0xFFFF0000 (`whd/src/include/whd_cdc_bdc.h:37-46`) |
| 12 | 4 | `status` | `uint32_t` | 'status code returned from the device'; sent as 0 (`whd/src/whd_cdc_bdc.c:243`) |

Size check: compiled (gcc 13.3, x86-64).

### `bdc_header_t` (whd)
Header of data frames and event frames: tx at `whd/src/whd_cdc_bdc.c:458-495`, rx data at `whd/src/whd_cdc_bdc.c:711-715`, rx event at `whd/src/whd_cdc_bdc.c:779` and `whd/src/whd_cdc_bdc.c:810`; pragma pack(1) (`whd/src/include/whd_cdc_bdc.h:71-96`); 4 bytes, matching BDC_HEADER_LEN = 4 (`whd/src/include/whd_cdc_bdc.h:56`); byte fields only; defined at `whd/src/include/whd_cdc_bdc.h:80-87`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 1 | `flags` | `uint8_t` | sent as BDC_PROTO_VER (2) << BDC_FLAG_VER_SHIFT (4) (`whd/src/whd_cdc_bdc.c:471`, `whd/src/whd_cdc_bdc.c:41-42`) |
| 1 | 1 | `priority` | `uint8_t` | '802.1d Priority (low 3 bits)' (`whd/src/whd_cdc_bdc.c:484-488`) |
| 2 | 1 | `flags2` | `uint8_t` | sent as the bsscfg index (`whd/src/whd_cdc_bdc.c:491`); BDC_FLAG2_IF_MASK 0x0f (`whd/src/whd_cdc_bdc.c:43`) |
| 3 | 1 | `data_offset` | `uint8_t` | 'Offset from end of BDC header to packet data, in 4-uint8_t words' (`whd/src/include/whd_cdc_bdc.h:85`), i.e. 4-byte words; sent as 0 (`whd/src/whd_cdc_bdc.c:495`); on receive payload = 4 + (data_offset << 2) (`whd/src/whd_cdc_bdc.c:714-715`) |

Size check: compiled (gcc 13.3, x86-64).

### `ethernet_header_t` (whd)
Ethernet II header at the start of each data frame handed to whd_cdc_tx_queue_data (`whd/src/whd_cdc_bdc.c:423-437`), also the first member of struct bcm_event in `whd/src/whd_sdpcm.c:135`, with the same layout as whd_event_ether_header_t (`whd/src/include/whd_events_int.h:476-481`); pragma pack(1) (`whd/src/include/whd_cdc_bdc.h:71-96`); 14 bytes; big-endian ethertype, read with ntoh16 at `whd/src/whd_cdc_bdc.c:437`; defined at `whd/src/include/whd_cdc_bdc.h:89-94`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 6 | `destination_address` | `whd_mac_t` |  |
| 6 | 6 | `source_address` | `whd_mac_t` |  |
| 12 | 2 | `ethertype` | `uint16_t` |  |

Size check: compiled (gcc 13.3, x86-64).

### `bus_common_header_t` (whd)
Common prefix of control and data packets: rx at `whd/src/whd_sdpcm.c:342-344`, tx at `whd/src/whd_sdpcm.c:582-611`; no pragma at its definition (the pack(1) region starts at `whd/src/include/whd_sdpcm.h:81`), but both members have alignment 1, so there is no padding; 20 bytes for a 4-byte host pointer and MAX_BUS_HEADER_SIZE = 4 (SDIO/SPI); little-endian SDPCM frame tag inside bus_header on receive (dtoh16 at `whd/src/whd_sdpcm.c:346-347`), while on transmit the two frametag words are stored with no htod16 (`whd/src/whd_sdpcm.c:608-609`), i.e. in host order; defined at `whd/src/include/whd_sdpcm.h:75-79`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 8 | `buffer_header` | `whd_buffer_header_t` | host queue pointer (not sent) + bus-specific header bytes; see whd_buffer_header_t |
| 8 | 12 | `bus_header` | `uint8_t[12]` | BUS_HEADER_LEN = 12 (`whd/src/include/whd_sdpcm.h:54`): the SDPCM header (frame tag + software header), copied to/from an sdpcm_header_t at `whd/src/whd_sdpcm.c:344` and `whd/src/whd_sdpcm.c:611`. Breakdown per sdpcm_header_t (`whd/src/whd_sdpcm.c:99-103`, pack(1) from `whd/src/whd_sdpcm.c:73`): bytes 0-1 frametag[0] = frame size, bytes 2-3 frametag[1] = ~size (`whd/src/whd_sdpcm.c:608-609`), then the 8-byte sdpcm_sw_header_t (`whd/src/whd_sdpcm.c:85-94`): sequence, channel_and_flags, next_length, header_length, wireless_flow_control, bus_data_credit, _reserved[2] |

Size check: computed (for a 32-bit target with 4-byte pointers and MAX_BUS_HEADER_SIZE = 4; an x86-64 compile with 8-byte pointers gives 24; a gcc -m32 compile with _Static_assert gives 20).

### `control_header_t` (whd)
Full header of a command or named-variable request packet (`whd/src/whd_cdc_bdc.c:169` and `whd/src/whd_cdc_bdc.c:207`), followed by the payload (DATA_AFTER_HEADER, `whd/src/whd_cdc_bdc.c:214`), of which the last 32 bytes minus the unused part of the bus header go on the bus; pragma pack(1) (`whd/src/include/whd_sdpcm.h:81-94`); 36 bytes for a 4-byte host pointer and a 4-byte bus header, matching IOCTL_OFFSET = sizeof(whd_buffer_header_t) + 12 + 16 (`whd/src/include/whd_sdpcm.h:55`); byte order per member; defined at `whd/src/include/whd_sdpcm.h:82-86`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 20 | `common` | `bus_common_header_t` |  |
| 20 | 16 | `cdc_header` | `cdc_header_t` |  |

Size check: computed (for a 32-bit target with 4-byte pointers and MAX_BUS_HEADER_SIZE = 4; a gcc -m32 compile with _Static_assert gives 36).

### `data_header_t` (whd)
Full header prepended to each outgoing data frame (`whd/src/whd_cdc_bdc.c:448` and `whd/src/whd_cdc_bdc.c:458`); pragma pack(1) (`whd/src/include/whd_sdpcm.h:81-94`); 26 bytes for a 4-byte host pointer and a 4-byte bus header; byte order per member; defined at `whd/src/include/whd_sdpcm.h:88-93`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 20 | `common` | `bus_common_header_t` |  |
| 20 | 2 | `_padding` | `uint8_t[2]` | explicit 2 padding bytes between the SDPCM header and the BDC header; they are sent, and the SDPCM software header's data offset covers them: header_length = sizeof(sdpcm_header_t) + 2 for DATA_HEADER, sizeof(sdpcm_header_t) otherwise (`whd/src/whd_sdpcm.c:605-606`) |
| 22 | 4 | `bdc_header` | `bdc_header_t` |  |

Size check: computed (for a 32-bit target with 4-byte pointers and MAX_BUS_HEADER_SIZE = 4; a gcc -m32 compile with _Static_assert gives 26).

### `sdpcm_sw_header_t` (whd)
Software header of every frame on the bus, bytes 4-11 of the 12-byte frame header: member sw_header of sdpcm_header_t after the 4-byte frametag[2] (`whd/src/whd_sdpcm.c:99-103`), which whd copies to and from the bus_header bytes of bus_common_header_t (`whd/src/whd_sdpcm.c:344`, `whd/src/whd_sdpcm.c:542-544`, `whd/src/whd_sdpcm.c:611`); on receive whd_sdpcm_update_credit casts the frame data + 4 to it (`whd/src/whd_sdpcm.c:304`) and whd_sdpcm_process_rx_packet reads the channel and header length from it (`whd/src/whd_sdpcm.c:391`, `whd/src/whd_sdpcm.c:414`, `whd/src/whd_sdpcm.c:438`, `whd/src/whd_sdpcm.c:451`); on transmit whd_send_to_bus zeroes the whole header and sets three members (`whd/src/whd_sdpcm.c:603-607`); pragma pack(1) (`whd/src/whd_sdpcm.c:73-144`); 8 bytes; byte fields only; defined at `whd/src/whd_sdpcm.c:85-94`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 1 | `sequence` | `uint8_t` | 'Rx/Tx sequence number'; on transmit set to 0 when queued (`whd/src/whd_sdpcm.c:607`) and to tx_seq when the packet is taken for sending, tx_seq then incremented (`whd/src/whd_sdpcm.c:543-545`); no read of the received value found in `whd/src/whd_sdpcm.c` |
| 1 | 1 | `channel_and_flags` | `uint8_t` | the comment says '4 MSB Channel number, 4 LSB arbitrary flag', while the code takes the channel from the low 4 bits, & 0x0f (`whd/src/whd_sdpcm.c:308`, `whd/src/whd_sdpcm.c:391`); sent as the header type alone: CONTROL_HEADER 0, ASYNCEVENT_HEADER 1, DATA_HEADER 2 (`whd/src/whd_sdpcm.c:604`, `whd/src/include/whd_sdpcm.h:45-47`) |
| 2 | 1 | `next_length` | `uint8_t` | 'Length of next data frame, reserved for Tx'; sent as 0 (`whd/src/whd_sdpcm.c:603`); not read in `whd/src/whd_sdpcm.c` |
| 3 | 1 | `header_length` | `uint8_t` | 'Data offset': bytes from the start of the frame header to the body; sent as sizeof(sdpcm_header_t) + 2 = 14 for DATA_HEADER and sizeof(sdpcm_header_t) = 12 otherwise (`whd/src/whd_sdpcm.c:605-606`); on receive that many bytes are removed before the CDC or BDC layer (`whd/src/whd_sdpcm.c:412-414`, `whd/src/whd_sdpcm.c:436-438`) |
| 4 | 1 | `wireless_flow_control` | `uint8_t` | 'Flow control bits, reserved for Tx'; sent as 0 (`whd/src/whd_sdpcm.c:603`); on receive passed to whd_bus_set_flow_control (`whd/src/whd_sdpcm.c:320`) |
| 5 | 1 | `bus_data_credit` | `uint8_t` | 'Maximum Sequence number allowed by firmware for Tx'; sent as 0 (`whd/src/whd_sdpcm.c:603`); on receive, for channels below 3, becomes tx_max, replaced by tx_seq + 2 when it is more than 0x40 ahead of tx_seq (`whd/src/whd_sdpcm.c:308-317`) |
| 6 | 2 | `_reserved` | `uint8_t[2]` | 'Reserved'; sent as 0 (`whd/src/whd_sdpcm.c:603`) |

Size check: compiled (gcc 13.3, x86-64).

### `sdpcm_bcmeth_header_t` (whd)
Vendor event header, struct tag bcmeth_hdr, with the same members as whd_event_eth_hdr_t (`whd/src/include/whd_events_int.h:467-474`); its only use is as member bcmeth of sdpcm_bcm_event_t, between the Ethernet header and the event message (`whd/src/whd_sdpcm.c:133-142`), and no use of sdpcm_bcm_event_t was found in whd/src outside its definition: received events are parsed through whd_event_t instead (`whd/src/whd_cdc_bdc.c:810`); pragma pack(1) (`whd/src/whd_sdpcm.c:73-144`); 10 bytes; byte order not stated for this struct (the comment 'these fields are stored in network order' at `whd/src/whd_sdpcm.c:114` stands over the next struct, sdpcm_raw_event_header_t); defined at `whd/src/whd_sdpcm.c:105-112`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 2 | `subtype` | `uint16_t` | 'Vendor specific..32769' |
| 2 | 2 | `length` | `uint16_t` |  |
| 4 | 1 | `version` | `uint8_t` | 'Version is 0' |
| 5 | 3 | `oui` | `uint8_t[3]` | 'Broadcom OUI' |
| 8 | 2 | `usr_subtype` | `uint16_t` | 'user specific Data' |

Size check: compiled (gcc 13.3, x86-64).

### `country_chan_info_t` (whd)
Channel triplet inside country_info_ie_fixed_portion_t (`whd/src/include/whd_chip.h:175`), which whd treats as over-the-air IE content found in scan results, not a host-interface record (inferred); pragma pack(1) (`whd/src/include/whd_chip.h:142-344`); 3 bytes; byte fields only; defined at `whd/src/include/whd_chip.h:149-154`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 1 | `first_chan_num` | `uint8_t` |  |
| 1 | 1 | `num_chans` | `uint8_t` |  |
| 2 | 1 | `max_tx_pwr_level` | `uint8_t` |  |

Size check: compiled (gcc 13.3, x86-64).

### `whd_tlv8_header_t` (whd)
Generic 8-bit type / 8-bit length TLV header used to walk the IE area by whd_parse_tlvs / whd_tlv_find_tlv8 (`whd/src/whd_utils.c:106-135`); pragma pack(1) (`whd/src/include/whd_chip.h:142-344`); 2 bytes; byte fields only; defined at `whd/src/include/whd_chip.h:157-161`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 1 | `type` | `uint8_t` | IE id |
| 1 | 1 | `length` | `uint8_t` | length of the data that follows |

Size check: compiled (gcc 13.3, x86-64).

### `whd_tlv8_data_t` (whd)
Return type of whd_tlv_find_tlv8 (`whd/src/whd_utils.c:106`, `whd/src/whd_utils.c:122`); pragma pack(1) (`whd/src/include/whd_chip.h:142-344`); variable size, 2 fixed bytes plus a flexible tail (sizeof with the one declared element is 3); byte fields only; defined at `whd/src/include/whd_chip.h:163-168`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 1 | `type` | `uint8_t` |  |
| 1 | 1 | `length` | `uint8_t` |  |
| 2 | variable | `data` | `uint8_t[1]` | flexible tail, declared with length 1 (1 byte as declared) |

Size check: compiled (gcc 13.3, x86-64).

### `country_info_ie_fixed_portion_t` (whd)
802.11 country information element as carried in the IE area of a scan result (wl_bss_info_t at ie_offset; the IE area pointer is bss_info + ie_offset, `whd/src/whd_wifi_api.c:2771-2773`), found with DOT11_IE_ID_COUNTRY at `whd/src/whd_wifi_api.c:3002`, ccode read at `whd/src/whd_wifi_api.c:3005-3006`, with COUNTRY_INFO_IE_MINIMUM_LENGTH = 6 (`whd/src/include/whd_chip.h:147`); pragma pack(1) (`whd/src/include/whd_chip.h:142-344`); variable size, 5 fixed bytes plus a flexible tail (sizeof with the one declared element is 8); byte fields only; defined at `whd/src/include/whd_chip.h:170-176`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 2 | `tlv_header` | `whd_tlv8_header_t` | id, length |
| 2 | 2 | `ccode` | `char[2]` | two letter country code |
| 4 | 1 | `env` | `uint8_t` | indoor/outdoor environment |
| 5 | variable | `country_chan_info` | `country_chan_info_t[1]` | flexible tail, declared with length 1 (3 bytes as declared); 3 bytes per triplet |

Size check: compiled (gcc 13.3, x86-64).

### `supported_operating_classes_ie_t` (whd)
802.11 supported operating classes element as carried in the IE area of a scan result (wl_bss_info_t at ie_offset), found with DOT11_IE_ID_SUPPORTED_OPERATING_CLASSES at `whd/src/whd_wifi_api.c:3013` (inside #ifdef COMPONENT_WIFI6, `whd/src/whd_wifi_api.c:3011`); pragma pack(1) (`whd/src/include/whd_chip.h:142-344`); 258 bytes as declared at maximum size, the real element being shorter; byte fields only; defined at `whd/src/include/whd_chip.h:180-184`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 2 | `tlv_header` | `whd_tlv8_header_t` |  |
| 2 | 1 | `current_operating_class` | `uint8_t` |  |
| 3 | 255 | `operating_classes` | `uint8_t[255]` | DOT11_MAX_SUPPORTED_OPERATING_CLASSES = 255 (`whd/src/include/whd_chip.h:38`); only tlv_header.length bytes are present on the air |

Size check: compiled (gcc 13.3, x86-64).

### `rsn_ie_fixed_portion_t` (whd)
802.11 RSN element as carried in the IE area of a scan result (wl_bss_info_t at ie_offset; the IE area pointer is bss_info + ie_offset, `whd/src/whd_wifi_api.c:2771-2773`), found with DOT11_IE_ID_RSN at `whd/src/whd_wifi_api.c:2790`, with RSN_IE_MINIMUM_LENGTH = 8 (`whd/src/include/whd_chip.h:196`); pragma pack(1) (`whd/src/include/whd_chip.h:142-344`); variable size, 10 fixed bytes plus a flexible tail (sizeof with the one declared element is 14); mixed byte order as used by the parser, with no explicit statement in the header: the 4-byte suite selectors are read as big-endian (ntoh32(...) & 0xFF takes the last byte as sent as the suite type: group_key_suite at `whd/src/whd_wifi_api.c:2879`, pairwise_suite_list[a] at `whd/src/whd_wifi_api.c:2897`), pairwise_suite_count is read with no conversion (`whd/src/whd_wifi_api.c:2811`, `whd/src/whd_wifi_api.c:2817`), i.e. host order, little on a little-endian host, and version is never read; defined at `whd/src/include/whd_chip.h:187-194`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 2 | `tlv_header` | `whd_tlv8_header_t` |  |
| 2 | 2 | `version` | `uint16_t` |  |
| 4 | 4 | `group_key_suite` | `uint32_t` | 'See whd_80211_cipher_t for values' |
| 8 | 2 | `pairwise_suite_count` | `uint16_t` |  |
| 10 | variable | `pairwise_suite_list` | `uint32_t[1]` | flexible tail, declared with length 1 (4 bytes as declared); akm_suite_portion_t follows the last pairwise suite (`whd/src/whd_wifi_api.c:2817`) |

Size check: compiled (gcc 13.3, x86-64).

### `vendor_specific_ie_header_t` (whd)
802.11 vendor-specific element header as carried in the IE area of a scan result (wl_bss_info_t at ie_offset), checked by whd_is_wpa_ie (`whd/src/whd_utils.c:138-142`; call at `whd/src/whd_wifi_api.c:2800`), with VENDOR_SPECIFIC_IE_MINIMUM_LENGTH = 4 (`whd/src/include/whd_chip.h:204`); pragma pack(1) (`whd/src/include/whd_chip.h:142-344`); 6 bytes; byte fields only; defined at `whd/src/include/whd_chip.h:198-202`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 2 | `tlv_header` | `whd_tlv8_header_t` |  |
| 2 | 4 | `oui` | `uint8_t[4]` | 3-byte OUI + 1 type byte |

Size check: compiled (gcc 13.3, x86-64).

### `wpa_ie_fixed_portion_t` (whd)
802.11 WPA element as carried in the IE area of a scan result (wl_bss_info_t at ie_offset), found with DOT11_IE_ID_VENDOR_SPECIFIC at `whd/src/whd_wifi_api.c:2797-2798`, with WPA_IE_MINIMUM_LENGTH = 12 (`whd/src/include/whd_chip.h:216`); pragma pack(1) (`whd/src/include/whd_chip.h:142-344`); variable size, 14 fixed bytes plus a flexible tail (sizeof with the one declared element is 18); mixed byte order as used by the parser, with no explicit statement in the header: multicast_suite is read as big-endian (ntoh32(...) & 0xFF, `whd/src/whd_wifi_api.c:2924`), unicast_suite_list is a byte array whose 4th byte [a][3] is the cipher type (`whd/src/whd_wifi_api.c:2946`), unicast_suite_count is read with no conversion (`whd/src/whd_wifi_api.c:2917`, `whd/src/whd_wifi_api.c:2934`), i.e. host order, and version is never read; defined at `whd/src/include/whd_chip.h:207-214`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 6 | `vendor_specific_header` | `vendor_specific_ie_header_t` |  |
| 6 | 2 | `version` | `uint16_t` |  |
| 8 | 4 | `multicast_suite` | `uint32_t` |  |
| 12 | 2 | `unicast_suite_count` | `uint16_t` |  |
| 14 | variable | `unicast_suite_list` | `uint8_t[1][4]` | flexible tail, declared with length 1 (4 bytes as declared); 4 bytes per suite; akm_suite_portion_t follows (`whd/src/whd_wifi_api.c:2934`) |

Size check: compiled (gcc 13.3, x86-64).

### `akm_suite_portion_t` (whd)
AKM suite list that follows the pairwise/unicast suite list inside an RSN or WPA element (`whd/src/whd_wifi_api.c:2817` and `whd/src/whd_wifi_api.c:2934`); pragma pack(1) (`whd/src/include/whd_chip.h:142-344`); variable size, 2 fixed bytes plus a flexible tail (sizeof with the one declared element is 6); mixed byte order as used by the parser, with no explicit statement in the header: akm_suite_list[a] is read as big-endian (ntoh32(...) & 0xFF, `whd/src/whd_wifi_api.c:2821` and `whd/src/whd_wifi_api.c:2937`) and akm_suite_count is read with no conversion (`whd/src/whd_wifi_api.c:2819`, `whd/src/whd_wifi_api.c:2935`), i.e. host order; defined at `whd/src/include/whd_chip.h:218-222`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 2 | `akm_suite_count` | `uint16_t` |  |
| 2 | variable | `akm_suite_list` | `uint32_t[1]` | flexible tail, declared with length 1 (4 bytes as declared) |

Size check: compiled (gcc 13.3, x86-64).

### `rsnx_ie_t` (whd)
802.11 RSNX element as carried in the IE area of a scan result (wl_bss_info_t at ie_offset), found with DOT11_IE_ID_RSNX at `whd/src/whd_wifi_api.c:2963`; pragma pack(1) (`whd/src/include/whd_chip.h:142-344`); variable size, 2 fixed bytes plus a flexible tail (sizeof with the one declared element is 3); byte fields only; defined at `whd/src/include/whd_chip.h:225-229`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 2 | `tlv_header` | `whd_tlv8_header_t` |  |
| 2 | variable | `data` | `uint8_t[1]` | flexible tail, declared with length 1 (1 byte as declared); bit DOT11_RSNX_SAE_H2E (5) of data[0] is tested (`whd/src/whd_wifi_api.c:2964-2965`) |

Size check: compiled (gcc 13.3, x86-64).

### `extended_rates_t` (whd)
By name an extended supported rates element (inferred from the name only; no use site found in whd/src or whd/inc, so its role as a record sent or received is unverified); pragma pack(1) (`whd/src/include/whd_chip.h:142-344`); variable size, 2 fixed bytes plus a flexible tail (sizeof with the one declared element is 3); byte fields only; defined at `whd/src/include/whd_chip.h:231-235`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 2 | `tlv_header` | `whd_tlv8_header_t` |  |
| 2 | variable | `data` | `uint8_t[1]` | flexible tail, declared with length 1 (1 byte as declared) |

Size check: compiled (gcc 13.3, x86-64).

### `ht_capabilities_ie_t` (whd)
802.11 HT capabilities element as carried in the IE area of a scan result (wl_bss_info_t at ie_offset), found with DOT11_IE_ID_HT_CAPABILITIES at `whd/src/whd_wifi_api.c:2971`, its length required to equal HT_CAPABILITIES_IE_LENGTH (`whd/src/whd_wifi_api.c:2972`) = 26 (`whd/src/include/whd_types_int.h:64`); pragma pack(1) (`whd/src/include/whd_chip.h:142-344`); 28 bytes, the 2-byte TLV header plus 26 bytes of element body; byte order not stated: ht_capabilities_info is tested against the HT_CAPABILITIES_INFO_* bits with no conversion (`whd/src/whd_wifi_api.c:2976-2979`), i.e. host order, little on a little-endian host, and the other multi-byte fields are never read (recalled, not in these sources: 802.11 fields are little-endian); defined at `whd/src/include/whd_chip.h:242-254`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 2 | `tlv_header` | `whd_tlv8_header_t` |  |
| 2 | 2 | `ht_capabilities_info` | `uint16_t` | bit definitions at `whd/src/include/whd_chip.h:256-271` |
| 4 | 1 | `ampdu_parameters` | `uint8_t` |  |
| 5 | 10 | `rx_mcs` | `uint8_t[10]` |  |
| 15 | 2 | `rxhighest_supported_data_rate` | `uint16_t` |  |
| 17 | 1 | `tx_supported_mcs_set` | `uint8_t` |  |
| 18 | 3 | `tx_mcs_info` | `uint8_t[3]` |  |
| 21 | 2 | `ht_extended_capabilities` | `uint16_t` |  |
| 23 | 4 | `transmit_beam_forming_capabilities` | `uint32_t` |  |
| 27 | 1 | `antenna_selection_capabilities` | `uint8_t` |  |

Size check: compiled (gcc 13.3, x86-64).

### `hnd_log_t` (whd)
Console log descriptor, a memory-mapped record (not a packet) that whd reads from chip RAM over the backplane: sizeof(c->log) bytes at console_addr + offsetof(hnd_cons_t, log) (`whd/src/whd_chip.c:534-537`); pragma pack(1) (`whd/src/include/whd_chip.h:142-344`), all members 'uint' = unsigned int (typedef at `whd/src/include/whd_chip.h:273`); 16 bytes, assuming unsigned int is 32 bits; little-endian for multi-byte fields, converted with htod*/dtoh*, which are identity unless IL_BIGENDIAN (`whd/src/include/whd_endian.h:44-62`): dtoh32 on buf_size, idx, buf at `whd/src/whd_chip.c:551`, `whd/src/whd_chip.c:564`, `whd/src/whd_chip.c:585`; defined at `whd/src/include/whd_chip.h:274-280`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `buf` | `uint (32-bit)` | chip address of the console ring buffer; read from there at `whd/src/whd_chip.c:585-588` |
| 4 | 4 | `buf_size` | `uint (32-bit)` | ring buffer size (`whd/src/whd_chip.c:551`) |
| 8 | 4 | `idx` | `uint (32-bit)` | write index; whd polls for it to advance (`whd/src/whd_chip.c:564-579`) |
| 12 | 4 | `out_idx` | `uint (32-bit)` | 'output index' |

Size check: compiled (gcc 13.3, x86-64).

### `hnd_cons_t` (whd)
Console structure, a memory-mapped record (not a packet) that whd locates in chip RAM at wlan_shared_t.console_addr and uses only for offsetof(hnd_cons_t, log) (`whd/src/whd_chip.c:531-534`), never writing vcons_in or cbuf in these sources; pragma pack(1) (`whd/src/include/whd_chip.h:142-344`); 156 bytes; little-endian for multi-byte fields, converted with htod*/dtoh*, which are identity unless IL_BIGENDIAN (`whd/src/include/whd_endian.h:44-62`), shown for the embedded log member; defined at `whd/src/include/whd_chip.h:284-308`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `vcons_in` | `volatile uint (32-bit)` | virtual UART: host writes an input line into cbuf then its length here (comment `whd/src/include/whd_chip.h:286-291`) |
| 4 | 4 | `vcons_out` | `volatile uint (32-bit)` | 'currently unused' |
| 8 | 16 | `log` | `hnd_log_t` | output ring buffer descriptor |
| 24 | 4 | `cbuf_idx` | `uint (32-bit)` |  |
| 28 | 128 | `cbuf` | `char[128]` | CBUF_LEN = 128 (`whd/src/include/whd_chip.h:282`); console input line buffer |

Size check: compiled (gcc 13.3, x86-64).

### `wlan_shared_t` (whd)
Shared-info structure, a memory-mapped record (not a packet) that whd reads from chip RAM over the backplane with sizeof(wlan_shared_t) (`whd/src/whd_chip.c:493-494`), taking its address from the last word of RAM per whd's comment that the firmware puts the address of the wlan_shared_t struct into RAM's final word (`whd/src/whd_chip.c:937-939`); pragma pack(1) (`whd/src/include/whd_chip.h:142-344`); 68 bytes; little-endian for multi-byte fields, converted with htod*/dtoh*, which are identity unless IL_BIGENDIAN (`whd/src/include/whd_endian.h:44-62`): dtoh32 on only the first seven words, flags, trap_addr, assert_exp_addr, assert_file_addr, assert_line, console_addr and msgtrace_addr, at `whd/src/whd_chip.c:506-512`, of which flags and console_addr are the ones used in that function (`whd/src/whd_chip.c:515`, `whd/src/whd_chip.c:531`); defined at `whd/src/include/whd_chip.h:320-339`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `flags` | `uint (32-bit)` | low byte is the shared-struct version: mask 0x00ff, must be <= WLAN_SHARED_VERSION 0x0003 (`whd/src/whd_chip.c:70-71`, `whd/src/whd_chip.c:515`) |
| 4 | 4 | `trap_addr` | `uint (32-bit)` |  |
| 8 | 4 | `assert_exp_addr` | `uint (32-bit)` |  |
| 12 | 4 | `assert_file_addr` | `uint (32-bit)` |  |
| 16 | 4 | `assert_line` | `uint (32-bit)` |  |
| 20 | 4 | `console_addr` | `uint (32-bit)` | chip address of hnd_cons_t (`whd/src/whd_chip.c:531`) |
| 24 | 4 | `msgtrace_addr` | `uint (32-bit)` |  |
| 28 | 4 | `fwid` | `uint (32-bit)` |  |
| 32 | 4 | `total_lfrag_pktcount` | `uint (32-bit)` |  |
| 36 | 4 | `reserved` | `uint (32-bit)` |  |
| 40 | 4 | `reserved1` | `uint (32-bit)` |  |
| 44 | 4 | `h2d_mb_addr` | `uint (32-bit)` |  |
| 48 | 4 | `d2h_mb_addr` | `uint (32-bit)` |  |
| 52 | 4 | `ring_info_ptr` | `uint (32-bit)` |  |
| 56 | 4 | `scratch_mem_size` | `uint (32-bit)` |  |
| 60 | 4 | `scratch_mem_ptr_low` | `uint (32-bit)` |  |
| 64 | 4 | `scratch_mem_ptr_high` | `uint (32-bit)` |  |

Size check: compiled (gcc 13.3, x86-64).

### `whd_country_info_t` (whd)
Payload of command 320 WLC_SET_CUSTOM_COUNTRY (`whd/src/include/whd_wlioctl.h:4270`; see the entry for command 320), sent at `whd/src/whd_chip.c:801-810` in a buffer allocated 10 bytes larger than the struct (`whd/src/whd_chip.c:802-803`), and only when the chip id is 43362 (`whd/src/whd_chip.c:797`), so whd does not use it for CYW43439; pragma pack(1) (`whd/src/include/whd_chip.h:368-377`); 68 bytes; byte fields only; defined at `whd/src/include/whd_chip.h:370-375`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 3 | `abbrev` | `char[3]` |  |
| 3 | 1 | `rev` | `uint8_t` |  |
| 4 | 64 | `data` | `uint8_t[64]` |  |

Size check: compiled (gcc 13.3, x86-64).
