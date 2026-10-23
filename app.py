import io
import sys
import traceback
from contextlib import redirect_stdout

from flask import Flask, flash, redirect, render_template, request, url_for
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from sqlalchemy import func

from config import Config
from models import (
    AptitudeAttempt,
    AptitudeQuestion,
    CodingAttempt,
    CodingProblem,
    InterviewAttempt,
    InterviewQuestion,
    User,
    db,
)
from seed_data import seed_all

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


def run_python_code(code: str, stdin_data: str) -> tuple[bool, str]:
    """Execute user code safely for educational sandbox (local only)."""
    if any(bad in code for bad in ("import os", "import sys", "open(", "__import__", "exec(", "eval(", "subprocess")):
        return False, "Unsafe code detected. Avoid system imports and file access."

    old_stdin = sys.stdin
    try:
        sys.stdin = io.StringIO(stdin_data)
        buf = io.StringIO()
        with redirect_stdout(buf):
            exec(code, {"__builtins__": __builtins__})
        return True, buf.getvalue().strip()
    except Exception:
        return False, traceback.format_exc(limit=1).strip().split("\n")[-1]
    finally:
        sys.stdin = old_stdin


def judge_coding(problem: CodingProblem, code: str) -> tuple[bool, str]:
    inputs = problem.test_input.strip().split("\n")
    expected = problem.test_output.strip().split("\n")
    if len(inputs) != len(expected):
        return False, "Test data misconfigured."

    for i, (inp, exp) in enumerate(zip(inputs, expected), start=1):
        ok, out = run_python_code(code, inp)
        if not ok:
            return False, f"Runtime error on test {i}: {out}"
        if out.strip() != exp.strip():
            return False, f"Failed test {i}. Expected '{exp}', got '{out}'."
    return True, f"All {len(inputs)} test cases passed!"


@app.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        if not name or not email or not password:
            flash("All fields are required.", "error")
            return render_template("register.html")
        if User.query.filter_by(email=email).first():
            flash("Email already registered.", "error")
            return render_template("register.html")
        user = User(name=name, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash("Account created. Please log in.", "success")
        return redirect(url_for("login"))
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for("dashboard"))
        flash("Invalid email or password.", "error")
    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully.", "success")
    return redirect(url_for("index"))


@app.route("/dashboard")
@login_required
def dashboard():
    apt_stats = (
        db.session.query(
            func.count(AptitudeAttempt.id),
            func.coalesce(func.avg(AptitudeAttempt.score * 100.0 / AptitudeAttempt.total), 0),
        )
        .filter_by(user_id=current_user.id)
        .first()
    )
    coding_solved = (
        CodingAttempt.query.filter_by(user_id=current_user.id, passed=True)
        .with_entities(CodingAttempt.problem_id)
        .distinct()
        .count()
    )
    coding_total = CodingProblem.query.count()
    interview_count = InterviewAttempt.query.filter_by(user_id=current_user.id).count()
    interview_avg = (
        db.session.query(func.coalesce(func.avg(InterviewAttempt.self_rating), 0))
        .filter_by(user_id=current_user.id)
        .scalar()
    )

    recent_apt = (
        AptitudeAttempt.query.filter_by(user_id=current_user.id)
        .order_by(AptitudeAttempt.created_at.desc())
        .limit(5)
        .all()
    )
    recent_code = (
        CodingAttempt.query.filter_by(user_id=current_user.id)
        .order_by(CodingAttempt.created_at.desc())
        .limit(5)
        .all()
    )

    return render_template(
        "dashboard.html",
        apt_attempts=apt_stats[0] or 0,
        apt_avg=round(float(apt_stats[1] or 0), 1),
        coding_solved=coding_solved,
        coding_total=coding_total,
        interview_count=interview_count,
        interview_avg=round(float(interview_avg or 0), 1),
        recent_apt=recent_apt,
        recent_code=recent_code,
    )


# ---------- Aptitude ----------
@app.route("/aptitude")
@login_required
def aptitude():
    categories = ["Quantitative", "Logical", "Verbal"]
    counts = {
        c: AptitudeQuestion.query.filter_by(category=c).count() for c in categories
    }
    return render_template("aptitude.html", categories=categories, counts=counts)


