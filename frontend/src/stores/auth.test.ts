import { describe, it, expect, beforeEach } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useAuthStore } from '../stores/auth'

describe('Auth Store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    localStorage.clear()
  })

  it('debería iniciar con token null', () => {
    const auth = useAuthStore()
    expect(auth.token).toBeNull()
    expect(auth.isAuthenticated).toBe(false)
  })

  it('debería guardar token cuando se hace login', () => {
    const auth = useAuthStore()
    auth.login('fake-token', 'admin', ['RH_ADMIN'])

    expect(auth.token).toBe('fake-token')
    expect(auth.username).toBe('admin')
    expect(auth.roles).toEqual(['RH_ADMIN'])
    expect(auth.isAuthenticated).toBe(true)
    expect(localStorage.getItem('token')).toBe('fake-token')
  })

  it('debería limpiar todo al hacer logout', () => {
    const auth = useAuthStore()
    auth.login('fake-token', 'admin', ['RH_ADMIN'])
    auth.logout()

    expect(auth.token).toBeNull()
    expect(auth.username).toBe('')
    expect(auth.roles).toEqual([])
    expect(localStorage.getItem('token')).toBeNull()
  })

  it('debería restaurar sesión desde localStorage', () => {
    localStorage.setItem('token', 'restored-token')
    localStorage.setItem('username', 'admin')
    localStorage.setItem('roles', 'RH_ADMIN,PAYROLL_USER')

    const auth = useAuthStore()
    auth.restoreSession()

    expect(auth.token).toBe('restored-token')
    expect(auth.isAuthenticated).toBe(true)
  })
})
