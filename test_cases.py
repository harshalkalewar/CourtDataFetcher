import unittest
from main import app, db
from models import CaseData


class CourtAppTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()


    def tearDown(self):
        # Dropping tables after each test
        with app.app_context():
            db.session.remove()
            db.drop_all()


    def test_FetchCaseDetails_ReturnsDataSuccessfully(self):
        # Post a case that exists
        response = self.app.post('/', data={
            'case_type': 'CS(COMM)',
            'case_number': 5,
            'case_year': 2017
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'CS(COMM)', response.data)   


    def test_FetchCaseDetails_ReturnsCachedCase(self):

        self.app.post('/', data={
            'case_type': 'CS(COMM)',
            'case_number': 5,
            'case_year': 2017
        })

        response = self.app.post('/', data={
            'case_type': 'CS(COMM)',
            'case_number': 5,
            'case_year': 2017
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'CS(COMM)', response.data)         


    def test_FetchCaseDetails_ThrowsInvalidCaseException(self):
        # Post a case that doesn't exist
        response = self.app.post('/', data={
            'case_type': 'ABC',
            'case_number': 9999,
            'case_year': 2099
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Case Details Not Found', response.data)        


if __name__ == '__main__':
    unittest.main()