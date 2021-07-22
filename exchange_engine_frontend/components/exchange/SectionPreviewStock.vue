<template>
  <div style="width:100%;">
    <h1>Акции</h1>
    <div v-if="stocks.length == 0" style="display: flex;justify-content: center;margin-top:25px;height: 170px;align-items: center;">
      <v-progress-circular indeterminate color="primary" />
    </div>
    <v-scale-transition v-else>
      <hooper :items-to-show="4" style="margin-top:25px;height: 170px">
        <slide v-for="(stock) in stocks" :key="stock.id">
          <div class="mr-2 ml-2" style="height: 100%;">
            <PreviewStock :stock="stock" />
          </div>
        </slide>
        <hooper-navigation slot="hooper-addons" />
      </hooper>
    </v-scale-transition>
  </div>
</template>

<script>
import {
  Hooper,
  Slide,
  Navigation as HooperNavigation
} from 'hooper'
import '@/assets/hooper.css'

import {
  mapGetters
} from 'vuex'

export default {
  components: {
    PreviewStock: () => import('@/components/exchange/PreviewStock'),
    Hooper,
    Slide,
    HooperNavigation
  },
  data: () => ({
    stocksInterval: undefined,
    post: []
  }),
  computed: {
    ...mapGetters({
      stocks: 'GET_EXchange_MAIN'
    })
  }
}

</script>

<style>
</style>
