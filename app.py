from flask import Flask, render_template, request, redirect, flash, url_for, session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'S3cr3tK3y_2025$!'

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Sendhan@2005",
    database="student_management_system"
)
mycursor = mydb.cursor(dictionary=False)

@app.route('/studentmainpage', methods=['POST'])
def student_main():
    username = request.form.get('Username')
    password = request.form.get('Password')

    print(f"Received Username: {username}, Password: {password}")

    mycursor.execute("SELECT * FROM student_login_details WHERE Username=%s AND Password=%s", (username, password))
    user = mycursor.fetchone()

    print("Query Result:", user)

    if user:
        session['username'] = username
        return redirect(url_for('gotostudentmainpage'))
    else:
        flash("Invalid Username or Password", "danger")
        return redirect(url_for('studentlogin')), 401

@app.route('/gotostudentmainpage', methods=['GET'])
def gotostudentmainpage():
    username = session.get('username')

    if not username:
        flash("Session expired. Please log in again.", "danger")
        return redirect(url_for('studentlogin'))

    mycursor.execute("SELECT * FROM STUDENT_DETAILS WHERE Username=%s", (username,))
    user = mycursor.fetchone()

    if user:
        id, fname, lname, dob, email = user[:5]  # Unpack tuple
        valuesdata = [id, fname, lname, dob, email]
        return render_template('Student Main Page.html', values=valuesdata)
    else:
        flash("User not found!", "danger")
        return redirect(url_for('studentlogin'))

@app.route('/')
def index():
    return render_template('HomePage.html')

@app.route('/studentlogin')
def studentlogin():
    return render_template('LoginPage.html')

@app.route('/student_portal', methods=['POST'])
def student_portal():
    username = request.form.get('username')
    password = request.form.get('password')

    sql = "SELECT * FROM STUDENT_LOGIN_DETAILS WHERE USERNAME = %s AND PASSWORD = %s"
    mycursor.execute(sql, (username, password))
    myresult = mycursor.fetchone()

    if myresult:
        return render_template('Student Main Page.html')
    else:
        return "Invalid Student Credentials!"

@app.route('/admin')
def admin():
    return render_template('AdminLogin.html')

@app.route('/Stusignup')
def Stusignup():
    return render_template('SignUpPage.html')

@app.route('/StudentSignUp', methods=['POST'])
def StudentSignUp():
    regno = request.form.get('registration_number')
    fname = request.form.get('firstname')
    lastname = request.form.get('lastname')
    dob = request.form.get('dob')
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')

    sqlstudentinfo = "INSERT INTO STUDENT_DETAILS (REGNO, FNAME, LNAME, DOB, EMAIL, USERNAME, PASSWORD) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    mycursor.execute(sqlstudentinfo, (regno, fname, lastname, dob, email, username, password))
    mydb.commit()

    sqlstudentlogininfo = "INSERT INTO STUDENT_LOGIN_DETAILS (USERNAME, PASSWORD) VALUES (%s, %s)"
    mycursor.execute(sqlstudentlogininfo, (username, password))
    mydb.commit()

    flash("Signup Successful!", "success")
    return render_template('returnfromsignupadminhome.html')

@app.route('/returnfromadminstudentdata')
def returnfromadminstudentdata():
    return render_template('Admin Page.html')

@app.route('/viewdata')
def viewdata():
    sql = "SELECT * FROM STUDENT_DETAILS"
    mycursor.execute(sql)
    students = mycursor.fetchall()
    return render_template('dataofmultiplestudenttoadmin.html', students=students)

@app.route('/adminlogin', methods=['POST'])
def adminlogin():
    username = request.form.get('Username')
    password = request.form.get('Password')

    sql = "SELECT * FROM ADMIN_LOGIN_DETAILS WHERE username=%s AND password=%s"
    mycursor.execute(sql, (username, password))
    result = mycursor.fetchone()

    if result:
        return render_template('Admin Page.html')
    else:
        return "Invalid Admin Credentials!"

if __name__ == '__main__':
    app.run(debug=True)