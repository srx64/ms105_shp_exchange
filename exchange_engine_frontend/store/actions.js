export default {
  FETCH_LIST_STOCKS ({
    state,
    commit,
    dispatch
  }) {
    return new Promise((resolve, reject) => {
      this.$axios.get('/api/v1/stocks/')
        .then((response) => {
          commit('SET_LIST_STOCKS', response.data)
          resolve()
        })
        .catch((err) => {
          reject(err)
        })
    })
  },
  FETCH_STOCK ({
    state,
    commit,
    dispatch
  }, id) {
    return new Promise((resolve, reject) => {
      this.$axios.get('/api/v1/stocks/' + id)
        .then((response) => {
          commit('SET_STOCK', response.data)
        })
      console.log('1')
      dispatch('FETCH_CANDLES', id)
      console.log('2')
      resolve()
    })
  },
  async FETCH_CANDLES ({
    state,
    commit,
    dispatch
  }, id) {
    const res = await this.$axios.get('/api/v1/candles/' + id + '/1')
    console.log(new Date())
    console.log(res)
    commit('SET_CANDLES', res.data.data)
  },
  async FETCH_PORTFOLIO ({
    state,
    commit,
    dispatch
  }) {
    const res = await this.$axios.get('/api/v1/portfolio/')
    commit('SET_PORTFOLIO', res.data)
    console.log(new Date())
    console.log(res)
  }
}
