<template>
  <div>
    <h1>Novedades</h1>
    <div v-if="loading">Cargando...</div>
    <div v-else>
      <NovedadForm @saved="load" />
      <ul>
        <li v-for="n in novedades" :key="n.id">{{ n.empleado_id }} - {{ n.periodo }} - {{ n.descripcion }}</li>
      </ul>
    </div>
  </div>
</template>

<script lang="ts">
import { ref, onMounted } from 'vue'
import api from '../services/api'
import NovedadForm from '../components/NovedadForm.vue'

export default {
  components: { NovedadForm },
  setup() {
    const novedades = ref([])
    const loading = ref(false)

    const load = async () => {
      loading.value = true
      try {
        const res = await api.get('/novedades/')
        novedades.value = res.data.items || res.data
      } finally {
        loading.value = false
      }
    }

    onMounted(load)
    return { novedades, loading, load }
  }
}
</script>
