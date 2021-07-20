<template>
  <v-row>
    <v-col cols="12">
      <Search />
    </v-col>
    <v-col cols="12">
      <h1 class="mb-5">
        Каталог акций
      </h1>
      <v-data-table
        :headers="headers"
        :items="listStoks"
        :page.sync="page"
        :items-per-page="itemsPerPage"
        hide-default-footer
        class="elevation-1"
        @page-count="pageCount = $event"
      >
        <template #body="{ items }">
          <tbody>
            <nuxt-link v-for="item in items" :key="item.name" :to="'/exchange/stocks/'+item.id" tag="tr">
              <td>
                <v-avatar class="mr-5" size="40">
                  <img
                    src="https://sun9-72.userapi.com/impf/afjNvm5m-xJpOwlsM3z40g-lWS5pmKRC7X-aag/3a3MVsH-O5I.jpg?size=300x300&quality=96&proxy=1&sign=062273059165b28df03875be67fa2b3a&type=album"
                    alt="John"
                  >
                </v-avatar>{{ item.name }}
              </td>
              <td>
                <div style="display: flex;flex-direction: column;justify-content: center; margin:10px;margin-left:0;">
                  <span> 1 084,12 ₮ </span>
                  <span class="green--text"> 1,42 %</span>
                </div>
              </td>
              <td> {{ item.price }} ₮ </td>
            </nuxt-link>
          </tbody>
        </template>
      </v-data-table>
      <div class="text-center pt-2">
        <v-pagination v-model="page" :length="pageCount" />
      </div>
    </v-col>
  </v-row>
</template>

<script>
import { listStoks } from '@/store/data'

export default {
  name: 'Exchange',
  components: {
    Search: () => import('@/components/exchange/Search')
  },
  data: () => ({
    page: 1,
    pageCount: 0,
    itemsPerPage: 10,
    headers: [{
      text: 'Название',
      align: 'start',
      value: 'name'
    },
    {
      text: 'Изменение за день',
      value: 'calories'
    },
    {
      text: 'Цена',
      value: 'price'
    }
    ],
    listStoks,
    desserts: [{
      name: 'Frozen Yogurt',
      calories: 159,
      fat: 6.0,
      carbs: 24,
      protein: 4.0,
      iron: '1%'
    },
    {
      name: 'Ice cream sandwich',
      calories: 237,
      fat: 9.0,
      carbs: 37,
      protein: 4.3,
      iron: '1%'
    },
    {
      name: 'Eclair',
      calories: 262,
      fat: 16.0,
      carbs: 23,
      protein: 6.0,
      iron: '7%'
    },
    {
      name: 'Cupcake',
      calories: 305,
      fat: 3.7,
      carbs: 67,
      protein: 4.3,
      iron: '8%'
    },
    {
      name: 'Gingerbread',
      calories: 356,
      fat: 16.0,
      carbs: 49,
      protein: 3.9,
      iron: '16%'
    },
    {
      name: 'Jelly bean',
      calories: 375,
      fat: 0.0,
      carbs: 94,
      protein: 0.0,
      iron: '0%'
    },
    {
      name: 'Lollipop',
      calories: 392,
      fat: 0.2,
      carbs: 98,
      protein: 0,
      iron: '2%'
    },
    {
      name: 'Honeycomb',
      calories: 408,
      fat: 3.2,
      carbs: 87,
      protein: 6.5,
      iron: '45%'
    },
    {
      name: 'Donut',
      calories: 452,
      fat: 25.0,
      carbs: 51,
      protein: 4.9,
      iron: '22%'
    },
    {
      name: 'KitKat',
      calories: 518,
      fat: 26.0,
      carbs: 65,
      protein: 7,
      iron: '6%'
    }
    ]
  })
}

</script>
