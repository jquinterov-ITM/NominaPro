<template>
  <div class="home-shell">
    <section class="hero card">
      <div>
        <p class="eyebrow">NominaPro demo 2026</p>
        <h1>Controla empleados, novedades y liquidaciones desde una sola pantalla.</h1>
        <p>
          El backend protege las escrituras con JWT y roles. Desde aquí puedes iniciar sesión con la cuenta de demo y seguir operando las vistas.
        </p>
      </div>

      <div class="hero-actions">
        <router-link to="/empleados" class="button">Ir a Empleados</router-link>
        <router-link to="/novedades" class="button pseudo">Ir a Novedades</router-link>
      </div>
    </section>

    <section class="card auth-card">
      <header>
        <h3>Acceso de demo</h3>
      </header>

      <div v-if="auth.isAuthenticated" class="session-box">
        <p><strong>Sesión activa:</strong> {{ auth.displayName }}</p>
        <p><strong>Roles:</strong> {{ auth.roleLabel }}</p>
        <p><strong>Token:</strong> {{ auth.tokenPreview }}</p>
        <button class="small bg-error" type="button" @click="auth.logout()">Cerrar sesión</button>
      </div>

      <form v-else class="login-form" @submit.prevent="handleLogin">
        <div class="field">
          <label>Usuario</label>
          <input v-model.trim="loginForm.username" type="text" autocomplete="username" required />
        </div>
        <div class="field">
          <label>Clave</label>
          <input v-model="loginForm.password" type="password" autocomplete="current-password" required />
        </div>

        <p v-if="loginError" class="feedback error">{{ loginError }}</p>
        <p v-else class="feedback hint">Usa la cuenta de demo para habilitar los botones de escritura.</p>

        <button type="submit" :disabled="auth.loading">
          {{ auth.loading ? 'Ingresando...' : 'Ingresar' }}
        </button>
      </form>
    </section>

    <div class="cards-grid">
      <article class="card feature-card">
        <header>
          <h3>👥 Gestión de Empleados</h3>
        </header>
        <section>Agrega y administra empleados, modalidad de salario y validaciones básicas del formulario.</section>
        <footer><router-link to="/empleados" class="button">Ir a Empleados</router-link></footer>
      </article>

      <article class="card feature-card">
        <header>
          <h3>🗓️ Novedades del Mes</h3>
        </header>
        <section>Ingresa horas extras, incapacidades y descuentos con control de duplicados por período.</section>
        <footer><router-link to="/novedades" class="button">Ir a Novedades</router-link></footer>
      </article>

      <article class="card feature-card">
        <header>
          <h3>💵 Liquidación</h3>
        </header>
        <section>Calcula la nómina, verifica aportes, parafiscales y prestaciones con el flujo protegido.</section>
        <footer><router-link to="/nominas" class="button">Ir a Nómina</router-link></footer>
      </article>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'

import { useAuthStore } from '../stores/auth'

const auth = useAuthStore()

const loginForm = reactive({
  username: 'admin',
  password: 'secret'
})

const loginError = ref('')

const handleLogin = async () => {
  loginError.value = ''

  try {
    await auth.login(loginForm.username, loginForm.password)
  } catch {
    loginError.value = auth.error || 'No se pudo iniciar sesión.'
  }
}
</script>

<style scoped>
.home-shell {
  display: grid;
  gap: 20px;
}

.hero {
  display: grid;
  gap: 16px;
  padding: 24px;
  background: linear-gradient(135deg, #0f172a 0%, #1d4ed8 100%);
  color: #f8fafc;
}

.hero h1 {
  margin: 6px 0 10px;
  max-width: 760px;
}

.hero p {
  max-width: 760px;
  color: #dbeafe;
}

.eyebrow {
  text-transform: uppercase;
  letter-spacing: 0.12em;
  font-size: 0.78rem;
  margin: 0;
  color: #bfdbfe;
}

.hero-actions {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.auth-card,
.feature-card {
  min-height: 100%;
}

.login-form {
  display: grid;
  gap: 12px;
}

.session-box {
  display: grid;
  gap: 8px;
}

.feedback {
  margin: 0;
}

.feedback.error {
  color: #b42318;
}

.feedback.hint {
  color: #5b6472;
}

.cards-grid {
  display: grid;
  gap: 16px;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
}
</style>
