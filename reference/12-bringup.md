# Chip bring-up and memory map

## Cores and base addresses per driver

### How each driver finds the cores
| Driver | Method | Citations |
|---|---|---|
| linux | Discovers cores at run time: reads the EROM pointer from chipcommon offset 0xfc (`eromptr`) and walks the DMP descriptor table, recording each component's id, register base, wrapper base and revision | `linux/brcmfmac/chip.c:905-963` `linux/include/chipcommon.h:107` |
| embassy | Fixed `ChipInfo` table per chip type (Cyw43439, Cyw4373, Cyw43455); never reads the EROM | `embassy/lib.rs:269-362` `embassy/lib.rs:269-295` |
| c-driver | Fixed `#define`s for one chip family; no per-chip table; never reads the EROM | `c-driver/cyw43_ll.c:119-124` |
| whd | `switch` statements keyed by chip id; no EROM scan found in whd/src | `whd/src/whd_chip_constants.c:238-310` |

The enumeration (chipcommon) base address is 0x18000000 in all four drivers. `linux/include/soc.h:9` `linux/brcmfmac/chip.c:965-968` `embassy/consts.rs:235` `c-driver/cyw43_ll.c:119` `whd/src/bus_protocols/whd_chip_reg.h:70`

### Chip id register
| Driver | What it reads | Citations |
|---|---|---|
| linux | 32 bits at enumeration base + 0. Chip id = bits 15:0 (mask 0x0000ffff); revision = bits 19:16 (mask 0x000f0000, shift 16); package = bits 23:20; core count = bits 27:24; interconnect type = bits 31:28 (mask 0xf0000000, shift 28). A read of 0xFFFFFFFF is treated as a failed read | `linux/brcmfmac/chip.c:983-992` `linux/brcmfmac/chip.c:976` `linux/include/chipcommon.h:222-230` `linux/include/chipcommon.h:14` |
| embassy (gSPI) | 16 bits at 0x18000000, compared with the expected id; no revision or type decode | `embassy/runner.rs:518-527` |
| whd (gSPI) | 2 bytes at the chipcommon base, stored as the chip id | `whd/src/bus_protocols/whd_bus_spi_protocol.c:695-697` |
| c-driver | Not found in c-driver: no chip id read anywhere | `c-driver/cyw43_ll.c:1564-1951` |

The chip id is the decimal number 43439 for the CYW43439 and 43430 for the BCM43430 in linux, embassy and whd. `linux/include/brcm_hw_ids.h:33` `linux/include/brcm_hw_ids.h:62` `embassy/lib.rs:132-141` `whd/src/whd_chip.c:824`

c-driver has no chip id constant. `c-driver/cyw43_ll.c:119-124`

embassy only logs a warning ("chip ID does not match!") when the id read differs from the compiled-in chip type; bring-up continues. `embassy/runner.rs:523-527`

### Chip id through the SDIO core (SDIO only)

whd and embassy can read the chip id from the SDIO core instead of chipcommon: set bit 0x40 (ADDR_RST) in DEVICE_CTL (function 1, 0x10009), read the three backplane window registers SBADDRLOW/MID/HIGH to form the SDIO core base ((low<<8)|(mid<<16)|(high<<24)), restore DEVICE_CTL, then read base + 0x330 (SDIO_CORE_CHIPID_REG). Otherwise both read chipcommon 0x18000000. `whd/src/bus_protocols/whd_bus_sdio_protocol.c:487-532` `whd/src/bus_protocols/whd_sdio.h:194-195` `embassy/runner.rs:346-371` `embassy/consts.rs:96` `embassy/consts.rs:99-100`

| Driver | When it takes this path | Width | Citations |
|---|---|---|---|
| whd | CCCR card capability (0xF0) bit 0x40 CHIPID_PRESENT is set; bit 0x80 SECURE_MODE only produces a log line | 32 bits; chip id = bits 15:0, revision = bits 19:16 | `whd/src/bus_protocols/whd_bus_sdio_protocol.c:492-523` |
| embassy | Card capability bit 0x80 SECURE_MODE is set (it has no CHIPID_PRESENT constant) | 16 bits, no revision | `embassy/runner.rs:346-368` |
| linux | Not found: always reads the 32-bit chipid register at the enumeration base | - | `linux/brcmfmac/chip.c:983-984` |
| c-driver | Not found: no chip id read | - | `c-driver/cyw43_ll.c:1760-1773` |

### Interconnect type

linux treats interconnect type 0 as Sonics (SOCI_SB, only the 4329 supported) and type 1 as AXI (SOCI_AI, EROM scan); any other type is rejected with -ENODEV. `linux/brcmfmac/chip.c:20-22` `linux/brcmfmac/chip.c:999-1048`

embassy, c-driver and whd implement only the AI wrapper register layout; no interconnect type test found. `embassy/consts.rs:123-133` `c-driver/cyw43_ll.c:141-146` `whd/src/whd_chip.c:62-68`

### EROM descriptors as linux decodes them
| Item | Layout | Citations |
|---|---|---|
| Descriptor type | Low 4 bits (mask 0xF): 0x0 empty, bit 0 valid, 0x1 component, 0x3 master port, 0x5 address (0x8 = address size > 32 bit flag), 0xF end of table | `linux/brcmfmac/chip.c:24-71` |
| Component descriptor A | Designer bits 31:20, part number bits 19:8, class bits 7:4 | `linux/brcmfmac/chip.c:24-71` |
| Component descriptor B | Revision bits 31:24, slave wrappers bits 23:19, master wrappers bits 18:14, slave ports bits 13:9, master ports bits 8:4 | `linux/brcmfmac/chip.c:24-71` |
| Address descriptor | Base bits 31:12, port number bits 11:8, slave type bits 7:6 (0 slave, 1 bridge, 2 slave wrapper, 3 master wrapper), size type bits 5:4 (0 = 4K, 1 = 8K, 2 = 16K, 3 = size descriptor follows) | `linux/brcmfmac/chip.c:24-71` |

linux keeps a core only if it has at least one master or slave wrapper, or is the PMU or GCI core. `linux/brcmfmac/chip.c:833-902` `linux/brcmfmac/chip.c:938-959`

linux takes the first 4K/8K "slave" address region as the register base, and the first 4K/8K wrapper region as the wrapper base (master wrapper if the core has a master port descriptor, else slave wrapper). `linux/brcmfmac/chip.c:833-902` `linux/brcmfmac/chip.c:938-959`

linux requires a CPU core (ARM CM3, CR4 or CA7) and, if the CPU is an ARM CM3, an internal-memory (SOCRAM) core as well; otherwise attach fails (-ENXIO / -ENODEV). `linux/brcmfmac/chip.c:524-566`

linux attach order: bus "prepare" hook (ALP clock, pull-ups off); recognition (chipid read, EROM scan, cores check, set passive, optional bus reset hook plus set passive again, RAM info); setup (read chipcommon capabilities and capabilities_ext, PMU capabilities/revision, bus setup hook). `linux/brcmfmac/chip.c:1138-1182` `linux/brcmfmac/chip.c:1050-1065` `linux/brcmfmac/chip.c:1099-1136`

### Core addresses for the 43439 / 43430
| Core | embassy, c-driver, whd | linux | Citations |
|---|---|---|---|
| Chipcommon | 0x18000000 | 0x18000000 (enumeration base) | `embassy/consts.rs:235` `c-driver/cyw43_ll.c:119` `whd/src/bus_protocols/whd_chip_reg.h:70` `linux/include/soc.h:9` |
| WLAN ARM core | Registers 0x18003000, wrapper 0x18103000 (base + 0x100000) | Not tabulated: base and wrapper come from the EROM scan; the only hard-coded ARM base is the 4329's 0x18002000 | `embassy/lib.rs:272` `embassy/lib.rs:117` `c-driver/cyw43_ll.c:121` `c-driver/cyw43_ll.c:124` `c-driver/cyw43_ll.c:1338-1346` `whd/src/whd_chip_constants.c:248-253` `whd/src/include/whd_chip_constants.h:27` `linux/brcmfmac/chip.c:84-91` |
| SOCSRAM (internal memory) | Registers 0x18004000, wrapper 0x18104000 | Not tabulated: from the EROM scan (core id BCMA_CORE_INTERNAL_MEM) | `embassy/lib.rs:273-275` `c-driver/cyw43_ll.c:122` `c-driver/cyw43_ll.c:1341-1342` `whd/src/whd_chip_constants.c:265-284` `linux/brcmfmac/chip.c:1292` |
| SDIO device core (the bus core, also used on gSPI) | 0x18002000 | Not tabulated: looked up by core id BCMA_CORE_SDIO_DEV after the EROM scan | `embassy/lib.rs:276` `embassy/consts.rs:236` `c-driver/cyw43_ll.c:120` `whd/src/whd_chip_constants.c:300-305` `linux/brcmfmac/sdio.c:3996-3999` |
| PMU | whd and embassy: in chipcommon (0x18000000). c-driver: no PMU base; it addresses only CHIPCOMMON_SR_CONTROL1 | Separate PMU core only when chipcommon rev >= 35 and the capabilities_ext AOB_PRESENT bit is set; else chipcommon | `whd/src/whd_chip_constants.c:312-320` `embassy/lib.rs:277` `c-driver/cyw43_ll.c:128` `linux/brcmfmac/chip.c:1238-1253` |
| Bluetooth | embassy only: `ChipInfo` lists 0x19000000 for all three chip types (field marked dead_code). Not found in whd's chip constants or in c-driver | Not found | `embassy/lib.rs:274` `embassy/lib.rs:167-170` `whd/src/whd_chip_constants.c:132-236` `c-driver/cyw43_ll.c:119-124` |

### Other chips in whd's table
| Item | Values | Citations |
|---|---|---|
| ARM wrapper | 0x18102000 for 0x4373 / 55560 / 55500 / 55530; 0x18103000 for 43012 / 43022 / 43430 / 43439; 0x18111000 for 43909 / 43907 / 54907 | `whd/src/whd_chip_constants.c:238-337` |
| SDIO core | 0x18004000 (55560); 0x18003000 (55500 / 55530); 0x18005000 (0x4373); 0x18002000 (43012 / 43022 / 43430 / 43439) | `whd/src/whd_chip_constants.c:238-337` |
| PMU base | Chipcommon for 0x4373 / 43430 / 43439; 0x18012000 for 43012 / 43022 / 555x0; 0x18011000 for 43909 / 43907 / 54907 | `whd/src/whd_chip_constants.c:238-337` |
| embassy | Agrees for the 4373 (ARM wrapper 0x18102000, SDIO core 0x18005000). Adds a 43455 entry (ARM wrapper 0x18102000, SDIO core 0x18004000, no SOCSRAM) that whd does not have | `embassy/lib.rs:301-362` |

### Core id to address mapping in the drivers

whd's `whd_get_core_address` maps WLAN_ARM_CORE to the ARM core wrapper base, SOCRAM_CORE to the SOCSRAM wrapper base, and SDIOD_CORE to the SDIO core register base; embassy's `base_addr` does the same. `whd/src/whd_chip.c:150-171` `embassy/lib.rs:151-157`

c-driver has only two ids, CORE_WLAN_ARM (1) and CORE_SOCRAM (2), both returning wrapper bases. `c-driver/cyw43_ll.c:1335-1346`

### SDIO core register offsets used during bring-up
| Register (linux name) | Offset from SDIO core base | Citations |
|---|---|---|
| intstatus | 0x20 | `linux/brcmfmac/sdio.h:199-226` `c-driver/cyw43_ll.c:129-132` `embassy/consts.rs:74-76` `whd/src/bus_protocols/whd_sdio.h:32-37` |
| hostintmask | 0x24 | `linux/brcmfmac/sdio.h:199-226` `c-driver/cyw43_ll.c:129-132` `embassy/consts.rs:74-76` `whd/src/bus_protocols/whd_sdio.h:32-37` |
| intmask | 0x28 | `linux/brcmfmac/sdio.h:199-226` |
| sbintstatus | 0x2C | `linux/brcmfmac/sdio.h:199-226` |
| sbintmask | 0x30 | `linux/brcmfmac/sdio.h:199-226` |
| funcintmask | 0x34 | `linux/brcmfmac/sdio.h:199-226` `c-driver/cyw43_ll.c:129-132` `embassy/consts.rs:74-76` `whd/src/bus_protocols/whd_sdio.h:32-37` |
| tosbmailbox | 0x40 | `linux/brcmfmac/sdio.h:199-226` `c-driver/cyw43_ll.c:129-132` `embassy/consts.rs:80-82` `whd/src/bus_protocols/whd_sdio.h:32-37` |
| tohostmailbox | 0x44 | `linux/brcmfmac/sdio.h:199-226` |
| tosbmailboxdata | 0x48 | `linux/brcmfmac/sdio.h:199-226` `embassy/consts.rs:80-82` `whd/src/bus_protocols/whd_sdio.h:32-37` |
| tohostmailboxdata | 0x4C | `linux/brcmfmac/sdio.h:199-226` `embassy/consts.rs:80-82` `whd/src/bus_protocols/whd_sdio.h:32-37` |

linux reaches these as core base + `SD_REG(field)`; the numeric offsets follow from the field list of `struct sdpcmd_regs` (4 x u32, 8 x u16, then u32 fields) (computed). `linux/brcmfmac/sdio.h:199-226` `linux/brcmfmac/sdio.c:172-173`

