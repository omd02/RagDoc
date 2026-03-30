import Layout from "../components/layout"
import UploadPanel from "../components/UploadPanel"
import QueryBox from "../components/QueryBox"
import Results from "../components/Results"
import { useState } from "react"
import type { QueryResponse } from "../api/api"
import { motion } from "framer-motion"

export default function SearchPage() {
  const [queryResponse, setQueryResponse] = useState<QueryResponse | null>(null)
  const [refreshKey, setRefreshKey] = useState(0)

  const refreshDocuments = () => {
    setRefreshKey((prev) => prev + 1)
  }

  return (
    <Layout refreshKey={refreshKey}>
      <div className="max-w-5xl mx-auto space-y-12 py-12 px-6">
        <motion.div 
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center space-y-4"
        >
          <h1 className="text-4xl font-extrabold text-white tracking-tight">
            Document <span className="text-indigo-500">Intelligence</span>
          </h1>
          <p className="text-slate-400 font-medium text-lg max-w-2xl mx-auto">
            Upload your documents and ask questions to extract insights instantly with AI.
          </p>
        </motion.div>

        <div className="grid grid-cols-1 gap-10">
          <UploadPanel refreshDocuments={refreshDocuments} />
          <div className="space-y-6">
            <QueryBox setQueryResponse={setQueryResponse} />
            <Results response={queryResponse} />
          </div>
        </div>
      </div>
    </Layout>
  )
}
