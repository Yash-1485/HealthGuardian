import streamlit as st
import requests
import mysql.connector as conn
import DB_Creadentials as crd
from User import User

def run():
    try:
        st.title("Welcome to the Health Guardian")
        
        flag=False
        user=None
        if("User" in st.session_state):
            user:User=st.session_state["User"]
            flag=True
            # st.write(user.name)    
        
    except Exception as e:
        print(e)
    
    # Health Related Articles Section 
    try:
        API_KEY = "d9524a8c976943d48e9fa008c5c93cbb" #NewsAPI
        API_URL = "https://newsapi.org/v2/everything"

        # Predefined Health Topics
        TOPICS = {
            "General Health": "health",
            "Nutrition": "nutrition",
            "Fitness": "fitness",
            "Mental Health": "mental health",
            "Disease Prevention": "disease prevention",
            "Medical Research": "medical research",
        }

        def fetch_health_articles(topic):
            """Fetch articles from NewsAPI based on the selected health topic."""
            params = {
                "q": topic,
                "apiKey": API_KEY,
                "language": "en",
                "sortBy": "publishedAt",
            }
            response = requests.get(API_URL, params=params)
            
            if response.status_code == 200:
                return response.json().get("articles", [])
            else:
                return None

        def main():
            st.title("📰 Health Related Article")
            st.subheader("Stay updated with the latest health trends!")
            selected_topic = st.selectbox("Choose a Health Topic", list(TOPICS.keys()))

            if st.button("Get Articles"):
                topic_query = TOPICS[selected_topic]  # Get actual query string
                articles = fetch_health_articles(topic_query)

                if articles:
                    st.success(f"Showing latest articles on **{selected_topic}**")
                    for article in articles[:5]:  # Display top 5 articles
                        st.subheader(article["title"])
                        st.write(article.get("description", "No description available."))
                        st.write(f"[Read more]({article['url']})")
                        st.write("---")  # Separator
                else:
                    st.warning("No articles found. Please try again later.")
        main()
    except Exception as e:
        print(e)
