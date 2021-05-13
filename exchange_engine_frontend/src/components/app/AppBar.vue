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
          :src="require('@/assets/logo_shp_exchange_horizontal.png')"
          contain
          max-width="150"
          width="100%"
        />
      </v-col>
      <v-col
        class="d-flex justify-center"
      >
        <v-btn 
          to="/app"
          value="exchange"
          class="mx-2"
          exact
        >
          <span>Биржа</span>

          <v-icon>mdi-finance</v-icon>
        </v-btn>
        <v-btn 
          to="/app/portfolio"
          value="portfolio"
          class="mx-2"
          exact
        >
          <span>Портфель</span>

          <v-icon>mdi-briefcase-account-outline</v-icon>
        </v-btn>
      </v-col>
      <v-col
        class="d-flex justify-end "
      >
        <v-menu
          bottom
          min-width="200px"
          rounded
          offset-y
        >
          <template v-slot:activator="{ on }">
            <v-btn
              icon
              x-large
              v-on="on"
            >
              <v-avatar
                color="brown"
                size="48"
              >
                <span class="white--text headline">{{ getInitials }}</span>
              </v-avatar>
            </v-btn>
          </template>
          <v-card>
            <v-list-item-content class="justify-center">
              <div class="mx-auto text-center">
                <v-avatar
                  color="brown"
                >
                  <span class="white--text headline">{{ getInitials }}</span>
                </v-avatar>
                <h3>{{ fullName }}</h3>
                <p class="caption mt-1">
                  {{ profile.email }}
                </p>
                <v-divider class="my-3"></v-divider>
                <v-btn
                
                  to="/app/profile"
                  depressed
                  text
                >
                  Профиль
                </v-btn>
                <v-divider class="my-3"></v-divider>
                <v-btn
                  to="/auth/logout"
                  depressed
                  color="red"
                  text
                >
                  Выйти
                </v-btn>
              </div>
            </v-list-item-content>
          </v-card>
        </v-menu>
        
      </v-col>
    </v-row>
  </v-app-bar>
</template>

<script>
  import { mapState } from 'vuex'
  
	export default {
		name: 'HomeAppBar',

    computed: {
      ...mapState(['profile']),
      fullName() {
        return this.profile.surname + ' ' + this.profile.name
      },
      getInitials() {
        let initials = this.profile.surname[0] + this.profile.name[0]
        return initials
      }
    }
	}
</script>

<style scoped>
  .redbtn {
    color: red;
  }
</style>