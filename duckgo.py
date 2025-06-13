import os
import streamlit as st
from langchain_community.tools.ddg_search.tool import DuckDuckGoSearchResults
import google.generativeai as genai

# ----------------------------
# Set Gemini API Key
# ----------------------------
GOOGLE_API_KEY = "AIzaSyCK7QRKCq4GuBZErZaMLRInRjmT891g6Bg"  # Replace safely
genai.configure(api_key=GOOGLE_API_KEY)

# ----------------------------
# Initialize Model
# ----------------------------
model = genai.GenerativeModel("gemini-1.5-flash")

# ----------------------------
# Streamlit UI
# ----------------------------
st.set_page_config(page_title="🔍 Web Search + Gemini", layout="centered")
st.title("🌐 Ask Anything (Web Search + Gemini)")

query = st.text_input("Enter your search query:")

if st.button("🔎 Search"):
    if not query.strip():
        st.warning("Please enter a search query.")
    else:
        try:
            with st.spinner("Searching and thinking..."):

                # Run DuckDuckGo search
                search_tool = DuckDuckGoSearchResults()
                search_results = search_tool.run(query)

                if isinstance(search_results, list):
                    context = "\n\n".join([
                        f"🔹 {res.get('title', '')}\n{res.get('snippet', '')}\n🔗 {res.get('link', '')}"
                        if isinstance(res, dict) else str(res)
                        for res in search_results
                    ])
                else:
                    context = str(search_results)

                # Build prompt
                prompt = f"""
You are a helpful assistant. Based on the following web search results, answer the user's question.

Search Results:
{context}

User Question:
{query}
"""

                # Generate response
                response = model.generate_content(prompt)
                st.success("✅ Answer generated!")
                st.markdown(f"**Answer:**\n\n{response.text}")

        except Exception as e:
            st.error(f"❌ An error occurred: {e}")
