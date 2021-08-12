<template>
  <div>
    <v-btn elevation="1" class="mb-6" outlined @click="swap()">
      Сменить тип графика
    </v-btn>
    <div v-if="select_chart === 1">
      <v-btn-toggle v-model="text">
        <v-btn value="left" outlined>
          <span class="hidden-sm-and-down">1m</span>
        </v-btn>

        <v-btn value="center" outlined>
          <span class="hidden-sm-and-down">5m</span>
        </v-btn>

        <v-btn value="right" outlined>
          <span class="hidden-sm-and-down">15m</span>
        </v-btn>

        <v-btn value="justify" outlined>
          <span class="hidden-sm-and-down">30m</span>
        </v-btn>
        <v-btn value="justify" outlined>
          <span class="hidden-sm-and-down">60м</span>
        </v-btn>
      </v-btn-toggle>
      <apexchart height="450" type="candlestick" :options="options" :series="series" />
    </div>
    <div v-else>
      <v-btn-toggle v-model="selection">
        <v-btn value="left" outlined @click="updateData('one_month')">
          <span class="hidden-sm-and-down">1m</span>
        </v-btn>

        <v-btn value="center" outlined @click="updateData('six_months')">
          <span class="hidden-sm-and-down">6M</span>
        </v-btn>

        <v-btn value="right" outlined @click="updateData('one_year')">
          <span class="hidden-sm-and-down">1Y</span>
        </v-btn>

        <v-btn value="justify" outlined @click="updateData('ytd')">
          <span class="hidden-sm-and-down">YTD</span>
        </v-btn>
        <v-btn value="justify" outlined @click="updateData('all')">
          <span class="hidden-sm-and-down">all</span>
        </v-btn>
      </v-btn-toggle>
      <div id="chart-timeline">
        <apexchart ref="chart" type="area" height="450" :options="chartOptions" :series="series2" />
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  data: () => ({
    select_chart: 1,
    selectedCandlesType: 0,
    stock: {
      name: 'JSi',
      price: 121212.121212
    },
    candlesInterval: undefined,
    model: '',
    dialog2: false,
    text: '',
    options: {
      chart: {
        id: 'main-chart',
        locales: [{
          name: 'ru',
          options: {
            months: ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль',
              'Август', 'Сентябрь',
              'Октябрь', 'Ноябрь', 'Декабрь'
            ],
            shortMonths: ['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн', 'Июл', 'Авг',
              'Сен', 'Окт', 'Ноя',
              'Дек'
            ],
            days: ['Воскресенье', 'Понедельник', 'Вторник', 'Среда', 'Четверг',
              'Пятница', 'Суббота'
            ],
            shortDays: ['Вс', 'Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб'],
            toolbar: {
              exportToSVG: 'Скачать SVG',
              exportToPNG: 'Скачать PNG',
              menu: 'Меню',
              selection: 'Зона',
              selectionZoom: 'Зона увелечения',
              zoomIn: 'Увеличить',
              zoomOut: 'Уменьшить',
              pan: 'Переместить',
              reset: 'Домой'
            }
          }
        }],
        defaultLocale: 'ru',
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
          show: false,
          autoSelected: 'pan',
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
          }
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
    stocks_portfolio: {
      aver_price: 12345.21333,
      count: 120,
      stock: {
        name: 'JSi',
        price: 123123.12444
      }
    },
    selection: 'one_year',
    chartOptions: {
      chart: {
        id: 'area-datetime',
        type: 'area',
        height: 350,
        zoom: {
          autoScaleYaxis: true
        },
        toolbar: {
          show: false,
          autoSelected: 'pan',
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
          }
        }
      },
      annotations: {
      },
      dataLabels: {
        enabled: false
      },
      markers: {
        size: 0,
        style: 'hollow'
      },
      xaxis: {
        type: 'datetime',
        tickAmount: 6
      },
      tooltip: {
        x: {
          format: 'dd MMM yyyy'
        }
      },
      fill: {
        type: 'gradient',
        gradient: {
          shadeIntensity: 1,
          opacityFrom: 0.0,
          opacityTo: 0.0,
          stops: [0, 100]
        }
      }
    }
  }),
  computed: {
    ...mapGetters({
      series: 'GET_CANDLES',
      series2: 'GET_LINE_GRAPH'
    })
  },
  methods: {
    swap () {
      if (this.select_chart === 1) {
        this.select_chart = 2
      } else {
        this.select_chart = 1
      }
    },
    updateData (timeline) {
      this.selection = timeline
      const d = new Date()
      switch (timeline) {
        case 'one_month':
          d.setHours(d.getHours() - 1)
          this.$refs.chart.zoomX(
            d.getTime(),
            new Date().getTime()
          )
          break
        case 'six_months':
          this.$refs.chart.zoomX(
            new Date('27 Sep 2012').getTime(),
            new Date('27 Feb 2013').getTime()
          )
          break
        case 'one_year':
          this.$refs.chart.zoomX(
            new Date('27 Feb 2012').getTime(),
            new Date('27 Feb 2013').getTime()
          )
          break
        case 'ytd':
          this.$refs.chart.zoomX(
            new Date('01 Jan 2013').getTime(),
            new Date('27 Feb 2013').getTime()
          )
          break
        case 'all':
          this.$refs.chart.zoomX(
            new Date('23 Jan 2012').getTime(),
            new Date('27 Feb 2013').getTime()
          )
          break
        default:
      }
    }
  }
}

</script>

<style>

</style>
