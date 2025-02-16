import mysql.connector as conn
import DB_Creadentials as crd
import pandas as pd
from datetime import datetime, timedelta

def fetch_health_data(user_id, period="daily"):
    try:
        db = conn.connect(host=crd.host, user=crd.user, password=crd.pwd, database=crd.database)
        cur = db.cursor(dictionary=True)

        today = datetime.today().date()

        if period == "daily":
            query = """SELECT * FROM health_data WHERE uid = %s AND record_date = %s"""
            cur.execute(query, (user_id, today))

        elif period == "weekly":
            start_date = today - timedelta(days=7)
            query = """SELECT * FROM health_data WHERE uid = %s AND record_date BETWEEN %s AND %s ORDER BY record_date"""
            cur.execute(query, (user_id, start_date, today))

        elif period == "monthly":
            start_date = today - timedelta(days=30)
            query = """SELECT * FROM health_data WHERE uid = %s AND record_date BETWEEN %s AND %s ORDER BY record_date"""
            cur.execute(query, (user_id, start_date, today))

        data = cur.fetchall()
        dummy_data=data.copy()
        record_dates=[]
        bp_systolic=[]
        bp_diastolic=[]
        heartbeat=[]
        sugar=[]
        oxygen=[]
        weight=[]
        temperature=[]
        bmi=[]
        # print(data,dummy_data)
        for inner_data in dummy_data:
            record_dates.append(inner_data['record_date'])
            bp_systolic.append(inner_data['bp_systolic'])
            bp_diastolic.append(inner_data['bp_diastolic'])
            heartbeat.append(inner_data['heartbeat'])
            sugar.append(inner_data['sugar'])
            oxygen.append(inner_data['oxygen'])
            weight.append(inner_data['weight'])
            temperature.append(inner_data['temperature'])
            bmi.append(inner_data['bmi'])
        # print(data,dummy_data)
        
        health_dictonary={
            'Record Dates:':record_dates,
            'Bp(Systolic)':bp_systolic,
            'Bp(Diastolic)':bp_diastolic,
            'Heartbeat':heartbeat,
            'Sugar':sugar,
            'Oxygen':oxygen,
            'Weight':weight,
            'Temprature':temperature,
            'BMI':bmi,
        }
        
        df=pd.DataFrame(health_dictonary)
        db.close()

        return pd.DataFrame(data) if data else None,df

    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

def generate_recommendations(df):
    if df is None or df.empty:
        return "No data available to generate recommendations."

    # Calculate average values
    avg_bp_systolic = df["Bp(Systolic)"].mean()
    avg_bp_diastolic = df["Bp(Diastolic)"].mean()
    avg_heartbeat = df["Heartbeat"].mean()
    avg_sugar = df["Sugar"].mean()
    avg_oxygen = df["Oxygen"].mean()
    avg_weight = df["Weight"].mean()
    avg_temperature = df["Temprature"].mean()
    avg_bmi = df["BMI"].mean()

    # Define normal ranges
    normal_ranges = {
        "bp_systolic": (90, 160),
        "bp_diastolic": (60, 100),
        "heartbeat": (60, 100),
        "sugar": (70, 160),
        "oxygen": (95, 100),
        "bmi": (18.5, 24.9)
    }

    recommendations = []
    avg_para=[(avg_bp_systolic,avg_bp_diastolic),avg_heartbeat,avg_sugar,avg_oxygen,avg_bmi,avg_temperature]
    # Blood Pressure
    if avg_bp_systolic > normal_ranges["bp_systolic"][1] or avg_bp_diastolic > normal_ranges["bp_diastolic"][1]:
        recommendations.append("High BP detected. Reduce salt intake and engage in light exercises.")
    elif avg_bp_systolic < normal_ranges["bp_systolic"][0] or avg_bp_diastolic < normal_ranges["bp_diastolic"][0]:
        recommendations.append("Low BP detected. Stay hydrated and increase salt intake moderately.")
    else:
        recommendations.append('BP is normal, not to worry.')

    # Heart Rate
    if avg_heartbeat > normal_ranges["heartbeat"][1]:
        recommendations.append("High heart rate detected. Reduce caffeine and stress levels.")
    elif avg_heartbeat < normal_ranges["heartbeat"][0]:
        recommendations.append("Low heart rate detected. Increase physical activity.")
    else:
        recommendations.append('Heartbeat is normal, not to worry.')

    # Sugar Levels
    if avg_sugar > normal_ranges["sugar"][1]:
        recommendations.append("High sugar levels detected. Reduce sugar intake and exercise more.")
    elif avg_sugar < normal_ranges["sugar"][0]:
        recommendations.append("Low sugar levels detected. Eat small frequent meals rich in protein.")
    else:
        recommendations.append('Sugar Level is normal, not to worry.')

    # Oxygen Levels
    if avg_oxygen < normal_ranges["oxygen"][0]:
        recommendations.append("Low oxygen levels detected. Practice breathing exercises and check for respiratory issues.")
    else:
        recommendations.append('Oxygen Level is normal, not to worry.')

    # BMI
    if avg_bmi > normal_ranges["bmi"][1]:
        recommendations.append("High BMI detected. Focus on a balanced diet and regular workouts.")
    elif avg_bmi < normal_ranges["bmi"][0]:
        recommendations.append("Low BMI detected. Increase calorie intake with healthy foods.")
    else:
        recommendations.append('BMI is normal, not to worry.')

    # Temperature
    if avg_temperature > 99.5:
        recommendations.append("High body temperature detected. Check for fever and stay hydrated.")
    else:
        recommendations.append('Temprature is normal, not to worry.')

    return recommendations,avg_para
