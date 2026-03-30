import { useEffect, useState } from "react"
import { getDocuments, deleteDocument } from "../api/api"
import type { DocumentItem } from "../types/document"
import { motion, AnimatePresence } from "framer-motion"

interface SidebarProps {
  refreshKey?: number
}

export default function Sidebar({ refreshKey }: SidebarProps) {
  const [documents, setDocuments] = useState<DocumentItem[]>([])
  const [open, setOpen] = useState(true)

  useEffect(() => {
    const fetchDocuments = async () => {
      try {
        const res = await getDocuments()
        setDocuments(res.data.documents)
      } catch (error) {
        console.error("Failed to fetch documents:", error)
      }
    }
    fetchDocuments()
  }, [refreshKey])

  const handleDelete = async (id: number) => {
    try {
      await deleteDocument(id)
      const res = await getDocuments()
      setDocuments(res.data.documents)
    } catch (error) {
      console.error("Failed to delete document:", error)
    }
  }

  return (
    <motion.div
      animate={{ width: open ? 320 : 80 }}
      transition={{ type: "spring", stiffness: 300, damping: 30 }}
      className="bg-slate-900 border-r border-slate-800 text-slate-300 h-full flex flex-col overflow-hidden relative"
    >
      <div className="p-6 flex items-center justify-between">
        {open && (
          <motion.h2 
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="text-xs font-bold text-slate-500 uppercase tracking-widest"
          >
            My Documents
          </motion.h2>
        )}
        <button
          onClick={() => setOpen(!open)}
          className="p-2 rounded-lg hover:bg-slate-800 transition-colors text-slate-400 hover:text-white"
        >
          {open ? (
            <svg xmlns="http://www.w3.org/2000/svg" className="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="m15 18-6-6 6-6"/></svg>
          ) : (
            <svg xmlns="http://www.w3.org/2000/svg" className="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="m9 18 6-6-6-6"/></svg>
          )}
        </button>
      </div>

      <div className="flex-1 overflow-y-auto px-4 py-2 custom-scrollbar">
        <AnimatePresence mode="popLayout">
          {documents.map((doc) => (
            <motion.div
              layout
              key={doc.id}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              className={`group flex items-center gap-3 p-3 rounded-xl transition-all cursor-default mb-2 ${
                open ? "hover:bg-slate-800 border border-transparent hover:border-slate-700" : "justify-center"
              }`}
            >
              <div className="min-w-[40px] h-10 bg-indigo-500/10 rounded-lg flex items-center justify-center text-indigo-400 group-hover:scale-110 transition-transform">
                <svg xmlns="http://www.w3.org/2000/svg" className="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"/><polyline points="14 2 14 8 20 8"/></svg>
              </div>

              {open && (
                <>
                  <span className="flex-1 truncate text-sm font-medium group-hover:text-white transition-colors">
                    {doc.filename}
                  </span>
                  <button
                    onClick={() => handleDelete(doc.id)}
                    className="opacity-0 group-hover:opacity-100 p-1.5 hover:bg-red-500/20 rounded-md text-red-500 transition-all transform hover:scale-110"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M3 6h18"/><path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"/><path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"/><line x1="10" y1="11" x2="10" y2="17"/><line x1="14" y1="11" x2="14" y2="17"/></svg>
                  </button>
                </>
              )}
            </motion.div>
          ))}
        </AnimatePresence>
        
        {open && documents.length === 0 && (
          <div className="text-center py-10 opacity-30 italic text-sm">
            No documents yet
          </div>
        )}
      </div>

      <div className="p-4 border-t border-slate-800">
        <button className={`w-full flex items-center gap-3 p-3 rounded-xl bg-indigo-600 text-white font-bold transition-all shadow-lg shadow-indigo-500/20 active:scale-95 hover:bg-indigo-500 ${!open && "justify-center"}`}>
          <svg xmlns="http://www.w3.org/2000/svg" className="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M12 5v14M5 12h14"/></svg>
          {open && <span>Upload Document</span>}
        </button>
      </div>
    </motion.div>
  )
}