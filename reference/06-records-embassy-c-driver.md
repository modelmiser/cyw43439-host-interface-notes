# Wire records: embassy and c-driver

embassy's records and the layouts the c-driver builds by hand.

## embassy

### `SharedMemData` (embassy)
Shared-memory record that embassy reads over the backplane to find the firmware log console (feature `firmware-logs` only); `repr(C)`, not packed, 32 bytes; byte order not stated in the type: plain integers reinterpreted in place, so host order (little-endian on the supported targets); linux declares the same record `__le32`; defined at `embassy/structs.rs:48-58` `embassy/structs.rs:12-13` `embassy/runner.rs:717` `linux/brcmfmac/sdio.c:377-384`; embassy reads the record's address from the 32-bit word at atcm_ram_base + chip_ram_size - 4 - socram_srmem_size, then reads the record from that address `embassy/runner.rs:721-722` `embassy/runner.rs:725-727`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | flags | u32 | `embassy/structs.rs:50` |
| 4 | 4 | trap_addr | u32 | `embassy/structs.rs:51` |
| 8 | 4 | assert_exp_addr | u32 | `embassy/structs.rs:52` |
| 12 | 4 | assert_file_addr | u32 | `embassy/structs.rs:53` |
| 16 | 4 | assert_line | u32 | `embassy/structs.rs:54` |
| 20 | 4 | console_addr | u32 | address of the console record; embassy adds 8 to reach the log sub-record; the only field embassy uses `embassy/runner.rs:729` |
| 24 | 4 | msgtrace_addr | u32 | `embassy/structs.rs:56` |
| 28 | 4 | fwid | u32 | linux has `u8 tag[32]` at this offset instead `linux/brcmfmac/sdio.c:385` |

Size check: compiled
Differences: linux `struct sdpcm_shared_le`: linux continues after offset 28 with `tag[32]` and `brpt_addr`; embassy stops at 32 bytes. linux reads the address at `linux/brcmfmac/sdio.c:1043-1047`. `linux/brcmfmac/sdio.c:377` `linux/brcmfmac/sdio.c:365` `linux/brcmfmac/sdio.c:385-386`
Differences: whd `wlan_shared_t`: whd continues with 9 more 4-byte fields and reads `sizeof(wlan_shared_t)` bytes from the address found in the last RAM word. The record sits inside `#pragma pack(1)`; all fields are 4 bytes, so the layout is unchanged. `whd/src/include/whd_chip.h:320-339` `whd/src/include/whd_chip.h:330-338` `whd/src/include/whd_chip.h:142` `whd/src/include/whd_chip.h:344` `whd/src/whd_chip.c:483` `whd/src/whd_chip.c:493-494`
Differences: linux and whd disagree from offset 28 on: linux has `tag[32]`, whd has `fwid`. `linux/brcmfmac/sdio.c:385` `whd/src/include/whd_chip.h:320-339`
Differences: c-driver: no shared or console record found in `c-driver/cyw43_ll.c`.

### `SharedMemLog` (embassy)
Console log descriptor, read from `console_addr + 8`; `repr(C)`, not packed, 16 bytes; byte order not stated in the type: host order (little-endian on the supported targets); linux declares `__le32`; defined at `embassy/structs.rs:63-69` `embassy/structs.rs:12-13` `embassy/runner.rs:729` `embassy/runner.rs:735-737` `linux/brcmfmac/sdio.c:72-74`; the +8 skips two 4-byte fields, vcons_in and vcons_out, of the console record `whd/src/include/whd_chip.h:292-300` `linux/brcmfmac/sdio.c:88-89`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | buf | u32 | backplane address of the log ring buffer; embassy reads 1024 (0x400) bytes from it `embassy/runner.rs:748-749` |
| 4 | 4 | buf_size | u32 | embassy ignores it and always reads 1024 (0x400) bytes `embassy/runner.rs:748` |
| 8 | 4 | idx | u32 | write index into buf; embassy compares it with the last index it saw `embassy/runner.rs:739-742` |
| 12 | 4 | out_idx | u32 | linux has `char *_buf_compat` here; whd names it out_idx `linux/brcmfmac/sdio.c:75` `whd/src/include/whd_chip.h:279` |

Size check: compiled
Differences: whd computes the same address as console_addr + offsetof(hnd_cons_t, log). `whd/src/whd_chip.c:534`
Differences: linux `struct rte_log_le`: the fourth member is a host pointer, so its size depends on the host; only the first three `__le32` are wire data. `linux/brcmfmac/sdio.c:71-76`
Differences: whd record: `hnd_log_t`. `whd/src/include/whd_chip.h:274-280`
Differences: c-driver: not found in these sources.

### `SdpcmHeader` (embassy)
Header of every WLAN (F2) frame in both directions; `repr(C)`, not packed, no padding arises, 12 bytes; byte order not stated in the type: host order (little-endian on the supported targets); c-driver and whd also use plain uint16_t; linux builds both header words with cpu_to_le32 on a byte buffer; defined at `embassy/structs.rs:74-92` `embassy/structs.rs:12-13` `linux/brcmfmac/sdio.c:1499-1511` `linux/brcmfmac/sdio.c:1335-1351`; embassy builds it for commands and for tx data, and parses it on receive `embassy/runner.rs:1469-1479` `embassy/runner.rs:897-907` `embassy/structs.rs:96-128` `embassy/runner.rs:1152`; receive checks in embassy: len equals NOT len_inv, len equals the length reported by the bus, header_length is at least 12 and no more than the packet length `embassy/structs.rs:106-124`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 2 | len | u16 | frame length including this header `embassy/runner.rs:898` `embassy/runner.rs:1470` |
| 2 | 2 | len_inv | u16 | bitwise NOT of len; checked on receive `embassy/structs.rs:106` |
| 4 | 1 | sequence | u8 | rx/tx sequence number `embassy/structs.rs:78` |
| 5 | 1 | channel_and_flags | u8 | channel: 0 control, 1 event, 2 data. The source comment says channel in the 4 MSB, flags in the 4 LSB (wording as in whd), but embassy writes the channel number unshifted and on receive takes it from the low nibble (`& 0x0f`). linux masks the channel as the low nibble of this byte (0x00000f00 of the little-endian word). `embassy/consts.rs:156-158` `embassy/structs.rs:80` `whd/src/whd_sdpcm.c:88` `embassy/runner.rs:901` `embassy/runner.rs:1473` `embassy/runner.rs:1164` `embassy/runner.rs:1368` `linux/brcmfmac/sdio.c:1337-1338` |
| 6 | 1 | next_length | u8 | length of next data frame, reserved for tx, per source comment `embassy/structs.rs:82` |
| 7 | 1 | header_length | u8 | data offset from frame start; embassy sends 12 for control frames, 14 for data frames `embassy/structs.rs:84` `embassy/runner.rs:1475` `embassy/runner.rs:903` |
| 8 | 1 | wireless_flow_control | u8 | flow control bits, reserved for tx, per source comment `embassy/structs.rs:86` |
| 9 | 1 | bus_data_credit | u8 | highest tx sequence number allowed, per source comment. On receive embassy makes it the tx sequence limit for channels 0-2, clamped to seq + 2 when more than 64 (0x40) ahead. `embassy/structs.rs:88` `embassy/runner.rs:1367-1374`; after parsing, embassy consumes bus_data_credit and uses the channel to choose the next parser. `embassy/runner.rs:1158` `embassy/runner.rs:1164-1166` |
| 10 | 2 | reserved | [u8; 2] | `embassy/structs.rs:91` |

Size check: compiled
Differences: linux: no struct. linux uses a byte buffer of a 4-byte hardware header plus an 8-byte software header, with field masks. `linux/brcmfmac/sdio.c:1330-1351`
Differences: whd `sdpcm_header_t`: whd splits the same 12 bytes into `frametag[2]` plus `sdpcm_sw_header_t`, under `#pragma pack(1)`. `whd/src/whd_sdpcm.c:85-103` `whd/src/whd_sdpcm.c:73` `whd/src/whd_sdpcm.c:144`
Differences: c-driver record: `struct sdpcm_header_t`. `c-driver/cyw43_ll.c:754-764`

### `CdcHeader` (embassy)
Control-channel (command) header that follows `SdpcmHeader`; `repr(C, packed(2))`, 16 bytes; byte order not stated in the type: host order (little-endian on the supported targets); linux declares all four words `__le32`; defined at `embassy/structs.rs:132-139` `embassy/structs.rs:12-13` `linux/brcmfmac/bcdc.c:26-30`; packed(2) does not change the layout (no field would be padded); it lowers alignment to 2 (inferred from the compiled layout) `embassy/structs.rs:132`; embassy builds it, copies it to offset 12 of the frame, and parses it from responses `embassy/runner.rs:1481-1487` `embassy/runner.rs:1492` `embassy/structs.rs:162-173` `embassy/runner.rs:1168`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | cmd | u32 | command number `embassy/runner.rs:1482` |
| 4 | 4 | len | u32 | payload length. linux comment: lower 16 bits output buffer length, upper 16 bits input buffer length. On receive embassy cuts the payload slice to this length without a bounds check against the packet. `embassy/runner.rs:1483` `linux/brcmfmac/bcdc.c:27-28` `embassy/structs.rs:171` |
| 8 | 2 | flags | u16 | embassy writes kind \| iface << 12. linux: bit 0 error, bit 1 set, 0xF000 interface. `embassy/runner.rs:1484` `linux/brcmfmac/bcdc.c:34-37` |
| 10 | 2 | id | u16 | request id, incremented per command. In linux, whd and c-driver this is the upper 16 bits of one 32-bit flags word (mask 0xFFFF0000). embassy accepts a response only when id equals the last request id. `embassy/runner.rs:1467` `embassy/runner.rs:1485` `linux/brcmfmac/bcdc.c:38-39` `embassy/runner.rs:1173` |
| 12 | 4 | status | u32 | embassy sends 0. A non-zero status in a response is only logged, as a signed number. `embassy/runner.rs:1486` `embassy/runner.rs:1174-1176` |

Size check: compiled
Differences: linux `struct brcmf_proto_bcdc_dcmd`: embassy splits the 32-bit flags word into flags (u16) + id (u16); the bytes are the same on a little-endian host. `linux/brcmfmac/bcdc.c:25-31`
Differences: whd record: `cdc_header_t`, under `#pragma pack(1)`. `whd/src/include/whd_cdc_bdc.h:72-78` `whd/src/include/whd_cdc_bdc.h:71` `whd/src/include/whd_cdc_bdc.h:96`
Differences: c-driver record: `struct ioctl_header_t`; c-driver fills the single flags word as id << CDCF_IOC_ID_SHIFT \| kind \| iface << CDCF_IOC_IF_SHIFT. `c-driver/cyw43_ll.c:851-856` `c-driver/cyw43_ll.c:899-907`

### `BdcHeader` (embassy)
Header of data-channel and event-channel frames, after `SdpcmHeader` (plus 2 pad bytes on tx data); `repr(C)`, not packed, all single bytes, 4 bytes, endianness not applicable; defined at `embassy/structs.rs:181-189`; embassy builds it for tx data and parses it for events and for rx data `embassy/runner.rs:909-914` `embassy/structs.rs:193-208` `embassy/runner.rs:1189` `embassy/runner.rs:1353`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 1 | flags | u8 | protocol version in the high nibble: embassy sends 2 << 4 `embassy/structs.rs:176-177` `embassy/runner.rs:910` |
| 1 | 1 | priority | u8 | 802.1d priority, low 3 bits, per source comment `embassy/structs.rs:184` |
| 2 | 1 | flags2 | u8 | linux: low nibble is the interface index. embassy always sends 0; c-driver sends the interface number. `linux/brcmfmac/bcdc.c:54-55` `embassy/runner.rs:912` `c-driver/cyw43_ll.c:945` |
| 3 | 1 | data_offset | u8 | offset from the end of this header to the packet data, in 4-byte words `embassy/structs.rs:187` `embassy/structs.rs:202`; on receive embassy skips 4 * data_offset bytes after the header. `embassy/structs.rs:202-204`; embassy sizes its rx buffers for a data offset of one word. `embassy/lib.rs:56-57` |

Size check: compiled
Differences: linux record: `struct brcmf_proto_bcdc_header`. `linux/brcmfmac/bcdc.c:71-76`
Differences: whd record: `bdc_header_t`. `whd/src/include/whd_cdc_bdc.h:80-87`
Differences: c-driver record: `struct sdpcm_bdc_header_t`. `c-driver/cyw43_ll.c:920-925`

### `EthernetHeader` (embassy)
Ethernet header of an event frame; first member of `EventPacket`; `repr(C)`, not packed, alignment 2, no padding, 14 bytes; ether_type is big-endian on the wire; embassy swaps it in place; defined at `embassy/structs.rs:213-218` `embassy/structs.rs:329` `embassy/structs.rs:222-224`; embassy has no byte-conversion impl for this type; it is used only embedded in `EventPacket` `embassy/structs.rs:214`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 6 | destination_mac | [u8; 6] | `embassy/structs.rs:215` |
| 6 | 6 | source_mac | [u8; 6] | `embassy/structs.rs:216` |
| 12 | 2 | ether_type | u16 | big-endian; embassy drops the event unless it equals 34924 (0x886c) after the swap `embassy/runner.rs:1199-1206` |

Size check: compiled
Differences: linux: `struct ethhdr` as member `eth` of `struct brcmf_event`; the definition of `struct ethhdr` is not in these sources. `linux/brcmfmac/fweh.h:245`
Differences: whd records: `whd_event_ether_header_t` (inside `#pragma pack(1)`) and `ethernet_header_t`. `whd/src/include/whd_events_int.h:476-481` `whd/src/include/whd_events_int.h:466` `whd/src/include/whd_events_int.h:507` `whd/src/include/whd_cdc_bdc.h:89-94`
Differences: c-driver: no struct; it checks bytes 12-13 of the payload for 0x88 0x6c. `c-driver/cyw43_ll.c:1065-1066`

### `EventHeader` (embassy)
Vendor Ethernet header of an event frame; second member of `EventPacket`; `repr(C)`, not packed, alignment 2, no padding, 10 bytes; subtype, length and user_subtype are big-endian on the wire; embassy swaps them in place; linux declares them `__be16`; defined at `embassy/structs.rs:229-236` `embassy/structs.rs:330` `embassy/structs.rs:239-243` `linux/brcmfmac/fweh.h:216-220`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 2 | subtype | u16 | big-endian; embassy requires 32769; a whd comment gives the same value `embassy/runner.rs:1216-1220` `whd/src/include/whd_events_int.h:469` |
| 2 | 2 | length | u16 | big-endian `embassy/structs.rs:239-243` |
| 4 | 1 | version | u8 | `embassy/structs.rs:233` |
| 5 | 3 | oui | [u8; 3] | embassy requires 00:10:18 `embassy/runner.rs:1207-1215` |
| 8 | 2 | user_subtype | u16 | big-endian; embassy requires 1 `embassy/runner.rs:1222-1226` |

Size check: compiled
Differences: linux record: `struct brcm_ethhdr`, `__packed`. `linux/brcmfmac/fweh.h:215-221`
Differences: whd records: `whd_event_eth_hdr_t` and `sdpcm_bcmeth_header_t`. `whd/src/include/whd_events_int.h:467-474` `whd/src/whd_sdpcm.c:105-112`
Differences: c-driver: no struct; it checks only the OUI, at payload bytes 19-21 (5-7 of this header). `c-driver/cyw43_ll.c:1074`

### `EventMessage` (embassy)
Event message body; third member of `EventPacket`; `repr(C, packed(2))`, 48 bytes; all multi-byte fields are big-endian on the wire; embassy swaps them in place; linux declares `__be16`/`__be32`; a whd comment says the fields are in network order; defined at `embassy/structs.rs:248-272` `embassy/structs.rs:331` `embassy/structs.rs:315-323` `linux/brcmfmac/fweh.h:224-230` `whd/src/whd_sdpcm.c:114`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 2 | version | u16 | `embassy/structs.rs:251` |
| 2 | 2 | flags | u16 | `embassy/structs.rs:253` |
| 4 | 4 | event_type | u32 | embassy keeps only the low 8 bits `embassy/runner.rs:1228` |
| 8 | 4 | status | u32 | embassy keeps only the low 8 bits for its status enum; the full u32 is published with the event `embassy/runner.rs:1229` `embassy/runner.rs:1317` `embassy/runner.rs:1343` |
| 12 | 4 | reason | u32 | `embassy/structs.rs:259` |
| 16 | 4 | auth_type | u32 | `embassy/structs.rs:261` |
| 20 | 4 | datalen | u32 | length of the event data that follows the packet `embassy/structs.rs:356` |
| 24 | 6 | addr | [u8; 6] | station address `embassy/structs.rs:265` |
| 30 | 16 | ifname | [u8; 16] | `embassy/structs.rs:267` |
| 46 | 1 | ifidx | u8 | `embassy/structs.rs:269` |
| 47 | 1 | bsscfgidx | u8 | `embassy/structs.rs:271` |

