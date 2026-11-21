# Procedures

Step-by-step sequences each driver uses for ten operations: the commands, named variables (iovar) and events involved, what ends each sequence, and where the drivers differ. Payload values are as the driver sends them.

## Scan

### embassy

1. host-side event filter — enable ESCAN_RESULT (69) in the driver's own event mask — no bytes sent; this is embassy's local filter, the firmware mask was set to all-ones minus a few at init (bsscfg:event_msgs, `embassy/control.rs:305-319`). Note: event number: `embassy/events.rs:146` — `embassy/control.rs:828`
2. variable (set, command SetVar=263) — escan — ScanParams (`embassy/structs.rs:454-469`): version u32=1, action u16=1, sync_id u16=1, ssid_len u32 (0 when no SSID given), ssid[32] (zero when none), bssid[6] (ff:ff:ff:ff:ff:ff when none given), bss_type u8=2, scan_type u8 (0 active, 1 passive; passive is the ScanOptions default), nprobes u32, active_time u32, passive_time u32, home_time u32, channel_num u32=0, channel_list[1] u16=0. Note: active_time/passive_time: only the one matching scan_type carries dwell_time in ms, the other is 0xFFFFFFFF; with no dwell_time both are 0xFFFFFFFF (`embassy/control.rs:780-802`). home_time 0xFFFFFFFF unless given. nprobes: the option is a u16 and the default is written `unwrap_or(!0).into()` (`embassy/control.rs:820`) on an `Option<u16>` (`embassy/control.rs:83`), i.e. 0xFFFF widened to u32 = 0x0000FFFF, not 0xFFFFFFFF (inferred from the types). Sent on interface 0 through a 256-byte named-variable buffer (`embassy/control.rs:835`, `embassy/control.rs:717-727`). Size (computed from the field layout, not stated in source): the fields end at offset 74; the struct is repr(C) with 4-byte alignment, so size_of is 76 and to_bytes() sends all 76 bytes including 2 trailing padding bytes (`embassy/structs.rs:4-13`, `embassy/structs.rs:453-470`). — `embassy/control.rs:804-835`
3. event wait — ESCAN_RESULT (69), status 8 (PARTIAL) — one BSS record per event: runner parses ScanResults header then one BssInfo and queues it. Note: Scanner::next returns Some(bss) for each (`embassy/control.rs:917-926`) — `embassy/runner.rs:1320-1327`
4. event wait — ESCAN_RESULT (69), status != 8 — end of scan: Scanner::next disables the local event mask and returns None. Note: any status other than PARTIAL ends the stream; success (0) and abort statuses are not told apart — `embassy/control.rs:919-922`

Succeeds when: Stream of BssInfo ends with None on the first ESCAN_RESULT whose status is not 8 (`embassy/control.rs:919-922`).

Fails when:

- No distinction between completed and aborted scans (`embassy/control.rs:919-922`).
- No timeout: if no terminating event arrives the caller waits forever (`embassy/control.rs:918`).
- A PARTIAL event whose payload fails to parse is dropped in the runner (`embassy/runner.rs:1321-1326`).
- Events are published without blocking into a bounded queue; a slow consumer can lose results (`embassy/control.rs:773-775`, `embassy/runner.rs:1333-1340`).
- embassy does not act on the command status: the runner only logs a warning when the CDC status is non-zero ('TODO: propagate error instead', `embassy/runner.rs:1174-1176`), so a rejected command does not stop the sequence.
- Dropping the Scanner only clears the local event mask; no abort command is sent (`embassy/control.rs:932-936`).

### linux

