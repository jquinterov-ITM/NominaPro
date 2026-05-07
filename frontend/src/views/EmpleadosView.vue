<template>
  <div class="empleados-page">
    <div class="page-header">
      <h1>Empleados</h1>
      <p>Crear, consultar y eliminar empleados desde una interfaz más limpia.</p>
    </div>

    <form class="empleado-form card" novalidate @submit.prevent="crearEmpleado">
      <div class="field-group">
        <label>Nombre</label>
        <input v-model="form.nombre" required />
      </div>

      <div class="field-group">
        <label>Documento</label>
        <input v-model="form.documento" required />
      </div>

      <div class="field-group">
        <label>Salario base</label>
        <input
          v-model="form.salario_base"
          type="text"
          placeholder="Ej: 1500000 o 1.500.000"
          required
        />
      </div>

      <div class="field-group field-group--wide">
        <label>Tipo salario</label>
        <select v-model="form.tipo_salario">
          <option value="ORDINARIO">ORDINARIO</option>
          <option value="INTEGRAL">INTEGRAL</option>
        </select>
      </div>

      <div class="actions">
        <button :disabled="saving">{{ saving ? 'Guardando...' : 'Crear empleado' }}</button>
      </div>
    </form>

    <p v-if="error" class="error">{{ error }}</p>
    <p v-if="success" class="success">{{ success }}</p>

    <div v-if="loading">Cargando...</div>
    <div v-else class="list-space">
      <EmployeeCard
        v-for="e in empleados"
        :key="e.id"
        :empleado="e"
        :deleting="deletingId === e.id"
        @delete="eliminarEmpleado"
      />
    </div>
  </div>
</template>

<script lang="ts">
import { ref, onMounted } from 'vue'
import api from '../services/api'
import EmployeeCard from '../components/EmployeeCard.vue'
import { normalizeForApi } from '../utils/format'

export default {
  components: { EmployeeCard },
  setup() {
    const empleados = ref([])
    const loading = ref(false)
    const saving = ref(false)
    const deletingId = ref<number | null>(null)
    const error = ref('')
    const success = ref('')

    const form = ref({
      nombre: '',
      documento: '',
      salario_base: '',
      tipo_salario: 'ORDINARIO'
    })

    const load = async () => {
      loading.value = true
      try {
        const res = await api.get('/empleados/')
        empleados.value = res.data.items || res.data
      } catch (err: any) {
        const data = err?.response?.data || {}
        error.value = data.message || data.detail || 'No se pudieron cargar los empleados.'
      } finally {
        loading.value = false
      }
    }

    const extractApiError = (err: any, fallback: string) => {
      const data = err?.response?.data || {}
      const message = data.message || data.detail
      const details = data.details

      if (Array.isArray(details) && details.length > 0) {
        const formatted = details
          .map((item: any) => item?.msg || item?.message || item?.detail)
          .filter(Boolean)
          .join(' | ')
        return formatted || message || fallback
      }

      if (typeof details === 'string' && details.trim()) {
        return details
      }

      return message || fallback
    }

    const crearEmpleado = async () => {
      error.value = ''
      success.value = ''

      const nombre = form.value.nombre.trim()
      const documento = form.value.documento.trim()
      const rawSalario = form.value.salario_base.trim()
      if (!nombre || !documento || !rawSalario) {
        error.value = 'Nombre, documento y salario base son obligatorios.'
        return
      }

      // Normalizar y validar usando la utilidad compartida
      const salarioStr = normalizeForApi(rawSalario)
      const salarioNum = Number(salarioStr)
      if (Number.isNaN(salarioNum) || salarioNum <= 0) {
        error.value = 'El salario base debe ser un número válido mayor a 0.'
        return
      }
      // Enviar como cadena normalizada para preservar precisión Decimal en el backend

      saving.value = true
      try {
        await api.post('/empleados/', {
          nombre,
          documento,
          salario_base: salarioStr,
          tipo_salario: form.value.tipo_salario
        })
        success.value = 'Empleado creado correctamente.'
        form.value = {
          nombre: '',
          documento: '',
          salario_base: '',
          tipo_salario: 'ORDINARIO'
        }
        await load()
      } catch (err: any) {
        error.value = extractApiError(err, 'No se pudo crear el empleado.')
      } finally {
        saving.value = false
      }
    }

    const eliminarEmpleado = async (empleado: any) => {
      const ok = window.confirm(`¿Eliminar a ${empleado.nombre} (${empleado.documento})?`)
      if (!ok) return

      error.value = ''
      success.value = ''
      deletingId.value = empleado.id
      try {
        await api.delete(`/empleados/${empleado.id}`)
        success.value = 'Empleado eliminado correctamente.'
        await load()
      } catch (err: any) {
        error.value = extractApiError(err, 'No se pudo eliminar el empleado.')
      } finally {
        deletingId.value = null
      }
    }

    onMounted(load)
    return { empleados, loading, form, crearEmpleado, eliminarEmpleado, saving, deletingId, error, success }
  }
}
</script>

<style scoped>
.empleados-page {
  display: grid;
  gap: 16px;
}

.page-header {
  display: grid;
  gap: 4px;
}

.page-header h1 {
  margin: 0;
}

.page-header p {
  margin: 0;
  color: #5f6b7a;
}

.card {
  background: linear-gradient(180deg, #ffffff 0%, #fbfcfe 100%);
  border: 1px solid #e3e8ef;
  border-radius: 16px;
  box-shadow: 0 10px 24px rgba(15, 23, 42, 0.06);
  padding: 18px;
}

.empleado-form {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 14px 16px;
}

.field-group {
  display: grid;
  gap: 6px;
}

.field-group--wide {
  grid-column: 1 / -1;
}

.empleado-form label {
  display: block;
  font-size: 0.92rem;
  font-weight: 600;
  color: #243447;
}

.empleado-form input,
.empleado-form select {
  width: 100%;
  min-height: 46px;
  border: 1px solid #cbd5e1;
  border-radius: 10px;
  padding: 10px 12px;
  background: #fff;
  color: #0f172a;
  transition: border-color 0.15s ease, box-shadow 0.15s ease;
  box-sizing: border-box;
}

.empleado-form input:focus,
.empleado-form select:focus {
  outline: none;
  border-color: #0b57a4;
  box-shadow: 0 0 0 3px rgba(11, 87, 164, 0.12);
}

.actions {
  grid-column: 1 / -1;
  display: flex;
  justify-content: flex-end;
  margin-top: 2px;
}

.actions button {
  min-width: 190px;
  min-height: 46px;
  border-radius: 10px;
  font-weight: 700;
  letter-spacing: 0.01em;
}

.error {
  margin: 0;
  color: #b00020;
}

.success {
  margin: 0;
  color: #0b7a35;
}

.list-space {
  display: grid;
  gap: 10px;
}

@media (max-width: 760px) {
  .empleado-form {
    grid-template-columns: 1fr;
  }

  .actions {
    justify-content: stretch;
  }

  .actions button {
    width: 100%;
  }
}
</style>
