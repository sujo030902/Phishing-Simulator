import json
import urllib.parse
from http.server import BaseHTTPRequestHandler

def check_options(handler):
    """
    Handles OPTIONS requests for CORS preflight.
    Returns True if the request was an OPTIONS request and has been handled.
    """
    if handler.command == 'OPTIONS':
        handler.send_response(204)
        _send_cors_headers(handler)
        handler.end_headers()
        return True
    return False

def _send_cors_headers(handler):
    """Internal helper to add CORS headers."""
    handler.send_header('Access-Control-Allow-Origin', '*')
    handler.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
    handler.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')

def parse_body(handler):
    """
    Reads and parses the JSON body from the request.
    Returns a dictionary. Returns empty dict on failure.
    """
    try:
        content_length_header = handler.headers.get('Content-Length')
        if not content_length_header:
            return {}
            
        content_length = int(content_length_header)
        if content_length == 0:
            return {}
            
        body = handler.rfile.read(content_length).decode('utf-8')
        if not body:
            return {}
            
        return json.loads(body)
    except Exception as e:
        print(f"Error parsing body: {e}")
        return {}

def parse_path(path):
    """
    Parses the path and returns a list of clean path segments.
    Ignores query parameters.
    Example: '/api/campaigns/123?foo=bar' -> ['api', 'campaigns', '123']
    """
    parsed_url = urllib.parse.urlparse(path)
    clean_path = parsed_url.path.strip('/')
    if not clean_path:
        return []
    return clean_path.split('/')

def send_json(handler, status, data):
    """
    Sends a JSON response with the given status code and data.
    """
    try:
        response_body = json.dumps(data).encode('utf-8')
    except Exception as e:
        response_body = json.dumps({"error": f"JSON serialization failed: {str(e)}"}).encode('utf-8')
        status = 500

    handler.send_response(status)
    handler.send_header('Content-Type', 'application/json')
    _send_cors_headers(handler)
    handler.end_headers()
    handler.wfile.write(response_body)

def send_error(handler, status, message):
    """
    Sends a JSON error response.
    """
    send_json(handler, status, {'error': message})
