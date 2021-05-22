export default {
  state: {
    snackbarText: ''
  },
  mutations: {
    showSnackbar (state, payload) {
      state.snackbarText = payload.text
    }
  }
}