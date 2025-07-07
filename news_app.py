import os
import requests
import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAI
from langchain.prompts import PromptTemplate

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# Initialize Gemini
llm = GoogleGenerativeAI(model="models/gemini-1.5-flash", api_key=GOOGLE_API_KEY)

# Streamlit UI
st.title("🗞 AI News Assistant")
st.subheader("Get latest news summaries with Gemini + LangChain")

category = st.selectbox("Choose a news category", ["general", "sports", "technology", "business", "entertainment", "health", "science"])
if st.button("Get News"):
    with st.spinner("Fetching news..."):

        # 1. Get latest news articles from NewsAPI
        url = f"https://newsapi.org/v2/top-headlines?category={category}&language=en&pageSize=5&apiKey={NEWS_API_KEY}"
        response = requests.get(url).json()

        articles = response.get("articles", [])
        if not articles:
            st.warning("No news found.")
        else:
            headlines = "\n".join(f"- {article['title']}" for article in articles if article['title'])

            # 2. Summarize with Gemini
            prompt = PromptTemplate(
                input_variables=["headlines"],
                template="""
                Summarize the following news headlines into 3–4 short bullet points with accurate info and plain language:
                {headlines}
                """
            )
            final_prompt = prompt.format(headlines=headlines)
            summary = llm.invoke(final_prompt)

            # 3. Display
            st.markdown("### 🔎 News Summary")
            st.markdown(summary)