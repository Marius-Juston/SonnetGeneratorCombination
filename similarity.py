import multiprocessing

from gensim.models.doc2vec import TaggedDocument, Doc2Vec
from gensim.test.utils import get_tmpfile

lines = []

with open("sonnets2.txt", 'r') as f:
    transform = map(lambda x: tuple(x.lower().strip().split()), f.readlines())
    transform = set(transform)
    lines = filter(lambda x: len(x) != 0 and x[0] != '-------------------------------------------------------',
                   transform)
    # lines = fil
    # lines = set(lines)

documents = {i: TaggedDocument(doc, [i]) for i, doc in enumerate(lines)}
model = Doc2Vec(documents.values(), vector_size=100, window=300, min_count=1, workers=multiprocessing.cpu_count(),
                alpha=0.0001, epochs=5000)
print(model.epochs)
print(model.alpha)

fname = get_tmpfile("my_doc2vec_model")
model.save(fname)
model = Doc2Vec.load(fname)

model.delete_temporary_training_data(keep_doctags_vectors=True, keep_inference=True)

tokens = "How do I love you? Let me count the ways.".lower().split()

new_vector = model.infer_vector(tokens)
sims = model.docvecs.most_similar([new_vector])

for id, probability in sims:
    print(" ".join(documents[id].words), probability)
