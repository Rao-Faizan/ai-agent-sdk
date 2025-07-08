# import os
# import json
# import logging
# import time
# import requests
# from flask import Flask, request
# from twilio.twiml.messaging_response import MessagingResponse
# from dotenv import load_dotenv

# load_dotenv()
# app = Flask(__name__)

# logging.basicConfig(
#     level=logging.DEBUG,
#     format='%(asctime)s - %(levelname)s - %(message)s',
#     handlers=[logging.FileHandler('scraper.log', encoding='utf-8'), logging.StreamHandler()]
# )

# BASE_URL = "https://ait.iak.ngo"
# URLS = {
#     "home": BASE_URL,
#     "about": f"{BASE_URL}/about",
#     "courses": f"{BASE_URL}/courses",
#     "contact": f"{BASE_URL}/contact"
# }

# PARSEHUB_TOKENS = {
#     "home": "t8F_RYHScEfy",
#     "about": "t0UiRaP4qXGv",
#     "courses": "t9YOV0GCYTVY",
#     "contact": "tn6uFYTDF5AG"
# }

# def load_json_data(file_path):
#     try:
#         if os.path.exists(file_path):
#             with open(file_path, 'r', encoding='utf-8') as f:
#                 return json.load(f)
#         return {}
#     except Exception as e:
#         logging.error(f"Error loading JSON {file_path}: {e}")
#         return {}

# def save_json_data(file_path, data):
#     try:
#         with open(file_path, 'w', encoding='utf-8') as f:
#             json.dump(data, f, indent=2)
#         logging.debug(f"Saved data to {file_path}")
#     except Exception as e:
#         logging.error(f"Error saving JSON {file_path}: {e}")

# def clean_contact_data(data):
#     if not data or "selection1" not in data:
#         return {"contact": {"address": "", "email": [], "phone": []}}
#     cleaned = {"contact": {"address": "", "email": [], "phone": []}}
#     seen = set()
#     for item in data.get("selection1", []):
#         text = item.get("name", "").strip()
#         if text and text not in seen:
#             if "@" in text:
#                 cleaned["contact"]["email"].append(text)
#             elif text.replace("+", "").isdigit() and len(text) > 6:
#                 cleaned["contact"]["phone"].append(text)
#             elif "A 507" in text:
#                 cleaned["contact"]["address"] = "A 507, Sector 11-A, Near Power House Chorangi, North Karachi, Karachi, Pakistan"
#             seen.add(text)
#     if not cleaned["contact"]["address"] and not cleaned["contact"]["email"] and not cleaned["contact"]["phone"]:
#         cleaned["contact"]["address"] = "Contact info not available"
#     return cleaned

# def clean_home_data(data):
#     if not data or "selection1" not in data:
#         return {"home": {"title": ""}}
#     cleaned = {"home": {"title": ""}}
#     seen = set()
#     for item in data.get("selection1", []):
#         text = item.get("name", "").strip()
#         if text and "Shape Your Future in Tech" in text and text not in seen:
#             cleaned["home"]["title"] = text.split("How to Register")[0].strip()
#             seen.add(text)
#             break
#     if not cleaned["home"]["title"]:
#         cleaned["home"]["title"] = "Welcome to AIT"
#     return cleaned

# def clean_about_data(data):
#     if not data or ("selection1" not in data and "selection3" not in data):
#         return {"about": {"about": "AIT is a tech institute.", "mission": ""}}
#     cleaned = {"about": {"about": "", "mission": ""}}
#     seen = set()
#     for item in data.get("selection1", []):
#         text = item.get("name", "").strip()
#         if text and "AL-Khair Institute of Technology" in text and text not in seen:
#             cleaned["about"]["about"] = text
#             seen.add(text)
#     for item in data.get("selection3", []):
#         text = item.get("name", "").strip()
#         if "Message from our CEO" in text and text not in seen:
#             cleaned["about"]["mission"] = text
#             seen.add(text)
#     if not cleaned["about"]["about"]:
#         cleaned["about"]["about"] = "AIT is a tech institute."
#     if not cleaned["about"]["mission"]:
#         cleaned["about"]["mission"] = "Mission not available."
#     return cleaned

