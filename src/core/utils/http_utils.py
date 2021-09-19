import base64
import json
from starlette.datastructures import URL


def get_url_path(request) -> URL:
    scope = dict(request.scope)
    scope.update({"query_string": b""})
    return URL(scope=scope)


def encode_backend_state(redirect_uri, state) -> str:
    state = {
        'frontend': {
            'state': state,
            'redirect_uri': redirect_uri
        }
    }
    return base64.b64encode(json.dumps(state).encode('utf-8')).decode('utf-8')


def decode_backend_state(state: str):
    return json.loads(base64.b64decode(state.encode('utf-8')).decode('utf-8'))
