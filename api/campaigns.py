from api.store import data_store
from api.utils import parse_path, parse_body, send_json, send_error, handle_options

def handler(request):
    if request.method == 'OPTIONS':
        return handle_options()

    path_parts = parse_path(request.path)
    # Expected: ['', 'api', 'campaigns', ...]

    if request.method == 'GET':
        # GET /api/campaigns
        if len(path_parts) <= 3:
             campaigns = data_store.get_all_campaigns()
             return send_json(200, campaigns)
             
        # GET /api/campaigns/<id>/stats
        if len(path_parts) == 5 and path_parts[4] == 'stats':
            try:
                campaign_id = int(path_parts[3])
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
        if len(path_parts) == 3 or (len(path_parts) == 4 and path_parts[3] == ''):
            data = parse_body(request)
            name = data.get('name')
            template_id = data.get('template_id')
            
            if not name or not template_id:
                return send_error(400, "Name and Template ID required")
            
            # Simple validation for template_id type
            try:
                template_id = int(template_id)
            except ValueError:
                return send_error(400, "Invalid Template ID")

            campaign = data_store.create_campaign(name, template_id)
            return send_json(201, {'message': 'Campaign created', 'id': campaign['id']})

        # POST /api/campaigns/<id>/launch
        if len(path_parts) == 5 and path_parts[4] == 'launch':
            try:
                campaign_id = int(path_parts[3])
                count = data_store.launch_campaign(campaign_id)
                return send_json(200, {'message': f'Campaign launched to {count} targets'})
            except ValueError as e:
                # ValueError from int conversion or launch_campaign validation
                return send_error(400, str(e))

        # POST /api/campaigns/track/<result_id>/<action>
        # e.g. /api/campaigns/track/123/open
        if len(path_parts) >= 6 and path_parts[3] == 'track':
            try:
                result_id = int(path_parts[4])
                action = path_parts[5]
                success = data_store.track_action(result_id, action)
                if success:
                     # Tracking pixel usually returns minimal content or explicit OK
                     return send_json(200, {'success': True})
                else:
                     return send_error(404, "Result ID not found")
            except ValueError:
                 return send_error(400, "Invalid Result ID")
                 
        return send_error(404, "Endpoint not found")

    if request.method == 'DELETE':
        # DELETE /api/campaigns/<id>
        if len(path_parts) == 4 and path_parts[3]:
            try:
                campaign_id = int(path_parts[3])
                data_store.delete_campaign(campaign_id)
                return send_json(200, {'message': 'Campaign deleted'})
            except ValueError:
                return send_error(400, "Invalid Campaign ID")
        
        return send_error(404, "Endpoint not found")

    return send_error(405, "Method Not Allowed")
