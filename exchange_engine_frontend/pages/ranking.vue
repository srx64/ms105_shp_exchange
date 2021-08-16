<template>
  <v-main>
    <v-container>
      <h1>Рейтинг</h1>
      {{ ratingList }}
      <div>
        <div v-for="n in 20" v-bind:key="n" style="padding: 10px;margin-bottom: 15px;background: white;border-radius: 10px">
          <v-row>
            <v-col :cols="'auto'">
              <v-avatar color="primary" size="40"></v-avatar>
            </v-col>
            <v-col>
              NAME
            </v-col>
            <v-col class="d-flex align-center text-center" :cols="2">
              {{n}}
            </v-col>
          </v-row>
        </div>
      </div>
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
