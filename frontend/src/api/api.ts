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

export const register = (email: string, password: string) => {
  return API.post("/register", { email, password })
}

export const login = (email: string, password: string) => {
  return API.post("/login", { email, password })
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

export const uploadDocument = (file: File) => {

  const formData = new FormData()
  formData.append("file", file)

  return API.post("/upload", formData, {
    headers: {
      "Content-Type": "multipart/form-data"
    }
  })

}