Size check: compiled
Differences: linux record: `struct brcmf_event_msg_be`, `__packed`. `linux/brcmfmac/fweh.h:223-235`
Differences: whd records: `struct whd_event_msg` (inside `#pragma pack(1)`) and `sdpcm_raw_event_header_t`. `whd/src/include/whd_events_int.h:483-496` `whd/src/include/whd_events_int.h:466` `whd/src/include/whd_events_int.h:507` `whd/src/whd_sdpcm.c:115-130`
Differences: c-driver `cyw43_async_event_t`: same 48 bytes with unnamed filler: `_0` (version) at 0, flags at 2, event_type 4, status 8, reason 12, `_1[30]` covering auth_type, datalen, addr and ifname, interface at 46, `_2` at 47, a type-specific union at 48 (offsets compiled with gcc). c-driver byte-swaps only flags, event_type, status and reason. `c-driver/cyw43_ll.h:237-249` `c-driver/cyw43_ll.c:735-741`

### `EventPacket` (embassy)
Whole event frame carried after the BDC header on the event channel; `repr(C, packed(2))`, 72 bytes fixed plus `msg.datalen` bytes of event data; Ethernet type, vendor header and message are big-endian; embassy swaps them in place on parse; defined at `embassy/structs.rs:327-332` `embassy/structs.rs:354` `embassy/structs.rs:361-365`; embassy parses it, then validates it field by field `embassy/runner.rs:1194` `embassy/structs.rs:346-359` `embassy/runner.rs:1199-1226`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 14 | eth | EthernetHeader | see `EthernetHeader` `embassy/structs.rs:329` |
| 14 | 10 | hdr | EventHeader | see `EventHeader` `embassy/structs.rs:330` |
| 24 | 48 | msg | EventMessage | see `EventMessage` `embassy/structs.rs:331` |
| 72 | variable | (event data) | [u8] | msg.datalen bytes; not part of the struct; embassy's parser returns them `embassy/structs.rs:356` |

Size check: compiled
Differences: linux record: `struct brcmf_event`, `__packed`. `linux/brcmfmac/fweh.h:244-248`
Differences: whd records: `whd_event_t` and `sdpcm_bcm_event_t`. `whd/src/include/whd_events_int.h:499-505` `whd/src/whd_sdpcm.c:133-142`
Differences: c-driver: no struct for the whole packet. It checks the ether type at payload bytes 12-13 and the OUI 00:10:18 at bytes 19-21 in place, skips 24 bytes (Ethernet + vendor header), and casts the rest to `cyw43_async_event_t`. `c-driver/cyw43_ll.c:1065-1066` `c-driver/cyw43_ll.c:1074` `c-driver/cyw43_ll.c:1081-1082` `c-driver/cyw43_ll.c:735` `c-driver/cyw43_ll.h:237-249`

### `DownloadHeader` (embassy)
Header of the value of named variable (iovar) "clmload" (CLM blob download); `repr(C)`, not packed, no padding, 12 bytes fixed plus chunk data; byte order not stated in the type: host order (little-endian on the supported targets); linux declares `__le16`/`__le32`; defined at `embassy/structs.rs:369-375` `embassy/structs.rs:12-13` `linux/brcmfmac/fwil_types.h:1107-1110`; embassy sends "clmload\0" (8 bytes) + this header + chunk with SetVar, then reads "clmload_status" and requires 0 `embassy/control.rs:244-255` `embassy/control.rs:259`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 2 | flag | u16 | bits: NO_CRC 1 (0x0001), BEGIN 2 (0x0002), END 4 (0x0004), HANDLER_VER 4096 (0x1000) `embassy/structs.rs:379-382` |
| 2 | 2 | dload_type | u16 | CLM = 2 `embassy/structs.rs:385` |
| 4 | 4 | len | u32 | chunk length `embassy/control.rs:247` |
| 8 | 4 | crc | u32 | embassy sends 0 `embassy/control.rs:248` |
| 12 | variable | (data) | [u8] | len bytes; not in the embassy struct; embassy copies the chunk after the header. linux and whd declare a trailing data member. `embassy/control.rs:253` `linux/brcmfmac/fwil_types.h:1106-1112` `whd/src/include/whd_wlioctl.h:4167-4174` |

Size check: compiled
Differences: linux record: `struct brcmf_dload_data_le`; named variable "clmload". `linux/brcmfmac/fwil_types.h:1106-1112` `linux/brcmfmac/common.c:194`
Differences: whd `struct wl_dload_data`: it ends in `data[1]`, so sizeof is 16 with tail padding (compiled with gcc; the struct is outside the pack(1) regions of that file). `whd/src/include/whd_wlioctl.h:4167-4174` `whd/src/whd_clm.c:138` `whd/src/include/whd_wlioctl.h:3864-3918` `whd/src/include/whd_wlioctl.h:4188-4289`
Differences: c-driver: no struct; written field by field. `c-driver/cyw43_ll.c:1508-1517`

### `CountryInfo` (embassy)
Value of named variable "country", set during init; `repr(C)`, not packed, no padding, 12 bytes; byte order not stated in the type: host order (little-endian on the supported targets); linux declares rev `__le32`; defined at `embassy/structs.rs:389-394` `embassy/structs.rs:12-13` `embassy/control.rs:279-284` `linux/brcmfmac/fwil_types.h:766`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | country_abbrev | [u8; 4] | embassy sends two letters + two zero bytes `embassy/control.rs:280` |
| 4 | 4 | rev | i32 | embassy sends -1 when the configured revision is 0 `embassy/control.rs:282` |
| 8 | 4 | country_code | [u8; 4] | embassy sends the same two letters `embassy/control.rs:281` |

Size check: compiled
Differences: linux record: `struct brcmf_fil_country_le`, buffer size 4; named variable "country". `linux/brcmfmac/fwil_types.h:764-768` `linux/brcmfmac/fwil_types.h:146` `linux/brcmfmac/cfg80211.c:8494`
Differences: whd record: `wl_country_t`, buffer size 4. `whd/src/include/whd_wlioctl.h:668-673` `whd/src/include/whd_wlioctl.h:667`
Differences: c-driver: no struct. It builds the same layout by hand after the 8-byte name "country\0": abbrev as a le32 at +8, rev at +12 (0xFFFFFFFF when the revision is 0), code at +16; 20 bytes sent. `c-driver/cyw43_ll.c:2014-2022`

### `SsidInfo` (embassy)
Argument of command SetSsid (26), which starts the join; also embedded in `SsidInfoWithIndex`; `repr(C)`, not packed, no padding, 36 bytes; byte order not stated in the type: host order (little-endian on the supported targets); linux declares the length `__le32`; defined at `embassy/structs.rs:399-403` `embassy/structs.rs:12-13` `embassy/consts.rs:468` `embassy/control.rs:438-442` `embassy/control.rs:469` `linux/brcmfmac/fwil_types.h:358`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | len | u32 | SSID length `embassy/control.rs:438-442` |
| 4 | 32 | ssid | [u8; 32] | zero padded `embassy/control.rs:440-442` |

Size check: compiled
Differences: linux `struct brcmf_ssid_le`: same layout, but at BRCMF_C_SET_SSID linux sends the larger `struct brcmf_join_params`, which starts with it. `linux/brcmfmac/fwil_types.h:357-360` `linux/brcmfmac/cfg80211.c:1921-1922` `linux/brcmfmac/fwil_types.h:509-512`
Differences: whd record: `wlc_ssid_t`, filled and sent with WLC_SET_SSID. `whd/src/include/whd_wlioctl.h:496-500` `whd/src/whd_wifi_api.c:2478-2483`
Differences: c-driver: no struct. It builds a 36-byte buffer with a le32 length at 0 and the SSID at 4, and sends it with WLC_SET_SSID, length 36. `c-driver/cyw43_ll.c:2296-2297` `c-driver/cyw43_ll.c:2329` `c-driver/cyw43_ll.c:2342`

### `PassphraseInfo` (embassy)
Argument of command SetWsecPmk (268), for WPA/WPA2 join and AP start; `repr(C)`, not packed, alignment 2, no padding, 68 bytes; byte order not stated in the type: host order (little-endian on the supported targets); linux declares `__le16`; defined at `embassy/structs.rs:408-413` `embassy/structs.rs:12-13` `embassy/consts.rs:689` `embassy/control.rs:411-418` `embassy/control.rs:619-625` `linux/brcmfmac/fwil_types.h:585-586`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 2 | len | u16 | passphrase length `embassy/control.rs:411-418` |
| 2 | 2 | flags | u16 | embassy sets bit 0 when the key is a passphrase rather than a pre-hashed PMK; whd names bit 0 WSEC_PASSPHRASE `embassy/control.rs:407-410` `whd/src/include/whd_wlioctl.h:785` |
| 4 | 64 | passphrase | [u8; 64] | zero padded `embassy/control.rs:411-418` |

Size check: compiled
Differences: the record size differs between drivers. embassy: 68 bytes, key[64]. `embassy/structs.rs:409`
Differences: c-driver: no struct; le16 key_len at 0, le16 flags = 1 at 2, key at 4; sends 4 + 64 = 68 bytes. `c-driver/cyw43_ll.c:2252-2254` `c-driver/cyw43_ll.c:2258` `c-driver/cyw43_ll.c:277`
Differences: whd `wsec_pmk_t`: key[65], sizeof 70 with tail padding (compiled with gcc; outside the pack(1) regions of that file). `whd/src/include/whd_wlioctl.h:781` `whd/src/include/whd_wlioctl.h:786-791` `whd/src/whd_ap.c:502`
Differences: linux `struct brcmf_wsec_pmk_le`: key[128], sizeof 132 (compiled with gcc). `linux/brcmfmac/fwil_types.h:68` `linux/brcmfmac/fwil_types.h:584-588` `linux/brcmfmac/cfg80211.c:1730`

### `SaePassphraseInfo` (embassy)
Value of named variable "sae_password", for WPA3 join and AP start; `repr(C)`, not packed, alignment 2, no padding, 130 bytes; byte order not stated in the type: host order (little-endian on the supported targets); linux declares key_len `__le16`; defined at `embassy/structs.rs:418-422` `embassy/structs.rs:12-13` `embassy/control.rs:423-429` `embassy/control.rs:630-635` `linux/brcmfmac/fwil_types.h:597`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 2 | len | u16 | password length `embassy/control.rs:423-429` |
| 2 | 128 | passphrase | [u8; 128] | zero padded `embassy/control.rs:423-429` |

Size check: compiled
Differences: linux record: `struct brcmf_wsec_sae_pwd_le`. `linux/brcmfmac/fwil_types.h:596-599`
Differences: whd record: `wsec_sae_password_t`, maximum length 128; named variable set at `whd/src/whd_wifi_api.c:791-800`. `whd/src/include/whd_wlioctl.h:794-798` `whd/src/include/whd_wlioctl.h:793`
Differences: c-driver: no struct; le16 key_len at 0, key at 2; sends 2 + 128 bytes as "sae_password". `c-driver/cyw43_ll.c:2262-2264` `c-driver/cyw43_ll.c:2266` `c-driver/cyw43_ll.c:278`

### `SsidInfoWithIndex` (embassy)
Value of named variable "bsscfg:ssid" when starting an AP: a u32 bsscfg index in front of `SsidInfo`; `repr(C)`, not packed, no padding, 40 bytes; byte order not stated in the type: host order (little-endian on the supported targets); defined at `embassy/structs.rs:427-431` `embassy/structs.rs:12-13` `embassy/control.rs:575-583`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | index | u32 | bsscfg index; embassy sends 0 `embassy/control.rs:576` |
| 4 | 4 | ssid_info.len | u32 | SSID length `embassy/control.rs:575-583` |
| 8 | 32 | ssid_info.ssid | [u8; 32] | `embassy/control.rs:575-583` |

Size check: compiled
Differences: all three other drivers build the same 40-byte value for "bsscfg:ssid". linux: `struct brcmf_mbss_ssid_le` (bsscfgidx, SSID_len, SSID[32]). `linux/brcmfmac/fwil_types.h:751-755` `linux/brcmfmac/cfg80211.c:796-801`
Differences: whd: no struct; data[0] bsscfg index, data[1] SSID length, SSID from data[2]. `whd/src/whd_ap.c:412-417`
Differences: c-driver: no struct; le32 interface index at 0, le32 ssid_len at 4, 32-byte SSID at 8; 4 + 4 + 32 bytes. `c-driver/cyw43_ll.c:2382-2386`
Differences: linux's generic bsscfg helper adds the "bsscfg:" prefix and the index only when the index is non-zero. `linux/brcmfmac/fwil.c:259-260` `linux/brcmfmac/fwil.c:273-288`

### `EventMask` (embassy)
Value of named variable "bsscfg:event_msgs", set during init; `repr(C)`, not packed, no padding, 28 bytes; byte order not stated in the type: host order (little-endian on the supported targets); defined at `embassy/structs.rs:436-440` `embassy/structs.rs:12-13` `embassy/control.rs:305-319`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | iface | u32 | bsscfg index; embassy sends 0 `embassy/control.rs:306` |
| 4 | 24 | events | [u8; 24] | embassy treats bit N (byte N/8, bit N%8) as the enable for event N: it sets all bytes to 0xFF, then clears the bits of selected events. `embassy/structs.rs:444-447` `embassy/control.rs:307-317`; embassy clears PROBRESP_MSG twice. `embassy/control.rs:315-316` |

Size check: compiled
Differences: the mask length differs between drivers. embassy: 4-byte index + 24 mask bytes. `embassy/structs.rs:437`
Differences: c-driver: no struct; 4-byte index + 19 mask bytes; 18 in a commented-out variant. `c-driver/cyw43_ll.c:2051-2060` `c-driver/cyw43_ll.c:2292-2293`
Differences: whd: no struct; same "bsscfg:event_msgs" name, 4-byte index + 16 mask bytes. `whd/src/whd_events.c:290-300` `whd/src/whd_events.c:409-419` `whd/src/include/whd_wlioctl.h:1932`
Differences: linux: no struct; a raw bit array sized DIV_ROUND_UP(event code count, 8), sent as plain "event_msgs" with no index. `linux/brcmfmac/fweh.c:356-357` `linux/brcmfmac/fweh.c:462`
Differences: when any event number is above 127, whd switches to "bsscfg:event_msgs_ext" with `eventmsgs_ext_t`; embassy does not use it. `whd/src/whd_events.c:274-276` `whd/src/whd_events.c:304-323` `whd/src/include/whd_wlioctl.h:1056-1063`

### `ScanParams` (embassy)
Value of named variable "escan", which starts a scan; `repr(C)`, not packed, 2 bytes of tail padding, 76 bytes; byte order not stated in the type: host order (little-endian on the supported targets); linux declares `__le32`/`__le16`; defined at `embassy/structs.rs:453-469` `embassy/structs.rs:12-13` `embassy/control.rs:804-835` `linux/brcmfmac/fwil_types.h:461-463` `linux/brcmfmac/fwil_types.h:375-385`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | version | u32 | embassy sends 1; whd ESCAN_REQ_VERSION 1 `embassy/control.rs:805` `whd/src/include/whd_wlioctl.h:547` |
| 4 | 2 | action | u16 | embassy sends 1 = start; whd WL_SCAN_ACTION_START `embassy/control.rs:806` `whd/src/include/whd_wlioctl.h:522` |
| 6 | 2 | sync_id | u16 | embassy sends 1 `embassy/control.rs:807` |
| 8 | 4 | ssid_len | u32 | embassy sends 0 when no SSID is given `embassy/control.rs:808` |
| 12 | 32 | ssid | [u8; 32] | `embassy/structs.rs:459` |
| 44 | 6 | bssid | [u8; 6] | embassy default ff:ff:ff:ff:ff:ff `embassy/control.rs:817` |
| 50 | 1 | bss_type | u8 | embassy sends 2; whd names 2 WL_BSSTYPE_ANY. linux and whd type it signed 8-bit. `embassy/control.rs:818` `whd/src/include/whd_wlioctl.h:503` `linux/brcmfmac/fwil_types.h:371` `whd/src/include/whd_wlioctl.h:510` |
| 51 | 1 | scan_type | u8 | active or passive. whd and c-driver type it int8_t, linux u8. `embassy/control.rs:796-800` `embassy/control.rs:819` `whd/src/include/whd_wlioctl.h:511` `c-driver/cyw43_ll.h:263` `linux/brcmfmac/fwil_types.h:374` |
| 52 | 4 | nprobes | u32 | embassy's option is a u16; when unset embassy sends 65535 (0x0000FFFF), the u16 all-ones value widened to u32, not 0xFFFFFFFF. The linux comment gives -1 as "use default". `embassy/control.rs:83` `embassy/control.rs:820` `linux/brcmfmac/fwil_types.h:375` |
| 56 | 4 | active_time | u32 | `embassy/structs.rs:464` |
| 60 | 4 | passive_time | u32 | `embassy/structs.rs:465` |
| 64 | 4 | home_time | u32 | when unset embassy sends all ones (0xFFFFFFFF); the linux comment gives -1 as "use default" `embassy/control.rs:823` `linux/brcmfmac/fwil_types.h:382-384` |
| 68 | 4 | channel_num | u32 | embassy sends 0 = all channels. linux: low half channel count, high half SSID count. `embassy/control.rs:824` `linux/brcmfmac/fwil_types.h:385-395` |
| 72 | 2 | channel_list | [u16; 1] | one placeholder entry; embassy sends 0 `embassy/control.rs:825` |
| 74 | 2 | (pad) | u8[2] | tail padding to 4-byte alignment; sent on the wire because embassy's byte conversion covers size_of `embassy/structs.rs:8-13` `embassy/control.rs:835` |

