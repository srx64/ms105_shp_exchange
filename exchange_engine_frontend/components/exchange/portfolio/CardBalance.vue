<template>
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
</template>

<script>
export default {

}
</script>

<style>

</style>
