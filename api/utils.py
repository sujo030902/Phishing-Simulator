import json
from http.server import BaseHTTPRequestHandler

def check_options(handler):
    if handler.command == 'OPTIONS':
        handler.send_response(204)
        handler.send_header('Access-Control-Allow-Origin', '*')
        handler.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        handler.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        handler.end_headers()
        return True
    return False

def parse_body(handler):
    try:
        content_length = int(handler.headers.get('Content-Length', 0))
        if content_length == 0:
            return {}
        body = handler.rfile.read(content_length).decode('utf-8')
        return json.loads(body)
    except Exception as e:
        print(f"Error parsing body: {e}")
        return {}

def send_json(handler, status, data):
    try:
        response_body = json.dumps(data).encode('utf-8')
    except Exception as e:
        response_body = json.dumps({"error": f"JSON serialization failed: {str(e)}"}).encode('utf-8')
        status = 500

    handler.send_response(status)
    handler.send_header('Content-Type', 'application/json')
    handler.send_header('Access-Control-Allow-Origin', '*')
    handler.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
    handler.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    handler.end_headers()
    handler.wfile.write(response_body)

def send_error(handler, status, message):
    send_json(handler, status, {'error': message})
