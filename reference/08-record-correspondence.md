# Record correspondence across drivers

Records that serve the same purpose in two or more drivers, matched by purpose and field names rather than by record name, followed by the places where their layouts differ. Records with no counterpart in a second driver are in the per-driver record chapters.

## Conventions

- "—": no counterpart for that driver was found in these sources; it is not a claim that the driver lacks one.
- "no struct": the driver builds or parses the bytes by hand at the cited line.
- Sizes are the bytes on the wire unless "sizeof" is written.
- "Frame header", "control header" and "data header" are the 12-byte SDPCM header, the 16-byte CDC header and the 4-byte BDC header.

## Framing

| what it is | embassy | c-driver (hand-built layout name) | linux | whd | same layout? | citations |
|---|---|---|---|---|---|---|
| Frame header (SDPCM header) on the WLAN function, 12 bytes: length, inverted length, sequence, channel and flags, next length, header length, flow control, credit, 2 reserved | `SdpcmHeader` | `sdpcm_header_t` | no struct: hardware header (4) + software header (8), accessed with mask macros | `sdpcm_header_t` = `frametag[2]` + `sdpcm_sw_header_t` | yes | `embassy/structs.rs:75` `c-driver/cyw43_ll.c:754` `linux/brcmfmac/sdio.c:1311` `linux/brcmfmac/sdio.c:1321` `whd/src/whd_sdpcm.c:85` `whd/src/whd_sdpcm.c:99` |
| Frame tag, 4 bytes: length and its inverse (first 4 bytes of the row above) | `SDIO frame tag (hand-built)` | `size`, `size_com` members of `sdpcm_header_t` | hardware header | `frametag[2]` member of `sdpcm_header_t` | yes | `embassy/runner.rs:1062` `c-driver/cyw43_ll.c:754` `linux/brcmfmac/sdio.c:1311` `whd/src/whd_sdpcm.c:101` |
| Control header (CDC header), 16 bytes: cmd, len, flags, status | `CdcHeader` | `ioctl_header_t` | `brcmf_proto_bcdc_dcmd` | `cdc_header_t` | yes. embassy splits the 32-bit flags word into `flags` u16 at 8 and `id` u16 at 10; the other three declare one u32 at 8 | `embassy/structs.rs:133` `c-driver/cyw43_ll.c:851` `linux/brcmfmac/bcdc.c:25` `whd/src/include/whd_cdc_bdc.h:72` |
| Data and event header (BDC header), 4 bytes: flags, priority, flags2, data_offset | `BdcHeader` | `sdpcm_bdc_header_t` | `brcmf_proto_bcdc_header` | `bdc_header_t` | yes | `embassy/structs.rs:182` `c-driver/cyw43_ll.c:920` `linux/brcmfmac/bcdc.c:71` `whd/src/include/whd_cdc_bdc.h:80` |
| Transmitted control frame: frame header (12), control header (16), payload | `ioctl frame (hand-built)` | `tx_control_frame (hand-built)` | no struct: frame header then `brcmf_proto_bcdc_dcmd` | `control_header_t` | yes on the wire. whd's struct starts with a host-only `whd_buffer_header_t` (host queue pointer + 4 bus bytes for SDIO and SPI; 8 bytes with a 4-byte pointer) in front of the 12-byte frame header | `embassy/runner.rs:1463` `c-driver/cyw43_ll.c:893` `linux/brcmfmac/sdio.c:1321` `linux/brcmfmac/bcdc.c:25` `whd/src/include/whd_sdpcm.h:82` `whd/src/include/whd_sdpcm.h:75` `whd/src/include/whd_types_int.h:197` `whd/inc/whd_types.h:200` |
| Transmitted data frame: frame header (12), 2 pad bytes, data header (4), Ethernet frame | `tx data frame (hand-built)` | `tx_data_frame (hand-built)` | no struct: the data header is pushed in front of the Ethernet frame, then the bus code puts the frame header and `head_pad` alignment bytes in front of it | `data_header_t` | yes for embassy, c-driver, whd: all three put 2 pad bytes between the frame header and the data header. linux differs: the pad is the buffer address modulo `head_align`, not a fixed 2, the frame header grows by `SDPCM_HWEXT_LEN` when transmit glomming is on, and the data-offset field is set to pad + header length. whd's struct has the same 8-byte host prefix as the row above | `embassy/runner.rs:892` `c-driver/cyw43_ll.c:928` `linux/brcmfmac/bcdc.c:256` `linux/brcmfmac/sdio.c:2094` `linux/brcmfmac/sdio.c:2216` `linux/brcmfmac/sdio.c:2232` `linux/brcmfmac/sdio.c:3574-3585` `whd/src/include/whd_sdpcm.h:88` |
| Received frame: frame header, then the body at `header_length`; data and event bodies start with the data header and skip 4 × `data_offset` bytes after it | `rx frame (hand-parsed)` | `rx_frame, control and data channels (hand-parsed)` | no struct: `brcmf_sdio_hdparse` reads the frame header and the body offset (`dat_offset`); `brcmf_proto_bcdc_hdrpull` removes the data header and `data_offset << 2` bytes | no struct: `whd_sdpcm_process_rx_packet` reads the frame header through `sdpcm_header_t` and removes `header_length` bytes; the payload of a data frame starts 4 + (`data_offset << 2`) bytes after that | yes | `embassy/runner.rs:1151` `c-driver/cyw43_ll.c:962` `linux/brcmfmac/sdio.c:1371` `linux/brcmfmac/sdio.c:1439` `linux/brcmfmac/bcdc.c:281-323` `whd/src/whd_sdpcm.c:334` `whd/src/whd_sdpcm.c:436-438` `whd/src/whd_cdc_bdc.c:714-715` |
| Ethernet header, 14 bytes: destination, source, ether type | `EthernetHeader` | no struct: only bytes 12-13 are checked | `struct ethhdr` (kernel type, definition not in these sources), member `eth` of `brcmf_event` | `whd_event_ether_header_t`, `ethernet_header_t`, `wl_ether_header` | yes | `embassy/structs.rs:214` `c-driver/cyw43_ll.c:1065` `linux/brcmfmac/fweh.h:245` `whd/src/include/whd_events_int.h:476` `whd/src/include/whd_cdc_bdc.h:89` `whd/src/include/whd_wlioctl.h:54` |
| Vendor event header, 10 bytes: subtype, length, version, oui[3], user subtype | `EventHeader` | no struct: `rx_async_event_frame_prefix (hand-parsed)` checks the 3 OUI bytes at payload offset 19 | `brcm_ethhdr` | `whd_event_eth_hdr_t`, `sdpcm_bcmeth_header_t` | yes | `embassy/structs.rs:230` `c-driver/cyw43_ll.c:1050` `linux/brcmfmac/fweh.h:215` `whd/src/include/whd_events_int.h:467` `whd/src/whd_sdpcm.c:105` |
| Event message, 48 bytes: version, flags, event_type, status, reason, auth_type, datalen, addr[6], ifname[16], ifidx, bsscfgidx | `EventMessage` | `cyw43_async_event_t` | `brcmf_event_msg_be` | `whd_event_header_t` (`struct whd_event_msg`) | yes for bytes 0-47. c-driver names only `flags`, `event_type`, `status`, `reason` and `interface` (offset 46), declares the rest as filler `_0`, `_1[30]`, `_2`, and continues the same struct with a union of event data at 48 (156 bytes as declared) | `embassy/structs.rs:249` `c-driver/cyw43_ll.h:237` `linux/brcmfmac/fweh.h:223` `whd/src/include/whd_events_int.h:483` |
| Event packet: Ethernet header (14), vendor event header (10), event message (48), event data | `EventPacket` | `rx_async_event_frame_prefix (hand-parsed)`: event message taken at payload offset 24 | `brcmf_event` | `whd_event_t` | yes | `embassy/structs.rs:328` `c-driver/cyw43_ll.c:1050` `linux/brcmfmac/fweh.h:244` `whd/src/include/whd_events_int.h:499` |
| Word written to the last 4 bytes of chip RAM after the NVRAM: low 16 bits NVRAM length in 4-byte words, high 16 bits its inverse | `NVRAM length word (hand-built)` | `NVRAM length word (hand-built)` | no struct | no struct | yes. linux and whd's M2M path mask the low half (the word count) to 16 bits; embassy, c-driver and whd's SDIO and SPI paths leave it unmasked (c-driver masks only the inverted half before shifting it up); the results are equal while the word count fits in 16 bits | `embassy/runner.rs:568` `c-driver/cyw43_ll.c:1801` `linux/brcmfmac/firmware.c:447` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:2156` `whd/src/bus_protocols/whd_bus_spi_protocol.c:1283` `whd/src/bus_protocols/whd_bus_m2m_protocol.c:704` |

## Named variables and control values

| what it is | embassy | c-driver (hand-built layout name) | linux | whd | same layout? | citations |
|---|---|---|---|---|---|---|
| Set-variable request payload: name, NUL, value | `iovar set request (hand-built)` | `iovar_set_n / iovar_get (hand-built, generic)`, `iovar_set_u32 (hand-built)` | no struct: `brcmf_create_iovar` | no struct: `whd_cdc_get_iovar_buffer` | yes as sent. whd's buffer helper zero-fills `(64 - name_length) % 4` bytes in front of the name (name_length counts the NUL); whd's send routine skips leading zero bytes of a variable request and moves the rest forward before it fills the control header, so the frame starts with the name | `embassy/control.rs:717` `c-driver/cyw43_ll.c:1556` `c-driver/cyw43_ll.c:1538` `linux/brcmfmac/fwil.c:167` `whd/src/whd_cdc_bdc.c:349` `whd/src/whd_cdc_bdc.c:354-366` `whd/src/whd_cdc_bdc.c:212-229` |
| Get-variable request payload: name, NUL, zero fill; the reply value starts at offset 0 | `iovar get request (hand-built)` | `iovar_set_n / iovar_get (hand-built, generic)` | no struct: `brcmf_fil_iovar_data_get` | — | yes for embassy, c-driver, linux | `embassy/control.rs:731` `c-driver/cyw43_ll.c:1556` `c-driver/cyw43_ll.c:1969` `linux/brcmfmac/fwil.c:226` |
| Value of a `bsscfg:` variable taking two u32 (first is the bsscfg index) | `bsscfg u32 pair value (hand-built)` | `iovar_set_u32_u32 (hand-built)` | no struct: `brcmf_create_bsscfg` | no struct: `data[0]` = bsscfg index | yes for embassy and c-driver (two le32). linux writes the `bsscfg:` prefix and the index only when the index is non-zero; for index 0 it sends the plain name with no index | `embassy/control.rs:695` `c-driver/cyw43_ll.c:1546` `linux/brcmfmac/fwil.c:259` `linux/brcmfmac/fwil.c:262` `whd/src/whd_events.c:298` |
| `bss` value, 8 bytes: bsscfg index u32, enable u32 | `bsscfg u32 pair value (hand-built)` | `iovar_set_u32_u32 (hand-built)` | `brcmf_fil_bss_enable_le` | no struct: `data[0]` = bsscfg index, `data[1]` = up/down | yes | `embassy/control.rs:615` `embassy/control.rs:695` `c-driver/cyw43_ll.c:2457` `c-driver/cyw43_ll.c:1546` `linux/brcmfmac/fwil_types.h:244` `linux/brcmfmac/cfg80211.c:5479-5482` `whd/src/whd_ap.c:571-575` |
| `clmload` chunk header, 12 bytes: flag, dload_type, len, crc; chunk data follows | `DownloadHeader` (inside `clmload request (hand-built)`) | `clmload chunk (hand-built)` | `brcmf_dload_data_le` | `wl_dload_data_t` | header: yes. differs: sent length rounding. See "clmload chunk" | `embassy/structs.rs:370` `embassy/control.rs:250` `c-driver/cyw43_ll.c:1512-1515` `linux/brcmfmac/fwil_types.h:1106` `whd/src/include/whd_wlioctl.h:4167` |
| `country` value, 12 bytes: country_abbrev[4], rev, ccode[4] | `CountryInfo` | `country iovar value (hand-built)` | `brcmf_fil_country_le` | `wl_country_t` | yes | `embassy/structs.rs:390` `c-driver/cyw43_ll.c:2014` `linux/brcmfmac/fwil_types.h:764` `whd/src/include/whd_wlioctl.h:668` |
| SSID with 32-bit length, 36 bytes (command 26 and embedded in other records) | `SsidInfo` | `WLC_SET_SSID value (hand-built)` | `brcmf_ssid_le` | `wlc_ssid_t` | yes | `embassy/structs.rs:400` `c-driver/cyw43_ll.c:2296` `linux/brcmfmac/fwil_types.h:357` `whd/src/include/whd_wlioctl.h:496` |
| SSID with 8-bit length, 33 bytes | — | — | `brcmf_ssid8_le` | `ssid_info_t` (no use site in whd); `whd_ssid_t` (host-side API type, not sent as a block) | yes | `linux/brcmfmac/fwil_types.h:363` `whd/src/include/whd_wlioctl.h:479` `whd/inc/whd_types.h:584` |
| `bsscfg:ssid` value, 40 bytes: bsscfg index, SSID length, SSID[32] | `SsidInfoWithIndex` | `bsscfg:ssid value (hand-built)` | `brcmf_mbss_ssid_le` | no struct: built at the cited line | yes | `embassy/structs.rs:428` `c-driver/cyw43_ll.c:2382` `linux/brcmfmac/fwil_types.h:751` `whd/src/whd_ap.c:412` |
| Passphrase / PMK for command 268: key_len, flags, key | `PassphraseInfo` | `wsec_pmk (hand-built)` | `brcmf_wsec_pmk_le` | `wsec_pmk_t` | differs: key array length and sent size. See "Passphrase / PMK record" | `embassy/structs.rs:409` `c-driver/cyw43_ll.c:2252` `linux/brcmfmac/fwil_types.h:584` `whd/src/include/whd_wlioctl.h:786` |
| `sae_password` value, 130 bytes: length u16, password[128] | `SaePassphraseInfo` | `sae_password value (hand-built)` | `brcmf_wsec_sae_pwd_le` | `wsec_sae_password_t` | yes | `embassy/structs.rs:419` `c-driver/cyw43_ll.c:2262` `linux/brcmfmac/fwil_types.h:596` `whd/src/include/whd_wlioctl.h:794` |
| Event mask value: bit array, one bit per event number | `EventMask` | `bsscfg:event_msgs value (hand-built)` | no struct: `fweh->event_mask` | no struct: built at the cited line | differs: mask length, and linux sends no index. See "Event mask" | `embassy/structs.rs:437` `c-driver/cyw43_ll.c:2051` `linux/brcmfmac/fweh.c:356` `linux/brcmfmac/fweh.c:462` `whd/src/whd_events.c:290` |
| Extended event mask: ver, command, len, maxgetsize, mask bytes | — | — | `brcmf_eventmsgs_ext` | `eventmsgs_ext_t` | 4-byte header: yes. whd declares the tail as `mask[1]` (sizeof 5) and allocates sizeof + mask length + 4; linux declares a flexible tail (sizeof 4). whd sends it as `bsscfg:event_msgs_ext` with a u32 bsscfg index in front; linux sends it as `event_msgs_ext` with the struct as the whole value | `linux/brcmfmac/cyw/fwil_types.h:31` `linux/brcmfmac/cyw/core.c:79` `whd/src/include/whd_wlioctl.h:1056` `whd/src/whd_events.c:304` |
| `mkeep_alive` value, 11 bytes fixed: version, length, period_msec, len_bytes, keep_alive_id, data | `mkeep_alive packet (hand-built)` | — | `brcmf_mkeep_alive_pkt_le` | definition not found; only a reference to `wl_mkeep_alive_pkt_t` in a macro | yes for embassy and linux. The values differ: embassy writes 11 to `length`, linux leaves it 0 | `embassy/control.rs:686` `linux/brcmfmac/fwil_types.h:1230` `linux/brcmfmac/cfg80211.c:4298` `whd/src/include/whd_wlioctl.h:3299` |
| `mcast_list` value: count u32, then 6-byte addresses | `mcast_list value (hand-built)` | `mcast_list value (hand-built)` | no struct: built at the cited lines | `mcast_list_t` | yes. Sent length differs: embassy and c-driver send every slot of their fixed table (c-driver 4 + 10 × 6 = 64); linux sends 4 + 6 × count | `embassy/runner.rs:1393` `c-driver/cyw43_ll.c:2085` `linux/brcmfmac/core.c:160` `whd/src/whd_wifi_api.c:129` |
| `cur_etheraddr` value, 6 bytes | read with `iovar get request (hand-built)`, 6 bytes | `cur_etheraddr value (hand-built)` | — | — | yes for embassy and c-driver | `embassy/control.rs:848` `c-driver/cyw43_ll.c:2072` |

## Scan

| what it is | embassy | c-driver (hand-built layout name) | linux | whd | same layout? | citations |
|---|---|---|---|---|---|---|
| `escan` value: version, action, sync_id, then scan parameters (SSID, bssid, bss_type, scan_type, nprobes, active_time, passive_time, home_time, channel_num, channel list) | `ScanParams` | `cyw43_wifi_scan_options_t` | `brcmf_escan_params_le` holding `brcmf_scan_params_le` or `brcmf_scan_params_v2_le` | `wl_escan_params_t` holding `wl_scan_params_t` | differs: linux has a second parameter layout (v2); sent lengths differ. See "Escan parameters" | `embassy/structs.rs:454` `c-driver/cyw43_ll.h:255` `linux/brcmfmac/fwil_types.h:460` `linux/brcmfmac/fwil_types.h:368` `linux/brcmfmac/fwil_types.h:409` `whd/src/include/whd_wlioctl.h:548` `whd/src/include/whd_wlioctl.h:506` |
| Escan result header, 12 bytes: buflen, version, sync_id u16, bss_count u16; one BSS record follows | `ScanResults` | `_scan_result_t (escan result wrapper, function-local struct)` | `brcmf_escan_result_le` | `wl_escan_result_t` | yes | `embassy/structs.rs:476` `c-driver/cyw43_ll.c:669` `linux/brcmfmac/fwil_types.h:470` `whd/src/include/whd_wlioctl.h:556` |
| Scan result list header, 12 bytes: buflen, version, count u32; BSS records follow | — | — | `brcmf_scan_results` (used by linux only as a host-side buffer) | `wl_scan_results_t` (no use site in whd) | yes | `linux/brcmfmac/fwil_types.h:453` `whd/src/include/whd_wlioctl.h:534` |
| BSS record, 128 bytes fixed, information elements at `ie_offset` | `BssInfo` | `cyw43_scan_result_internal_t` | `brcmf_bss_info_le` | `wl_bss_info_t` | sizes and offsets: yes. differs: naming of bytes 97-99. See "BSS record" | `embassy/structs.rs:507` `c-driver/cyw43_ll.c:486` `linux/brcmfmac/fwil_types.h:314` `whd/inc/whd_types.h:926` |
| Rate set, 20 bytes: count u32, rates[16] (also bytes 52-71 of the BSS record) | fields `rateset_count`, `rates` of `BssInfo` | fields `rateset_count`, `rateset_rates` of `cyw43_scan_result_internal_t` | `brcm_rateset_le` | `wl_rateset_t` | yes | `embassy/structs.rs:507` `c-driver/cyw43_ll.c:486` `linux/brcmfmac/fwil_types.h:350` `whd/src/include/whd_wlioctl.h:573` |
| Information element header, 2 bytes: id, length | — | `auth IE offsets (RSN / WPA vendor IE, hand-parsed)`, bytes 0-1 | `brcmf_tlv` | `whd_tlv8_header_t`, `whd_tlv8_data_t` | yes | `c-driver/cyw43_ll.c:575` `linux/brcmfmac/cfg80211.h:413` `whd/src/include/whd_chip.h:157` `whd/src/include/whd_chip.h:163` |
| Vendor-specific information element header, 6 bytes: id, length, OUI[3], type | — | `auth IE offsets (RSN / WPA vendor IE, hand-parsed)`, bytes 0-5 | `brcmf_vs_tlv` | `vendor_specific_ie_header_t` | yes. whd declares bytes 2-5 as one `oui[4]`; linux as `oui[3]` + `oui_type` | `c-driver/cyw43_ll.c:575` `linux/brcmfmac/cfg80211.c:253` `whd/src/include/whd_chip.h:198` |
| List of u32 with a u32 count in front (channel and chanspec lists) | — | — | `brcmf_chanspec_list` | `wl_uint32_list_t`, `whd_list_t` | yes | `linux/brcmfmac/fwil_types.h:708` `whd/src/include/whd_wlioctl.h:613` `whd/inc/whd_types.h:575` |
| Channel information, 12 bytes: hw_channel, target_channel, scan_channel | — | — | `brcmf_channel_info_le`, `brcmf_fil_chan_info_le` (two identical definitions, no use site in linux) | `channel_info_t` | yes | `linux/brcmfmac/fwil_types.h:608` `linux/brcmfmac/fwil_types.h:223` `whd/src/include/whd_wlioctl.h:978` |

## Join, keys, stations

| what it is | embassy | c-driver (hand-built layout name) | linux | whd | same layout? | citations |
|---|---|---|---|---|---|---|
| `join` variable value: SSID (36), join scan parameters (20), association parameters | — (embassy joins with command 26 and `SsidInfo`) | `join iovar value (hand-built)` | `brcmf_ext_join_params_le` | `wl_extjoin_params_t` | differs: bytes 62-63 and sent length. See "Association parameters and the records that embed them" | `embassy/control.rs:438` `c-driver/cyw43_ll.c:2299` `linux/brcmfmac/fwil_types.h:530` `whd/src/include/whd_wlioctl.h:4259` |
| Join scan parameters, 20 bytes: scan_type u8, 3 pad, nprobes, active_time, passive_time, home_time | — | bytes 36-55 of `join iovar value (hand-built)` | `brcmf_join_scan_params_le` | `wl_join_scan_params_t` | yes | `c-driver/cyw43_ll.c:2299` `linux/brcmfmac/fwil_types.h:515` `whd/src/include/whd_wlioctl.h:619` |
| Association parameters: bssid[6], 2 bytes, chanspec_num u32, chanspec list | — | bytes 56-69 of `join iovar value (hand-built)` | `brcmf_assoc_params_le` | `wl_assoc_params_t` | differs: bytes 6-7 and sizeof. See "Association parameters and the records that embed them" | `c-driver/cyw43_ll.c:2299` `linux/brcmfmac/fwil_types.h:482` `whd/src/include/whd_wlioctl.h:4239` |
| Command 26 value with association parameters: SSID (36) then association parameters | — | — | `brcmf_join_params` | `wl_join_params_t` | differs: sizeof 52 (linux) against 50 (whd). Same section | `linux/brcmfmac/fwil_types.h:509` `whd/src/include/whd_wlioctl.h:4251` |
| Key record, 164 bytes: index, len, data[32], algo at 112, flags at 116, iv_initialized at 132, rxiv at 140, ea[6] at 156 | — | — | `brcmf_wsec_key_le` | `wl_wsec_key_t` (no use site in whd) | yes. The reserved runs are declared differently: linux `pad_2[3]` (12 bytes at 120), whd `pad_2` (8 at 120) + `pad_3` (4 at 128); every named field has the same offset. The linux size rests on `WLAN_MAX_KEY_LEN` = 32 | `linux/brcmfmac/fwil_types.h:558` `linux-headers/ieee80211.h:2267` `whd/src/include/whd_wlioctl.h:760` |
| Station value, 12 bytes: u32 value, ea[6], 2 pad | — | — | `brcmf_scb_val_le` | `scb_val_t`; `client_rssi_t` (same two fields under `#pragma pack(1)`, so 10 bytes with no pad; sent in a 12-byte buffer with command 127) | yes for bytes 0-9 | `linux/brcmfmac/fwil_types.h:602` `whd/src/include/whd_wlioctl.h:936` `whd/src/whd_wifi_api.c:135` `whd/src/whd_wifi_api.c:127` `whd/src/whd_wifi_api.c:1317-1320` |
| Station information (`sta_info`) | — | — | `brcmf_sta_info_le` | `sta_info_t` (no use site in whd) | differs: 296 bytes (linux) against 76 (whd). See "Station information" | `linux/brcmfmac/fwil_types.h:614` `whd/src/include/whd_wlioctl.h:942` |
| Associated-station list (command 159): count u32, then 6-byte addresses | — | `WLC_GET_ASSOCLIST value (hand-built)` | `brcmf_assoclist_le` | `whd_maclist_t`; `struct mac_list` (same fields, no use site) | field layout: yes. differs: buffer size. See "Associated-station list" | `c-driver/cyw43_ll.c:2489` `linux/brcmfmac/fwil_types.h:842` `whd/inc/whd_types.h:1141` `whd/src/include/whd_wlioctl.h:984` |
| PMKID entry, 22 bytes: bssid[6], pmkid[16] | — | — | `brcmf_pmksa` | `pmkid_t` | yes | `linux/brcmfmac/fwil_types.h:893` `whd/inc/whd_types.h:1152` |
| PMKID list (`pmkid_info`): count u32, then 22-byte entries | — | — | `brcmf_pmk_list_le` (16 entries declared, 356 bytes) | `pmkid_list_t` (1 entry declared; whd sizes the buffer as 4 + 16 × 22) | yes | `linux/brcmfmac/fwil_types.h:949` `whd/inc/whd_types.h:1158` `whd/src/whd_wifi_api.c:1203` `whd/src/include/whd_wlioctl.h:851` |
| Authentication request status, 60 bytes: flags u16, peer_mac[6], ssid_len u32, ssid[32], pmkid[16] | — | — | `brcmf_auth_req_status_le` | `whd_auth_req_status_t` | yes | `linux/brcmfmac/cyw/fwil_types.h:53` `whd/inc/whd_types.h:1168` |
| Management frame transmit parameters, 32 bytes fixed: version, dwell_time, len u16, frame control u16, channel u16, da[6], bssid[6], 2 pad, packet id u32, data | — | — | `brcmf_mf_params_le` | `whd_auth_params_t` | yes for the 32 fixed bytes. linux declares a flexible tail (sizeof 32); whd declares `data[1]` (sizeof 36) | `linux/brcmfmac/cyw/fwil_types.h:74` `whd/inc/whd_types.h:1195` |
| EDCF access-category parameter, 4 bytes: ACI, ECW, TXOP u16 | — | — | `brcmf_cfg80211_edcf_acparam` | `edcf_acparam_t` | yes | `linux/brcmfmac/cfg80211.h:279` `whd/src/include/whd_wlioctl.h:3909` |
| Revision information (command 98) | — | — | `brcmf_rev_info_le` | `wlc_rev_info_t` (no use site in whd) | differs: 68 bytes (linux) against 60 (whd). See "Revision information" | `linux/brcmfmac/fwil_types.h:791` `whd/src/include/whd_wlioctl.h:1006` |
| Packet counters, 20 bytes: rx_good_pkt, rx_bad_pkt, tx_good_pkt, tx_bad_pkt, rx_ocast_good_pkt | — | — | `brcmf_pktcnt_le` | `get_pktcnt_t` | yes | `linux/brcmfmac/fwil_types.h:1134` `whd/src/include/whd_wlioctl.h:989` |
| `rssi_event` value, 16 bytes: rate_limit_msec u32, level count u8, levels[8], 3 pad | — | — | `brcmf_rssi_event_le` | `wl_rssi_event_t` (no use site in whd) | yes | `linux/brcmfmac/fwil_types.h:869` `whd/src/include/whd_wlioctl.h:3849` |
| Interface event data, 5 bytes: ifidx, action, flags, bsscfgidx, role | — | — | `brcmf_if_event` | `wl_vif_event_t` | yes | `linux/brcmfmac/fweh.h:279` `whd/src/include/whd_wlioctl.h:4605` |

