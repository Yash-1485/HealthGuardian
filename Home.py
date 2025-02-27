import streamlit as st
import requests
import pandas as pd
import numpy as np
import mysql.connector as conn
import DB_Creadentials as crd
from User import User
from Fetch_Health_Data import *
import time
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
        
    # Health Related Recommandations
    try:
        def getRecommandations(period="weekly"):
            period = st.radio("Select Time Period", ["Daily", "Weekly", "Monthly"])
            if(period):
                try:
                    data=generate_recommendations(fetch_health_data(user.uid,period.lower())[1])
                    recommandations,avg_para=data[0],data[1]
                    if(count_today_user_entries(user.uid)==0 and period.lower()=='daily'):
                        st.warning('You haven\'t log health data today')
                        time.sleep(2)
                        raise Exception("Haven't logged today's data")
                    if data:
                        max_len = max(len(avg_para), len(recommandations))
                        avg_para += ["N/A"] * (max_len - len(avg_para))
                        recommandations += ["No recommendation"] * (max_len - len(recommandations))
                        avg_para = [float(x) if isinstance(x, np.float64) else x for x in avg_para]
                        avg_para = [float(x) if isinstance(x, np.int32) else x for x in avg_para]
                        data_dict = {
                            "Parameter": ["Blood Pressure (Systolic/Diastolic)", "Heartbeat", "Sugar", "Oxygen", "BMI", "Temperature"],
                            "Average Value": [
                                f"{round(float(bp[0]), 2)}/{round(float(bp[1]), 2)}" if isinstance(bp, tuple) else 
                                str(round(float(bp), 2)) if isinstance(bp, (int, float, np.float64)) else "N/A"
                                for bp in avg_para
                            ],
                            "Recommendation": recommandations[:len(avg_para)]
                        }

                        df=pd.DataFrame(data_dict)
                        st.table(df)
                    else:
                        st.info('You haven\'t log any health data')
                except Exception as e:
                    print(e)
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
                    for article in articles[:5]:  # Display top 5 articles only
                        st.subheader(article["title"])
                        st.write(article.get("description", "No description available."))
                        st.write(f"[Read more]({article['url']})")
                        st.write("---")  # Separator
                else:
                    st.warning("No articles found. Please try again later.")        
        if count_user_entries(user.uid)!=0:
            getRecommandations()
            main()
        else:
            st.info('You haven\'t load any data till date, load data from Health Data section')
            main()
    except Exception as e:
        print(e)

def count_user_entries(uid):
    db = conn.connect(host=crd.host, user=crd.user, password=crd.pwd, database=crd.database)
    cur = db.cursor()
    query = "SELECT COUNT(*) FROM health_data WHERE uid = %s"
    cur.execute(query, (uid,))
    count = cur.fetchone()[0]  # Fetch the counted value
    db.close()
    return count

def count_today_user_entries(uid):
    db = conn.connect(host=crd.host, user=crd.user, password=crd.pwd, database=crd.database)
    cur = db.cursor()
    
    query = "SELECT COUNT(*) FROM health_data WHERE uid = %s AND record_date = %s"
    cur.execute(query, (uid,datetime.today().date()))
    count = cur.fetchone()[0]  # Fetch the counted value
    db.close()
    return count