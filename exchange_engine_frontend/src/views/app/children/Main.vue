<template>
  <v-row
    no-gutters
    class="grey lighten-5 align-stretch"
  >
    <v-col>
      <v-list 
        two-line
        subheader
      >
        <v-list-item-group
          v-model="selectedItem"
          color="primary"
        >
          <template
            v-for="(stock, index) in stocks"
          >
          <v-list-item
            :key="stock.id"
          >
            <v-list-item-avatar
              size="25px"
              class="justify-center"
              color="primary"
            >
              <span
                class="white--text"
              >
                {{ stock.name[0] + stock.name[1] }}
              </span>
            </v-list-item-avatar>
  
            <v-list-item-content>
              <v-list-item-title v-text="stock.name">
              </v-list-item-title>
              <v-list-item-subtitle v-text="stock.description">
              </v-list-item-subtitle>
            </v-list-item-content>

            <v-list-item-action>
              <v-icon 
                v-if="stock.is_active"
                color="green"
              >
                mdi-circle
              </v-icon>
              <v-icon
                v-else
                color="red"
              >
                mdi-circle
              </v-icon>
            </v-list-item-action>
          </v-list-item>

          <v-divider
            v-if="index < stocks.length - 1"
            :key="'divider-' + index"
          ></v-divider>
          </template>
        </v-list-item-group>
      </v-list>
    </v-col>
    
    <v-divider  vertical/>

    <v-col>
      <v-card
        v-if="selectedItem != undefined" 
        class="pa-6"
        elevation="0"
        tile
      >
        <v-card-title> {{stocks[selectedItem].name}} </v-card-title>
        <v-card-text>Описание: {{stocks[selectedItem].description}}</v-card-text>
        <v-form>
          <v-text-field v-model="amount" hint="" label="Количество" type="number"></v-text-field>
          <v-checkbox
          v-model="limit_order"
          hide-details
          label="Отложенная заявка"
          class="shrink mr-2 mt-0"
        ></v-checkbox>
          <v-text-field v-if="limit_order" :disabled="!limit_order" v-model="price" hint="" label="Цена" type="number"></v-text-field>
          <v-checkbox
          hide-details
          label="Торговля с плечом"
          class="shrink mr-2 mt-0"
          :disabled="limit_order"
          v-model="leverage_trade"
        ></v-checkbox>
        <v-text-field v-model="ratio" v-if="leverage_trade" hint="" label="Размер плеча" type="number"></v-text-field>
          <v-card-actions>
            <v-btn color="success" @click="trade(0)"> Купить </v-btn> 
            <v-btn color="error" @click="trade(1)"> Продать </v-btn>
          </v-card-actions>
        </v-form>
      </v-card>
      
      <v-container
        v-else
      >
        <BaseTitle
          align="center"
          weight="regular"
        >
          Ни одной акции не выбрано
        </BaseTitle>

        <BaseBody
          class="text-center"
        >
          Пожалуйста, выберите любую акцию из списка справа для просмотра ее информации
        </BaseBody>
      </v-container>
    </v-col>
  </v-row>
</template>

<script>
  import { getAPI } from '@/axios-api'

  export default {
    name: 'App',

    data: () => ({
      selectedItem: undefined,
      limit_order: false,
      leverage_trade: false,
      price: 0,
      amount: 0,
      stocks: [],
      ratio: 0,
    }),

    methods: {
      getStocks(){
        getAPI.get('api/v1/stocks/', {
            headers: { 
              Authorization: `Bearer ${this.$store.state.accessToken}` 
            } 
          })
          .then(response => {
            this.stocks = response.data
          })
          .catch(err => {
            console.log(err)
          })
      },
      trade(type){
        var url_trade = this.leverage_trade && !this.leverage_trade ? 'trading/leverage/' : 'orders/add'
        getAPI.post(url_trade, {
          stock: this.stocks[this.selectedItem].name.toString(),
          type: type,
          price: this.limit_order ? this.price : 0,
          amount: this.amount,
          ratio: this.ratio,
        },
        {
          headers: { 
            Authorization: `Bearer ${this.$store.state.accessToken}` 
          } 
        })
        .then(response => {
          console.log(response)
          this.$store.commit({
              type: 'showSnackbar',
              text: 'Вы создали заявку'
            })
        })
        .catch(err => {
          console.log(err)
          this.$store.commit({
              type: 'showSnackbar',
              text: 'Введите корректные данные для торговли'
            })
        })
      }
    },
    computed: {
      generateAlert: function(){
        var str = 'Вы хотите создать '
        str += this.limit_order ? 'отложенную заявку по цене ' + this.price : 'заявку по текущей цене '
        str += this.leverage_trade ? 'с плечом  ' : ''
        //str += получить количество акций, если 0 то к строке прибавить <в шорт> иначе <в лонг>
        // сделать dialog component https://vuetifyjs.com/en/components/dialogs/#transitions
        return str
      }
    },
    created () {
      this.getStocks()
    }
  }
</script>