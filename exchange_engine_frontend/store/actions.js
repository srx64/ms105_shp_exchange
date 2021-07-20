import { listStoks } from './data'

export default {
  async FETCH_LIST_STOCKS ({ state, commit, dispatch }) {
    try {
      const promise = new Promise((resolve, reject) => {
        setTimeout(() => resolve(listStoks), 10000)
      })
      const result = await promise
      commit('SET_LIST_STOCKS', result)
      console.log(result)
    } catch (e) {
      console.log(e)
    }
  }
}
