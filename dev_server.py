from http.server import HTTPServer, BaseHTTPRequestHandler
import sys
import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Ensure we can import from api/
sys.path.append(os.getcwd())

from api import campaigns, targets, templates, health

PORT = 3000

class MockRequest:
    def __init__(self, method, path, body):
        self.method = method
        self.path = path
        self.body = body

class DevServerHandler(BaseHTTPRequestHandler):
    """
    Adapts standard HTTP requests to the Vercel 'def handler(request)' signature.
    """
    
    def do_ALL(self, method):
        # 1. Read Request Body
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length) if content_length > 0 else b""
        
        # 2. Create Mock Request Object
        # Vercel's request object usually exposes .body as bytes or parsed JSON
        # For this simulator, we pass raw bytes as .body to be safe
        mock_req = MockRequest(method, self.path, body)

        # 3. Route to proper module
        response = None
        
        try:
            if self.path.startswith('/api/campaigns'):
                response = campaigns.handler(mock_req)
            elif self.path.startswith('/api/targets'):
                response = targets.handler(mock_req)
            elif self.path.startswith('/api/templates'):
                response = templates.handler(mock_req)
            elif self.path.startswith('/api/health'):
                response = health.handler(mock_req)
            else:
                response = {
                    "statusCode": 404,
                    "headers": {"Content-Type": "application/json"},
                    "body": json.dumps({"error": "Not Found"})
                }
        except Exception as e:
            print(f"Server Error: {e}")
            response = {
                "statusCode": 500,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"error": str(e)})
            }

        # 4. Write Response
        self.send_response(response.get("statusCode", 200))
        
        headers = response.get("headers", {})
        for k, v in headers.items():
            self.send_header(k, v)
            
        self.end_headers()
        
        resp_body = response.get("body", "")
        if isinstance(resp_body, str):
            self.wfile.write(resp_body.encode('utf-8'))
        else:
            self.wfile.write(resp_body)

    def do_GET(self): self.do_ALL('GET')
    def do_POST(self): self.do_ALL('POST')
    def do_DELETE(self): self.do_ALL('DELETE')
    def do_PUT(self): self.do_ALL('PUT')
    def do_OPTIONS(self): self.do_ALL('OPTIONS')

if __name__ == '__main__':
    print(f"Starting Local Dev Server on http://localhost:{PORT}")
    print("API Endpoints available at /api/...")
    print("Run 'npm run dev' in the 'frontend' folder to start the UI.")
    server = HTTPServer(('0.0.0.0', PORT), DevServerHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    server.server_close()
    print("Server stopped.")
