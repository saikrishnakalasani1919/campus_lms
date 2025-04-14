from flask import Flask, render_template, request, redirect, url_for, flash, session,jsonify
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
        #cursor = mysql.connection.cursor()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM users WHERE email = %s AND role = %s", (username, role))
        user = cursor.fetchone()

        if user and check_password_hash(user['password'], password):
            # Set session variables
            session['user_id'] = user['user_id']
            session['username'] = user['email']
            session['email'] = user['email']  # Store the email in session
            session['full_name'] = user['full_name']
            session['role'] = user['role']

            flash(f"Welcome, {user['full_name']}!", "success")

            # Redirect based on the role
            if role == 'student':
                return redirect(url_for('student_dashboard'))
            elif role == 'faculty':
                return redirect(url_for('faculty_dashboard'))
            elif role == 'admin':
                return redirect(url_for('admin_dashboard'))
        else:
            flash("Invalid credentials", "danger")
            return redirect(url_for('login'))  # Redirect back to login if invalid

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        full_name = request.form['full_name']
        gender = request.form['gender']
        email = request.form['email']
        country_code = request.form['country_code']
        phone_no = request.form['phone_no']
        institute_name = request.form['institute_name']  # new field
        role = request.form['role']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash("Passwords do not match.", 'danger')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password)

        try:
            cursor.execute("""
                INSERT INTO users (full_name, gender, email, country_code, phone_no, institute_name, role, password)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (full_name, gender, email, country_code, phone_no, institute_name, role, hashed_password))
            conn.commit()
            flash("Registration successful! Please log in.", 'success')
            return redirect(url_for('login'))
        except mysql.connector.Error as err:
            flash(f"Error: {err}", 'danger')
            return redirect(url_for('register'))

    return render_template('register.html')

@app.route('/student-dashboard')
def student_dashboard():
    if 'user_id' not in session:
        flash("Please log in first", "warning")
        return redirect(url_for('login'))
    
    return render_template("student_dashboard.html",
                           first_name=session.get('full_name'),
                           username=session.get('username'),
                           role=session.get('role'))


# @app.route('/faculty-dashboard')
# def faculty_dashboard():
#     return render_template("faculty_dashboard.html",
#                            name=session.get('full_name'),
#                            classes_handled=3,
#                            assignments_created=12,
#                            student_feedback=4.5)

@app.route('/faculty-dashboard')
def faculty_dashboard():
    if 'user_id' not in session or session.get('role') != 'faculty':
        flash("Login required", "danger")
        return redirect(url_for('login'))

    faculty_email = session['email']
    
    cursor.execute("SELECT COUNT(*) as course_count FROM courses WHERE faculty_email = %s", (faculty_email,))
    classes_handled = cursor.fetchone()['course_count']

    return render_template("faculty_dashboard.html",
                           name=session.get('full_name'),
                           classes_handled=classes_handled,
                           assignments_created=12,  # Replace with real data later
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


# @app.route('/mycourses')
# def mycourses():
#     # Example static course data — replace with database fetch if needed later
#     courses = [
#         {"name": "Data Structures", "desc": "Arrays, Linked Lists, Trees", "progress": 70},
#         {"name": "Full Stack Web Dev", "desc": "React, Flask, MySQL", "progress": 40},
#         {"name": "Machine Learning", "desc": "Supervised & Unsupervised Learning", "progress": 55},
#         {"name": "Communication Skills", "desc": "English & Soft Skills Training", "progress": 90},
#     ]
#     return render_template("mycourses.html", courses=courses)

@app.route('/assignments')
def assignments():
    if 'user_id' not in session or session.get('role') != 'faculty':
        flash("Access denied. Faculty login required.", "danger")
        return redirect(url_for('login'))
    return render_template("assignments.html")

# @app.route('/managecourse')
# def managecourse():
#     if 'user_id' not in session or session.get('role') != 'faculty':
#         flash("Access denied. Faculty login required.", "danger")
#         return redirect(url_for('login'))
#     return render_template("managecourse.html")
@app.route('/managecourse', methods=['GET'])
def managecourse():
    if 'user_id' not in session or session.get('role') != 'faculty':
        flash("Access denied. Faculty login required.", "danger")
        return redirect(url_for('login'))

    faculty_email = session['email']
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT course_name, course_code, semester FROM courses WHERE faculty_email = %s", (faculty_email,))
    courses = cursor.fetchall()

    return render_template("managecourse.html", courses=courses)

@app.route('/add_course', methods=['POST'])
def add_course():
    #if 'email' not in session:
    if 'email' not in session or session.get('role') != 'faculty':
        return redirect(url_for('login'))

    course_name = request.form['course_name']
    course_code = request.form['course_code']
    semester = request.form['semester']
    faculty_email = session['email']

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT institute_name FROM users WHERE email=%s", (faculty_email,))
    institute = cursor.fetchone()
    institute_name = institute['institute_name'] if institute else ''

    cursor.execute(
        "INSERT INTO courses (course_name, course_code, semester, faculty_email, institute_name) VALUES (%s, %s, %s, %s, %s)",
        (course_name, course_code, semester, faculty_email, institute_name)
    )
    conn.commit()
    flash("Course added successfully!", "success")
    return redirect('/managecourse')
 
@app.route('/mycourses')
def my_courses():
    if 'email' not in session:
        return redirect(url_for('login'))

    user_email = session['email']
    cursor = conn.cursor(dictionary=True)

    # Get student's institute name
    cursor.execute("SELECT institute_name FROM users WHERE email = %s", (user_email,))
    institute = cursor.fetchone()
    
    if institute:
        institute_name = institute['institute_name']
        cursor.execute("SELECT course_name, course_code, semester FROM courses WHERE institute_name = %s", (institute_name,))
        courses = cursor.fetchall()
    else:
        courses = []

    return render_template('mycourses.html', courses=courses)




@app.route('/uploadcourses')
def uploadcourses():
    if 'user_id' not in session or session.get('role') != 'faculty':
        flash("Access denied. Faculty login required.", "danger")
        return redirect(url_for('login'))
    return render_template("uploadcourses.html")

@app.route('/analytics')
def analytics():
    if 'user_id' not in session or session.get('role') != 'student':
        flash("Access denied. Faculty login required.", "danger")
        return redirect(url_for('login'))
    return render_template("analytics.html")

# @app.route('/coding')
# def coding():
#     if 'user_id' not in session or session.get('role') != 'student':
#         flash("Access denied. Faculty login required.", "danger")
#         return redirect(url_for('login'))
#     return render_template("coding.html")


@app.route("/coding")
def coding():
    if 'user_id' not in session:
        return redirect(url_for('login'))  # protect route
    return render_template("coding.html")

@app.route("/save_code", methods=["POST"])
def save_code():
    if 'user_id' not in session:
        return jsonify({"status": "error", "message": "Login required"}), 401
    
    data = request.json
    user_id = session['user_id']
    language = data['language']
    code = data['code']

    cursor.execute("INSERT INTO code_submissions (user_id, language, code) VALUES (%s, %s, %s)",
                   (user_id, language, code))
    conn.commit()

    return jsonify({"status": "success", "message": "Code saved!"})
# @app.route('/faculty_dashboard')
# def faculty_dashboard():
#     faculty_email = session['email']
#     # cursor = mysql.connection.cursor()
#     cursor = conn.cursor(dictionary=True)

#     cursor.execute("SELECT course_name, course_code, semester FROM courses WHERE faculty_email = %s", (faculty_email,))
#     courses = cursor.fetchall()
#     return render_template('managecourse.html', courses=courses)
@app.route('/delete_course/<course_code>', methods=['POST'])
def delete_course(course_code):
    if 'email' not in session:
        return redirect(url_for('login'))
    faculty_email = session['email']
    cursor.execute("DELETE FROM courses WHERE course_code = %s AND faculty_email = %s", (course_code, faculty_email))
    conn.commit()
    flash("Course deleted.", "info")
    return redirect(url_for('managecourse'))
 

@app.route("/attendence")
def attendence():
    if 'user_id' not in session:
        return redirect(url_for('login'))  # protect route
    return render_template("attendence.html")


@app.route("/codetask")
def codetask():
    if 'user_id' not in session:
        return redirect(url_for('login'))  # protect route
    return render_template("codetask.html")

@app.route("/ai")
def ai():
    if 'user_id' not in session:
        return redirect(url_for('login'))  # protect route
    return render_template("ai.html")


# Show topics for selected course
@app.route("/course/<int:course_id>")
def view_course(course_id):
    topics = fetch_topics(course_id)  # Fetch from course_topics
    progress = fetch_student_progress(session['user_id'], course_id)  # Join to know which topics are done
    return render_template("course_view.html", topics=topics, progress=progress)

# AJAX route to update progress
@app.route("/update_progress", methods=["POST"])
def update_progress():
    data = request.json
    student_id = session['user_id']
    topic_id = data['topic_id']
    completed = data['completed']

    # insert or update progress
    update_topic_progress(student_id, topic_id, completed)
    return jsonify({"status": "success"})


if __name__ == '__main__':
    app.run(debug=True)
