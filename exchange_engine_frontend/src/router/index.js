import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    component: () => import('../components/home/layouts/Index.vue'),
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
    component: () => import('../views/app/View.vue'),
    meta: {
      requiresLogin: false
    },
    children: [
      {
        path: '',
        name: 'App',
        component: () => import('../views/app/children/Main.vue')
      },
      {
        path: 'profile',
        name: 'Profile',
        component: () => import('../views/app/children/Profile.vue')
      },
      {
        path: 'portfolio',
        name: 'Portfolio',
        component: () => import('../views/app/children/Portfolio.vue')
      },
      {
        path: 'orders',
        name: 'Orders',
        component: () => import('../views/app/children/Orders.vue')
      }
    ]
  },
  {
    path: '/test',
    component: () => import('../views/test/Graph.vue'),
    children: [
      {
        path: 'hexagon-ava',
        name: 'Hexagon',
        component: () => import('../views/test/Hexagon.vue')
      },
      {
        path: 'graph',
        name: 'Graph',
        component: () => import('../views/test/Graph.vue')
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
