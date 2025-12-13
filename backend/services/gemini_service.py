import os
import google.generativeai as genai
import json

class GeminiService:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash')

        # Configure safety settings to allow simulation content
        self.safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_NONE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_NONE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_NONE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_NONE"
            },
        ]

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
        - body: Email body (HTML allowed)
        """
        
        try:
            # Simplified call without explicit safety settings first to test basic connectivity
            response = self.model.generate_content(prompt)
            
            # Accessing text can raise ValueError if blocked
            try:
                text = response.text.strip()
            except ValueError:
                print(f"Gemini blocked the response. Feedback: {response.prompt_feedback}")
                return None
                
            print(f"Gemini Raw Response: {text}") # Debug log
            print(f"Gemini Raw Response: {text}") # Debug log

            # Clean up markdown
            if text.startswith("```"):
                text = text.split("\n", 1)[1]
            if text.endswith("```"):
                text = text.rsplit("\n", 1)[0]
            
            text = text.replace("```json", "").replace("```", "").strip()
            
            return json.loads(text)
        except Exception as e:
            print(f"Error generating template from Gemini: {e}")
            return None

gemini_service = GeminiService()
