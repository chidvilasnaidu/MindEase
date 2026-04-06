"""
gemini_client.py - FINAL STABLE VERSION
Uses google-genai SDK
"""

import logging
import time
from google import genai
from google.genai import types

from config import GEMINI_CONFIG, APP_CONFIG
from prompts import SYSTEM_PROMPT

# ── Logging ─────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler(APP_CONFIG.log_file),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger("gemini_client")

# ── Responses ────────────────────────────────────────────────
FALLBACK_RESPONSE = (
    "I'm having a little trouble connecting right now. "
    "Please know your feelings are valid and I'm here for you. "
    "Could you try again in a moment?"
)

CRISIS_KEYWORDS = [
    "suicide", "kill myself", "end my life", "self-harm", "hurt myself",
    "don't want to live", "want to die", "cutting myself"
]

CRISIS_RESPONSE = (
    "💙 I hear you, and I'm really concerned about your safety right now.\n\n"
    "Please reach out to a crisis helpline immediately:\n"
    "- iCall (India): 9152987821\n"
    "- Vandrevala Foundation: 1860-2662-345\n"
    "- International: befrienders.org\n\n"
    "If you are in immediate danger, please call emergency services (112).\n\n"
    "I'm here with you. Can you tell me more about what's going on?"
)


def _check_crisis(text: str) -> bool:
    return any(kw in text.lower() for kw in CRISIS_KEYWORDS)


# ── Client ───────────────────────────────────────────────────
class GeminiClient:
    def __init__(self):
        if not GEMINI_CONFIG.api_key:
            raise ValueError("GEMINI_API_KEY missing")

        self.client = genai.Client(api_key=GEMINI_CONFIG.api_key)

        # ✅ Stable working model
        self.model = "gemini-2.0-flash"

        # ⏱ internal cooldown (prevents API spam)
        self.last_call = 0

        logger.info("Gemini initialized | model=%s", self.model)

    def get_response(self, chat_history: list, user_message: str):

        # 🚨 Crisis detection
        if _check_crisis(user_message):
            return CRISIS_RESPONSE, None

        # ⛔ Internal rate limit (extra safety)
        if time.time() - self.last_call < 1.5:
            return "⏳ Please wait a moment before sending another message.", None

        self.last_call = time.time()

        # ── Build conversation ────────────────────────────────
        contents = []

        # System primer
        contents.append(types.Content(
            role="user",
            parts=[types.Part(text=SYSTEM_PROMPT)]
        ))
        contents.append(types.Content(
            role="model",
            parts=[types.Part(text="I'm MindEase, here to support you. How are you feeling today?")]
        ))

        # History
        for turn in chat_history:
            contents.append(types.Content(
                role=turn["role"],
                parts=[types.Part(text=turn["parts"][0])]
            ))

        # Current message
        contents.append(types.Content(
            role="user",
            parts=[types.Part(text=user_message)]
        ))

        # ── API Call ──────────────────────────────────────────
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=contents,
                config=types.GenerateContentConfig(
                    max_output_tokens=GEMINI_CONFIG.max_output_tokens,
                    temperature=GEMINI_CONFIG.temperature,
                    top_p=GEMINI_CONFIG.top_p,
                ),
            )

            text = response.text.strip()

            return text, None

        except Exception as e:
            err = str(e)

            # ✅ Handle rate limit cleanly
            if "429" in err or "RESOURCE_EXHAUSTED" in err:
                logger.warning("Rate limit hit")
                return "⏳ Too many requests. Please wait a few seconds and try again.", None

            logger.error("Gemini error: %s", err)
            return FALLBACK_RESPONSE, None