import Vue from 'vue'
import Vuex from 'vuex'

import User from './modules/user'
import Token from './modules/token'
import Snackbar from './modules/snackbar'

Vue.use(Vuex)

export default new Vuex.Store({
  modules: {
    token: Token,
    user: User,
    snackbar: Snackbar,
  }
})