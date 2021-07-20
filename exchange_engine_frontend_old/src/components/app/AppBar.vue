<template>
  <v-app-bar
    id="home-app-bar"
    color="grey lighten-4"
		app
		elevation="1"
    style="z-index: 13"
		elevate-on-scroll
		height="80"
	>
    <v-row>
      <v-col
        class="d-flex align-center hidden-sm-and-down"
      >
        <BaseImg
          :src="require('@/assets/logo_shp_exchange_horizontal.png')"
          contain
          max-width="150"
          width="100%"
        />
      </v-col>
      <v-col
        class="d-flex justify-center align-center"
      >
        <v-btn 
          to="/app"
          value="exchange"
          class="mx-2"
          exact
          text
        >
          <span>Биржа</span>

          <v-icon
            class="ml-1"
          >
            mdi-finance
          </v-icon>
        </v-btn>
        <v-btn 
          to="/app/portfolio"
          value="portfolio"
          class="mx-2"
          exact
          text
        >
          <span>Портфель</span>

          <v-icon
            class="ml-1"
          >
            mdi-briefcase-account-outline
          </v-icon>
        </v-btn>
        <v-btn 
          to="/app/orders"
          value="orders"
          class="mx-2"
          exact
          text
        >
          <span>Заявки</span>

          <v-icon
            class="ml-1"
          >
            mdi-order-bool-descending-variant
          </v-icon>
        </v-btn>
      </v-col>
      <v-col
        class="d-flex justify-end align-center"
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
                color="grey lighten-3"
                size="48"
              >
                <v-img v-if="profile.avatar" class="d-flex align-center" :src="profile.avatar"/>
                <span v-else-if="profile.first_name && profile.last_name" class="white--text headline">{{ getInitials }}</span>
              </v-avatar>
            </v-btn>
          </template>
          <v-card>
            <v-list-item-content class="justify-center">
              <div class="mx-auto text-center">
                <v-avatar
                  color="grey lighten-3"
                >
                  <v-img v-if="profile.avatar" :src="profile.avatar"/>
                  <span v-else-if="profile.first_name && profile.last_name" class="white--text headline">{{ getInitials }}</span>
                </v-avatar>
                <h3 v-if="profile.first_name && profile.last_name">{{ fullName }}</h3>
                <p v-if="profile.email" class="caption mt-1">
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
	export default {
		name: 'HomeAppBar',

    computed: {
      profile() {
        return this.$store.getters.profile
      },
      fullName() {
        return this.profile.last_name + ' ' + this.profile.first_name
      },
      getInitials() {
        return this.profile.last_name[0] + this.profile.first_name[0]
      }
    }
	}
</script>