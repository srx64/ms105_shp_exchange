import Vue from 'vue'
import Vuex from 'vuex'

import User from './modules/user'
import SuperUser from './modules/superuser'
import Token from './modules/token'
import Snackbar from './modules/snackbar'

Vue.use(Vuex)

export default new Vuex.Store({
  modules: {
    token: Token,
    user: User,
    superuser: SuperUser,
    snackbar: Snackbar,
  }
})
