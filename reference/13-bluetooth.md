# Bluetooth over the shared bus

How embassy and pico-sdk (on top of c-driver) carry Bluetooth HCI traffic over the WiFi bus of the CYW43439: registers, ring buffers, record header, patch download, handshake and interrupts. whd and linux are covered where they define or handle the same registers and bits.

## Registers and bits

### Where the code lives
| Driver | What it contains | Citations |
|---|---|---|
| embassy | Full transport: patch download, ring buffers, wake handshake. Enabled by the cargo feature `bluetooth`. `new_with_bluetooth()` takes a separate patch slice and passes `Some(bluetooth_firmware)` to `Runner::init`, which calls `init_bluetooth` after WiFi chip init. | `embassy/bluetooth.rs:218` `embassy/lib.rs:12` `embassy/lib.rs:663` `embassy/lib.rs:696` `embassy/runner.rs:703` `embassy/runner.rs:708` |
| pico-sdk | Full transport, in `cybt_shared_bus.c` and `cybt_shared_bus_driver.c`. | `pico-sdk/cybt_shared_bus.c:103` `pico-sdk/cybt_shared_bus_driver.c:284` |
| pico-sdk (`cybt_shared_bus.h`) | Not a header in these sources: the file holds only the text "404: Not Found", so it defines nothing. | `pico-sdk/cybt_shared_bus.h:1` |
| c-driver | Declares the API only: `cyw43_btbus_init(cyw43_ll_t *self)`, `cyw43_btbus_read(uint8_t *buf, uint32_t max_buf_size, uint32_t *size)`, `cyw43_btbus_write(uint8_t *buf, uint32_t size)`. Supplies backplane helpers and the interrupt check. The transport itself is in pico-sdk. | `c-driver/cyw43_btbus.h:19` `c-driver/cyw43_btbus.h:20` `c-driver/cyw43_btbus.h:21` |
| whd | No ring-buffer, record-header or patch-download code. Has register addresses, an info getter (`whd_get_bt_info`), an attach/detach pair that stores a Bluetooth interrupt callback, the FC_CHANGE dispatch to that callback on SPI and SDIO, and one sleep-path test of the callback. | `whd/src/whd_wifi_api.c:102` `whd/src/whd_wifi_api.c:487` `whd/src/bus_protocols/whd_bus.c:61` `whd/src/bus_protocols/whd_bus.c:88` `whd/src/whd_chip.c:884` |
| linux | No Bluetooth shared-bus code. No match under linux/ for btsdio, bt_ctrl_reg, host_ctrl_reg, h2b, b2h, host2bt, bt2host, or for the addresses 0x18000c7c, 0x18000d6c, 0x18000d68, 0x18000c78. linux does define and handle I_HMB_FC_CHANGE, as WLAN flow control (see Interrupt handling). | `linux/brcmfmac/sdio.c:268` |

c-driver build switches and entry points:

- c-driver gates the shared-bus transport on `CYW43_ENABLE_BLUETOOTH` (default 0). `c-driver/cyw43_config.h:51` `c-driver/cyw43_config.h:53`
- A separate `CYW43_ENABLE_BLUETOOTH_OVER_UART` (default 0) selects an HCI-UART transport in `cyw43_bthci_uart.c`. That is a different mechanism, not the shared bus. `c-driver/cyw43_config.h:59` `c-driver/cyw43_bthci_uart.c:9`
- With `CYW43_ENABLE_BLUETOOTH` set, c-driver's default WiFi firmware include name changes from `firmware/w43439A0_7_95_49_00_combined.h` to `firmware/wb43439A0_7_95_49_00_combined.h` (`CYW43_CHIPSET_FIRMWARE_INCLUDE_FILE`). `c-driver/cyw43_config.h:65` `c-driver/cyw43_config.h:66` `c-driver/cyw43_config.h:67` `c-driver/cyw43_config.h:69`
- `cyw43_t` has a `bool bt_loaded`, present only with `CYW43_ENABLE_BLUETOOTH`. c-driver sets it false in `cyw43_init` and again after `cyw43_ll_deinit`, and true after a successful `cyw43_btbus_init`. `c-driver/cyw43.h:139` `c-driver/cyw43_ctrl.c:90` `c-driver/cyw43_ctrl.c:118` `c-driver/cyw43_ctrl.c:822`
- `cyw43_bluetooth_hci_init/read/write` each call `cyw43_ensure_bt_up`. That brings WiFi up (`cyw43_ensure_up`), then calls `cyw43_btbus_init` once and sets `bt_loaded = true` on success. read/write then call `cyw43_btbus_read` / `cyw43_btbus_write`. `c-driver/cyw43_ctrl.c:816` `c-driver/cyw43_ctrl.c:820` `c-driver/cyw43_ctrl.c:822` `c-driver/cyw43_ctrl.c:841` `c-driver/cyw43_ctrl.c:856`
- `cyw43_ensure_bt_up` holds `CYW43_THREAD_ENTER` / `CYW43_THREAD_EXIT` around the bring-up. `c-driver/cyw43_ctrl.c:817` `c-driver/cyw43_ctrl.c:825`
- c-driver's public API: `cyw43_bluetooth_hci_init()`; `cyw43_bluetooth_hci_read(buf, max_size, len)`, where `len` returns the data length including an initial 4-byte header whose last byte is the packet type; `cyw43_bluetooth_hci_write(buf, len)`, where the buffer must include that 4-byte header. `c-driver/cyw43.h:812` `c-driver/cyw43.h:819` `c-driver/cyw43.h:826` `c-driver/cyw43.h:829` `c-driver/cyw43.h:835` `c-driver/cyw43.h:838`
- The callback `cyw43_bluetooth_hci_process(void)` is declared and called by c-driver but not defined in these sources. `c-driver/cyw43.h:843` `c-driver/cyw43_ctrl.c:208`

c-driver backplane helpers used by the pico-sdk transport. The definitions of all four, and of `cyw43_ll_bt_has_work`, are compiled only with `CYW43_ENABLE_BLUETOOTH`; the declarations in `cyw43_ll.h` are not guarded. `c-driver/cyw43_ll.c:2540` `c-driver/cyw43_ll.h:317` `c-driver/cyw43_ll.h:326`

| Helper | What c-driver does | Citations |
|---|---|---|
| `cyw43_ll_write_backplane_reg`, `cyw43_ll_read_backplane_reg` | One 4-byte `cyw43_write_backplane` / `cyw43_read_backplane` call (32-bit register). | `c-driver/cyw43_ll.h:326` `c-driver/cyw43_ll.h:327` `c-driver/cyw43_ll.c:2552` `c-driver/cyw43_ll.c:2554` `c-driver/cyw43_ll.c:2559` |
| `cyw43_ll_write_backplane_mem` | Loops, splitting at each 0x8000 window boundary (`BACKPLANE_ADDR_MASK` 0x7fff). Sets the window. Writes with `SBSDIO_SB_ACCESS_2_4B_FLAG` (0x08000) OR-ed into the address. Only prints on a failed write. Always returns 0. | `c-driver/cyw43_ll.h:328` `c-driver/cyw43_ll.c:2565` `c-driver/cyw43_ll.c:2566` `c-driver/cyw43_ll.c:2569` `c-driver/cyw43_ll.c:2571` `c-driver/cyw43_ll.c:123` `c-driver/cyw43_ll.c:126` |
| `cyw43_ll_read_backplane_mem` | One transfer. Asserts `len <= CYW43_BUS_MAX_BLOCK_SIZE` and that the read does not cross a window. | `c-driver/cyw43_ll.h:329` `c-driver/cyw43_ll.c:2581` `c-driver/cyw43_ll.c:2583` `c-driver/cyw43_ll.c:2584` |
| both mem helpers | Set the backplane window back to `CHIPCOMMON_BASE_ADDRESS` (0x18000000) afterwards. | `c-driver/cyw43_ll.c:2577` `c-driver/cyw43_ll.c:2578` `c-driver/cyw43_ll.c:2587` `c-driver/cyw43_ll.c:119` |
| compile gate | `CYW43_ENABLE_BLUETOOTH`, around the definitions only. | `c-driver/cyw43_ll.c:2540` |

embassy's `bp_read` / `bp_write` chunk to 64 bytes and to the 0x8000 window themselves, and do not restore the window afterwards in these functions. `embassy/spi.rs:311` `embassy/spi.rs:354` `embassy/consts.rs:109` `embassy/consts.rs:112`

### Bluetooth registers (backplane, 32-bit)
| Name | Address | Direction as used | Defined by | Not found in | Citations |
|---|---|---|---|---|---|
| BT_CTRL_REG_ADDR | 0x18000c7c | Controller-to-host status. The host only reads it. | embassy, pico-sdk, whd | c-driver, linux | `embassy/consts.rs:192` `pico-sdk/cybt_shared_bus_driver.c:54` `whd/src/whd_wifi_api.c:102` `embassy/bluetooth.rs:317` `pico-sdk/cybt_shared_bus_driver.c:428` |
| HOST_CTRL_REG_ADDR | 0x18000d6c | Host-to-controller control. The host writes it. | embassy, pico-sdk, whd | c-driver, linux | `embassy/consts.rs:193` `pico-sdk/cybt_shared_bus_driver.c:55` `whd/src/whd_wifi_api.c:103` `embassy/bluetooth.rs:350` `pico-sdk/cybt_shared_bus_driver.c:383` |
| WLAN_RAM_BASE_REG_ADDR | 0x18000d68 | Read once at init. embassy and pico-sdk use the value as the base address of the shared ring-buffer block in WLAN RAM ("btfw ram base"). | embassy, pico-sdk | whd (see below) | `embassy/consts.rs:194` `pico-sdk/cybt_shared_bus_driver.c:56` `embassy/bluetooth.rs:375` `pico-sdk/cybt_shared_bus_driver.c:676` `pico-sdk/cybt_shared_bus_driver.c:681` |
| BT_BUF_REG_ADDR | 0x18000c78 | whd only stores it into `bt_info->bt_buf_reg_addr` and never reads it. What the register holds is not stated in these sources (unverified). | whd | embassy, pico-sdk | `whd/src/whd_wifi_api.c:104` `whd/src/whd_wifi_api.c:500` |
| BT2WLAN_PWRUP_ADDR | 0x640894, an offset in the Bluetooth address space. Absolute address written: 0x19000000 + 0x640894 = 0x19640894. | Host writes 0x03 at init. | embassy, pico-sdk | whd | `embassy/consts.rs:190` `pico-sdk/cybt_shared_bus_driver.c:35` `pico-sdk/cybt_shared_bus_driver.c:31` `pico-sdk/cybt_shared_bus_driver.c:323` `embassy/lib.rs:274` `embassy/bluetooth.rs:221` |

- `BT2WLAN_PWRUP_WAKE` = 0x03. pico-sdk's comment: bit 0 is "WLAN Power UP", bit 1 is "WLAN Wake". The same source comments that the address "is specific to 43012B0". `pico-sdk/cybt_shared_bus_driver.c:33` `pico-sdk/cybt_shared_bus_driver.c:34` `pico-sdk/cybt_shared_bus_driver.c:35` `embassy/consts.rs:189`
- The Bluetooth memory window starts at backplane address 0x19000000: pico-sdk `BTFW_MEM_OFFSET`, embassy `ChipInfo.bluetooth_base_address` for the CYW43439 (embassy lists the same value for CYW4373 and CYW43455). Both drivers add this base to every patch-record destination address. `pico-sdk/cybt_shared_bus_driver.c:31` `pico-sdk/cybt_shared_bus_driver.c:329` `embassy/lib.rs:274` `embassy/lib.rs:306` `embassy/lib.rs:341` `embassy/bluetooth.rs:262`
- embassy asserts the value read from WLAN_RAM_BASE_REG_ADDR is non-zero. pico-sdk does not check it; its `cybt_reg_read` always returns `CYBT_SUCCESS`. `embassy/bluetooth.rs:376` `pico-sdk/cybt_shared_bus_driver.c:676` `pico-sdk/cybt_shared_bus_driver.c:551`
- embassy defines `FUNC_BT = 3` next to `FUNC_BUS` 0, `FUNC_BACKPLANE` 1, `FUNC_WLAN` 2, but its Bluetooth transport never uses bus function 3. All Bluetooth traffic is backplane (function 1) register and memory access. `embassy/consts.rs:6` `embassy/bluetooth.rs:317` `embassy/bluetooth.rs:421` `embassy/bluetooth.rs:487`

### BT_CTRL bits (read by the host)
| Bit | Mask | Name | Meaning as used | Defined by | Citations |
|---|---|---|---|---|---|
| 8 | 1 << 8 | BTSDIO_REG_BT_AWAKE_BITMASK | Both drivers poll it as "Bluetooth controller awake". | embassy, pico-sdk; not defined in whd | `embassy/consts.rs:197` `pico-sdk/cybt_shared_bus_driver.c:84` `embassy/bluetooth.rs:334` `pico-sdk/cybt_shared_bus_driver.c:445` |
| 24 | 1 << 24 | BTSDIO_REG_FW_RDY_BITMASK | Both drivers poll it after the patch download as "Bluetooth firmware ready". | embassy, pico-sdk; not defined in whd | `embassy/consts.rs:200` `pico-sdk/cybt_shared_bus_driver.c:85` `embassy/bluetooth.rs:319` `pico-sdk/cybt_shared_bus_driver.c:434` |

Only bits 8 and 24 of BT_CTRL are named in any of these sources. No other BT_CTRL bit is defined or tested. `pico-sdk/cybt_shared_bus_driver.c:84` `pico-sdk/cybt_shared_bus_driver.c:85` `embassy/consts.rs:197` `embassy/consts.rs:200`

