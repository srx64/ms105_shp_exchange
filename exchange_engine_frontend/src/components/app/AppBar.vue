<template>
  <v-app-bar
    id="home-app-bar"
    color="grey lighten-4"
		app
		elevation="1"
		elevate-on-scroll
		height="80"
	>
    <v-row>
      <v-col
        class="hidden-sm-and-down"
      >
        <BaseImg
          :src="require('@/assets/logo.png')"
          contain
          max-width="46"
          width="100%"
        />
      </v-col>
      <v-col>
        <v-tabs
          centered
          background-color="grey lighten-4"
        >
          <v-tab
            to="/app"
          >
            Главная
          </v-tab>
          <v-tab
            to="/app/profile"
          >
            Профиль
          </v-tab>
          <v-tab
            to="/app/portfolio"
          >
            Портфель
          </v-tab>
        </v-tabs>
      </v-col>
      <v-col
        class="d-flex justify-end "
      >
        <v-avatar
          size="40px"
          color="primary"
        >
          <v-img 
            v-if="avatar"
            :src="avatar"
          />
          <span 
            v-else
            class="white--text headline"
          >
            {{ getInitials }}
          </span>
        </v-avatar>

        <div
          class="text-center"
        >
          <strong>
            {{ fullName }}
          </strong>
          <br>
          <BaseBtn
            to="/auth/logout"
            class="pa-1"
            color="red"
            height="auto"
            small 
            text  
          >
            Выйти
          </BaseBtn>
        </div> 
      </v-col>
    </v-row>
  </v-app-bar>
</template>

<script>
  import { getAPI } from '@/axios-api'
  
	export default {
		name: 'HomeAppBar',

    data: () => ({
      surname: 'Ф',
      name: 'А',
      balance: 0,
      avatar: '@/assets/andrey.jpg'
    }),

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
            this.surname = profile.first_name
            this.name = profile.last_name
            this.balance = profile.balance
            if (response.data.avatar.avatar){
              this.avatar = 'http://127.0.0.1:8000' + response.data.avatar.avatar
            }
          })
          .catch(err => {
            console.log(err)
          })
      },
    },

    computed: {
      fullName() {
        return this.surname + ' ' + this.name
      },
      getInitials() {
        let initials = this.surname[0] + this.name[0]
        return initials
      }
    },

    created () {
      this.getProfile()
      this.$store.subscribe((mutation) => {
        if (mutation.type === 'changeProfile') {
          this.getProfile()
        }
      })
    }
	}
</script>