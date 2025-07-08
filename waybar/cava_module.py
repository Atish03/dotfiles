#!/bin/python3
import os
import struct
import subprocess
import tempfile
import json

BARS_NUMBER = 20
# OUTPUT_BIT_FORMAT = "8bit"
OUTPUT_BIT_FORMAT = "16bit"
# RAW_TARGET = "/tmp/cava.fifo"
RAW_TARGET = "/dev/stdout"
SENSITIVITY = 150

conpat = """
[general]
bars = %d
sensitivity = %d
[output]
method = raw
raw_target = %s
bit_format = %s
"""

config = conpat % (BARS_NUMBER, SENSITIVITY, RAW_TARGET, OUTPUT_BIT_FORMAT)
bytetype, bytesize, bytenorm = ("H", 2, 65535) if OUTPUT_BIT_FORMAT == "16bit" else ("B", 1, 255)

bar_map = {
        0: "⠁",
        1: "⠁",
        2: "⠃",
        3: "⠇",
        4: "⡇"
        }

def run():
    with tempfile.NamedTemporaryFile() as config_file:
        config_file.write(config.encode())
        config_file.flush()

        process = subprocess.Popen(["cava", "-p", config_file.name], stdout=subprocess.PIPE)
        chunk = bytesize * BARS_NUMBER
        fmt = bytetype * BARS_NUMBER

        if RAW_TARGET != "/dev/stdout":
            if not os.path.exists(RAW_TARGET):
                os.mkfifo(RAW_TARGET)
            source = open(RAW_TARGET, "rb")
        else:
            source = process.stdout

        while True:
            data = source.read(chunk)
            if len(data) < chunk:
                break
            # sample = [i for i in struct.unpack(fmt, data)]  # raw values without norming
            sample = "".join([bar_map[int((i / bytenorm) * 4)] for i in struct.unpack(fmt, data)])
            
            output = {
                "text": sample,
                "class": "custom-cava"
            }

            print(json.dumps(output), flush=True)

if __name__ == "__main__":
    run()

