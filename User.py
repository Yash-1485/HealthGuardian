import DB_Creadentials as crd
import mysql.connector as conn

class User:
    def __init__(self, name, age, gender, birthdate, blood_group, height, email, password):
        self.uid = getuid()  # Unique User ID
        self.name = name
        self.age = age
        self.gender = gender
        self.birthdate = birthdate
        self.blood_group = blood_group
        self.height = height  # Height in meters
        self.email = email
        self.pwd = password  # Store hashed password
        self.health_data = {}  # Dictionary to store daily health metrics
        
    # Getters
    def get_uid(self):
        return self.uid

    def get_name(self):
        return self.name

    def get_age(self):
        return self.age

    def get_gender(self):
        return self.gender

    def get_birthdate(self):
        return self.birthdate

    def get_blood_group(self):
        return self.blood_group

    def get_height(self):
        return self.height

    def get_email(self):
        return self.email

    def get_health_data(self, date):
        return self.health_data.get(date, "No data available")

    # Setters
    def set_name(self, name):
        self.name = name

    def set_age(self, age):
        self.age = age

    def set_gender(self, gender):
        self.gender = gender

    def set_birthdate(self, birthdate):
        self.birthdate = birthdate

    def set_blood_group(self, blood_group):
        self.blood_group = blood_group

    def set_height(self, height):
        self.height = height

    def set_email(self, email):
        self.email = email

    def set_password(self, password):
        self.pwd = password

    # Method to add a new daily health record
    def add_health_record(self, date, bp, heartbeat, sugar, oxygen, weight, temperature):
        bmi = self.calculate_bmi(weight)
        self.health_data[date] = {
            "bp": bp,  
            "heartbeat": heartbeat,
            "sugar": sugar,
            "oxygen": oxygen,
            "weight": weight,
            "temperature": temperature,
            "bmi": bmi
        }

    # Method to update an existing health record
    def update_health_record(self, date, bp=None, heartbeat=None, sugar=None, oxygen=None, weight=None, temperature=None):
        if date in self.health_data:
            if bp is not None:
                self.health_data[date]["bp"].append(bp)
            if heartbeat is not None:
                self.health_data[date]["heartbeat"].append(heartbeat)
            if sugar is not None:
                self.health_data[date]["sugar"].append(sugar)
            if oxygen is not None:
                self.health_data[date]["oxygen"].append(oxygen)
            if weight is not None:
                self.health_data[date]["weight"].append(weight)
                self.health_data[date]["bmi"] = self.calculate_bmi(weight)  # Recalculate BMI
            if temperature is not None:
                self.health_data[date]["temperature"].append(temperature)
        else:
            print(f"No record found for {date}")

    # BMI Calculation
    def calculate_bmi(self, weight):
        return round(weight / (self.height ** 2), 2)  # BMI formula: weight (kg) / height^2 (m^2)

    # Provide diet recommendation based on BMI
    def get_diet_recommendation(self, bmi):
        if bmi < 18.5:
            return "Underweight: Increase calorie intake with protein-rich foods."
        elif 18.5 <= bmi < 24.9:
            return "Normal: Maintain a balanced diet with proteins, carbs, and fats."
        elif 25 <= bmi < 29.9:
            return "Overweight: Reduce sugar intake and increase physical activity."
        else:
            return "Obese: Consult a dietitian for a strict diet plan."
    
def getuid():
    db=conn.connect(host=crd.host,user=crd.user,password=crd.pwd,database=crd.database)
    cursor=db.cursor()
    query = "SELECT * FROM HealthGuardian.USER ORDER BY uid DESC LIMIT 1"
    cursor.execute(query)

    # Fetching the last enered result
    last_entry = cursor.fetchone()
    if(cursor.rowcount!=0):
        print(last_entry[0])
        return last_entry[0]+1
    else:
        return 1

# # Example Usage:
# user = User("U001", "John Doe", 30, "Male", "1993-05-15", "O+", 1.75, "john@example.com", "securepassword")
# user.add_health_record("2025-02-15", [120, 80], [75], [90], [98], [70], [36.5])

# # Retrieve health data
# print(user.get_health_data("2025-02-15"))

# # Get BMI and diet suggestion
# bmi = user.calculate_bmi(70)  # Example weight in kg
# print(f"BMI: {bmi}, Diet Suggestion: {user.get_diet_recommendation(bmi)}")
