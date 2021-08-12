<template>
  <v-app style="background: ;">
    <v-fade-transition mode="out-in">
      <Nuxt keep-alive :keep-alive-props="{ max: 10 }" />
    </v-fade-transition>
  </v-app>
</template>

<script>
export default {
}
</script>

<style>

</style>
