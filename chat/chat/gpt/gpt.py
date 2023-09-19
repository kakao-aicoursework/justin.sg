import datetime
import os

import openai
from dotenv import load_dotenv
from langchain import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import (
    SystemMessage
)

from chat.model.Message import Message

load_dotenv()
openai.api_key = os.environ.get('OPENAI_API_KEY')


def read_prompt_template(file_path: str) -> str:
    with open(file_path, "r") as f:
        prompt_template = f.read()

    return prompt_template


manual = read_prompt_template("project_data.txt")
chat = ChatOpenAI(temperature=0.8)
system_msg = f"""
assistant는 카카오싱크 API에서 제공하는 기능이 무엇인지 설명하는 역할을 담당한다.
<manual>
{manual}
</manual>"""


class GPT:
    def execute(self, question):
        system_message_prompt = SystemMessage(content=system_msg)
        human_template = ("manual을 기반으로 질문: {question}에 대답해줘")
        human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
        chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
        chain = LLMChain(llm=chat, prompt=chat_prompt)

        return Message(
            origin_input_text=question,
            result_text=chain.run(question=question),
            created_at=datetime.datetime.now().isoformat()
        )
