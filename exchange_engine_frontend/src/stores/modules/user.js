import { getAPI } from '@/axios-api'

export default {
  state: {
    profile: {
      surname: 'Иванченко',
      name: 'Антон',
      email: 'test@test.ru',
      balance: 2303,
      avatar: 'http://surl.li/sfip'
    }
  },
  getters: {
    PROFILE: state => {
      return state.profile
    }
  },
  mutations: {},
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
            console.log(response);
            resolve(response)
          })
          .catch(err => {
            reject(err)
          })
      })
    },
    refreshToken (context) {
      return new Promise((resolve, reject) => {
        getAPI.post('/api-token-refresh/', {
          refresh: context.getters.getRefresh
        })
          .then(response => {
            context.commit('updateStorage', { access: response.data.access, refresh: context.getters.getRefresh })
            console.log(response.data.access)
            resolve()
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
  }
}