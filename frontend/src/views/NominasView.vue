<template>
  <div>
    <h1>Nóminas</h1>
    <div v-if="loading">Cargando...</div>
    <div v-else>
      <NominaDetail v-for="n in nominas" :key="n.id" :nomina="n" />
    </div>
  </div>
</template>

<script lang="ts">
import { ref, onMounted } from 'vue'
import api from '../services/api'
import NominaDetail from '../components/NominaDetail.vue'

export default {
  components: { NominaDetail },
  setup() {
    const nominas = ref([])
    const loading = ref(false)

    const load = async () => {
      loading.value = true
      try {
        const res = await api.get('/nominas/')
        nominas.value = res.data
      } finally {
        loading.value = false
      }
    }

    onMounted(load)
    return { nominas, loading }
  }
}
</script>
