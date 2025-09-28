from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from googletrans import Translator   # ✅ translation module

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)

translator = Translator()

# 🔹 Responses dictionary (English + Hindi + Rajasthani + Bengali – can add more)
responses = {
    "en": {
        "fee deadline": "💰 The last date to pay fees is the 25th of each month.",
        "fee structure": "💰 Fee Structure: Tuition ₹25,000, Hostel ₹15,000, Transport ₹8,000, Exam ₹2,000.",
        "documents": "📄 Required docs: 10th+12th marksheets, Transfer Certificate, Aadhar card, Photos, Caste certificate.",
        "admission process": "📝 Admission starts in June. Fill form, attach documents, submit online or office, pay initial fee, seat via cutoff/merit.",
        "default": "🤔 Sorry, I don’t know that yet."
    },
    "hi": {
        "fee deadline": "💰 फीस जमा करने की अंतिम तिथि हर महीने की 25 तारीख है।",
        "fee structure": "💰 फीस संरचना: ट्यूशन ₹25,000, हॉस्टल ₹15,000, ट्रांसपोर्ट ₹8,000, परीक्षा ₹2,000।",
        "documents": "📄 आवश्यक दस्तावेज़: 10वीं+12वीं मार्कशीट, ट्रांसफर सर्टिफिकेट, आधार कार्ड, फोटो, जाति प्रमाण पत्र।",
        "admission process": "📝 प्रवेश जून से शुरू। फॉर्म भरें, दस्तावेज़ जमा करें, शुल्क भरें, मेरिट/कटऑफ के अनुसार सीट पक्की करें।",
        "default": "🤔 क्षमा करें, यह जानकारी उपलब्ध नहीं है।"
    },
    "raj": {
        "fee deadline": "💰 फीस जमा करन री आखरी तारीख २५ है।",
        "fee structure": "💰 फीस सांचो: ट्यूशन ₹25,000, हॉस्टल ₹15,000, ट्रांसपोर्ट ₹8,000, परीक्षा ₹2,000।",
        "documents": "📄 जरूरी कागद: 10वीं+12वीं मार्कशीट, ट्रांसफर सर्टिफिकेट, आधार कार्ड, फोटो, जाति प्रमाण।",
        "admission process": "📝 जून सूं दाखला चालू। फॉर्म भरो, कागद जमा करो, फीस भरो, मेरिट/कटऑफ सूं सीट पक्की करो।",
        "default": "🤔 माफ करजो, हां जानकारी नीं है।"
    },
    "bn": {
        "fee deadline": "💰 ফি জমা দেওয়ার শেষ তারিখ প্রতি মাসের 25 তারিখ।",
        "fee structure": "💰 ফি কাঠামো: টিউশন ₹25,000, হোস্টেল ₹15,000, ট্রান্সপোর্ট ₹8,000, পরীক্ষা ₹2,000।",
        "documents": "📄 ভর্তি প্রয়োজনীয় নথি: 10ম+12শ মার্কশিট, টিসি, আধার কার্ড, ছবি, জাতিগত প্রমাণ।",
        "admission process": "📝 জুন থেকে ভর্তি। ফর্ম পূরণ করুন, নথি জমা করুন, ফি দিন, কাটঅফ/মেরিট অনুযায়ী আসন নিশ্চিত করুন।",
        "default": "🤔 আমি জানি না।"
    }
}


# 🔹 Intent detection (English only)
def detect_intent(message):
    msg = message.lower()
    if "fee structure" in msg:
        return "fee structure"
    if "fee" in msg and ("deadline" in msg or "last date" in msg):
        return "fee deadline"
    if "documents" in msg or "certificate" in msg or "doc" in msg:
        return "documents"
    if "admission" in msg or "apply" in msg or "process" in msg:
        return "admission process"
    return "default"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    msg = data.get("message", "")
    target_lang = data.get("lang", "en")  # dropdown language chosen by user

    # 1. Detect + translate input to English for intent detection
    try:
        translated_to_en = translator.translate(msg, dest="en").text.lower()
    except:
        translated_to_en = msg.lower()  # fallback if translation fails

    # 2. Find intent
    intent = detect_intent(translated_to_en)

    # 3. Get response in selected language
    lang_res = responses.get(target_lang, responses["en"])
    response_text = lang_res.get(intent, lang_res["default"])

    return jsonify({"response": response_text})


if __name__ == "__main__":
    app.run(debug=True)