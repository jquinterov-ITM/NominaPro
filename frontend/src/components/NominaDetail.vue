<template>
  <div class="nomina-detail">
    <h3>{{ empleadoNombre }}</h3>
    <div class="subtle">Empleado #{{ nomina.empleado_id }} · Periodo {{ nomina.periodo }}</div>
    <div>Total devengado: {{ formatCurrency(nomina.total_devengado) }}</div>
    <div>Total deducido: {{ formatCurrency(nomina.total_deducido) }}</div>
    <div>Neto a pagar: {{ formatCurrency(nomina.neto_pagar) }}</div>
  </div>
</template>

<script lang="ts">
import { formatCurrency } from '../utils/format'

export default {
  props: {
    nomina: { type: Object, required: true },
    empleadoNombre: { type: String, default: 'Empleado' }
  },
  methods: {
    formatCurrency
  }
}
</script>

<style scoped>
.nomina-detail {
  border: 1px solid #e0e0e0;
  padding: 14px;
  border-radius: 12px;
  background: #fff;
  display: grid;
  gap: 6px;
}

.subtle {
  color: #64748b;
  font-size: 0.92rem;
}
</style>