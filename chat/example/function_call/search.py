import json
import os

import openai
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.environ.get('OPENAI_API_KEY')


def scrap_google_news(keyword: str, limit: int = 5):
    google_search_url = "https://www.google.com/search"
    params = {
        "q": keyword,
        "tbm": "nws",
        "num": limit
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36"
    }

    res = requests.get(google_search_url, params=params, headers=headers)
    soup = BeautifulSoup(res.content, "html.parser")
    return [
        {
            "link": element.find("a")["href"],
            "title": element.select_one("div.MBeuO").get_text(),
            "snippet": element.select_one(".GI74Re").get_text()
        }
        for element in soup.select("div.SoaBEf")
    ]


def news_gpt(messages, temperature=0, max_tokens=1024):
    functions = [
        {
            "name": "scrap_google_news",
            "description": "구글에서 뉴스를 검색합니다.",
            "parameters": {
                "type": "object",
                "properties": {
                    "keyword": {
                        "type": "string",
                        "description": "검색 키워드"
                    }
                },
                "required": ["keyword"]
            }
        }
    ]

    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        functions=functions,
        function_call="auto",
        temperature=temperature,
        max_tokens=max_tokens,
    )

    return res.choices[0].message


def get_function_call_result(res: object, function_dic):
    if res.get("function_call"):
        function_name = res.function_call.name
        function_arguments = json.loads(res.function_call.arguments)

        return function_dic[function_name](function_arguments['keyword'])
    else:
        return None


functions = {
    "scrap_google_news": scrap_google_news
}

function_call_res = get_function_call_result(news_gpt([
    {
        "role": "user",
        "content": "세계 경제에 대한 뉴스를 요약해줘"
    }
]), functions)

result = news_gpt([
    {
        "role": "user",
        "content": json.dumps(function_call_res, ensure_ascii=False)
    },
    {
        "role": "user",
        "content": "세계 경제에 대한 뉴스를 요약해줘"
    }
])

print(json.dumps(result, ensure_ascii=False, indent=2))