### HOST_CTRL bits (written by the host)
| Bit | Mask | Name | Meaning as used | Citations |
|---|---|---|---|---|
| 1 | 1 << 1 | BTSDIO_REG_DATA_VALID_BITMASK | Host-to-controller notification bit. Both drivers toggle it (XOR) in functions named "toggle interrupt" (`cybt_toggle_bt_intr`, `toggle_intr`); live code never sets it to a fixed level. That the controller reacts to the change and not the level is (inferred) from the toggling; no source states how the controller samples the bit (unverified). | `embassy/consts.rs:196` `pico-sdk/cybt_shared_bus_driver.c:80` `embassy/bluetooth.rs:100` `pico-sdk/cybt_shared_bus_driver.c:402` |
| 17 | 1 << 17 | BTSDIO_REG_WAKE_BT_BITMASK | Both drivers set it before polling BT_AWAKE, as "wake the Bluetooth controller" (from the constant name and its use). | `embassy/consts.rs:198` `pico-sdk/cybt_shared_bus_driver.c:81` `embassy/bluetooth.rs:82` `pico-sdk/cybt_shared_bus_driver.c:454` |
| 24 | 1 << 24 | BTSDIO_REG_SW_RDY_BITMASK | Both drivers set it once at the end of init, as "host software ready" (from the constant name and its use). Same bit position as FW_RDY in BT_CTRL. | `embassy/consts.rs:199` `pico-sdk/cybt_shared_bus_driver.c:82` `embassy/bluetooth.rs:90` `pico-sdk/cybt_shared_bus_driver.c:382` |

- The only HOST_CTRL bits either host sets are 1, 17 and 24. pico-sdk treats any other bit set in its copy of HOST_CTRL as register corruption and panics ("cyw43 btsdio register corruption") in `cybt_toggle_bt_intr`. `pico-sdk/cybt_shared_bus_driver.c:395` `pico-sdk/cybt_shared_bus_driver.c:398`
- embassy has no corruption check; it builds the value only from a local shadow, so other bits cannot appear. `embassy/bluetooth.rs:68`
- Neither driver reads HOST_CTRL back from the chip. pico-sdk's `cybt_reg_read` returns the cached `host_ctrl_cache_reg` for that address and `cybt_reg_write` updates the cache. embassy keeps a `HostCtrl(u32)` shadow and only writes. Both shadows start at 0. `pico-sdk/cybt_shared_bus_driver.c:50` `pico-sdk/cybt_shared_bus_driver.c:538` `pico-sdk/cybt_shared_bus_driver.c:545` `embassy/bluetooth.rs:68` `embassy/bluetooth.rs:71` `embassy/bluetooth.rs:350`
- Because pico-sdk serves the HOST_CTRL read from the cache, its corruption check examines the cached value, not the chip register. `pico-sdk/cybt_shared_bus_driver.c:393` `pico-sdk/cybt_shared_bus_driver.c:395` `pico-sdk/cybt_shared_bus_driver.c:545`
- embassy documents the write-only shadow as mirroring pico-sdk's Infineon-supplied WiFi/BT corruption fix (commit 8dbc6f20, #1362): backplane reads are not authoritative for host-owned state when both radios are fully utilised. pico-sdk's own comment says register corruption occurs "if both wifi and bluetooth are fully utilised". `embassy/bluetooth.rs:64` `pico-sdk/cybt_shared_bus_driver.c:16`

### whd `whd_bt_info`

`whd_get_bt_info` zeroes and fills `struct whd_bt_info` (four `uint32_t`, size 16). `whd/src/include/whd_int.h:104` `whd/src/whd_wifi_api.c:497`

| Offset | Size | Field | Value whd stores | Citations |
|---|---|---|---|---|
| 0 | 4 | bt_buf_reg_addr | BT_BUF_REG_ADDR 0x18000c78 | `whd/src/include/whd_int.h:106` `whd/src/whd_wifi_api.c:500` `whd/src/whd_wifi_api.c:104` |
| 4 | 4 | host_ctrl_reg_addr | HOST_CTRL_REG_ADDR 0x18000d6c | `whd/src/whd_wifi_api.c:499` |
| 8 | 4 | bt_ctrl_reg_addr | BT_CTRL_REG_ADDR 0x18000c7c | `whd/src/whd_wifi_api.c:498` |
| 12 | 4 | wlan_buf_addr | 32-bit result of reading the named variable (iovar) `IOVAR_STR_BTADDR` "bus:btsdiobufaddr". Left 0 if the read fails; the function still returns `WHD_SUCCESS`. | `whd/src/include/whd_int.h:109` `whd/src/whd_wifi_api.c:501` `whd/src/whd_wifi_api.c:504` `whd/src/whd_wifi_api.c:506` `whd/src/include/whd_wlioctl.h:1065` |

Where each driver gets the ring-buffer base:

| Driver | Source of the base address | Citations |
|---|---|---|
| embassy | Reads register 0x18000d68. No named variable. | `embassy/bluetooth.rs:375` |
| pico-sdk | Reads register 0x18000d68. No named variable. | `pico-sdk/cybt_shared_bus_driver.c:676` |
| whd | Does not define 0x18000d68. Gets `wlan_buf_addr` from the named variable "bus:btsdiobufaddr". | `whd/src/whd_wifi_api.c:501` `whd/src/include/whd_wlioctl.h:1065` `whd/src/whd_wifi_api.c:104` |

### Interrupt-related registers
| Register | Address | Bits used for Bluetooth | Citations |
|---|---|---|---|
| SDIO_INT_STATUS | SDIO core base 0x18002000 + 0x20 = 0x18002020 (backplane, 32-bit). 0x18002000 is the CYW43439 base; embassy lists other bases for other chips. | Bit 5, `I_HMB_FC_CHANGE` (1 << 5): embassy, c-driver and whd use it as the Bluetooth-to-host interrupt. | `c-driver/cyw43_ll.c:117` `c-driver/cyw43_ll.c:120` `c-driver/cyw43_ll.c:129` `embassy/consts.rs:72` `embassy/consts.rs:74` `embassy/lib.rs:276` `embassy/lib.rs:308` `embassy/lib.rs:343` `whd/src/bus_protocols/whd_sdio.h:116` `whd/src/bus_protocols/whd_sdio.h:32` |
| SDIO_INT_HOST_MASK | SDIO core base + 0x24 = 0x18002024 | With Bluetooth enabled on SPI, embassy, c-driver and whd write `I_HMB_FC_CHANGE` (0x20) to it. | `c-driver/cyw43_ll.c:130` `c-driver/cyw43_ll.c:1834` `embassy/consts.rs:75` `embassy/runner.rs:664` `embassy/runner.rs:665` `whd/src/bus_protocols/whd_bus_spi_protocol.c:1127` `whd/src/bus_protocols/whd_bus_spi_protocol.c:1128` `whd/src/bus_protocols/whd_sdio.h:36` |
| SPI interrupt enable | Bus function, address 0x0006, 16-bit | `F1_INTR` = 0x2000, added to the enable mask only when Bluetooth is enabled. | `c-driver/cyw43_spi.h:72` `c-driver/cyw43_spi.h:26` `c-driver/cyw43_ll.c:1626` `c-driver/cyw43_ll.c:1628` `embassy/consts.rs:152` `embassy/consts.rs:13` `embassy/spi.rs:268` `embassy/runner.rs:660` `whd/src/bus_protocols/whd_spi.h:97` `whd/src/bus_protocols/whd_spi.h:37` `whd/src/bus_protocols/whd_bus_spi_protocol.c:1119` |

- The pico-sdk files never touch SDIO_INT_STATUS; the check is in c-driver (`cyw43_ll_bt_has_work`). `c-driver/cyw43_ll.c:2542`
- linux defines the same bit with a different meaning: `I_HMB_FC_CHANGE` = `I_HMB_SW1`, "Flow Control State Changed". `linux/brcmfmac/sdio.c:268`
- In c-driver and embassy the Bluetooth write of `I_HMB_FC_CHANGE` (0x20) to SDIO_INT_HOST_MASK comes after, and replaces, an earlier write of `I_HMB_SW_MASK` (0xF0) to the same register. The register is written whole, not OR-ed. `c-driver/cyw43_ll.c:1822` `c-driver/cyw43_ll.c:1834` `embassy/runner.rs:616` `embassy/runner.rs:662`

Names of SDIO_INT_STATUS bits 4 to 7 per driver:

| Bit | whd | embassy | c-driver | linux | Citations |
|---|---|---|---|---|---|
| 4 | I_HMB_FC_STATE | not named | not named | I_HMB_FC_STATE = I_HMB_SW0, "Flow Control State" | `whd/src/bus_protocols/whd_sdio.h:115` `linux/brcmfmac/sdio.c:267` |
| 5 | I_HMB_FC_CHANGE | I_HMB_FC_CHANGE | I_HMB_FC_CHANGE | I_HMB_FC_CHANGE = I_HMB_SW1, "Flow Control State Changed" | `whd/src/bus_protocols/whd_sdio.h:116` `embassy/consts.rs:72` `c-driver/cyw43_ll.c:117` `linux/brcmfmac/sdio.c:268` |
| 6 | I_HMB_FRAME_IND | not named | not named | I_HMB_FRAME_IND = I_HMB_SW2 | `whd/src/bus_protocols/whd_sdio.h:117` `linux/brcmfmac/sdio.c:269` |
| 7 | I_HMB_HOST_INT | I_HMB_HOST_INT | not named | I_HMB_HOST_INT = I_HMB_SW3 | `whd/src/bus_protocols/whd_sdio.h:118` `embassy/consts.rs:89` `linux/brcmfmac/sdio.c:270` |
| 4-7 | I_HMB_SW_MASK = 0xF0 | I_HMB_SW_MASK 0xF0 | I_HMB_SW_MASK 0xf0 | I_HMB_SW_MASK 0x000000f0 | `whd/src/bus_protocols/whd_sdio.h:113` `embassy/consts.rs:71` `c-driver/cyw43_ll.c:116` `linux/brcmfmac/sdio.c:211` |

SPI interrupt enable set written with Bluetooth:

| Driver | Enable mask | Citations |
|---|---|---|
| c-driver | F1_INTR, F2_F3_FIFO_RD_UNDERFLOW, F2_F3_FIFO_WR_OVERFLOW, COMMAND_ERROR, DATA_ERROR, F2_PACKET_AVAILABLE, F1_OVERFLOW (OR-ed). | `c-driver/cyw43_ll.c:1623` `c-driver/cyw43_ll.c:1626` |
| whd | Same set. Its comment says the reason for enabling F1 INT is so that, in SPI, the interrupt that BT FW raises with HMB_FC_CHANGED can be received. | `whd/src/bus_protocols/whd_bus_spi_protocol.c:1116` `whd/src/bus_protocols/whd_bus_spi_protocol.c:1119` |
| embassy | Writes the same set in `SpiBus::init`; `Runner::init` later overwrites the register with only IRQ_F2_PACKET_AVAILABLE OR IRQ_F1_INTR. | `embassy/spi.rs:261` `embassy/spi.rs:268` `embassy/spi.rs:270` `embassy/runner.rs:658` `embassy/runner.rs:660` `embassy/runner.rs:671` |

### Bus settings the transport depends on

c-driver and embassy configure a response-delay pad for backplane (F1) reads on gSPI. Every ring-buffer and index read goes through this path. `c-driver/cyw43_ll.c:1612` `embassy/spi.rs:245` `embassy/spi.rs:330`

| Driver | Pad | How it is set | Citations |
|---|---|---|---|
| c-driver | `CYW43_BACKPLANE_READ_PAD_LEN_BYTES` = 16 on SPI; 0 on SDIO builds. | Written to `SPI_RESP_DELAY_F1` (bus function address 0x001d). | `c-driver/cyw43_spi.h:33` `c-driver/cyw43_ll.c:1612` `c-driver/cyw43_ll.h:194` `c-driver/cyw43_ll.h:198` |
| embassy | `WHD_BUS_SPI_BACKPLANE_READ_PADD_SIZE` = 4 (one word skipped in `bp_read`). | Written to `SPI_RESP_DELAY_F1` (0x001d). | `embassy/consts.rs:186` `embassy/consts.rs:187` `embassy/spi.rs:245` `embassy/spi.rs:330` |
| whd | `WHD_BUS_SPI_BACKPLANE_READ_PADD_SIZE` = 4, the constant embassy copies. | Defines `SPI_RESP_DELAY_F1` 0x001d, but no write of it was found in whd/src. whd sets a 4-byte delay through the `SPI_RESPONSE_DELAY` byte of the bus control register. | `whd/src/bus_protocols/whd_spi.h:44` `whd/src/bus_protocols/whd_bus_spi_protocol.h:53` `whd/src/bus_protocols/whd_bus_spi_protocol.c:623` |

F2 watermark read-back check:

| Driver | Check | Citations |
|---|---|---|
| c-driver | Only with `CYW43_ENABLE_BLUETOOTH`, during bus init: write 0x10 to `SDIO_FUNCTION2_WATERMARK` (0x10008), read it back, return `-CYW43_EIO` if it is not 0x10 ("check we can set the watermark"). 0x10 is not the final value: later in the same init c-driver writes `SPI_F2_WATERMARK` (32) to the register on SPI, `SDIO_F2_WATERMARK` on SDIO. | `c-driver/cyw43_ll.c:108` `c-driver/cyw43_ll.c:1733` `c-driver/cyw43_ll.c:1735` `c-driver/cyw43_ll.c:1737` `c-driver/cyw43_ll.c:1738` `c-driver/cyw43_ll.c:148` `c-driver/cyw43_ll.c:1829` `c-driver/cyw43_ll.c:1838` |
| embassy | Same write and read-back on its SPI branch (`REG_BACKPLANE_FUNCTION2_WATERMARK` = 0x10008, value 0x10), on every SPI init and not gated on Bluetooth. Fails with `assert!(watermark == 0x10)`. Comment: "Not present in whd driver". 0x10 is not the final value: later in the same init the SPI branch writes `SPI_F2_WATERMARK` (0x20) to the same register. | `embassy/consts.rs:58` `embassy/runner.rs:484` `embassy/runner.rs:487` `embassy/runner.rs:489` `embassy/runner.rs:491` `embassy/consts.rs:106` `embassy/runner.rs:677` |

