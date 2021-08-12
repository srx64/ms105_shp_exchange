<template>
  <v-main>
    <TopBar />
    <section class="pt-5">
      <v-container>
        <v-row class="flex-column-reverse flex-md-row">
          <v-col cols="12" md="8">
            <ListGroupStocks :stocks="listStockPortfolio" />
          </v-col>
          <v-col cols="12" md="4">
            <div class="text-h6">
              Операции
            </div>
          </v-col>
        </v-row>
      </v-container>
    </section>
  </v-main>
</template>

<script>
import {
  mapGetters
} from 'vuex'

export default {
  name: 'Portfolio',
  components: {
    TopBar: () => import('@/components/exchange/portfolio/TopBar.vue'),
    ListGroupStocks: () => import('@/components/exchange/portfolio/ListGroupStocks.v2.vue')
  },
  layout: 'app',
  async fetch () {
    await this.$store.dispatch('FETCH_PORTFOLIO')
  },
  computed: {
    ...mapGetters({
      listStockPortfolio: 'GET_PORTFOLIO'
    })
  },
  activated () {
    if (this.$fetchState.timestamp <= Date.now() - 60000) {
      this.$fetch()
    }
  }
}

</script>

<style>
</style>
