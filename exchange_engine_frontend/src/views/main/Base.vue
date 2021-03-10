<template>
  <v-container>
    <ul>
      <router-link to="/authentication">Authentication</router-link> |
      <router-link to="/app">App</router-link>
    </ul>
    <h1 class="display-2 font-weight-bold mb-3">
      Main
    </h1>
    <v-main>
      <HelloWorld/>
    </v-main>
  </v-container>
</template>

<script>
  import HelloWorld from '@/components/main/HelloWorld.vue'

  export default {
    name: 'Main',
    components: {
      HelloWorld
    }
  }
</script>
