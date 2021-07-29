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
    registerUser (registrationinfo) {
      console.log(registrationinfo)
    }
  }
}
</script>

<style>
</style>
