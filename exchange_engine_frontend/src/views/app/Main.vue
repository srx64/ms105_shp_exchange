<template>
  <div>

          <v-row>
        <v-col cols="12">
          <v-container fluid>
            <v-card>
              <v-row no-gutters align="stretch" justify="center">

                <v-col cols="6" align="center" class="black--text pa-4">
                          <v-list dense>
                            <v-subheader>Акции</v-subheader>
                            <v-list-item-group
                              v-model="selectedItem"
                              color="primary"
                            >
                              <v-list-item
                                v-for="(item, i) in stocks"
                                :key="i"
                              >
                                <v-list-item-content>
                                  <v-list-item-title v-text="item.name"></v-list-item-title>
                                </v-list-item-content>
                              </v-list-item>
                            </v-list-item-group>
                          </v-list>
                </v-col>

                <v-col cols="6" align="center">
                    <v-card class="pa-6">
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
                </v-col>



              </v-row>
            </v-card>
          </v-container>
        </v-col>
      </v-row>
  </div>
</template>

<script>
  import { getAPI } from '../../axios-api'
  import { mapState } from 'vuex'

  export default {
    name: 'App',

    data: () => ({
      username: '',
      email: '',
      balance: '',
      price: null,
      amount: null,
      stocks: null,
      selectedItem: 1,
    }),

    computed: mapState(['APIData']),

    onIdle () {
      console.log('refresh')
      this.$store.dispatch('userRefresh')
    },

    methods: {
      // getProfile () {
      //   getAPI.get('api/v1/profile/', {
      //       headers: { 
      //         Authorization: `Bearer ${this.$store.state.accessToken}` 
      //       } 
      //     })
      //     .then(response => {
      //       this.$store.state.APIData = response.data
      //       let profile = response.data.profile
      //       this.username = profile.username
      //       this.email = profile.email
      //       this.balance = profile.balance
      //     })
      //     .catch(err => {
      //       console.log(err)
      //     })
      // },
      getStocks(){
        getAPI.get('api/v1/stocks/', {
            headers: { 
              Authorization: `Bearer ${this.$store.state.accessToken}` 
            } 
          })
          .then(response => {
            this.stocks = response.data;
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
          })
          .catch(err => {
            console.log(err)
          })
      }
    },

    mounted () {
      this.getStocks()
    }
  }
</script>