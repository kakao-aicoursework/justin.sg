import openai
import datetime
import os
from dotenv import load_dotenv
from chat.model.Message import Message

load_dotenv()
openai.api_key = os.environ.get('OPENAI_API_KEY')

dictionary = {
    "한국어": ["오늘 날씨 어때", "딥러닝 기반의 AI기술이 인기를끌고 있다."],
    "영어": ["How is the weather today", "Deep learning-based AI technology is gaining popularity."],
    "일본어": ["今日の天気はどうですか", "ディープラーニングベースのAIテクノロジーが人気を集めています。"]
}

class GPT:
    def translate(self, text: str, src_language: str, target_language: str) -> Message:
        system_instruction = f"""
        - assistant는 번역의 역할만 담당한다.
        - assistant는 user의 질문의 번역의 원본으로 인식한다..
        - assistant는 {src_language}를 {target_language}로 적절하게 번역하고 번역된 텍스트만 출력한다.
        """

        fewshot_messages = []
        src_examples = dictionary[src_language]
        trg_examples = dictionary[target_language]

        for src_text, trg_text in zip(src_examples, trg_examples):
            fewshot_messages.append({"role": "user", "content": src_text})
            fewshot_messages.append({"role": "assistant", "content": trg_text})

        messages = [
            {"role": "system", "content": system_instruction},
            *fewshot_messages,
            {"role": "user", "content": text}
        ]

        # [
        #     {
        #         'role':'system',
        #         'content':'assistant는 번역앱으로서 동작한다. 한국어를 영어로 적절하게 번역하고 번역된 텍스트만 출력한다.'
        #     },
        #     {
        #         'role':'user',
        #         'content':'오늘 날씨 어때'
        #     },
        #     {
        #         'role':'assistant',
        #         'content':'How is the weather today'
        #     },
        #     {
        #         'role':'user',
        #         'content':'딥러닝 기반의 AI기술이 인기를끌고 있다.'
        #     },
        #     {
        #         'role':'assistant',
        #         'content':'Deep learning-based AI technology is gaining popularity.'
        #     },
        #     {
        #         'role':'user',
        #         'content':'안녕하세요.'
        #     }
        # ]
        #

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        return Message(
            origin_input_text=text,
            result_text=response['choices'][0]['message']['content'],
            created_at=datetime.datetime.now().isoformat()
        )