c-driver defines only intstatus (0x20), host int mask (0x24), function int mask (0x34) and tosbmailbox (0x40). `c-driver/cyw43_ll.c:129-132`

### Bluetooth shared-bus addresses

No WLAN firmware download was found in pico-sdk's Bluetooth shared-bus driver. `pico-sdk/cybt_shared_bus_driver.c:676-692`

pico-sdk reads the Bluetooth firmware's buffer base from backplane register 0x18000d68 (WLAN_RAM_BASE_REG_ADDR) and uses control registers 0x18000c7c (BT_CTRL_REG_ADDR) and 0x18000d6c (HOST_CTRL_REG_ADDR); embassy defines the same three addresses. `pico-sdk/cybt_shared_bus_driver.c:49-56` `pico-sdk/cybt_shared_bus_driver.c:676-692` `embassy/consts.rs:192-194`

### What c-driver does not have

c-driver has none of: EROM/core discovery, a chip id read, RESETSTATUS polling, a working core-disable write, shared-structure or console log reading, a save/restore capability test, or CR4 (non-zero RAM base) support. `c-driver/cyw43_ll.c:119-146` `c-driver/cyw43_ll.c:1333-1386` `c-driver/cyw43_ll.c:1775-1805`

## Wrapper registers

### Register map (offsets from a core's wrapper base)
| Register | Offset | Bits | linux | Citations |
|---|---|---|---|---|
| IOCTRL | 0x408 | 0x0001 clock enable (SICF_CLOCK_EN); 0x0002 force gated clocks on (SICF_FGC); 0x0020 CPU halt (SICF_CPUHALT, ARM core specific) | Uses BCMA_IOCTL (0x0408), BCMA_IOCTL_CLK (0x0001) and BCMA_IOCTL_FGC (0x0002) from the kernel's bcma header; chip.c itself defines ARMCR4_BCMA_IOCTL_CPUHALT 0x0020 and the D11 core bits PHYCLOCKEN 0x0004 and PHYRESET 0x0008 | `embassy/consts.rs:125-128` `c-driver/cyw43_ll.c:141-144` `whd/src/whd_chip.c:62-64` `whd/src/include/whd_chip.h:37` `linux-headers/bcma/bcma_regs.h:29-31` `linux/brcmfmac/chip.c:77-82` |
| RESETCTRL | 0x800 | Bit 0 (AIRC_RESET = 1): embassy, c-driver and whd write 1 to put a core into reset and 0 to release it | Uses BCMA_RESET_CTL (0x0800) and BCMA_RESET_CTL_RESET (0x0001) from the kernel's bcma header | `embassy/consts.rs:130-131` `c-driver/cyw43_ll.c:145-146` `whd/src/whd_chip.c:65-67` `linux-headers/bcma/bcma_regs.h:41-42` `linux/brcmfmac/chip.c:359-370` |
| RESETSTATUS | 0x804 | whd and embassy wait for it to read 0 and treat that as no backplane operation pending | The kernel's bcma header defines BCMA_RESET_ST at 0x0804, but chip.c does not use it: linux polls RESET_CTL itself (SPINWAIT 300 us) | `whd/src/whd_chip.c:66` `embassy/consts.rs:133` `linux-headers/bcma/bcma_regs.h:43` `linux/brcmfmac/chip.c:373-375` |

c-driver has no RESETSTATUS define or read. `c-driver/cyw43_ll.c:141-146`

whd and embassy poll RESETSTATUS before and after each write in `whd_reset_core` / `reset_core`. `whd/src/whd_chip.c:222-224` `embassy/chip.rs:37-45`

whd's `SPINWAIT(exp, 300)` names its argument "us", but each of its up to 30 polls sleeps 10 ms, so the real limit is about 300 ms; embassy's limit is 300 ms. `whd/src/whd_chip.c:41-52` `whd/src/whd_chip.c:222-224` `embassy/chip.rs:37-45`

### Access width

embassy, c-driver and whd read and write IOCTRL / RESETCTRL as single bytes over the backplane. `embassy/chip.rs:14-20` `c-driver/cyw43_ll.c:1350-1370` `whd/src/whd_chip.c:185-199`

linux uses 32-bit reads and writes through `ops->read32/write32`. `linux/brcmfmac/chip.c:271-275` `linux/brcmfmac/chip.c:359-381`

### Core-is-up test

All four drivers treat a core as up when (IOCTRL & (FGC | CLOCK_EN)) == CLOCK_EN and (RESETCTRL & RESET) == 0. `embassy/chip.rs:11-25` `c-driver/cyw43_ll.c:1374-1386` `whd/src/whd_chip.c:176-211` `linux/brcmfmac/chip.c:264-278`

In c-driver a failed test only prints "core not up"; bring-up continues. `c-driver/cyw43_ll.c:1377-1383`

### Disable a core
| Driver | Sequence | Citations |
|---|---|---|
| whd (`whd_disable_device_core`) | Read RESETCTRL twice; if the RESET bit is already set, return success. Else write IOCTRL = CPUHALT if requested, else 0; read IOCTRL back; delay 1 ms; write RESETCTRL = 1; delay 1 ms | `whd/src/whd_chip.c:276-333` |
| embassy (`disable_device_core`) | Same sequence as whd. Two of its dummy reads (`bp_read8` without `.await`) are never executed | `embassy/chip.rs:102-128` `embassy/chip.rs:106-118` |
| c-driver | Reads RESETCTRL twice and returns 0 if in reset. Otherwise it does not disable the core: it warns "core not in reset" and returns -EIO (marked TODO) | `c-driver/cyw43_ll.c:1348-1360` |
| linux | If not in reset: write IOCTRL = prereset OR FGC OR CLK, read back, write RESET_CTL = RESET, sleep 10-20 us, wait up to 300 us for RESET_CTL to read back RESET. Then always write IOCTRL = reset OR FGC OR CLK and read back | `linux/brcmfmac/chip.c:350-382` |

### Reset (enable) a core
| Driver | Sequence | Citations |
|---|---|---|
| whd, embassy, c-driver (`reset_device_core`) | Disable the core; write IOCTRL = FGC OR CLOCK_EN (OR CPUHALT if requested); read IOCTRL; write RESETCTRL = 0; delay 1 ms; write IOCTRL = CLOCK_EN (OR CPUHALT); read IOCTRL; delay 1 ms | `whd/src/whd_chip.c:338-396` `embassy/chip.rs:131-165` `c-driver/cyw43_ll.c:1362-1372` |
| linux (`brcmf_chip_ai_resetcore`) | coredisable; then loop (at most 51 writes, 40-60 us apart) writing RESET_CTL = 0 while the RESET bit still reads set; then write IOCTRL = postreset OR CLK and read it back. FGC is cleared by that final write | `linux/brcmfmac/chip.c:434-493` |
| whd (`whd_wlan_armcore_run`, WLAN ARM core only) | IOCTRL = FGC OR CLOCK_EN (OR CPUHALT); read; RESETCTRL = 0; 1 ms; IOCTRL = CLOCK_EN (OR CPUHALT); read; 1 ms. This is reset_device_core without the disable step. Not found in embassy or c-driver | `whd/src/whd_chip.c:401-459` `embassy/chip.rs:1-175` `c-driver/cyw43_ll.c:1333-1386` |

### Reset for CR4 chips (non-zero RAM base; not the 43439)
| Driver | Sequence | Citations |
|---|---|---|
| whd (`whd_reset_core(core, bits, resetbits)`) | Wait RESETSTATUS == 0; write RESETCTRL = 1; delay 10 ms; wait RESETSTATUS == 0; write IOCTRL = bits OR resetbits OR FGC OR CLOCK_EN; wait RESETSTATUS == 0; then while RESETCTRL reads non-zero, at most 9 times (loop_counter = 10, pre-decremented in the loop test): wait, write RESETCTRL = 0, wait; finally write IOCTRL = bits OR CLOCK_EN and delay 1 ms. Returns success even if RESETCTRL is still non-zero when the loop ends; only bus write errors are reported | `whd/src/whd_chip.c:216-271` |
| embassy (`reset_core`) | Same order, without the 10 ms delay and the final 1 ms delay. Up to 10 passes, each writing RESETCTRL = 0 unconditionally and then reading it back. Returns an error if RESETCTRL is still non-zero afterwards. Every RESETSTATUS wait that times out (300 ms) is also an error | `embassy/chip.rs:28-99` |
| c-driver | Not found: no CR4 path | `c-driver/cyw43_ll.c:1362-1372` |

### CR4 passive / active (not the 43439)
| Driver | Passive (before download) | Active (after download) | Citations |
|---|---|---|---|
| linux | Reset the CR4 core keeping only the CPUHALT IOCTRL bit (prereset = current HALT bit, reset = postreset = CPUHALT); disable the D11 cores | Bus activate hook (clear intstatus, write reset vector to address 0), then resetcore(CR4, CPUHALT, 0, 0) | `linux/brcmfmac/chip.c:1068-1097` `linux/brcmfmac/chip.c:1322-1350` |
| whd (SDIO path, RAM base non-zero) | `whd_reset_core(ARM, SICF_CPUHALT, SICF_CPUHALT)` | `whd_reset_core(ARM, 0, 0)` | `whd/src/bus_protocols/whd_bus_sdio_protocol.c:1183-1242` |
| embassy (RAM base != 0 and bus is SDIO) | `reset_core(WLAN, true, true)` | `reset_core(WLAN, false, false)` | `embassy/runner.rs:529-532` `embassy/runner.rs:597-599` |

## RAM

### 43439 / 43430
| Item | embassy, c-driver, whd | linux | Citations |
|---|---|---|---|
| RAM size used for download placement | 524288 bytes (0x80000, 512 KiB) | Not a constant: summed at run time from the SOCRAM core's bank registers | `embassy/lib.rs:278` `c-driver/cyw43_ll.c:41` `whd/src/whd_chip_constants.c:339-346` `linux/brcmfmac/chip.c:593-636` |
| RAM base (firmware load address) | Backplane address 0 | `rambase` is assigned only for CR4 / SYS_MEM chips. For a SOCRAM (CM3) chip the field is never written in `brcmf_chip_get_raminfo`; it stays 0 from the zeroed allocation of the chip structure (inferred) | `embassy/lib.rs:279` `c-driver/cyw43_ll.c:1792` `whd/src/whd_chip_constants.c:382-410` `whd/src/whd_chip.c:54` `linux/brcmfmac/chip.c:756-795` `linux/brcmfmac/chip.c:1155` |
| Save/restore (retention) RAM size | whd and embassy: 65536 bytes (64 KiB), hard-coded. c-driver: no retention size constant | 65536 bytes (64 KiB), hard-coded | `whd/src/whd_chip_constants.c:412-428` `embassy/lib.rs:280` `c-driver/cyw43_ll.c:41` `linux/brcmfmac/chip.c:638-653` |

### How linux computes the SOCRAM size

linux reads `coreinfo` (SOCRAM offset 0x00): number of banks = (coreinfo & 0xf0) >> 4, plus bit 0x100 for core rev >= 23. `linux/brcmfmac/chip.c:579-636` `linux/brcmfmac/chip.c:144-163`

For core rev > 7 and != 12, for each bank linux writes `bankidx` (offset 0x10) = (memtype RAM 0 << 8) | index and reads `bankinfo` (offset 0x40): bank size = ((bankinfo & 0x7f) + 1) * 8192 bytes; bit 0x00010000 marks a retention bank, whose size is added to `srsize`. `linux/brcmfmac/chip.c:579-636` `linux/brcmfmac/chip.c:165-185`

For core rev <= 7 or == 12: size = nb * (1 << ((coreinfo & 0xf) + 14)), with a last-bank special case from bits 0x00f00000. `linux/brcmfmac/chip.c:579-636`

embassy, c-driver and whd do not read these registers; their size is a constant. `embassy/lib.rs:278` `c-driver/cyw43_ll.c:41` `whd/src/whd_chip_constants.c:339-380`

linux rejects a RAM size of 0 or one larger than 4 MiB (BRCMF_CHIP_MAX_MEMSIZE). `linux/brcmfmac/chip.c:93-94` `linux/brcmfmac/chip.c:800-808`

linux reports the usable RAM size to upper layers as ramsize - srsize. `linux/brcmfmac/sdio.c:3594-3601`

### CR4 chips (not the 43439)
| Chip | RAM base | RAM size | Citations |
|---|---|---|---|
| 4373 | 0x160000 (linux, whd, embassy) | embassy and whd: constant 917504 (0xE0000). linux: computed | `linux/brcmfmac/chip.c:710-754` `whd/src/whd_chip_constants.c:359-362` `whd/src/whd_chip_constants.c:385-388` `embassy/lib.rs:310-311` |
| 4345 / 43454 (43455) | 0x198000 (linux, embassy) | embassy: constant 819200 (0xC8000). linux: computed | `linux/brcmfmac/chip.c:710-754` `embassy/lib.rs:345-346` |

linux computes CR4 RAM size from the ARM core's CAP (0x04), BANKIDX (0x40) and BANKINFO (0x44) registers. `linux/brcmfmac/chip.c:679-708` `linux/brcmfmac/chip.c:205-217`

### SOCSRAM bank-3 remap disable (43430 / 43439)

