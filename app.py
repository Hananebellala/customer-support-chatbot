import os
import streamlit as st
import json
import re
from rapidfuzz import fuzz

# --------------------
# Load FAQs
# --------------------
with open("data/faqs.json", "r", encoding="utf-8") as f:
    faqs = json.load(f)

st.set_page_config(page_title="Algerian Shop Chatbot", page_icon="❓")
st.title("Customer Support Chatbot")

# --------------------
# Language choice
# --------------------
lang_choice = st.radio("Select Language / اختر اللغة / Choisissez la langue",
                       ["English", "Français", "العربية"])

lang_map = {"English": "en", "Français": "fr", "العربية": "ar"}
lang = lang_map[lang_choice]

# --------------------
# Keywords dictionary
# --------------------
KEYWORDS = {
    "delivery": {"delivery", "deliver", "ship", "shipping", "order", "توصيل", "وصل", "livraison", "envoyer"},
    "refund": {"refund", "refunding", "return", "returns", "money back", "استرجاع", "إرجاع", "remboursement", "rembourser"},
    "exchange": {"exchange", "swap", "change", "size", "تبديل", "تغيير", "changer", "échange"},
    "payment_methods": {"payment", "pay", "card", "visa", "mastercard", "paypal", "الدفع", "بطاقة", "paiement", "payer"},
    "shipping_fees": {"fees", "cost", "charges", "expensive", "رسوم", "تكلفة", "frais", "prix"},
    "tracking": {"track", "tracking", "where", "package", "تتبع", "تبع", "suivre", "suivi"},
    "contact": {"contact", "support", "email", "phone", "اتصال", "دعم", "مساعدة", "aider"},
    "store_hours": {"hours", "time", "open", "closing", "working", "مفتوح", "وقت", "horaire", "ouvert"},
    "warranty": {"warranty", "guarantee", "ضمان", "كفالة", "garantie"},
    "bulk_orders": {"bulk", "wholesale", "large", "big order", "جملة", "كمية", "grossiste", "commande en gros"},
    "availability": {"available", "stock", "out of stock", "توفر", "موجود", "disponible", "rupture"},
    "languages": {"language", "arabic", "french", "english", "لغة", "العربية", "الفرنسية", "الإنجليزية"},
    
    # Small talk
    "greeting": {"hi", "hello", "hey", "salam", "سلام", "bonjour", "salut", "هلا"},
    "how_are_you": {"how are you", "كيف حالك", "ça va", "comment ça va", "labas"},
    "thanks": {"thanks", "thank you", "شكرا", "merçi", "merci", "choukran"},
    "bye": {"bye", "goodbye", "مع السلامة", "إلى اللقاء", "au revoir", "salut"}
}


def normalize(text):
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)  # remove punctuation
    return text.strip()

# --------------------
# Match keywords with fuzzy matching
# --------------------
def match_keyword(question, threshold=80):
    q = question.lower()
    best_match, best_score = None, 0
    for key, words in KEYWORDS.items():
        for w in words:
            score = fuzz.partial_ratio(q, w)
            if score > best_score:
                best_score = score
                best_match = key
    return best_match if best_score >= threshold else None

# --------------------
# Get answer (offline, FAQ only)
# --------------------
def get_answer(question, lang):
    key = match_keyword(question)
    if key and key in faqs:
        return faqs[key][lang]
    else:
        return {
            "en": "Sorry, I couldn’t find an exact answer. Please contact support.",
            "fr": "Désolé, je n’ai pas trouvé de réponse exacte. Veuillez contacter le support.",
            "ar": "عذرًا، لم أجد إجابة دقيقة. يرجى الاتصال بالدعم."
        }[lang]

# --------------------
# User input
# --------------------
user_input = st.text_input("Ask your question")
if user_input:
    answer = get_answer(user_input, lang)
    st.success(answer)
