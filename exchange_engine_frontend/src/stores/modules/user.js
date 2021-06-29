import { getAPI } from '@/axios-api'

export default {
  state: {
    profile: {},
    portfolio: []
  },
  getters: {
    profile: state => {
      return state.profile
    },
    portfolio: state => {
      return state.portfolio
    }
  },
  mutations: {
    updateProfile(state, payload) {
      state.profile = payload
    },
    updatePortfolio(state, payload) {
      state.portfolio = payload
    }
  },
  actions: {
    userLogin (context, usercredentials) {
      return new Promise((resolve, reject) => {
        getAPI.post('/api-token/', {
          username: usercredentials.username,
          password: usercredentials.password
        })
          .then(response => {
            context.commit('updateStorage', { access: response.data.access, refresh: response.data.refresh })
            resolve()
          })
          .catch(err => {
            reject(err)
          })
      })
    },
    userReg (context, usercredentials) {
      return new Promise((resolve, reject) => {
        getAPI.post('api/v1/register/', {
          email: usercredentials.email,
          username: usercredentials.username,
          password: usercredentials.password,
          password2: usercredentials.password2
        })
          .then(response => {
            resolve(response)
          })
          .catch(err => {
            reject(err)
          })
      })
    },
    userLogout (context) {
      if (context.getters.loggedIn) {
          context.commit('destroyToken')
      }
    },
    refreshToken (context) {
      return new Promise((resolve, reject) => {
        getAPI.post('/api-token-refresh/', {
          refresh: context.getters.getRefresh
        })
          .then(response => {
            context.commit('updateStorage', { access: response.data.access, refresh: context.getters.getRefresh })
            resolve()
          })
          .catch(err => {
            reject(err)
          })
      })
    },
    getProfile(context) {
      return new Promise((resolve, reject) => {
        getAPI.get('/api/v1/profile/', {
          headers: {
            Authorization: `Bearer ${context.getters.accessToken}`
          }
        })
          .then(response => {
            console.log(response.data.avatar)
            if (response.data.avatar.indexOf(getAPI.defaults.baseURL) != 0)
              response.data.avatar = getAPI.defaults.baseURL + response.data.avatar
            console.log(response.data.avatar)
            context.commit('updateProfile', response.data)
            resolve()
          })
          .catch(err => {
            reject(err)
          })
      })
    },
    getPortfolio(context) {
      return new Promise((resolve, reject) => {
        getAPI.get('/api/v1/portfolio/', {
          headers: {
            Authorization: `Bearer ${context.getters.accessToken}`
          }
        })
          .then(response => {
            if (context.getters.profile.is_superuser) {
              for (let security of response.data) {
                if (!context.getters.usernames.has(security.user)) {
                  context.dispatch('loadUsername', { id: security.user })
                }
                security.user = context.getters.usernames.get(security.user)
              }
              response.data.sort(function (a, b) {
                a.user.toLowerCase()
                b.user.toLowerCase()
                if (a.user != b.user) {
                  return a.user > b.user ? 1 : -1
                }
                return 0;
              })
            }
            context.commit('updatePortfolio', response.data)
            resolve()
          })
          .catch(err => {
            reject(err)
          })
      })
    }
  }
}
