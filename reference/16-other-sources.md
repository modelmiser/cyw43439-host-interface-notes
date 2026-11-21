# Other sources

Material from the smaller source files: the PIO SPI bus, the SDIO crate, the bcma headers, the country table, host glue and service loops. It closes with cross-driver comparisons and the questions these sources leave open.

## PIO SPI bus for the Pico W (embassy-pio/lib.rs)

### Pins and electrical setup

- embassy's PioSpi uses one PIO state machine and two PIO pins. The clock is the program's 1-bit side-set pin. One data pin is the OUT pin, the IN pin and the SET (direction) pin at once. `embassy-pio/lib.rs:18-26` `embassy-pio/lib.rs:200-204`
- Chip-select is an ordinary GPIO output, held outside the PIO program. `embassy-pio/lib.rs:18-26`
- Data pin: no pull, Schmitt trigger on, 12 mA drive, fast slew, input-synchroniser bypass. `embassy-pio/lib.rs:190-194` `embassy-pio/lib.rs:212`
- Clock pin: 12 mA drive, fast slew. `embassy-pio/lib.rs:196-198`
- Both pins start as outputs driven low. `embassy-pio/lib.rs:216-217`

### Wire bit order

- embassy shifts both output and input with `ShiftDirection::Left` and auto-fill on. `embassy-pio/lib.rs:205-210`
- The threshold lines are commented out, so the PIO default threshold applies. `embassy-pio/lib.rs:207` `embassy-pio/lib.rs:210`
- Whole u32 words are moved by DMA in both directions. `embassy-pio/lib.rs:249-252` `embassy-pio/lib.rs:277-280`
- (unverified) A left shift sends and receives the most significant bit of each u32 first, and the default threshold is 32 bits. This is RP2040/RP2350 PIO behaviour (recalled, not in these sources). The source lines are confirmed; this reading of them is not. `embassy-pio/lib.rs:205-210`
- Consequence for a caller (inferred): the 32-bit command word built by embassy/spi.rs goes on the wire as one u32, not as a little-endian byte stream. `embassy-pio/lib.rs:249-252` `embassy-pio/lib.rs:277-280`

### Clocking: the three PIO programs

embassy loads one of three programs. They share the write loop and differ in the turnaround and in the side-set phase of the read loop. `embassy-pio/lib.rs:101-123` `embassy-pio/lib.rs:134-155` `embassy-pio/lib.rs:165-186`

| Phase | Low-speed program | High-speed program | Overclock program | Citations |
|---|---|---|---|---|
| Write loop | `out pins, 1 side 0` then `jmp x-- lp side 1` | same | same | `embassy-pio/lib.rs:170-172` `embassy-pio/lib.rs:139-141` `embassy-pio/lib.rs:106-108` |
| Direction switch | `set pindirs, 0 side 0` | `set pindirs, 0 side 0` | `set pindirs, 0 side 0` | `embassy-pio/lib.rs:174` `embassy-pio/lib.rs:143` `embassy-pio/lib.rs:110` |
| Turnaround padding | `nop side 0` (clock stays low) | `nop side 1` | `nop side 1` then `nop side 0` | `embassy-pio/lib.rs:175` `embassy-pio/lib.rs:144` `embassy-pio/lib.rs:111-112` |
| Read loop | `in pins, 1 side 1` then `jmp y-- lp2 side 0` | `in pins, 1 side 0` then `jmp y-- lp2 side 1` | `in pins, 1 side 1` then `jmp y-- lp2 side 0` | `embassy-pio/lib.rs:177-179` `embassy-pio/lib.rs:146-148` `embassy-pio/lib.rs:114-116` |
| Clock rising edges from the direction switch to the end of the read loop (counted from the side-set values) | Y+1 | Y+2 | Y+2 | `embassy-pio/lib.rs:174-179` `embassy-pio/lib.rs:143-148` `embassy-pio/lib.rs:110-116` |
| Tail | `wait 1 pin 0 side 0` then `irq 0 side 0` | same | same | `embassy-pio/lib.rs:181-183` `embassy-pio/lib.rs:150-152` `embassy-pio/lib.rs:118-120` |

- Write: a bit is placed on the data pin with the clock low; the following loop instruction raises the clock. Bits written = X+1. `embassy-pio/lib.rs:106-108` `embassy-pio/lib.rs:139-141` `embassy-pio/lib.rs:170-172`
- Read: one bit is sampled per two PIO instructions. Bits read = Y+1. `embassy-pio/lib.rs:114-116` `embassy-pio/lib.rs:146-148` `embassy-pio/lib.rs:177-179`
- In the high-speed program the `in` instruction carries side 0 and the loop jump side 1, the opposite phase to the other two programs. `embassy-pio/lib.rs:146-148`
- The high-speed and overclock programs produce one more clock rising edge than the low-speed program before the first `in` instruction (the turnaround `nop side 1`). `embassy-pio/lib.rs:144` `embassy-pio/lib.rs:111` `embassy-pio/lib.rs:175`
- At which instant of an instruction a PIO `in` samples relative to its side-set change is PIO behaviour (recalled, not in these sources). `embassy-pio/lib.rs:114-116`

### Program selection and clock dividers

- Effective PIO clock = clk_sys / (clock_divider / 256). `embassy-pio/lib.rs:67`
- Above 100 MHz embassy loads the overclock program; 75 MHz to 100 MHz inclusive the high-speed program; below 75 MHz the low-speed program. `embassy-pio/lib.rs:85-91` `embassy-pio/lib.rs:125` `embassy-pio/lib.rs:157`
- The file says the cut-offs were found experimentally and that the programs are based on the pico-sdk's cyw43_bus_pio_spi.pio. That pico-sdk file is not found in these sources. `embassy-pio/lib.rs:85-91`
- The gSPI clock is half the PIO clock (two instructions per bit), per embassy's comments. `embassy-pio/lib.rs:28-46`
- The comments call 50 MHz the manufacturer-recommended maximum gSPI clock. This is a comment in embassy, not a datasheet citation. `embassy-pio/lib.rs:36-39` `embassy-pio/lib.rs:92-93`

| Constant | Value (8.8 fixed point) | gSPI clock, RP2040 at 133 MHz (per comment) | gSPI clock, RP2350 at 150 MHz (per comment) | Citations |
|---|---|---|---|---|
| `DEFAULT_CLOCK_DIVIDER` | 2 << 8 | 33.25 MHz | 37.5 MHz | `embassy-pio/lib.rs:28-32` |
| `OVERCLOCK_CLOCK_DIVIDER` | 1 << 8 | 66.5 MHz | 75 MHz | `embassy-pio/lib.rs:34-40` |
| `RM2_CLOCK_DIVIDER` | 3 << 8 | 22.16 MHz | 25 MHz | `embassy-pio/lib.rs:42-46` |

- embassy emits a trace warning when the divider has a non-zero fractional part. Reason given: fractional PIO dividers mix long and short clock cycles, and the short ones may exceed the intended maximum gSPI speed. The comment says the chip "seems to handle the jitter well". `embassy-pio/lib.rs:72-83`

### Transaction framing
| Step | Write (`cmd_write`) | Read (`cmd_read`) | Citations |
|---|---|---|---|
| Before starting | disable the state machine, set data pin to output, jump to program start, re-enable | same | `embassy-pio/lib.rs:231-246` `embassy-pio/lib.rs:257-275` |
| X (bits to write, minus 1) | 32 * words - 1 | 31 (the command word only) | `embassy-pio/lib.rs:233` `embassy-pio/lib.rs:259` |
| Y (bits to read, minus 1) | 31 | 32 * read.len() + 32 - 1 | `embassy-pio/lib.rs:234` `embassy-pio/lib.rs:260` |
| Pushed by DMA | all words, command word first | the command word | `embassy-pio/lib.rs:251` `embassy-pio/lib.rs:279` |
| Pulled by DMA | one u32, returned as status | read.len() words into the caller's buffer, then one more u32 returned as status | `embassy-pio/lib.rs:248-253` `embassy-pio/lib.rs:277-291` |
| Chip-select | low before the transfer, high after the status word | same | `embassy-pio/lib.rs:299-304` `embassy-pio/lib.rs:306-311` |

- There is no chip-select toggle between command, data and status. `embassy-pio/lib.rs:299-311` `embassy/spi.rs:13-14`

### Status word capture

- The u32 embassy's bus trait returns from cmd_write and cmd_read is always the last 32 bits clocked in after the payload. `embassy-pio/lib.rs:248-253` `embassy-pio/lib.rs:282-291`
- After a write, that word is the 32 bits clocked in immediately after the last written bit plus the turnaround. `embassy-pio/lib.rs:231-254`
- embassy/spi.rs stores the returned word in `self.status` after every transfer. `embassy/spi.rs:135` `embassy/spi.rs:144` `embassy/spi.rs:152` `embassy/spi.rs:161` `embassy/spi.rs:282` `embassy/spi.rs:292`
- embassy expects those bits to be the gSPI status word because it sets STATUS_ENABLE (and INTR_WITH_STATUS) in the bus-control register during init. `embassy/spi.rs:215-226`
- The transfers before that write (the swapped bus-test reads and writes) also capture a trailing word into `self.status`. These sources do not define its content. `embassy/spi.rs:152` `embassy/spi.rs:161` `embassy/spi.rs:215-226`

### Backplane read padding at the PIO level

- The PIO layer does nothing special for backplane reads. The response delay appears as one extra leading u32 in the read buffer. The trait doc says: to read n words from the backplane, pass an n+1 word slice. `embassy/spi.rs:20-25`
- embassy's `readn` uses a 2-word buffer for the backplane function and takes word [1]. `embassy/spi.rs:129-139`
- embassy's `bp_read` reads len/4 rounded up, plus 1, words and copies from byte offset 4. `embassy/spi.rs:323-330`

### 16-bit swapped accesses before 32-bit mode

- The PIO layer has no notion of word length. embassy/spi.rs swaps the two 16-bit halves of the command word and of the data (`swap16`) around the same PIO routines until it has written WORD_LENGTH_32 to the bus-control register. `embassy/spi.rs:147-162` `embassy/spi.rs:190-226`

### Interrupt wait

- Every embassy PIO program ends with `wait 1 pin 0` then `irq 0`. `embassy-pio/lib.rs:118-120` `embassy-pio/lib.rs:150-152` `embassy-pio/lib.rs:181-183`
- The only IN pin configured is the data pin. `embassy-pio/lib.rs:203`
- So after the read phase the state machine stalls until the data pin, now an input, reads high, then raises PIO interrupt flag 0 (inferred: that `wait 1 pin 0` indexes the IN-pin mapping is PIO behaviour, recalled, not in these sources). `embassy-pio/lib.rs:118-120` `embassy-pio/lib.rs:203`
- `wait_for_event()` awaits that PIO IRQ and nothing else. `embassy-pio/lib.rs:21` `embassy-pio/lib.rs:322-324`
- In this implementation the interrupt is therefore sampled on the data pin while the bus is idle, level-sensitive high. This matches INTERRUPT_POLARITY_HIGH that embassy writes to the bus-control register. `embassy-pio/lib.rs:118-120` `embassy/spi.rs:220`
- The wait/irq pair sits at the end of the transfer program, and every new transfer disables the state machine and jumps back to the program start. The PIO IRQ can only fire after a transfer has completed and before the next one starts. `embassy-pio/lib.rs:232-246` `embassy-pio/lib.rs:258-275`
- Whether the board routes the chip's interrupt onto the data line is not stated in this file. The only board reference is the comment naming pico-sdk's cyw43_spi_gpio_setup(). `embassy-pio/lib.rs:313-315`

