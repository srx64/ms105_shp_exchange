<template>
  <v-dialog v-model="dialog" persistent max-width="600px">
    <template #activator="{ on, attrs }">
      <v-btn block elevation="0" color="primary" v-bind="attrs" v-on="on">
        Купить
      </v-btn>
    </template>
    <v-card class="pt-0 pb-4">
      <v-card-title>
        <v-btn tile icon @click="dialog = false">
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-card-title>
      <v-card-text>
        <v-row>
          <v-col cols="12">
            <v-card eleva tion="0" outlined>
              <v-card-text class="pl-4 pr-4 pt-2 pb-2">
                <v-row no-gutters>
                  <v-col class="d-flex align-center text-caption text-sm-subtitle-1">
                    Баланс
                  </v-col>
                  <v-col class="d-flex align-center justify-end">
                    <p class="text-body-2 text-sm-subtitle-1 ma-0 text-no-wrap">
                      {{ $auth.user.balance | numeral('0,0.00') }} ₮
                    </p>
                  </v-col>
                </v-row>
              </v-card-text>
            </v-card>
          </v-col>
          <v-col cols="12">
            <v-card outlined class="">
              <v-card-text class="">
                <v-row no-gutters>
                  <v-col class="d-flex align-center">
                    <v-list-item-avatar class="ma-0 mr-5">
                      <v-icon class="grey lighten-1" dark>
                        mdi-note-text-outline
                      </v-icon>
                    </v-list-item-avatar>
                    <h1 class="text-subtitle-2 text-truncate">
                      {{ stock.name }}
                    </h1>
                  </v-col>
                  <v-col class="d-flex align-center justify-end text-center text-sm-end">
                    <p class="mt-5 mt-sm-0 text-caption text-sm-subtitle-1 ma-0 text-no-wrap">
                      Стоимость сейчас {{ stock.price | numeral('0,0.00') }}₮
                    </p>
                  </v-col>
                </v-row>
              </v-card-text>
            </v-card>
          </v-col>
          <v-col cols="12">
            <v-select v-model="select" :items="items" label="Тип заявки" outlined />
            <v-form v-if="select == 0">
              <v-text-field v-model="amount" type="number" min="1" outlined label="Колическво" />
            </v-form>
            <v-form v-if="select == 1">
              <v-text-field min="0" append-icon="₮" outlined label="Цена" />
              <v-text-field v-model="amount" type="number" min="1" outlined label="Колическво" />
            </v-form>
            <v-form v-if="select == 2">
              <v-text-field v-model="ratio" min="0" append-icon="₮" outlined label="Размер плеча" />
              <v-text-field v-model="amount" type="number" min="1" outlined label="Колическво" />
            </v-form>
          </v-col>

          <v-col>
            <v-btn block elevation="0" color="primary" text @click="trade()">
              Купить
            </v-btn>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  props: ['stock'],
  data: () => ({
    dialog: false,
    items: [{
      text: 'Лучшая цена',
      value: 0
    },
    {
      text: 'Отложенная заявка',
      value: 1
    },
    {
      text: 'Торговля с плечом',
      value: 2
    }
    ],
    select: 0,
    limit_order: false,
    price: 0,
    amount: 1,
    ratio: 0
  }),
  methods: {
    trade () {
      const urlTrade = this.select === 2 ? 'trading/leverage/' : 'orders/add'
      this.$axios.post(urlTrade, {
        stock: this.stock.name.toString(),
        type: 0,
        amount: this.amount,
        ratio: this.ratio,
        price: this.limit_order ? this.price : 0
      })
        .then((response) => {
          console.log(response)
        })
        .catch((err) => {
          console.log(err)
        })
      this.dialog = false
    }
  }
}
</script>

<style>

</style>
