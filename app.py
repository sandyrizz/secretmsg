import streamlit as st
from supabase import create_client
from cryptography.fernet import Fernet
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=".env")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

if not all([SUPABASE_URL, SUPABASE_KEY, SECRET_KEY, ADMIN_PASSWORD]):
    st.error("Environment variables not loaded properly.")
    st.stop()
    
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
cipher = Fernet(SECRET_KEY.encode())

st.set_page_config(page_title="SecretMsg", page_icon="🔒")

st.title("📩 Send Anonymous Message")
st.write("Your message is encrypted before being stored 🔐")

message = st.text_area("Type your secret message")

if st.button("Send"):
    if message.strip():
        encrypted = cipher.encrypt(message.encode()).decode()

        supabase.table("messages").insert({
            "content": encrypted
        }).execute()

        st.success("Message sent securely 🔒")
    else:
        st.warning("Message cannot be empty")

st.markdown("---")
password_input = st.text_input("Admin Password", type="password")

if password_input == ADMIN_PASSWORD:
    st.subheader("📥 Decrypted Messages")

    data = supabase.table("messages").select("*").order("id", desc=True).execute()

    for row in data.data:
        decrypted = cipher.decrypt(row["content"].encode()).decode()
        st.write("•", decrypted)