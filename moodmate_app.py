from rag_retriever import retrieve_relevant_context
import streamlit as st
import requests
import os
from dotenv import load_dotenv


load_dotenv()  
HF_TOKEN = os.getenv("HF_TOKEN")

# 🪄 Streamlit Page Settings
st.set_page_config(page_title="MoodMate 🕯️", page_icon="🌷")
st.title("🌷 MoodMate – Your Soft-Spoken Support AI")
st.write("Tell me how you're feeling today, and I’ll hold space for you 💌")

# 🧠 User Input
user_input = st.text_input("💭 What's on your mind?", placeholder="I'm feeling a bit overwhelmed today...")


if user_input:
    with st.spinner("MoodMate is thinking... 🧠"):
        try:
            # 🔍 Step 1: Retrieve relevant context from file
            context = retrieve_relevant_context(user_input, file_path="data/mood_knowledge.txt")

            # 📝 Step 2: Combine context + query
            full_prompt = f"Context:\n{context}\n\nUser Query:\n{user_input}"

            # 🚀 Step 3: Prepare request
            headers = {
                "Authorization": f"Bearer {HF_TOKEN}",
                "Content-Type": "application/json"
            }

            data = {
                "inputs": {
                    "past_user_inputs": [],
                    "generated_responses": [],
                    "text": full_prompt
                }
            }

            # 🔗 Step 4: Send to HuggingFace endpoint
            response = requests.post(
                "https://api-inference.huggingface.co/chat/assistant/68566fc693d565d0bdbac000",
                headers=headers,
                json=data
            )

            # 📤 Step 5: Show reply or error
            if response.status_code == 200:
                moodmate_reply = response.json().get("generated_text", "")
                st.markdown(f"🕯️ **MoodMate says:**\n\n{moodmate_reply}")
            else:
                st.error(f"Oops! Something went wrong. Status code: {response.status_code}")

        except Exception as e:
            st.error(f"An error occurred: {e}")