| Host | How it waits for the chip's interrupt | Citations |
|---|---|---|
| embassy, PioSpi | PIO program waits for the data pin to read high, then raises PIO IRQ 0; `wait_for_event` awaits it | `embassy-pio/lib.rs:118-120` `embassy-pio/lib.rs:322-324` |
| embassy, trait default | a bus implementation that does not override `wait_for_event` just yields, so the runner polls continuously | `embassy/spi.rs:31-35` |
| embassy, SDIO | `wait_for_event` delegates to the sdio crate, which delegates to the host bus implementation (not found in these sources); the result is ignored | `sdio-crate/src/sdio.rs:550-553` `embassy/sdio.rs:389-390` |
| c-driver | reads a GPIO chosen at build time: CYW43_PIN_WL_HOST_WAKE, else CYW43_PIN_WL_IRQ, else the SDIO data-1 pin | `c-driver/cyw43_ctrl.c:254-266` |
| c-driver, arming | falling-edge interrupt on CYW43_PIN_WL_HOST_WAKE only in non-SPI builds without USE_SDIOIT; on CYW43_PIN_WL_IRQ whenever that pin is defined; with USE_SDIOIT the SDIO in-band interrupt is enabled instead | `c-driver/cyw43_ctrl.c:177-185` |

### Reset preparation

- Before the power pin is pulsed embassy calls `prepare_reset()`: disable the state machine, make the data pin an output driven low, set CS high. `embassy-pio/lib.rs:313-320`
- The comment says the data pin must be held low across the WL_REG_ON pulse, "as per pico-sdk's cyw43_spi_gpio_setup()". `embassy-pio/lib.rs:314-315`

| Host | Power pin low | Wait after raising it, before first bus access | Citations |
|---|---|---|---|
| embassy | 20 ms | 250 ms | `embassy/spi.rs:181-187` |
| c-driver | 20 ms | 50 ms | `c-driver/cyw43_ctrl.c:140-144` |

## SDIO crate used by embassy (sdio-crate/src/sdio.rs)

### CCCR register map (function 0)

embassy imports three of these names: CCCR_IO_ENABLE, CCCR_IO_READY, CCCR_INT_ENABLE. `embassy/sdio.rs:5` `embassy/runner.rs:11`

| Address | Crate name | Notes | Citations |
|---|---|---|---|
| 0 (0x00) | `CCCR_REV` | | `sdio-crate/src/sdio.rs:257-291` |
| 1 (0x01) | `CCCR_SD_REV` | | `sdio-crate/src/sdio.rs:257-291` |
| 2 (0x02) | `CCCR_IO_ENABLE` | imported by embassy; same value as c-driver SDIOD_CCCR_IOEN and whd | `sdio-crate/src/sdio.rs:262` `c-driver/cyw43_ll.c:190-192` `whd/src/bus_protocols/whd_sdio.h:45-47` |
| 3 (0x03) | `CCCR_IO_READY` | imported by embassy; same value as c-driver SDIOD_CCCR_IORDY and whd | `sdio-crate/src/sdio.rs:264` `c-driver/cyw43_ll.c:190-192` `whd/src/bus_protocols/whd_sdio.h:45-47` |
| 4 (0x04) | `CCCR_INT_ENABLE` | imported by embassy; same value as c-driver SDIOD_CCCR_INTEN and whd; bit 0 is the master enable | `sdio-crate/src/sdio.rs:266` `c-driver/cyw43_ll.c:190-192` `whd/src/bus_protocols/whd_sdio.h:45-47` `sdio-crate/src/sdio.rs:534-538` |
| 5 (0x05) | `CCCR_INT_PENDING` | | `sdio-crate/src/sdio.rs:257-291` |
| 6 (0x06) | `CCCR_IO_ABORT` | embassy's own copy: SDIOD_CCCR_IOABORT 0x06 | `sdio-crate/src/sdio.rs:270` `embassy/consts.rs:211-218` |
| 7 (0x07) | `CCCR_BUS_CTRL` | | `sdio-crate/src/sdio.rs:257-291` |
| 8 (0x08) | `CCCR_CARD_CAP` | | `sdio-crate/src/sdio.rs:257-291` |
| 9 (0x09) | `CCCR_CIS_PTR` | 3 bytes | `sdio-crate/src/sdio.rs:257-291` |
| 12 (0x0C) | `CCCR_BUS_SUSPEND` | | `sdio-crate/src/sdio.rs:257-291` |
| 13 (0x0D) | `CCCR_FUNC_SEL` | | `sdio-crate/src/sdio.rs:257-291` |
| 14 (0x0E) | `CCCR_EXEC_FLAGS` | | `sdio-crate/src/sdio.rs:257-291` |
| 15 (0x0F) | `CCCR_READY_FLAGS` | | `sdio-crate/src/sdio.rs:257-291` |
| 16 (0x10) | `CCCR_FN0_BLKSZ_LO` | embassy's own copy: SDIOD_CCCR_BLKSIZE_0 0x10 | `sdio-crate/src/sdio.rs:286` `embassy/consts.rs:211-218` |
| 17 (0x11) | `CCCR_FN0_BLKSZ_HI` | | `sdio-crate/src/sdio.rs:257-291` |
| 18 (0x12) | `CCCR_POWER_CTRL` | | `sdio-crate/src/sdio.rs:257-291` |
| 19 (0x13) | `CCCR_HIGH_SPEED` | embassy's own copy: SDIOD_CCCR_SPEED_CONTROL 0x13 | `sdio-crate/src/sdio.rs:291` `embassy/consts.rs:211-218` |

- embassy's SDIOD_CCCR_F1BLKSIZE_0 0x110 and F2BLKSIZE_0 0x210 equal the crate's fbr_base(n) = n * 0x100 plus FBR_BLKSZ_LO 0x10. `embassy/consts.rs:211-218` `sdio-crate/src/sdio.rs:353-361`
- embassy's SDIOD_CCCR_BRCM_CARDCAP 0xf0 and SDIOD_SEP_INT_CTL 0xf2 have no counterpart in the crate; its CCCR list ends at 0x13. `embassy/consts.rs:211-218` `sdio-crate/src/sdio.rs:257-291`

### CCCR bit fields
| Register | Field | Value | Citations |
|---|---|---|---|
| BUS_CTRL | width mask | 0x03 (1-bit 0x00, 4-bit 0x02, 8-bit 0x03) | `sdio-crate/src/sdio.rs:293-334` |
| BUS_CTRL | ECSI | 0x20 | `sdio-crate/src/sdio.rs:293-334` |
| BUS_CTRL | SCSI | 0x40 | `sdio-crate/src/sdio.rs:293-334` |
| BUS_CTRL | CD_DISABLE | 0x80 | `sdio-crate/src/sdio.rs:293-334` |
| CARD_CAP | SDC | 0x01 | `sdio-crate/src/sdio.rs:293-334` |
| CARD_CAP | SMB | 0x02 | `sdio-crate/src/sdio.rs:293-334` |
| CARD_CAP | SRW | 0x04 | `sdio-crate/src/sdio.rs:293-334` |
| CARD_CAP | SBS | 0x08 | `sdio-crate/src/sdio.rs:293-334` |
| CARD_CAP | S4MI | 0x10 | `sdio-crate/src/sdio.rs:293-334` |
| CARD_CAP | E4MI | 0x20 | `sdio-crate/src/sdio.rs:293-334` |
| CARD_CAP | LSC | 0x40 | `sdio-crate/src/sdio.rs:293-334` |
| CARD_CAP | 4BLS | 0x80 | `sdio-crate/src/sdio.rs:293-334` |
| HIGH_SPEED | SHS (supported) | 0x01 | `sdio-crate/src/sdio.rs:293-334` |
| HIGH_SPEED | EHS (enable) | 0x02 | `sdio-crate/src/sdio.rs:293-334` |
| INT_ENABLE | master enable | 0x01; the crate ORs it into the function mask; embassy has CCCR_INT_ENABLE_MASTER = 0x01 | `sdio-crate/src/sdio.rs:534-538` `embassy/consts.rs:79` |

### FBR layout

Each function N has a Function Basic Register block at N * 0x100. `sdio-crate/src/sdio.rs:336-378`

| Offset in block | Crate name | Size | Citations |
|---|---|---|---|
| 0 (0x00) | FUNCTION_IF | 1 | `sdio-crate/src/sdio.rs:336-378` |
| 1 (0x01) | EXT_IF | 1 | `sdio-crate/src/sdio.rs:336-378` |
| 2 (0x02) | POWER_SEL | 1 | `sdio-crate/src/sdio.rs:336-378` |
| 9 (0x09) | CIS_PTR | 3 | `sdio-crate/src/sdio.rs:336-378` |
| 12 (0x0C) | CSA_PTR | 3 | `sdio-crate/src/sdio.rs:336-378` |
| 15 (0x0F) | CSA_DATA | 1 | `sdio-crate/src/sdio.rs:336-378` |
| 16 (0x10) | BLKSZ_LO | 1 | `sdio-crate/src/sdio.rs:336-378` |
| 17 (0x11) | BLKSZ_HI | 1 | `sdio-crate/src/sdio.rs:336-378` |

### CMD52 (IO_RW_DIRECT) argument

Response type R5. `sdio-crate/src/sdio.rs:46-65`

| Bits | Field | Citations |
|---|---|---|
| 31 | write flag | `sdio-crate/src/sdio.rs:46-65` |
| 30:28 | function (3 bits) | `sdio-crate/src/sdio.rs:46-65` |
| 27 | RAW (read-after-write) | `sdio-crate/src/sdio.rs:46-65` |
| 25:9 | register address (17 bits) | `sdio-crate/src/sdio.rs:46-65` |
| 7:0 | write data; 0 on reads | `sdio-crate/src/sdio.rs:46-65` |

- c-driver packs the same fields as write<<31, fn<<28, block_mode<<27, inc<<26, addr<<9, len, ORed together. Its CMD52 calls always leave the RAW bit 0. `c-driver/cyw43_sdio.c:17-19` `c-driver/cyw43_sdio.c:24-27`

### CMD53 (IO_RW_EXTENDED) argument
| Bits | Field | Citations |
|---|---|---|
| 31 | write flag | `sdio-crate/src/sdio.rs:83-91` `sdio-crate/src/sdio.rs:121-129` `sdio-crate/src/sdio.rs:159-167` `sdio-crate/src/sdio.rs:206-214` |
| 30:28 | function | `sdio-crate/src/sdio.rs:83-91` `sdio-crate/src/sdio.rs:121-129` `sdio-crate/src/sdio.rs:159-167` `sdio-crate/src/sdio.rs:206-214` |
| 27 | block mode (0 = byte mode) | `sdio-crate/src/sdio.rs:83-91` `sdio-crate/src/sdio.rs:121-129` `sdio-crate/src/sdio.rs:159-167` `sdio-crate/src/sdio.rs:206-214` |
| 26 | OP code (1 = incrementing address) | `sdio-crate/src/sdio.rs:83-91` `sdio-crate/src/sdio.rs:121-129` `sdio-crate/src/sdio.rs:159-167` `sdio-crate/src/sdio.rs:206-214` |
| 25:9 | address (17 bits) | `sdio-crate/src/sdio.rs:83-91` `sdio-crate/src/sdio.rs:121-129` `sdio-crate/src/sdio.rs:159-167` `sdio-crate/src/sdio.rs:206-214` |
| 8:0 | count: bytes in byte mode, blocks in block mode; masked to 9 bits | `sdio-crate/src/sdio.rs:83-91` `sdio-crate/src/sdio.rs:121-129` `sdio-crate/src/sdio.rs:159-167` `sdio-crate/src/sdio.rs:206-214` |

