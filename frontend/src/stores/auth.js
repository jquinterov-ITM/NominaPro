import { computed, ref, reactive } from 'vue'

import api from '../services/api'

const TOKEN_KEY = 'nominapro_token'
const USERNAME_KEY = 'nominapro_username'
const ROLES_KEY = 'nominapro_roles'

const decodeTokenPayload = (token) => {
  const payloadPart = token.split('.')[1] || ''
  const normalized = payloadPart.replace(/-/g, '+').replace(/_/g, '/')
  const padded = normalized.padEnd(Math.ceil(normalized.length / 4) * 4, '=')

  try {
    return JSON.parse(atob(padded))
  } catch {
    return {}
  }
}

const readRoles = () => {
  try {
    const raw = localStorage.getItem(ROLES_KEY)
    return raw ? JSON.parse(raw) : []
  } catch {
    return []
  }
}

const token = ref(localStorage.getItem(TOKEN_KEY) || '')
const username = ref(localStorage.getItem(USERNAME_KEY) || '')
const roles = ref(readRoles())
const loading = ref(false)
const error = ref('')

const persistSession = () => {
  if (token.value) {
    localStorage.setItem(TOKEN_KEY, token.value)
    localStorage.setItem(USERNAME_KEY, username.value)
    localStorage.setItem(ROLES_KEY, JSON.stringify(roles.value))
    return
  }

  localStorage.removeItem(TOKEN_KEY)
  localStorage.removeItem(USERNAME_KEY)
  localStorage.removeItem(ROLES_KEY)
}

const applyToken = (nextToken) => {
  token.value = nextToken
  if (!nextToken) {
    username.value = ''
    roles.value = []
    persistSession()
    return
  }

  const payload = decodeTokenPayload(nextToken)
  username.value = payload.sub || payload.username || ''
  roles.value = Array.isArray(payload.roles) ? payload.roles : []
  persistSession()
}

const hydrateSession = () => {
  const storedToken = localStorage.getItem(TOKEN_KEY) || ''
  if (!storedToken) {
    return
  }

  const payload = decodeTokenPayload(storedToken)
  token.value = storedToken
  username.value = payload.sub || payload.username || localStorage.getItem(USERNAME_KEY) || ''
  roles.value = Array.isArray(payload.roles) ? payload.roles : readRoles()

  if (!username.value) {
    token.value = ''
    roles.value = []
    persistSession()
    return
  }

  persistSession()
}

hydrateSession()

const login = async (inputUsername, password) => {
  loading.value = true
  error.value = ''

  try {
    const formData = new URLSearchParams()
    formData.append('username', inputUsername)
    formData.append('password', password)

    const response = await api.post('/auth/token', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    })

    applyToken(response.data.access_token)
    return response.data
  } catch (requestError) {
    error.value = requestError.response?.data?.message || requestError.response?.data?.detail || 'No se pudo iniciar sesión.'
    throw requestError
  } finally {
    loading.value = false
  }
}

const logout = () => {
  error.value = ''
  applyToken('')
}

const authState = reactive({
  token,
  username,
  roles,
  loading,
  error,
  isAuthenticated: computed(() => Boolean(token.value)),
  displayName: computed(() => username.value || 'Invitado'),
  roleLabel: computed(() => (roles.value.length ? roles.value.join(', ') : 'Sin roles')),
  tokenPreview: computed(() => (token.value ? `${token.value.slice(0, 18)}...` : '')),
  login,
  logout
})

export function useAuthStore() {
  return authState
}