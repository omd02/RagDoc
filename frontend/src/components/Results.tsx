import type { SearchResult } from "../api/api"
import { motion } from "framer-motion"

interface ResultsProps {
  results: SearchResult[]
}

export default function Results({ results }: ResultsProps) {

  if (!results || results.length === 0) {
    return (
      <p className="text-center text-gray-300">
        No results yet
      </p>
    )
  }

  return (

    <div className="space-y-4 w-full">

      <h2 className="text-xl font-semibold text-white">
        Results
      </h2>

      {results.map((r, i) => (

        <motion.div
          key={i}
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3 }}
          className="bg-white text-black p-5 rounded-xl shadow-lg w-full"
        >

          <p className="text-sm text-gray-500">
            {r.source} — Page {r.page}
          </p>

          <p className="mt-2 leading-relaxed">
            {r.text}
          </p>

        </motion.div>

      ))}

    </div>

  )

}