### whd SDIO sleep-register bits with Bluetooth names

whd uses them only for other chips (list below), not the CYW43439. Not found in the embassy or pico-sdk Bluetooth code. `whd/src/whd_chip.c:1209` `whd/src/whd_chip.c:1315` `whd/src/whd_chip.c:1376`

| Register (sdiorev31) | Bit | Name | Citations |
|---|---|---|---|
| SDIO_WAKEUP_CTRL | 2 | SBSDIO_WCTRL_BT_WAKE_TILL_ALP_AVAIL | `whd/src/bus_protocols/whd_sdio.h:243` |
| SDIO_WAKEUP_CTRL | 3 | SBSDIO_WCTRL_BT_WAKE_TILL_HT_AVAIL | `whd/src/bus_protocols/whd_sdio.h:244` |
| SDIO_WAKEUP_CTRL | 5 | SBSDIO_WCTRL_BT_DISABLE_AUTOSET_KSO | `whd/src/bus_protocols/whd_sdio.h:246` |
| SDIO_SLEEP_CSR | 2 | SBSDIO_SLPCSR_KEEP_BT_KSO | `whd/src/bus_protocols/whd_sdio.h:252` |
| SDIO_SLEEP_CSR | 3 | SBSDIO_SLPCSR_BT_DEVON | `whd/src/bus_protocols/whd_sdio.h:253` |

- whd uses three of them, only when built with `CP_OVER_SDIO`. It ORs BT_WAKE_TILL_ALP_AVAIL into SDIO_WAKEUP_CTRL for chips 43012, 0x4373, 55560, 55500, 55530, 43022. KEEP_BT_KSO and BT_DEVON replace the WL bits in the KSO write and compare for chips 55500 and 55530. `whd/src/whd_chip.c:1209` `whd/src/whd_chip.c:1217` `whd/src/whd_chip.c:1218` `whd/src/whd_chip.c:1314` `whd/src/whd_chip.c:1317` `whd/src/whd_chip.c:1375` `whd/src/whd_chip.c:1378`
- embassy defines only the WL bits (`SBSDIO_SLPCSR_KEEP_WL_KS` bit 0, `SBSDIO_SLPCSR_WL_DEVON` bit 1). `embassy/consts.rs:84` `embassy/consts.rs:85`

## Ring-buffer block and index rules per driver

### Layout

All offsets are relative to base = the value read from WLAN_RAM_BASE_REG_ADDR. `pico-sdk/cybt_shared_bus_driver.c:685` `embassy/bluetooth.rs:420`

| Offset | Size | Name | Use by the drivers | Citations |
|---|---|---|---|---|
| 0 (0x0000) | 4096 (0x1000) | Host-to-controller data ring (`BTSDIO_OFFSET_HOST_WRITE_BUF` = 0) | Host writes records here. | `pico-sdk/cybt_shared_bus_driver.c:87` `pico-sdk/cybt_shared_bus_driver.c:685` `embassy/consts.rs:203` `embassy/bluetooth.rs:420` |
| 4096 (0x1000) | 4096 (0x1000) | Controller-to-host data ring (`BTSDIO_OFFSET_HOST_READ_BUF` = `BTSDIO_FWBUF_SIZE`) | Host reads records here. | `pico-sdk/cybt_shared_bus_driver.c:88` `pico-sdk/cybt_shared_bus_driver.c:686` `embassy/consts.rs:204` `embassy/bluetooth.rs:486` |
| 8192 (0x2000) | 4 | HOST2BT_IN | Host write position in the host-to-controller ring. | `pico-sdk/cybt_shared_bus_driver.c:37` `pico-sdk/cybt_shared_bus_driver.c:689` `embassy/consts.rs:206` |
| 8196 (0x2004) | 4 | HOST2BT_OUT | Read by the host before a transmit to compute free space. Controller's read position in the host-to-controller ring (inferred). | `pico-sdk/cybt_shared_bus_driver.c:38` `pico-sdk/cybt_shared_bus_driver.c:690` `pico-sdk/cybt_shared_bus.c:206` `embassy/consts.rs:207` `embassy/bluetooth.rs:401` |
| 8200 (0x2008) | 4 | BT2HOST_IN | Read by the host before a receive to compute the used count. Controller's write position in the controller-to-host ring (inferred). | `pico-sdk/cybt_shared_bus_driver.c:39` `pico-sdk/cybt_shared_bus_driver.c:691` `pico-sdk/cybt_shared_bus.c:260` `embassy/consts.rs:208` `embassy/bluetooth.rs:478` |
| 8204 (0x200C) | 4 | BT2HOST_OUT | Host read position in the controller-to-host ring. | `pico-sdk/cybt_shared_bus_driver.c:40` `pico-sdk/cybt_shared_bus_driver.c:692` `embassy/consts.rs:209` |

- `BTSDIO_FWBUF_SIZE` = 0x1000 (4096 bytes) is the size of each ring. `pico-sdk/cybt_shared_bus_driver.h:10` `embassy/consts.rs:202`
- The four indexes are contiguous 32-bit words in the order H2B_IN, H2B_OUT, B2H_IN, B2H_OUT. pico-sdk fetches all four with one 16-byte memory read starting at H2B_IN into a `uint32_t[4]` and unpacks `buf[0..3]` in that order into `cybt_fw_membuf_index_t` (four `uint32_t` at offsets 0, 4, 8, 12; size 16). `pico-sdk/cybt_shared_bus_driver.c:502` `pico-sdk/cybt_shared_bus_driver.c:504` `pico-sdk/cybt_shared_bus_driver.c:506` `pico-sdk/cybt_shared_bus_driver.c:509` `pico-sdk/cybt_shared_bus_driver.h:52` `pico-sdk/cybt_shared_bus_driver.h:57`
- embassy never reads the four as a block. It reads only the one index it needs (HOST2BT_OUT before a transmit) with a single `bp_read32`. `embassy/bluetooth.rs:401`
- Byte order of the index words is not stated in any source. pico-sdk uses them in host order after a raw memory read on a little-endian MCU; embassy goes through `bp_read32` / `bp_write32`. Little-endian is (inferred). `pico-sdk/cybt_shared_bus_driver.c:506` `embassy/bluetooth.rs:401`

### Index ownership and initialisation

- At initialisation both drivers write 0 to all four indexes, including H2B_OUT and B2H_IN, which the host does not write again (next bullets), in the order H2B_IN, H2B_OUT, B2H_IN, B2H_OUT. `pico-sdk/cybt_shared_bus_driver.c:695` `pico-sdk/cybt_shared_bus_driver.c:698` `embassy/bluetooth.rs:378` `embassy/bluetooth.rs:381`
- During operation the host writes only HOST2BT_IN and BT2HOST_OUT. pico-sdk enforces this: `cybt_reg_write_idx` asserts the index is `H2B_BUF_IN_ADDR_IDX` or `B2H_BUF_OUT_ADDR_IDX`. embassy writes HOST2BT_IN after a transmit and BT2HOST_OUT after a receive. `pico-sdk/cybt_shared_bus_driver.c:639` `pico-sdk/cybt_shared_bus.c:237` `pico-sdk/cybt_shared_bus.c:307` `embassy/bluetooth.rs:441` `embassy/bluetooth.rs:518`
- After initialisation the host only reads HOST2BT_OUT and BT2HOST_IN: embassy reads HOST2BT_OUT before a transmit and BT2HOST_IN before a receive, and no host code writes them. That the controller advances these two, and which side owns them, is (inferred); no source states it (unverified). `embassy/bluetooth.rs:401` `embassy/bluetooth.rs:478` `pico-sdk/cybt_shared_bus.c:206` `pico-sdk/cybt_shared_bus.c:260`

### Rules per driver
| Rule | pico-sdk | embassy | Citations |
|---|---|---|---|
| Index range | Index values are byte offsets 0..4095 (0x0FFF). Asserts each of the four values read is < `BTSDIO_FWBUF_SIZE`. Refuses to write an index >= `BTSDIO_FWBUF_SIZE`. | No range check on an index read from the chip. Reduces differences modulo 0x1000. | `pico-sdk/cybt_shared_bus_driver.c:527` `pico-sdk/cybt_shared_bus_driver.c:530` `pico-sdk/cybt_shared_bus_driver.c:640` `pico-sdk/cybt_shared_bus_driver.c:641` `embassy/bluetooth.rs:402` |
| Ring access direction | Asserts `mem_idx == H2B_BUF_ADDR_IDX` on write and `== B2H_BUF_ADDR_IDX` on read, and `offset + data_len <= BTSDIO_FWBUF_SIZE` on both. | Same usage, no assertions. | `pico-sdk/cybt_shared_bus_driver.c:650` `pico-sdk/cybt_shared_bus_driver.c:651` `pico-sdk/cybt_shared_bus_driver.c:664` `pico-sdk/cybt_shared_bus_driver.c:665` `embassy/bluetooth.rs:420` |
| Host copy of indexes | Re-reads all four from the chip at the start of every read and every write. Keeps no host-side copy apart from a debug `last_buf_index`. | Keeps host-side copies of the two host-owned indexes (`h2b_write_pointer`, `b2h_read_pointer`, both starting at 0) and never reads them back from the chip. | `pico-sdk/cybt_shared_bus.c:205` `pico-sdk/cybt_shared_bus.c:259` `pico-sdk/cybt_shared_bus_driver.c:523` `embassy/bluetooth.rs:56` |
| Wrap | Bit mask: `value & (BTSDIO_FWBUF_SIZE - 1)`. | Remainder: `value % BTSDIO_FWBUF_SIZE`. Same result; the size is a power of two. | `pico-sdk/cybt_shared_bus.c:39` `pico-sdk/cybt_shared_bus.c:236` `pico-sdk/cybt_shared_bus.c:305` `embassy/bluetooth.rs:422` |
| Used count (receive) | `CIRC_BUF_CNT(in, out)` = `(in - out) & (BTSDIO_FWBUF_SIZE - 1)`, called as `CIRC_BUF_CNT(bt2host_in, bt2host_out)` with both values freshly read from the chip. | `write_pointer.wrapping_sub(self.b2h_read_pointer) % BTSDIO_FWBUF_SIZE`; `write_pointer` is BT2HOST_IN from the chip, `b2h_read_pointer` is the host's cached copy. | `pico-sdk/cybt_shared_bus.c:39` `pico-sdk/cybt_shared_bus.c:260` `embassy/bluetooth.rs:479` |
| Free space (transmit) | `CIRC_BUF_SPACE(in, out)` = `CIRC_BUF_CNT(out, in + 4)` = `(out - (in + 4)) & 0xFFF`. Four bytes are always kept free: an empty ring reports 4092 bytes and in == out always means empty. | Same formula: `read_pointer.wrapping_sub(self.h2b_write_pointer + 4) % BTSDIO_FWBUF_SIZE`; `read_pointer` is HOST2BT_OUT from the chip, `h2b_write_pointer` is cached. | `pico-sdk/cybt_shared_bus.c:39` `pico-sdk/cybt_shared_bus.c:40` `pico-sdk/cybt_shared_bus.c:206` `embassy/bluetooth.rs:402` |
| Record does not fit | Accepts a transmit when the rounded record length (header + padded payload) is <= free space. Otherwise asserts, then returns `CYBT_ERR_QUEUE_FULL`. `cyw43_btbus_write` ignores that return value and returns 0. | Same test (`available < total_len`), made after `try_receive` has borrowed the packet at the head of the channel. Logs a warning ("bluetooth tx queue full, retrying"), yields and returns without calling `receive_done`, which only the success path reaches. `hci_write` has no retry loop; the runner calls it again each time `tx_chan.poll_receive` reports a packet. `try_receive` returns the slot at the head without advancing; only `receive_done` advances the head (embassy-sync `zerocopy_channel.rs:234-245`, `:332-334`, `:405-415` at the same embassy commit; that crate is outside the source folder). So the packet stays queued and is offered again. | `pico-sdk/cybt_shared_bus.c:207` `pico-sdk/cybt_shared_bus.c:208` `pico-sdk/cybt_shared_bus.c:209` `pico-sdk/cybt_shared_bus.c:350` `embassy/bluetooth.rs:403` `embassy/bluetooth.rs:404` `embassy/bluetooth.rs:408` `embassy/bluetooth.rs:409` `embassy/bluetooth.rs:394` `embassy/bluetooth.rs:447` `embassy/runner.rs:851` `embassy/runner.rs:934` |
| Address bookkeeping | Precomputes six absolute addresses in a `cybt_fw_membuf_info_t` (host2bt_buf, host2bt_in, host2bt_out, bt2host_buf, bt2host_in, bt2host_out). Callers use an index enum, `H2B_BUF_ADDR_IDX` = 0x10 to `B2H_BUF_OUT_ADDR_IDX` = 0x15. | Stores only the base and adds constant offsets at each use. | `pico-sdk/cybt_shared_bus_driver.c:58` `pico-sdk/cybt_shared_bus_driver.c:65` `pico-sdk/cybt_shared_bus_driver.c:685` `pico-sdk/cybt_shared_bus_driver.c:692` `pico-sdk/cybt_shared_bus_driver.h:43` `pico-sdk/cybt_shared_bus_driver.h:50` `embassy/bluetooth.rs:55` `embassy/bluetooth.rs:378` |

