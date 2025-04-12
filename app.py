from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flashing messages

# MySQL connection setup (change as per your config)
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Krishna1919@',
    database='lms'
)
cursor = conn.cursor(dictionary=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']

        # Fetch user by email and role
        cursor.execute("SELECT * FROM users WHERE email = %s AND role = %s", (username, role))
        user = cursor.fetchone()

        if user and check_password_hash(user['password'], password):
            flash(f"Welcome, {user['full_name']}!", "success")

            # Redirect based on role with user passed to template
            if role == 'student':
                return render_template("student_dashboard.html", user=user)
            elif role == 'faculty':
                return render_template("faculty_dashboard.html", user=user)
            elif role == 'admin':
                return render_template("admin_dashboard.html", user=user)
        else:
            flash("Invalid credentials", "danger")
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        full_name = request.form['full_name']
        gender = request.form['gender']
        email = request.form['email']
        country_code = request.form['country_code']
        phone_no = request.form['phone_no']
        role = request.form['role']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash("Passwords do not match.", 'danger')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password)

        try:
            cursor.execute("""
                INSERT INTO users (full_name, gender, email, country_code, phone_no, role, password)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (full_name, gender, email, country_code, phone_no, role, hashed_password))
            conn.commit()
            flash("Registration successful! Please log in.", 'success')
            return redirect(url_for('login'))
        except mysql.connector.Error as err:
            flash(f"Error: {err}", 'danger')
            return redirect(url_for('register'))

    return render_template('register.html')

@app.route('/student-dashboard')
def student_dashboard():
    return render_template("student_dashboard.html",
                           name=session.get('full_name'),
                           courses_count=5,
                           problems_solved=42,
                           streak_days=6)

@app.route('/faculty-dashboard')
def faculty_dashboard():
    return render_template("faculty_dashboard.html",
                           name=session.get('full_name'),
                           classes_handled=3,
                           assignments_created=12,
                           student_feedback=4.5)

@app.route('/admin-dashboard')
def admin_dashboard():
    return render_template("admin_dashboard.html",
                           name=session.get('full_name'),
                           total_users=120,
                           active_courses=15,
                           reports_generated=18)

@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", 'info')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
