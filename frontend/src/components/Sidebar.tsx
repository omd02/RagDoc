import { useEffect, useState } from "react"
import { getDocuments, deleteDocument } from "../api/api"
import type { DocumentItem } from "../types/document"

interface SidebarProps {
  refreshKey?: number
}

export default function Sidebar({ refreshKey }: SidebarProps) {

  const [documents, setDocuments] = useState<DocumentItem[]>([])
  const [open, setOpen] = useState(true)

  useEffect(() => {

    const fetchDocuments = async () => {

      const res = await getDocuments()

      setDocuments(res.data.documents)

    }

    fetchDocuments()

  }, [refreshKey])

  const handleDelete = async (id: number) => {

    await deleteDocument(id)

    const res = await getDocuments()

    setDocuments(res.data.documents)

  }

  return (

    <div
      className={`bg-slate-800 text-white h-full transition-all duration-300 ${
        open ? "w-64" : "w-14"
      }`}
    >

      <button
        onClick={() => setOpen(!open)}
        className="p-4 text-lg"
      >
        ☰
      </button>

      {open && (

        <div className="p-4">

          <h2 className="mb-4 font-semibold">
            Documents
          </h2>

          <div className="space-y-2">

            {documents.map((doc) => (

              <div
                key={doc.id}
                className="flex justify-between items-center bg-slate-700 p-2 rounded"
              >

                <span className="truncate">
                  {doc.filename}
                </span>

                <button
                  onClick={() => handleDelete(doc.id)}
                  className="text-red-400"
                >
                  ✕
                </button>

              </div>

            ))}

          </div>

        </div>

      )}

    </div>

  )

}