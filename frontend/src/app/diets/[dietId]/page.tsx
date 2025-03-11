import { getDietById } from "@/services/api"

interface Props {
  params: {
    dietId: string
  }
}

export default async function DietDetailsPage({ params }: Props) {
  const diet = await getDietById(params.dietId)
  if (!diet) {
    return <p>Diet not found</p>
  }
  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">{diet.name}</h1>
      <p>{diet.description}</p>
      <p>Price: {diet.price} USD</p>
    </div>
  )
}
