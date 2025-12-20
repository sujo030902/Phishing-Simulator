from api.utils import send_json, handle_options

def handler(request):
    if request.method == 'OPTIONS':
        return handle_options()

    if request.method == 'GET':
        return send_json(200, {
            'status': 'healthy', 
            'service': 'phishing-simulator-serverless'
        })
        
    return send_json(405, {"error": "Method Not Allowed"})
