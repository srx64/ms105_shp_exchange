<template>
  <div>
    <h1>Вход</h1>
    <Form :submit-form="loginUser" />
  </div>
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
