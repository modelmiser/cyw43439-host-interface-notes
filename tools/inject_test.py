#!/usr/bin/env python3
"""Test transmitter for the Pico monitor-mode study. Run as root: sudo python3 -I inject_test.py mon0

Sends broadcast 802.11 data frames from a made-up address (02:c0:ff:ee:00:01) through a monitor
interface, in timed phases of different frame sizes and rates, and counts what the same interface
hears. It changes no settings, touches no other interface, and stops by itself after about 7.5
minutes (Ctrl+C stops it at once). Writes one JSON line per event to the log file named below.

Airtime: no rate is requested, so the card sends at its own default. At a low rate the 400-byte and
1,400-byte phases (46 s each) can take a large share of the channel. Use a channel you are entitled
to load, and expect other traffic on it to slow down meanwhile.
"""
import json
import os
import socket
import struct
import sys
import threading
import time
from datetime import datetime, timezone

IFACE = sys.argv[1] if len(sys.argv) > 1 else "mon0"
LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "inject-log.jsonl")
MARK = bytes.fromhex("02c0ffee0001")
BROADCAST = b"\xff" * 6
RADIOTAP = bytes.fromhex("0000080000000000")  # version 0, length 8, no fields

# (name, seconds, frame length in bytes incl. the 24-byte 802.11 header, frames per second)
PHASES = [
    ("none-start", 120, 0, 0),
    ("small-200", 46, 60, 200),
    ("large-25", 46, 1400, 25),
    ("medium-100", 46, 400, 100),
    ("small-5", 46, 60, 5),
    ("none-mid", 46, 0, 0),
    ("large-5", 46, 1400, 5),
    ("small-200-again", 46, 60, 200),
]


def now():
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds")


def frame(length, phase, seq):
    header = struct.pack("<HH", 0x0008, 0) + BROADCAST + MARK + MARK + struct.pack("<H", (seq & 0xFFF) << 4)
    body = bytes.fromhex("aaaa0300000088b5") + struct.pack("<BI", phase, seq)
    body += b"\x5a" * max(0, length - len(header) - len(body))
    return RADIOTAP + header + body[: max(0, length - len(header))]


heard = {"frames": 0, "beacons": 0, "ours": 0}
stop = False


def listen(sock):
    while not stop:
        try:
            data = sock.recv(4096)
        except socket.timeout:
            continue
        except OSError:
            return
        if len(data) < 4:
            continue
        rt_len = struct.unpack_from("<H", data, 2)[0]
        dot11 = data[rt_len:]
        if not dot11:
            continue
        heard["frames"] += 1
        if dot11[0] == 0x80:
            heard["beacons"] += 1
        if len(dot11) >= 16 and dot11[10:16] == MARK:
            heard["ours"] += 1


def main():
    global stop
    sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x0003))
    sock.bind((IFACE, 0))
    sock.settimeout(0.5)
    log = open(LOG, "a", buffering=1)
    threading.Thread(target=listen, args=(sock,), daemon=True).start()
    log.write(json.dumps({"utc": now(), "event": "start", "iface": IFACE, "phases": PHASES}) + "\n")
    print("test transmitter started on", IFACE, "- runs about 7.5 minutes; log:", LOG, flush=True)
    seq = 0
    try:
        for index, (name, seconds, length, rate) in enumerate(PHASES):
            for key in heard:
                heard[key] = 0
            sent = errors = 0
            begin = time.monotonic()
            log.write(json.dumps({"utc": now(), "event": "phase-start", "phase": name, "length": length, "rate": rate}) + "\n")
            print(now(), "phase", name, flush=True)
            while True:
                elapsed = time.monotonic() - begin
                if elapsed >= seconds:
                    break
                if rate == 0:
                    time.sleep(0.2)
                    continue
                due = int(elapsed * rate)
                while sent + errors < due:
                    try:
                        sock.send(frame(length, index, seq))
                        sent += 1
                    except OSError:
                        errors += 1
                    seq += 1
                time.sleep(min(0.002, 1.0 / rate))
            log.write(json.dumps({"utc": now(), "event": "phase-end", "phase": name, "sent": sent,
                                  "send_errors": errors, **{"heard_" + k: v for k, v in heard.items()}}) + "\n")
    except KeyboardInterrupt:
        log.write(json.dumps({"utc": now(), "event": "interrupted"}) + "\n")
    finally:
        stop = True
        log.write(json.dumps({"utc": now(), "event": "end"}) + "\n")
        sock.close()
    print("done", flush=True)


if __name__ == "__main__":
    main()
