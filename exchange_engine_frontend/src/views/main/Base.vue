<template>
  <v-container>
    <Header/>
    <v-main>
      <h1> 
        Main
      </h1>
    </v-main>
  </v-container>
</template>

<script>
  import Header from '@/components/main/Header.vue'

  export default {
    name: 'Main',
    components: {
      Header
    }
  }
</script>
