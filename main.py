import json
import google.generativeai as genai
from google.generativeai import configure

with open('secret.txt', 'r') as file:
    API_KEY = file.read()
configure(api_key=API_KEY)
model=genai.GenerativeModel('gemini-1.5-flash')

with open("courses.json", "r") as f:
    data = json.load(f)

with open("rules.json", "r") as f:
    rules = json.load(f)

for cse_course in data["courses"]["CSE"][:5]:
    print(model.generate_content(rules["prereq"] + "\n\n" + cse_course).text)