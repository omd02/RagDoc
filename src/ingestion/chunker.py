def chunk_documents(documents, chunk_size=300, overlap=50):
    """
    Split documents into overlapping chunks.

    Args:
        documents (list): list of document dicts with text and metadata
        chunk_size (int): number of words per chunk
        overlap (int): overlapping words between chunks

    Returns:
        list: chunked documents
    """

    chunks = []

    for doc in documents:

        text = doc["text"]
        metadata = doc["metadata"]

        words = text.split()

        start = 0

        while start < len(words):

            end = start + chunk_size

            chunk_words = words[start:end]
            chunk_text = " ".join(chunk_words)

            chunk = {
                "text": chunk_text,
                "metadata": metadata
            }

            chunks.append(chunk)

            start += chunk_size - overlap

    return chunks