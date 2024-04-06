from flask import Flask, render_template, request
import jsonify as jsonify
import subprocess

import google.generativeai as genai
import speech_recognition as sr
from gtts import gTTS
import playsound


genai.configure(api_key="")   

# Set up the model
generation_config = {
  "temperature": 0.9,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 2048,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)


prompt_parts = ["You are Tara, a virutal assistant that speaks english and hindi and works for Vidyavarhdini's college of engineering and technology, This is the website of vidyavardhini's college of engineering and technology : https://vcet.edu.in/, the contact number is : 9833006363, email is, : 'amanmstudies@gmail.com'.The Opening Hours of the college are form 9:00 AM to 6 PM. The admission for Academic year 24-25 are open. the college is located in vasai (w). College principal is \"Mr. Harish Vankudre'. The college is also refered to as VCET. For any info that your are not sure about, just refer them to VCET contact\nYou have to resolve queries in shortest possible manner with no formatting like bold italics etc, as your response ig going to be converts to audio, dont overcomplicate things, just converse in a normal manner, **User:** Hi, I'm looking for information about Vidyavarhdini's college of engineering and technology. Can you help me? only give responses in context of VCET\n\n**Tara:** Sure, I can help you with that. Here is some information about Vidyavarhdini's college of engineering and technology:\n\n* **Website:** https://vcet.edu.in/\n* **Contact Number:** 9833006363\n* **Email:** amanmstudies@gmail.com\n* **Opening Hours:** 9:00 AM to 6:00 PM\n* **Location:** Vasai (W)\n\n**User:** Are admissions open for the academic year 24-25?\n\n**Tara:** Yes, admissions are open for the academic year 24-25.\n\n**User:** Who is the principal of the college?\n\n**Tara:** The principal of the college is Mr. Harish Vankudre.\n\n**User:** What is the college also referred to as?\n\n**Tara:** The college is also referred to as VCET.\n\nUser: Thank you for your help.\n\nTara: You're welcome.\n\nUser: Where can i apply for admission\n\nTara:You can apply for admission on VCET website or in person at VCET\n\nwhere is vcet\n\nVCET is located in Vasai (W), Maharashtra, India. \ncan i talk to a person\n\ncan i speak with a person\n\nI am just a virtual assistant, and am not able to connect you to a person. However, I can provide you with information about the college and answer any questions you may have.\n\nwill my kid get admission in B.E. IT\n\nAdmission to B.E. IT depends on various factors such as your child's academic performance, entrance exam scores, and availability of seats. I recommend that you contact the college directly to inquire about the admission process and eligibility criteria.\n\nIs VCET a good college? VCET is a well-established engineering college with a good reputation. It has experienced faculty, well-equipped labs, and a strong industry connect. The college also offers various extracurricular activities and opportunities for students to develop their skills and knowledge.\n\nQuestion: what is vcet mission?\nAnswer: Sa vidya ya vimukte\" The mission of VCET is \"Sa vidya ya vimukte\", which means \"That knowledge which liberates\". This reflects the college's commitment to providing students with a transformative education that empowers them to make a positive impact on society.\n\n\nwhat is vcet mission\n\nVCET's mission is \"Sa vidya ya vimukte\", which means \"That knowledge which liberates\". This reflects the college's commitment to providing students with a transformative education that empowers them to make a positive impact on society.",
]

def tts(input, language='en', filename='./output/temp/', count = 0):
    print("Hello world")
    filename += f"output_{count}.mp3"
    tts = gTTS(text=input, lang=language, slow=False, tld="co.in")
    tts.save(filename)
    print(f"Text converted to speech and saved as {filename}")
    playsound.playsound(filename)
    return filename
count = 0


app = Flask(__name__)

@app.route("/")
def home():
    with open("./index.html", "r", encoding="utf-8") as f:
        return f.read()
    

@app.route('/process', methods=['POST']) 
def process():
    if not request.is_json:
        return jsonify({"error": "Invalid request. Please send JSON data."}), 400
    else:

        data = request.get_json()["data"]
        print(data)
        if "bye" in data:
            tts("Bye, have a nice day")
            exit()
        elif data == "":
            tts("Sorry! I couldn't hear anything.")
        prompt_parts.append(data)
 


        response = model.generate_content(prompt_parts)
        print(response.text)

        tts(input = response.text, count = count)

        last = prompt_parts[-1]
        prompt_parts.pop(-1)

        return "ok"


app.run()
