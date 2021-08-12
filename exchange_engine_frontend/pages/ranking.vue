<template>
  <v-main>
    <v-container>
      <h1>Рейтинг</h1>
      {{ ratingList }}
    </v-container>
  </v-main>
</template>

<script>
export default {
  layout: 'app',
  async fetch () {
    await this.$store.dispatch('FETCH_RATING')
  },
  computed: {
    ratingList () {
      return this.$store.state.rating
    }
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