## Offloads, action frames, P2P

| what it is | embassy | c-driver (hand-built layout name) | linux | whd | same layout? | citations |
|---|---|---|---|---|---|---|
| Packet filter pattern, 8 bytes fixed: offset, size_bytes, then mask and pattern | — | — | `brcmf_pkt_filter_pattern_le` | `wl_pkt_filter_pattern_t` | yes | `linux/brcmfmac/fwil_types.h:279` `whd/src/include/whd_wlioctl.h:3636` |
| Packet filter, 20 bytes fixed: id, type, negate_match, pattern union | — | — | `brcmf_pkt_filter_le` | `wl_pkt_filter_t` | yes | `linux/brcmfmac/fwil_types.h:295` `whd/src/include/whd_wlioctl.h:3642` |
| Packet filter enable, 8 bytes: id, enable | — | — | `brcmf_pkt_filter_enable_le` | `wl_pkt_filter_enable_t` | yes | `linux/brcmfmac/fwil_types.h:305` `whd/src/include/whd_wlioctl.h:3654` |
| `wowl_pattern` value: operation string, masksize, offset, patternoffset, patternsize, id, reasonsize, type, mask, pattern | — | — | `brcmf_fil_wowl_pattern_le` | `wl_wowl_pattern_t` | differs: the 4 operation bytes are inside the linux struct and outside the whd struct. See "Wake pattern" | `linux/brcmfmac/fwil_types.h:738` `whd/src/include/whd_wlioctl.h:3770` |
| `wowl_wakeind` value | — | — | `brcmf_wowl_wakeind_le` | `wl_wowl_wakeind_t` (no use site in whd) | differs: 8 bytes (linux) against 4 (whd). See "Wake indication" | `linux/brcmfmac/fwil_types.h:882` `whd/src/include/whd_wlioctl.h:3789` |
| Preferred-network scan parameters (`pfn_set`), 24 bytes | — | — | `brcmf_pno_param_le` | `wl_pfn_param_t` (no use site in whd) | yes | `linux/brcmfmac/fwil_types.h:999` `whd/src/include/whd_wlioctl.h:3522` |
| Preferred-network channel configuration, 140 bytes: reporttype, channel_num, channel_list (128 bytes), flags | — | — | `brcmf_pno_config_le` | `wl_pfn_cfg_t` | yes | `linux/brcmfmac/fwil_types.h:1020` `whd/src/include/whd_wlioctl.h:3553` |
| Preferred network, 56 bytes: SSID (36), flags, infra, auth, wpa_auth, wsec | — | — | `brcmf_pno_net_param_le` | `wl_pfn_t` | yes | `linux/brcmfmac/fwil_types.h:1037` `whd/src/include/whd_wlioctl.h:3565` |
| Preferred-network found entry, 44 bytes: bssid[6], channel, SSID_len, SSID[32], RSSI u16, timestamp u16 | — | — | `brcmf_pno_net_info_le` | `wl_pfn_net_info_t` holding `wl_pfn_subnet_info_t` | yes. whd nests the first 40 bytes as a sub-struct | `linux/brcmfmac/fwil_types.h:1056` `whd/src/include/whd_wlioctl.h:3503` `whd/src/include/whd_wlioctl.h:3495` |
| Preferred-network scan result: version, status, count, then entries | — | — | `brcmf_pno_scanresults_le`, `brcmf_pno_scanresults_v2_le` | `wl_pfn_scanresult_t` (no use site in whd) | first 12 bytes: yes. differs after that. See "Preferred-network scan result" | `linux/brcmfmac/fwil_types.h:1072` `linux/brcmfmac/fwil_types.h:1078` `whd/src/include/whd_wlioctl.h:3512` |
| Preferred-network BSSID entry, 8 bytes: address[6], flags u16 | — | — | `brcmf_pno_bssid_le` | `wl_pfn_bssid_t` | yes | `linux/brcmfmac/fwil_types.h:1120` `whd/src/include/whd_wlioctl.h:3546` |
| Action frame: da[6], len u16, packet id u32, data | — | — | `brcmf_fil_action_frame_le` | `wl_action_frame_t` | differs: data array 1800 bytes (linux) against 1040 (whd). See "Action frame" | `linux/brcmfmac/fwil_types.h:229` `whd/src/include/whd_wlioctl.h:60` |
| Action frame parameters: channel, dwell_time, bssid[6], 2 pad, action frame | — | — | `brcmf_fil_af_params_le` | `wl_af_params_t`, alias `whd_af_params_t` | first 16 bytes: yes. differs in total size through the embedded action frame. Same section | `linux/brcmfmac/fwil_types.h:236` `whd/src/include/whd_wlioctl.h:68` `whd/inc/whd_types.h:142` |
| Received management frame prefix, 16 bytes: version u16, u16 at 2, rssi, mactime, rate | — | — | `brcmf_rx_mgmt_data` | `wl_rx_mgmt_data_t` | yes. linux names bytes 2-3 `chanspec`, whd `channel` | `linux/brcmfmac/fwil_types.h:718` `whd/src/include/whd_wlioctl.h:76` |
| P2P interface request, 10 bytes: address[6], type, chanspec u16 | — | — | `brcmf_fil_p2p_if_le` | `wl_p2p_if_t` (no use site in whd) | differs: width of the type field. See "P2P interface request" | `linux/brcmfmac/fwil_types.h:217` `whd/src/include/whd_wlioctl.h:3947` |
| P2P discovery state, 6 bytes: state u8, 1 pad, chanspec u16, dwell u16 | — | — | `brcmf_p2p_disc_st_le` | `wl_p2p_disc_st_t` (no use site in whd) | yes | `linux/brcmfmac/p2p.c:105` `whd/src/include/whd_wlioctl.h:3921` |
| `p2p_scan` value: type u8, 3 reserved, escan parameters at 4 | — | — | `brcmf_p2p_scan_le` | `wl_p2p_scan_t` (first 4 bytes), `wl_p2p_escan_t` (whole record) | yes through the channel list at 76. sizeof differs (linux 88, whd 80) because the linux union also holds the v2 scan parameters | `linux/brcmfmac/p2p.c:132` `whd/src/include/whd_wlioctl.h:3929` `whd/src/include/whd_wlioctl.h:3937` |

