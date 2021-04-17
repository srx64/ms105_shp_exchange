<template>
  <v-container>
    <h1> Портфель </h1>
      <v-data-table v-if="rows"
    dense
    :headers="headers"
    :items="rows"
    class="elevation-1"
    ></v-data-table>
  </v-container>
</template>

<script>
// @ is an alias to /src
  import { getAPI } from '../../../axios-api'
  import { mapState } from 'vuex'

export default {
  name: 'Portfolio',
  data() {
    return {
      rows: false,
      headers:[ { text: 'Акция', value: 'stock' },
          { text: 'Количество', value: 'count' },
          { text: 'Percentage', value: 'percentage' },]
    };
  },

  computed: mapState(['APIData']),

  methods: {
      getPortfolio () {
        getAPI.get('api/v1/portfolio/', {
            headers: { 
              Authorization: `Bearer ${this.$store.state.accessToken}` 
            } 
          })
          .then(response => {
            this.rows = response.data;
            console.log(response.data)
          })
          .catch(err => {
            console.log(err)
          })
      },
    },

    mounted () {
      this.getPortfolio()
    }
  }
</script>
<style scoped>
</style>