Size check: compiled
Differences: linux `struct brcmf_escan_params_le`: linux nests the scan parameters (`struct brcmf_scan_params_le`) inside the escan header; embassy flattens version, action, sync_id and the scan parameters into one record. `linux/brcmfmac/fwil_types.h:460-468` `linux/brcmfmac/fwil_types.h:368` `linux/brcmfmac/cfg80211.c:1491`
Differences: whd `wl_escan_params_t`: nested the same way, containing `wl_scan_params_t`. `whd/src/include/whd_wlioctl.h:548-554` `whd/src/include/whd_wlioctl.h:506-518` `whd/src/whd_wifi_api.c:3320`
Differences: c-driver record: `cyw43_wifi_scan_options_t`, the same flat layout: size 76, channel_list at 72 (compiled with gcc), sent with sizeof, so the same 2 tail bytes go out. `c-driver/cyw43_ll.h:255-270` `c-driver/cyw43_ll.c:2202`

### `ScanResults` (embassy)
Header of the data of event ESCAN_RESULT when its status is PARTIAL; `BssInfo` follows; `repr(C, packed(2))`, 12 bytes fixed plus bss_count `BssInfo` records with their IEs; byte order not stated in the type: host order (little-endian on the supported targets); linux declares `__le32`/`__le16`; defined at `embassy/structs.rs:475-481` `embassy/structs.rs:12-13` `embassy/runner.rs:1320-1321` `linux/brcmfmac/fwil_types.h:471-474`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | buflen | u32 | `embassy/structs.rs:477` |
| 4 | 4 | version | u32 | `embassy/structs.rs:478` |
| 8 | 2 | sync_id | u16 | `embassy/structs.rs:479` |
| 10 | 2 | bss_count | u16 | `embassy/structs.rs:480` |
| 12 | variable | (bss_info) | BssInfo[...] | not in the struct; embassy's parser returns the rest `embassy/structs.rs:485-498`; embassy parses only the first `BssInfo` after the header. `embassy/runner.rs:1321-1327` `embassy/runner.rs:1324` |

Size check: compiled
Differences: linux record: `struct brcmf_escan_result_le`, bss_info_le member at offset 12 (compiled with gcc). `linux/brcmfmac/fwil_types.h:470-476`
Differences: whd record: `wl_escan_result_t`. `whd/src/include/whd_wlioctl.h:556-563`
Differences: c-driver: a local `struct _scan_result_t` (buflen, version, sync_id, bss_count, then the bss record), read at event + 48. `cyw43_ev_scan_result_t` is the host-side summary, not this header. `c-driver/cyw43_ll.c:669-675` `c-driver/cyw43_ll.h:222-234`

### `BssInfo` (embassy)
One scan result inside the ESCAN_RESULT (status PARTIAL) event data, after `ScanResults`; `repr(C, packed(2))` with explicit reserved fields standing in for natural-alignment padding, 128 bytes fixed plus information elements; byte order not stated in the type: host order (little-endian on the supported targets); linux declares `__le32`/`__le16`; defined at `embassy/structs.rs:505-569` `embassy/structs.rs:12-13` `linux/brcmfmac/fwil_types.h:315-345`; embassy's own test asserts 116 / 120 / 124 / 128 `embassy/structs.rs:579-586`; embassy parses it and hands it to the user as a BssInfo payload, consumed by the scanner `embassy/runner.rs:1324` `embassy/structs.rs:602-610` `embassy/runner.rs:1327` `embassy/control.rs:917-924`; reserved6 and reserved7 are explicit padding described by source comments; whether other embassy versions carry them is not found in these sources `embassy/structs.rs:556-560` `embassy/structs.rs:565-567`; a record version "109" is named only in source comments `embassy/structs.rs:556` `embassy/structs.rs:590`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | version | u32 | `embassy/structs.rs:509` |
| 4 | 4 | length | u32 | byte length of this record including IEs, per linux comment `linux/brcmfmac/fwil_types.h:316-318` |
| 8 | 6 | bssid | [u8; 6] | `embassy/structs.rs:513` |
| 14 | 2 | beacon_period | u16 | `embassy/structs.rs:515` |
| 16 | 2 | capability | u16 | `embassy/structs.rs:517` |
| 18 | 1 | ssid_len | u8 | `embassy/structs.rs:519` |
| 19 | 32 | ssid | [u8; 32] | `embassy/structs.rs:521` |
| 51 | 1 | reserved1 | [u8; 1] | (pad) explicit, before the 4-byte rateset count `embassy/structs.rs:522` |
| 52 | 4 | rateset_count | u32 | `embassy/structs.rs:524` |
| 56 | 16 | rates | [u8; 16] | 500 kbps units, per source comments `embassy/structs.rs:525` `linux/brcmfmac/fwil_types.h:326` |
| 72 | 2 | chanspec | u16 | `embassy/structs.rs:528` |
| 74 | 2 | atim_window | u16 | `embassy/structs.rs:530` |
| 76 | 1 | dtim_period | u8 | `embassy/structs.rs:532` |
| 77 | 1 | reserved2 | [u8; 1] | (pad) explicit `embassy/structs.rs:533` |
| 78 | 2 | rssi | i16 | dBm, per source comments; linux types it `__le16` `embassy/structs.rs:534` `linux/brcmfmac/fwil_types.h:331` |
| 80 | 1 | phy_noise | i8 | `embassy/structs.rs:537` |
| 81 | 1 | n_cap | u8 | `embassy/structs.rs:539` |
| 82 | 2 | reserved3 | [u8; 2] | (pad) explicit `embassy/structs.rs:540` |
| 84 | 4 | nbss_cap | u32 | `embassy/structs.rs:542` |
| 88 | 1 | ctl_ch | u8 | `embassy/structs.rs:544` |
| 89 | 3 | reserved4 | [u8; 3] | (pad) explicit `embassy/structs.rs:545` |
| 92 | 4 | reserved32 | [u32; 1] | `embassy/structs.rs:546` |
| 96 | 1 | flags | u8 | `embassy/structs.rs:548` |
| 97 | 1 | vht_cap | u8 | linux has reserved[3] covering offsets 97-99 instead `linux/brcmfmac/fwil_types.h:340` |
| 98 | 2 | reserved5 | [u8; 2] | `embassy/structs.rs:551` |
| 100 | 16 | basic_mcs | [u8; 16] | `embassy/structs.rs:553` |
| 116 | 2 | ie_offset | u16 | offset of the IEs from the start of the record, per linux comment `linux/brcmfmac/fwil_types.h:343`; a source comment says a CYW43439 reports ie_offset 128 for these records; no code in these sources checks it. `embassy/structs.rs:565-566` |
| 118 | 2 | reserved6 | [u8; 2] | (pad) explicit; a source comment explains it as the natural-alignment padding between ie_offset and ie_length `embassy/structs.rs:556-560` |
| 120 | 4 | ie_length | u32 | `embassy/structs.rs:562` |
| 124 | 2 | snr | i16 | `embassy/structs.rs:564` |
| 126 | 2 | reserved7 | [u8; 2] | (pad) explicit tail padding `embassy/structs.rs:565-567` |
| ie_offset | variable | (information elements) | [u8] | ie_length bytes; not in the struct `embassy/structs.rs:568` |

Size check: compiled
Differences: linux `struct brcmf_bss_info_le` (not packed): same offsets. A gcc build of the linux struct gives size 128, rateset 52, chanspec 72, RSSI 78, nbss_cap 84, reserved32 92, flags 96, basic_mcs 100, ie_offset 116, ie_length 120, SNR 124. linux has reserved[3] at 97-99 where embassy has vht_cap + reserved5. `linux/brcmfmac/fwil_types.h:314-348` `linux/brcmfmac/fwil_types.h:340`
Differences: whd record: `wl_bss_info_t`, with the same reserved1..reserved5 and vht_cap members; not inside a pack region. whd rejects records whose ie_offset is below sizeof(wl_bss_info_t). `whd/inc/whd_types.h:926-964` `whd/inc/whd_types.h:880-904` `whd/inc/whd_types.h:1120-1147` `whd/src/whd_wifi_api.c:2664-2665`
Differences: c-driver `cyw43_scan_result_internal_t`: same fields with explicit pad1..pad6, including pad6[2] between ie_offset and ie_length; size 128, rssi 78, ie_offset 116, ie_length 120, SNR 124 (compiled with gcc). It has pad5[3] where embassy has vht_cap + reserved5. `c-driver/cyw43_ll.c:486-516` `c-driver/cyw43_ll.c:512-514` `c-driver/cyw43_ll.c:510`

### `mkeep_alive packet (hand-built)` (embassy)
Value of named variable "mkeep_alive"; byte array, no padding, 11 bytes fixed plus keepalive frame data (embassy sends 11 with no data), little-endian; defined at `embassy/control.rs:683-692`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 2 | version | u16 | embassy sends 1; whd WL_MKEEP_ALIVE_VERSION 1 `embassy/control.rs:687` `whd/src/include/whd_wlioctl.h:3298` |
| 2 | 2 | length | u16 | embassy sends 11, the fixed length; linux leaves it 0 `embassy/control.rs:688` `linux/brcmfmac/cfg80211.c:4298-4305` |
| 4 | 4 | period_msec | u32 | `embassy/control.rs:689` |
| 8 | 2 | len_bytes | u16 | embassy sends 0, which its source comment calls a null frame `embassy/control.rs:690` |
| 10 | 1 | keep_alive_id | u8 | slot id; linux doc: 0 - 3 `embassy/control.rs:691` `linux/brcmfmac/fwil_types.h:1227` |
| 11 | variable | data | u8[] | len_bytes bytes; flexible tail; embassy sends none `embassy/control.rs:690` |

Size check: computed
Differences: linux `struct brcmf_mkeep_alive_pkt_le` (`__packed`, data at offset 11): same layout. linux zero-initialises the record and sets only version, period_msec, len_bytes and keep_alive_id, leaving length 0; embassy sets length to 11. `linux/brcmfmac/fwil_types.h:1230-1237` `linux/brcmfmac/cfg80211.c:4298-4305` `linux/brcmfmac/cfg80211.c:4307` `embassy/control.rs:688`
Differences: whd: definition of `wl_mkeep_alive_pkt_t` not found in whd; only a reference in WL_MKEEP_ALIVE_FIXED_LEN and the variable name exist. `whd/src/include/whd_wlioctl.h:3299` `whd/src/include/whd_wlioctl.h:1101`
Differences: c-driver: not found in these sources.

### `iovar set request (hand-built)` (embassy)
Payload of command SetVar (263) for every named variable; byte array, no padding, size = name + 1 NUL + value; value bytes as supplied; embassy's integer helpers write little-endian; defined at `embassy/control.rs:717-728` `embassy/consts.rs:684` `embassy/control.rs:703`; embassy's default buffer is 196 bytes; 256 for "escan" `embassy/control.rs:714` `embassy/control.rs:835`; embassy's runner builds the same layout itself for "mcast_list" and "allmulti" `embassy/runner.rs:1392-1408`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | name.len() | name | ASCII bytes | `embassy/control.rs:721` |
| name.len() | 1 | NUL | u8 | `embassy/control.rs:722` |
| name.len()+1 | variable | value | [u8] | val.len() bytes; no alignment padding between name and value `embassy/control.rs:723` |

Size check: computed
Differences: linux: `brcmf_create_iovar` writes name with NUL, then data; sent with BRCMF_C_SET_VAR. `linux/brcmfmac/fwil.c:167-184` `linux/brcmfmac/fwil.c:201-205`
Differences: whd: `whd_cdc_get_iovar_buffer` copies name + NUL and returns the pointer just after it for the value, but it also reserves (64 - name_length) % 4 zero bytes in front of the name so the value is 4-byte aligned. The handling of those leading bytes before sending is (unverified). `whd/src/whd_cdc_bdc.c:349-366` `whd/src/whd_cdc_bdc.c:355` `whd/src/whd_cdc_bdc.c:364-365`
Differences: c-driver: `cyw43_write_iovar_n` writes name + NUL then value; sent with WLC_SET_VAR. `c-driver/cyw43_ll.c:1556-1562`

### `iovar get request (hand-built)` (embassy)
Payload of command GetVar (262); byte array, size = max(name + 1, result length); byte order not stated; embassy decodes u32 results as little-endian; defined at `embassy/control.rs:731-746` `embassy/consts.rs:683` `embassy/control.rs:710`; embassy uses a fixed 64-byte buffer `embassy/control.rs:734`; embassy uses it for "clmload_status", "cur_etheraddr" (6 bytes) and "mcast_list" `embassy/control.rs:259` `embassy/control.rs:848-849` `embassy/control.rs:659`; the embassy source carries a TODO saying it "always returns all zeros" `embassy/control.rs:730`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | name.len() | name | ASCII bytes | `embassy/control.rs:735` |
| name.len() | 1 | NUL | u8 | `embassy/control.rs:736` |
| name.len()+1 | variable | (zero fill) | u8[] | up to res.len(); request length is max(name.len()+1, res.len()); the response overwrites the buffer from offset 0 `embassy/control.rs:738` `embassy/control.rs:743-744` |

Size check: computed
Differences: linux: `brcmf_fil_iovar_data_get` sends the same name + data buffer with BRCMF_C_GET_VAR and copies the response from the start of the buffer. `linux/brcmfmac/fwil.c:226-232`
Differences: whd: `whd_proto_get_iovar`. `whd/src/whd_clm.c:159`
Differences: c-driver: name + zero bytes, then WLC_GET_VAR. `c-driver/cyw43_ll.c:2077-2078`

### `clmload request (hand-built)` (embassy)
Command SetVar payload for each CLM chunk; byte array, 20 bytes fixed plus chunk; header fields in host order (see `DownloadHeader`); defined at `embassy/control.rs:250-254`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 8 | name | b"clmload\0" | `embassy/control.rs:251` |
| 8 | 12 | header | DownloadHeader | see `DownloadHeader` `embassy/control.rs:252` |
| 20 | variable | chunk | [u8] | chunk.len() bytes; chunk size = MAX_IOCTL_LEN - 8 - 12 = 1024 `embassy/control.rs:253` `embassy/control.rs:229` `embassy/ioctl.rs:17` |

Size check: computed
Differences: linux: `struct brcmf_dload_data_le` after the variable name. `linux/brcmfmac/fwil_types.h:1106` `linux/brcmfmac/common.c:194`
Differences: whd: `struct wl_dload_data`. `whd/src/include/whd_wlioctl.h:4167` `whd/src/whd_clm.c:138`
Differences: c-driver: it builds the identical 8 + 12 + data layout but rounds the sent length up to a multiple of 8; embassy sends the exact length. `c-driver/cyw43_ll.c:1508-1517` `c-driver/cyw43_ll.c:1521-1522` `embassy/control.rs:254`

### `mcast_list value (hand-built)` (embassy)
Value of named variable "mcast_list"; byte array, no padding, 4 + 6 * count bytes, little-endian count; offsets are relative to the value, which follows the 11-byte name "mcast_list\0"; defined at `embassy/runner.rs:1392-1399` `embassy/control.rs:661`; embassy's runner sets it; Control::list_multicast_addresses reads it `embassy/runner.rs:1392-1399` `embassy/control.rs:657-668`; the companion "allmulti" named variable is a single little-endian u32 in embassy `embassy/runner.rs:1404-1408`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | count | u32 | number of addresses `embassy/runner.rs:1395` |
| 4 | variable | addrs | [u8; 6][count] | 6 * count bytes; read back at `embassy/control.rs:662-665` `embassy/runner.rs:1396-1398`; embassy's runner always sends the full-size buffer (4 + 6 * MULTICAST_FILTER_SIZE after the name), not just count entries. `embassy/runner.rs:1393`; embassy's read side uses a 64-byte buffer, so at most 10 addresses can be returned. `embassy/control.rs:658` |

Size check: computed
Differences: linux: no struct; `__le32` count then 6-byte addresses, sent as "mcast_list". `linux/brcmfmac/core.c:160-175` `linux/brcmfmac/core.c:178`
Differences: whd record: `mcast_list_t` (uint32_t entry_count; whd_mac_t macs[1]) under `#pragma pack(1)`; read and rewritten at `whd/src/whd_wifi_api.c:3962-3995`. `whd/src/whd_wifi_api.c:127-133`
Differences: c-driver: 4 + MAX_MULTICAST_REGISTERED_ADDRESS * 6 bytes. `c-driver/cyw43_ll.c:2090-2129`

