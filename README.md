# CYW43439 on the Pico W / Pico 2 W: notes on the radio firmware's host interface

The Raspberry Pi Pico W and Pico 2 W carry an Infineon CYW43439 radio. Its firmware is a closed
binary; what a host can ask it to do is documented mainly by the drivers that talk to it,
Infineon's own among them. These notes
collect that interface in one place for the part embassy's Rust driver (`cyw43`) uses, and report
what one board did when asked for things the driver does not use: monitor mode, the Wi-Fi Direct
listen state, and the events that carry received management frames.

## How to read this

**Sources.** Everything comes from public driver source or from watching a board. Nothing here was
obtained by disassembling, decompiling or searching the firmware image; its licence (Infineon
Permissive Binary License 1.0, clause 2) forbids reverse engineering except where the law permits it.
The build tag quoted below is what the running firmware prints in its own log.

| Short name | What | Version read |
|---|---|---|
| embassy | `embassy-rs/embassy`, `cyw43/src` | main at `bb6ce6898` (November 2026); the `BssInfo` row in §4 is with PR #7601 applied |
| linux | Linux `drivers/net/wireless/broadcom/brcm80211/brcmfmac` | a tree at `15bf0c75de` (2026-11-06) |
| whd | `Infineon/wifi-host-driver`, `whd_wlioctl.h` and `whd_chip.h` | `bd99da7b0`; consulted for the four records where embassy and linux differ |
| c-driver | `georgerobotics/cyw43-driver` (MIT) | `fa9627e` |
| pico-sdk | `raspberrypi/pico-sdk`, `pico_cyw43_driver/cybt_shared_bus` | `079c6f390` |
| nexmon | `seemoo-lab/nexmon`, `seemoo-lab/pico-nexmon` | master, November 2026 |

**Reference.** The `reference/` folder holds a longer, source-only reference to the same interface: 18
chapters on what the public drivers define and send, with a citation for each statement. It reports no
board results; its own README covers its conventions and the licences of its sources.

**Evidence labels.** Each claim carries one:

- `[source]` — read in the named driver; not checked on hardware.
- `[board ×N]` — observed on hardware in N separate trials (a trial is one boot of a test firmware).
  Where one boot repeated a step, the label says so ("×1, three rounds").

**The hardware.** One Pico 2 W, SPI bus, the Wi-Fi firmware build embassy ships: `7.95.61 (abcd531 CY)`
as its start-up log reports (`RTE (SDIO-CDC) 7.95.61 (abcd531 CY) on BCM43439 r5`). The c-driver file
this build comes from is named `wb43439A0_7_95_49_00_combined.h`; the name and the tag differ. One board and
one firmware build (two other builds were run once each for the monitor burst and pool figures only, §7):
treat every `[board]` result as "this happened here", not "this is how the chip behaves".

Upstream `cyw43` has no public call for arbitrary commands, raw events or raw data-channel frames.
The trials used a small diagnostics patch to the driver, included here with an example program
(the ten files in `patches/`, exported with `git format-patch` against embassy main `bb6ce6898`; apply
them in order with `git am`); it is not upstream and not proposed for upstream. Every event count in these
notes was taken by that patch after the driver's packet-validity checks and before its own event mask
and two-entry event queue.
The trials themselves ran in a larger test firmware (with Bluetooth) that is not included. The
bus-status sampling of §7 is the fourth patch (a probe in the driver's main loop that also logs the
raw credit byte and unparsed packets); a second example, `wifi_monitor_credit`, runs the monitor
sequence with it, without Bluetooth, and produced the credit figures quoted in §7; a third,
`wifi_monitor_variants`, with the sixth patch's knobs, ran the three driver-side variants; a fourth,
`wifi_keyhole`, reads the firmware's own counters and memory-use line around the stall; a fifth,
`wifi_teardown`, reads that line after each step of undoing monitor mode. A sixth,
`wifi_downup`, does the same with no Wi-Fi Direct state and across an interface down and up. The probe
consumes the driver's cached status word, so it adds bus traffic of its own, and it was running in
every monitor-mode run reported here except those added on 2026-11-22 (the last subsection of §7),
which used hooks that are not among the patches and say for themselves where the probe ran. The first
example (`wifi_interface_probe`), built against upstream embassy with only the patch and without
Bluetooth, was run once; for the seven variables it reads, the listen-state sequence and a single
monitor window it gave the same results as the test firmware (it runs no scans). Every run, test
firmware and examples alike, used the diagnostics patch: none used the unmodified upstream driver.
The radio-restart result in §7 comes from the test firmware, whose restart code is not in the patches.
The examples print the firmware's `counters` record as hex; the field values quoted in §7 were decoded
by hand against whd's `wl_cnt_ver_ten_t`. All of them use the board-settings file embassy ships for
the Pico W, as embassy's own Pico 2 W example does. The firmware's text log was off in the test firmware and on in
the examples. The test firmware never
called the driver's power-management function; the power-save mode read back as 0 (off) `[board ×1]`.

## 1. The firmware

