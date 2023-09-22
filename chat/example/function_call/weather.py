import os

import openai
import json
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.environ.get('OPENAI_API_KEY')

def get_current_weather(location: str, unit="섭씨"):
    weather_info = {
        "location": location,
        "temperature": "24",
        "unit": unit,
        "forecast": ["sunny", "windy", "rain", "snow"]
    }

    return json.dumps(weather_info)


messages = [
    {"role": "user", "content": "오늘 서울 날씨 어때?"}
]

functions = [
    {
        "name": "get_current_weather",
        "description": "주어진 지역의 현재 날씨를 알려준다.",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "지역, 서울, 부산, 전남"
                },
                "unit": {
                    "type": "string",
                    "enum": ["섭씨", "화씨"]
                }
            }
        },
        "required": ["location"]
    }
]

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=messages,
    functions=functions,
    function_call="auto",
)
response_message = response["choices"][0]["message"]

# - 첫번째 응답은 어떤 function_call이 선택되었고 argument가 무엇인지만 확인할 수 있다.
# - 여러 function이 있을 수 있으니 dictionary로 만들어 보관한다.
# - 첫번째 응답의 메시지에 실제 동작할 function의 응답값을 포함하여 다시 호출한다.
# - 두번째 호출에는 functions, function_call 정보가 없이 그냥 메시지만 보낸다.
# - 첫번째 요청은 어떤 function_call을 사용할지 판단. 두번째가 진짜 질의



available_functions = {
    get_current_weather: get_current_weather
}

if response_message.get("function_call"):
    # Note: the JSON response may not always be valid; be sure to handle errors
    available_functions = {
        "get_current_weather": get_current_weather,
    }
    function_name = response_message["function_call"]["name"]
    fuction_to_call = get_current_weather
    function_args = json.loads(response_message["function_call"]["arguments"])
    function_response = fuction_to_call(
        location=function_args.get("location"),
        unit=function_args.get("unit"),
    )

    messages.append(response_message)
    messages.append(
        {
            "role": "function",
            "name": function_name,
            "content": function_response,
        }
    )

    second_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
    )


    json_data = json.dumps(second_response, ensure_ascii=False)

    print(second_response.choices[0].message.content)
