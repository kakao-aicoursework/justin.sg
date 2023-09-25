import os
from typing import List

from dotenv import load_dotenv
from langchain.docstore.document import Document
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma

from chat.search.Search import Search

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.environ.get('OPENAI_API_KEY')
search = Search()


class ManualVectorDB:
    manual_file_path = "./manual.txt"
    collection_name = "manual"
    collection_persist_directory = "./manual_persist"
    collection = None
    chunk_size = 500
    chunk_overlap = 100
    db = Chroma(
        persist_directory="./manual_persist",
        embedding_function=OpenAIEmbeddings(),
        collection_name=collection_name,
    )
    search_url = [
        "https://developers.kakao.com/docs/latest/ko/kakaologin/rest-api"
    ]

    def create(self, leaning_messages: List[str]):
        input_text_list = self.load_file()
        search_text_list = [search.query(url) for url in self.search_url]

        self.add_embeddings(input_text_list)
        self.add_embeddings(search_text_list)

        leaning_messages.append("Croma Collection 생성이 완료 되었습니다.")
        leaning_messages.append("Manual File 데이터의 Document 등록이 완료 되었습니다.")
        leaning_messages.append("Search 데이터의 Document 등록이 완료 되었습니다.")


    def load_file(self) -> List[str]:
        def to_dic(input_text: str):
            # 빈문자 제거
            lines = [item for item in input_text.strip().splitlines() if item != ""]
            result = []
            key = None
            content = ""

            for line in lines:
                if line.startswith('#'):
                    if key is not None:
                        result.append({"key": key, "content": content.strip()})
                    key = line.strip('#')
                    content = ""
                else:
                    content += line + "\n"

            if key is not None:
                result.append({"key": key, "content": content.strip()})

            return [f"{text_item.get('key')}" "\n" f"{text_item.get('content')}" "\n" for text_item in result]

        # '#' 기준으로 split 해서 list(key, content) 형태로 구성한다.
        with open(self.manual_file_path, "r") as f:
            prompt_template = f.read()

        print("Success loading Text file.")
        return to_dic(prompt_template)

    def add_embeddings(self, text_list: List[str]):
        text_splitter = CharacterTextSplitter(chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap)
        documents = text_splitter.split_documents(
            [Document(page_content=text) for text in text_list]
        )

        # Chroma DB에 Document 저장
        self.db.from_documents(
            documents,
            # 어떤 Embedding 기법을 사용할지 지정하는 코드 (OpenAIEmbeddings을 사용하겠다.)
            OpenAIEmbeddings(),
            collection_name=self.collection_name,
            persist_directory=self.collection_persist_directory,
        )

        print("Success adding embedding documents")

    def query(self, query: str, max_document_size: int = 3):
        docs = self.db.similarity_search(query=query, k=max_document_size)

        return [doc.page_content for doc in docs]