1. precondition — no scan busy / aborting / suppressed, not connecting — vif not up -> -EIO; scan busy / aborting / suppressed, or the vif is connecting -> -EAGAIN — `linux/brcmfmac/cfg80211.c:1539-1561`
2. host / variable (set) — P2P scan preparation (unverified), then vndr_ie — brcmf_p2p_scan_prep (its commands are unverified), then brcmf_vif_set_mgmt_ie(vif, BRCMF_VNDR_IE_PRBREQ_FLAG, request->ie), which sets the variable vndr_ie with the probe-request vendor elements when its add/delete buffer is not empty (`linux/brcmfmac/cfg80211.c:5068-5073`); an error from either fails the request. Note: runs before the escan variable; BUSY bit and scan_request are set just before (`linux/brcmfmac/cfg80211.c:1565-1566`) — `linux/brcmfmac/cfg80211.c:1568-1576`
3. variable (set), quirk only — mpc — u32 = 0, only on devices with the NEED_MPC quirk — `linux/brcmfmac/cfg80211.c:1026-1030`, `linux/brcmfmac/cfg80211.c:1518`
4. variable (set) — escan — brcmf_escan_params_le (`linux/brcmfmac/fwil_types.h:460-468`): version u32 = 2 with v2 scan params when the SCAN_V2 feature is present, else version 1 with v1 params; action u16 = 1; sync_id u16 = 0x1234. Scan params: bssid ff x6, bss_type 2, nprobes / active_time / passive_time / home_time = -1, channel list as chanspecs, then (aligned to 4) one {len u32, ssid[32]} per requested SSID; channel_num = (n_ssids shifted left 16) OR n_channels. scan_type = 0 (active) when at least one SSID is requested, 1 (passive) when none. Note: an SSID entry of length 0 is the broadcast (wildcard) probe (`linux/brcmfmac/cfg80211.c:1160-1166`). v2 params also carry version = 2 and a length field (`linux/brcmfmac/cfg80211.c:1113`, `linux/brcmfmac/cfg80211.c:1128`, `linux/brcmfmac/cfg80211.c:1177`). In the v2 layout scan_type is a 32-bit field written with cpu_to_le32 (`linux/brcmfmac/cfg80211.c:1115`, `linux/brcmfmac/cfg80211.c:1175`). Constants: versions `linux/brcmfmac/fwil_types.h:54`, `linux/brcmfmac/fwil_types.h:73-74`; action `linux/brcmfmac/cfg80211.h:51`; NSSID shift `linux/brcmfmac/fwil_types.h:58` — `linux/brcmfmac/cfg80211.c:1096-1181`, `linux/brcmfmac/cfg80211.c:1443-1491`
5. host — arm 10000 ms scan timer — `linux/brcmfmac/cfg80211.c:1586-1588`, `linux/brcmfmac/cfg80211.h:49`
6. event wait — ESCAN_RESULT status 8 (PARTIAL) — one record per event (bss_count must be 1); merged into a host buffer, duplicates of the same BSSID/band/SSID update the stored RSSI — `linux/brcmfmac/cfg80211.c:3699-3767`
7. event wait — ESCAN_RESULT any other status except 4 — results reported to cfg80211; aborted = (status != 0); scan request completed. Note: completion also sets mpc back to 1 on quirk devices (`linux/brcmfmac/cfg80211.c:1228`) — `linux/brcmfmac/cfg80211.c:3769-3779`, `linux/brcmfmac/cfg80211.c:1184-1260`
8. command (set), on timeout — BRCMF_C_SCAN = 50 — scan params with channel_num = 1 and channel_list[0] = 0xFFFF (the driver's 'scan abort' form), v2 or converted to v1. Note: sent when the 10 s timer fires; the scan is then reported as aborted — `linux/brcmfmac/cfg80211.c:1123-1130`, `linux/brcmfmac/cfg80211.c:1203-1226`, `linux/brcmfmac/cfg80211.c:3611-3631`

Succeeds when: Final ESCAN_RESULT with status 0 -> cfg80211_scan_done with aborted = false (`linux/brcmfmac/cfg80211.c:3775-3776`, `linux/brcmfmac/cfg80211.c:1250-1257`).

Fails when:

- ESCAN_RESULT with status 4 (ABORT) is ignored outright (`linux/brcmfmac/cfg80211.c:3690-3691`).
- Any other non-zero, non-8 final status -> scan reported aborted (`linux/brcmfmac/cfg80211.c:3775`).
- No terminating event within 10 s -> command 50 abort and scan reported aborted (`linux/brcmfmac/cfg80211.c:3611-3631`).
- escan set returning an error fails the request; -EBUSY is logged as 'system busy : escan canceled' (`linux/brcmfmac/cfg80211.c:1491-1497`).
- Malformed PARTIAL events (bad lengths, bss_count != 1) are dropped (`linux/brcmfmac/cfg80211.c:3701-3733`).

### whd

1. argument check — scan_type must be 0 (active), 1 (passive), 4 (prohibited channels) or 8 (no BSSID filter); bss_type 0, 1 or 2 — else WHD_BADARG. Note: enum values `whd/inc/whd_types.h:347-361` — `whd/src/whd_wifi_api.c:3277-3288`
2. host — register handler for ESCAN_RESULT (69) — previous scan handler de-registered first — `whd/src/whd_wifi_api.c:3306-3318`, `whd/src/whd_wifi_api.c:161`
3. variable (set), side effect of handler registration — bsscfg:event_msgs (or bsscfg:event_msgs_ext when any registered event number exceeds 127) — u32 bsscfg index, then a 16-byte bit mask (WL_EVENTING_MASK_LEN, `whd/src/include/whd_wlioctl.h:1932`) holding the union of every currently registered handler's events; the _ext form carries version/command/length header plus a mask sized to the highest event. Note: whd rewrites the firmware event mask each time a handler is registered; de-registering only edits the host table and sends nothing (`whd/src/whd_events.c:597-626`) — `whd/src/whd_events.c:255-325`, `whd/src/whd_events.c:348-425`
4. variable (set) — escan — wl_escan_params_t (`whd/src/include/whd_wlioctl.h:548-554`): version u32 = 1, action u16 = 1 (START), sync_id u16 = 0 (buffer zeroed, never written), then scan params: ssid (len u32 + 32 bytes; zero unless optional_ssid), bssid (ff x6 unless optional_mac), bss_type, scan_type, nprobes / active_time / passive_time / home_time all -1 unless extended params are given, channel_num and channel_list (each entry converted with CH20MHZ_CHSPEC) when a channel list is given. Note: with an SSID on a tri-band platform the driver substitutes its own 2G/5G/6G channel list (`whd/src/whd_wifi_api.c:3290-3294`) — `whd/src/whd_wifi_api.c:3320-3389`
5. event wait — ESCAN_RESULT status 8 (PARTIAL) — one record per event: requires bss_info version match and bss_count == 1; converted and passed to the callback with WHD_SCAN_INCOMPLETE — `whd/src/whd_wifi_api.c:2633-2656`, `whd/src/whd_wifi_api.c:3022-3023`
6. event wait — ESCAN_RESULT status 0 — callback(NULL, WHD_SCAN_COMPLETED_SUCCESSFULLY); handler de-registered — `whd/src/whd_wifi_api.c:2615-2622`
7. event wait — ESCAN_RESULT status 9 (NEWSCAN), 10 (NEWASSOC) or 4 (ABORT) — callback(NULL, WHD_SCAN_ABORTED); handler de-registered. Note: status values `whd/inc/whd_events.h:61-71` — `whd/src/whd_wifi_api.c:2623-2631`
8. variable (set), optional abort — escan — wl_escan_params_t zeroed except version = 1, action = 3 (WL_SCAN_ACTION_ABORT). Note: whd_wifi_stop_scan; action constants `whd/src/include/whd_wlioctl.h:522-524` — `whd/src/whd_wifi_api.c:3394-3419`

Succeeds when: ESCAN_RESULT with status 0 -> WHD_SCAN_COMPLETED_SUCCESSFULLY (`whd/src/whd_wifi_api.c:2615-2617`).

Fails when:

- Statuses 4, 9, 10 -> WHD_SCAN_ABORTED (`whd/src/whd_wifi_api.c:2623-2626`).
- Any other non-8 status is ignored and the handler stays registered (`whd/src/whd_wifi_api.c:2633-2636`).
- If the callback clears the result pointer the driver reports ABORTED and de-registers, without sending an abort command (`whd/src/whd_wifi_api.c:3025-3032`).
- The escan set failing returns its error (CHECK_RETURN, `whd/src/whd_wifi_api.c:3389`).
- whd_wifi_scan_synch waits for completion with no timeout (`whd/src/whd_wifi_api.c:3209-3219`).

### c-driver

1. precondition — an interface must be up — returns -EPERM when itf_state == 0 — `c-driver/cyw43_ctrl.c:595-598`
2. host state — wifi_scan_state = 1, store callback — `c-driver/cyw43_ctrl.c:606-609`
3. variable (set) — escan — cyw43_wifi_scan_options_t (`c-driver/cyw43_ll.h:255-270`): version u32=1, action u16=1, pad u16=0, ssid_len u32 (caller; 0 = all), ssid[32] (caller), bssid[6]=ff x6, bss_type i8=2, scan_type i8 (caller; 0 active, 1 passive), nprobes i32=-1, active_time i32=-1, passive_time i32=-1, home_time i32=-1, channel_num i32=0, channel_list[1] u16=0. Note: station interface. The public header says the option values 'are currently ignored' (`c-driver/cyw43.h:366`) but the low-level function leaves ssid_len, ssid and scan_type as the caller set them. Size (computed, not stated in source): fields end at offset 74, natural alignment 4, so sizeof(cyw43_wifi_scan_options_t) = 76 bytes are sent (`c-driver/cyw43_ll.c:2202`) — `c-driver/cyw43_ll.c:2188-2205`
4. event wait — ESCAN_RESULT (69) status 8 — result callback called once per event with the parsed record (bssid, ssid, channel & 0xff, rssi, auth_mode derived from RSN/WPA elements). Note: only while wifi_scan_state == 1 — `c-driver/cyw43_ctrl.c:319-326`, `c-driver/cyw43_ll.c:668-718`, `c-driver/cyw43_ll.c:744-746`
5. event wait — ESCAN_RESULT (69) status 0 — wifi_scan_state = 2: scan complete. Note: cyw43_wifi_scan_active() then returns false (`c-driver/cyw43.h:381-383`) — `c-driver/cyw43_ctrl.c:327-330`

Succeeds when: ESCAN_RESULT with status 0 sets the scan state to 2 (`c-driver/cyw43_ctrl.c:327-329`).

Fails when:

- Any ESCAN_RESULT status other than 8 or 0 is ignored, so the scan state stays 'active' (`c-driver/cyw43_ctrl.c:321-330`).
- A non-zero return from the result callback does not abort the scan ('TODO need to abort scan', `c-driver/cyw43_ctrl.c:324-326`).
- A record whose element offsets exceed its length is marked invalid by overwriting the event status with 0xFFFFFFFF, which then matches neither branch (`c-driver/cyw43_ll.c:677-681`).
- No timeout and no abort command. `c-driver/cyw43_ctrl.c:593-617`, `c-driver/cyw43_ll.c:2188-2205`
- Most set helpers in cyw43_ll.c are void and discard the command result (`c-driver/cyw43_ll.c:1538-1562`, `c-driver/cyw43_ll.c:1956-1960`); the only failure surfaced is a 500 ms response timeout inside cyw43_do_ioctl, which returns -ETIMEDOUT to callers that check it (`c-driver/cyw43_ll.c:1294-1325`, `c-driver/cyw43_config.h:92`).

### Differences

Differences: All four drivers start a scan by setting the variable `escan` and read results from ESCAN_RESULT (69) events with status 8, one BSS record per event. `embassy/control.rs:804-835`, `linux/brcmfmac/cfg80211.c:1443-1491`, `whd/src/whd_wifi_api.c:3320-3389`, `c-driver/cyw43_ll.c:2188-2205`

| Aspect | embassy | linux | whd | c-driver | Citations |
|---|---|---|---|---|---|
| `escan` version | 1 | 2 with the v2 parameter layout when the SCAN_V2 feature is present, else 1 | 1 | 1 | `embassy/control.rs:804-835`, `linux/brcmfmac/cfg80211.c:1443-1491`, `whd/src/whd_wifi_api.c:3320-3389`, `c-driver/cyw43_ll.c:2188-2205` |
| sync_id | 1 | 0x1234 | 0 (buffer zeroed, field never written) | 0 (written as a pad field) | `embassy/control.rs:804-835`, `linux/brcmfmac/cfg80211.c:1443-1491`, `whd/src/whd_wifi_api.c:3320-3389`, `c-driver/cyw43_ll.c:2188-2205` |
| Scan type | caller option; default passive | not chosen directly: active when at least one SSID is requested, passive when none | caller argument 0, 1, 4 or 8; whd_wifi_scan_synch passes active | caller's field, 0 active or 1 passive | `embassy/control.rs:804-835`, `linux/brcmfmac/cfg80211.c:1096-1181`, `whd/src/whd_wifi_api.c:3277-3288`, `whd/src/whd_wifi_api.c:3209`, `c-driver/cyw43_ll.c:2188-2205` |
| nprobes when not given | 0x0000FFFF as written (inferred from the option's u16 type) | -1 | -1 | -1 | `embassy/control.rs:820`, `embassy/control.rs:83`, `linux/brcmfmac/cfg80211.c:1096-1181`, `whd/src/whd_wifi_api.c:3320-3389`, `c-driver/cyw43_ll.c:2188-2205` |
| SSID filter | one, optional | several per request, each {len u32, ssid[32]}; length 0 is the wildcard | one, optional | one, from the caller | `embassy/control.rs:804-835`, `linux/brcmfmac/cfg80211.c:1096-1181`, `linux/brcmfmac/cfg80211.c:1160-1166`, `whd/src/whd_wifi_api.c:3320-3389`, `c-driver/cyw43_ll.c:2188-2205` |
| BSSID filter | optional, else ff x6 | always ff x6 | optional, else ff x6 | always ff x6 | `embassy/control.rs:804-835`, `linux/brcmfmac/cfg80211.c:1096-1181`, `whd/src/whd_wifi_api.c:3320-3389`, `c-driver/cyw43_ll.c:2188-2205` |
| Channel list | none: channel_num 0 | chanspec list; channel_num = (n_ssids shifted left 16) OR n_channels | optional list, entries converted with CH20MHZ_CHSPEC | none: channel_num 0 | `embassy/control.rs:804-835`, `linux/brcmfmac/cfg80211.c:1096-1181`, `whd/src/whd_wifi_api.c:3320-3389`, `c-driver/cyw43_ll.c:2188-2205` |
| Firmware event mask | set once at init; the scan only edits embassy's local filter | not sent in the scan path; `event_msgs` is written elsewhere | rewritten (`bsscfg:event_msgs` or `bsscfg:event_msgs_ext`) each time a handler is registered | not sent in the scan path; `bsscfg:event_msgs` is built elsewhere | `embassy/control.rs:828`, `embassy/control.rs:305-319`, `linux/brcmfmac/fweh.c:462`, `linux/brcmfmac/cfg80211.c:1443-1491`, `whd/src/whd_events.c:255-325`, `whd/src/whd_events.c:348-425`, `c-driver/cyw43_ll.c:2059`, `c-driver/cyw43_ll.c:2188-2205` |
| Result delivery | stream: Scanner::next returns one BssInfo per event | merged into a host buffer, reported to cfg80211 at the end | callback per record | callback per record; completion is a polled state flag | `embassy/control.rs:917-926`, `linux/brcmfmac/cfg80211.c:3699-3767`, `linux/brcmfmac/cfg80211.c:3769-3779`, `whd/src/whd_wifi_api.c:2633-2656`, `c-driver/cyw43_ctrl.c:319-330` |
| End of scan | any status other than 8; completed and aborted are not told apart | any status other than 8 and 4; aborted = (status != 0); status 4 is ignored | status 0 completed; 4, 9, 10 aborted; other statuses ignored | status 0 completed; every other non-8 status ignored | `embassy/control.rs:919-922`, `linux/brcmfmac/cfg80211.c:3690-3691`, `linux/brcmfmac/cfg80211.c:3769-3779`, `whd/src/whd_wifi_api.c:2615-2636`, `c-driver/cyw43_ctrl.c:321-330` |
| Abort command | none; dropping the Scanner sends nothing | command 50 (BRCMF_C_SCAN) with channel_num 1 and channel_list[0] = 0xFFFF | `escan` with action 3 | none | `embassy/control.rs:932-936`, `linux/brcmfmac/cfg80211.c:1203-1226`, `whd/src/whd_wifi_api.c:3394-3419`, `c-driver/cyw43_ctrl.c:324-326` |
| Host timeout | none | 10000 ms timer, then the abort command | none in whd_wifi_scan_synch | none | `embassy/control.rs:918`, `linux/brcmfmac/cfg80211.c:1586-1588`, `linux/brcmfmac/cfg80211.c:3611-3631`, `whd/src/whd_wifi_api.c:3209-3219`, `c-driver/cyw43_ctrl.c:593-617` |
| Rejected `escan` set | command status only logged | error fails the request | error returned | set helpers discard the result | `embassy/runner.rs:1174-1176`, `linux/brcmfmac/cfg80211.c:1491-1497`, `whd/src/whd_wifi_api.c:3389`, `c-driver/cyw43_ll.c:1538-1562` |

## Join open

### embassy

1. command (set), conditional — Disassoc = 52 — empty. Note: only when an earlier join was started and not completed/left (started_join flag) — `embassy/control.rs:369-371`, `embassy/control.rs:841`
2. variable (set) — ampdu_ba_wsize — u32 = 8 — `embassy/control.rs:374`
3. command (set) — SetWsec = 134 — u32 = 0 — `embassy/control.rs:377`
4. variable (set) — bsscfg:sup_wpa — u32 0 (bsscfg index), u32 0 — `embassy/control.rs:378`
5. command (set) — SetInfra = 20 — u32 = 1 — `embassy/control.rs:379`
6. command (set) — SetAuth = 22 — u32 = 0 (open system) — `embassy/control.rs:380`
7. command (set) — SetWpaAuth = 165 — u32 = 0 (WPA_AUTH_DISABLED, `embassy/consts.rs:742`) — `embassy/control.rs:381`
8. host-side event filter — enable SET_SSID (0), AUTH (3), PSK_SUP (46) in the driver's own event mask — no bytes sent. Note: done before the join command so no event is missed (`embassy/control.rs:466-467`) — `embassy/control.rs:464`
9. command (set) — SetSsid = 26 — SsidInfo (`embassy/structs.rs:400-403`): len u32, ssid[32]; 36 bytes. Note: interface 0; this starts the join — `embassy/control.rs:438-442`, `embassy/control.rs:469`
10. event wait — SET_SSID (0) status 0 — join() returns Ok. Note: the runner separately raises the network link when it sees JOIN (1) status 0 (`embassy/runner.rs:1268-1271`, `embassy/runner.rs:1298-1304`) — `embassy/control.rs:480`

Succeeds when: SET_SSID event with status 0 (`embassy/control.rs:480`).

Fails when:

- SET_SSID status 3 (NO_NETWORKS) -> JoinError::NetworkNotFound (`embassy/control.rs:481`).
- SET_SSID any other non-zero status -> JoinError::JoinFailure(status) (`embassy/control.rs:482-484`).
- No timeout inside join(); the caller must add one (`embassy/control.rs:474-496`).
- embassy does not act on the command status: the runner only logs a warning when the CDC status is non-zero ('TODO: propagate error instead', `embassy/runner.rs:1174-1176`), so a rejected command does not stop the sequence.
- Link later drops on LINK status 0 flags 0, DEAUTH status 0, any DEAUTH_IND, any DISASSOC_IND (`embassy/runner.rs:1249-1258`).

### linux

1. variable (set) — wpaie — WPA or RSN element from the request, or empty; primary interface only; result ignored — `linux/brcmfmac/cfg80211.c:2449-2466`
2. variable (set) — vndr_ie — vendor elements for association requests: brcmf_vif_set_mgmt_ie(BRCMF_VNDR_IE_ASSOCREQ_FLAG, sme->ie) sets vndr_ie when its add/delete buffer is not empty; an error is only logged — `linux/brcmfmac/cfg80211.c:2468-2473`, `linux/brcmfmac/cfg80211.c:5068-5073`
3. variable (set) — wpa_auth — u32 = 0 (WPA_AUTH_DISABLED) when the request has no WPA version. Note: brcmf_fil_bsscfg_* helpers send the plain variable name when the interface's bsscfg index is 0 and `bsscfg:<name>` + u32 index otherwise (`linux/brcmfmac/fwil.c:248-290`). — `linux/brcmfmac/cfg80211.c:1957-1989`
4. variable (set) — auth — u32: 0 open system, 1 shared key, 3 SAE, 2 for any other request value (automatic). Note: on devices with the AUTO_AUTH quirk an 'automatic' request is first rewritten to open system (`linux/brcmfmac/cfg80211.c:2355-2364`, `linux/brcmfmac/cfg80211.c:2496`) — `linux/brcmfmac/cfg80211.c:1991-2029`
5. variable (set) — wsec — u32 = pairwise | group cipher bits = 0 for open — `linux/brcmfmac/cfg80211.c:2031-2104`
6. variable (set), FWSUP feature only — sup_wpa — u32 = 0. Note: key-management and shared-key steps return early without commands when there are no AKM suites / no WEP key (`linux/brcmfmac/cfg80211.c:2130-2131`, `linux/brcmfmac/cfg80211.c:2300`) — `linux/brcmfmac/cfg80211.c:2521-2546`
7. command (set) + variable (set) — BRCMF_C_SET_ASSOC_PREFER = 205, then join_pref — first, unless the request's bss_select behaviour is BAND_PREF: command BRCMF_C_SET_ASSOC_PREFER = 205 with u32 WLC_BAND_AUTO, result ignored (`linux/brcmfmac/cfg80211.c:2377-2378`; `linux/brcmfmac/fwil.h:74`). Then variable 'join_pref' with two brcmf_join_pref_params records. When user space gave no bss_select (behaviour 0, __NL80211_BSS_SELECT_ATTR_INVALID) the driver's default pair is sent instead: {RSSI_DELTA, len 2, rssi_gain BRCMF_JOIN_PREF_RSSI_BOOST, band 5G} + {RSSI, len 2, 0, 0} (`linux/brcmfmac/cfg80211.c:2381-2383`; `linux/brcmfmac/common.c:80-100`). Otherwise {BAND or RSSI_DELTA record, if selected} + {RSSI, len 2, 0, 0}, always sizeof two records (`linux/brcmfmac/cfg80211.c:2384-2406`). Errors only logged — `linux/brcmfmac/cfg80211.c:2366-2409`, `linux/brcmfmac/cfg80211.c:2620`, `linux/brcmfmac/common.c:80-100`
8. variable (set) — join — brcmf_ext_join_params_le: ssid (len u32 + 32), scan params (scan_type = -1, home_time = -1; active_time 320, passive_time 400, nprobes 16 when a channel is known, else all -1), assoc params (BSSID or ff x6, chanspec_num 1 + one chanspec when a channel is known). Note: brcmf_fil_bsscfg_* helpers send the plain variable name when the interface's bsscfg index is 0 and `bsscfg:<name>` + u32 index otherwise (`linux/brcmfmac/fwil.c:248-290`). Size (computed from the layouts at `linux/brcmfmac/fwil_types.h:482-490`, `linux/brcmfmac/fwil_types.h:515-534`, not stated in source): ssid_le 36 + scan_le 20 + 12 bytes of assoc_le up to chanspec_list = 68 bytes, or 70 with one chanspec (`linux/brcmfmac/cfg80211.c:2569-2572`) - the same 70-byte shape c-driver builds by hand (`c-driver/cyw43_ll.c:2300-2325`). scan_type is a u8, so -1 is 0xFF (`linux/brcmfmac/fwil_types.h:516`, `linux/brcmfmac/fwil_types.h:61`). — `linux/brcmfmac/cfg80211.c:2564-2623`, `linux/brcmfmac/cfg80211.c:80-82`
9. command (set), fallback — BRCMF_C_SET_SSID = 26 — only if the 'join' variable failed: struct brcmf_join_params. With no known channel only the 36-byte ssid_le part is sent (join_params_size = sizeof(ssid_le)), so the BSSID that was filled in is not sent; with a channel the whole struct is sent: ssid_le + assoc params (bssid, chanspec_num 1, one chanspec) (`linux/brcmfmac/cfg80211.c:2629-2647`) — `linux/brcmfmac/cfg80211.c:2629-2649`
10. event wait — SET_SSID status 0 — connect reported successful; carrier on — `linux/brcmfmac/cfg80211.c:6255-6259`, `linux/brcmfmac/cfg80211.c:6796-6811`

Succeeds when: SET_SSID event with status 0 (`linux/brcmfmac/cfg80211.c:6255-6259`). Handler brcmf_notify_connect_status is registered for LINK, DEAUTH_IND, DEAUTH, DISASSOC_IND, ASSOC_IND, REASSOC_IND, SET_SSID and PSK_SUP (`linux/brcmfmac/cfg80211.c:6993-7026`).

Fails when:

- SET_SSID with non-zero status -> connect reported failed (WLAN_STATUS_AUTH_TIMEOUT) (`linux/brcmfmac/cfg80211.c:6303-6306`, `linux/brcmfmac/cfg80211.c:6705-6712`).
- LINK with status 3 (NO_NETWORKS) -> failed (`linux/brcmfmac/cfg80211.c:6297-6301`).
- PSK_SUP with status other than 6 -> failed (`linux/brcmfmac/cfg80211.c:6308-6313`).
- DEAUTH, DEAUTH_IND, DISASSOC_IND, or LINK without the link flag while connecting/connected -> connect failed / disconnected; driver then sends command 52 with no payload if it had been connected, and clears the PMK (command 268 with key_len 0) if the firmware supplicant was in use (`linux/brcmfmac/cfg80211.c:6274-6289`, `linux/brcmfmac/cfg80211.c:6812-6835`, `linux/brcmfmac/cfg80211.c:1745-1781`). When already connected, such an event for a different BSSID is ignored (`linux/brcmfmac/cfg80211.c:6819-6822`).
- Any configuration command failing returns the error from connect() (`linux/brcmfmac/cfg80211.c:2490-2517`).
- No driver-side join timeout in this function; cfg80211/user space owns it. `linux/brcmfmac/cfg80211.c:2449-2649`
- Order of tests in the handler: link-up, then link-down, then no-network (`linux/brcmfmac/cfg80211.c:6796-6840`), so an event that satisfies an earlier test never reaches a later one.

### whd

1. host — clear join status word for this bsscfg — `whd/src/whd_wifi_api.c:1755-1756`
2. command (set) — WLC_SET_WSEC = 134 — u32 = 0 (auth_type & 0xFF) — `whd/src/whd_wifi_api.c:1766`
3. variable (set) — roam_off — u32 = 0 — `whd/src/whd_wifi_api.c:1785-1786`
4. variable (set) — bsscfg:sup_wpa — u32 bsscfg index, u32 0; result ignored — `whd/src/whd_wifi_api.c:1817-1824`
5. variable (set) — bsscfg:sup_wpa2_eapver — u32 index, u32 0xFFFFFFFF; result ignored — `whd/src/whd_wifi_api.c:1826-1831`
6. command (set) — WLC_SET_INFRA = 20 — u32 = 1 — `whd/src/whd_wifi_api.c:1910`
7. command (set) — WLC_SET_AUTH = 22 — u32 = 0 (WL_AUTH_OPEN_SYSTEM) — `whd/src/whd_wifi_api.c:1912-1921`
8. variable (set) — mfp — u32 = 0 (WL_MFP_NONE, the initial value; not read first for open); skipped when is_mfp_auto; result ignored — `whd/src/whd_wifi_api.c:1722`, `whd/src/whd_wifi_api.c:1758-1763`, `whd/src/whd_wifi_api.c:1928-1947`
9. command (set) — WLC_SET_WPA_AUTH = 165 — u32 = 0 (WPA_AUTH_DISABLED) — `whd/src/whd_wifi_api.c:1975-1980`, `whd/src/whd_wifi_api.c:2049-2050`
10. host — register join handler for SET_SSID (0), LINK (16), AUTH (3), DEAUTH_IND (6), DISASSOC_IND (12), PSK_SUP (46), CSA_COMPLETE_IND (80), REASSOC (9), PROBRESP_MSG (71) — Note: event numbers from `whd/inc/whd_events.h:37-53` and `whd/src/include/whd_events_int.h:107`, `whd/src/include/whd_events_int.h:115`. REASSOC status 0 sets LINK_READY|SSID_SET (`whd/src/whd_wifi_api.c:1464-1471`) — `whd/src/whd_wifi_api.c:156-160`, `whd/src/whd_wifi_api.c:2063-2076`
11. variable (set), side effect of handler registration — bsscfg:event_msgs (or bsscfg:event_msgs_ext when any registered event number exceeds 127) — u32 bsscfg index, then a 16-byte bit mask (WL_EVENTING_MASK_LEN, `whd/src/include/whd_wlioctl.h:1932`) holding the union of every currently registered handler's events; the _ext form carries version/command/length header plus a mask sized to the highest event. Note: whd rewrites the firmware event mask each time a handler is registered; de-registering only edits the host table and sends nothing (`whd/src/whd_events.c:597-626`) — `whd/src/whd_events.c:255-325`, `whd/src/whd_events.c:348-425`
12. command (set) — WLC_SET_SSID = 26 — wlc_ssid_t: SSID_len u32, SSID[32]; 36 bytes. Note: whd_wifi_join. whd_wifi_join_specific instead sends the 'join' variable (wl_extjoin_params_t with BSSID, scan_type 0, times -1, optional single chanspec), falls back to SET_SSID with wl_join_params_t when the variable is unsupported, and uses WLC_REASSOC when already connected to the same SSID (`whd/src/whd_wifi_api.c:2320-2398`) — `whd/src/whd_wifi_api.c:2478-2483`
13. event wait — PROBRESP_MSG, AUTH status 0, LINK flags&1, SET_SSID status 0 — status word reaches the success value — `whd/src/whd_wifi_api.c:2114-2174`, `whd/src/whd_wifi_api.c:2205-2206`

Succeeds when: whd_wifi_check_join_status returns WHD_SUCCESS only when the status word is exactly PROBE_RESPONSE|AUTHENTICATED|LINK_READY|SSID_SET|SECURITY_COMPLETE (`whd/src/whd_wifi_api.c:2205-2206`). Bits are set by: PROBRESP_MSG (any) -> PROBE_RESPONSE (`whd/src/whd_wifi_api.c:1473-1475`); AUTH status 0 -> AUTHENTICATED (`whd/src/whd_wifi_api.c:1439-1443`); LINK with flags bit 0 -> LINK_READY (`whd/src/whd_wifi_api.c:1422-1426`); SET_SSID status 0 -> SSID_SET (`whd/src/whd_wifi_api.c:1405-1410`); PSK_SUP wire status 6 while LINK_READY -> SECURITY_COMPLETE (`whd/src/whd_wifi_api.c:1359-1368`); for open networks SECURITY_COMPLETE is pre-set (`whd/src/whd_wifi_api.c:1975-1980`).

Fails when:

- SET_SSID status 3 sets NO_NETWORKS; WHD_NETWORK_NOT_FOUND is returned only when that is the sole bit set (`whd/src/whd_wifi_api.c:1412-1415`, `whd/src/whd_wifi_api.c:2187-2188`, `whd/src/whd_wifi_api.c:2148-2151`). In an open join SECURITY_COMPLETE is already set (`whd/src/whd_wifi_api.c:1979`), so the word is NO_NETWORKS|SECURITY_COMPLETE, which falls to the default case: WHD_INVALID_JOIN_STATUS, ended by the 3000 ms rule below, not WHD_NETWORK_NOT_FOUND (`whd/src/whd_wifi_api.c:2221-2229`; inferred from the switch, not from a comment in source).
- SET_SSID any other non-zero status ends the attempt (`whd/src/whd_wifi_api.c:1416-1419`).
- AUTH status 6 (unsolicited) ignored; any other non-zero AUTH status ends the attempt (`whd/src/whd_wifi_api.c:1444-1452`).
- DEAUTH_IND / DISASSOC_IND clear AUTHENTICATED and LINK_READY (`whd/src/whd_wifi_api.c:1433-1437`).
- Wait loop: 1000 ms semaphore slices, re-evaluating the status word each time (`whd/src/whd_wifi_api.c:2134-2160`). It ends at once on WHD_SUCCESS or WHD_NETWORK_NOT_FOUND. It ends after 3000 ms (DEFAULT_JOIN_RESPONSE_TIMEOUT) only while whd_wifi_check_join_status returns WHD_INVALID_JOIN_STATUS, which is the default case for a status word that has no PROBE_RESPONSE bit and is not one of the listed patterns (`whd/src/whd_wifi_api.c:2221-2229`) - for example NO_NETWORKS together with the pre-set SECURITY_COMPLETE of an open join, or AUTHENTICATED without a probe response. A status word of exactly 0 (nothing seen yet), or exactly SECURITY_COMPLETE, returns WHD_NOT_AUTHENTICATED (`whd/src/whd_wifi_api.c:2208-2210`) and, like every other in-progress result, runs to the overall timeout: the configured wifi_join_timeout or 13000 ms (`whd/src/whd_wifi_api.c:76-78`, `whd/src/whd_wifi_api.c:2123-2127`, `whd/src/whd_wifi_api.c:2156-2159`).
- On any non-success result the driver calls whd_wifi_leave (command 52) (`whd/src/whd_wifi_api.c:2167-2171`).
- Command errors abort the sequence through CHECK_RETURN, except the sup_wpa / sup_wpa2_eapver / mfp sets whose results are ignored (`whd/src/whd_wifi_api.c:1824`, `whd/src/whd_wifi_api.c:1831`, `whd/src/whd_wifi_api.c:1942-1946`).

### c-driver

1. variable (set) — ampdu_ba_wsize — u32 = 8. Note: station interface — `c-driver/cyw43_ll.c:2212`
2. command (set) — WLC_SET_WSEC = 134 — u32 = 0 (auth_type & 0xff) — `c-driver/cyw43_ll.c:2236`
3. variable (set) — bsscfg:sup_wpa — u32 0, u32 0 — `c-driver/cyw43_ll.c:2240`
4. variable (set) — bsscfg:sup_wpa2_eapver — u32 0, u32 0xFFFFFFFF. Note: sent for open as well — `c-driver/cyw43_ll.c:2244`
5. variable (set) — bsscfg:sup_wpa_tmo — u32 0, u32 5000. Note: sent for open as well — `c-driver/cyw43_ll.c:2248`, `c-driver/cyw43_ll.c:258`
6. command (set) — WLC_SET_INFRA = 20 — u32 = 1 — `c-driver/cyw43_ll.c:2271`
7. command (set) — WLC_SET_AUTH = 22 — u32 = 0 — `c-driver/cyw43_ll.c:2275`
8. variable (set) — mfp — u32 = 0 (MFP_NONE) — `c-driver/cyw43_ll.c:2276`
9. command (set) — WLC_SET_WPA_AUTH = 165 — u32 = 0 — `c-driver/cyw43_ll.c:2214-2216`, `c-driver/cyw43_ll.c:2280`
10. command (set) or variable (set) — WLC_SET_SSID = 26, or 'join' when a BSSID is given — SET_SSID: u32 ssid_len + ssid[32], 36 bytes. 'join': 70 bytes = ssid_len u32, ssid[32], scan_type u8 0 + 3 pad, nprobes -1, active_time -1, passive_time -1, home_time -1, bssid[6] + 2 pad, chanspec_num u32 (1 when a channel is given), chanspec u16 = channel | 0x1000 (20 MHz, 2.4 GHz) — `c-driver/cyw43_ll.c:2296-2330`
11. event wait — AUTH (3) status 0, LINK (16) status 0 flags&1 — state reaches 0x0e01, link reported up to the IP stack — `c-driver/cyw43_ctrl.c:366-372`, `c-driver/cyw43_ctrl.c:389-394`, `c-driver/cyw43_ctrl.c:422-426`

Succeeds when: Join completes when the state word equals ACTIVE|AUTH|LINK|KEYED = 0x0e01 (`c-driver/cyw43_ctrl.c:32-40`, `c-driver/cyw43_ctrl.c:422-426`): AUTH (3) status 0 sets AUTH (`c-driver/cyw43_ctrl.c:366-372`); LINK (16) status 0 with flags bit 0 on the station interface sets LINK (`c-driver/cyw43_ctrl.c:389-394`); PSK_SUP (46) status 6 sets KEYED (`c-driver/cyw43_ctrl.c:403-405`), and for open networks KEYED is pre-set (`c-driver/cyw43_ctrl.c:661-664`).

Fails when:

- Before any command: -EPERM if the station interface is not active (`c-driver/cyw43_ctrl.c:643-646`); -EINVAL for an auth_type outside the six handled values (`c-driver/cyw43_ll.c:2214-2226`) or a key longer than 64 bytes (128 for pure WPA3) (`c-driver/cyw43_ll.c:2228-2233`). ampdu_ba_wsize has already been sent when -EINVAL is returned (`c-driver/cyw43_ll.c:2212`).
- SET_SSID (0) status 3 with reason 0 -> state NONET (CYW43_LINK_NONET); any other non-zero SET_SSID status -> FAIL (`c-driver/cyw43_ctrl.c:355-365`).
- AUTH status 2 (timeout), 5 (no ack), 6 (unsolicited) are ignored; any other non-zero AUTH status -> BADAUTH (`c-driver/cyw43_ctrl.c:373-382`).
- DEAUTH_IND (6) status 0 reason 2 -> driver schedules command 52 (disassoc) and clears the state (`c-driver/cyw43_ctrl.c:383-388`, `c-driver/cyw43_ctrl.c:216-221`).
- PRUNE (23) status 0 reason 8 (RSN mismatch) -> driver sets WPA_AUTH (165) = 0x0004 and re-sends SET_SSID (`c-driver/cyw43_ctrl.c:348-354`, `c-driver/cyw43_ctrl.c:223-232`; `c-driver/cyw43_ll.c:2335-2343`).
- ICV_ERROR (49) -> re-send SET_SSID (`c-driver/cyw43_ctrl.c:416-420`).
- DISASSOC (11) on the station interface -> IP-stack link-down callback; and only if the state kind is still ACTIVE the state word is reset to plain ACTIVE (0x0001), dropping the AUTH/LINK/KEYED flags so the join has to collect them again (`c-driver/cyw43_ctrl.c:332-337`).
- The join call returns immediately; there is no timeout in the driver, the caller polls cyw43_wifi_link_status (`c-driver/cyw43_ctrl.c:619-636`).
- Most set helpers in cyw43_ll.c are void and discard the command result (`c-driver/cyw43_ll.c:1538-1562`, `c-driver/cyw43_ll.c:1956-1960`); the only failure surfaced is a 500 ms response timeout inside cyw43_do_ioctl, which returns -ETIMEDOUT to callers that check it (`c-driver/cyw43_ll.c:1294-1325`, `c-driver/cyw43_config.h:92`).

### Differences

Differences: embassy and c-driver configure security with commands 134 / 22 / 165 and start the join with command 26; linux uses the variables `wsec` / `auth` / `wpa_auth` and tries the variable `join` first. `embassy/control.rs:377-381`, `embassy/control.rs:469`, `c-driver/cyw43_ll.c:2236-2330`, `linux/brcmfmac/cfg80211.c:1957-2104`, `linux/brcmfmac/cfg80211.c:2564-2649`

| Aspect | embassy | linux | whd | c-driver | Citations |
|---|---|---|---|---|---|
| Join trigger | command 26 (SET_SSID), 36 bytes | variable `join` first; command 26 only if `join` failed | command 26 in whd_wifi_join; whd_wifi_join_specific sends `join`, falls back to command 26, or uses WLC_REASSOC | command 26, or variable `join` (70 bytes) when a BSSID is given | `embassy/control.rs:438-442`, `embassy/control.rs:469`, `linux/brcmfmac/cfg80211.c:2564-2649`, `whd/src/whd_wifi_api.c:2478-2483`, `whd/src/whd_wifi_api.c:2320-2398`, `c-driver/cyw43_ll.c:2296-2330` |
| wsec / auth / wpa_auth | commands 134 / 22 / 165, all 0 | variables `wsec` / `auth` / `wpa_auth` | commands 134 / 22 / 165, all 0 | commands 134 / 22 / 165, all 0 | `embassy/control.rs:377-381`, `linux/brcmfmac/cfg80211.c:1957-2104`, `whd/src/whd_wifi_api.c:1766`, `whd/src/whd_wifi_api.c:1912-1921`, `whd/src/whd_wifi_api.c:2049-2050`, `c-driver/cyw43_ll.c:2236`, `c-driver/cyw43_ll.c:2275`, `c-driver/cyw43_ll.c:2280` |
| SET_INFRA (20) | 1 | not sent in the connect path | 1 | 1 | `embassy/control.rs:379`, `linux/brcmfmac/cfg80211.c:2449-2649`, `whd/src/whd_wifi_api.c:1910`, `c-driver/cyw43_ll.c:2271` |
| Disassoc first | command 52 when an earlier join was started and not completed or left | no | no | no | `embassy/control.rs:369-371`, `linux/brcmfmac/cfg80211.c:2449-2649`, `whd/src/whd_wifi_api.c:1717-2080`, `c-driver/cyw43_ll.c:2207-2333` |
| ampdu_ba_wsize | 8 | not found in these sources | not sent in the join path; set only in the AP code | 8 | `embassy/control.rs:374`, `whd/src/whd_ap.c:118`, `whd/src/whd_ap.c:128`, `c-driver/cyw43_ll.c:2212` |
| sup_wpa | `bsscfg:sup_wpa` = 0 | `sup_wpa` = 0, FWSUP feature only | `bsscfg:sup_wpa` = 0, result ignored | `bsscfg:sup_wpa` = 0 | `embassy/control.rs:378`, `linux/brcmfmac/cfg80211.c:2521-2546`, `whd/src/whd_wifi_api.c:1817-1824`, `c-driver/cyw43_ll.c:2240` |
| sup_wpa2_eapver for open | not sent | not sent | 0xFFFFFFFF, result ignored | 0xFFFFFFFF | `embassy/control.rs:369-469`, `linux/brcmfmac/cfg80211.c:2449-2649`, `whd/src/whd_wifi_api.c:1826-1831`, `c-driver/cyw43_ll.c:2244` |
| sup_wpa_tmo for open | not sent | not sent | not sent | 5000 | `embassy/control.rs:369-469`, `linux/brcmfmac/cfg80211.c:2449-2649`, `whd/src/whd_wifi_api.c:1717-2080`, `c-driver/cyw43_ll.c:2248` |
| mfp for open | not sent | not sent | 0, skipped when is_mfp_auto, result ignored | 0 | `embassy/control.rs:369-469`, `linux/brcmfmac/cfg80211.c:2449-2649`, `whd/src/whd_wifi_api.c:1928-1947`, `c-driver/cyw43_ll.c:2276` |
| roam_off | not sent | not sent in the connect path; set outside it | 0 | not sent | `embassy/control.rs:369-469`, `linux/brcmfmac/cfg80211.c:2449-2649`, `linux/brcmfmac/cfg80211.c:7131`, `whd/src/whd_wifi_api.c:1785-1786`, `c-driver/cyw43_ll.c:2207-2333` |
| Association preference | none | command 205 then variable `join_pref` | none | none | `embassy/control.rs:369-469`, `linux/brcmfmac/cfg80211.c:2366-2409`, `whd/src/whd_wifi_api.c:1717-2080`, `c-driver/cyw43_ll.c:2207-2333` |
| Success test | SET_SSID status 0 | SET_SSID status 0 | PROBRESP_MSG + AUTH status 0 + LINK with flags bit 0 + SET_SSID status 0 (SECURITY_COMPLETE pre-set) | AUTH status 0 + LINK status 0 with flags bit 0 (KEYED pre-set) | `embassy/control.rs:480`, `linux/brcmfmac/cfg80211.c:6255-6259`, `whd/src/whd_wifi_api.c:2205-2206`, `whd/src/whd_wifi_api.c:1975-1980`, `c-driver/cyw43_ctrl.c:422-426`, `c-driver/cyw43_ctrl.c:661-664` |
| Timeout | none inside join() | none in the driver | blocking call: 13000 ms or the configured value; 3000 ms while the status word is invalid | none; the call returns at once and the caller polls | `embassy/control.rs:474-496`, `linux/brcmfmac/cfg80211.c:2449-2649`, `whd/src/whd_wifi_api.c:2123-2160`, `c-driver/cyw43_ctrl.c:619-636` |
| After a failed attempt | error returned to the caller | connect reported failed | driver sends leave (command 52) | state set to NONET / FAIL / BADAUTH; some events trigger a re-send of SET_SSID | `embassy/control.rs:481-484`, `linux/brcmfmac/cfg80211.c:6303-6306`, `whd/src/whd_wifi_api.c:2167-2171`, `c-driver/cyw43_ctrl.c:355-382`, `c-driver/cyw43_ctrl.c:416-420` |

## Join WPA2

### embassy

1. command (set), conditional — Disassoc = 52 — empty. Note: only when an earlier join was started and not completed/left — `embassy/control.rs:369-371`, `embassy/control.rs:841`
2. variable (set) — ampdu_ba_wsize — u32 = 8 — `embassy/control.rs:374`
3. command (set) — SetWsec = 134 — u32 = cipher bits: AES 0x04 (default), TKIP 0x02 (optional), OR-ed. Note: constants `embassy/consts.rs:732-733` — `embassy/control.rs:383-390`
4. variable (set) — bsscfg:sup_wpa — u32 0, u32 1 — `embassy/control.rs:392`
5. variable (set) — bsscfg:sup_wpa2_eapver — u32 0, u32 0xFFFFFFFF — `embassy/control.rs:393`
6. variable (set) — bsscfg:sup_wpa_tmo — u32 0, u32 2500 — `embassy/control.rs:394`
7. delay — 100 ms — `embassy/control.rs:396`
8. delay — 3 ms — `embassy/control.rs:417`
9. command (set) — SetWsecPmk = 268 — PassphraseInfo (`embassy/structs.rs:409-413`): len u16, flags u16, passphrase[64]; 68 bytes. flags = 1 for a text passphrase (8..64 bytes), 0 when passphrase_is_prehashed (then exactly 32 bytes). Note: length rules `embassy/control.rs:193-209` — `embassy/control.rs:406-419`
10. command (set) — SetInfra = 20 — u32 = 1 — `embassy/control.rs:432`
11. command (set) — SetAuth = 22 — u32 = 0 (AUTH_OPEN) — `embassy/control.rs:400-401`, `embassy/control.rs:433`
12. variable (set) — mfp — u32 = 1 (MFP_CAPABLE) for JoinAuth::Wpa2; 0 (MFP_NONE) for JoinAuth::Wpa. Note: plain 'mfp', no bsscfg prefix — `embassy/control.rs:400-401`, `embassy/control.rs:434`
13. command (set) — SetWpaAuth = 165 — u32 = 0x0080 (WPA2_PSK) for Wpa2; 0x0004 (WPA_PSK) for Wpa. Note: constants `embassy/consts.rs:743-744` — `embassy/control.rs:400-401`, `embassy/control.rs:435`
14. host-side event filter — enable SET_SSID (0), AUTH (3), PSK_SUP (46) in the driver's own event mask — no bytes sent. Note: done before the join command so no event is missed (`embassy/control.rs:466-467`) — `embassy/control.rs:464`
15. command (set) — SetSsid = 26 — SsidInfo (`embassy/structs.rs:400-403`): len u32, ssid[32]; 36 bytes. Note: interface 0; this starts the join — `embassy/control.rs:438-442`, `embassy/control.rs:469`
16. event wait — PSK_SUP (46) status 6 — join() returns Ok. Note: status 6 is named UNSOLICITED in embassy's shared status enum; for PSK_SUP c-driver and whd name value 6 'KEYED' (`c-driver/cyw43_ll.h:88`) — `embassy/control.rs:489`

Succeeds when: PSK_SUP event with status 6 (`embassy/control.rs:489`). SET_SSID status 0 alone is not treated as success for a secured join (`embassy/control.rs:480` requires secure_network == false).

Fails when:

- SET_SSID status 3 -> NetworkNotFound; other non-zero SET_SSID status -> JoinFailure(status) (`embassy/control.rs:481-484`).
- PSK_SUP status 4 with reason 0 is ignored ('waiting for M1') (`embassy/control.rs:485-487`).
- Any other PSK_SUP (including status 4 with reason 15 = handshake timeout) -> AuthenticationFailure (`embassy/control.rs:491-493`; test at `embassy/control.rs:1052-1057`).
- AUTH (3) status 1 (FAIL) -> AuthenticationFailure (`embassy/control.rs:491`).
- No timeout inside join(). `embassy/control.rs:474-496`
- embassy does not act on the command status: the runner only logs a warning when the CDC status is non-zero ('TODO: propagate error instead', `embassy/runner.rs:1174-1176`), so a rejected command does not stop the sequence.
- Runner link state for secured networks needs JOIN status 0 and PSK_SUP status 6 with flags 0 and reason 0 while auth_ok (`embassy/runner.rs:1268-1285`, `embassy/runner.rs:1298`); PSK_SUP reason 14 ignored (`embassy/runner.rs:1287`).

### linux

1. variable (set) — wpaie — RSN element from the request; result ignored — `linux/brcmfmac/cfg80211.c:2449-2466`
2. variable (set) — vndr_ie — vendor elements for association requests: brcmf_vif_set_mgmt_ie(BRCMF_VNDR_IE_ASSOCREQ_FLAG, sme->ie) sets vndr_ie when its add/delete buffer is not empty; an error is only logged — `linux/brcmfmac/cfg80211.c:2468-2473`, `linux/brcmfmac/cfg80211.c:5068-5073`
3. variable (set) — wpa_auth — u32 = 0x00C0 (WPA2_AUTH_PSK | WPA2_AUTH_UNSPECIFIED) for WPA version 2; 0x0006 for version 1. Note: constants `linux/include/brcmu_wifi.h:219-226` — `linux/brcmfmac/cfg80211.c:1966-1981`
4. variable (set) — auth — u32 as requested (0 open system, 2 automatic by default). Note: on devices with the AUTO_AUTH quirk an 'automatic' request is first rewritten to open system (`linux/brcmfmac/cfg80211.c:2355-2364`, `linux/brcmfmac/cfg80211.c:2496`) — `linux/brcmfmac/cfg80211.c:2005-2020`
5. variable (set) — wsec — u32 = cipher bits (CCMP -> AES, TKIP -> TKIP) — `linux/brcmfmac/cfg80211.c:2046-2094`
6. variable (get) — wpa_auth — read back to choose the key-management branch — `linux/brcmfmac/cfg80211.c:2134-2139`
7. variable (set), MFP feature + RSN element present — mfp — u32 = 2 if the element's capabilities have MFP-required, 1 if MFP-capable, else 0; result ignored — `linux/brcmfmac/cfg80211.c:2242-2273`
8. variable (set) — wpa_auth — u32 = 0x0080 for AKM PSK (PSK-SHA256, FT-PSK, 802.1X variants have their own values) — `linux/brcmfmac/cfg80211.c:2165-2204`, `linux/brcmfmac/cfg80211.c:2276-2281`
9. variable (set), FWSUP feature only — sup_wpa — u32 = 1 when the request carries a PSK (firmware supplicant), else 0. Note: without the FWSUP feature or without a PSK in the request, the 4-way handshake is left to user space and the next step is skipped — `linux/brcmfmac/cfg80211.c:2523-2546`
10. command (set), firmware-supplicant PSK only — BRCMF_C_SET_WSEC_PMK = 268 — brcmf_wsec_pmk_le (`linux/brcmfmac/fwil_types.h:584-588`): key_len u16 = 32, flags u16 = 0, key[128]; the 32-byte PMK, not the passphrase. Note: struct size by layout is 132 bytes (computed) — `linux/brcmfmac/cfg80211.c:2547-2549`, `linux/brcmfmac/cfg80211.c:1710-1743`, `linux/brcmfmac/fwil_types.h:65`
11. command (set) + variable (set) — BRCMF_C_SET_ASSOC_PREFER = 205, then join_pref — first, unless the request's bss_select behaviour is BAND_PREF: command BRCMF_C_SET_ASSOC_PREFER = 205 with u32 WLC_BAND_AUTO, result ignored (`linux/brcmfmac/cfg80211.c:2377-2378`; `linux/brcmfmac/fwil.h:74`). Then variable 'join_pref' with two brcmf_join_pref_params records. When user space gave no bss_select (behaviour 0, __NL80211_BSS_SELECT_ATTR_INVALID) the driver's default pair is sent instead: {RSSI_DELTA, len 2, rssi_gain BRCMF_JOIN_PREF_RSSI_BOOST, band 5G} + {RSSI, len 2, 0, 0} (`linux/brcmfmac/cfg80211.c:2381-2383`; `linux/brcmfmac/common.c:80-100`). Otherwise {BAND or RSSI_DELTA record, if selected} + {RSSI, len 2, 0, 0}, always sizeof two records (`linux/brcmfmac/cfg80211.c:2384-2406`). Errors only logged — `linux/brcmfmac/cfg80211.c:2366-2409`, `linux/brcmfmac/cfg80211.c:2620`, `linux/brcmfmac/common.c:80-100`
12. variable (set) — join — brcmf_ext_join_params_le: ssid (len u32 + 32), scan params (scan_type = -1, home_time = -1; active_time 320, passive_time 400, nprobes 16 when a channel is known, else all -1), assoc params (BSSID or ff x6, chanspec_num 1 + one chanspec when a channel is known). Note: brcmf_fil_bsscfg_* helpers send the plain variable name when the interface's bsscfg index is 0 and `bsscfg:<name>` + u32 index otherwise (`linux/brcmfmac/fwil.c:248-290`). Size (computed from the layouts at `linux/brcmfmac/fwil_types.h:482-490`, `linux/brcmfmac/fwil_types.h:515-534`, not stated in source): ssid_le 36 + scan_le 20 + 12 bytes of assoc_le up to chanspec_list = 68 bytes, or 70 with one chanspec (`linux/brcmfmac/cfg80211.c:2569-2572`) - the same 70-byte shape c-driver builds by hand (`c-driver/cyw43_ll.c:2300-2325`). scan_type is a u8, so -1 is 0xFF (`linux/brcmfmac/fwil_types.h:516`, `linux/brcmfmac/fwil_types.h:61`). — `linux/brcmfmac/cfg80211.c:2564-2623`, `linux/brcmfmac/cfg80211.c:80-82`
13. command (set), fallback — BRCMF_C_SET_SSID = 26 — only if the 'join' variable failed: struct brcmf_join_params. With no known channel only the 36-byte ssid_le part is sent (join_params_size = sizeof(ssid_le)), so the BSSID that was filled in is not sent; with a channel the whole struct is sent: ssid_le + assoc params (bssid, chanspec_num 1, one chanspec) (`linux/brcmfmac/cfg80211.c:2629-2647`) — `linux/brcmfmac/cfg80211.c:2629-2649`
14. event wait — SET_SSID status 0 and (firmware supplicant) PSK_SUP status 6 — with the firmware supplicant both are required, in either order; without it SET_SSID status 0 alone — `linux/brcmfmac/cfg80211.c:6244-6272`, `linux/brcmfmac/fweh.h:138`

Succeeds when: Firmware supplicant: SET_SSID status 0 and PSK_SUP status 6 (BRCMF_E_STATUS_FWSUP_COMPLETED) both seen (`linux/brcmfmac/cfg80211.c:6250-6270`). Host supplicant: SET_SSID status 0. Handler brcmf_notify_connect_status is registered for LINK, DEAUTH_IND, DEAUTH, DISASSOC_IND, ASSOC_IND, REASSOC_IND, SET_SSID and PSK_SUP (`linux/brcmfmac/cfg80211.c:6993-7026`).

Fails when:

- SET_SSID with non-zero status -> connect reported failed (WLAN_STATUS_AUTH_TIMEOUT) (`linux/brcmfmac/cfg80211.c:6303-6306`, `linux/brcmfmac/cfg80211.c:6705-6712`).
- LINK with status 3 (NO_NETWORKS) -> failed (`linux/brcmfmac/cfg80211.c:6297-6301`).
- PSK_SUP with status other than 6 -> failed (`linux/brcmfmac/cfg80211.c:6308-6313`).
- DEAUTH, DEAUTH_IND, DISASSOC_IND, or LINK without the link flag while connecting/connected -> connect failed / disconnected; driver then sends command 52 with no payload if it had been connected, and clears the PMK (command 268 with key_len 0) if the firmware supplicant was in use (`linux/brcmfmac/cfg80211.c:6274-6289`, `linux/brcmfmac/cfg80211.c:6812-6835`, `linux/brcmfmac/cfg80211.c:1745-1781`). When already connected, such an event for a different BSSID is ignored (`linux/brcmfmac/cfg80211.c:6819-6822`).
- Any configuration command failing returns the error from connect() (`linux/brcmfmac/cfg80211.c:2490-2517`).
- No driver-side join timeout in this function; cfg80211/user space owns it. `linux/brcmfmac/cfg80211.c:2449-2649`
- Order of tests in the handler: link-up, then link-down, then no-network (`linux/brcmfmac/cfg80211.c:6796-6840`), so an event that satisfies an earlier test never reaches a later one.

### whd

1. argument check — key length — 8..64 for WPA/WPA2 PSK types, at most 128 for SAE types; else WHD_INVALID_KEY. WEP types rejected — `whd/src/whd_wifi_api.c:1734-1751`
2. host — clear join status word — `whd/src/whd_wifi_api.c:1755-1756`
3. variable (get) — mfp — current value read and kept (whd's comment: in older branches the mfp setting gets overwritten when wsec is set) — `whd/src/whd_wifi_api.c:1758-1763`
4. command (set) — WLC_SET_WSEC = 134 — u32 = auth_type & 0xFF (AES 0x04, TKIP 0x02, both 0x06). Note: security constants `whd/inc/whd_types.h:63-69`, `whd/inc/whd_types.h:303-319` — `whd/src/whd_wifi_api.c:1766`
5. variable (set) — roam_off — u32 = 0 — `whd/src/whd_wifi_api.c:1785-1786`
6. variable (set) — bsscfg:sup_wpa — u32 index, u32 1; result ignored. Note: chip 43022 only: bsscfg:wpa_auth, bsscfg:wsec and a wake-on-wireless setting are sent before this (`whd/src/whd_wifi_api.c:1791-1815`) — `whd/src/whd_wifi_api.c:1817-1824`
7. variable (set) — bsscfg:sup_wpa2_eapver — u32 index, u32 0xFFFFFFFF; result ignored — `whd/src/whd_wifi_api.c:1826-1831`
8. variable (set) — bsscfg:sup_wpa_tmo — u32 index, u32 3000; 'unsupported' result tolerated — `whd/src/whd_wifi_api.c:1850-1852`, `whd/src/whd_wifi_api.c:716-738`, `whd/src/whd_wifi_api.c:79`
9. delay — 1 ms — `whd/src/whd_wifi_api.c:767-768`
10. command (set) — WLC_SET_WSEC_PMK = 268 — wsec_pmk_t (`whd/src/include/whd_wlioctl.h:786-791`): key_len u16, flags u16 = 1 (WSEC_PASSPHRASE) or 0 when the PMK join option is set, key[65]; zeroed first. Note: struct size by layout is 70 bytes (computed, not stated in source) — `whd/src/whd_wifi_api.c:740-773`, `whd/src/whd_wifi_api.c:1853`
11. command (set) — WLC_SET_INFRA = 20 — u32 = 1 — `whd/src/whd_wifi_api.c:1910`
12. command (set) — WLC_SET_AUTH = 22 — u32 = 0 — `whd/src/whd_wifi_api.c:1912-1921`
13. variable (set) — mfp — u32 = 1 (WL_MFP_CAPABLE) when the type has the WPA2 bit; otherwise the value read earlier; skipped when is_mfp_auto; result ignored. Note: enum `whd/inc/whd_types.h:440-442` — `whd/src/whd_wifi_api.c:1928-1947`
14. command (set) — WLC_SET_WPA_AUTH = 165 — u32: WPA2 PSK types 0x0080; WPA PSK types 0x0004; WPA2_AES_PSK_SHA256 uses WPA2_AUTH_PSK_SHA256. Note: constants `whd/src/include/whd_wlioctl.h:827`, `whd/src/include/whd_wlioctl.h:831` — `whd/src/whd_wifi_api.c:1982-1997`, `whd/src/whd_wifi_api.c:2049-2050`
15. host — register join handler for SET_SSID (0), LINK (16), AUTH (3), DEAUTH_IND (6), DISASSOC_IND (12), PSK_SUP (46), CSA_COMPLETE_IND (80), REASSOC (9), PROBRESP_MSG (71) — Note: event numbers from `whd/inc/whd_events.h:37-53` and `whd/src/include/whd_events_int.h:107`, `whd/src/include/whd_events_int.h:115`. REASSOC status 0 sets LINK_READY|SSID_SET (`whd/src/whd_wifi_api.c:1464-1471`) — `whd/src/whd_wifi_api.c:156-160`, `whd/src/whd_wifi_api.c:2063-2076`
16. variable (set), side effect of handler registration — bsscfg:event_msgs (or bsscfg:event_msgs_ext when any registered event number exceeds 127) — u32 bsscfg index, then a 16-byte bit mask (WL_EVENTING_MASK_LEN, `whd/src/include/whd_wlioctl.h:1932`) holding the union of every currently registered handler's events; the _ext form carries version/command/length header plus a mask sized to the highest event. Note: whd rewrites the firmware event mask each time a handler is registered; de-registering only edits the host table and sends nothing (`whd/src/whd_events.c:597-626`) — `whd/src/whd_events.c:255-325`, `whd/src/whd_events.c:348-425`
17. command (set) — WLC_SET_SSID = 26 — wlc_ssid_t: SSID_len u32, SSID[32]; 36 bytes. Note: whd_wifi_join. whd_wifi_join_specific instead sends the 'join' variable (wl_extjoin_params_t with BSSID, scan_type 0, times -1, optional single chanspec), falls back to SET_SSID with wl_join_params_t when the variable is unsupported, and uses WLC_REASSOC when already connected to the same SSID (`whd/src/whd_wifi_api.c:2320-2398`) — `whd/src/whd_wifi_api.c:2478-2483`
18. event wait — PROBRESP_MSG, AUTH status 0, LINK flags&1, SET_SSID status 0, PSK_SUP wire status 6 — status word reaches the success value. Note: whd adds 256 to the status and reason of PSK_SUP events before handlers see them (`whd/src/whd_cdc_bdc.c:866-871`, `whd/src/include/whd_events_int.h:197`), so WLC_SUP_KEYED = 6+256 in the source corresponds to wire status 6. — `whd/src/whd_wifi_api.c:2114-2174`, `whd/src/whd_wifi_api.c:2205-2206`

Succeeds when: whd_wifi_check_join_status returns WHD_SUCCESS only when the status word is exactly PROBE_RESPONSE|AUTHENTICATED|LINK_READY|SSID_SET|SECURITY_COMPLETE (`whd/src/whd_wifi_api.c:2205-2206`). Bits are set by: PROBRESP_MSG (any) -> PROBE_RESPONSE (`whd/src/whd_wifi_api.c:1473-1475`); AUTH status 0 -> AUTHENTICATED (`whd/src/whd_wifi_api.c:1439-1443`); LINK with flags bit 0 -> LINK_READY (`whd/src/whd_wifi_api.c:1422-1426`); SET_SSID status 0 -> SSID_SET (`whd/src/whd_wifi_api.c:1405-1410`); PSK_SUP wire status 6 while LINK_READY -> SECURITY_COMPLETE (`whd/src/whd_wifi_api.c:1359-1368`); for open networks SECURITY_COMPLETE is pre-set (`whd/src/whd_wifi_api.c:1975-1980`).

Fails when:

- PSK_SUP events are ignored until LINK_READY is set (`whd/src/whd_wifi_api.c:1360-1361`).
- PSK_SUP wire status 4 with reason 15 -> WHD_EAPOL_KEY_PACKET_M1_TIMEOUT; status 8 reason 15 -> M3 timeout (a sign, per whd's comment, that the passphrase might be wrong); status 10 reason 15 -> G1 timeout; any other non-6 status -> WHD_EAPOL_KEY_FAILURE; each ends the attempt (`whd/src/whd_wifi_api.c:1369-1401`, `whd/src/whd_wifi_api.c:2190-2203`).
- SET_SSID status 3 sets NO_NETWORKS; the wait ends with WHD_NETWORK_NOT_FOUND only when that is the sole bit set (`whd/src/whd_wifi_api.c:1412-1415`, `whd/src/whd_wifi_api.c:2187-2188`, `whd/src/whd_wifi_api.c:2148-2151`).
- SET_SSID any other non-zero status ends the attempt (`whd/src/whd_wifi_api.c:1416-1419`).
- AUTH status 6 (unsolicited) ignored; any other non-zero AUTH status ends the attempt (`whd/src/whd_wifi_api.c:1444-1452`).
- DEAUTH_IND / DISASSOC_IND clear AUTHENTICATED and LINK_READY (`whd/src/whd_wifi_api.c:1433-1437`).
- Wait loop: 1000 ms semaphore slices, re-evaluating the status word each time (`whd/src/whd_wifi_api.c:2134-2160`). It ends at once on WHD_SUCCESS or WHD_NETWORK_NOT_FOUND. It ends after 3000 ms (DEFAULT_JOIN_RESPONSE_TIMEOUT) only while whd_wifi_check_join_status returns WHD_INVALID_JOIN_STATUS, which is the default case for a status word that has no PROBE_RESPONSE bit and is not one of the listed patterns (`whd/src/whd_wifi_api.c:2221-2229`) - for example NO_NETWORKS together with the pre-set SECURITY_COMPLETE of an open join, or AUTHENTICATED without a probe response. A status word of exactly 0 (nothing seen yet), or exactly SECURITY_COMPLETE, returns WHD_NOT_AUTHENTICATED (`whd/src/whd_wifi_api.c:2208-2210`) and, like every other in-progress result, runs to the overall timeout: the configured wifi_join_timeout or 13000 ms (`whd/src/whd_wifi_api.c:76-78`, `whd/src/whd_wifi_api.c:2123-2127`, `whd/src/whd_wifi_api.c:2156-2159`).
- On any non-success result the driver calls whd_wifi_leave (command 52) (`whd/src/whd_wifi_api.c:2167-2171`).
- Command errors abort the sequence through CHECK_RETURN, except the sup_wpa / sup_wpa2_eapver / mfp sets whose results are ignored (`whd/src/whd_wifi_api.c:1824`, `whd/src/whd_wifi_api.c:1831`, `whd/src/whd_wifi_api.c:1942-1946`).

### c-driver

1. variable (set) — ampdu_ba_wsize — u32 = 8. Note: station interface — `c-driver/cyw43_ll.c:2212`
2. command (set) — WLC_SET_WSEC = 134 — u32 = auth_type & 0xff: WPA2_AES 0x04, WPA2_MIXED 0x06, WPA_TKIP 0x02. Note: auth_type constants `c-driver/cyw43_ll.h:169-181` — `c-driver/cyw43_ll.c:2236`
3. variable (set) — bsscfg:sup_wpa — u32 0, u32 1 — `c-driver/cyw43_ll.c:2240`
4. variable (set) — bsscfg:sup_wpa2_eapver — u32 0, u32 0xFFFFFFFF — `c-driver/cyw43_ll.c:2244`
5. variable (set) — bsscfg:sup_wpa_tmo — u32 0, u32 5000 — `c-driver/cyw43_ll.c:2248`
6. delay — 2 ms — `c-driver/cyw43_ll.c:2255`
7. command (set) — WLC_SET_WSEC_PMK = 268 — 68 bytes: key_len u16, flags u16 = 1, key bytes. Note: the 130-byte stack buffer is not cleared before this write, so bytes after the key are whatever was there (`c-driver/cyw43_ll.c:2210`, `c-driver/cyw43_ll.c:2252-2254`) — `c-driver/cyw43_ll.c:2250-2259`
8. command (set) — WLC_SET_INFRA = 20 — u32 = 1 — `c-driver/cyw43_ll.c:2271`
9. command (set) — WLC_SET_AUTH = 22 — u32 = 0 — `c-driver/cyw43_ll.c:2275`
10. variable (set) — mfp — u32 = 1 (MFP_CAPABLE) when wpa_auth is WPA2 (0x80); 0 for WPA-TKIP — `c-driver/cyw43_ll.c:2276`
11. command (set) — WLC_SET_WPA_AUTH = 165 — u32 = 0x0080 for WPA2_AES / WPA2_MIXED; 0x0004 for WPA_TKIP — `c-driver/cyw43_ll.c:2217-2220`, `c-driver/cyw43_ll.c:2280`
12. command (set) or variable (set) — WLC_SET_SSID = 26, or 'join' when a BSSID is given — as in the open join — `c-driver/cyw43_ll.c:2296-2330`
13. event wait — AUTH (3) status 0, LINK (16) status 0 flags&1, PSK_SUP (46) status 6 — state reaches 0x0e01 — `c-driver/cyw43_ctrl.c:366-372`, `c-driver/cyw43_ctrl.c:389-394`, `c-driver/cyw43_ctrl.c:403-405`, `c-driver/cyw43_ctrl.c:422-426`

Succeeds when: Join completes when the state word equals ACTIVE|AUTH|LINK|KEYED = 0x0e01 (`c-driver/cyw43_ctrl.c:32-40`, `c-driver/cyw43_ctrl.c:422-426`): AUTH (3) status 0 sets AUTH (`c-driver/cyw43_ctrl.c:366-372`); LINK (16) status 0 with flags bit 0 on the station interface sets LINK (`c-driver/cyw43_ctrl.c:389-394`); PSK_SUP (46) status 6 sets KEYED (`c-driver/cyw43_ctrl.c:403-405`), and for open networks KEYED is pre-set (`c-driver/cyw43_ctrl.c:661-664`).

Fails when:

- Before any command: -EPERM if the station interface is not active (`c-driver/cyw43_ctrl.c:643-646`); -EINVAL for an auth_type outside the six handled values (`c-driver/cyw43_ll.c:2214-2226`) or a key longer than 64 bytes (128 for pure WPA3) (`c-driver/cyw43_ll.c:2228-2233`). ampdu_ba_wsize has already been sent when -EINVAL is returned (`c-driver/cyw43_ll.c:2212`).
- PSK_SUP status 4, 8 or 10 with reason 15 (timeout waiting for M1 / M3 / G1) -> driver re-sends SET_SSID with the stored SSID (`c-driver/cyw43_ctrl.c:406-410`, `c-driver/cyw43_ctrl.c:228-232`; `c-driver/cyw43_ll.c:2340-2343`).
- Any other PSK_SUP status -> BADAUTH (`c-driver/cyw43_ctrl.c:411-415`).
- SET_SSID (0) status 3 with reason 0 -> state NONET (CYW43_LINK_NONET); any other non-zero SET_SSID status -> FAIL (`c-driver/cyw43_ctrl.c:355-365`).
- AUTH status 2 (timeout), 5 (no ack), 6 (unsolicited) are ignored; any other non-zero AUTH status -> BADAUTH (`c-driver/cyw43_ctrl.c:373-382`).
- DEAUTH_IND (6) status 0 reason 2 -> driver schedules command 52 (disassoc) and clears the state (`c-driver/cyw43_ctrl.c:383-388`, `c-driver/cyw43_ctrl.c:216-221`).
- PRUNE (23) status 0 reason 8 (RSN mismatch) -> driver sets WPA_AUTH (165) = 0x0004 and re-sends SET_SSID (`c-driver/cyw43_ctrl.c:348-354`, `c-driver/cyw43_ctrl.c:223-232`; `c-driver/cyw43_ll.c:2335-2343`).
- ICV_ERROR (49) -> re-send SET_SSID (`c-driver/cyw43_ctrl.c:416-420`).
- DISASSOC (11) on the station interface -> IP-stack link-down callback; and only if the state kind is still ACTIVE the state word is reset to plain ACTIVE (0x0001), dropping the AUTH/LINK/KEYED flags so the join has to collect them again (`c-driver/cyw43_ctrl.c:332-337`).
- The join call returns immediately; there is no timeout in the driver, the caller polls cyw43_wifi_link_status (`c-driver/cyw43_ctrl.c:619-636`).
- Most set helpers in cyw43_ll.c are void and discard the command result (`c-driver/cyw43_ll.c:1538-1562`, `c-driver/cyw43_ll.c:1956-1960`); the only failure surfaced is a 500 ms response timeout inside cyw43_do_ioctl, which returns -ETIMEDOUT to callers that check it (`c-driver/cyw43_ll.c:1294-1325`, `c-driver/cyw43_config.h:92`).

### Differences

Differences: embassy, whd and c-driver hand the firmware the passphrase (command 268, flags 1); linux hands it a 32-byte PMK with flags 0, and only when its firmware-supplicant feature is in use. `embassy/control.rs:406-419`, `whd/src/whd_wifi_api.c:740-773`, `c-driver/cyw43_ll.c:2250-2259`, `linux/brcmfmac/cfg80211.c:2547-2549`

| Aspect | embassy | linux | whd | c-driver | Citations |
|---|---|---|---|---|---|
| Key write (command 268) | PassphraseInfo, 68 bytes: flags 1 for a text passphrase, 0 for a pre-hashed 32-byte key | brcmf_wsec_pmk_le: key_len 32, flags 0, the PMK; struct 132 bytes (computed); firmware supplicant with a PSK only | wsec_pmk_t: flags 1, or 0 with the PMK join option; struct 70 bytes (computed); zeroed first | 68 bytes, flags 1; buffer not cleared before the write | `embassy/control.rs:406-419`, `linux/brcmfmac/cfg80211.c:2547-2549`, `linux/brcmfmac/cfg80211.c:1710-1743`, `whd/src/whd_wifi_api.c:740-773`, `c-driver/cyw43_ll.c:2250-2259` |
| Delay before the key write | 100 ms, then 3 ms | none found (unverified) | 1 ms | 2 ms | `embassy/control.rs:396`, `embassy/control.rs:417`, `whd/src/whd_wifi_api.c:767-768`, `c-driver/cyw43_ll.c:2255` |
| sup_wpa | 1 | 1 when the request carries a PSK, else 0; FWSUP feature only | 1, result ignored | 1 | `embassy/control.rs:392`, `linux/brcmfmac/cfg80211.c:2523-2546`, `whd/src/whd_wifi_api.c:1817-1824`, `c-driver/cyw43_ll.c:2240` |
| sup_wpa2_eapver | 0xFFFFFFFF | not sent | 0xFFFFFFFF, result ignored | 0xFFFFFFFF | `embassy/control.rs:393`, `linux/brcmfmac/cfg80211.c:2449-2649`, `whd/src/whd_wifi_api.c:1826-1831`, `c-driver/cyw43_ll.c:2244` |
| sup_wpa_tmo | 2500 | not sent | 3000, "unsupported" tolerated | 5000 | `embassy/control.rs:394`, `linux/brcmfmac/cfg80211.c:2449-2649`, `whd/src/whd_wifi_api.c:1850-1852`, `c-driver/cyw43_ll.c:2248` |
| wsec | command 134: AES 0x04, optional TKIP 0x02 OR-ed | variable `wsec`: cipher bits from the request | command 134: auth_type AND 0xFF | command 134: auth_type AND 0xff (0x04, 0x06, 0x02) | `embassy/control.rs:383-390`, `linux/brcmfmac/cfg80211.c:2046-2094`, `whd/src/whd_wifi_api.c:1766`, `c-driver/cyw43_ll.c:2236` |
| wpa_auth | command 165: 0x0080 (WPA2), 0x0004 (WPA) | variable written twice: 0x00C0 (0x0006 for WPA version 1), then 0x0080 for AKM PSK | command 165: 0x0080, 0x0004, or the PSK-SHA256 value | command 165: 0x0080, or 0x0004 for WPA_TKIP | `embassy/control.rs:435`, `linux/brcmfmac/cfg80211.c:1966-1981`, `linux/brcmfmac/cfg80211.c:2165-2204`, `whd/src/whd_wifi_api.c:1982-1997`, `c-driver/cyw43_ll.c:2217-2220` |
| auth | command 22 = 0 | variable `auth` as requested: 0 open system, 2 automatic by default | command 22 = 0 | command 22 = 0 | `embassy/control.rs:433`, `linux/brcmfmac/cfg80211.c:2005-2020`, `whd/src/whd_wifi_api.c:1912-1921`, `c-driver/cyw43_ll.c:2275` |
| mfp | 1 for WPA2, 0 for WPA; not read first | from the RSN element supplied by user space: 2, 1 or 0; MFP feature only | read before WLC_SET_WSEC; then 1 when the type has the WPA2 bit, else the value read | 1 for WPA2, 0 for WPA-TKIP | `embassy/control.rs:434`, `linux/brcmfmac/cfg80211.c:2242-2273`, `whd/src/whd_wifi_api.c:1758-1763`, `whd/src/whd_wifi_api.c:1928-1947`, `c-driver/cyw43_ll.c:2276` |
| roam_off | not sent | not sent in the connect path; set outside it | 0 | not sent | `embassy/control.rs:369-469`, `linux/brcmfmac/cfg80211.c:2449-2649`, `linux/brcmfmac/cfg80211.c:7131`, `whd/src/whd_wifi_api.c:1785-1786`, `c-driver/cyw43_ll.c:2207-2333` |
| Key length check | 8..64 text, exactly 32 pre-hashed | not applicable (PMK) | 8..64 | maximum 64 only | `embassy/control.rs:193-209`, `whd/src/whd_wifi_api.c:1734-1751`, `c-driver/cyw43_ll.c:2229-2233` |
| Success test | PSK_SUP status 6; SET_SSID status 0 alone is not enough | firmware supplicant: SET_SSID status 0 and PSK_SUP status 6, either order; host supplicant: SET_SSID status 0 | status word with PROBE_RESPONSE, AUTHENTICATED, LINK_READY, SSID_SET and SECURITY_COMPLETE (PSK_SUP wire status 6 after LINK) | AUTH + LINK + PSK_SUP status 6: state 0x0e01 | `embassy/control.rs:489`, `embassy/control.rs:480`, `linux/brcmfmac/cfg80211.c:6244-6272`, `whd/src/whd_wifi_api.c:2205-2206`, `whd/src/whd_wifi_api.c:1359-1368`, `c-driver/cyw43_ctrl.c:403-405`, `c-driver/cyw43_ctrl.c:422-426` |
| PSK_SUP status 4 / 8 / 10 with reason 15 (M1 / M3 / G1 timeout) | one AuthenticationFailure; status 4 with reason 0 is ignored | any status other than 6: connect failed | distinct M1 / M3 / G1 timeout error codes; attempt ends | driver re-sends SET_SSID with the stored SSID | `embassy/control.rs:485-493`, `linux/brcmfmac/cfg80211.c:6308-6313`, `whd/src/whd_wifi_api.c:1369-1401`, `c-driver/cyw43_ctrl.c:406-410` |
| PRUNE (23) reason 8 | not handled in join | no handler found (unverified) | not handled in the join path | sets WPA_AUTH (165) = 0x0004 and re-sends SET_SSID | `embassy/control.rs:474-496`, `whd/src/whd_wifi_api.c:2063-2076`, `c-driver/cyw43_ctrl.c:348-354` |

## Join WPA3

### embassy

1. command (set), conditional — Disassoc = 52 — empty. Note: only when an earlier join was started and not completed/left — `embassy/control.rs:369-371`, `embassy/control.rs:841`
2. variable (set) — ampdu_ba_wsize — u32 = 8 — `embassy/control.rs:374`
3. command (set) — SetWsec = 134 — u32 = cipher bits: AES 0x04 (default), TKIP 0x02 (optional), OR-ed. Note: constants `embassy/consts.rs:732-733` — `embassy/control.rs:383-390`
4. variable (set) — bsscfg:sup_wpa — u32 0, u32 1 — `embassy/control.rs:392`
5. variable (set) — bsscfg:sup_wpa2_eapver — u32 0, u32 0xFFFFFFFF — `embassy/control.rs:393`
6. variable (set) — bsscfg:sup_wpa_tmo — u32 0, u32 2500 — `embassy/control.rs:394`
7. delay — 100 ms — `embassy/control.rs:396`
8. delay + command (set), mixed only — SetWsecPmk = 268 — JoinAuth::Wpa2Wpa3 only: 3 ms delay, then PassphraseInfo len u16, flags u16 = 1, passphrase[64]; 68 bytes. Skipped for JoinAuth::Wpa3. Note: (wpa12, wpa3) = (false, true) for Wpa3 and (true, true) for Wpa2Wpa3 — `embassy/control.rs:398-420`
9. delay — 3 ms — `embassy/control.rs:428`
10. variable (set) — sae_password — SaePassphraseInfo (`embassy/structs.rs:419-422`): len u16, passphrase[128]; 130 bytes. Note: pre-hashed passphrases are rejected for WPA3 before any command (`embassy/control.rs:198-199`) — `embassy/control.rs:422-430`
11. command (set) — SetInfra = 20 — u32 = 1 — `embassy/control.rs:432`
12. command (set) — SetAuth = 22 — u32 = 3 (AUTH_SAE) for both Wpa3 and Wpa2Wpa3. Note: `embassy/consts.rs:736` — `embassy/control.rs:402-403`, `embassy/control.rs:433`
13. variable (set) — mfp — u32 = 2 (MFP_REQUIRED) for Wpa3; 1 (MFP_CAPABLE) for Wpa2Wpa3 — `embassy/control.rs:402-403`, `embassy/control.rs:434`
14. command (set) — SetWpaAuth = 165 — u32 = 0x40000 (WPA3_SAE_PSK) for both. Note: `embassy/consts.rs:745` — `embassy/control.rs:402-403`, `embassy/control.rs:435`
15. host-side event filter — enable SET_SSID (0), AUTH (3), PSK_SUP (46) in the driver's own event mask — no bytes sent. Note: done before the join command so no event is missed (`embassy/control.rs:466-467`) — `embassy/control.rs:464`
16. command (set) — SetSsid = 26 — SsidInfo (`embassy/structs.rs:400-403`): len u32, ssid[32]; 36 bytes. Note: interface 0; this starts the join — `embassy/control.rs:438-442`, `embassy/control.rs:469`
17. event wait — PSK_SUP (46) status 6 — join() returns Ok — `embassy/control.rs:489`

Succeeds when: PSK_SUP event with status 6 (`embassy/control.rs:489`).

Fails when:

- Same event handling as the WPA2 join: SET_SSID status 3 / other non-zero, PSK_SUP other than (4, reason 0) and 6, AUTH status 1 (`embassy/control.rs:481-493`).
- Runner also treats AUTH status 1 with reason 16 and auth_type 3 as link down ('specific for WPA3 networks') (`embassy/runner.rs:1246-1258`).
- No timeout inside join(). `embassy/control.rs:474-496`
- embassy does not act on the command status: the runner only logs a warning when the CDC status is non-zero ('TODO: propagate error instead', `embassy/runner.rs:1174-1176`), so a rejected command does not stop the sequence.

### linux

1. variable (set) — wpaie — RSN element from the request; result ignored — `linux/brcmfmac/cfg80211.c:2449-2466`
2. variable (set) — vndr_ie — vendor elements for association requests: brcmf_vif_set_mgmt_ie(BRCMF_VNDR_IE_ASSOCREQ_FLAG, sme->ie) sets vndr_ie when its add/delete buffer is not empty; an error is only logged — `linux/brcmfmac/cfg80211.c:2468-2473`, `linux/brcmfmac/cfg80211.c:5068-5073`
3. variable (set) — wpa_auth — u32 = 0x40000 for WPA version 3, and for version 2 with AKM SAE on Cypress/Infineon-vendor firmware; otherwise the version-2 value 0x00C0 — `linux/brcmfmac/cfg80211.c:1966-1981`
4. variable (set) — auth — u32 = 3 when the request's auth type is SAE. Note: on devices with the AUTO_AUTH quirk an 'automatic' request is first rewritten to open system (`linux/brcmfmac/cfg80211.c:2355-2364`, `linux/brcmfmac/cfg80211.c:2496`) — `linux/brcmfmac/cfg80211.c:2005-2020`
5. variable (set) — wsec — u32 = cipher bits — `linux/brcmfmac/cfg80211.c:2046-2094`
6. variable (get) — wpa_auth — read back — `linux/brcmfmac/cfg80211.c:2134-2139`
7. variable (set), MFP feature + RSN element present — mfp — u32 from the RSN capabilities (2 required, 1 capable, 0 none) — `linux/brcmfmac/cfg80211.c:2242-2273`
8. variable (set) — wpa_auth — u32 = 0x40000 for AKM SAE (FT-over-SAE adds the FT bit). Note: the SAE AKM branch is only reached when the read-back value has the SAE bit — `linux/brcmfmac/cfg80211.c:2205-2221`, `linux/brcmfmac/cfg80211.c:2276-2281`
9. variable (set), FWSUP feature — sup_wpa — u32 = 1 when an SAE password is supplied — `linux/brcmfmac/cfg80211.c:2216-2218`, `linux/brcmfmac/cfg80211.c:2523-2546`
10. variable (set), SAE feature — wpaie — empty ('clean up user-space RSNE') — `linux/brcmfmac/cfg80211.c:2550-2557`
11. variable (set) or command (set), vendor-specific — sae_password / BRCMF_C_SET_WSEC_PMK — Cypress/Infineon vendor module: variable 'sae_password' = key_len u16 + key[128] (`linux/brcmfmac/cyw/core.c:26-50`). Broadcom WCC vendor module: command 268 with key_len, flags = 1 (BRCMF_WSEC_PASSPHRASE), key (`linux/brcmfmac/wcc/core.c:16-21`). No vendor handler -> -EOPNOTSUPP (`linux/brcmfmac/fwvid.h:54-63`). Note: the Cypress path does not zero the struct before copying the password (`linux/brcmfmac/cyw/core.c:30-41`) — `linux/brcmfmac/cfg80211.c:2558`
12. command (set), if a PSK is also supplied — BRCMF_C_SET_WSEC_PMK = 268 — key_len 32, flags 0, PMK (the WPA2 half of a mixed network) — `linux/brcmfmac/cfg80211.c:2559-2561`
13. command (set) + variable (set) — BRCMF_C_SET_ASSOC_PREFER = 205, then join_pref — first, unless the request's bss_select behaviour is BAND_PREF: command BRCMF_C_SET_ASSOC_PREFER = 205 with u32 WLC_BAND_AUTO, result ignored (`linux/brcmfmac/cfg80211.c:2377-2378`; `linux/brcmfmac/fwil.h:74`). Then variable 'join_pref' with two brcmf_join_pref_params records. When user space gave no bss_select (behaviour 0, __NL80211_BSS_SELECT_ATTR_INVALID) the driver's default pair is sent instead: {RSSI_DELTA, len 2, rssi_gain BRCMF_JOIN_PREF_RSSI_BOOST, band 5G} + {RSSI, len 2, 0, 0} (`linux/brcmfmac/cfg80211.c:2381-2383`; `linux/brcmfmac/common.c:80-100`). Otherwise {BAND or RSSI_DELTA record, if selected} + {RSSI, len 2, 0, 0}, always sizeof two records (`linux/brcmfmac/cfg80211.c:2384-2406`). Errors only logged — `linux/brcmfmac/cfg80211.c:2366-2409`, `linux/brcmfmac/cfg80211.c:2620`, `linux/brcmfmac/common.c:80-100`
14. variable (set) — join — brcmf_ext_join_params_le: ssid (len u32 + 32), scan params (scan_type = -1, home_time = -1; active_time 320, passive_time 400, nprobes 16 when a channel is known, else all -1), assoc params (BSSID or ff x6, chanspec_num 1 + one chanspec when a channel is known). Note: brcmf_fil_bsscfg_* helpers send the plain variable name when the interface's bsscfg index is 0 and `bsscfg:<name>` + u32 index otherwise (`linux/brcmfmac/fwil.c:248-290`). Size (computed from the layouts at `linux/brcmfmac/fwil_types.h:482-490`, `linux/brcmfmac/fwil_types.h:515-534`, not stated in source): ssid_le 36 + scan_le 20 + 12 bytes of assoc_le up to chanspec_list = 68 bytes, or 70 with one chanspec (`linux/brcmfmac/cfg80211.c:2569-2572`) - the same 70-byte shape c-driver builds by hand (`c-driver/cyw43_ll.c:2300-2325`). scan_type is a u8, so -1 is 0xFF (`linux/brcmfmac/fwil_types.h:516`, `linux/brcmfmac/fwil_types.h:61`). — `linux/brcmfmac/cfg80211.c:2564-2623`, `linux/brcmfmac/cfg80211.c:80-82`
15. command (set), fallback — BRCMF_C_SET_SSID = 26 — only if the 'join' variable failed: struct brcmf_join_params. With no known channel only the 36-byte ssid_le part is sent (join_params_size = sizeof(ssid_le)), so the BSSID that was filled in is not sent; with a channel the whole struct is sent: ssid_le + assoc params (bssid, chanspec_num 1, one chanspec) (`linux/brcmfmac/cfg80211.c:2629-2647`) — `linux/brcmfmac/cfg80211.c:2629-2649`
16. event wait — SET_SSID status 0 and PSK_SUP status 6 — both required when the firmware supplicant handles SAE — `linux/brcmfmac/cfg80211.c:6244-6272`

Succeeds when: SET_SSID status 0 and PSK_SUP status 6 (`linux/brcmfmac/cfg80211.c:6250-6270`). Handler brcmf_notify_connect_status is registered for LINK, DEAUTH_IND, DEAUTH, DISASSOC_IND, ASSOC_IND, REASSOC_IND, SET_SSID and PSK_SUP (`linux/brcmfmac/cfg80211.c:6993-7026`).

Fails when:

- SET_SSID with non-zero status -> connect reported failed (WLAN_STATUS_AUTH_TIMEOUT) (`linux/brcmfmac/cfg80211.c:6303-6306`, `linux/brcmfmac/cfg80211.c:6705-6712`).
- LINK with status 3 (NO_NETWORKS) -> failed (`linux/brcmfmac/cfg80211.c:6297-6301`).
- PSK_SUP with status other than 6 -> failed (`linux/brcmfmac/cfg80211.c:6308-6313`).
- DEAUTH, DEAUTH_IND, DISASSOC_IND, or LINK without the link flag while connecting/connected -> connect failed / disconnected; driver then sends command 52 with no payload if it had been connected, and clears the PMK (command 268 with key_len 0) if the firmware supplicant was in use (`linux/brcmfmac/cfg80211.c:6274-6289`, `linux/brcmfmac/cfg80211.c:6812-6835`, `linux/brcmfmac/cfg80211.c:1745-1781`). When already connected, such an event for a different BSSID is ignored (`linux/brcmfmac/cfg80211.c:6819-6822`).
- Any configuration command failing returns the error from connect() (`linux/brcmfmac/cfg80211.c:2490-2517`).
- No driver-side join timeout in this function; cfg80211/user space owns it. `linux/brcmfmac/cfg80211.c:2449-2649`
- Order of tests in the handler: link-up, then link-down, then no-network (`linux/brcmfmac/cfg80211.c:6796-6840`), so an event that satisfies an earlier test never reaches a later one.

### whd

1. argument check — key length — 8..64 for WPA/WPA2 PSK types, at most 128 for SAE types; else WHD_INVALID_KEY. WEP types rejected. Note: For WPA3_WPA2_PSK the 128-byte limit here is not the effective one: whd_wifi_enable_sup_set_passphrase and whd_wifi_set_passphrase both reject a key outside 8..64 (`whd/src/whd_wifi_api.c:1113-1117`, `whd/src/whd_wifi_api.c:746-751`, `whd/src/whd_wifi_api.c:96-97`). whd_wifi_sae_password only requires 1..128 (`whd/src/whd_wifi_api.c:781`). — `whd/src/whd_wifi_api.c:1734-1751`
2. host — clear join status word — `whd/src/whd_wifi_api.c:1755-1756`
3. variable (get) — mfp — current value read and kept (whd's comment: in older branches the mfp setting gets overwritten when wsec is set) — `whd/src/whd_wifi_api.c:1758-1763`
4. command (set) — WLC_SET_WSEC = 134 — u32 = auth_type & 0xFF (AES 0x04, TKIP 0x02, both 0x06). Note: security constants `whd/inc/whd_types.h:63-69`, `whd/inc/whd_types.h:303-319` — `whd/src/whd_wifi_api.c:1766`
5. variable (set) — roam_off — u32 = 0 — `whd/src/whd_wifi_api.c:1785-1786`
6. variable (set) — bsscfg:sup_wpa — u32 index, u32 1; result ignored. Note: chip 43022 only: bsscfg:wpa_auth, bsscfg:wsec and a wake-on-wireless setting are sent before this (`whd/src/whd_wifi_api.c:1791-1815`) — `whd/src/whd_wifi_api.c:1817-1824`
7. variable (set) — bsscfg:sup_wpa2_eapver — u32 index, u32 0xFFFFFFFF; result ignored — `whd/src/whd_wifi_api.c:1826-1831`
8. variable (set) + command (set), mixed only — bsscfg:sup_wpa then WLC_SET_WSEC_PMK = 268 — WHD_SECURITY_WPA3_WPA2_PSK only: bsscfg:sup_wpa (index, 1) again, 1 ms delay, wsec_pmk_t with flags 1 (key length must be 8..64) — `whd/src/whd_wifi_api.c:1860-1863`, `whd/src/whd_wifi_api.c:1099-1134`
9. variable (set) — bsscfg:sup_wpa_tmo — u32 index, u32 3000; 'unsupported' tolerated — `whd/src/whd_wifi_api.c:1864-1866`
10. delay + variable (set) — sae_password — when the firmware-capability flag SAE is set: 1 ms delay, wsec_sae_password_t: password_len u16, password[128]; 130 bytes. Note: `whd/src/include/whd_wlioctl.h:793-798` — `whd/src/whd_wifi_api.c:1867-1870`, `whd/src/whd_wifi_api.c:775-803`
11. variable (set), alternative — roam_off — when the SAE capability flag is not set: u32 = 1 (roaming off; SAE is then done by a host supplicant) — `whd/src/whd_wifi_api.c:1871-1876`
12. command (set) — WLC_SET_INFRA = 20 — u32 = 1 — `whd/src/whd_wifi_api.c:1910`
13. command (set) — WLC_SET_AUTH = 22 — u32 = 3 (WL_AUTH_SAE). Note: `whd/src/include/whd_wlioctl.h:4276` — `whd/src/whd_wifi_api.c:1912-1921`
14. variable (set) — mfp — u32 = 2 (REQUIRED) for WPA3_SAE; 1 (CAPABLE) for WPA3_WPA2_PSK; skipped when is_mfp_auto; result ignored — `whd/src/whd_wifi_api.c:1928-1947`
15. command (set) — WLC_SET_WPA_AUTH = 165 — u32 = 0x40000 for both WPA3_SAE and WPA3_WPA2_PSK. Note: `whd/src/include/whd_wlioctl.h:844` — `whd/src/whd_wifi_api.c:1999-2002`, `whd/src/whd_wifi_api.c:2049-2050`
16. host — register join handler for SET_SSID (0), LINK (16), AUTH (3), DEAUTH_IND (6), DISASSOC_IND (12), PSK_SUP (46), CSA_COMPLETE_IND (80), REASSOC (9), PROBRESP_MSG (71) — Note: event numbers from `whd/inc/whd_events.h:37-53` and `whd/src/include/whd_events_int.h:107`, `whd/src/include/whd_events_int.h:115`. REASSOC status 0 sets LINK_READY|SSID_SET (`whd/src/whd_wifi_api.c:1464-1471`) — `whd/src/whd_wifi_api.c:156-160`, `whd/src/whd_wifi_api.c:2063-2076`
17. variable (set), side effect of handler registration — bsscfg:event_msgs (or bsscfg:event_msgs_ext when any registered event number exceeds 127) — u32 bsscfg index, then a 16-byte bit mask (WL_EVENTING_MASK_LEN, `whd/src/include/whd_wlioctl.h:1932`) holding the union of every currently registered handler's events; the _ext form carries version/command/length header plus a mask sized to the highest event. Note: whd rewrites the firmware event mask each time a handler is registered; de-registering only edits the host table and sends nothing (`whd/src/whd_events.c:597-626`) — `whd/src/whd_events.c:255-325`, `whd/src/whd_events.c:348-425`
18. command (set) — WLC_SET_SSID = 26 — wlc_ssid_t: SSID_len u32, SSID[32]; 36 bytes. Note: whd_wifi_join. whd_wifi_join_specific instead sends the 'join' variable (wl_extjoin_params_t with BSSID, scan_type 0, times -1, optional single chanspec), falls back to SET_SSID with wl_join_params_t when the variable is unsupported, and uses WLC_REASSOC when already connected to the same SSID (`whd/src/whd_wifi_api.c:2320-2398`) — `whd/src/whd_wifi_api.c:2478-2483`
19. event wait — PROBRESP_MSG, AUTH status 0, LINK flags&1, SET_SSID status 0, PSK_SUP wire status 6 — status word reaches the success value. Note: whd adds 256 to the status and reason of PSK_SUP events before handlers see them (`whd/src/whd_cdc_bdc.c:866-871`, `whd/src/include/whd_events_int.h:197`), so WLC_SUP_KEYED = 6+256 in the source corresponds to wire status 6. — `whd/src/whd_wifi_api.c:2114-2174`, `whd/src/whd_wifi_api.c:2205-2206`

Succeeds when: whd_wifi_check_join_status returns WHD_SUCCESS only when the status word is exactly PROBE_RESPONSE|AUTHENTICATED|LINK_READY|SSID_SET|SECURITY_COMPLETE (`whd/src/whd_wifi_api.c:2205-2206`). Bits are set by: PROBRESP_MSG (any) -> PROBE_RESPONSE (`whd/src/whd_wifi_api.c:1473-1475`); AUTH status 0 -> AUTHENTICATED (`whd/src/whd_wifi_api.c:1439-1443`); LINK with flags bit 0 -> LINK_READY (`whd/src/whd_wifi_api.c:1422-1426`); SET_SSID status 0 -> SSID_SET (`whd/src/whd_wifi_api.c:1405-1410`); PSK_SUP wire status 6 while LINK_READY -> SECURITY_COMPLETE (`whd/src/whd_wifi_api.c:1359-1368`); for open networks SECURITY_COMPLETE is pre-set (`whd/src/whd_wifi_api.c:1975-1980`).

Fails when:

- Same PSK_SUP classification as the WPA2 join (`whd/src/whd_wifi_api.c:1369-1401`).
- SET_SSID status 3 sets NO_NETWORKS; the wait ends with WHD_NETWORK_NOT_FOUND only when that is the sole bit set (`whd/src/whd_wifi_api.c:1412-1415`, `whd/src/whd_wifi_api.c:2187-2188`, `whd/src/whd_wifi_api.c:2148-2151`).
- SET_SSID any other non-zero status ends the attempt (`whd/src/whd_wifi_api.c:1416-1419`).
- AUTH status 6 (unsolicited) ignored; any other non-zero AUTH status ends the attempt (`whd/src/whd_wifi_api.c:1444-1452`).
- DEAUTH_IND / DISASSOC_IND clear AUTHENTICATED and LINK_READY (`whd/src/whd_wifi_api.c:1433-1437`).
- Wait loop: 1000 ms semaphore slices, re-evaluating the status word each time (`whd/src/whd_wifi_api.c:2134-2160`). It ends at once on WHD_SUCCESS or WHD_NETWORK_NOT_FOUND. It ends after 3000 ms (DEFAULT_JOIN_RESPONSE_TIMEOUT) only while whd_wifi_check_join_status returns WHD_INVALID_JOIN_STATUS, which is the default case for a status word that has no PROBE_RESPONSE bit and is not one of the listed patterns (`whd/src/whd_wifi_api.c:2221-2229`) - for example NO_NETWORKS together with the pre-set SECURITY_COMPLETE of an open join, or AUTHENTICATED without a probe response. A status word of exactly 0 (nothing seen yet), or exactly SECURITY_COMPLETE, returns WHD_NOT_AUTHENTICATED (`whd/src/whd_wifi_api.c:2208-2210`) and, like every other in-progress result, runs to the overall timeout: the configured wifi_join_timeout or 13000 ms (`whd/src/whd_wifi_api.c:76-78`, `whd/src/whd_wifi_api.c:2123-2127`, `whd/src/whd_wifi_api.c:2156-2159`).
- On any non-success result the driver calls whd_wifi_leave (command 52) (`whd/src/whd_wifi_api.c:2167-2171`).
- Command errors abort the sequence through CHECK_RETURN, except the sup_wpa / sup_wpa2_eapver / mfp sets whose results are ignored (`whd/src/whd_wifi_api.c:1824`, `whd/src/whd_wifi_api.c:1831`, `whd/src/whd_wifi_api.c:1942-1946`).

### c-driver

1. variable (set) — ampdu_ba_wsize — u32 = 8. Note: station interface — `c-driver/cyw43_ll.c:2212`
2. command (set) — WLC_SET_WSEC = 134 — u32 = 0x04 (auth_type & 0xff for both WPA3_SAE_AES_PSK and WPA3_WPA2_AES_PSK) — `c-driver/cyw43_ll.c:2236`
3. variable (set) — bsscfg:sup_wpa — u32 0, u32 1 — `c-driver/cyw43_ll.c:2240`
4. variable (set) — bsscfg:sup_wpa2_eapver — u32 0, u32 0xFFFFFFFF — `c-driver/cyw43_ll.c:2244`
5. variable (set) — bsscfg:sup_wpa_tmo — u32 0, u32 5000 — `c-driver/cyw43_ll.c:2248`
6. delay + command (set), mixed only — WLC_SET_WSEC_PMK = 268 — only for WPA3_WPA2_AES_PSK: 2 ms delay, then 68 bytes key_len u16, flags u16 = 1, key. Skipped for WPA3_SAE_AES_PSK — `c-driver/cyw43_ll.c:2250-2259`
7. delay — 2 ms — `c-driver/cyw43_ll.c:2265`
8. variable (set) — sae_password — 130 bytes: key_len u16, password[128] (buffer zeroed first) — `c-driver/cyw43_ll.c:2261-2267`
9. command (set) — WLC_SET_INFRA = 20 — u32 = 1 — `c-driver/cyw43_ll.c:2271`
10. command (set) — WLC_SET_AUTH = 22 — u32 = 3 (AUTH_TYPE_SAE) — `c-driver/cyw43_ll.c:2275`, `c-driver/cyw43_ll.c:264`
11. variable (set) — mfp — u32 = 1 (MFP_CAPABLE) for both pure WPA3 and mixed — `c-driver/cyw43_ll.c:2276`
12. command (set) — WLC_SET_WPA_AUTH = 165 — u32 = 0x40000 — `c-driver/cyw43_ll.c:2221-2222`, `c-driver/cyw43_ll.c:2280`
13. command (set) or variable (set) — WLC_SET_SSID = 26, or 'join' when a BSSID is given — as in the open join — `c-driver/cyw43_ll.c:2296-2330`
14. event wait — AUTH (3) status 0, LINK (16) status 0 flags&1, PSK_SUP (46) status 6 — state reaches 0x0e01 — `c-driver/cyw43_ctrl.c:366-372`, `c-driver/cyw43_ctrl.c:389-394`, `c-driver/cyw43_ctrl.c:403-405`, `c-driver/cyw43_ctrl.c:422-426`

Succeeds when: Join completes when the state word equals ACTIVE|AUTH|LINK|KEYED = 0x0e01 (`c-driver/cyw43_ctrl.c:32-40`, `c-driver/cyw43_ctrl.c:422-426`): AUTH (3) status 0 sets AUTH (`c-driver/cyw43_ctrl.c:366-372`); LINK (16) status 0 with flags bit 0 on the station interface sets LINK (`c-driver/cyw43_ctrl.c:389-394`); PSK_SUP (46) status 6 sets KEYED (`c-driver/cyw43_ctrl.c:403-405`), and for open networks KEYED is pre-set (`c-driver/cyw43_ctrl.c:661-664`).

Fails when:

- Before any command: -EPERM if the station interface is not active (`c-driver/cyw43_ctrl.c:643-646`); -EINVAL for an auth_type outside the six handled values (`c-driver/cyw43_ll.c:2214-2226`) or a key longer than 64 bytes (128 for pure WPA3) (`c-driver/cyw43_ll.c:2228-2233`). ampdu_ba_wsize has already been sent when -EINVAL is returned (`c-driver/cyw43_ll.c:2212`).
- PSK_SUP status 4, 8 or 10 with reason 15 -> re-send SET_SSID; any other non-6 PSK_SUP status -> BADAUTH (`c-driver/cyw43_ctrl.c:406-415`).
- SET_SSID (0) status 3 with reason 0 -> state NONET (CYW43_LINK_NONET); any other non-zero SET_SSID status -> FAIL (`c-driver/cyw43_ctrl.c:355-365`).
- AUTH status 2 (timeout), 5 (no ack), 6 (unsolicited) are ignored; any other non-zero AUTH status -> BADAUTH (`c-driver/cyw43_ctrl.c:373-382`).
- DEAUTH_IND (6) status 0 reason 2 -> driver schedules command 52 (disassoc) and clears the state (`c-driver/cyw43_ctrl.c:383-388`, `c-driver/cyw43_ctrl.c:216-221`).
- PRUNE (23) status 0 reason 8 (RSN mismatch) -> driver sets WPA_AUTH (165) = 0x0004 and re-sends SET_SSID (`c-driver/cyw43_ctrl.c:348-354`, `c-driver/cyw43_ctrl.c:223-232`; `c-driver/cyw43_ll.c:2335-2343`).
- ICV_ERROR (49) -> re-send SET_SSID (`c-driver/cyw43_ctrl.c:416-420`).
- DISASSOC (11) on the station interface -> IP-stack link-down callback; and only if the state kind is still ACTIVE the state word is reset to plain ACTIVE (0x0001), dropping the AUTH/LINK/KEYED flags so the join has to collect them again (`c-driver/cyw43_ctrl.c:332-337`).
- The join call returns immediately; there is no timeout in the driver, the caller polls cyw43_wifi_link_status (`c-driver/cyw43_ctrl.c:619-636`).
- Most set helpers in cyw43_ll.c are void and discard the command result (`c-driver/cyw43_ll.c:1538-1562`, `c-driver/cyw43_ll.c:1956-1960`); the only failure surfaced is a 500 ms response timeout inside cyw43_do_ioctl, which returns -ETIMEDOUT to callers that check it (`c-driver/cyw43_ll.c:1294-1325`, `c-driver/cyw43_config.h:92`).

### Differences

Differences: embassy, whd, c-driver and linux's Cypress/Infineon vendor module all deliver the SAE password with the variable `sae_password` (u16 length, then 128 bytes). `embassy/control.rs:422-430`, `whd/src/whd_wifi_api.c:775-803`, `c-driver/cyw43_ll.c:2261-2267`, `linux/brcmfmac/cyw/core.c:26-50` linux's Broadcom WCC vendor module uses command 268 with flags 1 instead. `linux/brcmfmac/wcc/core.c:16-21` The drivers disagree on the mfp value for pure WPA3: embassy and whd send 2, c-driver sends 1. `embassy/control.rs:402-403`, `whd/src/whd_wifi_api.c:1928-1947`, `c-driver/cyw43_ll.c:2276` linux's external (user-space) SAE path is not described here; the linux column covers firmware SAE offload only. `linux/brcmfmac/cfg80211.c:2550-2561`

| Aspect | embassy | linux | whd | c-driver | Citations |
|---|---|---|---|---|---|
| SAE password | variable `sae_password`, 130 bytes | Cypress/Infineon vendor: variable `sae_password`; WCC vendor: command 268 with flags 1; no vendor handler: -EOPNOTSUPP | variable `sae_password`, 130 bytes, only when the firmware-capability flag SAE is set | variable `sae_password`, 130 bytes | `embassy/control.rs:422-430`, `linux/brcmfmac/cfg80211.c:2558`, `linux/brcmfmac/cyw/core.c:26-50`, `linux/brcmfmac/wcc/core.c:16-21`, `linux/brcmfmac/fwvid.h:54-63`, `whd/src/whd_wifi_api.c:1867-1870`, `c-driver/cyw43_ll.c:2261-2267` |
| No SAE capability | not checked | vendor handler decides | variable `roam_off` = 1 instead of the password | not checked | `embassy/control.rs:369-469`, `linux/brcmfmac/cfg80211.c:2558`, `whd/src/whd_wifi_api.c:1871-1876`, `c-driver/cyw43_ll.c:2207-2333` |
| Mixed WPA2/WPA3: PMK write | command 268 passphrase (flags 1) before `sae_password` | command 268 with a 32-byte PMK, flags 0, after the SAE password, when user space supplies both | `bsscfg:sup_wpa` = 1 a second time, 1 ms, command 268 (flags 1), before `sae_password` | command 268 (flags 1) before `sae_password` | `embassy/control.rs:398-420`, `linux/brcmfmac/cfg80211.c:2559-2561`, `whd/src/whd_wifi_api.c:1860-1863`, `whd/src/whd_wifi_api.c:1099-1134`, `c-driver/cyw43_ll.c:2250-2259` |
| Delay before `sae_password` | 3 ms | none found (unverified) | 1 ms | 2 ms | `embassy/control.rs:428`, `whd/src/whd_wifi_api.c:1867-1870`, `c-driver/cyw43_ll.c:2265` |
| auth | command 22 = 3 | variable `auth` = 3 | command 22 = 3 | command 22 = 3 | `embassy/control.rs:433`, `linux/brcmfmac/cfg80211.c:2005-2020`, `whd/src/whd_wifi_api.c:1912-1921`, `c-driver/cyw43_ll.c:2275` |
| mfp, pure WPA3 | 2 | from the RSN capabilities | 2 | 1 | `embassy/control.rs:402-403`, `linux/brcmfmac/cfg80211.c:2242-2273`, `whd/src/whd_wifi_api.c:1928-1947`, `c-driver/cyw43_ll.c:2276` |
| mfp, mixed | 1 | from the RSN capabilities | 1 | 1 | `embassy/control.rs:402-403`, `linux/brcmfmac/cfg80211.c:2242-2273`, `whd/src/whd_wifi_api.c:1928-1947`, `c-driver/cyw43_ll.c:2276` |
| wpa_auth | command 165 = 0x40000 for both | variable = 0x40000 (FT-over-SAE adds the FT bit) | command 165 = 0x40000 for both | command 165 = 0x40000 | `embassy/control.rs:435`, `linux/brcmfmac/cfg80211.c:2205-2221`, `whd/src/whd_wifi_api.c:1999-2002`, `c-driver/cyw43_ll.c:2221-2222` |
| wsec | command 134: 0x04, optional TKIP 0x02 | variable `wsec`: cipher bits | command 134: auth_type AND 0xFF | command 134: 0x04 | `embassy/control.rs:383-390`, `linux/brcmfmac/cfg80211.c:2046-2094`, `whd/src/whd_wifi_api.c:1766`, `c-driver/cyw43_ll.c:2236` |
| sup_wpa_tmo | 2500 | not sent | 3000 | 5000 | `embassy/control.rs:394`, `linux/brcmfmac/cfg80211.c:2449-2649`, `whd/src/whd_wifi_api.c:1864-1866`, `c-driver/cyw43_ll.c:2248` |
| Password length rule | 8..64 bytes, as for WPA2; pre-hashed keys rejected for WPA3 | none found (unverified) | SAE password 1..128; the mixed type is held to 8..64 by the passphrase helpers | at most 128 for pure WPA3, 64 for mixed | `embassy/control.rs:198-202`, `embassy/consts.rs:170-171`, `whd/src/whd_wifi_api.c:781`, `whd/src/whd_wifi_api.c:1113-1117`, `c-driver/cyw43_ll.c:2229-2233` |
| `wpaie` before the password | not used | set to empty | not used | not used | `embassy/control.rs:369-469`, `linux/brcmfmac/cfg80211.c:2550-2557`, `whd/src/whd_wifi_api.c:1717-2080`, `c-driver/cyw43_ll.c:2207-2333` |
| Success test | PSK_SUP status 6 | SET_SSID status 0 and PSK_SUP status 6 | same status word as the WPA2 join | state 0x0e01 as in the WPA2 join | `embassy/control.rs:489`, `linux/brcmfmac/cfg80211.c:6244-6272`, `whd/src/whd_wifi_api.c:2205-2206`, `c-driver/cyw43_ctrl.c:422-426` |
| WPA3-specific link-down | runner: AUTH status 1 with reason 16 and auth_type 3 | none found (unverified) | none found (unverified) | none found (unverified) | `embassy/runner.rs:1246-1258` |

## Leave

### embassy

1. command (set) — Disassoc = 52 — empty payload. Note: interface 0; clears the started_join flag after the command completes — `embassy/control.rs:840-844`

Succeeds when: Command accepted (no status check). No event is waited for. `embassy/control.rs:840-844`

Fails when:

- embassy does not act on the command status: the runner only logs a warning when the CDC status is non-zero ('TODO: propagate error instead', `embassy/runner.rs:1174-1176`), so a rejected command does not stop the sequence.
- The network link state only changes when the runner later sees a link-down event (`embassy/runner.rs:1249-1258`).

### linux

1. host — clear connection state bits, report disconnect to cfg80211 — `linux/brcmfmac/cfg80211.c:2674-2678`
2. command (set) — BRCMF_C_DISASSOC = 52 — brcmf_scb_val_le (`linux/brcmfmac/fwil_types.h:602-605`): val u32 = 802.11 reason code, ea[6] = current BSSID; 12 bytes as sent: sizeof(struct brcmf_scb_val_le) with val u32 at 0, ea[6] at 4 and 2 bytes of tail padding (the struct is not packed; size computed from the layout at `linux/brcmfmac/fwil_types.h:602-605`, not stated in source). Note: scbval is a stack variable that is not zeroed; only ea and val are assigned, so the 2 padding bytes are whatever the stack held (`linux/brcmfmac/cfg80211.c:2666`, `linux/brcmfmac/cfg80211.c:2679-2682`) — `linux/brcmfmac/cfg80211.c:2679-2684`

Succeeds when: Command returns 0. `linux/brcmfmac/cfg80211.c:2679-2684`

Fails when:

- Interface not up -> -EIO (`linux/brcmfmac/cfg80211.c:2671-2672`).
- Command error logged and returned. `linux/brcmfmac/cfg80211.c:2679-2684`

### whd

1. host — de-register the join event handler — host table only, no command — `whd/src/whd_wifi_api.c:2522-2526`, `whd/src/whd_events.c:597-626`
2. command (set) — WLC_DISASSOC = 52 — no payload. Note: a failure is only logged — `whd/src/whd_wifi_api.c:2528-2534`
3. variable (set), chip 43022 only — bsscfg:sup_wpa — u32 index, u32 0; result ignored — `whd/src/whd_wifi_api.c:2536-2546`
4. host — join status word = 0, role invalid — `whd/src/whd_wifi_api.c:2552-2553`

Succeeds when: Always returns WHD_SUCCESS once past the argument checks (`whd/src/whd_wifi_api.c:2567`).

Fails when:

- Bad interface index -> WHD_BADARG (`whd/src/whd_wifi_api.c:2517-2521`).
- The command result is not propagated (`whd/src/whd_wifi_api.c:2529-2534`).

### c-driver

1. host state — wifi_join_state = 0 (station interface only) — `c-driver/cyw43_ctrl.c:674-676`
2. command (set) — WLC_DISASSOC = 52 (public constant CYW43_IOCTL_SET_DISASSOC = 0x69 = 52*2+1) — no payload, sent on the interface number passed in. Note: the public command numbers carry the set flag in bit 0 and are halved before sending — `c-driver/cyw43_ctrl.c:678`, `c-driver/cyw43_ll.h:29-33`, `c-driver/cyw43_ll.c:1327-1330`

Succeeds when: Return value of the command (0). `c-driver/cyw43_ctrl.c:678`

Fails when:

- -ETIMEDOUT if no response within 500 ms (`c-driver/cyw43_ll.c:1294-1325`).
- The link-down callback runs later on the DISASSOC (11) or LINK-down event (`c-driver/cyw43_ctrl.c:332-333`, `c-driver/cyw43_ctrl.c:398-400`).

### Differences

Differences: All four drivers send command 52 and wait for no event. `embassy/control.rs:840-844`, `linux/brcmfmac/cfg80211.c:2679-2684`, `whd/src/whd_wifi_api.c:2528-2534`, `c-driver/cyw43_ctrl.c:678` Only linux sends a payload with it. `linux/brcmfmac/cfg80211.c:2679-2684`

| Aspect | embassy | linux | whd | c-driver | Citations |
|---|---|---|---|---|---|
| Command 52 payload | empty | brcmf_scb_val_le: val u32 = reason code, ea[6] = BSSID; 12 bytes by layout (computed); the 2 padding bytes are not zeroed | none | none | `embassy/control.rs:840-844`, `linux/brcmfmac/cfg80211.c:2679-2684`, `linux/brcmfmac/cfg80211.c:2666`, `linux/brcmfmac/fwil_types.h:602-605`, `whd/src/whd_wifi_api.c:2528-2534`, `c-driver/cyw43_ctrl.c:678` |
| Other sends | none | none in the leave path; linux's own link-down path sends command 52 with no payload and clears the PMK | `bsscfg:sup_wpa` = 0 on chip 43022 only | none | `embassy/control.rs:840-844`, `linux/brcmfmac/cfg80211.c:1756-1778`, `whd/src/whd_wifi_api.c:2536-2546`, `c-driver/cyw43_ctrl.c:674-678` |
| Host state | clears the started_join flag | clears connection state bits, reports the disconnect to cfg80211 | de-registers the join handler; status word 0, role invalid | wifi_join_state = 0 on the station interface | `embassy/control.rs:840-844`, `linux/brcmfmac/cfg80211.c:2674-2678`, `whd/src/whd_wifi_api.c:2522-2526`, `whd/src/whd_wifi_api.c:2552-2553`, `c-driver/cyw43_ctrl.c:674-676` |
| Command result | not acted on, only logged | logged and returned | only logged; the function returns WHD_SUCCESS | returned; -ETIMEDOUT after 500 ms without a response | `embassy/runner.rs:1174-1176`, `linux/brcmfmac/cfg80211.c:2679-2684`, `whd/src/whd_wifi_api.c:2529-2534`, `whd/src/whd_wifi_api.c:2567`, `c-driver/cyw43_ll.c:1294-1325` |
| Other callers | join() sends it first when an earlier join is unfinished | the link-down path also sends command 52, with no payload, when the interface had been connected | also run automatically after a failed join | the same call is used with the AP interface number | `embassy/control.rs:369-371`, `linux/brcmfmac/cfg80211.c:1745-1763`, `whd/src/whd_wifi_api.c:2167-2171`, `c-driver/cyw43_ctrl.c:678` |

## Start AP

### embassy

1. command (set) — Down = 3 — empty — `embassy/control.rs:560`, `embassy/control.rs:348-350`
2. variable (set) — apsta — u32 = 0 — `embassy/control.rs:563`
3. command (set) — Up = 2 — empty — `embassy/control.rs:566`, `embassy/control.rs:343-345`
4. command (set) — SetAuth = 22 — u32 = 0 (AUTH_OPEN), for every AP security type — `embassy/control.rs:569`
5. command (set) — SetAp = 118 — u32 = 1 — `embassy/control.rs:572`
6. variable (set) — bsscfg:ssid — SsidInfoWithIndex (`embassy/structs.rs:428-431`): index u32 = 0, len u32, ssid[32]; 40 bytes — `embassy/control.rs:575-583`
7. command (set) — SetChannel = 30 — u32 = channel number — `embassy/control.rs:586`
8. variable (set) — bsscfg:wsec — u32 0, u32 (security & 0xFF): open 0; WPA2 / WPA3 / mixed all 0x04 (AES). Note: Security enum `embassy/consts.rs:244-249` — `embassy/control.rs:548-557`, `embassy/control.rs:589`
9. variable (set) — mfp — u32: open 0, WPA2 0, WPA3 2 (required), mixed 1 (capable) — `embassy/control.rs:548-557`, `embassy/control.rs:592`
10. variable (set) — bsscfg:wpa_auth — u32 0, u32: open 0; WPA2 0x0084 (WPA2_PSK|WPA_PSK); WPA3 0x40000; mixed 0x40080 (WPA2_PSK|SAE). Note: sent for open too, with value 0 — `embassy/control.rs:548-557`, `embassy/control.rs:595`
11. delay, secured only — 100 ms — `embassy/control.rs:597-598`
12. variable (set), WPA3 and mixed — sae_password — SaePassphraseInfo len u16, passphrase[128]; 130 bytes. Note: sent first: for WPA2/WPA3 mixed start_ap calls set_ap_sae_passphrase and then set_ap_wpa2_passphrase (`embassy/control.rs:604-607`); for WPA3-only this is the only key write — `embassy/control.rs:600-607`, `embassy/control.rs:629-636`
13. command (set), WPA2 and mixed — SetWsecPmk = 268 — PassphraseInfo len u16, flags u16 = 1, passphrase[64]; 68 bytes. Note: for mixed this follows sae_password (`embassy/control.rs:604-607`); for WPA2-only it is the only key write (`embassy/control.rs:602`). No 3 ms delay here, unlike the station join — `embassy/control.rs:600-607`, `embassy/control.rs:618-627`
14. variable (set) — 2g_mrate — u32 = 22 (11 Mbit/s in 500 kbit/s units) — `embassy/control.rs:612`
15. variable (set) — bss — u32 0, u32 1 (BSS up) — `embassy/control.rs:615`

Succeeds when: None checked: the function returns after the last command. No event is waited for. `embassy/control.rs:543-616`

Fails when:

- Passphrase shorter than 8 or longer than 64 bytes panics before any command (`embassy/control.rs:544-546`).
- embassy does not act on the command status: the runner only logs a warning when the CDC status is non-zero ('TODO: propagate error instead', `embassy/runner.rs:1174-1176`), so a rejected command does not stop the sequence.

### linux

1. command (get) — BRCMF_C_GET_REGULATORY = 46 — current 802.11d setting stored — `linux/brcmfmac/cfg80211.c:5289-5299`
2. variable (set) — mpc — u32 = 0 — `linux/brcmfmac/cfg80211.c:5319-5320`, `linux/brcmfmac/cfg80211.c:1032-1045`
3. variable (set) — arp_ol, arpoe, ndoe — brcmf_configure_arp_nd_offload(false): arp_ol u32 = 0; arpoe = 0 only when the arp_ol set succeeded; then ndoe = 0; errors only logged — `linux/brcmfmac/cfg80211.c:5321`, `linux/brcmfmac/core.c:96-136`
4. command (set), if changed — BRCMF_C_SET_REGULATORY = 47 — u32 0/1 — `linux/brcmfmac/cfg80211.c:5325-5333`
5. command (set), if given — BRCMF_C_SET_BCNPRD = 76 — u32 beacon interval — `linux/brcmfmac/cfg80211.c:5335-5343`
6. command (set), if given — BRCMF_C_SET_DTIMPRD = 78 — u32 DTIM period — `linux/brcmfmac/cfg80211.c:5344-5352`
7. command (set), interface 0 or no RSDB/MCHAN feature — BRCMF_C_DOWN = 3 — u32 = 1 — `linux/brcmfmac/cfg80211.c:5354-5363`
8. variable (set), same condition — apsta — u32 = 0; result ignored — `linux/brcmfmac/cfg80211.c:5364`
9. command (set) — BRCMF_C_SET_INFRA = 20 — u32 = 1 — `linux/brcmfmac/cfg80211.c:5367-5371`
10. variable (set), MBSS feature — mbss — u32 = 1 — `linux/brcmfmac/cfg80211.c:5380-5381`
11. command (set) — BRCMF_C_SET_AP = 118 — u32 = 1 — `linux/brcmfmac/cfg80211.c:5383-5388`
12. variable (set) — chanspec — u32 chanspec ('Firmware 10.x requires setting channel after enabling AP and before bringing interface up') — `linux/brcmfmac/cfg80211.c:5389-5398`
13. command (set) — BRCMF_C_UP = 2 — u32 = 1 — `linux/brcmfmac/cfg80211.c:5400-5404`
14. command (set), if a PSK is supplied — BRCMF_C_SET_WSEC_PMK = 268 — key_len 32, flags 0, PMK — `linux/brcmfmac/cfg80211.c:5406-5413`
15. variable/command (set), if an SAE password is supplied — sae_password (vendor-specific, see the SAE join entry) — `linux/brcmfmac/cfg80211.c:5414-5420`
16. variables (set), secured — wme_bss_disable, [bip], auth, wsec, [mfp], wpa_auth — parsed from the beacon's RSN/WPA element: wme_bss_disable 0/1 (RSN only); auth = 0; wsec = cipher bits | 0x40 (SES_OW_ENABLED); mfp 0/1/2 if the MFP feature is present; wpa_auth = OR of AKM bits (PSK 0x80 or 0x04, SAE 0x40000, ...). Note: order as listed (`linux/brcmfmac/cfg80211.c:4786`, `linux/brcmfmac/cfg80211.c:4799`, `linux/brcmfmac/cfg80211.c:4812`, `linux/brcmfmac/cfg80211.c:4818`, `linux/brcmfmac/cfg80211.c:4827`, `linux/brcmfmac/cfg80211.c:4834`); an SAE-PWE vendor setting may follow (`linux/brcmfmac/cfg80211.c:5138-5207`) — `linux/brcmfmac/cfg80211.c:4593-4840`, `linux/brcmfmac/cfg80211.c:5222-5247`
17. variables (set), open — auth, wsec, wpa_auth — all u32 = 0. Note: the return value of brcmf_configure_opensecurity is not checked by its caller (`linux/brcmfmac/cfg80211.c:5250`); wpa_auth is 1 (WPA_AUTH_NONE) instead of 0 in IBSS mode (`linux/brcmfmac/cfg80211.c:4566-4569`) — `linux/brcmfmac/cfg80211.c:4547-4577`, `linux/brcmfmac/cfg80211.c:5248-5251`
18. command (set) — BRCMF_C_SET_SSID = 26 — brcmf_join_params with only the SSID filled ('create softap'). Note: sizeof(struct brcmf_join_params) is sent in full, zeroed apart from the SSID (`linux/brcmfmac/cfg80211.c:5436-5441`). brcmf_cfg80211_reconfigure_wep runs just before this (`linux/brcmfmac/cfg80211.c:5431-5434`); when a WEP key is stored it re-sends the key, reads the variable wsec and sets it again with WEP_ENABLED added (`linux/brcmfmac/cfg80211.c:3041-3071`) — `linux/brcmfmac/cfg80211.c:5431-5445`
19. variable (set) — closednet — u32 = 1 for a hidden SSID, else 0 — `linux/brcmfmac/cfg80211.c:5447-5455`
20. variable (set) — vndr_ie — brcmf_config_ap_mgmt_ie: beacon, probe-response and association-response vendor elements, each through brcmf_vif_set_mgmt_ie, which sets vndr_ie when its add/delete buffer is not empty — `linux/brcmfmac/cfg80211.c:5493`, `linux/brcmfmac/cfg80211.c:5101-5135`, `linux/brcmfmac/cfg80211.c:5068-5073`

Succeeds when: Every checked command returns 0; then the AP_CREATED bit is set and the carrier turned on (`linux/brcmfmac/cfg80211.c:5493-5495`). No event is waited for.

Fails when:

- Any checked command failing returns its error; mpc is set back to 1 and offloads re-enabled (`linux/brcmfmac/cfg80211.c:5497-5502`).
- P2P group-owner interfaces use a different tail: 'chanspec', security, bsscfg 'ssid', then 'bss' {index, 1} (`linux/brcmfmac/cfg80211.c:5458-5486`).

### whd

1. command (set), AP on primary interface only — WLC_DOWN = 3 — no payload. Note: whd_create_softap_interface, called from whd_wifi_init_ap when the AP interface is not yet created (`whd/src/whd_ap.c:359-362`); its return value is not checked there — `whd/src/whd_ap.c:221-224`
2. variable (set), primary only — apsta — u32 = 0; 'unsupported' tolerated — `whd/src/whd_ap.c:225-233`
3. command (set), primary only — WLC_UP = 2 — no payload — `whd/src/whd_ap.c:234`
4. variable (get) — bss — request u32 = bsscfg index; reply BSS_UP (1) -> already up, return; a failed get means the interface does not exist yet — `whd/src/whd_ap.c:247-271`, `whd/src/whd_ap.c:55-58`
5. host — register handler for IF and LINK events — `whd/src/whd_ap.c:70`, `whd/src/whd_ap.c:278-289`
6. variable (set), side effect of handler registration — bsscfg:event_msgs (or bsscfg:event_msgs_ext when any registered event number exceeds 127) — u32 bsscfg index, then a 16-byte bit mask (WL_EVENTING_MASK_LEN, `whd/src/include/whd_wlioctl.h:1932`) holding the union of every currently registered handler's events; the _ext form carries version/command/length header plus a mask sized to the highest event. Note: whd rewrites the firmware event mask each time a handler is registered; de-registering only edits the host table and sends nothing (`whd/src/whd_events.c:597-626`) — `whd/src/whd_events.c:255-325`, `whd/src/whd_events.c:348-425`
7. event wait, only if the bss get failed — IF or LINK event — semaphore, 10000 ms — `whd/src/whd_ap.c:290-294`, `whd/src/whd_ap.c:167-190`
8. command (set), primary only — WLC_SET_AP = 118 — u32 = 1 — `whd/src/whd_ap.c:297-305`
9. variable (set) — cur_etheraddr — whd_wifi_set_mac_address: for an interface in the AP role the 6-byte address has its locally-administered bit (0x02 of the first octet) inverted before it is sent. Note: when the interface has no address yet, the primary interface's address is read first (`whd/src/whd_ap.c:307-319`); name constant `whd/src/include/whd_wlioctl.h:1078` — `whd/src/whd_ap.c:321-325`, `whd/src/whd_wifi.c:59-92`, `whd/src/whd_wifi.c:42`
10. variable (set) — bsscfg:ssid — u32 index, u32 length, ssid bytes; 40-byte buffer; sent via the primary interface — `whd/src/whd_ap.c:411-417`
11. variable (set) — chanspec — u32 = CH20MHZ_CHSPEC(chanspec) — `whd/src/whd_ap.c:419-420`, `whd/src/whd_wifi_api.c:556-591`
12. variable (set) — bsscfg:wsec — u32 index, u32 auth_type & 0xFF (or, for WPS types, auth_type without the WPS bit OR SES_OW_ENABLED) — `whd/src/whd_ap.c:422-434`
13. variable (set) — mfp — u32 = 2 for WPA3_SAE, 1 for WPA3_WPA2_PSK, else 0 — `whd/src/whd_ap.c:435-443`
14. variable (set) — bsscfg:wpa_auth — u32 index, u32: open 0; WPA3_SAE 0x40000; WPA3_WPA2_PSK 0x40080; WPA_TKIP_PSK 0x0004; every other type 0x0084 — `whd/src/whd_ap.c:445-467`
15. variable (set), WPA3 / mixed with SAE capability — sae_password — 1 ms delay; password_len u16, password[128]. Note: for pure WPA3 with the capability flag this is the only key command — `whd/src/whd_ap.c:469-481`, `whd/src/whd_wifi_api.c:775-803`
16. delay + command (set), all other secured cases — WLC_SET_WSEC_PMK = 268 — 1 ms delay; wsec_pmk_t key_len u16, flags u16 = 1 (0 with the PMK join option), key; whd_ap.c does not memset the buffer in this path (whether whd_proto_get_ioctl_buffer returns zeroed memory is unverified) — `whd/src/whd_ap.c:483-504`
17. variable (set), any WPA3 type — sae_max_pwe_loop — u32 = 5; failure ignored — `whd/src/whd_ap.c:49`, `whd/src/whd_ap.c:506-517`
18. variable (set), 2.4 GHz chanspec only — 2g_mrate — u32 = 22 — `whd/src/whd_ap.c:45`, `whd/src/whd_ap.c:519-526`
19. variable (get/set) — arpoe, ndoe — each read; if non-zero set to 0. Note: whd_wifi_start_ap begins here — `whd/src/whd_ap.c:554-567`
20. variable (set) — bss — u32 bsscfg index, u32 1 (BSS_UP); via the primary interface — `whd/src/whd_ap.c:569-575`
21. event wait — LINK or IF event — semaphore, 10000 ms; then AP marked up. Note: any LINK or IF event releases the wait; status and flags are not examined — `whd/src/whd_ap.c:577-582`, `whd/src/whd_ap.c:167-190`

Succeeds when: A LINK or IF event arrives within 10 s of the 'bss' up command (`whd/src/whd_ap.c:577-582`).

Fails when:

- Semaphore timeout (10 s) -> error return (`whd/src/whd_ap.c:578-579`).
- WPA/WPA2 key length outside 8..64 -> WHD_WPA_KEYLEN_BAD; WEP types -> WHD_WEP_NOT_ALLOWED; SSID too long -> WHD_WLAN_BADSSIDLEN (`whd/src/whd_ap.c:368-409`).
- AP already up -> WHD_AP_ALREADY_UP inside interface creation (`whd/src/whd_ap.c:241-245`).
- Most sets abort the sequence on error (CHECK_RETURN_WITH_SEMAPHORE); sae_password and sae_max_pwe_loop results are not checked (`whd/src/whd_ap.c:473`, `whd/src/whd_ap.c:480`, `whd/src/whd_ap.c:513-516`).

### c-driver

1. precondition — first interface-up runs cyw43_ll_wifi_on — includes apsta = 1 (`c-driver/cyw43_ll.c:2038`) and the default power-save sequence. Note: apsta stays 1; no down/up cycle and no SET_AP command in this driver — `c-driver/cyw43_ctrl.c:561-568`, `c-driver/cyw43_ll.c:2000-2070`
2. variable (get) — bss — request: 'bss\0' + u32 1 (AP bsscfg index), sent on the station interface; a non-zero reply means the AP is already up and the rest is skipped. Note: source comments note this can fail with status 0xffffffe2 when the AP is down and that the result should then not be trusted — `c-driver/cyw43_ll.c:2358-2369`
3. variable (set) — ampdu_ba_wsize — u32 = 2 — `c-driver/cyw43_ll.c:2378-2379`
4. variable (set) — bsscfg:ssid — u32 1, u32 ssid_len, ssid[32]; 40 bytes — `c-driver/cyw43_ll.c:2381-2386`
5. command (set) — WLC_SET_CHANNEL = 30 — u32 = channel — `c-driver/cyw43_ll.c:2389`
6. variable (set) — bsscfg:wsec — u32 1, u32 auth (the full constant, not masked: open 0, WPA_TKIP 0x00200002, WPA2_AES 0x00400004, WPA2_MIXED 0x00400006, WPA3_SAE 0x01000004, WPA3_WPA2 0x01400004). Note: values from `c-driver/cyw43_ll.h:149-181` — `c-driver/cyw43_ll.c:2392`
7. variable (set) — mfp — u32: 2 for WPA3_SAE, 1 for WPA3_WPA2, else 0; sent on the AP interface — `c-driver/cyw43_ll.c:2394-2401`
8. variable (set), secured only — bsscfg:wpa_auth — u32 1, u32: WPA_TKIP 0x0004; WPA2_AES / WPA2_MIXED 0x0084; WPA3_SAE 0x40000; WPA3_WPA2 0x40080. Note: not sent for open — `c-driver/cyw43_ll.c:2403-2418`
9. delay + variable (set), WPA3 and mixed — sae_password — 2 ms delay; 130 bytes key_len u16, password[128]; AP interface — `c-driver/cyw43_ll.c:2421-2427`
10. delay + command (set), WPA / WPA2 / mixed — WLC_SET_WSEC_PMK = 268 — 2 ms delay; 68 bytes key_len u16, flags u16 = 1, key[64]; AP interface — `c-driver/cyw43_ll.c:2428-2435`
11. variable (set), WPA3 and mixed — sae_max_pwe_loop — as written the call is cyw43_write_iovar_u32(self, "sae_max_pwe_loop", WWD_AP_INTERFACE, 5) against the signature (var, val, iface): value 1 (WWD_AP_INTERFACE, `c-driver/cyw43_ll.c:152`), interface 5. Note: whd sends value 5 for the same variable (`whd/src/whd_ap.c:49`, `whd/src/whd_ap.c:507-512`); the value and interface arguments are in the opposite order to the helper's signature — `c-driver/cyw43_ll.c:2438-2440`, `c-driver/cyw43_ll.c:1538`
12. command (set) — WLC_SET_GMODE = 110 — u32 = 1 (auto); AP interface — `c-driver/cyw43_ll.c:2443`
13. variable (set) — 2g_mrate — u32 = 22; AP interface — `c-driver/cyw43_ll.c:2446`
14. command (set) — WLC_SET_DTIMPRD = 78 — u32 = 1; AP interface — `c-driver/cyw43_ll.c:2449`
15. host — IP stack interface initialised — `c-driver/cyw43_ctrl.c:572-576`
16. variable (set) — bss — u32 1 (AP index), u32 1 (up); station interface — `c-driver/cyw43_ctrl.c:577-580`, `c-driver/cyw43_ll.c:2454-2460`
17. event wait — LINK (16) status 0 flags&1 on a non-station interface — IP-stack link-up callback for that interface. Note: not awaited by the caller — `c-driver/cyw43_ctrl.c:389-397`

Succeeds when: No return-value success test: cyw43_wifi_set_up is void. Link-up is signalled by a LINK event with flags bit 0 on the AP interface (`c-driver/cyw43_ctrl.c:389-397`).

Fails when:

- Key longer than 64 (128 for pure WPA3) -> -EINVAL from the init function, which the caller ignores (`c-driver/cyw43_ll.c:2371-2376`; `c-driver/cyw43_ctrl.c:749`).
- Most set helpers in cyw43_ll.c are void and discard the command result (`c-driver/cyw43_ll.c:1538-1562`, `c-driver/cyw43_ll.c:1956-1960`); the only failure surfaced is a 500 ms response timeout inside cyw43_do_ioctl, which returns -ETIMEDOUT to callers that check it (`c-driver/cyw43_ll.c:1294-1325`, `c-driver/cyw43_config.h:92`).

### Differences

Differences: embassy, whd and c-driver bring the AP up with the variable `bss`; linux uses command 26 (SET_SSID) and uses `bss` only for P2P group-owner interfaces. `embassy/control.rs:615`, `whd/src/whd_ap.c:569-575`, `c-driver/cyw43_ll.c:2454-2460`, `linux/brcmfmac/cfg80211.c:5431-5445`, `linux/brcmfmac/cfg80211.c:5458-5486` embassy runs the AP on bsscfg index 0 with apsta off; c-driver keeps apsta = 1 and uses index 1. `embassy/control.rs:563`, `embassy/control.rs:575-583`, `c-driver/cyw43_ll.c:2038`, `c-driver/cyw43_ll.c:2381-2386` Only whd waits for an event after `bss` up. `whd/src/whd_ap.c:577-582`

| Aspect | embassy | linux | whd | c-driver | Citations |
|---|---|---|---|---|---|
| bsscfg index | 0 | the interface's own | the caller's interface | 1 | `embassy/control.rs:575-583`, `linux/brcmfmac/cfg80211.c:5257-5503`, `whd/src/whd_ap.c:411-417`, `c-driver/cyw43_ll.c:2381-2386` |
| Down / apsta / up | Down, apsta = 0, Up | DOWN (u32 1), apsta = 0 when interface 0 or no RSDB/MCHAN feature; UP after the channel | WLC_DOWN, apsta = 0, WLC_UP only when the AP is on the primary interface | none; apsta stays 1 from interface-up | `embassy/control.rs:560-566`, `linux/brcmfmac/cfg80211.c:5354-5364`, `linux/brcmfmac/cfg80211.c:5400-5404`, `whd/src/whd_ap.c:221-234`, `c-driver/cyw43_ctrl.c:561-568`, `c-driver/cyw43_ll.c:2038` |
| SET_AP (118) | 1 | 1 | 1, primary interface only | not sent | `embassy/control.rs:572`, `linux/brcmfmac/cfg80211.c:5383-5388`, `whd/src/whd_ap.c:297-305`, `c-driver/cyw43_ll.c:2358-2460` |
| Channel | command 30, channel number | variable `chanspec` | variable `chanspec`, CH20MHZ_CHSPEC | command 30, channel number | `embassy/control.rs:586`, `linux/brcmfmac/cfg80211.c:5389-5398`, `whd/src/whd_ap.c:419-420`, `c-driver/cyw43_ll.c:2389` |
| SSID | `bsscfg:ssid`, 40 bytes | carried by command 26, brcmf_join_params with only the SSID filled | `bsscfg:ssid`, 40-byte buffer | `bsscfg:ssid`, 40 bytes | `embassy/control.rs:575-583`, `linux/brcmfmac/cfg80211.c:5431-5445`, `whd/src/whd_ap.c:411-417`, `c-driver/cyw43_ll.c:2381-2386` |
| Start | `bss` {0, 1} | command 26; `bss` {index, 1} for P2P group owner only | `bss` {index, 1} | `bss` {1, 1} | `embassy/control.rs:615`, `linux/brcmfmac/cfg80211.c:5431-5445`, `linux/brcmfmac/cfg80211.c:5458-5486`, `whd/src/whd_ap.c:569-575`, `c-driver/cyw43_ll.c:2454-2460` |
| auth | command 22 = 0 for every type | variable `auth` = 0 | not sent in the AP path (unverified) | not sent in the AP path; command 22 is sent only by the join code | `embassy/control.rs:569`, `linux/brcmfmac/cfg80211.c:4593-4840`, `linux/brcmfmac/cfg80211.c:4547-4577`, `c-driver/cyw43_ll.c:2275` |
| wsec | `bsscfg:wsec` = security AND 0xFF | `wsec` = cipher bits OR 0x40 (SES_OW_ENABLED); 0 for open | `bsscfg:wsec` = auth_type AND 0xFF | `bsscfg:wsec` = the full constant, not masked | `embassy/control.rs:589`, `linux/brcmfmac/cfg80211.c:4593-4840`, `linux/brcmfmac/cfg80211.c:4547-4577`, `linux/include/brcmu_wifi.h:211`, `whd/src/whd_ap.c:422-434`, `c-driver/cyw43_ll.c:2392` |
| wpa_auth, open | 0 sent | 0 sent | 0 sent | not sent | `embassy/control.rs:595`, `linux/brcmfmac/cfg80211.c:4547-4577`, `whd/src/whd_ap.c:445-467`, `c-driver/cyw43_ll.c:2403-2418` |
| wpa_auth, WPA2 | 0x0084 | OR of the AKM bits in the beacon's element (PSK 0x80 or 0x04) | 0x0084 (0x0004 for WPA_TKIP_PSK) | 0x0084 (0x0004 for WPA_TKIP) | `embassy/control.rs:595`, `linux/brcmfmac/cfg80211.c:4593-4840`, `whd/src/whd_ap.c:445-467`, `c-driver/cyw43_ll.c:2403-2418` |
| wpa_auth, WPA3 / mixed | 0x40000 / 0x40080 | SAE bit 0x40000 OR-ed in | 0x40000 / 0x40080 | 0x40000 / 0x40080 | `embassy/control.rs:595`, `linux/brcmfmac/cfg80211.c:4593-4840`, `whd/src/whd_ap.c:445-467`, `c-driver/cyw43_ll.c:2403-2418` |
| mfp | open 0, WPA2 0, WPA3 2, mixed 1 | 0, 1 or 2 from the element, MFP feature only | WPA3 2, mixed 1, else 0 | WPA3 2, mixed 1, else 0 | `embassy/control.rs:592`, `linux/brcmfmac/cfg80211.c:4593-4840`, `whd/src/whd_ap.c:435-443`, `c-driver/cyw43_ll.c:2394-2401` |
| Key writes | `sae_password` (WPA3, mixed), then command 268 passphrase with flags 1 (WPA2, mixed) | command 268 with a 32-byte PMK, flags 0; `sae_password` vendor-specific | pure WPA3 with the SAE capability: `sae_password` only; every other secured type: command 268 with flags 1 (0 with the PMK join option), preceded by `sae_password` for mixed with the SAE capability | `sae_password` (WPA3, mixed), then command 268 with flags 1 (WPA, WPA2, mixed) | `embassy/control.rs:600-607`, `linux/brcmfmac/cfg80211.c:5406-5420`, `whd/src/whd_ap.c:469-504`, `c-driver/cyw43_ll.c:2421-2435` |
| Delay before key writes | 100 ms once | none found (unverified) | 1 ms each | 2 ms each | `embassy/control.rs:597-598`, `whd/src/whd_ap.c:469-504`, `c-driver/cyw43_ll.c:2421-2435` |
| sae_max_pwe_loop | not sent | an SAE-PWE vendor setting may follow the security variables | 5, failure ignored | the call as written sends value 1 on interface 5 | `embassy/control.rs:543-616`, `linux/brcmfmac/cfg80211.c:5138-5207`, `whd/src/whd_ap.c:506-517`, `c-driver/cyw43_ll.c:2438-2440`, `c-driver/cyw43_ll.c:1538`, `c-driver/cyw43_ll.c:152` |
| 2g_mrate | 22 | not found in these sources | 22, 2.4 GHz chanspec only | 22 | `embassy/control.rs:612`, `whd/src/whd_ap.c:519-526`, `c-driver/cyw43_ll.c:2446` |
| Other settings | none | mpc 0, regulatory, beacon period (76), DTIM period (78), SET_INFRA 1, mbss, closednet, ARP/ND offload off | arpoe / ndoe set to 0 when non-zero, AP MAC address | ampdu_ba_wsize 2, SET_GMODE 1, DTIM period 1 | `embassy/control.rs:543-616`, `linux/brcmfmac/cfg80211.c:5289-5381`, `linux/brcmfmac/cfg80211.c:5447-5455`, `whd/src/whd_ap.c:554-567`, `whd/src/whd_ap.c:307-325`, `c-driver/cyw43_ll.c:2378-2379`, `c-driver/cyw43_ll.c:2443`, `c-driver/cyw43_ll.c:2449` |
| Event wait | none | none | LINK or IF event within 10000 ms; status and flags not examined | LINK event with flags bit 0 calls the link-up callback; not awaited | `embassy/control.rs:543-616`, `linux/brcmfmac/cfg80211.c:5493-5495`, `whd/src/whd_ap.c:577-582`, `c-driver/cyw43_ctrl.c:389-397` |

## Stop AP

### embassy

1. variable (set) — bss — u32 0, u32 0 (BSS down) — `embassy/control.rs:641`
2. command (set) — SetAp = 118 — u32 = 0 — `embassy/control.rs:644`
3. command (set) — Down = 3 — empty — `embassy/control.rs:647`
4. variable (set) — apsta — u32 = 1 — `embassy/control.rs:650`
5. command (set) — Up = 2 — empty — `embassy/control.rs:653`

Succeeds when: None checked; returns after the last command. `embassy/control.rs:641-653`

Fails when:

- embassy does not act on the command status: the runner only logs a warning when the CDC status is non-zero ('TODO: propagate error instead', `embassy/runner.rs:1174-1176`), so a rejected command does not stop the sequence.

### linux

1. delay — 400 ms — 'most likely deauths outstanding' — `linux/brcmfmac/cfg80211.c:5519-5521`
2. command (set), if PSK offload was used — BRCMF_C_SET_WSEC_PMK = 268 — key_len 0 (clears the key) — `linux/brcmfmac/cfg80211.c:5523-5527`, `linux/brcmfmac/cfg80211.c:1740-1743`
3. variable/command (set), if SAE offload was used — sae_password (vendor-specific) — empty password — `linux/brcmfmac/cfg80211.c:5528-5529`
4. variable (set), bsscfg 0 — closednet — u32 = 0 — `linux/brcmfmac/cfg80211.c:5538-5540`
5. command (set) — BRCMF_C_SET_SSID = 26 — all-zero brcmf_join_params — `linux/brcmfmac/cfg80211.c:5542-5546`
6. command (set) — BRCMF_C_DOWN = 3 — u32 = 1 — `linux/brcmfmac/cfg80211.c:5547-5549`
7. command (set) — BRCMF_C_SET_AP = 118 — u32 = 0 — `linux/brcmfmac/cfg80211.c:5550-5552`
8. variable (set), MBSS feature — mbss — u32 = 0 — `linux/brcmfmac/cfg80211.c:5553-5554`
9. command (set) — BRCMF_C_SET_REGULATORY = 47 — restore the stored value — `linux/brcmfmac/cfg80211.c:5555-5556`
10. command (set) — BRCMF_C_UP = 2 — u32 = 1 ('bring device back up so it can be used again'). Note: followed by brcmf_vif_clear_mgmt_ies, which calls brcmf_vif_set_mgmt_ie with empty element sets for the association-response (or probe-request), probe-response and beacon flags (`linux/brcmfmac/cfg80211.c:5562`, `linux/brcmfmac/cfg80211.c:5080-5099`) — `linux/brcmfmac/cfg80211.c:5557-5560`
11. variable (set) — mpc — u32 = 1 — `linux/brcmfmac/cfg80211.c:5571`
12. variable (set) — arp_ol, arpoe, ndoe — brcmf_configure_arp_nd_offload(true): arp_ol u32 = BRCMF_ARP_OL_AGENT | BRCMF_ARP_OL_PEER_AUTO_REPLY; arpoe = 1 only when the arp_ol set succeeded; then ndoe = 1; the whole call is skipped while a soft AP is still running; errors only logged — `linux/brcmfmac/cfg80211.c:5573`, `linux/brcmfmac/core.c:96-136`

Succeeds when: No event wait; errors are logged and the sequence continues, returning the last error value (`linux/brcmfmac/cfg80211.c:5542-5577`).

Fails when:

- Multi-BSS secondary interfaces only send DOWN (`linux/brcmfmac/cfg80211.c:5533-5536`).
- Non-AP interface types (P2P GO) send 'bss' {index, 0} instead (`linux/brcmfmac/cfg80211.c:5563-5569`).

### whd

1. variable (get) — bss — request u32 = bsscfg index; 'not found' or a value other than 1 -> AP treated as already down, return success — `whd/src/whd_ap.c:622-645`
2. variable (set) — bss — u32 bsscfg index, u32 0 (BSS_DOWN); via the primary interface — `whd/src/whd_ap.c:681-687`
3. event wait — LINK or IF event — semaphore, 10000 ms — `whd/src/whd_ap.c:689-695`
4. command (set), AP on primary interface only — WLC_SET_AP = 118 — u32 = 0 — `whd/src/whd_ap.c:697-704`
5. event wait, primary only — LINK or IF event — semaphore, 10000 ms — `whd/src/whd_ap.c:705-711`
6. host — de-register AP event handler, mark AP down, role invalid — `whd/src/whd_ap.c:714-736`
7. variable (set), if firmware-capability flag OFFLOADS — arpoe, ndoe — each u32 = 1 — `whd/src/whd_ap.c:738-743`

Succeeds when: Both waits satisfied; returns WHD_SUCCESS (`whd/src/whd_ap.c:745`).

Fails when:

- Either 10 s wait timing out -> that error is returned after cleanup (`whd/src/whd_ap.c:690-722`).

### c-driver

1. variable (set) — bss — u32 1 (AP index), u32 0 (down); station interface — `c-driver/cyw43_ctrl.c:581-584`, `c-driver/cyw43_ll.c:2454-2460`
2. host — IP stack interface removed, interface bit cleared — `c-driver/cyw43_ctrl.c:585-588`
3. event — LINK (16) status 0 without flags bit 0 — IP-stack link-down callback. Note: not awaited — `c-driver/cyw43_ctrl.c:398-401`

Succeeds when: None checked (void function). `c-driver/cyw43_ctrl.c:581-588`

Fails when:

- Most set helpers in cyw43_ll.c are void and discard the command result (`c-driver/cyw43_ll.c:1538-1562`, `c-driver/cyw43_ll.c:1956-1960`); the only failure surfaced is a 500 ms response timeout inside cyw43_do_ioctl, which returns -ETIMEDOUT to callers that check it (`c-driver/cyw43_ll.c:1294-1325`, `c-driver/cyw43_config.h:92`).

### Differences

Differences: c-driver sends one command, embassy five, and linux a longer sequence built around an empty SET_SSID. `c-driver/cyw43_ctrl.c:581-584`, `embassy/control.rs:641-653`, `linux/brcmfmac/cfg80211.c:5542-5560` Only whd waits for events, and only embassy restores apsta = 1. `whd/src/whd_ap.c:689-711`, `embassy/control.rs:650`

| Aspect | embassy | linux | whd | c-driver | Citations |
|---|---|---|---|---|---|
| `bss` down | {0, 0} | not sent for the AP interface type; P2P group owner sends {index, 0} | {index, 0}, after a `bss` get shows the AP up | {1, 0} | `embassy/control.rs:641`, `linux/brcmfmac/cfg80211.c:5563-5569`, `whd/src/whd_ap.c:622-645`, `whd/src/whd_ap.c:681-687`, `c-driver/cyw43_ctrl.c:581-584` |
| Empty SET_SSID (26) | no | all-zero brcmf_join_params | no | no | `embassy/control.rs:641-653`, `linux/brcmfmac/cfg80211.c:5542-5546`, `whd/src/whd_ap.c:622-745`, `c-driver/cyw43_ctrl.c:581-588` |
| SET_AP (118) = 0 | yes | yes | primary interface only | no | `embassy/control.rs:644`, `linux/brcmfmac/cfg80211.c:5550-5552`, `whd/src/whd_ap.c:697-704`, `c-driver/cyw43_ctrl.c:581-588` |
| Down / up cycle | Down, apsta = 1, Up | DOWN before SET_AP 0, UP after; multi-BSS secondary interfaces send only DOWN | none | none | `embassy/control.rs:647-653`, `linux/brcmfmac/cfg80211.c:5547-5560`, `linux/brcmfmac/cfg80211.c:5533-5536`, `whd/src/whd_ap.c:622-745`, `c-driver/cyw43_ctrl.c:581-588` |
| apsta | set to 1 | not restored | not touched | not touched | `embassy/control.rs:650`, `linux/brcmfmac/cfg80211.c:5505-5577`, `whd/src/whd_ap.c:622-745`, `c-driver/cyw43_ctrl.c:581-588` |
| Key clearing | none | command 268 with key_len 0; empty `sae_password` | none | none | `embassy/control.rs:641-653`, `linux/brcmfmac/cfg80211.c:5523-5529`, `whd/src/whd_ap.c:622-745`, `c-driver/cyw43_ctrl.c:581-588` |
| Event wait | none | none; 400 ms delay at the start | LINK or IF within 10000 ms after `bss` down, and again after SET_AP 0 | none; a LINK event without flags bit 0 calls the link-down callback | `embassy/control.rs:641-653`, `linux/brcmfmac/cfg80211.c:5519-5521`, `whd/src/whd_ap.c:689-695`, `whd/src/whd_ap.c:705-711`, `c-driver/cyw43_ctrl.c:398-401` |
| Other | none | closednet 0, mbss 0, regulatory restored, mpc 1, ARP/ND offload on | arpoe / ndoe = 1 when the OFFLOADS capability flag is set | IP stack interface removed | `embassy/control.rs:641-653`, `linux/brcmfmac/cfg80211.c:5538-5540`, `linux/brcmfmac/cfg80211.c:5553-5556`, `linux/brcmfmac/cfg80211.c:5571-5573`, `whd/src/whd_ap.c:738-743`, `c-driver/cyw43_ctrl.c:585-588` |

## Power save

### embassy

1. variable (set), mode 2 only — pm2_sleep_ret — u32 ms: SuperSave 2000, Aggressive 2000, PowerSave 200, Performance 20. Note: values `embassy/lib.rs:434-443` — `embassy/control.rs:356-357`
2. variable (set), mode 2 only — bcn_li_bcn — u32: SuperSave 255, others 1. Note: `embassy/lib.rs:445-454` — `embassy/control.rs:358`
3. variable (set), mode 2 only — bcn_li_dtim — u32: SuperSave 255, others 1. Note: `embassy/lib.rs:456-465` — `embassy/control.rs:359`
4. variable (set), mode 2 only — assoc_listen — u32: SuperSave 255, Aggressive 10, PowerSave 10, Performance 1. Note: `embassy/lib.rs:467-476` — `embassy/control.rs:360`
5. command (set) — SetPm = 86 — u32: 0 for None, 1 for ThroughputThrottling, 2 for all other modes. Note: `embassy/lib.rs:478-484` — `embassy/control.rs:362`

Succeeds when: None checked. `embassy/control.rs:356-362`

Fails when:

- embassy does not act on the command status: the runner only logs a warning when the CDC status is non-zero ('TODO: propagate error instead', `embassy/runner.rs:1174-1176`), so a rejected command does not stop the sequence.

### linux

1. host — store preference; stop here if the interface is not up yet — `linux/brcmfmac/cfg80211.c:3351-3363`
2. command (set) — BRCMF_C_SET_PM = 86 — u32 = 2 (PM_FAST) when enabled, 0 (PM_OFF) when disabled or for P2P client interfaces — `linux/brcmfmac/cfg80211.c:3365-3379`, `linux/include/defs.h:76-78`
3. variable (set) — pm2_sleep_ret — u32 = min(timeout, 2000) with the comparison done as unsigned. Note: sent after SET_PM and regardless of the mode — `linux/brcmfmac/cfg80211.c:3381-3384`, `linux/brcmfmac/cfg80211.c:90`

Succeeds when: Returns the result of the last set. `linux/brcmfmac/cfg80211.c:3381-3384`

Fails when:

- SET_PM error is logged; the function then still sends pm2_sleep_ret and returns that call's result (`linux/brcmfmac/cfg80211.c:3373-3384`).

### whd

1. command (set), whd_wifi_enable_powersave — WLC_SET_PM = 86 — u32 = 1 (PM1_POWERSAVE_MODE) — `whd/src/whd_wifi_api.c:3783-3800`, `whd/inc/whd_types.h:85-87`
2. variable (set), whd_wifi_enable_powersave_with_throughput — pm2_sleep_ret — u32 = (ms / 10) * 10; argument must be 10..2000 ms. Note: chip 43362 only: also 'pm_limit' (`whd/src/whd_wifi_api.c:3909-3912`) — `whd/src/whd_wifi_api.c:3881-3906`, `whd/src/whd_wifi_api.c:87-88`
3. command (set), ...with_throughput — WLC_SET_PM = 86 — u32 = 2 (PM2_POWERSAVE_MODE) — `whd/src/whd_wifi_api.c:3914-3919`
4. command (set), whd_wifi_disable_powersave — WLC_SET_PM = 86 — u32 = 0 — `whd/src/whd_wifi_api.c:3922-3938`
5. command (get), whd_wifi_get_powersave_mode — WLC_GET_PM = 85 — u32 reply — `whd/src/whd_wifi_api.c:3802-3816`

Succeeds when: Command result WHD_SUCCESS. `whd/src/whd_wifi_api.c:3799`, `whd/src/whd_wifi_api.c:3919`

Fails when:

- Delay below 10 ms -> WHD_DELAY_TOO_SHORT, above 2000 ms -> WHD_DELAY_TOO_LONG (`whd/src/whd_wifi_api.c:3893-3902`).
- Command error returned (with an assert in debug builds) (`whd/src/whd_wifi_api.c:3799`, `whd/src/whd_wifi_api.c:3919`).

### c-driver

1. decode — pm_in = 0x00adbrrm — m = mode (bits 0-3), rr = sleep-return in 10 ms units (bits 4-11), b = bcn_li_bcn (12-15), d = bcn_li_dtim (16-19), a = assoc_listen (20-23) — `c-driver/cyw43_ctrl.c:500-515`, `c-driver/cyw43.h:784-790`
2. variable (set) — pm2_sleep_ret — u32 = rr clamped to 1..200, times 10 (ms). Note: sent for every mode — `c-driver/cyw43_ll.c:2142-2148`
3. variable (set) — bcn_li_bcn — u32 — `c-driver/cyw43_ll.c:2154`
4. variable (set) — bcn_li_dtim — u32 — `c-driver/cyw43_ll.c:2155`
5. variable (set) — assoc_listen — u32 — `c-driver/cyw43_ll.c:2156`
6. command (set) — WLC_SET_PM = 86 — u32 mode: 0 none, 1 PM1, 2 PM2 — `c-driver/cyw43_ll.c:2165`, `c-driver/cyw43_ll.h:187-189`
7. command (set) — WLC_SET_GMODE = 110 — u32 = 1 — `c-driver/cyw43_ll.c:2167-2170`
8. command (set) — WLC_SET_BAND = 142 — u32 = 0 (any) — `c-driver/cyw43_ll.c:2172-2173`

Succeeds when: Returns 0 unconditionally after the sequence (`c-driver/cyw43_ll.c:2175`).

Fails when:

- Most set helpers in cyw43_ll.c are void and discard the command result (`c-driver/cyw43_ll.c:1538-1562`, `c-driver/cyw43_ll.c:1956-1960`); the only failure surfaced is a 500 ms response timeout inside cyw43_do_ioctl, which returns -ETIMEDOUT to callers that check it (`c-driver/cyw43_ll.c:1294-1325`, `c-driver/cyw43_config.h:92`).

### Differences

Differences: All four drivers set the mode with command 86. `embassy/control.rs:362`, `linux/brcmfmac/cfg80211.c:3365-3379`, `whd/src/whd_wifi_api.c:3783-3800`, `c-driver/cyw43_ll.c:2165` embassy, whd and c-driver write `pm2_sleep_ret` before command 86; linux writes it after. `embassy/control.rs:356-362`, `whd/src/whd_wifi_api.c:3881-3919`, `c-driver/cyw43_ll.c:2142-2165`, `linux/brcmfmac/cfg80211.c:3365-3384`

| Aspect | embassy | linux | whd | c-driver | Citations |
|---|---|---|---|---|---|
| Mode values sent | 0 None, 1 ThroughputThrottling, 2 all other modes | 2 when enabled, 0 when disabled or P2P client; mode 1 is used elsewhere in the driver | 1, 2 or 0, one entry point each | 0, 1 or 2 from the low 4 bits of the argument | `embassy/control.rs:362`, `embassy/lib.rs:478-484`, `linux/brcmfmac/cfg80211.c:3365-3379`, `linux/brcmfmac/cfg80211.c:4253`, `whd/src/whd_wifi_api.c:3783-3800`, `whd/src/whd_wifi_api.c:3914-3938`, `c-driver/cyw43_ll.c:2165`, `c-driver/cyw43_ctrl.c:500-515` |
| pm2_sleep_ret | mode 2 only: 2000, 2000, 200 or 20 ms by preset | every call, after SET_PM: min(timeout, 2000) | whd_wifi_enable_powersave_with_throughput only: 10..2000 ms rounded down to 10 | every mode: 1..200 units of 10 ms | `embassy/control.rs:356-357`, `embassy/lib.rs:434-443`, `linux/brcmfmac/cfg80211.c:3381-3384`, `whd/src/whd_wifi_api.c:3881-3906`, `c-driver/cyw43_ll.c:2142-2148` |
| bcn_li_bcn, bcn_li_dtim, assoc_listen | mode 2 only | not sent here | not sent here | every mode | `embassy/control.rs:358-360`, `linux/brcmfmac/cfg80211.c:3351-3384`, `whd/src/whd_wifi_api.c:3783-3938`, `c-driver/cyw43_ll.c:2154-2156` |
| After SET_PM | nothing | pm2_sleep_ret | nothing | SET_GMODE (110) = 1, SET_BAND (142) = 0 | `embassy/control.rs:362`, `linux/brcmfmac/cfg80211.c:3381-3384`, `whd/src/whd_wifi_api.c:3914-3919`, `c-driver/cyw43_ll.c:2167-2173` |
| When applied | application call only; init sets no mode | cfg80211 request; only stored while the interface is down | application call | also applied with the default preset when the first interface comes up | `embassy/control.rs:263-340`, `linux/brcmfmac/cfg80211.c:3351-3363`, `whd/src/whd_wifi_api.c:3783-3800`, `c-driver/cyw43_ctrl.c:567` |
| Presets | PowerSave: 200 ms, 1, 1, 10 (see the embassy steps for the others) | none | none | DEFAULT = PERFORMANCE = mode 2, 200 ms, 1, 1, 10; AGGRESSIVE = mode 1, 10 ms, 0, 0, 0; NONE = mode 0, 10 ms, 0, 0, 0 | `embassy/lib.rs:434-476`, `c-driver/cyw43.h:795-810` |
| Read-back | none found (unverified) | none in the set path; BRCMF_C_GET_PM is read in the wake-on-WLAN code | WLC_GET_PM (85) | four variable gets plus WLC_GET_PM (85) | `linux/brcmfmac/cfg80211.c:4252`, `whd/src/whd_wifi_api.c:3802-3816`, `c-driver/cyw43_ll.c:2178-2186` |
| Errors | command status only logged | SET_PM error logged; pm2_sleep_ret still sent and its result returned | returned; delay outside 10..2000 ms rejected | results discarded; returns 0 | `embassy/runner.rs:1174-1176`, `linux/brcmfmac/cfg80211.c:3373-3384`, `whd/src/whd_wifi_api.c:3893-3902`, `c-driver/cyw43_ll.c:2175` |

## Multicast filter

### embassy

1. trigger — network stack changes its multicast list — runner sees poll_multicast_filter_changed; init also marks it changed. Note: applied by the runner task, not by Control — `embassy/runner.rs:832-875`, `embassy/control.rs:335-337`
2. variable (set) — mcast_list — u32 count, then count x 6-byte addresses; the request buffer is fixed at name + 4 + 6*MULTICAST_FILTER_SIZE bytes and the whole list is replaced in one write. Note: unused slots are sent as zero bytes — `embassy/runner.rs:1390-1399`
3. variable (set), conditional — allmulti — u32 = 1 when the stack's list overflowed, 0 when it no longer does; only sent when the value changes — `embassy/runner.rs:1401-1410`
4. variable (get), optional read-back — mcast_list — response: u32 count, then addresses; Control::list_multicast_addresses reads up to 64 bytes. Note: the generic get helper carries the comment 'TODO this is not really working, it always returns all zeros' (`embassy/control.rs:730`) — `embassy/control.rs:657-669`

Succeeds when: None checked. `embassy/runner.rs:1390-1410`

Fails when:

- embassy does not act on the command status: the runner only logs a warning when the CDC status is non-zero ('TODO: propagate error instead', `embassy/runner.rs:1174-1176`), so a rejected command does not stop the sequence.

### linux

1. variable (set) — mcast_list — u32 count, then count x 6-byte addresses from the network device's list; exact length — `linux/brcmfmac/core.c:158-184`
2. variable (set) — allmulti — u32 = 1 if the interface has IFF_ALLMULTI, else 0. Note: the mcast_list failure branch forces 1 only when its address counter cnt is still non-zero; the copy loop counts cnt down to 0 when every address was copied (`linux/brcmfmac/core.c:170-182`) — `linux/brcmfmac/core.c:155-156`, `linux/brcmfmac/core.c:186-193`
3. command (set) — BRCMF_C_SET_PROMISC = 10 — u32 = 1 if IFF_PROMISC else 0 — `linux/brcmfmac/core.c:195-205`
4. variable (set) — arp_ol, arpoe, ndoe — brcmf_configure_arp_nd_offload(enable = not promiscuous): arp_ol u32 = BRCMF_ARP_OL_AGENT | BRCMF_ARP_OL_PEER_AUTO_REPLY when enabling, else 0; arpoe = enable only when the arp_ol set succeeded; then ndoe = enable; enabling is skipped while a soft AP is running; errors only logged — `linux/brcmfmac/core.c:206`, `linux/brcmfmac/core.c:96-136`

Succeeds when: No overall result (work-queue function); each failure is logged. `linux/brcmfmac/core.c:158-206`

Fails when:

- mcast_list failure is logged (`linux/brcmfmac/core.c:179-182`).
- SET_PROMISC returning -EBADE is logged once as unsupported on older chips (`linux/brcmfmac/core.c:198-205`).

### whd

1. argument check — address must have the multicast bit — else WHD_WLAN_BADARG — `whd/src/whd_wifi_api.c:3950-3955`
2. variable (get) — mcast_list — request buffer 4 + 10*6 bytes; reply u32 count + addresses — `whd/src/whd_wifi_api.c:3961-3970`, `whd/src/whd_wifi_api.c:57`
3. host — register: stop with success if the address is already listed — `whd/src/whd_wifi_api.c:3971-3981`
4. variable (set), register — mcast_list — u32 count+1, then the old addresses followed by the new one; buffer sized exactly — `whd/src/whd_wifi_api.c:3983-3996`
5. variable (set), unregister — mcast_list — u32 count-1, then the list without the matching address; sent only if the address was found — `whd/src/whd_wifi_api.c:4018-4050`

Succeeds when: Set returns WHD_SUCCESS. `whd/src/whd_wifi_api.c:3983-3996`, `whd/src/whd_wifi_api.c:4018-4050`

Fails when:

- Get or set error is returned. `whd/src/whd_wifi_api.c:3961-3996`, `whd/src/whd_wifi_api.c:4018-4050`
- No check against the 10-entry request size when adding an 11th address in this function (`whd/src/whd_wifi_api.c:3983-3995`).

### c-driver

1. variable (get) — mcast_list — request buffer: 'mcast_list\0' + 4 + 10*6 zero bytes; reply: u32 count then addresses. Note: station interface; MAX_MULTICAST_REGISTERED_ADDRESS = 10 (`c-driver/cyw43_ll.c:253`) — `c-driver/cyw43_ll.c:2089-2098`
2. host — edit list — add: no-op if already present, -EPERM if 10 entries; remove: swap with last entry and decrement — `c-driver/cyw43_ll.c:2101-2126`
3. variable (set) — mcast_list — u32 count + 60 bytes (always the full 10-slot buffer) — `c-driver/cyw43_ll.c:2128-2129`
4. delay — 50 ms — `c-driver/cyw43_ll.c:2130`

Succeeds when: Returns 0. `c-driver/cyw43_ll.c:2089-2130`

Fails when:

- Get fails -> its error is returned (`c-driver/cyw43_ll.c:2092-2095`).
- List full on add -> -EPERM (`c-driver/cyw43_ll.c:2117-2119`).

### Differences

Differences: All four drivers write the variable `mcast_list`: u32 count, then 6-byte addresses. `embassy/runner.rs:1390-1399`, `linux/brcmfmac/core.c:158-184`, `whd/src/whd_wifi_api.c:3983-3996`, `c-driver/cyw43_ll.c:2128-2129` embassy and linux replace the whole list from host state; whd and c-driver read the list back from the firmware and add or remove one address. `embassy/runner.rs:1390-1399`, `linux/brcmfmac/core.c:158-184`, `whd/src/whd_wifi_api.c:3961-3996`, `c-driver/cyw43_ll.c:2089-2129`

| Aspect | embassy | linux | whd | c-driver | Citations |
|---|---|---|---|---|---|
| Method | replace the whole list from the network stack's list | replace the whole list from the network device's list | get, edit one address, set | get, edit one address, set | `embassy/runner.rs:1390-1399`, `linux/brcmfmac/core.c:158-184`, `whd/src/whd_wifi_api.c:3961-3996`, `c-driver/cyw43_ll.c:2089-2129` |
| Bytes written | fixed: 4 + 6 x MULTICAST_FILTER_SIZE after the name; unused slots zero | exact length | exact length | always 4 + 60 (10 slots) | `embassy/runner.rs:1390-1399`, `linux/brcmfmac/core.c:158-184`, `whd/src/whd_wifi_api.c:3983-3996`, `c-driver/cyw43_ll.c:2128-2129` |
| allmulti | 1 when the stack's list overflowed, 0 when it no longer does; sent only on change | sent every time: 1 for IFF_ALLMULTI, or after a `mcast_list` failure while the copy counter is non-zero, else 0 | no use found in whd/src/*.c | appears only inside an `#if 0` monitor-mode block | `embassy/runner.rs:1401-1410`, `linux/brcmfmac/core.c:155-156`, `linux/brcmfmac/core.c:170-193`, `whd/src/whd_wifi_api.c:3950-4050`, `c-driver/cyw43_ll.c:1978-1997` |
| Promiscuous | not sent | command 10 = 1 for IFF_PROMISC, else 0 | not sent | not sent | `embassy/runner.rs:1390-1410`, `linux/brcmfmac/core.c:195-205`, `whd/src/whd_wifi_api.c:3950-4050`, `c-driver/cyw43_ll.c:2089-2130` |
| List limit | MULTICAST_FILTER_SIZE slots | none in the driver: the buffer is sized from the network device's count | get buffer holds 10; no check when adding an 11th | 10; -EPERM when full | `embassy/runner.rs:1390-1399`, `linux/brcmfmac/core.c:159-161`, `whd/src/whd_wifi_api.c:3961-3970`, `whd/src/whd_wifi_api.c:3983-3995`, `c-driver/cyw43_ll.c:2117-2119` |
| Argument check | none | none | address must have the multicast bit | none | `whd/src/whd_wifi_api.c:3950-3955` |
| Delay after the set | none | none | none | 50 ms | `c-driver/cyw43_ll.c:2130` |
| Follow-up | optional `mcast_list` get for read-back | ARP / ND offload setting | none | none | `embassy/control.rs:657-669`, `linux/brcmfmac/core.c:206` |

## Signal strength

### embassy

1. command (get) — GetRssi = 127 — 4-byte buffer, zero on the way out; response read as i32. Note: asserts the response length is 4; converted with from_ne_bytes — `embassy/control.rs:672-677`

Succeeds when: Response of 4 bytes. `embassy/control.rs:672-677`

Fails when:

- Panics if the response length is not 4 (`embassy/control.rs:675`).
- embassy does not act on the command status: the runner only logs a warning when the CDC status is non-zero ('TODO: propagate error instead', `embassy/runner.rs:1174-1176`), so a rejected command does not stop the sequence.

### linux

1. variable (get) — tdls_sta_info, then sta_info on failure — request: peer MAC in a brcmf_sta_info_le buffer; reply: the station record — `linux/brcmfmac/cfg80211.c:3204-3219`
2. host — use per-antenna rssi[] / rx_lastpkt_rssi[] from the record when the SCBSTATS flag is set and any antenna value is non-zero — signal = average of last-packet values over the antennas — `linux/brcmfmac/cfg80211.c:3260-3280`
3. command (get), fallback when no antenna value and connected — BRCMF_C_GET_RSSI = 127 — reached only inside the SCBSTATS block (`linux/brcmfmac/cfg80211.c:3235-3297`). brcmf_scb_val_le, memset to zero; 12 bytes as sent: sizeof(struct brcmf_scb_val_le) with val u32 at 0, ea[6] at 4 and 2 bytes of tail padding (the struct is not packed; size computed from the layout at `linux/brcmfmac/fwil_types.h:602-605`, not stated in source); reply val = RSSI in dBm — `linux/brcmfmac/cfg80211.c:3281-3296`, `linux/brcmfmac/fwil_types.h:602-605`

Succeeds when: tdls_sta_info or sta_info get succeeds (and, in the fallback, command 127 succeeds). `linux/brcmfmac/cfg80211.c:3204-3219`, `linux/brcmfmac/cfg80211.c:3281-3296`

Fails when:

- sta_info get failing -> error (`linux/brcmfmac/cfg80211.c:3215-3218`).
- Command 127 failing -> error (`linux/brcmfmac/cfg80211.c:3286-3289`).

### whd

1. precondition — interface role must be station — else WHD_BADARG — `whd/src/whd_wifi_api.c:1300-1306`
2. command (get) — WLC_GET_RSSI = 127 — 4-byte buffer, int32 reply — `whd/src/whd_wifi_api.c:1304`
3. command (get), AP-side variant — WLC_GET_RSSI = 127 — client_rssi_t: client MAC + rssi field (rounded up to 4-byte multiple); reply int32 in the first 4 bytes. Note: whd_wifi_get_ap_client_rssi — `whd/src/whd_wifi_api.c:1309-1333`

Succeeds when: Command result WHD_SUCCESS. `whd/src/whd_wifi_api.c:1304`

Fails when:

- Not in station role -> WHD_BADARG. `whd/src/whd_wifi_api.c:1300-1306`

### c-driver

1. precondition — station interface active — else -EPERM — `c-driver/cyw43_ctrl.c:724-727`
2. command (get) — WLC_GET_RSSI = 127 (public constant CYW43_IOCTL_GET_RSSI = 0xfe = 127*2) — 4-byte buffer, reply read as int32; station interface — `c-driver/cyw43_ctrl.c:728`, `c-driver/cyw43_ll.h:43`

Succeeds when: Return value 0 from the command. `c-driver/cyw43_ctrl.c:728`

Fails when:

- -EPERM when the station interface is not up; -ETIMEDOUT on no reply (`c-driver/cyw43_ll.c:1294-1325`).

### Differences

Differences: embassy, whd and c-driver read command 127 with a 4-byte buffer and take the reply as a signed 32-bit value. `embassy/control.rs:672-677`, `whd/src/whd_wifi_api.c:1304`, `c-driver/cyw43_ctrl.c:728` linux reads the variable `tdls_sta_info`, then `sta_info` when that fails, and uses command 127 only as a fallback, with a 12-byte request (10 bytes of fields + 2 padding, computed). `linux/brcmfmac/cfg80211.c:3204-3219`, `linux/brcmfmac/cfg80211.c:3281-3296`

| Aspect | embassy | linux | whd | c-driver | Citations |
|---|---|---|---|---|---|
| Primary source | command 127, 4-byte buffer, i32 reply | variable `tdls_sta_info`, then `sta_info` on failure; per-antenna values from the record | command 127, 4-byte buffer, int32 reply | command 127, 4-byte buffer, int32 reply | `embassy/control.rs:672-677`, `linux/brcmfmac/cfg80211.c:3204-3219`, `linux/brcmfmac/cfg80211.c:3260-3280`, `whd/src/whd_wifi_api.c:1304`, `c-driver/cyw43_ctrl.c:728` |
| Other form of command 127 | none | fallback: zeroed brcmf_scb_val_le, 12 bytes as sent (computed); reply val = RSSI | AP-side variant: client MAC + rssi field in the request | none | `linux/brcmfmac/cfg80211.c:3281-3296`, `linux/brcmfmac/fwil_types.h:602-605`, `whd/src/whd_wifi_api.c:1309-1333` |
| Precondition | none | fallback only when no antenna value and connected | interface role must be station | station interface active | `embassy/control.rs:672-677`, `linux/brcmfmac/cfg80211.c:3281-3296`, `whd/src/whd_wifi_api.c:1300-1306`, `c-driver/cyw43_ctrl.c:724-727` |
| Failure | panics if the response is not 4 bytes | error returned | WHD_BADARG | -EPERM, or -ETIMEDOUT on no reply | `embassy/control.rs:675`, `linux/brcmfmac/cfg80211.c:3215-3218`, `linux/brcmfmac/cfg80211.c:3286-3289`, `whd/src/whd_wifi_api.c:1300-1306`, `c-driver/cyw43_ctrl.c:724-727`, `c-driver/cyw43_ll.c:1294-1325` |
| RSSI events | none found (unverified) | a separate handler, brcmf_notify_rssi, is registered for the RSSI event and compares the reported value with stored low and high thresholds; it is not part of this read | none found (unverified) | none found (unverified) | `linux/brcmfmac/cfg80211.c:6886-6915`, `linux/brcmfmac/cfg80211.c:7027` |