### Transmit sequence
| Step | Both drivers | pico-sdk detail | embassy detail | Citations |
|---|---|---|---|---|
| 1 | Request the bus: set WAKE_BT (bit 17) in HOST_CTRL if not already set, then poll BT_CTRL for BT_AWAKE (bit 8). | | | `pico-sdk/cybt_shared_bus.c:316` `pico-sdk/cybt_shared_bus.c:319` `pico-sdk/cybt_shared_bus.c:321` `pico-sdk/cybt_shared_bus.c:345` `embassy/bluetooth.rs:384` `embassy/bluetooth.rs:391` |
| 2 | Read HOST2BT_OUT and compute free space. Give up if the rounded record does not fit. | Reads all four indexes. | Reads HOST2BT_OUT only. | `pico-sdk/cybt_shared_bus.c:205` `pico-sdk/cybt_shared_bus.c:206` `embassy/bluetooth.rs:401` `embassy/bluetooth.rs:402` |
| 3 | Copy header and padded payload into the host-to-controller ring at base + 0 + HOST2BT_IN. Split the copy in two at the end of the ring. | Writes header and payload as one contiguous buffer: one memory write, or two when wrapping. | Writes the 4-byte header with its own backplane write, advances its pointer by 4, then writes the payload with one or two more writes. | `pico-sdk/cybt_shared_bus.c:212` `pico-sdk/cybt_shared_bus.c:215` `pico-sdk/cybt_shared_bus.c:219` `pico-sdk/cybt_shared_bus.c:230` `embassy/bluetooth.rs:420` `embassy/bluetooth.rs:421` `embassy/bluetooth.rs:426` `embassy/bluetooth.rs:432` |
| 4 | Write the new position to HOST2BT_IN: old + record length, wrapped to 0..0xFFF. | | | `pico-sdk/cybt_shared_bus.c:236` `pico-sdk/cybt_shared_bus.c:237` `embassy/bluetooth.rs:438` `embassy/bluetooth.rs:441` |
| 5 | Toggle DATA_VALID (bit 1) in HOST_CTRL. | | | `pico-sdk/cybt_shared_bus.c:239` `embassy/bluetooth.rs:444` `embassy/bluetooth.rs:445` |

- pico-sdk wrap detail: `first_write_len = BTSDIO_FWBUF_SIZE - host2bt_in`. If that is < 4 it is forced to 0 and the whole record is written at offset 0; the index is still advanced by the full length. Indexes are multiples of 4, so a first part of 1 to 3 bytes should not occur (inferred). `pico-sdk/cybt_shared_bus.c:219` `pico-sdk/cybt_shared_bus.c:220` `pico-sdk/cybt_shared_bus.c:224` `pico-sdk/cybt_shared_bus.c:226`
- embassy has no such special case. It splits the payload at exactly `BTSDIO_FWBUF_SIZE - h2b_write_pointer`. `embassy/bluetooth.rs:428`
- pico-sdk requires the transmit buffer pointer to be 4-byte aligned: assert plus `CYBT_ERR_BADARG` in `cybt_hci_write_buf`, and `CYBT_ERR_BADARG` in `cybt_mem_write_idx`. `pico-sdk/cybt_shared_bus.c:197` `pico-sdk/cybt_shared_bus.c:198` `pico-sdk/cybt_shared_bus_driver.c:656`
- embassy has no alignment requirement on the packet; its bus layer copies through its own 4-aligned scratch buffer. `embassy/spi.rs:355`
- embassy takes transmit packets from a 4-slot zero-copy channel of 1024-byte buffers (`BT_HCI_MTU` = 1024; 4 TX and 4 RX slots). It releases the slot (`receive_done`) only after the index update and the interrupt toggle. `embassy/bluetooth.rs:24` `embassy/bluetooth.rs:25` `embassy/bluetooth.rs:105` `embassy/bluetooth.rs:394` `embassy/bluetooth.rs:447`
- pico-sdk has no queue in the transport; it writes the caller's buffer synchronously. `pico-sdk/cybt_shared_bus.c:333`
- embassy transmit has no explicit length check against the packet slot. The payload slice is `msg.buf[1..][..rounded_len]` and `msg.buf[1..]` is 1023 bytes, so a queued packet with `msg.len` of 1022 to 1024 (payload 1021 to 1023, rounded up to 1024) would panic on the slice. `msg.len = 0` would underflow `msg.len as u32 - 1`. The largest packet that can be sent is `msg.len = 1021` (1020 payload bytes). All of this is (inferred). `embassy/bluetooth.rs:105` `embassy/bluetooth.rs:110` `embassy/bluetooth.rs:397` `embassy/bluetooth.rs:398` `embassy/bluetooth.rs:425`
- pico-sdk has no slot limit. It holds `cmd_len` in a `uint16_t` (`size - 4` truncated to 16 bits); the only bound is free ring space, at most 4092 bytes including the header. `pico-sdk/cybt_shared_bus.c:337`

### Receive sequence
| Aspect | pico-sdk | embassy | Citations |
|---|---|---|---|
| Wake before reading | `cyw43_btbus_read` calls `cybt_bus_request` (set WAKE_BT, wait for awake) before every read. | Does not set WAKE_BT or wait for BT_AWAKE before reading; `handle_irq` never calls `bt_bus_request`. Wake handshake on transmit only. | `pico-sdk/cybt_shared_bus.c:417` `pico-sdk/cybt_shared_bus.c:316` `embassy/bluetooth.rs:472` `embassy/bluetooth.rs:384` `embassy/bluetooth.rs:391` |
| Steps per packet | Two separate `cybt_hci_read` calls: first 4 bytes (header), then `ROUNDUP(len, 4)` bytes of payload. Each call re-reads the indexes, copies data, writes BT2HOST_OUT and toggles DATA_VALID. | Reads the header without consuming it, checks the whole record is present and a host queue slot is free, reads the payload, writes BT2HOST_OUT once, then toggles once. | `pico-sdk/cybt_shared_bus.c:362` `pico-sdk/cybt_shared_bus.c:363` `pico-sdk/cybt_shared_bus.c:389` `pico-sdk/cybt_shared_bus.c:259` `pico-sdk/cybt_shared_bus.c:307` `pico-sdk/cybt_shared_bus.c:312` `embassy/bluetooth.rs:487` |
| Index writes and toggles per packet | 2 BT2HOST_OUT writes and 2 DATA_VALID toggles (after header, after payload). | 1 index write and 1 toggle. | `pico-sdk/cybt_shared_bus.c:307` `pico-sdk/cybt_shared_bus.c:312` `pico-sdk/cybt_shared_bus.c:363` `pico-sdk/cybt_shared_bus.c:389` `embassy/bluetooth.rs:518` `embassy/bluetooth.rs:526` |
| Toggle on empty ring | Toggles DATA_VALID at the end of every `cybt_hci_read` call, even when the ring was empty and nothing was consumed; the toggle is outside the if/else. | Toggles only after a record has been consumed. An empty ring breaks out of the loop with no register write. | `pico-sdk/cybt_shared_bus.c:273` `pico-sdk/cybt_shared_bus.c:274` `pico-sdk/cybt_shared_bus.c:312` `embassy/bluetooth.rs:480` |
| Short data | Clamps the requested length to the used count (`read_len = min(ROUNDUP(*p_length, 4), fw_b2h_buf_count)`) and returns the actual count. If fewer payload bytes are present than the header announced, logs "failed to read all data" and returns a short packet (`size = total_read_len + 4`) with success. | If `available < 4 + rounded_len`, warns ("ringbuf data not enough for a full packet?") and leaves the record in the ring untouched. | `pico-sdk/cybt_shared_bus.c:257` `pico-sdk/cybt_shared_bus.c:276` `pico-sdk/cybt_shared_bus.c:310` `pico-sdk/cybt_shared_bus.c:401` `pico-sdk/cybt_shared_bus.c:404` `pico-sdk/cybt_shared_bus.c:406` `embassy/bluetooth.rs:492` |
| Oversize packet | Rejects a packet whose header length exceeds `max_buf_size - 4`: sets `*size = 0`, asserts, returns false; `cyw43_btbus_read` then returns -1. The 4 header bytes have already been consumed from the ring. | No explicit length check against the 1024-byte packet buffer. The slice `msg.buf[1..][..rounded_len]` would panic for `rounded_len` > 1023. | `pico-sdk/cybt_shared_bus.c:379` `pico-sdk/cybt_shared_bus.c:383` `pico-sdk/cybt_shared_bus.c:420` `pico-sdk/cybt_shared_bus.c:363` `embassy/bluetooth.rs:504` |
| Lost-data detection | Keeps a static `available` count (bytes left after the previous read). Panics with "cyw43 buffer overflow" if the freshly computed used count is smaller than it. | Not found: no overflow detection. | `pico-sdk/cybt_shared_bus.c:248` `pico-sdk/cybt_shared_bus.c:264` `pico-sdk/cybt_shared_bus.c:269` `pico-sdk/cybt_shared_bus.c:302` `embassy/bluetooth.rs:479` |
| Wrap | Splits a read that would cross the end of the ring into [index .. 0x1000) and [0 .. rest). Applies the same "first part < 4 bytes becomes 0" rule as on transmit. | Same split, no special case. | `pico-sdk/cybt_shared_bus.c:280` `pico-sdk/cybt_shared_bus.c:287` `pico-sdk/cybt_shared_bus.c:288` `pico-sdk/cybt_shared_bus.c:292` `pico-sdk/cybt_shared_bus.c:298` `embassy/bluetooth.rs:505` `embassy/bluetooth.rs:507` `embassy/bluetooth.rs:511` |
| Packets per service | `cyw43_btbus_read` returns at most one packet per call. Any loop belongs to the caller (`cyw43_bluetooth_hci_process`, declared in c-driver, defined outside these sources). | Drains in a loop until the used count is 0, so one interrupt can deliver several records. | `pico-sdk/cybt_shared_bus.c:416` `c-driver/cyw43.h:843` `c-driver/cyw43_ctrl.c:208` `embassy/bluetooth.rs:476` `embassy/bluetooth.rs:480` |
| Host queue full | Not found: no deferred-drain state. Data is copied into the caller's buffer immediately. | If the 4-slot host RX channel is full (`try_send` fails), sets `pending_drain = true` and breaks before advancing its read pointer, leaving the whole record in the ring. The runner resumes the drain when queue space appears, without a new interrupt. | `pico-sdk/cybt_shared_bus.c:283` `embassy/bluetooth.rs:496` `embassy/bluetooth.rs:497` `embassy/bluetooth.rs:498` `embassy/bluetooth.rs:463` `embassy/bluetooth.rs:474` `embassy/runner.rs:820` `embassy/runner.rs:951` |
| Buffer alignment | Requires the receive buffer to be 4-byte aligned (assert + `CYBT_ERR_BADARG`). Its `cybt_mem_read` asserts `data_len >= 4`. | `bp_read` asserts only that the backplane address is a multiple of 4. | `pico-sdk/cybt_shared_bus.c:250` `pico-sdk/cybt_shared_bus.c:251` `pico-sdk/cybt_shared_bus_driver.c:592` `embassy/spi.rs:304` |

## Record header

Every record in either ring starts with a 4-byte header. pico-sdk's comment gives the format as "Cmd Len B0, Cmd Len B1, Cmd Len B2, HCI pckt type, Data". `pico-sdk/cybt_shared_bus.c:340`

| Offset | Size | Field | Notes | Citations |
|---|---|---|---|---|
| 0 | 3 | Payload length, 24-bit little-endian | Counts the bytes after the packet-type byte. pico-sdk: `cmd_len = size - 4`, where `size` includes the 4-byte header and the type byte is byte 3 of that header; `cmd_len` is a `uint16_t` and byte 2 is written as 0. embassy: `len = msg.len - 1`, where `msg` starts with the type byte and has no header. | `pico-sdk/cybt_shared_bus.c:337` `pico-sdk/cybt_shared_bus.c:334` `pico-sdk/cybt_shared_bus.c:341` `pico-sdk/cybt_shared_bus.c:343` `pico-sdk/cybt_shared_bus.c:378` `embassy/bluetooth.rs:397` `embassy/bluetooth.rs:414` `embassy/bluetooth.rs:490` |
| 3 | 1 | HCI packet type indicator | See the value table below. | `pico-sdk/cybt_shared_bus.c:362` `embassy/bluetooth.rs:417` |
| 4 | ROUNDUP(len, 4) | Payload, padded to a multiple of 4 | A record occupies 4 + ROUNDUP(len, 4) bytes of ring. The indexes always advance by a multiple of 4. The pad bytes are whatever follows the payload in the host buffer; neither driver zeroes them. | `pico-sdk/cybt_shared_bus.c:204` `pico-sdk/cybt_shared_bus.c:257` `embassy/bluetooth.rs:398` `embassy/bluetooth.rs:399` `embassy/bluetooth.rs:425` `embassy/bluetooth.rs:491` |

Length field handling per driver:

| Direction | pico-sdk | embassy | Citations |
|---|---|---|---|
| Transmit | Holds the length in a `uint16_t` and always writes byte 2 as 0. | Writes all three bytes: `len`, `len >> 8`, `len >> 16`. | `pico-sdk/cybt_shared_bus.c:334` `pico-sdk/cybt_shared_bus.c:343` `embassy/bluetooth.rs:414` `embassy/bluetooth.rs:416` |
| Receive | Decodes 24 bits: `((buf[2] << 16) & 0xFFFF00)` OR `((buf[1] << 8) & 0xFF00)` OR `(buf[0] & 0xFF)`. | Decodes 24 bits: `header[0]` OR `header[1] << 8` OR `header[2] << 16`. | `pico-sdk/cybt_shared_bus.c:378` `embassy/bluetooth.rs:490` |