- c-driver uses the same packing. `c-driver/cyw43_sdio.c:17-19`
- c-driver encodes a 512-byte byte-mode transfer as count 0. The crate masks buf.len() with 0x1FF, which gives the same result for 512. `c-driver/cyw43_sdio.c:43` `sdio-crate/src/sdio.rs:83-91`

### Splitting a buffer into CMD53 transfers
| Host | How a buffer becomes CMD53 transfers | Citations |
|---|---|---|
| embassy (sdio crate) | whole blocks in block mode, then the remainder (len % BLOCK_SIZE) in byte mode at address + block part; incrementing-address bit always set; BLOCK_SIZE = BACKPLANE_MAX_TRANSFER_SIZE = 64 | `sdio-crate/src/sdio.rs:671-699` `embassy/sdio.rs:27` `embassy/sdio.rs:152-166` `embassy/consts.rs:112` |
| c-driver | one CMD53 per transfer: byte mode when len <= 512 (length rounded up to CYW43_SDIO_CMD53_BYTE_MODE_DATA_ALIGN), otherwise block mode with the length rounded up to a multiple of 64; never a block part plus a byte remainder | `c-driver/cyw43_sdio.c:34-52` |

### CMD5 argument and reply

- Crate CMD5 argument: bit 24 = switch-to-1.8 V request, bits 23:15 = 9-bit voltage window. `sdio-crate/src/sdio.rs:19-30`
- From the R4 reply the crate reads the number of I/O functions from bits 30:28 of the OCR. `sdio-crate/src/sdio.rs:238-242`

### Card acquisition sequence

embassy's SDIO init first calls the crate's `reacquire(freq)`. `embassy/sdio.rs:172-181`

| Step | embassy (sdio crate) | c-driver | Citations |
|---|---|---|---|
| Clock limit | clamps the frequency to the host limit and to 50 MHz; puts the bus idle | not found in these sources; the SDIO host sits behind the port hooks | `sdio-crate/src/sdio.rs:406-494` `c-driver/cyw43_sdio.h:17-24` |
| Reset / inquiry | CMD5 with argument 0 (inquiry) | CMD0, then CMD5 with argument 0; errors ignored | `sdio-crate/src/sdio.rs:406-494` `c-driver/cyw43_ll.c:1643-1655` |
| Voltage negotiation | re-sends CMD5 with the voltage window from bits 23:15 of the inquiry reply (0x1FF if empty) until the card reports ready | none beyond the one CMD5 | `sdio-crate/src/sdio.rs:406-494` `c-driver/cyw43_ll.c:1643-1655` |
| Address and select | get-relative-address command, then select with the returned RCA | CMD3 to get the RCA, CMD7 to select | `sdio-crate/src/sdio.rs:406-494` `c-driver/cyw43_ll.c:1643-1655` |
| Bus width | reads CARD_CAP; writes the width into BUS_CTRL; 4-bit only if the host is 4-bit and the card is not a low-speed card without 4-bit support | later, in bus init, the driver writes (reg & ~3) or-ed with 2 to SDIOD_CCCR_BICTRL | `sdio-crate/src/sdio.rs:406-494` `c-driver/cyw43_ll.c:1681-1707` |
| Speed | host set to at most 25 MHz; if more was requested and HIGH_SPEED.SHS is set, writes EHS and raises the clock | after asserting bit 0 of SDIOD_CCCR_SPEED_CONTROL, sets bit 1; then calls the port hook cyw43_sdio_enable_high_speed_4bit() for the host controller | `sdio-crate/src/sdio.rs:406-494` `c-driver/cyw43_ll.c:1681-1707` |
| 1.8 V switch | not done | not found in these sources | `sdio-crate/src/sdio.rs:406-494` `c-driver/cyw43_ll.c:1643-1655` |

### Crate helpers embassy does not use

- The crate offers `enable_functions` (set bits in IO_ENABLE, then poll IO_READY every 2 ms with no timeout), `enable_interrupts` and `set_block_size`. `sdio-crate/src/sdio.rs:504-548`
- embassy's SDIO bring-up writes CCCR_IO_ENABLE, CCCR_INT_ENABLE and the block-size registers itself through read8/write8. `embassy/sdio.rs:188-228`

### SDIO interrupt wait

- For SDIO, embassy's `wait_for_event` delegates to the crate's `wait_for_event`, which delegates to the host bus implementation (not found in these sources). The result is ignored. `sdio-crate/src/sdio.rs:550-553` `embassy/sdio.rs:389-390`

## Wrapper registers (linux-headers/bcma/bcma_regs.h)

### Wrapper (agent) register offsets

linux adds these offsets to each core's wrapper base. `linux/brcmfmac/chip.c:271-275` `linux/brcmfmac/chip.c:359-381`

| Offset | linux name | Bits (linux) | Same number in other drivers | Citations |
|---|---|---|---|---|
| 1032 (0x0408) | `BCMA_IOCTL` | CLK 0x0001, FGC 0x0002; core-specific bits mask 0x3FFC | embassy AI_IOCTRL_OFFSET 0x408; c-driver AI_IOCTRL_OFFSET 0x408, SICF_CLOCK_EN 0x0001, SICF_FGC 0x0002 | `linux-headers/bcma/bcma_regs.h:27-43` `embassy/consts.rs:125-133` `c-driver/cyw43_ll.c:141-146` |
| 1280 (0x0500) | `BCMA_IOST` | | not found in these sources | `linux-headers/bcma/bcma_regs.h:27-43` |
| 2048 (0x0800) | `BCMA_RESET_CTL` | RESET 0x0001 | embassy AI_RESETCTRL_OFFSET 0x800; c-driver AI_RESETCTRL_OFFSET 0x800, AIRC_RESET 1 | `linux-headers/bcma/bcma_regs.h:27-43` `embassy/consts.rs:125-133` `c-driver/cyw43_ll.c:141-146` |
| 2052 (0x0804) | `BCMA_RESET_ST` | | embassy AI_RESETSTATUS_OFFSET 0x804 | `linux-headers/bcma/bcma_regs.h:27-43` `embassy/consts.rs:125-133` |

### Core-specific IOCTL-register bits linux adds
| linux name | Value | Same bit elsewhere | Citations |
|---|---|---|---|
| `ARMCR4_BCMA_IOCTL_CPUHALT` | 0x0020 | SICF_CPUHALT in c-driver and whd | `linux/brcmfmac/chip.c:78-82` `c-driver/cyw43_ll.c:142` `whd/src/include/whd_chip.h:37` |
| `D11_BCMA_IOCTL_PHYCLOCKEN` | 0x0004 | not found in these sources | `linux/brcmfmac/chip.c:78-82` |
| `D11_BCMA_IOCTL_PHYRESET` | 0x0008 | not found in these sources | `linux/brcmfmac/chip.c:78-82` |

### Where the wrapper base comes from
| Host | Source of the wrapper base | Citations |
|---|---|---|
| linux | not hard-coded: read from the chip's core-enumeration table (the slave-wrapper address descriptor, masked with 0xFFFFF000) while scanning cores; stored per core | `linux/brcmfmac/chip.c:897-899` `linux/brcmfmac/chip.c:950-955` `linux/brcmfmac/chip.c:517` |
| c-driver | fixed WRAPPER_REGISTER_OFFSET 0x100000 added to hard-coded core base addresses | `c-driver/cyw43_ll.c:119-124` |
| whd | same fixed WRAPPER_REGISTER_OFFSET 0x100000 | `whd/src/include/whd_chip_constants.h:27` |

### Shared clock-control/status register

- The header defines BCMA_CLKCTLST at core offset 480 (0x01E0), for ChipCommon rev >= 20, PCIe and 80211 cores. `linux-headers/bcma/bcma_regs.h:5-22`
- No linux file in these sources references BCMA_CLKCTLST. `linux-headers/bcma/bcma_regs.h:5-22`

| Bit name | Value | Citations |
|---|---|---|
| FORCEALP | 0x1 | `linux-headers/bcma/bcma_regs.h:5-22` |
| FORCEHT | 0x2 | `linux-headers/bcma/bcma_regs.h:5-22` |
| FORCEILP | 0x4 | `linux-headers/bcma/bcma_regs.h:5-22` |
| HAVEALPREQ | 0x8 | `linux-headers/bcma/bcma_regs.h:5-22` |
| HAVEHTREQ | 0x10 | `linux-headers/bcma/bcma_regs.h:5-22` |
| HWCROFF | 0x20 | `linux-headers/bcma/bcma_regs.h:5-22` |
| HAVEALP | 0x10000 | `linux-headers/bcma/bcma_regs.h:5-22` |
| HAVEHT | 0x20000 | `linux-headers/bcma/bcma_regs.h:5-22` |
| BP_ON_ALP | 0x40000 | `linux-headers/bcma/bcma_regs.h:5-22` |
| BP_ON_HT | 0x80000 | `linux-headers/bcma/bcma_regs.h:5-22` |

## Core identifiers (linux-headers/bcma/bcma.h)

### Core ids linux uses on the SDIO path

linux uses these ids at `linux/brcmfmac/chip.c:538-548` and `linux/brcmfmac/sdio.c:3997-4002`.

| Core | Id | Citations |
|---|---|---|
| CHIPCOMMON | 0x800 | `linux-headers/bcma/bcma.h:97` |
| INTERNAL_MEM (SOCRAM) | 0x80E | `linux-headers/bcma/bcma.h:111` |
| 80211 | 0x812 | `linux-headers/bcma/bcma.h:115` |
| PMU | 0x827 | `linux-headers/bcma/bcma.h:136` |
| SDIO_DEV | 0x829 | `linux-headers/bcma/bcma.h:138-139` |
| ARM_CM3 | 0x82A | `linux-headers/bcma/bcma.h:138-139` |
| ARM_CR4 | 0x83E | `linux-headers/bcma/bcma.h:155-156` |
| GCI | 0x840 | `linux-headers/bcma/bcma.h:155-156` |
| ARM_CA7 | 0x847 | `linux-headers/bcma/bcma.h:158-159` |
| SYS_MEM | 0x849 | `linux-headers/bcma/bcma.h:158-159` |

- Each core's register space is BCMA_CORE_SIZE = 0x1000 bytes. `linux-headers/bcma/bcma.h:163`
- Manufacturer ids: ARM 0x43B, MIPS 0x4A7, BCM 0x4BF. `linux-headers/bcma/bcma.h:62-64`

### Which cores linux touches for a 43439

- linux treats 43430 and 43439 alike on the Cortex-M3 path. `linux/brcmfmac/chip.c:1281-1302`
- Making the chip passive: linux disables the ARM_CM3 core with brcmf_chip_coredisable(core, 0, 0), which puts it in reset. The CPUHALT bit of the wrapper IOCTL register is used only on the CR4/CA7 path. `linux/brcmfmac/chip.c:1068-1092` `linux/brcmfmac/chip.c:1281-1302`
- It then resets the 80211 core with pre-reset bits PHYRESET and PHYCLOCKEN, reset bits PHYCLOCKEN, post-reset bits PHYCLOCKEN. `linux/brcmfmac/chip.c:1281-1302`
- It then resets the INTERNAL_MEM core and, only for these two chip ids, writes 3 to the SOCRAM bank-index register and 0 to the bank-PDA register ("disable bank #3 remap"). `linux/brcmfmac/chip.c:1281-1302`
- Activating: linux checks INTERNAL_MEM is up, calls the bus activate hook, and resets ARM_CM3 with all-zero IOCTL-register bits. `linux/brcmfmac/chip.c:1304-1320`
- linux assumes 64 KiB of save/restore RAM for these chips. `linux/brcmfmac/chip.c:644-649`
- linux tests save/restore capability by reading chipcommon sr_control1 != 0. `linux/brcmfmac/chip.c:1457-1461`
- c-driver names the same two SOCRAM registers SOCSRAM_BANKX_INDEX (+0x10) and SOCSRAM_BANKX_PDA (+0x44), and the same chipcommon register CHIPCOMMON_SR_CONTROL1 (+0x508). `c-driver/cyw43_ll.c:128-134`
- linux reaches the two SOCRAM registers as SOCRAMREGOFFS(bankidx) and SOCRAMREGOFFS(bankpda); in struct sbsocramregs these fields sit at offsets 0x10 and 0x44 (computed), the same numbers as the c-driver's. `linux/brcmfmac/chip.c:165-202` `linux/brcmfmac/chip.c:1281-1302`

