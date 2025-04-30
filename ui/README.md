# 📊 Genesis UI Dashboard (Streamlit)

This Streamlit dashboard allows you to:
- View a summary of all Genesis claim reports
- See file readiness status per claim (RRT, Final Demand, Prophet)
- Download full ZIP casefiles when all documents are present

---

## 🚀 Quick Start

### 1. Install dependencies:
```bash
pip install -r requirements.txt
```

### 2. Run the dashboard:
```bash
streamlit run report_dashboard_ui.py
```

### 3. Access it in your browser:
Go to [http://localhost:8501](http://localhost:8501)

---

## 🧩 Requirements
- `streamlit`
- `requests`

Ensure your FastAPI backend is running at:
```
http://localhost:8000
```
You can change this by editing `API_URL` in `report_dashboard_ui.py`.

---

## 📁 File Structure
```
ui/
├── report_dashboard_ui.py       # Streamlit dashboard app
├── requirements.txt             # Frontend dependencies
└── README.md                    # This file
```

---

## 📦 Future Features
- Regenerate missing reports on demand
- Exhibit upload preview
- Email sendout of final ZIPs
