import Vue from 'vue'
import VueRouter from 'vue-router'

import Main from '../views/main/Base.vue'
import Authentication from '../views/authentication/Base.vue'
import App from '../views/app/Base.vue' 

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Main',
    component: Main
  },
  {
    path: '/authentication',
    name: 'Authentication',
    component: Authentication,
    children: [
      {
        path: 'login',
        component: () => import('../views/authentication/children/Login.vue')
      },
      {
        path: 'registration',
        component: () => import('../views/authentication/children/Registration.vue')
      }
    ]
  },
  {
    path: '/app',
    name: 'App',
    component: App
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
