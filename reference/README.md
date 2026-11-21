# CYW43439 host interface: a reference from four public drivers

What a host can send to the radio firmware on a Raspberry Pi Pico W / Pico 2 W and what comes back,
as shown by the public drivers that talk to it. Assembled 2026-11-21.

## What this is, and is not

- Every statement is about what a **driver** defines or does, with a citation to the driver source line.
  It is not a statement about how the firmware behaves unless a driver's own comment says so.
- Built from driver source only. No firmware image was opened, searched, disassembled or run through
  any tool; the firmware's licence (Infineon Permissive Binary License 1.0, clause 2) forbids reverse
  engineering. Firmware images were left out of the source folder the work was done from.
- Not checked on hardware. What one board did when asked is in the write-up at the top of this
  repository (`../README.md`). `18-board-checks.md` lists the claims here that a board could settle.
- Where drivers disagree, both sides are shown and none is declared right. `17-differences.md` collects them.

## Sources

| Short name | What | Version |
|---|---|---|
| embassy | `embassy-rs/embassy`, `cyw43/src` and `cyw43-pio/src` | main `bb6ce6898` plus the two-line padding fix of PR #7601 |
| linux | `drivers/net/wireless/broadcom/brcm80211` (brcmfmac, brcmutil, include) and two `include/linux` headers | tree at `15bf0c75de` |
| whd | `Infineon/wifi-host-driver`, `WHD/COMPONENT_WIFI6/inc` and `src` | `bd99da7` |
| c-driver | `georgerobotics/cyw43-driver`, `src` | `fa9627e` |
| pico-sdk | `raspberrypi/pico-sdk`, `pico_cyw43_driver/cybt_shared_bus` | master, November 2026 |
| sdio-crate | the Rust `sdio` crate, 0.5.3 (constants embassy's SDIO path uses) | 0.5.3 |

Citations read `driver/path:line`: the short name from the table, then the path inside that source and the
line. The source folder itself is not included here; the table gives the versions.

Three conventions to know:

- **Absences.** A claim that a driver does not define or send something cites the block that was searched
  (a register block, a function, a header range) or nothing at all; it cannot cite a line that shows it.
  These claims rest on a search of the source folder.
- **Constants from outside the folder.** linux sizes that involve an address or an interface name assume
  `ETH_ALEN` = 6 and `IFNAMSIZ` = 16; neither is defined in the source folder. Remarks marked "recalled, not
  in these sources" are the author's memory, labelled as such.
- **Sizes.** "Compiled" sizes come from compiling the driver's own headers (whd with its HAL headers
  stubbed); "computed" sizes are added up from the member list.

## Chapters

| File | Contents |
|---|---|
| `01-commands.md` | 284 command numbers: names per driver, direction, who sends it, payload. 125 are sent by no driver. |
| `02-variables.md` | 257 named variables ("iovars"), merged across drivers. 18 are used by all four. |
| `03-events.md` | 144 event codes from embassy's list, 13 more that other drivers define, and event-mask sizing. |
| `04-records-linux.md` | Wire records in linux, field by field. |
| `05-records-whd.md` | Wire records in Infineon's driver. |
| `06-records-embassy-c-driver.md` | embassy's records and the layouts the c-driver builds by hand. |
| `07-records-other.md` | Records defined outside the main type headers. |
| `08-record-correspondence.md` | Which record in one driver corresponds to which in another, and where layouts differ. |
| `09-framing.md` | SDPCM, BDC and command headers; sequence numbers and send credit; reception. |
| `10-spi.md` | The SPI bus: command word, registers, status word, interrupts, watermark, packet reads. |
| `11-sdio.md` | The SDIO bus. |
| `12-bringup.md` | Cores, memory map, firmware and settings download, regulatory data, per-driver start-up sequence. |
| `13-bluetooth.md` | Bluetooth over the shared bus: registers, ring buffers, patch download, handshake. |
| `14-codes.md` | Channel-word encoding, firmware error codes, event status / reason / flag codes. |
| `15-procedures.md` | Scan, join, leave, access point, power save, multicast filter, signal strength: step lists per driver. |
| `16-other-sources.md` | Findings from source files the other chapters do not draw on. |
| `17-differences.md` | Digest of where the drivers disagree, and hazards their own comments flag. |
| `18-board-checks.md` | Forty claims a board could settle by read-only or harmless means. |

