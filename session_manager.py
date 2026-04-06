"""
session_manager.py - Session-based multi-turn conversation memory.
Maintains structured chat history with context window management.
"""

from config import APP_CONFIG


class SessionManager:
    """
    Manages in-session conversation history in Gemini's expected format.
    Automatically trims history to stay within token budget.
    """

    def __init__(self):
        self.history: list[dict] = []

    def add_user_message(self, text: str) -> None:
        self.history.append({"role": "user", "parts": [text]})
        self._trim()

    def add_model_message(self, text: str) -> None:
        self.history.append({"role": "model", "parts": [text]})
        self._trim()

    def _trim(self) -> None:
        """Keep only the most recent N turns to manage token usage."""
        max_entries = APP_CONFIG.max_history_turns * 2  # user + model pairs
        if len(self.history) > max_entries:
            self.history = self.history[-max_entries:]

    def get_history(self) -> list[dict]:
        """Return current history (excludes the current user message)."""
        # History passed to build_messages excludes the last user entry
        # because build_messages appends the new user message itself
        if self.history and self.history[-1]["role"] == "user":
            return self.history[:-1]
        return self.history

    def clear(self) -> None:
        self.history = []

    @property
    def turn_count(self) -> int:
        return len(self.history) // 2