Packet-type byte values named by pico-sdk. The enum is declared but not referenced by the transport code in the same file. `pico-sdk/cybt_shared_bus.c:42` `pico-sdk/cybt_shared_bus.c:50`

| Value | Name | Citations |
|---|---|---|
| 0 (0x00) | HCI_PACKET_TYPE_IGNORE | `pico-sdk/cybt_shared_bus.c:43` |
| 1 (0x01) | HCI_PACKET_TYPE_COMMAND | `pico-sdk/cybt_shared_bus.c:44` |
| 2 (0x02) | HCI_PACKET_TYPE_ACL | `pico-sdk/cybt_shared_bus.c:45` |
| 3 (0x03) | HCI_PACKET_TYPE_SCO | `pico-sdk/cybt_shared_bus.c:46` |
| 4 (0x04) | HCI_PACKET_TYPE_EVENT | `pico-sdk/cybt_shared_bus.c:47` |
| 7 (0x07) | HCI_PACKET_TYPE_DIAG | `pico-sdk/cybt_shared_bus.c:48` |
| 255 (0xFF) | HCI_PACKET_TYPE_LOOPBACK | `pico-sdk/cybt_shared_bus.c:49` |

embassy has no such enum. It passes the type byte through as byte 0 of an H4-style packet; the bt-hci-transport crate parses it. `embassy/bluetooth.rs:503`

Host-side framing:

| Driver | What the caller's buffer holds | Citations |
|---|---|---|
| pico-sdk | The 4-byte bus header followed by the payload. On transmit the caller pre-sets byte 3 to the packet type. Raw buffer API: `cyw43_btbus_read` / `cyw43_btbus_write`. | `pico-sdk/cybt_shared_bus.c:331` `pico-sdk/cybt_shared_bus.c:332` `pico-sdk/cybt_shared_bus.c:415` `pico-sdk/cybt_shared_bus.c:416` |
| embassy | An H4 packet: type byte, then payload. The driver builds or strips the bus header itself. | `embassy/bluetooth.rs:417` `embassy/bluetooth.rs:503` `embassy/bluetooth.rs:521` |

embassy host-facing API (`BtDriver` implements `bt_hci_transport::Transport`): `embassy/bluetooth.rs:575`

- `read()` awaits the next RX slot, asserts `buf.len < rx.len()`, reads the packet kind from byte 0 (`PacketKind::read`), parses the rest with `P::read_hci`, then releases the slot. `embassy/bluetooth.rs:575` `embassy/bluetooth.rs:582` `embassy/bluetooth.rs:583` `embassy/bluetooth.rs:587` `embassy/bluetooth.rs:588`
- `write()` awaits a free TX slot, serialises the packet with `WithIndicator` (type byte first) into the 1024-byte slot, sets `len` to the bytes written and publishes it. A serialisation failure maps to `Error::Io(ErrorKind::Other)`. `embassy/bluetooth.rs:596` `embassy/bluetooth.rs:600` `embassy/bluetooth.rs:602` `embassy/bluetooth.rs:604` `embassy/bluetooth.rs:605`
- Read errors map `InvalidValue` to `InvalidData`, `BufferTooSmall` to `InvalidInput`, `UnexpectedEof` to `BrokenPipe`. `embassy/bluetooth.rs:565` `embassy/bluetooth.rs:566` `embassy/bluetooth.rs:568`

## Patch download format

### Source of the patch
| Driver | Where the patch comes from | Citations |
|---|---|---|
| pico-sdk | Symbols `cyw43_btfw_43439` (data) and `cyw43_btfw_43439_len` (length), declared in the included header `cyw43_btfw_43439.h`. With `CYW43_USE_HEX_BTFW` it uses `brcm_patchram_buf` / `brcm_patch_ram_length` and logs "CYW43_USE_HEX_BTFW is true" at error level. | `pico-sdk/cybt_shared_bus.c:17` `pico-sdk/cybt_shared_bus.c:120` `pico-sdk/cybt_shared_bus.c:121` `pico-sdk/cybt_shared_bus.c:125` `pico-sdk/cybt_shared_bus.c:126` `pico-sdk/cybt_shared_bus.c:128` `pico-sdk/cybt_shared_bus.c:129` |
| embassy | A caller-supplied `&Aligned<A4, [u8]>` argument to `new_with_bluetooth`. | `embassy/lib.rs:668` |

### Container (binary form)

Used by embassy, and by pico-sdk with `CYW43_USE_HEX_BTFW` off. `embassy/bluetooth.rs:239` `pico-sdk/cybt_shared_bus_driver.c:302`

| Offset | Size | Field | Notes | Citations |
|---|---|---|---|---|
| 0 | 1 | version_len | pico-sdk asserts that byte [version_len] is 0, so version_len counts the string including its NUL terminator. | `pico-sdk/cybt_shared_bus_driver.c:301` `pico-sdk/cybt_shared_bus_driver.c:303` `pico-sdk/cybt_shared_bus_driver.c:304` `embassy/bluetooth.rs:239` |
| 1 | version_len | Version string | pico-sdk prints it from offset 1 as a C string. | `pico-sdk/cybt_shared_bus_driver.c:306` `embassy/bluetooth.rs:240` |
| version_len + 1 | 1 | One byte both drivers skip | pico-sdk's comment calls it the "record count". Neither driver reads it, so its meaning is (unverified). | `pico-sdk/cybt_shared_bus_driver.c:308` `pico-sdk/cybt_shared_bus_driver.c:309` `embassy/bluetooth.rs:241` `embassy/bluetooth.rs:242` |
| version_len + 2 | | Records | | `pico-sdk/cybt_shared_bus_driver.c:309` `embassy/bluetooth.rs:242` |

Neither driver uses the skipped byte or the total firmware length to bound parsing. pico-sdk stores `fw_len` in its control block but the binary parser never reads it. embassy relies on slice bounds checks only. `pico-sdk/cybt_shared_bus_driver.c:320` `pico-sdk/cybt_shared_bus_driver.c:240` `pico-sdk/cybt_shared_bus_driver.c:250` `embassy/bluetooth.rs:170` `embassy/bluetooth.rs:179`

### Record (binary form)
| Offset | Size | Field | Notes | Citations |
|---|---|---|---|---|
| 0 | 1 | num_bytes | Data length, 0..255. | `pico-sdk/cybt_shared_bus_driver.c:243` `pico-sdk/cybt_shared_bus_driver.c:244` `embassy/bluetooth.rs:170` |
| 1 | 2 | Address | 16-bit, big-endian. | `pico-sdk/cybt_shared_bus_driver.c:245` `pico-sdk/cybt_shared_bus_driver.c:246` `embassy/bluetooth.rs:173` |
| 3 | 1 | Record type | | `pico-sdk/cybt_shared_bus_driver.c:247` `embassy/bluetooth.rs:176` |
| 4 | num_bytes | Data | No checksum byte in the binary form. | `pico-sdk/cybt_shared_bus_driver.c:253` `pico-sdk/cybt_shared_bus_driver.c:254` `embassy/bluetooth.rs:183` |

Both parsers stop at the first record whose num_bytes is 0. The test is made after all 4 header bytes have been consumed, regardless of the type byte. `pico-sdk/cybt_shared_bus_driver.c:249` `pico-sdk/cybt_shared_bus_driver.c:250` `embassy/bluetooth.rs:179` `embassy/bluetooth.rs:180`

Record types (Intel-HEX numbering). Constant definitions: `pico-sdk/cybt_shared_bus_driver.c:74` `pico-sdk/cybt_shared_bus_driver.c:75` `pico-sdk/cybt_shared_bus_driver.c:76` `pico-sdk/cybt_shared_bus_driver.c:77` `pico-sdk/cybt_shared_bus_driver.c:78` `embassy/consts.rs:179` `embassy/consts.rs:183`

| Type | Name | What both parsers do | Citations |
|---|---|---|---|
| 0 | DATA | dest_addr = the record's 16-bit address plus the mode-dependent offset. The reader returns num_bytes and the caller writes the data to backplane address 0x19000000 + dest_addr. | `pico-sdk/cybt_shared_bus_driver.c:267` `pico-sdk/cybt_shared_bus_driver.c:268` `pico-sdk/cybt_shared_bus_driver.c:276` `pico-sdk/cybt_shared_bus_driver.c:329` `embassy/bluetooth.rs:202` `embassy/bluetooth.rs:203` `embassy/bluetooth.rs:210` `embassy/bluetooth.rs:262` |
| 1 | END_OF_DATA | Defined but never tested by either parser. Such a record with num_bytes > 0 would be skipped like any unknown type; termination relies solely on num_bytes == 0. | `pico-sdk/cybt_shared_bus_driver.c:75` `pico-sdk/cybt_shared_bus_driver.c:257` `pico-sdk/cybt_shared_bus_driver.c:267` `embassy/bluetooth.rs:186` `embassy/bluetooth.rs:212` |
| 2 | EXTENDED_SEGMENT_ADDRESS | hi_addr = `data[0] << 8` OR `data[1]` (big-endian); mode = SEGMENT. A following DATA record is placed at addr + (hi_addr << 4). | `pico-sdk/cybt_shared_bus_driver.c:260` `pico-sdk/cybt_shared_bus_driver.c:262` `pico-sdk/cybt_shared_bus_driver.c:271` `pico-sdk/cybt_shared_bus_driver.c:272` `embassy/bluetooth.rs:191` `embassy/bluetooth.rs:193` `embassy/bluetooth.rs:206` |
| 4 | EXTENDED_ADDRESS | hi_addr = `data[0] << 8` OR `data[1]` (big-endian); mode = EXTENDED. A following DATA record is placed at addr + (hi_addr << 16). | `pico-sdk/cybt_shared_bus_driver.c:257` `pico-sdk/cybt_shared_bus_driver.c:259` `pico-sdk/cybt_shared_bus_driver.c:269` `pico-sdk/cybt_shared_bus_driver.c:270` `embassy/bluetooth.rs:187` `embassy/bluetooth.rs:189` `embassy/bluetooth.rs:205` |
| 5 | ABSOLUTE_32BIT_ADDRESS | abs_base_addr32 = `data[0] << 24` OR `data[1] << 16` OR `data[2] << 8` OR `data[3]` (big-endian); mode = LINEAR32. A following DATA record is placed at addr + abs_base_addr32. | `pico-sdk/cybt_shared_bus_driver.c:263` `pico-sdk/cybt_shared_bus_driver.c:266` `pico-sdk/cybt_shared_bus_driver.c:273` `pico-sdk/cybt_shared_bus_driver.c:274` `embassy/bluetooth.rs:195` `embassy/bluetooth.rs:200` `embassy/bluetooth.rs:207` |

Address modes:

- Constants: `BTFW_ADDR_MODE_UNKNOWN` = 0, `EXTENDED` = 1, `SEGMENT` = 2, `LINEAR32` = 3. `pico-sdk/cybt_shared_bus_driver.c:69` `pico-sdk/cybt_shared_bus_driver.c:72` `embassy/consts.rs:174` `embassy/consts.rs:177`
- Both drivers start in EXTENDED mode with hi_addr = 0, so data records before any address record are placed at their 16-bit address. `pico-sdk/cybt_shared_bus_driver.c:289` `embassy/bluetooth.rs:251` `embassy/bluetooth.rs:252`
- In both drivers `abs_base_addr32` is a local variable reset to 0 on every call of the record reader, and the reader returns after each DATA record. A type-5 base therefore applies only to the first DATA record after it, while LINEAR32 mode persists and later DATA records get base 0. `hi_addr` and `addr_mode` live in the caller's struct and persist across records. `pico-sdk/cybt_shared_bus_driver.c:241` `pico-sdk/cybt_shared_bus_driver.c:276` `pico-sdk/cybt_shared_bus_driver.c:102` `embassy/bluetooth.rs:167` `embassy/bluetooth.rs:210` `embassy/bluetooth.rs:159`

### Text variant (pico-sdk only)

- pico-sdk has a second parser, compiled when `CYW43_USE_HEX_BTFW` is true, for ASCII Intel-HEX text. Lines end with '\n'. Per line: 2 hex characters of byte count at column 1, 4 of address at column 3, 2 of type at column 7, data from column 9. It asserts `line_len == num_bytes * 2 + 11` and processes only lines longer than 9 characters. `pico-sdk/cybt_shared_bus_driver.c:116` `pico-sdk/cybt_shared_bus_driver.c:140` `pico-sdk/cybt_shared_bus_driver.c:190` `pico-sdk/cybt_shared_bus_driver.c:192` `pico-sdk/cybt_shared_bus_driver.c:193` `pico-sdk/cybt_shared_bus_driver.c:195` `pico-sdk/cybt_shared_bus_driver.c:198` `pico-sdk/cybt_shared_bus_driver.c:201`
- The text parser accepts only digits and upper-case A-F; anything else decodes as 0xFF nibbles. It never checks column 0 for ':' and never verifies the trailing checksum byte. `pico-sdk/cybt_shared_bus_driver.c:153` `pico-sdk/cybt_shared_bus_driver.c:156` `pico-sdk/cybt_shared_bus_driver.c:192`
- In this mode the version string and length come from separate symbols (`brcm_patch_version`, `brcm_patchram_buf`, `brcm_patch_ram_length`), and the version/record-count prefix is not skipped. `pico-sdk/cybt_shared_bus_driver.c:302` `pico-sdk/cybt_shared_bus.c:21` `pico-sdk/cybt_shared_bus.c:23` `pico-sdk/cybt_shared_bus.c:125`
- Not found in embassy: binary form only. `embassy/bluetooth.rs:166`

