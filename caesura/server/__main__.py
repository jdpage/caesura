#!/usr/bin/env python3
"""Command-line driver for caesura server.
"""
__author__ = "Jonathan David Page"
__copyright__ = "Copyright 2014, Jonathan David Page"

import logging
from . import core

# set up logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s: %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

# turn down the volume on asyncio
logger.getChild("asyncio").setLevel(logging.WARNING)

server = core.CaesuraServer('', 8888)
server.run()