About 3 MB of text and 33,000 citations, every one resolving to an existing file and line.

## How it was made

Three multi-agent runs on 2026-11-20/21 (269 agents in all):

1. **Extract** — 44 agents each took one slice (a block of commands or events, one driver's variables, a
   range of a type header, a transport topic) and wrote cited entries; 44 fresh agents re-opened every
   citation and corrected the files; one agent listed what was missing. Output: 2,182 entries.
2. **Write** — seven gap topics extracted and verified the same way; the variables merged across drivers;
   52 chapter parts written from the verified files, each then checked by a fresh agent against the
   source; a digest, a board-check list and a consistency report.
3. **Clean** — duplicated records merged, commands outside embassy's list added, every part brought to one
   format, a second consistency report.

## Known rough edges

From the second consistency report, not yet fixed:

- Bullet shape differs between some parts (three, four or five fields; some free-form bullets).
- Some table rows that state an absence ("no driver sends it") carry no citation; there is no line to cite.
- A few records parts carry scope remarks ("not compiled", a second include folder not covered).
- `09-framing.md` still has groups of adjacent bullets that share one pooled citation list; the lines
  are right where checked but are not split per bullet.

## Cross-family read (2026-11-21)

Eight reviewer runs from two other model families (Grok 4.7, Composer 2.5; four chapter groups, both
reviewers on each) sampled about 300 citations, 50 absence or "all four" claims and 50 numbers.

- Absence claims and numbers held, with one exception each. About 15 citations were wrong: most pointed
  at a neighbouring line; about six were errors of content.
- Each finding was then checked against the source by a fresh agent. Confirmed ones were fixed, along
  with every repeat of the same fault found by search (some 60 lines); eight reviewer findings were
  declined with source evidence. The agents' own further samples: 73 entries checked by hand, 7 wrong
  and fixed; and every struct-backed record entry (about 375) recompiled and compared, 1 wrong and fixed.
- The three missing whd records now have entries.
- What the reviewers trusted least, and a reader should too: sentences about control flow (queues,
  retries, what happens to a buffer) and rows that tie a specific call site to one line. Register tables,
  record layouts, sizes and code lists held up.

## A finding to follow up

By source reading, embassy's event-mask check indexes past the end of its array for an event code that
is not in its list (`03-events.md`, "Events outside embassy's list"). Predicted from the source and
reproduced in a scratch copy of the arithmetic; not observed in embassy or on hardware.

## Licences

The text of this reference (descriptions, tables, arrangement) is under the MIT licence, like the rest of
this repository. Names, numbers, sizes and offsets are reported from the sources as facts. Short source
comments quoted here, shown in quotation marks or introduced as a source comment, stay under the licence of
the source they come from:

| Source | Licence, as stated in the files read |
|---|---|
| embassy | MIT or Apache-2.0 |
| linux, brcm80211 | ISC |
| linux, general headers (`linux-headers/`) | GPL-2.0; only constants are cited, no text is quoted |
| whd | Apache-2.0 in each file's header; the repository's top-level `LICENSE.txt` is an Infineon end-user agreement. whd's comments are described here in our own words, not quoted (checked for runs of eight or more identical words); three short log messages are given literally so they can be matched against log output |
| c-driver | MIT |
| pico-sdk | BSD-3-Clause |
| sdio-crate | MIT or Apache-2.0 |

**Our reasoning on whd, and how to object.** Every whd file cited carries an Apache-2.0 header, and
Infineon publishes that source itself. We read the top-level agreement as covering the firmware and other
binaries shipped in the same repository, not the source files that state their own licence. If you hold
rights in any source used here and read this differently, or want something corrected or removed, please
open an issue at https://github.com/modelmiser/cyw43439-host-interface-notes/issues. We will take the
material down or change it on request.