### Writing a DATA record to the chip

- Both drivers write each DATA record with one logical backplane write that starts on a 4-byte boundary and has a length that is a multiple of 4. `pico-sdk/cybt_shared_bus_driver.c:336` `pico-sdk/cybt_shared_bus_driver.c:337` `embassy/bluetooth.rs:265` `embassy/bluetooth.rs:266`
- If the destination start is unaligned, the host reads the existing 32-bit word at the rounded-down address and prepends its first (start % 4) bytes. `pico-sdk/cybt_shared_bus_driver.c:338` `pico-sdk/cybt_shared_bus_driver.c:340` `pico-sdk/cybt_shared_bus_driver.c:342` `embassy/bluetooth.rs:268` `embassy/bluetooth.rs:271`
- If the end (aligned start + bytes so far) is unaligned, the host reads the existing 32-bit word at the rounded-down end address and appends its bytes from index (end % 4) to 3. Existing memory on both sides of the record is preserved. `pico-sdk/cybt_shared_bus_driver.c:353` `pico-sdk/cybt_shared_bus_driver.c:354` `pico-sdk/cybt_shared_bus_driver.c:355` `pico-sdk/cybt_shared_bus_driver.c:356` `embassy/bluetooth.rs:289` `embassy/bluetooth.rs:290` `embassy/bluetooth.rs:294` `embassy/bluetooth.rs:297`
- Byte order of the pad words: pico-sdk reads the word into a `uint32_t` with a raw memory read and indexes its bytes in memory order; embassy reads it with `bp_read32` and uses `to_le_bytes()`. On a little-endian host both give the same bytes in address order. `pico-sdk/cybt_shared_bus_driver.c:340` `pico-sdk/cybt_shared_bus_driver.c:343` `embassy/bluetooth.rs:268` `embassy/bluetooth.rs:269`
- pico-sdk's comments give the reason for the padding as avoiding "alignment issues with SD host controllers". `pico-sdk/cybt_shared_bus_driver.c:333` `pico-sdk/cybt_shared_bus_driver.c:350`
- embassy asserts start % 4 == 0, end % 4 == 0 and length % 4 == 0 before writing. `embassy/bluetooth.rs:306` `embassy/bluetooth.rs:307` `embassy/bluetooth.rs:308`
- Neither driver checks the result of the individual patch writes. pico-sdk's `cybt_mem_write` always returns `CYBT_SUCCESS` and `cybt_fw_download` ignores it. embassy discards the `Result` (`let _ = bus.bp_write(...)`). Both judge success only by FW_RDY appearing afterwards. Neither reads the patch back. `pico-sdk/cybt_shared_bus_driver.c:365` `pico-sdk/cybt_shared_bus_driver.c:375` `pico-sdk/cybt_shared_bus_driver.c:588` `embassy/bluetooth.rs:309` `embassy/bluetooth.rs:313`

| Aspect | pico-sdk | embassy | Citations |
|---|---|---|---|
| Write splitting | `cybt_fw_download` splits a record write at a 0x1000 (4 KiB) address boundary. `cybt_mem_write` further limits each transfer to `CYW43_BUS_MAX_BLOCK_SIZE` (64 bytes on SPI, 16384 on SDIO) and again to the 0x1000 boundary. The c-driver helper below splits at the 0x8000 backplane window. | No 0x1000 split. `bp_write` chunks to `BACKPLANE_MAX_TRANSFER_SIZE` = 64 bytes and to the 0x8000 backplane window only. | `pico-sdk/cybt_shared_bus_driver.c:364` `pico-sdk/cybt_shared_bus_driver.c:367` `pico-sdk/cybt_shared_bus_driver.c:577` `pico-sdk/cybt_shared_bus_driver.c:578` `c-driver/cyw43_ll.h:193` `c-driver/cyw43_ll.h:197` `c-driver/cyw43_ll.c:2565` `c-driver/cyw43_ll.c:2566` `embassy/spi.rs:354` |
| Buffers | Record data buffer `BTFW_MAX_STR_LEN` = 600 bytes. Write buffer `BTFW_DOWNLOAD_BLK_SIZE + BTFW_SD_ALIGN` = (600 / 2 + 8) + 32 = 340 bytes, with the working pointer advanced to a 32-byte (`BTFW_SD_ALIGN`) boundary. Both heap-allocated for the download and freed afterwards. | Two 256-byte stack arrays (`data_buffer` and `aligned_data_buffer`, `[u8; 0x100]`). | `pico-sdk/cybt_shared_bus_driver.h:11` `pico-sdk/cybt_shared_bus_driver.h:12` `pico-sdk/cybt_shared_bus_driver.h:13` `pico-sdk/cybt_shared_bus.c:56` `pico-sdk/cybt_shared_bus.c:61` `pico-sdk/cybt_shared_bus.c:138` `pico-sdk/cybt_shared_bus_driver.c:313` `pico-sdk/cybt_shared_bus_driver.c:314` `embassy/bluetooth.rs:244` |
| Largest record plus padding | The 308-byte block has room for 255 + 3 + 3. | The 256-byte aligned buffer cannot hold a maximal record plus padding. A record whose num_bytes plus front padding (start % 4, up to 3) exceeds 256, for example 254 data bytes at an address with remainder 3, would index past the array and panic (inferred). | `pico-sdk/cybt_shared_bus_driver.h:13` `embassy/bluetooth.rs:245` `embassy/bluetooth.rs:272` `embassy/bluetooth.rs:277` |

## Wake/awake/ready handshake and timeouts

### Init sequence

The order of the seven steps is identical in embassy and pico-sdk. `embassy/bluetooth.rs:221` `embassy/bluetooth.rs:229` `pico-sdk/cybt_shared_bus.c:131` `pico-sdk/cybt_shared_bus.c:146` `pico-sdk/cybt_shared_bus.c:155` `pico-sdk/cybt_shared_bus.c:160` `pico-sdk/cybt_shared_bus.c:166` `pico-sdk/cybt_shared_bus.c:167` `pico-sdk/cybt_shared_bus_driver.c:323`

Bluetooth init runs only after the WiFi firmware is up. embassy calls `init_bluetooth` at the end of `Runner::init`, after F2 is ready and chip init. c-driver calls `cyw43_btbus_init` only after `cyw43_ensure_up` succeeds. `embassy/runner.rs:697` `embassy/runner.rs:703` `c-driver/cyw43_ctrl.c:818` `c-driver/cyw43_ctrl.c:820`

| Step | Action (both drivers) | pico-sdk | embassy | Citations |
|---|---|---|---|---|
| 1 | Write `BT2WLAN_PWRUP_WAKE` (0x03) to backplane address 0x19000000 + 0x640894. | Inside `cybt_fw_download`, immediately before the first record, no delay. | In `init_bluetooth`, followed by a 2 ms delay before the download starts. | `pico-sdk/cybt_shared_bus_driver.c:323` `embassy/bluetooth.rs:221` `embassy/bluetooth.rs:223` |
| 2 | Download the patch: write each DATA record to Bluetooth memory. | | | `pico-sdk/cybt_shared_bus.c:131` `embassy/bluetooth.rs:224` |
| 3 | Wait for FW_RDY (bit 24) in BT_CTRL, polling at 1 ms intervals. | First sleeps `BTFW_WAIT_TIME_MS` = 150 ms. Then polls up to 301 times (do/while with post-decrement of 300), 1 ms between polls. Worst case about 450 ms. | No initial delay. Polls exactly 300 times, 1 ms between polls. Worst case about 300 ms. | `pico-sdk/cybt_shared_bus.c:146` `pico-sdk/cybt_shared_bus.c:82` `pico-sdk/cybt_shared_bus.c:83` `embassy/bluetooth.rs:225` `embassy/bluetooth.rs:313` `embassy/bluetooth.rs:316` |
| 4 | Read WLAN_RAM_BASE_REG_ADDR for the buffer base and write 0 to the four ring indexes. | | | `pico-sdk/cybt_shared_bus.c:155` `pico-sdk/cybt_shared_bus_driver.c:674` `embassy/bluetooth.rs:226` `embassy/bluetooth.rs:373` |
| 5 | Wait for BT_AWAKE (bit 8) in BT_CTRL, polling at 1 ms intervals. The host has not set WAKE_BT at this point. That the controller is expected to be awake by itself after the download is (inferred), not stated in any source (unverified). | Up to 301 polls (`BTSDIO_FW_AWAKE_POLLING_RETRY_COUNT` = 300, do/while post-decrement). | Exactly 300 polls. | `pico-sdk/cybt_shared_bus.c:160` `pico-sdk/cybt_shared_bus.c:93` `pico-sdk/cybt_shared_bus.c:99` `embassy/bluetooth.rs:227` `embassy/bluetooth.rs:328` `embassy/bluetooth.rs:331` |
| 6 | Set SW_RDY (bit 24) in HOST_CTRL. | | | `pico-sdk/cybt_shared_bus.c:166` `pico-sdk/cybt_shared_bus_driver.c:378` `embassy/bluetooth.rs:228` `embassy/bluetooth.rs:347` |
| 7 | Toggle DATA_VALID (bit 1) in HOST_CTRL. The shadow value after init is therefore 0x01000002. | | | `pico-sdk/cybt_shared_bus.c:167` `pico-sdk/cybt_shared_bus_driver.c:390` `embassy/bluetooth.rs:229` `embassy/bluetooth.rs:360` |

### Per-operation wake

- Both drivers set WAKE_BT in HOST_CTRL only if the shadow shows it clear (no write if already set), then poll BT_AWAKE for up to about 300 ms. `pico-sdk/cybt_shared_bus_driver.c:448` `pico-sdk/cybt_shared_bus_driver.c:458` `pico-sdk/cybt_shared_bus.c:319` `pico-sdk/cybt_shared_bus.c:321` `embassy/bluetooth.rs:79` `embassy/bluetooth.rs:86` `embassy/bluetooth.rs:355` `embassy/bluetooth.rs:387`
- Neither driver ever clears WAKE_BT. pico-sdk's only call is `cybt_set_bt_awake(true)`; embassy's only call is `bt_set_awake(bus, true)`. After the first operation the bit stays set and the per-operation wake is only a BT_AWAKE poll. `pico-sdk/cybt_shared_bus.c:319` `embassy/bluetooth.rs:386`
- pico-sdk brackets every read and write with `CYW43_THREAD_ENTER` (in `cybt_bus_request`) and `CYW43_THREAD_EXIT` (in `cybt_bus_release`) to serialise against WiFi use of the bus. `pico-sdk/cybt_shared_bus.c:317` `pico-sdk/cybt_shared_bus.c:328`
- embassy has a TODO for this lock and relies on the single runner task owning the bus. `embassy/bluetooth.rs:385` `embassy/runner.rs:934`
- Both drivers define an unused "set interrupt level" helper. pico-sdk's `cybt_set_bt_intr(value)` can set or clear DATA_VALID. embassy's `bt_set_intr` can only set it and is marked dead code ("TODO: use this"). All live code toggles. `pico-sdk/cybt_shared_bus_driver.c:410` `pico-sdk/cybt_shared_bus_driver.c:414` `embassy/bluetooth.rs:365` `embassy/bluetooth.rs:367` `embassy/bluetooth.rs:95`

### Timing constants
| Constant (pico-sdk) | Value | embassy | Citations |
|---|---|---|---|
| BTSDIO_FW_READY_POLLING_INTERVAL_MS | 1 | literal 1 ms | `pico-sdk/cybt_shared_bus.c:26` `embassy/bluetooth.rs:323` |
| BTSDIO_BT_AWAKE_POLLING_INTERVAL_MS | 1 | literal 1 ms | `pico-sdk/cybt_shared_bus.c:27` `embassy/bluetooth.rs:337` |
| BTSDIO_FW_READY_POLLING_RETRY_COUNT | 300 | literal 300 | `pico-sdk/cybt_shared_bus.c:29` `embassy/bluetooth.rs:316` |
| BTSDIO_FW_AWAKE_POLLING_RETRY_COUNT | 300 | literal 300 | `pico-sdk/cybt_shared_bus.c:30` `embassy/bluetooth.rs:331` |
| BTFW_WAIT_TIME_MS | 150 | no 150 ms wait | `pico-sdk/cybt_shared_bus.c:33` `pico-sdk/cybt_shared_bus.c:83` `embassy/bluetooth.rs:313` `embassy/bluetooth.rs:316` |
| BTSDIO_FWBUF_OPER_DELAY_US | 250. Defined in both pico-sdk files, used in neither. | Not found in embassy. | `pico-sdk/cybt_shared_bus.c:32` `pico-sdk/cybt_shared_bus_driver.c:90` |

### Timeout and error handling
| Event | pico-sdk | embassy | Citations |
|---|---|---|---|
| FW_RDY timeout | Wait returns `CYBT_ERR_TIMEOUT`. At init this trips an assert and `cyw43_btbus_init` returns `CYBT_ERR_HCI_INIT_FAILED`. | Fails `assert!(success == true)`. | `pico-sdk/cybt_shared_bus.c:90` `pico-sdk/cybt_shared_bus.c:147` `pico-sdk/cybt_shared_bus.c:152` `embassy/bluetooth.rs:325` |
| BT_AWAKE timeout at init | Wait returns `CYBT_ERR_TIMEOUT`; trips an assert and returns an error. | Logs bt_ctrl and host_ctrl, then panics "Bluetooth controller failed to acknowledge host wake". | `pico-sdk/cybt_shared_bus.c:100` `pico-sdk/cybt_shared_bus.c:161` `pico-sdk/cybt_shared_bus.c:163` `embassy/bluetooth.rs:339` `embassy/bluetooth.rs:344` |
| BT_AWAKE timeout in a bus request | The result is only asserted ("todo: Handle failure"). With asserts disabled the timeout is ignored. | Same panic as above. | `pico-sdk/cybt_shared_bus.c:318` `pico-sdk/cybt_shared_bus.c:322` `pico-sdk/cybt_shared_bus.c:323` `embassy/bluetooth.rs:344` |

