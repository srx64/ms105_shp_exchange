import { getAPI } from '@/axios-api'

export default {
  state: {
    usernames: new Map()
  },
  getters: {
    usernames(state) {
      return state.usernames;
    }
  },
  mutations: {
    addUsername(state, { id, username }) {
      state.usernames.set(id, username)
    }
  },
  actions: {
    loadUsername(context, { id }) {
      return new Promise((resolve, reject) => {
        getAPI.get('/api/v1/profile/' + id, {
          headers: {
            Authorization: `Bearer ${context.getters.accessToken}`
          }
        })
          .then(response => {
            context.commit('addUsername', { id: id, username: response.data.username })
            resolve()
          })
          .catch(err => {
            reject(err)
          })
      })
    }
  }
}
