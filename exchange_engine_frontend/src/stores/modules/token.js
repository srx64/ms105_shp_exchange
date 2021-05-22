export default {
  state: {
    accessToken: null,
    refreshToken: null,
  },
  getters: {
    loggedIn (state) {
      return state.accessToken != null
    },
    accessToken (state) {
      return state.accessToken
    }
  },
  mutations: {
    updateStorage (state, { access, refresh }) {
      state.accessToken = access
      state.refreshToken = refresh
      localStorage.setItem('accessToken', access);
      localStorage.setItem('refreshToken', refresh)
    },
    destroyToken (state) {
      state.accessToken = null
      state.refreshToken = null
    },
  },
  
}