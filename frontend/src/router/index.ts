import { createRouter, createWebHistory } from 'vue-router'
import { setupRouterGuards } from './guards'
import Login from '../views/LoginView.vue'
import Dashboard from '../views/DashboardView.vue'
import Empleados from '../views/EmpleadosView.vue'
import Novedades from '../views/NovedadesView.vue'
import Nominas from '../views/NominasView.vue'

const routes = [
  { path: '/login', component: Login },
  { path: '/', component: Dashboard },
  { path: '/empleados', component: Empleados },
  { path: '/novedades', component: Novedades },
  { path: '/nominas', component: Nominas }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

setupRouterGuards(router)

export default router
