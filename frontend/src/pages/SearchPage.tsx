import Layout from "../components/layout"
import UploadPanel from "../components/UploadPanel"
import QueryBox from "../components/QueryBox"
import Results from "../components/Results"
import { useState } from "react"
import type { SearchResult } from "../api/api"
const refreshDocuments = () => {
  setRefreshKey((prev) => prev + 1)
}

export default function SearchPage() {

  const [results, setResults] = useState<SearchResult[]>([])

  return (

    <Layout>

      <div className="max-w-3xl mx-auto space-y-6">

        <UploadPanel refreshDocuments={refreshDocuments}/>

        <QueryBox setResults={setResults} />

        <Results results={results} />

      </div>

    </Layout>

  )

}