<template>
  <header class="ex-navbar-wrapper">
    <div class="ex-navbar">
      <v-container style="height: 100%!important;display: flex;align-items: center;">
        <v-row style="width: 100%;">
          <v-col cols="auto" class="logo">
            SHP.EXchange
          </v-col>
          <v-col class="ex-nav">
            <nuxt-link to="/user/portfolio" class="ex-nav-item">
              Портфель
            </nuxt-link>
            <nuxt-link to="/exchange" class="ex-nav-item">
              Биржа
            </nuxt-link>
            <nuxt-link to="/ranking" class="ex-nav-item">
              Рейтинг
            </nuxt-link>
          </v-col>
          <v-col cols="auto" class="ex-nav-other">
            <div class="ex-nav-other-item">
              <v-icon>
                mdi-bell-outline
              </v-icon>
            </div>
            <nuxt-link class="ex-nav-other-item" to="/user/setting" style="text-decoration: none;">
              <v-icon>
                mdi-cog-outline
              </v-icon>
            </nuxt-link>
            <v-menu offset-y>
              <template #activator="{ on, attrs }">
                <div v-bind="attrs" class="ex-avatar" v-on="on">
                  <img :src="$auth.user.avatar" alt="">
                </div>
              </template>
              <v-list nav>
                <v-list-item-group color="primary">
                  <v-list-item disabled>
                    <v-list-item-title>Темная тема</v-list-item-title>
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
      </v-container>
    </div>
  </header>
</template>

<script>
export default {

}

</script>

<style>
  .ex-navbar-wrapper {
    height: 82px;
    width: 100%;
    display: flex;
    justify-content: center;
    position: relative;
  }

  .ex-navbar {
    width: 95%;
    height: 100%;
    background: #FFFFFF;
    box-shadow: 0px 4px 10px #E8F2FF;
    border-radius: 0px 0px 15px 15px;
  }

  .logo {
    font-family: 'Quantico', sans-serif;
    font-style: normal;
    font-weight: normal;
    font-size: 28px;
    line-height: 24px;
    /* identical to box height, or 86% */
    color: #000000;
    display: flex;
    align-items: center;
    text-align: center;
  }

  .ex-nav {
    display: flex;
    align-items: center;
  }

  .ex-nav .ex-nav-item {
    font-weight: 600;
    padding: 8px 14px 8px 14px;
    margin: 0 10px 0 10px;
    transition: all 0.3s;
    color: #000;
    text-decoration: none;
    border-radius: 5px;
    display: flex;
    align-items: center;
  }

  .ex-nav .ex-nav-item:hover {
    background-color: rgba(143, 143, 143, 0.137);
  }

  .ex-nav::after,
  .ex-nav::before {
    content: "";
    height: 80%;
    width: 2px;
    background-color: #d0d1d27c;
  }

  .ex-nav-other {
    display: flex;
    justify-content: flex-end;
    align-items: center;
  }

  .ex-nav-other-item {
    width: 40px;
    height: 40px;
    margin: 0 20px 0 0;
    display: flex;
    justify-content: center;
    align-items: center;
    transition: all 0.3s;
    border-radius: 9px;
  }

  .ex-nav-other-item:hover {
    background-color: rgba(143, 143, 143, 0.137);
  }

  .ex-avatar {
    margin: 0 !important;
    width: 50px;
    height: 50px;
    border: 1px solid #D9EAFF;
    border-radius: 16px;
    overflow: hidden;
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: center
  }

  .ex-avatar img {
    width: 60px;
    height: 60px;
    border: 2px solid #FFFFFF;
    box-sizing: border-box;
  }

</style>
