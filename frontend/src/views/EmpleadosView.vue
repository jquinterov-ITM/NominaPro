<template>
  <div class="page">
    <section class="page-head card">
      <div>
        <p class="eyebrow">Operación</p>
        <h2>Gestión de Empleados</h2>
        <p>Administra el maestro de empleados con una vista limpia y orientada a control.</p>
      </div>
      <div class="page-head__actions">
        <button class="button" @click="mostrarFormulario = true">➕ Nuevo Empleado</button>
      </div>
    </section>

    <p v-if="successMessage" class="feedback success">{{ successMessage }}</p>
    <p v-if="apiError" class="feedback error">{{ apiError }}</p>

    <!-- Formulario para crear o editar empleado -->
    <div v-if="mostrarFormulario" class="card panel-card mt-4">
      <header class="panel-card__header">Crear Empleado</header>
      <section>
        <form @submit.prevent="guardarEmpleado">
          <div class="flex two">
            <div class="field">
              <label>Nombre Completo</label>
              <input type="text" v-model="nuevoEmpleado.nombre" required />
            </div>
            <div class="field">
              <label>Identificación</label>
              <input type="text" v-model="nuevoEmpleado.identificacion" required />
            </div>
            <div class="field">
              <label>Tipo de Salario</label>
              <select v-model="nuevoEmpleado.tipo_salario" required>
                <option value="ORDINARIO">Ordinario</option>
                <option value="INTEGRAL">Integral (Mínimo 13 SMMLV)</option>
              </select>
            </div>
            <div class="field">
              <label>Salario Base (COP)</label>
              <input type="text" v-model="salarioBaseFormatted" placeholder="Ej: 1.500.000" required />
              <small class="error" v-if="errorSalario">{{ errorSalario }}</small>
              <small v-else-if="parametroVigente" class="hint">
                Salario integral mínimo del año {{ currentYear }}: $ {{ Number(parametroVigente.smmlv * 13).toLocaleString('es-CO') }}
              </small>
              <small v-else-if="cargandoParametros" class="hint">Validando parámetros legales...</small>
            </div>
          </div>
          
          <div class="mt-4 actions-row">
            <button type="submit" :disabled="cargando || !auth.isAuthenticated">{{ cargando ? 'Guardando...' : 'Guardar' }}</button>
            <button type="button" class="pseudo" @click="cerrarFormulario">Cancelar</button>
          </div>

          <p v-if="!auth.isAuthenticated" class="feedback hint">
            Inicia sesión en la portada para habilitar la creación y eliminación.
          </p>
        </form>
      </section>
    </div>

    <!-- Tabla de empleados -->
    <section class="card table-card mt-4">
    <table class="primary">
      <thead>
        <tr>
          <th>ID</th>
          <th>Nombre</th>
          <th>Identificación</th>
          <th>Tipo Salario</th>
          <th>Salario Base</th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr v-if="cargandoLista">
          <td colspan="6" class="text-center">Cargando...</td>
        </tr>
        <tr v-else-if="empleados.length === 0">
          <td colspan="6" class="text-center">No hay empleados registrados.</td>
        </tr>
        <tr v-for="emp in empleados" :key="emp.id">
          <td>{{ emp.id }}</td>
          <td>{{ emp.nombre }}</td>
          <td>{{ emp.documento }}</td>
          <td><span class="label">{{ emp.tipo_salario }}</span></td>
          <td>$ {{ Number(emp.salario_base).toLocaleString('es-CO') }}</td>
          <td>
            <button class="small bg-error" @click="eliminar(emp.id)">Eliminar</button>
          </td>
        </tr>
      </tbody>
    </table>
    </section>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

import api from '../services/api'
import { useAuthStore } from '../stores/auth'

const empleados = ref([])
const parametrosLegales = ref([])
const mostrarFormulario = ref(false)
const cargando = ref(false)
const cargandoLista = ref(false)
const cargandoParametros = ref(false)
const formError = ref('')
const errorSalario = ref('')
const apiError = ref('')
const successMessage = ref('')
const auth = useAuthStore()
const currentYear = new Date().getFullYear()

const empleadoVacio = {
  nombre: '',
  identificacion: '',
  tipo_salario: 'ORDINARIO',
  salario_base: null
}

const nuevoEmpleado = ref({ ...empleadoVacio })

const salarioBaseFormatted = computed({
  get: () => {
    if (!nuevoEmpleado.value.salario_base) return ''
    return Number(nuevoEmpleado.value.salario_base).toLocaleString('es-CO')
  },
  set: (newValue) => {
    // Quita todo lo que no sea número para calcular el valor real
    const stringNumerico = newValue.replace(/\D/g, '')
    nuevoEmpleado.value.salario_base = stringNumerico ? parseFloat(stringNumerico) : null
  }
})

