from http.server import BaseHTTPRequestHandler
from api.store import data_store
from api.utils import check_options, parse_body, parse_path, send_json, send_error

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        check_options(self)

    def do_GET(self):
        # GET /api/campaigns
        # GET /api/campaigns/<id>/stats
        try:
            path_parts = parse_path(self.path)
            # Expected: ['api', 'campaigns'] or ['api', 'campaigns', '123', 'stats']
            
            # Base endpoint: /api/campaigns
            if len(path_parts) == 2 and path_parts[1] == 'campaigns':
                campaigns = data_store.get_all_campaigns()
                send_json(self, 200, campaigns)
                return

            # Stats endpoint: /api/campaigns/<id>/stats
            if len(path_parts) == 4 and path_parts[1] == 'campaigns' and path_parts[3] == 'stats':
                try:
                    campaign_id = int(path_parts[2])
                    stats = data_store.get_campaign_stats(campaign_id)
                    if stats:
                        send_json(self, 200, stats)
                    else:
                        send_error(self, 404, "Campaign not found")
                except ValueError:
                    send_error(self, 400, "Invalid Campaign ID")
                return
            
            send_error(self, 404, "Endpoint not found")

        except Exception as e:
            send_error(self, 500, str(e))

    def do_POST(self):
        # POST /api/campaigns -> Create
        # POST /api/campaigns/<id>/launch -> Launch
        # POST /api/campaigns/<result_id>/track/open -> Track Open
        # POST /api/campaigns/<result_id>/track/click -> Track Click
        
        try:
            path_parts = parse_path(self.path)
            data = parse_body(self)

            # Check for Tracking: /api/campaigns/<result_id>/track/<action>
            # parts: ['api', 'campaigns', '101', 'track', 'open']
            if len(path_parts) == 5 and path_parts[3] == 'track':
                try:
                    result_id = int(path_parts[2])
                    action = path_parts[4]
                    
                    if action in ['open', 'click']:
                        success = data_store.track_action(result_id, action)
                        if success:
                            send_json(self, 200, {'message': f'Tracked {action}'})
                        else:
                            send_error(self, 404, "Result ID not found")
                        return
                except ValueError:
                    pass # Fall through to other routes if parsing fails
            
            # Check for Launch: /api/campaigns/<id>/launch
            if len(path_parts) == 4 and path_parts[3] == 'launch':
                try:
                    campaign_id = int(path_parts[2])
                    target_ids = data.get('target_ids')
                    count = data_store.launch_campaign(campaign_id, target_ids)
                    send_json(self, 200, {'message': f'Campaign launched. Sent to {count} targets.'})
                except ValueError as e:
                    send_error(self, 400, str(e))
                return

            # Check for Create: /api/campaigns
            if len(path_parts) == 2 and path_parts[1] == 'campaigns':
                name = data.get('name')
                template_id = data.get('template_id')
                if not name or not template_id:
                    send_error(self, 400, "Name and Template ID required")
                    return
                
                # Validate template_id
                try:
                    tmp_id_int = int(template_id)
                except:
                    send_error(self, 400, "Template ID must be a number")
                    return

                campaign = data_store.create_campaign(name, tmp_id_int)
                send_json(self, 201, {'message': 'Campaign created', 'id': campaign['id']})
                return

            send_error(self, 404, "Endpoint not found")

        except Exception as e:
            send_error(self, 500, str(e))

    def do_DELETE(self):
        # DELETE /api/campaigns/<id>
        try:
            path_parts = parse_path(self.path)
            # ['api', 'campaigns', '123']
            
            if len(path_parts) == 3 and path_parts[1] == 'campaigns':
                try:
                    campaign_id = int(path_parts[2])
                    data_store.delete_campaign(campaign_id)
                    send_json(self, 200, {'message': 'Campaign deleted'})
                except ValueError:
                     send_error(self, 400, "Invalid ID")
                return
            
            send_error(self, 404, "Endpoint not found")

        except Exception as e:
            send_error(self, 500, str(e))
