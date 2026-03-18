import { createContext, useState } from "react"
import type { ReactNode } from "react"

interface AuthContextType {
  token: string | null
  login: (token: string) => void
  logout: () => void
}

interface AuthProviderProps {
  children: ReactNode
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

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

export default AuthContext