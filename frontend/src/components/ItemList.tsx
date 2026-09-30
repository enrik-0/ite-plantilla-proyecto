// ponytail: shared type lives here, no separate types/ file until a second consumer needs it
export interface Item {
  id: string
  name: string
  description: string
  created_at: string
}

export default function ItemList({ items }: { items: Item[] }) {
  return (
    <ul>
      {items.map((item) => (
        <li key={item.id}>
          <strong>{item.name}</strong>: {item.description}
        </li>
      ))}
    </ul>
  )
}
