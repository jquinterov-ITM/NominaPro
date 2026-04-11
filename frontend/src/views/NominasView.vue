<template>
  <div>
    <h2>Liquidación Mensual de Nómina</h2>
    
    <div class="flex">
      <button class="success" @click="mostrarFormulario = true">⚡ Generar / Liquidar Mes</button>
    </div>

    <p v-if="successMessage" class="feedback success">{{ successMessage }}</p>
    <p v-if="apiError" class="feedback error">{{ apiError }}</p>

    <!-- Formulario para liquidar -->
    <div v-if="mostrarFormulario" class="card mt-4">
      <header>Parámetros de Liquidación</header>
      <section>
        <form @submit.prevent="generarNomina">
          <div class="flex two">
            <div class="field">
              <label>Mes a Liquidar (Período)</label>
              <input type="month" v-model="periodoLiquidacion" required />
            </div>
          </div>
          
          <div v-if="apiError" class="pseudo button error mt-2">
             Error: {{ apiError }}
          </div>
          
          <div class="mt-4">
            <button type="submit" :disabled="cargando || !auth.isAuthenticated">{{ cargando ? 'Procesando...' : 'Procesar Liquidación' }}</button>
            <button type="button" class="pseudo" @click="cerrarFormulario">Cancelar</button>
          </div>

          <p v-if="formError" class="feedback error">{{ formError }}</p>
          <p v-if="!auth.isAuthenticated" class="feedback hint">
            Inicia sesión en la portada para liquidar o eliminar nóminas.
          </p>
        </form>
      </section>
    </div>

    <!-- Tabla Histórica de Nóminas -->
    <table class="primary mt-4">
      <thead>
        <tr>
          <th>ID</th>
          <th>Período</th>
          <th>Empleado</th>
          <th>Total Devengado</th>
          <th>Total Deducido</th>
          <th>Neto a Pagar</th>
          <th>Estado</th>
        </tr>
      </thead>
      <tbody>
        <tr v-if="cargandoLista">
          <td colspan="7" class="text-center">Cargando histórico de nóminas...</td>
        </tr>
        <tr v-else-if="nominas.length === 0">
          <td colspan="7" class="text-center">No hay liquidaciones registradas.</td>
        </tr>
        <tr v-for="nom in nominas" :key="nom.id">
          <td>{{ nom.id }}</td>
          <td>{{ nom.periodo }}</td>
          <td>{{ getNombreEmpleado(nom.empleado_id) }}</td>
          <td>$ {{ Number(nom.total_devengado || 0).toLocaleString('es-CO') }}</td>
          <td>$ {{ Number(nom.total_deducido || 0).toLocaleString('es-CO') }}</td>
          <td><strong>$ {{ Number(nom.neto_pagar || 0).toLocaleString('es-CO') }}</strong></td>
          <td><span class="label" :class="estadoClass(nom.estado)">{{ nom.estado }}</span></td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

import api from '../services/api'
import { useAuthStore } from '../stores/auth'

const nominas = ref([])
const empleados = ref([])
const mostrarFormulario = ref(false)
const cargando = ref(false)
const cargandoLista = ref(false)
const formError = ref('')
const apiError = ref('')
const successMessage = ref('')
const auth = useAuthStore()

const mesActual = new Date().toISOString().slice(0, 7)
const periodoLiquidacion = ref(mesActual)

const periodoValido = computed(() => /^[0-9]{4}-[0-9]{2}$/.test(periodoLiquidacion.value))

const obtenerMensajeError = (error, fallback) => {
  return error.response?.data?.message || error.response?.data?.detail || fallback
}

const cargarDatosBase = async () => {
  cargandoLista.value = true
  apiError.value = ''
  try {
    const resEmpleados = await api.get('/empleados/')
    empleados.value = resEmpleados.data

    const resNom = await api.get('/nominas/')
    nominas.value = resNom.data
  } catch (error) {
    apiError.value = error.response?.data?.detail || 'No se pudo cargar la información desde el servidor.'
  } finally {
    cargandoLista.value = false
  }
}

const getNombreEmpleado = (id) => {
  const emp = empleados.value.find(e => e.id === id)
  return emp ? emp.nombre : 'Desconocido'
}

const generarNomina = async () => {
  apiError.value = ''
  formError.value = ''
  successMessage.value = ''

  if (!periodoValido.value) {
    formError.value = 'El período debe tener formato YYYY-MM.'
    return
  }

  cargando.value = true
  
  const payload = {
    periodo: periodoLiquidacion.value
  }
  
  try {
    await api.post('/nominas/liquidar', payload)
    await cargarDatosBase()
    successMessage.value = `Nómina de ${periodoLiquidacion.value} procesada correctamente.`
    cerrarFormulario(true)
  } catch (error) {
    apiError.value = obtenerMensajeError(error, 'Ocurrió un error al liquidar.')
  } finally {
    cargando.value = false
  }
}

const cerrarFormulario = (mantenerMensaje = false) => {
  mostrarFormulario.value = false
  periodoLiquidacion.value = mesActual
  apiError.value = ''
  formError.value = ''
  if (!mantenerMensaje) {
    successMessage.value = ''
  }
}

const estadoClass = (estado) => {
  if (estado === 'CERRADA_DIAN') return 'bg-success'
  if (estado === 'LIQUIDADA') return 'bg-warning'
  return 'bg-info' // Para BORRADOR
}

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
.bg-info { background-color: #17a2b8; color: white;}
.bg-warning { background-color: #ffc107; color: black; }
.bg-success { background-color: #28a745; color: white; }
</style>
