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
        db.close()

        return pd.DataFrame(data) if data else None

    except Exception as e:
        print(f"Error fetching data: {e}")
        return None
