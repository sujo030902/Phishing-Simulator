from http.server import BaseHTTPRequestHandler
from api.store import data_store
from api.utils import check_options, parse_body, parse_path, send_json, send_error

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        check_options(self)

    def do_GET(self):
        # GET /api/targets
        try:
            path_parts = parse_path(self.path)
            # ['api', 'targets']
            
            if len(path_parts) == 2 and path_parts[1] == 'targets':
                targets = data_store.get_all_targets()
                send_json(self, 200, targets)
                return
            
            send_error(self, 404, "Endpoint not found")
        except Exception as e:
            send_error(self, 500, str(e))

    def do_POST(self):
        # POST /api/targets
        try:
            path_parts = parse_path(self.path)
            
            if len(path_parts) == 2 and path_parts[1] == 'targets':
                data = parse_body(self)
                if not data.get('email'):
                    send_error(self, 400, "Email is required")
                    return

                try:
                    new_target = data_store.add_target(data)
                    send_json(self, 201, {'message': 'Target created', 'id': new_target['id']})
                except ValueError as e:
                    send_error(self, 400, str(e))
                return
            
            send_error(self, 404, "Endpoint not found")
                
        except Exception as e:
            send_error(self, 500, str(e))

    def do_DELETE(self):
        # DELETE /api/targets/<id>
        try:
            path_parts = parse_path(self.path)
            # Expected path: /api/targets/<id> -> ['api', 'targets', '123']
            
            if len(path_parts) == 3 and path_parts[1] == 'targets':
                try:
                    target_id = int(path_parts[2])
                    data_store.delete_target(target_id)
                    send_json(self, 200, {'message': 'Target deleted'})
                except ValueError:
                    send_error(self, 400, "Invalid target ID")
                return

            send_error(self, 404, "Endpoint not found")

        except Exception as e:
            send_error(self, 500, str(e))
