from typing import List

import pynecone as pc

from chat.db.ManualVectorDB import ManualVectorDB
from chat.gpt.gpt import GPT
from chat.model.Message import Message

db = ManualVectorDB()
gpt = GPT()


class State(pc.State):
    input_text: str = ""
    messages: List[Message] = []
    is_working = False
    leaning_messages: List[str] = []

    async def submit_handler(self):
        self.is_working = True
        yield

        if self.input_text.strip() == "":
            self.is_working = False
            return

        related_documents = db.query(self.input_text, 1)

        res = gpt.execute(self.input_text, related_documents)

        self.messages.append(res)

        self.is_working = False

    def leaning_handler(self):
        db.create(self.leaning_messages)
