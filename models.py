from datetime import datetime

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

db = SQLAlchemy()


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    aptitude_attempts = db.relationship("AptitudeAttempt", backref="user", lazy=True)
    coding_attempts = db.relationship("CodingAttempt", backref="user", lazy=True)
    interview_attempts = db.relationship("InterviewAttempt", backref="user", lazy=True)

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


class AptitudeQuestion(db.Model):
    __tablename__ = "aptitude_questions"

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)  # Quantitative / Logical / Verbal
    question = db.Column(db.Text, nullable=False)
    option_a = db.Column(db.String(255), nullable=False)
    option_b = db.Column(db.String(255), nullable=False)
    option_c = db.Column(db.String(255), nullable=False)
    option_d = db.Column(db.String(255), nullable=False)
    correct_option = db.Column(db.String(1), nullable=False)  # A/B/C/D
    explanation = db.Column(db.Text, nullable=True)


class AptitudeAttempt(db.Model):
    __tablename__ = "aptitude_attempts"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class CodingProblem(db.Model):
    __tablename__ = "coding_problems"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    difficulty = db.Column(db.String(20), nullable=False)  # Easy / Medium / Hard
    description = db.Column(db.Text, nullable=False)
    sample_input = db.Column(db.Text, nullable=False)
    sample_output = db.Column(db.Text, nullable=False)
    hints = db.Column(db.Text, nullable=True)
    starter_code = db.Column(db.Text, nullable=True)
    # Expected function body logic check via multiple test cases (JSON-like lines)
    test_input = db.Column(db.Text, nullable=False)
    test_output = db.Column(db.Text, nullable=False)


class CodingAttempt(db.Model):
    __tablename__ = "coding_attempts"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    problem_id = db.Column(db.Integer, db.ForeignKey("coding_problems.id"), nullable=False)
    code = db.Column(db.Text, nullable=False)
    passed = db.Column(db.Boolean, default=False)
    result_message = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    problem = db.relationship("CodingProblem", backref="attempts")


class InterviewQuestion(db.Model):
    __tablename__ = "interview_questions"

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)  # HR / Technical / Behavioral
    question = db.Column(db.Text, nullable=False)
    model_answer = db.Column(db.Text, nullable=False)
    tips = db.Column(db.Text, nullable=True)


class InterviewAttempt(db.Model):
    __tablename__ = "interview_attempts"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey("interview_questions.id"), nullable=False)
    user_answer = db.Column(db.Text, nullable=False)
    self_rating = db.Column(db.Integer, nullable=False)  # 1-5
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    question = db.relationship("InterviewQuestion", backref="attempts")
