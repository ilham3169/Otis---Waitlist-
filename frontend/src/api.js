const API_BASE = "http://127.0.0.1:8000"

export async function fetchWaitlist() {
  const res = await fetch(`${API_BASE}/waitlist/all-users`)
  if (!res.ok) throw new Error('Failed to fetch waitlist')
  return res.json()
}

export async function addParty(payload) {
  const res = await fetch(`${API_BASE}/waitlist/create`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  })
  if (!res.ok) throw new Error('Failed to add party')
  return res.json()
}

export async function updateStatus(id, status) {
  const res = await fetch(`${API_BASE}/waitlist/edit/${id}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ status })
  })
  if (!res.ok) throw new Error('Failed to update entry')
  return res.json()
}

export async function sendSMS(phoneNumber) {
  const res = await fetch(`${API_BASE}/sms/send-notify`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ number: phoneNumber })
  })
  if (!res.ok) throw new Error('Failed to send SMS')
  return res.json()
}

export async function fetchSmsQuota() {
  const res = await fetch(`${API_BASE}/sms/quota`, {
    method: 'POST'  })
  if (!res.ok) throw new Error('Failed to fetch quota')
  const data = await res.json()
  return data
}
