from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='Doctor') # Doctor, Nurse, Admin
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Patient(db.Model):
    __tablename__ = 'patients'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.String(30), unique=True, nullable=False)
    hospital_number = db.Column(db.String(30), unique=True, nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    height = db.Column(db.Float, nullable=False) # cm
    weight = db.Column(db.Float, nullable=False) # kg
    bmi = db.Column(db.Float, nullable=False)
    contact = db.Column(db.String(20))
    date_of_visit = db.Column(db.Date, default=datetime.utcnow)
    medication_status = db.Column(db.String(200))
    symptoms = db.Column(db.Text)
    
    predictions = db.relationship('Prediction', backref='patient', lazy=True, cascade='all, delete-orphan')

class Prediction(db.Model):
    __tablename__ = 'predictions'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    dataset_filename = db.Column(db.String(255), nullable=False)
    risk_level = db.Column(db.String(30), nullable=False) # Healthy, Early, Moderate, High
    confidence_score = db.Column(db.Float, nullable=False)
    prob_healthy = db.Column(db.Float, nullable=False)
    prob_early = db.Column(db.Float, nullable=False)
    prob_moderate = db.Column(db.Float, nullable=False)
    prob_high = db.Column(db.Float, nullable=False)
    
    # EGG Feature extractions
    bradygastria_power = db.Column(db.Float)
    normogastria_power = db.Column(db.Float)
    tachygastria_power = db.Column(db.Float)
    dominant_frequency = db.Column(db.Float)
    
    # Store raw EGG signal array as a JSON string
    raw_signal = db.Column(db.Text, nullable=True)
    
    recommendation = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)