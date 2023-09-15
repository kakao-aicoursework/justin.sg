"""Welcome to Pynecone! This file outlines the steps to create a basic app."""

import pynecone as pc
from chat import style
from chat.State import State
from chat.gpt.gpt import dictionary


def chat_wrap() -> pc.Component:
    return pc.box(
        pc.foreach(State.messages, lambda message: pc.box(
            # 질의
            pc.box(pc.text(message.origin_input_text, style=style.question_style), text_align="right"),

            # 응답 message.created_at
            pc.box(
                pc.text(message.result_text), pc.text(message.created_at, font_size="13px", margin_top="10px"),
                style=style.answer_style, text_align="left"),
        )),
        margin_bottom="30px"
    )


def language_wrap() -> pc.Component:
    languages = list(dictionary.keys())

    return pc.hstack(
        pc.select(
            languages,
            value=State.src_language,
            on_change=State.set_src_language,
            margin_top="1rem",
        ),
        pc.select(
            languages,
            value=State.target_language,
            on_change=State.set_target_language,
            margin_top="1rem",
        ),
        margin_bottom="50px"
    )


def action_bar_wrap() -> pc.Component:
    return pc.hstack(
        pc.input(
            placeholder="번역할 문장을 입력하세요.",
            on_blur=State.set_input_text,
            style=style.input_style,
        ),
        pc.button("번역", on_click=State.submit, style=style.button_style),
    )


def index() -> pc.Component:
    return pc.container(
        language_wrap(),
        chat_wrap(),
        action_bar_wrap(),
    )


app = pc.App(state=State)
app.add_page(index)
app.compile()
