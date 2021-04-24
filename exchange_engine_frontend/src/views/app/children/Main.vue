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
          <v-text-field v-model="price" hint="" label="Цена" type="number"></v-text-field>
          <v-text-field v-model="amount" hint="" label="Количество" type="number"></v-text-field>
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
      price: 0,
      amount: 0,
      stocks: [],
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
        getAPI.post('orders/add', {
          stock: this.stocks[this.selectedItem].name.toString(),
          type: type,
          price: this.price,
          amount: this.amount,
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

    created () {
      this.getStocks()
    }
  }
</script>