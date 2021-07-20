<template>
  <v-container
    class="px-10"
  >
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
        <!-- <span>
          {{ sumSecurities(portfolio) }}
        </span> -->
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
            {{ security.stock.name }}
          </span>
        </v-list-item-avatar>

        <div
          v-if="profile.is_superuser"
          class="mr-5"
        >
          <v-list-item-subtitle>
            Владелец
          </v-list-item-subtitle>
          <v-list-item-title
            class="d-inline"
          >
            {{ security.user }}
          </v-list-item-title>
        </div>

        <v-list-item-content>
          <v-list-item-title v-text="security.stock.name"/>
          <v-list-item-subtitle v-if="security.count < 0">
            (Торговля на понижение)
          </v-list-item-subtitle>
        </v-list-item-content>
        <v-list-item-action
          v-if="security.count < 0"
        >
          <v-list-item-title
            class="font-weight-medium mb-n2"
          >
            {{ security.count }} x {{ (-security.count * security.stock.price).toFixed(2) }}&#x20AE;
          </v-list-item-title>
          <v-list-item-title
            :class="(security.stock.price - security.aver_price < 0) ? 'green--text': (security.stock.price - security.aver_price > 0) ? 'red--text' : 'grey--text'"
          >
            {{ (security.count * (security.stock.price - security.aver_price)).toFixed(2) }}&#x20AE;
            <span class="grey--text"> | </span>
            {{ ((security.stock.price - security.aver_price) / security.stock.price * -100).toFixed(2) }}%
          </v-list-item-title>
        </v-list-item-action>
        <v-list-item-action
          v-else
        >
          <v-list-item-title
            class="font-weight-medium mb-n2"
          >
            {{ security.count }} x {{ security.stock.price.toFixed(2) }}&#x20AE;
          </v-list-item-title>
          <v-list-item-title
            :class="(security.stock.price - security.aver_price < 0) ? 'red--text': (security.stock.price - security.aver_price > 0) ? 'green--text' : 'grey--text'"
          >
            {{ (security.count * (security.stock.price - security.aver_price)).toFixed(2) }}&#x20AE;
            <span class="grey--text"> | </span>
            {{ ((security.stock.price - security.aver_price) / security.stock.price * 100).toFixed(2) }}%
          </v-list-item-title>
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
export default {
  name: 'Portfolio',

  data: () => ({
    portfolioInterval: undefined
  }),

  computed: {
    portfolio() {
      return this.$store.getters.portfolio
    },
    profile() {
      return this.$store.getters.profile
    }
  },

  methods: {
    sumSecurities(securities) {
      let sum = 0

      for (let key in securities) {
        sum += securities[key].price
      }

      return sum.toFixed(2)
    }
  },
}
</script>
<style scoped>
</style>
