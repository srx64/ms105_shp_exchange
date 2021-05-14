import Vue from 'vue'
import Vuex from 'vuex'

import User from './modules/user'
import Token from './modules/token'

Vue.use(Vuex)

export default new Vuex.Store({
  modules: {
    user: User,
    token: Token
  },
  state: {
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
    
    showSnackbar (state, payload) {
      state.snackbarText = payload.text
    },

  },
})