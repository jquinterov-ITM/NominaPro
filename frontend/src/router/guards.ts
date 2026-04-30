import { useAuthStore } from '../stores/auth'

// Router guard para proteger rutas
export function setupRouterGuards(router: any) {
  router.beforeEach((to: any, from: any, next: any) => {
    const authStore = useAuthStore()
    const isLoginPage = to.path === '/login'

    // Si no hay token y no está en login, redirigir a login
    if (!authStore.isAuthenticated && !isLoginPage) {
      next('/login')
    }
    // Si hay token y está en login, redirigir a dashboard
    else if (authStore.isAuthenticated && isLoginPage) {
      next('/')
    }
    // Si no hay token y está en login, permitir
    else {
      next()
    }
  })
}

