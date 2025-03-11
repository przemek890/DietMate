import { NextRequest, NextResponse } from "next/server"

export async function POST(request: NextRequest) {
  try {
    const { dietId, userData } = await request.json()
    const res = await fetch("http://127.0.0.1:5000/api/purchase", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ dietId, userData })
    })
    if (!res.ok) {
      throw new Error("Purchase failed")
    }
    const data = await res.json()
    return NextResponse.json(data, { status: 200 })
  } catch {
    return NextResponse.json({ error: "Purchase error" }, { status: 500 })
  }
}
