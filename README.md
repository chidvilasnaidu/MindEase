# 🌿 MindEase — Production-Ready Mental Health Support Chatbot

A production-grade, domain-specific AI chatbot powered by the **Google Gemini API**, built with clean architecture principles, advanced prompt engineering, and deployed on AWS EC2.

---

## 📐 Architecture Overview

```
User
 └──► Streamlit UI (app.py)
         └──► SessionManager (session_manager.py)   ← Multi-turn memory
         └──► GeminiClient (gemini_client.py)        ← API layer
                  └──► PromptsModule (prompts.py)   ← Prompt engineering
                  └──► Gemini API (Google Cloud)
         └──► Config (config.py)                    ← All settings
```

### Module Breakdown

| File | Responsibility |
|------|---------------|
| `config.py` | All configuration (model, tokens, app settings). No hardcoded values. |
| `prompts.py` | System prompt, role instructions, domain constraints, message builder |
| `gemini_client.py` | Gemini API calls, exception handling, logging, crisis detection, fallback |
| `session_manager.py` | Chat history, multi-turn memory, context window trimming |
| `app.py` | Streamlit UI only — chat display, input, sidebar |

---

## 🚀 Local Setup

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/mindease-chatbot.git
cd mindease-chatbot
```

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

## 📁 Project Structure

```
mindease-chatbot/
├── app.py               # Streamlit UI
├── gemini_client.py     # Gemini API integration
├── prompts.py           # Prompt engineering module
├── session_manager.py   # Conversation memory
├── config.py            # Configuration
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variable template
├── .gitignore
└── README.md
```

---

## 🧪 Tech Stack

- **LLM:** Google Gemini 1.5 Flash
- **UI:** Streamlit
- **Language:** Python 3.10+
- **Deployment:** AWS EC2 (Ubuntu)
- **Process management:** nohup background execution

---

*Built as part of Innomatics Research Labs GenAI Project.*
