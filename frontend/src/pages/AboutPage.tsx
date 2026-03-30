import Layout from "../components/layout"
import { motion } from "framer-motion"

export default function AboutPage() {
  const features = [
    { title: "FastAPI Backend", desc: "High-performance, modern Python framework for building APIs.", icon: "⚡" },
    { title: "FAISS Vector Search", desc: "Efficient similarity search and clustering of dense vectors.", icon: "🔍" },
    { title: "SQLite Storage", desc: "Reliable and lightweight relational database for metadata.", icon: "📁" },
    { title: "React + Tailwind", desc: "Modern, responsive, and highly customizable user interface.", icon: "🎨" }
  ]

  return (
    <Layout>
      <div className="max-w-4xl mx-auto py-12 px-6">
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="space-y-12"
        >
          <div className="text-center space-y-4">
            <h1 className="text-5xl font-extrabold text-white tracking-tight">
              About <span className="text-indigo-500">RagDoc</span>
            </h1>
            <p className="text-xl text-slate-400 max-w-2xl mx-auto leading-relaxed">
              An advanced AI-powered document intelligence tool leveraging Retrieval-Augmented Generation (RAG).
            </p>
          </div>

          <div className="bg-slate-900/40 backdrop-blur-xl border border-slate-800 p-8 rounded-[2.5rem] shadow-2xl space-y-6">
            <p className="text-lg text-slate-300 leading-relaxed">
              RagDoc transforms static documents into interactive knowledge bases. By combining state-of-the-art 
              language models with efficient vector retrieval, it allows you to "talk" to your data with 
              unprecedented precision.
            </p>
            <p className="text-lg text-slate-300 leading-relaxed">
              When you upload a document, RagDoc automatically processes, chunks, and indexes it into a 
              high-dimensional vector space. When you ask a question, the system retrieves only the most 
              relevant context to generate accurate, source-backed answers.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {features.map((f, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: i * 0.1 + 0.2 }}
                className="bg-slate-900/40 border border-slate-800 p-6 rounded-3xl hover:border-indigo-500/30 transition-all hover:translate-y-[-4px] group"
              >
                <div className="text-3xl mb-4 bg-slate-800 w-12 h-12 flex items-center justify-center rounded-2xl group-hover:scale-110 transition-transform">
                  {f.icon}
                </div>
                <h3 className="text-xl font-bold text-white mb-2">{f.title}</h3>
                <p className="text-slate-400 leading-relaxed">{f.desc}</p>
              </motion.div>
            ))}
          </div>

          <div className="text-center pt-8">
            <p className="text-slate-500 font-medium italic">
              Built for speed, accuracy, and ease of use.
            </p>
          </div>
        </motion.div>
      </div>
    </Layout>
  )
}