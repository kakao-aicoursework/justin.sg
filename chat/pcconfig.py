import pynecone as pc

class ChatConfig(pc.Config):
    pass

config = ChatConfig(
    app_name="chat",
    db_url="sqlite:///pynecone.db",
    env=pc.Env.DEV,
)