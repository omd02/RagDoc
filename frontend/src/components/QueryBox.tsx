import { useState } from "react";
import { queryDocuments } from "../api/api";
import type { SearchResult } from "../api/api";
interface QueryBoxProps {
  setResults: (results: SearchResult[]) => void;
}

export default function QueryBox({ setResults }: QueryBoxProps) {

  const [query, setQuery] = useState("");

  const handleSearch = async () => {

    if (!query) return;

    const response = await queryDocuments(query);

    setResults(response.data.results);

  };

  return (

    <div className="border border-gray-300 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-400 p-3 w-full rounded mb-4 outline-none transition">

      <h2 className="text-xl font-semibold mb-4">
        Ask a Question
      </h2>

      <input
        type="text"
        placeholder="What is machine learning?"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        className="border p-2 w-full mb-4"
      />

      <button
        onClick={handleSearch}
        className="px-4 py-2 bg-green-500 text-white rounded"
      >
        Search
      </button>

    </div>
  );
}