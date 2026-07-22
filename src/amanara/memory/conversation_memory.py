from collections import deque


class ConversationMemory:
    def __init__(self, max_turns: int = 5):
        self.max_turns = max_turns
        self.messages = deque(maxlen=max_turns * 2)

    def add_user_message(self, message: str):
        self.messages.append(("User", message))

    def add_assistant_message(self, message: str):
        self.messages.append(("Assistant", message))

    def get_history(self) -> str:
        if not self.messages:
            return ""

        return "\n".join(
            f"{role}: {message}"
            for role, message in self.messages
        )

    def clear(self):
        self.messages.clear()