## Chip RAM records and Bluetooth

| what it is | embassy | c-driver (hand-built layout name) | linux | whd | same layout? | citations |
|---|---|---|---|---|---|---|
| Shared record in chip RAM, found through the last word of RAM: flags, trap_addr, assert_exp_addr, assert_file_addr, assert_line, console_addr, msgtrace_addr, more | `SharedMemData` | — | `sdpcm_shared_le` | `wlan_shared_t` | first 28 bytes: yes. differs from offset 28 and in size. See "Shared record in chip RAM" | `embassy/structs.rs:49` `linux/brcmfmac/sdio.c:377` `whd/src/include/whd_chip.h:320` |
| Console log descriptor in chip RAM: buf, buf_size, idx, fourth word | `SharedMemLog` | — | `rte_log_le` | `hnd_log_t` | first 12 bytes: yes. differs: fourth member. See "Console log descriptor and console record" | `embassy/structs.rs:64` `linux/brcmfmac/sdio.c:71` `whd/src/include/whd_chip.h:274` |
| Console record in chip RAM: vcons_in, vcons_out, log descriptor at 8, cbuf_idx, cbuf[128] | no struct: reads the log descriptor at console_addr + 8 | — | `rte_console` | `hnd_cons_t` | first 20 bytes: yes. differs after that. Same section | `embassy/runner.rs:729` `linux/brcmfmac/sdio.c:78` `whd/src/include/whd_chip.h:284` |
| Bluetooth ring record header: 3-byte length, 1-byte HCI packet type, payload padded to a multiple of 4 | `BT HCI ring record header (hand-built)` | — | — | — | yes against pico-sdk, which describes and decodes the same 4 bytes at the cited lines | `embassy/bluetooth.rs:413` `pico-sdk/cybt_shared_bus.c:340` `pico-sdk/cybt_shared_bus.c:378` |
| Bluetooth shared buffer region: two 4096-byte buffers, then four 4-byte ring pointers | `BT shared buffer region (constants)` | — | — | — | yes against pico-sdk (same offsets) | `embassy/consts.rs:202` `pico-sdk/cybt_shared_bus_driver.c:37` `pico-sdk/cybt_shared_bus_driver.c:87` `pico-sdk/cybt_shared_bus_driver.h:10` |
| Bluetooth patch file record (file format parsed by the host): num_bytes, 2-byte address, type, data | `BT patch record (hand-parsed)` | — | — | — | yes against pico-sdk's binary parser | `embassy/bluetooth.rs:170` `pico-sdk/cybt_shared_bus_driver.c:240` |

