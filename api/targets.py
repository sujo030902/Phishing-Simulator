from api.store import data_store
from api.utils import parse_path, parse_body, send_json, send_error, handle_options

def handler(request):
    if request.method == 'OPTIONS':
        return handle_options()

    path_parts = parse_path(request.path)
    # ['api', 'targets', ...]

    if request.method == 'GET':
        if len(path_parts) <= 3:
            targets = data_store.get_all_targets()
            return send_json(200, targets)
        return send_error(404, "Endpoint not found")

    if request.method == 'POST':
        # POST /api/targets
        if len(path_parts) == 3 or (len(path_parts) == 4 and path_parts[3] == ''):
            data = parse_body(request)
            email = data.get('email')
            
            if not email:
                return send_error(400, "Email is required")
                
            try:
                target = data_store.add_target(data)
                return send_json(201, {'message': 'Target added', 'id': target['id']})
            except ValueError as e:
                return send_error(400, str(e)) # e.g. Email exists
                
        return send_error(404, "Endpoint not found")

    if request.method == 'DELETE':
        # DELETE /api/targets/<id>
        if len(path_parts) == 4 and path_parts[3]:
            try:
                target_id = int(path_parts[3])
                data_store.delete_target(target_id)
                return send_json(200, {'message': 'Target deleted'})
            except ValueError:
                return send_error(400, "Invalid ID")

        return send_error(404, "Endpoint not found")

    return send_error(405, "Method Not Allowed")
