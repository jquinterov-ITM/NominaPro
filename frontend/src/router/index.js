import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import EmpleadosView from '../views/EmpleadosView.vue'
import { useAuthStore } from '../stores/auth'

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
      meta: { requiresAuth: true },
      component: EmpleadosView
    },
    {
      path: '/novedades',
      name: 'novedades',
      meta: { requiresAuth: true },
      component: () => import('../views/NovedadesView.vue')
    },
    {
      path: '/nominas',
      name: 'nominas',
      meta: { requiresAuth: true },
      component: () => import('../views/NominasView.vue')
    }
  ]
})

router.beforeEach((to) => {
  const auth = useAuthStore()
  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    return { name: 'home' }
  }

  if (to.name === 'home' && auth.isAuthenticated) {
    return { name: 'empleados' }
  }

  if (!auth.isAuthenticated && to.name !== 'home') {
    return { name: 'home' }
  }

  return true
})

export default router
