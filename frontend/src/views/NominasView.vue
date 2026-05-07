<template>
  <div class="nominas-page">
    <div class="page-header">
      <h1>Nóminas</h1>
      <p>Liquida un mes completo y consulta el historial agrupado por período y empleado.</p>
    </div>

    <section class="card controls">
      <div class="field-group">
        <label>Período a liquidar</label>
        <input v-model="selectedPeriodo" type="month" />
      </div>

      <div class="actions">
        <button :disabled="liquidando" @click="liquidarMes">
          {{ liquidando ? 'Liquidando...' : 'Liquidar mes' }}
        </button>
      </div>
    </section>

    <p v-if="error" class="error">{{ error }}</p>
    <p v-if="success" class="success">{{ success }}</p>

    <section class="card controls">
      <div class="field-group">
        <label>Filtrar historial por período</label>
        <input v-model="filterPeriodo" type="month" />
      </div>

      <div class="actions">
        <button class="secondary" :disabled="loading" @click="load(filterPeriodo)">
          {{ loading ? 'Cargando...' : 'Buscar' }}
        </button>
        <button class="ghost" :disabled="loading && !filterPeriodo" @click="load()">
          Ver todo
        </button>
      </div>
    </section>

    <div v-if="loading && !grupos.length">Cargando...</div>

    <div v-else class="groups">
      <section v-for="grupo in grupos" :key="grupo.periodo" class="card group-card">
        <div class="group-header">
          <div>
            <h2>{{ grupo.periodo }}</h2>
            <p>{{ grupo.items.length }} empleado(s) liquidado(s)</p>
          </div>
        </div>

        <div class="employee-grid">
          <NominaDetail
            v-for="n in grupo.items"
            :key="n.id"
            :nomina="n"
            :empleado-nombre="empleadosMap[n.empleado_id] || `Empleado #${n.empleado_id}`"
          />
        </div>
      </section>
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
    const nominas = ref<any[]>([])
    const grupos = ref<Array<{ periodo: string; items: any[] }>>([])
    const empleadosMap = ref<Record<number, string>>({})
    const loading = ref(false)
    const liquidando = ref(false)
    const error = ref('')
    const success = ref('')
    const selectedPeriodo = ref(new Date().toISOString().slice(0, 7))
    const filterPeriodo = ref('')

    const buildGroups = (items: any[]) => {
      const map = new Map<string, any[]>()
      items.forEach((item) => {
        const periodo = item.periodo
        const current = map.get(periodo) || []
        current.push(item)
        map.set(periodo, current)
      })

      grupos.value = Array.from(map.entries())
        .sort(([a], [b]) => b.localeCompare(a))
        .map(([periodo, items]) => ({ periodo, items }))
    }

    const loadEmployees = async () => {
      const res = await api.get('/empleados/')
      const items = res.data.items || res.data
      empleadosMap.value = Object.fromEntries(
        items.map((item: any) => [item.id, item.nombre])
      )
    }

    const load = async (periodo?: string) => {
      loading.value = true
      error.value = ''
      try {
        const params = periodo ? { periodo } : undefined
        const res = await api.get('/nominas/', { params })
        const items = res.data.items || res.data
        nominas.value = items
        buildGroups(items)
        await loadEmployees()
        success.value = periodo ? `Historial filtrado por ${periodo}.` : 'Historial cargado correctamente.'
      } catch (err: any) {
        const data = err?.response?.data || {}
        error.value = data.message || data.detail || 'No se pudo cargar el historial de nóminas.'
      } finally {
        loading.value = false
      }
    }

    const liquidarMes = async () => {
      error.value = ''
      success.value = ''
      liquidando.value = true
      try {
        await api.post('/nominas/liquidar', { periodo: selectedPeriodo.value })
        success.value = `Nómina liquidada para ${selectedPeriodo.value}.`
        filterPeriodo.value = selectedPeriodo.value
        await load(selectedPeriodo.value)
      } catch (err: any) {
        const data = err?.response?.data || {}
        error.value = data.message || data.detail || 'No se pudo liquidar la nómina.'
      } finally {
        liquidando.value = false
      }
    }

    onMounted(load)
    return {
      nominas,
      grupos,
      empleadosMap,
      loading,
      liquidando,
      error,
      success,
      selectedPeriodo,
      filterPeriodo,
      load,
      liquidarMes
    }
  }
}
</script>

<style scoped>
.nominas-page {
  display: grid;
  gap: 16px;
}

.page-header {
  display: grid;
  gap: 4px;
}

.page-header h1,
.group-header h2 {
  margin: 0;
}

.page-header p,
.group-header p {
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

.controls {
  display: grid;
  grid-template-columns: minmax(220px, 280px) 1fr;
  gap: 14px;
  align-items: end;
}

.field-group {
  display: grid;
  gap: 6px;
}

.field-group label {
  font-size: 0.92rem;
  font-weight: 600;
  color: #243447;
}

.field-group input {
  min-height: 46px;
  border: 1px solid #cbd5e1;
  border-radius: 10px;
  padding: 10px 12px;
  background: #fff;
  box-sizing: border-box;
}

.actions {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
  flex-wrap: wrap;
}

.actions button {
  min-height: 46px;
  border-radius: 10px;
  min-width: 140px;
}

.secondary {
  background: #0b57a4;
}

.ghost {
  background: #eef2f7;
  color: #0f172a;
}

.error {
  margin: 0;
  color: #b00020;
}

.success {
  margin: 0;
  color: #0b7a35;
}

.groups {
  display: grid;
  gap: 14px;
}

.group-card {
  display: grid;
  gap: 14px;
}

.group-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.employee-grid {
  display: grid;
  gap: 12px;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
}

@media (max-width: 760px) {
  .controls {
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
