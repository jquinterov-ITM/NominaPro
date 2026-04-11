import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount, flushPromises } from '@vue/test-utils'
import EmpleadosView from '../views/EmpleadosView.vue'
import api from '../services/api'
import { reactive } from 'vue'

// Mocks
vi.mock('../services/api')
const mockAuth = reactive({
  isAuthenticated: false
})
vi.mock('../stores/auth', () => ({
  useAuthStore: () => mockAuth
}))

describe('EmpleadosView.vue', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    api.get.mockResolvedValue({ data: [] })
  })

  it('muestra mensaje de carga inicialmente', async () => {
    // Mock diferido
    api.get.mockReturnValue(new Promise(() => {})) // Nunca resuelve para ver carga
    
    const wrapper = mount(EmpleadosView)
    // Forzar un tick para que onMounted dispare cargarEmpleados
    await wrapper.vm.$nextTick()
    
    expect(wrapper.text()).toContain('Cargando...')
  })

  it('renderiza la lista de empleados cuando la API responde', async () => {
    const mockEmpleados = [
      { id: 1, nombre: 'Juan Perez', documento: '12345', tipo_salario: 'ORDINARIO', salario_base: 1500000 },
      { id: 2, nombre: 'Maria Lopez', documento: '67890', tipo_salario: 'INTEGRAL', salario_base: 20000000 }
    ]
    
    // Configurar respuestas para las dos llamadas sucesivas (empleados y parámetros)
    api.get.mockResolvedValueOnce({ data: mockEmpleados })
    api.get.mockResolvedValueOnce({ data: [] })

    const wrapper = mount(EmpleadosView)
    
    // Esperar a que se resuelvan todas las promesas (onMounted -> cargarEmpleados)
    await flushPromises()

    expect(wrapper.text()).toContain('Juan Perez')
    expect(wrapper.text()).toContain('Maria Lopez')
    expect(wrapper.findAll('tbody tr').length).toBe(2)
  })

  it('muestra el formulario de creación al hacer clic en el botón', async () => {
    const wrapper = mount(EmpleadosView)
    await wrapper.find('button.success').trigger('click')
    
    expect(wrapper.find('form').exists()).toBe(true)
    expect(wrapper.find('header').text()).toBe('Crear Empleado')
  })

  it('deshabilita el botón de guardar si el usuario no está autenticado', async () => {
    mockAuth.isAuthenticated = false
    const wrapper = mount(EmpleadosView)
    await wrapper.find('button.success').trigger('click') // Abrir form

    const submitBtn = wrapper.find('button[type="submit"]')
    expect(submitBtn.attributes('disabled')).toBeDefined()
    expect(wrapper.text()).toContain('Inicia sesión en la portada para habilitar la creación')
  })
})