const parametroVigente = computed(() => {
  return parametrosLegales.value.find((item) => item.anio === currentYear)
})

const obtenerMensajeError = (error, fallback) => {
  return error.response?.data?.message || error.response?.data?.detail || fallback
}

const cargarEmpleados = async () => {
  cargandoLista.value = true
  try {
    const res = await api.get('/empleados/')
    empleados.value = res.data
  } catch (error) {
    apiError.value = obtenerMensajeError(error, 'No se pudo cargar la lista de empleados.')
  } finally {
    cargandoLista.value = false
  }
}

const cargarParametros = async () => {
  cargandoParametros.value = true
  try {
    const res = await api.get('/parametros/')
    parametrosLegales.value = res.data
  } catch (error) {
    console.error('No se pudieron cargar los parámetros legales', error)
  } finally {
    cargandoParametros.value = false
  }
}

const validarEmpleado = () => {
  const nombre = nuevoEmpleado.value.nombre.trim()
  const documento = nuevoEmpleado.value.identificacion.trim()
  const salario = Number(nuevoEmpleado.value.salario_base)

  if (!nombre) return 'El nombre es obligatorio.'
  if (!documento) return 'La identificación es obligatoria.'
  if (!salario || salario <= 0) return 'El salario base debe ser mayor que cero.'

  if (nuevoEmpleado.value.tipo_salario === 'INTEGRAL' && parametroVigente.value) {
    const minimoIntegral = Number(parametroVigente.value.smmlv) * 13
    if (salario < minimoIntegral) {
      return `El salario integral para ${currentYear} debe ser al menos $ ${Number(minimoIntegral).toLocaleString('es-CO')}.`
    }
  }

  return ''
}

const guardarEmpleado = async () => {
  errorSalario.value = ''
  apiError.value = ''
  formError.value = ''
  successMessage.value = ''

  const validacion = validarEmpleado()
  if (validacion) {
    if (validacion.includes('salario integral')) {
      errorSalario.value = validacion
    } else {
      formError.value = validacion
    }
    return
  }
  
  cargando.value = true
  try {
    const payload = {
      nombre: nuevoEmpleado.value.nombre,
      documento: nuevoEmpleado.value.identificacion,
      tipo_salario: nuevoEmpleado.value.tipo_salario,
      salario_base: parseFloat(nuevoEmpleado.value.salario_base)
    }
    
    await api.post('/empleados/', payload)
    await cargarEmpleados()
    successMessage.value = 'Empleado creado correctamente.'
    cerrarFormulario(true)
  } catch (error) {
    apiError.value = obtenerMensajeError(error, 'Ocurrió un error interno en el motor de nómina (Backend).')
  } finally {
    cargando.value = false
  }
}

const cerrarFormulario = (mantenerMensaje = false) => {
  mostrarFormulario.value = false
  nuevoEmpleado.value = { ...empleadoVacio }
  errorSalario.value = ''
  apiError.value = ''
  formError.value = ''
  if (!mantenerMensaje) {
    successMessage.value = ''
  }
}

const eliminar = async (id) => {
  if (confirm("¿Estás seguro de eliminar este empleado?")) {
     try {
       await api.delete(`/empleados/${id}`)
       await cargarEmpleados()
       successMessage.value = 'Empleado eliminado correctamente.'
     } catch (error) {
       apiError.value = obtenerMensajeError(error, 'No se pudo eliminar el empleado.')
     }
  }
}

onMounted(() => {
  cargarEmpleados()
  cargarParametros()
})
</script>

<style scoped>
.page {
  display: grid;
  gap: 1rem;
}

.page-head {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 1rem;
  padding: 1.25rem 1.4rem;
  border: 1px solid rgba(30, 51, 77, 0.08);
  background: linear-gradient(180deg, #fff 0%, #f8fafc 100%);
}

.page-head h2 {
  margin: 0.35rem 0 0.35rem;
  color: #10253d;
}

.page-head p {
  margin: 0;
  color: #5f7084;
}

.page-head__actions {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
}

.eyebrow {
  margin: 0;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: #3f67a9;
  font-size: 0.75rem;
  font-weight: 700;
}

.panel-card,
.table-card {
  border: 1px solid rgba(30, 51, 77, 0.08);
  background: #fff;
}

.panel-card__header {
  padding-bottom: 0.75rem;
  margin-bottom: 1rem;
  border-bottom: 1px solid rgba(30, 51, 77, 0.08);
  font-weight: 700;
  color: #10253d;
}

.actions-row {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
}

.mt-4 { margin-top: 20px; }
.mt-2 { margin-top: 10px; }
.text-center { text-align: center; }
.feedback { margin: 10px 0 0; }
.feedback.success { color: #19692c; }
.feedback.error { color: #a61b1b; }
.feedback.hint { color: #5c6677; }
.hint { display: block; margin-top: 6px; color: #5c6677; }
</style>
