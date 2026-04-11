import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import EmpleadosView from '../views/EmpleadosView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/empleados',
      name: 'empleados',
      component: EmpleadosView
    },
    {
      path: '/novedades',
      name: 'novedades',
      component: () => import('../views/NovedadesView.vue')
    },
    {
      path: '/nominas',
      name: 'nominas',
      component: () => import('../views/NominasView.vue')
    }
  ]
})

export default router
