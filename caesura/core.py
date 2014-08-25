import logging
import asyncio
from .web import server

logger = logging.getLogger(__name__)


class Caesura:
    def __init__(self):
        self.loop = asyncio.get_event_loop()
        webcoro = self.loop.create_server(server.WebRouter, '', 8888)
        self.web = self.loop.run_until_complete(webcoro)
        logger.info("created web server")

    def run(self):
        try:
            logger.info("started")
            self.loop.run_forever()
        except KeyboardInterrupt:
            logger.info("exit")
        finally:
            self.web.close()
            self.loop.close()