# def clean_courses_data(data):
#     if not data or "selection1" not in data:
#         return {"courses": []}
#     cleaned = {"courses": []}
#     seen = set()
#     for item in data.get("selection1", []):
#         name = item.get("name", "").strip()
#         if name and name not in seen:
#             if "\n" in name:
#                 parts = name.split("\n")
#                 course_name = parts[0].strip() if parts else name
#                 description = "\n".join(parts[1:]).strip() if len(parts) > 1 else "No description available"
#             else:
#                 course_name = name
#                 description = "No description available"
#             cleaned["courses"].append({"name": course_name, "description": description})
#             seen.add(name)
#     return cleaned

# def scrape_with_parsehub():
#     api_key = os.getenv("PARSEHUB_API_KEY")
#     if not api_key:
#         logging.error("PARSEHUB_API_KEY not set")
#         return {}
    
#     scraped_data = {}
#     for page, token in PARSEHUB_TOKENS.items():
#         params = {"api_key": api_key, "start_url": URLS[page], "send_email": "0"}
#         try:
#             response = requests.post(f"https://www.parsehub.com/api/v2/projects/{token}/run", data=params)
#             logging.debug(f"ParseHub API response for {page}: {response.text}")
#             if response.status_code == 200:
#                 run_data = response.json()
#                 run_token = run_data["run_token"]
#                 for attempt in range(10):
#                     status = requests.get(f"https://www.parsehub.com/api/v2/runs/{run_token}?api_key={api_key}")
#                     if status.json().get("data_ready"):
#                         data = requests.get(f"https://www.parsehub.com/api/v2/runs/{run_token}/data?api_key={api_key}")
#                         parsed_data = json.loads(data.text) if data.text else {}
#                         if page == "contact":
#                             parsed_data = clean_contact_data(parsed_data)
#                         elif page == "home":
#                             parsed_data = clean_home_data(parsed_data)
#                         elif page == "about":
#                             parsed_data = clean_about_data(parsed_data)
#                         elif page == "courses":
#                             parsed_data = clean_courses_data(parsed_data)
#                         scraped_data.update(parsed_data)
#                         logging.debug(f"Scraped data for {page}: {parsed_data}")
#                         break
#                     time.sleep(30 if attempt < 5 else 60)
#                 else:
#                     logging.error(f"Data not ready after 10 attempts for {page}")
#         except Exception as e:
#             logging.error(f"ParseHub error for {page}: {e}")
#     save_json_data("website_data.json", scraped_data)
#     return scraped_data

# # Initialize website_data globally
# website_data = load_json_data("website_data.json")
# if not website_data:
#     website_data = scrape_with_parsehub()
# logging.info("Starting AIT WhatsApp Bot...")

# class AITConversationalAgent:
#     def __init__(self, data):
#         self.data = data if isinstance(data, dict) else (data[0] if isinstance(data, list) and data else {})

