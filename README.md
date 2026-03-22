# 🩸 Blood Bank Management System

A full-stack Blood Bank Management application built using **FastAPI (backend)** and **Streamlit (frontend)**.  
This system helps manage donors, blood inventory, and blood requests efficiently.

---

## 🚀 Live Demo

- 🌐 Frontend (Streamlit):  
  https://blood-bank-management-8x4ebimmhrrceqx5tamzat.streamlit.app/

- ⚙️ Backend API (FastAPI Docs):  
  https://blood-bank-management-1-nrdt.onrender.com/docs

---

## 🧠 Features

### 👤 Donor Management
- Add donors with validation (minimum 90 days between donations)
- View all donors
- Search donors by blood group
- Filter eligible donors

### 🩸 Blood Inventory
- Add blood units
- View available blood by group
- Low stock alerts

### 📩 Request Management
- Create blood requests
- View all requests
- Fulfill requests based on availability

### 📊 Dashboard
- Visual insights using charts
- Donor distribution (Pie chart)
- Blood availability (Bar chart)

---

## 🏗️ Tech Stack

### Backend
- FastAPI
- Pydantic
- Uvicorn

### Frontend
- Streamlit
- Plotly
- Pandas
- Requests

### Deployment
- Backend → Render
- Frontend → Streamlit Cloud

---

## 📁 Project Structure



blood-bank-management/
│
├── backend/
│   ├── main.py
│   ├── models.py
│   ├── utils.py
│   └── requirements.txt
│
├── frontend/
│   └── app.py
│
├── data/
│   ├── donors.json
│   ├── blood.json
│   └── requests.json
│
└── requirements.txt

`

---

## ⚙️ Installation & Setup (Local)

### 1️⃣ Clone the repository

bash
git clone https://github.com/DEVALLAADITHYA/blood-bank-management.git
cd blood-bank-management
`

---

### 2️⃣ Setup Backend

bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload


Backend runs at:


http://127.0.0.1:8000


---

### 3️⃣ Setup Frontend

bash
cd frontend
pip install -r ../requirements.txt
streamlit run app.py
```

---

## 🔗 API Endpoints

| Method | Endpoint              | Description           |
| ------ | --------------------- | --------------------- |
| POST   | /donor/add            | Add donor             |
| GET    | /donor/all            | Get all donors        |
| GET    | /donor/eligible       | Get eligible donors   |
| GET    | /donor/search         | Search by blood group |
| POST   | /blood/add            | Add blood units       |
| GET    | /blood/availability   | View blood stock      |
| POST   | /request/add          | Create request        |
| GET    | /request/all          | Get requests          |
| PUT    | /request/fulfill/{id} | Fulfill request       |

---

## ⚠️ Notes

* Data is stored in JSON files (for demo purposes)
* On Render (free tier), data may reset due to stateless storage
* For production, use:

  * MongoDB Atlas / PostgreSQL

---

## 🔥 Future Improvements

* 🔐 User authentication (JWT)
* 🗄️ Database integration (MongoDB/PostgreSQL)
* 📱 Mobile responsive UI
* 📊 Advanced analytics dashboard
* 📧 Email/SMS alerts for low stock

---

## 👨‍💻 Author

*Adithya Devalla*
GitHub: [https://github.com/DEVALLAADITHYA](https://github.com/DEVALLAADITHYA)
