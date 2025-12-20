from http.server import HTTPServer, BaseHTTPRequestHandler
import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Ensure we can import from api/
sys.path.append(os.getcwd())

from api import campaigns, targets, templates, health

PORT = 3000

class DevServerHandler(BaseHTTPRequestHandler):
    """
    A simple router that mimics Vercel's routing by delegating 
    to the specific handler classes defined in api/*.py.
    """
    
    def _dispatch(self, method):
        # CORS Pre-flight for local dev
        if method == 'OPTIONS':
            self.send_response(204)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
            self.end_headers()
            return

        # Simple Routing Logic mimicking vercel.json rewrites
        if self.path.startswith('/api/campaigns'):
            # Call the 'do_METHOD' on the handler CLASS, passing 'self' as the instance
            # This works because 'self' is a BaseHTTPRequestHandler instance, 
            # and the handler methods expect exactly that.
            if hasattr(campaigns.handler, f'do_{method}'):
                getattr(campaigns.handler, f'do_{method}')(self)
            else:
                self.send_error(405, "Method Not Allowed")
                
        elif self.path.startswith('/api/targets'):
            if hasattr(targets.handler, f'do_{method}'):
                getattr(targets.handler, f'do_{method}')(self)
            else:
                self.send_error(405, "Method Not Allowed")
                
        elif self.path.startswith('/api/templates'):
            if hasattr(templates.handler, f'do_{method}'):
                getattr(templates.handler, f'do_{method}')(self)
            else:
                self.send_error(405, "Method Not Allowed")
                
        elif self.path.startswith('/api/health'):
            if hasattr(health.handler, f'do_{method}'):
                getattr(health.handler, f'do_{method}')(self)
            else:
                self.send_error(405, "Method Not Allowed")
                
        else:
            self.send_error(404, "Not Found")

    def do_GET(self):
        self._dispatch('GET')

    def do_POST(self):
        self._dispatch('POST')

    def do_DELETE(self):
        self._dispatch('DELETE')

    def do_PUT(self):
        self._dispatch('PUT')

    def do_OPTIONS(self):
        self._dispatch('OPTIONS')

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