Before download, c-driver, whd, linux and embassy write 3 to the SOCSRAM bank index register (SOCSRAM base + 0x10) and 0 to the bank PDA register (SOCSRAM base + 0x44), as 32-bit writes. The drivers describe this as disabling the remap for SRAM bank 3. `c-driver/cyw43_ll.c:133-134` `c-driver/cyw43_ll.c:1781-1783` `whd/src/whd_chip.c:820-834` `whd/src/bus_protocols/whd_chip_reg.h:100-101` `linux/brcmfmac/chip.c:1295-1301` `linux/brcmfmac/chip.c:170` `linux/brcmfmac/chip.c:185` `embassy/chip.rs:167-175`

| Driver | When applied | Citations |
|---|---|---|
| embassy | Only when the chip type is C43439 | `embassy/chip.rs:168` |
| whd | 43430 and 43439 | `whd/src/whd_chip.c:820-834` |
| linux | 43430 and 43439; names the registers `bankidx` and `bankpda` via `struct sbsocramregs` offsets | `linux/brcmfmac/chip.c:1295-1301` `linux/brcmfmac/chip.c:1299-1300` |
| c-driver | Unconditionally | `c-driver/cyw43_ll.c:1781-1783` |

## Firmware download

### gSPI bus set-up before the clock steps
| Driver | Sequence | Citations |
|---|---|---|
| whd | (1) Repeatedly read the test register in fixed-address 16-bit mode until any of 8 response bytes equals the low byte of 0xFEEDBEAD (0xAD) or one of three bit-shifted forms ((v<<1)&0xff = 0x5A, ((v<<1)+1)&0xff = 0x5B, ((v+1)<<1)&0xff = 0x5C); up to 500 tries 1 ms apart. (2) Write the bus control register: 32-bit words, big-endian flag, wake-up, response delay 4, interrupt-with-status. (3) Read the test register again in 32-bit mode and require exactly 0xFEEDBEAD. (4) Clear the error interrupt bits DATA_UNAVAILABLE, COMMAND_ERROR, DATA_ERROR, F1_OVERFLOW. (5) Enable interrupts F2_F3_FIFO_RD_UNDERFLOW, F2_F3_FIFO_WR_OVERFLOW, COMMAND_ERROR, DATA_ERROR, F2_PACKET_AVAILABLE, F1_OVERFLOW | `whd/src/bus_protocols/whd_bus_spi_protocol.c:583-664` `whd/src/bus_protocols/whd_bus_spi_protocol.c:63` `whd/src/bus_protocols/whd_spi.h:53-57` |
| c-driver | Same order, except that it has no second test-register read: after writing the bus control register it reads that register back instead. The first test read is tried 10 times 1 ms apart and must equal the pattern exactly. Its bus control value also sets HIGH_SPEED_MODE, which whd's value does not. It additionally writes the F1 response-delay register with 16 (CYW43_BACKPLANE_READ_PAD_LEN_BYTES), and adds F1_INTR to the enable mask when Bluetooth is enabled | `c-driver/cyw43_ll.c:1570-1638` `whd/src/bus_protocols/whd_bus_spi_protocol.c:627-632` |
| embassy | Bus init: WL_REG_ON low 20 ms, then high 250 ms. (1) Poll the read-only test register (32-bit read with swapped byte order) until it equals 0xFEEDBEAD, for up to 500 ms. (2) Write TEST_PATTERN (0x12345678) to the read/write test register and require it to read back. (3) Read the bus control register, then write it: 32-bit words, HIGH_SPEED, interrupt polarity high, wake-up, response delay 4, STATUS_ENABLE, interrupt-with-status; no big-endian flag. (4) Read both test registers again in 32-bit mode and require 0xFEEDBEAD and TEST_PATTERN. (5) Write the F1 response-delay register with 4 (WHD_BUS_SPI_BACKPLANE_READ_PADD_SIZE). (6) Clear the error interrupt bits DATA_UNAVAILABLE, COMMAND_ERROR, DATA_ERROR, F1_OVERFLOW. (7) Enable the same six interrupts as whd, plus F1_INTR when Bluetooth is enabled. After start, the runner rewrites the enable mask to IRQ_F2_PACKET_AVAILABLE only (plus IRQ_F1_INTR with Bluetooth) | `embassy/spi.rs:172-272` `embassy/consts.rs:135-136` `embassy/consts.rs:187` `embassy/runner.rs:656-672` |

### SDIO bus set-up before download
| Driver | Sequence | Citations |
|---|---|---|
| whd | (1) Write CCCR I/O enable (0x02) = function 1 and read it back until it matches, up to 500 tries 1 ms apart (F0_WORKING_TIMEOUT_MS). (2) Unless 1-bit mode, set the bus-interface-control width field to 4-bit. (3) Write block size 64 to CCCR 0x10 until it reads back (up to 500 x 1 ms), then write 64 to the function-0, function-1 and function-2 block size registers. (4) CCCR interrupt enable = master, F1, F2. (5) Optionally set the high-speed bit. (6) Wait for the CCCR I/O-ready function-1 bit, up to 500 x 1 ms (F1_AVAIL_TIMEOUT_MS). (7) ALP: write 0x29 to CHIP_CLOCK_CSR, wait for ALP_AVAIL up to 100 x 1 ms, write 0. (8) Write 0 to the pull-up register. (9) I/O enable = F1, F2. (10) Set up the out-of-band interrupt. (11) Interrupt enable = master, F2 only. (12) Read I/O-ready. (13) Read the chip id. Then download | `whd/src/bus_protocols/whd_bus_sdio_protocol.c:340-485` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:69-75` |
| c-driver | Same order, after its own CMD0/5/3/7 enumeration: I/O enable F1 retried up to 100 times; 4-bit width; block size 64 checked once; interrupt enable master, F1, F2; requires the high-speed capability bit (assert) and sets high speed; waits only 10 x 1 ms for the function-1 ready bit. After ALP: I/O enable F1, F2; SEP_INT_CTL = MASK, EN; interrupt enable master, F2; read I/O-ready. It does not clear the pull-up register here | `c-driver/cyw43_ll.c:1642-1773` |
| embassy | Does the I/O-enable / interrupt-enable part after the ALP step, inside `read_chip_id_sdio`: pull-ups 0; I/O enable F1; interrupt enable master, F1, F2; then `enable_sdio_interrupts` (function-0 writes: SEP_INT_CTL = EN, MASK; address 0x24 = 0xFF; address 0x34 = 0x02; interrupt enable = master); I/O enable F1, F2 (skipped for the 43455); interrupt enable master, F2; read I/O-ready. `enable_sdio_interrupts` addresses function 0 with the SDIO-core offset constants 0x24 and 0x34. The earlier bus set-up (`init` in sdio.rs) follows whd steps 1, 3, 4 and 6: I/O enable = function 1 retried until it reads back (up to 500 ms); block size 64 written to CCCR 0x10 until it reads back (up to 500 ms), then to the function-0, function-1 and function-2 block size registers; interrupt enable = master, F1, F2; wait up to 500 ms for the function-1 I/O-ready bit | `embassy/runner.rs:281-344` `embassy/sdio.rs:175-235` |
| linux | Not found in sdio.c: card enumeration, block sizes and function enable are left to the kernel MMC core and bcmsdh.c (inferred) | `linux/brcmfmac/sdio.c:3951-3994` |

### Firmware file names (linux)

linux maps chip id 43439 (any revision, mask 0xFFFFFFFF) to firmware base name "brcmfmac43439-sdio", with a CLM blob expected. `linux/brcmfmac/sdio.c:615-619` `linux/brcmfmac/sdio.c:649-662`

linux maps 43430 rev 0 to "brcmfmac43430a0-sdio", rev 1 to "brcmfmac43430-sdio" (with CLM), and revs >= 2 to "brcmfmac43430b0-sdio". `linux/brcmfmac/sdio.c:615-619` `linux/brcmfmac/sdio.c:649-662`

linux firmware request items are indexed 0 code, 1 NVRAM, 2 CLM. `linux/brcmfmac/sdio.c:4207-4209`

### Download steps (43439, RAM base 0)
| Step | embassy, c-driver, whd | linux | Citations |
|---|---|---|---|
| 1. Halt cores | Disable the WLAN ARM core, disable the SOCSRAM core, then reset (enable) the SOCSRAM core, all without the CPU-halt flag. c-driver's "disable" calls only check that the core is already in reset | `brcmf_chip_cm3_set_passive`: disable the ARM CM3 core (coredisable 0,0); reset the 802.11 (D11) core with prereset PHYRESET OR PHYCLOCKEN and reset/postreset PHYCLOCKEN; resetcore the SOCRAM core with 0,0,0. Done at attach (`brcmf_chip_recognition`), not immediately before download | `c-driver/cyw43_ll.c:1777-1779` `c-driver/cyw43_ll.c:1348-1360` `whd/src/bus_protocols/whd_bus_spi_protocol.c:1038-1040` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:1191-1193` `embassy/runner.rs:533-535` `linux/brcmfmac/chip.c:1280-1302` |
| 2. SOCSRAM remap | Apply the bank-3 remap disable (bank index = 3, bank PDA = 0) | Same writes, inside set passive | `c-driver/cyw43_ll.c:1781-1783` `whd/src/bus_protocols/whd_bus_spi_protocol.c:1042` `embassy/runner.rs:537` `linux/brcmfmac/chip.c:1295-1301` |
| 3. Host-side image check | c-driver only: checks the firmware image trailer on the host. It looks in the last 800 bytes, skips a 16-byte "DVID" trailer, reads a 16-bit little-endian trailer length, requires it < 500 with a NUL before it, and searches for the string "Version: ". Failure aborts with -EIO. Not found in embassy or in whd's SPI download path | Not found | `c-driver/cyw43_ll.c:378-401` `c-driver/cyw43_ll.c:1785-1789` `embassy/runner.rs:540-545` `whd/src/bus_protocols/whd_bus_spi_protocol.c:1032-1046` `linux/brcmfmac/sdio.c:3388-3407` |
| 4. Write firmware | Write the whole firmware image to the RAM base address (0 for the 43439) through the backplane (function 1) window | Same | `c-driver/cyw43_ll.c:1791-1795` `embassy/runner.rs:540-544` `whd/src/bus_protocols/whd_bus_common.c:273-295` `linux/brcmfmac/sdio.c:3350-3367` |

### Chunking
| Driver | Constant | Citations |
|---|---|---|
| c-driver | Writes CYW43_BUS_MAX_BLOCK_SIZE bytes per transfer (64 on SPI, 16384 on SDIO). Sets the backplane window per chunk, masks the address with 0x7fff, and on SPI only ORs in the 0x08000 32-bit access flag. The image length passed in must already be padded to 4 bytes (SPI) or 64 bytes (SDIO) | `c-driver/cyw43_ll.c:403-436` `c-driver/cyw43_ll.h:191-198` `c-driver/cyw43_ll.c:43-51` `c-driver/cyw43_ll.c:123-126` |
| linux | Defines MEMBLOCK 2048 as its download block size and verifies in 2048-byte blocks. The download passes the whole image to `brcmf_sdiod_ramrw` in one call; that function transfers up to the end of the current 0x8000-byte backplane window (SBSDIO_SB_OFT_ADDR_LIMIT) per step | `linux/brcmfmac/sdio.c:131` `linux/brcmfmac/sdio.c:3318-3320` `linux/brcmfmac/sdio.c:3357-3358` `linux/brcmfmac/bcmsdh.c:669-735` `linux/brcmfmac/sdio.h:123` |
| whd | Backplane transfer limit is 1536 bytes on SDIO and 64 bytes on SPI. That the download loop uses this limit is unverified | `whd/src/bus_protocols/whd_bus_sdio_protocol.h:35` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:1654-1657` `whd/src/bus_protocols/whd_bus_spi_protocol.h:52` |
| embassy | Defines a 64-byte maximum backplane transfer and a 32768-byte (0x8000) window. The download goes through `bp_write`, which per transfer sends at most 64 bytes on SPI and at most 1024 bytes (BLOCK_BUFFER_SIZE) on SDIO, and never crosses a window boundary | `embassy/consts.rs:109-113` `embassy/runner.rs:540-544` `embassy/spi.rs:350-354` `embassy/sdio.rs:302-306` |

### Read-back verification
| Driver | Verification | Citations |
|---|---|---|
| embassy | Always on, sampled: four 16-byte samples (offsets 0, len/3, 2*len/3, len-16, each rounded down to a multiple of 4) and three 64-byte spans (start, middle, end). Fails init on mismatch. Skipped for images under 16 bytes | `embassy/runner.rs:155-251` `embassy/runner.rs:185-250` |
| c-driver | Whole image, only when CYW43_RESOURCE_VERIFY_DOWNLOAD is set (default 0) | `c-driver/cyw43_ll.c:444-478` `c-driver/cyw43_config.h:85-86` |
| linux | Whole image, only in DEBUG builds | `linux/brcmfmac/sdio.c:3296-3348` |
| whd | SPI path: none found. SDIO path: `whd_bus_sdio_verify_resource` is called after the write only when WPRINT_ENABLE_WHD_DEBUG is defined | `whd/src/bus_protocols/whd_bus_spi_protocol.c:1200-1261` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:1955` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:2091-2093` |

### Reset vector at address 0

whd, embassy and linux have a step that writes the first 32-bit word of the firmware image (the reset instruction) to backplane address 0; all three describe it as being for CR4 chips, whose RAM base is not 0. `whd/src/bus_protocols/whd_bus_spi_protocol.c:1221-1259` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:2094-2120` `embassy/runner.rs:253-276` `embassy/runner.rs:546-556` `linux/brcmfmac/sdio.c:3398` `linux/brcmfmac/sdio.c:3904-3907`

