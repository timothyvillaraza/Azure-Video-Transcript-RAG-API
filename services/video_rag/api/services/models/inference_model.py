from typing import List

class MessageModel:
    def __init__(self, response: str):
        self.session_id: str
        self.messages = response