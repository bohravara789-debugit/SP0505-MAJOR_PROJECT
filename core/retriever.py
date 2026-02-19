import numpy as np

def retrieve(query_embedding, index, chunks, top_k=4):
    D, I = index.search(
        np.array([query_embedding]).astype("float32"), top_k
    )
    return [chunks[i] for i in I[0]]

