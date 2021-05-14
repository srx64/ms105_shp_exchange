<template>
  <v-container>
    <h1>
      Портфель
    </h1>
    <v-list
      v-if="portfolio.length"
      two-line
      color="white"
    >
      <v-subheader 
        class="mr-8"
        inset
      >
        <span>
          Акции
        </span>
        <v-spacer/>
        <span>
          {{ sumSecurities(portfolio) }}
        </span>
      </v-subheader>

      <v-list-item
        v-for="security in portfolio"
        :key="security.title"
      >
        <v-list-item-avatar
          color="grey lighten-3 text-center caption"
        >
          <v-img
            v-if="security.icon"
            :src="security.icon"
          />

          <span 
            v-else
            class="text-center mx-auto"
          >
            {{ security.name }}
          </span>
        </v-list-item-avatar>

        <v-list-item-content>
          <v-list-item-title v-text="security.name"/>

          <v-list-item-subtitle v-text="security.description"/>
        </v-list-item-content>

        <v-list-item-action>
          <v-list-item-action
            class="font-weight-medium"
          >
            {{ security.price.toFixed(2) }}
          </v-list-item-action>
        </v-list-item-action>
      </v-list-item>
    </v-list>
    <h3
      v-else
    >
      Ваш портфель пока пуст
    </h3>
  </v-container>
</template>

<script>
import { getAPI } from '@/axios-api'

export default {
  name: 'Portfolio',

  computed: {
    portfolio() {
      return this.$store.getters.portfolio
    },
  },

  methods: {
      getPortfolio () {
        getAPI.get('api/v1/portfolio/', {
            headers: { 
              Authorization: `Bearer ${this.$store.state.accessToken}` 
            } 
          })
          .then(response => {
            console.log(response.data)
          })
          .catch(err => {
            console.log(err)
          })
      },
      sumSecurities(securities) {
        let sum = 0

        for (let key in securities) {
          sum += securities[key].price
        }

        return sum.toFixed(2)
      }
    },

    mounted () {
      this.getPortfolio()
    }
  }
</script>
<style scoped>
</style>