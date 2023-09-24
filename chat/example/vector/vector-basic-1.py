from gensim.models import Word2Vec
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

sentences = [
    item.split(" ") for item in [
        'this is a good product',
        'this is a excellent product',
        'it is a bad product',
        'it is the worst product',
    ]
]

model = Word2Vec(sentences, window=3, min_count=1, workers=1)
word_vectors = model.wv
word_vector_list = word_vectors.vectors

word_vectors.similarity('bad', 'good')
word_vectors.most_similar('bad')

# 2차원 변경
pca = PCA(n_components=2)
tdata = pca.fit_transform(word_vector_list)
vocabs = word_vectors.index_to_key

print(vocabs)

plt.figure(figsize=(8,6))
plt.scatter(tdata[:, 0], tdata[:,1], marker='o')
for i, v in enumerate(vocabs):
    plt.annotate(v, xy=(tdata[:, 0][i], tdata[: ,1][i]))
plt.show()
