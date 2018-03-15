#!/usr/bin/env python3
import io
import os
import sys
import datetime
from config import config


filename = str(datetime.datetime.now()).replace(":","-").replace(" ","_")
filepath = os.path.join(config['queue_path'], filename)

input_stream = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')

inheader=True
with open(filepath, "w", encoding="UTF-8") as fout:
    for l in input_stream:
        if not inheader:
            fout.write(l)
        if inheader and (l.startswith("From:") or l.startswith("Subject:")):
            fout.write(l)
        if inheader and l.strip()=="":
            inheader = False