embassy runs the step only when the RAM base is not 0, and linux only when the reset vector passed to the activate hook is not 0, so neither does it for the 43439. `embassy/runner.rs:546-556` `linux/brcmfmac/sdio.c:3904-3907` `linux/brcmfmac/chip.c:1314`

whd's condition is `(address != 0) && (reset_instr != 0)`, tested after `address` has been advanced past the last block written. For a firmware download that end address is not 0 even when the RAM base is 0, so on the 43439 whd also writes the image's first word to address 0 again (the value the download already put there) and reads it back (inferred from the code; whd's comment says the step is for CR4 chips only). The NVRAM download leaves `reset_instr` at 0 and skips it. `whd/src/bus_protocols/whd_bus_spi_protocol.c:1218-1259` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:2089-2120`

whd's SDIO-path copy of this step is compiled out when BLHS_SUPPORT is defined. `whd/src/bus_protocols/whd_bus_sdio_protocol.c:2094-2120`

whd and embassy read the word back and fail on mismatch; linux does not. `whd/src/bus_protocols/whd_bus_spi_protocol.c:1221-1259` `embassy/runner.rs:253-276` `linux/brcmfmac/sdio.c:3904-3907`

linux writes it in the bus "activate" hook after NVRAM download; for a CM3 chip activate is called with rstvec = 0, so nothing is written. `linux/brcmfmac/chip.c:1314`

c-driver has no CR4 support and no such write. `c-driver/cyw43_ll.c:1791-1805`

## NVRAM placement and length token

### Order

Firmware is written first and NVRAM second in all four drivers for the 43439; whd writes NVRAM before firmware only for the 43022 (DM_43022C1). `embassy/runner.rs:540-565` `c-driver/cyw43_ll.c:1791-1802` `linux/brcmfmac/sdio.c:3401-3414` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:1202-1235`

### Placement

embassy, c-driver and whd write the NVRAM text so that it ends 4 bytes before the end of RAM: address = RAM base + RAM size - 4 - padded NVRAM length (43439: 0x80000 - 4 - len). `embassy/runner.rs:558-564` `c-driver/cyw43_ll.c:1797-1800` `whd/src/bus_protocols/whd_bus_spi_protocol.c:1263-1280` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:2124-2153`

whd's 43022 build places it relative to NVRAM_DNLD_ADDR instead. `whd/src/bus_protocols/whd_bus_sdio_protocol.c:2124-2153`

linux reaches the same end result by a different route: the 4-byte token is appended to the NVRAM buffer on the host, and the whole buffer (text + token) is written at ramsize - total length + rambase. `linux/brcmfmac/sdio.c:3369-3386` `linux/brcmfmac/firmware.c:446-451`

### Length rounding
| Driver | Rounding before placement | Citations |
|---|---|---|
| embassy | Up to a multiple of 4 | `embassy/runner.rs:559` |
| whd | Up to a multiple of 4 on both buses (SDIO uses NVM_IMAGE_SIZE_ALIGNMENT, which is 4) | `whd/src/bus_protocols/whd_bus_spi_protocol.c:1272-1273` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:2137-2138` `whd/inc/whd_resource_api.h:38` |
| c-driver | To 4 on SPI and to 64 on SDIO (CYW43_WRITE_BYTES_PAD). The pad bytes come from whatever follows the NVRAM array in host memory | `c-driver/cyw43_ll.c:45-51` `c-driver/cyw43_ll.c:1798` `c-driver/cyw43_ll.c:1798-1800` |
| linux | roundup(stripped length + 1, 4), with explicit zero fill | `linux/brcmfmac/firmware.c:439-444` |

### Preprocessing

linux rewrites the NVRAM file on the host before download: it removes carriage returns, empty lines and comment lines, converts newlines to NULs, may add defaults and a MAC address entry, then pads and appends the token. `linux/brcmfmac/firmware.c:395-454`

embassy, c-driver and whd download the NVRAM bytes they are given unchanged. `embassy/runner.rs:561-564` `c-driver/cyw43_ll.c:1799-1800` `whd/src/bus_protocols/whd_bus_spi_protocol.c:1280` `whd/src/bus_protocols/whd_bus_spi_protocol.c:1263-1289`

### Length token

All four drivers put a little-endian length token in the last 32-bit word of RAM (RAM base + RAM size - 4): low 16 bits = NVRAM length in 32-bit words, high 16 bits = bitwise NOT of that word count. `embassy/runner.rs:567-570` `c-driver/cyw43_ll.c:1801-1802` `whd/src/bus_protocols/whd_bus_spi_protocol.c:1282-1287` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:2155-2160` `linux/brcmfmac/firmware.c:446-451`

| Driver | Expression | Masking | Citations |
|---|---|---|---|
| c-driver | ((~(len/4) & 0xffff) << 16) OR (len/4) | Inverted count masked to 16 bits before the shift | `c-driver/cyw43_ll.c:1801` |
| linux | (~token << 16) OR (token & 0x0000FFFF) | Low half masked | `linux/brcmfmac/firmware.c:447` |
| embassy | (!words << 16) OR words | None | `embassy/runner.rs:568` |
| whd | (~(size/4) << 16) OR (size/4), same expression on SPI and SDIO | None | `whd/src/bus_protocols/whd_bus_spi_protocol.c:1283` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:2155-2160` |

### Token read-back

embassy reads the token word back and fails init with "NVRAM magic write FAILED" if it differs. `embassy/runner.rs:572-595`

embassy also logs the first NVRAM word, noting it expects 0x4152564e ("NVRA" little-endian). `embassy/runner.rs:572-595`

embassy's comment says a missing token leaves the firmware unable to find the NVRAM, so F2 ready is never set (embassy's comment). `embassy/runner.rs:572-595`

c-driver and whd do not read the token back. `c-driver/cyw43_ll.c:1801-1802` `whd/src/bus_protocols/whd_bus_spi_protocol.c:1287`

## Start

### Release the ARM core (43439)
| Driver | Sequence | Citations |
|---|---|---|
| c-driver, whd, embassy | Take the WLAN ARM core out of reset with reset_device_core(ARM, no halt), then test that the core is up. In c-driver a failed is-up test is only a warning | `c-driver/cyw43_ll.c:1804-1805` `c-driver/cyw43_ll.c:1374-1386` `whd/src/bus_protocols/whd_bus_spi_protocol.c:1047-1054` `embassy/runner.rs:597-603` |
| linux | `brcmf_chip_cm3_set_active`: check the SOCRAM core is up; call the bus activate hook, which writes 0xFFFFFFFF to the SDIO core's intstatus register to clear all interrupts; then resetcore(ARM CM3, 0, 0, 0) | `linux/brcmfmac/chip.c:1304-1320` `linux/brcmfmac/sdio.c:3893-3908` |

embassy writes 0xFFFFFFFF to SDIO core base + 0x20 before release only for the 43455. `embassy/runner.rs:547-554` `embassy/runner.rs:550-554` `embassy/consts.rs:74`

No intstatus clear before release was found in c-driver or in whd's SPI download path. `c-driver/cyw43_ll.c:1804` `whd/src/bus_protocols/whd_bus_spi_protocol.c:1047-1054`

### Wait for the HT clock

After releasing the ARM core, c-driver, embassy and whd poll CHIP_CLOCK_CSR until bit 0x80 (HT available) is set. `c-driver/cyw43_ll.c:1807-1817` `embassy/runner.rs:605-611` `whd/src/bus_protocols/whd_bus_spi_protocol.c:1056-1069` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:1256-1275`

| Driver | Limit | Notes | Citations |
|---|---|---|---|
| c-driver | 1000 x 1 ms | Its comment says the wait takes about 29 ms | `c-driver/cyw43_ll.c:1807-1817` |
| embassy | 500 ms | - | `embassy/runner.rs:605-611` |
| whd | 1000 ms on SPI, 2500 ms on SDIO | - | `whd/src/bus_protocols/whd_bus_spi_protocol.c:71` `whd/src/bus_protocols/whd_bus_spi_protocol.c:1056-1069` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:74` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:1256-1275` |
| linux | Up to 1000 ms (PMU_MAX_TRANSITION_DLY/1000), polled every 5-10 ms | `brcmf_sdio_htclk` returns at once if save/restore is enabled (`sr_enabled`). Otherwise it requests the clock explicitly: writes 0x10 (HT_AVAIL_REQ), or 0x08 (ALP_AVAIL_REQ) while `alp_only` is set, as it is during download. It waits until SBSDIO_CLKAV is true: any availability bit while `alp_only`, otherwise both ALP and HT status bits (0xC0) | `linux/brcmfmac/sdio.c:785-866` |

whd notes that an HT-clock timeout means the firmware is not booting. `whd/src/bus_protocols/whd_bus_sdio_protocol.c:1266-1275`

### Host interrupt mask

After HT is available, c-driver, embassy and whd write the SDIO core's host interrupt mask register (SDIO core base + 0x24, 32-bit) with I_HMB_SW_MASK = 0x000000f0. `c-driver/cyw43_ll.c:116` `c-driver/cyw43_ll.c:130` `c-driver/cyw43_ll.c:1821-1822` `embassy/runner.rs:613-617` `embassy/consts.rs:71` `embassy/consts.rs:75` `whd/src/bus_protocols/whd_bus_spi_protocol.c:1076-1078` `whd/src/bus_protocols/whd_sdio.h:36` `whd/src/bus_protocols/whd_sdio.h:113` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:85` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:1283-1284`

linux writes I_HMB_SW_MASK | I_CHIPACTIVE (0xf0 | bit 29), and only after function 2 has been enabled. `linux/brcmfmac/sdio.c:782` `linux/brcmfmac/sdio.c:229` `linux/brcmfmac/sdio.h:217`

With Bluetooth enabled on SPI, c-driver and embassy then overwrite the mask with I_HMB_FC_CHANGE (bit 5) only. `c-driver/cyw43_ll.c:1832-1835` `embassy/runner.rs:659-668`

### Function interrupt mask (SDIO only)

On SDIO, c-driver, embassy and whd write 3 (function 1 | function 2) as one byte to the SDIO core's function interrupt mask register (SDIO core base + 0x34). `c-driver/cyw43_ll.c:131` `c-driver/cyw43_ll.c:1824-1826` `embassy/runner.rs:620-623` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:1286-1288` `whd/src/bus_protocols/whd_sdio.h:37` `whd/src/bus_protocols/whd_sdio.h:200-201`

linux declares `funcintmask` at offset 0x34 in `struct sdpcmd_regs`, but no code under linux/ reads or writes it. `linux/brcmfmac/sdio.h:221`

### F2 watermark

c-driver, embassy and whd set the function-2 watermark register (function 1 address 0x10008) to 32 (0x20) on gSPI and 8 on SDIO; the source comment gives the reason as avoiding a DMA hang in F2 when the SD clock is stopped. `c-driver/cyw43_ll.c:108` `c-driver/cyw43_ll.c:148-149` `c-driver/cyw43_ll.c:1828-1838` `embassy/consts.rs:58` `embassy/consts.rs:106-107` `embassy/runner.rs:625-629` `embassy/runner.rs:674-678` `whd/src/bus_protocols/whd_bus_spi_protocol.c:74` `whd/src/bus_protocols/whd_bus_spi_protocol.c:1080-1082` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:77` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:1290-1292`

linux's SDIO default watermark is also 8 (DEFAULT_F2_WATERMARK, written to SBSDIO_WATERMARK 0x10008). `linux/brcmfmac/sdio.c:4282-4357` `linux/brcmfmac/sdio.h:70`

linux gives ten other device ids (43751, 43752, 4373, 43012, 4329, 4339, 43455, 4359, 4354, 4356) per-device values plus the DEVICE_CTL F2WM_ENAB bit and a MESBUSYCTRL write; its switch has no case for a 43430/43439 device id, so the default branch applies with no F2WM_ENAB or MESBUSYCTRL write. `linux/brcmfmac/sdio.c:4282-4357`

### Wait for function 2

embassy, c-driver and whd then wait for function 2 to be ready: on gSPI, bit 5 (0x20, F2 RX ready) of the 32-bit SPI status register at bus address 0x8; on SDIO, bit 0x04 of the CCCR I/O-ready register. `embassy/runner.rs:682-692` `embassy/consts.rs:14` `embassy/consts.rs:45` `embassy/consts.rs:225` `c-driver/cyw43_ll.c:1843-1860` `whd/src/bus_protocols/whd_bus_spi_protocol.c:719-738` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:568-588`

| Driver | Limit | Citations |
|---|---|---|
| embassy | 1000 ms | `embassy/runner.rs:682-692` |
| c-driver | 1000 x 1 ms | `c-driver/cyw43_ll.c:1843-1860` |
| whd | 1000 x 1 ms on both buses (F2_READY_TIMEOUT_MS 1000) | `whd/src/bus_protocols/whd_bus_spi_protocol.c:60` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:72` |
| linux | Uses `sdio_enable_func(func2)` from the kernel MMC core; its timeout is not in these sources | `linux/brcmfmac/sdio.c:4271` |

whd notes that a timeout waiting for function 2 after download usually means wrong NVRAM variables, including crystal frequency. `whd/src/bus_protocols/whd_bus_spi_protocol.c:729-738`

### linux start sequence after download

linux, in order: start watchdog; make the backplane clock available; read CHIP_CLOCK_CSR and OR in FORCE_HT (0x02; HT_AVAIL_REQ on ULP chips); write the host's SDPCM protocol version to the SDIO core's tosbmailboxdata register (offset 0x48) as (4 << 16); enable function 2; write hostintmask; set the F2 watermark; then either run SR init (if `brcmf_chip_sr_capable` returns true) or restore the saved clock value. `linux/brcmfmac/sdio.c:4235-4370` `linux/brcmfmac/sdio.c:260` `linux/brcmfmac/sdio.c:290` `linux/brcmfmac/sdio.h:225`

embassy does the FORCE_HT / mailbox version 4<<16 (SDIO core base + 0x48) / enable F2 steps only for the 43455. `embassy/runner.rs:631-653` `embassy/consts.rs:81`

No tosbmailboxdata version write was found in c-driver, or in whd's SPI and SDIO download functions. `c-driver/cyw43_ll.c:1819-1841` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:1283-1294`

### Save/restore capability test (43430 / 43439)

linux and whd treat the firmware as save/restore capable when the 32-bit chipcommon register SR_CONTROL1 (0x18000000 + 0x508) reads non-zero after the firmware has started. `linux/brcmfmac/chip.c:1457-1461` `linux/include/chipcommon.h:180` `whd/src/whd_chip.c:1133-1149` `whd/src/bus_protocols/whd_chip_reg.h:97`

linux returns false first if the PMU revision is < 17. `linux/brcmfmac/chip.c:1433-1435`

c-driver only reads the register (in NDEBUG builds) and ignores the value; it assumes KSO mode (USE_KSO 1). `c-driver/cyw43_ll.c:128` `c-driver/cyw43_ll.c:1906-1909`

embassy has no SR_CONTROL1 read. `embassy/runner.rs:374-425`

### Save/restore (KSO) setup after F2 is ready
| Driver | Sequence | Citations |
|---|---|---|
| whd | Runs only if `whd_is_fw_sr_capable`. (1) Read wakeup control (function 1, 0x1001E), OR in bit 1 (wake till HT available), write back. (2) Write 0x08 (CMD_NODEC) to the CCCR Broadcom card capability register 0xF0. (3) Write 0x02 (FORCE_HT) to CHIP_CLOCK_CSR. (4) Read sleep CSR (function 1, 0x1001F) and set bit 0 (keep-SDIO-on, KSO) if clear. (5) Bus-specific sleep. (6) Write 0xF to the pull-up register 0x1000F ("put SPI interface block to sleep"). For 43012 / 0x4373 / 555x0 / 43022 it uses wake-till-ALP and HT_AVAIL_REQ instead | `whd/src/whd_chip.c:1201-1299` `whd/src/whd_chip.c:1207-1255` |
| c-driver | Runs steps 1-4 and 6 unconditionally (USE_KSO). Skips step 5: the SPI WAKE_UP-bit clear is under `#if 0`, with a note that it breaks wake after sleep. Immediately afterwards writes 0 to the pull-up register again ("clear pad pulls") | `c-driver/cyw43_ll.c:1864-1887` `c-driver/cyw43_ll.c:1877-1893` `c-driver/cyw43_ll.c:113-114` `c-driver/cyw43_ll.c:196` `c-driver/cyw43_ll.c:220-235` |
| linux (`brcmf_sdio_sr_init`) | Sets wakeup-control bit 1 (HT wait; bit 0 on ULP chips); writes card capability CMD14_SUPPORT OR CMD14_EXT (0x06; CMD_NODEC only for 43751 / 43752 / 43012); writes FORCE_HT to CHIP_CLOCK_CSR. The KSO bit is set earlier, in probe, only for SDIO core rev >= 12 | `linux/brcmfmac/sdio.c:3439-3528` |
| embassy | The wakeup / cardcap / FORCE_HT / KSO block is commented out for the 43439. On SDIO only, it writes the KSO bit twice and asserts it reads back. It then clears the pull-up register and requests HT (writes 0x10), waiting up to 500 ms for bit 0x80 | `embassy/runner.rs:374-425` |

### Waking through KSO (43430 / 43439)
| Driver | Procedure | Citations |
|---|---|---|
| whd, c-driver | Write the KSO bit (bit 0) to the sleep CSR 0x1001F twice (both writes may fail). Then up to 64 times: read it back and stop when (value & 0x03) == 0x03 (KSO and device-on) and value != 0xFF; else wait 1 ms and write again. To sleep: write 0 and wait only for bit 0 to clear | `whd/src/whd_chip.c:1301-1416` `whd/src/whd_chip.c:57-59` `whd/src/bus_protocols/whd_sdio.h:249-250` `c-driver/cyw43_ll.c:1388-1431` |
| linux (`brcmf_sdio_kso_control`) | One initial write of the KSO bit (not two). Returns immediately when clearing KSO on a 43012. On wake, sleeps 2-3 ms. Then loops: read sleep CSR; stop when (value & mask) == wanted (mask and wanted 0x03 to wake; mask 0x01, wanted 0 to sleep; no 0xFF test); give up after more than 5 consecutive read errors (BRCMF_SDIO_MAX_ACCESS_ERRORS); else wait 50 us (KSO_WAIT_US) and write again, up to MAX_KSO_ATTEMPTS = 1000000/50 = 20000 retries | `linux/brcmfmac/sdio.c:698-779` `linux/brcmfmac/sdio.c:326-328` `linux/brcmfmac/sdio.h:109-114` |

### Bus up without save/restore

When save/restore is not enabled, whd brings the bus up by writing HT_AVAIL_REQ (0x10) to CHIP_CLOCK_CSR and polling for HT_AVAIL (0x80) up to 1000 times 1 ms apart. `whd/src/whd_chip.c:55-56` `whd/src/whd_chip.c:1083-1104`

c-driver has the same loop compiled out behind USE_KSO. `c-driver/cyw43_ll.c:1438-1460`

embassy, on SDIO, writes HT_AVAIL_REQ in `wake_bus` and waits only 5 ms for bit 0x80. `embassy/runner.rs:771-789`

### linux SDIO probe extras after attach

linux enables KSO (SDIO core rev >= 12), sets drive strength (default 6 mA), sets the WLANRESET bit (bit 1) in CCCR Broadcom card control 0xF1 so an SDIO card reset also resets the WLAN backplane, and ORs the "resource reload" bits into the PMU control register so a backplane reset reloads PMU state. `linux/brcmfmac/sdio.c:4040-4072` `linux/brcmfmac/sdio.c:539` `linux/brcmfmac/sdio.h:43-44`

These steps were not found in embassy or c-driver. `embassy/runner.rs:460-715` `c-driver/cyw43_ll.c:1564-1951`

### c-driver timing and SPI clean-up

c-driver holds WL_REG_ON low 20 ms, then high 50 ms, before bus init. `c-driver/cyw43_ctrl.c:140-144`

c-driver enforces a minimum of 150 ms between the start of bus init and the event-mask command in wifi_on; its comment says the chip needs the time or SDIOIT / OOB WL_HOST_WAKE interrupts in bus-sleep mode do not work correctly. `c-driver/cyw43_ll.c:1568` `c-driver/cyw43_ll.c:2043-2048`

c-driver (SPI) reads the 16-bit SPI interrupt register after start and, if the DATA_UNAVAILABLE bit is set, writes the value back to clear it; its comment says it always seems to start with that error. `c-driver/cyw43_ll.c:1895-1904`

## Clocks

### CHIP_CLOCK_CSR (function 1, address 0x1000E)
| Bit | Driver name for the bit | Citations |
|---|---|---|
| 0x01 | Force ALP | `linux/brcmfmac/sdio.c:177-191` `embassy/consts.rs:115-120` `c-driver/cyw43_ll.c:213-217` `whd/src/bus_protocols/whd_sdio.h:210-217` |
| 0x02 | Force HT | `linux/brcmfmac/sdio.c:177-191` `embassy/consts.rs:115-120` `c-driver/cyw43_ll.c:213-217` `whd/src/bus_protocols/whd_sdio.h:210-217` |
| 0x04 | Force ILP (named by linux and whd; not found in embassy or c-driver) | `linux/brcmfmac/sdio.c:177-191` `whd/src/bus_protocols/whd_sdio.h:210-217` |
| 0x08 | ALP available request | `linux/brcmfmac/sdio.c:177-191` `embassy/consts.rs:115-120` `c-driver/cyw43_ll.c:136-139` `c-driver/cyw43_ll.c:213-217` `whd/src/bus_protocols/whd_sdio.h:210-217` |
| 0x10 | HT available request | `linux/brcmfmac/sdio.c:177-191` `embassy/consts.rs:115-120` `c-driver/cyw43_ll.c:136-139` `whd/src/bus_protocols/whd_sdio.h:210-217` |
| 0x20 | Force HW clock request off | `linux/brcmfmac/sdio.c:177-191` `embassy/consts.rs:115-120` `c-driver/cyw43_ll.c:213-217` `whd/src/bus_protocols/whd_sdio.h:210-217` |
| 0x40 | ALP available (status) | `linux/brcmfmac/sdio.c:177-191` `embassy/consts.rs:115-120` `c-driver/cyw43_ll.c:136-139` `c-driver/cyw43_ll.c:213-217` `whd/src/bus_protocols/whd_sdio.h:210-217` |
| 0x80 | HT available (status) | `linux/brcmfmac/sdio.c:177-191` `c-driver/cyw43_ll.c:136-139` `whd/src/bus_protocols/whd_sdio.h:210-217` |

The register address 0x1000E is defined in all four drivers. `linux/brcmfmac/sdio.h:83` `embassy/consts.rs:64` `c-driver/cyw43_ll.c:112` `whd/src/bus_protocols/whd_sdio.h:107`

### First clock step: ALP request
| Bus / driver | Value written | Then | Citations |
|---|---|---|---|
| gSPI: embassy, c-driver, whd | 0x08 (ALP_AVAIL_REQ) | Poll until bit 0x40 (ALP_AVAIL) is set, then write 0 to clear the request | `embassy/runner.rs:479-516` `c-driver/cyw43_ll.c:1726-1758` `whd/src/bus_protocols/whd_bus_spi_protocol.c:666-693` |
| SDIO: embassy, c-driver, whd | 0x29 (FORCE_HW_CLKREQ_OFF, ALP_AVAIL_REQ, FORCE_ALP) | Wait for ALP_AVAIL, then write 0 to clear the request | `embassy/runner.rs:493-501` `embassy/runner.rs:514-516` `c-driver/cyw43_ll.c:1727-1728` `c-driver/cyw43_ll.c:1757-1758` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:448-451` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:469-470` |
| SDIO: linux | 0x28 (FORCE_HW_CLKREQ_OFF, ALP_AVAIL_REQ), written as BRCMF_INIT_CLKCTL1 in probe_attach and again in buscoreprep; the read-back is checked | Wait for ALP, then write 0x21 (FORCE_HW_CLKREQ_OFF, FORCE_ALP), delay 65 us. The request is not cleared | `linux/brcmfmac/sdio.c:3848-3885` `linux/brcmfmac/sdio.c:314-316` |

### ALP wait limits
| Driver | Limit | Citations |
|---|---|---|
| embassy | 100 ms | `embassy/runner.rs:504-510` |
| whd | 100 x 1 ms on both buses (ALP_AVAIL_TIMEOUT_MS 100) | `whd/src/bus_protocols/whd_bus_spi_protocol.c:64` `whd/src/bus_protocols/whd_bus_spi_protocol.c:670-684` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:73` `whd/src/bus_protocols/whd_bus_sdio_protocol.c:453-467` |
| c-driver | 10 polls 1 ms apart (10 ms total) | `c-driver/cyw43_ll.c:1743-1752` `c-driver/cyw43_ll.c:1743-1749` |
| linux | Up to 1,000,000 us (PMU_MAX_TRANSITION_DLY), polled every 10 us by SPINWAIT; its comment says it may take up to 15 ms | `linux/brcmfmac/sdio.c:311-312` `linux/brcmfmac/sdio.c:3862-3881` `linux/brcmfmac/sdio.c:3872-3875` `linux/include/brcmu_utils.h:16-22` |

### F2 watermark probe before the ALP wait

Before the ALP wait, embassy (SPI path, always) and c-driver (only when Bluetooth is enabled) write 0x10 to the function-2 watermark register 0x10008 and require it to read back 0x10. `embassy/runner.rs:484-491` `c-driver/cyw43_ll.c:1733-1741`

embassy's comment says this is not present in whd; it was not found in whd's SPI init. `embassy/runner.rs:484-491` `whd/src/bus_protocols/whd_bus_spi_protocol.c:666-693`

### Pull-up register (function 1, address 0x1000F) written 0
| Driver | When | Citations |
|---|---|---|
| linux | At the end of the pre-attach clock step | `linux/brcmfmac/sdio.c:3887-3888` `linux/brcmfmac/sdio.h:85` |
| whd | In SDIO init, right after clearing the ALP request | `whd/src/bus_protocols/whd_bus_sdio_protocol.c:472-473` |
| embassy | At the start of its SDIO chip id read; and again in `init_cyw43439` after function 2 is ready (write 0, then read back) | `embassy/runner.rs:304-305` `embassy/runner.rs:404-407` `embassy/consts.rs:65` `embassy/consts.rs:228` |
| c-driver | After function 2 is ready, on both buses ("clear pad pulls"; write 0, then read back) | `c-driver/cyw43_ll.c:1889-1893` |

The later HT clock wait and the HT / KSO handling are in the Start section. `c-driver/cyw43_ll.c:1807-1817` `linux/brcmfmac/sdio.c:785-866`

## The shared-memory pointer, console and log

### Pointer location

linux, whd and embassy read a 32-bit word near the end of RAM to find the firmware's shared structure; the drivers treat the word that held the NVRAM length token as overwritten by the running firmware with the structure's address. `linux/brcmfmac/sdio.c:1039-1047` `linux/brcmfmac/sdio.c:1051-1054` `whd/src/whd_chip.c:934-950` `embassy/runner.rs:718-723`

| Driver | Address read | Citations |
|---|---|---|
| linux | Last word of RAM. For chips with RAM base 0 for which `brcmf_chip_sr_capable` returns true (43430 / 43439): RAM size - 4 - retention size, i.e. 0x80000 - 4 - 0x10000 = 0x6FFFC. Compiled only in DEBUG builds; otherwise the pointer is never read | `linux/brcmfmac/sdio.c:1039-1047` `linux/brcmfmac/sdio.c:1043-1045` `linux/brcmfmac/sdio.c:1021` `linux/brcmfmac/sdio.c:1103-1107` `linux/brcmfmac/sdio.c:1021-1107` |
| whd | Same rule as linux: minus the retention size when RAM base is 0 and `whd_is_fw_sr_capable` returns true | `whd/src/whd_chip.c:934-950` `whd/src/whd_chip.c:946-949` |
| embassy | Always subtracts the retention size (no save/restore-capable test); for the 43439 it reads 0 + 0x80000 - 4 - 0x10000 | `embassy/runner.rs:721` |
| c-driver | Not found: no shared-structure or console support | `c-driver/cyw43_ll.c:1564-1951` |

whd's log reader picks the address per chip: 43362 uses RAM size - 4 with RAM base 0; 43909 / 43907 / 54907 use RAM base + RAM size - 4 after ensuring the bus is up; 4334 and 4390 are unsupported; all others (including the 43439) use RAM base + RAM size - 4, minus the retention size when RAM base is 0 and `whd_is_fw_sr_capable` returns true, keeping the WLAN awake during the read. `whd/src/whd_chip.c:898-955`

### Pointer validity
| Driver | Check | Citations |
|---|---|---|
| linux (DEBUG builds only) | Rejects the pointer if it is 0 or still looks like an NVRAM token (high half equals the inverted low half) | `linux/brcmfmac/sdio.c:1022-1025` `linux/brcmfmac/sdio.c:1055-1060` `linux/brcmfmac/sdio.c:1024` `linux/brcmfmac/sdio.c:1021` |
| whd | Loops re-reading until the pointer is non-zero and lies strictly inside (RAM base, RAM base + RAM size); no timeout | `whd/src/whd_chip.c:478-484` `whd/src/whd_chip.c:480-484` |
| embassy | No check | `embassy/runner.rs:722-726` |

### Shared structure layout (32-bit little-endian fields)
| Offset | Field | Citations |
|---|---|---|
| 0 | flags | `linux/brcmfmac/sdio.c:365-387` `whd/src/include/whd_chip.h:320-339` `embassy/structs.rs:49-58` |
| 4 | trap_addr | `linux/brcmfmac/sdio.c:365-387` `whd/src/include/whd_chip.h:320-339` `embassy/structs.rs:49-58` |
| 8 | assert_exp_addr | `linux/brcmfmac/sdio.c:365-387` `whd/src/include/whd_chip.h:320-339` `embassy/structs.rs:49-58` |
| 12 | assert_file_addr | `linux/brcmfmac/sdio.c:365-387` `whd/src/include/whd_chip.h:320-339` `embassy/structs.rs:49-58` |
| 16 | assert_line | `linux/brcmfmac/sdio.c:365-387` `whd/src/include/whd_chip.h:320-339` `embassy/structs.rs:49-58` |
| 20 | console_addr (address of the console structure) | `linux/brcmfmac/sdio.c:365-387` `whd/src/include/whd_chip.h:320-339` `embassy/structs.rs:49-58` |
| 24 | msgtrace_addr | `linux/brcmfmac/sdio.c:365-387` `whd/src/include/whd_chip.h:320-339` `embassy/structs.rs:49-58` |

| Driver | Fields after offset 24 | Total size | Citations |
|---|---|---|---|
| linux | u8 tag[32] at 28, brpt_addr at 60 | 64 | `linux/brcmfmac/sdio.c:373-374` |
| whd | fwid at 28, then total_lfrag_pktcount, reserved, reserved1, h2d_mb_addr, d2h_mb_addr, ring_info_ptr, scratch_mem_size, scratch_mem_ptr_low, scratch_mem_ptr_high | 68 | `whd/src/include/whd_chip.h:329-338` |
| embassy | fwid at 28 | 32 | `embassy/structs.rs:57` |

### Flags

linux and whd treat the low 8 bits of flags as a version (mask 0x00FF); the maximum version the host accepts is 3. `linux/brcmfmac/sdio.c:296-300` `linux/brcmfmac/sdio.c:1081-1086` `whd/src/whd_chip.c:70-71` `whd/src/whd_chip.c:514-521`

linux also names 0x0100 assert built, 0x0200 assert, 0x0400 trap; these names are linux's only, and its use of them is in DEBUG builds. `linux/brcmfmac/sdio.c:296-300` `linux/brcmfmac/sdio.c:1021`

whd defines only the version mask and version. `whd/src/whd_chip.c:70-71`

embassy reads flags but never checks them. `embassy/runner.rs:727-729`

### Console structure (`hnd_cons_t` / `rte_console`)
| Offset | Field | Citations |
|---|---|---|
| 0 | vcons_in | `whd/src/include/whd_chip.h:274-308` `linux/brcmfmac/sdio.c:66-107` |
| 4 | vcons_out | `whd/src/include/whd_chip.h:274-308` `linux/brcmfmac/sdio.c:66-107` |
| 8 | log structure: buf (address of the ring buffer) at +0, buf_size at +4, idx (write index) at +8, fourth field at +12 | `whd/src/include/whd_chip.h:274-308` `linux/brcmfmac/sdio.c:66-107` `embassy/structs.rs:64-69` |
| 24 (whd, embassy layout) | cbuf_idx | `whd/src/include/whd_chip.h:274-308` |
| 28 (whd, embassy layout) | cbuf, 128-byte input line buffer; 156 bytes in all | `whd/src/include/whd_chip.h:274-308` |

| Driver | Fourth log field | Citations |
|---|---|---|
| whd | out_idx (output index) | `whd/src/include/whd_chip.h:279` |
| embassy | out_idx; the log address is taken as console_addr + 8 | `embassy/structs.rs:68` `embassy/runner.rs:729` |
| linux | A host pointer `_buf_compat` (kept for backward compatibility), so the host struct is pointer-sized there; its cbuf_idx / cbuf offsets depend on the host word size. Only buf, buf_size and idx, and offsetof(log_le) = 8, are used | `linux/brcmfmac/sdio.c:71-76` |

### Reading the console

linux and whd: read the log structure at console_addr + 8; if idx is unchanged since the last poll, do nothing; otherwise read the whole ring buffer from buf and print characters from the last index up to idx, splitting lines on '\n' and dropping a trailing '\r'. An idx greater than buf_size is treated as corrupt. `linux/brcmfmac/sdio.c:2859-2933` `whd/src/whd_chip.c:533-646`

| Driver | Differences | Citations |
|---|---|---|
| linux | DEBUG builds only; prints with the prefix "CONSOLE: "; line buffer 192 bytes; a partial line is left for the next poll; the host copy is allocated once using the buf_size read from the log structure | `linux/brcmfmac/sdio.c:2856` `linux/brcmfmac/sdio.c:2857` `linux/brcmfmac/sdio.c:2859-2933` |
| whd | Prints with the prefix "FW_CONS: "; leaves a partial line for the next call; host copy allocated once using buf_size; suggested host line buffer WLAN_LOG_BUF_LEN 4096 | `whd/src/whd_chip.c:533-646` `whd/src/include/whd_chip.h:341-342` |
| embassy | Does not use buf_size: always reads 1024 (0x400) bytes and wraps the index at 0x400; splits on '\r' or '\n'; no corrupt-index check | `embassy/runner.rs:732-769` |

### When the console is located

linux fetches the console address when the host-mailbox data it reads has DEVREADY (0x0002) or FWREADY (0x0008) set, and only in DEBUG builds. `linux/brcmfmac/sdio.c:1151-1168` `linux/brcmfmac/sdio.c:273-277`

linux polls the console from the watchdog every console_interval ms (BRCMF_CONSOLE = 10) and allocates at most CONSOLE_BUFFER_MAX 2024 bytes for a crash dump. `linux/brcmfmac/sdio.c:3715-3726` `linux/brcmfmac/bus.h:30` `linux/brcmfmac/sdio.c:69`

embassy locates it once at the end of runner init when the "firmware-logs" feature is on. `embassy/runner.rs:700-701`

whd locates it on every `whd_wifi_read_wlan_log` call. `whd/src/whd_chip.c:898-953`

## Regulatory (CLM) download

All four drivers download the CLM (regulatory) blob after the firmware is running, as a series of command 263 (SetVar) writes of the named variable (iovar) "clmload". `embassy/control.rs:251-255` `c-driver/cyw43_ll.c:1508` `c-driver/cyw43_ll.c:1522` `c-driver/cyw43_ll.c:185` `linux/brcmfmac/common.c:193-194` `whd/src/whd_clm.c:138` `whd/src/include/whd_wlioctl.h:1231`

### Payload of each clmload command
| Offset | Size | Field | Citations |
|---|---|---|---|
| 0 | 8 | NUL-terminated name "clmload" | `embassy/control.rs:244-253` `c-driver/cyw43_ll.c:1508-1517` `linux/brcmfmac/common.c:108-112` `whd/src/whd_clm.c:53-58` |
| 8 | 2 | u16 flag (little-endian) | `embassy/structs.rs:368-376` `c-driver/cyw43_ll.c:1508-1517` `linux/brcmfmac/fwil_types.h:1099-1112` `whd/src/include/whd_wlioctl.h:4167-4175` |
| 10 | 2 | u16 dload_type | `embassy/structs.rs:368-376` `c-driver/cyw43_ll.c:1508-1517` `linux/brcmfmac/fwil_types.h:1099-1112` `whd/src/include/whd_wlioctl.h:4167-4175` |
| 12 | 4 | u32 len: bytes of data in this chunk | `embassy/structs.rs:368-376` `c-driver/cyw43_ll.c:1508-1517` `linux/brcmfmac/fwil_types.h:1099-1112` `whd/src/include/whd_wlioctl.h:4167-4175` |
| 16 | 4 | u32 crc | `embassy/structs.rs:368-376` `c-driver/cyw43_ll.c:1508-1517` `linux/brcmfmac/fwil_types.h:1099-1112` `whd/src/include/whd_wlioctl.h:4167-4175` |
| 20 | len | Chunk data (header is 12 bytes with no padding; data starts 12 bytes after the header start) | `embassy/structs.rs:368-376` `c-driver/cyw43_ll.c:1508-1517` `linux/brcmfmac/fwil_types.h:1099-1112` `whd/src/include/whd_wlioctl.h:4167-4175` |

### Header flags
| Value | Meaning | Citations |
|---|---|---|
| 0x0001 | CRC not in use (defined by embassy and whd; used by no driver) | `embassy/structs.rs:379-382` `whd/src/include/whd_wlioctl.h:4154-4160` |
| 0x0002 | Begin (first chunk) | `embassy/structs.rs:379-382` `c-driver/cyw43_ll.c:1500-1506` `linux/brcmfmac/fwil_types.h:187-192` `whd/src/include/whd_wlioctl.h:4154-4160` |
| 0x0004 | End (last chunk) | `embassy/structs.rs:379-382` `c-driver/cyw43_ll.c:1500-1506` `linux/brcmfmac/fwil_types.h:187-192` `whd/src/include/whd_wlioctl.h:4154-4160` |
| 0x1000 | Downloader version 1 in bits 15:12 (mask 0xf000, shift 12); ORed into every chunk | `embassy/structs.rs:379-382` `c-driver/cyw43_ll.c:1500-1506` `linux/brcmfmac/fwil_types.h:187-192` `whd/src/include/whd_wlioctl.h:4154-4160` |

All four drivers send dload_type 2 for CLM (1 is ucode in whd's enum) and always send the crc field as 0. `embassy/structs.rs:385` `embassy/control.rs:246-248` `c-driver/cyw43_ll.c:1513-1515` `linux/brcmfmac/fwil_types.h:194` `linux/brcmfmac/common.c:110-112` `whd/src/include/whd_wlioctl.h:4162-4165` `whd/src/whd_clm.c:58`

### Chunk data size per command
| Driver | Size | Citations |
|---|---|---|
| embassy | 1024 (MAX_IOCTL_LEN 1044 minus 8 name bytes minus 12 header bytes) | `embassy/control.rs:228-229` `embassy/control.rs:229` `embassy/ioctl.rs:17` |
| c-driver | 1024 on SPI, 1536 on SDIO | `c-driver/cyw43_ll.c:1485-1489` |
| whd | 1024 (BLOCK_SIZE) | `whd/inc/whd_resource_api.h:35` `whd/src/whd_clm.c:109-130` |
| linux | 1400 (MAX_CHUNK_LEN) | `linux/brcmfmac/fwil_types.h:181-185` `linux/brcmfmac/fwil_types.h:185` `linux/brcmfmac/common.c:144-149` |

### Command payload length
| Driver | Length sent | Citations |
|---|---|---|
| embassy | Exactly name + header + data | `embassy/control.rs:250-255` |
| linux | Exactly name + header + data | `linux/brcmfmac/common.c:114-115` |
| c-driver | (20 + data length) rounded up to a multiple of 8 (ALIGN_UINT); the padding is whatever is in the buffer | `c-driver/cyw43_ll.c:1521-1522` `c-driver/cyw43_ll.c:1522` |
| whd | len + 8 - (len % 8): always adds 1 to 8 bytes, so a full extra 8 when already aligned. Not applied for the msgbuf protocol | `whd/src/whd_clm.c:60-67` `whd/src/whd_clm.c:61-63` |

### Status check

embassy and c-driver read the named variable "clmload_status" (command 262, GetVar) as a 32-bit value and treat 0 as success; whd defines the name. `embassy/control.rs:258-259` `c-driver/cyw43_ll.c:1526-1535` `whd/src/include/whd_wlioctl.h:1232`

| Driver | When read | On non-zero | Citations |
|---|---|---|---|
| embassy | Always, after the last chunk | Panics: `assert_eq!(status, 0)` | `embassy/control.rs:258-259` `embassy/control.rs:259` |
| c-driver | Always, after the last chunk | Prints a warning and continues | `c-driver/cyw43_ll.c:1526-1535` `c-driver/cyw43_ll.c:1531-1533` |
| linux | Only after a clmload command returned an error | Result becomes -EIO | `linux/brcmfmac/common.c:161-171` |
| whd | Only after a clmload command returned an error | Logs one status byte | `whd/src/whd_clm.c:148-173` |

### Missing blob

A missing CLM blob is not an error in linux, which logs "device may have limited channels available" and continues. `linux/brcmfmac/common.c:186-191`

whd skips the download without error when the resource size is 0, but treats a failed CLM download as fatal ("system unusable"). `whd/src/whd_clm.c:96-100` `whd/src/whd_management.c:434-443`

embassy and c-driver always download the blob they are given. `embassy/control.rs:263-264` `c-driver/cyw43_ll.c:1913-1916`

### Other blobs and the CLM version

linux reuses the same chunked download for two more blobs: "txcapload" / "txcapload_status" and "calload" / "calload_status", each still sent with dload_type 2. `linux/brcmfmac/common.c:102-118` `linux/brcmfmac/common.c:216-217` `linux/brcmfmac/common.c:260-261`

The CLM version string is read with the named variable "clmver": c-driver reads up to 128 bytes in debug builds after setting the country; linux reads it during pre-init and replaces newlines with spaces. `c-driver/cyw43_ll.c:2026-2031` `linux/brcmfmac/common.c:385-403`

whd defines the "clmver" name. `whd/src/include/whd_wlioctl.h:1233`

embassy's init does not read "clmver". `embassy/control.rs:263-340`

## Country

### Record of the "country" named variable (12 bytes)
| Offset | Size | Field | Citations |
|---|---|---|---|
| 0 | 4 | char country_abbrev[4] | `embassy/structs.rs:387-395` `linux/brcmfmac/fwil_types.h:757-768` `whd/src/include/whd_wlioctl.h:667-673` `c-driver/cyw43_ll.c:2013-2022` |
| 4 | 4 | s32 rev, little-endian | `embassy/structs.rs:387-395` `linux/brcmfmac/fwil_types.h:757-768` `whd/src/include/whd_wlioctl.h:667-673` `c-driver/cyw43_ll.c:2013-2022` |
| 8 | 4 | char ccode[4] | `embassy/structs.rs:387-395` `linux/brcmfmac/fwil_types.h:757-768` `linux/brcmfmac/fwil_types.h:146` `whd/src/include/whd_wlioctl.h:667-673` `c-driver/cyw43_ll.c:2013-2022` |

c-driver has no struct; it writes the same three words at name + 8, + 12 and + 16. `c-driver/cyw43_ll.c:2013-2022`

### Values sent

embassy, c-driver and whd put the same two-letter code, padded with zero bytes, in both country_abbrev and ccode, and send rev = -1 when the requested revision is 0. `embassy/control.rs:278-284` `c-driver/cyw43_ll.c:2014-2022` `whd/src/whd_management.c:196-211`

whd's comment gives the purpose of -1 as letting the firmware use any NVRAM/OTP aggregate to choose the revision; linux's doc comment says that on set, -1 indicates unspecified. `whd/src/whd_management.c:196-211` `linux/brcmfmac/fwil_types.h:761`

linux sets the country only from the cfg80211 regulatory notifier: it reads the current "country", skips if alpha2 already matches, takes ccode and rev from a per-platform table, or as a fallback sends the ISO code in both fields with rev 0. `linux/brcmfmac/cfg80211.c:8180-8234`

linux ignores regulatory requests for "00" and for any code whose two characters are not both 'A'..'Z'. `linux/brcmfmac/cfg80211.c:8469-8479`

### Host-side encoding

c-driver encodes a country as a 32-bit value: byte 0 and byte 1 are the two letters, bits 31:16 the revision (`CYW43_COUNTRY(A,B,REV)`); worldwide is "XX" rev 0. `c-driver/cyw43_country.h:24` `c-driver/cyw43_country.h:33-34`

On SDIO builds c-driver sends the worldwide code with revision 17; its comment ties this to the 1DX CLM and a throughput gain of about 25%. `c-driver/cyw43_ll.c:2005-2011`

whd uses the same packing (low 16 bits code, high 16 bits revision). `whd/src/whd_management.c:198-202`

whd initialises its internal status to country AUSTRALIA with aggregate code XV/0 before the caller's country is stored at platform init. `whd/src/whd_chip.c:107-114` `whd/src/whd_management.c:341`

`whd_init` stores the caller's country in the driver, substituting WHD_COUNTRY_UNITED_STATES when the configured value is 0. `whd/src/whd_management.c:255-258`

whd sends command 320 (WLC_SET_CUSTOM_COUNTRY) only for the 43362; for any other chip id the function returns WHD_UNSUPPORTED. `whd/src/whd_chip.c:791-818` `whd/src/include/whd_wlioctl.h:4270`

### Settle time after setting the country
| Driver | Handling | Citations |
|---|---|---|
| c-driver | Delays 50 ms; its comment says the command takes about 32 ms | `c-driver/cyw43_ll.c:2013-2024` `c-driver/cyw43_ll.c:2024` |
| embassy | Delays 100 ms; its comment says the next commands fail without the wait | `embassy/control.rs:286-287` `embassy/control.rs:287` |
| whd | No delay; retries the next command (event mask) up to 3 times (MAX_POST_SET_COUNTRY_RETRY) | `whd/src/whd_management.c:52` `whd/src/whd_management.c:509-525` `whd/src/whd_management.c:513-525` |
| linux | No delay; calls `brcmf_setup_wiphybands` afterwards | `linux/brcmfmac/cfg80211.c:8494-8499` |

## Post-download configuration

### Comparison
| Step | embassy | c-driver | whd | linux | Citations |
|---|---|---|---|---|---|
| "clmload" | yes | yes | yes | yes, if a blob file exists | `embassy/control.rs:263-340` `c-driver/cyw43_ll.c:1913-1942` `whd/src/whd_management.c:393-631` `linux/brcmfmac/common.c:265-457` |
| "bus:txglom" = 0 | yes | yes | yes | not in common pre-init; set in the SDIO bus pre-init only when the SDIO core rev is < 12 | `embassy/control.rs:263-340` `c-driver/cyw43_ll.c:1913-1942` `whd/src/whd_management.c:393-631` `linux/brcmfmac/common.c:265-457` `linux/brcmfmac/sdio.c:3553-3569` |
| "apsta" = 1 | yes | yes | yes | never set in pre-init | `embassy/control.rs:263-340` `c-driver/cyw43_ll.c:1913-1942` `whd/src/whd_management.c:393-631` `linux/brcmfmac/common.c:265-457` |
| "country" | yes | yes | yes | not in pre-init | `embassy/control.rs:263-340` `c-driver/cyw43_ll.c:2000-2070` `whd/src/whd_management.c:393-631` `linux/brcmfmac/common.c:265-457` |
| Event mask | yes | yes | yes | yes | `embassy/control.rs:263-340` `c-driver/cyw43_ll.c:2000-2070` `whd/src/whd_management.c:393-631` `linux/brcmfmac/common.c:265-457` |
| WLC_UP (2) | yes | yes | yes | not in pre-init | `embassy/control.rs:263-340` `c-driver/cyw43_ll.c:2000-2070` `whd/src/whd_management.c:393-631` `linux/brcmfmac/common.c:265-457` |
| WLC_SET_GMODE (110) = 1 | yes | yes (in `cyw43_ll_wifi_pm`) | yes | not in pre-init | `embassy/control.rs:263-340` `c-driver/cyw43_ll.c:2165-2173` `whd/src/whd_management.c:393-631` `linux/brcmfmac/common.c:265-457` |
| WLC_SET_ANTDIV = 0, "ampdu_ba_wsize" = 8, "ampdu_mpdu" = 4, WLC_SET_BAND = 0 | yes | yes (WLC_SET_BAND in `cyw43_ll_wifi_pm`) | not found in `whd_wifi_on` | never set in pre-init (antdiv, ampdu values) | `embassy/control.rs:263-340` `c-driver/cyw43_ll.c:2000-2070` `c-driver/cyw43_ll.c:2165-2173` `whd/src/whd_management.c:393-631` `linux/brcmfmac/common.c:265-457` |
| "ampdu_rx_factor" = 0 | no (its comment says it crashes) | yes | not found in `whd_wifi_on` | not found in pre-init | `embassy/control.rs:263-340` `c-driver/cyw43_ll.c:2000-2070` `whd/src/whd_management.c:393-631` `linux/brcmfmac/common.c:265-457` |
| mpc, join_pref, scan times, txbf, revinfo, ver | not found in `Control::init` | not found in bus_init / wifi_on | not found for the 43439 in `whd_wifi_on` ("mpc" is set only for 43909 / 43907 / 54907 and 55900) | yes | `linux/brcmfmac/common.c:405-454` `linux/brcmfmac/common.c:265-457` `embassy/control.rs:263-340` `c-driver/cyw43_ll.c:1913-1942` `c-driver/cyw43_ll.c:2000-2070` `whd/src/whd_management.c:393-631` `whd/src/whd_management.c:546-570` |

### Event mask named variable
| Driver | Named variable | Payload | Citations |
|---|---|---|---|
| embassy | "bsscfg:event_msgs" | u32 interface index + 24-byte mask | `embassy/control.rs:305-319` `embassy/structs.rs:437-440` |
| c-driver | "bsscfg:event_msgs" | 4-byte interface index + 19-byte mask | `c-driver/cyw43_ll.c:2050-2060` `c-driver/cyw43_ll.c:2060` |
| whd (init) | "event_msgs" | 16-byte mask only | `whd/src/whd_management.c:516-524` `whd/src/include/whd_wlioctl.h:1932` |
| linux | "event_msgs" | Mask only, `fweh->event_mask_len` bytes (a length set at run time) | `linux/brcmfmac/common.c:415-429` `linux/brcmfmac/common.c:415-416` |

### MAC address

The MAC address named variable is "cur_etheraddr" (6 bytes) in all four drivers. `embassy/control.rs:846-851` `c-driver/cyw43_ll.c:1940-1942` `linux/brcmfmac/common.c:223-232` `whd/src/whd_wifi.c:59-113`

| Driver | Use | Citations |
|---|---|---|
| embassy | Only reads it | `embassy/control.rs:846-851` |
| c-driver | Writes the host's MAC by default | `c-driver/cyw43_ll.c:1940-1942` `c-driver/cyw43_ll.c:2072-2083` |
| linux | Writes the host's MAC if valid, else reads the chip's | `linux/brcmfmac/common.c:223-232` `linux/brcmfmac/common.c:277-299` |
| whd | Offers `whd_wifi_set_mac_address`; for an AP-role interface it flips the locally-administered bit 0x02 of the first octet before setting | `whd/src/whd_wifi.c:59-113` |

### embassy

Sequence of `Control::init`. `embassy/control.rs:263-340`

| Step | Action | Citations |
|---|---|---|
| 1 | CLM download via "clmload", then assert clmload_status == 0 | `embassy/control.rs:263-264` `embassy/control.rs:227-260` |
| 2 | Set named variable "bus:txglom" = 0 (u32) | `embassy/control.rs:268-271` |
| 3 | Set named variable "apsta" = 1 (u32) | `embassy/control.rs:272` |
| 4 | Get named variable "cur_etheraddr" (6 bytes) to learn the MAC address | `embassy/control.rs:274-276` `embassy/control.rs:846-851` |
| 5 | Set named variable "country" (12-byte struct, rev -1 if the configured rev is 0), then wait 100 ms | `embassy/control.rs:278-287` |
| 6 | Command SetAntdiv (64) = 0 (chip antenna) | `embassy/control.rs:289-290` `embassy/consts.rs:503` |
| 7 | Set named variable "bus:txglom" = 0 again, then wait 100 ms | `embassy/control.rs:292-293` |
| 8 | Set named variable "ampdu_ba_wsize" = 8, wait 100 ms | `embassy/control.rs:296-297` |
| 9 | Set named variable "ampdu_mpdu" = 4, wait 100 ms. "ampdu_rx_factor" = 0 and a second "apsta" = 1 are commented out with the note that they crash | `embassy/control.rs:294-300` |
| 10 | Set named variable "bsscfg:event_msgs" with { u32 iface = 0, 24-byte mask all 0xFF except the bits for RADIO, IF, PROBREQ_MSG, PROBREQ_MSG_RX, PROBRESP_MSG, ROAM }, wait 100 ms | `embassy/control.rs:304-321` `embassy/structs.rs:437-448` |
| 11 | Command Up (2) with empty payload, wait 100 ms | `embassy/control.rs:323-326` `embassy/control.rs:343-345` `embassy/consts.rs:450` |
| 12 | Command SetGmode (110) = 1 (auto), then command SetBand (142) = 0 (any), wait 100 ms | `embassy/control.rs:328-331` `embassy/consts.rs:543` `embassy/consts.rs:575` |
| 13 | Host-side only: publish the MAC address to the network stack and ask the runner to re-apply the multicast filter list | `embassy/control.rs:333-340` |

Power management is not set by init. It is a separate call, `set_power_management`: "pm2_sleep_ret", "bcn_li_bcn", "bcn_li_dtim", "assoc_listen" when mode 2, then command SetPm (86). `embassy/control.rs:353-363` `embassy/consts.rs:522`

### c-driver
| Step | Function | Action | Citations |
|---|---|---|---|
| 1 | `cyw43_ll_bus_init` | Wake the bus (KSO), then CLM download via "clmload" and read "clmload_status" | `c-driver/cyw43_ll.c:1911-1916` |
| 2 | bus_init | Set named variable "bus:txglom" = 0 on interface 0 | `c-driver/cyw43_ll.c:1918` |
| 3 | bus_init | Set named variable "apsta" = 1 | `c-driver/cyw43_ll.c:1919` |
| 4 | bus_init | If a MAC address is supplied, set named variable "cur_etheraddr" (6 bytes). With CYW43_USE_OTP_MAC (default 0) it first gets "cur_etheraddr" and generates a locally administered MAC if the get fails or the reply equals the constant 00:A0:50:b5:59:5e that c-driver calls the default MAC | `c-driver/cyw43_ll.c:1921-1942` `c-driver/cyw43_config.h:127-128` |
| 5 | `cyw43_ll_wifi_on` | Set named variable "country" (code, rev or -1, code), delay 50 ms | `c-driver/cyw43_ll.c:2013-2024` |
| 6 | wifi_on, debug builds only | Get named variable "clmver" (128 bytes) and print it | `c-driver/cyw43_ll.c:2026-2031` |
| 7 | wifi_on | Command WLC_SET_ANTDIV (64) = 0 | `c-driver/cyw43_ll.c:2033-2034` `c-driver/cyw43_ll.c:176` |
| 8 | wifi_on | Set named variables "bus:txglom" = 0, "apsta" = 1, "ampdu_ba_wsize" = 8, "ampdu_mpdu" = 4, "ampdu_rx_factor" = 0, in that order | `c-driver/cyw43_ll.c:2036-2041` |
| 9 | wifi_on | Wait until at least 150 ms have passed since bus init started | `c-driver/cyw43_ll.c:2043-2048` |
| 10 | wifi_on | Set named variable "bsscfg:event_msgs": 18 name bytes, 4 bytes for the interface index (not written by this function), then a 19-byte mask of all 0xFF with events 20 (tx fail), 40 (radio), 44 (probe request), 54 (interface change) and 71 (probe response) cleared; total 41 bytes; delay 50 ms | `c-driver/cyw43_ll.c:2050-2062` |
| 11 | wifi_on | Command WLC_UP (2) with no payload, delay 50 ms | `c-driver/cyw43_ll.c:2064-2067` `c-driver/cyw43_ll.c:167` |
| 12 | `cyw43_wifi_set_up` -> `cyw43_wifi_pm` with CYW43_DEFAULT_PM (PM2, 200 ms, beacon 1, dtim 1, assoc 10) | Set named variables "pm2_sleep_ret" (value x 10 ms, clamped to 10..2000), "bcn_li_bcn", "bcn_li_dtim", "assoc_listen" | `c-driver/cyw43_ctrl.c:559-568` `c-driver/cyw43.h:784-810` `c-driver/cyw43_ll.c:2135-2156` |
| 13 | wifi_pm | Command WLC_SET_PM (86) = mode, command WLC_SET_GMODE (110) = 1 (auto), command WLC_SET_BAND (142) = 0 (any) | `c-driver/cyw43_ll.c:2165-2173` `c-driver/cyw43_ll.c:179-182` |

### linux
| Step | Function | Action | Citations |
|---|---|---|---|
| 1 | `brcmf_sdio_bus_preinit` | If SDIO core rev < 12, set named variable "bus:txglom" = 0; else set "bus:txglomalign" = max(sd_sgentry_align, ALIGNMENT) | `linux/brcmfmac/sdio.c:3553-3569` `linux/brcmfmac/core.c:1251-1254` |
| 2 | bus_preinit | If the host supports scatter-gather, set named variable "bus:rxglom" = 1; failure is allowed (then no tx glomming) | `linux/brcmfmac/sdio.c:3574-3587` |
| 3 | `brcmf_c_preinit_dcmds` | If the host has a valid MAC, set named variable "cur_etheraddr"; else get it, and if it equals the known default 00:90:4c:c5:12:38, replace it with a random MAC and set that | `linux/brcmfmac/common.c:244-246` `linux/brcmfmac/common.c:277-299` |
| 4 | preinit | Command BRCMF_C_GET_REVINFO (98) to read vendor / device / radio / core / board / driver / ucode / phy / chip revision info; failure is tolerated | `linux/brcmfmac/common.c:307-335` `linux/brcmfmac/fwil.h:53` |
| 5 | preinit | CLM download via "clmload" if a CLM blob file exists | `linux/brcmfmac/common.c:341-346` |
| 6 | preinit | TxCap blob via "txcapload" if present, then calibration blob via "calload" if the platform provides one | `linux/brcmfmac/common.c:348-360` |
| 7 | preinit | Get named variable "ver" (firmware version string; first line kept, last word used as the version number) | `linux/brcmfmac/common.c:362-383` |
| 8 | preinit | Get named variable "clmver"; failure ignored | `linux/brcmfmac/common.c:385-403` |
| 9 | preinit | Set named variable "mpc" = 1 | `linux/brcmfmac/common.c:405-410` |
| 10 | preinit | Set named variable "join_pref" with two entries: RSSI_DELTA (len 2, gain 8, band 5G), then RSSI (len 2, gain 0, band 0) | `linux/brcmfmac/common.c:80-100` `linux/brcmfmac/common.c:31-32` `linux/brcmfmac/common.c:412` |
| 11 | preinit | Get named variable "event_msgs", set the BRCMF_E_IF bit, set named variable "event_msgs" back | `linux/brcmfmac/common.c:414-433` |
| 12 | preinit | Command BRCMF_C_SET_SCAN_CHANNEL_TIME (185) = 40, then BRCMF_C_SET_SCAN_UNASSOC_TIME (187) = 40 | `linux/brcmfmac/common.c:28-29` `linux/brcmfmac/common.c:435-451` `linux/brcmfmac/fwil.h:71-72` |
| 13 | preinit | Set named variable "txbf" = 1, errors ignored | `linux/brcmfmac/common.c:453-454` |
| 14 | after preinit | Feature detection (`brcmf_feat_attach`), protocol init done, cfg80211 attach, net attach. The queries sent inside `brcmf_feat_attach` and `brcmf_cfg80211_attach` are not listed here | `linux/brcmfmac/core.c:1256-1276` |
| 15 | `brcmf_config_dongle`, on first interface up | Command BRCMF_C_UP (2) = 0; scan-time setup (15a); command BRCMF_C_SET_PM (86) = PM_FAST or PM_OFF; roam setup (15b); interface type change; ARP/ND offload; command BRCMF_C_SET_FAKEFRAG (219) = 1 (frameburst). The commands sent inside `brcmf_cfg80211_change_iface` and `brcmf_configure_arp_nd_offload` are not listed here | `linux/brcmfmac/cfg80211.c:8000-8049` `linux/brcmfmac/fwil.h:15` `linux/brcmfmac/fwil.h:52` `linux/brcmfmac/fwil.h:76` |
| 15a | `brcmf_dongle_scantime`, after BRCMF_C_UP | Command BRCMF_C_SET_SCAN_CHANNEL_TIME (185) = 40, BRCMF_C_SET_SCAN_UNASSOC_TIME (187) = 40, BRCMF_C_SET_SCAN_PASSIVE_TIME (258) = 120, in that order; the first failure stops the sequence | `linux/brcmfmac/cfg80211.c:7158-7186` `linux/brcmfmac/cfg80211.c:84-86` `linux/brcmfmac/cfg80211.c:8019` `linux/brcmfmac/fwil.h:71-72` `linux/brcmfmac/fwil.h:79` |
| 15b | `brcmf_dongle_roam`, after BRCMF_C_SET_PM | Set named variable "bcn_timeout" = 2 (4 when the roamoff setting is on); set named variable "roam_off" = the roamoff setting; command BRCMF_C_SET_ROAM_TRIGGER (55) with two le32 { -75, BRCM_BAND_ALL }; command BRCMF_C_SET_ROAM_DELTA (57) with two le32 { 20, BRCM_BAND_ALL }. Errors on the first two abort; errors on the last two are only logged. BRCM_BAND_ALL is 3 | `linux/brcmfmac/cfg80211.c:7107-7156` `linux/include/defs.h:64` `linux/brcmfmac/cfg80211.h:25-26` `linux/brcmfmac/cfg80211.h:92-93` `linux/brcmfmac/fwil.h:44-45` |

### whd

Sequence of `whd_wifi_on`. `whd/src/whd_management.c:393-631`

| Step | Action | Citations |
|---|---|---|
| 1 | Bus init (includes firmware/NVRAM download and start), protocol attach, state OFF -> DOWN, start the whd thread, add the primary interface | `whd/src/whd_management.c:424-432` `whd/src/whd_management.c:328-382` |
| 2 | CLM download via "clmload" (`whd_process_clm_data`); failure is fatal | `whd/src/whd_management.c:434-443` |
| 3 | Shared-bus Bluetooth init (`whd_bus_share_bt_init`; not for msgbuf). It only records the driver pointer in a host global (`g_bt_whd_driver`); no command or register access. Result not fatal | `whd/src/whd_management.c:445-451` `whd/src/bus_protocols/whd_bus.c:45-51` |
| 4 | Read firmware capabilities (`whd_wifi_read_fw_capabilities`): get named variable "cap" into a 768-byte buffer (MAX_CAPS_BUFFER_SIZE) and look for the substrings "sae ", "sae_ext ", "offloads ", "gcmp ", "icmp ", setting one fwcap flag bit per match. Result not fatal | `whd/src/whd_management.c:453-458` `whd/src/whd_chip.c:87-94` `whd/src/whd_chip.c:998-1020` `whd/src/whd_chip.c:60` `whd/src/include/whd_wlioctl.h:1162` |
| 5 | Set named variable "bus:txglom" = 0 (unsupported is tolerated) | `whd/src/whd_management.c:460-479` `whd/src/include/whd_wlioctl.h:1088` |
| 6 | Set named variable "apsta" = 1 (unsupported is tolerated, e.g. manufacturing-test firmware) | `whd/src/whd_management.c:481-499` `whd/src/include/whd_wlioctl.h:1071` |
| 7 | Set named variable "country" (see Country) | `whd/src/whd_management.c:500-507` `whd/src/whd_management.c:169-214` |
| 8 | Set named variable "event_msgs" to a 16-byte all-zero mask (no asynchronous events initially), retried up to 3 times | `whd/src/whd_management.c:512-530` `whd/src/include/whd_wlioctl.h:1932` `whd/src/include/whd_wlioctl.h:1074` |
| 9 | Command WLC_UP (2) | `whd/src/whd_management.c:532-533` `whd/src/whd_wifi_api.c:424` `whd/src/include/whd_wlioctl.h:1305` |
| 10 | If the "offloads" capability flag was set in step 4, call `whd_wifi_offload_config`: set named variable "offload_config" with a `wl_ol_cfg_v1_t` record (version 1, id WL_OL_CFG_ID_PROF, offload_skip = NOT of the feature mask, profile type low power), then `whd_configure_tko_offload`, whose failure is only logged | `whd/src/whd_management.c:535-544` `whd/src/whd_wifi_api.c:805-849` `whd/src/include/whd_wlioctl.h:1270` |
| 11 | Enable PM2 power save with return-to-sleep 200 ms: set named variable "pm2_sleep_ret", then command WLC_SET_PM (86) = PM2. 43909 / 43907 / 54907 instead disable power save and set "mpc" = 0 | `whd/src/whd_management.c:546-570` `whd/src/whd_management.c:56` `whd/src/whd_wifi_api.c:3905-3919` `whd/src/include/whd_wlioctl.h:1377` |
| 12 | Command WLC_SET_GMODE (110) = GMODE_AUTO (1) (not for msgbuf) | `whd/src/whd_management.c:580-596` `whd/src/include/whd_wlioctl.h:1398` `whd/src/include/whd_wlioctl.h:1674` |
| 13 | Chip-specific extras that do not apply to the 43439: scan-MAC randomisation off (55500), "ampdu_hostreorder" off (55500 / 55530 / 55572 / 55900) | `whd/src/whd_management.c:598-619` |