pico-sdk `cyw43_btbus_init` return values:

| Return | When | Citations |
|---|---|---|
| CYBT_ERR_OUT_OF_MEMORY (0xB2) | Either download buffer cannot be allocated. | `pico-sdk/cybt_shared_bus.c:58` `pico-sdk/cybt_shared_bus.c:64` `pico-sdk/cybt_shared_bus.c:109` `pico-sdk/cybt_shared_bus.c:111` `pico-sdk/cybt_shared_bus.c:114` |
| CYBT_ERR_HCI_INIT_FAILED (0xB4) | `cybt_fw_download` fails, or FW_RDY times out. | `pico-sdk/cybt_shared_bus.c:140` `pico-sdk/cybt_shared_bus.c:142` `pico-sdk/cybt_shared_bus.c:152` |
| Result of `cybt_init_buffer` or of the BT_AWAKE wait (`CYBT_ERR_TIMEOUT` 0xB3 on wake timeout) | When either returns non-zero. In this source `cybt_init_buffer` can only return `CYBT_SUCCESS`. | `pico-sdk/cybt_shared_bus.c:100` `pico-sdk/cybt_shared_bus.c:158` `pico-sdk/cybt_shared_bus.c:163` `pico-sdk/cybt_shared_bus_driver.c:676` `pico-sdk/cybt_shared_bus_driver.c:700` |
| CYBT_SUCCESS (0) | At the end. `cybt_set_host_ready` and `cybt_toggle_bt_intr` results are ignored. | `pico-sdk/cybt_shared_bus.c:166` `pico-sdk/cybt_shared_bus.c:169` |

- `cybt_fw_download` itself can only fail with `CYBT_ERR_BADARG` (0xB1): when `cybt_sharedbus_driver_init` has not stored the cyw43_ll pointer, or when the firmware pointer, length, write buffer or hex buffer is NULL/0. `pico-sdk/cybt_shared_bus_driver.c:293` `pico-sdk/cybt_shared_bus_driver.c:294` `pico-sdk/cybt_shared_bus_driver.c:297` `pico-sdk/cybt_shared_bus_driver.c:298` `pico-sdk/cybt_shared_bus_driver.c:375` `pico-sdk/cybt_shared_bus_driver.h:17`
- embassy's `init_bluetooth` returns `()`; every failure is an assert or panic. `embassy/bluetooth.rs:219`
- pico-sdk error codes for this transport: `CYBT_SUCCESS` = 0; `CYBT_ERR_BADARG` = 0xB1, then counting up: OUT_OF_MEMORY 0xB2, TIMEOUT 0xB3, HCI_INIT_FAILED 0xB4, and so on to QUEUE_FULL = 0xC4 (19 enumerators after BADARG). Values after BADARG are implicit: counted from the enum order, not written in the source. `pico-sdk/cybt_shared_bus_driver.h:16` `pico-sdk/cybt_shared_bus_driver.h:17` `pico-sdk/cybt_shared_bus_driver.h:18` `pico-sdk/cybt_shared_bus_driver.h:20` `pico-sdk/cybt_shared_bus_driver.h:36`
- embassy has a single error type, `Error::Io(ErrorKind)`, at the HCI transport layer; bus-level failures panic or are ignored. `embassy/bluetooth.rs:535`

## Interrupt handling

### The "Bluetooth has work" test

embassy, c-driver and whd do the same thing: read SDIO_INT_STATUS (32-bit backplane); if `I_HMB_FC_CHANGE` (bit 5) is set, write back `int_status & I_HMB_FC_CHANGE` (only that bit), and report work pending. `c-driver/cyw43_ll.c:2544` `c-driver/cyw43_ll.c:2546` `embassy/bluetooth.rs:451` `embassy/bluetooth.rs:455` `whd/src/bus_protocols/whd_bus_spi_protocol.c:401` `whd/src/bus_protocols/whd_bus_spi_protocol.c:412`

| Driver | Behaviour | Citations |
|---|---|---|
| c-driver | `cyw43_ll_bt_has_work` returns true. | `c-driver/cyw43_ll.c:2542` `c-driver/cyw43_ll.c:2544` `c-driver/cyw43_ll.c:2545` `c-driver/cyw43_ll.c:2546` |
| embassy | Returns true. | `embassy/bluetooth.rs:450` `embassy/bluetooth.rs:451` `embassy/bluetooth.rs:452` `embassy/bluetooth.rs:455` |
| whd | Only when a callback is registered. Calls the registered callback, and still calls it if the clearing write fails. | `whd/src/bus_protocols/whd_bus_spi_protocol.c:399` `whd/src/bus_protocols/whd_bus_spi_protocol.c:401` `whd/src/bus_protocols/whd_bus_spi_protocol.c:408` `whd/src/bus_protocols/whd_bus_spi_protocol.c:412` `whd/src/bus_protocols/whd_bus_spi_protocol.c:417` |
| pico-sdk | Not found in the pico-sdk files; relies on c-driver's `cyw43_ll_bt_has_work`. | `c-driver/cyw43_ll.c:2542` |
| linux | Clears the same bit by writing `I_HMB_FC_CHANGE` alone, re-reads the status and sets its WLAN `fcstate` from `I_HMB_FC_STATE` OR `I_HMB_FC_CHANGE`. Nothing Bluetooth-related. | `linux/brcmfmac/sdio.c:2643` |

- No driver tests the `F1_INTR` bit (0x2000) of the SPI interrupt status register to decide whether Bluetooth has work. `F1_INTR` appears only in interrupt-enable masks and, in embassy, in a debug formatter's bit list. `c-driver/cyw43_ll.c:1626` `embassy/spi.rs:268` `embassy/runner.rs:660` `embassy/consts.rs:395` `whd/src/bus_protocols/whd_bus_spi_protocol.c:1119`
- Each driver reads SDIO_INT_STATUS over the backplane on every service pass: c-driver on every poll while `bt_loaded`; embassy at the end of every SPI `handle_irq` when a `BtRunner` exists; whd at the start of every `whd_bus_spi_packet_available_to_read` when a callback is registered. `c-driver/cyw43_ctrl.c:207` `embassy/runner.rs:1017` `embassy/runner.rs:1033` `embassy/bluetooth.rs:474` `whd/src/bus_protocols/whd_bus_spi_protocol.c:431`

### What I_HMB_FC_CHANGE means to each driver
| Driver | Use of the bit | Citations |
|---|---|---|
| linux | WLAN transmit flow control. On `I_HMB_FC_CHANGE` it writes that bit back to intstatus, re-reads the register, and sets `bus->fcstate` from (`I_HMB_FC_STATE` OR `I_HMB_FC_CHANGE`). No Bluetooth shared-bus code. | `linux/brcmfmac/sdio.c:268` `linux/brcmfmac/sdio.c:2574` `linux/brcmfmac/sdio.c:2643` `linux/brcmfmac/sdio.c:2645` `linux/brcmfmac/sdio.c:2647` `linux/brcmfmac/sdio.c:2650` |
| c-driver | Only as the Bluetooth work indicator. | `c-driver/cyw43_ll.c:2545` |
| embassy | Only as the Bluetooth work indicator. | `embassy/bluetooth.rs:452` |
| whd | Calls the Bluetooth callback. With `CYCFG_ULP_SUPPORT_ENABLED` its SDIO path separately acks `I_HMB_FC_STATE`. | `whd/src/bus_protocols/whd_bus_sdio_protocol.c:761` |

### c-driver

c-driver polls near the top of its poll routine: if `bt_loaded` and `cyw43_ll_bt_has_work()`, it calls `cyw43_bluetooth_hci_process()` (provided by the Bluetooth stack glue; not found in these sources). This runs before WiFi packet processing. `c-driver/cyw43_ctrl.c:206` `c-driver/cyw43_ctrl.c:207` `c-driver/cyw43_ctrl.c:208` `c-driver/cyw43_ctrl.c:212`

c-driver enables the interrupt path unconditionally at bus init when compiled with `CYW43_ENABLE_BLUETOOTH`. `c-driver/cyw43_ll.c:1625`

### embassy

- embassy enables the interrupt path at init when a Bluetooth firmware was passed. `embassy/runner.rs:659`
- embassy runs the Bluetooth check after WiFi receive handling, inside the SPI branch of `handle_irq`. `embassy/runner.rs:1032`
- embassy calls `BtRunner::handle_irq` only in the SPI branch of `Runner::handle_irq`. The SDIO branch has no Bluetooth handling, so the shared-bus Bluetooth transport is SPI-only in embassy. `embassy/runner.rs:968` `embassy/runner.rs:1015` `embassy/runner.rs:1032` `embassy/runner.rs:1034`
- Supporting facts: `SdioBus::init` ignores its bluetooth flag (parameter named `_bluetooth_enabled`); `new_with_bluetooth` is offered only for `SpiBus` with `Cyw43439`; the SDIO branch writes every remaining observed SDIO_INT_STATUS bit back (after handling `I_HMB_HOST_INT` separately), which would write `I_HMB_FC_CHANGE` back without servicing it. `embassy/sdio.rs:175` `embassy/lib.rs:674` `embassy/runner.rs:994` `embassy/runner.rs:1011`
- `BtRunner::handle_irq` proceeds if the FC_CHANGE bit was set or a deferred drain is pending. It always performs the SDIO_INT_STATUS read/clear first. `embassy/bluetooth.rs:473` `embassy/bluetooth.rs:474` `embassy/bluetooth.rs:475`
- embassy's runner selects among: pending command, WiFi TX, Bluetooth work (deferred RX drain ready, or a TX packet queued), and the bus event/IRQ. A queued Bluetooth TX packet triggers `hci_write`; a deferred drain or bus event triggers `handle_irq`. Bluetooth TX is attempted only while WiFi has bus credit (inside the `has_credit()` branch). `embassy/runner.rs:830` `embassy/runner.rs:846` `embassy/runner.rs:861` `embassy/runner.rs:932` `embassy/runner.rs:934` `embassy/runner.rs:936`

### whd

- At WiFi bring-up `whd_bus_share_bt_init` stores the driver handle in `g_bt_whd_driver`, retrievable with `whd_bt_get_whd_driver`. It is skipped when built with `PROTO_MSGBUF`. A failure only logs "Shared bus for bt is fail". `whd/src/bus_protocols/whd_bus.c:45` `whd/src/bus_protocols/whd_bus.c:49` `whd/src/bus_protocols/whd_bus.c:53` `whd/src/whd_management.c:445` `whd/src/whd_management.c:446` `whd/src/whd_management.c:449`
- A Bluetooth stack registers with `whd_bus_bt_attach(whd_driver, btdata, bt_int_fun)`. `whd/src/bus_protocols/whd_bus.c:61` `whd/src/bus_protocols/whd_bus_protocol_interface.h:86` `whd/inc/whd.h:43`
- The callback is stored in `struct whd_bt_dev { void *bt_data; void (*bt_int_cb)(void *); uint32_t bt_use_count; whd_bool_t intr }`. `intr` ends up `WHD_TRUE` only when a callback was given. `whd/src/include/whd_int.h:96` `whd/src/include/whd_int.h:100` `whd/src/include/whd_int.h:122` `whd/src/bus_protocols/whd_bus.c:77` `whd/src/bus_protocols/whd_bus.c:80` `whd/src/bus_protocols/whd_bus.c:83`
- Attach is a no-op returning `WHD_SUCCESS` if a bt_dev already exists. Allocation failure returns `WHD_BUFFER_UNAVAILABLE_PERMANENT`. `whd/src/bus_protocols/whd_bus.c:65` `whd/src/bus_protocols/whd_bus.c:74`
- Attach calls `whd_bus_init_stats` after setting `intr = WHD_TRUE` and before storing the callback, so the bus init_stats hook always sees `intr` true. `whd/src/bus_protocols/whd_bus.c:77` `whd/src/bus_protocols/whd_bus.c:79`
- `bt_use_count` is never referenced elsewhere in whd/src. `whd/src/include/whd_int.h:100`
- `whd_bus_bt_detach` clears both fields, frees the struct and sets `whd_driver->bt_dev = NULL`. `whd/src/bus_protocols/whd_bus.c:88` `whd/src/bus_protocols/whd_bus.c:100` `whd/src/bus_protocols/whd_bus_protocol_interface.h:88`
- By contrast embassy has no callback and handles Bluetooth inline in the runner; c-driver uses the fixed callback name `cyw43_bluetooth_hci_process`. `embassy/runner.rs:1034` `c-driver/cyw43.h:843`
- whd SPI enables the Bluetooth interrupt path in `whd_bus_spi_init_stats`, only when a bt_dev with `intr` set exists. It writes the SPI interrupt enable register (2 bytes) with `F1_INTR` included, then writes `I_HMB_FC_CHANGE` (4 bytes) to SDIO_INT_HOST_MASK. Failures only log. `whd/src/bus_protocols/whd_bus_spi_protocol.c:1109` `whd/src/bus_protocols/whd_bus_spi_protocol.c:1113` `whd/src/bus_protocols/whd_bus_spi_protocol.c:1117` `whd/src/bus_protocols/whd_bus_spi_protocol.c:1122` `whd/src/bus_protocols/whd_bus_spi_protocol.c:1127`
- Because `whd_bus_bt_attach` calls `whd_bus_init_stats` while `intr` is still `WHD_TRUE`, an attach with a NULL callback would also take this enable path if that call dispatches to `whd_bus_spi_init_stats`. The dispatch is through a bus function pointer, so the target is (unverified). `whd/src/bus_protocols/whd_bus.c:77` `whd/src/bus_protocols/whd_bus.c:79` `whd/src/bus_protocols/whd_bus.h:112`
- whd SPI: `whd_bus_spi_packet_available_to_read` first calls `whd_bus_spi_bt_packet_available_to_read`, which (only if a callback is registered) does the FC_CHANGE read/clear and then invokes `bt_int_cb(bt_data)`. `whd/src/bus_protocols/whd_bus_spi_protocol.c:394` `whd/src/bus_protocols/whd_bus_spi_protocol.c:399` `whd/src/bus_protocols/whd_bus_spi_protocol.c:417` `whd/src/bus_protocols/whd_bus_spi_protocol.c:431`
- whd SPI without a Bluetooth interrupt callback (btdev present, `intr` false) falls back to polling: the WLAN-event wait timeout becomes `BT_POLLING_TIME` = 100 ms and `bus_interrupt` is forced true. Not found in embassy or c-driver. `whd/src/bus_protocols/whd_bus_spi_protocol.c:97` `whd/src/bus_protocols/whd_bus_spi_protocol.c:802` `whd/src/bus_protocols/whd_bus_spi_protocol.c:804` `whd/src/bus_protocols/whd_bus_spi_protocol.c:805`
- whd SDIO: in `whd_bus_sdio_packet_available_to_read`, if a callback is registered and `I_HMB_FC_CHANGE` is set in the status already read, it calls `bt_int_cb` and sets `int_status = 0`, which skips the later "clear HOSTINTMASK bits" write for that pass. `whd/src/bus_protocols/whd_bus_sdio_protocol.c:777` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:779` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:781` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:782` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:786`
- whd sleep interaction: when a Bluetooth interrupt callback is registered, `whd_allow_wlan_bus_to_sleep` returns `WHD_SUCCESS` without calling `whd_kso_enable(WHD_FALSE)` on save-restore-capable chips (the non-4334/43362 branch with `save_restore_enable` true). whd does not put the bus to sleep through KSO while Bluetooth shares it. The HT-clock-request clear in the non-save-restore branch is unaffected. `whd/src/whd_chip.c:850` `whd/src/whd_chip.c:854` `whd/src/whd_chip.c:877` `whd/src/whd_chip.c:884` `whd/src/whd_chip.c:886` `whd/src/whd_chip.c:888`
- No bus-sleep interaction was found in the embassy or pico-sdk Bluetooth code. `embassy/bluetooth.rs:384` `pico-sdk/cybt_shared_bus.c:316`

