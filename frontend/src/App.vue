<template>
  <div class="shell">
    <header class="topbar">
      <div class="topbar__inner">
        <div class="topbar__brand">
          <a href="#" class="brand">
            <span class="brand__title">NominaPro</span>
            <span class="brand__year">2026</span>
          </a>
        </div>

        <nav v-if="auth.isAuthenticated" class="topbar__nav" aria-label="Navegación principal">
          <RouterLink to="/">Inicio</RouterLink>
          <RouterLink to="/empleados">Empleados</RouterLink>
          <RouterLink to="/novedades">Novedades</RouterLink>
          <RouterLink to="/nominas">Liquidación</RouterLink>
        </nav>

        <section class="auth-rail" :class="{ 'auth-rail--active': auth.isAuthenticated }">
          <span v-if="!auth.isAuthenticated" class="auth-rail__guest">Acceso privado</span>
          <div class="auth-rail__avatar" aria-hidden="true">
            {{ initials }}
          </div>
          <div v-if="auth.isAuthenticated" class="auth-rail__copy">
            <strong>{{ auth.displayName }}</strong>
            <span>{{ auth.isAuthenticated ? auth.roleLabel : 'Sesión no iniciada' }}</span>
          </div>
          <button v-if="auth.isAuthenticated" class="auth-rail__action" type="button" @click="auth.logout()">Salir</button>
        </section>
      </div>
    </header>

    <main class="page-content">
      <RouterView />
    </main>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { RouterLink, RouterView } from 'vue-router'
import { useAuthStore } from './stores/auth'

const auth = useAuthStore()

const initials = computed(() => {
  const source = auth.displayName || 'N'
  return source
    .split(/\s+/)
    .filter(Boolean)
    .slice(0, 2)
    .map(part => part[0]?.toUpperCase() || '')
    .join('') || 'N'
})
</script>

<style scoped>
.shell {
  min-height: 100vh;
  background: #f4f7fb;
}

.topbar {
  position: sticky;
  top: 0;
  z-index: 20;
  background: rgba(255, 255, 255, 0.98);
  border-bottom: 1px solid rgba(32, 62, 92, 0.08);
  box-shadow: 0 1px 0 rgba(255, 255, 255, 0.9), 0 10px 24px rgba(17, 32, 48, 0.03);
}

.topbar__inner {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0.8rem 1.25rem;
  display: grid;
  grid-template-columns: minmax(180px, auto) minmax(0, 1fr) auto;
  align-items: center;
  gap: 1rem;
}

.topbar__brand {
  display: inline-flex;
  align-items: center;
  flex: 0 0 auto;
  white-space: nowrap;
}

.brand {
  display: inline-flex;
  align-items: baseline;
  gap: 0.5rem;
  text-decoration: none;
  color: #10253d;
  white-space: nowrap;
}

.brand__title {
  font-size: 1.25rem;
  font-weight: 800;
  letter-spacing: -0.03em;
}

.brand__year {
  font-size: 0.82rem;
  padding: 0.18rem 0.5rem;
  border-radius: 999px;
  background: #eef3f9;
  color: #43607f;
  font-weight: 700;
}

.topbar__nav {
  display: flex;
  justify-content: center;
  gap: 0.5rem;
  flex-wrap: nowrap;
  min-width: 0;
  justify-self: center;
  white-space: nowrap;
  margin: 0;
  padding: 0;
  background: transparent;
  border: 0;
  box-shadow: none;
  align-self: center;
}

.auth-rail__guest {
  font-size: 0.82rem;
  font-weight: 700;
  color: #3f67a9;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  margin-right: 0.35rem;
}

.topbar__nav a {
  text-decoration: none;
  color: #3d5368;
  font-weight: 600;
  padding: 0.45rem 0.8rem;
  border-radius: 999px;
  transition: background-color 0.18s ease, color 0.18s ease, transform 0.18s ease, padding 0.18s ease;
}

.topbar__nav a:hover {
  background: rgba(28, 71, 143, 0.07);
  transform: translateY(-1px);
}

.topbar__nav a.router-link-exact-active {
  color: #13469a;
  background: rgba(19, 70, 154, 0.08);
  box-shadow: inset 0 0 0 1px rgba(19, 70, 154, 0.12);
}

.auth-rail {
  display: inline-flex;
  align-items: center;
  gap: 0.6rem;
  padding: 0.12rem 0 0.12rem 0.75rem;
  min-width: 0;
  flex: 0 0 auto;
  border-left: 1px solid rgba(89, 114, 141, 0.14);
  white-space: nowrap;
  justify-self: end;
}

.auth-rail__avatar {
  width: 2.35rem;
  height: 2.35rem;
  border-radius: 50%;
  display: grid;
  place-items: center;
  font-weight: 800;
  color: #fff;
  background: linear-gradient(135deg, #315ca8, #183a6d);
  box-shadow: 0 6px 14px rgba(23, 56, 98, 0.16);
  flex: 0 0 auto;
}

.auth-rail--active .auth-rail__avatar {
  background: linear-gradient(135deg, #315ca8, #183a6d);
  box-shadow: 0 8px 20px rgba(23, 56, 98, 0.18);
}

.auth-rail:not(.auth-rail--active) .auth-rail__avatar {
  display: none;
}

.auth-rail__copy {
  display: flex;
  flex-direction: column;
  line-height: 1.15;
  min-width: 0;
}

.auth-rail__copy strong {
  color: #122437;
  font-size: 0.98rem;
}

.auth-rail__copy span {
  color: #6b7a8a;
  font-size: 0.8rem;
}

.auth-rail__action {
  margin-left: auto;
  border: 0;
  border-radius: 999px;
  padding: 0.5rem 0.85rem;
  font-weight: 700;
  color: #fff;
  background: #12469b;
  box-shadow: 0 6px 14px rgba(18, 70, 155, 0.16);
}

.page-content {
  padding: 1.5rem;
}

@media (max-width: 760px) {
  .topbar__inner {
    grid-template-columns: 1fr;
  }

  .topbar__brand {
    margin-right: auto;
  }

  .topbar__nav {
    justify-content: flex-start;
    order: 3;
    width: 100%;
  }

  .auth-rail {
    justify-self: start;
    border-left: 0;
    padding-left: 0;
  }
}

@media (max-width: 640px) {
  .topbar__inner {
    padding: 0.85rem 1rem;
  }

  .page-content {
    padding: 1rem;
  }

  .auth-rail {
    width: 100%;
    padding-left: 0;
    margin-left: 0;
  }
}
</style>
