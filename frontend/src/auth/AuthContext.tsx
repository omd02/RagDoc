import { createContext, useState, useContext } from "react"
import type { ReactNode } from "react"

interface AuthContextType {
  token: string | null
  login: (token: string) => void
  logout: () => void
}

interface AuthProviderProps {
  children: ReactNode
}

export const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: AuthProviderProps) {

  const [token, setToken] = useState<string | null>(
    localStorage.getItem("token")
  )

  const login = (token: string) => {
    localStorage.setItem("token", token)
    setToken(token)
  }

  const logout = () => {
    localStorage.removeItem("token")
    setToken(null)
  }

  return (
    <AuthContext.Provider value={{ token, login, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {

  const context = useContext(AuthContext)

  if (!context) {
    throw new Error("useAuth must be used inside AuthProvider")
  }

  return context
}