<template>
  <v-row
    no-gutters
  >
    <v-col>
      <v-list 
        subheader
        two-line
      >
        <template v-for='(stock, index) in stocks'>
          <v-list-item
            :key='stock.id'
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
        </template>
      </v-list>
    </v-col>
    <v-col>
      <v-card
        class="pa-2"
        outlined
        tile
      >
        One of two columns
      </v-card>
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
          'is_active': false
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