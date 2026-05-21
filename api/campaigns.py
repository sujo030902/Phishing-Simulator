from api.store import data_store
from api.utils import parse_path, parse_body, send_json, send_error, handle_options

def handler(request):
    if request.method == 'OPTIONS':
        return handle_options()

    path_parts = parse_path(request.path)

    if request.method == 'GET':
        # GET /api/campaigns
        if len(path_parts) == 2 and path_parts[0] == 'api' and path_parts[1] == 'campaigns':
            campaigns = data_store.get_all_campaigns()
            return send_json(200, campaigns)

        # GET /api/campaigns/<id>/stats
        if len(path_parts) == 4 and path_parts[0] == 'api' and path_parts[1] == 'campaigns' and path_parts[3] == 'stats':
            try:
                campaign_id = int(path_parts[2])
                stats = data_store.get_campaign_stats(campaign_id)
                if stats:
                    return send_json(200, stats)
                else:
                    return send_error(404, "Campaign not found")
            except ValueError:
                return send_error(400, "Invalid Campaign ID")

        return send_error(404, "Endpoint not found")

    if request.method == 'POST':
        # POST /api/campaigns
        if len(path_parts) == 2 and path_parts[0] == 'api' and path_parts[1] == 'campaigns':
            data = parse_body(request)
            if data is None:
                return send_error(400, "Invalid JSON body")

            name = data.get('name')
            template_id = data.get('template_id')

            if not name or template_id is None or template_id == '':
                return send_error(400, "Name and Template ID required")

            try:
                template_id = int(template_id)
            except ValueError:
                return send_error(400, "Invalid Template ID")

            campaign = data_store.create_campaign(name, template_id)
            return send_json(201, {'message': 'Campaign created', 'id': campaign['id']})

        # POST /api/campaigns/<id>/launch
        if len(path_parts) == 4 and path_parts[0] == 'api' and path_parts[1] == 'campaigns' and path_parts[3] == 'launch':
            try:
                campaign_id = int(path_parts[2])
                data = parse_body(request)
                if data is None:
                    return send_error(400, "Invalid JSON body")

                target_ids = data.get('target_ids')
                count = data_store.launch_campaign(campaign_id, target_ids)
                return send_json(200, {'message': f'Campaign launched to {count} targets'})
            except ValueError as e:
                return send_error(400, str(e))

        # POST /api/campaigns/<id>/track/<action>
        # e.g. /api/campaigns/123/open
        if len(path_parts) == 5 and path_parts[0] == 'api' and path_parts[1] == 'campaigns':
            try:
                if path_parts[3] == 'track':
                    result_id = int(path_parts[2])
                    action = path_parts[4]
                elif path_parts[2] == 'track':
                    result_id = int(path_parts[3])
                    action = path_parts[4]
                else:
                    return send_error(404, "Endpoint not found")

                success = data_store.track_action(result_id, action)
                if success:
                    return send_json(200, {'success': True})
                else:
                    return send_error(404, "Result ID not found")
            except ValueError:
                return send_error(400, "Invalid Result ID")

        return send_error(404, "Endpoint not found")

    if request.method == 'DELETE':
        # DELETE /api/campaigns/<id>
        if len(path_parts) == 3 and path_parts[0] == 'api' and path_parts[1] == 'campaigns':
            try:
                campaign_id = int(path_parts[2])
                data_store.delete_campaign(campaign_id)
                return send_json(200, {'message': 'Campaign deleted'})
            except ValueError:
                return send_error(400, "Invalid Campaign ID")

        return send_error(404, "Endpoint not found")

    return send_error(405, "Method Not Allowed")
