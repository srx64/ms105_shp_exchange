<template>
  <v-main>
    <v-container>
      <v-row>
        <v-col cols="12">
          <Search />
        </v-col>
        <v-col cols="12">
          <h1 class="mb-5">
            Каталог акций
          </h1>
          <div v-if="listStoks.length == 0" style="display: flex;justify-content: center;margin-top:25px;height: 170px;align-items: center;">
            <v-progress-circular indeterminate color="primary" />
          </div>
          <div v-else>
            <v-data-table
              :headers="headers"
              :items="listStoks"
              :page.sync="page"

              hide-default-footer
              class="elevation-1"
              @page-count="pageCount = $event"
            >
              <template #body="{ items }">
                <tbody>
                  <nuxt-link v-for="item in items" :key="item.name" :to="'/exchange/сatalog/stocks/'+item.id" tag="tr">
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
          </div>
        </v-col>
      </v-row>
    </v-container>
  </v-main>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'Exchange',
  components: {
    Search: () => import('@/components/exchange/Search')
  },
  layout: 'app',
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
    ]
  }),
  computed: {
    ...mapGetters({
      listStoks: 'GET_EXchange_MAIN'
    })
  },
  created () {
    if (!this.$store.state.list_update) {
      this.$store.dispatch('FETCH_LIST_STOCKS')
    }
  }
}

</script>
