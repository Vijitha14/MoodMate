from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def retrieve_relevant_context(user_query, file_path="mood_knowledge.txt", top_k=3):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            knowledge_chunks = f.read().split("\n\n")  # assumes chunks are separated by blank lines

        corpus = knowledge_chunks + [user_query]
        vectorizer = TfidfVectorizer()
        vectors = vectorizer.fit_transform(corpus)

        similarity_scores = cosine_similarity(vectors[-1], vectors[:-1]).flatten()
        top_indices = similarity_scores.argsort()[-top_k:][::-1]
        top_chunks = [knowledge_chunks[i] for i in top_indices]

        return "\n".join(top_chunks)

    except Exception as e:
        print(f"Error loading knowledge base: {e}")
        return ""

