<template>
  <div style="position: fixed;">
    
    <v-card
      class="d-flex align-center mb-6"
      color="grey lighten-2"
      flat
      height=""
      tile
    >   
      <v-card
        v-for="n in 3"
        :key="n"
        class="pa-2"
        outlined
        tile
      >
        align-center
        <v-img 
          contain
          width="200"
          src="https://citydog.by/content/_posts/560X459/5dbdf7e95316d.jpg"
        />
      </v-card>
    </v-card>
  </div>
</template>

<script>
  export default {
    name: 'Authentication',
    components: {
      
    }
  }
</script>