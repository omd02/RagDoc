import { useState, useRef } from "react"
import { uploadDocument } from "../api/api"
import { motion, AnimatePresence } from "framer-motion"

interface UploadPanelProps {
  refreshDocuments: () => void
}

export default function UploadPanel({ refreshDocuments }: UploadPanelProps) {
  const [file, setFile] = useState<File | null>(null)
  const [status, setStatus] = useState<"idle" | "uploading" | "success" | "error">("idle")
  const [isDragging, setIsDragging] = useState(false)
  const fileInputRef = useRef<HTMLInputElement>(null)

  const handleUpload = async (selectedFile?: File) => {
    const fileToUpload = selectedFile || file
    if (!fileToUpload) return

    setStatus("uploading")
    try {
      await uploadDocument(fileToUpload)
      setStatus("success")
      refreshDocuments()
      setFile(null)
      setTimeout(() => setStatus("idle"), 3000)
    } catch {
      setStatus("error")
      setTimeout(() => setStatus("idle"), 3000)
    }
  }

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(true)
  }

  const handleDragLeave = () => {
    setIsDragging(false)
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(false)
    const droppedFile = e.dataTransfer.files[0]
    if (droppedFile) {
      setFile(droppedFile)
      handleUpload(droppedFile)
    }
  }

  return (
    <motion.div 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-slate-800/50 backdrop-blur-xl border border-slate-700/50 p-8 rounded-3xl shadow-2xl overflow-hidden relative"
    >
      <div 
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={() => fileInputRef.current?.click()}
        className={`border-2 border-dashed rounded-2xl p-8 transition-all cursor-pointer flex flex-col items-center justify-center gap-4 ${
          isDragging ? "border-indigo-500 bg-indigo-500/10 scale-[1.02]" : "border-slate-700 hover:border-slate-600 hover:bg-slate-700/30"
        }`}
      >
        <input 
          type="file" 
          ref={fileInputRef}
          onChange={(e) => {
            const selected = e.target.files?.[0] || null
            setFile(selected)
            if (selected) handleUpload(selected)
          }}
          className="hidden" 
        />
        
        <div className={`w-16 h-16 rounded-full flex items-center justify-center transition-all ${
          status === "uploading" ? "bg-indigo-500/20 text-indigo-400 animate-pulse" : 
          status === "success" ? "bg-emerald-500/20 text-emerald-400" :
          status === "error" ? "bg-red-500/20 text-red-400" : "bg-slate-700 text-slate-400"
        }`}>
          {status === "uploading" ? (
            <svg xmlns="http://www.w3.org/2000/svg" className="w-8 h-8 animate-bounce" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>
          ) : status === "success" ? (
            <svg xmlns="http://www.w3.org/2000/svg" className="w-8 h-8" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
          ) : status === "error" ? (
            <svg xmlns="http://www.w3.org/2000/svg" className="w-8 h-8" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>
          ) : (
            <svg xmlns="http://www.w3.org/2000/svg" className="w-8 h-8" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>
          )}
        </div>

        <div className="text-center">
          <h3 className="text-lg font-bold text-white mb-1">
            {status === "uploading" ? "Uploading..." : status === "success" ? "Upload Successful!" : status === "error" ? "Upload Failed" : "Click or drag to upload"}
          </h3>
          <p className="text-sm text-slate-400">
            {file ? file.name : "Support PDF, TXT, DOCX (Max 10MB)"}
          </p>
        </div>
      </div>

      <AnimatePresence>
        {status === "uploading" && (
          <motion.div 
            initial={{ width: 0 }}
            animate={{ width: "100%" }}
            className="absolute bottom-0 left-0 h-1 bg-indigo-500 shadow-[0_0_10px_rgba(99,102,241,0.5)]"
          />
        )}
      </AnimatePresence>
    </motion.div>
  )
}