| Part | Size | Label |
|---|---|---|
| ROM inside the chip | 640 KiB | `[source]` as published in nexmon's build definitions for 7.95.49; not a measurement, not confirmed for 7.95.61 |
| Chip RAM | 512 KiB | `[source]` embassy (`chip_ram_size`); nexmon gives the same |
| Wi-Fi image, loaded at every boot | 231,077 bytes | measured file size |
| Bluetooth patch | 6,164 bytes | measured file size |
| Regulatory table (CLM) | 984 bytes | measured file size |

The c-driver also ships
a Wi-Fi-only build, which nexmon names `7_95_49_2271bb6`. That is the build the nexmon patches target, so nexmon's
patch addresses do not apply to the build embassy uses.

## 2. Framing

Every packet on the bus starts with a 12-byte header (SDPCM: length, inverted length, sequence,
channel, flow control). Three channels follow it `[source]`:

- **control** — a command and its reply, behind a 16-byte header (`cmd`, `len`, `flags` + `id`, `status`).
- **event** — a 4-byte BDC header, an Ethernet header, a 10-byte Broadcom event header and a 48-byte
  event message, both with **big-endian** fields, then event data.
- **data** — Ethernet frames behind a BDC header.

## 3. Commands and named variables

Upstream embassy's list of commands ("ioctls") has 282 entries, of which 18 appear in its code
`[source]` (the diagnostics patch adds four more: 9, 10, 107, 108): Up (2), Down (3), SetInfra (20),
SetAuth (22), SetSsid (26), SetChannel (30), Disassoc (52), SetAntdiv (64), SetPm (86), SetGmode (110),
SetAp (118), GetRssi (127), SetWsec (134), SetBand (142), SetWpaAuth (165), GetVar (262), SetVar (263),
SetWsecPmk (268).

A named variable ("iovar") is a NUL-terminated name followed by its value, sent with GetVar or
SetVar. A name starting `bsscfg:` takes a 4-byte interface-config ("bsscfg") index before the value.

