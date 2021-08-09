<template>
  <div>
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
            </v-icon> {{ (security.stock.price - security.aver_price).toFixed(2) }}₮
            ({{ ((security.stock.price - security.aver_price) / security.stock.price * 100).toFixed(2) }}%)
          </p>
        </v-list-item-action>
      </v-list-item>
      <v-divider />
    </v-list-item-group>
    <h1 class="text-h4 mb-6">
      Акции
    </h1>
    <div class="list-stocks-wrapper">
      <div class="list-stocks">
        <div class="ex-list-stocks-item">
          <div class="item--detali">
            <v-list-item-avatar>
              <v-icon class="grey lighten-1" dark />
            </v-list-item-avatar>
            <div>
              <div>Ozon</div>
              <div>1 шт.</div>
            </div>
          </div>
          <div class="item--info">
            <div> 400 810,63₮</div>
            <div>↑ 1 084,12 ₮ (1,42 %)</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ListGroupStocks',
  props: ['stocks']
}

</script>

<style>
  .ex-list-stocks-wrapper,
  .ex-list-stocks {
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    padding: 0px;
  }

  .ex-list-stocks-item {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    padding: 10px 20px;
    background-color: white;
    border-radius: 8px;
    margin-bottom: 8px;
  }

  .ex-list-stocks-item .item--detali {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    padding: 0px;
  }

  .ex-list-stocks-item .item--info {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: flex-end;
    padding: 0px;
  }

</style>
