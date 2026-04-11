<template>
  <div>
    <h2>Registro de Novedades</h2>
    <div class="flex">
      <button class="success" @click="mostrarFormulario = true">➕ Nueva Novedad</button>
    </div>

    <p v-if="successMessage" class="feedback success">{{ successMessage }}</p>
    <p v-if="apiError" class="feedback error">{{ apiError }}</p>

    <!-- Formulario para nueva novedad -->
    <div v-if="mostrarFormulario" class="card mt-4">
      <header>Registrar Novedad Mensual</header>
      <section>
        <form @submit.prevent="guardarNovedad">
          <div class="flex two">
            <div class="field">
              <label>Empleado</label>
              <select v-model="nuevaNovedad.empleado_id" required>
                <option value="" disabled>Seleccione un empleado...</option>
                <option v-for="emp in empleados" :key="emp.id" :value="emp.id">
                  {{ emp.nombre }} ({{ emp.documento }})
                </option>
              </select>
            </div>
            
            <div class="field">
              <label>Mes de Causación (Período)</label>
              <input type="month" v-model="nuevaNovedad.periodo" required />
            </div>
            
            <div class="field">
              <label>Tipo de Novedad</label>
              <select v-model="nuevaNovedad.tipo" required>
                <option value="HORA_EXTRA">Horas Extras / Recargos</option>
                <option value="INCAPACIDAD">Incapacidad Médica</option>
                <option value="DESCUENTO">Descuento Administrativo</option>
                <option value="BONIFICACION">Bonificación / Comisión</option>
              </select>
            </div>
            
            <div class="field">
              <label>Valor Monetario (COP)</label>
              <input type="text" v-model="valorFormatted" placeholder="Ej: 50.000" required />
            </div>
          </div>
          
          <div v-if="apiError" class="pseudo button error mt-2">
             Error: {{ apiError }}
          </div>
          
          <div class="mt-4">
            <button type="submit" :disabled="cargando || !auth.isAuthenticated">{{ cargando ? 'Guardando...' : 'Guardar Novedad' }}</button>
            <button type="button" class="pseudo" @click="cerrarFormulario">Cancelar</button>
          </div>

          <p v-if="formError" class="feedback error">{{ formError }}</p>

          <p v-if="!auth.isAuthenticated" class="feedback hint">
            Inicia sesión en la portada para registrar o eliminar novedades.
          </p>
        </form>
      </section>
    </div>

    <!-- Tabla Histórica MVP -->
    <table class="primary mt-4">
      <thead>
        <tr>
          <th>ID</th>
          <th>Empleado</th>
          <th>Mes/Período</th>
          <th>Concepto</th>
          <th>Monto (COP)</th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr v-if="cargandoLista">
          <td colspan="6" class="text-center">Cargando novedades...</td>
        </tr>
        <tr v-else-if="novedades.length === 0">
          <td colspan="6" class="text-center">No hay novedades registradas para mostrar.</td>
        </tr>
        <tr v-for="nov in novedades" :key="nov.id">
          <td>{{ nov.id }}</td>
          <td>{{ getNombreEmpleado(nov.empleado_id) }}</td>
          <td>{{ nov.periodo }}</td>
          <td><span class="label">{{ nov.tipo }}</span></td>
          <td>$ {{ Number(nov.valor).toLocaleString('es-CO') }}</td>
          <td>
            <button class="small bg-error" @click="eliminar(nov.id)">Eliminar</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

import api from '../services/api'
import { useAuthStore } from '../stores/auth'

// Estados y Variables Reactivas
const novedades = ref([])
const empleados = ref([])
const mostrarFormulario = ref(false)
const cargando = ref(false)
const cargandoLista = ref(false)
const formError = ref('')
const apiError = ref('')
const successMessage = ref('')
const auth = useAuthStore()

// Fecha actual en formato YYYY-MM para el input type="month"
const mesActual = new Date().toISOString().slice(0, 7)

const novedadVacia = {
  empleado_id: '',
  periodo: mesActual,
  tipo: 'HORA_EXTRA',
  valor: null
}

const nuevaNovedad = ref({ ...novedadVacia })

