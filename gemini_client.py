import logging
import time
from google import genai
from config import (
    GEMINI_API_KEY,
    MODEL_NAME,
    TEMPERATURE,
    MAX_OUTPUT_TOKENS,
)

logger = logging.getLogger("gemini_client")

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


def generate_response(full_prompt: str, user_message: str = "") -> str:
    # Crisis detection — check ONLY the user's message, not the full prompt.
    # The full prompt contains the system prompt which has crisis keywords in it,
    # which was causing EVERY message to trigger the crisis response.
    if _check_crisis(user_message):
        return CRISIS_RESPONSE

    try:
        # Create client per request (matches friend's pattern — most stable)
        client = genai.Client(api_key=GEMINI_API_KEY)

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=full_prompt,
            config={
                "temperature": TEMPERATURE,
                "max_output_tokens": MAX_OUTPUT_TOKENS,
                "top_p": 0.9,
            },
        )

        if not response or not response.text:
            logger.warning("Empty response from Gemini.")
            return "Unable to generate a response at the moment. Please try again."

        final_text = response.text.strip()

        logger.info("Gemini response generated successfully.")
        return final_text

    except Exception as e:
        err = str(e)
        logger.error(f"Gemini API error: {err}")

        if "429" in err or "RESOURCE_EXHAUSTED" in err:
            return (
                "⏳ The AI service is currently rate-limited. "
                "Please wait a moment and try again."
            )

        return "I'm having trouble connecting right now. Please know your feelings are valid. Could you try again in a moment?"
