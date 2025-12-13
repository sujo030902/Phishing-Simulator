
import os
import logging
import traceback
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
load_dotenv()

try:
    from services.gemini_service import gemini_service
    
    print("Attempting to generate template...")
    result = gemini_service.generate_template(
        template_type="IT Support",
        sender_name="Help Desk",
        context="Password expiry warning"
    )
    
    if result:
        print("SUCCESS! Result:")
        print(result)
    else:
        print("FAILURE: returned None")

except Exception as e:
    print("CRASHED!")
    print(f"Error Type: {type(e).__name__}")
    print(f"Error Message: {e}")
    traceback.print_exc()
