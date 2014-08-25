__author__ = "Jonathan David Page"
__copyright__ = "Copyright 2014, Jonathan David Page"

from . import async_client
import asyncio


_loop = asyncio.get_event_loop()


def _synchronize(f):
    def fun(*args, **kwargs):
        return _loop.run_until_complete(f(*args, **kwargs))
    return fun


class CaesuraClient(async_client.CaesuraClient):
    @_synchronize
    def api_levels(self):
        return super().api_levels()

    @_synchronize
    def version_ok(self):
        return super().version_ok()
