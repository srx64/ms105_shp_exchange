<template>
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
</template>

<script>
export default {

}
</script>

<style>

</style>
