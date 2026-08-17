import { useEffect, useState, useCallback } from 'react'
import { fetchWaitlist, updateStatus, fetchSmsQuota } from './api.js'
import AddPartyForm from './components/AddPartyForm.jsx'
import WaitlistCard from './components/WaitlistCard.jsx'
import logo from './assets/logo.jpg'

export default function App() {
  const [entries, setEntries] = useState([])
  const [error, setError] = useState(false)
  const [showClosed, setShowClosed] = useState(false)
  const [busyId, setBusyId] = useState(null)
  const [smsQuota, setSmsQuota] = useState(null)


  const load = useCallback(async () => {
    try {
      const data = await fetchWaitlist()
      setEntries(data)
      setError(false)
    } catch (err) {
      setError(true)
    }
  }, [])

  useEffect(() => {
    load()
    const interval = setInterval(load, 10000)
    fetchSmsQuota().then(data => setSmsQuota(data)).catch(() => setSmsQuota(null))
    return () => clearInterval(interval)
  }, [load])

  async function handleAction(id, status) {
    setBusyId(id)
    try {
      await updateStatus(id, status)
      await load()
    } catch (err) {
      setError(true)
    } finally {
      setBusyId(null)
    }
  }

  const active = entries
    .filter(e => e.status === 'waiting' || e.status === 'notified')
    .sort((a, b) => new Date(a.joined_at) - new Date(b.joined_at))

  const closed = entries
    .filter(e => ['seated', 'no_show', 'cancelled'].includes(e.status))
    .sort((a, b) => new Date(b.joined_at) - new Date(a.joined_at))

  const waitingCount = entries.filter(e => e.status === 'waiting').length
  const notifiedCount = entries.filter(e => e.status === 'notified').length
  const seatedCount = entries.filter(e => e.status === 'seated').length

  return (
    <>
      <div className="topbar">

        <div className="brand">
          <img src={logo} alt="Otis logo" className="brand-logo" />
          <span>Otis Waitlist</span>
        </div>

        <div className="stats">
          <div>Quota<b>{smsQuota !== null ? smsQuota : 'Loading...'}</b></div>
          <div>Waiting<b>{waitingCount}</b></div>
          <div>Notified<b>{notifiedCount}</b></div>
          <div>Seated today<b>{seatedCount}</b></div>
        </div>

      </div>

      <div className="wrap">
        <AddPartyForm onAdded={load} />

        <div>
          <div className="list-head">
            <h1>Current queue</h1>
          </div>

          {error && <div className="top-error">Can't reach the server. Make sure the API is running.</div>}

          <div className="rail">
            {active.length === 0 ? (
              <div className="empty-state">No one's waiting right now.</div>
            ) : (
              active.map((entry, i) => (
                <WaitlistCard
                  key={entry.id}
                  entry={entry}
                  position={i + 1}
                  onAction={handleAction}
                  busy={busyId === entry.id}
                />
              ))
            )}
          </div>

          {closed.length > 0 && (
            <>
              <button className="closed-toggle" onClick={() => setShowClosed(!showClosed)}>
                {showClosed ? 'Hide closed tickets' : `Show closed tickets (${closed.length})`}
              </button>
              {showClosed && (
                <div className="closed-rail open">
                  {closed.map((entry, i) => (
                    <WaitlistCard
                      key={entry.id}
                      entry={entry}
                      position={i + 1}
                      onAction={handleAction}
                      busy={busyId === entry.id}
                    />
                  ))}
                </div>
              )}
            </>
          )}
        </div>
      </div>
    </>
  )
}