## Chipcommon bits (linux-headers/bcma/bcma_driver_chipcommon.h)

| linux name | Value | Use in linux | Citations |
|---|---|---|---|
| `BCMA_CC_CAP_EXT_AOB_PRESENT` | 0x40 | with chipcommon rev >= 35, decides that the PMU is a separate core | `linux-headers/bcma/bcma_driver_chipcommon.h:226` `linux/brcmfmac/chip.c:1245-1246` |
| `BCMA_CC_PMU_CTL_RES_RELOAD` | 0x2 | shifted left by `BCMA_CC_PMU_CTL_RES_SHIFT` = 13 and ORed into the PMU control register by the SDIO bus code | `linux-headers/bcma/bcma_driver_chipcommon.h:328-329` `linux/brcmfmac/sdio.c:4068` |
| `BCMA_CC_SROM_CONTROL_OTPSEL` | 0x10 | PCIe path only | `linux-headers/bcma/bcma_driver_chipcommon.h:273-274` `linux/brcmfmac/pcie.c:2107` |
| `BCMA_CC_SROM_CONTROL_OTP_PRESENT` | 0x20 | PCIe path only | `linux-headers/bcma/bcma_driver_chipcommon.h:273-274` `linux/brcmfmac/pcie.c:2098` |

## Length constants behind linux record sizes (linux-headers/ieee80211.h)

| Constant | Value | Citations |
|---|---|---|
| `IEEE80211_MAX_SSID_LEN` | 32 | `linux-headers/ieee80211.h:227` |
| `WLAN_MAX_KEY_LEN` | 32 | `linux-headers/ieee80211.h:2267` |
| `WLAN_PMKID_LEN` | 16 | `linux-headers/ieee80211.h:2270-2274` |
| `WLAN_PMK_NAME_LEN` | 16 | `linux-headers/ieee80211.h:2270-2274` |
| `WLAN_PMK_LEN` | 32 | `linux-headers/ieee80211.h:2270-2274` |
| `WLAN_PMK_LEN_SUITE_B_192` | 48 | `linux-headers/ieee80211.h:2270-2274` |
| WEP40 key length | 5 | `linux-headers/ieee80211.h:1900-1904` |
| WEP104 key length | 13 | `linux-headers/ieee80211.h:1900-1904` |
| CCMP key length | 16 | `linux-headers/ieee80211.h:1900-1904` |
| TKIP key length | 32 | `linux-headers/ieee80211.h:1900-1904` |

- ETH_ALEN and IFNAMSIZ are used but not defined in this header, and are not defined anywhere in these sources. `linux-headers/ieee80211.h:301`

## Country table (embassy/countries.rs)

- The table is a list of 237 constants of type `Country { code: [u8; 2], rev: u16 }`. Rev 0 means "the CLM's default". Almost all entries have rev 0. `embassy/countries.rs:4-12` `embassy/countries.rs:15`
- Of the 237 constants, 7 have a non-zero rev (the seven non-zero rows below). `embassy/countries.rs:87` `embassy/countries.rs:171` `embassy/countries.rs:235` `embassy/countries.rs:449` `embassy/countries.rs:451` `embassy/countries.rs:477` `embassy/countries.rs:481`
- Codes that are not two letters A-Z: 0A, 0B, 0C, E0, Q1, Q2. XX and XV are letters but not assigned ISO codes (recalled, not in these sources). `embassy/countries.rs:45` `embassy/countries.rs:171` `embassy/countries.rs:237` `embassy/countries.rs:451` `embassy/countries.rs:453` `embassy/countries.rs:473`

| embassy constant | Code | Rev | Citations |
|---|---|---|---|
| `BAKER_ISLAND` | 0B | 0 | `embassy/countries.rs:45` |
| `CANADA_REV950` | CA | 950 | `embassy/countries.rs:87` |
| `EUROPEAN_WIDE_REV895` | E0 | 895 | `embassy/countries.rs:171` |
| `KOREA_REPUBLIC_OF` | KR | 1 | `embassy/countries.rs:235` |
| `KOSOVO` | 0A | 0 | `embassy/countries.rs:237` |
| `UNITED_STATES_REV4` | US | 4 | `embassy/countries.rs:449` |
| `UNITED_STATES_REV931` | Q1 | 931 | `embassy/countries.rs:451` |
| `UNITED_STATES_NO_DFS` | Q2 | 0 | `embassy/countries.rs:453` |
| `WEST_BANK` | 0C | 0 | `embassy/countries.rs:473` |
| `WORLD_WIDE_XV_REV983` | XV | 983 | `embassy/countries.rs:477` |
| `WORLD_WIDE_XX` | XX | 0 | `embassy/countries.rs:479` |
| `WORLD_WIDE_XX_REV17` | XX | 17 | `embassy/countries.rs:481` |

| Aspect | embassy | c-driver | Citations |
|---|---|---|---|
| Table revisions | non-zero for seven entries above | rev 0 for every country, including South Korea and USA | `embassy/countries.rs:235` `embassy/countries.rs:449` `c-driver/cyw43_country.h:34-87` `c-driver/cyw43_country.h:78` `c-driver/cyw43_country.h:86` |
| Table entry encoding | struct of 2 code bytes and a u16 rev | one word: char0, char1 << 8, rev << 16, ORed together | `embassy/countries.rs:4-12` `c-driver/cyw43_country.h:24` |
| What is sent | named variable (iovar) `country` with a 12-byte CountryInfo: abbreviation = two letters + two zero bytes; rev = -1 when the table rev is 0, else the rev; country code = two letters + two zero bytes | same three fields and the same -1 for rev 0 | `embassy/control.rs:278-287` `embassy/structs.rs:390-395` `c-driver/cyw43_ll.c:2005-2022` |
| Default / substitution | default WORLD_WIDE_XX | on SDIO builds silently replaces worldwide (XX rev 0) by XX rev 17 ("for the 1DX CLM"; comment claims about 25% more throughput on PYBD) | `embassy/control.rs:58-67` `c-driver/cyw43_ll.c:2005-2022` |
| Delay afterwards | waits 100 ms ("next ioctls fail if we don't wait") | waits 50 ms after the command; its comment says setting the country takes about 32 ms | `embassy/control.rs:284-287` `c-driver/cyw43_ll.c:2013-2024` |

## SDIO port contract (c-driver/cyw43_sdio.h)

A port using the c-driver over SDIO must provide seven functions. `c-driver/cyw43_sdio.h:17-24`

| Hook | Purpose / when the c-driver calls it | Citations |
|---|---|---|
| `cyw43_sdio_init` | called after the WL_REG_ON pulse and before bus init | `c-driver/cyw43_sdio.h:17-24` `c-driver/cyw43_ctrl.c:146-150` |
| `cyw43_sdio_reinit` | called from the ensure-awake callback, in SDIO builds without USE_SDIOIT | `c-driver/cyw43_sdio.h:17-24` `c-driver/cyw43_ctrl.c:268-274` |
| `cyw43_sdio_deinit` | called when the bus is put to sleep in SDIO builds without USE_SDIOIT ("save power while WLAN bus sleeps") and at driver deinit in every SDIO build | `c-driver/cyw43_sdio.h:17-24` `c-driver/cyw43_ctrl.c:234-243` `c-driver/cyw43_ctrl.c:105-111` |
| `cyw43_sdio_set_irq(bool)` | only when USE_SDIOIT is set: called with true once the driver is up and again after each poll, and with false at driver deinit | `c-driver/cyw43_sdio.h:17-24` `c-driver/cyw43_ctrl.c:177-178` `c-driver/cyw43_ctrl.c:241-243` `c-driver/cyw43_ctrl.c:106-108` |
| `cyw43_sdio_enable_high_speed_4bit` | called once during bus init | `c-driver/cyw43_sdio.h:17-24` `c-driver/cyw43_ll.c:1707` |
| `cyw43_sdio_transfer(cmd, arg, *resp)` | command-only transactions: CMD0, CMD5, CMD3, CMD7 and every CMD52 | `c-driver/cyw43_sdio.h:17-24` `c-driver/cyw43_ll.c:1643-1655` `c-driver/cyw43_sdio.c:24-27` |
| `cyw43_sdio_transfer_cmd53(block_size, arg, len, buf)` | data transactions | `c-driver/cyw43_sdio.h:17-24` |

## Counters (c-driver/cyw43_stats.h)

- With CYW43_USE_STATS the c-driver keeps these counters, in enum order: F1_RESYNC, BUS_ERROR, SDIO_INT_CLEAR, SPI_INT_CLEAR, SPI_PACKET_AVAILABLE, SLEEP_COUNT, WAKE_COUNT, LWIP_RUN_COUNT, CYW43_RUN_COUNT, PENDSV_RUN_COUNT, PENDSV_DISABLED_COUNT, IRQ_COUNT, PACKET_IN_COUNT, PACKET_OUT_COUNT, LONGEST_IOCTL_TIME. `c-driver/cyw43_stats.h:19-44`
- LONGEST_IOCTL_TIME records the longest observed command round-trip in microseconds. `c-driver/cyw43_ll.c:1305-1309`
- The c-driver asserts that BUS_ERROR stays below 100. `c-driver/cyw43_ll.c:1162-1164`

## Network-stack glue for lwIP (c-driver/cyw43_lwip.c)

### Transmit hand-off

- The netif link-output function derives the interface number from the second character of the netif name ("w0" = station, "w1" = AP). `c-driver/cyw43_lwip.c:62-77` `c-driver/cyw43_lwip.c:169-171`
- It calls cyw43_send_ethernet(self, itf, p->tot_len, p, true) with the pbuf chain itself. A non-zero return is reported to the stack as ERR_IF. `c-driver/cyw43_lwip.c:62-77`
- MTU is fixed at 1500. `c-driver/cyw43_lwip.c:115`

### Receive hand-off
| Host | How a received Ethernet frame reaches the network stack | Citations |
|---|---|---|
| c-driver + lwIP | delivered through cyw43_cb_process_ethernet(cb_data, itf, len, buf); dropped unless the netif has its link-up flag set; otherwise copied into a newly allocated pool pbuf and passed to netif->input; the driver's receive buffer is not handed over | `c-driver/cyw43_lwip.c:247-265` |
| whd | passes ownership of its own packet buffer to the stack, with the buffer's current pointer at the Ethernet header; the stack must release it | `whd/src/whd_network_if.c:45-85` |

### Link state and status

- Link up/down callbacks set or clear the lwIP netif link flag and do nothing else. `c-driver/cyw43_lwip.c:267-299`
- cyw43_tcpip_link_status returns CYW43_LINK_UP when the netif is up, link-up and has an address (IPv4 non-zero, or a preferred global IPv6 address in IPv6-only builds). `c-driver/cyw43_lwip.c:267-299`
- It returns CYW43_LINK_NOIP when up but without an address; otherwise it falls back to the Wi-Fi level cyw43_wifi_link_status. `c-driver/cyw43_lwip.c:267-299`

