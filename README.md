# RagDoc - AI Powered Document Intelligence

RagDoc is a modern, high-performance Retrieval-Augmented Generation (RAG) system that allows you to interact with your documents using natural language. Upload PDFs, and ask complex questions to get precise, AI-generated answers with direct source citations.

## ✨ New Modern UI Features

The system has been completely overhauled with a focus on fluid user experience and premium aesthetics:

- **Glassmorphism Design:** A cohesive dark theme using semi-transparent materials and indigo accents.
- **Fluid Animations:** Powered by `framer-motion` for smooth layout transitions and state changes.
- **Interactive Sidebar:** Spring-animated collapsible sidebar to manage your document library.
- **Smart Upload:** Modern drag-and-drop interface with real-time progress feedback.
- **AI Insights:** Premium result display featuring AI avatars, source card highlights, and one-click copying.
- **Mobile Optimized:** Responsive layout that adapts to all screen sizes.

## 🚀 Key Features

- **End-to-End RAG Pipeline:** Automatic PDF processing, chunking, and vector indexing.
- **Vector Search:** Powered by FAISS for lightning-fast retrieval of relevant context.
- **Secure Auth:** JWT-based authentication system for private document storage.
- **Source Transparency:** Every AI answer includes exact references to pages and source text.

## 🛠️ Tech Stack

### Frontend
- **React 19 (TypeScript)**
- **Tailwind CSS** (Styling)
- **Framer Motion** (Animations)
- **Vite** (Build Tool)

### Backend
- **FastAPI** (Python)
- **FAISS** (Vector Database)
- **SQLite** (Metadata Database)
- **Groq/Transformers** (LLM & Embeddings)
- **PyPDF** (Document Ingestion)

## 📦 Getting Started

### Prerequisites
- Python 3.10+
- Node.js 18+
- Groq API Key (in `.env`)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repo-url>
   cd RagDoc
   ```

2. **Backend Setup**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   ```

4. **Environment Variables**
   Create a `.env` in the root:
   ```env
   GROQ_API_KEY=your_key_here
   DATABASE_URL=sqlite:///./storage/app.db
   SECRET_KEY=your_secret_key
   ```

5. **Run the Application**
   - **Backend:** `uvicorn src.api.server:app --reload`
   - **Frontend:** `npm run dev`

## 📄 License
This project is licensed under the MIT License.
