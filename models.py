# models.py

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime,timezone
from flask_migrate import Migrate 

db = SQLAlchemy()
def init_db(app):
    db.init_app(app)
    

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(300), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    transactions = db.relationship('Transaction', backref='user', lazy=True)


    def __repr__(self):
        return f"<User {self.username}>"

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    transaction_type = db.Column(db.String(10), nullable=False)  # 'expense' or 'earning'
    description = db.Column(db.String(255))
    date = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    category = db.Column(db.String(50))
    
    def __repr__(self):
        return f"<Transaction {self.id} - {self.transaction_type} {self.amount}>"

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    subtitle = db.Column(db.String(255))
    content = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(255))  # Store image path
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<Blog {self.id} - {self.title}>"
    