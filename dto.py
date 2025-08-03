class CaseDataDTO:
    def __init__(self, case_type, case_number, case_year, data: dict):
        self.case_type = case_type
        self.case_number = case_number
        self.case_year = case_year
        self.case_no = data.get("case_number")
        self.orders_link = data.get("orders_link")
        self.petitioner = data.get("petitioner")
        self.respondent = data.get("respondent")
        self.next_date = data.get("next_date")
        self.last_date = data.get("last_date")
        self.court_number = data.get("court_number")
        self.latest_order_link = data.get("latest_order_link")
