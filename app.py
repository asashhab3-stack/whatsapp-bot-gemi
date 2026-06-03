import os
from flask import Flask, request
import google.generativeai as genai
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# Config Gemini API
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

@app.route("/", methods=['GET'])
def home():
    return "WhatsApp Bot (ASA) is running successfully!"

@app.route("/webhook", methods=['POST'])
def webhook():
    incoming_msg = request.values.get('Body', '').strip()
    
    resp = MessagingResponse()
    msg = resp.message()
    
    if not incoming_msg:
        msg.body("لم أستلم أي نص.")
        return str(resp)
        
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(incoming_msg)
        
        msg.body(response.text)
    except Exception as e:
        msg.body(f"عذراً، حدث خطأ في معالجة الطلب.")
        
    return str(resp)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

