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
      {
        path: 'logout',
        name: 'Logout',
        component: () => import('../views/auth/children/Logout.vue')
      }
    ]
  },
  {
    path: '/app',
    component: () => import('../layouts/app/Index.vue'),
    meta: {
      requiresLogin: true
    },
    children: [
      {
        path: '',
        name: 'App',
        component: () => import('../views/app/Main.vue')
      },
      {
        path: 'profile',
        name: 'Profile',
        component: () => import('../views/app/Profile.vue')
      },
      {
        path: 'portfolio',
        name: 'Portfolio',
        component: () => import('../views/app/Portfolio.vue')
      }
    ]
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
