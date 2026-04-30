# AI-First HCP CRM Module

An AI-powered Customer Relationship Management (CRM) system designed specifically for Healthcare Professional (HCP) interactions. This tool enables field representatives to log, edit, and review HCP interactions using a conversational AI assistant.

## 🚀 Features
- **AI Chat Assistant:** Log interactions using natural language (e.g., "I met with Dr. Smith, sentiment was positive").
- **Dynamic Interaction Corrections:** The AI understands corrections to previous logs and updates the database automatically.
- **Real-Time Data Sync:** The recent interactions feed updates dynamically as the AI logs new meetings.
- **HCP Lookup:** Ask the AI to pull details about specific HCPs in the database.

## 🛠️ Tech Stack
- **Frontend:** React, Redux (State Management), Vite, Lucide Icons
- **Backend:** Python, FastAPI, SQLAlchemy
- **AI Framework:** LangGraph, LangChain
- **LLM Provider:** Groq (using `llama-3.1-8b-instant`)

## 📂 Project Structure
```
├── backend/          # Python FastAPI server
│   ├── agent/        # LangGraph AI agent and tools
│   ├── main.py       # API routes and server config
│   ├── database.py   # SQLAlchemy DB configuration
│   └── .env          # API keys
└── frontend/         # React Vite application
    ├── src/          
    │   ├── components/ # Chat UI and Interaction Lists
    │   ├── store/      # Redux slices
    │   └── App.jsx     # Main Layout
```

## ⚙️ Setup Instructions

### 1. Backend Setup
Navigate to the `backend` directory:
```bash
cd backend
```
Install the Python dependencies:
```bash
pip install -r requirements.txt
```
Create a `.env` file in the `backend` folder and add your Groq API key:
```env
GROQ_API_KEY=your_groq_api_key_here
```
Start the FastAPI server:
```bash
python main.py
```
*The backend will run on `http://localhost:8000`.*

### 2. Frontend Setup
Open a new terminal window and navigate to the `frontend` directory:
```bash
cd frontend
```
Install the Node.js dependencies:
```bash
npm install
```
Start the React development server:
```bash
npm run dev
```
*The frontend will run on `http://localhost:5173`.*

## 💡 Usage Example
Once both servers are running, open `http://localhost:5173` in your browser. 
In the Chat Assistant, try typing:
1. *"Log an interaction with HCP 1. The sentiment was positive and they liked the brochures."*
2. Wait for it to log, then say: *"Sorry, the sentiment was actually negative."*
3. Watch the Interaction List update in real-time!
