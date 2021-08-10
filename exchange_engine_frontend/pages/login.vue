<template>
  <v-main>
    <v-container style="height:100%;">
      <v-row style="height:100%;">
        <v-col cols="4" class="d-flex flex-column justify-center" style="height:100%;">
          <div class="d-flex flex-column" style="width:100%;">
            <h1>Вход</h1>
            <Form :submit-form="loginUser" />
            <p class="subtitle-1 mt-5 text-center">В первый раз тут? <NuxtLink to="/register">Зарегистрируйтесь</NuxtLink> за пару минут</p>
          </div>
        </v-col>
      </v-row>
    </v-container>
  </v-main>
</template>

<script>
export default {
  components: {
    Form: () => import('@/components/form/login.vue')
  },
  middleware: ['authenticated'],
  methods: {
    async loginUser (loginInfo) {
      try {
        await this.$auth.loginWith('local', {
          data: loginInfo
        })
        await this.$auth.fetchUser()
      } catch {
        console.log('error')
      }
    }
  }
}
</script>

<style>
</style>
