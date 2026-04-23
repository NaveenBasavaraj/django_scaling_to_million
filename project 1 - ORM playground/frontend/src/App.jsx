import { useEffect, useState } from 'react'

const API_BASE = import.meta.env.VITE_API_BASE || '/api'
const DEFAULT_QUERY = 'Customer.objects.all()'

function App() {
  const [resources, setResources] = useState([])
  const [resourceError, setResourceError] = useState('')
  const [queryText, setQueryText] = useState(DEFAULT_QUERY)
  const [queryOutput, setQueryOutput] = useState('')
  const [queryError, setQueryError] = useState('')
  const [isRunning, setIsRunning] = useState(false)

  useEffect(() => {
    const load = async () => {
      const names = ['customers', 'categories', 'products', 'orders']
      const data = await Promise.all(
        names.map(async (name) => {
          const response = await fetch(`${API_BASE}/${name}/`)
          if (!response.ok) throw new Error(`Failed to fetch ${name}`)
          const body = await response.json()
          return { name, count: body.count ?? body.length ?? 0 }
        })
      )
      setResources(data)
      setResourceError('')
    }

    load().catch(() => {
      setResources([])
      setResourceError('Could not load datasets. Check backend/CORS configuration.')
    })
  }, [])

  const runQuery = async () => {
    const expression = queryText.trim()
    if (!expression) {
      setQueryError('Please enter an ORM expression.')
      setQueryOutput('')
      return
    }

    setIsRunning(true)
    setQueryError('')

    try {
      const response = await fetch(`${API_BASE}/orm-query/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ expression }),
      })
      const body = await response.json()
      if (!response.ok) {
        setQueryOutput('')
        setQueryError(body.detail || `Request failed with status ${response.status}`)
      } else {
        setQueryOutput(JSON.stringify(body.result, null, 2))
      }
    } catch (_error) {
      setQueryOutput('')
      setQueryError('Request failed. Check backend availability.')
    } finally {
      setIsRunning(false)
    }
  }

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
        {resourceError && <p className="error">{resourceError}</p>}
        <ul>
          {resources.map((item) => (
            <li key={item.name}>
              <strong>{item.name}</strong>
              <span>{item.count} rows</span>
            </li>
          ))}
        </ul>
      </section>

      <section className="panel">
        <h2>Query Runner</h2>
        <p className="hint">
          Enter ORM expressions like <code>Customer.objects.all()</code> or{' '}
          <code>Order.objects.filter(quantity=1).count()</code>
        </p>
        <textarea
          className="query-box"
          value={queryText}
          onChange={(event) => setQueryText(event.target.value)}
          placeholder="Customer.objects.all()"
          rows={3}
        />
        <button className="run-btn" type="button" onClick={runQuery} disabled={isRunning}>
          {isRunning ? 'Running...' : 'Run Query'}
        </button>
        {queryError && <p className="error">{queryError}</p>}
        <pre className="output">{queryOutput || 'Run a query to view JSON output here.'}</pre>
      </section>
    </main>
  )
}

export default App