## Where the layouts differ

### clmload chunk

- The 12-byte header (flag u16, dload_type u16, len u32, crc u32) is the same in all four. `embassy/structs.rs:370` `c-driver/cyw43_ll.c:1512-1515` `linux/brcmfmac/fwil_types.h:1106` `whd/src/include/whd_wlioctl.h:4167`
- embassy sends name (8) + header (12) + chunk, exact length. `embassy/control.rs:250-254`
- linux sends 12 + len for the value, exact length. `linux/brcmfmac/common.c:114-115`
- c-driver rounds 20 + len up to a multiple of 8; the pad bytes are whatever was in the buffer. `c-driver/cyw43_ll.c:1521-1522`
- whd writes the length it was passed minus 12 into the header's len field, then, when built without PROTO_MSGBUF, replaces the length of the value (header + chunk) with `len + 8 - (len % 8)`, which adds 8 when it is already a multiple of 8, and copies that many bytes from the caller's buffer. `whd/src/whd_clm.c:53-56` `whd/src/whd_clm.c:61-67`
- whd declares the tail as `data[1]`, so its sizeof is 16; the other three have a 12-byte header. `whd/src/include/whd_wlioctl.h:4167`
- embassy and linux agree (exact length). c-driver and whd both pad toward 8 bytes but with different arithmetic. `embassy/control.rs:250-254` `linux/brcmfmac/common.c:114-115` `c-driver/cyw43_ll.c:1521-1522` `whd/src/whd_clm.c:61-67`

