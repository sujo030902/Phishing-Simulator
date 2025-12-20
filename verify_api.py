import sys
import os
import json
from http.server import BaseHTTPRequestHandler
from io import BytesIO

# Ensure root is in path
sys.path.append(os.getcwd())

# Import handlers
try:
    from api.campaigns import handler as campaigns_handler
    from api.targets import handler as targets_handler
    from api.templates import handler as templates_handler
except ImportError as e:
    print(f"Import Error: {e}")
    sys.exit(1)

class MockHandler(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        # We don't call super().__init__ because it tries to do socket stuff
        self.request = request
        self.client_address = client_address
        self.server = server
        self.headers = request.headers # Mock headers
        self.path = request.path
        self.command = request.command
        
        self.rfile = request.rfile
        self.wfile = request.wfile
        
        try:
            self.handle()
        finally:
            self.finish()
            
    def setup(self):
        pass
        
    def finish(self):
        pass

def run_test(name, handler_class, method, path, body=None):
    print(f"--- Testing {name} {method} {path} ---")
    mock_req = MockRequest(method, path, body)
    
    try:
        # Instantiate handler directly
        h = MockHandler(mock_req, ('0.0.0.0', 8888), None)
        # We need to monkeypath the class to use our MockHandler logic?
        # No, the api/*.py classes inherit BaseHTTPRequestHandler.
        # We need to mixin or just instantiate the api class but force it to behave like our mock?
        # Actually, simpler: The api handler IS a class.
        # We can instantiate it, but we need to intercept setup().
        
        # New strategy:
        # Create an instance of the api handler, but override setup/finish on the INSTANCE or Class
        handler_instance = handler_class(mock_req, ('0.0.0.0', 8888), None)
        # Wait, calling init calls setup() which calls makefile().
        # So we must ensure mock_req (which is passed as 'request') has makefile().
        
    except Exception as e:
        # Retry with a better mock structure
        print(f"FAILED with standard init: {e}")
        return None
        
# Re-define MockRequest to be more socket-like
class MockSocket:
    def __init__(self, rfile, wfile):
        self._rfile = rfile
        self._wfile = wfile
        
    def makefile(self, mode, *args, **kwargs):
        if 'r' in mode:
            return self._rfile
        return self._wfile

def run_test_v2(name, handler_class, method, path, body=None):
    print(f"--- Testing {name} {method} {path} ---")
    
    # Body
    if body:
        body_bytes = json.dumps(body).encode('utf-8')
        clen = str(len(body_bytes))
    else:
        body_bytes = b''
        clen = '0'
        
    rfile = BytesIO(body_bytes)
    wfile = BytesIO()
    
    sock = MockSocket(rfile, wfile)
    
    # We need to mock headers on the handler instance, but BaseHTTPRequestHandler parses them from rfile.
    # This is too complex to mock perfectly without writing HTTP bytes.
    # ALTERNATIVE: Javascript-style logic injecting.
    
    # Let's write raw HTTP to rfile so BaseHTTPRequestHandler parses it?
    # No, that's overkill.
    
    # Let's subclass the handler_class dynamically to override setup.
    class TestableHandler(handler_class):
        def __init__(self, *args, **kwargs):
            pass
            
    h = TestableHandler('mock_request', 'mock_addr', 'mock_server')
    h.rfile = rfile
    h.wfile = wfile
    h.command = method
    h.path = path
    h.headers = {'Content-Length': clen}
    h.requestline = f"{method} {path} HTTP/1.1"
    h.protocol_version = "HTTP/1.1"
    h.client_address = ('127.0.0.1', 8888)
    
    # Manually trigger the method
    try:
        if method == 'GET':
            h.do_GET()
        elif method == 'POST':
            h.do_POST()
        elif method == 'DELETE':
            h.do_DELETE()
            
        output = wfile.getvalue().decode('utf-8')
        # Parse output
        if '\r\n\r\n' in output:
            head, res_body = output.split('\r\n\r\n', 1)
        else:
            head, res_body = output, ""
            
        print(f"Status: {head.splitlines()[0]}")
        print(f"Body: {res_body}")
        
    except Exception as e:
        print(f"FAILED: {e}")


if __name__ == "__main__":
    print("Verifying API Handlers...")
    
    # Test Targets
    run_test_v2("Targets List", targets_handler, "GET", "/api/targets")
    run_test_v2("Create Target", targets_handler, "POST", "/api/targets", {
        "email": "test@example.com", "first_name": "Test", "last_name": "User"
    })
    
    # Test Campaigns
    run_test_v2("Campaigns List", campaigns_handler, "GET", "/api/campaigns")
    
    # Test Health
    # Need to import health handler
    from api.health import handler as health_handler
    run_test_v2("Health Check", health_handler, "GET", "/api/health")

    print("\nDone.")
