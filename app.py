import streamlit as st
import json
import os

with open("data/faqs.json", "r", encoding="utf-8") as f:
    faqs = json.load(f)

st.set_page_config(page_title="Algerian Shop Chatbot", page_icon="❓")
st.title("Customer Support Chatbot")

# Radio in human-readable names
lang_choice = st.radio("Select Language / اختر اللغة / Choisissez la langue",
                       ["English", "Français", "العربية"])

# Map to JSON keys
lang_map = {
    "English": "en",
    "Français": "fr",
    "العربية": "ar"
}
lang = lang_map[lang_choice]

# User input
user_input = st.text_input("Ask your question")

def get_answer(question, lang):
    question = question.lower()

    if "delivery" in question or "توصيل" in question or "livraison" in question:
        return faqs["delivery"][lang]
    elif "refund" in question or "استرجاع" in question or "remboursement" in question:
        return faqs["refund"][lang]
    elif "payment" in question or "الدفع" in question or "paiement" in question:
        return faqs["payment_methods"][lang]
    elif "fees" in question or "frais" in question or "رسوم" in question:
        return faqs["shipping_fees"][lang]
    elif "contact" in question or "اتصال" in question or "contact" in question:
        return faqs["contact"][lang]
    else:
        fallback = {
            "en": "Sorry, I don’t understand. Please contact support.",
            "fr": "Désolé, je ne comprends pas. Veuillez contacter le support.",
            "ar": "عذرًا، لم أفهم. يرجى الاتصال بخدمة العملاء."
        }
        return fallback[lang]

if user_input:
    answer = get_answer(user_input, lang)
    st.success(answer)
