<template>
  <div>
    <v-app-bar
      app
      elevation="1"
      elevate-on-scroll
      height="80"
    >
      <v-img
        :src="require('@/assets/logo.png')"
        class="mr-3"
        contain
        max-width="150"
        width="100%"
      />

      <v-spacer/>

      <div>
        <v-btn
          color="black"
          plain
          class="mx-1"
          to="/auth/login"
        >
          Войти
        </v-btn>

        <v-btn
          color="primary"
          class="mx-1"
          to="/auth/registration"
        >
          Зарегистрироваться
        </v-btn>
      </div>
    </v-app-bar>
  </div>
</template>

<script>
  export default {
    name: 'Header'
  }
</script>
