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
      localStorage.setItem('accessToken', null);
      localStorage.setItem('refreshToken', null)
    },
  },
  actions: {
    initialiseToken(context) {
      context.commit('initialiseStore')
    }
  }
}