<template>
  <div>
    <Header/>
    <v-main>
      <v-container
        fluid
        class="blue"
      >
        <div
          class="d-inline deep-purple ma-0 pa-10"
        >
          Hello, i'm block)
        </div>
      </v-container>
    </v-main>
    <Footer/>
  </div>
</template>

<script>
  import Header from '@/components/main/Header.vue'
  import Footer from '@/components/main/Footer.vue'

  export default {
    name: 'Main',
    components: {
      Header, Footer
    }
  }
</script>
