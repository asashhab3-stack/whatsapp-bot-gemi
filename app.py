# Project: WhatsApp Gemini Bot
# Developer Signature: ASA

import os
from flask import Flask, request
import google.generativeai as genai
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# إعداد مفتاح التوثيق لـ Gemini 
# (يفضل إضافته لاحقاً في إعدادات Render باسم GEMINI_API_KEY ليكون آمناً)
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY_HERE")
genai.configure(api_key=GEMINI_API_KEY)

@app.route("/", methods=['GET'])
def home():
    return "WhatsApp Bot (ASA) is running successfully!"

@app.route("/webhook", methods=['POST'])
def webhook():
    # استقبال الرسالة القادمة من مستخدم الواتساب
    incoming_msg = request.values.get('Body', '').strip()
    
    # تجهيز رد Twilio
    resp = MessagingResponse()
    msg = resp.message()
    
    if not incoming_msg:
        msg.body("لم أستلم أي نص.")
        return str(resp)
    
    try:
        # إرسال الرسالة إلى نموذج جيميناي للحصول على الرد
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(incoming_msg)
        
        # إرسال رد الذكاء الاصطناعي वापस إلى الواتساب
        msg.body(response.text)
    except Exception as e:
        msg.body(f"عذراً، حدث خطأ في معالجة الطلب: {str(e)}")
        
    return str(resp)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
