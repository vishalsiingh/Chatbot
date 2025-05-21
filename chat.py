import streamlit as st
import requests
import json
from fpdf import FPDF
import os

# Groq API Key
GROQ_API_KEY = "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"

# Available models
AVAILABLE_MODELS = {
    "LLaMA 3 70B": "llama3-70b-8192",
    "Mixtral 8x7B": "mixtral-8x7b-32768",
    "Gemma 7B": "gemma-7b-it"
}

# Set page
st.set_page_config(page_title="Groq AI Chatbot", page_icon="🤖")
st.title("🤖 Groq Chatbot with Export, Save & Model Selector")

# Select model
selected_model = st.selectbox("🧠 Choose Model", list(AVAILABLE_MODELS.keys()))
model_id = AVAILABLE_MODELS[selected_model]

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [{"role": "system", "content": "You are a helpful assistant."}]

# Chat API call
def chat_with_groq(message, chat_history):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model_id,
        "messages": chat_history + [{"role": "user", "content": message}],
        "temperature": 0.7
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return "Error: " + response.text

# Display chat
for msg in st.session_state.chat_history[1:]:
    with st.chat_message("user" if msg["role"] == "user" else "assistant", avatar="🧑‍💻" if msg["role"] == "user" else "🤖"):
        st.markdown(msg["content"])

# Chat input
user_input = st.text_input("Type your message here")

# Submit message
if st.button("Send"):
    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        response = chat_with_groq(user_input, st.session_state.chat_history)
        st.session_state.chat_history.append({"role": "assistant", "content": response})
        st.rerun()


# Save chat to JSON
def save_to_file(filename="chat_history.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(st.session_state.chat_history, f, indent=4)

# Export chat to PDF
def export_to_pdf(filename="chat_export.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for msg in st.session_state.chat_history[1:]:  # Skip system prompt
        role = "You" if msg["role"] == "user" else "Bot"
        content = msg["content"]
        pdf.multi_cell(0, 10, f"{role}: {content}")
        pdf.ln()
    pdf.output(filename)

# Export buttons
col1, col2 = st.columns(2)
with col1:
    if st.button("💾 Save to JSON"):
        save_to_file()
        st.success("Chat history saved to chat_history.json.")
with col2:
    if st.button("📄 Export to PDF"):
        export_to_pdf()
        st.success("Chat exported to chat_export.pdf.")