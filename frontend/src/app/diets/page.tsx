import { getDiets } from "@/services/api"

export default async function DietsPage() {
  const diets = await getDiets()
  return (
    <div>
      <h2 className="text-2xl font-bold mb-4">Available Diets</h2>
      <ul className="list-disc list-inside space-y-2">
        {diets.map(diet => (
          <li key={diet.id}>
            <a href={`/diets/${diet.id}`} className="text-blue-600 hover:underline">
              {diet.name}
            </a>
            {" "}
            {diet.price} USD
          </li>
        ))}
      </ul>
    </div>
  )
}
