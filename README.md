# 🍽️ Zomato AI Restaurant Recommender

An AI-powered restaurant recommendation web app that combines structured dataset filtering with Groq LLM-generated explanations.

## 🌐 Live Demo
- **Frontend:** https://zomato-milestone-six.vercel.app
- **Backend API:** https://zomato-milestone-t73o.onrender.com
- **API Docs (Swagger):** https://zomato-milestone-t73o.onrender.com/docs

## 🏗️ Tech Stack
| Layer | Technology |
|-------|-----------|
| Frontend | HTML, CSS, Vanilla JS |
| Backend | FastAPI (Python) |
| AI/LLM | Groq (Llama 3.3 70B) |
| Dataset | Zomato restaurant data |
| Hosting (Frontend) | Vercel |
| Hosting (Backend) | Render |

## 🚀 Running Locally

### Backend
```bash
cd backend
.\venv\Scripts\Activate.ps1       # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Backend runs at http://127.0.0.1:8000

### Frontend
Open `frontend/index.html` in your browser — no build step needed.

## ⚙️ Environment Variables

Create `backend/.env`:
```
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile
```

## 📁 Project Structure
```
├── backend/
│   ├── app/
│   │   ├── main.py          # FastAPI routes
│   │   ├── engine.py        # Dataset filtering logic
│   │   ├── recommender.py   # Groq LLM integration
│   │   ├── database.py      # Dataset loading
│   │   ├── schemas.py       # Pydantic models
│   │   └── config.py        # Environment config
│   ├── data/
│   │   └── zomato_cached.csv
│   └── requirements.txt
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── app.js
├── render.yaml              # Render deployment config
└── .gitignore
```
