from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse
from api.store import data_store
from api.utils import check_options, parse_body, send_json, send_error

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        check_options(self)

    def do_GET(self):
        # GET /api/targets
        try:
            targets = data_store.get_all_targets()
            send_json(self, 200, targets)
        except Exception as e:
            send_error(self, 500, str(e))

    def do_POST(self):
        # POST /api/targets
        try:
            data = parse_body(self)
            if not data.get('email'):
                send_error(self, 400, "Email is required")
                return

            try:
                new_target = data_store.add_target(data)
                send_json(self, 201, {'message': 'Target created', 'id': new_target['id']})
            except ValueError as e:
                send_error(self, 400, str(e))
                
        except Exception as e:
            send_error(self, 500, str(e))

    def do_DELETE(self):
        # DELETE /api/targets/<id>
        try:
            path_parts = self.path.split('/')
            # Expected path: /api/targets/<id>
            # So parts should be ['', 'api', 'targets', 'id']
            # or just targets/<id> if rewritten differently, but typically full path
            
            target_id = None
            if len(path_parts) > 3:
                try:
                    target_id = int(path_parts[-1])
                except ValueError:
                    pass
            
            if target_id is None:
                 # Check query params if path parsing fails or strictly follow path
                 # For now, assume path param
                 send_error(self, 400, "Invalid target ID")
                 return

            data_store.delete_target(target_id)
            send_json(self, 200, {'message': 'Target deleted'})

        except Exception as e:
            send_error(self, 500, str(e))
