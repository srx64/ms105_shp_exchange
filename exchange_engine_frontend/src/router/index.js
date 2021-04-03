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
        component: () => import('../views/home/children/Index.vue'),
      }
    ]
  },
  {
    path: '/auth',
    component: () => import('../views/auth/View.vue'),
    children: [
      {
        path: 'login',
        name: 'Login',
        component: () => import('../views/auth/children/Login.vue'),
      },
      {
        path: 'reg',
        name: 'Registration',
        component: () => import('../views/auth/children/Reg.vue'),
      },
    ]
  },
  {
    path: '/app',
    name: 'App',
    component: () => import('../views/app/View.vue'),
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
