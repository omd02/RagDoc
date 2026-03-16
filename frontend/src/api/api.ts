import axios from "axios";

export interface SearchResult {
  text: string;
  source: string;
  page: number;
}

const API = axios.create({
  baseURL: "http://localhost:8000"
});

export const uploadDocument = async (file: File) => {
  const formData = new FormData();
  formData.append("file", file);

  return API.post("/upload", formData);
};

export const queryDocuments = async (query: string) => {
  return API.post("/query", null, {
    params: { query }
  });
};

export const getDocuments = async () => {
  return API.get("/documents");
};