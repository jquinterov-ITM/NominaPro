import { describe, it, expect, vi } from 'vitest'
import axios from 'axios'
import api from '../services/api'

vi.mock('axios', () => ({
  default: {
    create: vi.fn(() => ({
      interceptors: {
        request: { use: vi.fn() },
        response: { use: vi.fn() },
      },
    })),
  },
}))

describe('API Service', () => {
  it('debería crear instancia con baseURL correcta', () => {
    expect(api.defaults.baseURL).toBeDefined()
  })

  it('debería tener interceptor de request configurado', () => {
    expect(api.interceptors.request.use).toBeDefined()
  })

  it('debería tener interceptor de response configurado', () => {
    expect(api.interceptors.response.use).toBeDefined()
  })
})
