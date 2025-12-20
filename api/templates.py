from http.server import BaseHTTPRequestHandler
from api.store import data_store
from api.utils import check_options, parse_body, parse_path, send_json, send_error
from api.gemini import gemini_service

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        check_options(self)

    def do_GET(self):
        # GET /api/templates
        try:
            path_parts = parse_path(self.path)
            
            if len(path_parts) == 2 and path_parts[1] == 'templates':
                templates = data_store.get_all_templates()
                send_json(self, 200, templates)
            else:
                send_error(self, 404, "Endpoint not found")
                
        except Exception as e:
            send_error(self, 500, str(e))

    def do_POST(self):
        # Routes:
        # /api/templates/generate -> AI
        # /api/templates/analyze  -> AI
        # /api/templates          -> Save
        
        try:
            path_parts = parse_path(self.path)
            data = parse_body(self)

            # Generate: /api/templates/generate
            if len(path_parts) == 3 and path_parts[2] == 'generate':
                template_type = data.get('type')
                sender_name = data.get('sender_name')
                context = data.get('context', '')
                
                if not template_type:
                    send_error(self, 400, "Template type is required")
                    return

                result = gemini_service.generate_template(template_type, sender_name, context)
                if result:
                    send_json(self, 200, result)
                else:
                    send_error(self, 500, "Failed to generate template")
                return

            # Analyze: /api/templates/analyze
            if len(path_parts) == 3 and path_parts[2] == 'analyze':
                subject = data.get('subject')
                body = data.get('body')
                
                if not subject or not body:
                    send_error(self, 400, "Subject and Body required")
                    return
                    
                analysis = gemini_service.analyze_template(subject, body)
                send_json(self, 200, {'analysis': analysis})
                return

            # Save: /api/templates
            if len(path_parts) == 2 and path_parts[1] == 'templates':
                new_template = data_store.add_template(data)
                send_json(self, 201, {'message': 'Template saved', 'id': new_template['id']})
                return

            send_error(self, 404, "Endpoint not found")

        except Exception as e:
            send_error(self, 500, str(e))
