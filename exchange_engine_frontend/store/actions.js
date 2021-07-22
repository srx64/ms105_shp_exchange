import { listStoks, listStockPortfolio } from '../assets/data'

export default {
  async FETCH_LIST_STOCKS ({ state, commit, dispatch }) {
    if (!state.list_update) {
      commit('SET_LIST_STOCKS_UPDATE')
    }
    try {
      const promise = new Promise((resolve, reject) => {
        setTimeout(() => resolve(listStoks), 10000)
      })
      const result = await promise
      commit('SET_LIST_STOCKS', result)
      console.log('FETCH_LIST_STOCKS ' + new Date())
      setTimeout(() => { dispatch('FETCH_LIST_STOCKS') }, 30000)
    } catch (e) {
      console.log(e)
      setTimeout(() => { dispatch('FETCH_LIST_STOCKS') }, 10000)
    }
  },
  async FETCH_PORTFOLIO ({ state, commit, dispatch }) {
    if (!state.portfolio_update) {
      commit('SET_PORTFOLIO_UPDATE')
    }
    try {
      const promise = new Promise((resolve, reject) => {
        setTimeout(() => resolve(listStockPortfolio), 10000)
      })
      const result = await promise
      commit('SET_PORTFOLIO', result)
      console.log('FETCH_PORTFOLIO ' + new Date())
      setTimeout(() => { dispatch('FETCH_PORTFOLIO') }, 30000)
    } catch (e) {
      console.log(e)
      setTimeout(() => { dispatch('FETCH_PORTFOLIO') }, 10000)
    }
  }
}
