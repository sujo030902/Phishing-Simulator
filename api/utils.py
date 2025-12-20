import json
from urllib.parse import urlparse

def parse_path(path):
    """
    Parses the URL path into segments, ignoring query parameters.
    Example: '/api/campaigns?foo=bar' -> ['', 'api', 'campaigns']
    """
    parsed = urlparse(path)
    # Split by slash and ignore empty strings if needed, but keeping split behavior 
    # compatible with previous logic: ['', 'api', 'campaigns']
    return parsed.path.split('/')

def parse_body(request):
    """
    Parses JSON body from the request object.
    Supports request.body as bytes or string.
    """
    try:
        if not request.body:
            return {}
        
        body_content = request.body
        if isinstance(body_content, bytes):
            body_content = body_content.decode('utf-8')
            
        return json.loads(body_content)
    except Exception as e:
        print(f"Error parsing body: {e}")
        return {}

def cors_headers():
    return {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization',
        'Content-Type': 'application/json'
    }

def send_json(status, data):
    """
    Returns the Vercel response dictionary.
    """
    headers = cors_headers()
    return {
        "statusCode": status,
        "headers": headers,
        "body": json.dumps(data)
    }

def send_error(status, message):
    return send_json(status, {"error": message})

def handle_options():
    """
    Helper for OPTIONS method CORS handling.
    """
    headers = cors_headers()
    # CORS preflight typically expects 204 No Content
    return {
        "statusCode": 204,
        "headers": headers,
        "body": "" 
    }
