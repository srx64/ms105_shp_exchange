<template>
  <v-app>
    <AppBar />
    <v-fade-transition mode="out-in">
      <Nuxt keep-alive :keep-alive-props="{ max: 10 }" />
    </v-fade-transition>
  </v-app>
</template>

<script>
export default {
  name: 'AppView',
  components: {
    AppBar: () => import('@/components/main/AppHeader.vue')
  },
  middleware: ['auth']
}

</script>

<style scoped>
  @import url('https://fonts.googleapis.com/css2?family=Quantico&display=swap');
  @import url('https://fonts.googleapis.com/css2?family=Roboto&display=swap');

  html,
  body {
    height: 100%;
    margin: 0;
  }

  #app {
    position: relative;
    display: flex;
    flex-direction: column;
    height: 100%;
    background: #F2F8FF;
  }

</style>
