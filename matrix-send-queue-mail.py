#!/usr/bin/env python3
import io
import os
import sys
import datetime
import mailparser
from config import config



filename = str(datetime.datetime.now()).replace(":","-").replace(" ","_")
filepath = os.path.join(config['queue_path'], filename)

# input_stream = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')

message = mailparser.parse_from_file_obj(sys.stdin)

mfrom = ", ".join([" ".join(r) for r in message.from_])
msubj = message.subject
mbody = "\n\n".join(message.text_plain)

with open(filepath, "w", encoding="UTF-8") as fout:
    fout.write("From: {}\n".format(mfrom))
    fout.write(msubj  + "\n\n")
    fout.write(mbody)

