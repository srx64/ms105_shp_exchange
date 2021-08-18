<template>
  <div>
    <div v-if="!eventsOnly" class="d-flex mb-5">
      <button class="ex-button" :class="active == 1 ? 'active': ''" @click="active = 1">
        Действия
      </button>
      <button class="ex-button" :class="active == 2 ? 'active': ''" @click="active = 2">
        Активные заявки
      </button>
    </div>
    <div v-if="active === 1" class="d-flex flex-column">
      <div v-for="itme in orders" :key="itme.date" class="">
        <h4>{{ itme.date }}</h4>
        <div>
          <div v-for="ord in itme.orders" :key="ord.id" class="ex-order" :class="eventsOnly ? '': 'detail'" @click="select(ord)" >
            <v-row>
              <v-col cols="auto">
                <v-list-item-avatar>
                  <v-icon class="grey lighten-1" dark />
                </v-list-item-avatar>
              </v-col>
              <v-col class="d-flex align-center">
                <div v-if="ord.type">
                  Продажа {{ ord.count }} {{ ord.count == 1 ? 'акции':'акций' }} {{ ord.stock.description }}
                </div>
                <div v-else>
                  Покупка {{ ord.count }} {{ ord.count == 1 ? 'акции':'акций' }} {{ ord.stock.description }}
                </div>
              </v-col>
              <v-col class="d-flex align-center" cols="auto">
                <div v-if="ord.type" class="green--text accent-3">
                  + {{ ord.price*ord.count | numeral('0,0.00') }}₮
                </div>
                <div v-else class="red--text accent-3">
                  - {{ ord.price*ord.count | numeral('0,0.00') }}₮
                </div>
              </v-col>
            </v-row>
          </div>
        </div>
      </div>
    </div>
    <div v-if="!eventsOnly && active === 2" />
  </div>
</template>

<script>
export default {
  name: 'ListOrders',
  props: {
    orders: {
      type: Array,
      required: true
    },
    activeOrders: {
      type: Array,
      required: false,
      default: null
    },
    eventsOnly: {
      type: Boolean,
      default: true
    }
  },
  data: () => ({
    active: 1,
    selectOrders: {}
  }),
  methods: {
    select (data) {
      if (!this.eventsOnly) {
        this.selectOrders = data
      }
    }
  }
}

</script>

<style>
.ex-button{
  background: white;
  padding: 6px 15px 6px 15px;
  border-radius: 40px;
  margin-right: 15px;
  box-shadow: 0px 0px 12px 0px rgba(50, 50, 50, 0.3);
  transition: all 0.35s;
}
.ex-button.active{
  background: black;
  color: white;
  box-shadow: none;
}
.ex-order {
  background: white;
  margin-bottom: 15px;
  border-radius: 15px;
  padding: 8px 15px 8px 15px;
}
.ex-order.detail {
  cursor: pointer;
}
</style>
