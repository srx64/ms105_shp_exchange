<template>
  <router-view/>
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