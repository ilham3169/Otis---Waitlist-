import { useState } from 'react'
import { addParty } from '../api.js'

export default function AddPartyForm({ onAdded }) {
  const [name, setName] = useState('')
  const [phone, setPhone] = useState('')
  const [partySize, setPartySize] = useState(2)
  const [notes, setNotes] = useState('')
  const [error, setError] = useState(false)
  const [submitting, setSubmitting] = useState(false)

  async function handleSubmit(e) {
    e.preventDefault()
    setError(false)
    setSubmitting(true)
    try {
      await addParty({
        name: name.trim(),
        phone_number: phone.trim(),
        party_size: parseInt(partySize, 10),
        notes: notes.trim() || null
      })
      setName('')
      setPhone('')
      setPartySize(2)
      setNotes('')
      onAdded()
    } catch (err) {
      setError(true)
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <form className="panel" onSubmit={handleSubmit}>
      <h2>Add to waitlist</h2>
      <p className="sub">Enter the party's details to add them to the queue.</p>

      <div className="field">
        <label htmlFor="name">Name</label>
        <input
          id="name"
          type="text"
          required
          placeholder="Party name"
          autoComplete="off"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
      </div>

      <div className="field-row">
        <div className="field">
          <label htmlFor="phone">Phone number</label>
          <input
            id="phone"
            type="tel"
            required
            placeholder="+1XXXXXXXXXX"
            autoComplete="off"
            value={phone}
            onChange={(e) => setPhone(e.target.value)}
          />
        </div>
        <div className="field narrow">
          <label htmlFor="party">Party</label>
          <input
            id="party"
            type="number"
            min="1"
            required
            value={partySize}
            onChange={(e) => setPartySize(e.target.value)}
          />
        </div>
      </div>

      <div className="field">
        <label htmlFor="notes">Notes (optional)</label>
        <textarea
          id="notes"
          placeholder="High chair, patio preferred, etc."
          value={notes}
          onChange={(e) => setNotes(e.target.value)}
        />
      </div>

      <button type="submit" className="btn btn-primary" disabled={submitting}>
        {submitting ? 'Adding…' : 'Add party'}
      </button>
      {error && <div className="form-error">Couldn't add that party. Check the fields and try again.</div>}
    </form>
  )
}
