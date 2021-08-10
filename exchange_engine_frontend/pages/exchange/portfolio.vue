<template>
  <v-main>
    <TopBar />
    <section class="pt-5">
      <v-container>
        <v-row class="flex-column-reverse flex-md-row">
          <v-col cols="12" md="8">
            <div
              v-if="listStockPortfolio.length == 0"
              style="display: flex;justify-content: center;margin-top:25px;height: 170px;align-items: center;"
            >
              <v-progress-circular indeterminate color="primary" />
            </div>
            <v-list v-else two-line class="transparent">
              <ListGroupStocks :stocks="listStockPortfolio" />
            </v-list>
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
  computed: {
    ...mapGetters({
      listStockPortfolio: 'GET_PORTFOLIO'
    })
  },
  created () {
    if (!this.$store.state.list_update) {
      this.$store.dispatch('FETCH_PORTFOLIO')
    }
  }
}

</script>

<style>
</style>