### Passphrase / PMK record

All four start with key_len u16 at 0, flags u16 at 2, key at 4. The key array length and the sent size differ. `embassy/structs.rs:409` `c-driver/cyw43_ll.c:2252` `linux/brcmfmac/fwil_types.h:584-588` `whd/src/include/whd_wlioctl.h:786-791`

| driver | key array | size sent | citations |
|---|---|---|---|
| embassy | 64 | 68 | `embassy/structs.rs:409` |
| c-driver | 64 | 68 (4 + `CYW43_WPA_MAX_PASSWORD_LEN`) | `c-driver/cyw43_ll.c:2252-2258` `c-driver/cyw43_ll.c:277` |
| whd | 65 (`WSEC_MAX_PSK_LEN` + 1) | 70 (sizeof, 1 tail pad byte) | `whd/src/include/whd_wlioctl.h:781` `whd/src/include/whd_wlioctl.h:786-791` `whd/src/whd_wifi_api.c:756-759` |
| linux | 128 (`BRCMF_WSEC_MAX_SAE_PASSWORD_LEN`) | 132 (sizeof) | `linux/brcmfmac/fwil_types.h:68` `linux/brcmfmac/fwil_types.h:584-588` `linux/brcmfmac/cfg80211.c:1710-1731` |

- embassy and c-driver agree. whd and linux each differ from every other driver. `embassy/structs.rs:409` `c-driver/cyw43_ll.c:2252-2258` `whd/src/include/whd_wlioctl.h:786-791` `linux/brcmfmac/fwil_types.h:584-588`
- In the c-driver station path the bytes after the copied key come from a stack buffer that is not cleared first. `c-driver/cyw43_ll.c:2210` `c-driver/cyw43_ll.c:2252-2254`

