<h1 align="center">🤖 GenAI Project – Agent AI Interview Scheduler</h1>

## 📌 Description
The GenAI Project is an SMS-based chatbot designed to interact with job candidates applying for a Python Developer position. It autonomously conducts conversations, collects and validates information, answers questions, and schedules interviews with human recruiters — or politely ends the conversation when appropriate.

This project leverages specialized agents, dynamic decision-making, and a knowledge base (vector DB + SQL) to deliver a smooth and intelligent pre-interview experience.

## 🧠 Agent Architecture
### Main Agent: Manages turn-by-turn conversation and decides among:

**Continue:** proceed with the conversation

**Schedule:** schedule the interview

**End:** politely end the conversation

## 🧠 Advisor Agents:

| Advisor             | Description                                                                                   |
|---------------------|-----------------------------------------------------------------------------------------------|
| **Exit Advisor**      | Confirms when it’s appropriate to end the conversation politely.                             |
| **Scheduling Advisor**| Checks recruiter calendars in the SQL database and validates proposed interview time slots.  |
| **Info Advisor**      | Answers candidate questions using knowledge from the vector database.                        |

##  📦 Requirements
- Python 3.10+ or higher 
- All dependencies listed in requirements.txt.
To install the dependencies, run:
```bash
pip install -r requirements.txt
```
---


## 🚀 Usage
### 1. Clone the repository:

```
git clone https://github.com/yourusername/genai-agent-scheduler.git
cd genai-agent-scheduler
```

### 2. Set up environment variables in a .env file:
```
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
DATABASE_URL=your_database_url
VECTOR_DB_API_KEY=your_vector_db_key
```

### 3. Run the application:
```
python main.py
```

## 🛠️ Project Structure

```plaintext
genai-agent-scheduler/
│── agents/
│── db/
│── vectorstore/
│── sms/
│── main.py
│── requirements.txt
│── README.md
│── .env.example
```

## ✅ Features
- SMS-based AI chatbot
- Automated candidate screening
- Intelligent scheduling
- Context-aware Q&A using vector database
- Multi-agent decision-making system

## 🤝 Contributing
Contributions are welcome! Fork the repository and submit a pull request.

## 📄 License
MIT License