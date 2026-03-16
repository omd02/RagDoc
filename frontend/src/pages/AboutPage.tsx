import Layout from "../components/layout"

export default function AboutPage() {

  return (

    <Layout>

      <div className="max-w-3xl mx-auto space-y-6">

        <h1 className="text-3xl font-bold">
          About RagDoc
        </h1>

        <p>
          RagDoc is an AI-powered document search tool built using a
          Retrieval-Augmented Generation (RAG) pipeline.
        </p>

        <p>
          Users can upload PDF documents, which are automatically processed,
          chunked, and converted into vector embeddings. These embeddings are
          stored in a vector database and allow the system to retrieve relevant
          sections of a document based on natural language questions.
        </p>

        <p>
          The system is built using:
        </p>

        <ul className="list-disc pl-6 space-y-2">
          <li>FastAPI backend</li>
          <li>FAISS vector search</li>
          <li>SQLite database</li>
          <li>React + Tailwind frontend</li>
        </ul>

        <p>
          This project demonstrates how modern AI systems combine document
          retrieval and language models to create intelligent search
          applications.
        </p>

      </div>

    </Layout>

  )

}