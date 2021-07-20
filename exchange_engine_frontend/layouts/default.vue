<template>
  <v-app style="background: ;">
    <AppBar />
    <v-main>
      <v-container>
        <v-fade-transition mode="out-in">
          <Nuxt keep-alive :keep-alive-props="{ max: 10 }" />
        </v-fade-transition>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
export default {
  name: 'AppView',
  components: {
    AppBar: () => import('@/components/main/AppBar')
  }
}
</script>

<style>

</style>
