let getAuthUser = () => { try { return JSON.parse(localStorage.getItem('skillproof_auth_user') || 'null') } catch { return null } }
const request = async (url, options = {}) => {
  const user = getAuthUser();
  const headers = { 'Content-Type': 'application/json', ...(options.headers || {}) }
  if (user?.uid) headers['X-User-Id'] = user.uid
  const response = await fetch(url, { ...options, headers })
  if (!response.ok) { const body = await response.json().catch(() => ({})); throw new Error(body.detail || `Request failed: ${response.status}`) }
  return response.json()
}
export const api = {
  profile: () => request('/api/profile'), register: (data) => request('/api/profile/register', { method: 'POST', body: JSON.stringify(data) }), updateProfile: (data) => request('/api/profile', { method: 'PUT', body: JSON.stringify(data) }),
  tasks: () => request('/api/tasks'), task: (id) => request(`/api/tasks/${id}`), startSession: (taskId) => request('/api/sessions', { method: 'POST', body: JSON.stringify({ task_id: taskId }) }), session: (id) => request(`/api/sessions/${id}`),
  resume: () => request('/api/sessions/resume'), saveVersion: (sessionId, code, workspace_state, note = '') => request(`/api/sessions/${sessionId}/versions`, { method: 'POST', body: JSON.stringify({ code, workspace_state, note }) }),
  run: (sessionId, code, workspace_state) => request(`/api/sessions/${sessionId}/run`, { method: 'POST', body: JSON.stringify({ code, workspace_state }) }),
  mentor: (sessionId, message, code = '', workspace_state = {}, history = []) => request(`/api/sessions/${sessionId}/mentor`, { method: 'POST', body: JSON.stringify({ message, code, workspace_state, history }) }),
  evaluate: (sessionId) => request(`/api/sessions/${sessionId}/evaluate`, { method: 'POST' }), submitCheck: (sessionId, answers) => request(`/api/sessions/${sessionId}/understanding-check`, { method: 'POST', body: JSON.stringify({ answers }) }),
  evidence: () => request('/api/evidence'), evidenceOne: (id) => request(`/api/evidence/${id}`)
}
