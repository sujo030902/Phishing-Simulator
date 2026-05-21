from http.server import HTTPServer, BaseHTTPRequestHandler
import sys
import os
import json
import traceback
from dotenv import load_dotenv

# Get the directory where this script is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load environment variables from the correct path
dotenv_path = os.path.join(BASE_DIR, '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
else:
    print(f"Warning: .env file not found at {dotenv_path}")

# Ensure we can import from the project root
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

try:
    from api import campaigns, targets, templates, health
except ImportError as e:
    print(f"Error importing API modules: {e}")
    print(f"Current sys.path: {sys.path}")
    print(f"Are you running this from the correct environment?")
    sys.exit(1)

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
        response = None
        try:
            # 1. Read Request Body
            try:
                content_length = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(content_length) if content_length > 0 else b""
            except (ValueError, TypeError):
                body = b""
            
            # 2. Create Mock Request Object
            mock_req = MockRequest(method, self.path, body)

            # 3. Route to proper module
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
            traceback.print_exc()
            response = {
                "statusCode": 500,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"error": str(e)})
            }

        # Ensure response is a dictionary
        if not isinstance(response, dict):
             response = {
                "statusCode": 500,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"error": "Handler returned invalid response type"})
            }

        # 4. Write Response
        status_code = response.get("statusCode", 200)
        self.send_response(status_code)
        
        headers = response.get("headers", {})
        resp_body = response.get("body", "")
        
        # Ensure body is bytes for writing
        if isinstance(resp_body, str):
            resp_body = resp_body.encode('utf-8')
        
        # Add Content-Length if not present and body exists
        if 'Content-Length' not in headers and resp_body:
            self.send_header('Content-Length', str(len(resp_body)))
            
        for k, v in headers.items():
            self.send_header(k, v)
            
        self.end_headers()
        
        # Do not write body for HEAD requests or if body is empty
        if method != 'HEAD' and resp_body:
            try:
                self.wfile.write(resp_body)
            except BrokenPipeError:
                pass

    def do_GET(self): self.do_ALL('GET')
    def do_POST(self): self.do_ALL('POST')
    def do_DELETE(self): self.do_ALL('DELETE')
    def do_PUT(self): self.do_ALL('PUT')
    def do_PATCH(self): self.do_ALL('PATCH')
    def do_OPTIONS(self): self.do_ALL('OPTIONS')

class ReusableHTTPServer(HTTPServer):
    allow_reuse_address = True

if __name__ == '__main__':
    print(f"Starting Local Dev Server on http://localhost:{PORT}")
    print("API Endpoints available at /api/...")
    print("Run 'npm run dev' in the 'frontend' folder to start the UI.")
    
    server = ReusableHTTPServer(('0.0.0.0', PORT), DevServerHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    server.server_close()
    print("Server stopped.")

