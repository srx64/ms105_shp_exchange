<template>
  <v-main>
    <v-container>
      <ListOrders :orders="orders" :activeOrders="activeOrders" :events-only="false" />
    </v-container>
  </v-main>
</template>

<script>
export default {
  components: {
    ListOrders: () => import('@/components/exchange/portfolio/ListOrders.v1.vue')
  },
  layout: 'app',
  data: () => ({
    tab: 1,
    items: [
      'События', 'Активные заявки'
    ],
    text: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.'
  }),
  async fetch () {
    await this.$store.dispatch('FETCH_ORDERS')
  },
  computed: {
    orders () {
      return this.$store.getters.GET_ORDERS
    },
    activeOrders () {
      return this.$store.getters.GET_ORDERS_ACTIVE
    }
  }
}
</script>

<style>
</style>