#     def get_response(self, message):
#         message = message.lower().strip()
#         # Greeting handling
#         if any(greet in message for greet in ['hello', 'Hey', 'assalamualikum', 'hy']):
#             return "Hello! Assalamualikum! 😊 Main AIT ka WhatsApp bot hoon. Aapki kaise madad kar sakta hoon? AIT ke bare mein   ke bare mein puch sakte ho!"
#         # Intent-based responses
#         if any(keyword in message for keyword in ['about', 'what is ait', 'ait ki information']):
#             about = self.data.get('about', {}).get('about', 'AIT is a tech institute.')
#             mission = self.data.get('about', {}).get('mission', 'Mission not available.')
#             return f"About AIT: {about}\nMission: {mission}"
#         elif any(keyword in message for keyword in ['contact', 'phone', 'email', 'address']):
#             contact = self.data.get('contact', {}).get('contact', {})
#             return f"Contact Info: Address: {contact.get('address', 'Not available')} | Email: {', '.join(contact.get('email', ['Not available']))} | Phone: {', '.join(contact.get('phone', ['Not available']))}"
#         elif any(keyword in message for keyword in ['courses', 'course list', 'offer courses', 'training']):
#             courses = self.data.get('courses', {}).get('courses', [])
#             if courses:
#                 course_list = '\n'.join([f"{c['name']}: {c['description']}" for c in courses])
#                 return f"Courses Offered:\n{course_list}"
#             return "Sorry, abhi koi courses available nahi hain. Thodi der baad phir try karen!"
#         elif any(keyword in message for keyword in ['home', 'welcome', 'start']):
#             home = self.data.get('home', {}).get('home', {})
#             return f"Welcome to AIT: {home.get('title', 'Welcome to AIT')}"
#         else:
#             return "Bhai, mujhe thoda samajh nahi aaya! AIT ke bare mein 'about', 'courses', 'contact', ya 'home' ke bare mein puch sakte ho. Ya kuch aur batayein, main madad karne ki koshish karunga! 😄"

# class CourseGuideAgent:
#     def __init__(self, data):
#         # Handle data as list or dict
#         if isinstance(data, list) and data:
#             effective_data = data[0] if isinstance(data[0], dict) else {}
#             self.courses = effective_data.get('courses', [])
#         else:
#             self.courses = data.get('courses', []) if isinstance(data, dict) else []

#     def get_course_details(self, course_name):
#         for course in self.courses:
#             if course_name.lower() in course['name'].lower():
#                 return f"{course['name']}:\nDescription: {course['description']}\nLevel: Check AIT website for exact level!\nDuration: Varies, usually 3-4 months per level.\nNote: Start with basics and progress to advanced topics."
#         return "Bhai, yeh course nahi mila! Available courses ke liye '!courses' ya 'course list' puch lo."

#     def get_response(self, message):
#         message = message.lower().strip()
#         if 'course' in message or 'training' in message:
#             if any(c.lower() in message for c in ['data analysis', 'data science', 'machine learning', 'graphic designing']):
#                 return self.get_course_details(message)
#             return "Puch lo kaunsa course chahiye (e.g., 'data analysis', 'data science', ya 'graphic designing') ya '!courses' se list dekho. Main tumhe step-by-step guide karunga!"
#         return "Bhai, courses ke bare mein puchne ke liye 'course' ya specific course name likho (jaise 'data analysis'). Main tumhe madad karunga! 😄"

# # Initialize agents
# conversational_agent = AITConversationalAgent(website_data)
# course_guide_agent = CourseGuideAgent(website_data)

# @app.route('/whatsapp', methods=['POST'])
# def whatsapp():
#     global website_data
#     incoming_msg = request.values.get('Body', '').lower().strip()
#     resp = MessagingResponse()
#     msg = resp.message()

#     if not website_data:
#         website_data = scrape_with_parsehub()

#     # Try conversational agent first
#     conv_response = conversational_agent.get_response(incoming_msg)
#     if "Bhai, mujhe thoda samajh nahi aaya" not in conv_response:
#         msg.body(conv_response)
#     else:
#         # Try course guide agent
#         guide_response = course_guide_agent.get_response(incoming_msg)
#         if "Bhai, courses ke bare mein puchne" not in guide_response:
#             msg.body(guide_response)
#         else:
#             msg.body(conv_response)

#     return str(resp)

# @app.route('/refresh', methods=['POST', 'GET'])
# def refresh():
#     global website_data
#     website_data = scrape_with_parsehub()
#     save_json_data("website_data.json", website_data)
#     conversational_agent = AITConversationalAgent(website_data)
#     course_guide_agent = CourseGuideAgent(website_data)
#     return "Data refreshed successfully."

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000, debug=True)


import os
import json
import logging
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
app = Flask(__name__)

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('bot.log', encoding='utf-8'), logging.StreamHandler()]
)

