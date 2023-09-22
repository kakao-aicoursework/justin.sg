from typing import List

import pynecone as pc

from chat.gpt.gpt import GPT
from chat.model.Message import Message


class State(pc.State):
    input_text: str = ""
    messages: List[Message] = []
    is_working = False

    async def submit(self):
        self.is_working = True
        yield

        if self.input_text.strip() == "":
            return

        res = GPT().execute(self.input_text)

        self.messages.append(res)

        self.is_working = False
