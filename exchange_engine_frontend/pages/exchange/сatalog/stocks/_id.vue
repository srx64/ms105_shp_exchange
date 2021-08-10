<template>
  <v-main>
    <v-container>
      <v-row>
        <v-col cols="12">
          <span @click="$router.push({ name: 'exchange-сatalog-stocks'})">
            <v-icon>mdi-arrow-left</v-icon> Акции
          </span>
        </v-col>
        <v-col cols="12">
          <h1 class="text-h4 text-xl-h3 text-truncate">
            {{ stock.name }}
          </h1>
          <div class="d-flex flex-column text-right">
            <p class="text-body-1 ma-0 text-no-wrap">
              {{ stock.price | numeral('0,0.00') }}₮
            </p>
            <!--<p class="text-body-1 ma-0 green--text darken-1 text-no-wrap">
                    <v-icon x-small color="green">mdi-arrow-up</v-icon> 1 084,12 ₮ (1,42 %)
                </p>-->
          </div>
        </v-col>
        <v-col cols="8">
          <chart />
        </v-col>
        <v-col cols="4">
          <h1 v-if="stocks_portfolio!=undefined">
            В портфеле
          </h1>
          <v-row class="align-center justify-end">
            <v-col v-if="stocks_portfolio!=undefined" cols="12">
              <v-card outlined elevation="0" class="pa-2 mt-8 mb-8">
                <v-card-text class="pb-0">
                  <v-row class="flex-sm-row">
                    <v-col class="text-center">
                      <p class="text-h5">
                        {{ stocks_portfolio.count }} {{ stocks_portfolio.count == 1 ? 'акция' : 'акций' }}
                      </p>
                      <p class="text-subtitle-1 text-no-wrap">
                        {{ stocks_portfolio.stock.price | numeral('0,0.00') }}₮ → {{ stocks_portfolio.aver_price | numeral('0,0.00') }}₮
                      </p>
                    </v-col>
                  </v-row>
                </v-card-text>
              </v-card>
            </v-col>
            <v-col v-if="stocks_portfolio!=undefined" cols="12">
              <sellStock :stocks_portfolio="stocks_portfolio" />
            </v-col>
            <v-col :cols="[stocks_portfolio!=undefined ? 12 : 12]" sm="12">
              <buyStock :stock="stock" />
            </v-col>
          </v-row>
        </v-col>
      </v-row>
    </v-container>
  </v-main>
</template>

<script>
export default {
  components: {
    sellStock: () => import('@/components/exchange/stocks/sell.vue'),
    buyStock: () => import('@/components/exchange/stocks/buy.vue'),
    chart: () => import('@/components/exchange/stocks/chart.vue')
  },
  layout: 'app',
  data: () => ({
    selectedCandlesType: 0,
    stock: {
      name: 'JSi',
      price: 121212.121212
    },
    candlesInterval: undefined,
    model: '',
    dialog2: false,
    text: '',
    stocks_portfolio: {
      aver_price: 12345.21333,
      count: 120,
      stock: {
        name: 'JSi',
        price: 123123.12444
      }
    }
  }),
  computed: {
  }
}

</script>

<style>

</style>
