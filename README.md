# Chatbot Azercell

🚀 A full-stack chatbot project with FastAPI backend and Streamlit frontend, containerized with Docker and deployable on AWS EC2. Here I have both simple chatbot and chatbot using Azercell knowledge base.
In backend part there is option to write query and test the answers. Also in frontend there are options to clear chat or start a new chat.
Below I have some query responses, as shown in pics with help of command (true, false) there is option to use or not use Azercell knowledge base.
Note: when running on your local machine whole repo due to aws configurations there might be problems, it is recommended to you to add .env file in backend folder with own creditals.

## 📂 Project Structure
chatbot_azercell/
│── backend/         # FastAPI backend  
│── frontend/        # Streamlit frontend   
│── docker-compose.yml  
│── README.md  

## ⚡ Features
- FastAPI Backend: Provides REST API for chatbot interactions  
- Streamlit Frontend: User-friendly UI for chatting with the bot  
- Dockerized: Run everything with docker compose  
- CI/CD with GitHub Actions: Automatic linting, building, and deployment on EC2  

## 🛠️ Setup Instructions

### 1. Clone Repository
```bash
git clone <yhttps://github.com/zahraibihsova/chatbot_azercell>
cd chatbot_azercell

2. Run Locally (without Docker)

Backend:

cd backend
pip install -r requirements.txt
uvicorn app:app --reload --host 0.0.0.0 --port 8000

Frontend:
cd frontend
pip install -r requirements.txt
streamlit run app.py


3. With docker
docker compose up --build


🧪 Example Queries
Backend API

POST /chat
{
  "message": "Hello "
}

{
  "reply": "Hello! How can I assist you today? Whether you have questions, need information, or just want to chat about something, I'm here to help. What's on your mind?"
}

POST /chat
{
  "message": "what is your name "
}

{
  "reply": "My name is Betty 💅🏻, nice to meet you!" #overall only to this question its reply is betty and I understand that chatbot is Claude
}

POST /chat
{
  "message": "can u inform me on azercell ethics "
}

{
  "reply": "# Azercell Ethics and Business Conduct Overview
Based on Azercell's Code of Conduct and Business Ethics, here are the key elements of their ethical framework" #response is long
}




--I hope everything is clear and understandable