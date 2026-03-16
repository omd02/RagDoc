import { useState } from "react"
import axios from "axios"
import { useNavigate } from "react-router-dom"
import { useAuth } from "../auth/UseAuth"

export default function LoginPage() {

  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")

  const navigate = useNavigate()

  const { login } = useAuth()

  const handleLogin = async () => {

    const res = await axios.post("http://localhost:8000/login", {
      email,
      password
    })

    login(res.data.access_token)

    navigate("/search")

  }

  return (

    <div className="min-h-screen flex items-center justify-center bg-slate-900">

      <div className="bg-white p-8 rounded-xl w-96">

        <h1 className="text-2xl mb-6">Login</h1>

        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e)=>setEmail(e.target.value)}
          className="border p-2 w-full mb-3"
        />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e)=>setPassword(e.target.value)}
          className="border p-2 w-full mb-4"
        />

        <button
          onClick={handleLogin}
          className="bg-blue-500 text-white w-full p-2 rounded"
        >
          Login
        </button>

      </div>

    </div>

  )

}