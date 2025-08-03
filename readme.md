GenAI Project - Agent AI Interview Scheduler
📌 Description
The GenAI Project is an SMS-based chatbot designed to interact with job candidates applying for a Python Developer position. It autonomously conducts conversations, collects and validates information, answers questions, and schedules interviews with human recruiters — or politely ends the conversation when appropriate.

This project leverages specialized agents, dynamic decision-making, and a knowledge base (vector DB + SQL) to deliver a smooth and intelligent pre-interview experience.

🧠 Agent Architecture
Main Agent: Manages turn-by-turn conversation and decides among:

Continue: proceed with the conversation

Schedule: schedule the interview

End: politely end the conversation

Advisor Agents:

Exit Advisor: Confirms when ending the conversation is appropriate.

Scheduling Advisor: Checks recruiter calendars via SQL database and validates proposed time slots.

Info Advisor: Answers candidate questions related to the position using vector database knowledge.

📦 Requirements
Python 3.10+ and dependencies listed in requirements.txt.
To install:

bash
Copy
Edit
pip install -r requirements.txt
🚀 Usage
Clone the repository:

bash
Copy
Edit
git clone https://github.com/yourusername/genai-agent-scheduler.git
cd genai-agent-scheduler
Set up environment variables in a .env file:

bash
Copy
Edit
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
DATABASE_URL=your_database_url
VECTOR_DB_API_KEY=your_vector_db_key
Run the application:

bash
Copy
Edit
python main.py
🛠️ Project Structure
css
Copy
Edit
genai-agent-scheduler/
│── agents/
│── db/
│── vectorstore/
│── sms/
│── main.py
│── requirements.txt
│── README.md
│── .env.example
✅ Features
SMS-based AI chatbot

Automated candidate screening

Intelligent scheduling

Context-aware Q&A using vector database

Multi-agent decision-making system

🤝 Contributing
Contributions are welcome! Fork the repository and submit a pull request.

📄 License
MIT License