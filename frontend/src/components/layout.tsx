import type { ReactNode } from "react"
import Navbar from "./Navbar"
import Sidebar from "./Sidebar"
import { motion, AnimatePresence } from "framer-motion"

interface LayoutProps {
  children: ReactNode
  refreshKey?: number
}

export default function Layout({ children , refreshKey }: LayoutProps) {
  return (
    <div className="h-screen flex flex-col bg-[#020617] text-white overflow-hidden">
      <Navbar />
      <div className="flex flex-1 overflow-hidden relative">
        {/* Background decorative elements */}
        <div className="absolute top-0 right-0 w-[500px] h-[500px] bg-indigo-600/5 rounded-full blur-[120px] -z-10" />
        <div className="absolute bottom-0 left-0 w-[500px] h-[500px] bg-blue-600/5 rounded-full blur-[120px] -z-10" />
        
        <Sidebar refreshKey={refreshKey} />
        
        <main className="flex-1 overflow-y-auto custom-scrollbar relative">
          <AnimatePresence mode="wait">
            <motion.div
              key={window.location.pathname}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              transition={{ duration: 0.3 }}
              className="min-h-full"
            >
              {children}
            </motion.div>
          </AnimatePresence>
        </main>
      </div>
    </div>
  )
}