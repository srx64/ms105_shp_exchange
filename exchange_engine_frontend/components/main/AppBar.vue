<template>
  <v-app-bar
    id="home-app-bar"
    style="position: absolute;background: #FFFFFF;filter: drop-shadow(0px 4px 6px rgba(200, 200, 200, 0.25));"
    app
    dense
    flat
    height="80"
  >
    <v-row>
      <v-col cols="auto">
        <h1>SHP.EXchange</h1>
      </v-col>
      <v-col class="d-flex justify-center align-center">
        <v-btn to="/exchange" value="exchange" class="mx-2" exact text>
          <span>Биржа</span>

          <v-icon class="ml-1">
            mdi-finance
          </v-icon>
        </v-btn>
        <v-btn to="/exchange/portfolio" value="portfolio" class="mx-2" exact text>
          <span>Портфель</span>

          <v-icon class="ml-1">
            mdi-briefcase-account-outline
          </v-icon>
        </v-btn>
      </v-col>
      <v-col cols="auto">
        <v-badge color="green" content="6" overlap bordered>
          <v-avatar color="grey lighten-2" size="40">
            <v-icon dark>
              mdi-bell-outline
            </v-icon>
          </v-avatar>
        </v-badge>
        <v-menu offset-y>
          <template #activator="{ on, attrs }">
            <v-avatar v-bind="attrs" class="ml-4" color="primary" size="40" v-on="on" />
          </template>
          <v-list nav>
            <v-list-item-group v-model="selectedItem" color="primary">
              <v-list-item to="/user/setting">
                <v-list-item-title>Настройки</v-list-item-title>
              </v-list-item>
              <v-list-item>
                <v-list-item-title @click="$auth.logout()">
                  Выйти
                </v-list-item-title>
              </v-list-item>
            </v-list-item-group>
          </v-list>
        </v-menu>
      </v-col>
    </v-row>
  </v-app-bar>
</template>

<script>
export default {
  name: 'HomeAppBar',
  data: () => ({
    selectedItem: 0
  })
}

</script>
