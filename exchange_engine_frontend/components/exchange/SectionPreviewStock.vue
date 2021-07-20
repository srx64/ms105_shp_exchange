<template>
  <div style="width:100%;">
    <h1>Акции</h1>
    <div v-if="$fetchState.pending" style="display: flex;justify-content: center;">
      <v-progress-circular indeterminate color="primary" />
    </div>
    <p v-else-if="$fetchState.error" style="display: flex;justify-content: center;">
      An error occurred :(
    </p>
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

import { listStoks } from '@/store/data'

export default {
  components: {
    PreviewStock: () => import('@/components/exchange/PreviewStock'),
    Hooper,
    Slide,
    HooperNavigation
  },
  data: () => ({
    stocks: [],
    stocksInterval: undefined,
    post: []
  }),
  async fetch () {
    this.post = await fetch('https://api.nuxtjs.dev/posts').then(res =>
      res.json()
    )
    this.stocks = listStoks
  },
  activated () {
    // https://nuxtjs.org/docs/2.x/features/data-fetching
    // Call fetch again if last fetch more than 30 sec ago
    if (this.$fetchState.timestamp <= Date.now() - 30000) {
      this.$fetch()
      console.log(1)
    }
  }
}
</script>

<style>
</style>
