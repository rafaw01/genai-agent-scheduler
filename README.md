
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
The GenAI Project is an SMS-based chatbot designed to interact with job candidates applying for a Python Developer position. It autonomously conducts conversations, collects and validates information, answers questions, and schedules interviews with human recruiters — or politely ends the conversation when appropriate.

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


## 📡 Usage:
```
python main.py
```

## 💻 Launch Agent AI

[Launch Agent AI](https://ganaifin.streamlit.app/)


## 🐍 Code Examples
```python
import pandas as pd
from openai import OpenAI

client = OpenAI(api_key="your_api_key_here")  # Replace with your actual API key or use environment variable

# Load data
df = pd.read_csv('data/dataset.csv')
```


## 🚀 Installation
### 1. Clone the repository:

```
git clone https://github.com/rafaw01/genai-agent-scheduler.git
cd genai-agent-scheduler
```

### 2. Run the application:
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

```
## 🛠️ To-Do List

- [x] Initial project setup  
- [x] Add python_project module  
- [x] Improve documentation  
- [x] Add web interface  

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