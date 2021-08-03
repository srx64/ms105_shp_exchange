<template>
  <div>
    <h1>Регистрация</h1>
    <Form :submit-form="registerUser" />
  </div>
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
