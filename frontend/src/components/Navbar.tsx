import Link from "next/link"

export default function Navbar() {
  return (
    <nav className="bg-gray-200 py-4 text-center">
      <Link href="/" className="mx-4 font-semibold hover:underline text-black">
        Home
      </Link>
      <Link href="/diets" className="mx-4 font-semibold hover:underline text-black">
        Diets
      </Link>
    </nav>
  )
}
