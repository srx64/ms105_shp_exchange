import { getAPI } from '@/axios-api'

export default {
  state: {
    profile: {
      surname: 'Иванченко',
      name: 'Антон',
      email: 'test@test.ru',
      balance: 2303,
      avatar: 'http://surl.li/sfip'
    },
    portfolio: [
      {
        "id": 2,
        "index": "0",
        "name": "FB",
        "description": "Facebook",
        "is_active": true,
        "price": 5316.452990988047
      },
      {
          "id": 3,
          "index": "0",
          "name": "MSFT",
          "description": "Microsoft",
          "is_active": true,
          "price": 5607.362115399917
      }
    ]
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
    userReg (usercredentials) {
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
            
            console.log(response.data.access)
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
            context.commit('updateProfile', response.data) 
            console.log(response.data)
            resolve()
          })
          .catch(err => {
            console.log(context.getters.profile)
            reject(err)
          })
      })
    }
  }
}