from http.server import BaseHTTPRequestHandler
from api.store import data_store
from api.utils import check_options, parse_body, send_json, send_error

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        check_options(self)

    def do_GET(self):
        # GET /api/campaigns
        # GET /api/campaigns/<id>/stats
        try:
            path_parts = self.path.split('/')
            # Expected: ['', 'api', 'campaigns', ...] 
            
            if len(path_parts) <= 3 or (len(path_parts) == 4 and path_parts[-1] == ''):
                # Request to /api/campaigns or /api/campaigns/
                campaigns = data_store.get_all_campaigns()
                send_json(self, 200, campaigns)
                return

            if len(path_parts) >= 5 and path_parts[4] == 'stats':
                # Request to /api/campaigns/<id>/stats
                try:
                    campaign_id = int(path_parts[3])
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
        # POST /api/campaigns/ -> Create
        # POST /api/campaigns/<id>/launch -> Launch
        # POST /api/campaigns/<result_id>/track/open -> Track Open
        # POST /api/campaigns/<result_id>/track/click -> Track Click
        
        try:
            path_parts = self.path.split('/')
            data = parse_body(self)

            # Check for Tracking first (as it might look deep)
            if 'track' in path_parts:
                try:
                    # layout: ['', 'api', 'campaigns', '<result_id>', 'track', 'open']
                    track_idx = path_parts.index('track')
                    action = path_parts[track_idx + 1] # open or click
                    result_id = int(path_parts[track_idx - 1])
                    
                    if action in ['open', 'click']:
                        success = data_store.track_action(result_id, action)
                        if success:
                            send_json(self, 200, {'message': f'Tracked {action}'})
                        else:
                            send_error(self, 404, "Result ID not found")
                        return
                except (ValueError, IndexError):
                    pass # Fall through
            
            # Check for Launch
            if len(path_parts) >= 5 and path_parts[4] == 'launch':
                try:
                    campaign_id = int(path_parts[3])
                    target_ids = data.get('target_ids')
                    count = data_store.launch_campaign(campaign_id, target_ids)
                    send_json(self, 200, {'message': f'Campaign launched. Sent to {count} targets.'})
                except ValueError as e:
                    send_error(self, 400, str(e))
                return

            # Check for Create
            # Basically /api/campaigns or /api/campaigns/
            if len(path_parts) <= 3 or (len(path_parts) == 4 and path_parts[-1] == ''):
                name = data.get('name')
                template_id = data.get('template_id')
                if not name or not template_id:
                    send_error(self, 400, "Name and Template ID required")
                    return
                
                campaign = data_store.create_campaign(name, template_id)
                send_json(self, 201, {'message': 'Campaign created', 'id': campaign['id']})
                return

            send_error(self, 404, "Endpoint not found")

        except Exception as e:
            send_error(self, 500, str(e))

    def do_DELETE(self):
        # DELETE /api/campaigns/<id>
        try:
            path_parts = self.path.split('/')
            if len(path_parts) >= 4:
                try:
                    campaign_id = int(path_parts[3])
                    data_store.delete_campaign(campaign_id)
                    send_json(self, 200, {'message': 'Campaign deleted'})
                except ValueError:
                     send_error(self, 400, "Invalid ID")
                return
            
            send_error(self, 404, "Endpoint not found")

        except Exception as e:
            send_error(self, 500, str(e))
