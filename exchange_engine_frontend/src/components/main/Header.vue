<template>
  <v-app-bar
      app
      color="grey"
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
        color="primary"
        outlined
        small
        class="mr-3"
        to="/authentication/login"
      >
        Войти
      </v-btn>

      <v-btn
        color="primary"
        to="/authentication/registration"
      >
        Зарегестрироваться
      </v-btn>
    </v-app-bar>
</template>

<script>
  export default {
    name: 'Header'
  }
</script>
