import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class Generator:

    def __init__(self, model_id="llama3-8b-8192"):
        """
        Using llama3-8b-8192 for faster, more memory-efficient responses on free tiers.
        """
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            # Fallback or warning instead of immediate crash to allow server to start
            print("WARNING: GROQ_API_KEY not found. LLM features will be unavailable.")
            self.client = None
        else:
            self.client = Groq(api_key=api_key)
        self.model_id = model_id

    def generate(self, query: str, context: list[dict]):
        if not self.client:
            return "Error: Groq API key is not configured. Please set GROQ_API_KEY in your .env file."

        # Extract context text from chunks
        context_text = "\n\n".join([f"Source: {c['metadata'].get('source', 'Unknown')}\n{c['text']}" for c in context])

        # Create system message
        system_message = (
            "You are a highly accurate and helpful AI assistant specialized in document analysis. "
            "Your goal is to answer questions based strictly on the provided context. "
            "Guidelines:\n"
            "1. Use ONLY the provided context to answer the question.\n"
            "2. If the context does not contain enough information, politely state that you cannot answer based on the provided documents.\n"
            "3. Be clear, concise, and professional.\n"
            "4. If there are multiple relevant parts in the context, synthesize them into a coherent answer.\n"
            "5. Cite the source if available (e.g., 'According to [source]...')."
        )

        # Create user prompt
        user_prompt = (
            f"Context provided below:\n"
            f"---------------------\n"
            f"{context_text}\n"
            f"---------------------\n"
            f"Question: {query}\n\n"
            f"Helpful and Accurate Answer:"
        )

        try:
            # Generate response
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": system_message,
                    },
                    {
                        "role": "user",
                        "content": user_prompt,
                    }
                ],
                model=self.model_id,
                temperature=0.1, # Slight temperature for better flow while maintaining accuracy
            )

            return chat_completion.choices[0].message.content
        except Exception as e:
            return f"Error during generation: {str(e)}"

class DocumentGrader:
    def __init__(self, model_id="llama3-8b-8192"):
        api_key = os.environ.get("GROQ_API_KEY")
        self.client = Groq(api_key=api_key) if api_key else None
        self.model_id = model_id

    def grade(self, query: str, document_text: str) -> bool:
        """
        Grades a document's relevance to the query.
        Returns True if relevant, False otherwise.
        """
        if not self.client:
            return True # Fallback if no API key

        # Only use the first 1500 chars for grading to save tokens and improve speed
        snippet = document_text[:1500]

        prompt = (
            f"You are a grader assessing relevance of a retrieved document to a user question. \n"
            f"Retrieved document snippet: \n\n {snippet} \n\n"
            f"User question: {query} \n\n"
            f"If the document contains keyword(s) or semantic meaning related to the user question, grade it as relevant. \n"
            f"Give a binary score 'yes' or 'no' score to indicate whether the document is relevant to the question."
        )

        try:
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.model_id,
                temperature=0,
            )
            score = response.choices[0].message.content.strip().lower()
            return "yes" in score
        except:
            return True # Default to true on error
