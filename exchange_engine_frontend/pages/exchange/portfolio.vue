<template>
  <v-row class="flex-column-reverse flex-md-row">
    <v-col cols="12" md="8">
      <div v-if="listStockPortfolio.length == 0" style="display: flex;justify-content: center;margin-top:25px;height: 170px;align-items: center;">
        <v-progress-circular indeterminate color="primary" />
      </div>
      <v-list v-else two-line class="transparent">
        <ListGroupStocks :stocks="listStockPortfolio" />
      </v-list>
    </v-col>
    <v-col cols="12" md="4">
      <v-card outlined elevation="0" class="pt-8 pl-4 pr-4 pb-8 mb-8 rounded-xl">
        <v-card-title class="text-h6 ">
          Стоимость портвеля
        </v-card-title>
        <v-card-text class="pt-2 pb-0">
          <v-row class="justify-space-between align-center">
            <v-col cols="auto">
              <h1>{{ $store.getters.GET_PORTFOLIO_SUMM }} ₮</h1>
            </v-col>
            <v-col>
              <p class="text-right text-subtitle-1 ma-0 green--text darken-1" style="white-space: nowrap;">
                <v-icon x-small color="green">
                  mdi-arrow-up
                </v-icon> 1 084,12 ₮ (1,42 %)
              </p>
            </v-col>
          </v-row>
        </v-card-text>
      </v-card>
      <v-card outlined elevation="0" class="pt-6 pl-4 pr-4 pb-6 mb-8 rounded-xl">
        <v-card-title class="text-h6">
          Баланс
        </v-card-title>
        <v-card-text class="pt-2 pb-0">
          <v-row class="justify-space-between align-center">
            <v-col cols="auto">
              <h1>{{ 1515151.156 }}₮</h1>
            </v-col>
            <v-col class="d-flex justify-space-around">
              <div class="d-flex flex-column justify-center align-center">
                <v-btn class="mx-2" fab dark small>
                  <v-icon dark>
                    mdi-plus
                  </v-icon>
                </v-btn>
                <p class="caption mt-1">
                  Пополнить
                </p>
              </div>
              <div class="d-flex flex-column justify-center align-center">
                <v-btn class="mx-2" fab dark small>
                  <v-icon dark>
                    mdi-clipboard-text
                  </v-icon>
                </v-btn>
                <p class="caption mt-1">
                  Заявки
                </p>
              </div>
            </v-col>
          </v-row>
        </v-card-text>
      </v-card>
    </v-col>
  </v-row>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'Portfolio',
  components: {
    ListGroupStocks: () => import('@/components/exchange/portfolio/ListGroupStocks')
  },
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
