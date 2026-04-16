<template>
  <div class="page">
    <section v-if="!auth.isAuthenticated" class="page-hero card">
      <div class="page-hero__copy">
        <p class="eyebrow">Acceso privado</p>
        <h1>Ingresa para ver empleados, novedades y liquidación.</h1>
        <p>
          La navegación y los módulos solo aparecen después de iniciar sesión. Esto evita mostrar información operativa sin autenticación.
        </p>
      </div>

      <div class="page-hero__actions">
        <a href="#login-box" class="button">Ir al formulario</a>
        <a href="#login-box" class="button pseudo">Entrar al sistema</a>
      </div>
    </section>

    <section v-if="!auth.isAuthenticated" id="login-box" class="panel-grid">
      <article class="card panel-card panel-card--login">
        <header class="panel-card__header">
          <h3>Acceso de demo</h3>
        </header>

        <form class="login-form" @submit.prevent="handleLogin">
          <div class="field">
            <label>Usuario</label>
            <input v-model.trim="loginForm.username" type="text" autocomplete="username" required />
          </div>
          <div class="field">
            <label>Clave</label>
            <input v-model="loginForm.password" type="password" autocomplete="current-password" required />
          </div>

          <p v-if="loginError" class="feedback error">{{ loginError }}</p>
          <p v-else class="feedback hint">Usa la cuenta de demo para entrar al panel privado.</p>

          <button type="submit" :disabled="auth.loading">
            {{ auth.loading ? 'Ingresando...' : 'Ingresar' }}
          </button>
        </form>
      </article>
    </section>

    <section v-else class="panel-grid">
      <article class="card panel-card panel-card--session">
        <header class="panel-card__header">
          <h3>Sesión activa</h3>
          <span class="status-dot status-dot--active">Autenticado</span>
        </header>

        <div class="session-box">
          <div class="session-box__row">
            <span>Usuario</span>
            <strong>{{ auth.displayName }}</strong>
          </div>
          <div class="session-box__row">
            <span>Roles</span>
            <strong>{{ auth.roleLabel }}</strong>
          </div>
          <button class="button button--danger" type="button" @click="auth.logout()">Cerrar sesión</button>
        </div>
      </article>

      <div class="cards-grid">
        <article class="card feature-card">
          <p class="feature-card__eyebrow">Operación</p>
          <h3>Empleados</h3>
          <p>Administra identificación, tipo de salario y validaciones básicas del formulario.</p>
          <router-link to="/empleados" class="button pseudo">Abrir módulo</router-link>
        </article>

        <article class="card feature-card">
          <p class="feature-card__eyebrow">Registro mensual</p>
          <h3>Novedades</h3>
          <p>Ingresa horas extras, incapacidades y descuentos con control de duplicados por período.</p>
          <router-link to="/novedades" class="button pseudo">Abrir módulo</router-link>
        </article>

        <article class="card feature-card">
          <p class="feature-card__eyebrow">Cierre</p>
          <h3>Liquidación</h3>
          <p>Calcula nómina, aporta prestaciones y revisa resultados con el flujo protegido.</p>
          <router-link to="/nominas" class="button pseudo">Abrir módulo</router-link>
        </article>
      </div>
    </section>
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
.page {
  display: grid;
  gap: 1.25rem;
}

.page-hero {
  display: grid;
  grid-template-columns: minmax(0, 1.6fr) minmax(220px, 0.9fr);
  gap: 1rem;
  align-items: end;
  padding: 1.5rem;
  background: linear-gradient(180deg, #ffffff 0%, #f7f9fc 100%);
  border: 1px solid rgba(30, 51, 77, 0.08);
}

.page-hero h1 {
  margin: 0.4rem 0 0.75rem;
  max-width: 780px;
  color: #10253d;
}

.page-hero p {
  margin: 0;
  max-width: 760px;
  color: #5f7084;
}

.page-hero__actions {
  display: flex;
  gap: 0.75rem;
  justify-content: flex-end;
  flex-wrap: wrap;
}

.eyebrow {
  text-transform: uppercase;
  letter-spacing: 0.12em;
  font-size: 0.78rem;
  margin: 0;
  color: #3f67a9;
  font-weight: 700;
}

.panel-grid {
  display: grid;
  gap: 1rem;
}

.panel-card,
.feature-card {
  min-height: 100%;
}

.panel-card--login,
.panel-card--session {
  max-width: 720px;
}

.login-form {
  display: grid;
  gap: 0.75rem;
}

.session-box {
  display: grid;
  gap: 0.7rem;
}

.session-box__row {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  padding: 0.65rem 0.75rem;
  border-radius: 0.8rem;
  background: #f7f9fc;
  border: 1px solid rgba(30, 51, 77, 0.06);
}

.session-box__row span {
  color: #6b7a8a;
}

.session-box__row strong {
  color: #10253d;
  text-align: right;
}

.token-row strong {
  word-break: break-all;
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

.feature-card {
  display: grid;
  gap: 0.8rem;
  padding: 1.25rem;
  border: 1px solid rgba(30, 51, 77, 0.08);
  background: #fff;
}

.feature-card h3 {
  margin: 0;
  color: #10253d;
}

.feature-card p {
  margin: 0;
  color: #5f7084;
}

.feature-card__eyebrow {
  margin: 0;
  color: #3f67a9;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  font-size: 0.75rem;
}

.panel-card {
  padding: 1.25rem;
  border: 1px solid rgba(30, 51, 77, 0.08);
  background: #fff;
}

.panel-card__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  margin-bottom: 1rem;
}

.panel-card__header h3 {
  margin: 0;
  color: #10253d;
}

.panel-card--login .panel-card__header,
.panel-card--session .panel-card__header {
  margin-bottom: 1.25rem;
}

.status-dot {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.35rem 0.7rem;
  border-radius: 999px;
  background: #eef2f7;
  color: #607083;
  font-size: 0.82rem;
  font-weight: 700;
}

.status-dot--active {
  background: rgba(19, 70, 154, 0.08);
  color: #13469a;
}

.button--danger {
  background: #b42318;
  border-color: #b42318;
}

@media (max-width: 860px) {
  .page-hero {
    grid-template-columns: 1fr;
  }

  .page-hero__actions {
    justify-content: flex-start;
  }
}
</style>
