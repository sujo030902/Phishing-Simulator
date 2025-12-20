from http.server import BaseHTTPRequestHandler
from api.utils import send_json, check_options

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        check_options(self)

    def do_GET(self):
        send_json(self, 200, {'status': 'healthy', 'service': 'phishing-simulator-serverless'})
