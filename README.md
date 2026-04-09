# 🌿 MindEase — Production-Ready Mental Health Support Chatbot

A production-grade, domain-specific AI chatbot powered by the **Google Gemini API**, built with clean architecture principles, advanced prompt engineering, and deployed on AWS EC2.

---

## 📐 Architecture Overview

User
└──► Streamlit UI (app.py)
└──► SessionManager (session_manager.py)
└──► GeminiClient (gemini_client.py)
└──► PromptsModule (prompts.py)
└──► Gemini API (Google Cloud)
└──► Config (config.py)

````

## 📦 Module Breakdown

- config.py → Configuration
- prompts.py → Prompt engineering
- gemini_client.py → API integration
- session_manager.py → Memory handling
- app.py → UI

---


## 🚀 Local Setup

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/mindease-chatbot.git
cd mindease-chatbot
````

### 2. Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set your API key

```bash
cp .env.example .env
# Edit .env and add your Gemini API key
export GEMINI_API_KEY="your_actual_key_here"
```

> Get your free Gemini API key at: https://aistudio.google.com/app/apikey

### 5. Run the app

```bash
streamlit run app.py
```

Visit: http://localhost:8501

## 🖼️ Screenshots & Feature Demonstration

The `Screenshots/` folder contains real chatbot interactions across different mental health scenarios.

### Users can:

- 🔍 Filter by topic
- ⚡ Click **"Try this"** to auto-send sample queries
- 🤖 See real-time AI responses

---

## 🧠 Category-wise Testing

### 🟢 General

- For users who don’t know how to start
- Tests greeting and initial comfort
- **Example:** “I don’t know what to say…”

---

### 😰 Stress

- Covers exams, work pressure, overthinking
- **Example:** “I feel overwhelmed with exams”

---

### 😟 Anxiety

- Covers panic attacks, social anxiety, future fear
- **Example:** “I feel anxious talking to people”

---

### 😔 Low Mood

- Covers sadness, low motivation, feeling like a burden
- **Example:** “I don’t feel like doing anything”

---

### 😴 Sleep

- Covers insomnia and racing thoughts
- **Example:** “I can’t sleep at night”

---

### 💔 Relationships

- Covers loneliness, breakups, family conflicts
- **Example:** “I feel alone even with people”

---

### 🧘 Coping

- User asks for solutions (breathing, mindfulness)
- **Example:** “How do I calm myself?”

---

### 🚨 Crisis (Critical)

- Covers hopelessness and dark thoughts

**Important:**

- 🚨 Triggers crisis detection system
- 🤝 Responds with safe, empathetic, resource-based output
- ✅ Confirms bug fix is working correctly

---

## ☁️ AWS EC2 Deployment

### Step 1 — Launch an EC2 Instance

- **AMI:** Ubuntu 22.04 LTS
- **Instance type:** t2.micro (free tier)
- **Security Group:** Add inbound rule → TCP port **8501** from `0.0.0.0/0`
- **Key pair:** Create or use existing `.pem` key

### Step 2 — Connect to EC2

```bash
chmod 400 your-key.pem
ssh -i your-key.pem ubuntu@YOUR_EC2_PUBLIC_IP
```

### Step 3 — Install Python & dependencies

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3-pip python3-venv git -y
```

### Step 4 — Clone & configure the project

```bash
git clone https://github.com/YOUR_USERNAME/mindease-chatbot.git
cd mindease-chatbot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 5 — Set the API key (environment variable — never hardcoded)

```bash
export GEMINI_API_KEY="your_actual_key_here"
# To persist across sessions:
echo 'export GEMINI_API_KEY="your_actual_key_here"' >> ~/.bashrc
source ~/.bashrc
```

### Step 6 — Run as a background process

```bash
nohup streamlit run app.py \
  --server.port 8501 \
  --server.address 0.0.0.0 \
  --server.headless true \
  > streamlit.log 2>&1 &
```

### Step 7 — Access the app

```
http://YOUR_EC2_PUBLIC_IP:8501
```

### Stop the background process

```bash
pkill -f "streamlit run"
```

---
## 🌐 Live Demo (AWS-EC2) : http://13.62.231.255:8501/

## ✨ Key Features

- **Multi-turn memory** — Maintains conversation context across the full session
- **Advanced prompt engineering** — Structured system prompt with role instructions, CBT framework, domain constraints
- **Crisis detection** — Keyword-based safety layer that immediately surfaces crisis resources
- **Token optimization** — Automatic history trimming to stay within context window
- **Structured logging** — All API calls, errors, and token usage logged to `chatbot.log`
- **Fallback handling** — Graceful recovery from API errors with empathetic fallback messages
- **Secure config** — Zero hardcoded credentials; all secrets via environment variables
- **Clean architecture** — UI, API, prompts, and memory are fully separated modules

---

## 🛡️ Safety & Ethics

- MindEase explicitly states it is **not a licensed therapist** and cannot diagnose or prescribe
- Crisis keywords trigger an **immediate override** response with emergency resources
- Indian crisis resources are prioritized (iCall, Vandrevala Foundation)
- The system prompt enforces empathetic, non-judgmental, evidence-based responses

---

## 🧪 Tech Stack

- **LLM:** Google Gemini 1.5 Flash
- **UI:** Streamlit
- **Language:** Python 3.10+
- **Deployment:** AWS EC2 (Ubuntu)
- **Process management:** nohup background execution

---

_Built as part of Innomatics Research Labs GenAI Project._
