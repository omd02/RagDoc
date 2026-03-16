import { useState } from "react";
import { uploadDocument } from "../api/api";

export default function UploadPanel() {

  const [file, setFile] = useState<File | null>(null);
  const [status, setStatus] = useState("");

  const handleUpload = async () => {

    if (!file) return;

    setStatus("Uploading...");

    try {
      await uploadDocument(file);
      setStatus("Document indexed successfully");
    } catch {
      setStatus("Upload failed");
    }

  };

  return (
    <div className="bg-white/90 backdrop-blur p-6 rounded-xl shadow-xl w-full">

      <h2 className="text-xl font-semibold mb-4">
        Upload PDF
      </h2>

      <input
        type="file"
        onChange={(e) => setFile(e.target.files?.[0] || null)}
        className="mb-4"
      />

      <button
        onClick={handleUpload}
        className="px-4 py-2 bg-blue-500 text-white rounded"
      >
        Upload
      </button>

      <p className="mt-3 text-sm">{status}</p>

    </div>
  );
}