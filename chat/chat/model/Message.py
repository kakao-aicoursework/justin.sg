from pynecone.base import Base


class Message(Base):
    origin_input_text: str
    result_text: str
    created_at: str