Status codes seen below: 0 accepted; −23 unsupported (linux `BRCMF_FW_UNSUPPORTED`); −14 buffer too
short (`BCME_BUFTOOSHORT`, position 14 in linux's error-name table); −1 a general error. The
firmware's own log names the first two the same way ("Unsupported", "Buffer too short"). Values are
little-endian unless stated.

### Three things about reading variables

- **An unknown name and an unsupported one return the same status.** A made-up name returned −23,
  the same as twelve real names from linux that this build rejects `[board ×2]`. The firmware's text
  log does tell them apart: for the made-up name it printed `unable to find iovar`.
- **The reply length does not tell you the value's size.** A 4-byte value read with a 48-byte buffer
  came back as 48 bytes: the value, then leftover bytes of the request. That is how this command
  protocol works (the reply length is taken from the request's header), not a fault, but the caller
  has to know the value's size. One exception among 35: `bus:txglom` returned 4 bytes `[board ×1]`.
- **The event mask reads back as 16 bytes.** embassy writes 24, the c-driver 19; reading
  `event_msgs` returned 16 bytes of mask followed by zeros `[board ×1]`.

### What this build answered `[board ×1]`

50 names taken from the public drivers, read once with a 48-byte buffer.

- **Accepted (35):** `ver`, `country`, `cur_etheraddr`, `chanspec`, `event_msgs`, `apsta`, `allmulti`,
  `mcast_list`, `bus:txglom`, `ampdu_ba_wsize`, `ampdu_mpdu`, `ampdu_rx_factor`, `pm2_sleep_ret`,
  `bcn_li_bcn`, `bcn_li_dtim`, `assoc_listen`, `2g_mrate`, `clmload_status`, `mfp`, `sup_wpa`, `wpa_auth`,
  `wsec`, `nmode`, `mimo_bw_cap`, `rxchain`, `txstreams`, `qtxpower`, `arp_hostip`, `arpoe`, `arp_version`,
  `wme_ac_sta`, `wowl`, `wowl_cap`, `wowl_wakeind`, `assoc_info`.
- **Exist, but the reply needs more than 48 bytes (status −14):** `cap`, `clmver`, `chanspecs`.
- **Rejected (status −23):** `wlc_ver`, `scan_ver`, `vhtmode`, `txbf_bfe_cap`, `txbf_bfr_cap`,
  `rsdb_mode`, `toe_ol`, `okc_enable`, `tdls_enable`, `wlfc_mode`, `pfn`, `pfnmem`.

`p2p_disc` cannot be read (−23) but can be written; `p2p_dev` reads only while discovery is on (§6).

## 4. Record layouts, compared with linux

Fourteen records embassy defines were compared field by field with linux `[source]`.

| embassy | Size | linux | Result |
|---|---|---|---|
| `SsidInfo` | 36 | `brcmf_ssid_le` | same |
| `ScanParams` | 76 (72 fixed, one channel entry, 2 pad) | `brcmf_escan_params_le` (v1) | same |
| `ScanResults` | 12 | `brcmf_escan_result_le` head | same |
| `BssInfo` | 124 at `bb6ce6898`; 128 with PR #7601 | `brcmf_bss_info_le` (128) | **wrong at `bb6ce6898`**, see below |
| `CountryInfo` | 12 | `brcmf_fil_country_le` | same |
| `SaePassphraseInfo` | 130 | `brcmf_wsec_sae_pwd_le` | same |
| `PassphraseInfo` | 68 | `brcmf_wsec_pmk_le` | differs: key field 64 bytes in embassy and the c-driver, 65 in whd's `wsec_pmk_t`, 128 in the linux tree cited (older kernels differ) |
| `DownloadHeader` | 12 | `brcmf_dload_data_le` | same |
| `CdcHeader` | 16 | `brcmf_proto_bcdc_dcmd` | same bytes |
| `EventHeader` | 10 | `brcm_ethhdr` | same |
| `EventMessage` | 48 | `brcmf_event_msg_be` | same |
| `EventMask` | 28 | index + mask | mask length varies: embassy 24, c-driver 19, whd 16 (`WL_EVENTING_MASK_LEN`) |
| `SharedMemData` | 32 | `sdpcm_shared_le` | differs from linux after the 7th field (linux: a 32-byte tag); matches whd's record, which has `fwid` there |
| `SharedMemLog` | 16 | `rte_log_le` | 4th field differs from linux (a pointer); matches whd's `hnd_log_t` (`out_idx`) |

**The `BssInfo` bug.** At `bb6ce6898` embassy's record is packed to 2 bytes and has no padding before
`ie_length`, where the C record has two bytes. `ie_length` and `snr` are therefore read two bytes
early. (The C record is also padded at the end to 128 bytes; embassy's is 124.) Fix: embassy PR #7601 (open at the time of writing). On the
board, the record's own length minus `ie_offset` equalled `ie_length` rounded up to a multiple of 4
on 1441 of 1441 sampled scan results with the fix applied.

Of the remaining differences from linux, two (`SharedMemData`, `SharedMemLog`) match Infineon's own
driver, so embassy follows the vendor's layout there; linux's differs. That
leaves `PassphraseInfo`, where three sources give three key sizes (64, 65, 128); it is not shown to
be a bug, since the firmware accepts embassy's 68-byte record when joining networks. The event mask's
16-byte read-back (§3) agrees with whd's length.

## 5. Events

embassy lists 144 event codes (numbers 0–189 with 46 unused). At start-up it enables all of them and then switches off
RADIO (40), IF (54), PROBREQ_MSG (44), PROBREQ_MSG_RX (137), PROBRESP_MSG (71) and ROAM (19). That
mask is the firmware's filter. Separately, the driver's own code handles nine events (in its runner
and its join and scan code) and discards the rest `[source]`. Event names here are embassy's;
linux spells two of them `P2P_PROBEREQ_MSG` and `PROBERESP_MSG`.

### What the firmware sends while scanning `[board ×1]`

With every event enabled and passive scans running back to back, eleven minutes produced two codes
only: 7,953 scan results (69) and 86 PROBREQ_MSG (44). RADIO, IF, ROAM and PROBRESP_MSG never fired
in that state. No transmitter of action frames or Wi-Fi Direct probes was known to be present.

### Probe requests as events `[board ×2]`

- **PROBREQ_MSG (44)** fires for probe requests from nearby devices, alongside scanning (scans
  completed at the same rate as before, about 34 a minute). Its data is the whole 802.11 frame from the frame-control field, with nothing in
  front: no signal strength, no channel. The sender is also in the event message's address field.
- **P2P_PROBREQ_MSG (72)** fires for Wi-Fi Direct probe requests while peer-to-peer discovery is on
  (§6) `[board ×1: 57 events, 11 decoded]`. Its data starts with the 16-byte big-endian record linux calls
  `brcmf_rx_mgmt_data`, then the whole frame:

  | Field | Size | Observed |
  |---|---|---|
  | `version` | u16 | 1 |
  | `chanspec` | u16 | `0x1001`, `0x1006` — the channel the frame was heard on |
  | `rssi` | u32, signed | −17 to −25 dBm with the sender at arm's length |
  | `mactime` | u32 | rose by about 70 million in 70 s: microseconds, apparently since the radio started |
  | `rate` | u32 | `0x0001000c` (meaning of the upper half not known) |

- **Each such frame is reported twice** (counts were exactly double event 44's, samples came in
  identical pairs). linux's handler says the firmware sends one per config index and drops the copy
  for index 0; the config index was not recorded here.
- It also arrived in the middle of a scan while discovery was on.
- An ordinary probe request (not Wi-Fi Direct) raised event 44 only. The signal-strength record is
  available for Wi-Fi Direct probes, not for probe requests in general.

### Fields an event does not define are not meaningful `[board ×2]`

The address field of the listen-complete event (55) contained bytes that were not an address (text
from an earlier request, in one case). Do not read fields the event does not document.

## 6. The Wi-Fi Direct listen state `[board ×8]`

linux uses this to sit on one channel for a set time `[source]`. The same sequence was accepted here, without
linux's interface down/up and without its `wsec` write:

1. `p2p_disc` = 0.
2. `p2p_da_override` = a 6-byte device address. linux requires it to differ from the primary one;
   the address used here was the device's own with the locally-administered bit set.
3. `p2p_disc` = 1. The firmware raises an IF event (54) whose 5 data bytes are: interface, action
   (1 add / 2 delete), flags, config index, role. (embassy switches event 54 off at start-up; it has
   to be enabled again to see this.)
4. Read `p2p_dev` to get the config index (1 here).
5. `bsscfg:p2p_state` with value: index u32, then state u8, one pad byte, chanspec u16, dwell-ms u16.
   State 0 is SCAN, 1 is LISTEN. A chanspec encodes channel, width and band: `0x1006` is channel 6,
   20 MHz, 2.4 GHz. A 5 s listen ("dwell") there is chanspec `0x1006`, dwell 5000.
6. Each dwell ends with a P2P_DISC_LISTEN_COMPLETE event (55).
7. To leave: `bsscfg:p2p_state` SCAN, then `p2p_disc` = 0.

Ordinary scans returned normal results between dwells. One TXFAIL event while a phone was searching
suggests the device transmits in this state (most likely a probe response). A phone's Wi-Fi Direct
screen, open during one trial, did not list it.

## 7. Monitor mode on the unpatched firmware

Described in an open pull request on `seemoo-lab/pico-nexmon` (#1, 2023): set `allmulti` to 1 and
send command 108 (SetMonitor) with value 1. Command 107 reads the setting back. The c-driver carries
the same two calls, disabled, and an open issue there (`georgerobotics/cyw43-driver` #20, 2022)
reports from two users what is measured below: data stops unless the host keeps sending commands,
and commands then time out. That issue predates the firmware image used here.

- **The command is accepted on build 7.95.61 and frames arrive** `[board ×4]`. It is not a documented
  feature of this firmware. Raw 802.11 frames arrive on the data channel, starting
  at the frame-control field with no extra header. Whether a trailing checksum is included was not
  checked.
- **It delivers frame types a scan never reports**, action frames among them `[board ×3]`.
- **Scans returned nothing while it was on** `[board ×2]`, and in the 15 s after a scan monitor
  delivered 0 frames in one trial and 3 in the other. With monitor off again, scans returned normal
  results (below).
- **It can be aimed.** Parking the radio with the listen state (§6) on channel 6 and then switching
  monitor on delivered frames received while the radio was parked there, including frames from a
  transmitter known to be on channel 6 `[board ×3]`.
- **Delivery stalls after 30 to 32 frames** `[board ×10+]`. The first measured window after switching
  monitor on (15 s) counted exactly 32 frames on the data channel in fourteen trials, 31 in one, and
  30 in three arranged differently (one of them with no listen state); one 6 s window counted 23
  (below). Several used the upstream driver plus the patch, without Bluetooth. All frames on the data channel are counted, of any kind,
  from the moment the monitor command's reply arrives; frames before that are not in the count.
  (Later runs put the burst itself at exactly 30; see "What the limit is" below.)
- **After that, about one frame arrived per command the host sent** `[board ×4]`. In eleven later
  phases with monitor on, the frame count equalled the number of commands sent in the phase in nine
  and was off by one in two; most phases had three commands and three frames. Commands were the only thing the host sent in those
  phases, so this does not separate "per command" from "per anything the host sends".
  (Since separated: a plain data packet does the same; below.)
- **Commands then stop getting through** `[board ×5]`. Three trials of the test firmware ended with a
  command that never returned, and the board was reset by its watchdog (Bluetooth was still being
  serviced each time). A fourth run, without Bluetooth, stopped at the first command after the burst,
  straight after two 1,040-byte reads of the firmware's counters; its cause was not recorded. A fifth
  hang was host-side (the trap below).
- **The firmware stops raising the send limit** `[board ×3]`. Every packet header carries a credit byte:
  the highest sequence number the firmware will accept from the host. Normally it runs about 15 ahead
  of the driver's sequence number and rises with each reply. With monitor on it stopped within the
  first window: in each later window every header that carried credit carried the same byte (40 in a
  run with the upstream driver plus the patch and no Bluetooth, 41 with Bluetooth), while the driver's sequence
  number climbed by one per command. In an earlier trial the two met, the driver logged that it had
  no credit, and the next command was never sent: the proximate cause of that hang, about 15 commands
  after the burst. The other two test-firmware hangs came at a similar point but their sequence
  numbers were not recorded. No packet read during the stall failed to parse, and the frozen value is the byte the
  firmware sent, not something the driver derived.
- **Commands and scans recover when the mode is undone; frame delivery does not.** With monitor
  off, scans returned normal results `[board ×5]`. The credit byte moved by one when monitor was
  switched off and resumed rising once the listen state and discovery were switched off `[board ×2]`;
  in the teardown runs below it rose at each undo step. Switching monitor on again did
  not bring a second full burst (see the buffer counts below).
- **Nothing was left waiting on the bus** `[board ×3]`. With the driver's task sampling its cached copy
  of the bus status word every 100 ms, "packet available" showed in 0–3 of about 150 samples per
  stalled window, and reading on a timer delivered no more frames than before. That excludes a packet
  sitting undrained. It does not by itself show the firmware stopped offering packets, since a healthy
  bus also rarely shows the bit. The power-save mode read back as 0 and the counting code has no
  limit of 32.
- **Three driver-side variants were tried once each and did not change the first-window count**
  `[board ×1 each, no Bluetooth, probe running]`. The driver's last bring-up write sets a packet-function watermark of 32,
  the same number as the burst: with that write changed to 16 and to 64 the first window still
  counted 32 (the value was not read back). The driver acknowledges only one interrupt-register bit
  where the c-driver and whd acknowledge every bit they read: acknowledging every bit read, after the
  read, gave the same count and the same frozen credit byte. A "poke" of the bus core's mailbox on
  every 100 ms sample (other drivers poke on a stall, on SDIO) made the firmware answer each poke with
  a packet the driver logged as an event with an unexpected type, not a data frame, each carrying the
  frozen credit byte; the first window again counted 32, and that run's second window never
  reported (not investigated). The pool was not read in these runs. Not
  tried: a host driver other than embassy's on this board, a data packet from the host in place of a
  command (since tried, below), and the probe switched off.
- **The firmware's own free-buffer figure falls to 4 of 50** `[board ×1, no Bluetooth]`. whd's header
  defines two named variables, `counters` and `memuse`, that none of the drivers read here (embassy, the c-driver, whd, linux) calls;
  this build answers both. They are ordinary run-time queries by name, like any other variable in §3.
  `memuse` returns one line of text (heap free, then the pool figure). It
  read "Packet pool: 33 of 50 available" before monitor was switched on and
  "Packet pool: 4 of 50 available" after the window in which 32 frames were delivered. Over the same
  window the `counters` record (version 10, laid out as whd's `wl_cnt_ver_ten_t`) showed `unchained`
  0 → 32, `rxnobuf` ("rx out of buffers errors") 1 → 36, `rxf0ovfl` ("receive fifo 0 overflows")
  0 → 1,327, while receptions started rose by about 1,390 and beacons from other networks by 193.
- **The listen state is not needed for this** `[board ×1, no Bluetooth]`. With no Wi-Fi Direct state at
  all (`allmulti`, then SetMonitor, then no commands for 15 s) 30 frames arrived and `memuse` went
  from 17 of 50 to 4 of 50. (Without Bluetooth the figure is 17 at start-up and read 33 once the listen
  state was set up; with Bluetooth it read 17 before monitor with the listen state set up.) The figure does not count delivered frames: it fell by 13 for 30 frames here and by 29 for 32
  frames above, and ended at 4 both times. (Measured since: it falls one per frame until it reaches 4,
  and delivery continues; below.) Why 4, and where the other buffers are, is not known.
- **The figure stays at 4 of 50** `[board ×1, three rounds, no Bluetooth]`. Switching monitor off,
  `allmulti` off, the listen state off and discovery off, running a scan and waiting 5 s left it at
  4 of 50 at every step, and through two further rounds. Later monitor sessions in that boot delivered 4
  frames each with the figure reading 4; in two earlier boots of the same test, where the figure was
  not read, the second session delivered 13. Taking the interface down and up (commands 3 and 2, both accepted) did not change it either
  `[board ×1, no listen state]`: still 4 of 50, and 4 frames from the next session. The firmware goes
  on answering commands and returning normal scan results with 4 buffers.
  Restarting the radio resets it `[board ×1, four rounds, with Bluetooth, test firmware]`: after an
  in-place restart (power cycle and firmware reload, about 0.8 s, 1.6 s with the Wi-Fi setup redone)
  the figure read 17 of 50 again and a new monitor session delivered 32 frames, four times running.
  On this board that was the only way found to get a second full burst.
- **A burst fills in about 0.6 to 3 s** `[board ×1, five rounds, with Bluetooth, test firmware]`. With the radio parked before monitor
  was switched on, 30 frames arrived within 0.60 s on channel 11 and 1.07 s on channel 1 (almost all
  beacons) and within 2.78 s on channel 6 (mostly other stations' data and control frames). Two
  other rounds on channel 6 (the first of the boot, and one after a restart) delivered fewer (23 over 5.3 s; 7 in 0.8 s and
  then none), unexplained.
  The burst takes whatever is on the air in arrival order.
- **What is and is not established** (one board, one firmware build). Observed: with monitor on,
  30 to 32 frames reach the host and then delivery all but stops; the firmware's free-buffer figure
  reads 4 of 50 from then on, through every undo step tried (monitor off, `allmulti` off, leaving the
  listen state, discovery off, interface down and up, a scan, a wait) and until the radio is
  restarted; later sessions deliver a few frames. The burst and the figure were seen with and without
  Bluetooth and with and without the listen state. Measured only with the listen state set up: the
  firmware's out-of-buffer and overflow counters rising across the burst, and the send-limit byte
  staying at one value while monitor is on. Not established: where the buffers are; why the figure does not recover once frames have been delivered; why the burst
  is 30 whatever the starting figure; whether the low pool causes the stall or both follow from
  something else, such as a queue toward the host that stops moving; and whether some host action
  none of those drivers shows would release it (a host packet releases one frame within the send
  credit, below; nothing found raises the credit). Two further readings, not shown: scans returning
  nothing while monitor is on fits there being no buffer for a result event; the action-frame events
  at switch-off (§8) fit something being released then. Of the hangs, one was the host running out of
  send credit and one was host-side; the others have no recorded cause. The measurements added
  below ("What the limit is, and what moves it") refine this paragraph: the burst is 30, the figure
  falls one per delivered frame until it reaches 4, and each host packet lets one more frame out
  within the send credit. They do not explain any of it.
- **A host-side trap** `[board ×1]`: monitor mode can deliver frames longer than an Ethernet frame
  (one of 1574 bytes was seen). A driver whose receive path assumes Ethernet-sized packets must be
  checked for that before using monitor mode.
- **No signal strength or channel comes with a frame** `[board ×4]`. That needs the nexmon firmware patch
  (GPL-3.0, for the Wi-Fi-only 7.95.49 build).

### What the limit is, and what moves it (added 2026-11-22)

Eight further boots on the same board. Five ran a test firmware with Bluetooth running, one boot per
bullet marked `[board ×1, … rounds]` below (settings; the 40-round burst run; host actions and the pool
readings, one boot; packets past the limit; the pump); in those the radio was restarted in place after
every round, so each round ("round" = one monitor session) starts from freshly loaded firmware. The
build comparison is a separate example program without Bluetooth, one boot per image. Channel and
listen state are given per bullet. The driver in these boots reads the bus when the radio raises its
interrupt line and after each packet it sends; the status-sampling probe of the patches ran in
the host-action rounds, the limit boot and the three build-comparison boots, and did not read packets. **None of this can be reproduced from the repository as it stands** (see "Code" at the
end of the list).

- **No setting tried, once each, changed the outcome** `[board ×1, seven rounds]`. Without the listen
  state: `mpc` (reads 1; set to 0 and read back as 0), SetMonitor values 2 and 3 (each accepted and
  read back), and `mpc` 0 with value 3 each gave 30 frames in the first 15 s, 1 in the next 15 s
  and `memuse` 17 → 4 of 50, the same as the two control rounds. With `mpc` 0 and the listen state
  on channel 6: 32 and 4 (the listen state's own commands account for the extra frames, below).
  Frames looked the same with values 2 and 3 (beginning at the frame-control field), so nothing
  here shows the firmware treats them differently from 1. `mpc` governs radio power-down when
  idle and was a weak candidate.
- **Two other released builds gave the same burst and pool figures, once each**
  `[board ×1 each, no Bluetooth, no listen state]`. The same program was run with three images as
  published (the c-driver's converted from its C-array form to a binary file, otherwise unaltered),
  each with the regulatory table published beside it and the same board configuration file, each
  reporting its own version and build date through `ver`: 7.95.61 (abcd531 CY, January 2023, the
  build used everywhere else in these notes, from embassy's `cyw43-firmware`), 7.95.49 (2271bb6 CY,
  November 2021, from the c-driver's `w43439A0_7_95_49_00_combined.h` at `fa9627e`) and 7.95.75
  (0a0104c CY, November 2023, `cyfmac43439-sdio.bin` from `RPi-Distro/firmware-nonfree`, branch
  `trixie`). Each: `memuse` 17 of 50, 30 frames in 15 s, 4 of 50, 1 frame in the next
  15 s; then, with monitor switched off, a scan returned results. Nothing else in this subsection
  was run on the other two builds.
- **The burst was 30 frames in 40 of 40 rounds, whatever the frames' size**
  `[board ×1, 40 rounds, listen state on channel 11]` (14 to 1,404 bytes seen; at most four
  1,404-byte frames in one burst). 30 frames arrived within 66 to 485 ms of the monitor command
  being sent (median about 268 ms) and then none until one more arrived with the next command, 4 s
  later. During these rounds a second radio on the same channel transmitted marked broadcast data
  frames of 60, 400 and 1,400 bytes at 5 to 200 a second, in timed phases; up to 19 of a round's
  first 30 frames were its frames. Control frames of 14 bytes and data frames of 1,404 bytes each
  counted as one; the bytes in a burst of 30 ranged from 2,228 to 13,192. `memuse` read 17 before
  and 4 after in every round. Shorter bursts also occur: 29 in one of the 18 host-action rounds
  below, a 15 s window of 29 in the pump run, and the 23 and 7 above; unexplained. The earlier
  counts of 32 fit 30 plus the two listen commands sent after the burst in each 15 s window (the
  first listen command goes out during the burst); the earlier 31 is not accounted for, and those
  trials did not log their host traffic per window.
- **Each command or small data packet the host sent was followed by exactly one more frame**
  `[board ×1, 18 rounds, listen state on channel 11]`. After the burst, five actions 150 ms apart,
  three rounds of each:

  | Host action | Frames that arrived |
  |---|---|
  | none | 0, 0, 0 |
  | five 4-byte read commands | 5, 5, 6 |
  | five small write commands | 5, 5, 5 |
  | five reads of `memuse` (512-byte reply buffer) | 5, 5, 5 |
  | five 60-byte data packets (broadcast, an experimental ethertype) | 5, 5, 5 |
  | ten such data packets | 10, 10, 10 |

  (In the round that shows 6, the burst had counted 29; and one pump round below brought 12 frames
  for 15 packets. So: 17 of these 18 rounds matched exactly.) A data packet gets no command reply,
  so the frame is not carried out by one; whether the firmware returns some other packet for it was
  not recorded. The driver reads the bus after every packet it sends, so a frame merely waiting for
  a read would look the same; against that, the "none" rounds delivered nothing although the driver
  reads whenever the radio raises its interrupt, reads forced on a timer delivered nothing extra in
  an earlier run ("Nothing was left waiting on the bus", above), and in the next bullet thousands
  of sends, each followed by a read, brought no frames once the limit was passed. It is not
  "anything the host does" either: the mailbox poke above brought no data frames. The data
  packets used send credit: the driver's sequence number rose by one per packet while the
  firmware's limit stayed where it was.
- **Packets sent past the frozen limit released nothing** `[board ×1, eight rounds, listen state on
  channel 11]`. At the end of a burst the limit was 16 ahead of the driver's sequence number (40
  against 24; 41 against 25 in one round). With the driver told to ignore the limit, 60 packets
  queued at 20 ms intervals (two rounds), 300 at 5 ms (two), 1,000 back to back (two) and 4,000 at
  5 ms (one) each let out exactly 16 frames. The credit byte stayed at one value in every header
  the firmware sent meanwhile (21 to 371 per round: the 16 frames plus headers whose kind was not
  recorded; the control round saw none). In the longer
  rounds the driver's 8-bit sequence number wrapped and re-used numbers inside the limit without
  releasing more frames, so the firmware is not simply admitting any packet whose number is inside
  the window; whether it discards the rest by sequence number or has 16 receive slots that are
  never refilled is not shown. A command written to the bus afterwards, itself numbered outside the
  16 the firmware had admitted, got no reply within 3 s in all seven rounds; that is the same refusal, not a separate
  failure. The radio restart recovered every time. The control round (no packets) delivered 0
  frames and its command was answered.
- **So in these controlled rounds a session delivered 30 frames, then one per host packet until the
  send credit left at the end of the burst was used up (16 in these runs): 46 at most.** With the
  pump below: 46, 46, 46 and 41. This describes most rounds, not all: see the short bursts and the
  unequal rounds noted above and below. (46 is also the pool's 50 less the 4 it never goes below, but the pool had only 17
  free at the start; treat that as coincidence unless shown otherwise.)
- **The free-buffer figure falls one per delivered frame until it reaches 4, and delivery then
  continues** `[board ×1, 18 rounds, same boot as the host-action rounds]`. One `memuse` read at a
  set time after the monitor command: with 3 frames delivered it read 14; with 7, 10; with 8 to
  10, 7 to 9; with 11, 6; with 13 or more, 4. Delivery then went on to 30 with the figure at 4. A
  read made while 13 or fewer frames had been delivered did not add a frame (eight rounds, total
  30); a read made with 18 to 28 delivered, or after the burst, added one (ten rounds, total 31).
  So the figure fell by one for each of the first 13 frames, from a start of 17, and did not recover;
  whether those buffers are the delivered frames' own is not shown. This was measured from that
  start only (from 33, without Bluetooth, the figure had fallen by 29 over
  a window of 32 frames, above). With a start of 17 the 30-frame limit is not the figure reaching 4.
- **The restart workaround, with a pump** `[board ×1, four rounds, listen state on channel 6]`.
  Before each restart the driver sent up to 16 of the 60-byte data packets, keeping to the send
  limit: 13 to 15 were sent and the rest were held back by the limit (the same commands preceded the
  pump each round, so why the number varied was not looked into). Frames per session: 46, 46, 46
  and 41 (in the first three, one frame more than packets, probably the preceding `memuse` read's); the 15 s windows before the pump had counted 32, 31, 31 and 29. In the fourth round 15
  packets brought 12 frames; not looked into. Restart and `memuse` were as before (about 1.6 s with
  the Wi-Fi setup; 17 → 4 → 17). The pump uses up the send credit, which is the state in which
  commands hang (above), so it is only of use immediately before a restart.
- **What these runs do not show:** why the free-buffer figure does not recover; why 30; anything
  on a second board; the per-packet rule or the limit on the other two builds. The test
  transmitter's frames were identified by their transmitter address in the frames the board
  delivered; the transmitting interface did not report its own transmissions.
- **Code.** These runs used a local test firmware, a script for the second radio, and driver hooks
  that are not among the ten patches: a count of frames carrying a marker address, a request to
  send small data packets, a switch to ignore the send limit, and the restart-with-pump loop. The
  build comparison used a variant of the `wifi_downup` example that reads its image from another
  file. Until those are published, this subsection is a report, not something a reader can rerun.

### Example: Wi-Fi Aware publish frames

A phone publishing a Wi-Fi Aware service was readable this way. The frames are public action frames
to the group address `51:6f:9a:01:00:00`, vendor-specific with the Wi-Fi Alliance type `0x13`, and
carry a service descriptor whose 6-byte service id is the start of SHA-256 of the service name; the
service-specific payload was in clear. The same phone appeared in ordinary scan results as a network
with an empty name on channel 6 and an address starting `50:6f:9a:01` (its Wi-Fi Aware cluster).

## 8. Action frames as events: what was tried

linux handles one event for received action frames, ACTION_FRAME_RX (75): the 16-byte record of §5,
then the frame body. It also lists ACTION_FRAME (59) without using it `[source]`. Either would be preferable to
monitor mode. All rows but the first had a Wi-Fi Aware publisher next to the board:

| Configuration | Events 59 / 75 |
|---|---|
| Ordinary scanning, all events enabled, no known transmitter, 11 min | none `[board ×1]` |
| Listen state on channel 6 | none `[board ×2]` |
| Listen state + `allmulti` | none `[board ×1]` |
| Listen state + promiscuous (command 10, read back as 1) | none `[board ×1]` |
| Monitor on, start a listen dwell, monitor off at once; 7 cycles and one control without monitor | none `[board ×1]` |
| Monitor on for 30 s or more with the listen state, then monitor off | a few after the switch `[board ×2]`; timed to the instant of the switch `[board ×1]` |

In the trial where their contents were captured, event 75 carried what linux describes — the record
(channel 6, −39 dBm, `rate` `0x00010060`) and the body — and event 59 carried the body alone, from
the category byte; each frame was reported twice. The samples from that switch were stamped within
microseconds of each other. Given §7, these are probably frames that were queued while monitor was on
and released when it was switched off; that reading is untested. None of the six configurations tried keeps these events coming. Not tried, and worth trying: a
Wi-Fi Direct peer sending action frames addressed to the device (a Wi-Fi Aware publisher sends to a
group address); adding that group address to `mcast_list`; an event mask on the peer-to-peer config
index (the mask here was set on index 0 only); a fixed channel without the listen state.

## 9. The Bluetooth transport `[source]` embassy and pico-sdk

Bluetooth HCI does not use the packet channels. It goes through two 4 KiB ring buffers inside the
Wi-Fi firmware's RAM, reached by backplane reads and writes. embassy and the pico-sdk agree on every
item:

| Address | Use |
|---|---|
| `0x19000000 + 0x640894` | write 3 to wake the Bluetooth side before loading its patch |
| `0x18000C7C` | controller status: bit 8 awake, bit 24 firmware ready |
| `0x18000D6C` | host control: bit 1 data valid (toggled per packet), bit 17 wake request, bit 24 host ready |
| `0x18000D68` | read once: base address of the ring-buffer block |

Block layout from that base: host→controller ring at `0x0000`, controller→host ring at `0x1000`,
then four 32-bit indexes at `0x2000` (host write), `0x2004` (controller read), `0x2008` (controller
write), `0x200C` (host read). A record is a 4-byte header (3 bytes of length, not counting the HCI
type byte, then the HCI type) and a payload padded to a multiple of 4. The pico-sdk source comments
that the power-up address "is specific to 43012B0"; both drivers use it on the 43439.

A failure mode of this transport on long runs, and a way to recover from it without a reset, is
described in a comment on embassy issue #7081 (an open issue reporting the same symptom).

## 10. Bring-up order `[source]`, simplified

The SPI path, in outline; bus-specific steps (the packet watermark write, waiting for the packet
function to become ready, interrupt enables) are left out. Read `runner.rs` for the exact sequence.

1. Bus check: read the test register until `0xFEEDBEAD`; write and read back `0x12345678`; set the bus
   control register.
2. Request the low-power (ALP) clock; wait for it; clear the request.
3. Read the chip id at `0x18000000`.
4. Disable the Wi-Fi core; reset the RAM core.
5. Write the Wi-Fi image to chip RAM at address 0 and verify it.
6. Write the board settings (NVRAM text) at the top of RAM, ending 4 bytes below the end; the last word is their
   length in words with its complement in the upper half.
7. Reset the Wi-Fi core so the image starts; wait for the fast (HT) clock.
8. Enable the mailbox interrupt bits.
9. With the driver's `firmware-logs` feature: a pointer 4 bytes below (RAM size − 64 KiB) gives a
   shared record; its `console_addr` field + 8 is the firmware's text log.
10. Load the regulatory table (CLM), set the country, enable events, bring the interface up.

## 11. Open questions

- Why the firmware's free-buffer figure drops to 4 of 50 in monitor mode and stays there, and why the
  burst is 30 (§7; most controlled rounds followed one pattern, 30 frames and then one per host packet
  until the send credit left at the end of the burst is used, but nothing explains it); whether the firmware's packet filters apply in monitor mode,
  so a burst could hold only wanted frames; and why some bursts stop short.
- Whether any configuration keeps action-frame events (59 / 75) coming (see the untried list in §8).
- Whether the device can be kept from transmitting in the listen state.
- Whether events above code 127 can be enabled, given the 16-byte mask read-back.
- All of the above on a second board, on a Pico W (RP2040), and on the 7.95.49 build (only the
  burst and pool figures have been measured on 7.95.49 and 7.95.75, once each; §7).

## Privacy

Probe requests and Wi-Fi Aware frames identify other people's devices and the networks they look
for. No captured frames, addresses or network names from the test location are included here, and
the example values above are from the author's own devices or are protocol constants. The Wi-Fi
Aware transmitter used as a known source was the author's own phone. The diagnostics patch can keep
the first bytes of received frames in memory for printing; none of that output is included.

## Licence

The text is under the MIT licence (`LICENSE`). The files in `patches/` are changes to embassy and are
offered under embassy's own licences (MIT or Apache-2.0).
