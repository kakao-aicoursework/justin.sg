import chromadb
import pandas as pd

client = chromadb.PersistentClient()
collections = client.list_collections()
collection_name = "k-drama"
drama_db = client.get_or_create_collection(name=collection_name)

drama_df = (pd.read_csv("kdrama.csv")
            .drop(["Aired Date", "Aired On", "Duration", "Content Rating", "Production companies", "Rank"], axis=1))

# 데이터 인덱스
ids = []
# 메타데이터
doc_meta = []
# 벡터로 변환 저장할 텍스트 데이터로 ChromaDB에 Embedding 데이터가 없으면 자동으로 벡터로 변환해서 저장
documents = []

for idx in range(len(drama_df)):
    item = drama_df.iloc[idx]
    id = item['Name'].lower().replace(' ', '-')
    document = f"{item['Name']}: {item['Synopsis']} : {str(item['Cast']).strip().lower()} : {str(item['Genre']).strip().lower()}"
    meta = {
        "rating": item['Rating']
    }

    ids.append(id)
    doc_meta.append(meta)
    documents.append(document)

# DB 저장
drama_db.add(
    documents=documents,
    metadatas=doc_meta,
    ids=ids
)
# DB 쿼리
drama_db.query(
    query_texts=["romantic comedy drama"],
    n_results=5,
)

print(drama_df.iloc[0])
