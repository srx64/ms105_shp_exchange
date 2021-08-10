<template>
  <v-main>
    <v-container style="height:100%;">
      <v-row class="justify-end" style="height:100%;">
        <v-col cols="4" class="d-flex flex-column justify-center" style="height:100%;">
          <div class="d-flex flex-column" style="width:100%;">
            <h1>Регистрация</h1>
            <Form :submit-form="registerUser" />
            <p class="subtitle-1 mt-5 text-center">Уже зарегистрированны? <NuxtLink to="/login">Войдите</NuxtLink> в систему</p>
          </div>
        </v-col>
      </v-row>
    </v-container>
  </v-main>
</template>

<script>
export default {
  components: {
    Form: () => import('@/components/form/register.vue')
  },
  methods: {
    async registerUser (registrationinfo) {
      try {
        const resp = await this.$axios.post('/api/v1/register', {
          email: registrationinfo.email,
          username: registrationinfo.username,
          password: registrationinfo.password,
          password2: registrationinfo.repeatPassword
        })
        console.log(resp)
      } catch {
        console.log('error')
      }
    }
  }
}
</script>

<style>
</style>
