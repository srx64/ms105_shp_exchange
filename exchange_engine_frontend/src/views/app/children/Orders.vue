<template>
  <v-container>
    <h1>
      Заявки
    </h1>
    <v-list
      v-if="orders.length"
      two-line
      color="white"
    >
      <v-subheader 
        class="mr-8"
        inset
      >
        <span>
          Покупка
        </span>
      </v-subheader>

      <v-list-item
        v-for="order in purchaseOrders"
        :key="order.id"
      >
        <v-list-item-avatar
          color="grey lighten-3 text-center caption"
        >
          <v-img
            v-if="order.icon"
            :src="order.icon"
          />

          <span 
            v-else
            class="text-center mx-auto"
          >
            {{ order.stock }}
          </span>
        </v-list-item-avatar>

        <v-list-item-content>
          <v-list-item-title 
            v-if="order.type"
          >
            Статус заявки на продажу {{ order.stock }}
          </v-list-item-title>
          <v-list-item-title 
            v-else
          >
            Статус заявки на покупку {{ order.stock }}
          </v-list-item-title>

          <v-list-item-subtitle
            v-if="order.is_closed"
            class="green--text"
          >
            Выполнена
          </v-list-item-subtitle>
          <v-list-item-subtitle
            v-else
            class="grey--text"
          >
            Открыта
          </v-list-item-subtitle>
        </v-list-item-content>

        <v-list-item-action>
          <v-list-item-title
            class="font-weight-medium"
          >
            {{ order.amount }} X {{ order.price.toFixed(2) }}
          </v-list-item-title>
          <v-list-item-subtitle
            
          >
            {{ (order.amount * order.price).toFixed(2) }}
          </v-list-item-subtitle>
        </v-list-item-action>
      </v-list-item>
      <h5
        v-if="!purchaseOrders.length"
        class="ml-15"
      >
        У вас пока нет заявок на продажу
      </h5>

      <v-divider/>

      <v-subheader 

        class="mr-8"
        inset
      >
        <span>
          Продажа
        </span>
      </v-subheader>

      <v-list-item
        v-for="order in saleOrders"
        :key="order.id"
      >
        <v-list-item-avatar
          color="grey lighten-3 text-center caption"
        >
          <v-img
            v-if="order.icon"
            :src="order.icon"
          />

          <span 
            v-else
            class="text-center mx-auto"
          >
            {{ order.stock }}
          </span>
        </v-list-item-avatar>

        <v-list-item-content>
          <v-list-item-title 
            v-if="order.type"
          >
            Статус заявки на продажу {{ order.stock }}
          </v-list-item-title>
          <v-list-item-title 
            v-else
          >
            Статус заявки на покупку {{ order.stock }}
          </v-list-item-title>

          <v-list-item-subtitle
            v-if="order.is_closed"
            class="green--text"
          >
            Выполнена
          </v-list-item-subtitle>
          <v-list-item-subtitle
            v-else
            class="grey--text"
          >
            Открыта
          </v-list-item-subtitle>
        </v-list-item-content>

        <v-list-item-action>
          <v-list-item-title
            class="font-weight-medium"
          >
            {{ order.amount }} X {{ order.price.toFixed(2) }}
          </v-list-item-title>
          <v-list-item-subtitle
            
          >
            {{ (order.amount * order.price).toFixed(2) }}
          </v-list-item-subtitle>
        </v-list-item-action>
      </v-list-item>
      <h5
        v-if="!saleOrders.length"
        class="ml-15"
      >
        У вас пока нет заявок на продажу
      </h5>
    </v-list>
  </v-container>
</template>

<script>
import { getAPI } from '@/axios-api'

export default {
  name: 'Orders',

  data: () => ({
    orders: {},
    ordersInterval: undefined
  }),

  methods: {
      getOrders () {
        getAPI.get('api/v1/orders/', {
            headers: { 
              Authorization: `Bearer ${this.$store.state.accessToken}` 
            } 
          })
          .then(response => {
            this.orders = response.data
          })
          .catch(err => {
            console.log(err)
            clearInterval(this.ordersInterval)
          })
      },
      orderClosed (order) {
        if (order.is_closed)
          return true
        return false
      }
    },

    computed: {
      purchaseOrders () {
        return this.orders.filter(function (el) {
          return el.type == false
        })
      },
      saleOrders () {
        return this.orders.filter(function (el) {
          return el.type == true
        })
      },
    },

    mounted () {
      this.getOrders()
      this.ordersInterval = setInterval(function() {
        this.getOrders()
      }.bind(this), 1000)
    },

    destroyed () {
      clearInterval(this.ordersInterval)
    }
  }
</script>