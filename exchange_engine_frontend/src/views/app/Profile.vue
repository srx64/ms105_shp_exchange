<template>
  <v-container>
    <v-text-field v-model="username" hint="This field uses counter prop" label="Username"></v-text-field>
    <v-text-field v-model="first_name" hint="This field uses counter prop" label="First Name"></v-text-field>
    <v-text-field v-model="last_name" hint="This field uses counter prop" label="Last Name"></v-text-field>
    <v-text-field v-model="email" hint="This field uses counter prop" label="Email"></v-text-field>

    <v-btn color="" class="mr-0" @click="send"> Сохранить </v-btn>

    <button v-on:click="get_data"> GET </button>
  </v-container>
</template>

<script>
// @ is an alias to /src
import axios from 'axios'

export default {
  name: 'Profile',
  data() {
    return {
      info: null,
      username: '',
      email: '',
      first_name: '',
      last_name: '',
      avatar: '',
    };
  },
  created () {
      this.get_data()
  },
  methods: {
    get_data () {
          axios
      .get('https://api.npoint.io/e07d530886a2fd5afbcc',)
      .then(response => {
        this.info = response.data;
        this.username = this.info.profile.username;
        this.first_name = this.info.profile.first_name;
        this.last_name = this.info.profile.last_name;
        this.email = this.info.profile.email;
        this.avatar = this.info.profile.avatar;
      });
    },
    send () {
      this.email = ''
    }
  }
}
</script>

<style scoped>
.container{
  text-align: center;
  width: 500px;
}
</style>
