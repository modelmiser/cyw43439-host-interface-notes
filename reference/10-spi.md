# The spi (gspi) bus

## Command word

### Scope and function numbers

- linux has no gSPI transport. Its only mentions of gSPI are two comments in the SDIO driver; there is no command word, bus register or status word code. Everything in this chapter comes from embassy, c-driver and whd. `linux/brcmfmac/sdio.c:1149` `linux/brcmfmac/sdio.c:2679`
- pico-sdk's Bluetooth shared-bus files do not touch the gSPI layer. They call c-driver's `cyw43_ll_read/write_backplane_reg` and `cyw43_ll_read/write_backplane_mem`. `pico-sdk/cybt_shared_bus_driver.c:537` `pico-sdk/cybt_shared_bus_driver.c:549` `pico-sdk/cybt_shared_bus_driver.c:581` `pico-sdk/cybt_shared_bus_driver.c:599`

| Function | Meaning | embassy | c-driver | whd | Citations |
|---|---|---|---|---|---|
| 0 | bus (the gSPI block's own registers) | `FUNC_BUS` | defined | defined | `embassy/consts.rs:3` `c-driver/cyw43_internal.h:17` `whd/src/bus_protocols/whd_bus_protocol_interface.h:40` |
| 1 | backplane | `FUNC_BACKPLANE` | defined | defined | `embassy/consts.rs:4` `c-driver/cyw43_internal.h:18` `whd/src/bus_protocols/whd_bus_protocol_interface.h:41` |
| 2 | WLAN data | `FUNC_WLAN` | defined | `WLAN_FUNCTION` | `embassy/consts.rs:5` `c-driver/cyw43_internal.h:19` `whd/src/bus_protocols/whd_bus_protocol_interface.h:42` |
| 3 | `FUNC_BT` in embassy only; defined, not used by any embassy SPI code (Bluetooth traffic goes over backplane memory, function 1) | `FUNC_BT` | not found (no function 3 constant) | not found (enum stops at 2; whd also defines `BUS_FUNCTION_MASK` 0x3) | `embassy/consts.rs:6` `c-driver/cyw43_internal.h:17-19` `whd/src/bus_protocols/whd_bus_protocol_interface.h:38-43` `whd/src/bus_protocols/whd_bus_protocol_interface.h:45` |

### Layout

The command is one 32-bit word. `embassy/spi.rs:447` `c-driver/cyw43_spi.c:34` `whd/src/bus_protocols/whd_bus_spi_protocol.c:953`

| Bits | Field | Values | Citations |
|---|---|---|---|
| 31 | direction | 1 = write, 0 = read | `embassy/spi.rs:447` `embassy/consts.rs:161` `embassy/consts.rs:162` `c-driver/cyw43_spi.c:34` `whd/src/bus_protocols/whd_bus_spi_protocol.c:953` `whd/src/bus_protocols/whd_bus_spi_protocol.c:128` |
| 30 | address mode | 1 = incrementing address, 0 = fixed address | `embassy/spi.rs:447` `embassy/consts.rs:163` `embassy/consts.rs:164` `c-driver/cyw43_spi.c:34` `whd/src/bus_protocols/whd_bus_spi_protocol.c:954` `whd/src/bus_protocols/whd_bus_spi_protocol.c:101` |
| 29:28 | function | 0 to 3 | `embassy/spi.rs:447` `c-driver/cyw43_spi.c:34` `whd/src/bus_protocols/whd_bus_spi_protocol.c:955` |
| 27:11 | address | 17 bits, mask 131071 (0x1FFFF) | `embassy/spi.rs:447` `c-driver/cyw43_spi.c:34` `whd/src/bus_protocols/whd_bus_spi_protocol.c:956` |
| 10:0 | length in bytes | 11 bits, mask 2047 (0x7FF) | `embassy/spi.rs:447` `c-driver/cyw43_spi.c:34` `whd/src/bus_protocols/whd_bus_spi_protocol.c:956` |

- c-driver's `pack_cmd` masks only the address. The function and size fields are not masked. `c-driver/cyw43_spi.c:34`
- c-driver has no named constants for the direction and address-mode bits. It passes `bool write` and `bool inc` to `pack_cmd`, always with `inc = true`. `c-driver/cyw43_spi.c:78`

### Address mode in use
| Driver | What it does | Citation |
|---|---|---|
| embassy | All transfers use incrementing mode, including the test-register read. `FIXED_ADDR` is defined and never used. | `embassy/spi.rs:130` `embassy/spi.rs:279` `embassy/spi.rs:148` |
| c-driver | All transfers use `inc = true`, including the test-register read. | `c-driver/cyw43_spi.c:78` `c-driver/cyw43_spi.c:95` `c-driver/cyw43_spi.c:40` |
| whd | Incrementing mode everywhere except the very first test-register read in bring-up, which uses fixed address. Its comment says that fixed address mode (non-incrementing) is required when accessing the known-value register. | `whd/src/bus_protocols/whd_bus_spi_protocol.c:355` `whd/src/bus_protocols/whd_bus_spi_protocol.c:597` `whd/src/bus_protocols/whd_bus_spi_protocol.c:586` |

### Length field

- embassy and whd mask the length to 11 bits (0x7FF), so one command word describes at most 2047 bytes. `embassy/spi.rs:447` `whd/src/bus_protocols/whd_bus_spi_protocol.c:956`
- whd defines `MAX_GSPI_TRANSFER_LEN` 2048 and documents "length < MAX_GSPI_TRANSFER_LEN" as a prerequisite. `whd/src/bus_protocols/whd_bus_spi_protocol.c:84` `whd/src/bus_protocols/whd_bus_spi_protocol.c:286`
- c-driver has no limit constant; the size goes into `pack_cmd` unmasked. `c-driver/cyw43_spi.c:34`
- All three drivers put the real byte count in the length field and round the data they clock up to a multiple of 4 bytes. `c-driver/cyw43_spi.c:65` `c-driver/cyw43_spi.c:78` `c-driver/cyw43_ll.c:846` `whd/src/bus_protocols/whd_bus_spi_protocol.c:968` `whd/src/bus_protocols/whd_bus_spi_protocol.c:302` `embassy/spi.rs:280` `embassy/spi.rs:279`

### Transaction shape

- All three drivers send a write as the command word followed immediately by the data words. `embassy/spi.rs:144` `embassy/spi.rs:25` `c-driver/cyw43_spi.c:66` `whd/src/bus_protocols/whd_bus_spi_protocol.c:1020`
- All three drivers perform a read by sending the command word and then clocking in the response, after any response-delay bytes (see Backplane access). `embassy/spi.rs:18` `c-driver/cyw43_spi.c:66` `whd/src/bus_protocols/whd_bus_spi_protocol.c:1015`
- How each driver lays the command word out as bytes is in Word length and byte order.

## Bus registers

The drivers access all of these registers through function 0. Bit tables for individual registers follow the address table; interrupt bits and status bits are in their own sections. `embassy/spi.rs:193` `c-driver/cyw43_ll.c:1593` `whd/src/bus_protocols/whd_bus_spi_protocol.c:646`

| Address | Name | Bits | Notes | Citations |
|---|---|---|---|---|
| 0 (0x0000) | `SPI_BUS_CONTROL` (embassy `REG_BUS_CTRL`) | 8 (inferred from address spacing and bit masks; not stated in the headers) | Bit names cover word length, endianness, clock phase/polarity, high-speed mode, interrupt polarity and wake-up. First byte of the 32-bit group 0x00-0x03 that the drivers write in one 4-byte access. | `embassy/consts.rs:9` `c-driver/cyw43_spi.h:21` `whd/src/bus_protocols/whd_spi.h:32` |
| 1 (0x0001) | `SPI_RESPONSE_DELAY` (embassy `REG_BUS_RESPONSE_DELAY`) | 8 (whd mask 0xFF) | Read response delay. whd's mask comment describes it as a read response delay that can be configured, as a multiple of 8 bits. Drivers set it by shifting a value by 8 bits inside the 32-bit write to address 0. | `embassy/consts.rs:10` `c-driver/cyw43_spi.h:22` `whd/src/bus_protocols/whd_spi.h:33` `whd/src/bus_protocols/whd_spi.h:69` |
| 2 (0x0002) | `SPI_STATUS_ENABLE` (embassy `REG_BUS_STATUS_ENABLE`) | 8 (inferred from address spacing and bit masks; not stated in the headers) | Bit names and comments cover whether a status word is sent after each transaction, and related options. Set by shifting by 16 bits inside the 32-bit write to address 0. | `embassy/consts.rs:11` `c-driver/cyw43_spi.h:23` `whd/src/bus_protocols/whd_spi.h:34` |
| 3 (0x0003) | `SPI_RESET_BP` | 8 (inferred from address spacing and bit masks; not stated in the headers) | Header comment "(corerev >= 1)". Defined in c-driver and whd; not defined in embassy (its register block is the range cited). No driver writes it explicitly; the bring-up 32-bit write to address 0 leaves this byte 0. | `c-driver/cyw43_spi.h:24` `whd/src/bus_protocols/whd_spi.h:35` `embassy/consts.rs:9-17` |
| 4 (0x0004) | `SPI_INTERRUPT_REGISTER` (embassy `REG_BUS_INTERRUPT`) | 16 | Header comment (all three drivers): "16 bits - Interrupt status". | `embassy/consts.rs:12` `c-driver/cyw43_spi.h:25` `whd/src/bus_protocols/whd_spi.h:36` |
| 6 (0x0006) | `SPI_INTERRUPT_ENABLE_REGISTER` (embassy `REG_BUS_INTERRUPT_ENABLE`) | 16 | Header comment (all three drivers): "16 bits - Interrupt mask". The drivers use one set of bit names for this and the interrupt register. | `embassy/consts.rs:13` `embassy/consts.rs:138` `c-driver/cyw43_spi.h:26` `c-driver/cyw43_spi.h:58` `whd/src/bus_protocols/whd_spi.h:37` |
| 8 (0x0008) | `SPI_STATUS_REGISTER` (embassy `REG_BUS_STATUS` / `SPI_STATUS_REGISTER`) | 32 | The drivers read the status word from this register. | `embassy/consts.rs:14` `embassy/consts.rs:37` `c-driver/cyw43_spi.h:27` `whd/src/bus_protocols/whd_spi.h:38` |
| 12 (0x000C) | `SPI_FUNCTION1_INFO` | 16 | c-driver names bit 0 `SPI_FUNCTIONX_ENABLED` and bit 1 `SPI_FUNCTIONX_READY`. Read only by c-driver, and only when `CYW43_CLEAR_SDIO_INT` is enabled (default 0). whd defines the address, never reads it, has no bit names. Not defined in embassy (its register block is the range cited). | `c-driver/cyw43_spi.h:28` `c-driver/cyw43_spi.h:38` `c-driver/cyw43_spi.h:39` `c-driver/cyw43_ll.c:1173` `c-driver/cyw43_config.h:28` `whd/src/bus_protocols/whd_spi.h:39` `embassy/consts.rs:9-17` |
| 14 (0x000E) | `SPI_FUNCTION2_INFO` | 16 | Defined only; no driver reads it. Not defined in embassy (its register block is the range cited). | `c-driver/cyw43_spi.h:29` `whd/src/bus_protocols/whd_spi.h:40` `embassy/consts.rs:9-17` |
| 16 (0x0010) | `SPI_FUNCTION3_INFO` | 16 | Defined only; no driver reads it. Not defined in embassy (its register block is the range cited). | `c-driver/cyw43_spi.h:30` `whd/src/bus_protocols/whd_spi.h:41` `embassy/consts.rs:9-17` |
| 20 (0x0014) | `SPI_READ_TEST_REGISTER` (embassy `REG_BUS_TEST_RO`) | 32 | Named read-only by embassy (`REG_BUS_TEST_RO`). The drivers expect the fixed value 0xFEEDBEAD. | `embassy/consts.rs:15` `embassy/consts.rs:136` `c-driver/cyw43_spi.h:31` `c-driver/cyw43_spi.h:18` `whd/src/bus_protocols/whd_spi.h:42` `whd/src/bus_protocols/whd_spi.h:53` |
| 24 (0x0018) | `REG_BUS_TEST_RW` (embassy name) | 32 | Named read/write by embassy. embassy writes 0x12345678 and reads it back during bring-up. Not found in c-driver (its `TEST_PATTERN` is 0xFEEDBEAD, not 0x12345678) or whd (no 0x18 in either register block, the ranges cited). | `embassy/consts.rs:16` `embassy/consts.rs:135` `embassy/spi.rs:203` `c-driver/cyw43_spi.h:18` `c-driver/cyw43_spi.h:21-35` `whd/src/bus_protocols/whd_spi.h:32-46` |
| 28 (0x001C) | `SPI_RESP_DELAY_F0` (embassy `REG_BUS_RESP_DELAY`) | 8 | Header comment "(corerev >= 3)". Named as the response delay for function 0. Defined only; no driver writes it. | `embassy/consts.rs:17` `c-driver/cyw43_spi.h:32` `whd/src/bus_protocols/whd_spi.h:43` |
| 29 (0x001D) | `SPI_RESP_DELAY_F1` | 8 | "(corerev >= 3)". The drivers treat it as the response delay, in bytes, for function 1 (backplane) reads. embassy writes 4, c-driver writes 16. whd defines it and never writes it; whd relies on the 4 written to `SPI_RESPONSE_DELAY` (address 1). | `embassy/consts.rs:186` `embassy/spi.rs:245` `c-driver/cyw43_spi.h:33` `c-driver/cyw43_ll.c:1612` `whd/src/bus_protocols/whd_spi.h:44` `whd/src/bus_protocols/whd_bus_spi_protocol.c:630` |
| 30 (0x001E) | `SPI_RESP_DELAY_F2` | 8 | "(corerev >= 3)". Defined only; no driver writes it. Not defined in embassy (its register block and its one response-delay constant are cited). | `c-driver/cyw43_spi.h:34` `whd/src/bus_protocols/whd_spi.h:45` `embassy/consts.rs:9-17` `embassy/consts.rs:186` |
| 31 (0x001F) | `SPI_RESP_DELAY_F3` | 8 | "(corerev >= 3)". Defined only; no driver writes it. Not defined in embassy (its register block and its one response-delay constant are cited). | `c-driver/cyw43_spi.h:35` `whd/src/bus_protocols/whd_spi.h:46` `embassy/consts.rs:9-17` `embassy/consts.rs:186` |
| 240 (0x00F0) | `SDIOD_CCCR_BRCM_CARDCAP` (SDIO-style name; not in any SPI header) | 8 | Written with `CMD_NODEC` (0x08), 1 byte, through the same function 0 register helper as the gSPI registers. See the note below. | `c-driver/cyw43_ll.c:196` `c-driver/cyw43_ll.c:222` `whd/src/bus_protocols/whd_sdio.h:66` `whd/src/bus_protocols/whd_sdio.h:193` `embassy/consts.rs:213` `embassy/consts.rs:98` |

Function 0 address 240 (0xF0), per driver. Whether the gSPI function 0 decodes this address is not found in these sources; only the writes are shown. `c-driver/cyw43_ll.c:1869` `whd/src/whd_chip.c:1244`

| Driver | When it writes 0x08 to function 0 address 0xF0 | Citations |
|---|---|---|
| c-driver | On SPI builds too: the `USE_KSO` block after F2 ready is not guarded by `CYW43_USE_SPI`. | `c-driver/cyw43_ll.c:1864` `c-driver/cyw43_ll.c:1869` |
| whd | In `whd_enable_save_restore`, bus-independent, only when `whd_is_fw_sr_capable` returns true (whd's test for save/restore-capable firmware). | `whd/src/whd_chip.c:1207` `whd/src/whd_chip.c:1244` `whd/src/whd_chip.c:1245` |
| embassy | Live only on the 4373/43455 start-up path (`init_cyw4373`). On the 43439 path the same write is inside a commented-out block. | `embassy/runner.rs:437` `embassy/runner.rs:440` `embassy/runner.rs:696` `embassy/runner.rs:396` |

### SPI_BUS_CONTROL bits (address 0)
| Bit | Mask | Name | Meaning in the headers | Citations |
|---|---|---|---|---|
| 0 | 0x01 | `WORD_LENGTH_32` | 0 = 16-bit words, 1 = 32-bit words | `embassy/consts.rs:20` `c-driver/cyw43_spi.h:42` `whd/src/bus_protocols/whd_spi.h:60` |
| 1 | 0x02 | `ENDIAN_BIG` | 0 = little endian, 1 = big endian | `embassy/consts.rs:21` `c-driver/cyw43_spi.h:43` `whd/src/bus_protocols/whd_spi.h:61` |
| 2 | 0x04 | `CLOCK_PHASE` | 0/1 clock phase delay. No driver sets it. | `embassy/consts.rs:22` `c-driver/cyw43_spi.h:44` `whd/src/bus_protocols/whd_spi.h:62` |
| 3 | 0x08 | `CLOCK_POLARITY` | 0/1 idle clock polarity low/high. No driver sets it. | `embassy/consts.rs:23` `c-driver/cyw43_spi.h:45` `whd/src/bus_protocols/whd_spi.h:63` |
| 4 | 0x10 | `HIGH_SPEED_MODE` (embassy `HIGH_SPEED`) | 1 = high-speed mode, 0 = normal mode | `embassy/consts.rs:24` `c-driver/cyw43_spi.h:46` `whd/src/bus_protocols/whd_spi.h:64` |
| 5 | 0x20 | `INTERRUPT_POLARITY_HIGH` | 1 = interrupt line active high, 0 = active low | `embassy/consts.rs:25` `c-driver/cyw43_spi.h:47` `whd/src/bus_protocols/whd_spi.h:65` |
| 6 | 0x40 | not named in any of the three drivers | | `embassy/consts.rs:25` `embassy/consts.rs:26` `c-driver/cyw43_spi.h:47` `c-driver/cyw43_spi.h:48` `whd/src/bus_protocols/whd_spi.h:65` `whd/src/bus_protocols/whd_spi.h:66` |
| 7 | 0x80 | `WAKE_UP` | Wake-up command from host to WLAN | `embassy/consts.rs:26` `c-driver/cyw43_spi.h:48` `whd/src/bus_protocols/whd_spi.h:66` |

### SPI_STATUS_ENABLE bits (address 2)
| Bit | Mask | Name | Meaning in the headers | Citations |
|---|---|---|---|---|
| 0 | 0x01 | `STATUS_ENABLE` | 1 = status word sent to host after each read/write, 0 = not sent | `embassy/consts.rs:29` `c-driver/cyw43_spi.h:51` `whd/src/bus_protocols/whd_spi.h:72` |
| 1 | 0x02 | `INTR_WITH_STATUS` | "0/1 Do-not / do-interrupt if status is sent" | `embassy/consts.rs:30` `c-driver/cyw43_spi.h:52` `whd/src/bus_protocols/whd_spi.h:73` |
| 2 | 0x04 | `RESP_DELAY_ALL` | "Applicability of resp delay to F1 or all func's read" (c-driver, whd; embassy defines the constant without a comment). No driver sets it. | `c-driver/cyw43_spi.h:53` `whd/src/bus_protocols/whd_spi.h:74` `embassy/consts.rs:31` |
| 3 | 0x08 | `DWORD_PKT_LEN_EN` | "Packet len denoted in dwords instead of bytes" (c-driver, whd; embassy defines the constant without a comment). No driver sets it. | `c-driver/cyw43_spi.h:54` `whd/src/bus_protocols/whd_spi.h:75` `embassy/consts.rs:32` |
| 5 | 0x20 | `CMD_ERR_CHK_EN` | Command error check enable (c-driver, whd; embassy defines the constant without a comment). No driver sets it. | `c-driver/cyw43_spi.h:55` `whd/src/bus_protocols/whd_spi.h:76` `embassy/consts.rs:33` |
| 6 | 0x40 | `DATA_ERR_CHK_EN` | Data error check enable (c-driver, whd; embassy defines the constant without a comment). No driver sets it. | `c-driver/cyw43_spi.h:56` `whd/src/bus_protocols/whd_spi.h:77` `embassy/consts.rs:34` |

### SPI_RESET_BP bits (address 3)
| Bit | Mask | Name | Meaning in the headers | Citations |
|---|---|---|---|---|
| 2 | 0x04 | `RESET_ON_WLAN_BP_RESET` | "enable reset for WLAN backplane". whd only; never used. c-driver has the register address only; not defined in embassy (its register block is the range cited). | `whd/src/bus_protocols/whd_spi.h:80` `c-driver/cyw43_spi.h:24` `embassy/consts.rs:9-17` |
| 7 | 0x80 | `RESET_SPI` | "reset the above enabled logic". whd only; never used. c-driver has the register address only; not defined in embassy (its register block is the range cited). | `whd/src/bus_protocols/whd_spi.h:81` `c-driver/cyw43_spi.h:24` `embassy/consts.rs:9-17` |

## Status word

### Bits
| Bits | Mask | Name | Notes | Citations |
|---|---|---|---|---|
| 0 | 0x00000001 | `STATUS_DATA_NOT_AVAILABLE` | | `embassy/consts.rs:40` `c-driver/cyw43_spi.h:79` `whd/src/bus_protocols/whd_spi.h:102` |
| 1 | 0x00000002 | `STATUS_UNDERFLOW` | | `embassy/consts.rs:41` `c-driver/cyw43_spi.h:80` `whd/src/bus_protocols/whd_spi.h:103` |
| 2 | 0x00000004 | `STATUS_OVERFLOW` | | `embassy/consts.rs:42` `c-driver/cyw43_spi.h:81` `whd/src/bus_protocols/whd_spi.h:104` |
| 3 | 0x00000008 | `STATUS_F2_INTR` | | `embassy/consts.rs:43` `c-driver/cyw43_spi.h:82` `whd/src/bus_protocols/whd_spi.h:105` |
| 4 | 0x00000010 | `STATUS_F3_INTR` | | `embassy/consts.rs:44` `c-driver/cyw43_spi.h:83` `whd/src/bus_protocols/whd_spi.h:106` |
| 5 | 0x00000020 | `STATUS_F2_RX_READY` | | `embassy/consts.rs:45` `c-driver/cyw43_spi.h:84` `whd/src/bus_protocols/whd_spi.h:107` |
| 6 | 0x00000040 | `STATUS_F3_RX_READY` | | `embassy/consts.rs:46` `c-driver/cyw43_spi.h:85` `whd/src/bus_protocols/whd_spi.h:108` |
| 7 | 0x00000080 | `STATUS_HOST_CMD_DATA_ERR` | | `embassy/consts.rs:47` `c-driver/cyw43_spi.h:86` `whd/src/bus_protocols/whd_spi.h:109` |
| 8 | 0x00000100 | `STATUS_F2_PKT_AVAILABLE` | | `embassy/consts.rs:48` `c-driver/cyw43_spi.h:87` `whd/src/bus_protocols/whd_spi.h:110` |
| 19:9 | 0x000FFE00, shift 9 | F2 packet length | 11 bits. All three drivers read it as the byte length of the pending function 2 packet. | `embassy/consts.rs:49` `embassy/consts.rs:50` `c-driver/cyw43_spi.h:88` `c-driver/cyw43_spi.h:89` `whd/src/bus_protocols/whd_spi.h:111` `whd/src/bus_protocols/whd_spi.h:112` `embassy/runner.rs:1055` `c-driver/cyw43_ll.c:1228` `whd/src/bus_protocols/whd_bus_spi_protocol.c:515` |
| 20 | 0x00100000 | `STATUS_F3_PKT_AVAILABLE` | | `embassy/consts.rs:51` `c-driver/cyw43_spi.h:90` `whd/src/bus_protocols/whd_spi.h:113` |
| 31:21 | 0xFFE00000, shift 21 | F3 packet length | 11 bits. Defined in all three; no driver reads it. | `embassy/consts.rs:52` `embassy/consts.rs:53` `c-driver/cyw43_spi.h:91` `c-driver/cyw43_spi.h:92` `whd/src/bus_protocols/whd_spi.h:114` `whd/src/bus_protocols/whd_spi.h:115` |

### How each driver obtains it

- (unverified) The status word is available two ways: as a 32-bit read of function 0 register 8 (0x0008), and, when `STATUS_ENABLE` is set, appended to every read/write transaction. No source states what the trailer contains; this is inferred from the `STATUS_ENABLE` comment plus embassy storing the returned u32 as status. `c-driver/cyw43_spi.h:51` `c-driver/cyw43_ll.c:1216` `whd/src/bus_protocols/whd_bus_spi_protocol.c:490` `embassy/spi.rs:135`

| Driver | Source of the status | Citations |
|---|---|---|
| embassy | `SpiBusCyw43::cmd_read` and `cmd_write` return a u32 that is stored as the latest status. A later `read32` of function 0 address 8 returns that cached value and zeroes the cache instead of doing a bus read, whenever the cached value is non-zero. That the returned u32 is the status trailer is (inferred); the trait doc does not say so. | `embassy/spi.rs:18` `embassy/spi.rs:25` `embassy/spi.rs:135` `embassy/spi.rs:144` `embassy/spi.rs:282` `embassy/spi.rs:292` `embassy/spi.rs:422` `embassy/spi.rs:424` |
| embassy-pio (the Pico W implementation of that trait) | `write` clocks out all the words, then clocks in 32 more bits and returns them as `status`. `cmd_read` clocks out the 32-bit command, clocks in `read.len()` words plus 32 more bits, and returns that last word as `status`. | `embassy-pio/lib.rs:233` `embassy-pio/lib.rs:234` `embassy-pio/lib.rs:248` `embassy-pio/lib.rs:253` `embassy-pio/lib.rs:259` `embassy-pio/lib.rs:260` `embassy-pio/lib.rs:282` `embassy-pio/lib.rs:291` |
| c-driver | Always reads register 8. Does not set `STATUS_ENABLE`; uses no transaction trailer. | `c-driver/cyw43_ll.c:1216` `c-driver/cyw43_ll.c:1575` |
| whd | Always reads register 8. Explicitly masks `STATUS_ENABLE` to 0 in the bus-control write. | `whd/src/bus_protocols/whd_bus_spi_protocol.c:631` |

### Names used when testing bits
| Driver | Names used | Citations |
|---|---|---|
| embassy | The `STATUS_*` names. | `embassy/runner.rs:1051` |
| whd | Literals and aliases: `(1 << 5)` for F2 RX ready, `GSPI_PACKET_AVAILABLE` (1 << 8), `GSPI_UNDERFLOW` (1 << 1). | `whd/src/bus_protocols/whd_bus_spi_protocol.c:76` `whd/src/bus_protocols/whd_bus_spi_protocol.c:77` `whd/src/bus_protocols/whd_bus_spi_protocol.c:723` `whd/src/bus_protocols/whd_bus_spi_protocol.c:315` |
| c-driver | Mixed. In the receive path it uses `GSPI_PACKET_AVAILABLE` (0x0100) and `F2_F3_FIFO_RD_UNDERFLOW` (0x0002) from its interrupt-bit list, which have the same numeric values as `STATUS_F2_PKT_AVAILABLE` and `STATUS_UNDERFLOW`, and the literal `(status >> 9) & 0x7FF` for the length. In the F2-ready wait it uses `STATUS_F2_RX_READY`. | `c-driver/cyw43_ll.c:1227` `c-driver/cyw43_ll.c:1230` `c-driver/cyw43_ll.c:1228` `c-driver/cyw43_ll.c:1847` |

### An all-ones status
| Driver | Handling of status 0xFFFFFFFF | Citations |
|---|---|---|
| c-driver | Treated as not valid yet; re-read up to 1000 times, then gives up and returns -1. | `c-driver/cyw43_ll.c:1215` `c-driver/cyw43_ll.c:1217` `c-driver/cyw43_ll.c:1222` |
| whd | Treated as not valid yet; re-read in a loop with no bound. | `whd/src/bus_protocols/whd_bus_spi_protocol.c:497` |
| embassy | No 0xFFFFFFFF check. Treats a zero cached status as "no cached value" and reads the register. | `embassy/spi.rs:422` |

## Interrupt register and acknowledgement

### Bits (registers 4 and 6, same layout)
| Bit | Mask | Name | Meaning (header comment where one exists, otherwise read from the name) | Citations |
|---|---|---|---|---|
| 0 | 0x0001 | `DATA_UNAVAILABLE` | Requested data not available; cleared by writing 1 | `embassy/consts.rs:139` `c-driver/cyw43_spi.h:59` `whd/src/bus_protocols/whd_spi.h:84` |
| 1 | 0x0002 | `F2_F3_FIFO_RD_UNDERFLOW` | F2/F3 FIFO read underflow | `embassy/consts.rs:140` `c-driver/cyw43_spi.h:60` `whd/src/bus_protocols/whd_spi.h:85` |
| 2 | 0x0004 | `F2_F3_FIFO_WR_OVERFLOW` | F2/F3 FIFO write overflow | `embassy/consts.rs:141` `c-driver/cyw43_spi.h:61` `whd/src/bus_protocols/whd_spi.h:86` |
| 3 | 0x0008 | `COMMAND_ERROR` | Command error; cleared by writing 1 | `embassy/consts.rs:142` `c-driver/cyw43_spi.h:62` `whd/src/bus_protocols/whd_spi.h:87` |
| 4 | 0x0010 | `DATA_ERROR` | Data error; cleared by writing 1 | `embassy/consts.rs:143` `c-driver/cyw43_spi.h:63` `whd/src/bus_protocols/whd_spi.h:88` |
| 5 | 0x0020 | `F2_PACKET_AVAILABLE` | A function 2 (WLAN) packet is available | `embassy/consts.rs:144` `c-driver/cyw43_spi.h:64` `whd/src/bus_protocols/whd_spi.h:89` |
| 6 | 0x0040 | `F3_PACKET_AVAILABLE` | A function 3 packet is available | `embassy/consts.rs:145` `c-driver/cyw43_spi.h:65` `whd/src/bus_protocols/whd_spi.h:90` |
| 7 | 0x0080 | `F1_OVERFLOW` | "Due to last write. Bkplane has pending write requests" | `embassy/consts.rs:146` `c-driver/cyw43_spi.h:66` `whd/src/bus_protocols/whd_spi.h:91` |
| 8 | 0x0100 | `MISC_INTR0` (embassy, whd); `GSPI_PACKET_AVAILABLE` (c-driver) | c-driver gives this bit a different name and then uses that macro on the status word (where 0x100 is `STATUS_F2_PKT_AVAILABLE`), never on the interrupt register. | `embassy/consts.rs:147` `whd/src/bus_protocols/whd_spi.h:92` `c-driver/cyw43_spi.h:67` `c-driver/cyw43_ll.c:1227` |
| 9 | 0x0200 | `MISC_INTR1` | Miscellaneous interrupt 1 | `embassy/consts.rs:148` `c-driver/cyw43_spi.h:68` `whd/src/bus_protocols/whd_spi.h:93` |
| 10 | 0x0400 | `MISC_INTR2` | Miscellaneous interrupt 2 | `embassy/consts.rs:149` `c-driver/cyw43_spi.h:69` `whd/src/bus_protocols/whd_spi.h:94` |
| 11 | 0x0800 | `MISC_INTR3` | Miscellaneous interrupt 3 | `embassy/consts.rs:150` `c-driver/cyw43_spi.h:70` `whd/src/bus_protocols/whd_spi.h:95` |
| 12 | 0x1000 | `MISC_INTR4` | Miscellaneous interrupt 4 | `embassy/consts.rs:151` `c-driver/cyw43_spi.h:71` `whd/src/bus_protocols/whd_spi.h:96` |
| 13 | 0x2000 | `F1_INTR` | Function 1 interrupt. The drivers enable it for Bluetooth notification. | `embassy/consts.rs:152` `c-driver/cyw43_spi.h:72` `whd/src/bus_protocols/whd_spi.h:97` `whd/src/bus_protocols/whd_bus_spi_protocol.c:1116` |
| 14 | 0x4000 | `F2_INTR` | Function 2 interrupt | `embassy/consts.rs:153` `c-driver/cyw43_spi.h:73` `whd/src/bus_protocols/whd_spi.h:98` |
| 15 | 0x8000 | `F3_INTR` | Function 3 interrupt | `embassy/consts.rs:154` `c-driver/cyw43_spi.h:74` `whd/src/bus_protocols/whd_spi.h:99` |

- embassy defines the same names with an `IRQ_` prefix (for example `IRQ_DATA_UNAVAILABLE`). `embassy/consts.rs:139`

Bus-error group (bits 1, 2 and 7, value 134 (0x0086)): `c-driver/cyw43_spi.h:76`

| Driver | Use | Citations |
|---|---|---|
| c-driver | Names the group `BUS_OVERFLOW_UNDERFLOW`. | `c-driver/cyw43_spi.h:76` |
| whd | Tests the literal 0x0086. Its comment says the mask "should be 0x87" but that data-not-available errors are sometimes flagged for no apparent reason. | `whd/src/bus_protocols/whd_bus_spi_protocol.c:439` |
| embassy | Not found (no bus-error test on the interrupt register). | `embassy/runner.rs:1017` |

### What starts interrupt handling
| Driver | Trigger | Citations |
|---|---|---|
| embassy | Waits on `SpiBusCyw43::wait_for_event`, then always reads the interrupt register. The trait's default `wait_for_event` yields (active polling) if the implementor does not wait on the IRQ pin. embassy-pio's implementation waits on the IRQ pin. | `embassy/runner.rs:1017` `embassy/spi.rs:33` `embassy/spi.rs:34` `embassy-pio/lib.rs:323` |
| c-driver | `cyw43_ll_has_work` only samples the host interrupt pin and compares it with the configured active level; no bus access. Bluetooth work is tested separately and first (`cyw43_ll_bt_has_work`, which does read the backplane). | `c-driver/cyw43_ll.c:2534` `c-driver/cyw43_ll.c:2536` `c-driver/cyw43_ll.c:2537` `c-driver/cyw43_ctrl.c:207` `c-driver/cyw43_ctrl.c:212` |
| c-driver, pin level | Active level is 1 when the port defines `CYW43_PIN_WL_HOST_WAKE` and 0 when it defines `CYW43_PIN_WL_IRQ`. `INTERRUPT_POLARITY_HIGH` is programmed only in the `HOST_WAKE` case. | `c-driver/cyw43_ll.c:55` `c-driver/cyw43_ll.c:56` `c-driver/cyw43_ll.c:57` `c-driver/cyw43_ll.c:58` `c-driver/cyw43_ll.c:1577` |
| whd | Requires an out-of-band interrupt pin for SPI; attach fails with `WHD_BADARG` without one. The pin handler only notifies the whd thread, which then reads the interrupt register through the packet-available routine. | `whd/src/bus_protocols/whd_bus_spi_protocol.c:176` `whd/src/bus_protocols/whd_bus_spi_protocol.c:179` `whd/src/bus_protocols/whd_bus_spi_protocol.c:1176` `whd/src/whd_thread.c:376` `whd/src/whd_thread.c:370` |
| whd, status-report scheme | `whd_bus_spi_use_status_report_scheme` returns `WHD_FALSE`, although the header defines `WHD_BUS_SPI_USE_STATUS_REPORT_SCHEME` as true. So the whd thread polls the bus only when the interrupt flag is set. | `whd/src/bus_protocols/whd_bus_spi_protocol.c:1154` `whd/src/bus_protocols/whd_bus_spi_protocol.h:50` `whd/src/whd_thread.c:371` |
| whd, wait | `whd_bus_spi_wait_for_wlan_event`: the semaphore timeout is the delayed-bus-release time if one is pending; else `BT_POLLING_TIME` (100 ms) when a BT device without its own interrupt is registered (the bus-interrupt flag is then forced true so the thread polls); else it lets the WLAN bus sleep and waits forever if that succeeded (1 ms if the sleep request did not return success). With zero bus credits the wait is capped at `WHD_THREAD_POKE_TIMEOUT` (100 ms) and the SPI poke, an empty stub, is called first. | `whd/src/bus_protocols/whd_bus_spi_protocol.c:788` `whd/src/bus_protocols/whd_bus_spi_protocol.c:791` `whd/src/bus_protocols/whd_bus_spi_protocol.c:797` `whd/src/bus_protocols/whd_bus_spi_protocol.c:802` `whd/src/bus_protocols/whd_bus_spi_protocol.c:804` `whd/src/bus_protocols/whd_bus_spi_protocol.c:805` `whd/src/bus_protocols/whd_bus_spi_protocol.c:809` `whd/src/bus_protocols/whd_bus_spi_protocol.c:814` `whd/src/bus_protocols/whd_bus_spi_protocol.c:819` `whd/src/bus_protocols/whd_bus_spi_protocol.c:822` `whd/src/bus_protocols/whd_bus_spi_protocol.c:825` `whd/src/bus_protocols/whd_bus_spi_protocol.c:91` `whd/src/bus_protocols/whd_bus_spi_protocol.c:93` `whd/src/bus_protocols/whd_bus_spi_protocol.c:97` |

### embassy

1. Read the 16-bit interrupt register. `embassy/runner.rs:1017`
2. If `F2_PACKET_AVAILABLE` is set, drain packets using the status word (see Reading a packet). `embassy/runner.rs:1022` `embassy/runner.rs:1023`
3. If `DATA_UNAVAILABLE` is set, write the 16-bit value 1 to the interrupt register, clearing only that bit. Comment: "this seems to be ignorable with no ill effects". `embassy/runner.rs:1026` `embassy/runner.rs:1029`
4. Run the Bluetooth handler. `embassy/runner.rs:1034`

- No other interrupt bit is written back at run time. `embassy/runner.rs:1026`
- embassy does not read or clear the SDIO core int-status on SPI except for the BT `FC_CHANGE` bit. `embassy/runner.rs:1017` `embassy/bluetooth.rs:451`

### c-driver

1. Unless the previous poll delivered a packet, return "no packet" if the host interrupt pin is not at its active level. `c-driver/cyw43_ll.c:1148`
2. Wake the bus. `c-driver/cyw43_ll.c:1152`
3. Read the 16-bit interrupt register. `c-driver/cyw43_ll.c:1158`
4. Warn "Bus error condition detected" if any of `F1_OVERFLOW`, F2/F3 underflow or overflow is set and the value changed since last time. `c-driver/cyw43_ll.c:1160` `c-driver/cyw43_ll.c:1161`
5. If the value is non-zero, write the same 16-bit value back to the interrupt register (write-1-to-clear of every bit read). `c-driver/cyw43_ll.c:1196` `c-driver/cyw43_ll.c:1198`
6. If `F2_PACKET_AVAILABLE` is not set return "no packet"; otherwise go on to the status word. `c-driver/cyw43_ll.c:1201`

- `had_successful_packet` shortcut: after a packet was read successfully, the next poll skips the pin check and the interrupt-register read and acknowledge, and goes straight to the status word. The flag is cleared when the status shows no packet, an invalid length, or a zero SDPCM header. `c-driver/cyw43_ll.c:1148` `c-driver/cyw43_ll.c:1154` `c-driver/cyw43_ll.c:1233` `c-driver/cyw43_ll.c:1239` `c-driver/cyw43_ll.c:1253` `c-driver/cyw43_ll.c:1256`
- Optional path, `CYW43_CLEAR_SDIO_INT` (default 0): also read the SDIO core's int-status over the backplane. If any `I_HMB_SW_MASK` bit is set, read `SPI_FUNCTION1_INFO`, write the masked bits back to the SDIO int-status, then re-read the gSPI interrupt register and use that fresh value for the acknowledge. `c-driver/cyw43_ll.c:1169` `c-driver/cyw43_ll.c:1170` `c-driver/cyw43_ll.c:1173` `c-driver/cyw43_ll.c:1181` `c-driver/cyw43_ll.c:1184` `c-driver/cyw43_ll.c:1193` `c-driver/cyw43_config.h:28`

### whd

`whd_bus_spi_packet_available_to_read`: `whd/src/bus_protocols/whd_bus_spi_protocol.c:424`

1. Ensure the WLAN bus is up. `whd/src/bus_protocols/whd_bus_spi_protocol.c:429`
2. Service the BT flow-control bit. `whd/src/bus_protocols/whd_bus_spi_protocol.c:431`
3. Read the 16-bit interrupt register. `whd/src/bus_protocols/whd_bus_spi_protocol.c:433`
4. Log "Bus error condition detected" if (value & 0x0086) != 0. `whd/src/bus_protocols/whd_bus_spi_protocol.c:439`
5. Read the SDIO core int-status over the backplane; if any `I_HMB_SW_MASK` (240, 0xF0) bit is set, write those bits back to it. `whd/src/bus_protocols/whd_bus_spi_protocol.c:445` `whd/src/bus_protocols/whd_bus_spi_protocol.c:453` `whd/src/bus_protocols/whd_bus_spi_protocol.c:456` `whd/src/bus_protocols/whd_bus_spi_protocol.c:95` `whd/src/bus_protocols/whd_sdio.h:113`
6. If the gSPI interrupt value is non-zero, write it back unchanged to the interrupt register (2 bytes). `whd/src/bus_protocols/whd_bus_spi_protocol.c:464` `whd/src/bus_protocols/whd_bus_spi_protocol.c:466`
7. Return value & `F2_PACKET_AVAILABLE`. `whd/src/bus_protocols/whd_bus_spi_protocol.c:473`

- whd also exposes `whd_bus_spi_ack_interrupt(intstatus)`: a 2-byte write of the given value to the interrupt register. `whd/src/bus_protocols/whd_bus_spi_protocol.c:389` `whd/src/bus_protocols/whd_bus_spi_protocol.c:391`

### Acknowledgement compared
| Driver | Gives the interrupt register back | SDIO core int-status (over backplane) | Citations |
|---|---|---|---|
| embassy | Only `DATA_UNAVAILABLE` (writes 1). | Not read or cleared, except the BT `FC_CHANGE` bit. | `embassy/runner.rs:1029` `embassy/runner.rs:1017` |
| c-driver | Every bit it read. | Clearing compiled out by default (`CYW43_CLEAR_SDIO_INT` 0). | `c-driver/cyw43_ll.c:1198` `c-driver/cyw43_config.h:28` |
| whd | Every bit it read. | Reads it on every interrupt and writes back the `I_HMB_SW_MASK` bits that are set. | `whd/src/bus_protocols/whd_bus_spi_protocol.c:466` `whd/src/bus_protocols/whd_bus_spi_protocol.c:456` |

### Bluetooth notification

- All three read the SDIO core int-status (4 bytes) over the backplane and, if `I_HMB_FC_CHANGE` (bit 5, 0x20) is set, write that bit back to clear it and then service BT. `embassy/bluetooth.rs:451` `embassy/bluetooth.rs:452` `embassy/bluetooth.rs:455` `c-driver/cyw43_ll.c:2544` `c-driver/cyw43_ll.c:2545` `c-driver/cyw43_ll.c:2546` `c-driver/cyw43_ll.c:117` `whd/src/bus_protocols/whd_bus_spi_protocol.c:401` `whd/src/bus_protocols/whd_bus_spi_protocol.c:408` `whd/src/bus_protocols/whd_bus_spi_protocol.c:412` `whd/src/bus_protocols/whd_sdio.h:116`
- The servicing routine is `bt_has_work` in embassy; `cyw43_ll_bt_has_work` in c-driver, polled from `cyw43_ctrl.c` whenever BT firmware is loaded; `whd_bus_spi_bt_packet_available_to_read` in whd, which calls the registered `bt_int_cb`. `embassy/bluetooth.rs:451` `c-driver/cyw43_ctrl.c:207` `whd/src/bus_protocols/whd_bus_spi_protocol.c:417`
- When BT is used, `F1_INTR` is enabled in the gSPI interrupt enable register and the SDIO core host-interrupt mask is set to `I_HMB_FC_CHANGE`. `embassy/runner.rs:660` `embassy/runner.rs:665` `c-driver/cyw43_ll.c:1626` `c-driver/cyw43_ll.c:1834` `whd/src/bus_protocols/whd_bus_spi_protocol.c:1119` `whd/src/bus_protocols/whd_bus_spi_protocol.c:1128`
- Each driver first writes `I_HMB_SW_MASK` (0xF0) to the host-int-mask register and then, with Bluetooth, writes `I_HMB_FC_CHANGE` (0x20) to the same register as a plain 4-byte write. The second write replaces the first value; it is not OR-ed in. `c-driver/cyw43_ll.c:1822` `c-driver/cyw43_ll.c:1832` `c-driver/cyw43_ll.c:1834` `c-driver/cyw43_ll.c:116` `c-driver/cyw43_ll.c:117` `embassy/runner.rs:616` `embassy/runner.rs:659` `embassy/runner.rs:665` `whd/src/bus_protocols/whd_bus_spi_protocol.c:1078` `whd/src/bus_protocols/whd_bus_spi_protocol.c:1128`
- In whd the second write happens later, in `whd_bus_spi_init_stats`, and only if a BT device with an interrupt is registered. `whd/src/bus_protocols/whd_bus_spi_protocol.c:1113`

## Bring-up handshake

### Step table
| Step | embassy | c-driver | whd | Citations |
|---|---|---|---|---|
| 0. Power/reset | Drives the power pin low for 20 ms, then high, then waits 250 ms before touching the bus. | Calls port hooks `cyw43_spi_init`, `cyw43_spi_gpio_setup`, `cyw43_spi_reset`. | No power/reset step inside `whd_bus_spi_init`. | `embassy/spi.rs:184` `embassy/spi.rs:185` `embassy/spi.rs:186` `embassy/spi.rs:187` `c-driver/cyw43_ll.c:1581` `c-driver/cyw43_ll.c:1586` `c-driver/cyw43_ll.c:1588` `whd/src/bus_protocols/whd_bus_spi_protocol.c:560` |
| 1. Test read, 16-bit (swapped) mode | Reads register 20 (0x14) until it returns 0xFEEDBEAD. Retries up to 500 ms (1 ms tick); fails init on timeout. Exact 32-bit compare, incrementing address. | Same read, 10 tries with 1 ms delays; fails with `-CYW43_EIO`. Exact 32-bit compare, incrementing address. | Fixed-address read with a tolerant byte search; see "whd's first read" below. | `embassy/spi.rs:193` `embassy/spi.rs:195` `embassy/spi.rs:197` `embassy/util.rs:70` `c-driver/cyw43_ll.c:1592` `c-driver/cyw43_ll.c:1593` `c-driver/cyw43_ll.c:1594` `c-driver/cyw43_ll.c:1597` `c-driver/cyw43_ll.c:1636` `whd/src/bus_protocols/whd_bus_spi_protocol.c:609` |
| 1b. Write test, 16-bit mode | Writes 0x12345678 to register 24 (0x18) and reads it back; a mismatch fails init. Then reads `SPI_BUS_CONTROL` (swapped) for tracing. | Not found (no write test). | Not found (no write test). | `embassy/spi.rs:203` `embassy/spi.rs:204` `embassy/spi.rs:206` `embassy/spi.rs:209` `c-driver/cyw43_ll.c:1601` `whd/src/bus_protocols/whd_bus_spi_protocol.c:612` |
| 2. Configure | One 4-byte write to function 0 address 0, still in 16-bit (swapped) format. Sets bus control (byte 0), response delay (byte 1) and status enable (byte 2) together. All three put 4 (0x04) in the response-delay byte and set `WORD_LENGTH_32` and `WAKE_UP`. Values differ; see "The configuration word". | same | same | `embassy/spi.rs:215` `embassy/spi.rs:218` `embassy/spi.rs:221` `embassy/spi.rs:222` `c-driver/cyw43_ll.c:1574` `c-driver/cyw43_ll.c:1575` `c-driver/cyw43_ll.c:1605` `whd/src/bus_protocols/whd_bus_spi_protocol.c:627` `whd/src/bus_protocols/whd_bus_spi_protocol.c:628` `whd/src/bus_protocols/whd_bus_spi_protocol.c:630` |
| 3. Switch | Every later transaction uses 32-bit, non-swapped words. | Same; also calls the port hook `cyw43_spi_set_polarity(self, 0)` because "the above command switched SPI configuration". Only driver that changes host SPI clock polarity here. | Same; sets `bus_gspi_32bit` to true. | `embassy/spi.rs:229` `c-driver/cyw43_spi.c:58` `c-driver/cyw43_spi.c:59` `whd/src/bus_protocols/whd_bus_spi_protocol.c:634` |
| 4. Verify, 32-bit mode | Reads `SPI_BUS_CONTROL` back (1 byte, traced). Re-reads the read-only test register (must be 0xFEEDBEAD) and the read/write test register (must still be 0x12345678). | Reads `SPI_BUS_CONTROL` back (4 bytes, logged). Does not re-read the test register in 32-bit mode. | Reads `SPI_BUS_CONTROL` back (4 bytes, value ignored). Then reads the test register and fails with `WHD_SPI_ID_READ_FAIL` unless it is exactly 0xFEEDBEAD. | `embassy/spi.rs:229` `embassy/spi.rs:234` `embassy/spi.rs:236` `embassy/spi.rs:240` `embassy/spi.rs:242` `c-driver/cyw43_ll.c:1609` `c-driver/cyw43_ll.c:1610` `whd/src/bus_protocols/whd_bus_spi_protocol.c:635` `whd/src/bus_protocols/whd_bus_spi_protocol.c:646` `whd/src/bus_protocols/whd_bus_spi_protocol.c:649` `whd/src/bus_protocols/whd_bus_spi_protocol.c:652` |
| 5. F1 response delay | 1-byte write of 4 to function 0 register 29 (0x1D). | 1-byte write of 16 to the same register. | Step absent; `SPI_RESP_DELAY_F1` is defined (the line cited) and never written. | `embassy/spi.rs:245` `embassy/consts.rs:187` `c-driver/cyw43_ll.c:1612` `c-driver/cyw43_ll.h:194` `whd/src/bus_protocols/whd_spi.h:44` |
| 6. Clear latched errors | 1-byte write to interrupt register 4 of `DATA_UNAVAILABLE` + `COMMAND_ERROR` + `DATA_ERROR` + `F1_OVERFLOW` = 153 (0x99). | identical | identical | `embassy/spi.rs:251` `embassy/spi.rs:254` `c-driver/cyw43_ll.c:1617` `c-driver/cyw43_ll.c:1618` `whd/src/bus_protocols/whd_bus_spi_protocol.c:656` `whd/src/bus_protocols/whd_bus_spi_protocol.c:657` |
| 7. Interrupt enable | 2-byte write to register 6 of `F2_F3_FIFO_RD_UNDERFLOW` + `F2_F3_FIFO_WR_OVERFLOW` + `COMMAND_ERROR` + `DATA_ERROR` + `F2_PACKET_AVAILABLE` + `F1_OVERFLOW` = 190 (0x00BE). Adds `F1_INTR` (0x2000) at run time when `bluetooth_enabled` is passed. | Same base value. `F1_INTR` is compile-time (`CYW43_ENABLE_BLUETOOTH`). | Same base value. `F1_INTR` is added later, in `whd_bus_spi_init_stats`, only if a BT device with interrupts is registered. | `embassy/spi.rs:261` `embassy/spi.rs:265` `embassy/spi.rs:267` `embassy/spi.rs:268` `embassy/spi.rs:270` `c-driver/cyw43_ll.c:1623` `c-driver/cyw43_ll.c:1624` `c-driver/cyw43_ll.c:1625` `c-driver/cyw43_ll.c:1626` `c-driver/cyw43_ll.c:1628` `whd/src/bus_protocols/whd_bus_spi_protocol.c:661` `whd/src/bus_protocols/whd_bus_spi_protocol.c:662` `whd/src/bus_protocols/whd_bus_spi_protocol.c:1119` |
| 8. ALP clock | Writes `SBSDIO_ALP_AVAIL_REQ` (0x08) to function 1 register `CHIP_CLOCK_CSR` 65550 (0x1000E); on SPI only that one bit, unlike SDIO. Polls the register for `ALP_AVAIL` (0x40) for 100 ms. Then writes 0 to clear the request. | Same writes; polls 10 tries x 1 ms. | Same writes; polls 100 x 1 ms, reading `CHIP_CLOCK_CSR` as a 2-byte value. | `embassy/runner.rs:481` `embassy/runner.rs:506` `embassy/runner.rs:516` `embassy/consts.rs:64` `embassy/consts.rs:115` `embassy/consts.rs:116` `c-driver/cyw43_ll.c:1730` `c-driver/cyw43_ll.c:1743` `c-driver/cyw43_ll.c:1745` `c-driver/cyw43_ll.c:1758` `whd/src/bus_protocols/whd_bus_spi_protocol.c:667` `whd/src/bus_protocols/whd_bus_spi_protocol.c:672` `whd/src/bus_protocols/whd_bus_spi_protocol.c:674` `whd/src/bus_protocols/whd_bus_spi_protocol.c:64` `whd/src/bus_protocols/whd_bus_spi_protocol.c:692` |
| 8b. Early watermark probe | Writes 16 (0x10) to the F2 watermark register and reads it back (see The F2 watermark). | Same, only with `CYW43_ENABLE_BLUETOOTH`. | Not found. | `embassy/runner.rs:484` `c-driver/cyw43_ll.c:1733` `whd/src/bus_protocols/whd_bus_spi_protocol.c:1081` |
| 9. After firmware start | Waits for the HT clock (`CHIP_CLOCK_CSR` bit 0x80) up to 500 ms. Writes `I_HMB_SW_MASK` (0xF0) as 4 bytes to the SDIO core host interrupt mask over the backplane. Sets the F2 watermark. Polls the status word for `STATUS_F2_RX_READY` (bit 5) up to 1000 ms. | HT wait 1000 x 1 ms. Same mask write and watermark. F2-ready poll 1000 x 1 ms, then `-CYW43_EIO`. | HT wait `HT_AVAIL_TIMEOUT_MS` = 1000 x 1 ms. Same mask write and watermark. F2-ready poll `F2_READY_TIMEOUT_MS` = 1000 x 1 ms, then `WHD_TIMEOUT`. | `embassy/runner.rs:607` `embassy/runner.rs:608` `embassy/runner.rs:616` `embassy/runner.rs:677` `embassy/runner.rs:687` `embassy/runner.rs:689` `c-driver/cyw43_ll.c:1808` `c-driver/cyw43_ll.c:1810` `c-driver/cyw43_ll.c:1822` `c-driver/cyw43_ll.c:1838` `c-driver/cyw43_ll.c:1843` `c-driver/cyw43_ll.c:1846` `c-driver/cyw43_ll.c:1847` `whd/src/bus_protocols/whd_bus_spi_protocol.c:1060` `whd/src/bus_protocols/whd_bus_spi_protocol.c:1061` `whd/src/bus_protocols/whd_bus_spi_protocol.c:1078` `whd/src/bus_protocols/whd_bus_spi_protocol.c:1081` `whd/src/bus_protocols/whd_bus_spi_protocol.c:721` `whd/src/bus_protocols/whd_bus_spi_protocol.c:723` `whd/src/bus_protocols/whd_bus_spi_protocol.c:737` `whd/src/bus_protocols/whd_bus_spi_protocol.c:60` `whd/src/bus_protocols/whd_bus_spi_protocol.c:71` |
| 10. Start-up `DATA_UNAVAILABLE` | No init-time clear; clears `DATA_UNAVAILABLE` whenever seen in the IRQ handler. | At the end of bus init reads the 16-bit interrupt register and, if `DATA_UNAVAILABLE` is set, writes the whole value back. Comment: "We always seem to start with a data unavailable error - so clear it now". | Not found as an init step. | `embassy/runner.rs:1026` `c-driver/cyw43_ll.c:1897` `c-driver/cyw43_ll.c:1898` `c-driver/cyw43_ll.c:1899` `c-driver/cyw43_ll.c:1900` `whd/src/bus_protocols/whd_bus_spi_protocol.c:755` |
| 11. Interrupt mask after firmware runs | Replaces the interrupt enable mask with only `F2_PACKET_AVAILABLE` (plus `F1_INTR` with Bluetooth), dropping the error and overflow enables from step 7. | Keeps the full mask from step 7; no second write. | Keeps the full mask; a second write only adds `F1_INTR` for BT. | `embassy/runner.rs:658` `embassy/runner.rs:660` `embassy/runner.rs:671` `c-driver/cyw43_ll.c:1628` `whd/src/bus_protocols/whd_bus_spi_protocol.c:1119` |

### 16-bit mode before the configuration write

- Every driver sends the first commands with the 32-bit command and data words rearranged ("swapped") until `SPI_BUS_CONTROL` has been written. `embassy/spi.rs:149` `embassy/spi.rs:159` `c-driver/cyw43_spi.c:40` `c-driver/cyw43_spi.h:96` `whd/src/bus_protocols/whd_bus_spi_protocol.c:360` `whd/src/bus_protocols/whd_bus_spi_protocol.c:574`
- That the chip is in 16-bit word mode after reset is (inferred) from all three drivers using swapped access before the bus-control write and from the c-driver header comment "Read and write before switching to 32bit mode"; no source states the reset default outright. `c-driver/cyw43_spi.h:96` `embassy/spi.rs:218` `whd/src/bus_protocols/whd_bus_spi_protocol.c:617`

| Driver | 16-bit-mode helper | Citations |
|---|---|---|
| c-driver `read_reg_u32_swap` | One 8-byte full-duplex transfer: 4 command bytes, then 4 clocked bytes. Result taken from bytes 4..7 with the same byte rearrangement. A non-zero transfer error code is returned in place of the register value. | `c-driver/cyw43_spi.c:39` `c-driver/cyw43_spi.c:40` `c-driver/cyw43_spi.c:41` `c-driver/cyw43_spi.c:43` `c-driver/cyw43_spi.c:47` `c-driver/cyw43_spi.c:16` |
| c-driver `write_reg_u32_swap` | One 8-byte write (command, value), then `cyw43_spi_set_polarity(self, 0)` unconditionally. | `c-driver/cyw43_spi.c:54` `c-driver/cyw43_spi.c:55` `c-driver/cyw43_spi.c:56` `c-driver/cyw43_spi.c:59` |
| embassy `read32_swapped` | `cmd_read` with the rotated command and a 1-word read buffer; result rotated back. | `embassy/spi.rs:148` `embassy/spi.rs:149` `embassy/spi.rs:150` `embassy/spi.rs:152` `embassy/spi.rs:154` |
| embassy `write32_swapped` | `cmd_write` of [rotated command, rotated value]. | `embassy/spi.rs:158` `embassy/spi.rs:159` `embassy/spi.rs:161` |
| whd | No separate swapped helpers. The generic register helpers apply `H32TO16LE` while `bus_gspi_32bit` is false; the first test read builds its own 12-byte transfer. | `whd/src/bus_protocols/whd_bus_spi_protocol.c:853` `whd/src/bus_protocols/whd_bus_spi_protocol.c:570` `whd/src/bus_protocols/whd_bus_spi_protocol.c:602` |

- The c-driver and embassy helpers all take function and address from the caller, use incrementing mode and length 4, and use no response-delay word. `c-driver/cyw43_spi.c:40` `embassy/spi.rs:149`

### whd's first read

- whd sends a fixed-address read of register 20 (0x14), size 4, with the header built as `SWAP32_16BIT_PARTS(SWAP32(cmd))`, and clocks 12 bytes in total. `whd/src/bus_protocols/whd_bus_spi_protocol.c:595` `whd/src/bus_protocols/whd_bus_spi_protocol.c:597` `whd/src/bus_protocols/whd_bus_spi_protocol.c:599` `whd/src/bus_protocols/whd_bus_spi_protocol.c:570`
- It repeats 1 ms apart, up to `FEADBEAD_TIMEOUT_MS` = 500 iterations, until any of the 8 response bytes equals the low byte of 0xFEEDBEAD or one of three one-bit-left-shifted variants. `whd/src/bus_protocols/whd_bus_spi_protocol.c:605` `whd/src/bus_protocols/whd_bus_spi_protocol.c:609` `whd/src/bus_protocols/whd_bus_spi_protocol.c:63` `whd/src/bus_protocols/whd_spi.h:54` `whd/src/bus_protocols/whd_spi.h:55` `whd/src/bus_protocols/whd_spi.h:56` `whd/src/bus_protocols/whd_spi.h:57`
- The four accepted byte values evaluate to 0xAD, 0x5A, 0x5B and 0x5C. These are computed from the macro definitions, not literal in the source. `whd/src/bus_protocols/whd_spi.h:54` `whd/src/bus_protocols/whd_spi.h:55` `whd/src/bus_protocols/whd_spi.h:56` `whd/src/bus_protocols/whd_spi.h:57`
- whd's comments say the first transfer is corrupted by a chip issue and the data "could be left shifted by one bit". `whd/src/bus_protocols/whd_bus_spi_protocol.c:583` `whd/src/bus_protocols/whd_bus_spi_protocol.c:588`
- The loop result is not checked for timeout; the exact read in step 4 catches failure. `whd/src/bus_protocols/whd_bus_spi_protocol.c:609`

### The configuration word (step 2)
| Driver | Bus control (byte 0) | Response delay (byte 1) | Status enable (byte 2) | Computed 32-bit word | Citations |
|---|---|---|---|---|---|
| embassy | `WORD_LENGTH_32`, `HIGH_SPEED`, `INTERRUPT_POLARITY_HIGH` (unconditional), `WAKE_UP`. `ENDIAN_BIG` not set; comment: "32-bit word length, little endian (which is the default endianness)". | 4 | `STATUS_ENABLE`, `INTR_WITH_STATUS` | 0x000304B1 | `embassy/spi.rs:212` `embassy/spi.rs:218` `embassy/spi.rs:219` `embassy/spi.rs:220` `embassy/spi.rs:221` `embassy/spi.rs:222` `embassy/spi.rs:223` `embassy/spi.rs:224` |
| c-driver | `WORD_LENGTH_32`, `ENDIAN_BIG`, `HIGH_SPEED_MODE`, `WAKE_UP`. `INTERRUPT_POLARITY_HIGH` only when `CYW43_PIN_WL_HOST_WAKE` is defined. | 4 | `INTR_WITH_STATUS` only | 0x00020493 (0x000204B3 with the polarity bit) | `c-driver/cyw43_ll.c:1574` `c-driver/cyw43_ll.c:1575` `c-driver/cyw43_ll.c:1576` `c-driver/cyw43_ll.c:1577` |
| whd (little-endian host build) | `WORD_LENGTH_32`, `ENDIAN_BIG`, `WAKE_UP`. `INTERRUPT_POLARITY_HIGH` when the out-of-band interrupt config is not falling-edge. `HIGH_SPEED_MODE` not set. On `IL_BIGENDIAN` builds `ENDIAN_BIG` is ANDed with 0. | 4 | `INTR_WITH_STATUS`; `STATUS_ENABLE` explicitly ANDed with 0 | 0x00020483 (0x000204A3 with the polarity bit) | `whd/src/bus_protocols/whd_bus_spi_protocol.c:576` `whd/src/bus_protocols/whd_bus_spi_protocol.c:577` `whd/src/bus_protocols/whd_bus_spi_protocol.c:619` `whd/src/bus_protocols/whd_bus_spi_protocol.c:621` `whd/src/bus_protocols/whd_bus_spi_protocol.c:628` `whd/src/bus_protocols/whd_bus_spi_protocol.c:629` `whd/src/bus_protocols/whd_bus_spi_protocol.c:631` `whd/src/bus_protocols/whd_bus_spi_protocol.c:632` |

### Wake and sleep
| Driver | What it does | Citations |
|---|---|---|
| whd | The bus-specific wake and sleep read `SPI_BUS_CONTROL` as 32 bits, set (wake) or clear (sleep) `WAKE_UP`, and write it back. | `whd/src/bus_protocols/whd_bus_spi_protocol.c:1090` `whd/src/bus_protocols/whd_bus_spi_protocol.c:1092` `whd/src/bus_protocols/whd_bus_spi_protocol.c:1102` `whd/src/bus_protocols/whd_bus_spi_protocol.c:1104` |
| c-driver | The equivalent `WAKE_UP` code is compiled out (`#if 0 && CYW43_USE_SPI`) with the note "This causes the device to fail after sleep". | `c-driver/cyw43_ll.c:1878` |
| c-driver | Calls `cyw43_ll_bus_sleep(false)` before every poll and send. When the bus is marked down this wakes it through the keep-SDIO-on (KSO) bit in function 1 sleep CSR 65567 (0x1001F): with `USE_KSO` = 1 it writes the bit twice, then re-reads up to 64 times at 1 ms, writing again after each failed read, until KSO and device-on are both set. No function 0 register is involved. When `bus_is_up` is already true the call returns without touching the bus. | `c-driver/cyw43_ll.c:39` `c-driver/cyw43_ll.c:1152` `c-driver/cyw43_ll.c:775` `c-driver/cyw43_ll.c:1436` `c-driver/cyw43_ll.c:1396` `c-driver/cyw43_ll.c:1475` `c-driver/cyw43_ll.c:1481` `c-driver/cyw43_ll.c:1404` `c-driver/cyw43_ll.c:1413` `c-driver/cyw43_ll.c:1426` `c-driver/cyw43_ll.c:114` |
| embassy | Not found; `WAKE_UP` is set once at bring-up. | `embassy/spi.rs:221` |

Pad-pull register `SDIO_PULL_UP`, function 1 address 65551 (0x1000F), in the sleep set-up: `whd/src/bus_protocols/whd_sdio.h:108` `c-driver/cyw43_ll.c:210` `embassy/consts.rs:65`

| Driver | What it writes | Citations |
|---|---|---|
| whd | `whd_enable_save_restore` calls the bus sleep hook (on SPI: clear `WAKE_UP`) and then writes 15 (0x0F), under the comment "Put SPI interface block to sleep". Runs only when `whd_is_fw_sr_capable` returns true. | `whd/src/whd_chip.c:1207` `whd/src/whd_chip.c:1283` `whd/src/whd_chip.c:1286` `whd/src/whd_chip.c:1288` `whd/src/whd_chip.c:1289` `whd/src/bus_protocols/whd_sdio.h:108` |
| c-driver | Writes 0x0F under the same comment (with the `WAKE_UP` clear compiled out), then immediately writes 0 and reads it back ("CLEAR PAD PULLS"). | `c-driver/cyw43_ll.c:210` `c-driver/cyw43_ll.c:1878` `c-driver/cyw43_ll.c:1884` `c-driver/cyw43_ll.c:1885` `c-driver/cyw43_ll.c:1891` `c-driver/cyw43_ll.c:1892` |
| embassy | On the 43439 only writes 0 and reads it back; never writes 0x0F. | `embassy/consts.rs:65` `embassy/runner.rs:406` `embassy/runner.rs:407` |

## Word length and byte order

- Word length is selected by `SPI_BUS_CONTROL` bit 0 (0 = 16-bit, 1 = 32-bit). All three drivers switch to 32-bit during bring-up and never switch back. `c-driver/cyw43_spi.h:42` `whd/src/bus_protocols/whd_spi.h:60` `embassy/spi.rs:218` `c-driver/cyw43_ll.c:1602` `whd/src/bus_protocols/whd_bus_spi_protocol.c:617`
- The swapped (16-bit-mode) helpers are used only before the bus-control write. c-driver comments that `write_reg_u32_swap` "is only used to switch the SPI bus configuration at start up". whd's register helpers apply `H32TO16LE` to header and value only while `bus_gspi_32bit` is false. `c-driver/cyw43_spi.c:50` `whd/src/bus_protocols/whd_bus_spi_protocol.c:853` `whd/src/bus_protocols/whd_bus_spi_protocol.c:855` `whd/src/bus_protocols/whd_bus_spi_protocol.c:959` `whd/src/bus_protocols/whd_bus_spi_protocol.c:964`

### Endianness setting
| Driver | `ENDIAN_BIG` | Citations |
|---|---|---|
| c-driver | Set. The command is then sent as little-endian bytes. | `c-driver/cyw43_ll.c:1574` |
| whd | Set on little-endian hosts. The command is then sent as native words. | `whd/src/bus_protocols/whd_bus_spi_protocol.c:628` |
| embassy | Not set. A TODO notes the C library's different value. | `embassy/spi.rs:218` `embassy/spi.rs:213` `embassy/spi.rs:212` |

### Command word as bytes, 32-bit mode
| Driver | How the command word is laid out | Citations |
|---|---|---|
| c-driver | 4 little-endian bytes (`cyw43_put_le32`). | `c-driver/cyw43_spi.c:78` `c-driver/cyw43_spi.c:26` |
| whd | Written as a native `uint32_t` into the buffer; no byte shuffling. | `whd/src/bus_protocols/whd_bus_spi_protocol.c:353` |
| embassy | Hands whole u32 words to the `SpiBusCyw43` trait. The WLAN-write command is stored with `to_le_bytes` in an aligned byte buffer. The bit order on the wire is decided by the trait implementation; for the Pico W implementation see the embassy-pio row. | `embassy/spi.rs:290` `embassy/spi.rs:18` |
| embassy-pio | Both PIO shift registers shift left, so each u32 word goes out and comes in most significant bit first. Chip select is driven low before and high after each `cmd_write` / `cmd_read`. | `embassy-pio/lib.rs:205` `embassy-pio/lib.rs:208` `embassy-pio/lib.rs:300` `embassy-pio/lib.rs:302` `embassy-pio/lib.rs:307` `embassy-pio/lib.rs:309` |

### The 16-bit-mode rearrangement
| Driver | Transformation of a 32-bit value with bytes b3 b2 b1 b0 (b0 least significant) | Citations |
|---|---|---|
| c-driver | `cyw43_put_swap32` emits the byte order [b1, b0, b3, b2]. | `c-driver/cyw43_spi.c:20` `c-driver/cyw43_spi.c:21` `c-driver/cyw43_spi.c:22` `c-driver/cyw43_spi.c:23` |
| whd | `H32TO16LE` swaps the two bytes inside each 16-bit half. On a little-endian host this is the same byte stream as c-driver's (inferred). | `whd/src/bus_protocols/whd_bus_spi_protocol.c:86` |
| embassy | `swap16` = `rotate_left(16)`: swaps the two 16-bit halves of the u32 it hands to the SPI trait. It is not a byte swap within halves. Whether this gives the same wire bits depends on the trait implementation's bit order. | `embassy/spi.rs:443` |
| embassy-pio | Sends each u32 most significant bit first, so a rotated word leaves as bytes b1, b0, b3, b2 (inferred from the shift direction and the rotation). | `embassy-pio/lib.rs:205` `embassy/spi.rs:443` |

- whd's two 16-bit-mode encodings are the same transformation: `SWAP32_16BIT_PARTS(SWAP32(x))`, used for the first test read, equals `H32TO16LE(x)`, used by the generic helpers. `SWAP32` is a full 4-byte reversal; reversing the bytes and then swapping the two 16-bit halves leaves each half byte-swapped in place. `whd/src/bus_protocols/whd_bus_spi_protocol.c:79` `whd/src/bus_protocols/whd_bus_spi_protocol.c:80` `whd/src/bus_protocols/whd_bus_spi_protocol.c:86` `whd/src/bus_protocols/whd_bus_spi_protocol.c:595` `whd/src/include/whd_endian.h:38`

## The F2 watermark

- The register is a function 1 register at address 65544 (0x10008), written as 1 byte. `embassy/consts.rs:58` `c-driver/cyw43_ll.c:108` `whd/src/bus_protocols/whd_sdio.h:101`

| Driver | Early probe (right after requesting ALP) | Run-time value (after HT clock, before the F2-ready wait) | What its comments say | Citations |
|---|---|---|---|---|
| embassy | Always on SPI: writes 16 (0x10), reads it back, asserts the read-back is 0x10. Comment says this is "Not present in whd driver". | 32 (0x20). The SDIO constant next to it is 8. | "Lower F2 Watermark to avoid DMA Hang in F2 when SD Clock is stopped" | `embassy/runner.rs:484` `embassy/runner.rs:487` `embassy/runner.rs:489` `embassy/runner.rs:491` `embassy/consts.rs:106` `embassy/consts.rs:107` `embassy/runner.rs:674` `embassy/runner.rs:677` |
| c-driver | Only with `CYW43_ENABLE_BLUETOOTH`: writes 0x10, reads it back, fails bus init with `-CYW43_EIO` if it differs. | 32 (0x20). The SDIO constant next to it is 8. | "Lower F2 Watermark to avoid DMA Hang in F2 when SD Clock is stopped" | `c-driver/cyw43_ll.c:1837` `c-driver/cyw43_ll.c:1733` `c-driver/cyw43_ll.c:1735` `c-driver/cyw43_ll.c:1737` `c-driver/cyw43_ll.c:1738` `c-driver/cyw43_ll.c:148` `c-driver/cyw43_ll.c:149` `c-driver/cyw43_ll.c:1838` |
| whd | Not found; only the single write of 32. | 32 (0x20). | Same "Lower F2 Watermark ..." reason. The comment on the constant says the value was taken from a DHD source file (`dhd_sdio.c`) and that on the 43362 it has to be at least 8 and word-aligned, or the dongle firmware crashes. | `whd/src/bus_protocols/whd_bus_spi_protocol.c:73` `whd/src/bus_protocols/whd_bus_spi_protocol.c:74` `whd/src/bus_protocols/whd_bus_spi_protocol.c:1080` `whd/src/bus_protocols/whd_bus_spi_protocol.c:1081` |

## Backplane access

### The address window

- All three drivers reach backplane addresses through a 32768-byte (0x8000) window. They put the low 15 bits (mask 0x7FFF) in the command word's address field. `embassy/consts.rs:110` `embassy/consts.rs:109` `c-driver/cyw43_ll.c:123` `whd/src/bus_protocols/whd_chip_reg.h:81` `whd/src/bus_protocols/whd_chip_reg.h:82`
- The drivers write the upper bits to three 1-byte function 1 registers: `embassy/spi.rs:106` `c-driver/cyw43_ll.c:338` `whd/src/bus_protocols/whd_bus_spi_protocol.c:1310`

| Address | Role | Holds | Citations |
|---|---|---|---|
| 65546 (0x1000A) | window address low | bits 15:8 of the window base | `embassy/consts.rs:60` `embassy/spi.rs:122` `c-driver/cyw43_ll.c:109` `c-driver/cyw43_ll.c:344` `whd/src/bus_protocols/whd_sdio.h:103` `whd/src/bus_protocols/whd_bus_spi_protocol.c:1344` |
| 65547 (0x1000B) | window address mid | bits 23:16 | `embassy/consts.rs:61` `embassy/spi.rs:114` `c-driver/cyw43_ll.c:110` `c-driver/cyw43_ll.c:341` `whd/src/bus_protocols/whd_sdio.h:104` `whd/src/bus_protocols/whd_bus_spi_protocol.c:1327` |
| 65548 (0x1000C) | window address high | bits 31:24 | `embassy/consts.rs:62` `embassy/spi.rs:106` `c-driver/cyw43_ll.c:111` `c-driver/cyw43_ll.c:338` `whd/src/bus_protocols/whd_sdio.h:105` `whd/src/bus_protocols/whd_bus_spi_protocol.c:1310` |

- All three drivers cache the current window base and write only the bytes that changed, in the order high, mid, low. `embassy/spi.rs:102` `embassy/spi.rs:110` `embassy/spi.rs:118` `embassy/spi.rs:126` `c-driver/cyw43_ll.c:334` `c-driver/cyw43_ll.c:337` `c-driver/cyw43_ll.c:340` `c-driver/cyw43_ll.c:343` `c-driver/cyw43_ll.c:346` `whd/src/bus_protocols/whd_bus_spi_protocol.c:1302` `whd/src/bus_protocols/whd_bus_spi_protocol.c:1306` `whd/src/bus_protocols/whd_bus_spi_protocol.c:1322` `whd/src/bus_protocols/whd_bus_spi_protocol.c:1339`

| Driver | Initial cached window | After an access | Citations |
|---|---|---|---|
| embassy | 0xAAAAAAAA at start and on every init, so the first access rewrites all three bytes ("Device loses both on reset"). | Leaves the window where the last access put it. | `embassy/spi.rs:63` `embassy/spi.rs:177` `embassy/spi.rs:178` `embassy/spi.rs:126` |
| c-driver | 0 | Moves the window back to the chipcommon base 0x18000000 after register read, register write, block write and block read. | `c-driver/cyw43_ll.c:287` `c-driver/cyw43_ll.c:360` `c-driver/cyw43_ll.c:375` `c-driver/cyw43_ll.c:2577` `c-driver/cyw43_ll.c:2587` `c-driver/cyw43_ll.c:119` |
| whd | 0 | Restores the window at the end of block transfers only; single-value register reads and writes do not restore it. | `whd/src/bus_protocols/whd_bus_common.c:234` `whd/src/bus_protocols/whd_bus_spi_protocol.c:579` `whd/src/bus_protocols/whd_bus_common.c:418` `whd/src/bus_protocols/whd_bus_spi_protocol.c:911` |

### The 32-bit access flag

- Bit 15 of the F1 address field (32768, 0x8000; `SBSDIO_SB_ACCESS_2_4B_FLAG` / `BACKPLANE_ADDRESS_32BIT_FLAG`) is the flag the drivers set for 32-bit backplane access (whd comment: "with b15, maps to 32-bit SB access"). `embassy/consts.rs:111` `c-driver/cyw43_ll.c:126` `whd/src/bus_protocols/whd_bus_spi_protocol.c:69`

| Driver | Single values | Block transfers | Citations |
|---|---|---|---|
| embassy | Flag only for 4-byte accesses. | Always set. | `embassy/spi.rs:76` `embassy/spi.rs:77` `embassy/spi.rs:319` `embassy/spi.rs:363` |
| c-driver | On SPI, set for every backplane register access regardless of size. | Set for firmware-download writes and the BT mem read/write helpers; not set for the download-verify read. | `c-driver/cyw43_ll.c:352` `c-driver/cyw43_ll.c:353` `c-driver/cyw43_ll.c:429` `c-driver/cyw43_ll.c:462` `c-driver/cyw43_ll.c:2569` `c-driver/cyw43_ll.c:2586` |
| whd | Flag only for 4-byte accesses. | Never set by the common block transfer. | `whd/src/bus_protocols/whd_bus_spi_protocol.c:915` `whd/src/bus_protocols/whd_bus_spi_protocol.c:933` `whd/src/bus_protocols/whd_bus_common.c:378` |

### Read padding (response delay)

- On function 1 reads all three drivers clock and discard padding bytes between the command and the data. No driver does so on reads from functions 0 and 2. `embassy/spi.rs:23` `embassy/spi.rs:133` `embassy/spi.rs:138` `c-driver/cyw43_spi.c:68` `c-driver/cyw43_spi.c:71` `whd/src/bus_protocols/whd_bus_spi_protocol.c:878` `whd/src/bus_protocols/whd_bus_spi_protocol.c:884`

| Driver | Padding on F1 reads | Where it is programmed | Padding counted in the command's length field | Citations |
|---|---|---|---|---|
| embassy | 4 bytes (one 32-bit word) | Register 1 (value 4) and register 29 (value 4) | No; only the data length. Extra bytes are just clocked. | `embassy/consts.rs:187` `embassy/spi.rs:222` `embassy/spi.rs:326` `embassy/spi.rs:330` `embassy/spi.rs:245` `embassy/spi.rs:130` `embassy/spi.rs:320` |
| c-driver | 16 bytes | Register 1 (value 4) and register 29 (value 16). The only driver whose F1 delay differs from the 4 all three write to register 1. | No; only the data length. | `c-driver/cyw43_ll.h:194` `c-driver/cyw43_spi.c:72` `c-driver/cyw43_ll.c:1612` `c-driver/cyw43_spi.c:78` |
| whd | 4 bytes | Register 1 (value 4) only | Yes: `value_length + padding` for registers; `transfer_size + padd_size` for blocks. | `whd/src/bus_protocols/whd_bus_spi_protocol.h:53` `whd/src/bus_protocols/whd_bus_spi_protocol.c:113` `whd/src/bus_protocols/whd_bus_spi_protocol.c:630` `whd/src/bus_protocols/whd_bus_spi_protocol.c:896` `whd/src/bus_protocols/whd_bus_common.c:402` |

- c-driver buffer layout for reads: a 5-word `spi_header` array sits immediately before the 2048-byte `spid_buf`. For backplane reads the command goes at `spi_header[0]`, so command (4) + padding (16) ends exactly where `spid_buf` starts. For other functions the command goes 16 bytes later, so the data again lands at `spid_buf[0]`. `c-driver/cyw43_internal.h:33` `c-driver/cyw43_internal.h:35` `c-driver/cyw43_spi.c:70` `c-driver/cyw43_spi.c:74` `c-driver/cyw43_spi.c:82`
- whd single-register buffer layout: `whd_bus_gspi_header_t` is a `uint32_t`. `whd_transfer_bytes_packet_t` is packed {`uint8_t bus_header[4]`; `uint32_t data[1]`}, 8 bytes (computed), and the command word is written at `data - 4`, i.e. over `bus_header`. `whd/src/bus_protocols/whd_bus_spi_protocol.h:37` `whd/src/bus_protocols/whd_bus_protocol_interface.h:61` `whd/src/bus_protocols/whd_bus_protocol_interface.h:65` `whd/src/bus_protocols/whd_bus_protocol_interface.h:66` `whd/src/bus_protocols/whd_bus_spi_protocol.c:948`
- For backplane reads the whd helper overlays `gspi_backplane_f1_read_packet_t` = packed {header, 4 bytes at offset 0; `response_delay[4]` at offset 4} followed by data at offset 8, so the value is taken 4 bytes later. The helper's local buffer is `MAX_BUS_HEADER_SIZE` + 4 + 4 = 12 bytes. `whd/src/bus_protocols/whd_bus_spi_protocol.c:108` `whd/src/bus_protocols/whd_bus_spi_protocol.c:112` `whd/src/bus_protocols/whd_bus_spi_protocol.c:113` `whd/src/bus_protocols/whd_bus_spi_protocol.c:120` `whd/src/bus_protocols/whd_bus_spi_protocol.c:121` `whd/src/bus_protocols/whd_bus_spi_protocol.c:875` `whd/src/bus_protocols/whd_bus_spi_protocol.c:881` `whd/src/bus_protocols/whd_bus_spi_protocol.c:883` `whd/src/bus_protocols/whd_bus_spi_protocol.c:899`
- (unverified) whd reads call the transfer with tx = NULL, tx length 4 and the header buffer as rx; writes pass the header buffer as tx with rx = NULL. How the HAL (`whd_hal_spi_transfer`) clocks the command out of the rx buffer is not found in these sources. `whd/src/bus_protocols/whd_bus_spi_protocol.c:1015` `whd/src/bus_protocols/whd_bus_spi_protocol.c:1020` `whd/src/bus_protocols/whd_bus_spi_protocol.c:266`

### Single values
| Driver | Sizes and shape | Citations |
|---|---|---|
| embassy | 1-, 2- and 4-byte reads all clock two 32-bit words and take the value from the second (the first is the response delay). Writes send [command, value]. | `embassy/spi.rs:131` `embassy/spi.rs:133` `embassy/spi.rs:138` `embassy/spi.rs:144` `embassy/spi.rs:379` `embassy/spi.rs:387` `embassy/spi.rs:397` |
| c-driver | The backplane register helpers accept only sizes 1 and 4 (asserted) and only function 1. | `c-driver/cyw43_ll.c:310` `c-driver/cyw43_ll.c:314` `c-driver/cyw43_ll.c:324` |
| whd | Accepts any `register_length` <= 4; reads the chip id as 2 bytes. | `whd/src/bus_protocols/whd_bus_spi_protocol.c:696` |

### Block transfers

- Maximum backplane (F1) block transfer over SPI is 64 bytes per command in all three drivers. `embassy/consts.rs:112` `c-driver/cyw43_ll.h:193` `whd/src/bus_protocols/whd_bus_spi_protocol.h:52` `whd/src/bus_protocols/whd_bus_spi_protocol.c:1159`
- Block transfers never cross a window boundary. embassy and whd shorten the chunk to the bytes remaining in the 0x8000 window. c-driver's download path asserts the chunk fits; its backplane-mem write helper clips to the window end. `embassy/spi.rs:309` `embassy/spi.rs:311` `whd/src/bus_protocols/whd_bus_common.c:363` `whd/src/bus_protocols/whd_bus_common.c:366` `c-driver/cyw43_ll.c:424` `c-driver/cyw43_ll.c:2566` `c-driver/cyw43_ll.c:2584`
- embassy asserts that block backplane addresses are multiples of 4, with the note "It seems the HW force-aligns the addr to 2 if data.len() >= 2, to 4 if data.len() >= 4". `embassy/spi.rs:300` `embassy/spi.rs:304` `embassy/spi.rs:347`
- c-driver has no alignment assert on its backplane mem helpers; whd has no alignment check in the common block transfer. `c-driver/cyw43_ll.c:2583` `whd/src/bus_protocols/whd_bus_common.c:362`
- pico-sdk's BT shared-bus code further splits its backplane memory reads and writes so that no transfer crosses a 4096-byte (0x1000) boundary and none exceeds `CYW43_BUS_MAX_BLOCK_SIZE`. `pico-sdk/cybt_shared_bus_driver.c:577` `pico-sdk/cybt_shared_bus_driver.c:578` `pico-sdk/cybt_shared_bus_driver.c:596`

## Reading a packet

### Comparison
| Topic | embassy | c-driver | whd | Citations |
|---|---|---|---|---|
| Length source | (status & 0x000FFE00) >> 9 | (status >> 9) & 0x7FF | (status >> 9) & 0x7FF | `embassy/runner.rs:1055` `c-driver/cyw43_ll.c:1228` `whd/src/bus_protocols/whd_bus_spi_protocol.c:515` |
| Length limits | None: no zero check, no upper limit, no underflow-bit check. The 11-bit field caps the length at 2047, which fits the runner's 4 + 2048 byte scratch buffer. | Rejects 0, more than 1536, or status underflow. | Rejects 0, more than `WHD_LINK_MTU - sizeof(whd_buffer_header_t)`, or status underflow. | `embassy/runner.rs:1055` `embassy/runner.rs:1082` `embassy/runner.rs:814` `c-driver/cyw43_ll.c:1229` `whd/src/bus_protocols/whd_bus_spi_protocol.c:501` |
| Abort | No F2 read abort on the SPI bus. | 1-byte write of bit 0 to function 1 address 65549 (0x1000D). | Same write. | `embassy/spi.rs:275` `c-driver/cyw43_ll.c:1232` `whd/src/bus_protocols/whd_bus_spi_protocol.c:505` |
| No buffer | Reads and parses the whole frame into a scratch buffer; only forwarding of a data frame is skipped. | No allocation step; always reads into the single 2048-byte `spid_buf` in the driver state. | Reads the first 12 bytes for the credit info and aborts the rest. | `embassy/runner.rs:1101` `c-driver/cyw43_ll.c:1242` `c-driver/cyw43_internal.h:35` `whd/src/bus_protocols/whd_bus_spi_protocol.c:532` |
| Loop | Until the status no longer shows a packet. | Caller polls until a poll returns -1. | Thread repeats until failure or `WHD_THREAD_RX_BOUND` packets. | `embassy/runner.rs:1042` `c-driver/cyw43_ll.c:1268` `c-driver/cyw43_ll.c:1272` `whd/src/whd_thread.c:385` |

### The abort register

- The F2 read abort is the same operation in c-driver and whd: a 1-byte write of bit 0 to function 1 address 65549 (0x1000D). `c-driver/cyw43_ll.c:1232` `whd/src/bus_protocols/whd_bus_spi_protocol.c:505`
- That address is the SDIO-style frame-control register. whd names bit 0 `SFC_RF_TERM` ("Read Frame Terminate"), bit 1 `SFC_WF_TERM`, bit 2 `SFC_CRC4WOOS`, bit 3 `SFC_ABORTALL`. `whd/src/bus_protocols/whd_sdio.h:106` `whd/src/bus_protocols/whd_sdio.h:228` `whd/src/bus_protocols/whd_sdio.h:229` `whd/src/bus_protocols/whd_sdio.h:230` `whd/src/bus_protocols/whd_sdio.h:231`
- embassy defines `REG_BACKPLANE_FRAME_CONTROL` = 0x1000D but uses it only in its SDIO bus, never on SPI. `embassy/consts.rs:63` `embassy/sdio.rs:243`

### embassy

1. Read the status (cached trailer or register 8). If `STATUS_F2_PKT_AVAILABLE` is clear, stop. Otherwise len = (status & 0x000FFE00) >> 9. `embassy/runner.rs:1048` `embassy/runner.rs:1051` `embassy/runner.rs:1055`
2. No validity checks on the length and no abort path. `embassy/runner.rs:1055` `embassy/runner.rs:1082` `embassy/runner.rs:814`
3. Take a packet-pool buffer if one is free and its capacity is at least len rounded up to 4 (SPI reads whole words, up to 3 bytes past len). Otherwise warn and read into the scratch buffer. Either way the frame is read and parsed: credits, command replies and events are still processed; only forwarding of a data frame to the network stack is skipped. `embassy/runner.rs:1078` `embassy/runner.rs:1081` `embassy/runner.rs:1082` `embassy/runner.rs:1099` `embassy/runner.rs:1101` `embassy/runner.rs:1134`
4. Issue one function 2 read command with address 0, incrementing mode and length = len, clocking ceil(len/4) words. A bus error breaks out of the loop. Then go back to step 1. The runner's `wake_bus` step does nothing on SPI; it acts only on SDIO. `embassy/runner.rs:1107` `embassy/runner.rs:1109` `embassy/runner.rs:799` `embassy/runner.rs:772` `embassy/spi.rs:279` `embassy/spi.rs:280` `embassy/runner.rs:1042`

- embassy also calls the status-drain routine directly after every WLAN write (queued command, data frame, and the inline command path), using the status returned by that write, without waiting for an interrupt. `embassy/runner.rs:870` `embassy/runner.rs:871` `embassy/runner.rs:928` `embassy/runner.rs:930` `embassy/runner.rs:1431` `embassy/runner.rs:1432`
- RX pool buffers must be 4-byte aligned and hold `RX_BUF_SIZE` = (12-byte SDPCM header + 2 padding + 4-byte BDC header + 4 BDC data offset + 1514 MTU) rounded up to 4. Both are asserted at run time. `embassy/lib.rs:42` `embassy/lib.rs:50` `embassy/lib.rs:60` `embassy/runner.rs:1084` `embassy/runner.rs:1089`

### c-driver

1. Read the 32-bit status register, retrying while it reads 0xFFFFFFFF, at most 1000 times; still 0xFFFFFFFF returns -1. If bit 8 (packet available) is clear: "No packet", clear `had_successful_packet`, return -1. `c-driver/cyw43_ll.c:1215` `c-driver/cyw43_ll.c:1216` `c-driver/cyw43_ll.c:1222` `c-driver/cyw43_ll.c:1227` `c-driver/cyw43_ll.c:1238` `c-driver/cyw43_ll.c:1239`
2. `bytes_pending` = (status >> 9) & 0x7FF. If it is 0, or exceeds `LINK_MTU - GSPI_PACKET_OVERHEAD` (1500 + 30 + 14 - 8 = 1536), or status bit 1 (underflow) is set: write (1 << 0) as one byte to function 1 register `SPI_FRAME_CONTROL` (0x1000D) to abort the F2 read, clear `had_successful_packet`, return -1. `c-driver/cyw43_ll.c:1228` `c-driver/cyw43_ll.c:1229` `c-driver/cyw43_ll.c:1230` `c-driver/cyw43_ll.c:1232` `c-driver/cyw43_ll.c:1208` `c-driver/cyw43_ll.c:1209` `c-driver/cyw43_ll.c:1210` `c-driver/cyw43_ll.c:1211` `c-driver/cyw43_ll.c:1212` `c-driver/cyw43_spi.h:94`
3. Read `bytes_pending` bytes from function 2, address 0, into `spid_buf`; a failed SPI transfer returns its error code. `c-driver/cyw43_ll.c:1242` `c-driver/cyw43_ll.c:1244`
4. Check the first two 16-bit words of the frame (SDPCM length and its complement). Both zero: "No packet zero size header", clear `had_successful_packet`, return -1. Otherwise set `had_successful_packet`; if `hdr[0] ^ hdr[1] != 0xFFFF` warn "hdr mismatch" and return -1; else hand the frame to SDPCM processing. `c-driver/cyw43_ll.c:1250` `c-driver/cyw43_ll.c:1252` `c-driver/cyw43_ll.c:1256` `c-driver/cyw43_ll.c:1257` `c-driver/cyw43_ll.c:1258` `c-driver/cyw43_ll.c:1261`

- Error tolerance: when packet processing returns `CYW43_ERROR_WRONG_PAYLOAD_TYPE` the SPI build ignores it. The comment says it can occur with a lot of traffic over the SPI "and seems to be harmless". The caller loops polling until a poll returns -1. `c-driver/cyw43_ll.c:1272` `c-driver/cyw43_ll.c:1281` `c-driver/cyw43_ll.c:1284`

### whd

`whd_bus_spi_read_frame`: `whd/src/bus_protocols/whd_bus_spi_protocol.c:479`

1. Ensure the bus is up, then read the 32-bit status register repeatedly while it equals 0xFFFFFFFF; a failed read returns the error. `whd/src/bus_protocols/whd_bus_spi_protocol.c:486` `whd/src/bus_protocols/whd_bus_spi_protocol.c:490` `whd/src/bus_protocols/whd_bus_spi_protocol.c:495` `whd/src/bus_protocols/whd_bus_spi_protocol.c:497`
2. If status bit 8 is set and the length field ((status >> 9) & 0x7FF) is 0, or exceeds `WHD_LINK_MTU - sizeof(whd_buffer_header_t)`, or status bit 1 (underflow) is set: write (1 << 0) as one byte to function 1 register `SPI_FRAME_CONTROL` (0x1000D) and return `WHD_NO_PACKET_TO_RECEIVE`. If bit 8 is clear, also return `WHD_NO_PACKET_TO_RECEIVE`, with no abort. `whd/src/bus_protocols/whd_bus_spi_protocol.c:499` `whd/src/bus_protocols/whd_bus_spi_protocol.c:501` `whd/src/bus_protocols/whd_bus_spi_protocol.c:502` `whd/src/bus_protocols/whd_bus_spi_protocol.c:503` `whd/src/bus_protocols/whd_bus_spi_protocol.c:505` `whd/src/bus_protocols/whd_bus_spi_protocol.c:506` `whd/src/bus_protocols/whd_bus_spi_protocol.c:507` `whd/src/bus_protocols/whd_bus_spi_protocol.c:520` `whd/src/bus_protocols/whd_bus_spi_protocol.c:82` `whd/src/bus_protocols/whd_spi.h:29`
3. Allocate an RX buffer of (bytes pending + header overhead). If allocation fails: read just the first 12 bytes of the frame from function 2 into a stack buffer; if more than 12 bytes were pending, write (1 << 0) to `SPI_FRAME_CONTROL` to abort the transfer so that, per whd's comment, dropping of the packet is forced; then update the bus credit from those 12 bytes and return the allocation error. `whd/src/bus_protocols/whd_bus_spi_protocol.c:524` `whd/src/bus_protocols/whd_bus_spi_protocol.c:525` `whd/src/bus_protocols/whd_bus_spi_protocol.c:530` `whd/src/bus_protocols/whd_bus_spi_protocol.c:532` `whd/src/bus_protocols/whd_bus_spi_protocol.c:535` `whd/src/bus_protocols/whd_bus_spi_protocol.c:536` `whd/src/bus_protocols/whd_bus_spi_protocol.c:538` `whd/src/bus_protocols/whd_bus_spi_protocol.c:543`
4. Read the whole frame with one function 2 read (address 0, incrementing, size = buffer size minus header, clocked rounded up to 4 bytes). On SPI transfer failure release the buffer and return the error. The whd thread repeats `read_frame` until it fails or `WHD_THREAD_RX_BOUND` packets have been read. `whd/src/bus_protocols/whd_bus_spi_protocol.c:548` `whd/src/bus_protocols/whd_bus_spi_protocol.c:551` `whd/src/bus_protocols/whd_bus_spi_protocol.c:302` `whd/src/whd_thread.c:179` `whd/src/whd_thread.c:385`

whd's length limit, numerically: `whd/src/bus_protocols/whd_bus_spi_protocol.c:501`

- `WHD_LINK_MTU` = `WHD_PAYLOAD_MTU` (1500) + `WHD_PHYSICAL_HEADER`, where `WHD_PHYSICAL_HEADER` = `WHD_LINK_HEADER` + `WHD_ETHERNET_SIZE` (14). `whd/inc/whd_types.h:252` `whd/inc/whd_types.h:242` `whd/inc/whd_types.h:216` `whd/inc/whd_types.h:231`
- `WHD_LINK_HEADER` = `BDC_HEADER_WITH_PAD` (6) + `BDC_HEADER_OFFSET_TO_DATA` (4) + `SDPCM_HEADER` (8 + 4) + `MAX_BUS_HEADER_SIZE` (4) + `BUFFER_OVERHEAD` (4) = 30, so `WHD_LINK_MTU` = 1544. `whd/inc/whd_types.h:202` `whd/inc/whd_types.h:218` `whd/inc/whd_types.h:219` `whd/inc/whd_types.h:236` `whd/inc/whd_types.h:188` `whd/inc/whd_types.h:195` `whd/inc/whd_types.h:197` `whd/inc/whd_types.h:211`
- `whd_buffer_header_t` is a packed struct of a queue pointer (`void *`) plus a 4-byte bus header. With 4-byte pointers the limit is 1544 - 8 = 1536 bytes, the same number c-driver hard-codes (1500 + 30 + 14 - 8). `whd/src/include/whd_types_int.h:194` `whd/src/include/whd_types_int.h:199` `whd/src/include/whd_types_int.h:200` `whd/inc/whd_types.h:1118` `whd/inc/whd_types.h:139` `c-driver/cyw43_ll.c:1212`
- The 4-byte pointer is an assumption about the host, not fixed by the source (whd's own `BUFFER_OVERHEAD` comment says 4 = sizeof(void *)). A 64-bit host would give 1544 - 12. `whd/inc/whd_types.h:211`

### Writing a packet (for comparison)

- A WLAN frame is sent as one function 2 write command: address 0, incrementing, length = exact frame length, followed by the frame padded to a 4-byte boundary. `embassy/spi.rs:290` `c-driver/cyw43_ll.c:848` `c-driver/cyw43_ll.c:48` `whd/src/bus_protocols/whd_bus_spi_protocol.c:273` `whd/src/bus_protocols/whd_bus_spi_protocol.c:334`
- embassy rounds the frame length itself up to 4 before building the command, so the command length is the padded length for data frames. `embassy/runner.rs:924`

| Topic | embassy | c-driver | whd | Citations |
|---|---|---|---|---|
| Wait for F2 ready before each F2 write | Not found; writes without checking F2 RX ready. | Not found; the send path checks only SDPCM credits and flow control. | Polls the status register until bit 5 (F2 RX ready) is set, up to `F2_READY_TIMEOUT_LOOPS` = 1000 reads; else fails with `WHD_TIMEOUT` ("Timeout waiting for data FIFO to be ready"). Present in both the buffer path and the byte path; the two log the timeout at different levels (error vs debug). | `embassy/spi.rs:287` `c-driver/cyw43_ll.c:779` `whd/src/bus_protocols/whd_bus_spi_protocol.c:313` `whd/src/bus_protocols/whd_bus_spi_protocol.c:315` `whd/src/bus_protocols/whd_bus_spi_protocol.c:316` `whd/src/bus_protocols/whd_bus_spi_protocol.c:61` `whd/src/bus_protocols/whd_bus_spi_protocol.c:327` `whd/src/bus_protocols/whd_bus_spi_protocol.c:328` `whd/src/bus_protocols/whd_bus_spi_protocol.c:988` `whd/src/bus_protocols/whd_bus_spi_protocol.c:990` `whd/src/bus_protocols/whd_bus_spi_protocol.c:1004` `whd/src/bus_protocols/whd_bus_spi_protocol.c:1005` |
| Size check | Not found. | Not found. | The byte-transfer path refuses a function 2 write whose gSPI size differs from the first 16-bit word of the payload (the SDPCM length), returning `WHD_SPI_SIZE_MISMATCH`. | `embassy/spi.rs:287` `c-driver/cyw43_spi.c:89` `whd/src/bus_protocols/whd_bus_spi_protocol.c:976` `whd/src/bus_protocols/whd_bus_spi_protocol.c:980` `whd/src/bus_protocols/whd_bus_spi_protocol.c:983` |
| Buffer alignment | Uses A4-aligned buffers. | Asserts `spid_buf` is 4-byte aligned. | Needs the command word 4-byte aligned in memory: if the packet header address is not 4-byte aligned it first copies the frame into a pre-allocated aligned buffer of `WHD_LINK_MTU` bytes. | `embassy/spi.rs:287` `embassy/util.rs:87` `c-driver/cyw43_ll.c:1511` `whd/src/bus_protocols/whd_bus_spi_protocol.c:341` `whd/src/bus_protocols/whd_bus_spi_protocol.c:346` `whd/src/bus_protocols/whd_bus_spi_protocol.c:741` |
| Poke | Pokes only on SDIO. | Mailbox poke compiled out on SPI. | The SPI poke function is an empty stub returning success (on SDIO a poke writes a mailbox bit). | `embassy/runner.rs:942` `c-driver/cyw43_ll.c:789` `whd/src/bus_protocols/whd_bus_spi_protocol.c:384` `whd/src/bus_protocols/whd_bus_spi_protocol.c:386` |

- c-driver's SPI build limits CLM download chunks to 1024 bytes (1024 + 512 on SDIO) and pads writes to 4 bytes (64 on SDIO). `c-driver/cyw43_ll.c:1485` `c-driver/cyw43_ll.c:1486` `c-driver/cyw43_ll.c:48` `c-driver/cyw43_ll.c:50`
