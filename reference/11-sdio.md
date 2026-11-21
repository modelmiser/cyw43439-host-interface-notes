# The sdio bus

## Function numbers

| Function | Role | Citations |
|---|---|---|
| 0 | Bus control: the CCCR and per-function blocks | `whd/src/bus_protocols/whd_bus_protocol_interface.h:40` `c-driver/cyw43_internal.h:17` `embassy/consts.rs:3` |
| 1 | Backplane access | `whd/src/bus_protocols/whd_bus_protocol_interface.h:41` `c-driver/cyw43_internal.h:18` `embassy/consts.rs:4` |
| 2 | WLAN data FIFO | `whd/src/bus_protocols/whd_bus_protocol_interface.h:42` `c-driver/cyw43_internal.h:19` `embassy/consts.rs:5` |
| 3 | Bluetooth; embassy defines FUNC_BT = 3, whd names the 0x300 function block "Bluetooth data FIFO" | `embassy/consts.rs:6` `whd/src/bus_protocols/whd_sdio.h:89` |

- linux uses the MMC core's func1/func2 objects instead of numeric constants. `linux/brcmfmac/sdio.h:169`
- c-driver selects the bus at compile time with CYW43_USE_SPI (default 0 = SDIO); cyw43_sdio.c is compiled only when CYW43_USE_SPI is 0. `c-driver/cyw43_config.h:23` `c-driver/cyw43_config.h:24` `c-driver/cyw43_sdio.c:15`
- embassy selects the bus at run time through the SealedBus trait constant TYPE; SdioBus sets TYPE = BusType::Sdio and runner.rs branches on bus_type(). `embassy/runner.rs:45` `embassy/runner.rs:51` `embassy/runner.rs:75` `embassy/sdio.rs:173`
- pico-sdk has no SDIO transport code. Its only "SDIO" names are BTSDIO_* Bluetooth shared-memory registers; no 0x10000-block register, mailbox, KSO or glom logic is found in pico-sdk. `pico-sdk/cybt_shared_bus_driver.c:37` `pico-sdk/cybt_shared_bus_driver.c:80`

### CMD52 and CMD53
| Argument bits | Field | Citations |
|---|---|---|
| 31 | Write flag | `c-driver/cyw43_sdio.c:18` `whd/src/bus_protocols/whd_bus_sdio_protocol.h:71` |
| 30:28 | Function number | `c-driver/cyw43_sdio.c:18` `whd/src/bus_protocols/whd_bus_sdio_protocol.h:70` |
| 27 | CMD53: block mode. CMD52: RAW flag (c-driver always passes 0 for CMD52) | `c-driver/cyw43_sdio.c:18` `c-driver/cyw43_sdio.c:25` `whd/src/bus_protocols/whd_bus_sdio_protocol.h:69` `whd/src/bus_protocols/whd_bus_sdio_protocol.h:80` |
| 26 | CMD53: op code, 1 = incrementing address | `c-driver/cyw43_sdio.c:18` `whd/src/bus_protocols/whd_bus_sdio_protocol.h:79` |
| 25:9 | Register address, 17 bits | `c-driver/cyw43_sdio.c:18` `sdio-crate/src/sdio.rs:88` `whd/src/bus_protocols/whd_bus_sdio_protocol.h:67` `whd/src/bus_protocols/whd_bus_sdio_protocol.h:78` |
| 8:0 (CMD53) | Byte or block count | `c-driver/cyw43_sdio.c:18` `sdio-crate/src/sdio.rs:89` `whd/src/bus_protocols/whd_bus_sdio_protocol.h:77` |
| 7:0 (CMD52) | Write data | `c-driver/cyw43_sdio.c:18` `c-driver/cyw43_sdio.c:25` `whd/src/bus_protocols/whd_bus_sdio_protocol.h:65` |