### `bsscfg u32 pair value (hand-built)` (embassy)
Value of named variables that take two u32; byte array, 8 bytes, little-endian; defined at `embassy/control.rs:695-699`; embassy uses it for "bsscfg:sup_wpa", "bsscfg:sup_wpa2_eapver", "bsscfg:sup_wpa_tmo", "bsscfg:wsec", "bsscfg:wpa_auth", "bss" (index, up/down) and "gpioout" (mask, value) `embassy/control.rs:378` `embassy/control.rs:392-394` `embassy/control.rs:589` `embassy/control.rs:595` `embassy/control.rs:615` `embassy/control.rs:641` `embassy/control.rs:512`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | val1 | u32 | bsscfg index for the "bsscfg:" variables and "bss"; a bit mask for "gpioout" `embassy/control.rs:697` |
| 4 | 4 | val2 | u32 | the value `embassy/control.rs:698` |

Size check: computed
Differences: linux: no struct. For a non-zero index `brcmf_create_bsscfg` writes "bsscfg:" + name + NUL, a le32 index, then the data; for index 0 it sends the plain name with no index. `linux/brcmfmac/fwil.c:262-288` `linux/brcmfmac/fwil.c:259-260`
Differences: whd: no struct; data[0] = bsscfg index before the value. `whd/src/whd_events.c:298` `whd/src/whd_ap.c:414`
Differences: c-driver: `cyw43_write_iovar_u32_u32` writes name + NUL, le32 val0, le32 val1; used for the same "bsscfg:sup_wpa*" variables. `c-driver/cyw43_ll.c:1546-1553` `c-driver/cyw43_ll.c:2240-2248`

### `ioctl frame (hand-built)` (embassy)
Every command request (named-variable requests included) written to the WLAN function; byte buffer, 12 + 16 + data bytes, sent rounded up to a multiple of 4; byte order as in `SdpcmHeader` and `CdcHeader`; defined at `embassy/runner.rs:1452-1503`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 12 | sdpcm | SdpcmHeader | channel 0 (control), header_length 12 `embassy/runner.rs:1469-1479` `embassy/runner.rs:1491` |
| 12 | 16 | cdc | CdcHeader | `embassy/runner.rs:1481-1487` `embassy/runner.rs:1492` |
| 28 | variable | data | [u8] | data.len() bytes `embassy/runner.rs:1493` |
| 28+data.len() | 0-3 | (pad) | u8[0..3] | transfer length rounded up to 4 bytes; SdpcmHeader.len keeps the unrounded length `embassy/runner.rs:1495` `embassy/runner.rs:1463` `embassy/runner.rs:1470`; the embassy source has a TODO asking whether len should be the rounded value. `embassy/runner.rs:1470` |

Size check: computed
Differences: linux: hardware + software header, then `struct brcmf_proto_bcdc_dcmd`. `linux/brcmfmac/sdio.c:1330-1333` `linux/brcmfmac/bcdc.c:25`
Differences: whd: `sdpcm_header_t` + `cdc_header_t`. `whd/src/whd_sdpcm.c:99` `whd/src/include/whd_cdc_bdc.h:72`
Differences: c-driver: `sdpcm_header_t`, then `ioctl_header_t` at offset SDPCM_HEADER_LEN, payload at SDPCM_HEADER_LEN + 16. `c-driver/cyw43_ll.c:903-910`

### `tx data frame (hand-built)` (embassy)
Outgoing Ethernet frames on the data channel; byte buffer, 12 + 2 + 4 + packet bytes, sent rounded up to a multiple of 4; byte order as in `SdpcmHeader`; defined at `embassy/runner.rs:892-925`; embassy states the receive direction has the same shape: 2 pad bytes after the 12-byte SDPCM header and a BDC data offset of one word `embassy/lib.rs:53-57`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 12 | sdpcm | SdpcmHeader | channel 2 (data), header_length 14 `embassy/runner.rs:897-907` `embassy/runner.rs:918` |
| 12 | 2 | (pad) | u8[2] | between the SDPCM and BDC headers, data packets only `embassy/runner.rs:883-891`; an embassy source comment says two zero bytes get appended to transmitted packets if the 2-byte pad is missing; this is the comment's claim, not shown by code. `embassy/runner.rs:885-887` |
| 14 | 4 | bdc | BdcHeader | flags 32 (0x20), other fields 0 `embassy/runner.rs:909-914` `embassy/runner.rs:919-920` |
| 18 | variable | packet | [u8] | Ethernet frame, packet.len() bytes `embassy/runner.rs:921-922` |
| 18+packet.len() | 0-3 | (pad) | u8[0..3] | rounded up to 4 bytes `embassy/runner.rs:924` |

Size check: computed
Differences: linux: no single record; `brcmf_proto_bcdc_hdrpush` prepends the 4-byte BCDC header and `brcmf_sdio_hdpack` writes the bus header. `linux/brcmfmac/bcdc.c:257-265` `linux/brcmfmac/bcdc.c:47` `linux/brcmfmac/sdio.c:1488`
Differences: whd record: `data_header_t` (bus header, `_padding[2]`, `bdc_header_t`) under `#pragma pack(1)`: the same 2 pad bytes. `control_header_t` just above it has no padding. `whd/src/include/whd_sdpcm.h:81-94` `whd/src/include/whd_sdpcm.h:82-86`
Differences: c-driver: places its BDC header at SDPCM_HEADER_LEN + 2 as well, and also sets flags 0x20. `c-driver/cyw43_ll.c:935-942` `c-driver/cyw43_ll.c:943`

### `SDIO frame tag (hand-built)` (embassy)
First 4 bytes of a pending F2 frame, read on the SDIO bus to learn the frame length before reading the rest; byte array, 4 bytes, little-endian; defined at `embassy/runner.rs:1057-1070` `embassy/runner.rs:1115`; these are the same bytes as `SdpcmHeader` len / len_inv; the initial read length is 4 `embassy/consts.rs:38`; on SPI embassy takes the length from the status register instead `embassy/runner.rs:1048-1055`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 2 | len | u16 | frame length `embassy/runner.rs:1063-1064` |
| 2 | 2 | len_inv | u16 | embassy requires len ^ len_inv == 0xFFFF and not both zero `embassy/runner.rs:1068` |

Size check: computed
Differences: linux: hardware header, 4 bytes. `linux/brcmfmac/sdio.c:1330`
Differences: whd: `frametag[2]` in `sdpcm_header_t`. `whd/src/whd_sdpcm.c:101`
Differences: c-driver: size / size_com in `struct sdpcm_header_t`. `c-driver/cyw43_ll.c:755-756`

### `NVRAM length word (hand-built)` (embassy)
Length word written to the last word of chip RAM (ram_addr + chip_ram_size - 4); the NVRAM is placed immediately below it; one 32-bit backplane write, 4 bytes; linux stores it as cpu_to_le32; defined at `embassy/runner.rs:567-570` `embassy/runner.rs:560` `linux/brcmfmac/firmware.c:448`; embassy reads the word back to verify it `embassy/runner.rs:572-575`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 2 | len_words | u16 (low half) | NVRAM length in 4-byte words; the length is first rounded up to a multiple of 4 `embassy/runner.rs:559` `embassy/runner.rs:567` |
| 2 | 2 | len_words_inv | u16 (high half) | bitwise NOT of len_words `embassy/runner.rs:568` |

Size check: computed
Differences: padding of the NVRAM differs: linux pads to roundup(len + 1, 4); embassy to div_ceil(4) * 4. `linux/brcmfmac/firmware.c:440` `embassy/runner.rs:559`
Differences: masking differs: linux and whd's M2M path mask the low half (the word count) to 16 bits; embassy, c-driver and whd's SDIO and SPI paths OR the word count in unmasked (c-driver masks only the inverted half to 16 bits before shifting it up, which changes nothing in a 32-bit word). The results are equal while the word count fits in 16 bits; above that the unmasked count runs into the high half, while linux and whd's M2M path cut it off. `linux/brcmfmac/firmware.c:447` `whd/src/bus_protocols/whd_bus_m2m_protocol.c:704` `embassy/runner.rs:568` `c-driver/cyw43_ll.c:1801` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:2156` `whd/src/bus_protocols/whd_bus_spi_protocol.c:1283`
Differences: linux: same formula. `linux/brcmfmac/firmware.c:446-450`
Differences: whd: same word, written to RAM base + CHIP_RAM_SIZE - 4 in all three bus back ends. `whd/src/bus_protocols/whd_bus_sdio_protocol.c:2138-2160` `whd/src/bus_protocols/whd_bus_spi_protocol.c:1273-1287` `whd/src/bus_protocols/whd_bus_m2m_protocol.c:692-707`
Differences: c-driver: same formula. `c-driver/cyw43_ll.c:1800-1802`

### `BT HCI ring record header (hand-built)` (embassy)
Record format in both Bluetooth shared ring buffers (host-to-BT and BT-to-host); byte array, 4 bytes fixed plus payload rounded up to a multiple of 4; 24-bit length, low byte first; defined at `embassy/bluetooth.rs:390-448` `embassy/bluetooth.rs:472-520` `embassy/bluetooth.rs:490`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 3 | len | u24 | payload length, not counting the HCI type byte or this header `embassy/bluetooth.rs:397` `embassy/bluetooth.rs:414-416` |
| 3 | 1 | hci_type | u8 | HCI packet type `embassy/bluetooth.rs:417` `embassy/bluetooth.rs:503` |
| 4 | variable | payload | [u8] | round_up(len, 4) bytes `embassy/bluetooth.rs:398` `embassy/bluetooth.rs:425` `embassy/bluetooth.rs:491` `embassy/bluetooth.rs:504` |

Size check: computed
Differences: pico-sdk describes and decodes the same header (three length bytes, HCI packet type, data); pico-sdk always writes byte 2 as 0. `pico-sdk/cybt_shared_bus.c:333-343` `pico-sdk/cybt_shared_bus.c:356-389` `pico-sdk/cybt_shared_bus.c:378` `pico-sdk/cybt_shared_bus.c:388` `pico-sdk/cybt_shared_bus.c:343`
Differences: linux: not found in these sources (no shared-bus Bluetooth code under linux/brcmfmac).
Differences: whd: not found in these sources.
Differences: c-driver: not found in these sources.

### `BT shared buffer region (constants)` (embassy)
Bluetooth shared-bus buffers on the backplane; a memory layout given by offset constants, not a struct; 8208 bytes to the end of the last pointer word (inferred; nothing in these sources states what lies between or after); the 32-bit pointers are accessed with 32-bit backplane reads and writes; defined at `embassy/consts.rs:202-209` `embassy/bluetooth.rs:401` `embassy/bluetooth.rs:441` `embassy/bluetooth.rs:478` `embassy/bluetooth.rs:518`; embassy reads the base address from the register at 0x18000d68 and zeroes the four pointers at init `embassy/bluetooth.rs:375` `embassy/consts.rs:194` `embassy/bluetooth.rs:55` `embassy/bluetooth.rs:378-381`; embassy's ring arithmetic is modulo the buffer size `embassy/bluetooth.rs:402` `embassy/bluetooth.rs:422` `embassy/bluetooth.rs:479`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4096 | host_write_buf | u8[0x1000] | host-to-BT ring; buffer size 4096 (0x1000) `embassy/consts.rs:202-203` |
| 4096 | 4096 | host_read_buf | u8[0x1000] | BT-to-host ring `embassy/consts.rs:204` |
| 8192 | 4 | host2bt_in | u32 | host write pointer; embassy writes it `embassy/consts.rs:206` `embassy/bluetooth.rs:441` |
| 8196 | 4 | host2bt_out | u32 | BT read pointer; embassy reads it `embassy/consts.rs:207` `embassy/bluetooth.rs:401` |
| 8200 | 4 | bt2host_in | u32 | BT write pointer; embassy reads it `embassy/consts.rs:208` `embassy/bluetooth.rs:478` |
| 8204 | 4 | bt2host_out | u32 | host read pointer; embassy writes it `embassy/consts.rs:209` `embassy/bluetooth.rs:518` |

Size check: computed
Differences: pico-sdk uses the same offsets, buffer size and base register. `cybt_fw_membuf_info_t` is a host struct holding the six resulting addresses, not a wire record. `pico-sdk/cybt_shared_bus_driver.c:37-40` `pico-sdk/cybt_shared_bus_driver.c:87-88` `pico-sdk/cybt_shared_bus_driver.h:10` `pico-sdk/cybt_shared_bus_driver.c:56` `pico-sdk/cybt_shared_bus_driver.c:58-65`
Differences: linux: not found in these sources.
Differences: whd: not found in these sources.

### `BT patch record (hand-parsed)` (embassy)
Record of the Bluetooth patch blob that the host parses before writing bytes to chip memory; layout taken from embassy's parsing code only (unverified); it is a file format consumed by the driver, not a record exchanged at run time; byte stream, 4 bytes fixed plus num_bytes; address fields big-endian; defined at `embassy/bluetooth.rs:166-199` `embassy/bluetooth.rs:309`; the record stream is preceded by a prefix that embassy skips: byte 0 = version length, then that many version bytes, then one more byte `embassy/bluetooth.rs:239-242`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 1 | num_bytes | u8 | data length; 0 ends the stream `embassy/bluetooth.rs:170` `embassy/bluetooth.rs:179`; embassy consumes the 4 header bytes before the num_bytes == 0 end test. `embassy/bluetooth.rs:170-181` |
| 1 | 2 | addr | u16 big-endian | `embassy/bluetooth.rs:173` |
| 3 | 1 | line_type | u8 | 0 data, 1 end, 2 extended segment address, 4 extended address, 5 absolute 32-bit address `embassy/consts.rs:179-183` |
| 4 | variable | data | u8[num_bytes] | for address records a big-endian u16 or u32 `embassy/bluetooth.rs:183` `embassy/bluetooth.rs:188` `embassy/bluetooth.rs:192` `embassy/bluetooth.rs:196-199`; embassy writes data to the Bluetooth base address + destination address, widened to whole 32-bit words by reading back the neighbouring bytes. `embassy/bluetooth.rs:262-309` |

Size check: computed
Differences: pico-sdk: the binary parser `cybt_fw_get_data` reads the same 4-byte header (num_bytes, addr high, addr low, type) then data. An ASCII-hex variant of the parser is in the same file (`pico-sdk/cybt_shared_bus_driver.c:173-232`). `hex_file_data_t` is host bookkeeping. `pico-sdk/cybt_shared_bus_driver.c:240-254` `pico-sdk/cybt_shared_bus_driver.c:257-275` `pico-sdk/cybt_shared_bus_driver.c:102-107`
Differences: linux: not found in these sources.
Differences: whd: not found in these sources.

### `rx frame (hand-parsed)` (embassy)
Every frame read from the WLAN function; byte buffer with headers overlaid in place, 12 bytes fixed plus header padding plus a channel-specific body; byte order as in `SdpcmHeader`, `CdcHeader`, `EventPacket`; defined at `embassy/runner.rs:1151-1365`; embassy takes the channel as channel_and_flags & 0x0f and ignores other channel values `embassy/runner.rs:1164` `embassy/runner.rs:1363`; embassy drops an empty body after the credit update `embassy/runner.rs:1158-1162`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 12 | sdpcm | SdpcmHeader | len must equal the length reported by the bus and NOT len_inv `embassy/structs.rs:106-114` |
| 12 | header_length - 12 | (pad) | u8[] | skipped: the body starts at header_length from the frame start; embassy expects 2 bytes here for data frames `embassy/structs.rs:116-126` `embassy/lib.rs:53-54` |
| header_length | variable | body (channel 0, control) | CdcHeader + [u8] | 16 + cdc.len bytes; command response, payload cut to cdc.len `embassy/runner.rs:1167-1183` `embassy/structs.rs:162-172` |
| header_length | variable | body (channel 1, event) | BdcHeader + skip + EventPacket + [u8] | alternative to the row above; 4 + 4*data_offset + 72 + msg.datalen bytes `embassy/runner.rs:1188-1197` `embassy/structs.rs:202-204` `embassy/structs.rs:346-358` |
| header_length | variable | body (channel 2, data) | BdcHeader + skip + Ethernet frame | alternative to the rows above; 4 + 4*data_offset + frame bytes; embassy hands the frame offset and length to the network stack `embassy/runner.rs:1352-1361` |

Size check: computed
Differences: linux: no single record; `brcmf_sdio_hdparse` reads the bus header and `brcmf_proto_bcdc_hdrpull` removes the 4-byte BCDC header. `linux/brcmfmac/sdio.c:1371` `linux/brcmfmac/bcdc.c:281-319`
Differences: whd: no single record; received frames are handled by `whd_sdpcm_process_rx_packet`. `whd/src/whd_sdpcm.c:334`
Differences: c-driver: same sequence: BDC header, skip data_offset << 2, then the payload. `c-driver/cyw43_ll.c:1061-1062`

