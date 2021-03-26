import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    component: () => import('../layouts/home/Index.vue'),
    children: [
      {
        path: '',
        name: 'Home',
        component: () => import('../views/home/Index.vue'),
      }
    ]
  },
  {
    path: '/auth',
    component: () => import('../views/auth/Base.vue'),
    children: [
      {
        path: 'login',
        name: 'Login',
        component: () => import('../views/auth/children/Login.vue'),
      },
      {
        path: 'registration',
        name: 'Registration',
        component: () => import('../views/auth/children/Registration.vue'),
      },
    ]
  },
  {
    path: '/app',
    name: 'App',
    component: () => import('../views/app/Base.vue')
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
