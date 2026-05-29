import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

def generate_phishing_template(theme: str):
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert red-teamer creating a realistic phishing simulation email. You MUST return ONLY a valid JSON object."
                },
                {
                    "role": "user",
                    "content": f"""
The theme is: {theme}

Design a highly realistic corporate or service HTML email template. 
Include elements like realistic spoofed sender information (e.g. From: IT Helpdesk <admin@company-portal-update.com>), corporate headers/footers, professional formatting, and strong psychological triggers (e.g., urgency, authority, panic, curiosity).
IMPORTANT: Use inline CSS for styling. The Call to Action button MUST be properly formatted HTML and centered. You must use this exact structure:
<div style="text-align: center; margin: 30px 0;">
    <a href="[LINK]" style="background-color: #007bff; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; display: inline-block; font-weight: bold;">[Your Call To Action Text]</a>
</div>
Do NOT use absolute positioning or floating for the button.

Analyze the template you just generated and provide 3-4 specific 'Red Flags' that an employee should have noticed.

Return the output STRICTLY as a JSON object with the following structure:
{{
    "subject": "The highly convincing email subject",
    "body": "The complete HTML code of the email body",
    "red_flags": [
        {{"title": "Name of Red Flag", "description": "Specific explanation of how this flag appears in your generated email."}}
    ]
}}
Do NOT wrap the output in markdown blocks like ```json. Return ONLY raw valid JSON text.
"""
                }
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.7,
            response_format={"type": "json_object"}
        )
        
        text = chat_completion.choices[0].message.content.strip()
        
        # Clean up markdown code blocks if the AI somehow included them despite instructions
        if text.startswith("```json"):
            text = text[7:]
        elif text.startswith("```html"):
            text = text[7:]
        elif text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
            
        data = json.loads(text.strip())
        return {
            "subject": data.get("subject", f"Alert: {theme}"),
            "body": data.get("body", text),
            "red_flags": data.get("red_flags", [])
        }
    except Exception as e:
        print(f"AI Generation failed: {e}")
        return {
            "subject": f"Important: {theme} Notification",
            "body": f"Hello,<br><br>This is an important notification regarding your {theme}. Please click the link below to review the details:<br><br><a href='[LINK]'>Review Details</a><br><br>Thank you,<br>Support Team",
            "red_flags": [{"title": "Generic Failure Template", "description": "The AI generation failed, falling back to a highly generic template."}]
        }
