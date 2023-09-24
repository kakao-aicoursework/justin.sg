import chromadb

client = chromadb.PersistentClient()
collections = client.list_collections()
collection_name = "k-drama"
drama_db = client.get_or_create_collection(name=collection_name)
