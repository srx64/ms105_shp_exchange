<template>
  <v-card
    class="mx-auto my-12"
    max-width="400"
  > 

    <v-card-title>Cafe Badilico</v-card-title>

    <v-card-text>
      


      <div>Small plates, salads & sandwiches - an intimate setting with 12 indoor seats plus patio seating.</div>
    </v-card-text>

    <v-divider class="mx-4"></v-divider>

    <v-card-text
      class="d-flex flex-wrap justify-space-between px-0"
    >
      <v-btn
        color="primary"
        class="mx-auto my-1"
        outlined
        to="/auth/reg"
      >
        Создать аккаунт
      </v-btn>

      <v-btn
        color="primary"
        class="mx-auto my-1"
        outlined
        to="/auth/reg"
      >
        Войти
      </v-btn>
    </v-card-text>
  </v-card> 
</template>

<script>
  export default {
    name: 'TestForm',
  }
</script>