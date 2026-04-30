<template>
  <form @submit.prevent="submit" class="novedad-form">
    <div>
      <label>Empleado ID</label>
      <input v-model="form.empleado_id" type="number" required />
    </div>
    <div>
      <label>Período (YYYY-MM)</label>
      <input v-model="form.periodo" placeholder="2026-01" required />
    </div>
    <div>
      <label>Descripción</label>
      <input v-model="form.descripcion" />
    </div>
    <div>
      <label>Monto</label>
      <input v-model.number="form.monto" type="number" step="0.01" />
    </div>
    <button>Guardar</button>
    <div v-if="error" class="error">{{ error }}</div>
  </form>
</template>

<script lang="ts">
import { reactive, ref } from 'vue'
import api from '../services/api'

export default {
  emits: ['saved'],
  setup(_, { emit }) {
    const form = reactive({ empleado_id: 0, periodo: '', descripcion: '', monto: 0 })
    const error = ref('')

    const submit = async () => {
      error.value = ''
      try {
        await api.post('/novedades/', form)
        emit('saved')
      } catch (err: any) {
        error.value = err?.response?.data?.detail || 'Error al guardar'
      }
    }

    return { form, submit, error }
  }
}
</script>

<style scoped>
.novedad-form{max-width:480px}
.novedad-form div{margin-bottom:8px}
.error{color:#b00020;margin-top:8px}
</style>