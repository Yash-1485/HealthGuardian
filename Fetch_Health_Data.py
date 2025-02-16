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
