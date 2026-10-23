 # PlacePrep — Placement Interview Preparation System

A full-stack web app for campus placement practice: **aptitude quizzes**, **coding exercises**, **mock interview questions**, and **progress tracking**.

**Stack:** Python · Flask · HTML/CSS/JavaScript · MySQL

---

## Features

| Module | What it does |
|--------|----------------|
| **Aptitude** | MCQs in Quantitative, Logical, Verbal with scoring & explanations |
| **Coding** | Python problems with sample I/O and automated test-case judging |
| **Mock Interview** | HR / Behavioral / Technical Qs with model answers & self-rating |
| **Progress** | Dashboard + full history of attempts and averages |
| **Auth** | Register / login (password hashed with Werkzeug) |

---

## Prerequisites

- Python 3.10+
- MySQL Server 8.x (or 5.7+)
- pip

---

## Setup

### 1. Database

**Option A — MySQL (recommended for final submission)**

```sql
CREATE DATABASE placement_prep CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

In `.env` set `DB_ENGINE=mysql` and your MySQL password.

**Option B — SQLite (quick demo, no MySQL install)**

In `.env` set:

```
DB_ENGINE=sqlite
```

### 2. Configure environment

Copy `.env.example` to `.env` and edit:

```
SECRET_KEY=any-random-string
DB_ENGINE=mysql
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=placement_prep
```

### 3. Install dependencies

```bash
cd chumma2
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate

pip install -r requirements.txt
```

### 4. Run the app

```bash
python app.py
```

Open **http://127.0.0.1:5000**

On first run the app creates tables and seeds sample questions automatically.

---

## Demo walkthrough

1. **Register** a student account  
2. **Dashboard** — see empty stats, then use quick links  
3. **Aptitude** → pick Quantitative / Logical / Verbal → submit → view score  
4. **Coding** → open “Sum of Two Numbers” → write:

   ```python
   a, b = map(int, input().split())
   print(a + b)
   ```

   → Run tests  
5. **Interview** → answer a question → rate yourself → read model answer  
6. **Progress** — review all history  

---

## Project structure

```
chumma2/
├── app.py              # Flask routes & coding judge
├── config.py           # MySQL / secret config
├── models.py           # SQLAlchemy models
├── seed_data.py        # Sample aptitude/coding/interview data
├── schema.sql          # Database creation script
├── requirements.txt
├── .env / .env.example
├── static/
│   ├── css/style.css
│   └── js/main.js
└── templates/          # Jinja2 HTML pages
```

---

## Database tables

- `users` — accounts  
- `aptitude_questions` / `aptitude_attempts`  
- `coding_problems` / `coding_attempts`  
- `interview_questions` / `interview_attempts`  

---

## Notes for viva / report

- **Flask** handles routing, sessions (Flask-Login), and templates.  
- **MySQL** stores users, questions, and attempt history via SQLAlchemy.  
- **Coding judge** runs student Python against stored test inputs (local sandbox; blocks unsafe imports).  
- **Progress** uses aggregates (`AVG`, `COUNT`) for dashboard metrics.  

---

## License

Academic / educational use.
