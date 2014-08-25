import aiohttp
import aiohttp.server
import asyncio
import logging
import json

logger = logging.getLogger(__name__)

API_LEVELS = [(0, 1, 0)]


class Endpoint:
    def __init__(self, server):
        self.server = server

    @asyncio.coroutine
    def handle(self, path_args, message, payload):
        logger.debug(message)
        if message.method == 'GET':
            response = yield from self.handle_get(message, **path_args)
        elif message.method == 'POST':
            response = yield from self.handle_post(message, **path_args)
        elif message.method == 'DELETE':
            response = yield from self.handle_delete(message, **path_args)
        elif message.method == 'PUT':
            response = yield from self.handle_put(message, **path_args)
        else:
            response = yield from self.server.handle_error(status=405,
                                                           message=message)
        return response

    def handle_get(self, message, *args, **kwargs):
        return (yield from self.handle_unsupported(message))

    def handle_post(self, message, *args, **kwargs):
        return (yield from self.handle_unsupported(message))

    def handle_put(self, message, *args, **kwargs):
        return (yield from self.handle_unsupported(message))

    def handle_delete(self, message, *args, **kwargs):
        return (yield from self.handle_unsupported(message))

    def handle_error(self, status=500):
        try:
            try:
                reason, msg = aiohttp.server.RESPONSES[status]
            except KeyError:
                status = 500
                reason, msg = '???', ''
            return (yield from self.respond(
                {'status': status,
                 'message': msg,
                 'reason': reason},
                status=status,
                close=True))
        finally:
            self.server.keep_alive(False)

    def handle_unsupported(self, message, *args, **kwargs):
        return (yield from self.handle_error(status=405))

    def respond(self, data, status=200, mime='application/json',
                close=False):
        body = json.dumps(data).encode('utf-8')
        response = aiohttp.Response(self.server.writer, status, close=close)
        response.add_headers(
            ('Content-type', '%s; charset=utf-8' % mime),
            ('Content-length', str(len(body))))
        response.send_headers()
        yield from response.write(body)
        yield from response.write_eof()
        return response


class NotFoundEndpoint(Endpoint):
    def handle_get(self, message, *args, **kwargs):
        return (yield from self.handle_error(404))


class ServerInfoEndpoint(Endpoint):
    def handle_get(self, message, *args, **kwargs):
        result = {
            'api_levels': ["%d.%d" % v for v in API_LEVELS],
            'endpoints': ["metadata", "audio", "users"],
        }
        return (yield from self.respond(result))


class MetadataInfoEndpoint(Endpoint):
    pass


class PagedQueryEndpoint(Endpoint):
    pass


class GroupCollectionEndpoint(Endpoint):
    pass


class GroupEndpoint(Endpoint):
    pass


class PeopleCollectionEndpoint(Endpoint):
    pass


class PeopleEndpoint(Endpoint):
    pass


class AlbumCollectionEndpoint(Endpoint):
    pass


class AlbumEndpoint(Endpoint):
    pass


class SongCollectionEndpoint(Endpoint):
    pass


class SongEndpoint(Endpoint):
    pass


class TrackCollectionEndpoint(Endpoint):
    pass


class TrackEndpoint(Endpoint):
    pass


class AudioCollectionEndpoint(Endpoint):
    pass


class AudioEndpoint(Endpoint):
    pass


class UserCollectionEndpoint(Endpoint):
    pass


class UserEndpoint(Endpoint):
    pass


class PlaylistCollectionEndpoint(Endpoint):
    pass


class PlaylistEndpoint(Endpoint):
    pass


class PlaylistEntryEndpoint(Endpoint):
    pass
