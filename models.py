from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class CaseData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    case_type = db.Column(db.String(50))
    case_number = db.Column(db.Integer)
    case_year = db.Column(db.Integer)
    case_no = db.Column(db.String(100))
    orders_link = db.Column(db.String(500))
    petitioner = db.Column(db.String(255))
    respondent = db.Column(db.String(255))
    next_date = db.Column(db.String(50))
    last_date = db.Column(db.String(50))
    court_number = db.Column(db.String(50))
    latest_order_link = db.Column(db.String(500))

    __table_args__ = (
        db.UniqueConstraint('case_type', 'case_number', 'case_year', name='unique_case'),
    )
