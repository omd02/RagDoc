import { Link, useNavigate } from "react-router-dom"
import { useAuth } from "../auth/UseAuth"
import { motion } from "framer-motion"

export default function Navbar() {
  const { logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate("/")
  }

  return (
    <nav className="w-full bg-slate-900/80 backdrop-blur-md border-b border-slate-800 text-white px-8 py-4 flex justify-between items-center sticky top-0 z-50">
      <motion.div 
        initial={{ opacity: 0, x: -20 }}
        animate={{ opacity: 1, x: 0 }}
        className="flex items-center gap-2"
      >
        <div className="w-10 h-10 bg-indigo-600 rounded-xl flex items-center justify-center shadow-lg shadow-indigo-500/20">
          <svg xmlns="http://www.w3.org/2000/svg" className="w-6 h-6" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"/><polyline points="14 2 14 8 20 8"/></svg>
        </div>
        <span className="font-extrabold text-2xl tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-white to-slate-400">
          RagDoc
        </span>
      </motion.div>

      <motion.div 
        initial={{ opacity: 0, x: 20 }}
        animate={{ opacity: 1, x: 0 }}
        className="flex gap-8 items-center"
      >
        <div className="flex gap-1">
          <Link to="/search" className="px-4 py-2 rounded-lg hover:bg-slate-800 transition-colors font-medium text-slate-300 hover:text-white">
            Search
          </Link>
          <Link to="/about" className="px-4 py-2 rounded-lg hover:bg-slate-800 transition-colors font-medium text-slate-300 hover:text-white">
            About
          </Link>
        </div>

        <button
          onClick={handleLogout}
          className="flex items-center gap-2 bg-slate-800 hover:bg-red-500/10 hover:text-red-400 text-slate-300 px-4 py-2 rounded-xl transition-all border border-slate-700 hover:border-red-500/30 font-semibold"
        >
          <svg xmlns="http://www.w3.org/2000/svg" className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>
          Logout
        </button>
      </motion.div>
    </nav>
  )
}