import { useState, useEffect } from 'react'
import ItemList, { type Item } from './components/ItemList'

function App() {
  const [items, setItems] = useState<Item[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetch('http://localhost:8000/api/v1/items')
      .then((res) => res.json())
      .then((data) => {
        setItems(data)
        setLoading(false)
      })
      .catch((err) => {
        setError(err.message)
        setLoading(false)
      })
  }, [])

  if (loading) return <div>Loading...</div>
  if (error) return <div>Error: {error}</div>

  return (
    <div className="App">
      <h1>Items List</h1>
      <ItemList items={items} />
    </div>
  )
}

export default App