### Multicast filter maintenance

- IGMP group joins and leaves become the MAC 01:00:5e + low 23 bits of the group address, passed to cyw43_wifi_update_multicast_filter(add/remove). `c-driver/cyw43_lwip.c:79-108`
- IPv6 MLD uses 33:33 + the last four address bytes. `c-driver/cyw43_lwip.c:79-108`
- The all-nodes link-local group is added when the station netif is created. `c-driver/cyw43_lwip.c:204-208`

### Interface bring-up and teardown

- cyw43_cb_tcpip_init adds the netif, reads the MAC with cyw43_wifi_get_mac, sets the netif default and up, and for the station interface starts DHCP. `c-driver/cyw43_lwip.c:110-128` `c-driver/cyw43_lwip.c:143-219`
- The AP interface starts the bundled DHCP server only when CYW43_NETUTILS is set. `c-driver/cyw43_lwip.c:143-219`
- cyw43_cb_tcpip_deinit stops DHCP, removes the netif and clears its address and flags. `c-driver/cyw43_lwip.c:221-245`
- Both interfaces are torn down at every driver power-up and at deinit. `c-driver/cyw43_ctrl.c:101-103` `c-driver/cyw43_ctrl.c:135-138`

## Power sequencing and GPIO wrapper (c-driver/cyw43_ctrl.c)

### Power pin setup, power-up and power-down

- cyw43_init configures the host-wake (or IRQ) pin as input without pull, WL_REG_ON as output driven low, and an optional RF-switch supply pin low. It resets all driver state (AP channel default 3). `c-driver/cyw43_ctrl.c:60-92`
- Power-up (cyw43_ensure_up, on first use): tear down both netifs, WL_REG_ON low 20 ms, high, wait 50 ms, SDIO init (SDIO builds), bus init, then enable polling/IRQ. `c-driver/cyw43_ctrl.c:124-191`
- cyw43_deinit: remove both netifs, disable the SDIO IRQ and deinit SDIO, cyw43_ll_deinit (SPI deinit only), then call cyw43_init again "to make sure all state is reset". That call drives WL_REG_ON low. `c-driver/cyw43_ctrl.c:94-122` `c-driver/cyw43_ll.c:297-304`
- What the source shows being reset is host-side state listed in cyw43_init: interface state, scan/join state, pending flags, AP settings, the poll hook. Nothing in these files says what the chip retains. `c-driver/cyw43_ctrl.c:60-92`

| Host | Power-cycle handling | Citations |
|---|---|---|
| c-driver | as above; has an explicit deinit that ends with WL_REG_ON low | `c-driver/cyw43_ctrl.c:94-122` `c-driver/cyw43_ctrl.c:124-191` |
| embassy | on (re)init resets its cached backplane window to 0xAAAAAAAA and status to 0 ("device loses both on reset"); pulses power 20 ms low, then waits 250 ms; no power-down routine found in spi.rs | `embassy/spi.rs:177-187` |

### GPIO wrapper

- cyw43_gpio_set exists only when CYW43_GPIO is enabled. It takes the driver lock, powers the chip up if needed (cyw43_ensure_up), then calls cyw43_ll_gpio_set(gpio, val). The first GPIO write can therefore trigger the whole chip bring-up. `c-driver/cyw43_ctrl.c:787-799`

## Chip record and bus callbacks (linux/brcmfmac/chip.h)

- Per chip, linux keeps: chip id, chip revision, enumeration-space base, chipcommon capabilities and extended capabilities, PMU capabilities and revision, RAM base (ARM CR4 chips only), RAM size including retention, retention (save/restore) RAM size, and a 12-character name. `linux/brcmfmac/chip.h:13-53`
- Per core, linux keeps: 16-bit id, 16-bit revision, register base. `linux/brcmfmac/chip.h:13-53`
- Chip bring-up is bus-independent and needs six callbacks from the bus: read32(addr), write32(addr, value), prepare ("prepare bus for core configuration"), reset, setup ("bus-specific core setup") and activate(chip, rstvec) (the bus should use rstvec when non-zero). `linux/brcmfmac/chip.h:55-72`
- Chipcommon registers are addressed as base + offsetof(struct chipcregs, field). `linux/brcmfmac/chip.h:10-11`

## Feature detection (linux/brcmfmac/feature.h and feature.c)

### Feature and quirk list

- Feature flags (bit = enum position): MBSS, MCHAN, PNO, WOWL, P2P, RSDB, TDLS, SCAN_RANDOM_MAC, WOWL_ND, WOWL_GTK, WOWL_ARP_ND, MFP, GSCAN, FWSUP, MONITOR, MONITOR_FLAG, MONITOR_FMT_RADIOTAP, MONITOR_FMT_HW_RX_HDR, DOT11H, SAE, FWAUTH, DUMP_OBSS, SCAN_V2, PMKID_V2, PMKID_V3, SAE_EXT, FBT, OKC. `linux/brcmfmac/feature.h:36-74`
- Quirks: AUTO_AUTH, NEED_MPC. `linux/brcmfmac/feature.h:76-96`

### Capability string to feature mapping (linux and whd)

Both linux and whd read the named variable `cap` into a 768-byte buffer and set a flag when a substring is found. linux uses strnstr; whd uses strstr. `linux/brcmfmac/feature.c:229-253` `whd/src/whd_chip.c:60` `whd/src/whd_chip.c:998-1020`

| Searched string | linux feature | whd flag (bit = 1 << id) | Citations |
|---|---|---|---|
| "mbss" | MBSS | not in whd's table | `linux/brcmfmac/feature.c:37-50` `whd/src/whd_chip.c:87-94` |
| "mchan" | MCHAN | not in whd's table | `linux/brcmfmac/feature.c:37-50` `whd/src/whd_chip.c:87-94` |
| "p2p" | P2P | not in whd's table | `linux/brcmfmac/feature.c:37-50` `whd/src/whd_chip.c:87-94` |
| "monitor" | MONITOR | not in whd's table | `linux/brcmfmac/feature.c:37-50` `whd/src/whd_chip.c:87-94` |
| "rtap" | MONITOR_FLAG and MONITOR_FMT_RADIOTAP | not in whd's table | `linux/brcmfmac/feature.c:37-50` `whd/src/whd_chip.c:87-94` |
| "802.11h" | DOT11H | not in whd's table | `linux/brcmfmac/feature.c:37-50` `whd/src/whd_chip.c:87-94` |
| "sae " (trailing space) | SAE | WHD_FWCAP_SAE (id 0) | `linux/brcmfmac/feature.c:37-50` `whd/src/whd_chip.c:87-94` `whd/inc/whd_types.h:528-532` |
| "idauth" | FWAUTH | not in whd's table | `linux/brcmfmac/feature.c:37-50` `whd/src/whd_chip.c:87-94` |
| "sae_ext" (linux, no trailing space) / "sae_ext " (whd, trailing space) | SAE_EXT | WHD_FWCAP_SAE_EXT (id 1) | `linux/brcmfmac/feature.c:37-50` `whd/src/whd_chip.c:87-94` `whd/inc/whd_types.h:528-532` |
| "fbt " (trailing space) | FBT | not in whd's table | `linux/brcmfmac/feature.c:37-50` `whd/src/whd_chip.c:87-94` |
| "okc" | OKC | not in whd's table | `linux/brcmfmac/feature.c:37-50` `whd/src/whd_chip.c:87-94` |
| "offloads " (trailing space) | not in linux's table | WHD_FWCAP_OFFLOADS (id 2) | `linux/brcmfmac/feature.c:37-50` `whd/src/whd_chip.c:87-94` `whd/inc/whd_types.h:528-532` |
| "gcmp " (trailing space) | not in linux's table | WHD_FWCAP_GCMP (id 3) | `linux/brcmfmac/feature.c:37-50` `whd/src/whd_chip.c:87-94` `whd/inc/whd_types.h:528-532` |
| "icmp " (trailing space) | not in linux's table | WHD_FWCAP_ICMP (id 4) | `linux/brcmfmac/feature.c:37-50` `whd/src/whd_chip.c:87-94` `whd/inc/whd_types.h:528-532` |

- In linux the trailing spaces in "sae " and "fbt " are part of the searched strings; linux thereby distinguishes "sae " from "sae_ext". `linux/brcmfmac/feature.c:37-50`
- In whd every searched name carries a trailing space. `whd/src/whd_chip.c:87-94`
- whd_fwcap_t is `{ whd_fwcap_id_t feature; const char *const fwcap_name; }`; the bits go into chip_info.fwcap_flags. `whd/src/include/whd_chip.h:128-132` `whd/src/whd_chip.c:998-1020`
- whd later tests these bits before using SAE (join and AP paths), GCMP, offload configuration and ICMP offload. `whd/src/whd_ap.c:471` `whd/src/whd_wifi_api.c:1867` `whd/src/whd_wifi_api.c:1768` `whd/src/whd_management.c:535` `whd/src/whd_ap.c:739` `whd/src/whd_wifi_api.c:6917`

### Features linux probes by trying a named variable

linux treats any result other than firmware error -23 (BRCMF_FW_UNSUPPORTED) as "supported". `linux/brcmfmac/feature.c:20` `linux/brcmfmac/feature.c:187-206`

| Probe | Feature set | Citations |
|---|---|---|
| get `pfn` | PNO | `linux/brcmfmac/feature.c:308-344` |
| get `wowl` (only if the bus supports wake) | WOWL | `linux/brcmfmac/feature.c:308-344` |
| get `rsdb_mode` | RSDB | `linux/brcmfmac/feature.c:308-344` |
| get `tdls_enable` | TDLS | `linux/brcmfmac/feature.c:308-344` |
| get `mfp` | MFP | `linux/brcmfmac/feature.c:308-344` |
| get `dump_obss` | DUMP_OBSS | `linux/brcmfmac/feature.c:308-344` |
| get `sup_wpa` | FWSUP | `linux/brcmfmac/feature.c:308-344` |
| get `scan_ver` | SCAN_V2 | `linux/brcmfmac/feature.c:308-344` |
| get `pfn_macaddr` succeeds | SCAN_RANDOM_MAC | `linux/brcmfmac/feature.c:308-344` |
| get `wowl_cap` (only when WOWL was set) succeeds | WOWL_ARP_ND; plus WOWL_ND when the reply has BRCMF_WOWL_PFN_FOUND, and WOWL_GTK when it has BRCMF_WOWL_GTK_FAILURE | `linux/brcmfmac/feature.c:311-322` |

### 43439-specific handling

- linux skips the GSCAN probe (set `pfn_gscan_cfg`) for chip ids 43430, 4345, 43454 and 43439. `linux/brcmfmac/feature.c:299-307`
- No other 43439-specific feature or quirk is applied in this file: MBSS is cleared only for 4330 and 43362; quirks exist only for 43236 and 4329. `linux/brcmfmac/feature.c:323-331` `linux/brcmfmac/feature.c:358-369`

### Version-based features and ordering

- linux sets PMKID_V2 when the `wlc_ver` reply reports major.minor >= 12.0 and PMKID_V3 when >= 13.0. `linux/brcmfmac/feature.c:139-178`
- linux has a table of four firmware version strings that force MONITOR or MONITOR_FMT_HW_RX_HDR. `linux/brcmfmac/feature.c:98-107`
- Order in brcmf_feat_attach: cap string, GSCAN probe, named-variable probes, wlc_ver overrides, firmware-id overrides, vendor hook, then the user's feature_disable mask is cleared from the result, then chip quirks. `linux/brcmfmac/feature.c:291-356`

