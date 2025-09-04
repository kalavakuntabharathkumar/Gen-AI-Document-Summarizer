import React, { useState } from 'react'
import { createRoot } from 'react-dom/client'
import axios from 'axios'

function App() {
  const [file, setFile] = useState<File | null>(null)
  const [token, setToken] = useState<string>('')
  const [docId, setDocId] = useState<string>('')
  const [summary, setSummary] = useState<string>('')
  const [status, setStatus] = useState<string>('')

  async function login() {
    const res = await axios.post('/api/login')
    setToken(res.data.token)
  }

  async function upload() {
    if (!file) return
    const form = new FormData()
    form.append('file', file)
    const res = await axios.post('/api/upload', form, { headers: { Authorization: `Bearer ${token}` } })
    setDocId(res.data.document_id)
    setStatus(res.data.status)
  }

  async function poll() {
    if (!docId) return
    const res = await axios.get(`/api/summary/${docId}`, { headers: { Authorization: `Bearer ${token}` } })
    setSummary(res.data.summary || '')
    setStatus(res.data.status)
  }

  return (
    <div style={{ maxWidth: 720, margin: '2rem auto', fontFamily: 'system-ui' }}>
      <h1>LexiSumm</h1>
      <button onClick={login}>Demo Login</button>
      <p>Token: {token ? '✅' : '—'}</p>
      <input type="file" onChange={e => setFile(e.target.files?.[0] || null)} />
      <button onClick={upload} disabled={!file || !token}>Upload</button>
      <button onClick={poll} disabled={!docId || !token}>Check Status</button>
      <p>Status: {status}</p>
      {summary && (<div><h3>Summary</h3><p>{summary}</p></div>)}
    </div>
  )
}

createRoot(document.getElementById('root')!).render(<App />)
