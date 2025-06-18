import os
import requests
import json
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

# Gemini API key from environment variable
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY') or 'AIzaSyDHfreU9kJ-wDGzgwdd92tWGw002__wfaQ'

# Website information
website_info = """
Website: https://ait.iak.ngo/
About: AIT is an NGO focused on education, health, and community development in underprivileged areas.
Mission: To empower communities through sustainable projects.
Services: Education programs, health camps, skill development workshops.
Contact: info@ait.iak.ngo
"""

app = Flask(__name__)

def get_gemini_response(user_input):
    """Generate a response using the Gemini API based on website info."""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    
    prompt = f"""
    You are an AI agent for the website https://ait.iak.ngo/. 
    Here is the website information:
    {website_info}
    
    Answer the user's question based on this information in a clear and concise way. If you don't know something, say so politely.
    User's question: {user_input}
    """

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        result = response.json()
        answer = result["candidates"][0]["content"]["parts"][0]["text"]
        return answer
    except Exception as e:
        return f"Sorry, I encountered an error: {str(e)}. Please try again later."

@app.route("/whatsapp", methods=['POST'])
def whatsapp_reply():
    """Respond to incoming WhatsApp messages using Twilio."""
    incoming_msg = request.values.get('Body', '').strip()
    
    # Generate response using Gemini API
    response_text = get_gemini_response(incoming_msg)
    
    # Create Twilio MessagingResponse
    resp = MessagingResponse()
    resp.message(response_text)
    
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)