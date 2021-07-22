<template>
  <v-list-item-group color="">
    <v-subheader inset class="text-h6">
      Акции
    </v-subheader>
    <v-list-item
      v-for="(security) in stocks"
      :key="security.stock.id"
      @click="$router.push({ name: 'exchange-сatalog-stocks-id', params:{id:security.stock.id }})"
    >
      <v-list-item-avatar>
        <v-icon class="grey lighten-1" dark />
      </v-list-item-avatar>

      <v-list-item-content>
        <v-list-item-title v-text="security.stock.name" />

        <v-list-item-subtitle v-text="security.count + ' шт.'" />
      </v-list-item-content>

      <v-list-item-action>
        <p class="text-overline ma-0">
          {{ security.stock.price.toFixed(2) }}₮
        </p>
        <p class="text-caption ma-0 green--text darken-1">
          <v-icon x-small color="green">
            mdi-arrow-up
          </v-icon> {{ (security.stock.price - security.aver_price).toFixed(2) }}₮ ({{ ((security.stock.price - security.aver_price) / security.stock.price * 100).toFixed(2) }}%)
        </p>
      </v-list-item-action>
    </v-list-item>
    <v-divider />
  </v-list-item-group>
</template>

<script>
export default {
  name: 'ListGroupStocks',
  props: ['stocks']
}
</script>

<style>

</style>
