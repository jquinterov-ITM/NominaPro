<template>
  <div style="padding: 40px; max-width: 400px; margin: auto">
    <h1>Login - NominaPro</h1>
    <form @submit.prevent="login">
      <div style="margin-bottom: 12px">
        <label>Usuario</label>
        <input v-model="username" style="width: 100%; padding: 8px" />
      </div>
      <div style="margin-bottom: 12px">
        <label>Clave</label>
        <input type="password" v-model="password" style="width: 100%; padding: 8px" />
      </div>
      <button style="width: 100%; padding: 10px" :disabled="loading">{{ loading ? 'Conectando...' : 'Entrar' }}</button>
    </form>
    <div v-if="error" style="color:#b00020; margin-top: 12px; padding: 10px; border: 1px solid #b00020; border-radius: 4px">
      ❌ {{ error }}
    </div>
    <div v-if="success" style="color:#00b050; margin-top: 12px; padding: 10px; border: 1px solid #00b050; border-radius: 4px">
      ✓ Conectado, redirigiendo...
    </div>
    <div style="margin-top: 20px; font-size: 0.9em; color: #666">
      Demo: admin / secret
    </div>
  </div>
</template>

<script lang="ts">
import { ref } from 'vue'
import api from '../services/api'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

export default {
  setup() {
    const username = ref('admin')
    const password = ref('secret')
    const error = ref('')
    const success = ref(false)
    const loading = ref(false)
    const router = useRouter()
    const authStore = useAuthStore()

    const login = async () => {
      error.value = ''
      success.value = false
      loading.value = true
      try {
        console.log('Intentando login con:', username.value)
        // El backend espera application/x-www-form-urlencoded
        const params = new URLSearchParams()
        params.append('username', username.value)
        params.append('password', password.value)
        
        const res = await api.post('/auth/token', params, {
          headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
        })
        console.log('Login exitoso:', res.data)
        const token = res.data.access_token
        authStore.login(token)
        success.value = true
        setTimeout(() => router.push('/'), 500)
      } catch (err: any) {
        console.error('Error de login:', err)
        const status = err?.response?.status
        const detail = err?.response?.data?.detail || err?.message || 'Error desconocido'
        error.value = `[${status || 'Error'}] ${detail}`
      } finally {
        loading.value = false
      }
    }

    return { username, password, error, success, loading, login }
  }
}
</script>
