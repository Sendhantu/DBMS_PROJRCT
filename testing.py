import mysql.connector

try:
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Sendhan@2005",
        database="student_management_system"
    )
    mycursor = mydb.cursor()
    mycursor.execute("select * from student_details")
    db_name = mycursor.fetchone()
    print(f"Connected to Database: {db_name[0]}")
except mysql.connector.Error as err:
    print(f"Error: {err}")
