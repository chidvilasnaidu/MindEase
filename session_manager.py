"""
session_manager.py - Multi-turn conversation memory.
"""

MAX_TURNS = 10


class SessionManager:
    def __init__(self):
        self.history: list[dict] = []

    def add_user_message(self, text: str) -> None:
        self.history.append({"role": "user", "content": text})
        self._trim()

    def add_model_message(self, text: str) -> None:
        self.history.append({"role": "assistant", "content": text})
        self._trim()

    def _trim(self) -> None:
        max_entries = MAX_TURNS * 2
        if len(self.history) > max_entries:
            self.history = self.history[-max_entries:]

    def build_context(self) -> str:
        """Build plain-text conversation context — same as friend's pattern."""
        context = ""
        for message in self.history:
            role = message["role"].capitalize()
            context += f"{role}: {message['content']}\n"
        return context

    def clear(self) -> None:
        self.history = []

    @property
    def turn_count(self) -> int:
        return len(self.history) // 2
