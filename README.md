# 🌿 MindEase — AI Mental Health Support Chatbot

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Google%20Gemini-1.5%20Flash-4285F4?style=for-the-badge&logo=google&logoColor=white"/>
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white"/>
  <img src="https://img.shields.io/badge/AWS%20EC2-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white"/>
  <img src="https://img.shields.io/badge/Ubuntu-22.04-E95420?style=for-the-badge&logo=ubuntu&logoColor=white"/>
</p>

<p align="center">
  <b>A production-ready, domain-specific AI chatbot for mental health support.</b><br/>
  Powered by Google Gemini API · Built with clean architecture · Deployed on AWS EC2
</p>

---

## 📌 What is MindEase?

MindEase is a production-grade mental health support chatbot that provides a safe, judgment-free space for users to talk about stress, anxiety, low mood, sleep issues, relationships, and more.

It is **not a replacement for therapy** — it is a compassionate first step, built with real engineering standards, CBT-based prompt engineering, and a crisis detection safety layer.

---

## ✨ Key Features

| Feature | Description |
|---|---|
| 🧠 **Multi-Turn Memory** | Maintains full conversation context across the session |
| 🎯 **Advanced Prompt Engineering** | CBT-based system prompts with role instructions & domain constraints |
| 🚨 **Crisis Detection** | Keyword-based safety layer — instantly surfaces Indian emergency helplines |
| ⚡ **Token Optimization** | Auto-trims history to stay within Gemini's context window |
| 📋 **Structured Logging** | All API calls, errors & token usage logged to `chatbot.log` |
| 🔄 **Fallback Handling** | Graceful recovery from API failures with empathetic responses |
| 🔐 **Secure Config** | Zero hardcoded credentials — all secrets via environment variables |
| 🏗️ **Clean Architecture** | UI, API, prompts & memory fully separated into dedicated modules |

---

## 🗂️ Project Structure

```
mindease-chatbot/
│
├── app.py                  # Streamlit UI layer
├── gemini_client.py        # Gemini API integration & error handling
├── session_manager.py      # Conversation memory & session management
├── prompts.py              # Prompt engineering module
├── config.py               # Configuration & environment variables
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variable template
├── Screenshots/            # Demo screenshots & chatbot interactions
└── README.md
```

---

## 📐 Architecture

```
User Input
    │
    ▼
┌─────────────────────┐
│   Streamlit UI      │  ← app.py
│   (Chat Interface)  │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│   Session Manager   │  ← session_manager.py
│   (Memory & History)│
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐     ┌──────────────────┐
│   Gemini Client     │────►│  Prompts Module  │
│   (API Integration) │     │  (CBT Framework) │
└────────┬────────────┘     └──────────────────┘
         │
         ▼
┌─────────────────────┐
│   Google Gemini API │  ← Cloud (Google)
│   (LLM Response)    │
└─────────────────────┘
         │
         ▼
    Response rendered
    in Streamlit UI
```

---

## 🧩 Supported Topics

| Category | Example Query |
|---|---|
| 🟢 General | *"I don't know what to say…"* |
| 😰 Stress | *"I feel overwhelmed with exams"* |
| 😟 Anxiety | *"I feel anxious talking to people"* |
| 😔 Low Mood | *"I don't feel like doing anything"* |
| 😴 Sleep | *"I can't sleep at night"* |
| 💔 Relationships | *"I feel alone even with people"* |
| 🧘 Coping | *"How do I calm myself?"* |
| 🚨 Crisis | Triggers immediate override → emergency resources |

---

## 🚀 Local Setup

### Prerequisites
- Python 3.10+
- A free [Google Gemini API Key](https://aistudio.google.com/app/apikey)

### Step 1 — Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/mindease-chatbot.git
cd mindease-chatbot
```

### Step 2 — Create a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
```

### Step 3 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 4 — Configure environment variables
```bash
cp .env.example .env
```
Open `.env` and add your key:
```env
GEMINI_API_KEY=your_actual_key_here
```

### Step 5 — Run the app
```bash
streamlit run app.py
```
## Visit: **http://13.62.231.255:8501/**

---

## ☁️ AWS EC2 Deployment

### 1. Launch EC2 Instance
- **AMI:** Ubuntu 22.04 LTS
- **Instance type:** t2.micro *(free tier eligible)*
- **Security Group:** Inbound rule → TCP port `8501` from `0.0.0.0/0`

### 2. Connect via SSH
```bash
chmod 400 your-key.pem
ssh -i your-key.pem ubuntu@YOUR_EC2_PUBLIC_IP
```

### 3. Install dependencies on EC2
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3-pip python3-venv git -y
```

### 4. Clone & set up project
```bash
git clone https://github.com/YOUR_USERNAME/mindease-chatbot.git
cd mindease-chatbot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 5. Set API key (persisted)
```bash
echo 'export GEMINI_API_KEY="your_actual_key_here"' >> ~/.bashrc
source ~/.bashrc
```

### 6. Run as background process
```bash
nohup streamlit run app.py \
  --server.port 8501 \
  --server.address 0.0.0.0 \
  --server.headless true \
  > streamlit.log 2>&1 &
```

### 7. Access the live app
```
http://YOUR_EC2_PUBLIC_IP:8501
```

### Stop the process
```bash
pkill -f "streamlit run"
```

---

## 🛡️ Safety & Ethics

- MindEase explicitly states it is **not a licensed therapist** and cannot diagnose or prescribe
- Crisis keywords trigger an **immediate safety override** with emergency helpline details
- **Indian crisis resources** are prioritized — iCall & Vandrevala Foundation
- System prompt enforces empathetic, non-judgmental, evidence-based responses at all times

---

## 🧪 Tech Stack

| Layer | Technology |
|---|---|
| LLM | Google Gemini 1.5 Flash |
| UI | Streamlit |
| Language | Python 3.10+ |
| Cloud | AWS EC2 (Ubuntu 22.04) |
| Process Management | nohup background execution |
| Security | python-dotenv + environment variables |

---

## 📦 Dependencies

```txt
streamlit
google-generativeai
python-dotenv
```

```bash
pip install -r requirements.txt
```

---

## 🖼️ Screenshots

> Add your screenshots here from the `Screenshots/` folder
>
> `![Chat UI](Screenshots/chat_demo.png)`

---

## 🤝 Contributing

Contributions are welcome! Please open an issue before submitting a PR.

1. Fork the repo
2. Create your branch → `git checkout -b feature/your-feature`
3. Commit changes → `git commit -m "Add your feature"`
4. Push → `git push origin feature/your-feature`
5. Open a Pull Request

---

## 📄 License

MIT License © 2026 MindEase

---

<p align="center">
  Built with ❤️ as part of <b>Innomatics Research Labs — GenAI Program</b><br/>
  <i>"Technology should serve humanity — especially when humanity is struggling."</i>
</p>
m