class AITBot:
    def __init__(self, data):
        self.data = self.clean_data(data)
        self.greetings = ['hello', 'hi', 'hey', 'assalamualikum', 'salam', 'hy']
        
    def clean_data(self, data):
        """Clean and organize the scraped data"""
        if not data:
            return {}
            
        cleaned = data.copy()
        
        # Clean courses data
        if 'courses' in cleaned and isinstance(cleaned['courses'], list):
            # These are the actual course names we want to show
            main_course_names = [
                "Data Analysis & Office Productivity",
                "Data Science, Machine Learning & AI Specialization",
                "Digital Marketing Specialization",
                "Foundations of Programming Specialization",
                "Game Development Specialization",
                "Graphic Design & Creative Arts Specialization",
                "Programming & Backend Development Specialization",
                "Web Development Specialization",
                "AI & Robotics Specialization",
                "AR/VR Development Specialization",
                "Blockchain Technology Specialization",
                "Business & Project Management Specialization",
                "Cybersecurity Specialization",
                "Data Engineering Specialization",
                "DevOps, Cloud Computing & Software Development Specialization",
                "Freelancing & Productivity Specialization",
                "Internet of Things (IoT) & Embedded Systems Specialization",
                "Mobile App Development Specialization",
                "Software Testing & Quality Assurance Specialization",
                "Language: Arabic",
                "Language: Japanese",
                "Language: English"
            ]
            
            # Create a clean courses list with only these names
            cleaned_courses = []
            for name in main_course_names:
                # Find the most complete description for this course
                best_desc = "Course details available"
                for course in cleaned['courses']:
                    if isinstance(course, dict) and course.get('name'):
                        if name.lower() in course['name'].lower():
                            desc = course.get('description', '')
                            if isinstance(desc, str) and len(desc) > len(best_desc):
                                best_desc = desc
                
                cleaned_courses.append({
                    'name': name,
                    'description': self.clean_description(best_desc),
                    'duration': self.extract_duration(best_desc)
                })
            
            cleaned['courses'] = cleaned_courses
        
        return cleaned
    
    def clean_description(self, desc):
        """Clean up course descriptions"""
        if not desc or not isinstance(desc, str):
            return "Course details available"
            
        # Take only the first line if there are multiple lines
        first_line = desc.split('\n')[0].strip()
        if not first_line or 'No description available' in first_line:
            return "Course details available"
        
        # Remove any duration information that might be in the description
        if 'month' in first_line.lower() or 'level' in first_line.lower():
            return "Course details available"
            
        return first_line
    
    def extract_duration(self, desc):
        """Extract duration from course description if available"""
        if not desc or not isinstance(desc, str):
            return "Contact for duration"
            
        # Look for duration pattern in the description
        for line in desc.split('\n'):
            if 'month' in line.lower():
                return line.strip()
        return "Contact for duration"
    
    def get_main_courses(self):
        """Get only the main technical courses (excluding languages)"""
        if not self.data.get('courses'):
            return []
            
        return [course for course in self.data['courses'] 
                if not course['name'].lower().startswith('language:')]
    
    def get_language_courses(self):
        """Get only language courses"""
        if not self.data.get('courses'):
            return []
            
        return [course for course in self.data['courses'] 
                if course['name'].lower().startswith('language:')]
    
    def get_course_list(self):
        """Get a clean list of available courses"""
        main_courses = self.get_main_courses()
        language_courses = self.get_language_courses()
        
        if not main_courses and not language_courses:
            return "Currently no courses available. Please check back later."
        
        response = "📚 *Available Courses at AIT:*\n\n"
        
        if main_courses:
            response += "💻 *Technical Courses:*\n"
            response += "\n".join(f"• {course['name']}" 
                               for course in sorted(main_courses, key=lambda x: x['name'])) 
            response += "\n\n"
        
        if language_courses:
            response += "🌍 *Language Courses:*\n"
            response += "\n".join(f"• {course['name']}" 
                                for course in sorted(language_courses, key=lambda x: x['name']))
            response += "\n\n"
        
        response += "For details about any course, type the course name (e.g., 'Data Analysis')"
        return response
    
    def get_course_details(self, course_name):
        """Get detailed information about a specific course"""
        all_courses = self.get_main_courses() + self.get_language_courses()
        if not all_courses:
            return "Course information not available currently."
            
        # Find exact match first
        for course in all_courses:
            if course_name.lower() == course['name'].lower():
                return (
                    f"🏫 *{course['name']}*\n\n"
                    f"📝 *Overview*: {course['description']}\n"
                    f"⏳ *Duration*: {course['duration']}\n\n"
                    "For enrollment, please contact:\n"
                    "📞 +92 333 2336203\n"
                    "✉️ ait.info@iak.ngo"
                )
        
        # Find partial matches
        similar = [c['name'] for c in all_courses if course_name.lower() in c['name'].lower()]
        if similar:
            return (
                f"Course '{course_name}' not found. Maybe you meant:\n\n" +
                "\n".join(f"• {name}" for name in similar) +
                "\n\nType the exact course name for details."
            )
        
        return (
            f"Course '{course_name}' not found.\n\n"
            "Type 'courses' to see available options or check your spelling."
        )
    
    def get_response(self, message):
        message = message.lower().strip()
        
        # Handle greetings
        if any(greet in message for greet in self.greetings):
            return (
                "Assalamualikum! 👋\n\n"
                "AL-Khair Institute of Technology (AIT) ka WhatsApp bot mein aapka welcome hai!\n\n"
                "Aap hum se in cheezon ke bare mein pooch sakte hain:\n"
                "✅ Courses aur training programs\n"
                "✅ Institute ke bare mein information\n"
                "✅ Contact details\n"
                "✅ Admission process\n\n"
                "Aap ka sawal?"
            )
        
        # Handle course list requests
        if any(word in message for word in ['courses', 'course', 'training', 'program', 'korz']):
            return self.get_course_list()
            
        # Handle specific course requests
        if any(word in message for word in ['data', 'analysis', 'digital', 'marketing', 'programming', 
                                          'game', 'design', 'web', 'ai', 'robotics', 'language']):
            return self.get_course_details(message)
        
        # Handle contact info
        if any(word in message for word in ['contact', 'address', 'phone', 'email', 'number']):
            return (
                "📌 *Contact Information:*\n\n"
                "🏠 *Address*: A 507, Sector 11-A, Near Power House Chorangi, North Karachi\n"
                "📞 *Phone*: (021) 36 902991, +92 333 2336203\n"
                "✉️ *Email*: ait.info@iak.ngo\n\n"
                "For quick response, WhatsApp this number directly!"
            )
        
        # Handle about info
        if any(word in message for word in ['about', 'ait', 'institute']):
            return (
                "🏫 *About AL-Khair Institute of Technology:*\n\n"
                "AIT offers quality IT training programs in Karachi to help students "
                "build careers in technology fields.\n\n"
                "Visit our website for complete information."
            )
        
        # Default response
        return (
            "Maaf karein, mein aap ke sawal ka jawab nahi de paya. 😔\n\n"
            "Kya aap in mein se kuch poochna chahenge?\n"
            "• 'courses' - All available programs\n"
            "• 'data analysis' - Specific course info\n"
            "• 'contact' - Institute contact details\n"
            "• 'about' - About AIT institute\n\n"
            "Ya phir apna sawal dobara try karein."
        )

# Load website data
def load_website_data():
    try:
        with open('website_data.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Error loading website data: {str(e)}")
        return {}

# Initialize bot
website_data = load_website_data()
ait_bot = AITBot(website_data)

@app.route('/whatsapp', methods=['POST'])
def whatsapp():
    incoming_msg = request.values.get('Body', '').strip()
    resp = MessagingResponse()
    msg = resp.message()
    
    response = ait_bot.get_response(incoming_msg)
    msg.body(response)
    
    return str(resp)

@app.route('/refresh', methods=['POST', 'GET'])
def refresh():
    global website_data, ait_bot
    website_data = load_website_data()
    ait_bot = AITBot(website_data)
    return "Data refreshed successfully."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)