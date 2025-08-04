
<p align="center">
  <img src="https://upload.wikimedia.org/wikipedia/commons/c/c3/Python-logo-notext.svg" alt="Python Logo" width="100" height="100">
</p>

<h1 align="center"> GenAI Project – Agent AI Interview Scheduler</h1>
<p align="center">
  SMS-based AI chatbot for candidate interaction and interview scheduling  
  <br/>
  <a href="https://github.com/rafaw01/genai-agent-scheduler">View Demo</a>
  ·
  <a href="https://github.com/rafaw01/genai-agent-scheduler/issues">Report Bug</a>
  ·
  <a href="https://github.com/rafaw01/genai-agent-scheduler/issues">Request Feature</a>
</p>


## Table of Contents
- [About the Project](#about-the-project)
- [Features](#features)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Screenshots](#screenshots)
- [Code Examples](#code-examples)
- [Project Structure](#project-structure)
- [To-Do List](#to-do-list)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)
- [Acknowledgements](#acknowledgements)



## 📌 About the Project
The GenAI Project is an SMS-based chatbot designed to interact with job candidates applying for a  position in Hi-Tech Market. It autonomously conducts conversations, collects and validates information, answers questions, and schedules interviews with human recruiters — or politely ends the conversation when appropriate.

This project leverages specialized agents, dynamic decision-making, and a knowledge base (vector DB + SQL) to deliver a smooth and intelligent pre-interview experience.

### 👨🏻‍💻 Agent Architecture
#### Main Agent: Manages turn-by-turn conversation and decides among:

**Continue:** proceed with the conversation

**Schedule:** schedule the interview

**End:** politely end the conversation

### 👨🏻‍💻 Advisor Agents:

| Advisor             | Description                                                                                   |
|---------------------|-----------------------------------------------------------------------------------------------|
| **Exit Advisor**      | Confirms when it’s appropriate to end the conversation politely.                             |
| **Scheduling Advisor**| Checks recruiter calendars in the SQL database and validates proposed interview time slots.  |
| **Info Advisor**      | Answers candidate questions using knowledge from the vector database.                        |



## ✅ Features
- [x] Data loading and cleaning 
- [x] Data handling with Pandas
- [x] SMS-based AI chatbot
- [x] Automated candidate screening
- [x] Intelligent scheduling
- [x] Context-aware Q&A using vector database
- [x] Multi-agent decision-making system
- [x] Streamlit 
- [x] LangChain
- [x] Agent Orchestration
- [x] Modern Python project structure
- [x] Easy customization 
- [x] Cloud deployment


## 🚀 Getting Started

###  📦 Pre-requisites
- Python 3.10+ or higher 
- All dependencies listed in requirements.txt.
To install the dependencies, run:
```bash
pip install -r requirements.txt
```
---


## 💻 Launch Agent AI

[Launch Agent AI](https://ganaifin.streamlit.app/)


## 🐍 Code Examples
```python
# Suppress prints during import of sub-agents
_silent_buf = io.StringIO()
with contextlib.redirect_stdout(_silent_buf):
    from exit_advisor import ExitAdvisor
    from info_advisor import InfoAdvisor
from scheduling_advisor import SchedulingAdvisor, df as schedule_df

# Keywords for routing
EXIT_KEYWORDS = {"exit", "quit", "bye"}
SCHED_KEYWORDS = {"schedule", "appointment", "interview", "meeting", "book", "booking", "set a meeting"}
INFO_KEYWORDS = {
    "who", "what", "how", "when", "where", "why", "which",
    "explain", "detail", "clarify", "clarification",
    "responsibility", "responsibilities"
}
GREETINGS = {"hi", "hello", "hey", "shalom", "שלום"}
```


## 🚀 Installation
### 1. Clone the repository:

```
git clone https://github.com/rafaw01/genai-agent-scheduler.git
cd genai-agent-scheduler
```

### 2. Run the application:
```
python Main_5.py
```

## 🛠️ Project Structure

```plaintext
GANAI_FINEL_PRO-MASTER/
├── .idea
│   ├── .gitignore
│   ├── .name
│   ├── GanAi_fin_pro.iml
│   ├── inspectionProfiles
│   │   └── profiles_settings.xml
│   ├── misc.xml
│   ├── modules.xml
│   └── vcs.xml
├── .venv
│   ├── .gitignore
│   ├── .streamlit
│   │   └── secrets.toml
│   ├── Include
│   │   └── site
│   │       └── python3.12
│   │           └── greenlet
│   │               └── greenlet.h
│   ├── Lib
│   │   └── site-packages
│   ├── nootbooks
│   │   ├── .env
│   │   ├── Main_5.py
│   │   ├── Python Developer Job Description.pdf
│   │   ├── Sample_Labeled_Conversations.csv
│   │   ├── __pycache__
│   │   │   ├── Main_5.cpython-312.pyc
│   │   │   ├── exit_advisor.cpython-312.pyc
│   │   │   ├── info_advisor.cpython-312.pyc
│   │   │   └── scheduling_advisor.cpython-312.pyc
│   │   ├── chat_history.json
│   │   ├── chroma_db
│   │   │   ├── chroma.sqlite3
│   │   │   └── ff2a810d-7be4-409e-9591-ecb9f4a2b2b0
│   │   │       ├── data_level0.bin
│   │   │       ├── header.bin
│   │   │       ├── length.bin
│   │   │       └── link_lists.bin
│   │   ├── confusion_matrix.png
│   │   ├── db_Tech.sql
│   │   ├── evaluate.py
│   │   ├── exit_advisor.py
│   │   ├── info_advisor.py
│   │   ├── scheduling_advisor.py
│   │   ├── secrets.toml
│   │   ├── sms_conversations.json
│   │   └── streamlit_app.py
│   ├── pyvenv.cfg
│   ├── secrets.toml
│   ├── share
│   │   ├── jupyter
│   │   │   ├── kernels
│   │   │   │   └── python3
│   │   │   │       ├── kernel.json
│   │   │   │       ├── logo-32x32.png
│   │   │   │       ├── logo-64x64.png
│   │   │   │       └── logo-svg.svg
│   │   │   └── nbextensions
│   │   │       └── pydeck
│   │   │           ├── extensionRequires.js
│   │   │           ├── index.js
│   │   │           └── index.js.map
│   │   └── man
│   │       └── man1
│   │           ├── ipython.1
│   │           ├── isympy.1
│   │           └── ttx.1
│   └── sms_conversations.json
├── .vs
│   └── slnx.sqlite
├── .vscode
│   └── settings.json
├── Python Developer Job Description.pdf
├── __pycache__
│   └── info_advisor.cpython-312.pyc
├── db_Tech.sql
├── dir
├── requirements.txt
├── secrets.toml
└── sms_conversations.json
```



## 🤝 Contributing
Contributions are welcome! Fork the repository and submit a pull request.


## 📄 License

Distributed under the XXX License. See LICENSE for more information.

## 📄 Contact

- Omer Leon - omerleon87@gmail.com
- Or Eliezer - or1234eli@gmail.com
- Rafael Wajnsztajn - rafaw01@gmail.com
- Project Link: https://github.com/rafaw01/genai-agent-scheduler

## 📄 Acknowledgements
- Python
- Pandas
- SQL 
- Fine-Tuning
- Embedding
- Agent Architecture (OpenAI API & LangChain)
- Streamlit
- Prompting Strategies
- Evaluation & Testing 