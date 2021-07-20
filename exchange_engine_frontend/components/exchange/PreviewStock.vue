<template>
  <nuxt-link tag="div" :to="'/exchange/stocks/'+stock.id" class="stock">
    <div class="stock-item">
      <h4>{{ stock.name }}</h4>
      <v-badge bordered color="error" icon="mdi-lock" overlap>
        <div class="stock-img">
          <img
            width="40px"
            src="https://www.comp-web-pro.ru/wp-content/uploads/2015/07/kak-udalitsya-iz-tvitera-navsegda.png"
            alt=""
          >
        </div>
      </v-badge>
    </div>
    <div class="stock-item">
      <div class="stock-text">
        <div style="white-space: nowrap;">
          За день
        </div>
        <div style="white-space: nowrap;">
          ↑ 1,42 %
        </div>
      </div>
      <v-sparkline :gradient="['#2ED954']" :line-width="3" :padding="15" :value="value" />
    </div>
  </nuxt-link>
</template>

<script>
const ll = {
  series: [{
    data: [25, 66, 41]
  }],
  chartOptions: {
    chart: {
      type: 'area',
      sparkline: {
        enabled: true
      }
    },
    series: [{
      data: [25, 66, 41, 59, 25, 44, 12, 36, 9, 21]
    }],
    stroke: {
      curve: 'smooth',
      width: 1
    },
    markers: {
      size: 0
    },
    colors: ['#FF3B30'],
    tooltip: {
      enabled: false
    },
    fill: {
      color: ['#FF3B30'],
      type: 'gradient',
      gradient: {
        shadeIntensity: 1,
        opacityFrom: 0.7,
        opacityTo: 0.6,
        stops: [0, 1000]
      }
    }
  }
}
export default {
  name: 'PreviewStock',
  props: ['stock'],
  data: () => ({
    ll,
    selectedGradient: ['#2ED954'],
    padding: 10,
    radius: 0,
    value: [0, 2, 5, 9, 5, 10, 3, 5, 0, 0, 1, 8, 2, 9, 0],
    width: 3
  })
}

</script>

<style scoped>
  .stock {
    width: 100%;
    height: 100%;
    background: #FFFFFF;
    box-shadow: 0px 0px 1px rgba(40, 41, 61, 0.08), 0px 0.5px 2px rgba(96, 97, 112, 0.16);
    border-radius: 5px;
    display: flex;
    flex-direction: column;
    justify-content: space-evenly;
    align-items: center;
    padding: 17px 21px 0 21px;
    transition: all 0.25s ease-in;
  }

  .stock:hover {
    cursor: pointer;
    transform: scale(1.015);
    box-shadow: 0px 0px 1px rgba(40, 41, 61, 0.08), 2px 5px 10px rgba(96, 97, 112, 0.16);
  }

  .stock-item {
    width: 100%;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-content: center;
    align-items: center;
  }

</style>
