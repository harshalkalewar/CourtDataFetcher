# Delhi High Court Case Details Scraper

This is a Python Flask application that allows users to fetch case details from the Delhi High Court website using a clean Flask web interface. It stores results in SQLite and displays them using a responsive HTML template.

---

## 🔧 Features

- ✅ Submit case type, number, and year via web form
- ✅ Scrapes case data from the [Delhi High Court](https://delhihighcourt.nic.in/) 
- ✅ Caches and stores results in SQLite
- ✅ Responsive and styled result page
- ✅ Fallback handling for invalid case input
- ✅ Built-in test cases for validation
- ✅ Download latest order PDFs

---


## 📦 Setup Instructions

```bash
git clone https://github.com/harshalkalewar/CourtDataFetcher.git
cd CourtDataFetcher
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

```

## 🚀 Run Locally

- python app.py
- Visit http://localhost:5000 to try it out.

## 🧪 Run Tests

- python test_app.py


## 📝 Folder Structure

```
CourtDataFetcher/
├── main.py
├── scraper.py
├── models.py
├── dto.py
├── templates/
│   ├── case_input_form.html
│   └── result.html
├── test_cases.py
├── requirements.txt
└── README.md
```


## 📮 Contributing

```
Pull requests welcome! For major changes, please open an issue first.
```

## 📄 License

```
MIT License
```