<template>
  <div class="page">
    <section class="page-head card">
      <div>
        <p class="eyebrow">Cierre mensual</p>
        <h2>Liquidación Mensual de Nómina</h2>
        <p>Consolida y revisa el resultado de la nómina en una interfaz más ejecutiva.</p>
      </div>
      <div class="page-head__actions">
        <button class="button" @click="mostrarFormulario = true">⚡ Generar / Liquidar Mes</button>
      </div>
    </section>

    <p v-if="successMessage" class="feedback success">{{ successMessage }}</p>
    <p v-if="apiError" class="feedback error">{{ apiError }}</p>

    <!-- Formulario para liquidar -->
    <div v-if="mostrarFormulario" class="card panel-card mt-4">
      <header class="panel-card__header">Parámetros de Liquidación</header>
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
          
          <div class="mt-4 actions-row">
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
    <section class="card table-card mt-4">
    <table class="primary">
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
    </section>
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
.bg-info { background-color: #17a2b8; color: white;}
.bg-warning { background-color: #ffc107; color: black; }
.bg-success { background-color: #28a745; color: white; }
</style>
