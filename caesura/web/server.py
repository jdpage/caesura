import logging
import asyncio
from aiohttp.server import ServerHttpProtocol
import aiohttp
import time
from werkzeug.routing import Map, Rule, NotFound, RequestRedirect
from . import api

logger = logging.getLogger(__name__)

# goal: select all five iron tracks
# GET /metadata/tracks?group.name=Five+Iron+Frenzy

# goal: select Black Sabbath albums with Dio singing
# GET /metadata/albums?group.name=Black+Sabbath&group.singer.name_contains=Dio

# goal: select GY!BE releases from after they moved the exclamation point
# GET /metadata/releases?group.under_name=Godspeed+You%21+Black+Emperor

# searchable endpoints:
#   groups
#   people
#   albums
#   releases
#   songs
#   tracks

# quantifiers:
#   under_
#   all_
#   any_
#   some_
#   no_

# matches:
#   _is
#   _contains
#   _in


class WebRouter(ServerHttpProtocol):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.api_root = '/'
        self.url_map = Map([
            Rule('/',
                 endpoint=api.ServerInfoEndpoint),
            Rule('/paged_query',
                 endpoint=api.PagedQueryEndpoint),
            Rule('/metadata',
                 endpoint=api.MetadataInfoEndpoint),
            Rule('/metadata/groups',
                 endpoint=api.GroupCollectionEndpoint),
            Rule('/metadata/groups/<int:id>',
                 endpoint=api.GroupEndpoint),
            Rule('/metadata/people',
                 endpoint=api.PeopleCollectionEndpoint),
            Rule('/metadata/people/<int:id>',
                 endpoint=api.PeopleEndpoint),
            Rule('/metadata/albums',
                 endpoint=api.AlbumCollectionEndpoint),
            Rule('/metadata/albums/<int:id>',
                 endpoint=api.AlbumEndpoint),
            Rule('/metadata/songs',
                 endpoint=api.SongCollectionEndpoint),
            Rule('/metadata/songs/<int:id>',
                 endpoint=api.SongEndpoint),
            Rule('/metadata/tracks',
                 endpoint=api.TrackCollectionEndpoint),
            Rule('/metadata/tracks/<int:id>',
                 endpoint=api.TrackEndpoint),
            Rule('/audio',
                 endpoint=api.AudioCollectionEndpoint),
            Rule('/audio/<audio_name>.<format>',
                 endpoint=api.AudioEndpoint),
            Rule('/users',
                 endpoint=api.UserCollectionEndpoint),
            Rule('/users/<user_id>',
                 endpoint=api.UserEndpoint),
            Rule('/users/<user_id>/playlists',
                 endpoint=api.PlaylistCollectionEndpoint),
            Rule('/users/<user_id>/playlists/<pl_id>',
                 endpoint=api.PlaylistEndpoint),
            Rule('/users/<user_id>/playlists/<pl_id>/<entry_id>',
                 endpoint=api.PlaylistEntryEndpoint)
        ])

    @asyncio.coroutine
    def handle_request(self, message, payload):
        now = time.time()
        urls = self.url_map.bind(message.headers['HOST'], self.api_root)
        try:
            endpoint_type, path_args = urls.match(message.path)
        except NotFound:
            endpoint_type, path_args = api.NotFoundEndpoint, {}
        endpoint = endpoint_type(self)
        response = yield from endpoint.handle(path_args, message, payload)
        self.log_access(message, None, response, time.time() - now)