## Differences between embassy and pico-sdk

Each row is detailed, with its full citations, in the section named in the last column; the last two rows appear only here.

| Topic | embassy | pico-sdk | Citations | Section |
|---|---|---|---|---|
| HOST_CTRL shadow | Local `HostCtrl(u32)` shadow, write-only. No corruption check. | Cached `host_ctrl_cache_reg`; reads are served from the cache. Panics if a bit other than 1, 17, 24 is set in the cache. | `embassy/bluetooth.rs:68` `pico-sdk/cybt_shared_bus_driver.c:395` `pico-sdk/cybt_shared_bus_driver.c:545` | Registers and bits |
| Buffer base zero check | Asserts non-zero. | No check. | `embassy/bluetooth.rs:376` `pico-sdk/cybt_shared_bus_driver.c:676` | Registers and bits |
| SPI interrupt enable | Final mask is F2_PACKET_AVAILABLE and F1_INTR only. | c-driver underneath enables seven bits. | `embassy/runner.rs:658` `c-driver/cyw43_ll.c:1626` | Registers and bits |
| gSPI backplane read pad | 4 bytes. | c-driver underneath: 16 bytes. | `embassy/spi.rs:330` `c-driver/cyw43_ll.h:194` | Registers and bits |
| F2 watermark read-back | On every SPI init; assert. | c-driver underneath: only with Bluetooth; returns `-CYW43_EIO`. | `embassy/runner.rs:491` `c-driver/cyw43_ll.c:1738` | Registers and bits |
| Reading the indexes | One `bp_read32` of the controller-owned index needed. | One 16-byte read of all four, every read and write. | `embassy/bluetooth.rs:401` `pico-sdk/cybt_shared_bus_driver.c:502` | Ring-buffer block |
| Host-owned indexes | Cached on the host, never read back. | Re-read from the chip each time. | `embassy/bluetooth.rs:56` `pico-sdk/cybt_shared_bus.c:205` | Ring-buffer block |
| Index range check | None; modulo 0x1000. | Asserts < 0x1000 on read and write. | `embassy/bluetooth.rs:402` `pico-sdk/cybt_shared_bus_driver.c:527` | Ring-buffer block |
| Ring direction assertions | None. | Asserts ring identity and bounds. | `embassy/bluetooth.rs:420` `pico-sdk/cybt_shared_bus_driver.c:650` | Ring-buffer block |
| Wrap arithmetic | `%`. | `&` mask. | `embassy/bluetooth.rs:422` `pico-sdk/cybt_shared_bus.c:39` | Ring-buffer block |
| Address bookkeeping | Base + constant offsets. | Six stored addresses + index enum. | `embassy/bluetooth.rs:55` `pico-sdk/cybt_shared_bus_driver.c:58` | Ring-buffer block |
| TX ring full | Warns "retrying" and returns without `receive_done`, so the packet stays at the head of the channel and is offered again; see the ring-buffer block. | Assert, then `CYBT_ERR_QUEUE_FULL`, which `cyw43_btbus_write` ignores. | `embassy/bluetooth.rs:403-409` `pico-sdk/cybt_shared_bus.c:350` | Ring-buffer block |
| TX copy | Header written separately, then payload. | Header and payload as one buffer. | `embassy/bluetooth.rs:421` `pico-sdk/cybt_shared_bus.c:215` | Ring-buffer block |
| Wrap special case | None. | First part < 4 bytes forced to 0 (TX and RX). | `embassy/bluetooth.rs:428` `pico-sdk/cybt_shared_bus.c:220` | Ring-buffer block |
| Buffer alignment | None required of the packet; `bp_read` asserts address % 4 == 0. | TX and RX buffer pointers must be 4-byte aligned. | `embassy/spi.rs:355` `embassy/spi.rs:304` `pico-sdk/cybt_shared_bus.c:197` `pico-sdk/cybt_shared_bus.c:250` | Ring-buffer block |
| TX queue | 4-slot channel of 1024-byte buffers. | None; synchronous write of the caller's buffer. | `embassy/bluetooth.rs:105` `pico-sdk/cybt_shared_bus.c:333` | Ring-buffer block |
| TX length limit | No explicit check; `msg.len` above 1021 would panic (inferred). | `uint16_t` length; bounded by free ring space only. | `embassy/bluetooth.rs:425` `pico-sdk/cybt_shared_bus.c:337` | Ring-buffer block |
| Wake before RX | No. | Yes. | `embassy/bluetooth.rs:391` `pico-sdk/cybt_shared_bus.c:417` | Ring-buffer block |
| RX consumption | Whole record at once; 1 index write, 1 toggle. | Header then payload; 2 index writes, 2 toggles. | `embassy/bluetooth.rs:526` `pico-sdk/cybt_shared_bus.c:312` | Ring-buffer block |
| Toggle on empty RX ring | No. | Yes. | `embassy/bluetooth.rs:480` `pico-sdk/cybt_shared_bus.c:312` | Ring-buffer block |
| RX short data | Leaves the record in the ring. | Returns a short packet with success. | `embassy/bluetooth.rs:492` `pico-sdk/cybt_shared_bus.c:404` | Ring-buffer block |
| RX oversize | No check; slice would panic. | Rejects after consuming the header. | `embassy/bluetooth.rs:504` `pico-sdk/cybt_shared_bus.c:379` | Ring-buffer block |
| RX lost-data detection | Not found. | Panic "cyw43 buffer overflow". | `embassy/bluetooth.rs:479` `pico-sdk/cybt_shared_bus.c:269` | Ring-buffer block |
| RX packets per service | Loop until empty. | One per call. | `embassy/bluetooth.rs:476` `pico-sdk/cybt_shared_bus.c:416` | Ring-buffer block |
| RX host queue full | `pending_drain`; record stays in the ring. | Not found. | `embassy/bluetooth.rs:496` `pico-sdk/cybt_shared_bus.c:283` | Ring-buffer block |
| TX length bytes | 24-bit. | 16-bit, byte 2 = 0. | `embassy/bluetooth.rs:416` `pico-sdk/cybt_shared_bus.c:343` | Record header |
| Packet-type names | No enum; passed through to bt-hci-transport. | Enum declared, unused. | `embassy/bluetooth.rs:503` `pico-sdk/cybt_shared_bus.c:43` | Record header |
| Caller's buffer | H4: type byte + payload. | 4-byte bus header + payload. | `embassy/bluetooth.rs:521` `pico-sdk/cybt_shared_bus.c:415` | Record header |
| Patch source | Caller-supplied slice. | Linked symbols `cyw43_btfw_43439`. | `embassy/lib.rs:668` `pico-sdk/cybt_shared_bus.c:120` | Patch download format |
| Text (Intel-HEX) patch | Not found. | Optional parser (`CYW43_USE_HEX_BTFW`). | `embassy/bluetooth.rs:166` `pico-sdk/cybt_shared_bus_driver.c:116` | Patch download format |
| Patch write splitting | 64 bytes and 0x8000 window. | 0x1000 boundary, bus block size, then 0x8000 window in c-driver. | `embassy/spi.rs:354` `pico-sdk/cybt_shared_bus_driver.c:364` | Patch download format |
| Patch buffers | Two 256-byte stack arrays; cannot hold a maximal record plus padding (inferred). | 600-byte and 340-byte heap buffers. | `embassy/bluetooth.rs:244` `embassy/bluetooth.rs:245` `pico-sdk/cybt_shared_bus_driver.h:13` | Patch download format |
| Delay after power-up write | 2 ms. | None. | `embassy/bluetooth.rs:223` `pico-sdk/cybt_shared_bus_driver.c:323` | Handshake and timeouts |
| FW_RDY wait | 300 polls, about 300 ms. | 150 ms sleep, then up to 301 polls, about 450 ms. | `embassy/bluetooth.rs:316` `pico-sdk/cybt_shared_bus.c:83` | Handshake and timeouts |
| BT_AWAKE polls | 300. | Up to 301. | `embassy/bluetooth.rs:331` `pico-sdk/cybt_shared_bus.c:99` | Handshake and timeouts |
| Timing constants | Literals. | Named constants, plus an unused 250 us constant. | `embassy/bluetooth.rs:316` `pico-sdk/cybt_shared_bus.c:32` | Handshake and timeouts |
| Timeout handling | Panics. | Returns an error code; a bus-request timeout is ignored with asserts disabled. | `embassy/bluetooth.rs:344` `pico-sdk/cybt_shared_bus.c:323` | Handshake and timeouts |
| Init result | Returns `()`; assert or panic on failure. | Returns `CYBT_ERR_*` codes. | `embassy/bluetooth.rs:219` `pico-sdk/cybt_shared_bus.c:169` | Handshake and timeouts |
| Error type | `Error::Io(ErrorKind)` at the HCI layer. | `CYBT_ERR_*` enum from 0xB1. | `embassy/bluetooth.rs:535` `pico-sdk/cybt_shared_bus_driver.h:17` | Handshake and timeouts |
| Bus locking | None; single runner task (TODO). | `CYW43_THREAD_ENTER` / `EXIT` around each operation. | `embassy/bluetooth.rs:385` `pico-sdk/cybt_shared_bus.c:317` | Handshake and timeouts |
| Unused "set intr" helper | Can only set. | Can set or clear. | `embassy/bluetooth.rs:95` `pico-sdk/cybt_shared_bus_driver.c:414` | Handshake and timeouts |
| Where the Bluetooth check runs | After WiFi receive handling, SPI branch only. | c-driver underneath: before WiFi packet processing. | `embassy/runner.rs:1032` `c-driver/cyw43_ctrl.c:206` | Interrupt handling |
| Debug state | Not found. On a wake timeout logs only bt_ctrl and host_ctrl. | Always-on `CYBT_CORRUPTION_TEST 1`: remembers the last index block, last HOST_CTRL and last BT_CTRL, and dumps them with `cybt_debug_dump` on an out-of-range index or unexpected HOST_CTRL bits. | `embassy/bluetooth.rs:339` `pico-sdk/cybt_shared_bus_driver.c:17` `pico-sdk/cybt_shared_bus_driver.c:19` `pico-sdk/cybt_shared_bus_driver.c:21` `pico-sdk/cybt_shared_bus_driver.c:467` `pico-sdk/cybt_shared_bus_driver.c:518` `pico-sdk/cybt_shared_bus_driver.c:521` | (only here) |
| Tests | Host-side unit tests for the receive path (Linux-only module `bluetooth_tests.rs`) script the bus operations: `BpRead32` of SDIO_INT_STATUS returning `I_HMB_FC_CHANGE`, then `BpWrite32` of the same value; per record a `BpRead32` of BT2HOST_IN, a 4-byte header read, a payload read, a `BpWrite32` of BT2HOST_OUT, and a `BpWrite32` of HOST_CTRL alternating DATA_VALID / 0. | No tests found in these sources. | `embassy/bluetooth.rs:612` `embassy/bluetooth_tests.rs:242` `embassy/bluetooth_tests.rs:243` `embassy/bluetooth_tests.rs:249` `embassy/bluetooth_tests.rs:250` `embassy/bluetooth_tests.rs:261` `embassy/bluetooth_tests.rs:265` | (only here) |
