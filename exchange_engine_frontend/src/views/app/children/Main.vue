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
          color="primary"
        >
          <div
            v-for="(stock, index) in stocks"
            :key="stock.id"
            @click="selectStock(stock.id)"
          >
            <v-list-item>
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
                <v-list-item-title>
                {{ stock.price.toFixed(2) }}&#x20AE;
                </v-list-item-title>
              </v-list-item-action>
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
          </div>
        </v-list-item-group>
      </v-list>
    </v-col>
    
    <v-divider  vertical/>

    <v-col>
      <v-card
        v-if="selectedStonkID != undefined" 
        class="pa-6"
        elevation="0"
        tile
      >
        <v-card-title v-text="selectedStock.name"/>
        <v-card-subtitle>
          Текущая цена: {{ selectedStock.price.toFixed(2) }}&#x20AE;
        </v-card-subtitle>
        <v-card-text>{{ selectedStock.description }}</v-card-text>
        <v-container
          hidden
        >
          <trading-vue
            hidden
            :data="this.$data"
            title-txt="NAME"
            :toolbar="true"
          />
        </v-container>
        <v-form>
          <v-text-field v-model="amount" hint="" label="Количество" type="number" ></v-text-field>
          <v-checkbox
          v-model="limit_order"
          hide-details
          label="Отложенная заявка"
          class="shrink mr-2 mt-0"
        ></v-checkbox>
          <v-text-field v-if="limit_order" append-icon="mdi-currency-mnt" :disabled="!limit_order" v-model="price" hint="" label="Цена" type="number"></v-text-field>
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
import TradingVue from "trading-vue-js";
  export default {
    name: 'App',
    components: { TradingVue },
    data: () => ({
      selectedStonkID: undefined,
      limit_order: false,
      leverage_trade: false,
      price: 0,
      amount: 1,
      stocks: [],
      ratio: 0,
      candles: [],
      ohlcv: [ [ 1620822279181, 2820, 3188.5, 3188.5, 2820 ], [ 1620822333716, 3090, 3085, 3090, 3085 ], [ 1620822395534, 3037.5, 3033, 3037.5, 3033 ]],
      item: '',
      stocksInterval: undefined
    }),
    // watch: {
    //   'selectedStonkID': function(val){
    //     if(val != undefined){
    //       this.getCandles()
    //     }
    //   }
    // },
    methods: {
      getStocks(){
        getAPI.get('api/v1/stocks/', {
            headers: { 
              Authorization: `Bearer ${this.$store.getters.accessToken}` 
            } 
          })
          .then(response => {
            this.stocks = response.data
          })
          .catch(err => {
            console.log(err)
            clearInterval(this.stocksInterval)
          })
      },
      getCandles(){
        if (this.selectedStonkID){
          getAPI.get('api/v1/candles/' + this.selectedStock.id + '/', )
          .then(response => {
            this.candles = response.data
            this.ohclv = []
            for(var i of this.candles)
              this.ohclv.push([new Date(i.date).valueOf(), i.open, i.close, i.high, i.low]);
            this.item = '<trading-vue :data="this.$data"></trading-vue>'
          })
          .catch(err => {
            console.log(err)
          })
        }
      },
      trade(type){
        var url_trade = this.leverage_trade && !this.leverage_trade ? 'trading/leverage/' : 'orders/add'
        getAPI.post(url_trade, {
          stock: this.selectedStock.name.toString(),
          type: type,
          price: this.limit_order ? this.price : 0,
          amount: this.amount,
          ratio: this.ratio,
        },
        {
          headers: { 
            Authorization: `Bearer ${this.$store.getters.accessToken}` 
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
      },
      selectStock (id) {
        this.selectedStonkID = id
      }
    },
    computed: {
      generateAlert () {
        var str = 'Вы хотите создать '
        str += this.limit_order ? 'отложенную заявку по цене ' + this.price : 'заявку по текущей цене '
        str += this.leverage_trade ? 'с плечом  ' : ''
        //str += получить количество акций, если 0 то к строке прибавить <в шорт> иначе <в лонг>
        // сделать dialog component https://vuetifyjs.com/en/components/dialogs/#transitions
        return str
      },
      selectedStock () {
        return this.stocks.find(obj => {
          return obj.id === this.selectedStonkID
        })
      }
    },
    mounted () {
      this.getStocks()
      this.stocksInterval = setInterval(function() {
        this.getStocks()
      }.bind(this), 10000)
    },

    destroyed () {
      clearInterval(this.stocksInterval)
    }
  }
</script>
