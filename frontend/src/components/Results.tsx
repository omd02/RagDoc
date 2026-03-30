import type { QueryResponse } from "../api/api"
import { motion, AnimatePresence } from "framer-motion"

interface ResultsProps {
  response: QueryResponse | null
}

export default function Results({ response }: ResultsProps) {
  if (!response) {
    return (
      <div className="flex flex-col items-center justify-center py-20 text-slate-500 gap-4 opacity-50">
        <svg xmlns="http://www.w3.org/2000/svg" className="w-16 h-16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1" strokeLinecap="round" strokeLinejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
        <p className="text-lg font-medium">Ready to answer your questions</p>
      </div>
    )
  }

  return (
    <div className="space-y-10 w-full mt-12">
      <AnimatePresence mode="wait">
        <motion.div
          key={response.answer}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="relative group"
        >
          {/* AI Answer Section */}
          <div className="absolute -left-12 top-0 hidden md:flex w-10 h-10 bg-indigo-600 rounded-full items-center justify-center shadow-lg shadow-indigo-500/20 text-white">
            <svg xmlns="http://www.w3.org/2000/svg" className="w-6 h-6" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M12 8V4H8"/><rect width="16" height="12" x="4" y="8" rx="2"/><path d="M2 14h2"/><path d="M20 14h2"/><path d="M15 13v2"/><path d="M9 13v2"/></svg>
          </div>

          <div className="bg-slate-800/40 backdrop-blur-xl border border-indigo-500/20 p-8 rounded-3xl shadow-2xl relative overflow-hidden">
            <div className="absolute top-0 right-0 p-4">
              <button 
                onClick={() => navigator.clipboard.writeText(response.answer)}
                className="p-2 hover:bg-white/5 rounded-lg text-slate-500 hover:text-white transition-colors"
                title="Copy to clipboard"
              >
                <svg xmlns="http://www.w3.org/2000/svg" className="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><rect width="14" height="14" x="8" y="8" rx="2" ry="2"/><path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/></svg>
              </button>
            </div>
            
            <h3 className="text-xs font-bold text-indigo-400 uppercase tracking-[0.2em] mb-4 flex items-center gap-2">
                <span className="w-1.5 h-1.5 bg-indigo-500 rounded-full animate-pulse" />
                AI Insight
            </h3>
            <div className="text-slate-200 text-lg leading-relaxed whitespace-pre-wrap font-medium">
                {response.answer}
            </div>
          </div>
        </motion.div>
      </AnimatePresence>

      {/* Sources Section */}
      <div className="space-y-6">
        <div className="flex items-center gap-4 px-2">
          <h2 className="text-lg font-bold text-white tracking-tight">
              Referenced Sources
          </h2>
          <div className="flex-1 h-px bg-slate-800" />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {response.context.map((r, i) => (
                <motion.div
                key={i}
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: i * 0.1 + 0.2 }}
                className="bg-slate-900/50 border border-slate-800 hover:border-indigo-500/30 p-5 rounded-2xl shadow-lg transition-all hover:translate-y-[-2px] group"
                >
                <div className="flex justify-between items-start mb-4">
                    <div className="flex items-center gap-2">
                      <div className="w-8 h-8 bg-slate-800 rounded-lg flex items-center justify-center text-indigo-400 border border-slate-700">
                        <svg xmlns="http://www.w3.org/2000/svg" className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"/><polyline points="14 2 14 8 20 8"/></svg>
                      </div>
                      <span className="text-xs font-bold text-slate-300 truncate max-w-[120px]">
                          {r.metadata.source}
                      </span>
                    </div>
                    <span className="text-[10px] font-bold text-slate-500 bg-slate-800 px-2 py-1 rounded-md uppercase tracking-tighter">
                        Page {r.metadata.page}
                    </span>
                </div>

                <div className="relative">
                  <svg xmlns="http://www.w3.org/2000/svg" className="absolute -left-1 -top-1 w-4 h-4 text-indigo-500/20" viewBox="0 0 24 24" fill="currentColor"><path d="M14.017 21L14.017 18C14.017 16.8954 14.9124 16 16.017 16H19.017C19.5693 16 20.017 15.5523 20.017 15V9C20.017 8.44772 19.5693 8 19.017 8H15.017C14.4647 8 14.017 8.44772 14.017 9V11C14.017 11.5523 13.5693 12 13.017 12H12.017C11.4647 12 11.017 11.5523 11.017 11V9C11.017 6.79086 12.8079 5 15.017 5H19.017C21.2261 5 23.017 6.79086 23.017 9V15C23.017 17.2091 21.2261 19 19.017 19H16.017C15.4647 19 15.017 19.4477 15.017 20V21H14.017ZM3.017 21L3.017 18C3.017 16.8954 3.91242 16 5.017 16H8.017C8.56928 16 9.017 15.5523 9.017 15V9C9.017 8.44772 8.56928 8 8.017 8H4.017C3.46472 8 3.017 8.44772 3.017 9V11C3.017 11.5523 2.56928 12 2.017 12H1.017C0.464718 12 0.0170002 11.5523 0.0170002 11V9C0.0170002 6.79086 1.80786 5 4.017 5H8.017C10.2261 5 12.017 6.79086 12.017 9V15C12.017 17.2091 10.2261 19 8.017 19H5.017C4.46472 19 4.017 19.4477 4.017 20V21H3.017Z"/></svg>
                  <p className="text-sm text-slate-400 line-clamp-4 leading-relaxed pl-4">
                      {r.text}
                  </p>
                </div>
                </motion.div>
            ))}
        </div>
      </div>
    </div>
  )
}

