import asyncio
from aiopg.sa import create_engine
import sqlalchemy as sa

class MusicDatabase:
    def __init__(self):
        self.metadata = sa.MetaData()

    @asyncio.coroutine
    def connect(self):
        self.engine = yield from create_engine(
                database='caesura',
                host='127.0.0.1')


