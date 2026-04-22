import { useEffect, useState } from 'react'

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000/api'

function App() {
  const [resources, setResources] = useState([])

  useEffect(() => {
    const load = async () => {
      const names = ['customers', 'categories', 'products', 'orders']
      const data = await Promise.all(
        names.map(async (name) => {
          const response = await fetch(`${API_BASE}/${name}/`)
          const body = await response.json()
          return { name, count: body.count ?? body.length ?? 0 }
        })
      )
      setResources(data)
    }

    load().catch(() => setResources([]))
  }, [])

  return (
    <main className="page">
      <section className="hero">
        <p className="eyebrow">Django ORM Learning Project</p>
        <h1>ORM Playground</h1>
        <p className="subtitle">
          Practice query thinking using read-only APIs backed by PostgreSQL.
        </p>
      </section>

      <section className="panel">
        <h2>Available Data Sets</h2>
        <ul>
          {resources.map((item) => (
            <li key={item.name}>
              <strong>{item.name}</strong>
              <span>{item.count} rows</span>
            </li>
          ))}
        </ul>
      </section>
    </main>
  )
}

export default App
