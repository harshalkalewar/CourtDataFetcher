from flask import Flask, render_template, request
from scraper import Scraper
from models import db, CaseData
from dto import CaseDataDTO 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def fetch_case_details():

    if request.method == 'POST':
        case_type = request.form['case_type']
        case_number = request.form['case_number']
        case_year = request.form['case_year']

        cached_case = CaseData.query.filter_by(case_type=case_type, case_number=case_number, case_year=case_year).first()
        if cached_case:
            return render_template("result.html", result=cached_case)
        
        scraper = Scraper()

        try:
            result = scraper.get_case_details(case_type, case_number, case_year)
            if not result or not result.get("orders_link"):
                return render_template("result.html", result=None)
            
            # Saving to DB
            new_case = CaseData(
                case_type=case_type,
                case_number=case_number,
                case_year=case_year,
                case_no=result["case_number"],
                orders_link=result["orders_link"],
                petitioner=result["petitioner"],
                respondent=result["respondent"],
                next_date=result["next_date"],
                last_date=result["last_date"],
                court_number=result["court_number"],
                latest_order_link=result["latest_order_link"]
            )
            db.session.add(new_case)
            db.session.commit()

            dto = CaseDataDTO(case_type, case_number, case_year, result)
            return render_template("result.html", result=dto)


        except Exception as e:
            scraper.driver.quit()
            return render_template("result.html", result=None)

    
    return render_template('case_input_form.html')


