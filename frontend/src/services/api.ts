// src/services/api.ts

export interface Diet {
    id: number
    name: string
    description: string
    price: number
  }
  
  export interface UserData {
    name: string
    email?: string
  }
  
  export interface PurchaseResponse {
    message: string
  }
  
  const BASE_URL = "http://127.0.0.1:5000"
  
  export async function getDiets(): Promise<Diet[]> {
    const res = await fetch(`${BASE_URL}/api/diets`)
    if (!res.ok) {
      throw new Error("Error fetching diets")
    }
    const data = await res.json() as { diets: Diet[] }
    return data.diets
  }
  
  export async function getDietById(dietId: string): Promise<Diet | null> {
    const res = await fetch(`${BASE_URL}/api/diets/${dietId}`)
    if (res.status === 404) {
      return null
    }
    if (!res.ok) {
      throw new Error("Error fetching diet")
    }
    return (await res.json()) as Diet
  }
  
  export async function purchaseDiet(
    dietId: number,
    userData: UserData
  ): Promise<PurchaseResponse> {
    const res = await fetch("/api/purchase", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ dietId, userData })
    })
    if (!res.ok) {
      throw new Error("Error purchasing diet")
    }
    return (await res.json()) as PurchaseResponse
  }
  