import chromadb

client = chromadb.PersistentClient()
collections = client.list_collections()
collection_name = "posts"
posts = client.get_or_create_collection(name=collection_name)


def add_posts():
    list = [
        "apple is delicious",
        "banana is sweet",
        "New York is big",
        "Paris is romantic"
    ]

    ids = [index + 1 for index, item in enumerate(list)]
    posts.add(
        documents=list,
        ids=ids
    )


# add_posts()

result = posts.query(
    query_texts=["yellow"],
    n_results=1
)

print(result)
