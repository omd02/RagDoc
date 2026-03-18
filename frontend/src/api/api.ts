import axios from "axios"

export interface SearchResult {
  text: string
  source: string
  page: number
}

const API = axios.create({
  baseURL: "http://localhost:8000"
})

API.interceptors.request.use((config) => {

  const token = localStorage.getItem("token")

  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }

  return config

})

export const uploadDocument = (file: File) => {

  const formData = new FormData()
  formData.append("file", file)

  return API.post("/upload", formData)

}

export const getDocuments = () => {

  return API.get("/documents")

}

export const deleteDocument = (id: number) => {

  return API.delete(`/documents/${id}`)

}

export const queryDocuments = (query: string) => {

  return API.post("/query", null, {
    params: { query }
  })

}