import { useState } from "react"
import axios from "axios"
import { useNavigate } from "react-router-dom"

export default function RegisterPage() {

  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")

  const navigate = useNavigate()

  const handleRegister = async () => {

    await axios.post("http://localhost:8000/register", {
      email,
      password
    })

    navigate("/")

  }

  return (

    <div className="min-h-screen flex items-center justify-center bg-slate-900">

      <div className="bg-white p-8 rounded-xl w-96">

        <h1 className="text-2xl mb-6">Register</h1>

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
          onClick={handleRegister}
          className="bg-green-500 text-white w-full p-2 rounded"
        >
          Register
        </button>

      </div>

    </div>

  )

}