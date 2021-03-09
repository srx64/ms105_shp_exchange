<template>
  <v-app>
    <v-main>
      <Register/>
    </v-main>
  </v-app>
</template>

<script>
import Register from './components/Register';

export default {
  name: 'App',

  components: {
    Register,
  },

  data() {
    return {
      
    }
  }
};
</script>
