<template>
  <v-container>
    <v-text-field v-model="username" hint="" label="Никнейм"></v-text-field>
    <v-text-field v-model="first_name" hint="" label="Имя"></v-text-field>
    <v-text-field v-model="last_name" hint="" label="Фамилия"></v-text-field>
    <v-text-field v-model="email" hint="" label="Email"></v-text-field>
    <v-text-field v-model="balance" hint="" label="Balance"></v-text-field>

    <v-btn color="" class="mr-0" @click="saveData"> Сохранить </v-btn>
  </v-container>
</template>

<script>
// @ is an alias to /src
  import { getAPI } from '../../axios-api'
  import { mapState } from 'vuex'

export default {
  name: 'Profile',
  data() {
    return {
      username: '',
      email: '',
      first_name: '',
      last_name: '',
      balance: '',
      avatar: '',
    };
  },

  computed: mapState(['APIData']),

  onIdle () {
      console.log('refresh')
      this.$store.dispatch('userRefresh')
    },

  created () {
      this.get_data()
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
            this.first_name = profile.first_name
            this.last_name = profile.last_name
            this.balance = profile.balance
          })
          .catch(err => {
            console.log(err)
          })
      },
      saveData(){
        getAPI.patch('api/v1/profile/', {
            first_name: this.first_name,
            last_name: this.last_name,
            email: this.email,
        },
        {
            headers: { 
              Authorization: `Bearer ${this.$store.state.accessToken}` 
            } 
          })
      }
    },

    mounted () {
      this.getProfile()
    }
  }
</script>

<style scoped>
.container{
  text-align: center;
  width: 500px;
}
</style>