## c-driver

### `sdpcm_header_t` (c-driver)
First header of every frame on WLAN function 2 in both directions, built in cyw43_sdpcm_send_common (`c-driver/cyw43_ll.c:829-848`) and parsed in sdpcm_process_rx_packet (`c-driver/cyw43_ll.c:963-995`); not packed (no packed attribute, natural alignment gives no padding); 12 bytes (compiled); byte order not stated, fields are read and written natively, so host order (little-endian on the little-endian hosts this driver targets); defined at `c-driver/cyw43_ll.c:754-764`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 2 | `size` | `uint16_t` | whole frame length including this header; set to SDPCM_HEADER_LEN + len (`c-driver/cyw43_ll.c:826`, `c-driver/cyw43_ll.c:830`). rx: frames with size < 12 or a failed complement check are ignored (`c-driver/cyw43_ll.c:964-973`); a frame with size == 12 is a flow-control-only frame and is dropped after the credit update (`c-driver/cyw43_ll.c:991-995`) |
| 2 | 2 | `size_com` | `uint16_t` | ~size & 0xffff (`c-driver/cyw43_ll.c:831`); rx check size == (~size_com & 0xffff) (`c-driver/cyw43_ll.c:964`). The SDIO and SPI poll paths also test the first two 16-bit words directly: both zero means no packet, (hdr[0] ^ hdr[1]) != 0xffff is an error (`c-driver/cyw43_ll.c:1118-1129`, `c-driver/cyw43_ll.c:1248-1260`) |
| 4 | 1 | `sequence` | `uint8_t` | tx sequence number, incremented per frame (`c-driver/cyw43_ll.c:832`, `c-driver/cyw43_ll.c:841`) |
| 5 | 1 | `channel_and_flags` | `uint8_t` | tx: kind, 0 = control, 2 = data (`c-driver/cyw43_ll.c:833`, `c-driver/cyw43_ll.c:156-158`); rx: low nibble is the channel, 0 control / 1 async event / 2 data (`c-driver/cyw43_ll.c:997`) |
| 6 | 1 | `next_length` | `uint8_t` | written 0 (`c-driver/cyw43_ll.c:834`) |
| 7 | 1 | `header_length` | `uint8_t` | tx: 12, or 14 for data frames (`c-driver/cyw43_ll.c:835`); rx: offset of the next header from frame start (`c-driver/cyw43_ll.c:1004`, `c-driver/cyw43_ll.c:1035`) |
| 8 | 1 | `wireless_flow_control` | `uint8_t` | tx 0 (`c-driver/cyw43_ll.c:836`); rx value copied to wlan_flow_control, non-zero stalls tx (`c-driver/cyw43_ll.c:981`, `c-driver/cyw43_ll.c:779`) |
| 9 | 1 | `bus_data_credit` | `uint8_t` | tx 0 (`c-driver/cyw43_ll.c:837`); rx: tx allowed while credit != tx sequence; accepted only if (credit - last) <= 20 and channel < 3 (`c-driver/cyw43_ll.c:983-989`, `c-driver/cyw43_ll.c:779`) |
| 10 | 2 | `reserved` | `uint8_t[2]` | written 0 (`c-driver/cyw43_ll.c:838-839`) |

Size check: compiled

### `ioctl_header_t` (c-driver)
Header of every command and named-variable (iovar) request and response, placed at frame offset 12 on tx (`c-driver/cyw43_ll.c:903`) and at header_length on rx (`c-driver/cyw43_ll.c:1004`); not packed (four uint32_t, no padding); 16 bytes (compiled); byte order not stated, fields are read and written natively, so host order (little-endian on the little-endian hosts this driver targets); defined at `c-driver/cyw43_ll.c:851-856`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `cmd` | `uint32_t` | WLC command number (`c-driver/cyw43_ll.c:904`); the public cyw43_ll_ioctl passes cmd >> 1 here and uses bit 0 as set/get (`c-driver/cyw43_ll.c:1329`) |
| 4 | 4 | `len` | `uint32_t` | comment: lower 16 is output len; upper 16 is input len (`c-driver/cyw43_ll.c:853`); written as len & 0xffff (`c-driver/cyw43_ll.c:905`) |
| 8 | 4 | `flags` | `uint32_t` | (request id << 16) & 0xffff0000 \| kind \| (iface << 12); kind is 0 = get, 2 = set (`c-driver/cyw43_ll.c:899-900`, `c-driver/cyw43_ll.c:160-165`). rx: id = (flags & 0xffff0000) >> 16 must equal the last id sent (`c-driver/cyw43_ll.c:1010-1015`); the interface number in rx flags is not extracted (TODO at `c-driver/cyw43_ll.c:1016`) |
| 12 | 4 | `status` | `uint32_t` | tx 0 (`c-driver/cyw43_ll.c:907`); rx value is not checked (TODO at `c-driver/cyw43_ll.c:1006-1008`). The payload follows this field: the code uses the literal 16 for the payload offset (`c-driver/cyw43_ll.c:910`, `c-driver/cyw43_ll.c:917`), and the response payload is copied back over the caller's buffer, min(len, res_len) bytes (`c-driver/cyw43_ll.c:1020-1024`, `c-driver/cyw43_ll.c:1312`) |

Size check: compiled

### `sdpcm_bdc_header_t` (c-driver)
Header in front of Ethernet frames (data channel) and async events (`c-driver/cyw43_ll.c:942`, `c-driver/cyw43_ll.c:1035`, `c-driver/cyw43_ll.c:1057`); not packed (four uint8_t); 4 bytes (compiled); byte order not applicable (single bytes); defined at `c-driver/cyw43_ll.c:920-925`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 1 | `flags` | `uint8_t` | tx 0x20 (`c-driver/cyw43_ll.c:943`) |
| 1 | 1 | `priority` | `uint8_t` | tx 0 (`c-driver/cyw43_ll.c:944`) |
| 2 | 1 | `flags2` | `uint8_t` | interface number: tx itf (`c-driver/cyw43_ll.c:945`); rx itf = flags2 (`c-driver/cyw43_ll.c:1037`) |
| 3 | 1 | `data_offset` | `uint8_t` | tx 0 (`c-driver/cyw43_ll.c:946`); rx: payload starts 4 + (data_offset << 2) bytes after this header (`c-driver/cyw43_ll.c:1041`, `c-driver/cyw43_ll.c:1061`). Rx data and async frames must be longer than 12 + 4 bytes (`c-driver/cyw43_ll.c:1029`, `c-driver/cyw43_ll.c:1051`) |

Size check: compiled

### `tx_control_frame (hand-built)` (c-driver)
Every command and named-variable request, sent with cyw43_sdpcm_send_common(CONTROL_HEADER, 16 + len) (`c-driver/cyw43_ll.c:917`); hand-built in a byte buffer; variable size, 28 fixed bytes + payload (computed); headers host-native, payload per command; built at `c-driver/cyw43_ll.c:893-918`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 12 | `sdpcm header` | `struct sdpcm_header_t` | channel_and_flags = 0, header_length = 12 (`c-driver/cyw43_ll.c:833-835`) |
| 12 | 16 | `command header` | `struct ioctl_header_t` | `c-driver/cyw43_ll.c:903-907` |
| 28 | variable (len) | `payload` | `uint8_t[]` | copied with memmove to spid_buf + 12 + 16 (`c-driver/cyw43_ll.c:910`); flexible tail. Rejected if 12 + 16 + len > sizeof(spid_buf) = 2048 (`c-driver/cyw43_ll.c:894`, `c-driver/cyw43_internal.h:35`). The driver's command buffers are built at &spid_buf[SDPCM_HEADER_LEN + 16], i.e. directly at this position (`c-driver/cyw43_ll.c:1493`, `c-driver/cyw43_ll.c:1539`, `c-driver/cyw43_ll.c:1957`). Bus padding: SPI pads the transfer to 4 bytes with the true size in the command word; SDIO pads per transfer mode (`c-driver/cyw43_ll.c:843-847`) |

Size check: computed

### `tx_data_frame (hand-built)` (c-driver)
Ethernet frame sent by cyw43_ll_send_ethernet with cyw43_sdpcm_send_common(DATA_HEADER, 6 + len) (`c-driver/cyw43_ll.c:959`); hand-built in a byte buffer; variable size, 18 fixed bytes + Ethernet frame (computed); headers host-native, Ethernet payload as supplied; built at `c-driver/cyw43_ll.c:928-960`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 12 | `sdpcm header` | `struct sdpcm_header_t` | channel_and_flags = 2, header_length = 14 (`c-driver/cyw43_ll.c:833-835`) |
| 12 | 2 | (pad) | `uint8_t[2]` | 2 bytes of padding after the sdpcm header, not written, so they hold whatever was in spid_buf (`c-driver/cyw43_ll.c:940-942`) |
| 14 | 4 | `bdc header` | `struct sdpcm_bdc_header_t` | `c-driver/cyw43_ll.c:942-946` |
| 18 | variable (len) | `ethernet frame` | `uint8_t[]` | copied to spid_buf + 12 + 6 (`c-driver/cyw43_ll.c:951`, `c-driver/cyw43_ll.c:955`); flexible tail. Rejected if 12 + 2 + 4 + len > 2048 (`c-driver/cyw43_ll.c:935`) |

Size check: computed

### `rx_frame, control and data channels (hand-parsed)` (c-driver)
Receive side of sdpcm_process_rx_packet for channel 0 (command and named-variable replies) and channel 2 (Ethernet data) (`c-driver/cyw43_ll.c:997-1049`), channel 1 being `rx_async_event_frame_prefix (hand-parsed)`; hand-parsed in a byte buffer; variable size, header_length + 16 + payload for control and header_length + 4 + 4 * data_offset + Ethernet frame for data (computed); headers read natively (host order); parsed at `c-driver/cyw43_ll.c:962-1049`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 12 | `sdpcm header` | `struct sdpcm_header_t` | size / size_com checked, flow control and credit taken, channel = channel_and_flags & 0x0f (`c-driver/cyw43_ll.c:963-997`). Return codes for rejected frames: -2 bad complement, -3 size < 12, -4 size == 12, -5 short control, -6 wrong request id, -7 short data, -8 short async, -11 unknown channel (`c-driver/cyw43_ll.c:964-1091`) |
| 12 | variable (header_length - 12) | (not examined) | `uint8_t[]` | skipped: the next header is located at buf[header_length], not at 12 (`c-driver/cyw43_ll.c:1004`, `c-driver/cyw43_ll.c:1035`) |
| header_length | 16 | `command header (channel 0)` | `struct ioctl_header_t` | frame must have size >= 12 + 16 (`c-driver/cyw43_ll.c:999`); id in flags bits 31..16 must match the last request (`c-driver/cyw43_ll.c:1010-1015`) |
| header_length + 16 | variable (size - (header_length + 16)) | `command reply payload (channel 0)` | `uint8_t[]` | `c-driver/cyw43_ll.c:1020-1024`; flexible tail. The reply is copied back over the request buffer, min(len, res_len) bytes (`c-driver/cyw43_ll.c:1312`) |
| header_length | 4 | `bdc header (channel 2)` | `struct sdpcm_bdc_header_t` | union alternative to the command header; frame must have size > 12 + 4 (`c-driver/cyw43_ll.c:1029`); interface = flags2 (`c-driver/cyw43_ll.c:1037`) |
| header_length + 4 | variable (data_offset << 2) | (not examined) | `uint8_t[]` | variable-length header extension, skipped (`c-driver/cyw43_ll.c:1038-1041`) |
| header_length + 4 + (data_offset << 2) | variable (size - offset) | `ethernet frame (channel 2)` | `uint8_t[]` | `c-driver/cyw43_ll.c:1041-1047`; flexible tail. The interface number is passed up in bit 31 of the length (`c-driver/cyw43_ll.c:1046`, `c-driver/cyw43_ll.c:1280`) |

Size check: computed

### `rx_async_event_frame_prefix (hand-parsed)` (c-driver)
Start of channel 1 (async event) frames, with offsets relative to the payload that follows the BDC header (payload = bdc + 4 + (data_offset << 2), `c-driver/cyw43_ll.c:1061`); hand-parsed by byte offset; variable size, 24 fixed bytes before the event message (computed); Ethernet type compared as bytes 0x88, 0x6c in that order (big-endian 0x886c); parsed at `c-driver/cyw43_ll.c:1050-1086`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 12 | (not examined) | `uint8_t[12]` | bytes 0..11 of the payload are not read; comment says the payload is an ethernet packet (`c-driver/cyw43_ll.c:1065`). c-driver gives no names for the unexamined bytes of this prefix (`c-driver/cyw43_ll.c:1050-1086`) |
| 12 | 2 | `ethertype` | `uint8_t[2]` | must be 0x88, 0x6c, else CYW43_ERROR_WRONG_PAYLOAD_TYPE (-9) (`c-driver/cyw43_ll.c:1066-1070`, `c-driver/cyw43_ll.c:261`) |
| 14 | 5 | (not examined) | `uint8_t[5]` | not read (`c-driver/cyw43_ll.c:1066-1074`) |
| 19 | 3 | `oui` | `uint8_t[3]` | must be 0x00, 0x10, 0x18 (comment: Broadcom OUI), else -10 (`c-driver/cyw43_ll.c:1074-1077`) |
| 22 | 2 | (not examined) | `uint8_t[2]` | not read (`c-driver/cyw43_ll.c:1074-1082`) |
| 24 | variable (len - 24) | `event message` | `cyw43_async_event_t` | handed up as payload + 24 with length len - 24 (`c-driver/cyw43_ll.c:1080-1082`). A source comment says the event buffer is &spid_buf[46] and only 2-byte aligned, so the event is moved down 2 bytes, 32 bits at a time, before the struct cast (`c-driver/cyw43_ll.c:721-735`) |

Size check: computed

### `cyw43_async_event_t` (c-driver)
Event message that starts 24 bytes into the async-event payload (`c-driver/cyw43_ll.c:1082`, `c-driver/cyw43_ll.c:735`) and is consumed in cyw43_cb_process_async_event (`c-driver/cyw43_ctrl.c:312`); not packed; 156 bytes as declared, 48 fixed + union (compiled); mixed byte order, with flags, event_type, status and reason converted from big-endian in place (`c-driver/cyw43_ll.c:738-741`) and the scan result in the union read natively (host order); defined at `c-driver/cyw43_ll.h:237-249`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 2 | `_0` | `uint16_t` | unnamed; first 2 bytes of the event message (`c-driver/cyw43_ll.h:238`). The struct is overlaid on the receive buffer after the 2-byte relocation, so offsets here equal wire offsets from the start of the event message (`c-driver/cyw43_ll.c:726-735`) |
| 2 | 2 | `flags` | `uint16_t` | big-endian on the wire (`c-driver/cyw43_ll.c:738`); bit 0 tested for link up on EV_LINK (`c-driver/cyw43_ctrl.c:391`) |
| 4 | 4 | `event_type` | `uint32_t` | big-endian on the wire (`c-driver/cyw43_ll.c:739`); CYW43_EV_* (`c-driver/cyw43_ll.h:50-66`) |
| 8 | 4 | `status` | `uint32_t` | big-endian on the wire (`c-driver/cyw43_ll.c:740`); CYW43_STATUS_* (`c-driver/cyw43_ll.h:69-79`). The driver overwrites it in place with -1 for a bad scan record (`c-driver/cyw43_ll.c:679`) |
| 12 | 4 | `reason` | `uint32_t` | big-endian on the wire (`c-driver/cyw43_ll.c:741`) |
| 16 | 30 | `_1` | `uint8_t[30]` | unnamed, not read (`c-driver/cyw43_ll.h:243`) |
| 46 | 1 | `interface` | `uint8_t` | compared with CYW43_ITF_STA (`c-driver/cyw43_ctrl.c:332`, `c-driver/cyw43_ctrl.c:393`); the comparison with CYW43_ITF_AP at `c-driver/cyw43_ctrl.c:341` is inside an `#if 0` block (`c-driver/cyw43_ctrl.c:339-345`) |
| 47 | 1 | `_2` | `uint8_t` | unnamed (`c-driver/cyw43_ll.h:245`) |
| 48 | 108 | `u.scan_result` | `cyw43_ev_scan_result_t` | union with one member; valid for EV_ESCAN_RESULT with status PARTIAL (8) (`c-driver/cyw43_ll.c:744`, `c-driver/cyw43_ctrl.c:319-323`). The driver overwrites two of its fields in place: channel &= 0xff and auth_mode (`c-driver/cyw43_ll.c:714-715`) |

Size check: compiled

