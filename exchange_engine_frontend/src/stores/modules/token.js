export default {
  state: {
    accessToken: null,
    refreshToken: null,
  },
  getters: {
    loggedIn (state) {
      return state.accessToken != null
    },
  },
  mutations: {
    destroyToken (state) {
      state.accessToken = null
      state.refreshToken = null
    },
  },
  
}