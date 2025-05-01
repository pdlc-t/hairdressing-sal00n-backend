# app/json_provider.py
from flask.json.provider import DefaultJSONProvider

class CustomJSONProvider(DefaultJSONProvider):
    def dumps(self, obj, **kwargs):
        # jeśli ktoś nie poda explicitnie ensure_ascii, wymusz na False
        kwargs.setdefault('ensure_ascii', False)
        return super().dumps(obj, **kwargs)