### `cyw43_ev_scan_result_t` (c-driver)
Public view of one EV_ESCAN_RESULT partial result, passed to the scan callback (`c-driver/cyw43_ctrl.c:323`) and covering the same bytes as _scan_result_t at event offset 48 (`c-driver/cyw43_ll.c:675`); not packed; 108 bytes (compiled); byte order not stated, read natively (host order); defined at `c-driver/cyw43_ll.h:222-234`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 20 | `_0` | `uint32_t[5]` | unnamed; overlays buflen, version, sync_id + bss_count of the escan wrapper and version, length of the bss record, see `_scan_result_t (escan result wrapper, function-local struct)` (`c-driver/cyw43_ll.h:223`). The overlay of each field on cyw43_scan_result_internal_t is the 12-byte wrapper header plus the internal offset (computed) (`c-driver/cyw43_ll.c:669-675`) |
| 20 | 6 | `bssid` | `uint8_t[6]` | access point mac address (`c-driver/cyw43_ll.h:224`) |
| 26 | 4 | `_1` | `uint16_t[2]` | unnamed; overlays beacon_period, capability (`c-driver/cyw43_ll.h:225`) |
| 30 | 1 | `ssid_len` | `uint8_t` | `c-driver/cyw43_ll.h:226` |
| 31 | 32 | `ssid` | `uint8_t[32]` | `c-driver/cyw43_ll.h:227` |
| 63 | 1 | (pad) | `uint8_t` | alignment padding before _2; overlays pad1 of the internal struct (`c-driver/cyw43_ll.h:227-228`) |
| 64 | 20 | `_2` | `uint32_t[5]` | unnamed; overlays rateset_count and rateset_rates[16] (`c-driver/cyw43_ll.h:228`) |
| 84 | 2 | `channel` | `uint16_t` | overlays chanspec; the driver masks it with 0xff in place (`c-driver/cyw43_ll.c:714`) |
| 86 | 4 | `_3` | `uint8_t[4]` | unnamed; overlays atim_window, dtim_period, pad2 (`c-driver/cyw43_ll.h:230`) |
| 90 | 2 | `rssi` | `int16_t` | signal strength (`c-driver/cyw43_ll.h:231`) |
| 92 | 12 | `_4` | `uint8_t[12]` | unnamed; overlays phy_noise, n_cap, pad3, nbss_cap, ctl_ch, pad4 (`c-driver/cyw43_ll.h:232`) |
| 104 | 4 | `auth_mode` | `uint32_t` | not a received value: the driver writes its computed CYW43_AUTH_FLAG_* value here (`c-driver/cyw43_ll.c:715`); the slot overlays reserved32[0] of the internal struct |

Size check: compiled

### `cyw43_scan_result_internal_t` (c-driver)
BSS record inside an escan result event, parsed in cyw43_ll_wifi_parse_scan_result (`c-driver/cyw43_ll.c:668-718`); not packed (explicit pad fields, compiled layout has no hidden padding except 2 tail bytes); 128 bytes as declared, variable on the wire because IEs follow at ie_offset (compiled); byte order not stated, read natively (host order); defined at `c-driver/cyw43_ll.c:486-516`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `version` | `uint32_t` | `c-driver/cyw43_ll.c:487` |
| 4 | 4 | `length` | `uint32_t` | record length; ie_offset + ie_length must not exceed it (`c-driver/cyw43_ll.c:677`). Only length, capability, ie_offset and ie_length are read by name (`c-driver/cyw43_ll.c:677-710`) |
| 8 | 6 | `bssid` | `uint8_t[6]` | `c-driver/cyw43_ll.c:489` |
| 14 | 2 | `beacon_period` | `uint16_t` | `c-driver/cyw43_ll.c:490` |
| 16 | 2 | `capability` | `uint16_t` | bit 0x0010 (DOT11_CAP_PRIVACY) adds the WEP flag (`c-driver/cyw43_ll.c:710`, `c-driver/cyw43_ll.c:238`) |
| 18 | 1 | `ssid_len` | `uint8_t` | `c-driver/cyw43_ll.c:492` |
| 19 | 32 | `ssid` | `uint8_t[32]` | `c-driver/cyw43_ll.c:493` |
| 51 | 1 | `pad1` | `uint8_t[1]` | declared pad field (`c-driver/cyw43_ll.c:494`) |
| 52 | 4 | `rateset_count` | `uint32_t` | `c-driver/cyw43_ll.c:495` |
| 56 | 16 | `rateset_rates` | `uint8_t[16]` | `c-driver/cyw43_ll.c:496` |
| 72 | 2 | `chanspec` | `uint16_t` | `c-driver/cyw43_ll.c:497` |
| 74 | 2 | `atim_window` | `uint16_t` | `c-driver/cyw43_ll.c:498` |
| 76 | 1 | `dtim_period` | `uint8_t` | `c-driver/cyw43_ll.c:499` |
| 77 | 1 | `pad2` | `uint8_t[1]` | declared pad field (`c-driver/cyw43_ll.c:500`) |
| 78 | 2 | `rssi` | `int16_t` | `c-driver/cyw43_ll.c:501` |
| 80 | 1 | `phy_noise` | `int8_t` | `c-driver/cyw43_ll.c:502` |
| 81 | 1 | `n_cap` | `uint8_t` | `c-driver/cyw43_ll.c:503` |
| 82 | 2 | `pad3` | `uint8_t[2]` | declared pad field (`c-driver/cyw43_ll.c:504`) |
| 84 | 4 | `nbss_cap` | `uint32_t` | `c-driver/cyw43_ll.c:505` |
| 88 | 1 | `ctl_ch` | `uint8_t` | `c-driver/cyw43_ll.c:506` |
| 89 | 3 | `pad4` | `uint8_t[3]` | declared pad field (`c-driver/cyw43_ll.c:507`) |
| 92 | 4 | `reserved32` | `uint32_t[1]` | the driver stores auth_mode here through the public overlay (`c-driver/cyw43_ll.c:508`, `c-driver/cyw43_ll.c:715`) |
| 96 | 1 | `flags` | `uint8_t` | `c-driver/cyw43_ll.c:509` |
| 97 | 3 | `pad5` | `uint8_t[3]` | declared pad field (`c-driver/cyw43_ll.c:510`) |
| 100 | 16 | `basic_mcs` | `uint8_t[16]` | `c-driver/cyw43_ll.c:511` |
| 116 | 2 | `ie_offset` | `uint16_t` | offset of the IEs from the start of this record (`c-driver/cyw43_ll.c:684`); the IE walk reads type/len byte pairs between ie_offset and ie_offset + ie_length (`c-driver/cyw43_ll.c:684-702`) |
| 118 | 2 | `pad6` | `uint8_t[2]` | declared pad field (`c-driver/cyw43_ll.c:513`) |
| 120 | 4 | `ie_length` | `uint32_t` | `c-driver/cyw43_ll.c:514` |
| 124 | 2 | `SNR` | `int16_t` | `c-driver/cyw43_ll.c:515` |
| 126 | 2 | (pad) | `uint8_t[2]` | compiler tail padding to 4-byte alignment (compiled) (`c-driver/cyw43_ll.c:486-516`) |

Size check: compiled

### `_scan_result_t (escan result wrapper, function-local struct)` (c-driver)
Event data of EV_ESCAN_RESULT, located at (uint8_t *)ev + 48 (`c-driver/cyw43_ll.c:675`); not packed; 140 bytes as declared, 12 fixed header + one bss record, with IEs following on the wire (compiled); byte order not stated, read natively (host order); defined at `c-driver/cyw43_ll.c:669-675`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `buflen` | `uint32_t` | `c-driver/cyw43_ll.c:670` |
| 4 | 4 | `version` | `uint32_t` | `c-driver/cyw43_ll.c:671` |
| 8 | 2 | `sync_id` | `uint16_t` | `c-driver/cyw43_ll.c:672` |
| 10 | 2 | `bss_count` | `uint16_t` | not read; the code assumes one record (`c-driver/cyw43_ll.c:673-675`) |
| 12 | 128 | `bss` | `cyw43_scan_result_internal_t` | followed on the wire by the IEs (`c-driver/cyw43_ll.c:674`, `c-driver/cyw43_ll.c:684`) |

Size check: compiled

### `auth IE offsets (RSN / WPA vendor IE, hand-parsed)` (c-driver)
IEs carried after the bss record in escan results (`c-driver/cyw43_ll.c:684-702`), used only to compute auth_mode and so 802.11 content rather than a record defined for the host interface (inferred); hand-parsed by byte offset; variable size (computed); counts read with cyw43_get_le16, little-endian (`c-driver/cyw43_ll.c:605`, `c-driver/cyw43_ll.c:627`); parsed at `c-driver/cyw43_ll.c:575-665`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 1 | `ie type` | `uint8_t` | 48 = RSN, 221 = vendor specific (`c-driver/cyw43_ll.c:689`, `c-driver/cyw43_ll.c:239-240`) |
| 1 | 1 | `ie len` | `uint8_t` | `c-driver/cyw43_ll.c:690` |
| 2 | 4 | (vendor: OUI + type) | `uint8_t[4]` | for the WPA IE, bytes 2..5 must equal 00 50 F2 01 (`c-driver/cyw43_ll.c:696`, `c-driver/cyw43_ll.c:241`); these bytes overlap the group cipher OUI field at offset 4. In an RSN IE the code never reads bytes 2..3 (`c-driver/cyw43_ll.c:590-605`); that they are a version field is (recalled, not in these sources) |
| 4 | 3 | `group cipher OUI` | `uint8_t[3]` | IE_AUTH_GROUP_CIPHER_OUI_OFFSET 4 (`c-driver/cyw43_ll.c:246`, `c-driver/cyw43_ll.c:590`). The same fixed offsets 4, 7, 8 are applied to both IE kinds (`c-driver/cyw43_ll.c:590-605`). For the vendor (WPA) IE the scan loop accepts the IE only when bytes 2..5 equal 00 50 F2 01 (`c-driver/cyw43_ll.c:696`), so byte 4 is 0xF2, while cyw43_ll_wifi_parse_ie_auth requires bytes 4..6 to equal the first three bytes of WPA_OUI_TYPE1, 00 50 F2 (`c-driver/cyw43_ll.c:584`, `c-driver/cyw43_ll.c:590`), so byte 4 would have to be 0x00; both cannot hold, so with wpa = 1 the function returns 0 at `c-driver/cyw43_ll.c:591` and that WPA result overwrites any RSN result (`c-driver/cyw43_ll.c:707-709`) (inferred from the code). The offsets 4 / 7 / 8 therefore describe only the RSN IE in practice (inferred) |
| 7 | 1 | `group cipher` | `uint8_t` | IE_AUTH_GROUP_CIPHER_OFFSET 7; 2 = TKIP, 4 = CCMP-128 (`c-driver/cyw43_ll.c:247`, `c-driver/cyw43_ll.c:593-599`, `c-driver/cyw43_ll.c:546-552`) |
| 8 | 2 | `pairwise cipher count` | `le16` | IE_AUTH_PAIRWISE_CIPHER_COUNT_OFFSET 8 (`c-driver/cyw43_ll.c:248`, `c-driver/cyw43_ll.c:605`) |
| 10 | variable (4 * count) | `pairwise suites` | `(uint8_t[3] oui, uint8_t type)[]` | `c-driver/cyw43_ll.c:606-624` |
| 10 + 4*n | 2 | `akm count` | `le16` | `c-driver/cyw43_ll.c:627` |
| 12 + 4*n | variable (4 * count) | `akm suites` | `(uint8_t[3] oui, uint8_t type)[]` | `c-driver/cyw43_ll.c:629-662` |

Size check: computed

### `cyw43_wifi_scan_options_t` (c-driver)
Value of the named variable "escan", sent as cyw43_write_iovar_n(self, "escan", sizeof(cyw43_wifi_scan_options_t), opts, STA) (`c-driver/cyw43_ll.c:2202`); not packed; 76 bytes, 72 used + 2 for channel_list[1] + 2 tail padding (compiled); byte order not stated, the struct is written natively and sent as bytes (host order); defined at `c-driver/cyw43_ll.h:255-270`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `version` | `uint32_t` | set to 1, comment ESCAN_REQ_VERSION (`c-driver/cyw43_ll.c:2191`). The driver overwrites every field except ssid_len, ssid and scan_type (`c-driver/cyw43_ll.c:2191-2201`) |
| 4 | 2 | `action` | `uint16_t` | set to 1, comment WL_SCAN_ACTION_START (`c-driver/cyw43_ll.c:2192`) |
| 6 | 2 | `_` | `uint16_t` | set to 0 (`c-driver/cyw43_ll.c:2193`) |
| 8 | 4 | `ssid_len` | `uint32_t` | caller supplied; 0 = all (`c-driver/cyw43_ll.h:259`). The public header says of the options "Values in here are currently ignored" (`c-driver/cyw43.h:366`), but ssid_len, ssid and scan_type are sent as the caller left them (`c-driver/cyw43_ll.c:2191-2202`) |
| 12 | 32 | `ssid` | `uint8_t[32]` | caller supplied (`c-driver/cyw43_ll.h:260`) |
| 44 | 6 | `bssid` | `uint8_t[6]` | set to ff:ff:ff:ff:ff:ff (`c-driver/cyw43_ll.c:2194`) |
| 50 | 1 | `bss_type` | `int8_t` | set to 2, comment WICED_BSS_TYPE_ANY (`c-driver/cyw43_ll.c:2195`) |
| 51 | 1 | `scan_type` | `int8_t` | caller supplied; 0 = active, 1 = passive (`c-driver/cyw43_ll.h:263`) |
| 52 | 4 | `nprobes` | `int32_t` | -1 (`c-driver/cyw43_ll.c:2196`) |
| 56 | 4 | `active_time` | `int32_t` | -1 (`c-driver/cyw43_ll.c:2197`) |
| 60 | 4 | `passive_time` | `int32_t` | -1 (`c-driver/cyw43_ll.c:2198`) |
| 64 | 4 | `home_time` | `int32_t` | -1 (`c-driver/cyw43_ll.c:2199`) |
| 68 | 4 | `channel_num` | `int32_t` | 0 (`c-driver/cyw43_ll.c:2200`) |
| 72 | 2 | `channel_list` | `uint16_t[1]` | 0 (`c-driver/cyw43_ll.c:2201`) |
| 74 | 2 | (pad) | `uint8_t[2]` | compiler tail padding (compiled); sent on the wire because sizeof() is used, content is whatever the caller's struct held (`c-driver/cyw43_ll.c:2202`, `c-driver/cyw43_ll.h:255-270`) |

Size check: compiled

### `iovar_set_u32 (hand-built)` (c-driver)
Payload of command WLC_SET_VAR (263) for named variables that carry one u32: bus:txglom, apsta, ampdu_ba_wsize, ampdu_mpdu, ampdu_rx_factor, pm2_sleep_ret, bcn_li_bcn, bcn_li_dtim, assoc_listen, mfp, 2g_mrate, sae_max_pwe_loop (`c-driver/cyw43_ll.c:1918-1919`, `c-driver/cyw43_ll.c:2212`, `c-driver/cyw43_ll.c:2379`, `c-driver/cyw43_ll.c:2037-2041`, `c-driver/cyw43_ll.c:2148-2156`, `c-driver/cyw43_ll.c:2276`, `c-driver/cyw43_ll.c:2401`, `c-driver/cyw43_ll.c:2439`, `c-driver/cyw43_ll.c:2446`), with the same shape built by hand for roam_off in `c-driver/cyw43_ctrl.c:683-696`; hand-built in a byte buffer; variable size, strlen(name) + 1 + 4 (computed); little-endian (cyw43_put_le32, `c-driver/cyw43_ll.c:1542`); built at `c-driver/cyw43_ll.c:1538-1544`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | variable (strlen + 1) | `name` | `char[]` | NUL-terminated variable name (`c-driver/cyw43_ll.c:1540-1541`) |
| strlen + 1 | 4 | `value` | `le32` | not aligned: it follows the NUL directly (`c-driver/cyw43_ll.c:1542`). The roam_off writer in cyw43_ctrl.c stores only the low byte and three zero bytes, which is the same le32 layout (`c-driver/cyw43_ctrl.c:692-695`). At `c-driver/cyw43_ll.c:2439` the call is cyw43_write_iovar_u32(self, "sae_max_pwe_loop", WWD_AP_INTERFACE, 5): by the function signature (name, val, iface) at `c-driver/cyw43_ll.c:1538` that sends value 1 on interface 5, which looks like swapped arguments (inferred) |

Size check: computed

