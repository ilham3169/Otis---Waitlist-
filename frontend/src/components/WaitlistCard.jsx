import { sendSMS, updateStatus } from '../api.js'

const STATUS_LABEL = {
  waiting: "Waiting",
  notified: "Table ready",
  seated: "Seated",
  no_show: "No-show",
  cancelled: "Cancelled"
}

function minutesSince(dateStr) {
  const iso = dateStr.endsWith('Z') ? dateStr : dateStr + 'Z'
  const diffMs = Date.now() - new Date(iso).getTime()
  return Math.max(0, Math.round(diffMs / 60000))
}

async function handleNotify(entry) {
  try {
    console.log(`Sending SMS to ${entry.phone_number}...`);
    await sendSMS(entry.phone_number);
    await updateStatus(entry.id, 'notified');
  } catch (err) {
    console.error('Failed to notify guest:', err);
  }
}


export default function WaitlistCard({ entry, position, onAction, busy }) {
  const mins = minutesSince(entry.joined_at)

  return (
    <div className="card">
      <div className="pos">{position}</div>
      <div className="info">
        <h3>{entry.name}</h3>
        <div className="line">
          <span>{entry.party_size} {entry.party_size === 1 ? 'guest' : 'guests'}</span>
          <span>&middot;</span>
          <span>{entry.phone_number}</span>
          <span>&middot;</span>
          <span>{mins} min</span>
        </div>
        {entry.notes && <div className="notes">{entry.notes}</div>}
      </div>
      <div className="right">
        <span className={`badge ${entry.status}`}>{STATUS_LABEL[entry.status]}</span>
        <div className="actions">
          {entry.status === 'waiting' && (
            <>
              <button className="action-btn primary" disabled={busy} onClick={() => handleNotify(entry)}>Notify</button>
              <button className="action-btn danger" disabled={busy} onClick={() => onAction(entry.id, 'cancelled')}>Cancel</button>
            </>
          )}
          {entry.status === 'notified' && (
            <>
              <button className="action-btn primary" disabled={busy} onClick={() => onAction(entry.id, 'seated')}>Seat</button>
              <button className="action-btn danger" disabled={busy} onClick={() => onAction(entry.id, 'no_show')}>No-show</button>
            </>
          )}
        </div>
      </div>
    </div>
  )
}
