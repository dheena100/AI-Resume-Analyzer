````md
# 🚀 AI Resume Analyzer & Job Matcher

A premium AI-powered Resume Analyzer web application built using Flask, Python, MySQL, Bootstrap, and Chart.js.

This project helps users:
- Upload resumes
- Extract skills automatically
- Analyze resume score
- Match jobs based on skills
- View resume history
- Get career insights

---

# 📌 Features

✅ User Authentication (Register/Login)

✅ Secure Password Hashing

✅ Resume PDF Upload

✅ Automatic Skill Extraction

✅ AI Resume Score Analysis

✅ Job Matching System

✅ Resume History Tracking

✅ Premium Dashboard UI

✅ Interactive Charts & Visualizations

✅ Responsive Design

✅ Cloud Deployment Ready

---

# 🛠️ Tech Stack

## Frontend
- HTML5
- CSS3
- Bootstrap 5
- JavaScript
- Chart.js

## Backend
- Python
- Flask

## Database
- MySQL

## Libraries Used
- flask-mysqldb
- pdfplumber
- werkzeug
- python-dotenv
- gunicorn

---

# 📂 Project Structure

```bash
AI_Resume_Analyzer/
│
├── static/
│   ├── css/
│   ├── uploads/
│
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── upload_resume.html
│   ├── result.html
│   ├── resume_history.html
│
├── app.py
├── requirements.txt
├── Procfile
├── .env
├── README.md
└── .gitignore
````

---

# ⚙️ Installation

## Clone Repository

```bash
git clone https://github.com/dheena100/AI-Resume-Analyzer.git
```

## Move Into Project

```bash
cd AI-Resume-Analyzer
```

## Create Virtual Environment

```bash
python -m venv venv
```

## Activate Virtual Environment

### Windows

```bash
venv\Scripts\activate
```

### Mac/Linux

```bash
source venv/bin/activate
```

---

# 📦 Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔐 Environment Variables

Create a `.env` file and add:

```env
SECRET_KEY=your_secret_key

MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DB=ai_resume_analyzer
MYSQL_PORT=3306
```

---

# 🗄️ Database Setup

Create database:

```sql
CREATE DATABASE ai_resume_analyzer;
```

### Users Table

```sql
CREATE TABLE users(
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    password TEXT
);
```

### Resumes Table

```sql
CREATE TABLE resumes(
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    resume_file VARCHAR(255),
    extracted_skills TEXT,
    resume_score INT,
    FOREIGN KEY(user_id)
    REFERENCES users(id)
    ON DELETE CASCADE
);
```

### Jobs Table

```sql
CREATE TABLE jobs(
    id INT AUTO_INCREMENT PRIMARY KEY,
    job_title VARCHAR(100),
    company_name VARCHAR(100),
    skills_required TEXT
);
```

---

# ▶️ Run Project

```bash
python app.py
```

Visit:

```bash
http://127.0.0.1:5000
```

---

# 🌐 Deployment

This project is deployment-ready using:

* Render
* Railway
* Heroku

Production server:

```bash
gunicorn app:app
```

---

# 📸 Screenshots

## Home Page

Premium landing page with animations and modern UI.

## Dashboard

AI-powered analytics dashboard.

## Resume Analysis

Interactive skill visualization using Chart.js.

## Resume History

Track all uploaded resumes and scores.

---

# 🔥 Future Enhancements

* AI Resume Suggestions
* ATS Score Checker
* OpenAI/Gemini Integration
* Resume PDF Report Generation
* Admin Dashboard
* Email Notifications
* Docker Deployment
* JWT Authentication

---

# 👨‍💻 Developer

## DHEENA G

B.Tech CSBS Graduate (2025)

Python Full Stack Developer

---

# ⭐ Support

If you like this project:

⭐ Star the repository

⭐ Share on LinkedIn

⭐ Fork the project

---

# 📄 License

This project is open-source and free to use.

```
```