### `iovar_set_u32_u32 (hand-built)` (c-driver)
Payload of command WLC_SET_VAR for named variables that carry two u32: bsscfg:sup_wpa (0, 0/1), bsscfg:sup_wpa2_eapver (0, -1), bsscfg:sup_wpa_tmo (0, 5000) (`c-driver/cyw43_ll.c:2240-2248`, `c-driver/cyw43_ll.c:258`), bsscfg:wsec (AP, auth) (`c-driver/cyw43_ll.c:2392`), bsscfg:wpa_auth (AP, val) (`c-driver/cyw43_ll.c:2418`), bss (AP, up) (`c-driver/cyw43_ll.c:2457`) and gpioout (1 << n, then 1 << n to set or 0 to clear) (`c-driver/cyw43_ll.c:2508`); hand-built in a byte buffer; variable size, strlen(name) + 1 + 8 (computed); little-endian (`c-driver/cyw43_ll.c:1550-1551`); built at `c-driver/cyw43_ll.c:1546-1553`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | variable (strlen + 1) | `name` | `char[]` | NUL-terminated (`c-driver/cyw43_ll.c:1548-1549`) |
| strlen + 1 | 4 | `val0` | `le32` | for the bsscfg: variables and "bss" this is the interface / bsscfg index; for gpioout it is the mask (`c-driver/cyw43_ll.c:1550`) |
| strlen + 5 | 4 | `val1` | `le32` | the value (`c-driver/cyw43_ll.c:1551`) |

Size check: computed

### `iovar_set_n / iovar_get (hand-built, generic)` (c-driver)
Generic payload of command WLC_SET_VAR (`c-driver/cyw43_ll.c:1561`), written by cyw43_write_iovar_n for cur_etheraddr (`c-driver/cyw43_ll.c:1941`), mcast_list (`c-driver/cyw43_ll.c:2129`), escan (`c-driver/cyw43_ll.c:2202`), sae_password (`c-driver/cyw43_ll.c:2266`, `c-driver/cyw43_ll.c:2426`), join (`c-driver/cyw43_ll.c:2325`) and bsscfg:ssid (`c-driver/cyw43_ll.c:2386`), together with the get form under command WLC_GET_VAR (262) used by cyw43_read_iovar_u32 (`c-driver/cyw43_ll.c:1969-1975`) for pm2_sleep_ret, bcn_li_bcn, bcn_li_dtim, assoc_listen (`c-driver/cyw43_ll.c:2180-2183`) and by the roam_off get (`c-driver/cyw43_ctrl.c:699-717`); hand-built in a byte buffer; variable size, strlen(name) + 1 + len (computed); value bytes as supplied by the caller; built at `c-driver/cyw43_ll.c:1556-1562`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | variable (strlen + 1) | `name` | `char[]` | NUL-terminated (`c-driver/cyw43_ll.c:1558`, `c-driver/cyw43_ll.c:1560`) |
| strlen + 1 | variable (len) | `value` | `uint8_t[]` | set: memmove'd first, since the caller's buffer may overlap (`c-driver/cyw43_ll.c:1559`). get: the request sends name + NUL followed by zero bytes for the expected result size, and the reply overwrites the buffer from offset 0 with the value, not after the name (`c-driver/cyw43_ll.c:1969-1975`, `c-driver/cyw43_ll.c:2080`, `c-driver/cyw43_ll.c:2098`, `c-driver/cyw43_ll.c:2364`, `c-driver/cyw43_ll.c:2475`, `c-driver/cyw43_ll.c:2526`). Examples of get request sizes: clmver sends 7 name bytes with len 128, the other 121 bytes being leftover buffer content, and prints the reply as a string (`c-driver/cyw43_ll.c:2028-2030`); ccgpioin sends 9 bytes, reply le32 (`c-driver/cyw43_ll.c:2520-2526`); clmload_status sends 19 bytes, reply u32 read natively, non-zero = failure (`c-driver/cyw43_ll.c:1527-1533`) |

Size check: computed

### `ioctl_u32 (hand-built)` (c-driver)
Payload of numbered commands that take or return one 32-bit value: WLC_SET_ANTDIV 64 (`c-driver/cyw43_ll.c:2034`), WLC_SET_PM 86 / WLC_GET_PM 85 (`c-driver/cyw43_ll.c:2165`, `c-driver/cyw43_ll.c:2184`), WLC_SET_GMODE 110 (`c-driver/cyw43_ll.c:2170`, `c-driver/cyw43_ll.c:2443`), WLC_SET_BAND 142 (`c-driver/cyw43_ll.c:2173`), WLC_SET_WSEC 134 (`c-driver/cyw43_ll.c:2236`), WLC_SET_INFRA 20 (`c-driver/cyw43_ll.c:2271`), WLC_SET_AUTH 22 (`c-driver/cyw43_ll.c:2275`), WLC_SET_WPA_AUTH 165 (`c-driver/cyw43_ll.c:2280`, `c-driver/cyw43_ll.c:2337`), WLC_SET_CHANNEL 30 (`c-driver/cyw43_ll.c:2389`), WLC_SET_DTIMPRD 78 (`c-driver/cyw43_ll.c:2449`), and in the control layer CYW43_IOCTL_GET_RSSI as int32 (`c-driver/cyw43_ctrl.c:728`) and the roam trigger / delta / scan period and interference mode wrappers (`c-driver/cyw43.h:242-254`, `c-driver/cyw43.h:471-513`); hand-built; 4 bytes (computed); little-endian in cyw43_ll.c (cyw43_put_le32 / cyw43_get_le32, `c-driver/cyw43_ll.c:1958`, `c-driver/cyw43_ll.c:1966`) and host-native in cyw43_ctrl.c, which passes a pointer to a uint32_t (`c-driver/cyw43_ctrl.c:446-452`); built at `c-driver/cyw43_ll.c:1956-1967`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `value` | `le32` | `c-driver/cyw43_ll.c:1958`. WLC_SET_GMODE and WLC_SET_BAND in cyw43_ll_wifi_pm are built by hand with the same 4-byte le32 payload rather than through cyw43_set_ioctl_u32 (`c-driver/cyw43_ll.c:2168-2173`). Commands with other payloads: WLC_UP (2) and CYW43_IOCTL_SET_DISASSOC are sent with a zero-length payload (`c-driver/cyw43_ll.c:2065`, `c-driver/cyw43_ctrl.c:220`, `c-driver/cyw43_ctrl.c:678`); WLC_GET_BSSID returns 6 bytes straight into the caller's buffer (`c-driver/cyw43_ll.c:2347`). WLC numbers are defined at `c-driver/cyw43_ll.c:167-187`; the public CYW43_IOCTL_* numbers are (WLC number << 1) \| set-bit (`c-driver/cyw43_ll.c:1329`, `c-driver/cyw43_ll.h:29-47`) |

Size check: computed

### `clmload chunk (hand-built)` (c-driver)
Value of the named variable "clmload", set with command WLC_SET_VAR on the STA interface, one request per chunk (`c-driver/cyw43_ll.c:1522`), with chunk size 1024 for SPI and 1024 + 512 for SDIO (`c-driver/cyw43_ll.c:1485-1489`), followed by a "clmload_status" get (`c-driver/cyw43_ll.c:1527-1533`); hand-built, 16/32-bit fields stored with native pointer writes; variable size, 20 fixed bytes including the 8-byte name + chunk data, padded to a multiple of 8 (computed); byte order not stated, native *(uint16_t *) / *(uint32_t *) stores, so host order (`c-driver/cyw43_ll.c:1512-1515`); built at `c-driver/cyw43_ll.c:1491-1523`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 8 | `name` | `char[8]` | "clmload\0" (`c-driver/cyw43_ll.c:1508`). Without the variable name the record is 12 fixed bytes: flag@0, type@2, len@4, zero@8, data@12 (computed) (`c-driver/cyw43_ll.c:1512-1517`) |
| 8 | 2 | `flag` | `uint16_t` | 1 << 12 (comment DLOAD_HANDLER_VER) \| 2 on the first chunk (DL_BEGIN) \| 4 on the last (DL_END) (`c-driver/cyw43_ll.c:1500-1506`, `c-driver/cyw43_ll.c:1512`) |
| 10 | 2 | `type` | `uint16_t` | constant 2; the source gives no name for it, `type` is a descriptive label (`c-driver/cyw43_ll.c:1513`) |
| 12 | 4 | `len` | `uint32_t` | number of data bytes in this chunk (`c-driver/cyw43_ll.c:1514`) |
| 16 | 4 | (crc / reserved) | `uint32_t` | constant 0; the source gives no name for it, the label is descriptive (`c-driver/cyw43_ll.c:1515`) |
| 20 | variable (len) | `data` | `uint8_t[]` | chunk of the CLM data (`c-driver/cyw43_ll.c:1517`); flexible tail |
| 20 + len | variable (0..7) | (pad) | `uint8_t[]` | request length is ALIGN_UINT(20 + len, 8); padding is leftover buffer content (`c-driver/cyw43_ll.c:1521-1522`) |

Size check: computed

### `country iovar value (hand-built)` (c-driver)
Value of the named variable "country", set with command WLC_SET_VAR on the STA interface in cyw43_ll_wifi_on (`c-driver/cyw43_ll.c:2022`); hand-built; 20 bytes including the 8-byte name, 12 without (computed); little-endian (cyw43_put_le32, `c-driver/cyw43_ll.c:2015-2021`); built at `c-driver/cyw43_ll.c:2014-2022`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 8 | `name` | `char[8]` | "country\0" (`c-driver/cyw43_ll.c:2014`). The source does not name the three fields that follow; the names here describe the values written (`c-driver/cyw43_ll.c:2015-2021`) |
| 8 | 4 | `country (first copy)` | `le32` | country & 0xffff: two ASCII letters in the low two bytes, then two zero bytes (`c-driver/cyw43_ll.c:2015`, `c-driver/cyw43_country.h:24`) |
| 12 | 4 | `revision` | `le32` | country >> 16, or 0xffffffff (-1) when the revision is 0 (`c-driver/cyw43_ll.c:2016-2020`). For SDIO builds the worldwide code XX gets revision 17 first (`c-driver/cyw43_ll.c:2005-2010`, `c-driver/cyw43_country.h:34`) |
| 16 | 4 | `country (second copy)` | `le32` | country & 0xffff again (`c-driver/cyw43_ll.c:2021`) |

Size check: computed

### `bsscfg:event_msgs value (hand-built)` (c-driver)
Value of the named variable "bsscfg:event_msgs", set with command WLC_SET_VAR, length 18 + 4 + 19, on the STA interface (`c-driver/cyw43_ll.c:2060`); hand-built; 41 bytes, 18 name + 4 + 19 (computed); the 4-byte index is not written by this code and the mask is a byte array in which event number i is byte i / 8, bit i % 8 (`c-driver/cyw43_ll.c:2052`); built at `c-driver/cyw43_ll.c:2051-2060`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 18 | `name` | `char[18]` | "bsscfg:event_msgs\0" (`c-driver/cyw43_ll.c:2059`) |
| 18 | 4 | `bsscfg index` (inferred) | `uint8_t[4]` | not written here: the buffer bytes 18..21 keep whatever the previous command left (`c-driver/cyw43_ll.c:2051-2060`). The commented-out variant writes 00 00 00 00 (`c-driver/cyw43_ll.c:2292`). The meaning of the 4 bytes as a bsscfg index is (inferred) from the other bsscfg: variables in this file (`c-driver/cyw43_ll.c:2240`, `c-driver/cyw43_ll.c:2382`, `c-driver/cyw43_ll.c:2392`) |
| 22 | 19 | `event mask` | `uint8_t[19]` | memset to 0xff, then bits 20, 40, 44, 54, 71 cleared (`c-driver/cyw43_ll.c:2051-2057`); comments name the cleared events: 20 tx fail, 40 radio, 44 probe request, 54 interface change, 71 probe response (`c-driver/cyw43_ll.c:2053-2057`). The commented-out join-time variant uses an 18-byte mask (`c-driver/cyw43_ll.c:2292-2293`) |

Size check: computed

### `cur_etheraddr value (hand-built)` (c-driver)
Value of the named variable "cur_etheraddr", read with command WLC_GET_VAR (`c-driver/cyw43_ll.c:2077-2080`) and set with WLC_SET_VAR via cyw43_write_iovar_n(..., 6, mac) (`c-driver/cyw43_ll.c:1941`); hand-built; 6 bytes for the value, the get request being 14 + 6 = 20 bytes (computed); byte array; built at `c-driver/cyw43_ll.c:2072-2083`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 14 | `name` | `char[14]` | "cur_etheraddr\0" (`c-driver/cyw43_ll.c:2077`) |
| 14 | 6 | `mac` | `uint8_t[6]` | zeros in the get request (`c-driver/cyw43_ll.c:2077`); the MAC in the set request (`c-driver/cyw43_ll.c:1941`). Get reply: the 6 MAC bytes are at offset 0 of the reply (`c-driver/cyw43_ll.c:2080`) |

Size check: computed

### `mcast_list value (hand-built)` (c-driver)
Value of the named variable "mcast_list", read with command WLC_GET_VAR (request: 11 name bytes + 64 zero bytes, `c-driver/cyw43_ll.c:2090-2092`) and set with WLC_SET_VAR with the full 64 bytes (`c-driver/cyw43_ll.c:2129`); hand-built; 64 bytes, 4 + 10 * 6 (computed); count little-endian (cyw43_get_le32 / cyw43_put_le32, `c-driver/cyw43_ll.c:2098`, `c-driver/cyw43_ll.c:2126`); built at `c-driver/cyw43_ll.c:2085-2133`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `count` | `le32` | number of valid addresses (`c-driver/cyw43_ll.c:2098`, `c-driver/cyw43_ll.c:2126`) |
| 4 | 60 | `addrs` | `uint8_t[10][6]` | MAX_MULTICAST_REGISTERED_ADDRESS = 10 (`c-driver/cyw43_ll.c:253`); the set always sends all 10 slots regardless of count, unused slots as they are (`c-driver/cyw43_ll.c:2129`) |

Size check: computed

### `wsec_pmk (hand-built)` (c-driver)
Payload of command WLC_SET_WSEC_PMK (268), sent on STA join (`c-driver/cyw43_ll.c:2258`) and AP init (`c-driver/cyw43_ll.c:2434`), with the source comment "68, see wsec_pmk_t" (`c-driver/cyw43_ll.c:2258`); hand-built; 68 bytes, 2 + 2 + 64 (computed); little-endian (cyw43_put_le16, `c-driver/cyw43_ll.c:2252-2253`); built at `c-driver/cyw43_ll.c:2252-2258`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 2 | `key_len` | `le16` | `c-driver/cyw43_ll.c:2252` |
| 2 | 2 | `flags` | `le16` | constant 1; the source gives no name, `flags` is a descriptive label (`c-driver/cyw43_ll.c:2253`, `c-driver/cyw43_ll.c:2430`) |
| 4 | 64 | `key` | `uint8_t[64]` | passphrase bytes; CYW43_WPA_MAX_PASSWORD_LEN 64 (`c-driver/cyw43_ll.c:277`). The AP path zero-fills the 64 key bytes first (`c-driver/cyw43_ll.c:2431`); in the STA path the bytes after the key (offset 4 + key_len up to 67) come from an uninitialised stack buffer (`c-driver/cyw43_ll.c:2210`, `c-driver/cyw43_ll.c:2252-2254`) |

Size check: computed

### `sae_password value (hand-built)` (c-driver)
Value of the named variable "sae_password", set with command WLC_SET_VAR on the STA interface (`c-driver/cyw43_ll.c:2266`) and the AP interface (`c-driver/cyw43_ll.c:2426`); hand-built; 130 bytes, 2 + 128 (computed); little-endian length (`c-driver/cyw43_ll.c:2263`, `c-driver/cyw43_ll.c:2422`); built at `c-driver/cyw43_ll.c:2262-2266`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 2 | `password_len` | `le16` | `c-driver/cyw43_ll.c:2263` |
| 2 | 128 | `password` | `uint8_t[128]` | zero-filled then the password; CYW43_WPA_SAE_MAX_PASSWORD_LEN 128 (`c-driver/cyw43_ll.c:278`, `c-driver/cyw43_ll.c:2262-2264`) |

Size check: computed

### `join iovar value (hand-built)` (c-driver)
Value of the named variable "join", set with command WLC_SET_VAR on the STA interface when a BSSID is supplied (`c-driver/cyw43_ll.c:2325`), which comments split into ssid, "scan params" (20 bytes at 36) and "assoc params" (14 bytes at 56) (`c-driver/cyw43_ll.c:2304`, `c-driver/cyw43_ll.c:2311`); hand-built; 70 bytes, 4 + 32 + 20 + 14 (computed); little-endian (cyw43_put_le32 / cyw43_put_le16, `c-driver/cyw43_ll.c:2301-2320`); built at `c-driver/cyw43_ll.c:2299-2325`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `ssid_len` | `le32` | `c-driver/cyw43_ll.c:2301`. Without a BSSID the driver sends command WLC_SET_SSID instead, see `WLC_SET_SSID value (hand-built)` (`c-driver/cyw43_ll.c:2326-2329`) |
| 4 | 32 | `ssid` | `uint8_t[32]` | `c-driver/cyw43_ll.c:2302` |
| 36 | 1 | `scan_type` | `uint8_t` | 0 (`c-driver/cyw43_ll.c:2305`) |
| 37 | 3 | (pad) | `uint8_t[3]` | not written after the memset to zero (`c-driver/cyw43_ll.c:2300`) |
| 40 | 4 | `nprobes` | `le32` | -1 (`c-driver/cyw43_ll.c:2306`) |
| 44 | 4 | `active_time` | `le32` | -1 (`c-driver/cyw43_ll.c:2307`) |
| 48 | 4 | `passive_time` | `le32` | -1 (`c-driver/cyw43_ll.c:2308`) |
| 52 | 4 | `home_time` | `le32` | -1 (`c-driver/cyw43_ll.c:2309`) |
| 56 | 6 | `bssid` | `uint8_t[6]` | `c-driver/cyw43_ll.c:2316` |
| 62 | 2 | (pad) | `uint8_t[2]` | zero, not written after the memset (`c-driver/cyw43_ll.c:2300`) |
| 64 | 4 | `chanspec_num` | `le32` | 1 when a channel is given, else 0 (`c-driver/cyw43_ll.c:2317-2318`) |
| 68 | 2 | `chanspec_list[0]` | `le16` | channel \| 0x1000 (WL_CHANSPEC_BW_20) \| 0 \| 0 (2G) (`c-driver/cyw43_ll.c:2312-2320`) |