## Tagged container xtlv (linux/brcmfmac/xtlv.c)

- Nominal record: u16 id, u16 len, then data; id and len little-endian. `linux/brcmfmac/xtlv.h:11-25` `linux/brcmfmac/xtlv.c:37-83`
- Option ALIGN32 (bit 0) rounds header + data up to a multiple of 4 when sizing. `linux/brcmfmac/xtlv.h:11-25` `linux/brcmfmac/xtlv.c:14-35`
- Option IDU8 (bit 1) shrinks the id to one byte. Option LENU8 (bit 2) shrinks the length to one byte (len must be <= 0xFF). Header size is therefore 4, 3 or 2 bytes. `linux/brcmfmac/xtlv.h:11-25` `linux/brcmfmac/xtlv.c:14-35`
- linux brcmf_fil_xtlv_data_set builds the NUL-terminated variable name immediately followed by one xtlv record (16-bit id, 16-bit len, data) sized with ALIGN32, and sends it with BRCMF_C_SET_VAR. `linux/brcmfmac/fwil.c:355-373` `linux/brcmfmac/fwil.c:375-402`
- Padding bytes added by the rounding are counted in the command length but not written by the packer. `linux/brcmfmac/fwil.c:355-373`

## Firmware vendor variants (linux/brcmfmac/fwvid.c)

- linux has three firmware-vendor variants: WCC, CYW and BCA (modules brcmfmac-wcc, -cyw, -bca). `linux/brcmfmac/fwvid.c:53-57` `linux/brcmfmac/bus.h:35-41`
- The variant is fixed per device-table entry and copied into the bus record at probe; brcmf_fwvid_attach installs that variant's hook table. `linux/brcmfmac/fwvid.c:60-84` `linux/brcmfmac/fwvid.c:153-176` `linux/brcmfmac/bcmsdh.c:1089`
- The linux SDIO device table has two 43439 entries. SDIO_DEVICE_ID_BROADCOM_43439 (Broadcom vendor id) is tagged WCC. SDIO_DEVICE_ID_BROADCOM_CYPRESS_43439 (Cypress vendor id) is tagged CYW. `linux/brcmfmac/bcmsdh.c:967-977` `linux/brcmfmac/bcmsdh.c:993` `linux/brcmfmac/bcmsdh.c:1004`
- Whether the "cyw" hooks apply in linux therefore depends on the SDIO vendor id the card reports. The numeric vendor and device ids are not defined in these sources. `linux/brcmfmac/bcmsdh.c:967-977`

## Firmware files and NVRAM parser (linux/brcmfmac/firmware.h and firmware.c)

### Firmware name mapping

- linux maps (chip id, revision bit mask) to a firmware base name under "brcm/". BRCMF_FW_CLM_DEF declares both "<base>.bin" and "<base>.clm_blob". `linux/brcmfmac/firmware.h:8-14` `linux/brcmfmac/firmware.h:26-45`
- For chip id 43439 the SDIO table uses revision mask 0xFFFFFFFF (all revisions) and base name "brcmfmac43439-sdio". `linux/brcmfmac/sdio.c:619` `linux/brcmfmac/sdio.c:662`
- A request holds a list of items, each either a binary or an NVRAM blob (data + length), with an OPTIONAL flag (0x0001), plus up to 8 board-type strings. Path names are limited to 320 characters. `linux/brcmfmac/firmware.h:8-14` `linux/brcmfmac/firmware.h:49-73`

### NVRAM text parser

- linux turns the NVRAM text file into the blob it downloads with a five-state parser: IDLE, KEY, VALUE, COMMENT, END. `linux/brcmfmac/firmware.c:20-33`
- Accepted characters are 0x20-0x7E except "#". `linux/brcmfmac/firmware.c:74-87`
- "#" and newline start a comment or skip to end of line. A key ends at "=". A key containing a space or an invalid character discards the line. `linux/brcmfmac/firmware.c:89-143`
- Keys starting "RAW1" are discarded. "macaddr" is discarded when the platform supplies a MAC. `linux/brcmfmac/firmware.c:89-143`
- Each "key=value" is copied followed by one NUL. `linux/brcmfmac/firmware.c:145-193`
- Parsing stops when the output would reach 64000 bytes (BRCMF_FW_MAX_NVRAM_SIZE). `linux/brcmfmac/firmware.c:20-33` `linux/brcmfmac/firmware.c:145-193` `linux/brcmfmac/firmware.c:400-452`
- Afterwards, if no "boardrev" key was seen, "boardrev=0xff" + NUL is appended; a platform MAC is appended as a macaddr entry. `linux/brcmfmac/firmware.c:373-384` `linux/brcmfmac/firmware.c:400-452`
- The buffer is NUL-padded to roundup(len + 1, 4). `linux/brcmfmac/firmware.c:400-452`
- A 4-byte little-endian token is appended: low 16 bits = padded length in 32-bit words, high 16 bits = bitwise complement of that word count. token = (~words << 16) OR (words & 0xFFFF). The returned length includes the token. `linux/brcmfmac/firmware.c:400-452`
- Keys beginning "devpath" or "pcie/" select the PCIe multi-device stripping paths, which do not apply to an SDIO device. `linux/brcmfmac/firmware.c:89-143`
- embassy and c-driver each write their own NVRAM length word; see `NVRAM length word (hand-built)` in the embassy and c-driver records chapters. `embassy/runner.rs:567-570` `c-driver/cyw43_ll.c:1798-1802`

## P2P bsscfg roles (linux/brcmfmac/p2p.h)

- linux P2P code indexes bss configurations as PRIMARY (0), DEVICE (P2P discovery, 1), CONNECTION (2), CONNECTION2 (3). Host-side bookkeeping only; no wire layout is defined in this header. `linux/brcmfmac/p2p.h:13-27`

## Transmit queue discipline (linux/brcmutil/utils.c)

- linux's packet queue is an array of per-precedence lists. brcmu_pktq_mdeq dequeues from the highest non-empty precedence whose bit is set in the caller's precedence bitmap, and returns NULL if none qualifies. `linux/brcmutil/utils.c:218-250`
- This is the primitive the linux SDIO transmit path and firmware-signalling code use to pick the next frame. `linux/brcmutil/utils.c:218-250` `linux/brcmfmac/sdio.c:2358` `linux/brcmfmac/fwsignal.c:1352`

## TRX image header (whd/src/bus_protocols/whd_trxhdr.h)

Size 32 bytes (TRXV5_SIZE 32; TRXV4_SIZE 692). `whd/src/bus_protocols/whd_trxhdr.h:29-43`

| Offset | Size | Field | Notes | Citations |
|---|---|---|---|---|
| 0 | 4 | `magic` | 0x30524448 ("HDR0") | `whd/src/bus_protocols/whd_trxhdr.h:29-43` |
| 4 | 4 | `len` | length of file including header | `whd/src/bus_protocols/whd_trxhdr.h:29-43` |
| 8 | 4 | `crc32` | CRC from flag_version to end of file | `whd/src/bus_protocols/whd_trxhdr.h:29-43` |
| 12 | 4 | `flag_version` | bits 0:15 flags, 16:31 version | `whd/src/bus_protocols/whd_trxhdr.h:29-43` |
| 16 | 16 | `offsets[4]` | four u32 | `whd/src/bus_protocols/whd_trxhdr.h:29-43` |

- In whd's SDIO download code the header is examined only inside `#ifdef BLHS_SUPPORT`: first block of the firmware resource, magic compared with TRX_MAGIC. `whd/src/bus_protocols/whd_bus_sdio_protocol.c:2031-2041`
- The only other user in these sources is the OCI bus file. `whd/src/bus_protocols/COMPONENT_WIFI_INTERFACE_OCI/whd_bus_oci_protocol.c:687-689`
- Whether a 43439 whd build defines BLHS_SUPPORT is not stated in these files. `whd/src/bus_protocols/whd_bus_sdio_protocol.c:2031-2041`

## Backplane transfer and firmware write (whd/src/bus_protocols/whd_bus_common.h and whd_bus_common.c)

### Timeouts and download stages

- WHD_BACKPLAIN_BUF_TIMEOUT = 0xFFFFFFFF (wait forever for a backplane transfer buffer). WHD_RX_BUF_TIMEOUT = 10. `whd/src/bus_protocols/whd_bus_common.h:28-42`
- The boot-loader-handshake stage enum is CHK_BL_INIT, PREP_FW_DOWNLOAD, POST_FW_DOWNLOAD, CHK_FW_VALIDATION, (PREP_NVRAM_DOWNLOAD on one chip variant), POST_NVRAM_DOWNLOAD, POST_WATCHDOG_RESET. `whd/src/bus_protocols/whd_bus_common.h:28-42`

### Backplane block transfer

- whd_bus_transfer_backplane_bytes gets one host buffer of (bus max transfer size + backplane read padding + MAX_BUS_HEADER_SIZE) bytes, waiting forever. `whd/src/bus_protocols/whd_bus_common.c:332-428` `whd/src/bus_protocols/whd_bus_common.h:28`
- It loops. Each chunk is limited to the bus max transfer size. If (address & 0x7FFF) + chunk would exceed 0x7FFF, the chunk is limited to 0x8000 - (address & 0x7FFF), so no chunk crosses a backplane window (BACKPLANE_ADDRESS_MASK 0x7FFF, BACKPLANE_WINDOW_SIZE = mask + 1). `whd/src/bus_protocols/whd_bus_common.c:332-428` `whd/src/bus_protocols/whd_chip_reg.h:81-82`
- The boundary test as written, (offset + size) > 0x7FFF, also "trims" a chunk that ends exactly at the window end by zero bytes; harmless. `whd/src/bus_protocols/whd_bus_common.c:332-428`
- Per chunk whd sets the window for the chunk address (CDC/BDC builds) and transfers on the backplane function at address & 0x7FFF. `whd/src/bus_protocols/whd_bus_common.c:332-428`
- For reads whd requests chunk + read-padding bytes and copies from data + padding. `whd/src/bus_protocols/whd_bus_common.c:332-428`
- On exit, success or failure, whd sets the window back to CHIPCOMMON_BASE_ADDRESS and releases the buffer. `whd/src/bus_protocols/whd_bus_common.c:332-428`
- The numeric bus max transfer size is bus-specific and not in this file. `whd/src/bus_protocols/whd_bus_common.c:332-428`

### Firmware write

- whd_bus_write_wifi_firmware_image takes the RAM start address from the per-chip ATCM_RAM_BASE_ADDRESS variable (comment: CR4 chips have an offset, CM3 starts from 0). `whd/src/bus_protocols/whd_bus_common.c:237-306`
- It asks the resource layer for the firmware size (zero size is WHD_BADARG) and calls whd_bus_download_resource(FIRMWARE, start, size). `whd/src/bus_protocols/whd_bus_common.c:237-306`
- The boot-loader-handshake calls around it exist only under BLHS_SUPPORT. `whd/src/bus_protocols/whd_bus_common.c:237-306`

## Resource access contract (whd/inc/whd_resource_api.h)

- whd obtains firmware, NVRAM and CLM through five host callbacks: resource size, resource block size, number of blocks, get block n (pointer + size), and a random-access read(offset, size). `whd/inc/whd_resource_api.h:35-50` `whd/src/whd_resource_if.c:45-117`
- A missing callback returns WHD_WLAN_NOFUNCTION. `whd/src/whd_resource_if.c:45-117`
- Resource types are WLAN_FIRMWARE, WLAN_NVRAM, WLAN_CLM (and BL_IMAGE when DOWNLOAD_RAM_BOOTLOADER is defined). The header's BLOCK_SIZE is 1024 and NVM_IMAGE_SIZE_ALIGNMENT is 4. `whd/inc/whd_resource_api.h:35-50`

