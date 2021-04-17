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
          <v-list-item
            v-for="stock in stocks"
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
            :key="index"
          ></v-divider>
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
      <div v-else>
        Hello
      </div>
    </v-col>
  </v-row>
</template>

<script>
  import { getAPI } from '../../../axios-api'
  import { mapState } from 'vuex'

  export default {
    name: 'App',

    data: () => ({
      username: '',
      email: '',
      balance: '',
      selectedItem: undefined,
      stocks: [
        {
          'id': 1,
          'name': 'OZON',
          'description': 'OZON',
          'is_active': true
        },
        {
          'id': 2,
          'name': 'AAPL',
          'description': 'Apple',
          'is_active': true
        },
        {
          'id': 3,
          'name': 'FB',
          'description': 'Facebook',
          'is_active': true
        },
        {
          'id': 4,
          'name': 'MSFT',
          'description': 'Microsoft',
          'is_active': true
        },
        {
          'id': 5,
          'name': 'TWTR',
          'description': 'Twitter',
          'is_active': true
        },
        {
          'id': 6,
          'name': 'OZON',
          'description': 'OZON',
          'is_active': true
        },
        {
          'id': 7,
          'name': 'AAPL',
          'description': 'Apple',
          'is_active': true
        },
        {
          'id': 8,
          'name': 'FB',
          'description': 'Facebook',
          'is_active': true
        },
        {
          'id': 9,
          'name': 'MSFT',
          'description': 'Microsoft',
          'is_active': true
        },
        {
          'id': 10,
          'name': 'TWTR',
          'description': 'Twitter',
          'is_active': true
        }
      ],
    }),

    computed: mapState(['APIData']),

    onIdle () {
      console.log('refresh')
      this.$store.dispatch('userRefresh')
    },

    methods: {
      getProfile () {
        getAPI.get('api/v1/profile/', {
            headers: { 
              Authorization: `Bearer ${this.$store.state.accessToken}` 
            } 
          })
          .then(response => {
            this.$store.state.APIData = response.data
            let profile = response.data.profile
            this.username = profile.username
            this.email = profile.email
            this.balance = profile.balance
          })
          .catch(err => {
            console.log(err)
          })
      }
    },

    mounted () {
      this.getProfile()
    }
  }
</script>