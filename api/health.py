from api.utils import send_json, handle_options, parse_path
import os
from dotenv import load_dotenv

# Ensure env vars are loaded
load_dotenv()

def handler(request):
    if request.method == 'OPTIONS':
        return handle_options()

    path_parts = parse_path(request.path)
    
    if request.method == 'GET':
        health_data = {
            'status': 'healthy', 
            'service': 'phishing-simulator-serverless'
        }
        
        # Check Gemini API key status
        gemini_key = os.getenv("GEMINI_API_KEY")
        if gemini_key:
            health_data['gemini_api_key'] = 'configured'
            # Check if we can import and initialize Gemini
            try:
                from api.gemini import gemini_service
                if gemini_service.model:
                    health_data['gemini_model'] = 'ready'
                else:
                    health_data['gemini_model'] = 'not_initialized'
            except Exception as e:
                health_data['gemini_model'] = f'error: {str(e)}'
        else:
            health_data['gemini_api_key'] = 'not_configured'
            health_data['gemini_model'] = 'not_available'
        
        return send_json(200, health_data)
        
    return send_json(405, {"error": "Method Not Allowed"})
