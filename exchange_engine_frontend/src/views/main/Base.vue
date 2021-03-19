<template>
  <div>
    <Header v-if="false"/>
    <HomeAppBar/>
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
  import HomeAppBar from '@/components/main/AppBar.vue'

  export default {
    name: 'Main',

    components: {
      Header, Footer, HomeAppBar
    }
  }
</script>
