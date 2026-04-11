import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import HomeView from '../views/HomeView.vue'
import { reactive, computed } from 'vue'

// Mock de useAuthStore
const mockAuth = reactive({
  isAuthenticated: false,
  displayName: 'Invitado',
  roleLabel: 'Sin roles',
  tokenPreview: '',
  loading: false,
  error: '',
  login: vi.fn(),
  logout: vi.fn()
})

vi.mock('../stores/auth', () => ({
  useAuthStore: () => mockAuth
}))

describe('HomeView.vue', () => {
  it('renderiza el título principal correctamente', () => {
    const wrapper = mount(HomeView, {
      global: {
        stubs: ['router-link']
      }
    })
    expect(wrapper.find('h1').text()).toContain('Controla empleados, novedades y liquidaciones')
  })

  it('muestra el formulario de login cuando no está autenticado', () => {
    mockAuth.isAuthenticated = false
    const wrapper = mount(HomeView, {
      global: {
        stubs: ['router-link']
      }
    })
    expect(wrapper.find('form.login-form').exists()).toBe(true)
    expect(wrapper.find('.session-box').exists()).toBe(false)
  })

  it('muestra la información de sesión cuando está autenticado', async () => {
    mockAuth.isAuthenticated = true
    mockAuth.displayName = 'Admin User'
    
    const wrapper = mount(HomeView, {
      global: {
        stubs: ['router-link']
      }
    })
    
    expect(wrapper.find('.session-box').exists()).toBe(true)
    expect(wrapper.find('.session-box').text()).toContain('Admin User')
    expect(wrapper.find('form.login-form').exists()).toBe(false)
  })

  it('llama a auth.logout al hacer clic en el botón de cerrar sesión', async () => {
    mockAuth.isAuthenticated = true
    const wrapper = mount(HomeView, {
      global: {
        stubs: ['router-link']
      }
    })

    await wrapper.find('button.bg-error').trigger('click')
    expect(mockAuth.logout).toHaveBeenCalled()
  })
})
