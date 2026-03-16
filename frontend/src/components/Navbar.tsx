import { Link, useNavigate } from "react-router-dom"
import { useAuth } from "../auth/UseAuth"

export default function Navbar() {

  const { logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate("/")
  }

  return (

    <div className="w-full bg-slate-900 text-white px-6 py-4 flex justify-between items-center shadow">

      <div className="font-bold text-xl">
        RagDoc
      </div>

      <div className="flex gap-6 items-center">

        <Link to="/search" className="hover:text-indigo-400">
          Search
        </Link>

        <Link to="/about" className="hover:text-indigo-400">
          About
        </Link>

        <button
          onClick={handleLogout}
          className="bg-red-500 px-3 py-1 rounded"
        >
          Logout
        </button>

      </div>

    </div>

  )

}