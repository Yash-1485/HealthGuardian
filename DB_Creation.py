import DB_Creadentials as crd
import mysql.connector as conn
def db_creation():
    try:
        db=conn.connect(host=crd.host,user=crd.user,password=crd.pwd)
        cur=db.cursor()
        create_db=f"CREATE DATABASE IF NOT EXISTS {crd.database}"
        cur.execute(create_db)
        create_tables=[f"""
        CREATE TABLE IF NOT EXISTS user(
            uid INT PRIMARY KEY,        
            name VARCHAR(100) NOT NULL,         
            age INT NOT NULL,                   
            gender ENUM('Male', 'Female', 'Other') NOT NULL,
            birthdate DATE NOT NULL,            
            blood_group VARCHAR(5) NOT NULL,    
            height DECIMAL(5,2) NOT NULL,       
            email VARCHAR(255) UNIQUE NOT NULL, 
            password VARCHAR(255) NOT NULL 
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS health_data(
            id INT AUTO_INCREMENT PRIMARY KEY,
            uid INT NOT NULL,         
            record_date DATE NOT NULL,        
            bp_systolic INT NOT NULL,         
            bp_diastolic INT NOT NULL,        
            heartbeat INT NOT NULL,           
            sugar DECIMAL(5,2) NOT NULL,      
            oxygen INT NOT NULL,              
            weight DECIMAL(5,2) NOT NULL,     
            temperature DECIMAL(4,2) NOT NULL,
            bmi DECIMAL(5,2) NOT NULL,        
            FOREIGN KEY (uid) REFERENCES user(uid) ON DELETE CASCADE
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS goals (
            id INT AUTO_INCREMENT PRIMARY KEY,
            uid INT,
            date DATE,
            goals JSON,
            completed BOOLEAN DEFAULT FALSE,
            FOREIGN KEY (uid) REFERENCES user(uid)
        );
        """
        ]
        db.database=crd.database
        for table in create_tables:
            cur.execute(table)
        db.commit()
        db.close()
    except Exception as e:
        print(e)
        
# CREATE TABLE IF NOT EXISTS goals (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     uid INT NOT NULL,
#     date DATE NOT NULL,
#     goals JSON,
#     custom_activities JSON,
#     completed BOOLEAN DEFAULT FALSE,
#     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#     updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
#     FOREIGN KEY (uid) REFERENCES user(uid) ON DELETE CASCADE
# );