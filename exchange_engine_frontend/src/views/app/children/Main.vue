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
        <v-container>
          <v-btn-toggle
            v-model="selectedCandlesType"
            mandatory
          >
            <v-btn>
              1MIN
            </v-btn>
            <v-btn>
              5MIN
            </v-btn>
            <v-btn>
              15MIN
            </v-btn>
            <v-btn>
              30MIN
            </v-btn>
            <v-btn>
              60MIN
            </v-btn>
          </v-btn-toggle>
          <apexchart type="candlestick" :options="options" :series="series"></apexchart>
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
          Пожалуйста, выберите любую акцию из списка слева для просмотра ее информации
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
      selectedCandlesType: 0,
      selectedStonkID: undefined,
      limit_order: false,
      leverage_trade: false,
      price: 0,
      amount: 1,
      stocks: [],
      ratio: 0,
      item: '',
      stocksInterval: undefined,
      options: {
        chart: {
          id: 'main-chart',
          locales: [{
            "name": "ru",
            "options": {
              "months": ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"],
              "shortMonths": ["Янв", "Фев", "Мар", "Апр", "Май", "Июн", "Июл", "Авг", "Сен", "Окт", "Ноя", "Дек"],
              "days": ["Воскресенье", "Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"],
              "shortDays": ["Вс", "Пн", "Вт", "Ср", "Чт", "Пт", "Сб"],
              "toolbar": {
                  "exportToSVG": "Скачать SVG",
                  "exportToPNG": "Скачать PNG",
                  "menu": "Меню",
                  "selection": "Зона",
                  "selectionZoom": "Зона увелечения",
                  "zoomIn": "Увеличить",
                  "zoomOut": "Уменьшить",
                  "pan": "Переместить",
                  "reset": "Домой"
              }
            }
          }],
          defaultLocale: "ru",
          animations: {
            enabled: true,
            easing: 'easeinout',
            speed: 300,
            animateGradually: {
                enabled: true,
                delay: 100
            },
            dynamicAnimation: {
                enabled: true,
                speed: 100
            }
          },
          toolbar: {
            show: true,
            offsetX: 0,
            offsetY: 0,
            tools: {
              download: true,
              selection: true,
              zoom: true,
              zoomin: true,
              zoomout: true,
              pan: true,
              reset: true | '<img src="/static/icons/reset.png" width="20">',
              customIcons: []
            },
          }
        },
        xaxis: {
          type: 'datetime'
        },
        yaxis: {
          tooltip: {
            enabled: true
          }
        }
      },
      series: [{
        data: []
      }]
    }),

    watch: {
      selectedCandlesType: function () {
        this.getCandles()
      }
    },

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
      getCandles () {
        getAPI.get('http://127.0.0.1:8000/api/v1/candles/' + this.selectedStonkID + '/' + (this.selectedCandlesType + 1))
          .then(response => {
            let data = response.data.map(function(candle) {
              return [Date.parse(candle.date), [candle.open, candle.high, candle.low, candle.close].map((price) => (price.toFixed(2)))]
            })

            this.candlesInterval = setInterval(function() {
              this.getCandles()
            }.bind(this), 60000)

            this.series = [{
              data: data
            }]
          })
          .catch(err => {
            console.log(err)
          })
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
        this.getCandles()
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
      }.bind(this), 5000)
    },

    destroyed () {
      clearInterval(this.stocksInterval)
    }
  }
</script>
