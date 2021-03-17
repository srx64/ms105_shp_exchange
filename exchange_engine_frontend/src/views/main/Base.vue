<template>
  <div>
    <Header/>
    <v-main>
      <v-container
        color="primary"
        class="pa-0"
      >
        <v-img 
          src="https://wonder-day.com/wp-content/uploads/2020/10/wonder-day-among-us-png-28.png"
          width="200"
        />
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
