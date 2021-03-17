<template>
  <div>
    <ul>
      <router-link to="/">Main</router-link>
    </ul>
    <h1 class="display-2 font-weight-bold mb-3">
      App
    </h1>
    <v-main>
      <router-view></router-view>
    </v-main>
  </div>
</template>

<script>
  export default {
    name: 'App',
    components: {
      
    }
  }
</script>