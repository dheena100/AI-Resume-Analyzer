from flask import Flask, render_template, request, redirect, session, flash
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import os
import pdfplumber

app = Flask(__name__)

# ==============================
# SECRET KEY
# ==============================
app.secret_key = "f334c46eada7c82d797aad8227e708b1"


# ==============================
# MYSQL CONFIGURATION
# ==============================
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'DheenaGopinath@2114'
app.config['MYSQL_DB'] = 'ai_resume_analyzer'

mysql = MySQL(app)


# ==============================
# UPLOAD FOLDER CONFIGURATION
# ==============================
UPLOAD_FOLDER = 'static/uploads'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create upload folder automatically if not exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ==============================
# HOME PAGE
# ==============================
@app.route('/')
def home():
    return render_template('index.html')


# ==============================
# REGISTER
# ==============================
@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        # HASH PASSWORD
        hashed_password = generate_password_hash(password)

        cur = mysql.connection.cursor()

        # Check email already exists
        cur.execute(
            "SELECT * FROM users WHERE email = %s",
            (email,)
        )

        existing_user = cur.fetchone()

        if existing_user:
            flash("Email already exists!")
            return redirect('/register')

        # Insert user
        cur.execute(
            "INSERT INTO users(name, email, password) VALUES(%s, %s, %s)",
            (name, email, hashed_password)
        )

        mysql.connection.commit()
        cur.close()

        flash("Registration Successful!")

        return redirect('/login')

    return render_template('register.html')


# ==============================
# LOGIN
# ==============================
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        cur = mysql.connection.cursor()

        # Get user by email
        cur.execute(
            "SELECT * FROM users WHERE email = %s",
            (email,)
        )

        user = cur.fetchone()

        cur.close()

        # VERIFY PASSWORD
        if user and check_password_hash(user[3], password):

            session['loggedin'] = True
            session['user_id'] = user[0]
            session['name'] = user[1]

            flash("Login Successful!")

            return redirect('/dashboard')

        else:
            flash("Invalid Email or Password")

    return render_template('login.html')


# ==============================
# DASHBOARD
# ==============================
@app.route('/dashboard')
def dashboard():

    if 'loggedin' in session:
        return render_template(
            'dashboard.html',
            name=session['name']
        )

    return redirect('/login')


# ==============================
# LOGOUT
# ==============================
@app.route('/logout')
def logout():

    session.clear()

    flash("Logged Out Successfully!")

    return redirect('/login')


# ==============================
# RESUME UPLOAD
# ==============================
@app.route('/upload_resume', methods=['GET', 'POST'])
def upload_resume():

    if 'loggedin' not in session:
        return redirect('/login')

    if request.method == 'POST':

        file = request.files['resume']

        if file.filename == '':
            flash("Please select a file")
            return redirect('/upload_resume')

        filename = secure_filename(file.filename)

        filepath = os.path.join(
            app.config['UPLOAD_FOLDER'],
            filename
        )

        file.save(filepath)

        # Extract text from PDF
        extracted_text = extract_text(filepath)

        # Extract skills
        extracted_skills = extract_skills(extracted_text)

        # Resume score
        resume_score = len(extracted_skills) * 10

        # Match jobs
        matched_jobs = match_jobs(extracted_skills)

        # Convert skills list to string
        skills_string = ", ".join(extracted_skills)

        # Save to database
        cur = mysql.connection.cursor()

        cur.execute(
            """
            INSERT INTO resumes
            (user_id, resume_file, extracted_skills, resume_score)
            VALUES(%s, %s, %s, %s)
            """,
            (
                session['user_id'],
                filename,
                skills_string,
                resume_score
            )
        )

        mysql.connection.commit()
        cur.close()

        return render_template(
            'result.html',
            skills=extracted_skills,
            score=resume_score,
            jobs=matched_jobs
        )

    return render_template('upload_resume.html')


# ==============================
# PDF TEXT EXTRACTION
# ==============================
def extract_text(pdf_path):

    text = ""

    with pdfplumber.open(pdf_path) as pdf:

        for page in pdf.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text

    return text


# ==============================
# SKILL EXTRACTION
# ==============================
def extract_skills(text):

    skills_list = [
        "Python",
        "Flask",
        "Django",
        "MySQL",
        "Java",
        "JavaScript",
        "HTML",
        "CSS",
        "React",
        "Git",
        "GitHub",
        "API",
        "Machine Learning"
    ]

    found_skills = []

    for skill in skills_list:

        if skill.lower() in text.lower():
            found_skills.append(skill)

    return found_skills


def match_jobs(user_skills):

    cur = mysql.connection.cursor()

    cur.execute("SELECT * FROM jobs")

    jobs = cur.fetchall()

    cur.close()

    matched_jobs = []

    for job in jobs:

        job_skills = job[3].split(',')

        match_count = 0

        for skill in user_skills:

            for js in job_skills:

                if skill.lower().strip() == js.lower().strip():
                    match_count += 1

        if match_count > 0:

            matched_jobs.append({
                'job_title': job[1],
                'company_name': job[2],
                'match_count': match_count
            })

    return matched_jobs

# ==============================
# RESUME HISTORY
# ==============================
@app.route('/resume_history')
def resume_history():

    if 'loggedin' not in session:
        return redirect('/login')

    cur = mysql.connection.cursor()

    cur.execute(
        """
        SELECT resume_file,
               extracted_skills,
               resume_score
        FROM resumes
        WHERE user_id = %s
        ORDER BY id DESC
        """,
        (session['user_id'],)
    )

    resumes = cur.fetchall()

    cur.close()

    return render_template(
        'resume_history.html',
        resumes=resumes
    )


# ==============================
# MAIN
# ==============================
if __name__ == '__main__':
    app.run(debug=True)