Size check: computed

### `WLC_SET_SSID value (hand-built)` (c-driver)
Payload of command WLC_SET_SSID (26), length 36, taken from self->last_ssid_joined on join without BSSID (`c-driver/cyw43_ll.c:2329`) and on rejoin (`c-driver/cyw43_ll.c:2342`), the buffer being declared as last_ssid_joined[36] (`c-driver/cyw43_internal.h:37`); hand-built; 36 bytes, 4 + 32 (computed); little-endian length (`c-driver/cyw43_ll.c:2296`); built at `c-driver/cyw43_ll.c:2296-2297`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `ssid_len` | `le32` | `c-driver/cyw43_ll.c:2296` |
| 4 | 32 | `ssid` | `uint8_t[32]` | only ssid_len bytes are copied; bytes after the SSID are whatever last_ssid_joined held before (`c-driver/cyw43_ll.c:2297`) |

Size check: computed

### `bsscfg:ssid value (hand-built)` (c-driver)
Value of the named variable "bsscfg:ssid", set with command WLC_SET_VAR in AP init and sent on the STA interface (`c-driver/cyw43_ll.c:2386`); hand-built; 40 bytes, 4 + 4 + 32 (computed); little-endian (`c-driver/cyw43_ll.c:2382-2383`); built at `c-driver/cyw43_ll.c:2382-2386`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `bsscfg index` | `le32` | WWD_AP_INTERFACE = 1 (`c-driver/cyw43_ll.c:2382`, `c-driver/cyw43_ll.c:152`) |
| 4 | 4 | `ssid_len` | `le32` | `c-driver/cyw43_ll.c:2383` |
| 8 | 32 | `ssid` | `uint8_t[32]` | zero-filled then the SSID (`c-driver/cyw43_ll.c:2384-2385`) |

Size check: computed

### `bss / maxassoc get request (hand-built)` (c-driver)
Request of command WLC_GET_VAR for the named variable "bss", to read the AP state (`c-driver/cyw43_ll.c:2363-2364`), and for "maxassoc" (`c-driver/cyw43_ll.c:2470-2475`), both replies being one le32 at offset 0; hand-built; 8 bytes for bss (4 name + 4) and 13 for maxassoc (9 name + 4) (computed); little-endian (`c-driver/cyw43_ll.c:2362`, `c-driver/cyw43_ll.c:2469`); built at `c-driver/cyw43_ll.c:2361-2364` and `c-driver/cyw43_ll.c:2468-2475`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 or 9 | `name` | `char[]` | "bss\0" (`c-driver/cyw43_ll.c:2361`) or "maxassoc\0" (`c-driver/cyw43_ll.c:2468`). The maxassoc request is issued twice in a row (`c-driver/cyw43_ll.c:2470-2471`) |
| 4 or 9 | 4 | `interface` | `le32` | WWD_AP_INTERFACE = 1 (`c-driver/cyw43_ll.c:2362`, `c-driver/cyw43_ll.c:2469`, `c-driver/cyw43_ll.c:152`). Source comment on the bss reply: "le or be?" (`c-driver/cyw43_ll.c:2364`), so the reply byte order is marked uncertain in the source |

Size check: computed

### `WLC_GET_ASSOCLIST value (hand-built)` (c-driver)
Payload of command WLC_GET_ASSOCLIST (159) on the AP interface, length 4 + maxassoc * 6 (`c-driver/cyw43_ll.c:2490`); hand-built; variable size, 4 + 6 * count (computed); count little-endian (`c-driver/cyw43_ll.c:2489`, `c-driver/cyw43_ll.c:2494`); built at `c-driver/cyw43_ll.c:2489-2496`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `count` | `le32` | request: capacity (max entries) (`c-driver/cyw43_ll.c:2489`); reply: number of associated stations (`c-driver/cyw43_ll.c:2494`) |
| 4 | variable (6 * count) | `macs` | `uint8_t[][6]` | flexible tail (`c-driver/cyw43_ll.c:2496`) |

Size check: computed

### `SPI command word (hand-built)` (c-driver)
Start of every SPI transfer, a 4-byte command followed by the payload padded to a multiple of 4 (`c-driver/cyw43_spi.c:64-66`, `c-driver/cyw43_spi.c:89-91`); bit-packed 32-bit word; 4 bytes (computed); little-endian in normal operation (cyw43_put_le32, `c-driver/cyw43_spi.c:78`, `c-driver/cyw43_spi.c:95`), and before the bus is configured sent with the two bytes of each 16-bit half swapped (cyw43_put_swap32, `c-driver/cyw43_spi.c:19-24`, `c-driver/cyw43_spi.c:40`); built at `c-driver/cyw43_spi.c:33-35`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| bit 31 | 1 bit | `write` | `bit 31` | 1 = write (`c-driver/cyw43_spi.c:34`). Register values are passed as native-order bytes (`c-driver/cyw43_spi.c:102-130`) |
| bit 30 | 1 bit | `inc` | `bit 30` | address increment; always true here (`c-driver/cyw43_spi.c:78`, `c-driver/cyw43_spi.c:95`) |
| bit 28 | 2 bits | `fn` | `bits 29..28` | 0 bus, 1 backplane, 2 WLAN (`c-driver/cyw43_internal.h:17-19`). Backplane (function 1) reads have CYW43_BACKPLANE_READ_PAD_LEN_BYTES = 16 dummy bytes between command and data (`c-driver/cyw43_spi.c:68-75`, `c-driver/cyw43_ll.h:194`); the same value is written to SPI_RESP_DELAY_F1 (`c-driver/cyw43_ll.c:1612`) |
| bit 11 | 17 bits | `addr` | `bits 27..11` | addr & 0x1ffff (`c-driver/cyw43_spi.c:34`) |
| bit 0 | 11 bits | `sz` | `bits 10..0` | length in bytes; not masked by pack_cmd (`c-driver/cyw43_spi.c:34`). The length of a pending rx frame is not taken from a header but from the SPI status register: bit 8 = packet available (tested with GSPI_PACKET_AVAILABLE 0x0100), bits 9..19 = byte count ((status >> 9) & 0x7FF) (`c-driver/cyw43_ll.c:1216`, `c-driver/cyw43_ll.c:1227-1228`, `c-driver/cyw43_spi.h:67`); the header also names these bits STATUS_F2_PKT_AVAILABLE and STATUS_F2_PKT_LEN_MASK / _SHIFT (`c-driver/cyw43_spi.h:87-89`) |

Size check: computed

### `SPI bus configuration word (hand-built)` (c-driver)
Word written once to bus function 0, address 0 (`c-driver/cyw43_ll.c:1605`; source comment: "Switch to 32bit mode", `c-driver/cyw43_ll.c:1602`) after reading TEST_PATTERN 0xFEEDBEAD from SPI_READ_TEST_REGISTER 0x14 (`c-driver/cyw43_ll.c:1593-1594`, `c-driver/cyw43_spi.h:18`, `c-driver/cyw43_spi.h:31`); 32-bit word with one byte per bus register 0..3; 4 bytes (computed); sent with cyw43_put_swap32 (16-bit halves byte-swapped) by write_reg_u32_swap (`c-driver/cyw43_spi.c:51-56`); built at `c-driver/cyw43_ll.c:1574-1578`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 1 | `SPI_BUS_CONTROL` | `uint8_t` | WORD_LENGTH_32 0x01 \| ENDIAN_BIG 0x02 \| HIGH_SPEED_MODE 0x10 \| WAKE_UP 0x80, plus INTERRUPT_POLARITY_HIGH 0x20 if CYW43_PIN_WL_HOST_WAKE is defined (`c-driver/cyw43_ll.c:1574-1578`, `c-driver/cyw43_spi.h:42-48`). The offset column is the register address, i.e. byte significance in the 32-bit value (byte 0 = least significant), which follows from the shifts 8 * register address in the source (`c-driver/cyw43_ll.c:1575`) |
| 1 | 1 | `SPI_RESPONSE_DELAY` | `uint8_t` | 0x4 (`c-driver/cyw43_ll.c:1575`) |
| 2 | 1 | `SPI_STATUS_ENABLE` | `uint8_t` | INTR_WITH_STATUS 0x02 (`c-driver/cyw43_ll.c:1575`, `c-driver/cyw43_spi.h:52`) |
| 3 | 1 | `SPI_RESET_BP` | `uint8_t` | 0 (not set) (`c-driver/cyw43_ll.c:1574-1578`) |

Size check: computed

### `SDIO CMD52 / CMD53 argument (hand-built)` (c-driver)
Argument word of SDIO register and data access (`c-driver/cyw43_sdio.c:24-53`); bit-packed 32-bit word; 4 bytes (computed); byte order not stated, passed as a uint32_t to the port's cyw43_sdio_transfer; built at `c-driver/cyw43_sdio.c:17-19`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| bit 31 | 1 bit | `write` | `bit 31` | `c-driver/cyw43_sdio.c:18` |
| bit 28 | 3 bits | `fn` | `bits 30..28` | `c-driver/cyw43_sdio.c:18` |
| bit 27 | 1 bit | `block_mode` | `bit 27` | CMD53 only: 1 when len > 512 (`c-driver/cyw43_sdio.c:38-50`) |
| bit 26 | 1 bit | `inc` | `bit 26` | CMD53: true (`c-driver/cyw43_sdio.c:51`); CMD52: false (`c-driver/cyw43_sdio.c:25`) |
| bit 9 | 17 bits | `addr` | `bits 25..9` | addr & 0x1ffff, masked by the callers before packing (`c-driver/cyw43_sdio.c:25`, `c-driver/cyw43_sdio.c:51`) |
| bit 0 | 9 bits | `len / data` | `bits 8..0` | CMD52: the data byte, val & 0xff; CMD53 byte mode: len & 0x1ff with 512 encoded as 0; block mode: number of 64-byte blocks (`c-driver/cyw43_sdio.c:25`, `c-driver/cyw43_sdio.c:43`, `c-driver/cyw43_sdio.c:49`). Byte-mode lengths are rounded up to CYW43_SDIO_CMD53_BYTE_MODE_DATA_ALIGN, default 4 (`c-driver/cyw43_sdio.c:42`, `c-driver/cyw43_config.h:32-33`); block-mode lengths to 64 (`c-driver/cyw43_sdio.c:46-48`). On SDIO rx the driver first reads 4 bytes, then the remainder rounded up to 8, 16 or a multiple of 64 (`c-driver/cyw43_ll.c:1119-1138`) |

Size check: computed

### `NVRAM length word (hand-built)` (c-driver)
Word written to chip RAM at CYW43_RAM_SIZE - 4 (512 KiB - 4) after the NVRAM text is written just below it at CYW43_RAM_SIZE - 4 - len (`c-driver/cyw43_ll.c:1798-1802`, `c-driver/cyw43_ll.c:41`); 32-bit word; 4 bytes (computed); byte order not stated, written with cyw43_write_backplane as a 32-bit value; built at `c-driver/cyw43_ll.c:1798-1802`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| bit 0 | 16 bits | `nvram length in words` | `bits 15..0` | wifi_nvram_len / 4 (`c-driver/cyw43_ll.c:1801`). The NVRAM length is padded to 4 bytes on SPI and 64 on SDIO before use (`c-driver/cyw43_ll.c:1798`, `c-driver/cyw43_ll.c:45-51`). The layout of the NVRAM content itself is not described by c-driver's download code (`c-driver/cyw43_ll.c:1798-1802`) |
| bit 16 | 16 bits | `complement` | `bits 31..16` | ~(wifi_nvram_len / 4) & 0xffff (`c-driver/cyw43_ll.c:1801`) |

Size check: computed

### `Bluetooth HCI UART command (hand-built)` (c-driver)
Commands sent to the Bluetooth controller over UART in cyw43_bluetooth_controller_init: reset (ogf 3, ocf 3), sent twice (`c-driver/cyw43_bthci_uart.c:217`, `c-driver/cyw43_bthci_uart.c:240`), vendor ogf 0x3f commands 0x18 set baudrate with 6 parameter bytes = le16 0 + le32 baudrate (`c-driver/cyw43_bthci_uart.c:134-138`), 0x2e before patch download (`c-driver/cyw43_bthci_uart.c:143`), 0x0001 set BD_ADDR with 6 bytes in reversed order (`c-driver/cyw43_bthci_uart.c:243-252`) and 0x27 sleep mode with 12 fixed bytes 01 02 02 00 00 00 01 00 00 00 00 00 (`c-driver/cyw43_bthci_uart.c:255`), and ogf 3 ocf 109 with 01 00, commented HCI_Write_LE_Host_Support (`c-driver/cyw43_bthci_uart.c:258`); hand-built; variable size, 4 fixed bytes + parameters, max 256 (computed); opcode low byte first; built at `c-driver/cyw43_bthci_uart.c:124-131`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 1 | `packet type` | `uint8_t` | 0x01 (`c-driver/cyw43_bthci_uart.c:126`). This is the UART path, and the whole file is compiled only when CYW43_ENABLE_BLUETOOTH_OVER_UART is set (`c-driver/cyw43_bthci_uart.c:15`). A second Bluetooth transport, cyw43_btbus_init / _read / _write, is declared in `c-driver/cyw43_btbus.h:19-21` and called from `c-driver/cyw43_ctrl.c:820`, `c-driver/cyw43_ctrl.c:841`, `c-driver/cyw43_ctrl.c:856`; its implementation is not found in c-driver. cyw43_bluetooth_hci_write notes only that the buffer needs a 4-byte header included in len (`c-driver/cyw43_ctrl.c:849-850`); that header's layout is not found in c-driver |
| 1 | 1 | `opcode low` | `uint8_t` | ocf (`c-driver/cyw43_bthci_uart.c:127`) |
| 2 | 1 | `opcode high` | `uint8_t` | ogf << 2 \| ocf >> 8 (`c-driver/cyw43_bthci_uart.c:128`) |
| 3 | 1 | `param_len` | `uint8_t` | `c-driver/cyw43_bthci_uart.c:129`. It is a single byte while the assert allows 256 (`c-driver/cyw43_bthci_uart.c:79`), so 255 is the largest length the header can express |
| 4 | variable (param_len) | `params` | `uint8_t[]` | HCI_PAYLOAD_LEN_MAX 256 (`c-driver/cyw43_bthci_uart.c:22`, `c-driver/cyw43_bthci_uart.c:85-88`). The patch download loop reads records of 3 header bytes (opcode low, opcode high which must be 0xfc, length) followed by that many bytes and replays each as a command, stopping after opcode low 0x4e (`c-driver/cyw43_bthci_uart.c:147-171`) |

Size check: computed

### `Bluetooth HCI UART command-complete response (hand-parsed)` (c-driver)
Reply to each HCI command in cyw43_bluetooth_hci_cmd_raw (`c-driver/cyw43_bthci_uart.c:78-122`); hand-parsed; variable size, 6 fixed bytes + sz (computed); byte fields; parsed at `c-driver/cyw43_bthci_uart.c:93-121`.

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 1 | `packet type` | `uint8_t` | must be 0x04 (`c-driver/cyw43_bthci_uart.c:103`) |
| 1 | 1 | `event code` | `uint8_t` | must be 0x0e, command complete (`c-driver/cyw43_bthci_uart.c:102-103`) |
| 2 | 1 | `length` | `uint8_t` | remaining payload read is length - 3 bytes (`c-driver/cyw43_bthci_uart.c:109`) |
| 3 | 3 | (not examined) | `uint8_t[3]` | read as part of the 6-byte header (HCI_RESP_HEADER_LEN 6, `c-driver/cyw43_bthci_uart.c:21`, `c-driver/cyw43_bthci_uart.c:94`) but not inspected |
| 6 | variable (length - 3) | `return bytes` | `uint8_t[]` | first 4 are handed back to the caller; byte 0 is checked as status == 0 during patch download (`c-driver/cyw43_bthci_uart.c:116-118`, `c-driver/cyw43_bthci_uart.c:164`) |

Size check: computed
