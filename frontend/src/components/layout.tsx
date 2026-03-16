import type { ReactNode } from "react"
import Navbar from "./Navbar"
import Sidebar from "./Sidebar"

interface LayoutProps {
  children: ReactNode
}

export default function Layout({ children }: LayoutProps) {

  return (

    <div className="h-screen flex flex-col">

      <Navbar />

      <div className="flex flex-1 overflow-hidden">

        <Sidebar />

        <main className="flex-1 bg-slate-900 text-white p-8 overflow-y-auto">

          {children}

        </main>

      </div>

    </div>

  )

}