### Event mask

| driver | variable name sent | bsscfg index in front | mask bytes | citations |
|---|---|---|---|---|
| embassy | `bsscfg:event_msgs` | u32 | 24 | `embassy/structs.rs:437-440` `embassy/control.rs:305-319` |
| c-driver | `bsscfg:event_msgs` | 4 bytes, not written at the cited lines (meaning inferred) | 19 | `c-driver/cyw43_ll.c:2051-2060` |
| whd | `bsscfg:event_msgs` | u32 | 16 (`WL_EVENTING_MASK_LEN`) | `whd/src/whd_events.c:290-300` `whd/src/include/whd_wlioctl.h:1932` |
| linux | `event_msgs` | none | `DIV_ROUND_UP(num_event_codes, 8)` | `linux/brcmfmac/fweh.c:356` `linux/brcmfmac/fweh.c:462` |

- embassy, c-driver and whd agree on the shape (index then mask) and disagree on the mask length. linux differs in both name and shape; whd's start-up use has the linux shape. `embassy/structs.rs:437-440` `c-driver/cyw43_ll.c:2051-2060` `whd/src/whd_events.c:290-300` `linux/brcmfmac/fweh.c:462` `whd/src/whd_management.c:516-524`
- whd also sends plain `event_msgs` with 16 zero mask bytes and no index once during start-up. `whd/src/whd_management.c:516-524` `whd/src/include/whd_wlioctl.h:1074`
- whd switches to the extended mask record when an event number above 127 is registered. `whd/src/whd_events.c:274` `whd/src/whd_events.c:304-323`
- linux's cyw vendor code sends the extended mask record instead, through its activate-events hook; when the hook succeeds linux does not send `event_msgs`. `linux/brcmfmac/cyw/core.c:79-99` `linux/brcmfmac/fweh.c:459-460`

### Escan parameters

- embassy and c-driver declare one flat 76-byte struct: version at 0, action at 4, sync_id at 6, ssid_len at 8, ssid at 12, bssid at 44, bss_type at 50, scan_type at 51, nprobes at 52, active_time at 56, passive_time at 60, home_time at 64, channel_num at 68, one channel entry at 72, 2 tail pad bytes. `embassy/structs.rs:454` `c-driver/cyw43_ll.h:255`
- c-driver names the bytes at 6 `_`; embassy names them `sync_id`. `c-driver/cyw43_ll.h:255` `embassy/structs.rs:454`
- whd nests an 8-byte escan header and `wl_scan_params_t`; with the header in front the offsets are the same as the flat struct (channel list at 8 + 64 = 72). `whd/src/include/whd_wlioctl.h:548` `whd/src/include/whd_wlioctl.h:506`
- linux nests an 8-byte escan header and a union of two parameter layouts. `linux/brcmfmac/fwil_types.h:460`
- linux v1 parameters (`brcmf_scan_params_le`) have the same offsets as whd's `wl_scan_params_t`: 64 fixed bytes, channel list at 64. `linux/brcmfmac/fwil_types.h:368` `whd/src/include/whd_wlioctl.h:506`
- linux v2 parameters (`brcmf_scan_params_v2_le`) are a different layout: version u16 at 0, length u16 at 2, SSID at 4, bssid at 40, bss_type at 46, 1 pad, scan_type as u32 at 48, nprobes at 52, active_time at 56, passive_time at 60, home_time at 64, channel_num at 68, channel list at 72 (72 fixed bytes). `linux/brcmfmac/fwil_types.h:409`
- linux uses v2 only when feature SCAN_V2 is set, otherwise converts to v1 before sending. `linux/brcmfmac/cfg80211.c:1472-1491`
- No other driver in these sources has the v2 layout. `embassy/structs.rs:454` `c-driver/cyw43_ll.h:255` `whd/src/include/whd_wlioctl.h:506`

Sent length:

| driver | length of the value | citations |
|---|---|---|
| embassy | 76 (the struct) | `embassy/control.rs:804-835` |
| c-driver | 76 (sizeof) | `c-driver/cyw43_ll.c:2202` |
| whd | 8 + 64 + 2 × channels to start; sizeof (76) to abort | `whd/src/whd_wifi_api.c:3264` `whd/src/whd_wifi_api.c:3303` `whd/src/whd_wifi_api.c:3405-3416` |
| linux | 8 + 72 (64 for v1) + 4 × ((n_channels + 1) / 2) + 36 × n_ssids | `linux/brcmfmac/cfg80211.c:1447-1459` `linux/brcmfmac/cfg80211.c:1475-1476` |

