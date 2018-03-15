#!/usr/bin/env python3

from __future__ import print_function

import json
import os
import sys
import time

from matrix_client.client import MatrixClient

from config import config


class MatrixSendServer:
    def __init__(self, config, room):
        self.queue_path = config['queue_path']
        self.client = MatrixClient(config['homeserver_uri'])
        self.token = self.client.login_with_password(username=config['username'],
                                                     password=config['password'])
        self.room = self.client.join_room(room)
        self.room_id = room
        self.message_queue = []
        self.limited_until = None

    def dequeue(self):
        """Dequeue as many messages as the server lets us"""
        for f in self.message_queue:
            with open(f, "r", encoding="UTF-8") as fin:
                message = fin.read()

            if self.limited_until is not None and time.time() * 1000 < self.limited_until:
                return

            try:
                self.room.send_text(message)
                self.message_queue.pop(0)
            except Exception as e:
                necessary_delay = json.loads(e.content)['retry_after_ms']
                sys.stderr.write("Sleeping for %s seconds... Queue depth %s\n" % (necessary_delay, len(self.message_queue)))
                sys.stderr.flush()
                self.limited_until = time.time() * 1000 + necessary_delay
            else:
                os.remove(f)

    def enqueue(self, f):
        if os.path.isfile(f) and not f in self.message_queue:
            self.message_queue.append(f)

    def run(self):
        print("run!")
        while True:
            for f in os.listdir(self.queue_path):
                f = os.path.join(self.queue_path, f)
                self.enqueue(f)
            self.dequeue()
            time.sleep(10)

MatrixSendServer(config, config['room']).run()
