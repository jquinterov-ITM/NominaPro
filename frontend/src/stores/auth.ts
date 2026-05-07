import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(localStorage.getItem('token'))
  const username = ref<string>(localStorage.getItem('username') || '')
  const roles = ref<string[]>([])

  const isAuthenticated = computed(() => !!token.value)

  const login = (newToken: string, user?: string, userRoles?: string[]) => {
    token.value = newToken
    localStorage.setItem('token', newToken)
    if (user) {
      username.value = user
      localStorage.setItem('username', user)
    }
    if (userRoles) {
      roles.value = userRoles
      localStorage.setItem('roles', userRoles.join(','))
    }
  }

  const logout = () => {
    token.value = null
    username.value = ''
    roles.value = []
    localStorage.removeItem('token')
    localStorage.removeItem('username')
    localStorage.removeItem('roles')
  }

  const restoreSession = () => {
    token.value = localStorage.getItem('token')
    username.value = localStorage.getItem('username') || ''
    const storedRoles = localStorage.getItem('roles')
    roles.value = storedRoles ? storedRoles.split(',') : []
  }

  const initToken = () => {
    restoreSession()
  }

  return { token, username, roles, isAuthenticated, login, logout, restoreSession, initToken }
})
