from nose.tools import *
from caesura.client.async_client import CaesuraClient
from caesura.server import CaesuraServer
import asyncio

PORT = 8889
loop = asyncio.get_event_loop()


@nottest
def aio_test(f):
    @make_decorator(f)
    def test_aio_wrapped():
        return loop.run_until_complete(f())
    return test_aio_wrapped


def setup():
    global s, c
    s = CaesuraServer('', PORT)
    loop.run_until_complete(s.start())
    c = CaesuraClient('http://localhost:%d' % PORT)


def teardown():
    global s, c
    s.stop()
    s = None
    c = None


@aio_test
def test_api_level():
    levels = yield from c.api_levels()
    assert_equal(levels, [(0, 1, 0)])


@aio_test
def test_version_ok():
    ok = yield from c.version_ok()
    assert_true(ok)

