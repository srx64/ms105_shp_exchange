<template>
  <div>
    <h1 class="display-2 font-weight-bold mb-3">
      User {{ username }}
    </h1>
    <h3>
      Email: {{ email }}
    </h3>
    <h3>
      balance: {{ balance }}
    </h3>\
  </div>
</template>

<script>
  import { getAPI } from '../../axios-api'
  import { mapState } from 'vuex'

  export default {
    name: 'App',

    data: () => ({
      username: '',
      email: '',
      balance: ''
    }),

    computed: mapState(['APIData']),

    onIdle () {
      console.log('refresh')
      this.$store.dispatch('userRefresh')
    },

    methods: {
      getProfile () {
        getAPI.get('api/v1/profile/', {
            headers: { 
              Authorization: `Bearer ${this.$store.state.accessToken}` 
            } 
          })
          .then(response => {
            this.$store.state.APIData = response.data
            let profile = response.data.profile
            this.username = profile.username
            this.email = profile.email
            this.balance = profile.balance
          })
          .catch(err => {
            console.log(err)
          })
      }
    },

    mounted () {
      this.getProfile()
    }
  }
</script>