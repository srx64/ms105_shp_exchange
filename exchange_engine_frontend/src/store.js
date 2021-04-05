import Vue from 'vue'
import Vuex from 'vuex'
import { getAPI } from './axios-api'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    accessToken: null,
    refreshToken: null,
    APIData: ''
  },

  mutations: {
    initialiseStore(state) {
      if (localStorage.getItem('accessToken')) {
        state.accessToken = localStorage.getItem('accessToken')
      }
      if (localStorage.getItem('refreshToken')) {
        state.refreshToken = localStorage.getItem('refreshToken')
      }
    },
    updateStorage (state, { access, refresh }) {
      state.accessToken = access
      state.refreshToken = refresh
      localStorage.setItem('accessToken', access);
      localStorage.setItem('refreshToken', refresh)
    },
    destroyToken (state) {
      state.accessToken = null
      state.refreshToken = null
    }
  },

  getters: {
    loggedIn (state) {
      return state.accessToken != null
    },
    getRefresh (state) {
      return state.refreshToken
    }
  },

  actions: {
    userLogout (context) {
      if (context.getters.loggedIn) {
          context.commit('destroyToken')
      }
    },
    userLogin (context, usercredentials) {
      return new Promise((resolve, reject) => {
        getAPI.post('/api-token/', {
          username: usercredentials.username,
          password: usercredentials.password
        })
          .then(response => {
            context.commit('updateStorage', { access: response.data.access, refresh: response.data.refresh }) 
            resolve()
          })
          .catch(err => {
            reject(err)
          })
      })
    },
    userReg (context, usercredentials) {
      return new Promise((resolve, reject) => {
        getAPI.post('api/v1/register/', {
          email: usercredentials.email,
          username: usercredentials.username,
          password: usercredentials.password,
          password2: usercredentials.password2
        })
          .then(response => {
            console.log(response);
            resolve()
          })
          .catch(err => {
            reject(err)
          })
      })
    },
    userRefresh (context) {
      return new Promise((resolve, reject) => {
        getAPI.post('/api-token-refresh/', {
          refresh: context.getters.getRefresh
        })
          .then(response => {
            context.commit('updateStorage', { access: response.data.access, refresh: context.getters.getRefresh })
            console.log(response.data.access)
            resolve()
          })
          .catch(err => {
            reject(err)
          })
      })
    }
  }
})