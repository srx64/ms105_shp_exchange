<template>
  <v-row>
    <v-col cols="12">
      <Search />
    </v-col>
    <v-col cols="12">
      <SectionPreviewStock />
    </v-col>
  </v-row>
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
  created () {
    if (!this.$store.state.list_update) {
      this.$store.dispatch('FETCH_LIST_STOCKS')
    }
  }
}

</script>
