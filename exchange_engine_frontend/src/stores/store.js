import Vue from 'vue'
import Vuex from 'vuex'

import User from './modules/user'
import Token from './modules/token'

Vue.use(Vuex)

export default new Vuex.Store({
  modules: {
    token: Token,
    user: User,
   
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
    
    
    showSnackbar (state, payload) {
      state.snackbarText = payload.text
    },

  },
})