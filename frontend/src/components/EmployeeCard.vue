<template>
  <div class="employee-card">
    <div class="top">
      <strong>{{ empleado.nombre }}</strong>
      <span class="id">Doc: {{ empleado.documento }}</span>
    </div>
    <div class="meta">Tipo salario: {{ empleado.tipo_salario }}</div>
    <div class="meta">Salario base: {{ formatCurrency(empleado.salario_base) }}</div>
    <div class="actions">
      <button class="danger" :disabled="deleting" @click="$emit('delete', empleado)">
        {{ deleting ? 'Eliminando...' : 'Eliminar' }}
      </button>
    </div>
  </div>
</template>

<script lang="ts">
import { formatCurrency } from '../utils/format'

export default {
  emits: ['delete'],
  props: {
    empleado: { type: Object, required: true },
    deleting: { type: Boolean, default: false }
  },
  methods: {
    formatCurrency
  }
}
</script>

<style scoped>
.employee-card{border:1px solid #ddd;padding:10px;border-radius:6px;margin-bottom:8px}
.top{display:flex;justify-content:space-between}
.meta{color:#666;font-size:0.9em}
.actions{margin-top:8px}
.danger{background:#b00020;color:#fff;border:none;padding:6px 10px;border-radius:6px;cursor:pointer}
.danger:disabled{opacity:0.7;cursor:not-allowed}
</style>