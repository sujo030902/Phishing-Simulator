import json
from api.utils import parse_body, parse_path
from api import campaigns, templates

class MockReq:
    def __init__(self, method, path, body):
        self.method = method
        self.path = path
        self.body = body

print("parse_path tests")
for path in ['/api/campaigns/', '/api/campaigns/1/launch', '/api/campaigns/track/123/open', '/api/templates/analyze', '/api/templates/analyze/']:
    print(path, parse_path(path))

print('\nparse_body tests')
for body in [b'{"name":"Test","template_id":"1"}', b'', b'{}', b'notjson']:
    req = MockReq('POST', '/api/campaigns/', body)
    print('body', body, 'parsed', parse_body(req))

print('\nhandlers')
req = MockReq('POST','/api/campaigns/', b'{"name":"Test","template_id":"1"}')
print('campaign create', campaigns.handler(req))
req = MockReq('POST','/api/campaigns/1/launch', b'{"target_ids":[1]}')
print('campaign launch', campaigns.handler(req))
req = MockReq('POST','/api/campaigns/track/1/open', b'')
print('track old-style', campaigns.handler(req))
req = MockReq('POST','/api/campaigns/1/track/open', b'')
print('track new-style', campaigns.handler(req))
req = MockReq('POST','/api/templates/analyze', b'{"subject":"Hi","body":"<p>test</p>"}')
print('analyze', templates.handler(req))
req = MockReq('POST','/api/templates/generate', b'{"type":"CEO Fraud","sender_name":"John","context":"Test"}')
print('generate', templates.handler(req))