## Protocol dispatch (whd/src/whd_proto.c)

- whd selects the control/data protocol at build time: without PROTO_MSGBUF it initialises CDC/BDC, with it msgbuf. `whd/src/whd_proto.c:54-100`
- All command traffic goes through a table of seven functions: get_ioctl_buffer, get_iovar_buffer, set_ioctl, get_ioctl, set_iovar, get_iovar, tx_queue_data. `whd/src/include/whd_proto.h:36-48`

## Header room and out-of-band interrupt (whd/inc/whd_types.h)

### Header room a host buffer must leave

CDC/BDC build (not PROTO_MSGBUF). `whd/inc/whd_types.h:213-219`

| Constant | Value | Citations |
|---|---|---|
| BDC_HEADER_WITH_PAD | 6 | `whd/inc/whd_types.h:188` |
| BDC_HEADER_OFFSET_TO_DATA | 4 | `whd/inc/whd_types.h:195-197` |
| SDPCM_HEADER | 12 | `whd/inc/whd_types.h:195-197` |
| MAX_BUS_HEADER_SIZE (SDIO and SPI) | 4 | `whd/inc/whd_types.h:199-203` |
| BUFFER_OVERHEAD | 4 | `whd/inc/whd_types.h:211` |
| WHD_LINK_HEADER (sum of the five above; in front of the Ethernet header) | 30 | `whd/inc/whd_types.h:213-219` |
| WHD_PHYSICAL_HEADER | 30 + 14 = 44 | `whd/inc/whd_types.h:231-252` |
| WHD_PAYLOAD_MTU | 1500 | `whd/inc/whd_types.h:231-252` |
| WHD_LINK_MTU (minimum packet-pool buffer size) | 1544 | `whd/inc/whd_types.h:231-252` |

### Out-of-band interrupt option

- whd's whd_oob_config_t holds: host GPIO pin, host pin drive mode, initial drive state, device-side GPIO selection ("must be zero"), is_falling_edge, interrupt priority. `whd/inc/whd_types.h:1359-1370`
- The register is SDIOD_SEP_INT_CTL, function-0 address 242 (0xF2); bits SEP_INTR_CTL_MASK 0x01, SEP_INTR_CTL_EN 0x02, SEP_INTR_CTL_POL 0x04. `whd/src/bus_protocols/whd_sdio.h:68` `whd/src/bus_protocols/whd_sdio.h:151-153`
- c-driver and embassy define the same register and bits. `c-driver/cyw43_ll.c:197` `c-driver/cyw43_ll.c:225-227` `embassy/consts.rs:214` `embassy/consts.rs:231-233`
- whd registers a GPIO callback that wakes the whd thread; events of the wrong edge are counted as errors. `whd/src/bus_protocols/whd_bus_sdio_protocol.c:1692-1766`

| Host | Value written to SDIOD_SEP_INT_CTL | Condition | Citations |
|---|---|---|---|
| whd | MASK + EN, plus POL when the interrupt is not falling-edge; optionally selects a non-default device GPIO first | only if a host pin is configured | `whd/src/bus_protocols/whd_bus_sdio_protocol.c:1733-1766` |
| c-driver | MASK + EN, no polarity bit (comment: active-low; OR in SEP_INTR_CTL_POL for active high) | always on SDIO builds; not configurable at run time | `c-driver/cyw43_ll.c:1766-1767` |
| embassy | EN + MASK, no polarity bit | SDIO path, unconditionally, in enable_sdio_interrupts | `embassy/runner.rs:281-285` |

## Data-path hand-off (whd/src/whd_network_if.c)

- Received frames are passed to the registered whd_network_process_ethernet_data callback in the whd thread, with buffer ownership transferred and the buffer's current pointer at the Ethernet header; other data precedes it. `whd/src/whd_network_if.c:45-105`
- Transmit calls the protocol's tx_queue_data. `whd/src/whd_network_if.c:45-105`
- To add its headers whd moves the buffer's front pointer back with whd_buffer_add_remove_at_front(buffer, -sizeof(data_header_t)). `whd/src/whd_cdc_bdc.c:447-448` `whd/src/whd_buffer_api.c:189-207`

## Service loop (whd/src/whd_thread.c)

CDC/BDC build (not PROTO_MSGBUF). `whd/src/whd_thread.c:348-349`

- If woken by a bus interrupt (or the bus uses the status-report scheme), whd clears the flag and asks whether a packet is available. `whd/src/whd_thread.c:349-422`
- If so it receives packets one at a time, up to WHD_THREAD_RX_BOUND = 20. `whd/src/whd_thread.c:349-422` `whd/src/include/whd_thread.h:48-52`
- Then it sends every queued packet. `whd/src/whd_thread.c:349-422`
- If the receive bound was hit, it re-sets the interrupt flag and loops again without sleeping; otherwise it sleeps on the transceive semaphore until the next event. `whd/src/whd_thread.c:349-422`
- A counter is incremented each pass in which the packet-available query returns WHD_BUS_FAIL and is cleared by any pass that receives. When it exceeds WHD_MAX_BUS_FAIL = 10 (test is ">"), the loop reports WLC_ERR_BUS through the error handler and carries on. `whd/src/whd_thread.c:386-415` `whd/src/include/whd_thread.h:48-52`

## Keep-awake counting (whd/src/include/whd_thread_internal.h)

- WHD_WLAN_KEEP_AWAKE increments a counter, ensures the WLAN bus is up, and asserts on failure. `whd/src/include/whd_thread_internal.h:33-48`
- WHD_WLAN_LET_SLEEP decrements the counter and at zero notifies the thread. `whd/src/include/whd_thread_internal.h:33-48`
- whd lets the chip sleep only when the counter is 0 and the state is WLAN_UP. `whd/src/include/whd_thread_internal.h:33-48`

## Polling entry points (whd/src/include/whd_poll.h)

- whd exposes whd_thread_send_one_packet, whd_thread_receive_one_packet and whd_thread_poll_all so the service work can be driven without the whd thread. msgbuf builds: send_packets / receive_packets. `whd/src/include/whd_poll.h:41-114`

## Packet-buffer contract (whd/src/include/whd_buffer_api.h)

Each wrapper forwards to a host-supplied function of the same name in `buffer_if`; the host functions themselves are not found in these sources. `whd/src/whd_buffer_api.c:63-76` `whd/src/whd_buffer_api.c:93-106`

| Wrapper | Notes | Citations |
|---|---|---|
| `whd_host_buffer_get(buffer*, direction, size, timeout)` | size is uint16_t, timeout in ms; missing callback returns WHD_WLAN_NOFUNCTION | `whd/src/include/whd_buffer_api.h:62-145` `whd/src/whd_buffer_api.c:63-76` `whd/src/bus_protocols/whd_bus_common.c:342-345` |
| `whd_buffer_release(buffer, direction)` | missing callback returns WHD_WLAN_NOFUNCTION | `whd/src/include/whd_buffer_api.h:62-145` `whd/src/whd_buffer_api.c:93-106` |
| `whd_buffer_get_current_piece_data_pointer(buffer)` | returns uint8_t pointer | `whd/src/include/whd_buffer_api.h:62-145` `whd/src/whd_buffer_api.c:120-125` |
| `whd_buffer_get_current_piece_size(buffer)` | returns uint16_t; missing callback returns 0 | `whd/src/include/whd_buffer_api.h:62-145` `whd/src/whd_buffer_api.c:147-159` |
| `whd_buffer_set_size(buffer, size)` | size is uint16_t; missing callback returns WHD_WLAN_NOFUNCTION | `whd/src/include/whd_buffer_api.h:62-145` `whd/src/whd_buffer_api.c:173-185` |
| `whd_buffer_add_remove_at_front(buffer*, amount)` | per its comment: negative amount makes room for headers in front, positive removes it; may return a different buffer handle chained in front when the original lacks head-room | `whd/src/include/whd_buffer_api.h:62-145` `whd/src/whd_buffer_api.c:187-210` |

- Direction is WHD_NETWORK_TX or WHD_NETWORK_RX. `whd/src/include/whd_buffer_api.h:62-145` `whd/src/bus_protocols/whd_bus_common.c:343`
- When the host did not supply a callback the wrapper logs "Function pointers not provided" through WPRINT_WHD_INFO. `whd/src/whd_buffer_api.c:63-106` `whd/src/whd_buffer_api.c:153-158` `whd/src/whd_buffer_api.c:179-184`

## Print levels (whd/src/include/whd_debug.h)

- whd's print macros are compile-time switches. As shipped only WPRINT_ENABLE_WHD_ERROR is defined; WPRINT_ENABLE_WHD_ERROR_RETURN, WPRINT_ENABLE_WHD_INFO and WPRINT_ENABLE_WHD_DEBUG are commented out. `whd/src/include/whd_debug.h:34-37`
- WPRINT_WHD_INFO and WPRINT_WHD_DEBUG therefore expand to nothing unless the header is edited or the symbol is defined by the build. `whd/src/include/whd_debug.h:93-115`
- Host-side logging only; no wire behaviour depends on it (unverified beyond the header switches; whd_debug.c and whd_logging.c may add to this). `whd/src/include/whd_debug.h:34-37`

## Single pending command state machine (embassy/ioctl.rs)

- embassy allows one command at a time, with three states. Pending: request copied into the shared buffer by the control task, runner woken. Sent: the runner took it via wait_pending. Done{resp_len}: the runner copied the response into the same buffer and woke the control task. `embassy/ioctl.rs:28-33` `embassy/ioctl.rs:92-102` `embassy/ioctl.rs:118-145`
- A response arriving when the state is not Sent is logged ("IOCTL Response but no pending Ioctl") and dropped. `embassy/ioctl.rs:118-145`
- Request kind is encoded Get = 0, Set = 2. `embassy/ioctl.rs:10-14`
- The response copied back to the caller is limited to the length of the caller's request buffer. `embassy/ioctl.rs:118-145`

## Cross-driver comparisons

### Command reply timeout
| Host | Timeout | Detail | Citations |
|---|---|---|---|
| c-driver | 500 ms (CYW43_IOCTL_TIMEOUT_US = 500000, overridable) | polls the device and dispatches any event or data frame that arrives meanwhile | `c-driver/cyw43_config.h:91-92` `c-driver/cyw43_ll.c:1299-1324` |
| linux (SDIO) | 2500 ms (DCMD_RESP_TIMEOUT) | the SDIO bus layer's wait for the control frame | `linux/brcmfmac/sdio.c:39` `linux/brcmfmac/sdio.c:1729-1740` |
| whd (CDC/BDC) | 5000 ms (WHD_IOCTL_TIMEOUT_MS) | comment: long enough to allow waking from deep sleep (formerly 400) | `whd/src/whd_cdc_bdc.c:58-59` `whd/src/whd_cdc_bdc.c:265` |
| whd (msgbuf) | 3000 ms | | `whd/src/include/whd_msgbuf.h:40-41` |
| embassy | none | do_ioctl awaits completion indefinitely; the only way out is cancel_ioctl(); control.rs wraps do_ioctl in a DropGuard that calls cancel_ioctl() when the caller's future is dropped, so a timeout exists only if the application drops the control call | `embassy/ioctl.rs:81-90` `embassy/ioctl.rs:104-106` `embassy/ioctl.rs:118-131` `embassy/control.rs:761-767` |