// Propiedad computada para formatear los miles sin romper el v-model numérico (Igual que en Empleados)
const valorFormatted = computed({
  get: () => {
    if (!nuevaNovedad.value.valor) return ''
    return Number(nuevaNovedad.value.valor).toLocaleString('es-CO')
  },
  set: (newValue) => {
    const stringNumerico = newValue.replace(/\D/g, '')
    nuevaNovedad.value.valor = stringNumerico ? parseFloat(stringNumerico) : null
  }
})

const obtenerMensajeError = (error, fallback) => {
  return error.response?.data?.message || error.response?.data?.detail || fallback
}

// Carga Inicial
const cargarDatosBase = async () => {
  cargandoLista.value = true
  apiError.value = ''
  
  try {
    // 1. Cargamos catálogo de la DB para el menú desplegable (FastAPI ya lo soporta)
    const resEmpleados = await api.get('/empleados/')
    empleados.value = resEmpleados.data

    // 2. Cargamos novedades reales desde el backend
    const resNov = await api.get('/novedades/')
    novedades.value = resNov.data

  } catch (error) {
    apiError.value = error.response?.data?.detail || 'No se pudo cargar la información desde el servidor.'
  } finally {
    cargandoLista.value = false
  }
}

const validarNovedad = () => {
  if (!nuevaNovedad.value.empleado_id) return 'Debes seleccionar un empleado.'
  if (!nuevaNovedad.value.periodo) return 'Debes indicar el período.'
  if (!/^[0-9]{4}-[0-9]{2}$/.test(nuevaNovedad.value.periodo)) return 'El período debe tener formato YYYY-MM.'
  if (!nuevaNovedad.value.tipo) return 'Debes seleccionar un tipo de novedad.'
  if (!nuevaNovedad.value.valor || Number(nuevaNovedad.value.valor) <= 0) return 'El valor debe ser mayor que cero.'
  return ''
}

// Búsqueda de nombre para la tabla
const getNombreEmpleado = (id) => {
  const emp = empleados.value.find(e => e.id === id)
  return emp ? emp.nombre : 'Desconocido'
}

// Capturar el formulario
const guardarNovedad = async () => {
  apiError.value = ''
  formError.value = ''
  successMessage.value = ''

  const validacion = validarNovedad()
  if (validacion) {
    formError.value = validacion
    return
  }

  cargando.value = true
  
  const payload = {
    empleado_id: Number(nuevaNovedad.value.empleado_id),
    periodo: nuevaNovedad.value.periodo,
    tipo: nuevaNovedad.value.tipo,
    valor: parseFloat(nuevaNovedad.value.valor)
  }
  
  try {
    const res = await api.post('/novedades/', payload)
    const existingIndex = novedades.value.findIndex(n => n.id === res.data.id)
    if (existingIndex >= 0) {
      novedades.value[existingIndex] = res.data
    } else {
      novedades.value.push(res.data)
    }
    successMessage.value = 'Novedad guardada correctamente.'
    cerrarFormulario(true)
  } catch (error) {
    apiError.value = obtenerMensajeError(error, 'Ocurrió un error al enviar al servidor.')
  } finally {
    cargando.value = false
  }
}

const cerrarFormulario = (mantenerMensaje = false) => {
  mostrarFormulario.value = false
  nuevaNovedad.value = { ...novedadVacia }
  apiError.value = ''
  formError.value = ''
  if (!mantenerMensaje) {
    successMessage.value = ''
  }
}

const eliminar = async (id) => {
  if (confirm("¿Seguro que deseas descartar esta novedad para el mes?")) {
    try {
      await api.delete(`/novedades/${id}`)
      novedades.value = novedades.value.filter(n => n.id !== id)
      successMessage.value = 'Novedad eliminada correctamente.'
    } catch (error) {
      apiError.value = obtenerMensajeError(error, 'No se pudo eliminar la novedad.')
    }
  }
}

// On Component Mount
onMounted(() => {
  cargarDatosBase()
})
</script>

<style scoped>
.mt-4 { margin-top: 20px; }
.mt-2 { margin-top: 10px; }
.text-center { text-align: center; }
.feedback { margin: 10px 0 0; }
.feedback.success { color: #19692c; }
.feedback.error { color: #a61b1b; }
.feedback.hint { color: #5c6677; }
</style>
