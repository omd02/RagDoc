import { useState } from "react"
import { uploadDocument } from "../api/api"

interface UploadPanelProps {
  refreshDocuments: () => void
}

export default function UploadPanel({
  refreshDocuments,
}: UploadPanelProps): JSX.Element {

  const [file, setFile] = useState<File | null>(null)
  const [status, setStatus] = useState("")

  const handleUpload = async () => {

    if (!file) return

    setStatus("Uploading...")

    try {

      await uploadDocument(file)

      setStatus("Upload successful")

      refreshDocuments()

    } catch {

      setStatus("Upload failed")

    }

  }

  return (

    <div className="bg-white/90 backdrop-blur text-black p-6 rounded-xl shadow-lg">

      <h2 className="text-xl font-semibold mb-4">
        Upload Document
      </h2>

      <input
        type="file"
        onChange={(e) => setFile(e.target.files?.[0] || null)}
        className="mb-4"
      />

      <button
        onClick={handleUpload}
        className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded"
      >
        Upload
      </button>

      <p className="mt-3 text-sm text-gray-600">
        {status}
      </p>

    </div>

  )
}