<template>
  <div>
    <Header v-if="authStore.isAuthenticated" />
    <main class="container">
      <router-view />
    </main>
  </div>
</template>

<script lang="ts">
import { onMounted } from 'vue'
import { useAuthStore } from './stores/auth'
import api from './services/api'
import Header from './components/Header.vue'

export default {
  components: { Header },
  setup() {
    const authStore = useAuthStore()

    onMounted(async () => {
      authStore.initToken()
      if (authStore.token) {
        try {
          await api.get('/api/auth/me')
        } catch {
          authStore.logout()
        }
      }
    })

    return { authStore }
  }
}
</script>

<style>
.container{padding:16px;max-width:1000px;margin:16px auto}
</style>
