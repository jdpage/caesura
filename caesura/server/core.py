"""caesura server object.
"""
__author__ = "Jonathan David Page"
__copyright__ = "Copyright 2014, Jonathan David Page"

import logging
import asyncio
from .web import server

logger = logging.getLogger(__name__)


class CaesuraServer:
    def __init__(self, hostname, port):
        self.hostname = hostname
        self.port = port
        self.web = None

    def start(self):
        loop = asyncio.get_event_loop()
        self.web = yield from loop.create_server(server.WebRouter,
                                                 self.hostname, self.port)
        logger.info("created web server")

    def stop(self):
        self.web.close()

    def run(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.start())
        try:
            logger.info("started")
            loop.run_forever()
        except KeyboardInterrupt:
            logger.info("exit")
        finally:
            self.stop()
            loop.close()

