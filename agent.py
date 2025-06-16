import requests
import json
import os

# Gemini API key environment variable se lo
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or "YOUR_GEMINI_API_KEY"  # Apni key yahan daal agar env var nahi hai

# Website ka basic info (abhi manually add kiya, baad mein scrape karenge)
website_info = """
Website: https://ait.iak.ngo/
About: AIT is an NGO focused on education, health, and community development in underprivileged areas.
Mission: To empower communities through sustainable projects.
Services: Education programs, health camps, skill development workshops.
Contact: info@ait.iak.ngo
"""

def get_gemini_response(user_input):
    # Gemini API endpoint
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
    
    # Prompt banate hain
    prompt = f"""
    You are an AI agent for the website https://ait.iak.ngo/. 
    Here is the website information:
    {website_info}
    
    Answer the user's question based on this information in a clear and concise way. If you don't know something, say so politely.
    User's question: {user_input}
    """

    # API request body
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    # Headers
    headers = {
        "Content-Type": "application/json"
    }

    try:
        # API call karo
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()  # Error check
        
        # Response parse karo
        result = response.json()
        answer = result["candidates"][0]["content"]["parts"][0]["text"]
        return answer
    except Exception as e:
        return f"Error: {e}"

# Test karne ke liye
while True:
    question = input("Apna sawal poocho (ya 'exit' likho band karne ke liye): ")
    if question.lower() == "exit":
        break
    answer = get_gemini_response(question)
    print("Jawab:", answer)