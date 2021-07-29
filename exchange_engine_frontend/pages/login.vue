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
  methods: {
    loginUser (logininfo) {
      console.log(logininfo)
    }
  }
}
</script>

<style>
</style>
