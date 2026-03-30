import { useState } from "react";
import { queryDocuments } from "../api/api";
import type { QueryResponse } from "../api/api";
import { motion } from "framer-motion";

interface QueryBoxProps {
  setQueryResponse: (response: QueryResponse) => void;
}

export default function QueryBox({ setQueryResponse }: QueryBoxProps) {
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSearch = async () => {
    if (!query) return;
    setLoading(true);

    try {
        const response = await queryDocuments(query);
        setQueryResponse(response.data);
    } catch (error) {
        console.error("Search error:", error);
    } finally {
        setLoading(false);
    }
  };

  return (
    <motion.div 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.1 }}
      className="bg-slate-800/40 backdrop-blur-xl border border-slate-700/50 p-1 rounded-2xl shadow-2xl w-full"
    >
      <div className="flex gap-2 p-2">
        <div className="flex-1 relative flex items-center">
          <div className="absolute left-4 text-slate-500">
            <svg xmlns="http://www.w3.org/2000/svg" className="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>
          </div>
          <input
              type="text"
              placeholder="Ask anything about your documents..."
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              className="w-full bg-slate-900/50 border border-slate-700/50 pl-12 pr-4 py-4 rounded-xl focus:border-indigo-500/50 focus:ring-2 focus:ring-indigo-500/20 focus:outline-none transition-all text-white placeholder-slate-500 font-medium text-lg"
              onKeyDown={(e) => e.key === "Enter" && handleSearch()}
          />
        </div>

        <button
            onClick={handleSearch}
            disabled={loading || !query}
            className={`px-8 py-4 rounded-xl font-bold text-white transition-all flex items-center gap-2 shadow-lg ${
                loading ? "bg-slate-700 cursor-not-allowed" : 
                !query ? "bg-slate-800 text-slate-500 cursor-not-allowed" : 
                "bg-indigo-600 hover:bg-indigo-500 active:scale-95 shadow-indigo-500/20"
            }`}
        >
            {loading ? (
              <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
            ) : (
              <svg xmlns="http://www.w3.org/2000/svg" className="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="m5 12 7-7 7 7"/><path d="M12 19V5"/></svg>
            )}
            <span>{loading ? "Thinking..." : "Ask"}</span>
        </button>
      </div>
    </motion.div>
  );
}

