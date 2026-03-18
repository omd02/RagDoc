import { useState } from "react"
import { useNavigate } from "react-router-dom"
import { useAuth } from "../auth/UseAuth"
import { Link } from "react-router-dom"
import { login as loginApi } from "../api/api"


export default function LoginPage() {

  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [error, setError] = useState("")

  const navigate = useNavigate()

  const { login } = useAuth()

  const handleLogin = async () => {

    setError("")

    try {

      const res = await loginApi(email, password)

      if (res.data.error) {
        setError(res.data.error)
        return
      }

      if (res.data.access_token) {
        login(res.data.access_token)
        navigate("/search")
      } else {
        setError("Invalid response from server")
      }

    } catch (err: any) {

      setError(err.response?.data?.detail || "Login failed")

    }

  }

  return (

    <div className="min-h-screen flex items-center justify-center bg-slate-900">

      <div className="bg-white p-8 rounded-xl w-96">

        <h1 className="text-2xl mb-6 font-semibold">Login</h1>

        {error && (
          <div className="bg-red-100 text-red-600 p-2 rounded mb-4 text-sm">
            {error}
          </div>
        )}

        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e)=>setEmail(e.target.value)}
          className="border p-2 w-full mb-3 rounded"
        />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e)=>setPassword(e.target.value)}
          className="border p-2 w-full mb-4 rounded"
        />

        <button
          onClick={handleLogin}
          className="bg-blue-500 hover:bg-blue-600 text-white w-full p-2 rounded mb-4 font-medium transition"
        >
          Login
        </button>

        <p className="text-sm text-center">
          Don't have an account?{" "}
          <Link to="/register" className="text-blue-600 hover:underline">
              Register
          </Link>
        </p>

      </div>

    </div>

  )

}