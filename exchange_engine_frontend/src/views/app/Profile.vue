<template>
  <v-container>
    <h1> {{username}} </h1>


    <!-- <v-row align="center" justify="center"> -->
      <v-btn absolute color="primary" fab @click="chooseFile"
              small dark >
              <input id="fileUpload" type="file" hidden @change="onFile">
              <v-icon>mdi-pencil</v-icon>
            </v-btn>

      <v-avatar
            size="200px"
            color="primary">
            <img v-if="url" :src="url"/>
            <span v-else class="white--text headline">
              {{ first_name[0] }} {{ last_name[0] }}
            </span>
      </v-avatar>
    <!-- </v-row> -->
    
      <v-card class="pa-6">
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
      <v-form>
        <v-file-input @change="onFile"
            v-model="file"
            color="primary"
            counter
            label="File input"
            placeholder="Select your files"
            prepend-icon="mdi-paperclip"
            outlined
            :show-size="1000"
          >
            <template v-slot:selection="{ index, text }">
              <v-chip
                v-if="index < 2"
                color="primary"
                dark
                label
                small
              >
                {{ text }}
              </v-chip>
            </template>
          </v-file-input>
        <v-btn x-small @click="onUpload" > <v-icon small> mdi-pencil </v-icon> Изменить </v-btn>
      </v-form>
    </v-card> -->

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
      selectedFile: null,
      url: null,
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
            this.url = 'http://127.0.0.1:8000' + response.data.avatar.avatar
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
      },
      chooseFile(){
        document.getElementById("fileUpload").click()
      },
      onFile(event){
        let ev = event.target.files[0]
        console.log(ev)
        this.selectedFile = ev
        this.url = URL.createObjectURL(this.selectedFile);
        const fd = new FormData();
        fd.append('file', this.selectedFile, this.selectedFile.name)
        getAPI.patch('api/v1/profile/', fd, {
            headers: { 
              Authorization: `Bearer ${this.$store.state.accessToken}` 
            } 
          })
          .then(res => {
            console.log(res)
          })
      },
      // onUpload(){
      //   const fd = new FormData();
      //   fd.append('file', this.selectedFile, this.selectedFile.name)
      //   getAPI.patch('api/v1/profile/', fd, {
      //       headers: { 
      //         Authorization: `Bearer ${this.$store.state.accessToken}` 
      //       } 
      //     })
      //     .then(res => {
      //       console.log(res)
      //     })
      // }
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