- embassy and c-driver agree with each other; whd and linux each compute the length. `embassy/control.rs:804-835` `c-driver/cyw43_ll.c:2202` `whd/src/whd_wifi_api.c:3264` `linux/brcmfmac/cfg80211.c:1447-1459`

### BSS record

- All four have a 128-byte fixed part with ie_offset at 116, ie_length at 120, SNR at 124. `embassy/structs.rs:507` `c-driver/cyw43_ll.c:486` `linux/brcmfmac/fwil_types.h:314` `whd/inc/whd_types.h:926`
- Bytes 97-99 (after `flags` at 96): embassy and whd declare `vht_cap` (1 byte) then 2 reserved bytes. `embassy/structs.rs:548-551` `whd/inc/whd_types.h:954-956`
- Bytes 97-99: c-driver declares `pad5[3]`; linux declares `reserved[3]`. `c-driver/cyw43_ll.c:509-510` `linux/brcmfmac/fwil_types.h:339-340`
- On bytes 97-99 embassy and whd agree with each other, and c-driver and linux agree with each other. `embassy/structs.rs:548-551` `whd/inc/whd_types.h:954-956` `c-driver/cyw43_ll.c:509-510` `linux/brcmfmac/fwil_types.h:339-340`
- The 2 bytes between ie_offset and ie_length are an explicit member in embassy (`reserved6`) and c-driver (`pad6`), and compiler padding in linux and whd; the offsets are the same. `embassy/structs.rs:560` `c-driver/cyw43_ll.c:513` `linux/brcmfmac/fwil_types.h:343-344` `whd/inc/whd_types.h:959-960`

### Association parameters and the records that embed them

Association parameters:

| driver | bytes 0-5 | bytes 6-7 | bytes 8-11 | chanspec list | sizeof | citations |
|---|---|---|---|---|---|---|
| linux `brcmf_assoc_params_le` | bssid | compiler padding | chanspec_num | at 12, one entry declared | 16 (2 tail pad bytes) | `linux/brcmfmac/fwil_types.h:482-487` |
| whd `wl_assoc_params_t` | bssid | `bssid_cnt` u16 | chanspec_num | at 12, one entry declared | 14 (inside a pack(1) region) | `whd/src/include/whd_wlioctl.h:4239-4245` |
| c-driver, bytes 56-69 of the `join` value | bssid | zero (buffer cleared, never written) | chanspec_num | at 12, one entry | 14 bytes used | `c-driver/cyw43_ll.c:2300` `c-driver/cyw43_ll.c:2316-2320` |

- whd writes 0 to `bssid_cnt` in the `join` path. `whd/src/whd_wifi_api.c:2360`
- The offsets of bssid, chanspec_num and the chanspec list agree in all three; only whd names bytes 6-7. `linux/brcmfmac/fwil_types.h:482-487` `whd/src/include/whd_wlioctl.h:4239-4245` `c-driver/cyw43_ll.c:2316-2320`

`join` variable value (SSID 36, scan parameters 20, association parameters):

| driver | size sent | citations |
|---|---|---|
| c-driver | 70 always (4 + 32 + 20 + 14) | `c-driver/cyw43_ll.c:2325` |
| whd | 70 (sizeof `wl_extjoin_params_t`) | `whd/src/whd_wifi_api.c:2346` `whd/src/include/whd_wlioctl.h:4259` |
| linux | 68, or 70 when one chanspec is set; sizeof is 72 and its 2 tail pad bytes are not sent | `linux/brcmfmac/cfg80211.c:2569-2572` `linux/brcmfmac/fwil_types.h:530` |

- c-driver and whd agree on 70 bytes. linux sends 68 when no channel is given. `c-driver/cyw43_ll.c:2325` `whd/src/whd_wifi_api.c:2346` `linux/brcmfmac/cfg80211.c:2569-2572`

Command 26 value with association parameters:

- linux `brcmf_join_params`: sizeof 52 (36 + 16); the length passed is built at each use site (36, 52, or computed). `linux/brcmfmac/fwil_types.h:509` `linux/brcmfmac/cfg80211.c:2631-2647`
- whd `wl_join_params_t`: sizeof 50 (36 + 14); whd sends sizeof. `whd/src/include/whd_wlioctl.h:4251` `whd/src/whd_wifi_api.c:2369-2386`
- embassy and c-driver send only the 36-byte SSID record with command 26. `embassy/control.rs:438-442` `c-driver/cyw43_ll.c:2296`

### Station information

- linux `brcmf_sta_info_le`: 296 bytes. `linux/brcmfmac/fwil_types.h:614`
- whd `sta_info_t`: 76 bytes, ending with rx_rate at 72. `whd/src/include/whd_wlioctl.h:942-959`
- Bytes 0-75 have the same fields at the same offsets in both: ver, len, cap, flags at 8, idle, ea at 16, rate set (count + 16 rates) at 24, in at 44, listen_interval_inms, tx_pkts, tx_failures, rx_ucast_pkts, rx_mcast_pkts, tx_rate at 68, rx_rate at 72. `linux/brcmfmac/fwil_types.h:614` `whd/src/include/whd_wlioctl.h:942`
- linux continues from offset 76 with decrypt counters, totals, 64-bit byte counters at 96, rssi at 144, and a version-dependent union at 200. `linux/brcmfmac/fwil_types.h:614`
- whd has no use site for its record; linux requests it with `tdls_sta_info` then `sta_info`. `linux/brcmfmac/cfg80211.c:3205-3214`

### Revision information

- linux `brcmf_rev_info_le`: 68 bytes, 17 u32, ending with `chippkg` at 60 and `nvramrev` at 64. `linux/brcmfmac/fwil_types.h:791` `linux/brcmfmac/fwil_types.h:806-808`
- whd `wlc_rev_info_t`: 60 bytes, 15 u32, ending with `anarev` at 56. `whd/src/include/whd_wlioctl.h:1006` `whd/src/include/whd_wlioctl.h:1020-1023`
- The first 15 fields are the same in both, in the same order. `linux/brcmfmac/fwil_types.h:791` `whd/src/include/whd_wlioctl.h:1006`
- linux reads it with command 98 and sizeof. `linux/brcmfmac/common.c:307-308`
- No use site for the whd record was found in whd. `whd/src/include/whd_wlioctl.h:1006`

### Associated-station list

- c-driver requests 4 + maxassoc × 6 bytes. `c-driver/cyw43_ll.c:2489-2490`
- whd sizes the buffer as 4 + max_clients × 6. `whd/src/whd_wifi_api.c:3498` `whd/inc/whd_types.h:1141-1145`
- linux declares a fixed array of 128 addresses, 772 bytes, and uses that buffer. `linux/brcmfmac/fwil_types.h:842-845` `linux/brcmfmac/fwil_types.h:149` `linux/brcmfmac/cfg80211.c:3316-3318`
- c-driver and whd agree (caller-sized). The field layout is the same in all three. `c-driver/cyw43_ll.c:2489-2490` `whd/inc/whd_types.h:1141-1145` `linux/brcmfmac/fwil_types.h:842-845`

### Wake pattern

