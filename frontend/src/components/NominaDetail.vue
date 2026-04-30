<template>
  <div class="nomina-detail">
    <h3>Periodo: {{ nomina.periodo }}</h3>
    <div>Empleado: {{ nomina.empleado_id }}</div>
    <div>Total devengado: {{ nomina.total_devengado }}</div>
    <div>Total deducciones: {{ nomina.total_deducciones }}</div>
    <div>Neto a pagar: {{ nomina.neto_pagar }}</div>
  </div>
</template>

<script lang="ts">
export default {
  props: { nomina: { type: Object, required: true } }
}
</script>

<style scoped>
.nomina-detail{border:1px solid #e0e0e0;padding:10px;border-radius:6px}
</style>