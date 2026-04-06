"""
config.py - Configuration-driven design. All settings in one place.
No hardcoded credentials.
"""

import os
from dataclasses import dataclass
from dotenv import load_dotenv
load_dotenv() 

@dataclass
class GeminiConfig:
    api_key: str = os.getenv("GEMINI_API_KEY", "")
    
    model_name: str = "gemini-pro"
    max_output_tokens: int = 1024
    temperature: float = 0.7
    top_p: float = 0.9


@dataclass
class AppConfig:
    app_title: str = "MindEase – Mental Health Support"
    app_icon: str = "🌿"
    max_history_turns: int = 20       # session memory cap (token optimization)
    log_file: str = "chatbot.log"


GEMINI_CONFIG = GeminiConfig()
APP_CONFIG = AppConfig()