- linux `brcmf_fil_wowl_pattern_le`: `cmd[4]` at 0, then masksize at 4, offset at 8, patternoffset at 12, patternsize at 16, id at 20, reasonsize at 24, type at 28; 32 fixed bytes, then mask, then pattern. `linux/brcmfmac/fwil_types.h:738-742`
- whd `wl_wowl_pattern_t`: masksize at 0, offset at 4, patternoffset at 8, patternsize at 12, id at 16, reasonsize at 20, type at 24; 28 bytes. `whd/src/include/whd_wlioctl.h:3770`
- whd copies the operation string without its NUL to the start of the value, skips one more byte (not written at the cited lines), then places the struct, mask, pattern. `whd/src/whd_wifi_api.c:6672-6684`
- With a 3-character operation ("add", "clr") the whd string takes 4 bytes, so the field offsets line up with the linux struct (inferred). `linux/brcmfmac/fwil_types.h:738-742` `whd/src/whd_wifi_api.c:6681-6684`
- Both set patternoffset to 28 + masksize, counted from the start of the 28-byte part. `linux/brcmfmac/cfg80211.c:4058` `whd/src/whd_wifi_api.c:6701`

### Wake indication

- linux `brcmf_wowl_wakeind_le`: 8 bytes, `pci_wakeind` u32 at 0, `ucode_wakeind` u32 at 4. `linux/brcmfmac/fwil_types.h:882-885`
- whd `wl_wowl_wakeind_t`: 4 bytes, `pci_wakeind` u8 at 0, 1 pad, `ucode_wakeind` u16 at 2. `whd/src/include/whd_wlioctl.h:3789-3793`
- linux reads it with `wowl_wakeind`. `linux/brcmfmac/cfg80211.c:4146-4147`
- No use site for the whd record was found in whd. `whd/src/include/whd_wlioctl.h:3789`

### Preferred-network scan result

- linux `brcmf_pno_scanresults_le`: 12-byte header (version, status, count); count entries of `brcmf_pno_net_info_le` (44 bytes each) follow. `linux/brcmfmac/fwil_types.h:1072` `linux/brcmfmac/cfg80211.c:3937-3945`
- linux also declares a v2 header with a fourth u32, `scan_ch_bucket`, at 12 (16 bytes). `linux/brcmfmac/fwil_types.h:1078`
- whd `wl_pfn_scanresult_t`: the same 12 bytes, then exactly one 44-byte net info at 12, then a BSS record at 56 (184 bytes fixed). No use site was found in whd. `whd/src/include/whd_wlioctl.h:3512`

### Action frame

- linux `brcmf_fil_action_frame_le`: da[6], len u16 at 6, packet_id u32 at 8, data[1800] at 12; 1812 bytes. `linux/brcmfmac/fwil_types.h:229-233` `linux/brcmfmac/fwil_types.h:13`
- whd `wl_action_frame_t`: da[6], len u16 at 6, packetId u32 at 8, data[1040] at 12; 1052 bytes. `whd/src/include/whd_wlioctl.h:60-66` `whd/src/include/whd_wlioctl.h:38`
- The enclosing parameter record has the same first 16 bytes in both (channel, dwell_time, bssid, 2 pad) and embeds the action frame at 16: 1828 bytes in linux, 1068 in whd. `linux/brcmfmac/fwil_types.h:236` `whd/src/include/whd_wlioctl.h:68`

### P2P interface request

- linux `brcmf_fil_p2p_if_le`: addr[6], `type` as le16 at 6, `chspec` le16 at 8; 10 bytes. `linux/brcmfmac/fwil_types.h:217-221`
- whd `wl_p2p_if_t`: mac_address[6], `interface_type` as u8 at 6, 1 pad byte at 7, `chan_spec` u16 at 8; 10 bytes. `whd/src/include/whd_wlioctl.h:3947-3952`
- Same size and same offsets for address and chanspec; byte 7 is the high byte of the type in linux and padding in whd. `linux/brcmfmac/fwil_types.h:219` `whd/src/include/whd_wlioctl.h:3950`
- whd has no use site for its record; linux uses it with `p2p_ifadd` and `p2p_ifupd`. `linux/brcmfmac/p2p.c:2128-2141` `linux/brcmfmac/p2p.c:2074-2104`

### Shared record in chip RAM

| driver | size | bytes 0-27 | from offset 28 | citations |
|---|---|---|---|---|
| embassy `SharedMemData` | 32 | flags, trap_addr, assert_exp_addr, assert_file_addr, assert_line, console_addr, msgtrace_addr | `fwid` u32 | `embassy/structs.rs:49-57` |
| whd `wlan_shared_t` | 68 | same | `fwid` u32, then total_lfrag_pktcount, reserved, reserved1, h2d_mb_addr, d2h_mb_addr, ring_info_ptr, scratch_mem_size, scratch_mem_ptr_low, scratch_mem_ptr_high | `whd/src/include/whd_chip.h:320-339` |
| linux `sdpcm_shared_le` | 64 | same | `tag[32]`, then `brpt_addr` u32 at 60 | `linux/brcmfmac/sdio.c:377-387` |

- embassy and whd agree on bytes 0-31; whd's record is longer. linux disagrees with both from offset 28. `embassy/structs.rs:49-57` `whd/src/include/whd_chip.h:320-339` `linux/brcmfmac/sdio.c:377-387`
- embassy uses only console_addr. `embassy/runner.rs:729`
- whd byte-converts only the first seven words. `whd/src/whd_chip.c:506-512`
- linux reads this record only in DEBUG builds. `linux/brcmfmac/sdio.c:1021-1103`

### Console log descriptor and console record

Log descriptor:

- embassy `SharedMemLog` and whd `hnd_log_t`: 16 bytes, buf, buf_size, idx, `out_idx`. `embassy/structs.rs:64-69` `whd/src/include/whd_chip.h:274-280`
- linux `rte_log_le`: buf, buf_size, idx as three le32, then a host pointer `_buf_compat`; sizeof is 24 on a 64-bit host and 16 on a 32-bit host. `linux/brcmfmac/sdio.c:71-76`
- embassy and whd agree. linux agrees on the first 12 bytes; its fourth member is a host pointer, `_buf_compat`, where embassy and whd declare a fourth 32-bit word named `out_idx`. `embassy/structs.rs:64-69` `whd/src/include/whd_chip.h:274-280` `linux/brcmfmac/sdio.c:71-76`

Console record:

- whd `hnd_cons_t`: vcons_in at 0, vcons_out at 4, log descriptor at 8 (16 bytes), cbuf_idx at 24, cbuf[128] at 28; 156 bytes. `whd/src/include/whd_chip.h:284`
- linux `rte_console`: vcons_in at 0, vcons_out at 4, log descriptor at 8; cbuf_idx and cbuf follow at offsets that depend on the host pointer size (32 and 36 on a 64-bit host, 24 and 28 on a 32-bit host). `linux/brcmfmac/sdio.c:78`
- linux reads sizeof(log descriptor) bytes at offset 8 of the console record in one place, and single u32 at offsets 8, 12 and 16 in another; no read of cbuf_idx or cbuf was found at the cited lines. `linux/brcmfmac/sdio.c:2871-2873` `linux/brcmfmac/sdio.c:2992-3008`
- embassy reads the log descriptor at console_addr + 8 and has no struct for the console record. `embassy/runner.rs:729` `embassy/runner.rs:735-737`
- All three agree on the log descriptor position (offset 8). `embassy/runner.rs:729` `linux/brcmfmac/sdio.c:78` `whd/src/include/whd_chip.h:284`
