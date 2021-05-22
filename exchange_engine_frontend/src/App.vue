<template>
  <v-app >
    <router-view/>
  </v-app>
</template>

<script>
  export default {
    name: 'App',

    metaInfo: {
      title: 'App',
      titleTemplate: '%s | Exchange engine',
      htmlAttrs: {
        lang: 'ru',
      }
    }
  }
</script>