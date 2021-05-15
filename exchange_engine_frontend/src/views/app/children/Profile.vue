<template>
  <v-container>
    <h1>
      {{ profile.username }}
    </h1>
    
      <v-btn
        @click="chooseFile"
        absolute  
        small  
        fab
      >
        <input id="fileUpload" type="file" hidden @change="onFile" accept="image/*">
        <v-icon>mdi-pencil</v-icon>
      </v-btn>

      <v-avatar
        size="200px"
      >
        <v-img v-if="url" :src="url"/>
      </v-avatar>
    
      <v-card class="pa-6">
        <v-card-title> Редактировать профиль </v-card-title>
        <v-form>
          <v-text-field v-model="username" hint="" label="Никнейм"></v-text-field>
          <v-text-field v-model="first_name" hint="" label="Имя"></v-text-field>
          <v-text-field v-model="last_name" hint="" label="Фамилия"></v-text-field>
          <v-text-field v-model="email" hint="" label="Email"></v-text-field>
          <v-text-field v-model="balance" hint="" label="Balance"></v-text-field>
          <v-btn color="" @click="saveData"> Сохранить </v-btn>
        </v-form>
      </v-card>

      <!-- <v-card class="pa-6">
        <v-card-title> Изменить пароль </v-card-title>
        <v-form>
          <v-text-field v-model="password" hint="" type="password" label="Старый пароль"></v-text-field>
          <v-text-field v-model="password2" hint="" type="password" label="Новый пароль"></v-text-field>
          <v-btn color="" @click="saveData"> Изменить </v-btn>
        </v-form>
      </v-card> -->
  </v-container>
</template>

<script>
import { getAPI } from '../../../axios-api'

export default {
  name: 'Profile',

  data: () => ({
    username: '',
    first_name: '',
    last_name: '',
    email: '',
    balance: 0,
    url: ''
  }),

  computed: {
    profile() {
      return this.$store.getters.profile
    }
  },

  methods: {
    saveData(){
      getAPI.patch('api/v1/profile/', {
        first_name: this.first_name,
        last_name: this.last_name,
        email: this.email,
        password: this.password,
        password2: this.password2,
      },
      {
        headers: { 
          Authorization: `Bearer ${this.$store.getters.accessToken}` 
        } 
      })
        .then(res => {
          console.log(res)
          this.saveProfile()
          this.$store.commit({
            type: 'showSnackbar',
            text: 'Профиль изменён'
          })
        })
        .catch(err => {
          console.log(err)
          this.$store.commit({
            type: 'showSnackbar',
            text: 'Введите корректные данные'
          })
        })
    },
    chooseFile(){
      document.getElementById("fileUpload").click()
    },
    onFile(event){
      this.selectedFile = event.target.files[0]
      this.url = URL.createObjectURL(this.selectedFile);
      const fd = new FormData();
      fd.append('file', this.selectedFile, this.selectedFile.name)
      getAPI.patch('api/v1/profile/', fd, {
          headers: { 
            Authorization: `Bearer ${this.$store.state.accessToken}` 
          } 
        })
        .then(res => {
          console.log(res, fd)
          this.profile.avatar = this.url
        })   
    },
    getProfile () {
      this.username = this.profile.username
      this.first_name = this.profile.first_name
      this.last_name = this.profile.last_name
      this.email = this.profile.email
      this.balance = this.profile.balance
      this.url = this.profile.avatar
    },
    saveProfile () {
      this.profile.username = this.username
      this.profile.first_name = this.first_name
      this.profile.last_name = this.last_name
      this.profile.email = this.email
      this.profile.balance = this.balance
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
