<template>
  <header class="app-header">
    <h2>NominaPro</h2>
    <nav>
      <router-link to="/">Inicio</router-link>
      <router-link to="/empleados">Empleados</router-link>
      <router-link to="/novedades">Novedades</router-link>
      <router-link to="/nominas">Nóminas</router-link>
    </nav>
    <div class="auth">
      <button @click="logout">Cerrar sesión</button>
    </div>
  </header>
</template>

<script lang="ts">
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

export default {
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    
    const logout = () => {
      authStore.logout()
      router.push('/login')
    }
    
    return { logout }
  }
}
</script>

<style scoped>
.app-header{display:flex;align-items:center;justify-content:space-between;padding:12px;background:#0b57a4;color:#fff}
.app-header nav a{color:#fff;margin-right:12px;text-decoration:none}
.auth button{background:transparent;border:1px solid #fff;color:#fff;padding:6px 10px;border-radius:4px}
</style>