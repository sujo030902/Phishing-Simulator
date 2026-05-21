from api.store import data_store
from api.utils import parse_path, parse_body, send_json, send_error, handle_options
from api.gemini import gemini_service

def handler(request):
    if request.method == 'OPTIONS':
        return handle_options()

    path_parts = parse_path(request.path)

    if request.method == 'GET':
        # GET /api/templates
        if len(path_parts) == 2 and path_parts[0] == 'api' and path_parts[1] == 'templates':
            templates = data_store.get_all_templates()
            return send_json(200, templates)

        return send_error(404, "Endpoint not found")

    if request.method == 'POST':
        data = parse_body(request)
        if data is None:
            return send_error(400, "Invalid JSON body")

        # Generate: /api/templates/generate
        if len(path_parts) == 3 and path_parts[0] == 'api' and path_parts[1] == 'templates' and path_parts[2] == 'generate':
            template_type = data.get('type')
            sender_name = data.get('sender_name')
            context = data.get('context', '')

            if not template_type:
                return send_error(400, "Template type is required")

            try:
                result = gemini_service.generate_template(template_type, sender_name, context)
                if result:
                    return send_json(200, result)
                else:
                    return send_error(500, "Failed to generate template - Gemini API returned no result")
            except ValueError as e:
                error_msg = str(e)
                print(f"Error in template generation: {error_msg}")
                return send_error(400, error_msg)
            except Exception as e:
                import traceback
                error_msg = str(e)
                print(f"Error in template generation: {error_msg}")
                print(traceback.format_exc())
                return send_error(500, f"Failed to generate template: {error_msg}")

        # Analyze: /api/templates/analyze
        if len(path_parts) == 3 and path_parts[0] == 'api' and path_parts[1] == 'templates' and path_parts[2] == 'analyze':
            subject = data.get('subject')
            body = data.get('body')

            print(f"DEBUG: Analyze request - subject: {subject[:50]}..., body: {body[:50]}...")

            if not subject or not body:
                return send_error(400, "Subject and Body required")

            try:
                analysis = gemini_service.analyze_template(subject, body)
                print(f"DEBUG: Analysis result: {analysis}")
                return send_json(200, {'analysis': analysis})
            except ValueError as e:
                error_msg = str(e)
                print(f"Error in template analysis: {error_msg}")
                return send_error(400, error_msg)
            except Exception as e:
                import traceback
                error_msg = str(e)
                print(f"Error in template analysis: {error_msg}")
                print(traceback.format_exc())
                return send_error(500, f"Failed to analyze template: {error_msg}")

        # Save: /api/templates
        if len(path_parts) == 2 and path_parts[0] == 'api' and path_parts[1] == 'templates':
            try:
                new_template = data_store.add_template(data)
                return send_json(201, {'message': 'Template saved', 'id': new_template['id']})
            except Exception as e:
                import traceback
                error_msg = str(e)
                print(f"Error saving template: {error_msg}")
                print(traceback.format_exc())
                return send_error(500, f"Failed to save template: {error_msg}")

        return send_error(404, "Endpoint not found")

    if request.method == 'PUT':
        # PUT /api/templates/<id>
        if len(path_parts) == 3 and path_parts[0] == 'api' and path_parts[1] == 'templates':
            try:
                template_id = int(path_parts[2])
                data = parse_body(request)
                if data is None:
                    return send_error(400, "Invalid JSON body")

                updated = data_store.update_template(template_id, data)
                if updated:
                    return send_json(200, updated)
                else:
                    return send_error(404, "Template not found")
            except ValueError:
                return send_error(400, "Invalid ID")

        return send_error(404, "Endpoint not found")

    if request.method == 'DELETE':
        # DELETE /api/templates/<id>
        if len(path_parts) == 3 and path_parts[0] == 'api' and path_parts[1] == 'templates':
            try:
                template_id = int(path_parts[2])
                data_store.delete_template(template_id)
                return send_json(200, {'message': 'Template deleted'})
            except ValueError:
                return send_error(400, "Invalid ID")

        return send_error(404, "Endpoint not found")

    return send_error(405, "Method Not Allowed")
