import datetime
import os
from typing import List

import openai
from dotenv import load_dotenv
from langchain import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
)

from chat.model.Message import Message

load_dotenv()
openai.api_key = os.environ.get('OPENAI_API_KEY')
llm = ChatOpenAI(temperature=0.1, max_tokens=3000, model="gpt-3.5-turbo")
system_msg = "assistant는 카카오싱크 API에서 제공하는 기능이 무엇인지 설명하는 역할을 담당한다."
table_of_contents = """
시작하기: 카카오싱크 목적
기능 소개: 카카오싱크의 기능
과정 예시: 카카오싱크를 사용하는 예시
도입 안내: 카카오싱크 도입을 위한 방법
설정 안내: 카카오싱크 설정 방법
RestAPI: RestAPI와 관련한 내용 설명
manager: 관리자와 연관된 내용 설명
"""


class GPT:
    def get_selected_table_of_content(self, message):
        table_of_contents_chain = LLMChain(
            llm=llm,
            prompt=ChatPromptTemplate.from_template(
                template="""
                너의 역할은 <table_of_contents>에서 하나를 선택하여 반환한다.
                <table_of_contents>
                {table_of_contents}
                </table_of_contents>

                user: {message}
                selection:
                """),
            verbose=True
        )

        return table_of_contents_chain.run({
            "message": message,
            "table_of_contents": table_of_contents
        })

    def execute(self, message, related_documents: List[str]):
        vector_chain = LLMChain(
            llm=llm,
            prompt=ChatPromptTemplate.from_template(
                template="""
                user가 입력한 {message}와 유사한 데이터로 선택된 {related_documents}을 활용하여 적절한 답을 한다.
                
                <message>
                    {message}
                </message>
                
                <related_documents>
                   {related_documents}
                </related_documents>
                
                answer:
                """),
            verbose=True
        )

        selection = self.get_selected_table_of_content(message)
        print(f"Selection : {selection}")

        if selection == "manager":
            # todo etc
            result = vector_chain.run(
                {
                    "message": message,
                    "related_documents": related_documents
                }
            )

            return Message(
                origin_input_text=message,
                result_text=f"""[   정의된 메뉴얼 정보가 없어 학습한 내용을 바탕으로 답변합니다.   ]
                {result}
                """,
                created_at=datetime.datetime.now().isoformat()
            )
        else:
            result = vector_chain.run(
                {
                    "message": message,
                    "related_documents": related_documents
                }
            )

            return Message(
                origin_input_text=message,
                result_text=result,
                created_at=datetime.datetime.now().isoformat()
            )
