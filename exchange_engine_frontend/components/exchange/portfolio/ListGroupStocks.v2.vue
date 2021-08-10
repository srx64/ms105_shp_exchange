<template>
  <div>
    <h1 class="text-h6 mb-6">
      Акции
    </h1>
    <div class="list-stocks-wrapper">
      <div class="list-stocks">
        <div
          v-for="(security) in stocks"
          :key="security.stock.id"
          class="ex-list-stocks-item"
          @click="$router.push({ name: 'exchange-сatalog-stocks-id', params:{id:security.stock.id }})"
        >
          <div class="item--detali">
            <v-list-item-avatar>
              <v-icon class="grey lighten-1" dark />
            </v-list-item-avatar>
            <div>
              <div>{{ security.stock.name }}</div>
              <div>{{ security.count + ' шт.' }}</div>
            </div>
          </div>
          <div class="item--info">
            <div> {{ security.stock.price | numeral('0,0.00') }}₮</div>
            <div>↑ {{ (security.stock.price - security.aver_price) | numeral('0,0.00') }} ₮ ({{ ((security.stock.price - security.aver_price) / security.stock.price * 100)| numeral('0.00') }} %)</div>
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
    cursor: pointer;
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
