<template>
  <v-app-bar
    id="home-app-bar"
		app
		elevation="1"
		elevate-on-scroll
		height="80"
	>
    <v-row>
      <v-col>
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
        </v-tabs>
      </v-col>
      <v-col
        class="d-flex justify-end "
      >
        <v-avatar
          size="40px"
          color="primary"
        >
          <span 
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
	export default {
		name: 'HomeAppBar',

    data: () => ({
      profile: {
        avatar: '',
        surname: 'Surname',
        name: 'Name',
        balance: '0   '
      }
    }),

    computed: {
      fullName() {
        return this.profile.surname + ' ' + this.profile.name
      },
      getInitials() {
        let initials = this.profile.surname[0] + this.profile.name[0]
        return initials.toUpperCase()
      }
    }
	}
</script>