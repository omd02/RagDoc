import Layout from "../components/layout"
import UploadPanel from "../components/UploadPanel"
import QueryBox from "../components/QueryBox"
import Results from "../components/Results"
import { useState } from "react"
import type { SearchResult } from "../api/api"

export default function SearchPage() {

  const [results, setResults] = useState<SearchResult[]>([])
  const [refreshKey, setRefreshKey] = useState(0)

  const refreshDocuments = () => {
    setRefreshKey((prev) => prev + 1)
  }

  return (

    <Layout refreshKey={refreshKey}>

      <div className="max-w-3xl mx-auto space-y-6">

        <UploadPanel refreshDocuments={refreshDocuments} />

        <QueryBox setResults={setResults} />

        <Results results={results} />

      </div>

    </Layout>

  )

}