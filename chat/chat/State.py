from typing import List

import pynecone as pc
from chat.gpt.gpt import GPT
from chat.model.Message import Message


class State(pc.State):
    input_text: str = ""
    src_language: str = "한국어"
    target_language: str = "영어"
    messages: List[Message] = []
    @pc.var
    def output(self) -> str:
        return "Translations will appear here."

    def submit(self):
        if self.input_text.strip() == "":
            return

        self.messages.append(
            GPT().translate(
                self.input_text,
                self.src_language,
                self.target_language
            )
        )