### Command buffer limits
| Host | SMLEN | MEDLEN | MAXLEN | Notes | Citations |
|---|---|---|---|---|---|
| whd (WLC_IOCTL_*) | 256 | 2048 | 8192 | comment on MEDLEN: minimum value for counters is 1636 | `whd/src/include/whd_wlioctl.h:1299-1301` |
| linux (BRCMF_DCMD_*) | 256 | 1536 | 8192 | shared command buffer proto_buf is MAXLEN bytes | `linux/brcmfmac/core.h:30-32` `linux/brcmfmac/core.h:123` |
| embassy | not defined | not defined | not defined | one buffer for every request and response: MAX_IOCTL_LEN = 8 + 12 + 1024 = 1044 bytes (a clmload chunk plus 20 bytes of headers); a larger request panics on an assert; a longer response is truncated | `embassy/ioctl.rs:16-17` `embassy/ioctl.rs:119` `embassy/ioctl.rs:137` |

### Data-frame priority in the BDC header on transmit
| Host | Priority byte | Citations |
|---|---|---|
| whd | for IPv4 (and 802.1AS ethertype) frames, derived from the IP DSCP field through a 64-entry table: DSCP 0-7 gives 0, 8-23 gives 1, 24-31 gives 0, 32-47 gives 5, 48-63 gives 7; left 0 when the TOS byte is 0; the same value is passed to the bus layer as the queueing priority; the station-role remap table is the identity | `whd/src/whd_cdc_bdc.c:75-85` `whd/src/whd_cdc_bdc.c:104-109` `whd/src/whd_cdc_bdc.c:421` `whd/src/whd_cdc_bdc.c:438-441` `whd/src/whd_cdc_bdc.c:469-491` `whd/src/whd_cdc_bdc.c:509` |
| linux | skb->priority & mask copied into the header; the frame was classified with cfg80211_classify8021d when the priority was 0 or above 7 | `linux/brcmfmac/bcdc.c:273` `linux/brcmfmac/core.c:361-363` |
| c-driver | always 0 | `c-driver/cyw43_ll.c:944` |
| embassy | always 0 | `embassy/runner.rs:909-911` |

### Scan-result security detection: which information elements each host reads
| Host | Method | Citations |
|---|---|---|
| c-driver | walks the scan record's IE area once; remembers the last RSN element (id 48) and the last vendor element whose first four body bytes are 00 50 F2 01; parses the RSN one; if a WPA vendor element was found, replaces that result with the parse of the WPA element; finally ORs in the WEP flag whenever the capability field has the privacy bit 0x0010 | `c-driver/cyw43_ll.c:683-715` `c-driver/cyw43_ll.c:703-712` `c-driver/cyw43_ll.c:238-241` |
| whd | looks for an RSN element first; searches for the WPA vendor element only when no RSN element exists; RSN (length-checked against 8 + 4 * pairwise count) wins, else WPA (length-checked against 12 + 4 * unicast count), else privacy bit gives WEP_PSK, else OPEN; afterwards reads the RSNX element and sets a scan-result flag when the SAE hash-to-element bit is set | `whd/src/whd_wifi_api.c:2789-2812` `whd/src/whd_wifi_api.c:2914-2968` `whd/src/whd_utils.c:138-150` `whd/src/include/whd_chip.h:196` `whd/src/include/whd_chip.h:216` |
| linux | no security type derived from scan results; hands capability, beacon interval and the unparsed IE block (bss + ie_offset, ie_length) to cfg80211_inform_bss_data; its TLV helpers (brcmf_parse_tlvs, brcmf_find_wpaie with OUI 00 50 F2 type 1) are used on connect / AP-start parameters, not on scan results | `linux/brcmfmac/cfg80211.c:3428-3445` `linux/brcmfmac/cfg80211.c:416-476` `linux/brcmfmac/cfg80211.c:40-41` |
| embassy | no IE parsing found in embassy; ie_offset and ie_length appear only as the BssInfo field definitions and in their layout tests | `embassy/structs.rs:555-562` `embassy/structs.rs:581-597` |

- Read literally, the c-driver's WPA-element parse compares the three bytes at element offset 4 (IE_AUTH_GROUP_CIPHER_OUI_OFFSET, shared with the RSN parse) with 00 50 F2 and returns 0 on a mismatch. The scan walk matched 00 50 F2 01 at element offset 2, so offset 4 holds F2 01 and the byte after them; the check therefore fails and the result is 0 (inferred). See also the c-driver records chapter. `c-driver/cyw43_ll.c:246` `c-driver/cyw43_ll.c:584-591` `c-driver/cyw43_ll.c:696`

### Scan-result security detection: suite selector matching

Both hosts choose the mapping from the last byte (suite type) of each 4-byte suite selector. whd masks the selector with 0xFF and does not test the other three bytes in the cited code. c-driver also compares the first 3 bytes with the expected OUI and returns 0 (no flags) on a mismatch. `whd/src/whd_wifi_api.c:2815-2912` `c-driver/cyw43_ll.c:575-665` `c-driver/cyw43_ll.c:242-243`

The c-driver's akm_suite_t and cipher_t are enums without explicit values, so they count from 0 in declaration order (computed): AKM_8021X 1, AKM_PSK 2, AKM_FT_8021X 3, AKM_FT_PSK 4, AKM_8021X_SHA256 5, AKM_PSK_SHA256 6, AKM_SAE_SHA256 8, AKM_FT_SAE_SHA256 9; CIPHER_TKIP 2, CIPHER_CCMP_128 4, CIPHER_GCMP_256 9. These match the explicit whd values. `c-driver/cyw43_ll.c:529-562` `whd/src/include/whd_chip.h:77-91` `whd/src/include/whd_chip.h:99-112`

### Scan-result security detection: RSN element AKM suite types

Flags joined with "+" are ORed into the result by the driver. `whd/src/whd_wifi_api.c:2815-2912` `c-driver/cyw43_ll.c:592-660`

| AKM type | whd flags | c-driver flags | Citations |
|---|---|---|---|
| 1 8021X | WPA2 + ENTERPRISE | WPA2 + ENTERPRISE (RSN); ENTERPRISE only (WPA element) | `whd/src/whd_wifi_api.c:2815-2912` `c-driver/cyw43_ll.c:592-660` |
| 2 PSK | WPA2 | WPA2 | `whd/src/whd_wifi_api.c:2815-2912` `c-driver/cyw43_ll.c:592-660` |
| 3 FT_8021X | WPA2 + ENTERPRISE, and fbtbitmap gets ENTERP_FBT | WPA2 + FBT + ENTERPRISE | `whd/src/whd_wifi_api.c:2815-2912` `c-driver/cyw43_ll.c:592-660` |
| 4 FT_PSK | WPA2, and fbtbitmap gets PSK_FBT (a separate record field, not the FBT_ENABLED security flag) | WPA2 + FBT | `whd/src/whd_wifi_api.c:2815-2912` `c-driver/cyw43_ll.c:592-660` |
| 5 8021X_SHA256 | ENTERPRISE + WPA3 + SHA256_1X | no case | `whd/src/whd_wifi_api.c:2831-2892` `c-driver/cyw43_ll.c:592-660` |
| 6 PSK_SHA256 | WPA2 + SHA256_1X | WPA2 + WPA2_SHA256 | `whd/src/whd_wifi_api.c:2815-2912` `c-driver/cyw43_ll.c:592-660` |
| 8 SAE_SHA256 | WPA3 | WPA3 | `whd/src/whd_wifi_api.c:2815-2912` `c-driver/cyw43_ll.c:592-660` |
| 9 FT_SAE_SHA256 | WPA3, and fbtbitmap gets SAE_FBT; in a second test of the same value, WPA3 + FBT_ENABLED | no case | `whd/src/whd_wifi_api.c:2831-2892` `c-driver/cyw43_ll.c:592-660` |
| 12 8021X_SUITE_B_192 | ENTERPRISE + WPA3 + SUITE_B_SHA384 | no case | `whd/src/whd_wifi_api.c:2831-2892` `c-driver/cyw43_ll.c:592-660` |
| 18 OWE | WPA3_OWE | no case | `whd/src/whd_wifi_api.c:2831-2892` `c-driver/cyw43_ll.c:592-660` |

### Scan-result security detection: ciphers (group and each pairwise)
| Cipher type | whd | c-driver | Citations |
|---|---|---|---|
| 2 TKIP | TKIP_ENABLED | TKIP flag | `whd/src/whd_wifi_api.c:2815-2912` `c-driver/cyw43_ll.c:592-660` |
| 4 CCMP_128 | AES_ENABLED | AES flag | `whd/src/whd_wifi_api.c:2815-2912` `c-driver/cyw43_ll.c:592-660` |
| 9 GCMP_256 | AES_ENABLED | no case; warns only | `whd/src/whd_wifi_api.c:2831-2892` `c-driver/cyw43_ll.c:592-660` |
| anything else | no flag (no branch in the cited code) | warning, no flag | `whd/src/whd_wifi_api.c:2879-2912` `c-driver/cyw43_ll.c:592-660` |

### Scan-result security detection: WPA vendor element
| Item | whd | c-driver | Citations |
|---|---|---|---|
| Base | security is set to WPA_SECURITY | same parser as for the RSN element, starting from CYW43_AUTH_FLAG_WPA_SECURITY and comparing against the 00 50 F2 01 string instead of 00 0F AC | `whd/src/whd_wifi_api.c:2919-2951` `c-driver/cyw43_ll.c:575-587` `c-driver/cyw43_ll.c:241-242` |
| Group cipher | 2 gives TKIP, 4 gives AES | TKIP gives TKIP flag, CCMP_128 gives AES flag | `whd/src/whd_wifi_api.c:2919-2951` `c-driver/cyw43_ll.c:592-660` |
| AKM | 1 gives ENTERPRISE | 8021X gives ENTERPRISE | `whd/src/whd_wifi_api.c:2919-2951` `c-driver/cyw43_ll.c:592-660` |
| Unicast cipher | 4 gives AES; unicast TKIP is not tested | TKIP gives TKIP flag, CCMP_128 gives AES flag | `whd/src/whd_wifi_api.c:2919-2951` `c-driver/cyw43_ll.c:592-660` |

- Selector name definitions: whd `whd/src/include/whd_chip.h:77-91` `whd/src/include/whd_chip.h:99-112`; c-driver `c-driver/cyw43_ll.c:529-562` `c-driver/cyw43_ll.h:149-160`
- The c-driver recognises only TKIP / CCMP_128 and AKMs PSK, PSK_SHA256, SAE_SHA256, 8021X, FT_8021X, FT_PSK; other values produce a warning and no flag. `c-driver/cyw43_ll.c:592-660`

## Open questions

- ETH_ALEN and IFNAMSIZ are used, not defined, in linux-headers/ieee80211.h; no definition in these sources. `linux-headers/ieee80211.h:301`
- The numeric SDIO vendor and device ids of the linux device table are not defined in these sources; only uses exist. `linux/brcmfmac/bcmsdh.c:967-977`
- MULTICAST_FILTER_SIZE, used by embassy, has no definition in these sources. `embassy/runner.rs:1393`
- The pico-sdk PIO program that embassy-pio says it follows is not found in these sources. `embassy-pio/lib.rs:86`
- cyw43_spi_gpio_setup(), which embassy-pio also names, is declared and called by c-driver, but its definition is not found in these sources. `embassy-pio/lib.rs:313-315` `c-driver/cyw43_spi.h:103` `c-driver/cyw43_ll.c:1586`
- No source states that the Pico W shares the data and interrupt lines; embassy-pio only shows that it waits for the data pin to read high. `embassy-pio/lib.rs:118-120`
- Whether a 43439 whd build defines BLHS_SUPPORT is not settled by these sources. `whd/src/bus_protocols/whd_bus_sdio_protocol.c:2031-2041`
