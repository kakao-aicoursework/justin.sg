"""Welcome to Pynecone! This file outlines the steps to create a basic app."""

import pynecone as pc

from chat import style
from chat.State import State


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


def action_bar_wrap() -> pc.Component:
    return pc.hstack(
        pc.input(
            placeholder="질문을 입력하세요.",
            on_blur=State.set_input_text,
            style=style.input_style,
        ),
        pc.button("질문", on_click=State.submit_handler, style=style.button_style),
    )


def loading() -> pc.Component:
    return pc.cond(
        State.is_working,
        pc.box(pc.spinner(color="lightgreen", thickness=5, speed="1.5s", size="xl"), style=style.spinner_style)
    )


def leaning_wrap() -> pc.Component:
    return pc.hstack(
        pc.box(
            pc.foreach(State.leaning_messages, lambda message: pc.box(
                pc.text(message, style=style.answer_style)
            )), width="100%"
        ),
        pc.button("학습", on_click=State.leaning_handler, style=style.button_style),
        margin_top="50px;"
    )


def index() -> pc.Component:
    return pc.container(
        leaning_wrap(),
        chat_wrap(),
        action_bar_wrap(),
        loading(),
    )


app = pc.App(state=State)
app.add_page(index)
app.compile()
