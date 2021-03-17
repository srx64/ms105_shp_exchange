<template>
  <v-app-bar
      app
      color="primary"
      dark
    >
      <div class="d-flex align-center">
        <v-img
          alt="Vuetify Logo"
          class="shrink mr-2"
          contain
          src="https://cdn.vuetifyjs.com/images/logos/vuetify-logo-dark.png"
          transition="scale-transition"
          width="40"
        />

        <h1>
          Exchange Engine
        </h1>
      </div>


      <v-spacer></v-spacer>

      
      <v-btn
        color="white"
        outlined
        small
        class="mr-3"
        to="/authentication/login"
      >
        Войти
      </v-btn>

      <v-btn
        color="white"
        class="primary--text"
        to="/authentication/registration"
      >
        Зарегистрироваться
      </v-btn>
    </v-app-bar>
</template>

<script>
  export default {
    name: 'Header'
  }
</script>
