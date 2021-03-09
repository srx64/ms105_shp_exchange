<template>
  <v-container>
    <ul>
      <router-link to="/">Main</router-link> |
      <router-link to="/authentication/login">Login</router-link> |
      <router-link to="/authentication/registration">Registration</router-link>
    </ul>
    <h1 class="display-2 font-weight-bold mb-3">
      Authentication
    </h1>
    <v-main>
      <router-view></router-view>
    </v-main>
  </v-container>
</template>

<script>
  export default {
    name: 'Authentication',
    components: {
      
    }
  }
</script>