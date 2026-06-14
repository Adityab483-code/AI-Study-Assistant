import faiss
import numpy as np

from sentence_transformers import SentenceTransformer

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


def create_chunks(
    pages,
    chunk_size=500,
    overlap=100
):

    chunks = []

    for page in pages:

        words = page["text"].split()

        start = 0

        while start < len(words):

            end = start + chunk_size

            chunk_text = " ".join(
                words[start:end]
            )

            chunks.append(
                {
                    "page": page["page"],
                    "text": chunk_text
                }
            )

            start += (
                chunk_size - overlap
            )

    return chunks


def create_vector_store(
    chunks
):

    texts = [
        chunk["text"]
        for chunk in chunks
    ]

    embeddings = (
        embedding_model.encode(
            texts
        )
    )

    index = faiss.IndexFlatL2(
        embeddings.shape[1]
    )

    index.add(
        np.array(
            embeddings,
            dtype="float32"
        )
    )

    return index


def retrieve_context(
    question,
    chunks,
    index,
    k=3
):

    question_embedding = (
        embedding_model.encode(
            [question]
        )
    )

    distances, indices = (
        index.search(
            np.array(
                question_embedding,
                dtype="float32"
            ),
            k
        )
    )

    context = []

    pages = []

    for idx in indices[0]:

        context.append(
            chunks[idx]["text"]
        )

        pages.append(
            chunks[idx]["page"]
        )

    return (
        "\n\n".join(context),
        list(set(pages))
    )