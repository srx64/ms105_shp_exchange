export default {
  state: {
    snackbarText: ''
  },
  getters: {
    snackbarText (state) {
      return state.snackbarText
    }
  },
  mutations: {
    showSnackbar (state, payload) {
      state.snackbarText = payload.text
    }
  }
}