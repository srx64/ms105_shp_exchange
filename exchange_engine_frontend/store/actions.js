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
      try {
        this.$axios.get('/api/v1/stocks/' + id)
          .then((response) => {
            commit('SET_STOCK', response.data)
          })
        dispatch('FETCH_CANDLES', id)
        resolve()
      } catch (err) {
        reject(err)
      }
    })
  },
  FETCH_CANDLES ({
    state,
    commit,
    dispatch
  }, id) {
    return new Promise((resolve, reject) => {
      try {
        this.$axios.get('/api/v1/candles/' + id + '/1')
          .then((response) => {
            commit('SET_CANDLES', response.data.sort((a, b) => (a.date < b.date && -1) || (a.date > b.date && 1) || 0))
          })
        resolve()
      } catch (err) {
        reject(err)
      }
    })
  },
  FETCH_PORTFOLIO ({
    state,
    commit,
    dispatch
  }) {
    return new Promise((resolve, reject) => {
      try {
        this.$axios.get('/api/v1/portfolio/')
          .then((response) => {
            commit('SET_PORTFOLIO', response.data)
          })
        resolve()
      } catch (err) {
        reject(err)
      }
    })
  },
  FETCH_RATING ({
    state,
    commit,
    dispatch
  }) {
    return new Promise((resolve, reject) => {
      try {
        this.$axios.get('api/v1/balance_statistics/')
          .then((response) => {
            commit('SET_RATING', response.data)
          })
        resolve()
      } catch (err) {
        reject(err)
      }
    })
  },
  FETCH_ORDERS ({
    state,
    commit,
    dispatch
  }) {
    return new Promise((resolve, reject) => {
      try {
        this.$axios.get('api/v1/orders/')
          .then((response) => {
            commit('SET_ORDERS', response.data)
          })
        resolve()
      } catch (err) {
        reject(err)
      }
    })
  }
}
