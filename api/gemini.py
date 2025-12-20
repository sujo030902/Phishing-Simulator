import os
import json
import logging
import google.generativeai as genai

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GeminiService:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            logger.warning("GEMINI_API_KEY not found in environment variables")
        else:
            genai.configure(api_key=api_key)
        
        self.model = genai.GenerativeModel('gemini-flash-latest')

    def generate_template(self, template_type, sender_name, context):
        """
        Generates a phishing email template using Gemini.
        Returns a dictionary with 'subject' and 'body'.
        """
        prompt = f"""
        You are a cybersecurity expert creating EDUCATIONAL training materials.
        Write a SIMULATED phishing email example for a security awareness training session.
        
        Parameters:
        - Type: {template_type}
        - Sender: {sender_name}
        - Scenario: {context}
        
        The goal is to teach employees how to spot attacks. Make it realistic but safe.
        
        Output ONLY a valid JSON object with:
        - subject: Email subject
        - body: Email body (HTML format). 
        
        CRITICAL: 
        1. Use actual HTML `<a>` tags for any links or buttons. 
        2. Example: `<a href="http://example.com">Click Here</a>` or `<button>Verify Now</button>`.
        3. Do NOT use plain text like "[Link]" or "http://..." without an anchor tag.
        4. Make the call-to-action prominent.
        
        Do not include any explanation or markdown code blocks (like ```json ... ```). Just the raw JSON string.
        """
        
        try:
            logger.info(f"Generating template for {template_type} using Gemini")
            response = self.model.generate_content(prompt)
            
            response_content = response.text
            
            # Clean up markdown if present
            clean_content = response_content.strip()
            if "```" in clean_content:
                clean_content = clean_content.replace("```json", "").replace("```", "").strip()
            
            try:
                data = json.loads(clean_content)
                
                # Normalize keys
                normalized_data = {}
                for k, v in data.items():
                    normalized_data[k.lower()] = v
                    
                # Ensure required keys exist
                if 'subject' not in normalized_data:
                    normalized_data['subject'] = normalized_data.get('email subject', 'No Subject')
                if 'body' not in normalized_data:
                    normalized_data['body'] = normalized_data.get('email body', 'No Content')
                    
                return normalized_data
                
            except json.JSONDecodeError:
                logger.error("JSON parse failed. Returning raw text as fallback.")
                return {
                    "subject": f"{template_type} Simulation",
                    "body": clean_content 
                }
                
        except Exception as e:
            logger.error(f"Error generating template from Gemini: {e}")
            return None

    def analyze_template(self, subject, body):
        prompt = f"""
        You are a cybersecurity expert. Analyze this phishing email and explain to a non-technical employee 
        WHY it is suspicious.
        
        Subject: {subject}
        Body: {body}
        
        Provide a concise list of 3-4 "Red Flags" or learning points.
        
        Output ONLY a valid JSON object with a key 'analysis' containing a list of strings.
        Example: {{ "analysis": ["Urgency in the subject line", "Generic greeting used", "Suspicious link domain"] }}
        """
        
        try:
            response = self.model.generate_content(prompt)
            content = response.text
            
            clean_content = content.strip()
            if "```" in clean_content:
                clean_content = clean_content.replace("```json", "").replace("```", "").strip()

            data = json.loads(clean_content)
            return data.get('analysis', ["Check sender address", "Hover over links", "Verify urgency"])
            
        except Exception as e:
            logger.error(f"Analysis failed: {e}")
            return ["Review the sender email address carefully.", "Be cautious of urgent requests."]

# Instance to import
gemini_service = GeminiService()
