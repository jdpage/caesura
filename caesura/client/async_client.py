__author__ = "Jonathan David Page"
__copyright__ = "Copyright 2014, Jonathan David Page"

import aiohttp


class CaesuraClient:
    API_LEVEL = (0, 1, 0)

    def __init__(self, api_root: str):
        """create a new client for a given server
        :param api_root: the base url of the server
        """
        self.api_root = api_root
        if self.api_root.endswith('/'):
            self.api_root = self.api_root.rstrip('/')

    def api_levels(self):
        r = yield from aiohttp.request('get', self.api_root + "/")
        root = yield from r.json()
        levels = root['api_levels']
        return [tuple(int(x) for x in v.split('.')) for v in levels]

    def version_ok(self) -> bool:
        for remote_level in (yield from self.api_levels()):
            remote_major, remote_minor, remote_patch = remote_level
            my_major, my_minor, my_patch = self.API_LEVEL
            if my_major != remote_major:
                continue
            if my_major == 0 and my_minor != remote_minor:
                continue
            if my_minor <= remote_minor:
                return True
        return False





