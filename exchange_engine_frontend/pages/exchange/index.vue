<template>
  <v-main>
    <v-container>
      <v-row>
        <v-col cols="12">
          <Search />
        </v-col>
        <v-col cols="12">
          <SectionPreviewStock />
        </v-col>
      </v-row>
    </v-container>
  </v-main>
</template>

<script>
export default {
  name: 'Exchange',
  components: {
    Search: () => import('@/components/exchange/Search'),
    SectionPreviewStock: () => import('@/components/exchange/SectionPreviewStock')
  },
  layout: 'app',
  data: () => ({
  }),
  // https://nuxtjs.org/docs/2.x/features/data-fetching#using-activated-hook
  async fetch () {
    await this.$store.dispatch('FETCH_LIST_STOCKS')
  },
  activated () {
    if (this.$fetchState.timestamp <= Date.now() - 60000) {
      this.$fetch()
    }
  }
}

</script>