@app.route("/aptitude/<category>", methods=["GET", "POST"])
@login_required
def aptitude_quiz(category):
    questions = AptitudeQuestion.query.filter_by(category=category).all()
    if not questions:
        flash("No questions in this category yet.", "info")
        return redirect(url_for("aptitude"))

    if request.method == "POST":
        score = 0
        results = []
        for q in questions:
            selected = request.form.get(f"q_{q.id}", "")
            correct = selected.upper() == q.correct_option.upper()
            if correct:
                score += 1
            results.append({"question": q, "selected": selected, "correct": correct})
        attempt = AptitudeAttempt(
            user_id=current_user.id,
            category=category,
            score=score,
            total=len(questions),
        )
        db.session.add(attempt)
        db.session.commit()
        return render_template(
            "aptitude_result.html",
            category=category,
            score=score,
            total=len(questions),
            results=results,
        )

    return render_template("aptitude_quiz.html", category=category, questions=questions)


# ---------- Coding ----------
@app.route("/coding")
@login_required
def coding():
    problems = CodingProblem.query.order_by(CodingProblem.id).all()
    solved_ids = {
        a.problem_id
        for a in CodingAttempt.query.filter_by(user_id=current_user.id, passed=True).all()
    }
    return render_template("coding.html", problems=problems, solved_ids=solved_ids)


@app.route("/coding/<int:problem_id>", methods=["GET", "POST"])
@login_required
def coding_solve(problem_id):
    problem = CodingProblem.query.get_or_404(problem_id)
    result_message = None
    passed = None
    code = problem.starter_code or ""

    if request.method == "POST":
        code = request.form.get("code", "")
        passed, result_message = judge_coding(problem, code)
        attempt = CodingAttempt(
            user_id=current_user.id,
            problem_id=problem.id,
            code=code,
            passed=passed,
            result_message=result_message,
        )
        db.session.add(attempt)
        db.session.commit()

    return render_template(
        "coding_solve.html",
        problem=problem,
        code=code,
        result_message=result_message,
        passed=passed,
    )


# ---------- Mock Interview ----------
@app.route("/interview")
@login_required
def interview():
    categories = ["HR", "Behavioral", "Technical"]
    questions = InterviewQuestion.query.order_by(InterviewQuestion.category).all()
    return render_template("interview.html", categories=categories, questions=questions)


@app.route("/interview/<int:question_id>", methods=["GET", "POST"])
@login_required
def interview_practice(question_id):
    question = InterviewQuestion.query.get_or_404(question_id)
    show_feedback = False
    user_answer = ""
    rating = 3

    if request.method == "POST":
        user_answer = request.form.get("answer", "").strip()
        rating = int(request.form.get("rating", 3))
        if not user_answer:
            flash("Please write your answer before submitting.", "error")
        else:
            attempt = InterviewAttempt(
                user_id=current_user.id,
                question_id=question.id,
                user_answer=user_answer,
                self_rating=rating,
            )
            db.session.add(attempt)
            db.session.commit()
            show_feedback = True
            flash("Answer saved. Compare with the model answer below.", "success")

    return render_template(
        "interview_practice.html",
        question=question,
        show_feedback=show_feedback,
        user_answer=user_answer,
        rating=rating,
    )


# ---------- Progress ----------
@app.route("/progress")
@login_required
def progress():
    apt_by_cat = (
        db.session.query(
            AptitudeAttempt.category,
            func.count(AptitudeAttempt.id),
            func.avg(AptitudeAttempt.score * 100.0 / AptitudeAttempt.total),
        )
        .filter_by(user_id=current_user.id)
        .group_by(AptitudeAttempt.category)
        .all()
    )
    all_apt = (
        AptitudeAttempt.query.filter_by(user_id=current_user.id)
        .order_by(AptitudeAttempt.created_at.desc())
        .all()
    )
    all_code = (
        CodingAttempt.query.filter_by(user_id=current_user.id)
        .order_by(CodingAttempt.created_at.desc())
        .all()
    )
    all_interview = (
        InterviewAttempt.query.filter_by(user_id=current_user.id)
        .order_by(InterviewAttempt.created_at.desc())
        .all()
    )
    return render_template(
        "progress.html",
        apt_by_cat=apt_by_cat,
        all_apt=all_apt,
        all_code=all_code,
        all_interview=all_interview,
    )


def create_app_tables():
    with app.app_context():
        db.create_all()
        seed_all()


if __name__ == "__main__":
    create_app_tables()
    app.run(debug=True, port=5000)
