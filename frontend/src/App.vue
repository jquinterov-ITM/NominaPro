<template>
  <div class="container">
    <header>
      <nav class="demo">
        <a href="#" class="brand">
          <span>NominaPro (2026)</span>
        </a>
        <!-- Responsive menu-->
        <input id="bmenu" type="checkbox" class="show">
        <label for="bmenu" class="burger pseudo button">&#9776;</label>
        <div class="menu">
          <router-link to="/">Inicio</router-link>
          <router-link to="/empleados">Empleados</router-link>
          <router-link to="/novedades">Novedades</router-link>
          <router-link to="/nominas">Liquidación</router-link>
        </div>
        <div class="session-chip" :class="{ active: auth.isAuthenticated }">
          <span>{{ auth.displayName }}</span>
          <small>{{ auth.roleLabel }}</small>
          <button v-if="auth.isAuthenticated" class="small" type="button" @click="auth.logout()">Salir</button>
        </div>
      </nav>
    </header>

    <main>
      <!-- Vue Router injects the matching View component here -->
      <RouterView />
    </main>
  </div>
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { useAuthStore } from './stores/auth'

const auth = useAuthStore()
</script>

<style scoped>
.brand { font-size: 1.2em; font-weight: bold; color: #007bff; text-decoration: none; margin-right: 15px; }
nav a { margin-right: 15px; text-decoration: none; color: #333; font-weight: 500; }
nav a.router-link-exact-active { border-bottom: 2px solid #007bff; color: #007bff; }
.session-chip {
  margin-left: auto;
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 12px;
  border-radius: 999px;
  background: #f3f6fb;
  color: #24324a;
  border: 1px solid #d8e2f0;
}
.session-chip.active {
  background: #eefbf1;
  border-color: #b9e5c4;
}
.session-chip small { color: #60708a; }
.session-chip button { padding: 6px 10px; }
</style>