- The drivers mask register addresses to 17 bits; linux's F1 mask is REG_F1_MISC_MASK = 0x1FFFF. `linux/brcmfmac/sdio.h:29` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:1038` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:1083` `c-driver/cyw43_sdio.c:25`
- whd uses CMD52 for any transfer of exactly 1 byte. `whd/src/bus_protocols/whd_bus_sdio_protocol.c:991` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:993`
- c-driver uses CMD52 for 8-bit register access and CMD53 with length 4 for 32-bit register access. `c-driver/cyw43_sdio.c:65` `c-driver/cyw43_sdio.c:70` `c-driver/cyw43_sdio.c:77` `c-driver/cyw43_sdio.c:82`
- embassy uses CMD52 for 8-bit and CMD53 for 16-bit and 32-bit register access. `embassy/sdio.rs:357` `embassy/sdio.rs:361` `embassy/sdio.rs:365` `embassy/sdio.rs:377`
- whd's CMD53 always sets op code 1 (incrementing address), including F2 FIFO transfers; c-driver always passes inc = true. `whd/src/bus_protocols/whd_bus_sdio_protocol.c:1084` `c-driver/cyw43_sdio.c:51`
- linux reads F2 with sdio_readsb (fixed address) and writes it with sdio_memcpy_toio (incrementing). `linux/brcmfmac/bcmsdh.c:301` `linux/brcmfmac/bcmsdh.c:326`
- whd reports no bus header on SDIO (WHD_BUS_HEADER_SIZE = 0) and does not use the "status report scheme". `whd/src/bus_protocols/whd_bus_sdio_protocol.h:33` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:1649` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:1651`
- whd and c-driver use no backplane read padding on SDIO: whd WHD_BUS_SDIO_BACKPLANE_READ_PADD_SIZE = 0 (4 on SPI), c-driver CYW43_BACKPLANE_READ_PAD_LEN_BYTES = 0 (16 on SPI). `whd/src/bus_protocols/whd_bus_sdio_protocol.h:36` `whd/src/bus_protocols/whd_bus_spi_protocol.h:53` `c-driver/cyw43_ll.h:194` `c-driver/cyw43_ll.h:198`

CMD53 byte mode against block mode:

| Driver | Rule | Citations |
|---|---|---|
| c-driver | Byte mode for lengths <= 512, length rounded up to a multiple of 4, 512 encoded as count 0. Otherwise block mode with 64-byte blocks, length rounded up to 64. | `c-driver/cyw43_sdio.c:38` `c-driver/cyw43_sdio.c:41` `c-driver/cyw43_sdio.c:45` `c-driver/cyw43_sdio.c:49` `c-driver/cyw43_config.h:31` `c-driver/cyw43_config.h:33` |
| whd, WLAN up | Byte mode below 64 bytes. Block mode with 64-byte blocks, count = ceil(size / 64), for 64 and above. This single-CMD53 branch is compiled only when COMPONENT_MTB_HAL is not defined. | `whd/src/bus_protocols/whd_bus_sdio_protocol.c:995` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:996` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:999` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:1002` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:1108` |
| whd, before WLAN up, and always with COMPONENT_MTB_HAL | The transfer is split into a block-mode part (multiple of 64) and a byte-mode remainder. | `whd/src/bus_protocols/whd_bus_sdio_protocol.c:1005` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:1010` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:1021` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:1125` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:1130` |
| embassy | Calls the sdio crate's cmd53_read / cmd53_write with BLOCK_SIZE = 64. The crate splits the buffer into a block-mode part (the largest multiple of 64) and a byte-mode remainder, both with incrementing address; it adds no padding. | `embassy/sdio.rs:27` `embassy/sdio.rs:154` `embassy/sdio.rs:162` `embassy/consts.rs:112` `sdio-crate/src/sdio.rs:671` `sdio-crate/src/sdio.rs:678` `sdio-crate/src/sdio.rs:682` `sdio-crate/src/sdio.rs:694` `sdio-crate/src/sdio.rs:752` |

linux helper constants:

| Name | Value | Meaning (linux names and comments) | Citations |
|---|---|---|---|
| REG_F0_REG_MASK | 0x7FF | F0 register mask | `linux/brcmfmac/sdio.h:28` |
| REG_F1_MISC_MASK | 0x1FFFF | F1 register mask | `linux/brcmfmac/sdio.h:29` |
| SDIOD_FBR_SIZE | 0x100 | Size of one function block | `linux/brcmfmac/sdio.h:13` |
| BRCMF_SDALIGN | 64 (1 << 6) | Packet alignment | `linux/brcmfmac/sdio.h:140` `linux/brcmfmac/sdio.h:141` |
| SDIO_REQ_4BYTE | 0x1 | Four-byte target (backplane) width | `linux/brcmfmac/sdio.h:332` `linux/brcmfmac/sdio.h:333` |
| SDIO_REQ_FIXED | 0x2 | Fixed address (FIFO); combined with 4BYTE as F2SYNC | `linux/brcmfmac/sdio.h:334` `linux/brcmfmac/sdio.h:335` `linux/brcmfmac/sdio.c:319` |
| DMA_ALIGN_MASK | 0x03 | Buffer alignment mask | `linux/brcmfmac/bcmsdh.c:42` |
| DCMD_RESP_TIMEOUT, CTL_DONE_TIMEOUT | 2500 ms each | Command response and control-done timeouts | `linux/brcmfmac/sdio.c:39` `linux/brcmfmac/sdio.c:40` |

### CCCR registers (function 0)

Standard registers the drivers use:

| F0 address | Name | Used by | Citations |
|---|---|---|---|
| 0x02 | IOEN, I/O enable | whd, c-driver, embassy | `whd/src/bus_protocols/whd_sdio.h:45` `c-driver/cyw43_ll.c:190` `sdio-crate/src/sdio.rs:262` |
| 0x03 | IORDY, I/O ready | whd, c-driver, embassy | `whd/src/bus_protocols/whd_sdio.h:46` `c-driver/cyw43_ll.c:191` `sdio-crate/src/sdio.rs:264` |
| 0x04 | INTEN, interrupt enable | whd, c-driver, embassy | `whd/src/bus_protocols/whd_sdio.h:47` `c-driver/cyw43_ll.c:192` `sdio-crate/src/sdio.rs:266` |
| 0x05 | INTPEND, interrupt pending | whd. Not defined in c-driver or in embassy's own constants (blocks cited as ranges); the sdio crate embassy uses defines `CCCR_INT_PENDING` = 0x05 and nothing reads it. | `whd/src/bus_protocols/whd_sdio.h:48` `c-driver/cyw43_ll.c:190-200` `embassy/consts.rs:211-218` `sdio-crate/src/sdio.rs:268` |
| 0x06 | IOABORT | whd, embassy. Not found in c-driver. | `whd/src/bus_protocols/whd_sdio.h:49` `embassy/consts.rs:215` `c-driver/cyw43_ll.c:190-200` |
| 0x07 | BICTRL, bus interface control | whd, c-driver; the sdio crate embassy uses names it CCCR_BUS_CTRL | `whd/src/bus_protocols/whd_sdio.h:50` `c-driver/cyw43_ll.c:193` `sdio-crate/src/sdio.rs:272` |
| 0x10, 0x11 | F0 block size | whd (both bytes); c-driver and embassy define only 0x10 | `whd/src/bus_protocols/whd_sdio.h:59` `whd/src/bus_protocols/whd_sdio.h:60` `c-driver/cyw43_ll.c:194` `embassy/consts.rs:211` |
| 0x13 | SPEED_CONTROL | whd, c-driver, embassy | `whd/src/bus_protocols/whd_sdio.h:62` `c-driver/cyw43_ll.c:195` `embassy/consts.rs:212` |
| 0x110, 0x111 | F1 block size | whd (both bytes); c-driver and embassy define only 0x110 | `whd/src/bus_protocols/whd_sdio.h:74` `whd/src/bus_protocols/whd_sdio.h:75` `c-driver/cyw43_ll.c:198` `embassy/consts.rs:216` |
| 0x210, 0x211 | F2 block size | whd, c-driver, embassy | `whd/src/bus_protocols/whd_sdio.h:81` `whd/src/bus_protocols/whd_sdio.h:82` `c-driver/cyw43_ll.c:199` `c-driver/cyw43_ll.c:200` `embassy/consts.rs:217` `embassy/consts.rs:218` |

- embassy takes its IOEN, IORDY and INTEN addresses from the sdio crate: it imports CCCR_IO_ENABLE, CCCR_IO_READY and CCCR_INT_ENABLE and defines only CCCR_INT_ENABLE_MASTER = 0x01 locally. `embassy/sdio.rs:5` `embassy/runner.rs:11` `embassy/consts.rs:79`
- The sdio crate defines them as 0x02, 0x03 and 0x04, the same as whd and c-driver. `sdio-crate/src/sdio.rs:262` `sdio-crate/src/sdio.rs:264` `sdio-crate/src/sdio.rs:266`
- linux uses the kernel MMC core's SDIO_CCCR_* names (SDIO_CCCR_ABORT, SDIO_CCCR_IENx, SDIO_CCCR_INTx). Their values are not in these sources; linux defines only the vendor registers 0xF0-0xF2 here. `linux/brcmfmac/bcmsdh.c:749` `linux/brcmfmac/sdio.h:33`

Bits:

| Register | Bits | Citations |
|---|---|---|
| IOEN, IORDY | 0x02 function 1, 0x04 function 2; whd also 0x08 function 3 | `whd/src/bus_protocols/whd_sdio.h:136` `whd/src/bus_protocols/whd_sdio.h:137` `whd/src/bus_protocols/whd_sdio.h:138` `whd/src/bus_protocols/whd_sdio.h:143` `linux/brcmfmac/sdio.h:16` `linux/brcmfmac/sdio.h:17` `c-driver/cyw43_ll.c:204` `c-driver/cyw43_ll.c:205` `embassy/consts.rs:222` `embassy/consts.rs:225` |
| INTEN | 0x01 master enable, 0x02 function 1, 0x04 function 2 | `whd/src/bus_protocols/whd_sdio.h:146` `whd/src/bus_protocols/whd_sdio.h:147` `whd/src/bus_protocols/whd_sdio.h:148` `linux/brcmfmac/sdio.h:39` `linux/brcmfmac/sdio.h:40` `linux/brcmfmac/sdio.h:41` `c-driver/cyw43_ll.c:201` `c-driver/cyw43_ll.c:203` `embassy/consts.rs:219` `embassy/consts.rs:221` |
| INTPEND | 0x02 F1, 0x04 F2; whd also 0x08 F3 and SDIOD_CCCR_INTPEND_INT1 = 0x02 | `linux/brcmfmac/sdio.h:23` `linux/brcmfmac/sdio.h:24` `linux/brcmfmac/sdio.h:25` `whd/src/bus_protocols/whd_sdio.h:122` `whd/src/bus_protocols/whd_sdio.h:156` `whd/src/bus_protocols/whd_sdio.h:157` `whd/src/bus_protocols/whd_sdio.h:158` |
| REV (0x00) | 0xF0 SDIO spec revision, 0x0F CCCR format version (whd) | `whd/src/bus_protocols/whd_sdio.h:129` `whd/src/bus_protocols/whd_sdio.h:130` |
| SDREV (0x01) | 0x0F SD format version (whd) | `whd/src/bus_protocols/whd_sdio.h:133` |
| IOABORT | 0x07 function to abort, 0x08 IO_ABORT_RESET_ALL (I/O card reset) (whd). RESET_ALL appears in whd code only in a commented-out line. | `whd/src/bus_protocols/whd_sdio.h:161` `whd/src/bus_protocols/whd_sdio.h:162` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:2261` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:2262` |
| BICTRL | 0x80 card-detect disable, 0x40 continuous-SPI-interrupt capable, 0x20 continuous-SPI-interrupt enable, 0x03 width mask: 0x02 = 4-bit, 0x00 = 1-bit (whd) | `whd/src/bus_protocols/whd_sdio.h:165` `whd/src/bus_protocols/whd_sdio.h:166` `whd/src/bus_protocols/whd_sdio.h:167` `whd/src/bus_protocols/whd_sdio.h:168` `whd/src/bus_protocols/whd_sdio.h:169` `whd/src/bus_protocols/whd_sdio.h:170` |
| CAPABILITIES (0x08) | 0x80 4BLS, 0x40 LSC, 0x20 E4MI, 0x10 S4MI, 0x08 SBS, 0x04 SRW, 0x02 SMB, 0x01 SDC (whd) | `whd/src/bus_protocols/whd_sdio.h:173` `whd/src/bus_protocols/whd_sdio.h:174` `whd/src/bus_protocols/whd_sdio.h:175` `whd/src/bus_protocols/whd_sdio.h:176` `whd/src/bus_protocols/whd_sdio.h:177` `whd/src/bus_protocols/whd_sdio.h:178` `whd/src/bus_protocols/whd_sdio.h:179` `whd/src/bus_protocols/whd_sdio.h:180` |
| POWER_CONTROL (0x12) | 0x01 SMPC (read-only), 0x02 EMPC (read-write) (whd) | `whd/src/bus_protocols/whd_sdio.h:183` `whd/src/bus_protocols/whd_sdio.h:184` |
| SPEED_CONTROL (0x13) | 0x01 SHS (read-only), 0x02 EHS (read-write) (whd) | `whd/src/bus_protocols/whd_sdio.h:187` `whd/src/bus_protocols/whd_sdio.h:188` |

whd's full F0 address list: 0x00 REV, 0x01 SDREV, 0x02 IOEN, 0x03 IORDY, 0x04 INTEN, 0x05 INTPEND, 0x06 IOABORT, 0x07 BICTRL, 0x08 CAPABILITIES, 0x09-0x0B common CIS pointer, 0x0C BUSSUSP, 0x0D FUNCSEL, 0x0E EXECFLAGS, 0x0F RDYFLAGS, 0x10/0x11 F0 block size, 0x12 POWER_CONTROL, 0x13 SPEED_CONTROL, 0x14 UHS_I, 0x15 DRIVE, 0x16 INTEXT, 0xF0 BRCM_CARDCAP, 0xF1 BRCM_CARDCTL, 0xF2 SEP_INT_CTL. `whd/src/bus_protocols/whd_sdio.h:43` `whd/src/bus_protocols/whd_sdio.h:51` `whd/src/bus_protocols/whd_sdio.h:55` `whd/src/bus_protocols/whd_sdio.h:61` `whd/src/bus_protocols/whd_sdio.h:65` `whd/src/bus_protocols/whd_sdio.h:68`

whd's per-function blocks sit at 0x100 (F1, backplane), 0x200 (F2, WLAN data FIFO) and 0x300 (F3, Bluetooth data FIFO): +0x00 INFO, +0x02 HP, +0x09..+0x0B CIS pointer, +0x10/+0x11 block size. `whd/src/bus_protocols/whd_sdio.h:69` `whd/src/bus_protocols/whd_sdio.h:76` `whd/src/bus_protocols/whd_sdio.h:83` `whd/src/bus_protocols/whd_sdio.h:89`

Broadcom vendor registers:

| F0 address | Name | Bits (meanings from the linux and whd header comments) | Citations |
|---|---|---|---|
| 0xF0 | BRCM_CARDCAP, card capability | 0x02 CMD14_SUPPORT; 0x04 CMD14_EXT (CMD14 allowed in FSM command state); 0x08 CMD_NODEC (sdiod_aos does not decode any command) | `linux/brcmfmac/sdio.h:33` `linux/brcmfmac/sdio.h:34` `linux/brcmfmac/sdio.h:35` `linux/brcmfmac/sdio.h:36` `whd/src/bus_protocols/whd_sdio.h:66` `whd/src/bus_protocols/whd_sdio.h:191` `whd/src/bus_protocols/whd_sdio.h:193` `c-driver/cyw43_ll.c:196` `c-driver/cyw43_ll.c:220` `c-driver/cyw43_ll.c:222` `embassy/consts.rs:213` `embassy/consts.rs:98` |
| 0xF0 | BRCM_CARDCAP, whd extras | 0x40 CHIPID_PRESENT (chip id readable from the SDIO core); 0x80 SECURE_MODE (bootloader security). embassy defines only 0x80. Not found in linux or c-driver. | `whd/src/bus_protocols/whd_sdio.h:194` `whd/src/bus_protocols/whd_sdio.h:195` `embassy/consts.rs:96` `linux/brcmfmac/sdio.h:33-36` `c-driver/cyw43_ll.c:220-222` |
| 0xF1 | BRCM_CARDCTRL, card control | 0x02 WLANRESET (whd: SDIOD_CCCR_BRCM_WLANRST_ONF0ABORT). Not found in c-driver or embassy. | `linux/brcmfmac/sdio.h:43` `linux/brcmfmac/sdio.h:44` `whd/src/bus_protocols/whd_sdio.h:67` `whd/src/bus_protocols/whd_sdio.h:197` `c-driver/cyw43_ll.c:190-200` `embassy/consts.rs:211-218` |
| 0xF2 | BRCM_SEPINT / SEP_INT_CTL, separate interrupt control | 0x01 MASK (out-of-band interrupt mask); 0x02 OE (output enable); 0x04 ACT_HI (set = active high) | `linux/brcmfmac/sdio.h:46` `linux/brcmfmac/sdio.h:47` `linux/brcmfmac/sdio.h:48` `linux/brcmfmac/sdio.h:49` `whd/src/bus_protocols/whd_sdio.h:68` `whd/src/bus_protocols/whd_sdio.h:151` `whd/src/bus_protocols/whd_sdio.h:153` `c-driver/cyw43_ll.c:225` `c-driver/cyw43_ll.c:227` `embassy/consts.rs:231` `embassy/consts.rs:233` |

- whd reads CARDCAP at init: bit 0x80 only prints a message; bit 0x40 selects reading the chip id from the SDIO core and sets chipid_in_sdiocore. `whd/src/bus_protocols/whd_bus_sdio_protocol.c:489` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:492` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:497` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:502`
- linux sets CARDCTRL WLANRESET at probe so that an SDIO card reset also resets the WLAN backplane. `linux/brcmfmac/sdio.c:4051` `linux/brcmfmac/sdio.c:4056` `linux/brcmfmac/sdio.c:4058`
- whd sets WLANRESET (read-modify-write of F0 0xF1) only in whd_wlan_reset_sdio, in BLHS_SUPPORT builds, when the chip id was read from the SDIO core. This path is not taken for the 43439 (inferred: no BLHS). `whd/src/bus_protocols/whd_bus_sdio_protocol.c:2243` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:2249` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:2253` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:2258`
- To route the interrupt to the out-of-band pin, the drivers write SEPINT = MASK + OE (0x03), plus 0x04 for active-high. c-driver and embassy write 0x03 (active low). linux and whd add the polarity bit from platform configuration. `c-driver/cyw43_ll.c:1766` `c-driver/cyw43_ll.c:1767` `embassy/runner.rs:284` `linux/brcmfmac/bcmsdh.c:149` `linux/brcmfmac/bcmsdh.c:153` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:1742` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:1745` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:1758`
- linux in out-of-band mode also ORs FUNC0 + FUNC1 + FUNC2 (0x07) into the CCCR interrupt-enable register. On unregister it writes 0 to SEPINT and to the interrupt-enable register. `linux/brcmfmac/bcmsdh.c:143` `linux/brcmfmac/bcmsdh.c:147` `linux/brcmfmac/bcmsdh.c:180` `linux/brcmfmac/bcmsdh.c:181`
- linux without an out-of-band IRQ claims the in-band SDIO interrupt on F1 (real handler) and F2 (dummy handler). `linux/brcmfmac/bcmsdh.c:159` `linux/brcmfmac/bcmsdh.c:160`
- For chip 43362 only, linux redirects the out-of-band interrupt to a device GPIO: F1 GPIO_SELECT (0x10005) = 0xF, GPIO_OUT (0x10006) = 0, GPIO_EN (0x10007) = 0x2, and bit 0x2 in chipcommon gpiocontrol. whd does the same writes, keyed on the configured dev_gpio_sel instead of the chip id. `linux/brcmfmac/bcmsdh.c:129` `linux/brcmfmac/bcmsdh.c:134` `linux/brcmfmac/bcmsdh.c:137` `linux/brcmfmac/bcmsdh.c:140` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:1365` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:1369` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:1373` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:1377` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:1753`
- linux's watchdog uses INTPEND as a polling fallback. Conditions: save/restore off, polling enabled, poll tick elapsed, no interrupt configured or none arrived since the last check, no DPC already triggered. It then reads the pending register through F0 and schedules the DPC if the F1 or F2 bit is set. `linux/brcmfmac/sdio.c:3677` `linux/brcmfmac/sdio.c:3685` `linux/brcmfmac/sdio.c:3689` `linux/brcmfmac/sdio.c:3696` `linux/brcmfmac/sdio.c:3702` `linux/brcmfmac/sdio.c:3707`
- whd reads INTPEND (4 bytes) only in the DM_43022C1 bootloader-handshake path, polling bit 0x02 up to 80000 times as a "backplane enabled" indication. `whd/src/bus_protocols/whd_bus_sdio_protocol.c:1882`
- Reading INTPEND is not found in c-driver or embassy. c-driver and embassy's own constants do not define the register (blocks cited as ranges); the sdio crate defines `CCCR_INT_PENDING` and has no read of it. `c-driver/cyw43_ll.c:190-200` `embassy/consts.rs:211-218` `sdio-crate/src/sdio.rs:268`

### Bring-up order: whd, c-driver, embassy

This table lists the SDIO-specific steps; core reset and firmware download are in the bring-up chapter.

| Step | Action | Per-driver detail | Citations |
|---|---|---|---|
| 1 | Enumerate the card: CMD0, CMD5 (errors ignored), CMD3 for the RCA, CMD7 to select. | c-driver does it itself. embassy calls the sdio crate's reacquire, which sends CMD5 (inquiry, then with a voltage window), CMD3 and the card select. whd leaves it to the HAL, linux to the MMC core. | `c-driver/cyw43_ll.c:1643` `c-driver/cyw43_ll.c:1644` `c-driver/cyw43_ll.c:1648` `c-driver/cyw43_ll.c:1655` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:338` `embassy/sdio.rs:177` `sdio-crate/src/sdio.rs:407` `sdio-crate/src/sdio.rs:428` `sdio-crate/src/sdio.rs:443` `sdio-crate/src/sdio.rs:451` `sdio-crate/src/sdio.rs:457` `linux/brcmfmac/bcmsdh.c:905` |
| 2 | Write IOEN (F0 0x02) = 0x02 and read back every 1 ms until it reads 0x02. | Limit: whd 500 iterations (F0_WORKING_TIMEOUT_MS), embassy 500 ms, c-driver 100 iterations. linux calls sdio_enable_func(func1). | `whd/src/bus_protocols/whd_bus_sdio_protocol.c:69` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:342` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:351` `embassy/sdio.rs:186` `embassy/sdio.rs:192` `c-driver/cyw43_ll.c:1662` `c-driver/cyw43_ll.c:1668` `linux/brcmfmac/bcmsdh.c:943` |
| 3 | Set 4-bit width: read BICTRL (F0 0x07), write (value & ~0x03) + 0x02. | whd skips it when sdio_1bit_mode is configured. embassy does not do it in its own file; the sdio crate's acquire does the same read-modify-write during enumeration, choosing 4-bit only when both the host and the card capability register allow it. | `whd/src/bus_protocols/whd_bus_sdio_protocol.c:360` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:363` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:367` `c-driver/cyw43_ll.c:1681` `c-driver/cyw43_ll.c:1682` `embassy/sdio.rs:177` `sdio-crate/src/sdio.rs:464` `sdio-crate/src/sdio.rs:471` `sdio-crate/src/sdio.rs:475` |
| 4 | Set block size 64: write 64 to F0 0x10 and read back until it sticks; then write 64 to F0 0x10, F1 0x110, F2 0x210 and 0 to F2 0x211. | linux uses F1 block size 64 and F2 block size 512 by default (256 for 4373/43752/4354/4356/4359, 128 for 4329); the 43439 takes the default 512. | `whd/src/bus_protocols/whd_bus_sdio_protocol.c:376` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:380` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:395` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:401` `c-driver/cyw43_ll.c:1685` `c-driver/cyw43_ll.c:1693` `c-driver/cyw43_ll.c:1696` `embassy/sdio.rs:200` `embassy/sdio.rs:211` `embassy/sdio.rs:216` `linux/brcmfmac/bcmsdh.c:903` |
| 5 | Write INTEN (F0 0x04) = 0x07 (master, F1, F2). | Same in all three. | `whd/src/bus_protocols/whd_bus_sdio_protocol.c:409` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:411` `c-driver/cyw43_ll.c:1698` `c-driver/cyw43_ll.c:1699` `embassy/sdio.rs:219` `embassy/sdio.rs:222` |
| 6 | High speed: read SPEED_CONTROL (F0 0x13); bit 0 (SHS) must be set; write value + 0x02 (EHS). | whd only when high_speed_sdio_clock is configured. embassy does not do it in its own file; the sdio crate's acquire sets EHS during enumeration, only when the requested clock is above 25 MHz and SHS reads set. | `whd/src/bus_protocols/whd_bus_sdio_protocol.c:413` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:416` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:420` `c-driver/cyw43_ll.c:1702` `c-driver/cyw43_ll.c:1704` `embassy/sdio.rs:177` `sdio-crate/src/sdio.rs:482` `sdio-crate/src/sdio.rs:483` `sdio-crate/src/sdio.rs:484` |
| 7 | Poll IORDY (F0 0x03) every 1 ms until bit 0x02 (F1 ready). | Limit: whd 500 (F1_AVAIL_TIMEOUT_MS), embassy 500 ms, c-driver 10 iterations. | `whd/src/bus_protocols/whd_bus_sdio_protocol.c:70` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:431` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:436` `embassy/sdio.rs:226` `embassy/sdio.rs:229` `c-driver/cyw43_ll.c:1710` `c-driver/cyw43_ll.c:1712` |
| 8 | Request ALP: write CHIP_CLOCK_CSR (0x1000E) = FORCE_HW_CLKREQ_OFF + ALP_AVAIL_REQ + FORCE_ALP = 0x29. | linux writes 0x28 first, waits for ALP, then writes 0x21. | `whd/src/bus_protocols/whd_bus_sdio_protocol.c:448` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:451` `c-driver/cyw43_ll.c:1727` `c-driver/cyw43_ll.c:1728` `embassy/runner.rs:493` `embassy/runner.rs:498` `linux/brcmfmac/sdio.c:3855` |
| 8a | c-driver with Bluetooth enabled: write 0x10 to the F2 watermark register (0x10008) and fail init if it does not read back 0x10. | embassy does this only on SPI. Not found in whd. | `c-driver/cyw43_ll.c:1733` `c-driver/cyw43_ll.c:1735` `c-driver/cyw43_ll.c:1737` `embassy/runner.rs:484` `embassy/runner.rs:487` `embassy/runner.rs:491` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:317-630` |
| 9 | Poll CHIP_CLOCK_CSR every 1 ms until ALP_AVAIL (0x40). | Limit: whd 100 (ALP_AVAIL_TIMEOUT_MS), embassy 100 ms, c-driver 10 iterations. | `whd/src/bus_protocols/whd_bus_sdio_protocol.c:73` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:453` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:457` `embassy/runner.rs:505` `embassy/runner.rs:507` `c-driver/cyw43_ll.c:1743` `c-driver/cyw43_ll.c:1745` |
| 10 | Clear the ALP request: write CHIP_CLOCK_CSR = 0. | Same in all three. | `whd/src/bus_protocols/whd_bus_sdio_protocol.c:469` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:470` `c-driver/cyw43_ll.c:1757` `c-driver/cyw43_ll.c:1758` `embassy/runner.rs:514` `embassy/runner.rs:516` |
| 11 | Write PULL_UP (0x1000F) = 0, then IOEN (F0 0x02) = 0x06 to enable F1 and F2. | c-driver does not write PULL_UP here, only at the end of init. embassy skips enabling F2 here for the 43455. embassy inserts extra writes between the two; see below. linux disables F2 at probe and enables it only after firmware download. | `whd/src/bus_protocols/whd_bus_sdio_protocol.c:472` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:473` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:476` `c-driver/cyw43_ll.c:1761` `c-driver/cyw43_ll.c:1762` `c-driver/cyw43_ll.c:1891` `embassy/runner.rs:305` `embassy/runner.rs:323` `embassy/runner.rs:330` `linux/brcmfmac/sdio.c:4523` |
| 12 | Configure the out-of-band interrupt (SEP_INT_CTL), write INTEN (F0 0x04) = 0x05 (master + F2), read IORDY once. | embassy writes SEP_INT_CTL = 0x03 before enabling F1+F2, not after. | `whd/src/bus_protocols/whd_bus_sdio_protocol.c:478` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:482` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:485` `c-driver/cyw43_ll.c:1767` `c-driver/cyw43_ll.c:1770` `c-driver/cyw43_ll.c:1772` `embassy/runner.rs:284` `embassy/runner.rs:335` `embassy/runner.rs:340` `embassy/runner.rs:344` |
| 13 | Read the chip id (16 bits at chipcommon 0x18000000, or from the SDIO core when CARDCAP says so), halt and reset the cores, download firmware and NVRAM over F1, release the ARM core. | Documented in the bring-up chapter. | `whd/src/bus_protocols/whd_bus_sdio_protocol.c:527` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:554` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:1191` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:1245` `c-driver/cyw43_ll.c:1777` `c-driver/cyw43_ll.c:1804` `embassy/runner.rs:518` `embassy/runner.rs:601` |
| 14 | Poll CHIP_CLOCK_CSR every 1 ms until HT_AVAIL (0x80). | Limit: whd 2500 (HT_AVAIL_TIMEOUT_MS in the SDIO file; 1000 in whd's SPI file), c-driver 1000 iterations ("takes about 29ms"), embassy 500 ms. | `whd/src/bus_protocols/whd_bus_sdio_protocol.c:74` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:1256` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:1260` `whd/src/bus_protocols/whd_bus_spi_protocol.c:71` `c-driver/cyw43_ll.c:1807` `c-driver/cyw43_ll.c:1810` `embassy/runner.rs:605` `embassy/runner.rs:608` |
| 15 | Write hostintmask (core + 0x24) = 0xF0 (4 bytes), funcintmask (core + 0x34) = 0x03 (1 byte), F2 watermark (0x10008) = 8. | Same in all three. | `whd/src/bus_protocols/whd_bus_sdio_protocol.c:1284` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:1287` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:1292` `c-driver/cyw43_ll.c:1822` `c-driver/cyw43_ll.c:1826` `c-driver/cyw43_ll.c:1829` `embassy/runner.rs:616` `embassy/runner.rs:622` `embassy/runner.rs:628` |
| 16 | Poll IORDY (F0 0x03) every 1 ms until bit 0x04 (F2 ready). The drivers use this as the sign that the firmware has started (inferred from their placing it right after the firmware start). | Limit 1000 ms or iterations in all three. whd comment: a failure here "could be due to incorrect NVRAM variables". linux: sdio_enable_func(func2) with enable_timeout raised to 3000 ms (SDIO_WAIT_F2RDY). | `whd/src/bus_protocols/whd_bus_sdio_protocol.c:72` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:568` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:573` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:580` `c-driver/cyw43_ll.c:1843` `c-driver/cyw43_ll.c:1852` `embassy/runner.rs:682` `embassy/runner.rs:689` `linux/brcmfmac/bcmsdh.c:940` |
| 17 | Enable save/restore and KSO (see "Sleep/keep-awake control"), then bring the bus up. | | `whd/src/bus_protocols/whd_bus_sdio_protocol.c:598` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:605` `c-driver/cyw43_ll.c:1864` `c-driver/cyw43_ll.c:1911` `embassy/runner.rs:694` `embassy/runner.rs:697` |

- c-driver waits until at least 150 ms have passed since the start of bus init before finishing wifi_on; its comment says in-band and out-of-band WL_HOST_WAKE interrupts in bus-sleep mode do not work correctly otherwise. `c-driver/cyw43_ll.c:1568` `c-driver/cyw43_ll.c:2043` `c-driver/cyw43_ll.c:2047`

embassy's own order between clearing the ALP request and firmware download (read_chip_id_sdio):

| Order | embassy action | Citations |
|---|---|---|
| 1 | PULL_UP (0x1000F) = 0 | `embassy/runner.rs:304` `embassy/runner.rs:305` |
| 2 | IOEN = 0x02 (F1 only) | `embassy/runner.rs:307` `embassy/runner.rs:308` |
| 3 | INTEN = 0x07 | `embassy/runner.rs:315` `embassy/runner.rs:316` |
| 4 | enable_sdio_interrupts: SEP_INT_CTL (F0 0xF2) = 0x03, F0 0x24 = 0xFF, F0 0x34 = 0x02, INTEN = 0x01 | `embassy/runner.rs:284` `embassy/runner.rs:290` `embassy/runner.rs:295` `embassy/runner.rs:300` |
| 5 | IOEN = 0x06 (skipped for the 43455) | `embassy/runner.rs:325` `embassy/runner.rs:326` `embassy/runner.rs:330` |
| 6 | INTEN = 0x05 | `embassy/runner.rs:335` `embassy/runner.rs:340` |
| 7 | Read IORDY once | `embassy/runner.rs:344` |
| 8 | Read BRCM_CARDCAP; take the chip id from the SDIO core if bit 0x80 is set, else 16 bits at 0x18000000 | `embassy/runner.rs:346` `embassy/runner.rs:347` `embassy/runner.rs:368` `embassy/runner.rs:370` |

- whd and c-driver have no second IOEN = 0x02 / INTEN = 0x07 writes and no F0 0x24/0x34 writes at this point; they write SEP_INT_CTL after IOEN = 0x06. `whd/src/bus_protocols/whd_bus_sdio_protocol.c:479` `c-driver/cyw43_ll.c:1762`

### Bring-up order: linux
| Step | linux action | Citations |
|---|---|---|
| 1 | brcmf_sdiod_probe: F1 block size 64, F2 block size 512 (device-dependent), F2 enable timeout 3000 ms, enable function 1. | `linux/brcmfmac/bcmsdh.c:44` `linux/brcmfmac/bcmsdh.c:45` `linux/brcmfmac/bcmsdh.c:50` `linux/brcmfmac/bcmsdh.c:907` `linux/brcmfmac/bcmsdh.c:930` `linux/brcmfmac/bcmsdh.c:940` `linux/brcmfmac/bcmsdh.c:943` |
| 2 | brcmf_sdio_probe_attach: write CHIPCLKCSR = BRCMF_INIT_CLKCTL1 = FORCE_HW_CLKREQ_OFF + ALP_AVAIL_REQ (0x28) to "force PLL off"; read back and require (value & ~0xC0) == 0x28, else fail with "ChipClkCSR access". | `linux/brcmfmac/sdio.c:315` `linux/brcmfmac/sdio.c:316` `linux/brcmfmac/sdio.c:3971` `linux/brcmfmac/sdio.c:3976` `linux/brcmfmac/sdio.c:3979` `linux/brcmfmac/sdio.c:3982` |
| 3 | brcmf_sdio_buscoreprep (from chip attach): write CHIPCLKCSR = 0x28; read back and check; spin until either availability bit is set, limit PMU_MAX_TRANSITION_DLY = 1,000,000 us; write CHIPCLKCSR = FORCE_HW_CLKREQ_OFF + FORCE_ALP (0x21); delay 65 us; write SDIOPULLUP = 0. | `linux/brcmfmac/sdio.c:312` `linux/brcmfmac/sdio.c:3854` `linux/brcmfmac/sdio.c:3856` `linux/brcmfmac/sdio.c:3866` `linux/brcmfmac/sdio.c:3875` `linux/brcmfmac/sdio.c:3883` `linux/brcmfmac/sdio.c:3885` `linux/brcmfmac/sdio.c:3888` |
| 4 | brcmf_sdio_kso_init (set KSO in SLEEPCSR if core rev >= 12 and not already set); set drive strength; set CARDCTRL WLANRESET; set PMU control so a backplane reset reloads PMU state. | `linux/brcmfmac/sdio.c:3516` `linux/brcmfmac/sdio.c:3519` `linux/brcmfmac/sdio.c:4040` `linux/brcmfmac/sdio.c:4049` `linux/brcmfmac/sdio.c:4058` `linux/brcmfmac/sdio.c:4062` `linux/brcmfmac/sdio.c:4068` |
| 5 | brcmf_sdio_probe: record the F2 block size and roundup = min(512, blocksize); disable F2; write CHIPCLKCSR = 0; clkstate = CLK_SDONLY; idletime = 1; sr_enabled = false. | `linux/brcmfmac/sdio.c:544` `linux/brcmfmac/sdio.c:4517` `linux/brcmfmac/sdio.c:4519` `linux/brcmfmac/sdio.c:4523` `linux/brcmfmac/sdio.c:4528` `linux/brcmfmac/sdio.c:4534` `linux/brcmfmac/sdio.c:4535` `linux/brcmfmac/sdio.c:4539` |
| 6 | Firmware callback: download firmware and NVRAM with alp_only = true (clock requests use ALP_AVAIL_REQ instead of HT_AVAIL_REQ), then alp_only = false. | `linux/brcmfmac/sdio.c:802` `linux/brcmfmac/sdio.c:803` `linux/brcmfmac/sdio.c:4235` `linux/brcmfmac/sdio.c:4237` `linux/brcmfmac/sdio.c:4240` |
| 6a | brcmf_sdio_buscore_activate: write 0xFFFFFFFF to intstatus to clear all interrupts before starting the firmware; write the reset vector to address 0 when one is given. embassy copies the intstatus clear for the 43455 only. Not found in whd or c-driver. | `linux/brcmfmac/sdio.c:3900` `linux/brcmfmac/sdio.c:3902` `linux/brcmfmac/sdio.c:3906` `embassy/runner.rs:547` `embassy/runner.rs:550` `embassy/runner.rs:552` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:1174-1316` `c-driver/cyw43_ll.c:1775-1805` |
| 7 | brcmf_sdio_clkctl(CLK_AVAIL) to get HT; then read CHIPCLKCSR, OR in FORCE_HT (HT_AVAIL_REQ on the 43012) and write it back, "to be sure F2 interrupt propagates". | `linux/brcmfmac/sdio.c:4248` `linux/brcmfmac/sdio.c:4253` `linux/brcmfmac/sdio.c:4257` `linux/brcmfmac/sdio.c:4258` `linux/brcmfmac/sdio.c:4259` |
| 8 | Write tosbmailboxdata = 4 << 16, then enable function 2. | `linux/brcmfmac/sdio.c:4267` `linux/brcmfmac/sdio.c:4269` `linux/brcmfmac/sdio.c:4271` |
| 9 | If F2 enabled: write hostintmask = I_HMB_SW_MASK + I_CHIPACTIVE, then program the per-chip F2 watermark. On failure disable F2 again and run the "checkdied" diagnostics. | `linux/brcmfmac/sdio.c:4276` `linux/brcmfmac/sdio.c:4279` `linux/brcmfmac/sdio.c:4282` `linux/brcmfmac/sdio.c:4354` `linux/brcmfmac/sdio.c:4358` `linux/brcmfmac/sdio.c:4361` |
| 10 | If brcmf_chip_sr_capable returns true run brcmf_sdio_sr_init, otherwise restore the saved CHIPCLKCSR value; mark the bus state DATA; register the interrupt handler. | `linux/brcmfmac/sdio.c:4364` `linux/brcmfmac/sdio.c:4365` `linux/brcmfmac/sdio.c:4368` `linux/brcmfmac/sdio.c:4380` `linux/brcmfmac/sdio.c:4382` |

## Backplane register block

whd's comment: F1 addresses 0x00000-0x0FFFF access the backplane through the backplane window. `whd/src/bus_protocols/whd_sdio.h:93` `whd/src/bus_protocols/whd_sdio.h:94`

The F1 "miscellaneous" registers occupy 0x10000 (SBSDIO_FUNC1_MISC_REG_START) to 0x1001F (SBSDIO_FUNC1_MISC_REG_LIMIT). whd's comment says addresses above 0xFFFF "do not require a backplane clock". `linux/brcmfmac/sdio.h:116` `linux/brcmfmac/sdio.h:117` `whd/src/bus_protocols/whd_sdio.h:95` `whd/src/bus_protocols/whd_sdio.h:96`

| F1 address | linux name | whd / embassy name | Meaning | Defined by | Citations |
|---|---|---|---|---|---|
| 0x10000 | SBSDIO_SPROM_CS | not found | sprom command and status | linux | `linux/brcmfmac/sdio.h:54` |
| 0x10001 | SBSDIO_SPROM_INFO | SBSDIO_FUNC1_SECURE_MODE (whd) | linux: sprom info. whd: "To read secure-mode bit", "Sdio rev 27 only"; read (1 byte) only in DM_43022C1 builds, 0 taken as "chip supports bootloader handshake". | linux, whd | `linux/brcmfmac/sdio.h:56` `whd/src/bus_protocols/whd_sdio.h:255` `whd/src/bus_protocols/whd_sdio.h:256` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:535` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:537` |
| 0x10002 | SBSDIO_SPROM_DATA_LOW | not found | sprom indirect access data byte 0 | linux | `linux/brcmfmac/sdio.h:58` |
| 0x10003 | SBSDIO_SPROM_DATA_HIGH | not found | sprom indirect access data byte 1 | linux | `linux/brcmfmac/sdio.h:60` |
| 0x10004 | SBSDIO_SPROM_ADDR_LOW | not found | sprom indirect access address byte 0 | linux | `linux/brcmfmac/sdio.h:62` |
| 0x10005 | SBSDIO_GPIO_SELECT | SDIO_GPIO_SELECT | gpio select | linux, whd, embassy | `linux/brcmfmac/sdio.h:64` `whd/src/bus_protocols/whd_sdio.h:98` `embassy/consts.rs:55` |
| 0x10006 | SBSDIO_GPIO_OUT | SDIO_GPIO_OUTPUT | gpio output | linux, whd, embassy | `linux/brcmfmac/sdio.h:66` `whd/src/bus_protocols/whd_sdio.h:99` `embassy/consts.rs:56` |
| 0x10007 | SBSDIO_GPIO_EN | SDIO_GPIO_ENABLE | gpio enable | linux, whd, embassy | `linux/brcmfmac/sdio.h:68` `whd/src/bus_protocols/whd_sdio.h:100` `embassy/consts.rs:57` |
| 0x10008 | SBSDIO_WATERMARK | SDIO_FUNCTION2_WATERMARK | F2 watermark. linux comment: "rev < 7, watermark for sdio device TX path". | linux, whd, embassy, c-driver | `linux/brcmfmac/sdio.h:69` `linux/brcmfmac/sdio.h:70` `whd/src/bus_protocols/whd_sdio.h:101` `embassy/consts.rs:58` `c-driver/cyw43_ll.c:108` |
| 0x10009 | SBSDIO_DEVICE_CTL | SDIO_DEVICE_CONTROL | device control ("control busy signal generation") | linux, whd, embassy | `linux/brcmfmac/sdio.h:71` `linux/brcmfmac/sdio.h:72` `whd/src/bus_protocols/whd_sdio.h:102` `whd/src/bus_protocols/whd_sdio.h:224` `embassy/consts.rs:59` `embassy/consts.rs:97` |
| 0x1000A | SBSDIO_FUNC1_SBADDRLOW | SDIO_BACKPLANE_ADDRESS_LOW | window address low; only bit 15 of the address is held here | linux, whd, embassy, c-driver | `linux/brcmfmac/sdio.h:74` `linux/brcmfmac/sdio.h:75` `whd/src/bus_protocols/whd_sdio.h:103` `whd/src/bus_protocols/whd_sdio.h:221` `embassy/consts.rs:60` `embassy/consts.rs:102` `c-driver/cyw43_ll.c:109` |
| 0x1000B | SBSDIO_FUNC1_SBADDRMID | SDIO_BACKPLANE_ADDRESS_MID | window address bits 23:16 | linux, whd, embassy, c-driver | `linux/brcmfmac/sdio.h:76` `linux/brcmfmac/sdio.h:77` `whd/src/bus_protocols/whd_sdio.h:104` `whd/src/bus_protocols/whd_sdio.h:222` `embassy/consts.rs:61` `embassy/consts.rs:103` `c-driver/cyw43_ll.c:110` |
| 0x1000C | SBSDIO_FUNC1_SBADDRHIGH | SDIO_BACKPLANE_ADDRESS_HIGH | window address bits 31:24 | linux, whd, embassy, c-driver | `linux/brcmfmac/sdio.h:78` `linux/brcmfmac/sdio.h:79` `whd/src/bus_protocols/whd_sdio.h:105` `whd/src/bus_protocols/whd_sdio.h:223` `embassy/consts.rs:62` `embassy/consts.rs:104` `c-driver/cyw43_ll.c:111` |
| 0x1000D | SBSDIO_FUNC1_FRAMECTRL | SDIO_FRAME_CONTROL | frame control (terminate, abort). c-driver defines the address only as SPI_FRAME_CONTROL; its SDIO path never uses it. | linux, whd, embassy | `linux/brcmfmac/sdio.h:80` `linux/brcmfmac/sdio.h:81` `whd/src/bus_protocols/whd_sdio.h:106` `embassy/consts.rs:63` `c-driver/cyw43_spi.h:94` |
| 0x1000E | SBSDIO_FUNC1_CHIPCLKCSR | SDIO_CHIP_CLOCK_CSR | chip clock CSR: ALP/HT control and status | linux, whd, embassy, c-driver | `linux/brcmfmac/sdio.h:82` `linux/brcmfmac/sdio.h:83` `whd/src/bus_protocols/whd_sdio.h:107` `embassy/consts.rs:64` `embassy/consts.rs:227` `c-driver/cyw43_ll.c:112` `c-driver/cyw43_ll.c:209` |
| 0x1000F | SBSDIO_FUNC1_SDIOPULLUP | SDIO_PULL_UP | SDIO pull-up (cmd, d0-d2) | linux, whd, embassy, c-driver | `linux/brcmfmac/sdio.h:84` `linux/brcmfmac/sdio.h:85` `whd/src/bus_protocols/whd_sdio.h:108` `embassy/consts.rs:65` `embassy/consts.rs:228` `c-driver/cyw43_ll.c:210` |
| 0x10010-0x10018 | not named | not named | No driver names these; linux's list jumps from 0x1000F to 0x10019. | none | `linux/brcmfmac/sdio.h:85` `linux/brcmfmac/sdio.h:87` `whd/src/bus_protocols/whd_sdio.h:108` `whd/src/bus_protocols/whd_sdio.h:109` |
| 0x10019 | SBSDIO_FUNC1_WFRAMEBCLO | not found | write frame byte count low. Not found in whd, embassy, c-driver. | linux | `linux/brcmfmac/sdio.h:86` `linux/brcmfmac/sdio.h:87` `whd/src/bus_protocols/whd_sdio.h:98-112` `embassy/consts.rs:55-69` `c-driver/cyw43_ll.c:108-114` |
| 0x1001A | SBSDIO_FUNC1_WFRAMEBCHI | not found | write frame byte count high. Not found in whd, embassy, c-driver. | linux | `linux/brcmfmac/sdio.h:88` `linux/brcmfmac/sdio.h:89` `whd/src/bus_protocols/whd_sdio.h:98-112` `embassy/consts.rs:55-69` `c-driver/cyw43_ll.c:108-114` |
| 0x1001B | SBSDIO_FUNC1_RFRAMEBCLO | SDIO_READ_FRAME_BC_LOW | read frame byte count low. Not found in c-driver. | linux, whd, embassy | `linux/brcmfmac/sdio.h:90` `linux/brcmfmac/sdio.h:91` `whd/src/bus_protocols/whd_sdio.h:109` `embassy/consts.rs:66` `c-driver/cyw43_ll.c:108-114` |
| 0x1001C | SBSDIO_FUNC1_RFRAMEBCHI | SDIO_READ_FRAME_BC_HIGH | read frame byte count high. Not found in c-driver. | linux, whd, embassy | `linux/brcmfmac/sdio.h:92` `linux/brcmfmac/sdio.h:93` `whd/src/bus_protocols/whd_sdio.h:110` `embassy/consts.rs:67` `c-driver/cyw43_ll.c:108-114` |
| 0x1001D | SBSDIO_FUNC1_MESBUSYCTRL | not found | MesBusyCtl (rev 11): RX FIFO watermark for "MES" access plus busy enable. Not found in whd, embassy, c-driver. | linux | `linux/brcmfmac/sdio.h:94` `linux/brcmfmac/sdio.h:95` `whd/src/bus_protocols/whd_sdio.h:98-112` `embassy/consts.rs:55-69` `c-driver/cyw43_ll.c:108-114` |
| 0x1001E | SBSDIO_FUNC1_WAKEUPCTRL | SDIO_WAKEUP_CTRL | wakeup control (SDIO core rev 12) | linux, whd, embassy, c-driver | `linux/brcmfmac/sdio.h:103` `linux/brcmfmac/sdio.h:104` `whd/src/bus_protocols/whd_sdio.h:111` `embassy/consts.rs:68` `c-driver/cyw43_ll.c:113` |
| 0x1001F | SBSDIO_FUNC1_SLEEPCSR | SDIO_SLEEP_CSR | sleep CSR (KSO) | linux, whd, embassy, c-driver | `linux/brcmfmac/sdio.h:109` `whd/src/bus_protocols/whd_sdio.h:112` `embassy/consts.rs:69` `embassy/consts.rs:83` `c-driver/cyw43_ll.c:114` |
| 0x10030 | not found | SDIO_REG_DAR_H2D_MSG_0 (whd) | bootloader handshake, host to dongle. Not found in linux, embassy, c-driver. | whd | `whd/src/bus_protocols/whd_sdio.h:267` `linux/brcmfmac/sdio.h:54-117` `embassy/consts.rs:55-69` `c-driver/cyw43_ll.c:108-114` |
| 0x10038 | not found | SDIO_REG_DAR_D2H_MSG_0 (whd) | bootloader handshake, dongle to host. Not found in linux, embassy, c-driver. | whd | `whd/src/bus_protocols/whd_sdio.h:268` `linux/brcmfmac/sdio.h:54-117` `embassy/consts.rs:55-69` `c-driver/cyw43_ll.c:108-114` |

- linux also defines a direct-mapped CIS space on F1: SBSDIO_CIS_BASE_COMMON = 0x1000, SBSDIO_CIS_SIZE_LIMIT = 512 (0x200) bytes per CIS, SBSDIO_CIS_OFT_ADDR_MASK = 0x1FFFF, SBSDIO_CIS_MANFID_TUPLE_LEN = 6. No code in sdio.c or bcmsdh.c references them. Not found in whd, c-driver, embassy. `linux/brcmfmac/sdio.c:163` `linux/brcmfmac/sdio.c:165` `linux/brcmfmac/sdio.c:167` `linux/brcmfmac/sdio.c:170` `whd/src/bus_protocols/whd_sdio.h:98-112` `c-driver/cyw43_ll.c:108-114` `embassy/consts.rs:55-69`

### Backplane window

- The drivers treat F1 addresses below 0x8000 as an offset into a 32768-byte (0x8000) backplane window: offset mask 0x7FFF (SBSDIO_SB_OFT_ADDR_MASK), window base mask 0xFFFF8000 (SBSDIO_SBWINDOW_MASK). `linux/brcmfmac/sdio.h:122` `linux/brcmfmac/sdio.h:123` `linux/brcmfmac/sdio.h:128` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:65` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:66` `whd/src/bus_protocols/whd_chip_reg.h:81` `embassy/consts.rs:109` `embassy/consts.rs:110` `c-driver/cyw43_ll.c:123`
- The drivers set bit 15 (0x8000, SBSDIO_SB_ACCESS_2_4B_FLAG) in the F1 address for 32-bit backplane access (linux and whd comment: "with b15, maps to 32-bit SB access"). `linux/brcmfmac/sdio.h:124` `linux/brcmfmac/sdio.h:125` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:67` `embassy/consts.rs:111` `c-driver/cyw43_ll.c:126`
- The drivers program the window base with three CMD52 writes: ADDRESS_HIGH (0x1000C) = base >> 24, ADDRESS_MID (0x1000B) = base >> 16, ADDRESS_LOW (0x1000A) = base >> 8, where base = addr & ~0x7FFF. Only bit 7 of the LOW byte can be set. `whd/src/bus_protocols/whd_bus_sdio_protocol.c:2175` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:2188` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:2205` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:2222` `c-driver/cyw43_ll.c:333` `c-driver/cyw43_ll.c:338` `c-driver/cyw43_ll.c:341` `c-driver/cyw43_ll.c:344` `embassy/sdio.rs:123` `embassy/sdio.rs:126` `embassy/sdio.rs:134` `embassy/sdio.rs:142` `linux/brcmfmac/bcmsdh.c:226` `linux/brcmfmac/bcmsdh.c:232` `linux/brcmfmac/bcmsdh.c:236`
- embassy initialises its cached window to 0xAAAAAAAA so the first access rewrites all three bytes. `embassy/sdio.rs:74`
- embassy's SDIO bp_read/bp_write assert that the backplane address is a multiple of 4; its comment says the hardware force-aligns the address to 2 for lengths >= 2 and to 4 for lengths >= 4. `embassy/sdio.rs:259` `embassy/sdio.rs:263` `embassy/sdio.rs:296` `embassy/sdio.rs:300`
- Bulk transfers do not cross a window boundary: each chunk is limited to the bytes left in the current window and the window is set again per chunk (linux, embassy). c-driver asserts that the chunk fits instead of splitting it. `linux/brcmfmac/bcmsdh.c:686` `linux/brcmfmac/bcmsdh.c:688` `linux/brcmfmac/bcmsdh.c:697` `linux/brcmfmac/bcmsdh.c:733` `embassy/sdio.rs:266` `embassy/sdio.rs:269` `embassy/sdio.rs:271` `c-driver/cyw43_ll.c:424` `c-driver/cyw43_ll.c:425`

| Behaviour | whd | c-driver | embassy | linux | Citations |
|---|---|---|---|---|---|
| 4-byte flag (0x8000) | Only on 4-byte register accesses | Only on 4-byte register accesses. Bulk firmware download writes without it; cyw43_ll_write_backplane_mem / read_backplane_mem add it always. | Only on 4-byte register accesses | Always: word access is 32-bit only (brcmf_sdiod_readl/writel); bulk RAM and F2 transfers carry it too | `whd/src/bus_protocols/whd_bus_sdio_protocol.c:928` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:945` `c-driver/cyw43_ll.c:355` `c-driver/cyw43_ll.c:370` `c-driver/cyw43_ll.c:2569` `embassy/sdio.rs:86` `embassy/sdio.rs:109` `linux/brcmfmac/bcmsdh.c:254` |
| Window write | Cached; writes only the changed bytes, order HIGH, MID, LOW | Same as whd | Same as whd | If the cached window (sbwad) differs, writes all three bytes, order LOW, MID, HIGH; stops at the first error; updates the cache only if all succeeded | `whd/src/bus_protocols/whd_bus_sdio_protocol.c:2180` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:2184` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:2200` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:2217` `c-driver/cyw43_ll.c:334` `c-driver/cyw43_ll.c:337` `c-driver/cyw43_ll.c:343` `embassy/sdio.rs:125` `embassy/sdio.rs:133` `embassy/sdio.rs:149` `linux/brcmfmac/bcmsdh.c:234` |
| After a single register access | Moves the window back to CHIPCOMMON_BASE_ADDRESS (0x18000000) | Same as whd | Same as whd | Does not restore; every F2 transfer first sets the window to the chipcommon core base | `whd/src/bus_protocols/whd_bus_sdio_protocol.c:934` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:951` `c-driver/cyw43_ll.c:119` `c-driver/cyw43_ll.c:360` `c-driver/cyw43_ll.c:375` `embassy/sdio.rs:98` `embassy/sdio.rs:119` `embassy/consts.rs:235` `linux/brcmfmac/bcmsdh.c:546` |
| Maximum F1 chunk | 1536 bytes (WHD_BUS_SDIO_MAX_BACKPLANE_TRANSFER_SIZE) | 16384 bytes (CYW43_BUS_MAX_BLOCK_SIZE) | 1024 bytes (BLOCK_BUFFER_SIZE) | Up to the full 0x8000 window; linux's download loop writes the firmware in MEMBLOCK = 2048-byte pieces | `whd/src/bus_protocols/whd_bus_sdio_protocol.h:35` `c-driver/cyw43_ll.h:197` `embassy/consts.rs:113` `embassy/sdio.rs:269` `linux/brcmfmac/bcmsdh.c:677` `linux/brcmfmac/sdio.c:131` |

### DEVICE_CTL (0x10009) bits
| Mask | Name | Meaning (from the header comments) | Written by | Citations |
|---|---|---|---|---|
| 0x01 | SBSDIO_DEVCTL_SETBUSY | Device asserts busy when receiving CMD53 | defined only | `linux/brcmfmac/sdio.c:140` `linux/brcmfmac/sdio.c:141` |
| 0x02 | SBSDIO_DEVCTL_SPI_INTR_SYNC | SDIO interrupt assertion synchronous to the SDIO clock | defined only | `linux/brcmfmac/sdio.c:142` `linux/brcmfmac/sdio.c:143` |
| 0x04 | SBSDIO_DEVCTL_CA_INT_ONLY | Mask all interrupts to the host except chipActive (rev 8) | linux, around a pending HT-clock wait | `linux/brcmfmac/sdio.c:144` `linux/brcmfmac/sdio.c:145` `linux/brcmfmac/sdio.c:830` `linux/brcmfmac/sdio.c:841` `linux/brcmfmac/sdio.c:886` `linux/brcmfmac/sdio.c:2620` |
| 0x08 | SBSDIO_DEVCTL_PADS_ISO | Isolate internal SDIO signals, tri-state the pads; cleared only by an SDIO bus power cycle (rev 9). Defined by linux and whd; neither writes it. | defined only | `linux/brcmfmac/sdio.c:146` `linux/brcmfmac/sdio.c:148` `whd/src/bus_protocols/whd_sdio.h:204` |
| 0x10 | SBSDIO_DEVCTL_F2WM_ENAB | Enable F2 watermark | linux, for chips with a per-chip watermark (not the 43439) | `linux/brcmfmac/sdio.c:149` `linux/brcmfmac/sdio.c:150` `linux/brcmfmac/sdio.c:4292` `linux/brcmfmac/sdio.c:4305` `linux/brcmfmac/sdio.c:4319` `linux/brcmfmac/sdio.c:4332` `linux/brcmfmac/sdio.c:4347` |
| 0x30 | SBSDIO_DEVCTL_SB_RST_CTL | Two-bit field, force SD-to-SB reset mapping (rev 11): 0x00 RST_CORECTL (decided by a CoreControl bit), 0x10 RST_BPRESET (force backplane reset), 0x20 RST_NOBPRESET (force no backplane reset) | defined only | `linux/brcmfmac/sdio.c:151` `linux/brcmfmac/sdio.c:152` `linux/brcmfmac/sdio.c:154` `linux/brcmfmac/sdio.c:156` `linux/brcmfmac/sdio.c:158` |
| 0x40 | SBSDIO_DEVCTL_ADDR_RST | "Reset SB Address to default value". Not found in linux or c-driver. | whd, embassy, when reading the chip id from the SDIO core | `whd/src/bus_protocols/whd_sdio.h:225` `embassy/consts.rs:99` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:505` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:517` `embassy/runner.rs:356` `embassy/runner.rs:366` `linux/brcmfmac/sdio.c:138-158` `c-driver/cyw43_ll.c:108-114` |

- linux gives 0x10 two meanings: F2WM_ENAB and the RST_BPRESET value of the 0x30 field. The header does not reconcile them. `linux/brcmfmac/sdio.c:150` `linux/brcmfmac/sdio.c:152` `linux/brcmfmac/sdio.c:156`
- c-driver never touches DEVICE_CTL on SDIO. `c-driver/cyw43_ll.c:108`
- The "defined only" names (SETBUSY, SPI_INTR_SYNC, PADS_ISO, the SB_RST_CTL values) appear only at their definitions in the linux, whd, c-driver and embassy sources. `linux/brcmfmac/sdio.c:141` `linux/brcmfmac/sdio.c:143` `linux/brcmfmac/sdio.c:148` `linux/brcmfmac/sdio.c:152`
- Chip id from the SDIO core: whd and embassy set ADDR_RST, read back the three window registers to learn the SDIO core's base address, restore DEVICE_CTL, then read the chip id at base + 0x330 (SDIO_CORE_CHIPID_REG). `whd/src/bus_protocols/whd_sdio.h:207` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:503` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:507` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:511` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:514` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:518` `embassy/consts.rs:100` `embassy/runner.rs:350` `embassy/runner.rs:360` `embassy/runner.rs:364` `embassy/runner.rs:368`
- whd takes this path when CARDCAP bit 0x40 (CHIPID_PRESENT) is set; embassy takes it when CARDCAP bit 0x80 (SECURE_MODE) is set. `whd/src/bus_protocols/whd_bus_sdio_protocol.c:497` `embassy/runner.rs:347`
- whd's block is compiled only when DM_43022C1 is not defined. whd reads 4 bytes and splits id and revision; embassy reads 16 bits and gets the id only. `whd/src/bus_protocols/whd_bus_sdio_protocol.c:487` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:519` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:520` `embassy/runner.rs:368`

### FRAME_CONTROL (0x1000D) bits
| Mask | Name | Meaning | Written by | Citations |
|---|---|---|---|---|
| 0x01 | SFC_RF_TERM | Read frame terminate | linux (brcmf_sdio_rxfail), whd, embassy | `linux/brcmfmac/sdio.c:244` `whd/src/bus_protocols/whd_sdio.h:228` `embassy/consts.rs:238` `linux/brcmfmac/sdio.c:1218` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:1326` `embassy/sdio.rs:243` |
| 0x02 | SFC_WF_TERM | Write frame terminate | linux (brcmf_sdio_txfail) | `linux/brcmfmac/sdio.c:245` `whd/src/bus_protocols/whd_sdio.h:229` `linux/brcmfmac/sdio.c:1269` |
| 0x04 | SFC_CRC4WOOS | CRC error for write out of sync | defined only | `linux/brcmfmac/sdio.c:246` `whd/src/bus_protocols/whd_sdio.h:230` |
| 0x08 | SFC_ABORTALL | Abort all in-progress frames | defined only | `linux/brcmfmac/sdio.c:247` `whd/src/bus_protocols/whd_sdio.h:231` |

### CHIP_CLOCK_CSR (0x1000E) bits
| Mask | Name | Meaning | Citations |
|---|---|---|---|
| 0x01 | SBSDIO_FORCE_ALP | Force ALP request to backplane | `linux/brcmfmac/sdio.c:177` `whd/src/bus_protocols/whd_sdio.h:210` `embassy/consts.rs:118` `c-driver/cyw43_ll.c:216` |
| 0x02 | SBSDIO_FORCE_HT | Force HT request to backplane | `linux/brcmfmac/sdio.c:179` `whd/src/bus_protocols/whd_sdio.h:211` `embassy/consts.rs:119` `c-driver/cyw43_ll.c:217` |
| 0x04 | SBSDIO_FORCE_ILP | Force ILP request to backplane (linux, whd only) | `linux/brcmfmac/sdio.c:181` `whd/src/bus_protocols/whd_sdio.h:212` |
| 0x08 | SBSDIO_ALP_AVAIL_REQ | Make ALP ready (power up xtal) | `linux/brcmfmac/sdio.c:183` `whd/src/bus_protocols/whd_sdio.h:213` `embassy/consts.rs:115` `c-driver/cyw43_ll.c:136` `c-driver/cyw43_ll.c:215` |
| 0x10 | SBSDIO_HT_AVAIL_REQ | Make HT ready (power up PLL) | `linux/brcmfmac/sdio.c:185` `whd/src/bus_protocols/whd_sdio.h:214` `embassy/consts.rs:120` `c-driver/cyw43_ll.c:137` |
| 0x20 | SBSDIO_FORCE_HW_CLKREQ_OFF | Squelch clock requests from hardware | `linux/brcmfmac/sdio.c:187` `whd/src/bus_protocols/whd_sdio.h:215` `embassy/consts.rs:117` `c-driver/cyw43_ll.c:214` |
| 0x40 | SBSDIO_ALP_AVAIL | Status: ALP is ready | `linux/brcmfmac/sdio.c:189` `whd/src/bus_protocols/whd_sdio.h:216` `embassy/consts.rs:116` `c-driver/cyw43_ll.c:138` `c-driver/cyw43_ll.c:213` |
| 0x80 | SBSDIO_HT_AVAIL | Status: HT is ready. embassy has no named constant; it tests the literal 0x80 or BACKPLANE_HT_AVAIL_REQ << 3. | `linux/brcmfmac/sdio.c:191` `whd/src/bus_protocols/whd_sdio.h:217` `c-driver/cyw43_ll.c:139` `embassy/runner.rs:416` `embassy/runner.rs:607` `embassy/runner.rs:779` |

- linux masks: SBSDIO_CSR_MASK = 0x1F (the five request/force bits); SBSDIO_AVBITS = 0xC0. `linux/brcmfmac/sdio.c:192` `linux/brcmfmac/sdio.c:193`
- linux tests: ALPAV is true when either availability bit is set; HTAV is true only when both are set (v & 0xC0 == 0xC0); ALPONLY = ALPAV and not HTAV; CLKAV(v, alponly) = ALPAV and (alponly or HTAV). `linux/brcmfmac/sdio.c:194` `linux/brcmfmac/sdio.c:195` `linux/brcmfmac/sdio.c:196` `linux/brcmfmac/sdio.c:197` `linux/brcmfmac/sdio.c:198`
- whd, c-driver and embassy test only the single bit 0x80 for HT. `whd/src/bus_protocols/whd_bus_sdio_protocol.c:1260` `c-driver/cyw43_ll.c:1810` `embassy/runner.rs:607`
- whd also defines SBSDIO_Rev8_HT_AVAIL = 0x40 and SBSDIO_Rev8_ALP_AVAIL = 0x80: the two status bits swapped for SDIO core rev 8. Not found in linux. `whd/src/bus_protocols/whd_sdio.h:218` `whd/src/bus_protocols/whd_sdio.h:219` `linux/brcmfmac/sdio.c:175-195`

### PULL_UP (0x1000F)
| Driver | Writes | Citations |
|---|---|---|
| linux | 0 only, during bring-up ("disable the extra SDIO pull-ups") | `linux/brcmfmac/sdio.c:3887` `linux/brcmfmac/sdio.c:3888` |
| whd | 0 during bring-up; 0xF after enabling save/restore, with the comment "Put SPI interface block to sleep" | `whd/src/bus_protocols/whd_bus_sdio_protocol.c:472` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:473` `whd/src/whd_chip.c:1288` `whd/src/whd_chip.c:1289` |
| c-driver | 0xF after enabling save/restore, then at once 0 ("CLEAR PAD PULLS") and a read-back | `c-driver/cyw43_ll.c:1884` `c-driver/cyw43_ll.c:1885` `c-driver/cyw43_ll.c:1889` `c-driver/cyw43_ll.c:1891` `c-driver/cyw43_ll.c:1892` |
| embassy | 0 during bring-up; 0 and a read-back in 43439 init; never 0xF | `embassy/runner.rs:304` `embassy/runner.rs:305` `embassy/runner.rs:406` |

### MESBUSYCTRL (0x1001D) bits
| Bits | Name | Meaning | Citations |
|---|---|---|---|
| 6:0 (mask 0x7F) | SBSDIO_MESBUSY_RXFIFO_WM | "Watermark for sdio device RX path" | `linux/brcmfmac/sdio.h:96` `linux/brcmfmac/sdio.h:97` `linux/brcmfmac/sdio.h:98` `linux/brcmfmac/sdio.h:99` |
| 7 (0x80) | SBSDIO_MESBUSYCTRL_ENAB | "Enable busy capability for MES access" | `linux/brcmfmac/sdio.h:100` `linux/brcmfmac/sdio.h:101` |

Not found in whd, c-driver, embassy. `whd/src/bus_protocols/whd_sdio.h:98-112` `c-driver/cyw43_ll.c:108-114` `embassy/consts.rs:55-69`

### WAKEUP_CTRL (0x1001E) bits
| Mask | Name | Notes | Citations |
|---|---|---|---|
| 0x01 | WakeTillAlpAvail (linux SBSDIO_FUNC1_WCTRL_ALPWAIT; whd SBSDIO_WCTRL_WL_WAKE_TILL_ALP_AVAIL) | | `linux/brcmfmac/sdio.h:105` `linux/brcmfmac/sdio.h:106` `whd/src/bus_protocols/whd_sdio.h:240` `embassy/consts.rs:121` `c-driver/cyw43_ll.c:230` |
| 0x02 | WakeTillHTAvail (linux SBSDIO_FUNC1_WCTRL_HTWAIT; whd SBSDIO_WCTRL_WL_WAKE_TILL_HT_AVAIL) | embassy has no named constant; the literal 0x02 appears only in commented-out code. | `linux/brcmfmac/sdio.h:107` `linux/brcmfmac/sdio.h:108` `whd/src/bus_protocols/whd_sdio.h:241` `c-driver/cyw43_ll.c:231` `embassy/runner.rs:394` |
| 0x04 | BT_WakeTillAlpAvail (whd, "in case of sdiorev31") | whd ORs it in instead of the WL bit in CP_OVER_SDIO builds for the ALP-family chips. | `whd/src/bus_protocols/whd_sdio.h:242` `whd/src/bus_protocols/whd_sdio.h:243` `whd/src/whd_chip.c:1217` `whd/src/whd_chip.c:1218` |
| 0x08 | BT_WakeTillHTAvail (whd) | defined only | `whd/src/bus_protocols/whd_sdio.h:244` |
| 0x10 | WL_DisableKSOAutoSet (whd) | defined only | `whd/src/bus_protocols/whd_sdio.h:245` |
| 0x20 | BT_DisableKSOAutoSet (whd) | defined only | `whd/src/bus_protocols/whd_sdio.h:246` |

The four whd-only bits are not found in linux, c-driver or embassy. `linux/brcmfmac/sdio.h:104-108` `c-driver/cyw43_ll.c:230-231` `embassy/consts.rs:121`

### SLEEP_CSR (0x1001F) bits
| Mask | Name | Notes | Citations |
|---|---|---|---|
| 0x01 | KSO, "keep SDIO on" (linux SBSDIO_FUNC1_SLEEPCSR_KSO_MASK, enable value 1; whd SBSDIO_SLPCSR_KEEP_WL_KSO; c-driver SBSDIO_SLPCSR_KEEP_SDIO_ON; embassy SBSDIO_SLPCSR_KEEP_WL_KS) | | `linux/brcmfmac/sdio.h:110` `linux/brcmfmac/sdio.h:111` `linux/brcmfmac/sdio.h:112` `whd/src/bus_protocols/whd_sdio.h:249` `c-driver/cyw43_ll.c:234` `embassy/consts.rs:84` |
| 0x02 | DEVON, "device on" status; the drivers only read it (linux SBSDIO_FUNC1_SLEEPCSR_DEVON_MASK; whd SBSDIO_SLPCSR_WL_DEVON; c-driver SBSDIO_SLPCSR_DEVICE_ON) | | `linux/brcmfmac/sdio.h:113` `linux/brcmfmac/sdio.h:114` `whd/src/bus_protocols/whd_sdio.h:250` `c-driver/cyw43_ll.c:235` `embassy/consts.rs:85` |
| 0x04 | SBSDIO_SLPCSR_KEEP_BT_KSO (whd, "in case of sdiorev31") | In CP_OVER_SDIO builds on 55500/55530, whd_kso_enable writes this bit and compares against KEEP_BT_KSO + BT_DEVON instead of the WL bits. | `whd/src/bus_protocols/whd_sdio.h:251` `whd/src/bus_protocols/whd_sdio.h:252` `whd/src/whd_chip.c:1314` `whd/src/whd_chip.c:1317` `whd/src/whd_chip.c:1378` |
| 0x08 | SBSDIO_SLPCSR_BT_DEVON (whd) | Same use as above. | `whd/src/bus_protocols/whd_sdio.h:253` `whd/src/whd_chip.c:1378` |

- The two BT bits are not found in linux, c-driver or embassy. `linux/brcmfmac/sdio.h:109-114` `c-driver/cyw43_ll.c:234-235` `embassy/consts.rs:83-85`
- linux treats KSO as an SDIO core rev 12 feature: brcmf_sdio_kso_init returns without touching SLEEP_CSR when the core rev is below 12, and the header groups WAKEUPCTRL and SLEEPCSR under "Sdio Core Rev 12". `linux/brcmfmac/sdio.c:3506` `linux/brcmfmac/sdio.c:3507` `linux/brcmfmac/sdio.c:3508` `linux/brcmfmac/sdio.h:103`

### Bootloader handshake registers (whd only; secure-bootloader chips, not the 43439)

- whd defines SDIO_REG_DAR_H2D_MSG_0 = 0x10030 and SDIO_REG_DAR_D2H_MSG_0 = 0x10038 when DM_43022C1 is not defined; with it they are 0x18002000 + 0x48 and + 0x4C. Used only in BLHS_SUPPORT builds. `whd/src/bus_protocols/whd_sdio.h:266` `whd/src/bus_protocols/whd_sdio.h:267` `whd/src/bus_protocols/whd_sdio.h:268` `whd/src/bus_protocols/whd_sdio.h:270` `whd/src/bus_protocols/whd_sdio.h:271` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:1783`

| Register | Bit | Name | Citations |
|---|---|---|---|
| D2H (0x10038) | 0 | START | `whd/src/bus_protocols/whd_sdio.h:277` |
| D2H | 1 | READY | `whd/src/bus_protocols/whd_sdio.h:278` |
| D2H | 2 | STEADY | `whd/src/bus_protocols/whd_sdio.h:279` |
| D2H | 3 | TRXHDR_PARSE_DONE | `whd/src/bus_protocols/whd_sdio.h:280` |
| D2H | 4 | VALDN_START | `whd/src/bus_protocols/whd_sdio.h:281` |
| D2H | 5 | VALDN_RESULT | `whd/src/bus_protocols/whd_sdio.h:282` |
| D2H | 6 | VALDN_DONE | `whd/src/bus_protocols/whd_sdio.h:283` |
| D2H | 7 | NVRAM_MV_DONE | `whd/src/bus_protocols/whd_sdio.h:284` |
| D2H | 8 | BP_CLK_DIS_REQ (DM_43022C1 only) | `whd/src/bus_protocols/whd_sdio.h:285` `whd/src/bus_protocols/whd_sdio.h:286` |
| H2D (0x10030) | value 0 | BL_INIT | `whd/src/bus_protocols/whd_sdio.h:290` |
| H2D | 0 | DL_FW_START | `whd/src/bus_protocols/whd_sdio.h:291` |
| H2D | 1 | DL_FW_DONE | `whd/src/bus_protocols/whd_sdio.h:292` |
| H2D | 2 | DL_NVRAM_DONE | `whd/src/bus_protocols/whd_sdio.h:293` |
| H2D | 3 | BL_RESET_ON_ERROR | `whd/src/bus_protocols/whd_sdio.h:294` |
| H2D | 4 | DL_NVRAM_START (DM_43022C1 only) | `whd/src/bus_protocols/whd_sdio.h:295` `whd/src/bus_protocols/whd_sdio.h:296` |
| H2D | 5 | BP_CLK_DIS_ACK (DM_43022C1 only) | `whd/src/bus_protocols/whd_sdio.h:297` |

- SDIO_BLHS_D2H_TIMEOUT_MS = 1000. `whd/src/bus_protocols/whd_sdio.h:274`
- whd reads and writes the H2D register as 1 byte with F1 CMD52. It polls the D2H register as 1 byte (2 with DM_43022C1) every 10 ms until the wanted flag is set, up to 1000 ms. `whd/src/bus_protocols/whd_bus_sdio_protocol.c:1786` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:1791` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:1801` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:1807` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:1810` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:1813`
- whd stages: CHK_BL_INIT writes BL_INIT then waits for READY; PREP_FW_DOWNLOAD writes DL_FW_START; POST_FW_DOWNLOAD writes DL_FW_DONE and then, without DM_43022C1, waits for TRXHDR_PARSE_DONE. `whd/src/bus_protocols/whd_bus_sdio_protocol.c:1840` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:1846` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:1848` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:1850` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:1852` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:1855` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:1895`
- whd later stages: CHK_FW_VALIDATION waits for VALDN_DONE and then VALDN_RESULT; POST_NVRAM_DOWNLOAD ORs DL_NVRAM_DONE into the H2D register. When a wait fails whd ORs BL_RESET_ON_ERROR into the H2D register and returns WHD_BLHS_VALIDATE_FAILED. `whd/src/bus_protocols/whd_bus_sdio_protocol.c:1908` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:1910` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:1911` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:1914` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:1915` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:1916` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:1926` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:1929`
- Not found in linux, c-driver, embassy. `linux/brcmfmac/sdio.h:54-117` `c-driver/cyw43_ll.c:108-114` `embassy/consts.rs:55-69`

### SDIO core registers (reached through the window)

- For the CYW43439, whd, embassy and c-driver place the SDIO device core at backplane address 0x18002000. `whd/src/whd_chip_constants.c:302` `whd/src/whd_chip_constants.c:304` `embassy/lib.rs:270` `embassy/lib.rs:276` `c-driver/cyw43_ll.c:120`
- linux does not hardcode it; it looks the core up by id BCMA_CORE_SDIO_DEV after chip enumeration. `linux/brcmfmac/sdio.c:3997`

The registers the small drivers use:

| Offset | whd / embassy name | linux field | Defined by | Citations |
|---|---|---|---|---|
| core + 0x20 | INT_STATUS | intstatus | whd, embassy, c-driver, linux | `whd/src/bus_protocols/whd_sdio.h:32` `embassy/consts.rs:74` `linux/brcmfmac/sdio.h:216` `c-driver/cyw43_ll.c:129` |
| core + 0x24 | INT_HOST_MASK | hostintmask | whd, embassy, c-driver, linux | `whd/src/bus_protocols/whd_sdio.h:36` `embassy/consts.rs:75` `linux/brcmfmac/sdio.h:217` `c-driver/cyw43_ll.c:130` |
| core + 0x34 | FUNCTION_INT_MASK | funcintmask | whd, embassy, c-driver, linux | `whd/src/bus_protocols/whd_sdio.h:37` `embassy/consts.rs:76` `linux/brcmfmac/sdio.h:221` `c-driver/cyw43_ll.c:131` |
| core + 0x40 | TO_SB_MAILBOX | tosbmailbox | whd, embassy, c-driver, linux | `whd/src/bus_protocols/whd_sdio.h:33` `embassy/consts.rs:80` `linux/brcmfmac/sdio.h:223` `c-driver/cyw43_ll.c:132` |
| core + 0x48 | TO_SB_MAILBOX_DATA | tosbmailboxdata | whd, embassy, linux; not c-driver | `whd/src/bus_protocols/whd_sdio.h:34` `embassy/consts.rs:81` `linux/brcmfmac/sdio.h:225` `c-driver/cyw43_ll.c:129-132` |
| core + 0x4C | TO_HOST_MAILBOX_DATA | tohostmailboxdata | whd, embassy, linux; not c-driver | `whd/src/bus_protocols/whd_sdio.h:35` `embassy/consts.rs:82` `linux/brcmfmac/sdio.h:226` `c-driver/cyw43_ll.c:129-132` |
| core + 0x330 | SDIO_CORE_CHIPID_REG | not found (falls in unnamed "DMA engines" padding) | whd, embassy | `whd/src/bus_protocols/whd_sdio.h:206` `whd/src/bus_protocols/whd_sdio.h:207` `embassy/consts.rs:100` `linux/brcmfmac/sdio.h:259` |

- whd reads 0x330 when CARDCAP reports CHIPID_PRESENT: low 16 bits are the chip id, bits 19:16 the chip revision. embassy reads only 16 bits there, so the revision field is whd-only. `whd/src/bus_protocols/whd_bus_sdio_protocol.c:514` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:518` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:519` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:520`

linux's struct sdpcmd_regs, the full map. Fields are 4 bytes unless noted. Offsets are (compiled); total size 4096 (0x1000) bytes. `linux/brcmfmac/sdio.h:199` `linux/brcmfmac/sdio.h:285`

| Offset | Field | Notes | Citations |
|---|---|---|---|
| 0x000 | corecontrol | | `linux/brcmfmac/sdio.h:200` |
| 0x004 | corestatus | | `linux/brcmfmac/sdio.h:201` |
| 0x00C | biststatus | | `linux/brcmfmac/sdio.h:202` `linux/brcmfmac/sdio.h:203` |
| 0x010 | pcmciamesportaladdr | 2 bytes | `linux/brcmfmac/sdio.h:206` |
| 0x014 | pcmciamesportalmask | 2 bytes | `linux/brcmfmac/sdio.h:208` |
| 0x018 | pcmciawrframebc | 2 bytes | `linux/brcmfmac/sdio.h:210` |
| 0x01C | pcmciaunderflowtimer | 2 bytes | `linux/brcmfmac/sdio.h:212` |
| 0x020 | intstatus | | `linux/brcmfmac/sdio.h:216` |
| 0x024 | hostintmask | | `linux/brcmfmac/sdio.h:217` |
| 0x028 | intmask | | `linux/brcmfmac/sdio.h:218` |
| 0x02C | sbintstatus | | `linux/brcmfmac/sdio.h:219` |
| 0x030 | sbintmask | | `linux/brcmfmac/sdio.h:220` |
| 0x034 | funcintmask | | `linux/brcmfmac/sdio.h:221` |
| 0x040 | tosbmailbox | | `linux/brcmfmac/sdio.h:223` |
| 0x044 | tohostmailbox | | `linux/brcmfmac/sdio.h:224` |
| 0x048 | tosbmailboxdata | | `linux/brcmfmac/sdio.h:225` |
| 0x04C | tohostmailboxdata | | `linux/brcmfmac/sdio.h:226` |
| 0x050 | sdioaccess | synchronized access to registers in the SDIO clock domain | `linux/brcmfmac/sdio.h:229` |
| 0x060 | pcmciaframectrl | 1 byte | `linux/brcmfmac/sdio.h:233` |
| 0x064 | pcmciawatermark | 1 byte | `linux/brcmfmac/sdio.h:235` |
| 0x100 | intrcvlazy | interrupt batching control | `linux/brcmfmac/sdio.h:239` |
| 0x110 | cmd52rd | counter (rev 8) | `linux/brcmfmac/sdio.h:242` `linux/brcmfmac/sdio.h:243` |
| 0x114 | cmd52wr | counter | `linux/brcmfmac/sdio.h:244` |
| 0x118 | cmd53rd | counter | `linux/brcmfmac/sdio.h:245` |
| 0x11C | cmd53wr | counter | `linux/brcmfmac/sdio.h:246` |
| 0x120 | abort | counter | `linux/brcmfmac/sdio.h:247` |
| 0x124 | datacrcerror | counter | `linux/brcmfmac/sdio.h:248` |
| 0x128 | rdoutofsync | counter | `linux/brcmfmac/sdio.h:249` |
| 0x12C | wroutofsync | counter | `linux/brcmfmac/sdio.h:250` |
| 0x130 | writebusy | counter | `linux/brcmfmac/sdio.h:251` |
| 0x134 | readwait | counter | `linux/brcmfmac/sdio.h:252` |
| 0x138 | readterm | counter | `linux/brcmfmac/sdio.h:253` |
| 0x13C | writeterm | counter | `linux/brcmfmac/sdio.h:254` |
| 0x1E0 | clockctlstatus | | `linux/brcmfmac/sdio.h:256` |
| 0x400-0x5FF | cis[512] | SDIO/PCMCIA CIS region (rev 6) | `linux/brcmfmac/sdio.h:261` `linux/brcmfmac/sdio.h:262` |
| 0x600-0x6FF | pcmciafcr[256] | | `linux/brcmfmac/sdio.h:264` `linux/brcmfmac/sdio.h:265` |
| 0x76E | backplanecsr | 2 bytes; followed by backplaneaddr0-3 and backplanedata0-3, 2 bytes each | `linux/brcmfmac/sdio.h:269` `linux/brcmfmac/sdio.h:270` `linux/brcmfmac/sdio.h:274` |
| 0x7BE | spromstatus | 2 bytes (rev 2) | `linux/brcmfmac/sdio.h:281` |

The statistics counters are not found in whd, embassy or c-driver. `whd/src/bus_protocols/whd_sdio.h:31-37` `embassy/consts.rs:74-82` `c-driver/cyw43_ll.c:129-132`

corecontrol (core + 0x00) bits, linux names only:

| Bit | Name | Meaning | Citations |
|---|---|---|---|
| 0 | CC_CISRDY | CIS ready. Not found in whd. | `linux/brcmfmac/sdio.c:236` `whd/src/bus_protocols/whd_sdio.h:31-37` |
| 1 | CC_BPRESEN | CCCR RES signal | `linux/brcmfmac/sdio.c:237` |
| 2 | CC_F2RDY | set CCCR IOR2 bit | `linux/brcmfmac/sdio.c:238` |
| 3 | CC_CLRPADSISO | clear SDIO pads isolation | `linux/brcmfmac/sdio.c:239` |
| 4 | CC_XMTDATAAVAIL_MODE | no comment in the source | `linux/brcmfmac/sdio.c:240` |
| 5 | CC_XMTDATAAVAIL_CTRL | no comment in the source | `linux/brcmfmac/sdio.c:241` |

These corecontrol names are definitions only: no code in linux's SDIO files reads or writes corecontrol. `linux/brcmfmac/sdio.c:236` `linux/brcmfmac/sdio.c:241`

### sdpcm_shared (linux, DEBUG builds)

- linux reads the address of the sdpcm_shared structure from the last 4-byte word of RAM: rambase + ramsize - 4, minus the SR memory size when rambase is 0 and brcmf_chip_sr_capable returns true. `linux/brcmfmac/sdio.c:1043` `linux/brcmfmac/sdio.c:1044` `linux/brcmfmac/sdio.c:1045`
- linux treats the word as invalid if it is 0 or still holds the NVRAM-length pattern (high half = inverse of low half). `linux/brcmfmac/sdio.c:1022` `linux/brcmfmac/sdio.c:1024`
- Structure as linux declares it: flags, trap_addr, assert_exp_addr, assert_file_addr, assert_line, console_addr, msgtrace_addr (4 bytes each), tag[32], brpt_addr. `linux/brcmfmac/sdio.c:365` `linux/brcmfmac/sdio.c:366` `linux/brcmfmac/sdio.c:370` `linux/brcmfmac/sdio.c:372` `linux/brcmfmac/sdio.c:373` `linux/brcmfmac/sdio.c:374`
- Flags: version mask 0x00FF (linux supports up to 3), ASSERT_BUILT 0x0100, ASSERT 0x0200, TRAP 0x0400. `linux/brcmfmac/sdio.c:296` `linux/brcmfmac/sdio.c:297` `linux/brcmfmac/sdio.c:298` `linux/brcmfmac/sdio.c:299` `linux/brcmfmac/sdio.c:300` `linux/brcmfmac/sdio.c:1081`

## Mailbox and interrupt bits

### intstatus (core + 0x20)
| Bit | Mask | Name | Meaning (linux comments) | Citations |
|---|---|---|---|---|
| 0 | 0x00000001 | I_SMB_SW0 | To-SB mail software interrupt 0 | `linux/brcmfmac/sdio.c:201` |
| 1 | 0x00000002 | I_SMB_SW1 | To-SB mail software interrupt 1 | `linux/brcmfmac/sdio.c:202` |
| 2 | 0x00000004 | I_SMB_SW2 | To-SB mail software interrupt 2 | `linux/brcmfmac/sdio.c:203` |
| 3 | 0x00000008 | I_SMB_SW3 | To-SB mail software interrupt 3 | `linux/brcmfmac/sdio.c:204` |
| 4 | 0x00000010 | I_HMB_SW0 = I_HMB_FC_STATE | To-host mail software interrupt 0: flow control state | `linux/brcmfmac/sdio.c:207` `linux/brcmfmac/sdio.c:267` `whd/src/bus_protocols/whd_sdio.h:115` |
| 5 | 0x00000020 | I_HMB_SW1 = I_HMB_FC_CHANGE | To-host mail software interrupt 1: flow control state changed | `linux/brcmfmac/sdio.c:208` `linux/brcmfmac/sdio.c:268` `whd/src/bus_protocols/whd_sdio.h:116` `embassy/consts.rs:72` `c-driver/cyw43_ll.c:117` |
| 6 | 0x00000040 | I_HMB_SW2 = I_HMB_FRAME_IND | To-host mail software interrupt 2: frame indication | `linux/brcmfmac/sdio.c:209` `linux/brcmfmac/sdio.c:269` `whd/src/bus_protocols/whd_sdio.h:117` |
| 7 | 0x00000080 | I_HMB_SW3 = I_HMB_HOST_INT | To-host mail software interrupt 3: miscellaneous interrupt (host mailbox data available) | `linux/brcmfmac/sdio.c:210` `linux/brcmfmac/sdio.c:270` `whd/src/bus_protocols/whd_sdio.h:118` `embassy/consts.rs:89` |
| 8 | 0x00000100 | I_WR_OOSYNC | Write frame out of sync | `linux/brcmfmac/sdio.c:213` |
| 9 | 0x00000200 | I_RD_OOSYNC | Read frame out of sync | `linux/brcmfmac/sdio.c:214` |
| 10 | 0x00000400 | I_PC | Descriptor error | `linux/brcmfmac/sdio.c:215` |
| 11 | 0x00000800 | I_PD | Data error | `linux/brcmfmac/sdio.c:216` |
| 12 | 0x00001000 | I_DE | Descriptor protocol error | `linux/brcmfmac/sdio.c:217` |
| 13 | 0x00002000 | I_RU | Receive descriptor underflow | `linux/brcmfmac/sdio.c:218` |
| 14 | 0x00004000 | I_RO | Receive FIFO overflow | `linux/brcmfmac/sdio.c:219` |
| 15 | 0x00008000 | I_XU | Transmit FIFO underflow | `linux/brcmfmac/sdio.c:220` |
| 16 | 0x00010000 | I_RI | Receive interrupt | `linux/brcmfmac/sdio.c:221` |
| 17 | 0x00020000 | I_BUSPWR | SDIO bus power change (rev 9). Defined only. | `linux/brcmfmac/sdio.c:222` |
| 18-22 | | not named | No driver names these bits. | `linux/brcmfmac/sdio.c:222` `linux/brcmfmac/sdio.c:223` |
| 23 | 0x00800000 | I_XMTDATA_AVAIL | "bits in fifo". Defined only. | `linux/brcmfmac/sdio.c:223` |
| 24 | 0x01000000 | I_XI | Transmit interrupt | `linux/brcmfmac/sdio.c:224` |
| 25 | 0x02000000 | I_RF_TERM | Read frame terminate. Defined only. | `linux/brcmfmac/sdio.c:225` |
| 26 | 0x04000000 | I_WF_TERM | Write frame terminate. Defined only. | `linux/brcmfmac/sdio.c:226` |
| 27 | 0x08000000 | I_PCMCIA_XU | PCMCIA transmit FIFO underflow | `linux/brcmfmac/sdio.c:227` |
| 28 | 0x10000000 | I_SBINT | sbintstatus interrupt | `linux/brcmfmac/sdio.c:228` |
| 29 | 0x20000000 | I_CHIPACTIVE | Chip from doze to active state | `linux/brcmfmac/sdio.c:229` |
| 30 | 0x40000000 | I_SRESET | CCCR RES interrupt. Defined only. | `linux/brcmfmac/sdio.c:230` |
| 31 | 0x80000000 | I_IOE2 | CCCR IOE2 bit changed. Defined only. | `linux/brcmfmac/sdio.c:231` |

- "Defined only": no code in linux's sdio.c, sdio.h or bcmsdh.c tests I_BUSPWR, I_XMTDATA_AVAIL, I_RF_TERM, I_WF_TERM, I_SRESET or I_IOE2. `linux/brcmfmac/sdio.c:222` `linux/brcmfmac/sdio.c:223` `linux/brcmfmac/sdio.c:225` `linux/brcmfmac/sdio.c:226` `linux/brcmfmac/sdio.c:230` `linux/brcmfmac/sdio.c:231`
- linux group masks: I_SMB_SW_MASK = 0x0000000F (shift 0); I_HMB_SW_MASK = 0x000000F0 (shift 4); I_ERRORS = I_PC, I_PD, I_DE, I_RU, I_RO, I_XU (0x0000FC00); I_DMA = I_RI, I_XI and I_ERRORS. `linux/brcmfmac/sdio.c:205` `linux/brcmfmac/sdio.c:206` `linux/brcmfmac/sdio.c:211` `linux/brcmfmac/sdio.c:212` `linux/brcmfmac/sdio.c:232` `linux/brcmfmac/sdio.c:233`
- whd, embassy and c-driver define only I_HMB_SW_MASK = 0xF0. `whd/src/bus_protocols/whd_sdio.h:113` `embassy/consts.rs:71` `c-driver/cyw43_ll.c:116`
- Every driver acknowledges interrupts by writing the bits it read back to intstatus (the drivers treat it as write-1-to-clear). `linux/brcmfmac/sdio.c:2577` `linux/brcmfmac/sdio.c:2578` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:245` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:790` `embassy/runner.rs:1011` `c-driver/cyw43_ll.c:1113`
- whd defines FRAME_AVAILABLE_MASK = I_HMB_SW_MASK (0xF0): any of the four host-mailbox bits left after acknowledgement means "a frame may be available". embassy copies this. `whd/src/bus_protocols/whd_sdio.h:120` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:798` `embassy/consts.rs:73` `embassy/runner.rs:997`
- linux reads frames only on I_HMB_FRAME_IND (bit 6) and only while clkstate == CLK_AVAIL. `linux/brcmfmac/sdio.c:2690`
- embassy comment: on the CYW4373, bit 17 (0x20000) is set and stays set if only the 0xF0 bits are cleared, causing an endless poll loop; embassy therefore writes back every bit it read. linux names bit 17 I_BUSPWR. `embassy/runner.rs:1001` `embassy/runner.rs:1004` `embassy/runner.rs:1008` `embassy/runner.rs:1011` `linux/brcmfmac/sdio.c:222`

### hostintmask (core + 0x24) and funcintmask (core + 0x34)
| Register | whd, c-driver, embassy | linux | Citations |
|---|---|---|---|
| hostintmask | Written with I_HMB_SW_MASK (0xF0) as a 4-byte backplane write once HT is available after firmware start | Written with I_HMB_SW_MASK + I_CHIPACTIVE (0x200000F0), only after F2 was enabled | `whd/src/bus_protocols/whd_bus_sdio_protocol.c:85` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:1283` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:1284` `c-driver/cyw43_ll.c:1821` `c-driver/cyw43_ll.c:1822` `embassy/runner.rs:613` `embassy/runner.rs:616` `linux/brcmfmac/sdio.c:782` `linux/brcmfmac/sdio.c:4279` |
| funcintmask | Written with 0x03 as a 1-byte backplane write right after hostintmask: bit 0 (0x01) SDIO_FUNC_MASK_F1, bit 1 (0x02) SDIO_FUNC_MASK_F2 | Never written; the field exists only in struct sdpcmd_regs | `whd/src/bus_protocols/whd_sdio.h:199` `whd/src/bus_protocols/whd_sdio.h:200` `whd/src/bus_protocols/whd_sdio.h:201` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:1286` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:1288` `c-driver/cyw43_ll.c:1825` `c-driver/cyw43_ll.c:1826` `embassy/runner.rs:621` `embassy/runner.rs:622` `linux/brcmfmac/sdio.h:221` |

- whd comment on funcintmask: this turns on the F2 interrupts, which the 43362 needs although the 4319 did not. `whd/src/bus_protocols/whd_bus_sdio_protocol.c:1286`
- linux filters intstatus through its saved copy of hostintmask before acting. `linux/brcmfmac/sdio.c:2573`
- linux on bus stop writes 0 to hostintmask, disables F2, then clears the previously enabled bits in intstatus. `linux/brcmfmac/sdio.c:2494` `linux/brcmfmac/sdio.c:2495` `linux/brcmfmac/sdio.c:2498` `linux/brcmfmac/sdio.c:2517` `linux/brcmfmac/sdio.c:2521`
- embassy has a second, different use of these offsets. enable_sdio_interrupts() writes 0xFF to address 0x24 and 0x02 to address 0x34 with function 0 CMD52 writes: these go to F0 addresses 0x24 and 0x34, not to the SDIO core's backplane registers. `embassy/runner.rs:289` `embassy/runner.rs:290` `embassy/runner.rs:294` `embassy/runner.rs:295` `embassy/consts.rs:75` `embassy/consts.rs:76` `embassy/consts.rs:77`
- embassy names the 0x02 value SDIO_FUNC_INT_MASK_F1, where whd's bit 1 is F2. `embassy/consts.rs:78` `whd/src/bus_protocols/whd_sdio.h:201`
- The same embassy function first writes SEP_INT_CTL (F0 0xF2) = 0x03 and last writes the CCCR interrupt-enable register = CCCR_INT_ENABLE_MASTER (0x01). Its doc comment calls the 0x24 write "Unmask all host-visible SDIOD interrupt sources". `embassy/runner.rs:278` `embassy/runner.rs:281` `embassy/runner.rs:284` `embassy/runner.rs:300` `embassy/consts.rs:79`
- whd and c-driver write these registers only through the backplane window at core base + offset. No other driver writes F0 0x24 or 0x34. Whether those F0 addresses mean anything to the chip cannot be settled from these sources. `whd/src/bus_protocols/whd_bus_sdio_protocol.c:1284` `c-driver/cyw43_ll.c:1822`

### tosbmailbox (core + 0x40) and tosbmailboxdata (core + 0x48)

linux and whd comment: the tosbmailbox bits correspond to intstatus bits (linux names those I_SMB_SW0..3). `linux/brcmfmac/sdio.c:253` `linux/brcmfmac/sdio.c:201` `whd/src/bus_protocols/whd_sdio.h:233`

| Bit | Mask | Name | Meaning | Written by | Citations |
|---|---|---|---|---|---|
| 0 | 0x01 | SMB_NAK | Frame NAK | linux; whd has the code but never reaches it | `linux/brcmfmac/sdio.c:254` `whd/src/bus_protocols/whd_sdio.h:234` |
| 1 | 0x02 | SMB_INT_ACK | Host interrupt ACK | linux, whd, embassy | `linux/brcmfmac/sdio.c:255` `whd/src/bus_protocols/whd_sdio.h:235` `embassy/consts.rs:88` |
| 2 | 0x04 | SMB_USE_OOB | Use OOB wakeup | none; defined by linux and whd, never written | `linux/brcmfmac/sdio.c:256` `whd/src/bus_protocols/whd_sdio.h:236` |
| 3 | 0x08 | SMB_DEV_INT | Miscellaneous interrupt | whd, embassy, c-driver (c-driver uses the literal 1 << 3); linux defines it but never writes it | `linux/brcmfmac/sdio.c:257` `whd/src/bus_protocols/whd_sdio.h:237` `embassy/consts.rs:87` `c-driver/cyw43_ll.c:790` |

- tosbmailboxdata: linux puts the host's SDPCM protocol version in bits 23:16 (SMB_DATA_VERSION_SHIFT = 16) and writes SDPCM_PROT_VERSION (4) << 16 just before enabling F2. `linux/brcmfmac/sdio.c:259` `linux/brcmfmac/sdio.c:260` `linux/brcmfmac/sdio.c:290` `linux/brcmfmac/sdio.c:4267` `linux/brcmfmac/sdio.c:4269` `linux/brcmfmac/sdio.c:4271`
- embassy does the same write (4 << 16) only for the 43455. `embassy/runner.rs:644`
- whd defines the register but never writes it in the SDIO protocol file. Not found in c-driver. `whd/src/bus_protocols/whd_sdio.h:34` `c-driver/cyw43_ll.c:129-132`

The transmit "poke":

- When the host has something to send but no transmit credit, whd, c-driver and embassy write SMB_DEV_INT (0x08) to tosbmailbox as a 4-byte backplane write. `whd/src/bus_protocols/whd_bus_sdio_protocol.c:1346` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:1348` `c-driver/cyw43_ll.c:790` `embassy/runner.rs:945`
- whd pokes each time its event wait is entered with a packet queued and zero credits. That wait is capped at WHD_THREAD_POKE_TIMEOUT = 100 ms, so 100 ms is the longest gap between pokes. `whd/src/bus_protocols/whd_bus_sdio_protocol.c:83` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:272` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:276` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:280`
- c-driver re-pokes no more often than once per 100 ms while stalled (flow control set, or last credit == tx sequence number). The poke is compiled only for SDIO. `c-driver/cyw43_ll.c:779` `c-driver/cyw43_ll.c:783` `c-driver/cyw43_ll.c:786` `c-driver/cyw43_ll.c:789`
- embassy pokes once per stalled loop iteration, then waits for a bus event (with the `bluetooth` feature: for a bus event or Bluetooth receive-queue space, whichever comes first); it has no 100 ms timer. The poke itself is made only on SDIO. `embassy/runner.rs:941` `embassy/runner.rs:942` `embassy/runner.rs:956` `embassy/runner.rs:959`
- Not found in linux: `SMB_DEV_INT` is defined (the line cited) and never used. `linux/brcmfmac/sdio.c:257`

### tohostmailboxdata (core + 0x4C)
| Bits | Name (linux; whd prefixes I_) | Meaning | Citations |
|---|---|---|---|
| 0x0001 | HMB_DATA_NAKHANDLED | Retransmit NAK'd frame | `linux/brcmfmac/sdio.c:273` `whd/src/bus_protocols/whd_sdio.h:259` |
| 0x0002 | HMB_DATA_DEVREADY | Talk to host after enable. linux comment: "does not occur with gSPI". | `linux/brcmfmac/sdio.c:274` `whd/src/bus_protocols/whd_sdio.h:260` `linux/brcmfmac/sdio.c:1148` `linux/brcmfmac/sdio.c:1149` |
| 0x0004 | HMB_DATA_FC | Per-priority flow-control update flag | `linux/brcmfmac/sdio.c:275` `whd/src/bus_protocols/whd_sdio.h:261` |
| 0x0008 | HMB_DATA_FWREADY | Firmware ready for protocol activity | `linux/brcmfmac/sdio.c:276` `whd/src/bus_protocols/whd_sdio.h:262` |
| 0x0010 | HMB_DATA_FWHALT | Firmware halted | `linux/brcmfmac/sdio.c:277` `whd/src/bus_protocols/whd_sdio.h:263` `embassy/consts.rs:90` |
| 23:16 (mask 0x00FF0000) | HMB_DATA_VERSION | linux reads this field as the device's SDPCM protocol version when DEVREADY or FWREADY is set | `linux/brcmfmac/sdio.c:282` `linux/brcmfmac/sdio.c:283` `linux/brcmfmac/sdio.c:1151` `linux/brcmfmac/sdio.c:1154` |
| 31:24 (mask 0xFF000000) | HMB_DATA_FCDATA | Per-priority flow-control bitmap; linux reads it when HMB_DATA_FC is set | `linux/brcmfmac/sdio.c:279` `linux/brcmfmac/sdio.c:280` `linux/brcmfmac/sdio.c:1175` `linux/brcmfmac/sdio.c:1177` |

- c-driver never reads the host mailbox and never examines I_HMB_HOST_INT. `c-driver/cyw43_ll.c:132` `c-driver/cyw43_ll.c:1110`
- whd looks only at FWHALT; the two fields are not found in whd. `whd/src/bus_protocols/whd_bus_sdio_protocol.c:721`
- linux expects protocol version 4 (SDPCM_PROT_VERSION) and logs "Version mismatch" otherwise; it does not fail. `linux/brcmfmac/sdio.c:290` `linux/brcmfmac/sdio.c:1155` `linux/brcmfmac/sdio.c:1156`
- linux comment: mailbox flow control (HMB_DATA_FC) has moved into the RX headers and is kept for older dongles. `linux/brcmfmac/sdio.c:1170` `linux/brcmfmac/sdio.c:1173`

Host-mailbox handling:

| Step | Action | linux | whd | embassy | Citations |
|---|---|---|---|---|---|
| 1 | When intstatus has I_HMB_HOST_INT, read tohostmailboxdata (4 bytes) | yes | yes | yes | `linux/brcmfmac/sdio.c:2656` `linux/brcmfmac/sdio.c:1121` `linux/brcmfmac/sdio.c:1122` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:711` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:714` `embassy/runner.rs:975` `embassy/runner.rs:978` |
| 2 | Write SMB_INT_ACK (0x02) to tosbmailbox (4 bytes) | whenever the read succeeded | only if the data was non-zero | only if the data was non-zero | `linux/brcmfmac/sdio.c:1125` `linux/brcmfmac/sdio.c:1127` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:715` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:717` `embassy/runner.rs:980` `embassy/runner.rs:982` |
| 3 | FWHALT (0x10) set | calls brcmf_fw_crashed | prints its log and raises error type WLC_ERR_FW | logs only | `linux/brcmfmac/sdio.c:1131` `linux/brcmfmac/sdio.c:1134` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:720` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:726` `embassy/runner.rs:987` `embassy/runner.rs:988` |
| 4 | Other bits | NAKHANDLED clears rxskip and re-raises I_HMB_FRAME_IND; DEVREADY/FWREADY latch the protocol version; FC updates the per-priority bitmap; any other bit logs "Unknown mailbox data content" | not found | not found | `linux/brcmfmac/sdio.c:1137` `linux/brcmfmac/sdio.c:1144` `linux/brcmfmac/sdio.c:1151` `linux/brcmfmac/sdio.c:1175` `linux/brcmfmac/sdio.c:1186` `linux/brcmfmac/sdio.c:1196` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:721` `embassy/runner.rs:987` |
| 5 | Clear I_HMB_HOST_INT in intstatus | already cleared when it latched intstatus | explicit write only under CYCFG_ULP_SUPPORT_ENABLED; otherwise cleared by the later write of the 0xF0 bits | writes I_HMB_HOST_INT unconditionally | `linux/brcmfmac/sdio.c:2578` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:752` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:753` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:790` `embassy/runner.rs:991` `embassy/runner.rs:994` |

- whd, CYCFG_ULP_SUPPORT_ENABLED builds only: a host-mailbox interrupt with data == 0 on chips 43012/43022 is taken as a deep-sleep (DS1/DS2) exit and triggers a firmware re-download. `whd/src/bus_protocols/whd_bus_sdio_protocol.c:728` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:731` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:734` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:742`

### Interrupt service, per driver

linux:

- brcmf_sdio_isr counts the interrupt. In interrupt context it only sets the ipend flag; otherwise it reads and clears intstatus at once (brcmf_sdio_intr_rstatus). It then schedules the DPC work. `linux/brcmfmac/sdio.c:3647` `linux/brcmfmac/sdio.c:3657` `linux/brcmfmac/sdio.c:3659` `linux/brcmfmac/sdio.c:3661` `linux/brcmfmac/sdio.c:3670`
- After the DPC, brcmf_sdio_clrintr re-enables the out-of-band IRQ line if it was disabled and nothing is pending. `linux/brcmfmac/sdio.c:2543` `linux/brcmfmac/sdio.c:2549` `linux/brcmfmac/sdio.c:2553`
- brcmf_sdio_intr_rstatus: read intstatus; AND with hostintmask; set fcstate from I_HMB_FC_STATE; if non-zero write the value back to clear and OR it into the pending set. `linux/brcmfmac/sdio.c:2566` `linux/brcmfmac/sdio.c:2568` `linux/brcmfmac/sdio.c:2573` `linux/brcmfmac/sdio.c:2574` `linux/brcmfmac/sdio.c:2578` `linux/brcmfmac/sdio.c:2580`
- On I_HMB_FC_CHANGE the DPC writes that bit to intstatus, re-reads intstatus, sets fcstate true if FC_STATE or FC_CHANGE is now set, and merges the newly read masked bits. `linux/brcmfmac/sdio.c:2639` `linux/brcmfmac/sdio.c:2643` `linux/brcmfmac/sdio.c:2647` `linux/brcmfmac/sdio.c:2650` `linux/brcmfmac/sdio.c:2652`
- The DPC logs and drops I_WR_OOSYNC, I_RD_OOSYNC and I_SBINT, and drops I_CHIPACTIVE; none trigger recovery. `linux/brcmfmac/sdio.c:2663` `linux/brcmfmac/sdio.c:2669` `linux/brcmfmac/sdio.c:2674` `linux/brcmfmac/sdio.c:2679` `linux/brcmfmac/sdio.c:2680`
- The DPC transmits data only when clkstate == CLK_AVAIL, fcstate is clear, the queue holds frames for non-flow-controlled priorities, and the credit window is open. `linux/brcmfmac/sdio.c:2718` `linux/brcmfmac/sdio.c:2720` `linux/brcmfmac/sdio.c:2721`
- Per DPC pass linux sends at most txminmax (1) frame while rx is still pending, otherwise txbound (20); rx is bounded at rxbound (50) frames. `linux/brcmfmac/sdio.c:123` `linux/brcmfmac/sdio.c:126` `linux/brcmfmac/sdio.c:129` `linux/brcmfmac/sdio.c:2722` `linux/brcmfmac/sdio.c:2723` `linux/brcmfmac/sdio.c:4471` `linux/brcmfmac/sdio.c:4473`

whd:

- whd_bus_sdio_packet_available_to_read: (1) ensure the bus is up; (2) read intstatus (4 bytes); (3) if I_HMB_HOST_INT, service the host mailbox; (4) if a Bluetooth callback is registered and I_HMB_FC_CHANGE is set, call it and treat the status as 0; (5) if any 0xF0 bit is set, write those bits back to intstatus; (6) return int_status & 0xF0. `whd/src/bus_protocols/whd_bus_sdio_protocol.c:700` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:703` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:711` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:777` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:782` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:786` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:790` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:798`
- In-band interrupt: whd registers a HAL callback and enables the HAL's card-interrupt event right after programming the block sizes. The callback accepts only WHD_HAL_SDIO_CARD_INTERRUPT (anything else is counted as an error interrupt) and notifies the whd thread. `whd/src/bus_protocols/whd_bus_sdio_protocol.c:404` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:407` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:1660` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:1665` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:1672` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:1680`
- whd enables the event again at the end of bus init and disables it at deinit. `whd/src/bus_protocols/whd_bus_sdio_protocol.c:613` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:641`
- whd's out-of-band GPIO handler checks the edge against the configured polarity and logs any other event as unexpected. `whd/src/bus_protocols/whd_bus_sdio_protocol.c:1692` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:1696` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:1698` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:1700`

embassy:

- handle_irq on SDIO: read intstatus with a 32-bit backplane read; service I_HMB_HOST_INT; if any 0xF0 bit remains call check_status (drain frames); finally write the full remaining value back to intstatus if non-zero. `embassy/runner.rs:969` `embassy/runner.rs:971` `embassy/runner.rs:975` `embassy/runner.rs:997` `embassy/runner.rs:998` `embassy/runner.rs:1008` `embassy/runner.rs:1011`

c-driver:

- SDIO poll: if no packet succeeded last time and the host-interrupt pin is not active (active level 0 on SDIO), return "no packet" without touching the bus; otherwise wake the bus and read. `c-driver/cyw43_ll.c:60` `c-driver/cyw43_ll.c:61` `c-driver/cyw43_ll.c:1098` `c-driver/cyw43_ll.c:1100` `c-driver/cyw43_ll.c:1103`
- Clearing intstatus (read; if any 0xF0 bit is set write those bits back) is compiled only when CYW43_CLEAR_SDIO_INT is set; it defaults to 0. `c-driver/cyw43_ll.c:1105` `c-driver/cyw43_ll.c:1109` `c-driver/cyw43_ll.c:1110` `c-driver/cyw43_ll.c:1113` `c-driver/cyw43_config.h:27` `c-driver/cyw43_config.h:28`
- With Bluetooth enabled, cyw43_ll_bt_has_work reads intstatus and, if I_HMB_FC_CHANGE (bit 5) is set, writes that bit back and reports Bluetooth work. whd also uses I_HMB_FC_CHANGE as the Bluetooth shared-bus interrupt; linux treats bit 5 only as a WLAN flow-control change. `c-driver/cyw43_ll.c:2542` `c-driver/cyw43_ll.c:2544` `c-driver/cyw43_ll.c:2546` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:777` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:781` `linux/brcmfmac/sdio.c:2643`

## Clock requests

- The drivers request ALP with ALP_AVAIL_REQ (0x08) and read ALP_AVAIL (0x40) as its status. They request HT with HT_AVAIL_REQ (0x10) and read HT_AVAIL (0x80) as its status. `linux/brcmfmac/sdio.c:183` `linux/brcmfmac/sdio.c:185` `linux/brcmfmac/sdio.c:189` `linux/brcmfmac/sdio.c:191` `whd/src/bus_protocols/whd_sdio.h:213` `whd/src/bus_protocols/whd_sdio.h:214` `whd/src/bus_protocols/whd_sdio.h:216` `whd/src/bus_protocols/whd_sdio.h:217`
- embassy's comment expands ALP as "Active Low Power"; whd's expands HT as "High Throughput". The linux and whd bit comments tie ALP to the crystal and HT to the PLL. `embassy/runner.rs:476` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:1256` `linux/brcmfmac/sdio.c:182` `linux/brcmfmac/sdio.c:184`
- The drivers drop all requests by writing 0 to CHIP_CLOCK_CSR. `linux/brcmfmac/sdio.c:880` `linux/brcmfmac/sdio.c:892` `embassy/runner.rs:516`

linux clock state machine:

- States: CLK_NONE = 0, CLK_SDONLY = 1, CLK_PENDING = 2, CLK_AVAIL = 3. `linux/brcmfmac/sdio.c:529` `linux/brcmfmac/sdio.c:530` `linux/brcmfmac/sdio.c:531` `linux/brcmfmac/sdio.c:532` `linux/brcmfmac/sdio.c:533`
- brcmf_sdio_htclk(on) with save/restore enabled only records CLK_AVAIL and touches no register. `linux/brcmfmac/sdio.c:795` `linux/brcmfmac/sdio.c:796` `linux/brcmfmac/sdio.c:797`
- brcmf_sdio_htclk(on) otherwise: write CHIPCLKCSR = HT_AVAIL_REQ (ALP_AVAIL_REQ when alp_only); read it back. `linux/brcmfmac/sdio.c:801` `linux/brcmfmac/sdio.c:803` `linux/brcmfmac/sdio.c:805` `linux/brcmfmac/sdio.c:813`
- If the clock is not yet available and the caller allows pending: set DEVICE_CTL bit CA_INT_ONLY (0x04), set CLK_PENDING, return. `linux/brcmfmac/sdio.c:820` `linux/brcmfmac/sdio.c:823` `linux/brcmfmac/sdio.c:830` `linux/brcmfmac/sdio.c:831` `linux/brcmfmac/sdio.c:834`
- If pending is not allowed: poll CHIPCLKCSR with 5-10 ms sleeps for up to PMU_MAX_TRANSITION_DLY / 1000 = 1000 ms. On timeout log "HT Avail timeout" and return -EBADE; on success set CLK_AVAIL. `linux/brcmfmac/sdio.c:846` `linux/brcmfmac/sdio.c:849` `linux/brcmfmac/sdio.c:856` `linux/brcmfmac/sdio.c:862` `linux/brcmfmac/sdio.c:863` `linux/brcmfmac/sdio.c:869`
- When leaving CLK_PENDING linux clears DEVICE_CTL bit CA_INT_ONLY. `linux/brcmfmac/sdio.c:837` `linux/brcmfmac/sdio.c:841`
- brcmf_sdio_htclk(off): clear CA_INT_ONLY if pending, set CLK_SDONLY, write CHIPCLKCSR = 0. `linux/brcmfmac/sdio.c:879` `linux/brcmfmac/sdio.c:882` `linux/brcmfmac/sdio.c:886` `linux/brcmfmac/sdio.c:891` `linux/brcmfmac/sdio.c:892` `linux/brcmfmac/sdio.c:893`
- DPC while CLK_PENDING (non-SR): read CHIPCLKCSR; if both availability bits are set, clear CA_INT_ONLY and move to CLK_AVAIL. `linux/brcmfmac/sdio.c:2600` `linux/brcmfmac/sdio.c:2601` `linux/brcmfmac/sdio.c:2611` `linux/brcmfmac/sdio.c:2617` `linux/brcmfmac/sdio.c:2620` `linux/brcmfmac/sdio.c:2623`
- On bus stop and on firmware start linux ORs FORCE_HT (HT_AVAIL_REQ on the 43012) into CHIPCLKCSR, "to assure F2 interrupt propagates". `linux/brcmfmac/sdio.c:2500` `linux/brcmfmac/sdio.c:2504` `linux/brcmfmac/sdio.c:2507` `linux/brcmfmac/sdio.c:4253` `linux/brcmfmac/sdio.c:4258`

Wake by clock request, without save/restore:

| Driver | Wake | Sleep | Notes | Citations |
|---|---|---|---|---|
| whd | Write CHIP_CLOCK_CSR = HT_AVAIL_REQ (0x10); poll for HT_AVAIL (0x80) every 1 ms, up to 1000 attempts | Write CHIP_CLOCK_CSR = 0 | Skips the request when the bus is already marked up | `whd/src/whd_chip.c:55` `whd/src/whd_chip.c:56` `whd/src/whd_chip.c:1083` `whd/src/whd_chip.c:1086` `whd/src/whd_chip.c:1093` `whd/src/whd_chip.c:877` `whd/src/whd_chip.c:880` `whd/src/whd_chip.c:1029` |
| c-driver | Same as whd | Same as whd | This branch is compiled out: USE_KSO is hard-defined to 1. Skips when bus_is_up. | `c-driver/cyw43_ll.c:39` `c-driver/cyw43_ll.c:1440` `c-driver/cyw43_ll.c:1442` `c-driver/cyw43_ll.c:1447` `c-driver/cyw43_ll.c:1451` `c-driver/cyw43_ll.c:1475` |
| embassy | wake_bus before every F2 write and before the first F2 read of each frame: write CHIP_CLOCK_CSR = HT_AVAIL_REQ (0x10), poll every 1 ms for bit 0x80 (written as HT_AVAIL_REQ << 3) with a 5 ms timeout | No sleep implemented | On SPI wake_bus does nothing | `embassy/runner.rs:771` `embassy/runner.rs:774` `embassy/runner.rs:779` `embassy/runner.rs:782` `embassy/runner.rs:798` `embassy/runner.rs:808` `embassy/runner.rs:1058` `embassy/runner.rs:1119` `embassy/util.rs:69` `embassy/util.rs:70` |

- embassy's 43439 init ends by writing CHIP_CLOCK_CSR = 0x10 (HT_AVAIL_REQ) and waiting up to 500 ms for 0x80. The whd-style WAKEUP_CTRL / CARDCAP / FORCE_HT / KSO block is present only as commented-out code ("These aren't needed if we don't want to sleep the bus"). `embassy/runner.rs:387` `embassy/runner.rs:388` `embassy/runner.rs:392` `embassy/runner.rs:401` `embassy/runner.rs:409` `embassy/runner.rs:411` `embassy/runner.rs:416` `embassy/runner.rs:417`
- At the same point, with SR enabled, whd and c-driver write FORCE_HT (0x02), not HT_AVAIL_REQ, for the 43439. `whd/src/whd_chip.c:1253` `c-driver/cyw43_ll.c:1870`

## Sleep/keep-awake control

### Deciding whether save/restore (SR) is in use

- For the 43430/43439, whd and linux read chipcommon sr_control1 (0x18000000 + 0x508); non-zero is taken to mean the firmware initialised the SR engine. `whd/src/whd_chip.c:1133` `whd/src/whd_chip.c:1136` `whd/src/whd_chip.c:1141` `whd/src/whd_chip.c:1143` `whd/src/bus_protocols/whd_chip_reg.h:97` `linux/brcmfmac/chip.c:1457` `linux/brcmfmac/chip.c:1459` `linux/brcmfmac/chip.c:1461` `linux/include/chipcommon.h:180`
- linux additionally requires PMU revision >= 17. `linux/brcmfmac/chip.c:1433` `linux/brcmfmac/chip.c:1434`
- c-driver reads CHIPCOMMON_SR_CONTROL1 only in NDEBUG builds and ignores the value; it uses KSO unconditionally (USE_KSO = 1). `c-driver/cyw43_ll.c:1908` `c-driver/cyw43_ll.c:39`
- Not found in embassy. `embassy/runner.rs:374-425`

linux brcmf_chip_sr_capable for other chips:

| Chips | Test | Citations |
|---|---|---|
| any | false if PMU revision < 17 | `linux/brcmfmac/chip.c:1433` `linux/brcmfmac/chip.c:1434` `linux/brcmfmac/chip.c:1435` |
| 4354, 4356, 4345, 43454 | PMU chipcontrol register 3, bit 2 | `linux/brcmfmac/chip.c:1440` `linux/brcmfmac/chip.c:1444` `linux/brcmfmac/chip.c:1446` `linux/brcmfmac/chip.c:1448` |
| 43241, 4335, 4339 | PMU chipcontrol 3 non-zero | `linux/brcmfmac/chip.c:1449` `linux/brcmfmac/chip.c:1452` `linux/brcmfmac/chip.c:1456` |
| 43430, 43439 | chipcommon sr_control1 non-zero | `linux/brcmfmac/chip.c:1457` `linux/brcmfmac/chip.c:1461` |
| 4355, 4373 | sr_control0 & CC_SR_CTL0_ENABLE_MASK | `linux/brcmfmac/chip.c:1462` `linux/brcmfmac/chip.c:1463` `linux/brcmfmac/chip.c:1467` |
| 4359, 43751, 43752, 43012 | PMU retention_ctl has neither MACPHY_DISABLE nor LOGIC_DISABLE | `linux/brcmfmac/chip.c:1468` `linux/brcmfmac/chip.c:1472` `linux/brcmfmac/chip.c:1475` |
| default | pmucapabilities_ext has SR_SUPPORTED, and retention_ctl as above | `linux/brcmfmac/chip.c:1476` `linux/brcmfmac/chip.c:1479` `linux/brcmfmac/chip.c:1484` |

### SR enable sequence
| Step | Action | whd | c-driver | linux | embassy | Citations |
|---|---|---|---|---|---|---|
| 1 | Read WAKEUP_CTRL (0x1001E), OR in WakeTillHTAvail (0x02), write back | yes; WakeTillAlpAvail (0x01) for 43012/4373/55560/55500/55530/43022 | yes | yes; WakeTillAlpAvail for the 43012 | commented out for the 43439; ALP variant for 4373/43455 only | `linux/brcmfmac/sdio.c:3449` `linux/brcmfmac/sdio.c:3453` `linux/brcmfmac/sdio.c:3464` `linux/brcmfmac/sdio.c:3470` `whd/src/whd_chip.c:1209` `whd/src/whd_chip.c:1222` `whd/src/whd_chip.c:1233` `whd/src/whd_chip.c:1236` `c-driver/cyw43_ll.c:1866` `c-driver/cyw43_ll.c:1868` `embassy/runner.rs:428` |
| 2 | Write BRCM_CARDCAP (F0 0xF0) | CMD_NODEC (0x08) | CMD_NODEC (0x08) | CMD14_SUPPORT + CMD14_EXT (0x06); CMD_NODEC only for 43751/43752/43012. The 43439 gets 0x06. | not for the 43439 | `whd/src/whd_chip.c:1240` `whd/src/whd_chip.c:1244` `whd/src/whd_chip.c:1245` `c-driver/cyw43_ll.c:1869` `linux/brcmfmac/sdio.c:3460` `linux/brcmfmac/sdio.c:3431` |
| 3 | Write CHIP_CLOCK_CSR = FORCE_HT (0x02); HT_AVAIL_REQ (0x10) for the ULP / 4373-family chips | yes | yes | yes | writes HT_AVAIL_REQ for the 43439 instead (see "Clock requests") | `linux/brcmfmac/sdio.c:3451` `linux/brcmfmac/sdio.c:3454` `linux/brcmfmac/sdio.c:3485` `linux/brcmfmac/sdio.c:3486` `whd/src/whd_chip.c:1246` `whd/src/whd_chip.c:1248` `whd/src/whd_chip.c:1253` `whd/src/whd_chip.c:1254` `c-driver/cyw43_ll.c:1870` |
| 4 | Read SLEEP_CSR (0x1001F); if KSO (bit 0) is clear, OR it in and write back; mark SR enabled | yes | yes | KSO was already set at probe (brcmf_sdio_kso_init); sr_init only sets the sr_enabled flag | on the 43439 writes SLEEP_CSR = KSO twice at the start of chip init and asserts the bit reads back set | `whd/src/whd_chip.c:1257` `whd/src/whd_chip.c:1265` `whd/src/whd_chip.c:1270` `whd/src/whd_chip.c:1278` `whd/src/whd_chip.c:1291` `c-driver/cyw43_ll.c:1871` `c-driver/cyw43_ll.c:1874` `linux/brcmfmac/sdio.c:3492` `linux/brcmfmac/sdio.c:3493` `linux/brcmfmac/sdio.c:4040` `embassy/runner.rs:377` |

- whd comment on CMD_NODEC: it makes sdiod_aos wake the host on any command-line activity even though the module will not decode or answer the command. `whd/src/whd_chip.c:1241` `whd/src/whd_chip.c:1242`
- linux logs "SR enabled"; from then on brcmf_sdio_htclk no longer writes CHIPCLKCSR and bus sleep/wake is done only with KSO. `linux/brcmfmac/sdio.c:3493` `linux/brcmfmac/sdio.c:3494` `linux/brcmfmac/sdio.c:795` `linux/brcmfmac/sdio.c:975` `linux/brcmfmac/sdio.c:976`
- embassy's SR set-up for the 4373 and 43455 (init_cyw4373): WAKEUP_CTRL OR WL_WAKE_TILL_ALP_AVAIL (0x01); BRCM_CARDCAP = CMD_NODEC (0x08); read SLEEP_CSR and set KSO if clear. The 43439 takes init_cyw43439 instead. `embassy/runner.rs:427` `embassy/runner.rs:433` `embassy/runner.rs:441` `embassy/runner.rs:446` `embassy/runner.rs:451` `embassy/runner.rs:694` `embassy/runner.rs:697`
- For 43012/4373/55560/55500/55530/43022, whd writes CHIP_CLOCK_CSR = HT_AVAIL_REQ at this point. Whenever its SR test passes it then calls the bus sleep hook and writes PULL_UP = 0xF. embassy's init_cyw4373 does none of these. `whd/src/whd_chip.c:1246` `whd/src/whd_chip.c:1249` `whd/src/whd_chip.c:1286` `whd/src/whd_chip.c:1289`

### KSO write procedure
| Step | Action | Per-driver detail | Citations |
|---|---|---|---|
| 1 | Write the wanted KSO value to SLEEP_CSR (0x1001F). Errors are ignored: the first write "goes to AOS wake up core if device is asleep" and may fail. | linux, whd, c-driver | `linux/brcmfmac/sdio.c:714` `linux/brcmfmac/sdio.c:716` `whd/src/whd_chip.c:1324` `whd/src/whd_chip.c:1329` `c-driver/cyw43_ll.c:1395` `c-driver/cyw43_ll.c:1396` |
| 2 | Write the value a second time at once. whd's comment says the SR module wakes up only after the KSO bit has been written twice in sequence, and that both of those writes may fail. | whd: twice for 43430/43439/43340/43342 whether setting or clearing; for every other chip once when clearing (then returns), twice when setting. c-driver: twice. embassy: writes SLEEP_CSR = KSO twice at the start of 43439 init. linux: one write, then a 2-3 ms sleep before polling when turning on. | `whd/src/whd_chip.c:1326` `whd/src/whd_chip.c:1328` `whd/src/whd_chip.c:1332` `whd/src/whd_chip.c:1354` `whd/src/whd_chip.c:1361` `whd/src/whd_chip.c:1367` `c-driver/cyw43_ll.c:1397` `embassy/runner.rs:377` `embassy/runner.rs:381` `linux/brcmfmac/sdio.c:734` |
| 3 | Read SLEEP_CSR back until it matches. Turning on: both bit 0 (KSO) and bit 1 (DEVON) set (mask 0x03, compare 0x03). Turning off: only bit 0 clear, because DEVON "may not get cleared right away". | linux, whd, c-driver. whd and c-driver also reject a read-back of 0xFF; linux has no 0xFF check and relies on the access error code. | `linux/brcmfmac/sdio.c:726` `linux/brcmfmac/sdio.c:729` `linux/brcmfmac/sdio.c:733` `linux/brcmfmac/sdio.c:738` `linux/brcmfmac/sdio.c:750` `linux/brcmfmac/sdio.c:752` `linux/brcmfmac/sdio.c:753` `whd/src/whd_chip.c:1337` `whd/src/whd_chip.c:1342` `whd/src/whd_chip.c:1349` `whd/src/whd_chip.c:1393` `whd/src/whd_chip.c:1395` `c-driver/cyw43_ll.c:1400` `c-driver/cyw43_ll.c:1405` `c-driver/cyw43_ll.c:1410` `c-driver/cyw43_ll.c:1419` `c-driver/cyw43_ll.c:1420` |
| 4 | On mismatch: delay, write the value again, re-read. Reason given: the sleep write "is synced to PMU 32khz clk, just one write attempt may fail". | linux, whd, c-driver | `linux/brcmfmac/sdio.c:745` `linux/brcmfmac/sdio.c:748` `linux/brcmfmac/sdio.c:761` `linux/brcmfmac/sdio.c:762` `whd/src/whd_chip.c:1388` `whd/src/whd_chip.c:1390` `whd/src/whd_chip.c:1400` `whd/src/whd_chip.c:1402` `c-driver/cyw43_ll.c:1414` `c-driver/cyw43_ll.c:1416` `c-driver/cyw43_ll.c:1424` `c-driver/cyw43_ll.c:1426` |

Retry budget:

| Driver | Attempts | Interval | Notes | Citations |
|---|---|---|---|---|
| whd | 64 (MAX_KSO_ATTEMPTS) | 1 ms (KSO_WAIT_MS) | | `whd/src/whd_chip.c:57` `whd/src/whd_chip.c:59` `whd/src/whd_chip.c:1307` `whd/src/whd_chip.c:1386` `whd/src/whd_chip.c:1404` |
| c-driver | 64 | 1 ms | | `c-driver/cyw43_ll.c:1413` `c-driver/cyw43_ll.c:1424` |
| linux | MAX_KSO_ATTEMPTS = PMU_MAX_TRANSITION_DLY / KSO_WAIT_US = 1,000,000 / 50 = 20,000; the do/while (try_cnt++ < MAX) lets the body run 20,001 times | 50 us | Bails out early on the 7th consecutive failed read: a read fails while the error counter already exceeds BRCMF_SDIO_MAX_ACCESS_ERRORS (5). Any successful read resets the counter. | `linux/brcmfmac/sdio.c:312` `linux/brcmfmac/sdio.c:326` `linux/brcmfmac/sdio.c:327` `linux/brcmfmac/sdio.c:328` `linux/brcmfmac/sdio.c:754` `linux/brcmfmac/sdio.c:756` `linux/brcmfmac/sdio.c:757` `linux/brcmfmac/sdio.c:758` `linux/brcmfmac/sdio.c:765` |

- For chips other than 43430/43439/43340/43342, whd does not poll when clearing KSO ("the chip could go down immediately after KSO bit is cleared"); it returns after the write. linux does the same for the 43012 only. `whd/src/whd_chip.c:1352` `whd/src/whd_chip.c:1357` `whd/src/whd_chip.c:1361` `whd/src/whd_chip.c:1363` `linux/brcmfmac/sdio.c:718` `linux/brcmfmac/sdio.c:721` `linux/brcmfmac/sdio.c:724`
- linux brackets KSO changes with sdio_retune_crc_disable / sdio_retune_hold_now ("Cannot re-tune if device is asleep; defer till we're awake"). `linux/brcmfmac/sdio.c:708` `linux/brcmfmac/sdio.c:710` `linux/brcmfmac/sdio.c:712` `linux/brcmfmac/sdio.c:774` `linux/brcmfmac/sdio.c:777`
- whd's CMD52 routine special-cases address SDIO_SLEEP_CSR: it returns the error without its usual error trace (its comment says the device perhaps gives no response to this cmd). `whd/src/bus_protocols/whd_bus_sdio_protocol.c:1053` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:1054` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:1056`

### Bus sleep policy

- With SR enabled, whd, c-driver and linux treat "bus up" as KSO set and "bus asleep" as KSO cleared: they set KSO (and wait for DEVON) before any F1/F2 access and may clear it when idle. `whd/src/whd_chip.c:882` `whd/src/whd_chip.c:888` `whd/src/whd_chip.c:1106` `whd/src/whd_chip.c:1110` `c-driver/cyw43_ll.c:1433` `c-driver/cyw43_ll.c:1436` `c-driver/cyw43_ll.c:1463` `c-driver/cyw43_ll.c:1480` `linux/brcmfmac/sdio.c:975` `linux/brcmfmac/sdio.c:982` `linux/brcmfmac/sdio.c:992` `linux/brcmfmac/sdio.c:994`
- embassy never clears KSO; it implements no bus sleep. `embassy/runner.rs:387`

| Driver | Going to sleep | Citations |
|---|---|---|
| linux, SR | Read CHIPCLKCSR; if none of the five request/force bits (0x1F) is set, write ALP_AVAIL_REQ first ("no clock, set ALP"); then clear KSO | `linux/brcmfmac/sdio.c:981` `linux/brcmfmac/sdio.c:983` `linux/brcmfmac/sdio.c:986` `linux/brcmfmac/sdio.c:988` `linux/brcmfmac/sdio.c:990` `linux/brcmfmac/sdio.c:992` |
| linux, non-SR | brcmf_sdio_bus_sleep calls clkctl(CLK_NONE); with SR the KSO clear is the whole of it | `linux/brcmfmac/sdio.c:1005` `linux/brcmfmac/sdio.c:1006` `linux/brcmfmac/sdio.c:1007` |
| whd | Clears KSO without touching CHIP_CLOCK_CSR. Does not clear KSO while a Bluetooth shared-bus interrupt callback is registered. | `whd/src/whd_chip.c:884` `whd/src/whd_chip.c:886` `whd/src/whd_chip.c:888` |
| c-driver | Clears KSO without touching CHIP_CLOCK_CSR | `c-driver/cyw43_ll.c:1436` |

- linux on wake calls clkctl(CLK_AVAIL) and restarts the watchdog timer, then records bus->sleeping. `linux/brcmfmac/sdio.c:1008` `linux/brcmfmac/sdio.c:1009` `linux/brcmfmac/sdio.c:1010` `linux/brcmfmac/sdio.c:1012`
- linux idle policy: a watchdog fires every 10 ms (BRCMF_WD_POLL). When no DPC is pending or running, clkstate is CLK_AVAIL and idletime > 0, it counts ticks and puts the bus to sleep once idlecount exceeds idletime (BRCMF_IDLE_INTERVAL = 1). `linux/brcmfmac/sdio.h:143` `linux/brcmfmac/sdio.h:144` `linux/brcmfmac/sdio.c:324` `linux/brcmfmac/sdio.c:3732` `linux/brcmfmac/sdio.c:3735` `linux/brcmfmac/sdio.c:3738` `linux/brcmfmac/sdio.c:3747` `linux/brcmfmac/sdio.c:4535`
- whd's SDIO bus-specific wakeup and sleep hooks are empty (return success); all SDIO sleep control is the common KSO / CHIP_CLOCK_CSR code. `whd/src/bus_protocols/whd_bus_sdio_protocol.c:1351` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:1353` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:1356` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:1358`
- whd marks the bus for "delayed release" after each successful F2 send and each completed frame read; the event wait then uses that timeout before allowing the bus to sleep. `whd/src/bus_protocols/whd_bus_sdio_protocol.c:304` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:306` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:912` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:256` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:263` `whd/src/bus_protocols/whd_bus_common.c:162`
- c-driver calls cyw43_ll_bus_sleep(false) (set KSO, wait for DEVON) before every send and before every SDIO poll read. `c-driver/cyw43_ll.c:775` `c-driver/cyw43_ll.c:1103`

## Glomming

- Glomming ("superframes") packs several SDPCM frames into one SDIO transfer. linux: SDPCM channel 3 (SDPCM_GLOM_CHANNEL) carries coalesced packets; channel-flag bit 0x80 (SDPCM_GLOMDESC, bit 7 of software-header byte 1) marks a glom descriptor. `linux/brcmfmac/sdio.c:421` `linux/brcmfmac/sdio.c:1342` `linux/brcmfmac/sdio.c:1344`
- No receive-side glom support is found in whd, embassy or c-driver. `whd/src/bus_protocols/whd_bus_sdio_protocol.c:808` `embassy/runner.rs:1164` `c-driver/cyw43_ll.c:1141`
- whd, c-driver and embassy turn glomming off at start-up by setting the named variable (iovar) "bus:txglom" = 0. whd comment: the 4319 has glomming off by default, the 43362 has it on; whd tolerates WHD_WLAN_UNSUPPORTED. `whd/src/whd_management.c:461` `whd/src/whd_management.c:465` `whd/src/whd_management.c:473` `whd/src/include/whd_wlioctl.h:1088` `c-driver/cyw43_ll.c:1918` `c-driver/cyw43_ll.c:2037` `embassy/control.rs:268` `embassy/control.rs:292`
- linux comment: the variable names are from the device's point of view. "bus:txglom" governs device-to-host transfers (what the host receives); "bus:rxglom" governs host-to-device glomming. `linux/brcmfmac/sdio.c:3553` `linux/brcmfmac/sdio.c:3556`
- linux preinit: core rev < 12 sets "bus:txglom" = 0; otherwise it sets "bus:txglomalign" = max(sd_sgentry_align, ALIGNMENT), ALIGNMENT being 4 (8 with 64-bit DMA addresses). `linux/brcmfmac/sdio.c:546` `linux/brcmfmac/sdio.c:549` `linux/brcmfmac/sdio.c:3557` `linux/brcmfmac/sdio.c:3560` `linux/brcmfmac/sdio.c:3564` `linux/brcmfmac/sdio.c:3567`
- Then, if the host controller supports scatter-gather, linux sets "bus:rxglom" = 1. If that succeeds host tx glom is on and the tx header grows by 8 bytes; failure is allowed. `linux/brcmfmac/sdio.c:3574` `linux/brcmfmac/sdio.c:3575` `linux/brcmfmac/sdio.c:3578` `linux/brcmfmac/sdio.c:3581` `linux/brcmfmac/sdio.c:3585`

linux receive glom:

| Step | linux action | Citations |
|---|---|---|
| 1 | A frame on channel 3 with the descriptor flag is the glom descriptor: after its 12-byte header it is a list of little-endian 2-byte sub-frame lengths. A channel-3 frame without the flag is an error ("glom superframe w/o descriptor"). | `linux/brcmfmac/sdio.c:2019` `linux/brcmfmac/sdio.c:2021` `linux/brcmfmac/sdio.c:2027` `linux/brcmfmac/sdio.c:2031` `linux/brcmfmac/sdio.c:1538` `linux/brcmfmac/sdio.c:1546` |
| 2 | Validate the descriptor: its length must be non-zero and even; every sub-length must be >= 12 and the first >= 24 (it also carries the superframe header); sub-lengths that are not multiples of the scatter-gather alignment are warned about. | `linux/brcmfmac/sdio.c:1538` `linux/brcmfmac/sdio.c:1539` `linux/brcmfmac/sdio.c:1549` `linux/brcmfmac/sdio.c:1550` `linux/brcmfmac/sdio.c:1556` `linux/brcmfmac/sdio.c:1557` |
| 3 | Allocate one buffer per sub-frame; enlarge the last so the total is a multiple of the F2 block size; read the whole superframe with a single F2 transfer. | `linux/brcmfmac/sdio.c:1560` `linux/brcmfmac/sdio.c:1563` `linux/brcmfmac/sdio.c:1567` `linux/brcmfmac/sdio.c:1571` `linux/brcmfmac/sdio.c:1620` `linux/brcmfmac/sdio.c:1626` |
| 4 | The superframe's own header must have length (rounded up to the block size) equal to the bytes read, channel 3, and no descriptor flag. Its next-length field seeds the following read. Its data offset is skipped to reach the first sub-frame. | `linux/brcmfmac/sdio.c:1399` `linux/brcmfmac/sdio.c:1400` `linux/brcmfmac/sdio.c:1413` `linux/brcmfmac/sdio.c:1428` `linux/brcmfmac/sdio.c:1650` `linux/brcmfmac/sdio.c:1653` `linux/brcmfmac/sdio.c:1656` |
| 5 | Each sub-frame has its own SDPCM header. Its length must not exceed its descriptor length; its channel must be data (2) or event (1). It is trimmed to its length, its data offset stripped, and delivered. Sequence numbers advance by one per sub-frame. | `linux/brcmfmac/sdio.c:1404` `linux/brcmfmac/sdio.c:1433` `linux/brcmfmac/sdio.c:1434` `linux/brcmfmac/sdio.c:1660` `linux/brcmfmac/sdio.c:1666` `linux/brcmfmac/sdio.c:1669` `linux/brcmfmac/sdio.c:1692` `linux/brcmfmac/sdio.c:1700` `linux/brcmfmac/sdio.c:1716` `linux/brcmfmac/sdio.c:1719` |
| Failure | If the single read fails or any header check fails: abort + read-frame-terminate without NAK, count rxglomfail, free the whole chain. | `linux/brcmfmac/sdio.c:1630` `linux/brcmfmac/sdio.c:1636` `linux/brcmfmac/sdio.c:1638` `linux/brcmfmac/sdio.c:1677` `linux/brcmfmac/sdio.c:1680` `linux/brcmfmac/sdio.c:1682` |

linux transmit glom. When host tx glom is on, an 8-byte "hardware extension header" (SDPCM_HWEXT_LEN = 8) sits between the 4-byte hardware tag and the 8-byte software header. linux comment: "Tx glom mode only, N/A for Rx or normal Tx". `linux/brcmfmac/sdio.c:1314` `linux/brcmfmac/sdio.c:1315` `linux/brcmfmac/sdio.c:1331`

| Offset in extension header | Size | Field | Citations |
|---|---|---|---|
| 0 | 2 | Packet length excluding the hardware tag | `linux/brcmfmac/sdio.c:1316` `linux/brcmfmac/sdio.c:1497` `linux/brcmfmac/sdio.c:1498` |
| 2 | 1 | Reserved | `linux/brcmfmac/sdio.c:1317` |
| 3 | 1 | Frame flags; bit 0 = last frame | `linux/brcmfmac/sdio.c:1318` `linux/brcmfmac/sdio.c:1498` `linux/brcmfmac/sdio.c:1499` |
| 4 | 2 | Reserved | `linux/brcmfmac/sdio.c:1319` |
| 6 | 2 | Tail padding length | `linux/brcmfmac/sdio.c:1320` `linux/brcmfmac/sdio.c:1500` `linux/brcmfmac/sdio.c:1501` |

- The extension header is not found in whd, embassy or c-driver. `whd/src/bus_protocols/whd_bus_sdio_protocol.c:293` `embassy/runner.rs:897` `c-driver/cyw43_ll.c:836`
- linux overwrites the hardware tag of the first packet with the total length of the chain including padding. It pads each packet to the scatter-gather alignment and the last one so the chain is a multiple of the F2 block size. `linux/brcmfmac/sdio.c:2137` `linux/brcmfmac/sdio.c:2140` `linux/brcmfmac/sdio.c:2145` `linux/brcmfmac/sdio.c:2248` `linux/brcmfmac/sdio.c:2252`
- linux chain size: min(open credit window tx_max - tx_seq, txglomsz, frames queued). txglomsz defaults to 32 (BRCMF_DEFAULT_TXGLOM_SIZE, module parameter "txglomsz"). `linux/brcmfmac/sdio.c:2349` `linux/brcmfmac/sdio.c:2351` `linux/brcmfmac/sdio.c:2354` `linux/brcmfmac/common.c:34` `linux/brcmfmac/common.c:36` `linux/brcmfmac/common.c:37`
- linux sizes the receive scatter-gather table for at least 32 frames (BRCMF_DEFAULT_RXGLOM_SIZE). `linux/brcmfmac/bcmsdh.c:52` `linux/brcmfmac/bcmsdh.c:776` `linux/brcmfmac/bcmsdh.c:777`
- linux counters: rxglomfail (failed deglom attempts), rxglomframes (superframes), rxglompkts (packets from superframes). `linux/brcmfmac/sdio.c:420` `linux/brcmfmac/sdio.c:421` `linux/brcmfmac/sdio.c:422`

## Frame read, abort and retry

### Frame read

- The drivers expect every F2 frame to start with a 4-byte hardware tag: bytes 0-1 = frame length (little-endian), bytes 2-3 = bitwise inverse of the length. The drivers take all-zero as "no frame"; otherwise length XOR checksum must be 0xFFFF. `linux/brcmfmac/sdio.c:1311` `linux/brcmfmac/sdio.c:1313` `linux/brcmfmac/sdio.c:1382` `linux/brcmfmac/sdio.c:1385` `linux/brcmfmac/sdio.c:1389` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:832` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:835` `c-driver/cyw43_ll.c:1120` `c-driver/cyw43_ll.c:1126` `embassy/runner.rs:1066` `embassy/runner.rs:1068`
- whd's stated read contract: the interrupt is only a hint; the host may read the 4-byte tag at any time; if a frame is available the tag is non-zero (>= 4) and the rest is read with one or more further CMD53 reads; if none, the tag reads as zero. `whd/src/bus_protocols/whd_bus_sdio_protocol.c:801` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:803` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:806`

| Aspect | whd | c-driver | embassy | linux | Citations |
|---|---|---|---|---|---|
| First read | 4 bytes (INITIAL_READ = 4) | 4 bytes | 4 bytes | 64 bytes (BRCMF_FIRSTREAD = 1 << 6), which holds the whole SDPCM header and often the whole frame | `whd/src/bus_protocols/whd_bus_sdio_protocol.c:79` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:823` `c-driver/cyw43_ll.c:1118` `c-driver/cyw43_ll.c:1119` `embassy/consts.rs:38` `embassy/runner.rs:1058` `linux/brcmfmac/sdio.c:136` |
| Second read | Exactly length - 4 bytes; block mode (64-byte blocks, count rounded up) when >= 64 and the WLAN is up (non-MTB-HAL builds) | Remaining size padded: <= 8 rounds up to 8, <= 16 rounds up to 16, otherwise up to a multiple of 64 | Passes exactly length - 4 bytes to the sdio crate's cmd53_read with BLOCK_SIZE = 64; the crate reads the largest multiple of 64 in block mode and the remainder in byte mode, with no padding | Remaining len - 64 bytes. When that is larger than one F2 block it is padded up to the block size, but only if the pad is within "roundup" and the total stays below MAX_RX_DATASZ; when it is one block or less it is rounded up to head_align | `whd/src/bus_protocols/whd_bus_sdio_protocol.c:855` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:857` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:900` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:999` `c-driver/cyw43_ll.c:1130` `c-driver/cyw43_ll.c:1133` `c-driver/cyw43_ll.c:1136` `c-driver/cyw43_ll.c:1138` `embassy/runner.rs:1117` `embassy/runner.rs:1119` `embassy/sdio.rs:27` `embassy/consts.rs:112` `sdio-crate/src/sdio.rs:678` `sdio-crate/src/sdio.rs:682` `sdio-crate/src/sdio.rs:694` `linux/brcmfmac/sdio.c:1930` `linux/brcmfmac/sdio.c:1935` `linux/brcmfmac/sdio.c:1848` `linux/brcmfmac/sdio.c:1850` `linux/brcmfmac/sdio.c:1853` |
| F2 address | 0, CMD53 incrementing | 0, incrementing | 0 | Sets the window to the chipcommon base, then uses (base & 0x7FFF) + 0x8000; this is 0x8000 when the base has zero low 15 bits, as 0x18000000 does. Reads with sdio_readsb (fixed address), writes with sdio_memcpy_toio. Sizes rounded up to a multiple of 4. | `whd/src/bus_protocols/whd_bus_sdio_protocol.c:1084` `c-driver/cyw43_sdio.c:51` `embassy/sdio.rs:238` `linux/brcmfmac/bcmsdh.c:546` `linux/brcmfmac/bcmsdh.c:551` `linux/brcmfmac/bcmsdh.c:556` `linux/brcmfmac/bcmsdh.c:558` `linux/brcmfmac/bcmsdh.c:292` `linux/brcmfmac/bcmsdh.c:301` `linux/brcmfmac/bcmsdh.c:323` `linux/brcmfmac/bcmsdh.c:326` |
| Bad tag checksum | Returns WHD_HWTAG_MISMATCH (the same return as for an all-zero tag), no abort | Logs "hdr mismatch", returns no-packet, no abort | Traces "hwtag mismatch" (also for an all-zero tag) and stops draining; no abort | Terminate only; no abort, no NAK | `whd/src/bus_protocols/whd_bus_sdio_protocol.c:832` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:835` `c-driver/cyw43_ll.c:1126` `c-driver/cyw43_ll.c:1128` `embassy/runner.rs:1068` `embassy/runner.rs:1069` `embassy/runner.rs:1070` `linux/brcmfmac/sdio.c:1392` |

- whd: a frame of length exactly 12 (an SDPCM header with no payload, a credit update) while the WLAN is up is completed with one 8-byte read into a stack buffer and only updates credits; no packet buffer is allocated. `whd/src/bus_protocols/whd_bus_sdio_protocol.c:838` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:841` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:850` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:851`
- whd with no receive buffer available: read 8 more bytes to complete the 12-byte SDPCM header, abort the read, update credits from the header, return WHD_RX_BUFFER_ALLOC_FAIL; the frame is dropped. `whd/src/bus_protocols/whd_bus_sdio_protocol.c:868` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:873` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:882` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:886` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:888`
- embassy drains every pending frame even when its packet pool is empty, reading into a scratch buffer, so that credits, command responses and events are still processed. `embassy/runner.rs:1098` `embassy/runner.rs:1101` `embassy/runner.rs:1131` `embassy/runner.rs:1134`
- c-driver: an all-zero tag means no packet and clears had_successful_packet, so the next poll consults the interrupt pin. `c-driver/cyw43_ll.c:1120` `c-driver/cyw43_ll.c:1123`
- linux read loop, normal frame: read 64 bytes; parse the header; a control-channel frame goes whole to brcmf_sdio_read_control; otherwise read the remainder. `linux/brcmfmac/sdio.c:1892` `linux/brcmfmac/sdio.c:1894` `linux/brcmfmac/sdio.c:1909` `linux/brcmfmac/sdio.c:1918` `linux/brcmfmac/sdio.c:1919` `linux/brcmfmac/sdio.c:1950`
- linux read-ahead: the SDPCM software header's "next length" byte (bits 23:16) times 16 is the length of the following frame. When non-zero linux reads that whole frame in one CMD53 with no separate header read, then checks that the real length rounded up to 16 equals the predicted one. `linux/brcmfmac/sdio.c:1324` `linux/brcmfmac/sdio.c:1345` `linux/brcmfmac/sdio.c:1346` `linux/brcmfmac/sdio.c:1455` `linux/brcmfmac/sdio.c:2058` `linux/brcmfmac/sdio.c:1969` `linux/brcmfmac/sdio.c:1973` `linux/brcmfmac/sdio.c:1982`
- Read-ahead is not found in whd, c-driver or embassy; they always read the 4-byte tag first. `whd/src/bus_protocols/whd_bus_sdio_protocol.c:823` `c-driver/cyw43_ll.c:1119` `embassy/runner.rs:1058`
- linux header limits: frame length >= 12 (SDPCM_HDRLEN); a non-control, non-superframe frame longer than MAX_RX_DATASZ (2048) is rejected; data offset must be >= 12 and <= length; a next-length above 2048 bytes is zeroed; a tx window more than 64 (0x40) ahead of tx_seq is replaced with tx_seq + 2. `linux/brcmfmac/sdio.c:304` `linux/brcmfmac/sdio.c:1333` `linux/brcmfmac/sdio.c:1395` `linux/brcmfmac/sdio.c:1420` `linux/brcmfmac/sdio.c:1440` `linux/brcmfmac/sdio.c:1456` `linux/brcmfmac/sdio.c:1460` `linux/brcmfmac/sdio.c:1472` `linux/brcmfmac/sdio.c:1475`
- linux buffers: first-read buffer MAX_HDR_READ = 64 bytes; control frames are limited by the common layer's maxctl; MAX_DATA_BUF = 32768 bytes, "must be large enough to hold biggest possible glom". `linux/brcmfmac/sdio.c:133` `linux/brcmfmac/sdio.c:134` `linux/brcmfmac/sdio.c:302` `linux/brcmfmac/sdio.c:303` `linux/brcmfmac/sdio.c:1792` `linux/brcmfmac/sdio.c:1799` `linux/brcmfmac/sdio.c:4079`

### Read abort
| Step | Action | linux | whd | embassy | c-driver | Citations |
|---|---|---|---|---|---|---|
| 1 | Write the function number 2 to the CCCR I/O abort register (F0 0x06) with CMD52 | Only when the caller asks (abort = true), e.g. after a failed CMD53; header-validation failures skip it | yes | yes | not found; the SDIO path has no abort | `linux/brcmfmac/bcmsdh.c:744` `linux/brcmfmac/bcmsdh.c:749` `linux/brcmfmac/sdio.c:1215` `linux/brcmfmac/sdio.c:1216` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:1321` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:1323` `whd/src/bus_protocols/whd_sdio.h:49` `embassy/sdio.rs:242` `embassy/consts.rs:215` `c-driver/cyw43_ll.c:1119` |
| 2 | Write SFC_RF_TERM (0x01) to FRAME_CONTROL (0x1000D) | yes | yes | yes | writes this only on its SPI path | `linux/brcmfmac/sdio.c:1218` `linux/brcmfmac/sdio.c:1219` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:1325` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:1327` `embassy/sdio.rs:243` `c-driver/cyw43_ll.c:1232` |
| 3 | Wait for the FIFO to flush: read RFRAMEBCHI (0x1001C) and RFRAMEBCLO (0x1001B) until both are 0 | Up to 65535 (0xFFFF) iterations; logs "count growing" if the count rises and "count never zeroed" if it never reaches 0 | No wait. Its doc comment lists the wait but the code does not do it; ABORT_TIMEOUT_MS (100) is defined and unused. | no wait | not found | `linux/brcmfmac/sdio.c:1222` `linux/brcmfmac/sdio.c:1226` `linux/brcmfmac/sdio.c:1230` `linux/brcmfmac/sdio.c:1234` `linux/brcmfmac/sdio.c:1241` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:1310` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:75` `embassy/sdio.rs:243` |
| 4 | Optional retransmit request: write SMB_NAK (0x01) to tosbmailbox (core + 0x40) | Writes 4 bytes; then sets rxskip and reads no further frames until it sees HMB_DATA_NAKHANDLED in the host mailbox data | The branch exists (1-byte write) but every call site passes retry = WHD_FALSE, so whd never sends a NAK | no NAK | not found | `linux/brcmfmac/sdio.c:1245` `linux/brcmfmac/sdio.c:1248` `linux/brcmfmac/sdio.c:1251` `linux/brcmfmac/sdio.c:1252` `linux/brcmfmac/sdio.c:459` `linux/brcmfmac/sdio.c:1874` `linux/brcmfmac/sdio.c:2685` `linux/brcmfmac/sdio.c:2687` `linux/brcmfmac/sdio.c:1138` `linux/brcmfmac/sdio.c:1144` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:1329` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:1332` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:827` `embassy/sdio.rs:243` |

- After a NAK, linux backs its expected receive sequence number off by one so the retransmitted frame is accepted. `linux/brcmfmac/sdio.c:2070` `linux/brcmfmac/sdio.c:2071` `linux/brcmfmac/sdio.c:2073`
- whd aborts (IOABORT + RF_TERM, no NAK) after any failed F2 CMD53 during a frame read and returns WHD_SDIO_RX_FAIL. `whd/src/bus_protocols/whd_bus_sdio_protocol.c:825` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:827` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:829` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:904` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:906` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:909`
- embassy on a failed F2 CMD53 read: zero the buffer, write IOABORT (F0 0x06) = 2, write FRAME_CONTROL = SFC_RF_TERM, return the error. Its comment says a timed-out partial F2 read leaves the same packet pending forever and that this mirrors whd's abort path. `embassy/sdio.rs:237` `embassy/sdio.rs:239` `embassy/sdio.rs:241` `embassy/sdio.rs:242` `embassy/sdio.rs:243` `embassy/sdio.rs:246`

linux recovery by failure type:

| Failure | Terminate (RF_TERM) | CMD52 abort | NAK | Citations |
|---|---|---|---|---|
| Header read fails | yes | yes | yes | `linux/brcmfmac/sdio.c:1896` `linux/brcmfmac/sdio.c:1900` |
| Control-frame body read fails ("Control frame failures need retransmission") | yes | yes | yes | `linux/brcmfmac/sdio.c:1811` `linux/brcmfmac/sdio.c:1812` `linux/brcmfmac/sdio.c:1816` |
| Data or event body read fails | yes | yes | only for the event channel (RETRYCHAN) | `linux/brcmfmac/sdio.c:541` `linux/brcmfmac/sdio.c:1954` `linux/brcmfmac/sdio.c:1959` `linux/brcmfmac/sdio.c:1960` |
| No memory for the packet | yes | no | only for events | `linux/brcmfmac/sdio.c:1939` `linux/brcmfmac/sdio.c:1942` `linux/brcmfmac/sdio.c:1943` |
| Bad hardware-tag checksum, over-long frame, bad data offset | yes | no | no | `linux/brcmfmac/sdio.c:1392` `linux/brcmfmac/sdio.c:1424` `linux/brcmfmac/sdio.c:1443` |
| Glom read or glom header failure | yes | yes | no | `linux/brcmfmac/sdio.c:1636` `linux/brcmfmac/sdio.c:1680` |
| Control frame larger than the common layer's maxctl; channel-3 frame without the descriptor flag | yes | no | no | `linux/brcmfmac/sdio.c:1792` `linux/brcmfmac/sdio.c:1795` `linux/brcmfmac/sdio.c:1803` `linux/brcmfmac/sdio.c:2034` |
| Frame length below 12; superframe/sub-frame length mismatch; descriptor flag in a superframe header; wrong superframe/sub-frame channel | no | no | no. The header parser returns an error without calling rxfail; for a normal frame the read loop moves on to the next iteration. | `linux/brcmfmac/sdio.c:1395` `linux/brcmfmac/sdio.c:1397` `linux/brcmfmac/sdio.c:1399` `linux/brcmfmac/sdio.c:1402` `linux/brcmfmac/sdio.c:1404` `linux/brcmfmac/sdio.c:1406` `linux/brcmfmac/sdio.c:1413` `linux/brcmfmac/sdio.c:1416` `linux/brcmfmac/sdio.c:1428` `linux/brcmfmac/sdio.c:1431` `linux/brcmfmac/sdio.c:1433` `linux/brcmfmac/sdio.c:1437` `linux/brcmfmac/sdio.c:1909` `linux/brcmfmac/sdio.c:1915` |
| Read-ahead frame: header fails to parse, or length differs from the predicted one | yes | yes | yes; then falls back to a normal header read | `linux/brcmfmac/sdio.c:1973` `linux/brcmfmac/sdio.c:1975` `linux/brcmfmac/sdio.c:1976` `linux/brcmfmac/sdio.c:1982` `linux/brcmfmac/sdio.c:1986` `linux/brcmfmac/sdio.c:1987` |
| Control frame arriving by read-ahead | yes | no | yes | `linux/brcmfmac/sdio.c:2003` `linux/brcmfmac/sdio.c:2006` `linux/brcmfmac/sdio.c:2007` `linux/brcmfmac/sdio.c:2009` |

### Frame write

- F2 writes carry the SDPCM frame directly, starting with the hardware tag; no bus-level command word precedes it as on SPI. embassy's SDIO wlan_write skips the 4 bytes its buffer reserves for the SPI command (cmd_buf()[4..]). `embassy/sdio.rs:252` `embassy/sdio.rs:253` `embassy/util.rs:85` `embassy/util.rs:95` `embassy/util.rs:99` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:293` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:297` `c-driver/cyw43_ll.c:848`

| Driver | Write padding | Citations |
|---|---|---|
| c-driver | Pads to 64 bytes on SDIO (CYW43_WRITE_BYTES_PAD = ALIGN(len, 64)), 4 on SPI; notes that on SDIO "the actual payload size may also be padded" | `c-driver/cyw43_ll.c:45` `c-driver/cyw43_ll.c:47` `c-driver/cyw43_ll.c:48` `c-driver/cyw43_ll.c:50` `c-driver/cyw43_ll.c:843` `c-driver/cyw43_ll.c:845` |
| embassy | Rounds the frame up to 4 bytes | `embassy/runner.rs:924` |
| linux | Rounds to 4 bytes; control frames longer than one block are padded up to the F2 block size when the pad is within "roundup" | `linux/brcmfmac/bcmsdh.c:323` `linux/brcmfmac/bcmsdh.c:324` `linux/brcmfmac/sdio.c:2420` `linux/brcmfmac/sdio.c:2424` `linux/brcmfmac/sdio.c:2427` |

- linux tx header length is 12 bytes (4 hardware + 8 software), or 20 with tx glom. Buffers are aligned to head_align (>= 4) and the SDPCM data offset absorbs the alignment padding. `linux/brcmfmac/sdio.c:3574` `linux/brcmfmac/sdio.c:3585` `linux/brcmfmac/sdio.c:4515` `linux/brcmfmac/sdio.c:2094` `linux/brcmfmac/sdio.c:2108` `linux/brcmfmac/sdio.c:2232` `linux/brcmfmac/sdio.c:4018` `linux/brcmfmac/sdio.c:4021`
- linux credit check: frames may be sent while (tx_max - tx_seq) is non-zero and has bit 7 clear (both counters are 8-bit and wrap). Data frames reserve TXCTL_CREDITS = 2 credits when a control frame is waiting. `linux/brcmfmac/sdio.c:665` `linux/brcmfmac/sdio.c:678` `linux/brcmfmac/sdio.c:683` `linux/brcmfmac/sdio.c:687` `linux/brcmfmac/sdio.c:692` `linux/brcmfmac/sdio.c:695`
- linux starts tx_seq at 255 (SDPCM_SEQ_WRAP - 1) at probe and resets tx_seq and rx_seq to 0 on bus stop. `linux/brcmfmac/sdio.c:1336` `linux/brcmfmac/sdio.c:4474` `linux/brcmfmac/sdio.c:2538` `linux/brcmfmac/sdio.c:2540`
- linux tx queue: TXQLEN 2048; flow control to the stack is asserted above TXHI (2048 - 256) and released below TXLOW (TXHI - 256); 8 priorities (PRIOMASK 7). `linux/brcmfmac/sdio.c:116` `linux/brcmfmac/sdio.c:117` `linux/brcmfmac/sdio.c:118` `linux/brcmfmac/sdio.c:119` `linux/brcmfmac/sdio.c:2388` `linux/brcmfmac/sdio.c:2390` `linux/brcmfmac/sdio.c:4076`

### Write abort and retry
| Driver | On a failed F2 write | Citations |
|---|---|---|
| linux | Send the CMD52 abort for function 2, write SFC_WF_TERM (0x02) to FRAME_CONTROL, then read WFRAMEBCHI (0x1001A) / WFRAMEBCLO (0x10019) up to 3 times until both are 0 | `linux/brcmfmac/sdio.c:1259` `linux/brcmfmac/sdio.c:1264` `linux/brcmfmac/sdio.c:1268` `linux/brcmfmac/sdio.c:1269` `linux/brcmfmac/sdio.c:1272` `linux/brcmfmac/sdio.c:1274` `linux/brcmfmac/sdio.c:1276` |
| whd | No write abort; the failed send returns the error | `whd/src/bus_protocols/whd_bus_sdio_protocol.c:308` |
| embassy | No write abort; the write error is discarded | `embassy/runner.rs:928` |
| c-driver | Not found | `c-driver/cyw43_ll.c:848` |

- linux retries a failed control-frame write up to TXRETRIES (2) more times, running the write-abort sequence after each failure; the sequence number advances only on success. `linux/brcmfmac/sdio.c:121` `linux/brcmfmac/sdio.c:2448` `linux/brcmfmac/sdio.c:2451` `linux/brcmfmac/sdio.c:2452` `linux/brcmfmac/sdio.c:2454` `linux/brcmfmac/sdio.c:2455`
- linux does not retry data frames: on failure the packets are completed with an error. `linux/brcmfmac/sdio.c:2316` `linux/brcmfmac/sdio.c:2317` `linux/brcmfmac/sdio.c:2323` `linux/brcmfmac/sdio.c:2328`
- linux defines SDIOH_API_ACCESS_RETRY_LIMIT = 2 but never uses it; it is not evidence of a retry. `linux/brcmfmac/bcmsdh.c:40`
- whd's low-level SDIO transfer does not retry. Its comment says the function's retry logic was broken, never actually retrying, and has since been taken out. `whd/src/bus_protocols/whd_bus_sdio_protocol.c:979` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:980` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:982`
- linux: a bus access failing with -ENOMEDIUM moves the device to state NOMEDIUM. `linux/brcmfmac/bcmsdh.c:309` `linux/brcmfmac/bcmsdh.c:310` `linux/brcmfmac/bcmsdh.c:328` `linux/brcmfmac/bcmsdh.c:329` `linux/brcmfmac/sdio.h:153` `linux/brcmfmac/sdio.h:156`
- linux: if any backplane access in the DPC fails it logs "failed backplane access over SDIO, halting operation" and stops processing. `linux/brcmfmac/sdio.c:2727` `linux/brcmfmac/sdio.c:2728` `linux/brcmfmac/sdio.c:2729`

## Watermark

| Driver | Value written to 0x10008 on SDIO after firmware start | Citations |
|---|---|---|
| whd | 8 (SDIO_F2_WATERMARK), one value for every chip | `whd/src/bus_protocols/whd_bus_sdio_protocol.c:77` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:1291` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:1292` |
| c-driver | 8 (SDIO_F2_WATERMARK) | `c-driver/cyw43_ll.c:149` `c-driver/cyw43_ll.c:1828` `c-driver/cyw43_ll.c:1829` |
| embassy | 8 (SDIO_F2_WATERMARK = 0x08), one value for every chip on SDIO | `embassy/consts.rs:107` `embassy/runner.rs:625` `embassy/runner.rs:628` |
| linux | 8 (DEFAULT_F2_WATERMARK = 0x8) for chips not in its per-chip switch, which includes the 43439 | `linux/brcmfmac/sdio.c:43` `linux/brcmfmac/sdio.c:4353` `linux/brcmfmac/sdio.c:4354` `linux/brcmfmac/sdio.c:4355` |

- whd comment: "Lower F2 Watermark to avoid DMA Hang in F2 when SD Clock is stopped". `whd/src/bus_protocols/whd_bus_sdio_protocol.c:1290`
- linux states the watermark is "expressed in number of words" and logs it as "F2 watermark to 0x%x*4 bytes"; by that reading 8 means 32 bytes (inferred). `linux/brcmfmac/sdio.c:42` `linux/brcmfmac/sdio.c:4286`
- Under linux the 43439's SDIO device id is not in the watermark switch. It takes the default branch: only SBSDIO_WATERMARK = 8 is written; DEVICE_CTL F2WM_ENAB is not set and MESBUSYCTRL is not written. `linux/brcmfmac/sdio.c:4282` `linux/brcmfmac/sdio.c:4283` `linux/brcmfmac/sdio.c:4298` `linux/brcmfmac/sdio.c:4311` `linux/brcmfmac/sdio.c:4325` `linux/brcmfmac/sdio.c:4338` `linux/brcmfmac/sdio.c:4353`
- On SPI the same register gets 32 (SPI_F2_WATERMARK; embassy 0x20). whd's SPI file comments that on the 43362 the value has to be at least 8 and word-aligned, or the dongle firmware crashes. linux has no SPI transport. `whd/src/bus_protocols/whd_bus_spi_protocol.c:73` `whd/src/bus_protocols/whd_bus_spi_protocol.c:74` `whd/src/bus_protocols/whd_bus_spi_protocol.c:1080` `whd/src/bus_protocols/whd_bus_spi_protocol.c:1082` `c-driver/cyw43_ll.c:148` `c-driver/cyw43_ll.c:1838` `embassy/consts.rs:106` `embassy/runner.rs:677` `linux/brcmfmac/sdio.c:43`
- c-driver's Bluetooth-build watermark test write (0x10, read back) is step 8a of the bring-up table. `c-driver/cyw43_ll.c:1733` `c-driver/cyw43_ll.c:1737`

linux per-chip watermarks. Each also sets DEVICE_CTL F2WM_ENAB (0x10). `linux/brcmfmac/sdio.c:4292`

| Chips | F2 watermark | MESBUSYCTRL value | Citations |
|---|---|---|---|
| 43751, 43752, 4373 | 64 (0x40) | 0x40 + 0x80 | `linux/brcmfmac/sdio.c:44` `linux/brcmfmac/sdio.c:45` `linux/brcmfmac/sdio.c:4283` `linux/brcmfmac/sdio.c:4288` `linux/brcmfmac/sdio.c:4292` `linux/brcmfmac/sdio.c:4295` |
| 43012 | 96 (0x60) | 0x50 + 0x80 | `linux/brcmfmac/sdio.c:46` `linux/brcmfmac/sdio.c:47` `linux/brcmfmac/sdio.c:48` `linux/brcmfmac/sdio.c:4298` `linux/brcmfmac/sdio.c:4301` `linux/brcmfmac/sdio.c:4308` |
| 4329, 4339 | 48 | 80 + 0x80 | `linux/brcmfmac/sdio.c:50` `linux/brcmfmac/sdio.c:51` `linux/brcmfmac/sdio.c:52` `linux/brcmfmac/sdio.c:4311` `linux/brcmfmac/sdio.c:4315` `linux/brcmfmac/sdio.c:4322` |
| 43455 | 96 (0x60) | 0x50 + 0x80 | `linux/brcmfmac/sdio.c:54` `linux/brcmfmac/sdio.c:55` `linux/brcmfmac/sdio.c:56` `linux/brcmfmac/sdio.c:4325` `linux/brcmfmac/sdio.c:4328` `linux/brcmfmac/sdio.c:4335` |
| 4359, 4354, 4356 | 64 (0x40) | 0x40 + 0x80 | `linux/brcmfmac/sdio.c:58` `linux/brcmfmac/sdio.c:59` `linux/brcmfmac/sdio.c:4338` `linux/brcmfmac/sdio.c:4343` `linux/brcmfmac/sdio.c:4350` |

## Differences from the SPI path

| Topic | SDIO | SPI | Citations |
|---|---|---|---|
| F1 register block at 0x10000 | Used | Shared: the SPI paths use the same addresses for the watermark, backplane window, frame control, chip clock CSR, pull-up, wakeup control and sleep CSR. c-driver uses its SDIO_* names on SPI too; whd's SPI file writes SDIO_CHIP_CLOCK_CSR and SDIO_FUNCTION2_WATERMARK. | `c-driver/cyw43_ll.c:108` `c-driver/cyw43_ll.c:112` `c-driver/cyw43_ll.c:1730` `c-driver/cyw43_ll.c:1838` `c-driver/cyw43_ll.c:1866` `c-driver/cyw43_ll.c:1885` `whd/src/bus_protocols/whd_bus_spi_protocol.c:667` `whd/src/bus_protocols/whd_bus_spi_protocol.c:1081` `whd/src/bus_protocols/whd_spi.h:29` |
| ALP request value | 0x29 (FORCE_HW_CLKREQ_OFF + ALP_AVAIL_REQ + FORCE_ALP) | 0x08 (ALP_AVAIL_REQ) only | `c-driver/cyw43_ll.c:1727` `c-driver/cyw43_ll.c:1728` `c-driver/cyw43_ll.c:1730` `embassy/runner.rs:479` `embassy/runner.rs:481` `embassy/runner.rs:493` `embassy/runner.rs:498` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:451` `whd/src/bus_protocols/whd_bus_spi_protocol.c:666` `whd/src/bus_protocols/whd_bus_spi_protocol.c:668` |
| Learning that a frame waits, and its length | No status word: the host reads the 4-byte hardware tag from F2 and takes the length from it | From the gSPI status register: F2 packet-available bit and an 11-bit length field at bits 19:9 | `embassy/runner.rs:1046` `embassy/runner.rs:1048` `embassy/runner.rs:1051` `embassy/runner.rs:1055` `embassy/runner.rs:1058` `embassy/runner.rs:1066` `embassy/consts.rs:48` `embassy/consts.rs:50` `c-driver/cyw43_ll.c:1118` `c-driver/cyw43_ll.c:1119` `c-driver/cyw43_ll.c:1226` `c-driver/cyw43_ll.c:1228` |
| Interrupt source | The SDIO core's intstatus (backplane, core + 0x20), host-mailbox bits 0xF0, delivered in-band or on the out-of-band pin through SEP_INT_CTL | The 2-byte gSPI interrupt register on function 0 (F2_PACKET_AVAILABLE 0x0020 and others) | `embassy/runner.rs:967` `embassy/runner.rs:968` `embassy/runner.rs:971` `embassy/runner.rs:1015` `embassy/runner.rs:1017` `embassy/runner.rs:1022` `embassy/consts.rs:144` `c-driver/cyw43_ll.c:1109` `c-driver/cyw43_ll.c:1110` |
| F2-ready test after firmware start | Poll CCCR IORDY bit 0x04 | Poll gSPI status register bit STATUS_F2_RX_READY (0x20) | `embassy/runner.rs:685` `embassy/runner.rs:686` `embassy/runner.rs:687` `embassy/consts.rs:45` `embassy/consts.rs:225` `c-driver/cyw43_ll.c:1844` `c-driver/cyw43_ll.c:1846` `c-driver/cyw43_ll.c:1847` `c-driver/cyw43_ll.c:1851` `c-driver/cyw43_ll.c:1852` |
| funcintmask (core + 0x34) | Written with 0x03 | Not written; the drivers program the gSPI interrupt-enable register instead, and with Bluetooth write hostintmask = I_HMB_FC_CHANGE (0x20) | `c-driver/cyw43_ll.c:1824` `c-driver/cyw43_ll.c:1826` `c-driver/cyw43_ll.c:1830` `c-driver/cyw43_ll.c:1832` `c-driver/cyw43_ll.c:1834` `embassy/runner.rs:620` `embassy/runner.rs:622` `embassy/runner.rs:656` `embassy/runner.rs:658` `embassy/runner.rs:662` `embassy/runner.rs:665` `embassy/runner.rs:671` |
| F2 watermark | 8 | 32 | `c-driver/cyw43_ll.c:148` `c-driver/cyw43_ll.c:149` `c-driver/cyw43_ll.c:1829` `c-driver/cyw43_ll.c:1838` `embassy/consts.rs:106` `embassy/consts.rs:107` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:77` `whd/src/bus_protocols/whd_bus_spi_protocol.c:74` |
| Maximum F1 (backplane) transfer | 1536 bytes (whd), 16384 bytes (c-driver) | 64 bytes (WHD_BUS_SPI_MAX_BACKPLANE_TRANSFER_SIZE; c-driver CYW43_BUS_MAX_BLOCK_SIZE = 64) | `whd/src/bus_protocols/whd_bus_spi_protocol.h:52` `whd/src/bus_protocols/whd_bus_sdio_protocol.h:35` `c-driver/cyw43_ll.h:193` `c-driver/cyw43_ll.h:197` |
| Backplane read padding | 0 | 4 (whd), 16 (c-driver) | `whd/src/bus_protocols/whd_bus_sdio_protocol.h:36` `whd/src/bus_protocols/whd_bus_spi_protocol.h:53` `c-driver/cyw43_ll.h:194` `c-driver/cyw43_ll.h:198` |
| 32-bit access flag (0x8000), c-driver | Only on 4-byte register accesses | On every backplane access including bulk download | `c-driver/cyw43_ll.c:352` `c-driver/cyw43_ll.c:353` `c-driver/cyw43_ll.c:355` `c-driver/cyw43_ll.c:356` `c-driver/cyw43_ll.c:428` `c-driver/cyw43_ll.c:429` |
| Read abort | CCCR I/O-abort CMD52 for function 2 first, then RF_TERM (whd, embassy, linux) | Only a write of 0x01 to FRAME_CONTROL (0x1000D), when the status register shows an invalid length or a FIFO underflow | `c-driver/cyw43_ll.c:1229` `c-driver/cyw43_ll.c:1230` `c-driver/cyw43_ll.c:1232` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:1322` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:1326` `embassy/sdio.rs:242` `embassy/sdio.rs:243` |
| "TX stalled" poke (SMB_DEV_INT to tosbmailbox) | Sent by c-driver and embassy | Not sent by c-driver or embassy | `c-driver/cyw43_ll.c:789` `c-driver/cyw43_ll.c:790` `c-driver/cyw43_ll.c:791` `embassy/runner.rs:942` `embassy/runner.rs:945` |
| Write padding, c-driver | 64 bytes | 4 bytes | `c-driver/cyw43_ll.c:45` `c-driver/cyw43_ll.c:48` `c-driver/cyw43_ll.c:50` |
| HT wait timeout, whd | 2500 ms | 1000 ms | `whd/src/bus_protocols/whd_bus_sdio_protocol.c:74` `whd/src/bus_protocols/whd_bus_spi_protocol.c:71` |
| "Wrong payload type" error, c-driver | Reported as an unexpected packet | Ignored ("can occur when there is a lot of traffic over the SPI") | `c-driver/cyw43_ll.c:1281` `c-driver/cyw43_ll.c:1282` `c-driver/cyw43_ll.c:1284` `c-driver/cyw43_ll.c:1286` `c-driver/cyw43_ll.c:1287` |
| Host-interrupt pin level, c-driver | Active low (host_interrupt_pin_active = 0) | Active high with CYW43_PIN_WL_HOST_WAKE, active low with CYW43_PIN_WL_IRQ | `c-driver/cyw43_ll.c:53` `c-driver/cyw43_ll.c:55` `c-driver/cyw43_ll.c:57` `c-driver/cyw43_ll.c:60` `c-driver/cyw43_ll.c:61` |
| Country code, c-driver | Appends CLM revision 17 to the worldwide country code ("For the 1DX CLM ... increases throughput by about 25% on PYBD") | Not done | `c-driver/cyw43_ll.c:2005` `c-driver/cyw43_ll.c:2006` `c-driver/cyw43_ll.c:2009` |
| wake_bus, embassy | HT request and poll before F2 transfers | Does nothing | `embassy/runner.rs:771` `embassy/runner.rs:772` `embassy/runner.rs:798` `embassy/runner.rs:799` |

- linux has no gSPI transport in the files read. Comments in its SDIO code still refer to gSPI behaviour: DEVREADY "does not occur with gSPI"; I_CHIPACTIVE "Would be active due to wake-wlan in gSPI". `linux/brcmfmac/sdio.c:1148` `linux/brcmfmac/sdio.c:1149` `linux/brcmfmac/sdio.c:2679`
